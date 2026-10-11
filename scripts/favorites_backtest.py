#!/usr/bin/env python3
"""Buying prediction-market favorites (Vamsi, Oct 11: a viral post claims an AI bot made $290,000 on Polymarket with a
100% win rate over 168 trades by buying contracts priced 87-92 cents that settle at $1). Robinhood's event contracts
are Kalshi's, so the test uses Kalshi's public data (no account): markets settled in the last --days days in sports,
weather, economic-release and crypto/index series, hourly candles of the bid and ask.
  strategy  the first hourly close at least an hour before the market's close where one side's ask is 87-92 cents
            (YES at the yes ask, NO at 1 - the yes bid; a spread over 5 cents skipped), held to settlement
  calibration  each market's favorite side at the hour nearest 24 hours before its close: the price against the
            share that won, by price band (the favorite-longshot bias: Burgi, Deng and Whelan found Kalshi
            contracts over 50 cents earned a small positive return, those under 10 cents lost over 60%)
Fees: Robinhood's 1 cent a contract plus Kalshi's taker fee 0.07 x p x (1 - p) (unrounded, as on a large order);
'gross' is before fees. Returns per dollar staked, means +/- 95% clustered by settlement date. Markets are sampled
evenly by close time, up to --per markets a series with some volume; candles cached in .cache/kalshi_fav.
  python scripts/favorites_backtest.py [--days 60] [--per 150] [--save]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
import threading
import time
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
BASE = "https://api.elections.kalshi.com/trade-api/v2"
CACHE = ROOT / ".cache" / "kalshi_fav"
SERIES = {
    "sports": ["KXMLBGAME", "KXNFLGAME", "KXNCAAFGAME", "KXWNBAGAME", "KXMLSGAME", "KXEPLGAME", "KXUFCFIGHT",
               "KXATPMATCH", "KXWTAMATCH"],
    "weather": ["KXHIGHNY", "KXHIGHCHI", "KXHIGHMIA", "KXHIGHLAX", "KXHIGHAUS", "KXHIGHDEN"],
    "economic releases": ["KXCPI", "KXPAYROLLS", "KXU3", "KXFED", "KXJOBLESSCLAIMS"],
    "crypto and index": ["KXBTCD", "KXETHD", "KXINX"],
}
LO, HI, MAX_SPREAD = 0.87, 0.92, 0.05
BANDS = [(0.50, 0.60), (0.60, 0.70), (0.70, 0.80), (0.80, 0.87), (0.87, 0.92), (0.92, 0.97), (0.97, 1.00)]
_lock = threading.Lock()
_last = [0.0]


def get(path: str) -> dict:
    with _lock:  # about 6 requests a second
        wait = 0.17 - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
    for attempt in range(4):
        try:
            req = urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read())
        except Exception:  # noqa: BLE001
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    return {}


def num(x) -> float | None:
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def ts(s: str) -> int:
    return int(dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp())


def settled(series: str, start: int, end: int, cap: int = 4000) -> list[dict]:
    out, cursor = [], ""
    while len(out) < cap:
        r = get(f"/markets?series_ticker={series}&status=settled&limit=1000&min_close_ts={start}&max_close_ts={end}"
                + (f"&cursor={cursor}" if cursor else ""))
        out += r.get("markets", [])
        cursor = r.get("cursor") or ""
        if not cursor:
            break
    return [m for m in out if m.get("result") in ("yes", "no") and (num(m.get("volume_fp")) or 0) >= 1000]


def candles(series: str, m: dict) -> list[dict]:
    f = CACHE / f"{m['ticker']}.json"
    if f.exists():
        return json.loads(f.read_text())
    close = ts(m["close_time"])
    start = max(ts(m["open_time"]), close - 72 * 3600) if m.get("open_time") else close - 72 * 3600
    r = get(f"/series/{series}/markets/{m['ticker']}/candlesticks?start_ts={start}&end_ts={close}&period_interval=60")
    out = []
    for c in r.get("candlesticks", []):
        a, b = num((c.get("yes_ask") or {}).get("close_dollars")), num((c.get("yes_bid") or {}).get("close_dollars"))
        if a is not None and b is not None:
            out.append({"t": c["end_period_ts"], "ask": a, "bid": b})
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(out))
    return out


def fee(p: float) -> float:
    return 0.01 + 0.07 * p * (1 - p)


def trade(side: str, p: float, result: str) -> dict:
    win = side == result
    f = fee(p)
    return {"win": win, "price": p, "gross": ((1.0 if win else 0.0) - p) / p,
            "net": ((1.0 if win else 0.0) - p - f) / (p + f)}


def study(series: str, m: dict) -> dict | None:
    try:
        cs = candles(series, m)
    except Exception:  # noqa: BLE001
        return None
    close = ts(m["close_time"])
    ok = [c for c in cs if c["t"] <= close - 3600 and 0 < c["bid"] < c["ask"] < 1 and c["ask"] - c["bid"] <= MAX_SPREAD]
    if not ok:
        return None
    day = dt.datetime.fromtimestamp(close, dt.timezone.utc).date().isoformat()
    out = {"series": series, "ticker": m["ticker"], "date": day, "result": m["result"]}
    for c in ok:  # the strategy: the first hour a side's ask sits at 87-92 cents
        if LO <= c["ask"] <= HI:
            out["strategy"] = {**trade("yes", c["ask"], m["result"]), "hours_left": round((close - c["t"]) / 3600)}
            break
        if LO <= 1 - c["bid"] <= HI:
            out["strategy"] = {**trade("no", 1 - c["bid"], m["result"]), "hours_left": round((close - c["t"]) / 3600)}
            break
    snap = min(ok, key=lambda c: abs(close - 24 * 3600 - c["t"]))  # calibration: the favorite near 24 hours out
    side, p = ("yes", snap["ask"]) if snap["ask"] >= 0.5 else ("no", 1 - snap["bid"])
    if p >= 0.5:
        out["calib"] = trade(side, p, m["result"])
    return out


def summarize(rows: list[dict], key: str) -> dict:
    xs = [r for r in rows if key in r]
    if not xs:
        return {"n": 0}
    t = [r[key] for r in xs]
    wins = sum(x["win"] for x in t)
    s = {"n": len(t), "win_rate": round(100 * wins / len(t), 1), "avg_price": round(sum(x["price"] for x in t) / len(t), 3),
         "breakeven": round(100 * sum(x["price"] + fee(x["price"]) for x in t) / len(t), 1)}
    for k in ("gross", "net"):
        m, se = cb.clustered([(r["date"], r[key][k]) for r in xs])
        s[k] = (round(100 * m, 2), round(196 * se, 2) if not math.isnan(se) else None)
    s["p168"] = (wins / len(t)) ** 168
    s["worst"] = round(100 * min(x["net"] for x in t), 1)
    return s


def report(res: dict) -> str:
    lines = [f"# Buying prediction-market favorites, {res['asof']}", "",
             f"Kalshi markets settled {res['start']} to {res['end']}: {res['markets']} sampled from {len(res['series'])} "
             f"series, {res['with_candles']} with usable hourly quotes. Method in the `scripts/favorites_backtest.py` "
             f"docstring. Returns % of the money staked per contract held to settlement; 'net' after Robinhood's 1 cent "
             f"and Kalshi's fee; ± 95% clustered by settlement date. Break-even is the win rate that returns zero after fees.",
             "", "## The 87-92 cent strategy", "",
             "| group | trades | won | break-even | avg price | return gross | return net | worst trade | 168 straight wins |",
             "|---|---|---|---|---|---|---|---|---|"]

    def row(name, s):
        if not s.get("n"):
            return f"| {name} | 0 | - | - | - | - | - | - | - |"
        g, n_ = s["gross"], s["net"]
        ci = lambda v: f"{v[0]:+.2f} ± {v[1]:.2f}" if v[1] is not None else f"{v[0]:+.2f}"  # noqa: E731
        return (f"| {name} | {s['n']} | {s['win_rate']}% | {s['breakeven']}% | {s['avg_price']:.3f} | {ci(g)} | {ci(n_)} | "
                f"{s['worst']}% | {s['p168']:.2e} |")

    lines.append(row("all", res["strategy"]["all"]))
    for g, s in res["strategy"]["groups"].items():
        lines.append(row(g, s))
    lines += ["", "## Calibration: the favorite 24 hours before the close", "",
              "| price band | markets | won | break-even | return gross | return net |", "|---|---|---|---|---|---|"]
    for band, s in res["calibration"].items():
        if s.get("n"):
            lines.append(f"| {band} | {s['n']} | {s['win_rate']}% | {s['breakeven']}% | {s['gross'][0]:+.2f} ± "
                         f"{s['gross'][1] or 0:.2f} | {s['net'][0]:+.2f} ± {s['net'][1] or 0:.2f} |")
    lines += ["", "## Reading", ""] + res.get("reading", [])
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--per", type=int, default=150, help="markets sampled per series")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    end = int(time.time())
    start = end - a.days * 86400
    picks = []
    for group, ss in SERIES.items():
        for s in ss:
            try:
                ms = sorted(settled(s, start, end), key=lambda m: m["close_time"])
            except Exception as e:  # noqa: BLE001
                print(f"  {s}: {str(e)[:60]}", file=sys.stderr)
                continue
            step = max(1, len(ms) // a.per)
            picks += [(group, s, m) for m in ms[::step][:a.per]]
            print(f"  {s}: {len(ms)} settled with volume, {len(ms[::step][:a.per])} sampled", file=sys.stderr)
    with ThreadPoolExecutor(12) as ex:
        got = list(ex.map(lambda x: (x[0], study(x[1], x[2])), picks))
    rows = [{**r, "group": g} for g, r in got if r]
    res = {"asof": dt.date.today().isoformat(),
           "start": dt.datetime.fromtimestamp(start, dt.timezone.utc).date().isoformat(),
           "end": dt.datetime.fromtimestamp(end, dt.timezone.utc).date().isoformat(),
           "series": [s for ss in SERIES.values() for s in ss], "markets": len(picks), "with_candles": len(rows),
           "strategy": {"all": summarize(rows, "strategy"),
                        "groups": {g: summarize([r for r in rows if r["group"] == g], "strategy") for g in SERIES}},
           "calibration": {f"{lo:.2f}-{hi:.2f}": summarize([r for r in rows if "calib" in r and lo <= r["calib"]["price"] < hi
                                                            or ("calib" in r and hi == 1.0 and r["calib"]["price"] >= lo)],
                                                           "calib") for lo, hi in BANDS}}
    text = report(res)
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests" / f"kalshi-favorites-{res['asof']}"
        out.with_suffix(".json").write_text(json.dumps(res, indent=2) + "\n")
        out.with_suffix(".md").write_text(text)
        print(f"saved {out.with_suffix('.md').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
