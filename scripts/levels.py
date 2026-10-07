#!/usr/bin/env python3
"""Support/resistance radar for high-volatility stocks (Vamsi's round 2 strategy: buy at support,
sell at resistance, stop below support).

  python scripts/levels.py build [--tickers A,B] [--min-names 20] [--save]
      Daily bars for the candidate list, volatility and liquidity filters, swing-pivot levels.
      --save writes config/radar.json (the live radar) and research/radar/<date>.md/.json.
  python scripts/levels.py check [--near 3] [--all]
      Compares the latest synced quotes (.cache/quotes.json) with config/radar.json:
      BUY ZONE (price at support, above the stop), BOUNCE (touched the zone after the radar's bars and
      held, entry reward:risk >= 1.5), NEAR (within --near % of the zone), TARGET (at the sell zone)
      and BROKEN (at or under the stop, or traded through it: support failed, no buy); HALTED (a zero-volume
      session in the last 5: no buy). Each line shows
      the day's move against the prior close, also in ATR; BUY ZONE and BOUNCE list the deepest dip first.

Levels: swing highs and lows over the last 120 sessions (a bar whose low or high is the extreme of the
3 bars on each side), clustered within half an ATR (min 1.5%) into zones. A level's strength is the
number of swings in its zone; a support or resistance needs at least two (tested twice). Support is the
nearest tested zone below the price (a zone within 0.1 ATR of the price counts when two of its swings are
lows: the price is sitting on support), resistance the nearest tested zone more than 0.1 ATR above. The buy
zone runs from support to support + 0.3 ATR, the sell zone from resistance - 0.3 ATR to resistance, and the stop sits
0.6 ATR under support. Reward:risk = (sell-zone bottom - buy-zone top) / (buy-zone top - stop).
These are arithmetic on past prices, not forecasts.
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
import marketdata as md  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
RADAR = ROOT / "config" / "radar.json"

# Vamsi's names first, then high-volatility peers: bitcoin miners and AI hosts, neoclouds, quantum,
# nuclear, space and drones, crypto equities and high-beta fintech. All US-listed common stock.
CANDIDATES = [
    "GPUS", "IREN", "BTDR",
    "CIFR", "WULF", "MARA", "RIOT", "CLSK", "HUT", "CORZ", "BITF", "HIVE", "APLD", "BTBT", "GLXY",
    "NBIS", "CRWV", "SMCI", "SOUN", "BBAI",
    "IONQ", "RGTI", "QBTS", "QUBT",
    "OKLO", "SMR", "NNE", "LEU",
    "RKLB", "ASTS", "LUNR", "RCAT", "ONDS", "UMAC",
    "COIN", "MSTR", "HOOD", "BMNR", "SBET", "CRCL",
    "AFRM", "UPST", "SOFI", "HIMS", "TEM",
    # Added Sat Oct 3 from Vamsi's watch list (the high-volatility ones; each joins the radar on a day it passes
    # the filters): semis and hardware, software, consumer internet, biotech, brokers and crypto platforms.
    "AXTI", "SMTC", "POET", "AEHR", "HIMX", "DELL", "ORCL", "NOW", "PATH", "META", "SNAP", "DUOL", "GRAB",
    "CRSP", "BULL", "BKKT", "ALMU",
    # Added Mon Oct 5 from the day's 15%+ movers that pass the filters (one Brazil fintech; AI and genomics biotech).
    "STNE", "RXRX", "DNA", "PCVX", "GRAL",
]
MUST_KEEP = {"GPUS", "IREN", "BTDR"}
# Names that trade mostly on bitcoin or ether (miners, hosts that still mine, treasuries, exchanges):
# one factor, so at most 2 of a book's 4 radar positions (RUNBOOK 2a).
CRYPTO_LINKED = {"IREN", "BTDR", "CIFR", "WULF", "MARA", "RIOT", "CLSK", "HUT", "CORZ", "BITF", "HIVE", "BTBT",
                 "GLXY", "COIN", "MSTR", "BMNR", "SBET", "CRCL", "BKKT"}

PIVOT_K = 3
LOOKBACK = 120
MIN_ATR_PCT = 4.0
STOP_ATR = 0.6  # the stop sits this many ATR under support
MAX_SIZE_PCT = 25.0  # a position is at most this % of equity ...
RISK_PCT = 1.5  # ... and loses at most this % of equity at its stop (replay test, Oct 6: RUNBOOK 2d) ...
GAP_PCT = 1.0  # ... counting a gap allowance: half the replay's stops gapped through at the open and filled on
# average 1.06% under their price (median 0.2%, 90th percentile 2.9%; 700 sessions, Oct 7); a 1% allowance did
# better than the plain stop distance in all four paper-rule samples and three of four real-book ones, with smaller
# drawdowns (research/replay/*-lessons.md, *-realbook.md, research/backtests/lessons-2026-10-07.md)


def size_pct(entry: float, stop: float) -> float:
    """Position size in % of equity: 25%, cut so the stop plus a GAP_PCT gap loses at most RISK_PCT of equity (a
    stop 8% under the entry gets 16.7%; GPUS's 9-10% stops in the replay lost 2.3-2.5% of equity at full size)."""
    if entry <= stop:
        return 0.0
    return round(min(MAX_SIZE_PCT, RISK_PCT / ((entry - stop) / entry + GAP_PCT / 100)), 1)
MIN_DOLLAR_VOL = 15e6


def bars(sym: str) -> dict | None:
    try:
        r = md.yahoo_chart(sym, "1y", "1d", False)
    except Exception as e:  # noqa: BLE001
        print(f"  {sym}: {str(e)[:90]}", file=sys.stderr)
        return None
    q = (r.get("indicators") or {}).get("quote") or [{}]
    q = q[0]
    ts = r.get("timestamp") or []
    rows = []
    for i, t in enumerate(ts):
        o, h, lo, c, v = (q.get(k, [None] * len(ts))[i] for k in ("open", "high", "low", "close", "volume"))
        if None in (h, lo, c):
            continue
        rows.append({"t": t, "o": o or c, "h": h, "l": lo, "c": c, "v": v or 0})
    meta = r.get("meta") or {}
    return {"sym": sym, "rows": rows, "name": meta.get("longName") or meta.get("shortName") or sym,
            "exchange": meta.get("fullExchangeName") or meta.get("exchangeName"),
            "type": meta.get("instrumentType")}


def atr(rows: list[dict], n: int = 14) -> float:
    trs = []
    for i in range(1, len(rows)):
        h, lo, pc = rows[i]["h"], rows[i]["l"], rows[i - 1]["c"]
        trs.append(max(h - lo, abs(h - pc), abs(lo - pc)))
    tail = trs[-n:]
    return sum(tail) / len(tail) if tail else 0.0


def annual_vol(rows: list[dict]) -> float | None:
    rets = [math.log(rows[i]["c"] / rows[i - 1]["c"]) for i in range(1, len(rows))
            if rows[i - 1]["c"] and rows[i]["c"]]
    if len(rets) < 30:
        return None
    m = sum(rets) / len(rets)
    var = sum((x - m) ** 2 for x in rets) / (len(rets) - 1)
    return math.sqrt(var) * math.sqrt(252) * 100


def pivots(rows: list[dict], k: int = PIVOT_K) -> tuple[list[tuple[int, float]], list[tuple[int, float]]]:
    lows, highs = [], []
    n = len(rows)
    for i in range(n):
        lo_w = rows[max(0, i - k):min(n, i + k + 1)]
        if rows[i]["l"] == min(r["l"] for r in lo_w) and i + 1 < n:
            lows.append((i, rows[i]["l"]))
        if rows[i]["h"] == max(r["h"] for r in lo_w) and i + 1 < n:
            highs.append((i, rows[i]["h"]))
    return lows, highs


def zones(points: list[tuple[int, float]], tol: float, n: int) -> list[dict]:
    """Cluster pivot prices into zones; strength = swings in the zone, recent swings break ties."""
    out: list[dict] = []
    for i, p in sorted(points, key=lambda x: x[1]):
        if out and p - out[-1]["hi"] <= tol:
            z = out[-1]
            z["pts"].append((i, p))
            z["hi"] = p
        else:
            out.append({"lo": p, "hi": p, "pts": [(i, p)]})
    for z in out:
        w = [1 + (i / max(1, n)) for i, _ in z["pts"]]
        z["level"] = sum(p * wi for (_, p), wi in zip(z["pts"], w)) / sum(w)
        z["strength"] = len(z["pts"])
        z["last_idx"] = max(i for i, _ in z["pts"])
    return out


def analyse(b: dict, stop_atr: float | None = None) -> dict | None:
    rows = b["rows"]
    if len(rows) < 60:
        return None
    last = rows[-1]
    price = last["c"]
    a = atr(rows)
    win = rows[-LOOKBACK:]
    n = len(win)
    tol = max(0.5 * a, 0.015 * price)
    lows, highs = pivots(win)
    zs = zones(lows + highs, tol, n)
    # A zone within 0.1 ATR of the price is support the price is sitting on when at least two of its swings are
    # lows (GRAB, Oct 2: lows at 3.07 twice against a 3.08 close; the strict "below" test used before Oct 5
    # skipped it). A zone at the price built from highs is old resistance the price has run into, not support.
    def n_lows(z: dict) -> int:
        return sum(1 for _, p in lows if z["lo"] <= p <= z["hi"])
    below = [z for z in zs if z["level"] < price - 0.1 * a or (z["level"] <= price + 0.1 * a and n_lows(z) >= 2)]
    above = [z for z in zs if z["level"] > price + 0.1 * a]
    sup = next((z for z in sorted(below, key=lambda z: -z["level"]) if z["strength"] >= 2), None)
    res = next((z for z in sorted(above, key=lambda z: z["level"]) if z["strength"] >= 2), None)
    if res is None and above:
        res = max(above, key=lambda z: z["level"])
    hi120 = max(r["h"] for r in win)
    lo120 = min(r["l"] for r in win)
    support = sup["level"] if sup else lo120
    resistance = res["level"] if res else max(hi120, price + 2 * a)
    stop = support - (STOP_ATR if stop_atr is None else stop_atr) * a
    zone_top = support + 0.3 * a
    sell_lo = resistance - 0.3 * a
    dv = sum(r["c"] * r["v"] for r in rows[-20:]) / min(20, len(rows))
    rr = (sell_lo - zone_top) / (zone_top - stop) if zone_top > stop else None
    sma50 = sum(r["c"] for r in rows[-50:]) / min(50, len(rows))
    chg120 = (price / win[0]["c"] - 1) * 100 if win[0]["c"] else None
    sec = sorted(below, key=lambda z: -z["level"])
    s2 = next((z["level"] for z in sec if z is not sup and z["level"] < support - 0.3 * a), None)
    return {
        "ticker": b["sym"], "name": b["name"], "exchange": b["exchange"], "price": round(price, 4),
        "asof": dt.datetime.fromtimestamp(last["t"], dt.timezone.utc).strftime("%Y-%m-%d"),
        "atr": round(a, 4), "atr_pct": round(a / price * 100, 2), "vol_1y": round(annual_vol(rows) or 0, 1),
        "dollar_vol_20d": round(dv), "low_120": round(lo120, 4), "high_120": round(hi120, 4),
        "support": round(support, 4), "support_strength": sup["strength"] if sup else 0,
        "support_2": round(s2, 4) if s2 else None,
        "buy_zone": [round(support, 4), round(zone_top, 4)], "stop": round(stop, 4),
        "resistance": round(resistance, 4), "resistance_strength": res["strength"] if res else 0,
        "resistance_1": round(min(z["level"] for z in above), 4) if above else None,
        "sell_zone": [round(sell_lo, 4), round(resistance, 4)],
        "vs_sma50_pct": round((price / sma50 - 1) * 100, 1), "chg_120d_pct": round(chg120, 1) if chg120 is not None else None,
        "reward_risk": round(rr, 2) if rr else None,
        "halted": any(not r["v"] for r in rows[-5:]),
        "to_zone_pct": round((price / zone_top - 1) * 100, 2),
        "upside_to_target_pct": round((sell_lo / zone_top - 1) * 100, 1),
        "risk_to_stop_pct": round((1 - stop / zone_top) * 100, 1),
    }


def fmt(x: float | None, d: int = 2) -> str:
    if x is None:
        return "-"
    return f"{x:,.{4 if x < 1 else d}f}"


def build(a) -> int:
    syms = [s.strip().upper() for s in a.tickers.split(",") if s.strip()] if a.tickers else CANDIDATES
    blocked = set(json.loads((ROOT / "config" / "blocklist.json").read_text()).get("tickers", {}))
    with ThreadPoolExecutor(max_workers=8) as ex:
        got = list(ex.map(bars, syms))
    rows, dropped = [], []
    for b in got:
        if not b:
            continue
        r = analyse(b)
        if not r:
            dropped.append((b["sym"], "under 60 sessions of history"))
            continue
        why = []
        if r["ticker"] in blocked:
            why.append("restricted list")
        if r["atr_pct"] < MIN_ATR_PCT:
            why.append(f"ATR {r['atr_pct']}% < {MIN_ATR_PCT}%")
        if r["dollar_vol_20d"] < MIN_DOLLAR_VOL:
            why.append(f"$vol {r['dollar_vol_20d'] / 1e6:.1f}M < {MIN_DOLLAR_VOL / 1e6:.0f}M")
        if r["support_strength"] < 2:
            why.append("no tested support below the price")
        if r["reward_risk"] is None or r["reward_risk"] < 1.5:
            why.append(f"reward:risk {r['reward_risk']} < 1.5")
        if r["halted"]:
            why.append("a zero-volume session in the last 5 (halted): no entry")
        if why and r["ticker"] not in MUST_KEEP:
            dropped.append((r["ticker"], "; ".join(why)))
            continue
        r["note"] = "; ".join(why)
        rows.append(r)
    rows.sort(key=lambda r: (r["ticker"] not in MUST_KEEP, r["to_zone_pct"]))
    print(f"{'ticker':6} {'last':>9} {'ATR%':>5} {'buy zone':>17} {'stop':>9} {'sell zone':>17} {'R:R':>4} "
          f"{'to zone':>8} {'up':>5} {'risk':>5} {'vs50d':>6} {'120d':>6} str")
    for r in rows:
        print(f"{r['ticker']:6} {fmt(r['price']):>9} {r['atr_pct']:>5.1f} "
              f"{fmt(r['buy_zone'][0]):>8}-{fmt(r['buy_zone'][1]):<8} {fmt(r['stop']):>9} "
              f"{fmt(r['sell_zone'][0]):>8}-{fmt(r['sell_zone'][1]):<8} "
              f"{r['reward_risk'] or 0:>4.1f} {r['to_zone_pct']:>+7.1f}% {r['upside_to_target_pct']:>4.0f}% "
              f"{r['risk_to_stop_pct']:>4.0f}% {r['vs_sma50_pct']:>+5.0f}% {r['chg_120d_pct'] or 0:>+5.0f}% "
              f"{r['support_strength']}/{r['resistance_strength']} {r['note']}")
    print(f"\n{len(rows)} on the radar; dropped: " + ", ".join(f"{t} ({w})" for t, w in dropped))
    if len(rows) < a.min_names:
        print(f"WARNING: only {len(rows)} names (wanted {a.min_names}); widen the candidate list", file=sys.stderr)
    if a.save:
        now = pfm.now_utc()
        doc = {"generated_at": pfm.iso(now), "asof": max(r["asof"] for r in rows),
               "method": __doc__.split("Levels:")[1].strip(), "names": rows,
               "dropped": [{"ticker": t, "why": w} for t, w in dropped]}
        RADAR.write_text(json.dumps(doc, indent=1) + "\n")
        d = pfm.et_date(now).isoformat()
        out = ROOT / "research" / "radar"
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{d}.json").write_text(json.dumps(doc, indent=1) + "\n")
        md_rows = "\n".join(
            f"| {r['ticker']} | {fmt(r['price'])} | {r['atr_pct']:.1f}% | {fmt(r['buy_zone'][0])}-{fmt(r['buy_zone'][1])} "
            f"| {fmt(r['stop'])} | {fmt(r['sell_zone'][0])}-{fmt(r['sell_zone'][1])} | {r['reward_risk'] or 0:.1f} "
            f"| {r['to_zone_pct']:+.1f}% | {r['note']} |"
            for r in rows)
        (out / f"{d}.md").write_text(
            f"# Radar {d} (closes of {doc['asof']})\n\n| ticker | last | ATR% | buy zone | stop | sell zone | R:R "
            f"| to zone | flags |\n|---|---|---|---|---|---|---|---|---|\n{md_rows}\n")
        print(f"saved {RADAR.relative_to(ROOT)} and research/radar/{d}.md")
    return 0


STATUS_ORDER = ["buy", "bounce", "near", "wait", "target", "broken", "halted", "no quote"]
STATUS_TEXT = {"buy": "BUY ZONE", "bounce": "BOUNCE", "near": "NEAR", "wait": "WAIT", "target": "TARGET",
               "broken": "BROKEN", "halted": "HALTED", "no quote": "NO QUOTE"}


def classify(r: dict, q: dict | None, asof: str, near: float = 3.0) -> dict:
    """Where a radar name trades against its levels.
    buy     latest print inside the buy zone (above the stop)
    bounce  a session after the radar's bars touched the zone, price is back above it, entry reward:risk >= 1.5
    near    within `near` % above the zone
    target  at or above the sell-zone bottom
    broken  at or under the stop, or a later session traded through it: support failed, no buy
    halted  a zero-volume session in the radar's last 5 (a trading halt): its levels are flat halt prints, no buy
            (GPUS reopened Aug 25 after 6 halted sessions at 0.45 and fell 19% in 5 minutes; the replay bought it)
    The day's low counts only for a session after the radar's last bar (asof)."""
    if not q or q.get("price") is None:
        return {"status": "no quote"}
    if r.get("halted"):
        return {"status": "halted", "price": pfm.mark(q)[0], "day_low": None, "to_zone_pct": 0.0, "rr_now": None}
    px = pfm.mark(q)[0]
    lo, hi = r["buy_zone"]
    stop, sell_lo = r["stop"], r["sell_zone"][0]
    fresh = bool(q.get("time")) and pfm.et_date(pfm.parse_ts(q["time"])).isoformat() > asof
    low = q.get("day_low") if fresh else None
    rr_now = (sell_lo - px) / (px - stop) if px > stop else None
    if px <= stop or (low is not None and low <= stop):
        st = "broken"
    elif px >= sell_lo:
        st = "target"
    elif px <= hi:
        st = "buy"
    elif low is not None and low <= hi and rr_now is not None and rr_now >= 1.5:
        st = "bounce"
    elif px <= hi * (1 + near / 100):
        st = "near"
    else:
        st = "wait"
    return {"status": st, "price": px, "day_low": low, "to_zone_pct": round((px / hi - 1) * 100, 2),
            "rr_now": round(rr_now, 2) if rr_now is not None else None}


def check(a) -> int:
    radar = json.loads(RADAR.read_text())
    qdoc = json.loads((ROOT / ".cache" / "quotes.json").read_text())
    quotes = qdoc["quotes"]
    hits = {k: [] for k in STATUS_ORDER}
    for r in radar["names"]:
        c = classify(r, quotes.get(r["ticker"]), radar["asof"], a.near)
        if c["status"] == "no quote":
            hits["no quote"].append(r["ticker"])
            continue
        line = (f"{r['ticker']:6} {fmt(c['price']):>9} zone {fmt(r['buy_zone'][0])}-{fmt(r['buy_zone'][1])} "
                f"stop {fmt(r['stop'])} sell {fmt(r['sell_zone'][0])}-{fmt(r['sell_zone'][1])} "
                f"R:R now {c['rr_now'] if c['rr_now'] is not None else '-'} ({c['to_zone_pct']:+.1f}% vs zone top)")
        if c["day_low"] is not None:
            line += f" low {fmt(c['day_low'])}"
        q = quotes.get(r["ticker"]) or {}
        dip = None
        ref = pfm.ref_close(q)
        if ref and c["price"] and r.get("atr"):
            day = (c["price"] / ref - 1) * 100
            dip = day / (r["atr"] / c["price"] * 100)
            line += f" day {day:+.1f}% ({dip:+.2f} ATR)"
        if c["status"] in ("buy", "bounce") and c["price"]:
            line += f" size {size_pct(c['price'], r['stop'])}% of equity"
        if r["ticker"] in CRYPTO_LINKED:
            line += " [crypto]"
        hits[c["status"]].append((dip if dip is not None else 0.0, line))
    print(f"radar {radar['generated_at']} (closes of {radar['asof']}); quotes {qdoc['generated_at']}")
    for k in STATUS_ORDER:
        if k == "no quote":
            if hits[k]:
                print("NO QUOTE: " + ", ".join(hits[k]))
            continue
        if k == "wait" and not a.all:
            print(f"WAIT: {len(hits[k])}")
            continue
        print(f"{STATUS_TEXT[k]}: {len(hits[k])}" + (" (deepest dip first: the entry order, RUNBOOK 2a)" if k in ("buy", "bounce") else ""))
        for _, h in sorted(hits[k], key=lambda x: x[0]) if k in ("buy", "bounce") else hits[k]:
            print("  " + h)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("--tickers", default="")
    b.add_argument("--min-names", type=int, default=20)
    b.add_argument("--save", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("--near", type=float, default=3.0)
    c.add_argument("--all", action="store_true", help="also list names waiting above the zone")
    a = ap.parse_args()
    return build(a) if a.cmd == "build" else check(a)


if __name__ == "__main__":
    raise SystemExit(main())
