#!/usr/bin/env python3
"""Intraday dips (Vamsi, Oct 6: a dip is a fall of 3-4% or more at any time of the session, often recovered by the
close, which daily bars never show). For each radar candidate's sessions over the last ~2 years (hourly bars): a buy
limit X% under the session's open fills when an hour's low trades 1 cent through it, at the limit (variant: X% under
the prior close, where an open below the limit fills at the open). Returns from the fill to that day's close, the
next close and the close 3 sessions later, after trade.py slippage, no stop; means +/- 95% clustered by date.
Splits for the 4% dip: the hour of the fill, company news (an SEC filing from the day before to the day after, as in
news_dip_backtest.py), the fill inside the radar support band (stop < fill <= support + 0.5 ATR, levels as of the
prior close) and SPY down 1%+ that session. Baseline: buying every session's open.
  python scripts/intraday_dip_backtest.py [--tickers A,B] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import dip_backtest as db  # noqa: E402
import levels as lv  # noqa: E402
import news_dip_backtest as nd  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
TICK = 0.01
FROM_OPEN = (3, 4, 5, 7, 10)
FROM_PREV = (3, 5, 10)


def fill_at(limit: float, bars: list[tuple], gap_fills: bool) -> tuple[float, int] | None:
    for j, (m, o, h, lo, c) in enumerate(bars):
        if lo <= limit - TICK:
            return (min(o, limit) if gap_fills else limit), j
    return None


def run(sym: str, spy: dict[str, float]) -> tuple[list[dict], list[dict]]:
    _, daily, _m5, h1 = db.load(sym)
    if not daily or not h1:
        return [], []
    dates = [nd.day(r) for r in daily]
    idx = {d: i for i, d in enumerate(dates)}
    news = nd.news_dates(sym, (dt.date.today() - dt.timedelta(days=760)).isoformat()) or {}
    fills, base = [], []
    for d, bars in sorted(h1.items()):
        i = idx.get(d)
        if i is None or i < 270 or i + 3 >= len(daily) or len(bars) < 6:
            continue
        o, prev, close = bars[0][1], daily[i - 1]["c"], daily[i]["c"]
        n1, n3 = daily[i + 1]["c"], daily[i + 3]["c"]
        a = lv.atr(daily[i - 30:i])
        if not a:
            continue
        base.append({"date": d, "close": nd.ret(o, close), "next": nd.ret(o, n1), "d3": nd.ret(o, n3)})
        has_news = any(x in news for x in dates[i - 1:i + 2])
        lvl = None
        for kind, xs, ref, gap in (("open", FROM_OPEN, o, False), ("prev", FROM_PREV, prev, True)):
            for x in xs:
                f = fill_at(ref * (1 - x / 100), bars, gap)
                if not f:
                    continue
                e, j = f
                if lvl is None:
                    lvl = lv.analyse({"sym": sym, "rows": daily[max(0, i - 261):i], "name": sym, "exchange": "",
                                      "type": ""}) or {}
                at_sup = bool(lvl and lvl.get("support_strength", 0) >= 2 and lvl["stop"] < e <= lvl["support"] + 0.5 * a)
                fills.append({"sym": sym, "date": d, "kind": kind, "x": x, "hour": bars[j][0], "news": has_news,
                              "at_sup": at_sup, "spy": spy.get(d), "close": nd.ret(e, close), "next": nd.ret(e, n1),
                              "d3": nd.ret(e, n3), "back": close >= ref, "atr_pct": a / prev * 100})
    return fills, base


def stats(name: str, g: list[dict], sessions: int) -> str:
    def cell(k: str) -> str:
        xs = [(r["date"], max(-40.0, min(40.0, r[k]))) for r in g]
        if not xs:
            return "-"
        m, se = cb.clustered(xs)
        return f"{m:+.2f} ± {1.96 * se:.2f}"
    if not g:
        return f"| {name} | 0 | | | | | | |"
    win = sum(1 for r in g if r["close"] > 0) / len(g) * 100
    back = sum(1 for r in g if r.get("back")) / len(g) * 100
    return (f"| {name} | {len(g):,} | {len(g) / max(1, sessions) * 100:.0f}% | {cell('close')} | {win:.0f}% | "
            f"{back:.0f}% | {cell('next')} | {cell('d3')} |")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    spy_rows = db.sb.daily("SPY", "5y") or []
    spy = {nd.day(r): (r["c"] / spy_rows[k - 1]["c"] - 1) * 100 for k, r in enumerate(spy_rows) if k}
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda s: run(s, spy), syms))
    fills = [f for fs, _ in res for f in fs]
    base = [b for _, bs in res for b in bs]
    n = len(base)
    if not n:
        print("no sessions with hourly bars")
        return 1
    L = [f"# Intraday dips: buy limits under the open or the prior close ({dt.date.today().isoformat()})", "",
         f"{sum(1 for fs, bs in res if bs)} of {len(syms)} radar candidates, hourly bars (last ~2 years), {n:,} "
         "sessions. Method: the `scripts/intraday_dip_backtest.py` docstring. Returns % after slippage, ± 95% clustered "
         "by date; no stop. \"Back\" = the session closed at or above the open (or prior close) the dip is measured "
         "from.", "",
         "| Buy limit | Fills | Of sessions | Fill to close | Up at close | Back by the close | Fill to next close | "
         "Fill to 3 sessions |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    m, se = cb.clustered([(b["date"], b["close"]) for b in base])
    m1, s1 = cb.clustered([(b["date"], b["next"]) for b in base])
    m3, s3 = cb.clustered([(b["date"], max(-40, min(40, b["d3"]))) for b in base])
    L.append(f"| Baseline: buy every open | {n:,} | 100% | {m:+.2f} ± {1.96 * se:.2f} | "
             f"{sum(1 for b in base if b['close'] > 0) / n * 100:.0f}% | | {m1:+.2f} ± {1.96 * s1:.2f} | "
             f"{m3:+.2f} ± {1.96 * s3:.2f} |")
    for x in FROM_OPEN:
        L.append(stats(f"{x}% under the open", [f for f in fills if f["kind"] == "open" and f["x"] == x], n))
    for x in FROM_PREV:
        L.append(stats(f"{x}% under the prior close", [f for f in fills if f["kind"] == "prev" and f["x"] == x], n))
    g4 = [f for f in fills if f["kind"] == "open" and f["x"] == 4]
    L += ["", "**The 4% dip under the open, split**", "",
          "| Group | Fills | Of sessions | Fill to close | Up at close | Back by the close | Fill to next close | "
          "Fill to 3 sessions |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for name, g in [("filled 9:30-10:30", [f for f in g4 if f["hour"] < 630]),
                    ("filled 10:30-12:30", [f for f in g4 if 630 <= f["hour"] < 750]),
                    ("filled 12:30-16:00", [f for f in g4 if f["hour"] >= 750]),
                    ("company news", [f for f in g4 if f["news"]]),
                    ("no company news", [f for f in g4 if not f["news"]]),
                    ("no news, fill in the support band", [f for f in g4 if not f["news"] and f["at_sup"]]),
                    ("no news, not at support", [f for f in g4 if not f["news"] and not f["at_sup"]]),
                    ("SPY down 1%+ that session", [f for f in g4 if f["spy"] is not None and f["spy"] <= -1]),
                    ("SPY not down 1%", [f for f in g4 if f["spy"] is not None and f["spy"] > -1]),
                    ("ATR under 6% of the price", [f for f in g4 if f["atr_pct"] < 6]),
                    ("ATR 6%+ of the price", [f for f in g4 if f["atr_pct"] >= 6])]:
        L.append(stats(name, g, n))
    text = "\n".join(L) + "\n"
    print(text)
    if a.save:
        p = ROOT / "research" / "backtests" / f"intraday-dips-{dt.date.today().isoformat()}.md"
        p.write_text(text)
        print("saved", p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
