#!/usr/bin/env python3
"""Evidence check for the big-mover idea: every one-day jump >= 15% on >= 2x volume in the last N sessions,
and what the stock did against the market (SPY) over the next 5 and 10 sessions, split by one-year
volatility, prior +/-15% days, jump size in the stock's own standard deviations, share price, market cap,
and the catalyst tags of the latest lookback scan. Also compares buying at the jump-day close with buying
at the first new post-jump closing high (a breakout entry).

  python scripts/jump_study.py [--days 30] [--min-move 15] [--min-mcap 30] [--save]

Uses the day's cached history from movers.py when present. --save writes research/movers/study-<date>.json.
Caveats it cannot remove: one market regime, overlapping windows, and a universe of stocks that are still
listed and above the size floor today (survivors).
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import movers  # noqa: E402
import portfolio as pfm  # noqa: E402

FUND = {"earnings-guidance", "contract-order", "refinancing", "clinical-regulatory"}


def main() -> int:
    import pandas as pd  # type: ignore
    import yfinance as yf  # type: ignore
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--min-move", type=float, default=15.0)
    ap.add_argument("--min-mcap", type=float, default=30.0)
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    uni = movers.universe(a.min_mcap)
    closes, vols = movers.history(sorted(uni), period="1y")
    events = movers.find_events(closes, vols, a.days, a.min_move)
    spy = yf.download("SPY", period="1y", interval="1d", progress=False, auto_adjust=False)["Close"]
    spy = spy["SPY"] if isinstance(spy, pd.DataFrame) else spy
    tags = {}
    looks = sorted((movers.ROOT / "research" / "movers").glob("lookback-*.json"))
    if looks:
        for r in json.loads(looks[-1].read_text())["rows"]:
            if r.get("tags"):
                tags[r["symbol"]] = set(r["tags"])

    def fwd(c, i, h):
        if i + h >= len(c):
            return None
        r = c.iloc[i + h] / c.iloc[i] - 1
        return (r - (spy.asof(c.index[i + h]) / spy.asof(c.index[i]) - 1)) * 100

    rows = []
    for e in events:
        c = closes[e["symbol"]].dropna()
        i = c.index.get_loc(pd.Timestamp(e["event_date"]))
        e["market_cap"] = uni.get(e["symbol"], {}).get("marketCap")
        e["event_price"] = float(c.iloc[i])
        e["fwd5"], e["fwd10"] = fwd(c, i, 5), fwd(c, i, 10)
        t = tags.get(e["symbol"])
        e["news"] = "unknown" if t is None else "fundamental" if t & FUND else "other"
        for j in range(i + 3, min(i + 21, len(c))):  # first new post-jump closing high, 3+ sessions later
            if c.iloc[j] > c.iloc[i:j].max():
                e["breakout_date"] = c.index[j].date().isoformat()
                e["breakout_fwd5"], e["breakout_fwd10"] = fwd(c, j, 5), fwd(c, j, 10)
                break
        rows.append(e)

    def line(label, g):
        f5 = [r["fwd5"] for r in g if r.get("fwd5") is not None]
        f10 = [r["fwd10"] for r in g if r.get("fwd10") is not None]
        md = lambda x: f"{st.median(x):+6.1f}%" if x else "     -"
        mn = lambda x: f"{st.mean(x):+6.1f}%" if x else "     -"
        up = sum(1 for x in f10 if x > 15)
        dn = sum(1 for x in f10 if x < -15)
        print(f"  {label:24} n={len(g):3}  5d median {md(f5)}  10d median {md(f10)} mean {mn(f10)}  "
              f"10d >+15%: {up}/{len(f10)}  <-15%: {dn}/{len(f10)}")

    def table(title, key, order):
        print(f"\n{title}")
        for k in order:
            g = [r for r in rows if key(r) == k]
            if g:
                line(k, g)

    print(f"{len(rows)} jumps >= {a.min_move:g}% on >= 2x volume in the last {a.days} sessions, "
          f"{len(uni)} stocks; returns are against SPY")
    line("all", rows)
    table("Noise rule (1y vol >= %g%% or >= %d days of +/-15%%)" % (movers.NOISY_VOL, movers.NOISY_SPIKES),
          lambda r: "noisy" if r.get("noisy") else "calm", ["calm", "noisy"])
    table("One-year volatility", lambda r: "?" if r.get("vol_1y") is None else "<50%" if r["vol_1y"] < 50 else
          "50-80%" if r["vol_1y"] < 80 else "80-120%" if r["vol_1y"] < 120 else "120-200%" if r["vol_1y"] < 200
          else ">=200%", ["<50%", "50-80%", "80-120%", "120-200%", ">=200%"])
    table("Days of +/-15% in the prior year", lambda r: "?" if r.get("spike_days_1y") is None else
          "0" if r["spike_days_1y"] == 0 else "1-3" if r["spike_days_1y"] <= 3 else "4-9"
          if r["spike_days_1y"] <= 9 else ">=10", ["0", "1-3", "4-9", ">=10"])
    table("Jump in the stock's own standard deviations", lambda r: "?" if r.get("jump_sigma") is None else
          "<3" if r["jump_sigma"] < 3 else "3-5" if r["jump_sigma"] < 5 else "5-8" if r["jump_sigma"] < 8
          else ">=8", ["<3", "3-5", "5-8", ">=8"])
    table("Share price on the jump day", lambda r: "<$1" if r["event_price"] < 1 else "$1-5" if r["event_price"] < 5
          else "$5-20" if r["event_price"] < 20 else ">=$20", ["<$1", "$1-5", "$5-20", ">=$20"])
    table("Market cap today", lambda r: "<$100M" if (r["market_cap"] or 0) < 1e8 else "$100-300M"
          if r["market_cap"] < 3e8 else "$300M-2B" if r["market_cap"] < 2e9 else ">$2B",
          ["<$100M", "$100-300M", "$300M-2B", ">$2B"])
    table("Calm stocks >= $100M, by catalyst (tags from the latest lookback scan)",
          lambda r: "excluded" if r.get("noisy") or (r["market_cap"] or 0) < 1e8 else r["news"],
          ["fundamental", "other", "unknown"])
    calm = [r for r in rows if not r.get("noisy") and (r["market_cap"] or 0) >= 1e8]
    b5 = [r["breakout_fwd5"] for r in calm if r.get("breakout_fwd5") is not None]
    d5 = [r["fwd5"] for r in calm if r.get("fwd5") is not None]
    print("\nEntry timing, calm stocks >= $100M (5 sessions after entry, against SPY)")
    if d5:
        print(f"  at the jump-day close:        n={len(d5):3} median {st.median(d5):+.1f}%  "
              f"up {sum(1 for x in d5 if x > 0)}/{len(d5)}")
    if b5:
        print(f"  at the first post-jump high:  n={len(b5):3} median {st.median(b5):+.1f}%  "
              f"up {sum(1 for x in b5 if x > 0)}/{len(b5)}")
    if a.save:
        now = pfm.now_utc()
        out = movers.ROOT / "research" / "movers" / f"study-{pfm.et_date(now).isoformat()}.json"
        out.write_text(json.dumps({"generated_at": pfm.iso(now), "days": a.days, "min_move": a.min_move,
                                   "universe": len(uni), "rows": rows}, indent=1, default=str))
        print(f"\nsaved {out.relative_to(movers.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
