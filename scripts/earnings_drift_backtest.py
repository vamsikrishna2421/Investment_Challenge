#!/usr/bin/env python3
"""Post-earnings drift (Oct 10, from the research on AI in trading: the measured edge of AI is reading text, earnings
releases above all, and the published LLM results trade the drift after the news, strongest in small stocks; Q3
earnings fall inside the challenge window). Does a stock keep moving the way its earnings reaction went?
Events: each candidate's 8-K filings with item 2.02 (results of operations) over 5 years, from SEC EDGAR; the
reaction day is the filing's session (accepted before 16:00 ET) or the next one (after the close); 2.02 filings
within 5 sessions of an earlier one (preliminary results, then the release) count once. The reaction is the move
from the prior close to the reaction day's close, in ATR units (14 sessions before), with the close's place in the
day's range. Bought at the reaction day's close (the 15:55 run can do this) and sold at the close 1, 3, 5 and 10
sessions later; returns % after trade.py-style slippage, means +/- 95% clustered by date. Baseline: every close of
the same names, held as long. Halves of the dates are shown apart for the 5-session edge.
  python scripts/earnings_drift_backtest.py [--tickers A,B | --large-caps] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import candle_backtest as cdl  # noqa: E402
import clue_backtest as cb  # noqa: E402
import levels as lv  # noqa: E402
import news_dip_backtest as nd  # noqa: E402
import portfolio as pfm  # noqa: E402
import sec  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache" / "sec_news"
HOLDS = (1, 3, 5, 10)
BUCKETS = [("up 2+ ATR", 2, 99), ("up 1-2 ATR", 1, 2), ("within 1 ATR", -1, 1), ("down 1-2 ATR", -2, -1),
           ("down 2+ ATR", -99, -2)]


def earnings_times(sym: str, start: str) -> list[dt.datetime]:
    """Acceptance times (ET) of the ticker's 8-K item 2.02 filings since start, cached for a day."""
    f = CACHE / f"{sym}.e202.json"
    if f.exists() and (dt.datetime.now().timestamp() - f.stat().st_mtime) < 86400:
        return [dt.datetime.fromisoformat(x) for x in json.loads(f.read_text())]
    t = sec.tickers()["by_ticker"]
    cik = t.get(sym.upper().replace("-", ".")) or t.get(sym.upper())
    if not cik:
        return []
    out: list[str] = []

    def take(rec: dict) -> None:
        for fm, it, acc in zip(rec.get("form", []), rec.get("items", []), rec.get("acceptanceDateTime", [])):
            if fm in ("8-K", "8-K/A") and "2.02" in (it or "") and fm == "8-K":
                ts = dt.datetime.fromisoformat(acc.replace("Z", "+00:00")).astimezone(pfm.ET)
                if ts.date().isoformat() >= start:
                    out.append(ts.replace(tzinfo=None).isoformat())

    sub = json.loads(sec.get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))
    take(sub.get("filings", {}).get("recent", {}))
    for page in sub.get("filings", {}).get("files", []):
        if page.get("filingTo", "") >= start:
            take(json.loads(sec.get("https://data.sec.gov/submissions/" + page["name"])))
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(sorted(set(out))))
    return [dt.datetime.fromisoformat(x) for x in sorted(set(out))]


def events(sym: str) -> tuple[list[dict], list[dict]]:
    rows = sb.daily(sym, "5y")
    if not rows or len(rows) < 120:
        return [], []
    dates = [nd.day(r) for r in rows]
    idx = {d: i for i, d in enumerate(dates)}
    try:
        times = earnings_times(sym, dates[0])
    except Exception as e:  # noqa: BLE001
        print(f"  {sym}: EDGAR {str(e)[:60]}", file=sys.stderr)
        return [], []
    base = []
    for i in range(20, len(rows) - max(HOLDS)):
        e = rows[i]["c"]
        base.append({"date": dates[i], **{f"d{h}": nd.ret(e, rows[i + h]["c"]) for h in HOLDS}})
    out, last = [], -99
    for ts in times:
        d = ts.date().isoformat()
        after = ts.hour * 60 + ts.minute >= 16 * 60
        # the first session on or after the filing date, one more when filed after the close
        r = next((k for k in range(len(dates)) if dates[k] >= d), None)
        if r is None:
            continue
        if after and dates[r] == d:
            r += 1
        if r - last <= 5:
            continue
        last = r
        if r < 20 or r + max(HOLDS) >= len(rows):
            continue
        a = lv.atr(rows[r - 15:r])
        pc, c, h, lo, o = rows[r - 1]["c"], rows[r]["c"], rows[r]["h"], rows[r]["l"], rows[r]["o"]
        if not a or not pc:
            continue
        ev = {"sym": sym, "date": dates[r], "react_atr": (c - pc) / a, "react_pct": (c / pc - 1) * 100,
              "gap_atr": (o - pc) / a, "close_pos": (c - lo) / (h - lo) if h > lo else 0.5,
              **{f"d{k}": nd.ret(c, rows[r + k]["c"]) for k in HOLDS}}
        # the 5-session hold with a stop 1 ATR under the entry (a gap through it fills at the open)
        stop, x = c - a, None
        for k in range(1, 6):
            if rows[r + k]["l"] <= stop:
                x = min(rows[r + k]["o"], stop)
                break
        ev["d5_stop"] = nd.ret(c, x if x is not None else rows[r + 5]["c"])
        ev["stopped"] = x is not None
        out.append(ev)
    return out, base


def stats(rows: list[dict], split: str) -> dict:
    s = {"n": len(rows)}
    for h in HOLDS:
        xs = [(r["date"], r[f"d{h}"]) for r in rows]
        if not xs:
            continue
        m, se = cb.clustered(xs)
        s[f"d{h}"] = (round(m, 2), round(1.96 * se, 2) if not math.isnan(se) else None)
        s[f"up{h}"] = round(100 * sum(v > 0 for _, v in xs) / len(xs))
    if rows:
        v = sorted(r["d5"] for r in rows)
        s["med5"] = round(v[len(v) // 2], 2)
    if rows and "d5_stop" in rows[0]:
        m, se = cb.clustered([(r["date"], r["d5_stop"]) for r in rows])
        s["d5_stop"] = (round(m, 2), round(1.96 * se, 2) if not math.isnan(se) else None)
        s["stopped"] = round(100 * sum(r["stopped"] for r in rows) / len(rows))
    for half, sel in (("a", [r for r in rows if r["date"] < split]), ("b", [r for r in rows if r["date"] >= split])):
        s[f"d5{half}"] = round(cb.clustered([(r["date"], r["d5"]) for r in sel])[0], 2) if sel else None
    return s


def report(res: dict) -> str:
    b = res["baseline"]
    lines = [f"# Post-earnings drift, {res['asof']}", "",
             f"{res['names']} {res['universe']}, {res['events']} earnings reactions (8-K item 2.02), {res['first']} to "
             f"{res['last']}; method in the `scripts/earnings_drift_backtest.py` docstring. Bought at the reaction "
             f"day's close; returns % after slippage, ± 95% clustered by date; 'up' is the share above zero. Edge = "
             f"bucket minus baseline; the 5-session edge also for each half of the dates (split {res['split']}).", "",
             "| reaction | n | +1 day | +3 days | +5 days | median (5) | up (5) | +10 days | edge 5 | edge 5 by half | "
             "edge 10 | +5 days, stop 1 ATR under (stopped) |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|"]

    def c(s, k):
        v = s.get(k)
        return f"{v[0]:+.2f} ± {v[1]:.2f}" if v and v[1] is not None else "-"

    def e(s, k):
        return f"{s[k][0] - b[k][0]:+.2f}" if s.get(k) and b.get(k) else "-"

    def hv(s):
        if s.get("d5a") is None or s.get("d5b") is None:
            return "-"
        return f"{s['d5a'] - b['d5a']:+.2f} / {s['d5b'] - b['d5b']:+.2f}"

    for name, s in [("baseline (every close)", b), ("all earnings reactions", res["all"])] + list(res["buckets"].items()):
        stop = f"{c(s, 'd5_stop')} ({s['stopped']}%)" if s.get("d5_stop") else "-"
        lines.append(f"| {name} | {s['n']} | {c(s, 'd1')} | {c(s, 'd3')} | {c(s, 'd5')} | {s.get('med5', '-')} | "
                     f"{s.get('up5', '-')}% | {c(s, 'd10')} | {e(s, 'd5')} | {hv(s)} | {e(s, 'd10')} | {stop} |")
    lines += ["", "## Reading", ""] + res.get("reading", [])
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tickers", help="comma list (default: the radar candidates)")
    ap.add_argument("--large-caps", action="store_true", help="the 60 largest US stocks (no index funds)")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    if not sec.enabled():
        print("no SEC contact configured (.secrets/sec_contact)", file=sys.stderr)
        return 1
    syms = [t.strip().upper() for t in a.tickers.split(",")] if a.tickers else \
        [t for t in cdl.LARGE if t not in ("SPY", "QQQ")] if a.large_caps else list(lv.CANDIDATES)
    with ThreadPoolExecutor(4) as ex:
        got = list(ex.map(events, syms))
    evs = [x for e_, _ in got for x in e_]
    base = [x for _, b_ in got for x in b_]
    ds = sorted({r["date"] for r in base})
    split = ds[len(ds) // 2]
    buckets = {}
    for name, lo, hi in BUCKETS:
        buckets[name] = stats([x for x in evs if lo <= x["react_atr"] < hi], split)
    buckets["down 1+ ATR (both down buckets)"] = stats([x for x in evs if x["react_atr"] < -1], split)
    buckets["up 1+ ATR, closed in the top quarter"] = stats(
        [x for x in evs if x["react_atr"] >= 1 and x["close_pos"] >= 0.75], split)
    buckets["down 1+ ATR, closed in the bottom quarter"] = stats(
        [x for x in evs if x["react_atr"] <= -1 and x["close_pos"] <= 0.25], split)
    buckets["gapped down 1+ ATR, closed up from the open"] = stats(
        [x for x in evs if x["gap_atr"] <= -1 and x["react_atr"] > x["gap_atr"] + 0.5], split)
    res = {"asof": dt.date.today().isoformat(),
           "universe": "large caps (60 largest US stocks)" if a.large_caps and not a.tickers else
           "names" if a.tickers else "radar candidates",
           "names": sum(1 for b_ in got if b_[1]), "events": len(evs), "first": ds[0], "last": ds[-1], "split": split,
           "baseline": stats(base, split), "all": stats(evs, split), "buckets": buckets}
    text = report(res)
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests" / f"earnings-drift-{res['asof']}{'-large' if a.large_caps else ''}"
        out.with_suffix(".json").write_text(json.dumps(res, indent=2) + "\n")
        out.with_suffix(".md").write_text(text)
        print(f"saved {out.with_suffix('.md').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
