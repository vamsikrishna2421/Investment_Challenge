#!/usr/bin/env python3
"""How long do dips take to recover, and how much of the drop comes back? (Vamsi, Oct 6.)
Events as in news_dip_backtest.py: radar candidates' sessions that closed 1+ ATR (14-day) under the prior close, over
the last --years, with the company's SEC filings from the day before to the day after split into offerings, results
and other news. For each dip: the session (1-20 after) whose close first gets back to the pre-dip close (full
recovery) and to half the drop; the share of the drop recovered by the close 5 and 10 sessions later; and how much
lower the price went first (lowest low over the next 5 sessions, % under the dip's close).
  python scripts/dip_recovery.py [--tickers A,B] [--years 4] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levels as lv  # noqa: E402
import news_dip_backtest as nd  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT


def events(sym: str, years: float, spy: dict[str, float]) -> list[dict]:
    rows = sb.daily(sym, "5y")
    if not rows or len(rows) < 300:
        return []
    dates = [nd.day(r) for r in rows]
    start = (dt.date.today() - dt.timedelta(days=int(365 * years))).isoformat()
    news = nd.news_dates(sym, start)
    if news is None:
        return []
    out = []
    for i in range(270, len(rows) - 21):
        if dates[i] < start:
            continue
        prev, a, c = rows[i - 1]["c"], lv.atr(rows[i - 30:i]), rows[i]["c"]
        if not a or (c - prev) / a > -1.0:
            continue
        drop = prev - c
        full = next((k for k in range(1, 21) if rows[i + k]["c"] >= prev), None)
        half = next((k for k in range(1, 21) if rows[i + k]["c"] >= c + 0.5 * drop), None)
        lvl = lv.analyse({"sym": sym, "rows": rows[max(0, i - 261):i], "name": sym, "exchange": "", "type": ""})
        kinds = sorted({k for d in dates[i - 1:i + 2] for k in news.get(d, [])})
        out.append({"sym": sym, "date": dates[i], "atr_drop": (c - prev) / a, "pct": (c / prev - 1) * 100,
                    "full": full, "half": half,
                    "rec5": (rows[i + 5]["c"] - c) / drop, "rec10": (rows[i + 10]["c"] - c) / drop,
                    "lower": (min(r["l"] for r in rows[i + 1:i + 6]) / c - 1) * 100,
                    "kind": "offering" if "offering" in kinds else ("results" if "results" in kinds else
                                                                     ("other news" if kinds else "no news")),
                    "at_sup": bool(lvl and lvl.get("support_strength", 0) >= 2
                                   and lvl["stop"] < rows[i]["l"] <= lvl["support"] + 0.5 * a),
                    "spy": spy.get(dates[i])})
    return out


def line(name: str, g: list[dict]) -> str:
    if not g:
        return f"| {name} | 0 | | | | | | | | |"
    n = len(g)
    pct = lambda k: sum(1 for e in g if e["full"] is not None and e["full"] <= k) / n * 100  # noqa: E731
    fd = [e["full"] for e in g if e["full"] is not None]
    hd = [e["half"] for e in g if e["half"] is not None]
    return (f"| {name} | {n:,} | {st.median(e['pct'] for e in g):+.1f}% | {pct(1):.0f}% | {pct(5):.0f}% | "
            f"{pct(10):.0f}% | {pct(20):.0f}% | {st.median(hd) if hd else float('nan'):.0f} "
            f"({len(hd) / n * 100:.0f}%) | {st.median(e['rec5'] for e in g) * 100:+.0f}% / "
            f"{st.median(e['rec10'] for e in g) * 100:+.0f}% | {st.median(e['lower'] for e in g):+.1f}% |")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--years", type=float, default=4.0)
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    spy_rows = sb.daily("SPY", "5y") or []
    spy = {nd.day(r): (r["c"] / spy_rows[k - 1]["c"] - 1) * 100 for k, r in enumerate(spy_rows) if k}
    with ThreadPoolExecutor(4) as ex:
        ev = [e for es in ex.map(lambda s: events(s, a.years, spy), syms) for e in es]
    L = [f"# Dip recovery: how long and how much ({dt.date.today().isoformat()})", "",
         f"{len(ev):,} sessions that closed 1+ ATR under the prior close, radar candidates, last {a.years:g} years. "
         "Method: the `scripts/dip_recovery.py` docstring. Medians; \"back\" = a close at or above the pre-dip close.",
         "", "| Dips | Count | Median drop | Back next day | Back within 5 | within 10 | within 20 | Sessions to win back "
         "half (share that did) | Drop recovered by day 5 / day 10 | Lower first (next 5 lows) |",
         "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    groups = [("All dips 1+ ATR", ev),
              ("1-2 ATR", [e for e in ev if e["atr_drop"] > -2]),
              ("2-3 ATR", [e for e in ev if -3 < e["atr_drop"] <= -2]),
              ("3+ ATR", [e for e in ev if e["atr_drop"] <= -3]),
              ("no company news", [e for e in ev if e["kind"] == "no news"]),
              ("results", [e for e in ev if e["kind"] == "results"]),
              ("offering", [e for e in ev if e["kind"] == "offering"]),
              ("other news", [e for e in ev if e["kind"] == "other news"]),
              ("no offering, low at support", [e for e in ev if e["kind"] != "offering" and e["at_sup"]]),
              ("no offering, not at support", [e for e in ev if e["kind"] != "offering" and not e["at_sup"]]),
              ("no offering, SPY down 1%+", [e for e in ev if e["kind"] != "offering" and (e["spy"] or 0) <= -1]),
              ("no offering, SPY not down 1%", [e for e in ev if e["kind"] != "offering" and (e["spy"] or 0) > -1])]
    L += [line(n, g) for n, g in groups]
    text = "\n".join(L) + "\n"
    print(text)
    if a.save:
        p = ROOT / "research" / "backtests" / f"dip-recovery-{dt.date.today().isoformat()}.md"
        p.write_text(text)
        print("saved", p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
