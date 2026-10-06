#!/usr/bin/env python3
"""How likely is a resting buy limit to fill before the close? (Vamsi, Oct 6: cancel real-money buy orders that are
very unlikely to fill and go for the next best waiting name; otherwise keep them and keep watching.)
For the radar candidates' hourly bars (last ~2 years), at each check hour from 9:30 to 14:30 ET: the share of
name-days whose low from that hour to the close traded k ATR (daily, 14-day, to the prior close) or more under the
price at the check, for k from 0.25 to 2. That is the fill rate of a limit k ATR under the price. Split by the price
against the prior close (names up 0.4+ ATR on the day dip back more often). real.py uses the tables (ODDS, ODDS_UP).
  python scripts/fill_odds.py [--tickers A,B] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dip_backtest as db  # noqa: E402
import levels as lv  # noqa: E402
import portfolio as pfm  # noqa: E402

KS = (0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0)
CHECKS = (570, 630, 690, 750, 810, 870)


def checks(sym: str) -> list[tuple]:
    try:
        _, daily, _m5, h1 = db.load(sym)
    except Exception:  # noqa: BLE001
        return []
    if not daily or not h1:
        return []
    idx = {dt.datetime.fromtimestamp(r["t"], dt.timezone.utc).astimezone(pfm.ET).date().isoformat(): i
           for i, r in enumerate(daily)}
    out = []
    for d, bars in h1.items():
        i = idx.get(d)
        if i is None or i < 30 or len(bars) < 6:
            continue
        a, prev = lv.atr(daily[i - 30:i]), daily[i - 1]["c"]
        if not a or a <= 0:
            continue
        for j, b in enumerate(bars):
            if b[0] in CHECKS:
                low = min(x[3] for x in bars[j:])
                out.append((b[0], (b[1] - low) / a, (b[1] - prev) / a))
    return out


def table(rows: list[tuple], label: str) -> list[str]:
    L = [f"**{label}**", "", "| Check (ET) | Name-days | " + " | ".join(f"k={k:g}" for k in KS) + " |",
         "|---|---:|" + "---:|" * len(KS)]
    for m in CHECKS:
        xs = [r for r in rows if r[0] == m]
        if xs:
            L.append(f"| {m // 60}:{m % 60:02d} | {len(xs):,} | "
                     + " | ".join(f"{sum(1 for r in xs if r[1] >= k) / len(xs) * 100:.0f}%" for k in KS) + " |")
    return L + [""]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(checks, syms))
    rows = [r for o in res for r in o]
    L = [f"# Resting buy-limit fill odds ({dt.date.today().isoformat()})", "",
         f"{sum(1 for o in res if o)} of {len(syms)} radar candidates, hourly bars (last ~2 years), {len(rows):,} "
         "name-hour checks. Each cell: the share of checks where the low from that hour to the close traded k ATR or "
         "more under the price at the check, i.e. the fill rate of a buy limit k ATR under the price. Method: the "
         "`scripts/fill_odds.py` docstring.", ""]
    L += table(rows, "All checks")
    L += table([r for r in rows if r[2] > 0], "Price above the prior close at the check")
    L += table([r for r in rows if r[2] >= 0.4], "Price 0.4+ ATR above the prior close at the check")
    L += ["Use (Vamsi, Oct 6; `real.py`): an open real-money buy with odds under 15% is cancelled for a waiting name "
          "with 30%+ odds that passes every entry rule, from 9:45 to 15:00; with none, the order stays and is watched.",
          "Caveats: hourly bars (the first check covers the whole first hour); the odds say nothing about how the "
          "trade does after the fill; a limit filled on a deep same-day dip often keeps falling (limits-2026-10-06.md)."]
    text = "\n".join(L) + "\n"
    print(text)
    if a.save:
        p = pfm.ROOT / "research" / "backtests" / f"fill-odds-{dt.date.today().isoformat()}.md"
        p.write_text(text)
        print("saved", p.relative_to(pfm.ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
