#!/usr/bin/env python3
"""Record a paper trade against the latest synced quote, with cash-account
checks. Appends to the book's ledger (default book: guided, or $BOOK).

  python scripts/trade.py buy  IONQ --usd 400 --why "..." [--stop 40 --target 60]
  python scripts/trade.py sell IONQ --all --why "..."
  python scripts/trade.py buy NKE261002C00036000 --qty 2 --why "..."   # 2 contracts
  python scripts/trade.py buy BTC-USD --usd 250 --why "..."
  python scripts/trade.py expire NKE261002C00036000 --why "expired"    # after expiry
Add --dry-run to validate without writing.

Fills: stocks/ETFs at the last trade plus slippage (extended hours need a live
print); options at the ask to buy and the bid to sell (Yahoo option chain,
regular session only); crypto at the last trade plus/minus the broker spread, 24/7.
"""
from __future__ import annotations

import argparse
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


def option_quote(tk: str, quotes: dict) -> dict | None:
    """Freshest bid/ask for a contract: the synced option chains, else quotes.json."""
    path = ROOT / ".cache" / "options.json"
    if path.exists():
        doc = json.loads(path.read_text())
        o = pfm.parse_option(tk)
        chain = (doc.get("underlyings", {}).get(o["underlying"]) or {}).get("chains", {}).get(o["expiry"]) or {}
        for row in chain.get("calls" if o["type"] == "call" else "puts", []):
            if row.get("contract") == tk:
                return {**row, "time": doc["generated_at"], "spot": doc["underlyings"][o["underlying"]].get("spot")}
    q = quotes.get(tk)
    return {**q, "time": q.get("time")} if q else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", default=None, help="guided (the only book)")
    ap.add_argument("side", choices=["buy", "sell", "expire"])
    ap.add_argument("ticker")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--usd", type=float)
    g.add_argument("--qty", type=float, help="shares, coins or option contracts")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--why", required=True)
    ap.add_argument("--tags", default="")
    ap.add_argument("--stop", type=float)
    ap.add_argument("--target", type=float)
    ap.add_argument("--broker-quote", default="",
                    help="options only: BID,ASK,UTC-TIME from the broker's read-only quote, used when the "
                         "synced chain shows no bid/ask (recorded in the transaction)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.side != "expire" and a.usd is None and a.qty is None and not a.all:
        fail("give --usd, --qty or --all")

    book = pfm.current_book(a.book)
    tk = a.ticker.upper()
    asset = pfm.asset_class(tk)
    mult = pfm.multiplier(tk)
    cfg = pfm.load_config(book)
    ledger = pfm.load_ledger(book)
    ledger_path = pfm.book_path("ledger", book)
    qdoc = json.loads((ROOT / ".cache" / "quotes.json").read_text())
    quotes = qdoc["quotes"]
    now = pfm.now_utc()
    em, rules = cfg["execution_model"], cfg["rules"]

    if asset != "stock" and not cfg["account"].get(asset + "s" if asset == "option" else asset):
        fail(f"the {book} book trades US stocks and ETFs only ({asset} not allowed)")
    if now > pfm.parse_ts(cfg["end_utc"]):
        fail("challenge window has ended")
    session = pfm.market_session(now)
    under = (pfm.parse_option(tk) or {}).get("underlying", tk)
    blocklist = json.loads((ROOT / "config" / "blocklist.json").read_text())
    if under in blocklist.get("tickers", {}):
        fail(f"{under} is on the restricted list: {blocklist['tickers'][under]}")

    pf = pfm.Portfolio(ledger, cfg)
    val = pf.valuation(quotes, now)
    today = pfm.et_date(now).isoformat()
    if val["counts"]["orders_today"] >= rules["max_orders_per_day"]:
        fail("daily order fuse reached (runaway-loop protection)")
    if val["counts"]["orders_total"] >= rules["max_orders_total"]:
        fail("total order fuse reached (runaway-loop protection)")

    # ---- reference price by asset class -------------------------------------
    extra = {}
    fee_per_unit = 0.0
    if a.side == "expire":
        if asset != "option" or not pfm.option_expired(tk, now):
            fail("expire is only for option contracts after their expiration close")
        uq = quotes.get(under) or {}
        if not uq.get("price"):
            fail(f"no quote for underlying {under}")
        ref, ref_time, bps = pfm.intrinsic(tk, float(uq["price"])), uq.get("time"), 0.0
        age = 0
        fill = round(ref, 4)
        extra = {"underlying_price": uq["price"]}
    elif asset == "option":
        oem = em["options"]
        if session not in oem["sessions_allowed"]:
            fail(f"options trade in the regular session only (now '{session}')")
        oq = option_quote(tk, quotes)
        if not oq:
            fail(f"no option-chain quote for {tk}; add {under} to options_watch and re-sync")
        age = (now - pfm.parse_ts(oq["time"])).total_seconds()
        if age > oem["max_quote_age_sec"]:
            fail(f"option chain for {under} is {int(age)}s old (max {oem['max_quote_age_sec']}s); re-sync")
        bid, ask, last = oq.get("bid") or 0.0, oq.get("ask") or 0.0, oq.get("last") or 0.0
        source = "option chain (yfinance)"
        if a.broker_quote:
            if bid > 0 and ask > 0:
                fail(f"the synced chain has a live quote for {tk} (bid {bid}, ask {ask}); drop --broker-quote")
            try:
                b_, a_, t_ = a.broker_quote.split(",")
                bid, ask, bq_time = float(b_), float(a_), pfm.parse_ts(t_)
            except ValueError:
                fail("--broker-quote takes BID,ASK,UTC-TIME (e.g. 0.90,1.15,2026-10-01T13:42:09Z)")
            age = (now - bq_time).total_seconds()
            if age > oem["max_quote_age_sec"] or age < -60:
                fail(f"broker quote is {int(age)}s old (max {oem['max_quote_age_sec']}s)")
            oq = {**oq, "time": t_}
            source = "broker read-only quote (synced chain had no bid/ask)"
        if a.side == "buy":
            if ask <= 0:
                fail(f"no ask for {tk} (bid {bid}, last {last})")
            fill = round(ask, 4)
        else:
            if bid <= 0:
                fail(f"no bid for {tk} (ask {ask}, last {last}); cannot sell now")
            fill = round(bid, 4)
        ref, ref_time, bps = (ask if a.side == "buy" else bid), oq["time"], 0.0
        fee_per_unit = oem["fee_per_contract"]
        extra = {"bid": bid, "ask": ask, "last": last, "iv": oq.get("iv"), "spot": oq.get("spot"),
                 "open_interest": oq.get("oi"), "volume": oq.get("volume"), "quote_source": source}
    elif asset == "crypto":
        cem = em["crypto"]
        q = quotes.get(tk)
        if not q or not q.get("price"):
            fail(f"no synced quote for {tk}; add it to the data run first")
        ref, ref_time = float(q["price"]), q.get("time") or qdoc["generated_at"]
        age = (now - pfm.parse_ts(ref_time)).total_seconds()
        if age > cem["max_quote_age_sec"]:
            fail(f"last {tk} trade is {int(age)}s old (max {cem['max_quote_age_sec']}s); re-sync")
        bps = float(cem["spread_bps"])
        fill = round(ref * (1 + bps / 10_000) if a.side == "buy" else ref * (1 - bps / 10_000), 6)
    else:
        if session not in em.get("sessions_allowed", ["regular"]):
            fail(f"market session is '{session}'; orders execute {em['sessions']}")
        q = quotes.get(tk)
        if not q or not q.get("price"):
            fail(f"no synced quote for {tk}; add it to the data run first")
        if q.get("stale"):
            fail(f"quote for {tk} is marked stale")
        extended = session != "regular"
        if extended:
            if not q.get("ext_price") or not q.get("ext_time"):
                fail(f"no {session}-market trade in {tk} yet this session; extended-hours orders need a live print")
            ref, ref_time = float(q["ext_price"]), q["ext_time"]
        else:
            ref, ref_time = float(q["price"]), q.get("time") or qdoc["generated_at"]
        age = (now - pfm.parse_ts(ref_time)).total_seconds()
        if age > em["max_quote_age_sec"]:
            fail(f"last {session} trade in {tk} is {int(age)}s old (max {em['max_quote_age_sec']}s); re-sync")
        bps = pfm.slippage_bps(ref, cfg, extended)
        fill = round(ref * (1 + bps / 10_000) if a.side == "buy" else ref * (1 - bps / 10_000), 4)

    compliance = {"session": session, "quote_age_sec": int(age), "cash_account": True, "asset": asset}
    name = (quotes.get(tk) or {}).get("name") or (quotes.get(under) or {}).get("name")

    if a.side == "buy":
        if a.all:
            fail("--all is only valid for sells")
        unit_cost = fill * mult + fee_per_unit
        if a.usd is not None:
            if asset == "option":
                qty = float(math.floor(a.usd / unit_cost))
            else:
                dp = 8 if asset == "crypto" else 4
                qty = math.floor(a.usd / fill * 10 ** dp) / 10 ** dp
        else:
            qty = float(int(a.qty)) if asset == "option" else a.qty
        if qty <= 0:
            fail("quantity rounds to zero")
        gross = round(qty * fill * mult, 2)
        fees = round(qty * fee_per_unit, 2)
        if gross + fees > pf.cash + 1e-6:
            fail(f"insufficient cash: need {gross + fees:.2f}, have {pf.cash:.2f}")
        held_mv = next((p["market_value"] for p in val["positions"] if p["ticker"] == tk), 0.0)
        weight = (held_mv + gross) / val["equity"] * 100
        if weight > rules["max_position_pct_at_entry"] + 1e-6:
            fail(f"position would be {weight:.1f}% of equity (cap {rules['max_position_pct_at_entry']}%)")
        settled, _ = pf.settled_cash_on(pfm.et_date(now))
        compliance.update({
            "funded_with_settled_cash": gross + fees <= settled + 1e-6,
            "position_weight_pct": round(weight, 1),
        })
        net_cash = -round(gross + fees, 2)
    else:
        held = pf.position_qty(tk)
        if held <= 0:
            fail(f"no position in {tk}")
        if a.usd is not None:
            fail("use --qty or --all for sells")
        qty = held if (a.all or a.side == "expire" or a.qty is None) else a.qty
        if qty > held + 1e-9:
            fail(f"cannot sell {qty}, only {held} held")
        left, consumed = qty, []
        for lot in pf.lots.get(tk, []):
            if left <= 1e-9:
                break
            consumed.append(lot)
            left -= min(lot["qty"], left)
        if asset != "crypto" and a.side == "sell":
            locked = [l for l in consumed if l["unsettled_until"] and today < l["unsettled_until"]]
            if locked:
                fail(f"good-faith-violation guard: lot {locked[0]['txn']} was bought with unsettled "
                     f"proceeds that settle {locked[0]['unsettled_until']}")
        is_dt = asset != "crypto" and a.side == "sell" and any(l["date"] == today for l in consumed)
        cap = rules.get("max_day_trades_rolling_5d")
        if is_dt and cap is not None and val["counts"]["day_trades_5d"] >= cap:
            fail("day-trade cap reached for the rolling 5-day window")
        gross = round(qty * fill * mult, 2)
        if asset == "stock":
            fees = pfm.sell_fees(qty, gross, cfg)
        else:
            fees = round(qty * fee_per_unit, 2) if a.side == "sell" else 0.0
        net_cash = round(gross - fees, 2)
        compliance.update({"day_trade": is_dt, "good_faith_ok": True})

    n = sum(1 for t in ledger["transactions"] if t["type"] != "DEPOSIT") + 1
    txn = {
        "id": f"T{n:04d}",
        "type": a.side.upper(),
        "ts": pfm.iso(now),
        "ticker": tk,
        "label": pfm.display_label(tk),
        "asset": asset,
        "name": name,
        "qty": qty,
        "multiplier": mult,
        "price": fill,
        "quote_price": ref,
        "quote_time": ref_time,
        "session": session,
        "quote_source": "yahoo-option-chain" if asset == "option" else "yahoo-v8-chart",
        "slippage_bps": bps,
        "gross": gross,
        "fees": fees,
        "net_cash": net_cash,
        "settle_date": today if asset == "crypto" else pfm.next_business_day(pfm.et_date(now)).isoformat(),
        "rationale": a.why,
        "tags": [t.strip() for t in a.tags.split(",") if t.strip()],
        "plan": {k: v for k, v in (("stop", a.stop), ("target", a.target)) if v is not None},
        "compliance": compliance,
    }
    if asset == "option":
        txn["option"] = pfm.parse_option(tk)
    if extra:
        txn["quote_detail"] = extra
    print(json.dumps(txn, indent=2))
    if a.dry_run:
        print("DRY RUN: not written")
        return 0
    ledger["transactions"].append(txn)
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
    after = pfm.Portfolio(ledger, cfg).valuation(quotes, now)
    print(f"OK [{book}] {txn['id']} {txn['type']} {qty} {txn['label']} @ {fill} | cash {after['cash']:.2f} "
          f"equity {after['equity']:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
