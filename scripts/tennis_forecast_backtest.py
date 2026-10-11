#!/usr/bin/env python3
"""Tennis forecast strategy on Kalshi (Oct 11: Vamsi asked for a backtest of my two prediction-market ideas from the
swing tests, a forecast better than the market's price and limit orders instead of paying the spread, then for the
competitions where the forecasts work best and the average monthly profit rate from $1,000).
Data: Kalshi's public settled match markets (ATP, WTA, ATP and WTA Challengers, ITF men and women; the historical
endpoint before its cutoff), cached in .cache/kalshi_tennis. Each match is an event of two markets, one per player,
with a stable competitor id.
  forecast  an Elo rating per player from every settled Kalshi match (men and women apart, all levels pooled;
            K = 250 / (matches + 5)^0.4, FiveThirtyEight's tennis form), using only matches settled before the entry
  entry     the hourly quote ENTRY_H hours before the market closed (a match ends at the close, so this is before
            play for nearly every match): buy the player at the ask (or the opponent at 1 - bid) when the forecast
            exceeds that cost plus fees by the margin; both players rated in 10+ earlier matches; spread 10 cents max
  limit     the same signal as a resting buy 1 cent over the bid, filled only if a trade prints 1 cent through it
            between the entry and 3 hours before the close (fills come when the price falls: adverse selection kept)
  fees      Robinhood's 1 cent a contract; Kalshi's taker fee 0.07 x p x (1 - p), maker 0.0175 x p x (1 - p)
  bankroll  $1,000, each bet 2% of the bankroll when placed, settled at the result; calendar months
  narrowing walk-forward: in each month, bet only in the competitions whose bets made money over the prior two
            months (10+ bets), against hindsight (the competitions that made money over the whole test)
  check     the forecast against the market's own mid price as forecasts (log loss), and the matches where they
            disagree most
  python scripts/tennis_forecast_backtest.py [--per 120] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import statistics as st
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import favorites_backtest as fb  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache" / "kalshi_tennis"
SERIES = {"KXATPMATCH": ("ATP tour", "men"), "KXWTAMATCH": ("WTA tour", "women"),
          "KXATPCHALLENGERMATCH": ("ATP Challenger", "men"), "KXWTACHALLENGERMATCH": ("WTA Challenger", "women"),
          "KXITFMATCH": ("ITF men", "men"), "KXITFWMATCH": ("ITF women", "women")}
ENTRY_H, FILL_UNTIL_H, MAX_SPREAD, MIN_N, STAKE = 6, 3, 0.10, 10, 0.02
PACE = 0.1  # seconds between requests (Kalshi allows about 20 reads a second; 429s back off)
MARGINS = (0.0, 0.03, 0.05, 0.10)


def get(path: str) -> dict:
    """A Kalshi request at PACE, with patience for the rate limit (HTTP 429: waits 5 s,
    doubling up to a minute) and none for a missing page (HTTP 404 raises at once)."""
    for attempt in range(8):
        with fb._lock:
            wait = PACE - (time.time() - fb._last[0])
            if wait > 0:
                time.sleep(wait)
            fb._last[0] = time.time()
        try:
            req = urllib.request.Request(fb.BASE + path, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as ex:
            if ex.code == 404 or attempt == 7:
                raise
            time.sleep(min(60, 5 * 2 ** attempt) if ex.code == 429 else 2)
        except Exception:  # noqa: BLE001
            if attempt == 7:
                raise
            time.sleep(2)
    return {}


_CUT: list = []


def cutoff() -> int:
    """Markets settled before this time are served by Kalshi's historical endpoints."""
    if not _CUT:
        _CUT.append(fb.ts(get("/historical/cutoff")["market_settled_ts"]))
    return _CUT[0]


def taker(p: float) -> float:
    return 0.01 + 0.07 * p * (1 - p)


def maker(p: float) -> float:
    return 0.01 + 0.0175 * p * (1 - p)


def markets(series: str) -> list[dict]:
    """Every settled market of the series (historical endpoint plus the recent one), cached for a day."""
    f = CACHE / f"markets-{series}.json"
    if f.exists() and time.time() - f.stat().st_mtime < 86400:
        return json.loads(f.read_text())
    out = []
    for base in (f"/historical/markets?series_ticker={series}&limit=1000",
                 f"/markets?series_ticker={series}&status=settled&limit=1000"):
        cursor = ""
        for _ in range(400):
            r = get(base + (f"&cursor={cursor}" if cursor else ""))
            out += [{k: m.get(k) for k in ("ticker", "event_ticker", "result", "close_time", "open_time", "title",
                                           "yes_sub_title", "custom_strike", "volume_fp")} for m in r.get("markets", [])]
            cursor = r.get("cursor") or ""
            if not cursor or not r.get("markets"):
                break
            time.sleep(1.0)
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(out))
    return out


def events() -> list[dict]:
    """Clean two-player matches: two markets, one won, two competitor ids; oldest first."""
    out = []
    for s, (comp, pool) in SERIES.items():
        by = defaultdict(list)
        for m in markets(s):
            by[m["event_ticker"]].append(m)
        for ev, ms in by.items():
            if len(ms) != 2 or sorted(m["result"] for m in ms) != ["no", "yes"]:
                continue
            ms.sort(key=lambda m: m["ticker"])
            ids = [(m.get("custom_strike") or {}).get("tennis_competitor") for m in ms]
            if None in ids or ids[0] == ids[1]:
                continue
            out.append({"event": ev, "series": s, "comp": comp, "pool": pool, "close": fb.ts(ms[0]["close_time"]),
                        "a": ids[0], "b": ids[1], "a_name": ms[0]["yes_sub_title"], "b_name": ms[1]["yes_sub_title"],
                        "ticker": ms[0]["ticker"], "a_won": ms[0]["result"] == "yes",
                        "qual": "Qualification" in (ms[0].get("title") or "")})
    out.sort(key=lambda e: e["close"])
    return out


def elo(evs: list[dict]) -> None:
    """Adds each match's pre-entry forecast for player a and both players' match counts, from the matches settled
    before the entry (ENTRY_H hours before this market's close)."""
    rating: dict[str, float] = defaultdict(lambda: 1500.0)
    n: dict[str, int] = defaultdict(int)
    j = 0
    for e in evs:
        t = e["close"] - ENTRY_H * 3600
        while j < len(evs) and evs[j]["close"] <= t:
            x = evs[j]
            ka, kb = (x["pool"], x["a"]), (x["pool"], x["b"])
            pa = 1 / (1 + 10 ** ((rating[kb] - rating[ka]) / 400))
            sa = 1.0 if x["a_won"] else 0.0
            rating[ka] += 250 / (n[ka] + 5) ** 0.4 * (sa - pa)
            rating[kb] += 250 / (n[kb] + 5) ** 0.4 * (pa - sa)
            n[ka] += 1
            n[kb] += 1
            j += 1
        ka, kb = (e["pool"], e["a"]), (e["pool"], e["b"])
        e["p"] = 1 / (1 + 10 ** ((rating[kb] - rating[ka]) / 400))
        e["na"], e["nb"] = n[ka], n[kb]


def quotes(e: dict) -> dict | None:
    """The yes bid and ask of player a's market at the entry, and the lowest and highest trades from then until
    FILL_UNTIL_H hours before the close, from hourly candles (cached)."""
    f = CACHE / "candles" / f"{e['ticker']}.json"
    if f.exists():
        cs = json.loads(f.read_text())
    else:
        q = f"?start_ts={e['close'] - 72 * 3600}&end_ts={e['close']}&period_interval=60"
        live = (f"/series/{e['series']}/markets/{e['ticker']}/candlesticks" + q, "_dollars")
        hist = (f"/historical/markets/{e['ticker']}/candlesticks" + q, "")
        first, second = (hist, live) if e["close"] < cutoff() else (live, hist)
        try:
            r, sfx = get(first[0]), first[1]
        except urllib.error.HTTPError as ex:  # the other endpoint when the market is not where expected
            if ex.code != 404:
                raise
            r, sfx = get(second[0]), second[1]
        cs = []
        for c in r.get("candlesticks", []):
            a = fb.num((c.get("yes_ask") or {}).get("close" + sfx))
            b = fb.num((c.get("yes_bid") or {}).get("close" + sfx))
            lo = fb.num((c.get("price") or {}).get("low" + sfx))
            hi = fb.num((c.get("price") or {}).get("high" + sfx))
            cs.append([c["end_period_ts"], a, b, lo, hi])
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(cs))
    t = e["close"] - ENTRY_H * 3600
    ok = [c for c in cs if c[0] <= t and c[1] is not None and c[2] is not None and 0 < c[2] < c[1] < 1
          and c[1] - c[2] <= MAX_SPREAD]
    if not ok:
        return None
    ask, bid = ok[-1][1], ok[-1][2]
    # trades from the entry until FILL_UNTIL_H hours before the close: a resting buy of player a fills on a low
    # trade, one of the opponent (priced 1 - yes) on a high one
    after = [c for c in cs if t < c[0] <= e["close"] - FILL_UNTIL_H * 3600]
    lows = [c[3] for c in after if c[3] is not None]
    highs = [c[4] for c in after if c[4] is not None]
    return {"ask": ask, "bid": bid, "low": min(lows) if lows else None, "high": max(highs) if highs else None}


def bets(e: dict, margin: float, how: str, pa: float, pb: float) -> dict | None:
    """The bet a forecast makes on match e, if any (pa: its chance for player a's contract, pb: for the opponent's):
    the side with the larger edge after fees, when that edge reaches the margin."""
    q = e.get("q")
    if not q:
        return None
    if how == "taker":
        ya, na_ = q["ask"], 1 - q["bid"]
        ea, eb = pa - ya - taker(ya), pb - na_ - taker(na_)
        if max(ea, eb) < margin:
            return None
        if ea >= eb:
            return {"side": "a", "price": ya, "fee": taker(ya), "won": e["a_won"]}
        return {"side": "b", "price": na_, "fee": taker(na_), "won": not e["a_won"]}
    ya, na_ = round(q["bid"] + 0.01, 2), round(1 - q["ask"] + 0.01, 2)
    ea, eb = pa - ya - maker(ya), pb - na_ - maker(na_)
    if max(ea, eb) < margin:
        return None
    if ea >= eb:  # filled when a trade prints 1 cent under the limit
        filled = q.get("low") is not None and q["low"] <= ya - 0.01
        return {"side": "a", "price": ya, "fee": maker(ya), "won": e["a_won"]} if filled else None
    filled = q.get("high") is not None and q["high"] >= 1 - na_ + 0.01
    return {"side": "b", "price": na_, "fee": maker(na_), "won": not e["a_won"]} if filled else None


def band(x: float) -> int:
    return min(9, int(x * 10))


def calibrate(priced: list[dict]) -> None:
    """The market-calibration forecast, walk-forward: a contract's chance is the share of contracts in the same
    competition and 10-cent price band that won in the months before (both players' contracts of every priced
    match), shrunk toward the price itself with 10 pseudo-contracts. It bets on the favorite-longshot bias where a
    competition showed one."""
    cnt: dict[tuple, list] = defaultdict(lambda: [0.0, 0])
    for m_ in sorted({month(e) for e in priced}):
        cur = [e for e in priced if month(e) == m_]
        for e in cur:
            xs = (e["q"]["ask"], 1 - e["q"]["bid"])
            e["cal"] = tuple((cnt[(e["comp"], band(x))][0] + 10 * x) / (cnt[(e["comp"], band(x))][1] + 10) for x in xs)
        for e in cur:
            for x, won in ((e["q"]["ask"], e["a_won"]), (1 - e["q"]["bid"], not e["a_won"])):
                c = cnt[(e["comp"], band(x))]
                c[0] += won
                c[1] += 1


def blend(priced: list[dict]) -> dict:
    """Elo blended with the market's mid price, walk-forward: per competition and month, the weight on Elo that
    minimized log loss over the months before (0 to 1 in steps of 0.05; 0, the market alone, with under 50 earlier
    matches). If Elo carries information the price lacks, the weight stays above 0 and the blend finds the edges."""
    weights: dict[str, list] = {}
    for c in {e["comp"] for e in priced}:
        xs = [e for e in priced if e["comp"] == c]
        for m_ in sorted({month(e) for e in xs}):
            prior = [e for e in xs if month(e) < m_]
            w = 0.0
            if len(prior) >= 50:
                w = min((k / 20 for k in range(21)), key=lambda w_: logloss(
                    [(w_ * e["p"] + (1 - w_) * (e["q"]["ask"] + e["q"]["bid"]) / 2, e["a_won"]) for e in prior]))
            weights.setdefault(c, []).append((m_, w))
            for e in xs:
                if month(e) == m_:
                    pa = w * e["p"] + (1 - w) * (e["q"]["ask"] + e["q"]["bid"]) / 2
                    e["blend"] = (pa, 1 - pa)
    return weights


FORECASTS = {"elo": lambda e: (e["p"], 1 - e["p"]), "blend": lambda e: e["blend"], "calibration": lambda e: e["cal"]}


def month(e: dict) -> str:
    return dt.datetime.fromtimestamp(e["close"], dt.timezone.utc).strftime("%Y-%m")


def day(e: dict) -> str:
    return dt.datetime.fromtimestamp(e["close"], dt.timezone.utc).date().isoformat()


def bankroll(rows: list[tuple[dict, dict]]) -> dict:
    """$1,000, each bet STAKE of the bankroll at the entry (open bets count as spent), settled at the close."""
    cash, open_ = 1000.0, []
    curve: list[tuple[str, float]] = []
    for e, b in sorted(rows, key=lambda x: x[0]["close"]):
        t = e["close"] - ENTRY_H * 3600
        for x in [x for x in open_ if x[0] <= t]:
            cash += x[1]
            open_.remove(x)
        eq = cash + sum(x[2] for x in open_)
        stake = min(eq * STAKE, cash)
        if stake < 1:
            continue
        k = stake / (b["price"] + b["fee"])
        cash -= stake
        open_.append((e["close"], k * (1.0 if b["won"] else 0.0), stake))
        curve.append((day(e), cash + sum(x[2] for x in open_)))
    for x in open_:
        cash += x[1]
    if rows:
        curve.append((day(max(rows, key=lambda x: x[0]["close"])[0]), cash))
    last: dict[str, float] = {}
    for d, v in curve:
        last[d[:7]] = v
    ms = sorted(last)
    rets, prev = [], 1000.0
    for m_ in ms:
        rets.append((m_, (last[m_] / prev - 1) * 100))
        prev = last[m_]
    return {"final": round(cash, 2), "months": rets}


def summary(rows: list[tuple[dict, dict]]) -> dict:
    if not rows:
        return {"n": 0}
    r = [((1.0 if b["won"] else 0.0) - b["price"] - b["fee"]) / (b["price"] + b["fee"]) for _, b in rows]
    m, se = cb.clustered([(day(e), x) for (e, _), x in zip(rows, r)])
    br = bankroll(rows)
    mr = [x for _, x in br["months"]]
    return {"n": len(rows), "won": round(100 * sum(b["won"] for _, b in rows) / len(rows), 1),
            "avg_price": round(st.mean(b["price"] for _, b in rows), 3),
            "breakeven": round(100 * st.mean(b["price"] + b["fee"] for _, b in rows), 1),
            "roi": round(100 * m, 2), "ci": round(196 * se, 2) if not math.isnan(se) else None,
            "final": br["final"], "month_mean": round(st.mean(mr), 2) if mr else None,
            "months_up": f"{sum(x > 0 for x in mr)}/{len(mr)}", "months": br["months"]}


def logloss(ps: list[tuple[float, bool]]) -> float:
    return -st.mean(math.log(max(1e-6, p if y else 1 - p)) for p, y in ps)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--per", type=int, default=120, help="matches priced per competition and month")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    evs = events()
    elo(evs)
    counts = defaultdict(int)
    for e in evs:
        counts[e["comp"]] += 1
    print("matches:", dict(counts), file=sys.stderr)
    rated = [e for e in evs if e["na"] >= MIN_N and e["nb"] >= MIN_N]
    by = defaultdict(list)
    for e in rated:
        by[(e["comp"], month(e))].append(e)
    pick = []
    for k, xs in sorted(by.items()):
        step = max(1, len(xs) // a.per)
        pick += xs[::step][:a.per]
    print(f"rated matches {len(rated)}, priced sample {len(pick)}", file=sys.stderr)

    def one(e):
        try:
            e["q"] = quotes(e)
        except Exception as ex:  # noqa: BLE001
            e["q"] = None
            e["err"] = str(ex)[:60]
        return e
    with ThreadPoolExecutor(8) as ex:
        pick = list(ex.map(one, pick))
    priced = [e for e in pick if e.get("q")]
    print(f"priced {len(priced)} of {len(pick)}", file=sys.stderr)
    comps = [c for c, _ in SERIES.values() if any(e["comp"] == c for e in priced)]
    res = {"asof": dt.date.today().isoformat(), "matches": dict(counts), "rated": len(rated), "priced": len(priced),
           "first": day(min(priced, key=lambda e: e["close"])) if priced else None,
           "last": day(max(priced, key=lambda e: e["close"])) if priced else None, "strategies": {},
           "forecast": {}, "narrow": {}}
    # the forecast against the market's mid as forecasts
    for c in ["all"] + comps:
        xs = [e for e in priced if c in ("all", e["comp"])]
        if len(xs) < 30:
            continue
        mid = [((e["q"]["ask"] + e["q"]["bid"]) / 2, e["a_won"]) for e in xs]
        mod = [(e["p"], e["a_won"]) for e in xs]
        dis = [e for e in xs if abs(e["p"] - (e["q"]["ask"] + e["q"]["bid"]) / 2) >= 0.15]
        res["forecast"][c] = {"n": len(xs), "logloss_market": round(logloss(mid), 4), "logloss_elo": round(logloss(mod), 4),
                              "disagree_n": len(dis),
                              "disagree_elo_right": round(100 * st.mean(
                                  (e["p"] > (e["q"]["ask"] + e["q"]["bid"]) / 2) == e["a_won"] for e in dis), 1) if dis else None}
    calibrate(priced)
    res["weights"] = blend(priced)
    for fc, prob in FORECASTS.items():
        for how in (("taker", "limit") if fc in ("elo", "blend") else ("taker",)):
            for mg in MARGINS:
                rows = [(e, b) for e in priced if (b := bets(e, mg, how, *prob(e)))]
                res["strategies"][f"{fc} {how} {mg:.2f}"] = {
                    "all": summary(rows), "by_comp": {c: summary([x for x in rows if x[0]["comp"] == c]) for c in comps}}
        # walk-forward narrowing (at the ask), and hindsight
        for mg in MARGINS:
            rows = [(e, b) for e in priced if (b := bets(e, mg, "taker", *prob(e)))]
            ms = sorted({month(e) for e, _ in rows})
            keep, out_ = [], []
            for i, m_ in enumerate(ms):
                if i < 2:
                    continue
                prior = [x for x in rows if month(x[0]) in ms[i - 2:i]]
                ok = set()
                for c in comps:
                    pr = [((1.0 if b["won"] else 0.0) - b["price"] - b["fee"]) / (b["price"] + b["fee"])
                          for e, b in prior if e["comp"] == c]
                    if len(pr) >= 10 and st.mean(pr) > 0:
                        ok.add(c)
                for x in rows:
                    if month(x[0]) == m_:
                        (keep if x[0]["comp"] in ok else out_).append(x)
            whole = {c: summary([x for x in rows if x[0]["comp"] == c]) for c in comps}
            best = {c for c, s_ in whole.items() if s_.get("n", 0) >= 10 and s_["roi"] > 0}
            res["narrow"][f"{fc} {mg:.2f}"] = {"walk_forward_kept": summary(keep), "walk_forward_dropped": summary(out_),
                                               "hindsight": summary([x for x in rows if x[0]["comp"] in best]),
                                               "hindsight_comps": sorted(best)}
    text = report(res, comps)
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests" / f"kalshi-tennis-forecast-{res['asof']}"
        out.with_suffix(".json").write_text(json.dumps(res, indent=1) + "\n")
        out.with_suffix(".md").write_text(text)
        print(f"saved {out.with_suffix('.md').relative_to(ROOT)}")
    return 0


def report(res: dict, comps: list[str]) -> str:
    def f(s):
        if not s.get("n"):
            return "0 | - | - | - | - | - |"
        ci = f" ± {s['ci']:.1f}" if s.get("ci") is not None else ""
        return (f"{s['n']} | {s['won']}% (needs {s['breakeven']}%) | {s['roi']:+.1f}%{ci} | ${s['final']:,.0f} | "
                f"{s['month_mean']:+.2f}% | {s['months_up']} |")
    L = [f"# Tennis forecast strategy on Kalshi, {res['asof']}", "",
         f"Method: `scripts/tennis_forecast_backtest.py` docstring. Settled matches: "
         + ", ".join(f"{k} {v:,}" for k, v in res["matches"].items())
         + f". Both players rated in {MIN_N}+ earlier matches: {res['rated']:,}; priced (an even sample by competition "
           f"and month, with a quote {ENTRY_H} hours before the close): {res['priced']:,}, {res['first']} to {res['last']}. "
           f"Return per bet after fees, ± 95% clustered by date; bankroll from $1,000 at {STAKE:.0%} a bet.", "",
         "## Is the forecast better than the market's price?", "",
         "Log loss of the match result (lower is better) with the market's mid price as the forecast and with the Elo "
         "forecast; and the matches where they differ by 15+ points: how often the Elo side won.", "",
         "| competition | matches | market log loss | Elo log loss | differ 15+ points | Elo's side won |",
         "|---|---:|---:|---:|---:|---:|"]
    for c, v in res["forecast"].items():
        L.append(f"| {c} | {v['n']} | {v['logloss_market']} | {v['logloss_elo']} | {v['disagree_n']} | "
                 f"{v['disagree_elo_right'] if v['disagree_elo_right'] is not None else '-'}% |")
    L += ["", "Weight on Elo in the blend, by month (0 = the market alone predicted best):", ""]
    for c, ws in sorted(res.get("weights", {}).items()):
        L.append(f"- {c}: " + ", ".join(f"{m_} {w:.2f}" for m_, w in ws))
    names = {"elo": "Elo forecast", "blend": "Elo blended with the price", "calibration": "calibration forecast"}
    L += ["", "## Betting the forecast's edge", "",
          "Elo: my rating of each player. Blend: Elo mixed with the market's mid at the weight that predicted best in "
          "the months before. Calibration: the share of contracts at the same price that won before, in the same "
          "competition (the favorite-longshot bias, where a competition showed one).", "",
          "| forecast, entry, minimum edge | bets | won | return per bet | $1,000 became | average month | months up |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for k, v in res["strategies"].items():
        fc, how, mg = k.split()
        L.append(f"| {names[fc]}, {'at the ask' if how == 'taker' else 'limit 1 cent over the bid'}, "
                 f"{float(mg) * 100:.0f} cents | " + f(v["all"]))
    L += ["", "By competition (at the ask, edges of 0 and 5 cents):", "",
          "| forecast, competition, minimum edge | bets | won | return per bet | $1,000 became | average month | months up |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for k, v in res["strategies"].items():
        fc, how, mg = k.split()
        if how != "taker" or mg not in ("0.00", "0.05"):
            continue
        for c in comps:
            L.append(f"| {names[fc]}, {c}, {float(mg) * 100:.0f} cents | " + f(v["by_comp"][c]))
    L += ["", "## Narrowing to the competitions where it worked", "",
          "Walk-forward: each month, only the competitions whose bets made money over the two months before (10+ bets); "
          "the bets it kept against those it dropped. Hindsight: the competitions that made money over the whole test.", "",
          "| forecast, minimum edge, version | bets | won | return per bet | $1,000 became | average month | months up |",
          "|---|---:|---:|---:|---:|---:|---:|"]
    for k, v in res["narrow"].items():
        fc, mg = k.split()
        lab = f"{names[fc]}, {float(mg) * 100:.0f} cents"
        L.append(f"| {lab}, walk-forward kept | " + f(v["walk_forward_kept"]))
        L.append(f"| {lab}, walk-forward dropped | " + f(v["walk_forward_dropped"]))
        L.append(f"| {lab}, hindsight ({', '.join(v['hindsight_comps']) or 'none'}) | " + f(v["hindsight"]))
    L += ["", "## Reading", ""]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
