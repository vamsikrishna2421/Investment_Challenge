#!/usr/bin/env python3
"""Real-money book: Vamsi's Robinhood agentic account (Vamsi, Tue Oct 6, 2026: "I permit you to operate on real
Robinhood account"; he opened the account's stock-order tools in .claude/settings.json the same day).

The account is the record: cash, positions and orders come from the Robinhood tools at every run, written by the
agent to .cache/real/account.json (format below). This script keeps each position's plan (stop, target, reason)
and a private journal in .secrets/real_book.json (git-ignored; mirrored to the private dashboard's database,
collection real_book), says which orders to place under stricter rules than the paper book, and builds the
private dashboard's snapshot (.cache/snapshot_real.json, collection snapshots_real). Nothing about this account
goes into the public repo or site.

  python scripts/real.py run [--skip A,B]      # sync with account.json, then the actions to take, in order
  python scripts/real.py record order --id ID --symbol X --kind entry|manual|stop|exit --qty Q --price P
                                [--stop S --target T --why "..."]      # after each order placed
  python scripts/real.py record cancel --id ID [--why "..."]           # after each order cancelled
  python scripts/real.py record note --title "..." --body "..."        # a private journal entry
  python scripts/real.py record pause --until YYYY-MM-DD --why "..."    # no new entries of its own (Vamsi); --off resumes
  python scripts/real.py snapshot | status

Rules (RUNBOOK 2e), stricter than the paper book because the money is real:
  entries  DAY buy limits at support (the bottom of the buy zone) for radar names with support tested 3+ times,
           R:R 2.5+ from support, within 8% above support, not HALTED, no offering or material news (--skip), not
           up 0.43+ ATR over the 5 sessions before (trade_clues: 64% of those were stopped within 3 sessions),
           crypto-linked at most 1 and only while the bitcoin gate is open, higher R:R first. No new orders while
           SPY is down 0.35%+ on the day, and open buy limits are cancelled then (trade_clues: fills on weak S&P
           days were stopped out more often).
  size     whole shares; at most 25% of the account value, cut so the stop loses at most 1.5% of it, at most
           $300, never more than the cash (no margin borrowing).
  limits   3 positions plus open buy orders; no new orders after a $30 loss on the day; none at all below $900
           account value (Vamsi is told).
  exits    a GTC stop-market sell at the plan stop right after a fill; at a run with the price at or above the
           target (the sell-zone bottom), cancel the stop and sell with a limit at the bid. On the challenge's
           last day (Wed Nov 4) no new orders after 14:55, and at 15:40 everything is sold unless Vamsi says
           otherwise.
Day-trade rules: FINRA replaced the pattern-day-trader rule with intraday margin standards on June 4, 2026, and
Robinhood's help page says its margin accounts no longer have day-trade limits; the account is limited margin
and never borrows. review_equity_order shows any alert before each order.

account.json, written by the agent from get_portfolio, get_equity_positions and get_equity_orders:
  {"asof": "2026-10-06T13:40:00Z", "total_value": 1000.0, "cash": 1000.0, "buying_power": 1000.0,
   "positions": [{"symbol": "X", "quantity": 3.0, "average_buy_price": 10.5}],
   "orders": [{"id": "...", "symbol": "X", "side": "buy", "type": "limit", "state": "filled", "quantity": 3,
               "cumulative_quantity": 3, "price": 10.5, "stop_price": null, "average_price": 10.49,
               "time_in_force": "gfd", "created_at": "...", "last_transaction_at": "..."}]}
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import levels as lv  # noqa: E402
import orders as od  # noqa: E402
import portfolio as pfm  # noqa: E402
import sr_backtest as sb  # noqa: E402

ROOT = pfm.ROOT
STATE = ROOT / ".secrets" / "real_book.json"
ACCOUNT = ROOT / ".cache" / "real" / "account.json"
SNAPSHOT = ROOT / ".cache" / "snapshot_real.json"
START_VALUE, START_UTC = 1000.0, "2026-10-06T13:30:00Z"
MAX_POS, MIN_STRENGTH, MIN_RR, MAX_USD, NEAR = 3, 3, 2.5, 300.0, 8.0
DAY_LOSS, KILL_VALUE, MAX_CRYPTO, SPY_MIN, MAX_RET5 = 30.0, 900.0, 1, -0.35, 0.43
OPEN_STATES = {"new", "queued", "confirmed", "unconfirmed", "partially_filled"}
# Odds that a buy limit k ATR under the price fills by the close, by the check time (ET minutes), from 61 radar
# candidates' hourly bars over ~2 years (Oct 6, research/backtests/fill-odds-2026-10-06.md): all checks, and checks
# with the price 0.4+ ATR above the prior close (names up on the day dip back more often).
ODDS_K = (0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0)
ODDS = {570: (1, .65, .37, .19, .10, .05, .02, .01), 630: (1, .52, .22, .09, .03, .01, .01, 0),
        690: (1, .44, .15, .05, .02, .01, 0, 0), 750: (1, .37, .11, .03, .01, .01, 0, 0),
        810: (1, .29, .07, .02, .01, 0, 0, 0), 870: (1, .20, .03, .01, 0, 0, 0, 0), 960: (1, 0, 0, 0, 0, 0, 0, 0)}
ODDS_UP = {570: (1, .73, .49, .31, .19, .11, .06, .02), 630: (1, .61, .31, .14, .07, .03, .02, .01),
           690: (1, .51, .22, .08, .03, .02, .01, 0), 750: (1, .44, .16, .06, .03, .01, .01, 0),
           810: (1, .36, .11, .04, .02, .01, 0, 0), 870: (1, .26, .06, .02, .01, 0, 0, 0), 960: (1, 0, 0, 0, 0, 0, 0, 0)}
# Vamsi, Oct 6: an open buy very unlikely to fill (odds under SWAP_BELOW) is cancelled for a waiting name that likely
# will (SWAP_TO or better), from 9:45 to 15:00; with no such name it stays and is watched.
SWAP_BELOW, SWAP_TO, SWAP_WINDOW = 0.15, 0.30, (9 * 60 + 45, 15 * 60)
RULES = ("Real money, Robinhood agentic account (Vamsi, Oct 6): DAY buy limits at tested support (3+ touches, R:R 2.5+), "
         "skipping names up over the prior 5 sessions and weak S&P days; whole shares, at most 1.5% of the account "
         "lost at a stop and $300 an order; 3 positions; no new orders after a $30 losing day or below $900; a stop "
         "order right after each fill; sell at the sell zone.")


def now_utc() -> dt.datetime:
    return pfm.now_utc()


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"opened": START_UTC, "start_value": START_VALUE, "plans": {}, "closed": [], "orders": {}, "journal": [],
            "history": [], "day": {}}


def save_state(s: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(s, indent=1) + "\n")


def load_account() -> dict:
    if not ACCOUNT.exists():
        sys.exit(f"no {ACCOUNT.relative_to(ROOT)}: write it from the Robinhood tools first (format in the docstring)")
    return json.loads(ACCOUNT.read_text())


def masked() -> str:
    p = ROOT / ".secrets" / "robinhood_account"
    return "••••" + p.read_text().strip()[-4:] if p.exists() else "the agentic account"


def tick(px: float) -> float:
    return round(px, 2) if px >= 1 else round(px, 4)


def note(s: dict, kind: str, title: str, body: str, tickers: list[str] | None = None) -> None:
    s["journal"].append({"id": f"R{len(s['journal']) + 1:04d}", "ts": pfm.iso(now_utc()), "kind": kind,
                         "title": title, "body": body, "tickers": tickers or []})


def quotes() -> dict:
    p = ROOT / ".cache" / "quotes.json"
    return json.loads(p.read_text())["quotes"] if p.exists() else {}


def price_of(q: dict | None) -> float | None:
    return pfm.mark(q)[0] if q else None


def sync(s: dict, a: dict) -> list[str]:
    """Fills of recorded buy orders open plans; fills of recorded sells close them. Returns warnings."""
    warn = []
    now = now_utc()
    today = pfm.et_date(now).isoformat()
    if s["day"].get("date") != today:
        s["day"] = {"date": today, "start_value": a["total_value"]}
    q = quotes()
    pt = {"t": a.get("asof") or pfm.iso(now), "value": a["total_value"],
          "SPY": price_of(q.get("SPY")), "QQQ": price_of(q.get("QQQ"))}
    if not s["history"] or s["history"][-1]["t"][:16] != pt["t"][:16]:
        s["history"].append(pt)
    held = {p["symbol"]: p for p in a["positions"] if float(p["quantity"]) > 0}
    for o in a["orders"]:
        rec = s["orders"].get(o["id"])
        if rec is None:
            if o["state"] in OPEN_STATES or o["state"] == "filled":
                warn.append(f"order {o['id'][:8]} {o['side']} {o['symbol']} ({o['state']}) was not placed by the real book")
            continue
        if rec.get("state") == o["state"]:
            continue
        rec["state"] = o["state"]
        filled = float(o.get("cumulative_quantity") or 0)
        avg = float(o["average_price"]) if o.get("average_price") else None
        if rec["kind"] in ("entry", "manual") and o["state"] in ("filled", "partially_filled", "cancelled") and filled > 0 and avg:
            p = s["plans"].setdefault(o["symbol"], {"symbol": o["symbol"], "qty": 0.0, "entry": avg, "stop": rec["stop"],
                                                   "target": rec["target"], "why": rec.get("why", ""),
                                                   "opened": o.get("last_transaction_at") or pfm.iso(now),
                                                   "stop_order_id": None})
            p["qty"], p["entry"] = filled, avg
            note(s, "trade", f"Bought {filled:g} {o['symbol']} at {avg:.4g}",
                 f"Buy limit {rec['price']} filled: {filled:g} shares at {avg:.4g} (${filled * avg:.2f}). Stop "
                 f"{rec['stop']}, target {rec['target']}. {rec.get('why', '')}", [o["symbol"]])
        if rec["kind"] in ("stop", "exit") and o["state"] == "filled" and avg:
            p = s["plans"].pop(o["symbol"], None)
            if p:
                pnl = (avg - p["entry"]) * filled
                s["closed"].append({**p, "exit": avg, "exit_qty": filled, "closed": o.get("last_transaction_at") or pfm.iso(now),
                                    "why_exit": "stop" if rec["kind"] == "stop" else "target", "pnl": round(pnl, 2),
                                    "ret_pct": round((avg / p["entry"] - 1) * 100, 2)})
                note(s, "review", f"Sold {filled:g} {o['symbol']} at {avg:.4g} ({'stop' if rec['kind'] == 'stop' else 'target'})",
                     f"Entry {p['entry']:.4g}, exit {avg:.4g}: {pnl:+.2f} ({(avg / p['entry'] - 1) * 100:+.2f}%). "
                     f"Plan: stop {p['stop']}, target {p['target']}. {p.get('why', '')}", [o["symbol"]])
    for sym in held:
        if sym not in s["plans"]:
            warn.append(f"{sym} is held but has no real-book plan: leave it alone and tell Vamsi")
    for sym, p in list(s["plans"].items()):
        if sym not in held:
            warn.append(f"plan for {sym} but no position in the account: check the order history")
        elif abs(float(held[sym]["quantity"]) - p["qty"]) > 1e-6:
            p["qty"] = float(held[sym]["quantity"])
    return warn


def open_orders(a: dict, side: str | None = None, kind: str | None = None, s: dict | None = None) -> list[dict]:
    out = []
    for o in a["orders"]:
        if o["state"] not in OPEN_STATES or (side and o["side"] != side):
            continue
        if kind and s is not None and s["orders"].get(o["id"], {}).get("kind") != kind:
            continue
        out.append(o)
    return out


def ret5(sym: str) -> float | None:
    rows = sb.daily(sym, "3mo")
    if not rows or len(rows) < 20:
        return None
    today = pfm.et_date(now_utc()).isoformat()
    if dt.datetime.fromtimestamp(rows[-1]["t"], dt.timezone.utc).astimezone(pfm.ET).date().isoformat() >= today:
        rows = rows[:-1]
    return (rows[-1]["c"] - rows[-6]["c"]) / lv.atr(rows)


def fill_odds(k: float, minute: int, up: bool) -> float:
    """Odds that a buy limit k ATR under the price fills by the close (interpolated in k and in time)."""
    table = ODDS_UP if up else ODDS
    ms = sorted(table)
    minute = min(max(minute, ms[0]), ms[-1])
    lo, hi = max(m for m in ms if m <= minute), min(m for m in ms if m >= minute)

    def at(row: tuple) -> float:
        if k <= 0:
            return 1.0
        if k > ODDS_K[-1]:
            return 0.0
        i = next(i for i in range(1, len(ODDS_K)) if k <= ODDS_K[i])
        f = (k - ODDS_K[i - 1]) / (ODDS_K[i] - ODDS_K[i - 1])
        return row[i - 1] + f * (row[i] - row[i - 1])

    a, b = at(table[lo]), at(table[hi])
    return a if hi == lo else a + (minute - lo) / (hi - lo) * (b - a)


def odds_of(sym: str, px: float | None, limit: float, radar: dict, q: dict, minute: int) -> tuple[float, float] | None:
    r, qq = radar.get(sym), q.get(sym) or {}
    if not r or not r.get("atr") or px is None:
        return None
    k = max(0.0, (px - limit) / r["atr"])
    up = bool(qq.get("prev_close")) and px >= qq["prev_close"] + 0.4 * r["atr"]
    return fill_odds(k, minute, up), k


def entry_action(x: dict, qty: int, extra: str = "") -> dict:
    return {"do": "place", "kind": "entry", "symbol": x["symbol"], "side": "buy", "type": "limit",
            "limit_price": f"{x['limit']:g}", "quantity": str(qty), "time_in_force": "gfd",
            "stop": x["stop"], "target": x["target"],
            "why": (f"radar support {x['limit']} tested {x['strength']}x, stop {x['stop']}, sell zone from "
                    f"{x['target']}, R:R {x['rr']}; {x['dist']:+.1f}% above support at {x['price']:.4g}; "
                    f"{x['ret5']:+.2f} ATR over 5 sessions; ${qty * x['limit']:.2f} risks "
                    f"${qty * (x['limit'] - x['stop']):.2f}{extra}")}


def entry_candidates(s: dict, a: dict, skip: set[str]) -> tuple[list[dict], list[str]]:
    radar = json.loads(lv.RADAR.read_text())
    q = quotes()
    taken = set(s["plans"]) | {o["symbol"] for o in open_orders(a, "buy")}
    rows, why_not = [], []
    for r in radar["names"]:
        tk = r["ticker"]
        px = price_of(q.get(tk))
        lim = tick(r["buy_zone"][0])
        if tk in taken or tk in skip or px is None or r.get("halted"):
            continue
        rr = (r["sell_zone"][0] - lim) / (lim - r["stop"]) if lim > r["stop"] else 0
        if r["support_strength"] < MIN_STRENGTH or rr < MIN_RR or px <= r["stop"] or (px / lim - 1) * 100 > NEAR:
            continue
        r5 = ret5(tk)
        if r5 is None or r5 >= MAX_RET5:
            why_not.append(f"{tk}: up {r5:+.2f} ATR over the 5 sessions before" if r5 is not None else f"{tk}: no daily bars")
            continue
        rows.append({"symbol": tk, "price": px, "limit": lim, "stop": tick(r["stop"]), "target": tick(r["sell_zone"][0]),
                     "rr": round(rr, 2), "strength": r["support_strength"], "ret5": round(r5, 2),
                     "crypto": tk in lv.CRYPTO_LINKED, "dist": round((px / lim - 1) * 100, 2)})
    rows.sort(key=lambda x: -x["rr"])
    return rows, why_not


def cmd_run(a_) -> int:
    s, a = load_state(), load_account()
    warn = sync(s, a)
    now = now_utc()
    et = now.astimezone(pfm.ET)
    q = quotes()
    value, cash = float(a["total_value"]), float(a["cash"])
    day_pnl = value - s["day"]["start_value"]
    spy = q.get("SPY") or {}
    spy_px = price_of(spy)
    spy_day = (spy_px / spy["prev_close"] - 1) * 100 if spy_px and spy.get("prev_close") else None
    end = pfm.parse_ts(pfm.load_config()["end_utc"]).astimezone(pfm.ET)
    final_day = et.date() == end.date()
    print(f"real book {masked()} {pfm.iso(now)}: value ${value:.2f}, cash ${cash:.2f}, day {day_pnl:+.2f}, "
          f"SPY {spy_day:+.2f}% on the day" if spy_day is not None else
          f"real book {masked()} {pfm.iso(now)}: value ${value:.2f}, cash ${cash:.2f}, day {day_pnl:+.2f}")
    for w in warn:
        print("  WARNING", w)
    acts = []
    stops = {o["symbol"]: o for o in open_orders(a, "sell") if o["type"] in ("stop_market", "stop") or o.get("stop_price")}
    liquidate = final_day and et.hour * 60 + et.minute >= 15 * 60 + 40
    for sym, p in s["plans"].items():
        px = price_of(q.get(sym))
        bid = (q.get(sym) or {}).get("bid") or (px * 0.998 if px else None)
        if liquidate or (px is not None and px >= p["target"]):
            if sym in stops:
                acts.append({"do": "cancel", "order_id": stops[sym]["id"], "symbol": sym, "why": "target" if not liquidate else "final liquidation"})
            acts.append({"do": "place", "kind": "exit", "symbol": sym, "side": "sell", "type": "limit",
                         "limit_price": f"{tick(bid):g}" if bid else None, "quantity": f"{p['qty']:g}", "time_in_force": "gfd",
                         "why": (f"final liquidation at 15:40" if liquidate else f"{px:.4g} reached the target {p['target']}")})
        elif sym not in stops:
            acts.append({"do": "place", "kind": "stop", "symbol": sym, "side": "sell", "type": "stop_market",
                         "stop_price": f"{p['stop']:g}", "quantity": f"{p['qty']:g}", "time_in_force": "gtc",
                         "why": f"plan stop for the {p['qty']:g} shares bought at {p['entry']:.4g}"})
    hard = []  # these also cancel Vamsi's own orders (kind manual); the S&P gate and the hours do not
    if value < KILL_VALUE:
        hard.append(f"account value ${value:.2f} is under ${KILL_VALUE:.0f}: no new orders; tell Vamsi")
    if day_pnl <= -DAY_LOSS:
        hard.append(f"down ${-day_pnl:.2f} today: no new orders until tomorrow")
    if final_day and et.hour * 60 + et.minute > 14 * 60 + 55:
        hard.append("final day after 14:55: no new orders")
    blocked = list(hard)
    if spy_day is not None and spy_day <= SPY_MIN:
        blocked.append(f"SPY {spy_day:+.2f}% on the day: no dip buys (S&P gate)")
    if et.hour < 7 or (et.hour * 60 + et.minute) > 15 * 60 + 30 or not pfm.is_business_day(et.date()):
        blocked.append("outside 7:00-15:30 ET on a business day: no new orders")
    pause = s.get("pause") or {}
    if pause.get("until") and et.date().isoformat() <= pause["until"]:
        blocked.append(f"Vamsi paused the real book's own entries through {pause['until']}: {pause.get('why', '')}")
    buys = open_orders(a, "buy", "entry", s)
    manual = open_orders(a, "buy", "manual", s)
    skip = {x.strip().upper() for x in a_.skip.split(",") if x.strip()}
    cancelled = set()
    for o, why in ([(o, blocked[0]) for o in buys] if blocked else []) + ([(o, hard[0]) for o in manual] if hard else []) \
            + [(o, f"{o['symbol']}: an offering or material company news today") for o in buys + manual
               if o["symbol"] in skip]:
        if o["id"] not in cancelled:
            cancelled.add(o["id"])
            acts.append({"do": "cancel", "order_id": o["id"], "symbol": o["symbol"], "why": why})
    for b in blocked:
        print("  NO NEW ORDERS:", b)
    rows, why_not = entry_candidates(s, a, skip)
    gate = od.btc_gate()
    held = buys + manual
    slots = MAX_POS - len(s["plans"]) - len(held)
    crypto = sum(1 for t in list(s["plans"]) + [o["symbol"] for o in held] if t in lv.CRYPTO_LINKED)
    free = cash - sum(float(o.get("price") or 0) * float(o.get("quantity") or 0) for o in held)
    print(f"  {gate['why']}")
    print(f"  {slots} free slots, ${free:.2f} cash after open buy orders; candidates (support {MIN_STRENGTH}+ touches, "
          f"R:R {MIN_RR}+, within {NEAR:.0f}% of support, not up {MAX_RET5} ATR over 5 sessions):")
    radar = {r["ticker"]: r for r in json.loads(lv.RADAR.read_text())["names"]}
    minute = et.hour * 60 + et.minute
    for x in rows:
        o = odds_of(x["symbol"], x["price"], x["limit"], radar, q, minute)
        x["odds"], x["k"] = o if o else (None, None)
        print(f"    {x['symbol']:6} {x['price']:>9.4g} limit {x['limit']} stop {x['stop']} target {x['target']} "
              f"R:R {x['rr']} tested {x['strength']}x 5-session {x['ret5']:+.2f} ATR {x['dist']:+.1f}% above"
              + (f", {x['k']:.2f} ATR to the limit, {x['odds']:.0%} fill odds" if o else "")
              + f"{' [crypto]' if x['crypto'] else ''}")
    for o in held:
        r = odds_of(o["symbol"], price_of(q.get(o["symbol"])), float(o["price"]), radar, q, minute)
        tag = " (Vamsi's order: kept by the swap rule and the S&P gate)" if o in manual else ""
        if r:
            print(f"  open buy {o['symbol']} limit {float(o['price']):g}: {r[1]:.2f} ATR to the limit, {r[0]:.0%} fill odds{tag}")
    for w in why_not:
        print("    skipped", w)
    if not blocked:
        for x in rows:
            if slots <= 0:
                break
            if x["crypto"] and (crypto >= MAX_CRYPTO or not gate["ok"]):
                continue
            usd = min(value * lv.MAX_SIZE_PCT / 100, value * lv.RISK_PCT / 100 / ((x["limit"] - x["stop"]) / x["limit"]),
                      MAX_USD, free)
            qty = math.floor(usd / x["limit"])
            if qty < 1:
                print(f"    {x['symbol']}: ${usd:.2f} buys no whole share at {x['limit']}")
                continue
            acts.append(entry_action(x, qty))
            slots -= 1
            free -= qty * x["limit"]
            crypto += x["crypto"]
    if not blocked and SWAP_WINDOW[0] <= minute <= SWAP_WINDOW[1]:
        chosen = {x["symbol"] for x in acts if x.get("kind") == "entry"}
        pool = [x for x in rows if x["symbol"] not in chosen and (x.get("odds") or 0) >= SWAP_TO]
        weak = []
        for o in buys:
            r = odds_of(o["symbol"], price_of(q.get(o["symbol"])), float(o["price"]), radar, q, minute)
            if r and r[0] < SWAP_BELOW:
                weak.append((r[0], r[1], o))
        for p_o, k_o, o in sorted(weak, key=lambda w: w[0]):
            res = float(o["price"]) * float(o["quantity"])
            c_after = crypto - (o["symbol"] in lv.CRYPTO_LINKED)
            pick = next((x for x in pool if not (x["crypto"] and (c_after >= MAX_CRYPTO or not gate["ok"]))), None)
            if pick is None:
                print(f"  KEEP {o['symbol']}: {p_o:.0%} fill odds, but no waiting name has {SWAP_TO:.0%}+")
                continue
            usd = min(value * lv.MAX_SIZE_PCT / 100,
                      value * lv.RISK_PCT / 100 / ((pick["limit"] - pick["stop"]) / pick["limit"]), MAX_USD, free + res)
            qty = math.floor(usd / pick["limit"])
            if qty < 1:
                continue
            acts.append({"do": "cancel", "order_id": o["id"], "symbol": o["symbol"],
                         "why": (f"very unlikely to fill: {k_o:.2f} ATR above the limit {float(o['price']):g} at "
                                 f"{et:%H:%M}, {p_o:.0%} odds by the close; replaced by {pick['symbol']} "
                                 f"({pick['odds']:.0%}) (Vamsi, Oct 6)")})
            acts.append(entry_action(pick, qty, f"; {pick['odds']:.0%} fill odds, replaces {o['symbol']} ({p_o:.0%})"))
            pool.remove(pick)
            free += res - qty * pick["limit"]
            crypto = c_after + pick["crypto"]
    save_state(s)
    print(f"ACTIONS ({len(acts)}): review_equity_order, then place_equity_order (market_hours regular_hours, a fresh "
          f"ref_id each), then record each one with real.py record")
    for x in acts:
        print("  " + json.dumps(x))
    return 0


def cmd_record(a_) -> int:
    s = load_state()
    if a_.what == "order":
        rec = {"kind": a_.kind, "symbol": a_.symbol.upper(), "qty": a_.qty, "price": a_.price, "stop": a_.stop,
               "target": a_.target, "why": a_.why, "placed": pfm.iso(now_utc()), "state": "placed"}
        s["orders"][a_.id] = rec
        if a_.kind == "stop" and rec["symbol"] in s["plans"]:
            s["plans"][rec["symbol"]]["stop_order_id"] = a_.id
        verb = {"entry": "Buy limit", "manual": "Buy limit (Vamsi's order)", "stop": "Stop order", "exit": "Sell"}[a_.kind]
        note(s, "trade", f"{verb} placed: {rec['symbol']} {a_.qty:g} at {a_.price}",
             f"{verb} {rec['symbol']} {a_.qty:g} at {a_.price}" + (f", stop {a_.stop}, target {a_.target}" if a_.kind in ("entry", "manual") else "")
             + f". {a_.why}", [rec["symbol"]])
    elif a_.what == "pause":
        if a_.off:
            s.pop("pause", None)
            note(s, "plan", "Entries resumed", a_.why or "Vamsi resumed the real book's own entries.")
        else:
            s["pause"] = {"until": a_.until, "why": a_.why}
            note(s, "plan", f"Entries paused through {a_.until}", a_.why)
    elif a_.what == "cancel":
        rec = s["orders"].get(a_.id)
        if rec:
            rec["state"] = "cancel requested"
        note(s, "trade", f"Order cancelled: {rec['symbol'] if rec else a_.id[:8]}", a_.why or "", [rec["symbol"]] if rec else [])
    else:
        note(s, a_.kind or "note", a_.title, a_.body)
    save_state(s)
    print("recorded", a_.what)
    return 0


def cmd_snapshot(a_) -> int:
    s, a = load_state(), load_account()
    q = quotes()
    now = now_utc()
    value, cash = float(a["total_value"]), float(a["cash"])
    held = {p["symbol"]: p for p in a["positions"] if float(p["quantity"]) > 0}
    positions = []
    for sym, h in held.items():
        qty, avg = float(h["quantity"]), float(h["average_buy_price"])
        qq = q.get(sym) or {}
        px = price_of(qq) or avg
        p = s["plans"].get(sym, {})
        mv = qty * px
        positions.append({"ticker": sym, "label": sym, "asset": "stock", "qty": qty, "avg_cost": avg,
                          "cost_basis": round(qty * avg, 2), "price": px, "prev_close": qq.get("prev_close"),
                          "market_value": round(mv, 2), "unrealized_pnl": round(mv - qty * avg, 2),
                          "unrealized_pct": round((px / avg - 1) * 100, 2),
                          "day_pnl": round(qty * (px - qq["prev_close"]), 2) if qq.get("prev_close") else None,
                          "weight_pct": round(mv / value * 100, 2) if value else None, "name": qq.get("name", sym),
                          "thesis": p.get("why", "Not opened by the real book."), "stop": p.get("stop"),
                          "target": p.get("target"), "opened": p.get("opened")})
    realized = sum(c["pnl"] for c in s["closed"])
    unreal = sum(p["unrealized_pnl"] for p in positions)
    trades = []
    for oid, o in sorted(s["orders"].items(), key=lambda kv: kv[1]["placed"]):
        trades.append({"id": oid[:8], "type": "BUY" if o["kind"] == "entry" else "SELL", "ts": o["placed"],
                       "ticker": o["symbol"], "qty": o["qty"], "price": o["price"], "state": o.get("state"),
                       "rationale": o.get("why", ""), "plan": {"stop": o.get("stop"), "target": o.get("target")}})
    hist = s["history"] or [{"t": START_UTC, "value": START_VALUE}]
    base_spy = next((h["SPY"] for h in hist if h.get("SPY")), None)
    base_qqq = next((h["QQQ"] for h in hist if h.get("QQQ")), None)
    eq = {"t": [h["t"] for h in hist], "equity": [h["value"] for h in hist],
          "SPY": [round((h["SPY"] / base_spy - 1) * 100, 3) if h.get("SPY") and base_spy else None for h in hist],
          "QQQ": [round((h["QQQ"] / base_qqq - 1) * 100, 3) if h.get("QQQ") and base_qqq else None for h in hist]}
    challenge = pfm.load_config()
    snap = {"id": now.strftime("%Y%m%dT%H%M%SZ"), "book": "real", "as_of": pfm.iso(now),
            "quotes_generated_at": json.loads((ROOT / ".cache" / "quotes.json").read_text()).get("generated_at"),
            "session": pfm.market_session(now),
            "challenge": {"name": "Real money (Robinhood agentic account)", "short_name": "Real",
                          "start_capital": s["start_value"], "accepted_utc": s["opened"], "trading_start_utc": START_UTC,
                          "end_utc": challenge["end_utc"], "goal_equity": None,
                          "account": {"type": f"Robinhood limited margin account {masked()} (no margin borrowing)",
                                      "margin": False}},
            "summary": {"as_of": pfm.iso(now), "start_capital": s["start_value"], "deposits": s["start_value"],
                        "equity": value, "cash": cash, "invested_value": round(value - cash, 2),
                        "net_profit": round(value - s["start_value"], 2),
                        "return_pct": round((value / s["start_value"] - 1) * 100, 2), "goal_equity": None,
                        "realized_pnl": round(realized, 2), "unrealized_pnl": round(unreal, 2),
                        "day_pnl": round(value - s["day"].get("start_value", value), 2),
                        "counts": {"orders_total": len(s["orders"]), "closed_trades": len(s["closed"])}},
            "positions": positions, "trades": trades, "closed": s["closed"], "equity": eq,
            "journal": list(reversed(s["journal"]))[:40],
            "orders": [o for o in a["orders"] if o["state"] in OPEN_STATES],
            "strategy": RULES, "note": "Private: real-account data, shown only on the private dashboard."}
    SNAPSHOT.write_text(json.dumps(snap, indent=1) + "\n")
    print(f"doc_id={snap['id']} value={value:.2f} positions={len(positions)} open_orders={len(snap['orders'])}")
    return 0


def cmd_status(a_) -> int:
    s = load_state()
    print(json.dumps({k: s[k] for k in ("plans", "day")}, indent=1))
    print(f"{len(s['closed'])} closed, {len(s['orders'])} orders, {len(s['journal'])} journal entries, "
          f"{len(s['history'])} history points")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--skip", default="")
    rec = sub.add_parser("record")
    rec.add_argument("what", choices=["order", "cancel", "note", "pause"])
    rec.add_argument("--until", default="")
    rec.add_argument("--off", action="store_true")
    rec.add_argument("--id", default="")
    rec.add_argument("--symbol", default="")
    rec.add_argument("--kind", default=None)
    rec.add_argument("--qty", type=float, default=0.0)
    rec.add_argument("--price", type=float, default=None)
    rec.add_argument("--stop", type=float, default=None)
    rec.add_argument("--target", type=float, default=None)
    rec.add_argument("--why", default="")
    rec.add_argument("--title", default="")
    rec.add_argument("--body", default="")
    sub.add_parser("snapshot")
    sub.add_parser("status")
    a = ap.parse_args()
    return {"run": cmd_run, "record": cmd_record, "snapshot": cmd_snapshot, "status": cmd_status}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
