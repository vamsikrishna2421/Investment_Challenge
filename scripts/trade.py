#!/usr/bin/env python3
"""Record a paper trade against the latest synced quote, with cash-account and
H-1B guardrail checks. Appends to ledger/transactions.json.

  python scripts/trade.py buy  IONQ --usd 400 --why "..." [--stop 40 --target 60]
  python scripts/trade.py sell IONQ --all --why "..."
  python scripts/trade.py sell IONQ --qty 3 --why "..."
Add --dry-run to validate without writing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import portfolio as pfm  # noqa: E402

ROOT = pfm.ROOT


def fail(msg: str) -> None:
    print(f"BLOCKED: {msg}")
    sys.exit(2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("side", choices=["buy", "sell"])
    ap.add_argument("ticker")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--usd", type=float)
    g.add_argument("--qty", type=float)
    g.add_argument("--all", action="store_true")
    ap.add_argument("--why", required=True)
    ap.add_argument("--tags", default="")
    ap.add_argument("--stop", type=float)
    ap.add_argument("--target", type=float)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    tk = a.ticker.upper()
    cfg = pfm.load_config()
    ledger = pfm.load_ledger()
    qdoc = json.loads((ROOT / ".cache" / "quotes.json").read_text())
    quotes = qdoc["quotes"]
    now = pfm.now_utc()
    em, rules = cfg["execution_model"], cfg["rules"]

    session = pfm.market_session(now)
    if session not in em.get("sessions_allowed", ["regular"]):
        fail(f"market session is '{session}'; orders execute {em['sessions']}")
    if now > pfm.parse_ts(cfg["end_utc"]):
        fail("challenge window has ended")
    blocklist = json.loads((ROOT / "config" / "blocklist.json").read_text())
    if tk in blocklist.get("tickers", {}):
        fail(f"{tk} is on the restricted list: {blocklist['tickers'][tk]}")
    q = quotes.get(tk)
    if not q or not q.get("price"):
        fail(f"no synced quote for {tk}; add it to the data run first")
    if q.get("stale"):
        fail(f"quote for {tk} is marked stale")
    extended = session != "regular"
    if extended:
        if not q.get("ext_price") or not q.get("ext_time"):
            fail(f"no {session}-market trade in {tk} yet this session; extended-hours orders need a live print")
        ref_price, ref_time = float(q["ext_price"]), q["ext_time"]
    else:
        ref_price, ref_time = float(q["price"]), q.get("time") or qdoc["generated_at"]
    age = (now - pfm.parse_ts(ref_time)).total_seconds()
    if age > em["max_quote_age_sec"]:
        fail(f"last {session} trade in {tk} is {int(age)}s old (max {em['max_quote_age_sec']}s); re-sync")

    pf = pfm.Portfolio(ledger, cfg)
    val = pf.valuation(quotes, now)
    today = pfm.et_date(now).isoformat()
    if val["counts"]["orders_today"] >= rules["max_orders_per_day"]:
        fail("daily order fuse reached (runaway-loop protection)")
    if val["counts"]["orders_total"] >= rules["max_orders_total"]:
        fail("total order fuse reached (runaway-loop protection)")

    ref = ref_price
    bps = pfm.slippage_bps(ref, cfg, extended)
    compliance = {"session": session, "quote_age_sec": int(age), "cash_account": True}

    if a.side == "buy":
        if a.all:
            fail("--all is only valid for sells")
        fill = round(ref * (1 + bps / 10_000), 4)
        if a.usd is not None:
            qty = math.floor(a.usd / fill * 10_000) / 10_000
        else:
            qty = a.qty
        gross = round(qty * fill, 2)
        if qty <= 0:
            fail("quantity rounds to zero")
        if gross > pf.cash + 1e-6:
            fail(f"insufficient cash: need {gross:.2f}, have {pf.cash:.2f}")
        held_mv = next((p["market_value"] for p in val["positions"] if p["ticker"] == tk), 0.0)
        weight = (held_mv + gross) / val["equity"] * 100
        if weight > rules["max_position_pct_at_entry"] + 1e-6:
            fail(f"position would be {weight:.1f}% of equity (cap {rules['max_position_pct_at_entry']}%)")
        settled, _ = pf.settled_cash_on(pfm.et_date(now))
        compliance.update({
            "funded_with_settled_cash": gross <= settled + 1e-6,
            "position_weight_pct": round(weight, 1),
        })
        fees = 0.0
        net_cash = -gross
    else:
        held = pf.position_qty(tk)
        if held <= 0:
            fail(f"no position in {tk}")
        qty = held if a.all else (held if a.qty is None else a.qty)
        if a.usd is not None:
            fail("use --qty or --all for sells")
        if qty > held + 1e-9:
            fail(f"cannot sell {qty}, only {held} held")
        # FIFO lots that this sale consumes
        left, consumed = qty, []
        for lot in pf.lots.get(tk, []):
            if left <= 1e-9:
                break
            consumed.append(lot)
            left -= min(lot["qty"], left)
        locked = [l for l in consumed if l["unsettled_until"] and today < l["unsettled_until"]]
        if locked:
            fail(f"good-faith-violation guard: lot {locked[0]['txn']} was bought with unsettled "
                 f"proceeds that settle {locked[0]['unsettled_until']}")
        is_dt = any(l["date"] == today for l in consumed)
        cap = rules.get("max_day_trades_rolling_5d")
        if is_dt and cap is not None and val["counts"]["day_trades_5d"] >= cap:
            fail("day-trade cap reached for the rolling 5-day window")
        fill = round(ref * (1 - bps / 10_000), 4)
        gross = round(qty * fill, 2)
        fees = pfm.sell_fees(qty, gross, cfg)
        net_cash = round(gross - fees, 2)
        compliance.update({"day_trade": is_dt, "good_faith_ok": True})

    n = sum(1 for t in ledger["transactions"] if t["type"] in ("BUY", "SELL")) + 1
    txn = {
        "id": f"T{n:04d}",
        "type": a.side.upper(),
        "ts": pfm.iso(now),
        "ticker": tk,
        "name": q.get("name"),
        "qty": qty,
        "price": fill,
        "quote_price": ref,
        "quote_time": ref_time,
        "session": session,
        "quote_source": q.get("source", "yahoo-v8-chart"),
        "slippage_bps": bps,
        "gross": gross,
        "fees": fees,
        "net_cash": net_cash,
        "settle_date": pfm.next_business_day(pfm.et_date(now)).isoformat(),
        "rationale": a.why,
        "tags": [t.strip() for t in a.tags.split(",") if t.strip()],
        "plan": {k: v for k, v in (("stop", a.stop), ("target", a.target)) if v is not None},
        "compliance": compliance,
    }
    print(json.dumps(txn, indent=2))
    if a.dry_run:
        print("DRY RUN: not written")
        return 0
    ledger["transactions"].append(txn)
    (ROOT / "ledger" / "transactions.json").write_text(json.dumps(ledger, indent=2) + "\n")
    after = pfm.Portfolio(ledger, cfg).valuation(quotes, now)
    print(f"OK {txn['id']} {txn['type']} {qty} {tk} @ {fill} | cash {after['cash']:.2f} "
          f"equity {after['equity']:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
