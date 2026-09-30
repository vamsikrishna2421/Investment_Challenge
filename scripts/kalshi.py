#!/usr/bin/env python3
"""Read-only prediction-market pricing from Kalshi's public API (no account, no orders).

  python scripts/kalshi.py                       # this week's macro set: payrolls, unemployment, CPI, Fed
  python scripts/kalshi.py KXPAYROLLS KXU3       # chosen series
  python scripts/kalshi.py --save                # also log to research/kalshi/<date>.json (to score surprises later)

For "Above X" ladders it prints each rung's yes price (the market's probability) and the implied median:
the level where the probability of "above" crosses 50%. A release is a surprise to the extent it lands away
from that median; this is the benchmark for event reactions (jobs report, CPI, Fed), not a trade signal.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio as pfm  # noqa: E402

BASE = "https://api.elections.kalshi.com/trade-api/v2"
DEFAULT = ["KXPAYROLLS", "KXU3", "KXCPI", "KXCPIYOY", "KXFED"]


def get(path: str) -> dict:
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def series_markets(series: str) -> list[dict]:
    """Open markets of the series' nearest-closing event."""
    best, best_close = None, None
    cursor = ""
    for _ in range(5):  # page through the series' open events
        j = get(f"/events?series_ticker={series}&status=open&limit=100&with_nested_markets=true"
                + (f"&cursor={cursor}" if cursor else ""))
        for e in j.get("events", []):
            closes = [m.get("close_time") for m in e.get("markets", []) if m.get("close_time")]
            if closes and (best_close is None or min(closes) < best_close):
                best, best_close = e, min(closes)
        cursor = j.get("cursor") or ""
        if not cursor:
            break
    if not best:
        return []
    return get(f"/markets?event_ticker={best['event_ticker']}&limit=200").get("markets", [])


def ladder(ms: list[dict]) -> dict:
    rows = []
    for m in ms:
        bid, ask, last = num(m.get("yes_bid_dollars")), num(m.get("yes_ask_dollars")), num(m.get("last_price_dollars"))
        mid = (bid + ask) / 2 if bid is not None and ask is not None and ask > 0 else last
        rows.append({"label": m.get("yes_sub_title") or m.get("subtitle") or m["ticker"], "strike": num(m.get("floor_strike")),
                     "bid": bid, "ask": ask, "last": last, "p": mid, "volume": num(m.get("volume_fp")),
                     "close_time": m.get("close_time"), "title": m.get("title")})
    rows.sort(key=lambda r: (r["strike"] is None, r["strike"] or 0))
    med = None
    # Rungs with a real two-sided market only: a 0.01/0.90 quote says nothing about the probability.
    above = [r for r in rows if r["strike"] is not None and r["p"] is not None
             and (r["ask"] is None or r["bid"] is None or r["ask"] - r["bid"] <= 0.15)]
    for lo, hi in zip(above, above[1:]):  # probability of "above" falls as the strike rises
        if lo["p"] >= 0.5 > hi["p"] and lo["p"] != hi["p"]:
            med = lo["strike"] + (lo["p"] - 0.5) / (lo["p"] - hi["p"]) * (hi["strike"] - lo["strike"])
            break
    return {"rows": rows, "median": med}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("series", nargs="*")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    out = {}
    for s in a.series or DEFAULT:
        try:
            ms = series_markets(s)
        except Exception as e:  # noqa: BLE001
            print(f"{s}: error {str(e)[:80]}")
            continue
        if not ms:
            print(f"{s}: no open markets")
            continue
        lad = ladder(ms)
        out[s] = lad
        r0 = lad["rows"][0]
        print(f"\n{s} | {r0['title']} | closes {str(r0['close_time'])[:16]}Z"
              + (f" | implied median {lad['median']:,.3f}" if lad["median"] is not None else ""))
        for r in lad["rows"]:
            if r["p"] is None or not (0.02 <= r["p"] <= 0.98):
                continue
            print(f"   {r['label'][:30]:30} p {r['p'] * 100:5.1f}%  (bid {r['bid']}, ask {r['ask']}, volume {r['volume']:,.0f})")
    if a.save and out:
        d = pfm.ROOT / "research" / "kalshi"
        d.mkdir(parents=True, exist_ok=True)
        f = d / f"{pfm.et_date(pfm.now_utc()).isoformat()}.json"
        prev = json.loads(f.read_text()) if f.exists() else {"snapshots": []}
        prev["snapshots"].append({"at": pfm.iso(pfm.now_utc()), "series": out})
        f.write_text(json.dumps(prev, indent=1))
        print(f"\nsaved {f.relative_to(pfm.ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
