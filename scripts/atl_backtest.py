#!/usr/bin/env python3
"""Buy stocks at an all-time low when there is no company news? (Vamsi, Oct 15.)

Universe: a seeded random sample of US common stocks listed on Nasdaq or the NYSE today (SEC
company_tickers_exchange.json, one ticker per company; ETFs by Yahoo's instrument type, warrants, units, rights,
preferreds and SPAC shells dropped). Survivors only: stocks that hit their lows and were delisted are missing, so
every return here is biased upward, the all-time-low events more than the baseline (they are the likelier to die).
Event: a session whose close is under every earlier price in the stock's history (the earlier daily closes of the
last 10 years and every monthly low before them), with 3+ years of listed history, $1M+ average daily dollar volume
over the 20 sessions before and 20+ sessions since the stock's previous event. Company news: an SEC news-form filing
(news_dip_backtest.NEWS_FORMS: 8-K, 6-K, offerings, 10-Q, 10-K, ...) dated 7 days before to 1 day after the event;
news that never reaches EDGAR (downgrades, press stories, sector news) counts as none. Entry at the event's close;
exits at the close 5, 20, 60, 120 and 250 sessions later, after slippage by the unadjusted price (0.05% a side at
$20+, 0.2% at $5+, 0.5% at $1+, 1% under $1). Baseline: every 10th eligible session of the same stocks (same history
and volume filters). Excess = the return minus SPY's over the same sessions. Means +/- 95% clustered by calendar
month, each return capped at +300%.
  python scripts/atl_backtest.py [--n 1500] [--seed 7] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import statistics as st
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import marketdata as md  # noqa: E402
import news_dip_backtest as nd  # noqa: E402
import portfolio as pfm  # noqa: E402
import sec  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache" / "atl"
H = (5, 20, 60, 120, 250)
MIN_DV = 1e6
MIN_DAYS = 3 * 365
GAP = 20
CAP = 300.0
SKIP_END = ("W", "U", "R", "P", "Q")  # 5-letter Nasdaq suffixes: warrants, units, rights, preferreds, bankruptcy
CRASH = ("2020-02-15", "2020-04-30")


def universe(n: int, seed: int) -> tuple[list[str], int]:
    f = CACHE / "universe.json"
    if f.exists() and time.time() - f.stat().st_mtime < 7 * 86400:
        data = json.loads(f.read_text())
    else:
        data = json.loads(sec.get("https://www.sec.gov/files/company_tickers_exchange.json"))
        CACHE.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(data))
    fi = {k: i for i, k in enumerate(data["fields"])}
    seen, out = set(), []
    for row in data["data"]:
        t, ex, name, cik = row[fi["ticker"]], row[fi["exchange"]], row[fi["name"]] or "", row[fi["cik"]]
        if ex not in ("Nasdaq", "NYSE") or not t or "-" in t or "." in t or cik in seen:
            continue
        if (len(t) == 5 and t[-1] in SKIP_END) or "acquisition" in name.lower():
            continue
        seen.add(cik)
        out.append(t.upper())
    out.sort()
    return random.Random(seed).sample(out, min(n, len(out))), len(out)


def chart(sym: str, rng: str, interval: str) -> dict | None:
    f = CACHE / f"{sym}_{rng}_{interval}.json"
    if f.exists() and time.time() - f.stat().st_mtime < 86400:
        return json.loads(f.read_text()) or None
    s, res = urllib.parse.quote(sym), None
    for attempt in range(4):
        host = "query1" if attempt % 2 == 0 else "query2"
        try:
            j = md.http_json(f"https://{host}.finance.yahoo.com/v8/finance/chart/{s}?range={rng}&interval={interval}"
                             f"&events=split&includePrePost=false", timeout=20)
            res = ((j.get("chart") or {}).get("result") or [None])[0]
            break
        except Exception as e:  # noqa: BLE001
            if "404" in str(e):
                break
            time.sleep(1.5 * (attempt + 1))
    else:
        return None
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(res or {}))
    return res


def bars(r: dict) -> list[tuple]:
    q = ((r.get("indicators") or {}).get("quote") or [{}])[0]
    ts, off = r.get("timestamp") or [], (r.get("meta") or {}).get("gmtoffset") or 0
    out = []
    for i, t in enumerate(ts):
        h, lo, c, v = (q.get(k, [None] * len(ts))[i] for k in ("high", "low", "close", "volume"))
        if None in (h, lo, c) or c <= 0 or lo <= 0:
            continue
        out.append((dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat(), h, lo, c, v or 0))
    return out


def splits(*rs: dict | None) -> list[tuple[str, float]]:
    out = {}
    for r in rs:
        off = ((r or {}).get("meta") or {}).get("gmtoffset") or 0
        for s in (((r or {}).get("events") or {}).get("splits") or {}).values():
            if s.get("numerator") and s.get("denominator"):
                d = dt.datetime.fromtimestamp(s["date"] + off, dt.timezone.utc).date().isoformat()
                out[d] = s["numerator"] / s["denominator"]
    return sorted(out.items())


def slip(raw: float) -> float:
    return 0.0005 if raw >= 20 else 0.002 if raw >= 5 else 0.005 if raw >= 1 else 0.01


def bucket(raw: float) -> str:
    return "$5+" if raw >= 5 else "$1-5" if raw >= 1 else "under $1"


def analyse(sym: str, spy: dict[str, float]) -> dict | None:
    d = chart(sym, "10y", "1d")
    if not d or (d.get("meta") or {}).get("instrumentType") != "EQUITY":
        return None
    rows = bars(d)
    if len(rows) < 300:
        return None
    m = chart(sym, "max", "1mo")
    mrows = bars(m) if m else []
    first = min([rows[0][0]] + [x[0] for x in mrows[:1]])
    start_month = rows[0][0][:8] + "01"
    pre = [x[2] for x in mrows if x[0] < start_month]
    pre_min = min(pre) if pre else float("inf")
    sp = splits(d, m)
    fac, acc, k = [1.0] * len(rows), 1.0, len(sp) - 1
    for i in range(len(rows) - 1, -1, -1):
        while k >= 0 and sp[k][0] > rows[i][0]:
            acc *= sp[k][1]
            k -= 1
        fac[i] = acc
    first_d = dt.date.fromisoformat(first)
    events, base, run_min, last = [], [], pre_min, -GAP
    dv = [r[3] * r[4] for r in rows]
    for i in range(len(rows)):
        c = rows[i][3]
        is_low = c < run_min
        run_min = min(run_min, c)
        if i < 20 or (dt.date.fromisoformat(rows[i][0]) - first_d).days < MIN_DAYS or sum(dv[i - 20:i]) / 20 < MIN_DV:
            continue
        low_event = is_low and i - last >= GAP
        if i % 10 and not low_event:
            continue
        raw = c * fac[i]
        fwd = {}
        for h in H:
            j = i + h
            if j < len(rows):
                x = rows[j][3]
                r = (x * (1 - slip(x * fac[j])) / (c * (1 + slip(raw))) - 1) * 100
                s0, s1 = spy.get(rows[i][0]), spy.get(rows[j][0])
                fwd[h] = (r, r - (s1 / s0 - 1) * 100 if s0 and s1 else None)
        nxt = rows[i + 1:i + 61]
        until = (dt.date.fromisoformat(rows[i][0]) + dt.timedelta(days=730)).isoformat()
        rec = {"sym": sym, "date": rows[i][0], "raw": raw, "bucket": bucket(raw), "fwd": fwd,
               "dd60": (min(x[2] for x in nxt) / c - 1) * 100 if len(nxt) == 60 else None,
               "lower60": (min(x[3] for x in nxt) < c) if len(nxt) == 60 else None,
               "rsplit": any(rows[i][0] < s_d <= until and ratio < 1 for s_d, ratio in sp)}
        if i % 10 == 0:
            base.append(rec)
        if low_event:
            last = i
            events.append({**rec, "spy_day": (spy[rows[i][0]] / spy[rows[i - 1][0]] - 1) * 100
                           if rows[i][0] in spy and rows[i - 1][0] in spy else None})
    return {"sym": sym, "events": events, "base": base}


def tag_news(evs: list[dict]) -> None:
    syms = sorted({e["sym"] for e in evs})

    def one(s: str) -> tuple[str, dict | None]:
        try:
            return s, nd.news_dates(s, "2015-06-01")
        except Exception as ex:  # noqa: BLE001
            print(f"  {s}: SEC {str(ex)[:60]}", file=sys.stderr)
            return s, None
    with ThreadPoolExecutor(4) as ex:
        news = dict(ex.map(one, syms))
    for e in evs:
        n = news.get(e["sym"])
        if n is None:
            e["news"] = None
            continue
        d0 = dt.date.fromisoformat(e["date"])
        kinds = {k for i in range(-7, 2) for k in n.get((d0 + dt.timedelta(days=i)).isoformat(), [])}
        e["news"], e["kinds"] = bool(kinds), sorted(kinds)


def cell(g: list[dict], h: int, ex: bool = False) -> str:
    xs = [(r["date"][:7], min(CAP, r["fwd"][h][1 if ex else 0])) for r in g
          if h in r["fwd"] and r["fwd"][h][1 if ex else 0] is not None]
    if len(xs) < 20:
        return "-"
    m, se = cb.clustered(xs)
    return f"{m:+.1f} ± {1.96 * se:.1f}"


def stats(g: list[dict], h: int) -> dict:
    xs = [r["fwd"][h] for r in g if h in r["fwd"]]
    if not xs:
        return {}
    return {"n": len(xs), "median": st.median(x[0] for x in xs), "up": sum(x[0] > 0 for x in xs) / len(xs) * 100,
            "beat": sum(1 for x in xs if x[1] is not None and x[1] > 0) / len(xs) * 100}


def report(groups: list[tuple[str, list[dict]]], meta: dict) -> str:
    out = [f"# All-time lows with and without company news ({meta['date']})", "",
           f"{meta['fetched']:,} of a {meta['n']:,}-stock random sample (seed {meta['seed']}) of the "
           f"{meta['pool']:,} US common stocks listed on Nasdaq or the NYSE today; daily bars for the last 10 years, "
           f"monthly before. {meta['eligible']:,} stocks had eligible sessions. Method: the `scripts/atl_backtest.py` "
           f"docstring. Survivors only, so the event returns are biased upward.", "",
           "**Return after buying at the close, % (mean ± 95%, capped at +300%)**", "",
           "| Group | Events | " + " | ".join(f"{h} sessions" for h in H) + " |",
           "|---|---:|" + "---:|" * len(H)]
    for name, g in groups:
        out.append(f"| {name} | {len(g):,} | " + " | ".join(cell(g, h) for h in H) + " |")
    out += ["", "**Against SPY over the same sessions, % (mean ± 95%), and the typical case**", "",
            "| Group | 20 vs SPY | 60 vs SPY | 250 vs SPY | 60 median | 60 up | 60 beat SPY | 250 median | 250 up | "
            "250 beat SPY | Lower close within 60 | Fell 20%+ more within 60 | Reverse split within 2 years |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name, g in groups:
        s60, s250 = stats(g, 60), stats(g, 250)
        ev = [r for r in g if r.get("lower60") is not None]
        low = f"{sum(r['lower60'] for r in ev) / len(ev) * 100:.0f}%" if ev else ""
        fell = f"{sum(r['dd60'] <= -20 for r in ev) / len(ev) * 100:.0f}%" if ev else ""
        rs = [r for r in g if "rsplit" in r]
        rsp = f"{sum(r['rsplit'] for r in rs) / len(rs) * 100:.0f}%" if rs else ""
        f = lambda s, k, p="%": f"{s[k]:+.1f}" if k == "median" and s else (f"{s[k]:.0f}{p}" if s else "-")  # noqa: E731
        out.append(f"| {name} | {cell(g, 20, True)} | {cell(g, 60, True)} | {cell(g, 250, True)} | {f(s60, 'median')} | "
                   f"{f(s60, 'up')} | {f(s60, 'beat')} | {f(s250, 'median')} | {f(s250, 'up')} | {f(s250, 'beat')} | "
                   f"{low} | {fell} | {rsp} |")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms, pool = universe(a.n, a.seed)
    sd = chart("SPY", "10y", "1d")
    spy = {r[0]: r[3] for r in bars(sd)}
    t0 = time.time()
    with ThreadPoolExecutor(8) as ex:
        res = [r for r in ex.map(lambda s: analyse(s, spy), syms) if r]
    print(f"fetched {len(res)} of {len(syms)} in {time.time() - t0:.0f}s", file=sys.stderr)
    evs = [e for r in res for e in r["events"]]
    base = [b for r in res for b in r["base"]]
    tag_news(evs)
    known = [e for e in evs if e.get("news") is not None]
    quiet = [e for e in known if not e["news"]]
    loud = [e for e in known if e["news"]]
    firsts = {}
    for e in sorted(quiet, key=lambda x: x["date"]):
        firsts.setdefault(e["sym"], e)
    groups = [("Baseline: every eligible session", base),
              ("All all-time lows", evs),
              ("No company news", quiet),
              ("Company news", loud),
              ("  news: offering", [e for e in loud if "offering" in e["kinds"]]),
              ("  news: results", [e for e in loud if "results" in e["kinds"]]),
              ("  news: other only", [e for e in loud if e["kinds"] == ["other"]]),
              ("No news, first low per stock", list(firsts.values())),
              ("No news, SPY down 1%+ that day", [e for e in quiet if (e["spy_day"] or 0) <= -1]),
              ("No news, SPY not down 1%", [e for e in quiet if (e["spy_day"] or 0) > -1]),
              ("No news, outside Feb 15-Apr 30 2020", [e for e in quiet if not CRASH[0] <= e["date"] <= CRASH[1]])]
    for b in ("$5+", "$1-5", "under $1"):
        groups.append((f"No news, price {b}", [e for e in quiet if e["bucket"] == b]))
        groups.append((f"  baseline, price {b}", [x for x in base if x["bucket"] == b]))
    meta = {"date": dt.date.today().isoformat(), "n": len(syms), "seed": a.seed, "pool": pool, "fetched": len(res),
            "eligible": sum(1 for r in res if r["base"]), "events": len(evs), "news_unknown": len(evs) - len(known)}
    text = report(groups, meta)
    print(text)
    print(json.dumps(meta), file=sys.stderr)
    if a.save:
        out = ROOT / "research" / "backtests" / f"atl-{meta['date']}"
        out.with_suffix(".md").write_text(text)
        out.with_suffix(".json").write_text(json.dumps({"meta": meta, "events": evs}, default=str))
        print(f"saved {out}.md/json", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
