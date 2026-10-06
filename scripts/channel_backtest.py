#!/usr/bin/env python3
"""Does a well-defined channel beat a loose one? (Vamsi, Oct 6: enter at the bottom of a proper channel, exit at the
top.) The radar trade from sr_backtest.py (daily bars, 5 years, radar candidates): buy the touch of the buy zone
(support to support + 0.3 ATR), stop 0.6 ATR under support, target the bottom of the sell zone under resistance,
time exit after --hold sessions. Trades are split by the channel as of the prior close: how many swings tested
the support and the resistance, and the channel's width in ATR. A proper channel: support and resistance each
tested 3+ times. Each group's average R (net return / risk to the stop) is set against random-day entries with the
same stop and target distances (sr_backtest.control); brackets are 95% bootstrap intervals.
  python scripts/channel_backtest.py [--tickers A,B] [--hold 10] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import random
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levels as lv  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT


def load(sym: str):
    rows = sb.daily(sym, "5y")
    if not rows or len(rows) <= 200:
        return sym, None, None
    return sym, rows, sb.levels_by_day(sym, rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--hold", type=int, default=10)
    ap.add_argument("--control", type=int, default=20)
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    with ThreadPoolExecutor(8) as ex:
        data = {s: (r, lv_) for s, r, lv_ in ex.map(load, syms) if r}
    rnd = random.Random(7)
    trades = []
    for s, (rows, lvl) in data.items():
        idx = {dt.datetime.fromtimestamp(r["t"], dt.timezone.utc).strftime("%Y-%m-%d"): j for j, r in enumerate(rows)}
        for t in sb.simulate(s, rows, lvl, "touch", a.hold):
            L = lvl[idx[t["date"]] - 1]
            t["res_strength"] = L["resistance_strength"]
            t["width_atr"] = (L["resistance"] - L["support"]) / L["atr"] if L["atr"] else None
            trades.append(t)
    groups = [("All radar touch trades", lambda t: True),
              ("Proper channel: support and resistance tested 3+ each", lambda t: t["strength"] >= 3 and t["res_strength"] >= 3),
              ("Support 3+, resistance under 3", lambda t: t["strength"] >= 3 and t["res_strength"] < 3),
              ("Support tested 2x", lambda t: t["strength"] == 2),
              ("Channel 2-5 ATR wide", lambda t: t["width_atr"] is not None and 2 <= t["width_atr"] < 5),
              ("Channel 5+ ATR wide", lambda t: t["width_atr"] is not None and t["width_atr"] >= 5),
              ("Proper channel, 2-5 ATR wide", lambda t: t["strength"] >= 3 and t["res_strength"] >= 3 and t["width_atr"] is not None and 2 <= t["width_atr"] < 5),
              ("Proper channel, support 4+ and resistance 4+", lambda t: t["strength"] >= 4 and t["res_strength"] >= 4)]
    L = [f"# Channel quality: proper channels against loose ones ({dt.date.today().isoformat()})", "",
         f"{len(data)} radar candidates, daily bars over 5 years, time exit after {a.hold} sessions. Method: the "
         "`scripts/channel_backtest.py` docstring. R = net return / risk to the stop; brackets = 95% bootstrap.", "",
         "| Trades | Count | Win rate | Target hit | Stopped | Avg return | Avg R | Random entries, same stop and target |",
         "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for name, f in groups:
        g = [t for t in trades if f(t)]
        if not g:
            L.append(f"| {name} | 0 | | | | | | |")
            continue
        rs = [t["R"] for t in g]
        lo, hi = sb.ci(rs, rnd, 1000)
        ctrl = [x for s in data for x in sb.control(s, data[s][0], data[s][1], [t for t in g if t["sym"] == s],
                                                      a.hold, a.control, rnd)]
        clo, chi = sb.ci(ctrl, rnd, 500) if ctrl else (float("nan"), float("nan"))
        L.append(f"| {name} | {len(g):,} | {sum(1 for t in g if t['R'] > 0) / len(g) * 100:.0f}% | "
                 f"{sum(1 for t in g if t['why'] == 'target') / len(g) * 100:.0f}% | "
                 f"{sum(1 for t in g if t['why'] == 'stop') / len(g) * 100:.0f}% | {st.fmean(t['ret'] for t in g):+.2f}% | "
                 f"{st.fmean(rs):+.3f} [{lo:+.3f}, {hi:+.3f}] | "
                 f"{st.fmean(ctrl) if ctrl else float('nan'):+.3f} [{clo:+.3f}, {chi:+.3f}] |")
    text = "\n".join(L) + "\n"
    print(text)
    if a.save:
        p = ROOT / "research" / "backtests" / f"channels-{dt.date.today().isoformat()}.md"
        p.write_text(text)
        print("saved", p.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
