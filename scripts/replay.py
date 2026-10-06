#!/usr/bin/env python3
"""Practice ground: replay the paper rules over past sessions as if live (Vamsi, Mon Oct 5: practice the rules on
the last 30 trading days without looking at what happened, learn from the bad cases, and refine the strategy).

  python scripts/replay.py [--days 30] [--limit support|top|none] [--stop-atr 0.6] [--btc-gate on|off]
                           [--rank dip|rr] [--runs on|off] [--max-hold N] [--entry radar|gap]
                           [--limit-until 600] [--tested-only on|off] [--end YYYY-MM-DD]
  python scripts/replay.py --grid [--days 30] [--end ...] [--save]   # the rule variants side by side
  python scripts/replay.py --grid --windows [--days 30] [--save]     # ... over every window in the data

Each session D, using only what was known at that moment (entry=radar, the live rules of Oct 6):
  8:40   the radar is rebuilt from the daily closes up to D-1 (levels.analyse and the radar's filters; GPUS, IREN
         and BTDR kept; a name with a zero-volume day in the last 5 sessions is skipped as halted); resting DAY
         buy limits go in for the free slots (4 positions plus orders), 25% of equity each (cut so a stop loses
         at most levels.RISK_PCT % of equity; the Oct 6 reports used plain 25%) from settled cash, at
         support (or the zone top) for names within 8% of support with R:R 1.5+ from the limit, higher R:R
         first; crypto-linked names at most 2 and only while the bitcoin gate is open (bitcoin at 8:40 above its
         20-day average, down less than 2% on the day and 5% over 3 days: orders.btc_gate).
  9:30   a buy order is cancelled if the stock opens at or under its stop (the 9:25 pre-market check).
  bars   5-minute bars in time order: a limit fills when a bar trades 1 cent through it (at the limit, or the
         bar's open if lower); a stop sells when a bar trades at or under it (at the stop or a lower open, less
         slippage); a fill and a stop in the same bar count as both (the cautious reading).
  runs   at :10, :25, :40 and :55 from 9:55: a position at or above its sell-zone bottom sells at the run price;
         free slots and settled cash buy names in BUY ZONE or BOUNCE with R:R 1.5+ at the run price, the deepest
         dip against the prior close first (or higher R:R), no re-entry in a name stopped out that day.
  16:00  DAY orders expire; proceeds settle the next business day (T+1); positions are held overnight.
entry=gap tests the one entry with an edge in dip_backtest.py: at the open, buy the candidates passing the radar's
ATR and dollar-volume filters that open 0.5+ ATR under the prior close, deepest gap first, and sell at the prior
close if it trades there, otherwise at the last bar (no stop, as in the backtest).
Slippage from trade.py's table; sell fees from the book's config. No news filter (an offering or bad company
news would have cancelled some entries live). A run sees the price at the end of a 5-minute bar.
Caveats: today's candidate list (selection bias: these names are popular now), and 30 sessions is one market.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pickle
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clue_backtest as cb  # noqa: E402
import levels as lv  # noqa: E402
import marketdata as md  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
CACHE = ROOT / ".cache" / "replay"
SLOTS, SIZE, MAX_CRYPTO, NEAR, TICK, GAP_ATR = 4, 0.25, 2, 8.0, 0.01, 0.5
RUN_BARS = set(range(590, 960, 15))  # bars starting 9:50, 10:05, ...: they end at the :55, :10, :25, :40 runs
LAST_BAR = 955
DEFAULTS = {"limit": "support", "stop_atr": 0.6, "btc_gate": "on", "rank": "dip", "runs": "on", "max_hold": 0,
            "entry": "radar", "limit_until": 960, "tested_only": "off", "entry_until": 960, "entry_from": 0, "risk_pct": lv.RISK_PCT,
            "protect": "none", "protect_at": 1.0, "protect_trail": 1.0}
GRID = [
    ("Live rules: limits at support, stop 0.6 ATR under it", {}),
    ("Limits at the zone top", {"limit": "top"}),
    ("No resting limits: run entries only (the Oct 5 rules)", {"limit": "none"}),
    ("Resting limits only, no run entries", {"runs": "off"}),
    ("Stop 1.0 ATR under support", {"stop_atr": 1.0}),
    ("Stop 1.5 ATR under support", {"stop_atr": 1.5}),
    ("Sell after 3 sessions if neither target nor stop", {"max_hold": 3}),
    ("Bitcoin gate off", {"btc_gate": "off"}),
    ("Rank run entries by R:R instead of dip", {"rank": "rr"}),
    ("Opening gap-down 0.5+ ATR, sell at the prior close or the close", {"entry": "gap"}),
    ("Limits cancelled at 10:00 (the first 30 minutes), runs after", {"limit_until": 600}),
    ("GPUS, IREN, BTDR only with a tested support", {"tested_only": "on"}),
    ("Both of the above", {"limit_until": 600, "tested_only": "on"}),
    ("Both, stop 1.0 ATR under support", {"limit_until": 600, "tested_only": "on", "stop_atr": 1.0}),
    ("Run entries only, GPUS/IREN/BTDR only with a tested support", {"limit": "none", "tested_only": "on"}),
]


TIMES = [
    ("Live rules: entries all day", {}),
    ("Entries until 10:30: limits cancelled then, no later run buys", {"entry_until": 630}),
    ("Entries until 11:00", {"entry_until": 660}),
    ("Entries until 10:30, run entries only (no resting limits)", {"entry_until": 630, "limit": "none"}),
    ("Entries until 10:30, limits only (no run buys)", {"entry_until": 630, "runs": "off"}),
    ("No entries before 10:30 (the reverse)", {"entry_from": 630}),
]
SIZING = [
    ("25% of equity a position (the rule before Oct 6)", {"risk_pct": 0.0}),
    ("Risk 1% of equity to the stop, at most 25%", {"risk_pct": 1.0}),
    ("Risk 1.5% of equity to the stop, at most 25%", {"risk_pct": 1.5}),
    ("Risk 2% of equity to the stop, at most 25%", {"risk_pct": 2.0}),
]
STOPS = [(f"Stop {x} ATR under support{' (live)' if x == 0.6 else ''}", {"stop_atr": x}) for x in (0.6, 0.8, 1.0, 1.2, 1.5)]
# Protecting open gains (Vamsi, Oct 6: plan the exits so the book doesn't give back its gains): once a position's best
# price since entry is protect_at ATR over the entry, its resting stop rises to the entry (be) or to protect_trail ATR
# under that best price (trail), never lower than before; it works from the next bar.
EXITS = [
    ("Live rules: hold to the target or the plan stop", {}),
    ("Stop to break-even after +0.5 ATR", {"protect": "be", "protect_at": 0.5}),
    ("Stop to break-even after +1 ATR", {"protect": "be", "protect_at": 1.0}),
    ("Trail 0.75 ATR under the high after +0.5 ATR", {"protect": "trail", "protect_at": 0.5, "protect_trail": 0.75}),
    ("Trail 0.5 ATR under the high after +1 ATR", {"protect": "trail", "protect_at": 1.0, "protect_trail": 0.5}),
    ("Trail 1 ATR under the high after +1 ATR", {"protect": "trail", "protect_at": 1.0, "protect_trail": 1.0}),
    ("Trail 1.5 ATR under the high after +1.5 ATR", {"protect": "trail", "protect_at": 1.5, "protect_trail": 1.5}),
]


def by_day(r: dict) -> dict:
    """Regular-session bars per ET date: (minute of day at bar start, open, high, low, close)."""
    q = ((r.get("indicators") or {}).get("quote") or [{}])[0]
    out: dict[str, list] = {}
    for i, t in enumerate(r.get("timestamp") or []):
        o, h, lo, c = (q.get(k, [None] * (i + 1))[i] for k in ("open", "high", "low", "close"))
        if None in (o, h, lo, c):
            continue
        d = dt.datetime.fromtimestamp(t, dt.timezone.utc).astimezone(pfm.ET)
        m = d.hour * 60 + d.minute
        if 570 <= m < 960:
            out.setdefault(d.date().isoformat(), []).append((m, float(o), float(h), float(lo), float(c)))
    return out


def load_data(syms: list[str], refresh: bool) -> dict:
    """Daily bars (5 years), 5-minute bars (60 sessions), hourly bars (2 years) and bitcoin, cached per day in
    .cache/replay."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"data2-{pfm.et_date(pfm.now_utc()).isoformat()}.pkl"
    if p.exists() and not refresh:
        return pickle.loads(p.read_bytes())

    def one(sym):
        daily = sb.daily(sym, "5y")
        got = []
        for rng, iv in (("60d", "5m"), ("730d", "1h")):
            try:
                got.append(by_day(md.yahoo_chart(sym, rng, iv, False)))
            except Exception:  # noqa: BLE001
                got.append({})
        return sym, daily, *got

    with ThreadPoolExecutor(8) as ex:
        got = list(ex.map(one, syms + ["SPY", "QQQ"]))

    def series(r):
        q = ((r.get("indicators") or {}).get("quote") or [{}])[0]
        return [(t, c) for t, c in zip(r.get("timestamp") or [], q.get("close") or []) if c]

    data = {"daily": {s: d for s, d, _, _ in got if d}, "5m": {s: m for s, _, m, _ in got if m},
            "1h": {s: h for s, _, _, h in got if h},
            "btc_daily": series(md.yahoo_chart("BTC-USD", "5y", "1d", False)),
            "btc_hourly": series(md.yahoo_chart("BTC-USD", "730d", "1h", False))}
    p.write_bytes(pickle.dumps(data))
    return data


def et_day(t: int) -> str:
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).astimezone(pfm.ET).date().isoformat()


def hhmm(m: int) -> str:
    return f"{m // 60}:{m % 60:02d}"


def btc_gate(data: dict, day: str) -> dict:
    """orders.btc_gate at 8:40 AM ET on `day`: the last full hourly bar against the daily closes of the UTC days
    before (bitcoin's daily bars run 00:00-24:00 UTC)."""
    at = dt.datetime.fromisoformat(day).replace(hour=8, minute=40, tzinfo=pfm.ET).timestamp()
    day0 = dt.datetime.fromisoformat(day).replace(tzinfo=dt.timezone.utc).timestamp()
    hit = next(((t, c) for t, c in reversed(data["btc_hourly"]) if t + 3600 <= at), None)
    closes = [c for t, c in data["btc_daily"] if t < day0]
    if len(closes) < 21:
        return {"ok": False, "d1": None, "d3": None}
    # before the hourly data starts (Oct 2024), the prior UTC day's close stands in for the 8:40 price
    px = hit[1] if hit and at - hit[0] < 86400 else closes[-1]
    sma = sum(closes[-20:]) / 20
    d1, d3 = (px / closes[-1] - 1) * 100, (px / closes[-3] - 1) * 100
    return {"ok": px > sma and d1 > -2 and d3 > -5, "d1": round(d1, 2), "d3": round(d3, 2)}


_RADAR: dict = {}


def radar_for(data: dict, idx: dict, names: list[str], day: str, stop_atr: float) -> tuple[dict, dict]:
    """The radar a 16:20 rebuild would have produced from the closes up to the session before `day`, and the ATR
    of every candidate passing the ATR and dollar-volume filters (the gap entry's universe)."""
    key = (id(data), day, stop_atr)
    if key not in _RADAR:
        _RADAR[key] = _radar_for(data, idx, names, day, stop_atr)
    radar, elig = _RADAR[key]
    return {k: dict(v) for k, v in radar.items()}, dict(elig)


def _radar_for(data: dict, idx: dict, names: list[str], day: str, stop_atr: float) -> tuple[dict, dict]:
    radar, elig = {}, {}
    for s in names:
        i = idx[s].get(day)
        rows = data["daily"][s]
        if i is None or i < 120 or any(r["v"] == 0 for r in rows[i - 5:i]):
            continue
        r = lv.analyse({"sym": s, "rows": rows[max(0, i - 250):i], "name": s, "exchange": "", "type": ""}, stop_atr)
        if not r:
            continue
        liquid = r["atr_pct"] >= lv.MIN_ATR_PCT and r["dollar_vol_20d"] >= lv.MIN_DOLLAR_VOL
        if liquid:
            elig[s] = r["atr"]
        if not (liquid and r["support_strength"] >= 2 and (r["reward_risk"] or 0) >= 1.5) and s not in lv.MUST_KEEP:
            continue
        S, Z = r["buy_zone"]
        radar[s] = {"S": S, "Z": Z, "stop": S - stop_atr * r["atr"], "target": r["sell_zone"][0], "atr": r["atr"],
                    "strength": r["support_strength"], "crypto": s in lv.CRYPTO_LINKED}
    return radar, elig


class Book:
    def __init__(self, cash: float, cfg: dict):
        self.cash, self.cfg = cash, cfg
        self.pending: list[tuple[str, float]] = []  # (settle day, amount)
        self.pos: dict[str, dict] = {}
        self.orders: list[dict] = []
        self.trades: list[dict] = []
        self.stopped_today: set[str] = set()
        self.placed = self.filled = 0

    def settled(self, day: str) -> float:
        return self.cash - sum(a for d, a in self.pending if d > day)

    def free_cash(self, day: str) -> float:
        return self.settled(day) - sum(o["usd"] for o in self.orders)

    def buy(self, tk, px, usd, day, n, minute, kind, ctx):
        qty = usd / px
        self.cash -= qty * px
        self.pos[tk] = {"qty": qty, "entry": px, "day": day, "n": n, "minute": minute, "kind": kind, "hi": px,
                        "lo": px, **ctx}

    def sell(self, tk, px, day, minute, why, settle):
        p = self.pos.pop(tk)
        gross = p["qty"] * px
        fees = pfm.sell_fees(p["qty"], gross, self.cfg)
        self.cash += gross - fees
        self.pending.append((settle, gross - fees))
        a = p["atr"]
        self.trades.append({**{k: v for k, v in p.items() if k not in ("qty", "hi", "lo", "n")}, "ticker": tk,
                            "exit": round(px, 4), "exit_day": day, "exit_minute": minute, "why": why,
                            "ret_pct": round(((gross - fees) / (p["qty"] * p["entry"]) - 1) * 100, 2),
                            "pnl": round(gross - fees - p["qty"] * p["entry"], 2),
                            "best_atr": round((p["hi"] - p["entry"]) / a, 2),
                            "worst_atr": round((p["lo"] - p["entry"]) / a, 2)})
        if why == "stop":
            self.stopped_today.add(tk)


def replay(data: dict, days: int, o: dict, cash: float = 1000.0, end: str | None = None, res: str = "5m") -> dict:
    """res "1h" replays on hourly bars (2 years): a run at the end of each hour, and a limit cancel before 10:30
    happens at 10:30, the end of the first bar."""
    src = data[res]
    step, runs_at, last_bar = (5, RUN_BARS, LAST_BAR) if res == "5m" else (60, set(range(570, 960, 60)), 930)
    cfg = pfm.load_config()
    blocked = set(json.loads((ROOT / "config" / "blocklist.json").read_text()).get("tickers", {}))
    now = pfm.now_utc()
    today = pfm.et_date(now).isoformat()
    closed = now.astimezone(pfm.ET).hour >= 16
    all_days = sorted(d for d in src.get("SPY", {}) if d < today or (d == today and closed))
    sessions = [d for d in all_days if not end or d <= end][-days:]
    settle = {d: all_days[i + 1] if i + 1 < len(all_days) else pfm.next_business_day(dt.date.fromisoformat(d)).isoformat()
              for i, d in enumerate(all_days)}
    idx = {s: {et_day(r["t"]): i for i, r in enumerate(rows)} for s, rows in data["daily"].items()}
    names = [s for s in lv.CANDIDATES if s in data["daily"] and s in src and s not in blocked]
    book = Book(cash, cfg)
    curve = []
    for n, day in enumerate(sessions):
        book.stopped_today = set()
        gate = btc_gate(data, day) if o["btc_gate"] == "on" else {"ok": True, "d1": None, "d3": None}
        radar, elig = radar_for(data, idx, names, day, o["stop_atr"])
        if o["entry"] == "gap":
            radar = {}
        bars, prev, close = {}, {}, {}
        for s in set(radar) | set(elig) | set(book.pos):
            i = idx[s].get(day)
            b = src.get(s, {}).get(day)
            if i is None or not b or abs(b[0][1] / data["daily"][s][i]["o"] - 1) > 0.2:  # no bars, or a split mismatch
                continue
            bars[s] = {x[0]: x for x in b}
            prev[s], close[s] = data["daily"][s][i - 1]["c"], data["daily"][s][i]["c"]
        radar = {s: r for s, r in radar.items() if s in bars and (o["tested_only"] == "off" or r["strength"] >= 2)}
        si = idx["SPY"].get(day)
        spy = {x[0]: x[4] for x in src.get("SPY", {}).get(day, [])}
        spy_prev = data["daily"]["SPY"][si - 1]["c"] if si else None
        eq_prev = book.cash + sum(p["qty"] * prev.get(t, p["entry"]) for t, p in book.pos.items())

        def size(eq, entry, stop):
            """25% of equity; with risk_pct, no more than that % of equity lost at the stop."""
            usd = eq * SIZE
            if o["risk_pct"] and entry > stop:
                usd = min(usd, eq * o["risk_pct"] / 100 / ((entry - stop) / entry))
            return usd

        def ctx(s, px, rr, r, status, m):
            first = bars[s].get(570)
            i = idx[s][day]
            back = data["daily"][s][i - 6]["c"] if i >= 6 else prev[s]
            return {"status": status, "stop": r["stop"], "target": r["target"], "atr": r["atr"], "rr": round(rr, 2),
                    "spy_day": round((spy[m] / spy_prev - 1) * 100, 2) if spy_prev and m in spy else None,
                    "prior5_atr": round((prev[s] - back) / r["atr"], 2),
                    "dist_atr": round((prev[s] - r.get("S", prev[s])) / r["atr"], 2),
                    "dip_atr": round((px - prev[s]) / r["atr"], 2),
                    "gap_atr": round((first[1] - prev[s]) / r["atr"], 2) if first else None,
                    "btc_d1": gate.get("d1"), "btc_ok": gate["ok"], "crypto": r["crypto"],
                    "strength": r["strength"], "exit_rule": r.get("exit_rule", "plan")}

        # 8:40: resting DAY buy limits for the free slots
        if o["limit"] != "none" and radar:
            slots = SLOTS - len(book.pos)
            crypto = sum(1 for t in book.pos if t in lv.CRYPTO_LINKED)
            cands = []
            for s, r in radar.items():
                if s in book.pos or prev[s] <= r["stop"]:
                    continue
                lim = round(r["S"] if o["limit"] == "support" else r["Z"], 2 if r["S"] >= 1 else 4)
                if (prev[s] / lim - 1) * 100 > NEAR or lim <= r["stop"]:
                    continue
                rr = (r["target"] - lim) / (lim - r["stop"])
                if rr >= 1.5:
                    cands.append((rr, s, lim))
            for rr, s, lim in sorted(cands, reverse=True):
                if slots <= 0:
                    break
                if radar[s]["crypto"] and (crypto >= MAX_CRYPTO or not gate["ok"]):
                    continue
                usd = min(size(eq_prev, lim, radar[s]["stop"]), book.free_cash(day))
                if usd < 25:
                    break
                book.orders.append({"ticker": s, "limit": lim, "usd": usd, "rr": rr})
                book.placed += 1
                slots -= 1
                crypto += radar[s]["crypto"]
        # 9:25: cancel a buy whose stock opens at or under its stop
        book.orders = [x for x in book.orders if bars[x["ticker"]].get(570, (0, 1e9))[1] > radar[x["ticker"]]["stop"]]
        # the open: gap-down entries (entry=gap)
        if o["entry"] == "gap":
            cands = []
            for s, a_ in elig.items():
                b = bars.get(s, {}).get(570)
                if not b or s in book.pos:
                    continue
                gap = (b[1] - prev[s]) / a_
                if gap <= -GAP_ATR:
                    cands.append((gap, s, b[1]))
            slots = SLOTS - len(book.pos)
            for gap, s, px in sorted(cands)[:max(slots, 0)]:
                usd = min(eq_prev * SIZE, book.free_cash(day))
                if usd < 25:
                    break
                fill = px * (1 + sb.slip(px))
                r = {"stop": 0.0, "target": prev[s], "atr": elig[s], "crypto": s in lv.CRYPTO_LINKED, "strength": 0,
                     "exit_rule": "day"}
                book.buy(s, fill, usd, day, n, 570, "gap", ctx(s, fill, 0, r, "gap", 570))
        day_low = {s: 1e18 for s in bars}
        for m in range(570, 960, step):
            if book.orders and m >= min(o["limit_until"], o["entry_until"]):
                book.orders = []  # cancel the unfilled resting buys
            for s, bs in bars.items():
                b = bs.get(m)
                if b:
                    day_low[s] = min(day_low[s], b[3])
            for x in list(book.orders):  # resting buy limits
                s = x["ticker"]
                b = bars[s].get(m)
                if not b or b[3] > x["limit"] - TICK or m < o["entry_from"]:
                    continue
                px = b[1] if b[1] <= x["limit"] - TICK else x["limit"]
                book.orders.remove(x)
                book.filled += 1
                r = radar[s]
                book.buy(s, px, x["usd"], day, n, m, "limit", ctx(s, px, x["rr"], r, "limit", m))
                book.pos[s]["lo"] = min(px, b[3])
                if b[3] <= r["stop"]:  # the same bar went through the stop: the cautious reading sells it there
                    base = min(r["stop"], px)
                    book.sell(s, base * (1 - sb.slip(base)), day, m, "stop", settle[day])
            for s in list(book.pos):  # resting stops; the best and worst prices while held
                p = book.pos[s]
                b = bars.get(s, {}).get(m)
                if not b or (p["day"] == day and p["minute"] == m and p["kind"] != "gap"):
                    continue
                if p["exit_rule"] == "day":
                    p["hi"], p["lo"] = max(p["hi"], b[2]), min(p["lo"], b[3])
                    if m > 570 and b[2] >= p["target"]:
                        base = max(p["target"], b[1])
                        book.sell(s, base * (1 - sb.slip(base)), day, m, "neutral", settle[day])
                    elif m == last_bar:
                        book.sell(s, b[4] * (1 - sb.slip(b[4])), day, m, "close", settle[day])
                    continue
                if b[3] <= p["stop"]:
                    base = b[1] if b[1] < p["stop"] else p["stop"]
                    p["lo"] = min(p["lo"], b[3])
                    book.sell(s, base * (1 - sb.slip(base)), day, m, "protect" if p.get("protected") else "stop",
                              settle[day])
                    continue
                p["hi"], p["lo"] = max(p["hi"], b[2]), min(p["lo"], b[3])
                if o["protect"] != "none" and p["hi"] - p["entry"] >= o["protect_at"] * p["atr"]:
                    new = p["entry"] if o["protect"] == "be" else p["hi"] - o["protect_trail"] * p["atr"]
                    if new > p["stop"]:
                        p["stop"], p["protected"] = new, True
                if o["max_hold"] and m == last_bar and n - p["n"] >= o["max_hold"] - 1:
                    book.sell(s, b[4] * (1 - sb.slip(b[4])), day, m, "time", settle[day])
            if m not in runs_at:
                continue
            for s in list(book.pos):  # a run: targets first, then market buys for the free slots
                b = bars.get(s, {}).get(m)
                if b and book.pos[s]["exit_rule"] == "plan" and b[4] >= book.pos[s]["target"]:
                    book.sell(s, b[4] * (1 - sb.slip(b[4])), day, m, "target", settle[day])
            if o["runs"] == "off" or not radar or m + step > o["entry_until"] or m + step <= o["entry_from"]:
                continue
            slots = SLOTS - len(book.pos) - len(book.orders)
            taken = set(book.pos) | {x["ticker"] for x in book.orders}
            crypto = sum(1 for t in taken if t in lv.CRYPTO_LINKED)
            cands = []
            for s, r in radar.items():
                b = bars[s].get(m)
                if not b or s in taken or s in book.stopped_today:
                    continue
                px = b[4]
                if px <= r["stop"] or day_low[s] <= r["stop"] or px >= r["target"]:
                    continue
                rr = (r["target"] - px) / (px - r["stop"])
                if not (px <= r["Z"] or day_low[s] <= r["Z"]) or rr < 1.5:
                    continue
                dip = (px - prev[s]) / r["atr"]
                cands.append(((dip, -rr) if o["rank"] == "dip" else (-rr, dip), s, px, rr,
                              "buy zone" if px <= r["Z"] else "bounce"))
            for _, s, px, rr, status in sorted(cands):
                if slots <= 0:
                    break
                if radar[s]["crypto"] and (crypto >= MAX_CRYPTO or not gate["ok"]):
                    continue
                usd = min(size(eq_prev, px, radar[s]["stop"]), book.free_cash(day))
                if usd < 25:
                    break
                fill = px * (1 + sb.slip(px))
                book.buy(s, fill, usd, day, n, m, "run", ctx(s, fill, rr, radar[s], status, m))
                slots -= 1
                crypto += radar[s]["crypto"]
        book.orders = []  # DAY orders expire at the close
        eq = book.cash + sum(p["qty"] * close.get(t, p["entry"]) for t, p in book.pos.items())
        curve.append({"day": day, "equity": round(eq, 2), "positions": sorted(book.pos)})
    first, last = sessions[0], sessions[-1]
    bench = {}
    for s in ("SPY", "QQQ"):
        rows = data["daily"].get(s) or []
        i0, i1 = idx.get(s, {}).get(first), idx.get(s, {}).get(last)
        if i0 is not None and i1 is not None:
            bench[s] = round((rows[i1]["c"] / rows[i0 - 1]["c"] - 1) * 100, 2)
    open_pos = []
    for t, p in book.pos.items():
        i = idx[t].get(last)
        c = data["daily"][t][i]["c"] if i is not None else p["entry"]
        open_pos.append({"ticker": t, "entry": round(p["entry"], 4), "day": p["day"], "stop": round(p["stop"], 4),
                         "target": round(p["target"], 4), "last": round(c, 4),
                         "ret_pct": round((c / p["entry"] - 1) * 100, 2)})
    return {"sessions": [first, last, len(sessions)], "equity": curve, "trades": book.trades, "open": open_pos,
            "bench": bench, "start": cash, "orders_placed": book.placed, "orders_filled": book.filled}


def summarize(res: dict) -> dict:
    tr = res["trades"]
    wins = [t for t in tr if t["pnl"] > 0]
    losses = [t for t in tr if t["pnl"] <= 0]
    eq = [e["equity"] for e in res["equity"]]
    peak, mdd = res["start"], 0.0
    for v in eq:
        peak = max(peak, v)
        mdd = min(mdd, v / peak - 1)
    gw, gl = sum(t["pnl"] for t in wins), -sum(t["pnl"] for t in losses)
    final = eq[-1] if eq else res["start"]
    return {"final": final, "ret_pct": round((final / res["start"] - 1) * 100, 2), "trades": len(tr),
            "wins": len(wins), "win_rate": round(len(wins) / len(tr) * 100, 1) if tr else None,
            "avg_win": round(st.mean(t["ret_pct"] for t in wins), 2) if wins else None,
            "avg_loss": round(st.mean(t["ret_pct"] for t in losses), 2) if losses else None,
            "avg_trade": round(st.mean(t["ret_pct"] for t in tr), 2) if tr else None,
            "profit_factor": round(gw / gl, 2) if gl else None, "max_drawdown_pct": round(mdd * 100, 2),
            "realized": round(sum(t["pnl"] for t in tr), 2),
            "unrealized": round(final - res["start"] - sum(t["pnl"] for t in tr), 2),
            "by_exit": {w: n for w in ("target", "stop", "time", "neutral", "close")
                        if (n := sum(1 for t in tr if t["why"] == w))},
            "fill_rate": (f"{res['orders_filled']}/{res['orders_placed']}" if res["orders_placed"] else None)}


def lessons(res: dict) -> list[str]:
    tr = res["trades"]
    groups = {
        "stopped the session it was bought": [t for t in tr if t["why"] == "stop" and t["exit_day"] == t["day"]],
        "stopped on a later session": [t for t in tr if t["why"] == "stop" and t["exit_day"] != t["day"]],
        "stopped at the open (gapped through the stop)": [t for t in tr if t["why"] == "stop" and t["exit_minute"] == 570
                                                         and t["exit_day"] != t["day"]],
        "never rose 0.5 ATR above the entry": [t for t in tr if t["best_atr"] < 0.5],
        "crypto-linked": [t for t in tr if t["crypto"]],
        "bought at the open after a gap down of 0.5+ ATR": [t for t in tr if t["minute"] == 570 and (t["gap_atr"] or 0) <= -0.5],
        "bought on a dip of 0.5+ ATR (any time)": [t for t in tr if t["dip_atr"] <= -0.5],
        "bought less than 0.25 ATR under the prior close": [t for t in tr if t["dip_atr"] > -0.25],
        "resting limit fills": [t for t in tr if t["kind"] == "limit"],
        "run entries inside the buy zone": [t for t in tr if t["status"] == "buy zone"],
        "run entries on a bounce (touched the zone, back above it)": [t for t in tr if t["status"] == "bounce"],
        "support tested 3+ times": [t for t in tr if t["strength"] >= 3],
        "support tested twice": [t for t in tr if t["strength"] == 2],
        "radar keeps (GPUS, IREN, BTDR) without a tested support": [t for t in tr if t["strength"] < 2 and t["kind"] != "gap"],
    }
    out = []
    for k, g in groups.items():
        if g:
            out.append(f"{k}: {len(g)} trade{'s' if len(g) > 1 else ''}, {sum(1 for t in g if t['pnl'] > 0)} won, "
                       f"average {st.mean(t['ret_pct'] for t in g):+.2f}%, total ${sum(t['pnl'] for t in g):+.2f}")
    return out


def analyze(res: dict) -> list[str]:
    """Trade returns by entry context, mean +/- 95% (clustered by entry date)."""
    tr = res["trades"]

    def band(k, cuts, labels):
        out = []
        for (lo, hi), lab in zip(zip(cuts[:-1], cuts[1:]), labels):
            out.append((lab, [t for t in tr if t.get(k) is not None and lo <= t[k] < hi]))
        return out
    inf = float("inf")
    groups = [("all", tr)]
    groups += [(f"entry: {k}", [t for t in tr if t["status"] == k]) for k in ("limit", "buy zone", "bounce", "gap")]
    groups += [("filled at the open bar", [t for t in tr if t["minute"] == 570]),
               ("filled 9:35-10:30", [t for t in tr if 570 < t["minute"] < 630]),
               ("filled after 10:30", [t for t in tr if t["minute"] >= 630])]
    groups += band("gap_atr", [-inf, -0.5, 0, inf], ["open gap <= -0.5 ATR", "open gap -0.5 to 0 ATR", "open gap up"])
    groups += band("dip_atr", [-inf, -1, -0.5, 0, inf],
                   ["entry 1+ ATR under the prior close", "entry 0.5-1 ATR under", "entry 0-0.5 ATR under", "entry above the prior close"])
    groups += band("prior5_atr", [-inf, -2, 0, inf], ["fell 2+ ATR over the 5 sessions before", "fell 0-2 ATR", "rose over the 5 sessions before"])
    groups += band("dist_atr", [-inf, 1, 2, inf], ["prior close < 1 ATR above support", "1-2 ATR above", "2+ ATR above"])
    groups += band("spy_day", [-inf, -1, 0, inf], ["S&P 500 down 1%+ at the entry", "S&P 500 down 0-1%", "S&P 500 up"])
    groups += band("strength", [0, 2, 3, 4, inf], ["support untested (radar keeps)", "support tested twice", "three times", "four+ times"])
    groups += band("rr", [0, 3, 6, inf], ["R:R under 3", "R:R 3-6", "R:R 6+"])
    groups += [("crypto-linked", [t for t in tr if t["crypto"]]), ("not crypto-linked", [t for t in tr if not t["crypto"]])]
    L = ["| Entry context | Trades | Average ± 95% | Median | Winners | P&L |", "|---|---:|---:|---:|---:|---:|"]
    for lab, g in groups:
        if len(g) < 5:
            continue
        m, se = cb.clustered([(t["day"], t["ret_pct"]) for t in g])
        L.append(f"| {lab} | {len(g)} | {m:+.2f}% ± {1.96 * se:.2f} | {st.median(t['ret_pct'] for t in g):+.2f}% | "
                 f"{sum(1 for t in g if t['pnl'] > 0) / len(g) * 100:.0f}% | ${sum(t['pnl'] for t in g):+.0f} |")
    return L


def headline(res: dict, s: dict) -> str:
    wr = f" ({s['win_rate']}%)" if s["trades"] else ""
    return (f"${res['start']:.0f} -> ${s['final']:.2f} ({s['ret_pct']:+.2f}%; realized ${s['realized']:+.2f}, open "
            f"positions ${s['unrealized']:+.2f}); S&P 500 {res['bench'].get('SPY', 0):+.2f}%, Nasdaq-100 "
            f"{res['bench'].get('QQQ', 0):+.2f}%. {s['trades']} closed trades, {s['wins']} winners{wr}, "
            f"average trade {s['avg_trade']}%, average win "
            f"{s['avg_win']}%, average loss {s['avg_loss']}%, profit factor {s['profit_factor']}, worst drawdown "
            f"{s['max_drawdown_pct']}%. Exits: {', '.join(f'{k} {v}' for k, v in s['by_exit'].items()) or 'none'}."
            + (f" Resting orders filled: {s['fill_rate']}." if s["fill_rate"] else ""))


def detail(res: dict, s: dict, title: str) -> list[str]:
    s0, s1, n = res["sessions"]
    L = [f"## {title}: {s0} to {s1} ({n} sessions)", "", headline(res, s), "",
         "### What the trades had in common", ""] + [f"- {x}" for x in lessons(res)] + [
         "", "### Trades", "", "Gap and dip: the open and the entry against the prior close, in ATR. Best and worst: the "
         "highest high and lowest low while held, in ATR from the entry.", "",
         "| Bought | Name | How | Entry | Gap / dip | R:R | Sold | Exit | Why | Return | Best / worst |",
         "|---|---|---|---:|---:|---:|---|---:|---|---:|---:|"]
    for t in sorted(res["trades"], key=lambda t: (t["day"], t["minute"])):
        L.append(f"| {t['day']} {hhmm(t['minute'])} | {t['ticker']}{' (crypto)' if t['crypto'] else ''} | {t['status']} | "
                 f"{t['entry']:.4g} | {t['gap_atr'] if t['gap_atr'] is not None else 0:+.2f} / {t['dip_atr']:+.2f} | "
                 f"{t['rr']} | {t['exit_day']} {hhmm(t['exit_minute'])} | {t['exit']:.4g} | {t['why']} | "
                 f"{t['ret_pct']:+.2f}% | {t['best_atr']:+.2f} / {t['worst_atr']:+.2f} |")
    if res["open"]:
        L += ["", "### Still open at the end", "", "| Name | Bought | Entry | Stop | Target | Last | Return |",
              "|---|---|---:|---:|---:|---:|---:|"]
        L += [f"| {p['ticker']} | {p['day']} | {p['entry']:.4g} | {p['stop']:.4g} | {p['target']:.4g} | {p['last']:.4g} | "
              f"{p['ret_pct']:+.2f}% |" for p in res["open"]]
    L += ["", "### Equity by session", "", "| Session | Equity | Holding at the close |", "|---|---:|---|"]
    L += [f"| {e['day']} | ${e['equity']:.2f} | {', '.join(e['positions']) or '-'} |" for e in res["equity"]]
    return L


def windows(data: dict, a) -> int:
    """Each rule set over every window of --days sessions in the 5-minute data: how much of a result is the rule
    and how much is the start date."""
    days = sorted(data[a.bars]["SPY"])
    now = pfm.now_utc()
    days = [d for d in days if d < pfm.et_date(now).isoformat() or now.astimezone(pfm.ET).hour >= 16]
    ends = days[a.days - 1:][::-1][::a.step][::-1]
    spy = {e: replay(data, a.days, DEFAULTS, a.cash, e, a.bars)["bench"].get("SPY", 0) for e in ends}
    rows, out = [], []
    for title, ov in GRID:
        o = {**DEFAULTS, **ov}
        rets, trades = [], []
        for e in ends:
            res = replay(data, a.days, o, a.cash, e, a.bars)
            sm = summarize(res)
            rets.append((e, sm["ret_pct"]))
            trades.append(sm["trades"])
        r = sorted(x for _, x in rets)
        beat = sum(1 for e, x in rets if x > spy[e])
        rows.append(f"| {title} | {st.median(r):+.1f}% | {st.mean(r):+.1f}% | {r[0]:+.1f}% | {r[-1]:+.1f}% | "
                    f"{beat}/{len(r)} | {sum(1 for x in r if x >= 100)}/{len(r)} | {st.mean(trades):.0f} |")
        out.append({"title": title, "options": o, "returns": rets})
    sp = sorted(spy.values())
    text = "\n".join([
        f"# Replay windows: {len(ends)} windows of {a.days} sessions ending {ends[0]} to {ends[-1]}, "
        f"{'5-minute' if a.bars == '5m' else 'hourly'} bars", "",
        f"$1,000 each window. S&P 500 over the same windows: median {st.median(sp):+.1f}%, {sp[0]:+.1f}% to "
        f"{sp[-1]:+.1f}%. " + ("The windows overlap, so they are not independent tests: the spread shows how much the "
                               "start date moves the result." if a.step < a.days else "The windows do not overlap."), "",
        "| Rules | Median return | Mean | Worst window | Best window | Beat the S&P 500 | Doubled ($2,000) | "
        "Closed trades per window |",
        "|---|---:|---:|---:|---:|---:|---:|---:|"] + rows)
    print(text)
    if a.save:
        o_ = ROOT / "research" / "replay"
        o_.mkdir(parents=True, exist_ok=True)
        stem = f"windows-{ends[-1]}-{a.days}-{a.bars}-{a.set}"
        (o_ / f"{stem}.md").write_text(text + "\n")
        (o_ / f"{stem}.json").write_text(json.dumps({"spy": spy, "rules": out}, indent=1) + "\n")
        print("saved", (o_ / f"{stem}.md").relative_to(ROOT))
    return 0


def label(o: dict) -> str:
    return " ".join(f"{k}={v}" for k, v in o.items() if DEFAULTS.get(k) != v) or "live rules"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--end", default=None, help="last session (YYYY-MM-DD); default the last full one")
    ap.add_argument("--cash", type=float, default=1000.0)
    ap.add_argument("--limit", choices=["support", "top", "none"], default=DEFAULTS["limit"])
    ap.add_argument("--stop-atr", type=float, default=DEFAULTS["stop_atr"])
    ap.add_argument("--btc-gate", choices=["on", "off"], default=DEFAULTS["btc_gate"])
    ap.add_argument("--rank", choices=["dip", "rr"], default=DEFAULTS["rank"])
    ap.add_argument("--runs", choices=["on", "off"], default=DEFAULTS["runs"])
    ap.add_argument("--max-hold", type=int, default=DEFAULTS["max_hold"])
    ap.add_argument("--entry", choices=["radar", "gap"], default=DEFAULTS["entry"])
    ap.add_argument("--limit-until", type=int, default=DEFAULTS["limit_until"],
                    help="minute of the day (ET) the unfilled buy limits are cancelled: 600 = 10:00")
    ap.add_argument("--tested-only", choices=["on", "off"], default=DEFAULTS["tested_only"],
                    help="entries in GPUS, IREN and BTDR only with a support tested twice")
    ap.add_argument("--bars", choices=["5m", "1h"], default="5m", help="5-minute (60 sessions) or hourly (2 years)")
    ap.add_argument("--step", type=int, default=1, help="with --windows: sessions between window ends")
    ap.add_argument("--analyze", action="store_true", help="trade returns by entry context")
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--set", choices=["rules", "stops", "times", "sizing", "exits"], default="rules",
                    help="with --grid: which variants")
    ap.add_argument("--risk-pct", type=float, default=DEFAULTS["risk_pct"],
                    help="size each position so the stop loses at most this % of equity (0: 25%% of equity)")
    ap.add_argument("--entry-from", type=int, default=DEFAULTS["entry_from"],
                    help="minute of the day (ET) before which no entry (limits do not fill, no run buys)")
    ap.add_argument("--entry-until", type=int, default=DEFAULTS["entry_until"],
                    help="minute of the day (ET) after which no entry: unfilled limits are cancelled, no run buys")
    ap.add_argument("--windows", action="store_true", help="with --grid: every --days window in the 5-minute data")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    data = load_data(lv.CANDIDATES, a.refresh)
    global GRID
    if a.set == "stops":
        GRID = STOPS
    if a.set == "times":
        GRID = TIMES
    if a.set == "sizing":
        GRID = SIZING
    if a.set == "exits":
        GRID = EXITS
    if a.grid and a.windows:
        return windows(data, a)
    if a.grid:
        rows, details, out_json = [], [], []
        for title, ov in GRID:
            o = {**DEFAULTS, **ov}
            res = replay(data, a.days, o, a.cash, a.end, a.bars)
            s = summarize(res)
            rows.append(f"| {title} | {s['ret_pct']:+.2f}% | {s['trades']} | {s['win_rate'] if s['trades'] else '-'}% | "
                        f"{s['avg_trade'] if s['trades'] else '-'}% | {s['profit_factor'] or '-'} | {s['max_drawdown_pct']}% | "
                        f"{', '.join(p['ticker'] for p in res['open']) or '-'} |")
            # long replays keep the comparison only (a 700-session trade log runs to megabytes)
            if res["sessions"][2] <= 60:
                details += detail(res, s, title) + [""]
                out_json.append({"title": title, "options": o, "summary": s, "lessons": lessons(res), **res})
            else:
                out_json.append({"title": title, "options": o, "summary": s, "lessons": lessons(res),
                                 "sessions": res["sessions"], "bench": res["bench"], "open": res["open"]})
        s0, s1, n = out_json[0]["sessions"]
        b = out_json[0]["bench"]
        text = "\n".join([
            f"# Replay of the rules, {s0} to {s1} ({n} sessions, {'5-minute' if a.bars == '5m' else 'hourly'} bars)", "",
            f"$1,000 each; S&P 500 {b.get('SPY', 0):+.2f}%, Nasdaq-100 {b.get('QQQ', 0):+.2f}% over the same sessions. "
            "Method and caveats: `scripts/replay.py` docstring. Return includes open positions at the last close.", "",
            "| Rules | Return | Closed trades | Winners | Average trade | Profit factor | Worst drawdown | Open at the end |",
            "|---|---:|---:|---:|---:|---:|---:|---|"] + rows + [""] + details)
        print(text.split("\n## ")[0])
        if a.save:
            out = ROOT / "research" / "replay"
            out.mkdir(parents=True, exist_ok=True)
            stem = f"replay-{s1}-{n}-{a.bars}-{a.set}"
            (out / f"{stem}.md").write_text(text + "\n")
            (out / f"{stem}.json").write_text(json.dumps(out_json, indent=1) + "\n")
            print("saved", (out / f"{stem}.md").relative_to(ROOT))
        return 0
    o = {k: getattr(a, k) for k in DEFAULTS}
    res = replay(data, a.days, o, a.cash, a.end, a.bars)
    s = summarize(res)
    if a.analyze:
        print(headline(res, s), "", *analyze(res), sep="\n")
        return 0
    print("\n".join(detail(res, s, label(o))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
