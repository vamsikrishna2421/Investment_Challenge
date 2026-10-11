#!/usr/bin/env python3
"""In-match swings (Vamsi, Oct 11: buy a tennis player at 30 cents while behind; if the match swings and the player
reaches 60 cents, buy the other player at 40 cents, so whoever wins pays $1 on 70 cents staked; or simply sell at
60). Kalshi's public trade history of settled ATP and WTA match markets (no account), one market per match:
  entry   the first trade at or under ENTRY cents on either player (bought at that price plus 1 cent of spread)
  swing   a later trade at or over TARGET on the same player: the other player is bought at 100 - that price plus 1
          cent, which locks the payout (selling there is the same trade)
  else    held to the result: $1 if the player wins, nothing if not
Fees: Robinhood's 1 cent a contract on each leg plus Kalshi's taker fee 0.07 x p x (1 - p) on each leg; 'gross' is
before fees and spread. Benchmark: if prices are fair, a player bought at E reaches T before losing with probability
E/T (a fair price can't drift), which makes the strategy worth zero before costs.
Split by the pre-match price (the median of the match market's first 30 trades, made before play): evenly
matched when both players opened between 35 and 65 cents (Vamsi's follow-up: only close matches), a clear
favorite otherwise.
Returns per dollar of the first leg, means +/- 95% clustered by match date. Markets sampled evenly by close time,
up to --per a series with some volume; trades cached in .cache/kalshi_trades.
  python scripts/swing_backtest.py [--days 60] [--per 200] [--series KXATPMATCH,KXWTAMATCH] [--save]
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
import clue_backtest as cb  # noqa: E402
import favorites_backtest as fb  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache" / "kalshi_trades"
SPREAD = 0.01
# Oct 11: Vamsi's follow-ups, buy under 15 cents and sell once it crosses 20; then buy inside 35-40 cents (close
# contests) and sell at 45 or 50. Each rule is (lowest entry, highest entry, exit); 0 = any price at or under the high.
PAIRS = [(0.0, 0.30, 0.60), (0.0, 0.20, 0.40), (0.0, 0.30, 0.50), (0.0, 0.40, 0.60), (0.0, 0.10, 0.30), (0.0, 0.20, 0.60),
         (0.0, 0.15, 0.20), (0.0, 0.15, 0.25), (0.35, 0.40, 0.45), (0.35, 0.40, 0.50)]


def rule_key(lo: float, hi: float, t: float) -> str:
    return (f"{lo:.2f}_" if lo else "") + f"{hi:.2f}-{t:.2f}"


def trades(m: dict) -> list[tuple[int, float]]:
    """(unix time, yes price) of every trade of 1+ contract, oldest first (dust trades of a fraction of a contract
    print at stale prices)."""
    f = CACHE / f"{m['ticker']}.json"
    if f.exists():
        return [tuple(x) for x in json.loads(f.read_text())]
    out, cursor = [], ""
    for _ in range(40):
        r = fb.get(f"/markets/trades?ticker={m['ticker']}&limit=1000" + (f"&cursor={cursor}" if cursor else ""))
        for t in r.get("trades", []):
            p = fb.num(t.get("yes_price_dollars"))
            if p is None and t.get("yes_price") is not None:
                p = fb.num(t["yes_price"]) / 100
            n = fb.num(t.get("count_fp")) or fb.num(t.get("count")) or 0
            if p is not None and t.get("created_time") and n >= 1:
                out.append((fb.ts(t["created_time"]), p))
        cursor = r.get("cursor") or ""
        if not cursor:
            break
    out.sort()
    CACHE.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(out))
    return out


def leg_cost(p: float, net: bool) -> float:
    return p + SPREAD + fb.fee(p + SPREAD) if net else p


def simulate(path: list[tuple[int, float]], result: str, entry: float, target: float, net: bool,
             lo: float = 0.0) -> dict | None:
    side, k0, buy = None, None, None
    for k, (_, y) in enumerate(path):
        if lo <= y <= entry:
            side, k0, buy = "yes", k, y
            break
        if lo <= 1 - y <= entry:
            side, k0, buy = "no", k, 1 - y
            break
    if side is None:
        return None
    c1 = leg_cost(buy, net)
    for _, y in path[k0 + 1:]:
        mine = y if side == "yes" else 1 - y
        if mine >= target:
            c2 = leg_cost(1 - mine, net)
            return {"swing": True, "won": None, "ret": (1.0 - c1 - c2) / c1, "buy": buy}
    won = side == result
    return {"swing": False, "won": won, "ret": ((1.0 if won else 0.0) - c1) / c1, "buy": buy}


def run_market(m: dict) -> dict | None:
    try:
        path = trades(m)
    except Exception:  # noqa: BLE001
        return None
    if len(path) < 20:
        return None
    day = dt.datetime.fromtimestamp(fb.ts(m["close_time"]), dt.timezone.utc).date().isoformat()
    first = sorted(p for _, p in path[:30])
    out = {"ticker": m["ticker"], "date": day, "trades": len(path), "result": m["result"],
           "p0": first[len(first) // 2]}
    for lo, e, t in PAIRS:
        for net in (True, False):
            r = simulate(path, m["result"], e, t, net, lo)
            if r:
                out[rule_key(lo, e, t) + ("" if net else "_g")] = r
    return out


def stats(rows: list[dict], key: str, target: float) -> dict:
    xs = [(r["date"], r[key]) for r in rows if key in r]
    if not xs:
        return {"n": 0}
    fair = 100 * sum(min(1.0, x["buy"] / target) for _, x in xs) / len(xs)
    m, se = cb.clustered([(d, x["ret"]) for d, x in xs])
    swings = sum(x["swing"] for _, x in xs)
    held = [x for _, x in xs if not x["swing"]]
    return {"n": len(xs), "swing_pct": round(100 * swings / len(xs), 1),
            "held_won_pct": round(100 * sum(x["won"] for x in held) / len(held), 1) if held else None,
            "avg_buy": round(sum(x["buy"] for _, x in xs) / len(xs), 3),
            "ret": round(100 * m, 2), "ci": round(196 * se, 2) if not math.isnan(se) else None, "fair": round(fair, 1)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--days", type=int, default=60)
    ap.add_argument("--per", type=int, default=200)
    ap.add_argument("--series", default="KXATPMATCH,KXWTAMATCH")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    import time  # noqa: PLC0415
    end = int(time.time())
    start = end - a.days * 86400
    picks = []
    for s in a.series.split(","):
        ms = sorted(fb.settled(s, start, end), key=lambda m: m["close_time"])
        one = {}
        for m in ms:  # one market per match: the two players' markets mirror each other
            one.setdefault(m["event_ticker"], m)
        ms = list(one.values())
        step = max(1, len(ms) // a.per)
        picks += ms[::step][:a.per]
        print(f"  {s}: {len(ms)} matches settled, {len(ms[::step][:a.per])} sampled", file=sys.stderr)
    with ThreadPoolExecutor(8) as ex:
        rows = [r for r in ex.map(run_market, picks) if r]
    groups = {"all matches": rows,
              "evenly matched (both opened 35-65 cents)": [r for r in rows if 0.35 <= r["p0"] <= 0.65],
              "clear favorite (opened outside 35-65 cents)": [r for r in rows if not 0.35 <= r["p0"] <= 0.65]}
    res = {"asof": dt.date.today().isoformat(), "series": a.series, "matches": len(rows),
           "start": dt.datetime.fromtimestamp(start, dt.timezone.utc).date().isoformat(),
           "end": dt.datetime.fromtimestamp(end, dt.timezone.utc).date().isoformat(),
           "groups": {g: {rule_key(lo, e, t): {"net": stats(rs, rule_key(lo, e, t), t),
                                                "gross": stats(rs, rule_key(lo, e, t) + "_g", t)} for lo, e, t in PAIRS}
                      for g, rs in groups.items()},
           "group_sizes": {g: len(rs) for g, rs in groups.items()}}
    lines = [f"# In-match swing trading on Kalshi tennis, {res['asof']}", "",
             f"{res['matches']} settled ATP/WTA match markets with trade history, {res['start']} to {res['end']}; method in "
             f"the `scripts/swing_backtest.py` docstring. Returns per dollar of the first leg; ± 95% clustered by date. "
             f"'Fair odds' is the share that would reach the target if prices were fair: the actual entry price over the target, "
             f"averaged (the first trade under the threshold is often well under it, after a jump)."]
    for g, pairs in res["groups"].items():
        lines += ["", f"## {g}: {res['group_sizes'][g]} matches", "",
                  "| buy at, sell at | matches entered | reached the target | fair odds | won when held | "
                  "return gross | return net (spread and fees) |", "|---|---|---|---|---|---|---|"]
        for k, v in pairs.items():
            gr, n_ = v["gross"], v["net"]
            if not n_.get("n"):
                continue
            ent, t = k.split("-")
            lo_, _, e = ent.rpartition("_")
            label = (f"{float(lo_) * 100:.0f}-" if lo_ else "") + f"{float(e) * 100:.0f}c, {float(t) * 100:.0f}c"
            lines.append(f"| {label} | {n_['n']} | {gr['swing_pct']}% | "
                         f"{gr['fair']}% | {gr['held_won_pct']}% | {gr['ret']:+.1f}% ± {gr['ci'] or 0:.1f} | "
                         f"{n_['ret']:+.1f}% ± {n_['ci'] or 0:.1f} |")
    lines += ["", "## Reading", ""]
    text = "\n".join(lines) + "\n"
    print(text)
    if a.save:
        out = ROOT / "research" / "backtests" / f"kalshi-swings-{res['asof']}"
        out.with_suffix(".json").write_text(json.dumps(res, indent=2) + "\n")
        out.with_suffix(".md").write_text(text)
        print(f"saved {out.with_suffix('.md').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
