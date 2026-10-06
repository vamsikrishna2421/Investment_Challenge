#!/usr/bin/env python3
"""Resting orders for the paper book (Vamsi, Mon Oct 5: put a buy at the support price so it fills by itself
when the price gets there, and the book doesn't miss the dips that happen between runs).

  python scripts/orders.py plan [--place] [--skip A,B]   radar names near their zones -> DAY buy limits
  python scripts/orders.py place TICKER --limit L --usd X --stop S --target T --why "..." [--tags radar]
  python scripts/orders.py cancel ID-or-TICKER --why "..."
  python scripts/orders.py list
  python scripts/orders.py fill                          every run, right after the sync

Model (what a Robinhood cash account supports, so the paper record carries over to a real one):
  buy limit   a DAY order, regular session only, placed for about 25% of equity and reserved from settled
              cash. It fills when a 1-minute bar trades at least 1 cent through the limit: at the limit, or at
              the bar's open when the bar opens below it (a gap fills at the open, which can be under the stop).
  stop        each position's plan stop is a resting stop-market sell, regular session only: it fills when a
              1-minute bar trades at or below the stop, at the stop or the bar's open if lower, less the
              trade.py slippage.
  target      Robinhood holds shares for one sell order at a time, so the sell zone stays a run check
              (TARGET HIT: cancel the stop and sell at that run with trade.py).
Bars are read from the order's placement (or the position's entry) to the last complete minute, and a fill is
recorded at the minute it would have happened. A buy order is cancelled before the open when the pre-market
price is at or under its stop (gapping through support). DAY orders expire at the 4:00 PM close.
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
import marketdata as md  # noqa: E402
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT
TICK = 0.01
SLOTS = 4
SIZE_PCT = 25.0
NEAR_PCT = 5.0
MAX_CRYPTO = 2


def path(book: str | None = None) -> Path:
    return pfm.book_path("ledger", book).parent / "orders.json"


def load(book: str | None = None) -> dict:
    p = path(book)
    return json.loads(p.read_text()) if p.exists() else {"orders": [], "stops_checked": {}}


def save(doc: dict, book: str | None = None) -> None:
    path(book).write_text(json.dumps(doc, indent=2) + "\n")


def state(book: str | None = None):
    cfg = pfm.load_config(book)
    ledger = pfm.load_ledger(book)
    qdoc = json.loads((ROOT / ".cache" / "quotes.json").read_text())
    pf = pfm.Portfolio(ledger, cfg)
    now = pfm.now_utc()
    val = pf.valuation(qdoc["quotes"], now)
    return cfg, ledger, qdoc, pf, val, now


def plans(ledger: dict) -> dict:
    """Stop and target per ticker from its latest buy."""
    out = {}
    for t in sorted(ledger["transactions"], key=lambda x: (x["ts"], x["id"])):
        if t["type"] == "BUY":
            out[t["ticker"]] = t.get("plan") or {}
    return out


def reserved(doc: dict) -> float:
    return sum(o["usd"] for o in doc["orders"] if o["status"] == "open" and o["side"] == "buy")


def session_close(d: dt.date) -> dt.datetime:
    return dt.datetime(d.year, d.month, d.day, 16, 0, tzinfo=pfm.ET).astimezone(pfm.UTC)


def bars_since(sym: str, since: dt.datetime, now: dt.datetime) -> list[tuple]:
    """Complete regular-session 1-minute bars that start after `since`: (start_utc, open, high, low, close)."""
    rng = "1d" if pfm.et_date(since) == pfm.et_date(now) else "5d"
    r = md.yahoo_chart(sym, rng, "1m", False)
    q = ((r.get("indicators") or {}).get("quote") or [{}])[0]
    start = since.replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    out = []
    for i, t in enumerate(r.get("timestamp") or []):
        o, h, lo, c = (q.get(k, [None] * (i + 1))[i] for k in ("open", "high", "low", "close"))
        if None in (o, h, lo, c):
            continue
        b = dt.datetime.fromtimestamp(t, pfm.UTC)
        et = b.astimezone(pfm.ET)
        if not (570 <= et.hour * 60 + et.minute < 960):
            continue
        if b < start or b + dt.timedelta(minutes=1) > now:
            continue
        out.append((b, float(o), float(h), float(lo), float(c)))
    return out


def txn_for(ledger: dict, cfg: dict, side: str, tk: str, qty: float, price: float, ts: dt.datetime, ref: float,
            bps: float, why: str, tags: list, plan: dict, compliance: dict, name: str | None) -> dict:
    gross = round(qty * price, 2)
    fees = pfm.sell_fees(qty, gross, cfg) if side == "SELL" else 0.0
    n = sum(1 for t in ledger["transactions"] if t["type"] != "DEPOSIT") + 1
    d = pfm.et_date(ts)
    return {
        "id": f"T{n:04d}", "type": side, "ts": pfm.iso(ts), "ticker": tk, "label": pfm.display_label(tk),
        "asset": "stock", "name": name, "qty": qty, "multiplier": 1, "price": round(price, 4),
        "quote_price": ref, "quote_time": pfm.iso(ts), "session": "regular", "quote_source": "yahoo-1m-bars",
        "slippage_bps": bps, "gross": gross, "fees": fees,
        "net_cash": -gross if side == "BUY" else round(gross - fees, 2),
        "settle_date": pfm.next_business_day(d).isoformat(), "rationale": why, "tags": tags, "plan": plan,
        "compliance": compliance,
    }


# ---------------------------------------------------------------------------------------------------------
def cmd_fill(a) -> int:
    cfg, ledger, qdoc, pf, val, now = state(a.book)
    doc = load(a.book)
    quotes = qdoc["quotes"]
    session = pfm.market_session(now)
    events = []
    # 1. pre-market guard: a buy order whose stop is already gone before the open
    for o in doc["orders"]:
        if o["status"] == "open" and o["side"] == "buy" and session == "pre":
            q = quotes.get(o["ticker"]) or {}
            ep = q.get("ext_price")
            if ep and o.get("stop") and float(ep) <= o["stop"]:
                o.update(status="cancelled", closed=pfm.iso(now),
                         note=f"pre-market {ep} at or under the stop {o['stop']}: gapping through support")
                events.append(f"CANCELLED {o['id']} buy {o['ticker']}: {o['note']}")
    # 2. buy limits
    for o in [o for o in doc["orders"] if o["status"] == "open" and o["side"] == "buy"]:
        since = max(pfm.parse_ts(o["placed"]), pfm.parse_ts(o.get("checked_through") or o["placed"]))
        try:
            bars = bars_since(o["ticker"], since, now)
        except Exception as e:  # noqa: BLE001
            events.append(f"NO DATA {o['ticker']}: {str(e)[:80]}")
            continue
        hit = next((b for b in bars if b[3] <= o["limit"] - TICK), None)
        if bars:
            o["checked_through"] = pfm.iso(bars[-1][0] + dt.timedelta(minutes=1))
        if not hit:
            continue
        b, op = hit[0], hit[1]
        price = op if op <= o["limit"] - TICK else o["limit"]
        qty = math.floor(o["usd"] / price * 10_000) / 10_000
        pf_now = pfm.Portfolio(ledger, cfg)
        settled, _ = pf_now.settled_cash_on(pfm.et_date(b))
        name = (quotes.get(o["ticker"]) or {}).get("name")
        txn = txn_for(ledger, cfg, "BUY", o["ticker"], qty, price, b, o["limit"], 0.0,
                      f"Resting buy limit {o['id']} filled: {o['why']}", o.get("tags", []),
                      {k: o[k] for k in ("stop", "target") if o.get(k) is not None},
                      {"session": "regular", "order": o["id"], "order_type": "limit", "limit": o["limit"],
                       "gap_fill": price < o["limit"], "cash_account": True, "asset": "stock",
                       "funded_with_settled_cash": qty * price <= settled + 1e-6}, name)
        ledger["transactions"].append(txn)
        o.update(status="filled", closed=pfm.iso(b), fill={"txn": txn["id"], "price": txn["price"], "qty": qty,
                                                          "ts": txn["ts"]})
        doc["stops_checked"][o["ticker"]] = pfm.iso(b)
        events.append(f"FILLED {o['id']} BUY {qty} {o['ticker']} @ {txn['price']} at "
                      f"{b.astimezone(pfm.ET):%a %H:%M} ET ({'gap below the limit' if price < o['limit'] else 'limit'}) "
                      f"-> {txn['id']}")
    # 3. stops on every position
    pf = pfm.Portfolio(ledger, cfg)
    plan = plans(ledger)
    for tk, lots in sorted(pf.lots.items()):
        stop = (plan.get(tk) or {}).get("stop")
        if not stop or pfm.asset_class(tk) != "stock":
            continue
        opened = pfm.parse_ts(min(l["ts"] for l in lots))
        since = max(opened, pfm.parse_ts(doc["stops_checked"].get(tk) or pfm.iso(opened)))
        try:
            bars = bars_since(tk, since, now)
        except Exception as e:  # noqa: BLE001
            events.append(f"NO DATA {tk}: {str(e)[:80]}")
            continue
        hit = next((b for b in bars if b[3] <= stop), None)
        if bars:
            doc["stops_checked"][tk] = pfm.iso(bars[-1][0] + dt.timedelta(minutes=1))
        if not hit:
            continue
        b, op = hit[0], hit[1]
        base = op if op < stop else stop
        bps = pfm.slippage_bps(base, cfg)
        price = round(base * (1 - bps / 10_000), 4)
        qty = pf.position_qty(tk)
        d = pfm.et_date(b).isoformat()
        locked = [l for l in lots if l["unsettled_until"] and d < l["unsettled_until"]]
        txn = txn_for(ledger, cfg, "SELL", tk, qty, price, b, stop, bps,
                      f"Resting stop {stop} triggered at {b.astimezone(pfm.ET):%H:%M} ET "
                      f"({'gapped open ' + format(op, '.4g') if op < stop else 'traded through'})",
                      ["radar", "stop"], {}, {"session": "regular", "order_type": "stop", "stop": stop,
                                             "day_trade": any(l["date"] == d for l in lots),
                                             "good_faith_ok": not locked, "cash_account": True, "asset": "stock"},
                      (quotes.get(tk) or {}).get("name"))
        ledger["transactions"].append(txn)
        doc["stops_checked"].pop(tk, None)
        events.append(f"STOPPED {tk}: SELL {qty} @ {txn['price']} at {b.astimezone(pfm.ET):%a %H:%M} ET -> {txn['id']}")
    # 4. DAY orders expire at the close
    for o in doc["orders"]:
        if o["status"] == "open" and now >= session_close(pfm.et_date(pfm.parse_ts(o["placed"]))):
            o.update(status="expired", closed=pfm.iso(now))
            events.append(f"EXPIRED {o['id']} buy {o['ticker']} @ {o['limit']}")
    if any(e.startswith(("FILLED", "STOPPED")) for e in events):
        pfm.book_path("ledger", a.book).write_text(json.dumps(ledger, indent=2) + "\n")
    save(doc, a.book)
    opn = [o for o in doc["orders"] if o["status"] == "open"]
    print(f"orders {pfm.iso(now)} ({session}): {len(opn)} open buy orders, ${reserved(doc):.2f} reserved; "
          f"stops watched on {len(pf.lots)} positions")
    for e in events:
        print("  " + e)
    return 0


def cmd_place(a) -> int:
    cfg, ledger, qdoc, pf, val, now = state(a.book)
    doc = load(a.book)
    tk = a.ticker.upper()
    if now > pfm.parse_ts(cfg["end_utc"]):
        print("BLOCKED: challenge window has ended")
        return 2
    blocklist = json.loads((ROOT / "config" / "blocklist.json").read_text())
    if tk in blocklist.get("tickers", {}):
        print(f"BLOCKED: {tk} is on the restricted list")
        return 2
    if any(o["status"] == "open" and o["ticker"] == tk for o in doc["orders"]) or pf.position_qty(tk) > 0:
        print(f"BLOCKED: {tk} already has an open order or a position")
        return 2
    settled, _ = pf.settled_cash_on(pfm.et_date(now))
    free = settled - reserved(doc)
    if a.usd > free + 1e-6:
        print(f"BLOCKED: ${a.usd:.2f} needs settled cash; ${free:.2f} free after open orders")
        return 2
    if a.stop is not None and a.stop >= a.limit:
        print("BLOCKED: the stop must sit under the limit")
        return 2
    n = len(doc["orders"]) + 1
    o = {"id": f"O{n:04d}", "side": "buy", "type": "limit", "tif": "day", "ticker": tk, "limit": a.limit,
         "usd": round(a.usd, 2), "stop": a.stop, "target": a.target, "why": a.why,
         "tags": [t.strip() for t in a.tags.split(",") if t.strip()], "placed": pfm.iso(now), "status": "open"}
    if a.dry_run:
        print("DRY RUN:", json.dumps(o))
        return 0
    doc["orders"].append(o)
    save(doc, a.book)
    print(f"OK {o['id']} DAY buy limit {tk} @ {a.limit} for ${o['usd']:.2f} (stop {a.stop}, target {a.target}); "
          f"${reserved(doc):.2f} of ${settled:.2f} settled cash reserved")
    return 0


def cmd_cancel(a) -> int:
    doc = load(a.book)
    key = a.ref.upper()
    hits = [o for o in doc["orders"] if o["status"] == "open" and key in (o["id"], o["ticker"])]
    for o in hits:
        o.update(status="cancelled", closed=pfm.iso(pfm.now_utc()), note=a.why)
        print(f"CANCELLED {o['id']} buy {o['ticker']} @ {o['limit']}: {a.why}")
    save(doc, a.book)
    return 0 if hits else 1


def cmd_list(a) -> int:
    doc = load(a.book)
    opn = [o for o in doc["orders"] if o["status"] == "open"]
    print(f"{len(opn)} open orders, ${reserved(doc):.2f} reserved")
    for o in opn:
        print(f"  {o['id']} {o['tif'].upper()} buy limit {o['ticker']} @ {o['limit']} ${o['usd']:.2f} "
              f"stop {o['stop']} target {o['target']} (placed {o['placed']})")
    for o in [o for o in doc["orders"] if o["status"] != "open"][-8:]:
        print(f"  {o['id']} {o['status']} {o['ticker']} @ {o['limit']} {o.get('fill') or o.get('note') or ''}")
    return 0


def cmd_plan(a) -> int:
    cfg, ledger, qdoc, pf, val, now = state(a.book)
    doc = load(a.book)
    quotes = qdoc["quotes"]
    radar = json.loads(lv.RADAR.read_text())
    skip = {s.strip().upper() for s in a.skip.split(",") if s.strip()}
    held = {p["ticker"] for p in val["positions"]}
    open_buys = [o for o in doc["orders"] if o["status"] == "open" and o["side"] == "buy"]
    taken = held | {o["ticker"] for o in open_buys}
    crypto = sum(1 for t in taken if t in lv.CRYPTO_LINKED)
    slots = SLOTS - len(held) - len(open_buys)
    settled, _ = pf.settled_cash_on(pfm.et_date(now))
    free = settled - reserved(doc)
    size = round(val["equity"] * SIZE_PCT / 100, 2)
    rows = []
    for r in radar["names"]:
        tk = r["ticker"]
        q = quotes.get(tk) or {}
        px = pfm.mark(q)[0] if q else None
        if tk in taken or tk in skip or px is None:
            continue
        lo, top = r["buy_zone"]
        if px <= r["stop"]:
            continue
        dist = (px / top - 1) * 100
        if dist > NEAR_PCT:
            continue
        rr = (r["sell_zone"][0] - top) / (top - r["stop"]) if top > r["stop"] else 0
        if rr < 1.5:
            continue
        rows.append({"ticker": tk, "price": px, "limit": round(top, 2 if top >= 1 else 4), "stop": r["stop"],
                     "target": r["sell_zone"][0], "rr": round(rr, 2), "dist": round(dist, 2),
                     "crypto": tk in lv.CRYPTO_LINKED})
    rows.sort(key=lambda x: -x["rr"])
    print(f"resting-order plan {pfm.iso(now)}: {slots} free slots, ${free:.2f} settled cash free, "
          f"${size:.2f} per order (25% of equity)")
    picks = []
    for x in rows:
        if len(picks) >= max(slots, 0):
            break
        if x["crypto"] and crypto >= MAX_CRYPTO:
            continue
        usd = min(size, free - sum(p["usd"] for p in picks))
        if usd < 25:
            break
        picks.append({**x, "usd": round(usd, 2)})
        crypto += x["crypto"]
    for x in rows:
        mark = "PLACE" if x in [{k: v for k, v in p.items() if k != "usd"} for p in picks] else "     "
        print(f"  {mark} {x['ticker']:6} {x['price']:>9.4g} limit {x['limit']} ({x['dist']:+.1f}% away) "
              f"stop {x['stop']} target {x['target']} R:R {x['rr']}{' [crypto]' if x['crypto'] else ''}")
    if not picks:
        print("  no order to place (no free slot or settled cash)" if rows else "  no radar name within 5% of its zone")
    if a.place:
        for p in picks:
            ns = argparse.Namespace(book=a.book, ticker=p["ticker"], limit=p["limit"], usd=p["usd"], stop=p["stop"],
                                    target=p["target"], tags="radar,resting",
                                    why=(f"radar buy zone top {p['limit']} (stop {p['stop']}, sell zone from "
                                         f"{p['target']}, R:R {p['rr']}); placed {p['dist']:+.1f}% above it"),
                                    dry_run=False)
            cmd_place(ns)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=None)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("plan")
    p.add_argument("--place", action="store_true")
    p.add_argument("--skip", default="", help="names with an offering or material news today")
    pl = sp.add_parser("place")
    pl.add_argument("ticker")
    pl.add_argument("--limit", type=float, required=True)
    pl.add_argument("--usd", type=float, required=True)
    pl.add_argument("--stop", type=float, required=True)
    pl.add_argument("--target", type=float)
    pl.add_argument("--why", required=True)
    pl.add_argument("--tags", default="radar,resting")
    pl.add_argument("--dry-run", action="store_true")
    c = sp.add_parser("cancel")
    c.add_argument("ref")
    c.add_argument("--why", required=True)
    sp.add_parser("list")
    sp.add_parser("fill")
    a = ap.parse_args()
    return {"plan": cmd_plan, "place": cmd_place, "cancel": cmd_cancel, "list": cmd_list, "fill": cmd_fill}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
