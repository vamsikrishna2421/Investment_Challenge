#!/usr/bin/env python3
"""Portfolio engine for the paper-trading challenge.

Replays ledger/transactions.json in time order and derives:
  * cash, T+1 settled vs unsettled cash (cash-account rules)
  * FIFO lots per ticker, realized / unrealized P&L
  * compliance flags: day trades, good-faith violations, wash-sale candidates
Valuation uses a quotes dict: {TICKER: {"price": float, "prev_close": float, ...}}.
Used both locally (trade entry, snapshots) and by the GitHub Actions data job.
"""
from __future__ import annotations

import datetime as dt
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
UTC = dt.timezone.utc

# NYSE full-day closures for 2026 (none fall inside the challenge window).
NYSE_HOLIDAYS = {
    "2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
    "2026-06-19", "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25",
}


def parse_ts(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


def iso(t: dt.datetime) -> str:
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def now_utc() -> dt.datetime:
    return dt.datetime.now(UTC).replace(microsecond=0)


def et_date(t: dt.datetime) -> dt.date:
    return t.astimezone(ET).date()


def fmt_et(t: dt.datetime) -> str:
    return t.astimezone(ET).strftime("%a %b %d, %I:%M %p ET").replace(" 0", " ")


def is_business_day(d: dt.date) -> bool:
    return d.weekday() < 5 and d.isoformat() not in NYSE_HOLIDAYS


def next_business_day(d: dt.date) -> dt.date:
    n = d + dt.timedelta(days=1)
    while not is_business_day(n):
        n += dt.timedelta(days=1)
    return n


def business_days_back(d: dt.date, n: int) -> dt.date:
    """Date of the n-th previous business day (n=4 -> 5-day rolling window start)."""
    cur = d
    while n > 0:
        cur -= dt.timedelta(days=1)
        if is_business_day(cur):
            n -= 1
    return cur


def market_session(t: dt.datetime) -> str:
    e = t.astimezone(ET)
    if not is_business_day(e.date()):
        return "closed"
    m = e.hour * 60 + e.minute
    if 4 * 60 <= m < 9 * 60 + 30:
        return "pre"
    if 9 * 60 + 30 <= m < 16 * 60:
        return "regular"
    if 16 * 60 <= m < 20 * 60:
        return "post"
    return "closed"


def load_json(p) -> dict:
    return json.loads(Path(p).read_text())


def load_config() -> dict:
    return load_json(ROOT / "config" / "challenge.json")


def load_ledger() -> dict:
    return load_json(ROOT / "ledger" / "transactions.json")


def ceil_cents(x: float) -> float:
    return math.ceil(round(x * 100, 6)) / 100.0


def slippage_bps(price: float, cfg: dict) -> float:
    for floor, bps in cfg["execution_model"]["slippage_bps_by_price"]:
        if price >= floor:
            return float(bps)
    return 50.0


def sell_fees(qty: float, gross: float, cfg: dict) -> float:
    em = cfg["execution_model"]
    sec = ceil_cents(gross * em["sec_fee_per_million"] / 1_000_000)
    taf = ceil_cents(min(math.ceil(qty) * em["finra_taf_per_share"], em["finra_taf_max"]))
    return round(sec + taf, 2)


class Portfolio:
    """Deterministic replay of the ledger."""

    def __init__(self, ledger: dict, cfg: dict):
        self.cfg = cfg
        self.txns = sorted(ledger["transactions"], key=lambda x: (x["ts"], x["id"]))
        self.cash = 0.0
        self.deposits = 0.0
        self.settled = 0.0
        self.pending: list[list] = []  # [settle_date(date), amount]
        self.lots: dict[str, list[dict]] = {}
        self.realized = 0.0
        self.realized_by_ticker: dict[str, float] = {}
        self.fees = 0.0
        self.day_trades: list[dict] = []
        self.gfv: list[dict] = []
        self.orders_by_day: dict[str, int] = {}
        self.sell_results: dict[str, dict] = {}
        self._replay()

    # -- settlement helpers -------------------------------------------------
    def _release(self, d: dt.date) -> None:
        keep = []
        for sd, amt in self.pending:
            if sd <= d:
                self.settled += amt
            else:
                keep.append([sd, amt])
        self.pending = keep

    def _fund(self, cost: float) -> dt.date | None:
        """Debit cost from settled cash first, then unsettled proceeds.
        Returns the date the funding settles if unsettled money was used."""
        if self.settled >= cost - 1e-9:
            self.settled -= cost
            return None
        need = cost - max(self.settled, 0.0)
        self.settled = min(self.settled, 0.0)
        until = None
        self.pending.sort(key=lambda p: p[0])
        for p in self.pending:
            if need <= 1e-9:
                break
            take = min(p[1], need)
            p[1] -= take
            need -= take
            until = p[0] if until is None or p[0] > until else until
        self.pending = [p for p in self.pending if p[1] > 1e-9]
        if need > 1e-6:
            self.settled -= need  # overdraft; validation blocks this for new orders
        return until

    # -- replay --------------------------------------------------------------
    def _replay(self) -> None:
        for t in self.txns:
            ts = parse_ts(t["ts"])
            d = et_date(ts)
            self._release(d)
            typ = t["type"]
            if typ == "DEPOSIT":
                self.cash += t["amount"]
                self.deposits += t["amount"]
                self.settled += t["amount"]
                continue
            self.orders_by_day[d.isoformat()] = self.orders_by_day.get(d.isoformat(), 0) + 1
            tk = t["ticker"]
            if typ == "BUY":
                cost = t["gross"] + t.get("fees", 0.0)
                self.fees += t.get("fees", 0.0)
                until = self._fund(cost)
                self.cash -= cost
                self.lots.setdefault(tk, []).append({
                    "txn": t["id"], "qty": t["qty"], "price": cost / t["qty"],
                    "date": d.isoformat(), "ts": t["ts"],
                    "unsettled_until": until.isoformat() if until else None,
                })
            elif typ == "SELL":
                qty = t["qty"]
                basis = 0.0
                consumed = []
                lots = self.lots.get(tk, [])
                while qty > 1e-9 and lots:
                    lot = lots[0]
                    take = min(lot["qty"], qty)
                    basis += take * lot["price"]
                    consumed.append({**lot, "take": take})
                    lot["qty"] -= take
                    qty -= take
                    if lot["qty"] <= 1e-9:
                        lots.pop(0)
                proceeds = t["gross"] - t.get("fees", 0.0)
                self.fees += t.get("fees", 0.0)
                pnl = proceeds - basis
                self.realized += pnl
                self.realized_by_ticker[tk] = self.realized_by_ticker.get(tk, 0.0) + pnl
                self.cash += proceeds
                self.pending.append([next_business_day(d), proceeds])
                is_dt = any(c["date"] == d.isoformat() for c in consumed)
                if is_dt:
                    self.day_trades.append({"date": d.isoformat(), "ticker": tk, "txn": t["id"]})
                for c in consumed:
                    if c["unsettled_until"] and d.isoformat() < c["unsettled_until"]:
                        self.gfv.append({"date": d.isoformat(), "ticker": tk, "txn": t["id"]})
                        break
                first_buy = min((parse_ts(c["ts"]) for c in consumed), default=ts)
                self.sell_results[t["id"]] = {
                    "realized_pnl": round(pnl, 2),
                    "cost_basis": round(basis, 2),
                    "return_pct": round(pnl / basis * 100, 2) if basis else 0.0,
                    "held_hours": round((ts - first_buy).total_seconds() / 3600, 1),
                    "day_trade": is_dt,
                }
            if tk in self.lots and not self.lots[tk]:
                del self.lots[tk]

    # -- views ---------------------------------------------------------------
    def settled_cash_on(self, d: dt.date) -> tuple[float, float]:
        s = self.settled + sum(a for sd, a in self.pending if sd <= d)
        u = sum(a for sd, a in self.pending if sd > d)
        return s, u

    def position_qty(self, tk: str) -> float:
        return sum(l["qty"] for l in self.lots.get(tk, []))

    def wash_sale_flags(self) -> list[dict]:
        out = []
        buys = [t for t in self.txns if t["type"] == "BUY"]
        for t in self.txns:
            if t["type"] != "SELL":
                continue
            r = self.sell_results.get(t["id"], {})
            if r.get("realized_pnl", 0) >= 0:
                continue
            d = et_date(parse_ts(t["ts"]))
            for b in buys:
                if b["ticker"] != t["ticker"]:
                    continue
                bd = et_date(parse_ts(b["ts"]))
                if bd > d and (bd - d).days <= 30:
                    out.append({"sell": t["id"], "rebuy": b["id"], "ticker": t["ticker"]})
        return out

    def valuation(self, quotes: dict, at: dt.datetime | None = None) -> dict:
        at = at or now_utc()
        d = et_date(at)
        positions = []
        mv_total = 0.0
        day_pnl = 0.0
        for tk, lots in sorted(self.lots.items()):
            qty = sum(l["qty"] for l in lots)
            if qty <= 1e-9:
                continue
            basis = sum(l["qty"] * l["price"] for l in lots)
            q = quotes.get(tk) or {}
            px = q.get("price")
            stale = px is None
            if px is None:
                px = basis / qty
            mv = qty * px
            mv_total += mv
            prev = q.get("prev_close")
            opened_today = all(l["date"] == d.isoformat() for l in lots)
            ref = basis / qty if (opened_today or prev is None) else prev
            dp = (px - ref) * qty
            day_pnl += dp
            locked = [l for l in lots if l["unsettled_until"] and d.isoformat() < l["unsettled_until"]]
            positions.append({
                "ticker": tk,
                "qty": round(qty, 6),
                "avg_cost": round(basis / qty, 4),
                "cost_basis": round(basis, 2),
                "price": round(px, 4),
                "prev_close": prev,
                "market_value": round(mv, 2),
                "unrealized_pnl": round(mv - basis, 2),
                "unrealized_pct": round((mv - basis) / basis * 100, 2) if basis else 0.0,
                "day_pnl": round(dp, 2),
                "day_change_pct": q.get("change_pct"),
                "ext_price": q.get("ext_price"),
                "ext_change_pct": q.get("ext_change_pct"),
                "quote_time": q.get("time"),
                "stale_quote": stale,
                "opened": min(l["ts"] for l in lots),
                "sell_locked_until": max(l["unsettled_until"] for l in locked) if locked else None,
            })
        equity = self.cash + mv_total
        for p in positions:
            p["weight_pct"] = round(p["market_value"] / equity * 100, 2) if equity else 0.0
        settled, unsettled = self.settled_cash_on(d)
        start = self.cfg["start_capital"]
        unreal = sum(p["unrealized_pnl"] for p in positions)
        window_start = business_days_back(d, 4).isoformat()
        return {
            "as_of": iso(at),
            "session": market_session(at),
            "start_capital": start,
            "deposits": round(self.deposits, 2),
            "equity": round(equity, 2),
            "cash": round(self.cash, 2),
            "settled_cash": round(settled, 2),
            "unsettled_cash": round(unsettled, 2),
            "invested_value": round(mv_total, 2),
            "net_profit": round(equity - self.deposits, 2),
            "return_pct": round((equity - self.deposits) / self.deposits * 100, 2) if self.deposits else 0.0,
            "goal_equity": round(start * self.cfg["goal_multiple"], 2),
            "goal_progress_pct": round((equity - start) / (start * (self.cfg["goal_multiple"] - 1)) * 100, 2),
            "realized_pnl": round(self.realized, 2),
            "unrealized_pnl": round(unreal, 2),
            "day_pnl": round(day_pnl, 2),
            "fees_paid": round(self.fees, 2),
            "positions": positions,
            "counts": {
                "orders_total": sum(self.orders_by_day.values()),
                "orders_today": self.orders_by_day.get(d.isoformat(), 0),
                "day_trades_5d": sum(1 for x in self.day_trades if x["date"] >= window_start),
                "day_trades_total": len(self.day_trades),
                "gfv": len(self.gfv),
                "wash_sale_flags": len(self.wash_sale_flags()),
            },
        }


def load_quotes(path: Path) -> dict:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data.get("quotes", {})


if __name__ == "__main__":
    import sys
    qpath = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / ".cache" / "quotes.json"
    pf = Portfolio(load_ledger(), load_config())
    print(json.dumps(pf.valuation(load_quotes(qpath)), indent=2))
