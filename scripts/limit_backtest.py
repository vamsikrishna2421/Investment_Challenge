#!/usr/bin/env python3
"""Where should a resting buy limit sit? (Vamsi, Mon Oct 5: put buys at support so they fill by themselves on
the dips.) Compares, for radar names within 5% of their buy zone at the prior close:
  zone top   a DAY limit at the top of the buy zone (support + 0.3 ATR): fills on the first touch
  support    a DAY limit at support itself (the bottom of the zone): fills only on a deeper dip
  run 10:30  no resting order; buy at the run price when the price is inside the zone (above the stop)
Levels come from the radar rebuilt on the bars up to the prior close (levels.analyse, same filters as the radar:
tested support, R:R 1.5+, ATR 4%+, $15M a day). Intraday path from hourly bars (last ~2 years): a limit fills in
the first hour whose low trades 1 cent through it, at the limit or the hour's open if lower; the run entry uses
the 10:30 price. After the fill the plan stop works as a resting stop (fills at the stop or a lower open, less
slippage). Exits measured two ways: that day's close, and the close 3 sessions later (stops checked on daily
lows in between). Returns after trade.py slippage; standard errors clustered by date.
  python scripts/limit_backtest.py [--tickers A,B] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import dip_backtest as db  # noqa: E402
import levels as lv  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
TICK = 0.01


def stop_exit(stop: float, bars: list[tuple]) -> float | None:
    """Fill of a resting stop on the bars after entry: (price) or None."""
    for b in bars:
        if b[3] <= stop:
            base = b[1] if b[1] < stop else stop
            return base * (1 - sb.slip(base))
    return None


def events(sym: str, daily: list[dict], h1: dict) -> list[dict]:
    out = []
    idx = {dt.datetime.fromtimestamp(r["t"], dt.timezone.utc).astimezone(pfm.ET).date().isoformat(): i
           for i, r in enumerate(daily)}
    for d, bars in h1.items():
        i = idx.get(d)
        if i is None or i < 260 or i + 3 >= len(daily):
            continue
        a = lv.analyse({"sym": sym, "rows": daily[max(0, i - 260):i], "name": sym, "exchange": "", "type": ""})
        if not a or a["support_strength"] < 2 or (a["reward_risk"] or 0) < 1.5:
            continue
        if a["atr_pct"] < lv.MIN_ATR_PCT or a["dollar_vol_20d"] < lv.MIN_DOLLAR_VOL:
            continue
        prev = daily[i - 1]["c"]
        S, Z, X = a["buy_zone"][0], a["buy_zone"][1], a["stop"]
        if prev > Z * 1.05 or prev <= X:
            continue
        close, c3 = daily[i]["c"], daily[i + 3]["c"]
        later = [(None, r["o"], r["h"], r["l"], r["c"]) for r in daily[i + 1:i + 4]]
        rows = sorted(bars)
        for name, lim in (("zone top", Z), ("support", S)):
            k = next((j for j, b in enumerate(rows) if b[3] <= lim - TICK), None)
            if k is None:
                out.append({"date": d, "rule": name, "filled": 0.0})
                continue
            b = rows[k]
            e = b[1] if b[1] <= lim - TICK else lim
            rec = {"date": d, "rule": name, "filled": 1.0, "entry_vs_prev": (e / prev - 1) * 100,
                   "gap": k == 0 and b[0] == 570 and b[1] <= lim - TICK}
            sx = stop_exit(X, rows[k:])
            r0 = (sx if sx else close * (1 - sb.slip(close))) / e - 1
            sx3 = sx or stop_exit(X, later)
            r3 = (sx3 if sx3 else c3 * (1 - sb.slip(c3))) / e - 1
            rec.update(day=r0 * 100, day3=r3 * 100, stopped=1.0 if sx3 else 0.0)
            out.append(rec)
        e = next((b[4] for b in rows if b[0] == 570), None)
        if e and X < e <= Z:
            e2 = e * (1 + sb.slip(e))
            after = [b for b in rows if b[0] >= 630]
            sx = stop_exit(X, after)
            r0 = (sx if sx else close * (1 - sb.slip(close))) / e2 - 1
            sx3 = sx or stop_exit(X, later)
            r3 = (sx3 if sx3 else c3 * (1 - sb.slip(c3))) / e2 - 1
            out.append({"date": d, "rule": "run 10:30", "filled": 1.0, "entry_vs_prev": (e / prev - 1) * 100,
                        "day": r0 * 100, "day3": r3 * 100, "stopped": 1.0 if sx3 else 0.0})
        else:
            out.append({"date": d, "rule": "run 10:30", "filled": 0.0})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default="")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] or lv.CANDIDATES
    with ThreadPoolExecutor(8) as ex:
        loaded = list(ex.map(db.load, syms))
    rows = []
    for sym, daily, _m5, h1 in loaded:
        if daily and len(daily) > 270 and h1:
            rows += events(sym, daily, h1)
    L = [f"# Resting buy-limit backtest ({dt.date.today().isoformat()})", "",
         "Radar names within 5% of their buy zone at the prior close; hourly bars, last ~2 years. Method: "
         "`scripts/limit_backtest.py` docstring. Returns per filled trade after slippage, ± 95% clustered by date.", "",
         "| Entry rule | Name-days | Filled | Entry vs prior close | Return to that close % | Return 3 sessions later % | Stopped within 3 sessions |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    res = {}
    groups = [(rule, [r for r in rows if r["rule"] == rule]) for rule in ("zone top", "support", "run 10:30")]
    for rule in ("zone top", "support"):
        g = [r for r in rows if r["rule"] == rule]
        groups.append((f"{rule}: filled at the open (gap into the zone)", [r for r in g if r.get("gap")]))
        groups.append((f"{rule}: filled later in the day", [r for r in g if r["filled"] and not r.get("gap")]))
    for rule, g in groups:
        f = [r for r in g if r["filled"]]
        cap = lambda v: max(-25.0, min(25.0, v))  # noqa: E731
        m0, s0 = cb.clustered([(r["date"], cap(r["day"])) for r in f])
        m3, s3 = cb.clustered([(r["date"], cap(r["day3"])) for r in f])
        ev = sum(r["entry_vs_prev"] for r in f) / len(f) if f else float("nan")
        st = sum(r["stopped"] for r in f) / len(f) if f else float("nan")
        res[rule] = {"n": len(g), "filled": len(f), "entry_vs_prev": ev, "day": m0, "day_se": s0, "day3": m3,
                     "day3_se": s3, "stopped": st}
        L.append(f"| {rule} | {len(g):,} | {len(f):,} ({len(f) / max(1, len(g)) * 100:.0f}%) | {ev:+.2f}% | "
                 f"{m0:+.2f} ± {1.96 * s0:.2f} | {m3:+.2f} ± {1.96 * s3:.2f} | {st * 100:.0f}% |")
    text = "\n".join(L) + "\n"
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests"
        stem = f"limits-{dt.date.today().isoformat()}"
        (out / f"{stem}.md").write_text(text)
        (out / f"{stem}.json").write_text(json.dumps(res, indent=1) + "\n")
        print("saved", (out / f"{stem}.md").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
