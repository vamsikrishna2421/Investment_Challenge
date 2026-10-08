#!/usr/bin/env python3
"""Strategy lab (Vamsi, Thu Oct 8: evolve the strategies, learn from the mistakes, come up with new ones): whole
strategies, not variants of the radar, tested on the same $1,000 / 22-session windows as replay.py.

  python scripts/strategy_lab.py [--windows 33] [--save]

Daily bars of the 68 candidates (5 years, replay.py's cache). Each session uses only what was known at the time:
the universe is the candidates passing the radar's filters at the prior close (ATR at least 4% of the price,
20-day dollar volume at least $15M, no zero-volume session in the last 5); ATR is the 14-session mean true range
before the day. Costs: trade.py's slippage table on every buy and sell (sr_backtest.slip); proceeds settle T+1
(a cash account: the paper book; the real book can reuse unsettled cash, so its results would be a little better).

Families:
  hold      buy-and-hold of the eligible universe, equal weights, bought at the window's first open: the drift
            the candidates gave anyone (the radar's results should be read against it)
  night     at the close (the 15:55 run), buy the names that fell `z`+ ATR from the prior close, deepest first,
            at most `slots`, `size` of equity each; sell at the next open (exit=open), the next close (exit=close)
            or the close `hold` sessions later (exit=days). Optional filters: `spy` (SPY down that % or more on the
            day: a market-wide sell-off, not one stock's bad news), `low` (closed in the lowest quarter of the range)
  mom       every `every` sessions at the open, hold the `slots` names with the best `look`-session return among
            the eligible (equal weights); optional `trend` (QQQ above its 20-day average at the prior close)
Caveats: today's candidate list (selection bias: these names are popular because they rose), the close and the
open priced at the daily bar (live: the 15:55 run price and the first trade), no news filter.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pickle
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levels as lv  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache" / "replay"


def load() -> dict:
    """The newest replay.py cache (daily bars of the candidates, SPY and QQQ)."""
    files = sorted(CACHE.glob("data2-*.pkl"))
    if not files:
        sys.exit("no replay cache: run python3 scripts/replay.py --days 5 first")
    return pickle.loads(files[-1].read_bytes())


def prep(data: dict) -> tuple[list[str], dict]:
    """Per session: each candidate's bar, prior close, ATR before the day and eligibility."""
    spy = data["daily"]["SPY"]
    days = [dt.datetime.fromtimestamp(r["t"], dt.timezone.utc).astimezone(pfm.ET).date().isoformat() for r in spy]
    pos = {d: i for i, d in enumerate(days)}
    table: dict[str, dict] = {d: {} for d in days}
    for s in lv.CANDIDATES + ["SPY", "QQQ"]:
        rows = data["daily"].get(s)
        if not rows:
            continue
        tr = [0.0] + [max(r["h"] - r["l"], abs(r["h"] - p["c"]), abs(r["l"] - p["c"])) for p, r in zip(rows, rows[1:])]
        for i in range(21, len(rows)):
            d = dt.datetime.fromtimestamp(rows[i]["t"], dt.timezone.utc).astimezone(pfm.ET).date().isoformat()
            if d not in pos:
                continue
            r, p = rows[i], rows[i - 1]
            atr = st.mean(tr[i - 14:i])
            dv = st.mean(x["c"] * x["v"] for x in rows[i - 20:i])
            ok = (s not in ("SPY", "QQQ") and p["c"] > 0 and atr / p["c"] * 100 >= lv.MIN_ATR_PCT and dv >= lv.MIN_DOLLAR_VOL
                  and all(x["v"] > 0 for x in rows[i - 5:i]) and abs(r["o"] / p["c"] - 1) < 0.6)
            sma20 = st.mean(x["c"] for x in rows[i - 20:i])
            table[d][s] = {"o": r["o"], "h": r["h"], "l": r["l"], "c": r["c"], "pc": p["c"], "atr": atr, "ok": ok,
                           "sma20_prev": sma20, "ret": {n: p["c"] / rows[i - 1 - n]["c"] - 1 for n in (5, 10, 20)
                                                      if i - 1 - n >= 0}}
    return days, table


class Book:
    """Cash, T+1 settlement, positions bought and sold at given prices with slippage."""

    def __init__(self, cash: float):
        self.cash, self.pending, self.pos, self.trades = cash, [], {}, []

    def settled(self, day: str) -> float:
        return self.cash - sum(a for d, a in self.pending if d > day)

    def buy(self, s: str, px: float, usd: float, day: str, extra: dict | None = None) -> None:
        fill = px * (1 + sb.slip(px))
        q = usd / fill
        self.cash -= usd
        self.pos[s] = {"q": q, "entry": fill, "day": day, **(extra or {})}

    def sell(self, s: str, px: float, day: str, settle: str) -> None:
        p = self.pos.pop(s)
        out = p["q"] * px * (1 - sb.slip(px))
        self.cash += out
        self.pending.append((settle, out))
        self.trades.append({"s": s, "in": p["day"], "out": day, "ret": out / (p["q"] * p["entry"]) - 1})

    def value(self, day_rows: dict, key: str = "c") -> float:
        return self.cash + sum(p["q"] * (day_rows.get(s) or {}).get(key, p["entry"]) for s, p in self.pos.items())


def run(days: list[str], table: dict, start: int, n: int, o: dict) -> dict:
    """One window: sessions days[start:start+n], $1,000."""
    sess = days[start:start + n]
    settle = {d: days[min(i + 1, len(days) - 1)] for i, d in enumerate(days)}
    book = Book(1000.0)
    fam = o["fam"]
    if fam == "hold":
        d0 = sess[0]
        elig = [s for s, r in table[d0].items() if r["ok"]]
        for s in elig:
            book.buy(s, table[d0][s]["o"], 1000.0 / len(elig) / (1 + 1e-9), d0)
    for k, d in enumerate(sess):
        T = table[d]
        if fam == "night":
            # the open: sell last night's buys (exit=open), or the ones due today
            for s in list(book.pos):
                p, r = book.pos[s], T.get(s)
                if r is None:
                    continue
                if o["exit"] == "open" and p["day"] != d:
                    book.sell(s, r["o"], d, settle[d])
            # the close: due exits, then new buys
            for s in list(book.pos):
                p, r = book.pos[s], T.get(s)
                if r is None or p["day"] == d:
                    continue
                held = days.index(d) - days.index(p["day"])
                if o["exit"] == "close" or (o["exit"] == "days" and held >= o["hold"]) or k == len(sess) - 1:
                    book.sell(s, r["c"], d, settle[d])
            if k == len(sess) - 1:
                continue
            spy = T.get("SPY")
            spy_day = (spy["c"] / spy["pc"] - 1) * 100 if spy else 0.0
            if o.get("spy") is not None and spy_day > -o["spy"]:
                continue
            cands = []
            for s, r in T.items():
                if not r["ok"] or s in book.pos or r["atr"] <= 0:
                    continue
                z = (r["c"] - r["pc"]) / r["atr"]
                low = (r["c"] - r["l"]) / (r["h"] - r["l"]) if r["h"] > r["l"] else 0.5
                if z <= -o["z"] and (not o.get("low") or low < 0.25):
                    cands.append((z, s))
            eq = book.value(T)
            slots = o["slots"] - len(book.pos)
            crypto = sum(1 for s in book.pos if s in lv.CRYPTO_LINKED)
            for z, s in sorted(cands):
                if slots <= 0:
                    break
                if s in lv.CRYPTO_LINKED and crypto >= o.get("max_crypto", 99):
                    continue
                usd = min(eq * o["size"], book.settled(d))
                if usd < 25:
                    break
                book.buy(s, T[s]["c"], usd, d)
                slots -= 1
                crypto += s in lv.CRYPTO_LINKED
        elif fam == "mom":
            if k % o["every"] == 0:
                q = T.get("QQQ")
                risk_on = not o.get("trend") or (q and q["pc"] > q["sma20_prev"])
                ranked = sorted(((r["ret"].get(o["look"], -9), s) for s, r in T.items() if r["ok"] and o["look"] in r["ret"]),
                                reverse=True)
                want = [s for _, s in ranked[:o["slots"]]] if risk_on else []
                for s in list(book.pos):
                    if s not in want and T.get(s):
                        book.sell(s, T[s]["o"], d, settle[d])
                eq = book.value(T, "o")
                for s in want:
                    if s in book.pos:
                        continue
                    usd = min(eq / o["slots"], book.settled(d))
                    if usd < 25:
                        break
                    book.buy(s, T[s]["o"], usd, d)
            if k == len(sess) - 1:
                for s in list(book.pos):
                    if T.get(s):
                        book.sell(s, T[s]["c"], d, settle[d])
    last = table[sess[-1]]
    final = book.value(last)
    spy = table[sess[-1]].get("SPY"), table[sess[0]].get("SPY")
    return {"ret": (final / 1000 - 1) * 100, "trades": book.trades,
            "spy": (spy[0]["c"] / spy[1]["pc"] - 1) * 100 if spy[0] and spy[1] else 0.0}


VARIANTS = [
    ("Buy-and-hold of the eligible candidates (the drift)", {"fam": "hold"}),
    ("Night: down 1.5+ ATR at the close, sell at the next open", {"fam": "night", "z": 1.5, "exit": "open", "slots": 4, "size": 0.25}),
    ("Night: down 2+ ATR, sell at the next open", {"fam": "night", "z": 2.0, "exit": "open", "slots": 4, "size": 0.25}),
    ("Night: down 1.5+ ATR, sell at the next close", {"fam": "night", "z": 1.5, "exit": "close", "slots": 4, "size": 0.25}),
    ("Night: down 1.5+ ATR, hold 3 sessions", {"fam": "night", "z": 1.5, "exit": "days", "hold": 3, "slots": 4, "size": 0.25}),
    ("Night: down 1.5+ ATR on a day SPY fell 0.5%+, next open", {"fam": "night", "z": 1.5, "exit": "open", "slots": 4, "size": 0.25, "spy": 0.5}),
    ("Night: down 1.5+ ATR on a day SPY fell 0.5%+, next close", {"fam": "night", "z": 1.5, "exit": "close", "slots": 4, "size": 0.25, "spy": 0.5}),
    ("Night: down 1.5+ ATR, closed in the lowest quarter, next open", {"fam": "night", "z": 1.5, "exit": "open", "slots": 4, "size": 0.25, "low": True}),
    ("Momentum: top 4 by 20-session return, weekly", {"fam": "mom", "look": 20, "every": 5, "slots": 4}),
    ("Momentum: top 4 by 10-session return, weekly", {"fam": "mom", "look": 10, "every": 5, "slots": 4}),
    ("Momentum: top 4 by 20 sessions, weekly, only with QQQ over its 20-day", {"fam": "mom", "look": 20, "every": 5, "slots": 4, "trend": True}),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--windows", type=int, default=33, help="separate 22-session windows ending at the last session")
    ap.add_argument("--len", type=int, default=22)
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    days, table = prep(load())
    now = pfm.now_utc()
    done = [d for d in days if d < pfm.et_date(now).isoformat() or now.astimezone(pfm.ET).hour >= 16]
    n_all = len(done)
    starts = [n_all - a.len * (k + 1) for k in range(a.windows)][::-1]
    starts = [s for s in starts if s >= 25]
    rows, out = [], []
    spy_w = None
    for title, o in VARIANTS:
        res = [run(days, table, s, a.len, o) for s in starts]
        r = sorted(x["ret"] for x in res)
        tr = [t["ret"] * 100 for x in res for t in x["trades"]]
        spy_w = [x["spy"] for x in res]
        beat = sum(1 for x in res if x["ret"] > x["spy"])
        rows.append(f"| {title} | {st.median(r):+.1f}% | {st.mean(r):+.1f}% | {r[0]:+.1f}% | {r[-1]:+.1f}% | {beat}/{len(r)} | "
                    f"{len(tr) / len(res):.0f} | {st.mean(tr) if tr else 0:+.2f}% | "
                    f"{sum(1 for t in tr if t > 0) / len(tr) * 100 if tr else 0:.0f}% |")
        out.append({"title": title, "options": o, "returns": [x["ret"] for x in res]})
    sp = sorted(spy_w)
    text = "\n".join([
        f"# Strategy lab: {len(starts)} separate windows of {a.len} sessions, {days[starts[0]]} to {done[-1]}", "",
        f"$1,000 each window; costs and T+1 settlement as in the `scripts/strategy_lab.py` docstring. S&P 500 over the "
        f"same windows: median {st.median(sp):+.1f}%, {sp[0]:+.1f}% to {sp[-1]:+.1f}%.", "",
        "| Strategy | Median | Mean | Worst window | Best window | Beat the S&P 500 | Trades per window | Average trade | Winners |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|"] + rows)
    print(text)
    if a.save:
        o_ = ROOT / "research" / "backtests"
        stem = f"lab-{done[-1]}-{len(starts)}x{a.len}"
        (o_ / f"{stem}.md").write_text(text + "\n")
        (o_ / f"{stem}.json").write_text(json.dumps(out, indent=1) + "\n")
        print("saved", (o_ / f"{stem}.md").relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
