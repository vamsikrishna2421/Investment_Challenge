#!/usr/bin/env python3
"""One-page dossier for a shortlisted stock: the numbers behind a deep dive, gathered in one pass.

  python scripts/dossier.py TICKER [--peers A,B,C] [--save]

Sections: snapshot; the last big move and how the market traded it (after-hours peak, next open,
close, since); SEC filings for 90 days with 8-K items decoded; insider trades; trailing fundamentals;
valuation against industry peers with a fair-value range (forward EPS x peer P/E quartiles, EBITDA x
peer EV/EBITDA, sales x peer EV/sales) and the multiple the current price implies; analyst targets;
the next earnings date and its consensus. It ends with the questions a written deep dive must answer
from the primary sources (the release and the 8-K exhibit: python scripts/sec.py TICKER --exhibit).

--save writes research/dossiers/<TICKER>-<date>.md; the written analysis goes below the numbers.
A fair-value range here is arithmetic on other companies' multiples, not a forecast: it shows which
assumptions the current price needs.
"""
from __future__ import annotations

import argparse
import datetime as dt
import math
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import movers  # noqa: E402
import portfolio as pfm  # noqa: E402
import sec  # noqa: E402

ROOT = pfm.ROOT
MAJOR = set(movers.EXCHANGES)


def fmt_money(x) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "-"
    a = abs(x)
    if a >= 1e12:
        return f"${x / 1e12:,.2f}T"
    if a >= 1e9:
        return f"${x / 1e9:,.2f}B"
    if a >= 1e6:
        return f"${x / 1e6:,.1f}M"
    return f"${x:,.2f}"


def pct(x, digits=1) -> str:
    return "-" if x is None else f"{x * 100:+.{digits}f}%"


def num(x, digits=1, suffix="") -> str:
    return "-" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:,.{digits}f}{suffix}"


def peers_for(info: dict, sym: str, n: int = 8) -> list[str]:
    """Same-industry US listings nearest in market cap (0.1x-10x), largest first."""
    import yfinance as yf  # type: ignore
    from yfinance import EquityQuery as Q  # type: ignore
    ind, mc = info.get("industry"), info.get("marketCap") or 0
    if not ind or not mc:
        return []
    q = Q("and", [Q("eq", ["region", "us"]), Q("eq", ["industry", ind]),
                  Q("gte", ["intradaymarketcap", mc / 10]), Q("lte", ["intradaymarketcap", mc * 10]),
                  Q("is-in", ["exchange", *movers.EXCHANGES])])
    try:
        quotes = yf.screen(q, size=60, sortField="intradaymarketcap", sortAsc=False).get("quotes", [])
    except Exception:  # noqa: BLE001
        return []
    cands = [x for x in quotes if x["symbol"] != sym and x.get("quoteType") == "EQUITY" and x.get("marketCap")]
    cands.sort(key=lambda x: abs(math.log(x["marketCap"] / mc)))
    return [x["symbol"] for x in cands[:n]]


def peer_row(sym: str) -> dict | None:
    import yfinance as yf  # type: ignore
    try:
        i = yf.Ticker(sym).get_info()
    except Exception:  # noqa: BLE001
        return None
    return {"symbol": sym, "mcap": i.get("marketCap"), "fpe": i.get("forwardPE"), "tpe": i.get("trailingPE"),
            "ev_ebitda": i.get("enterpriseToEbitda"), "ev_sales": i.get("enterpriseToRevenue"),
            "growth": i.get("revenueGrowth"), "ebitda_m": i.get("ebitdaMargins"), "gross_m": i.get("grossMargins")}


def quartiles(vals: list[float]) -> tuple[float, float, float] | None:
    v = sorted(x for x in vals if x is not None and x > 0 and x < 500)
    if len(v) < 3:
        return None
    q = st.quantiles(v, n=4)
    return q[0], st.median(v), q[2]


def last_big_move(sym: str) -> list[str]:
    """Largest one-day move on >= 2x volume in 60 sessions, and how the session around it traded."""
    import yfinance as yf  # type: ignore
    out = []
    t = yf.Ticker(sym)
    d = t.history(period="3mo", interval="1d")
    if d is None or len(d) < 25:
        return ["(not enough history)"]
    r = d["Close"].pct_change()
    base = d["Volume"].rolling(20).mean().shift(1)
    rv = d["Volume"] / base
    cand = [(i, r.iloc[i]) for i in range(len(d) - 60 if len(d) > 60 else 21, len(d))
            if rv.iloc[i] >= 2 and abs(r.iloc[i]) >= 0.05]
    if not cand:
        return ["No move of 5% or more on 2x volume in the last 60 sessions."]
    i, move = max(cand, key=lambda x: abs(x[1]))
    day = d.index[i]
    prev_close = float(d["Close"].iloc[i - 1])
    out.append(f"Biggest move: {move * 100:+.1f}% on {day.date()} (volume {rv.iloc[i]:.1f}x normal); "
               f"open {d['Open'].iloc[i]:.2f}, range {d['Low'].iloc[i]:.2f}-{d['High'].iloc[i]:.2f}, "
               f"close {d['Close'].iloc[i]:.2f} vs prior close {prev_close:.2f}.")
    since = float(d["Close"].iloc[-1]) / float(d["Close"].iloc[i]) - 1
    after = d["Close"].iloc[i:]
    out.append(f"Since: {since * 100:+.1f}% to {d['Close'].iloc[-1]:.2f}; closing range since "
               f"{after.min():.2f}-{after.max():.2f}.")
    # The evening before and the morning of the move, when Yahoo still has 15-minute bars (about 60 days).
    if (dt.datetime.now(dt.timezone.utc) - day.to_pydatetime().astimezone(dt.timezone.utc)).days < 55:
        try:
            m = t.history(start=(day - dt.timedelta(days=4)).date().isoformat(),
                          end=(day + dt.timedelta(days=1)).date().isoformat(), interval="15m", prepost=True)
            m.index = m.index.tz_convert("America/New_York")
            prev_day = d.index[i - 1].date()
            eve = m[(m.index.date == prev_day) & (m.index.hour >= 16)]
            pre = m[(m.index.date == day.date()) & ((m.index.hour < 9) | ((m.index.hour == 9) & (m.index.minute < 30)))]
            ext = [x for x in (eve, pre) if len(x)]
            # Base on the intraday series' own prior regular close: Yahoo's intraday bars are not split-adjusted
            # the way daily bars are, so mixing the two after a reverse split gives nonsense percentages.
            reg_prev = m[(m.index.date == prev_day) & (m.index.hour < 16) & (m.index.hour >= 9)]
            base_px = float(reg_prev["Close"].iloc[-1]) if len(reg_prev) else None
            if ext and base_px:
                import pandas as pd  # type: ignore
                e = pd.concat(ext)
                hi, lo = float(e["High"].max()), float(e["Low"].min())
                out.append(f"Extended hours before the open: high {hi:.2f} ({(hi / base_px - 1) * 100:+.1f}%), "
                           f"low {lo:.2f} ({(lo / base_px - 1) * 100:+.1f}%) vs the prior close of {base_px:.2f} "
                           "in the intraday data.")
        except Exception:  # noqa: BLE001
            pass
    return out


def build(sym: str, peers_override: list[str] | None = None) -> str:
    import yfinance as yf  # type: ignore
    t = yf.Ticker(sym)
    i = t.get_info() or {}
    now = pfm.now_utc()
    price = i.get("currentPrice") or i.get("regularMarketPrice")
    L = [f"# {sym}: {i.get('longName') or i.get('shortName') or sym}",
         f"{i.get('sector') or '-'} / {i.get('industry') or '-'} | dossier {pfm.fmt_et(now)}", ""]

    # Snapshot
    hi52, lo52 = i.get("fiftyTwoWeekHigh"), i.get("fiftyTwoWeekLow")
    L += ["## Snapshot",
          f"- Price {num(price, 2)} | market cap {fmt_money(i.get('marketCap'))} | enterprise value "
          f"{fmt_money(i.get('enterpriseValue'))} | shares {num((i.get('sharesOutstanding') or 0) / 1e6, 1, 'M')}",
          f"- 52-week {num(lo52, 2)}-{num(hi52, 2)} ({pct(price / hi52 - 1 if price and hi52 else None)} from the high) | "
          f"short interest {pct(i.get('shortPercentOfFloat'))} of float | beta {num(i.get('beta'), 2)} | "
          f"{fmt_money((i.get('averageVolume') or 0) * (price or 0))} traded a day"]
    try:
        closes, _ = movers.history([sym], period="1y")
        c = closes[sym].dropna()
        prof = movers.risk_profile(c, len(c) - 1)
        if prof:
            L.append(f"- One-year volatility {prof['vol_1y']:.0f}% annualized; {prof['spike_days_1y']} days of "
                     f"+/-15%{' (NOISY by the scanner rule)' if prof['noisy'] else ''}")
    except Exception:  # noqa: BLE001
        pass
    iss = movers.issuance(sym)
    if iss:
        L.append(f"- Share count {pct((iss.get('shares_change_1y_pct') or 0) / 100)} over a year"
                 + (f"; reverse split {iss['reverse_split']}" if iss.get("reverse_split") else ""))
    L.append("")

    # The move
    L += ["## Last big move and how it traded"] + [f"- {x}" for x in last_big_move(sym)] + [""]

    # Filings
    L.append("## SEC filings, last 90 days")
    try:
        fl = sec.filings(sym, dt.date.today() - dt.timedelta(days=90))
    except Exception as e:  # noqa: BLE001
        fl, L = [], L + [f"- (EDGAR unavailable: {str(e)[:80]})"]
    shown = 0
    for f in fl:
        if f["form"] in ("4", "3", "144") or (f["form"].startswith("SC 13G") or f["form"].startswith("SCHEDULE 13G")):
            continue
        L.append(f"- {f['date']} {f['form']}: {'; '.join(f['events']) or f.get('desc') or ''} ({f['url']})")
        shown += 1
        if shown >= 14:
            break
    if not fl:
        L.append("- none found (foreign filer, or EDGAR not configured)")
    try:
        it = t.insider_transactions
        if it is not None and len(it):
            cut = now.replace(tzinfo=None) - dt.timedelta(days=180)
            recent = it[it["Start Date"] >= cut] if "Start Date" in it else it
            txt = recent["Text"].fillna("").str.lower() if "Text" in recent else None
            if txt is not None:
                buys = recent[txt.str.contains("purchase|buy")]
                sells = recent[txt.str.contains("sale")]
                L.append(f"- Insiders, 6 months: {len(buys)} open-market buys ({fmt_money(buys['Value'].sum())}), "
                         f"{len(sells)} sales ({fmt_money(sells['Value'].sum())})")
    except Exception:  # noqa: BLE001
        pass
    L.append("")

    # Fundamentals
    fcf = None
    try:
        cf = t.quarterly_cashflow
        if cf is not None and "Free Cash Flow" in cf.index:
            fcf = float(cf.loc["Free Cash Flow"].iloc[:4].sum())
    except Exception:  # noqa: BLE001
        pass
    ebitda, debt, cash = i.get("ebitda"), i.get("totalDebt") or 0, i.get("totalCash") or 0
    L += ["## Fundamentals (trailing twelve months)",
          f"- Revenue {fmt_money(i.get('totalRevenue'))} ({pct(i.get('revenueGrowth'))} year on year, last quarter) | "
          f"gross margin {pct(i.get('grossMargins'))} | EBITDA margin {pct(i.get('ebitdaMargins'))} | "
          f"profit margin {pct(i.get('profitMargins'))}",
          f"- EBITDA {fmt_money(ebitda)} | free cash flow {fmt_money(fcf)} (last 4 quarters) | cash {fmt_money(cash)} | "
          f"debt {fmt_money(debt)} | net debt/EBITDA {num((debt - cash) / ebitda if ebitda and ebitda > 0 else None, 1, 'x')}",
          f"- EPS trailing {num(i.get('trailingEps'), 2)} | forward (consensus) {num(i.get('forwardEps'), 2)}", ""]

    # Valuation vs peers
    peers = peers_override or peers_for(i, sym)
    rows = [r for r in (peer_row(p) for p in peers) if r]
    me = {"symbol": sym, "mcap": i.get("marketCap"), "fpe": i.get("forwardPE"), "tpe": i.get("trailingPE"),
          "ev_ebitda": i.get("enterpriseToEbitda"), "ev_sales": i.get("enterpriseToRevenue"),
          "growth": i.get("revenueGrowth"), "ebitda_m": i.get("ebitdaMargins"), "gross_m": i.get("grossMargins")}
    rows = [r for r in rows if r["mcap"]]  # drop tickers Yahoo could not quote
    L += ["## Valuation against peers",
          "| | market cap | fwd P/E | trailing P/E | EV/EBITDA | EV/sales | revenue growth | EBITDA margin |",
          "|---|---|---|---|---|---|---|---|"]
    for r in [me] + rows:
        L.append(f"| {'**' + r['symbol'] + '**' if r is me else r['symbol']} | {fmt_money(r['mcap'])} | {num(r['fpe'])} | "
                 f"{num(r['tpe'])} | {num(r['ev_ebitda'])} | {num(r['ev_sales'])} | {pct(r['growth'])} | {pct(r['ebitda_m'])} |")
    qpe = quartiles([r["fpe"] for r in rows])
    qeb = quartiles([r["ev_ebitda"] for r in rows])
    qsa = quartiles([r["ev_sales"] for r in rows])
    # Market cap / price counts every share class; Yahoo's sharesOutstanding can miss one (Vicor's Class B).
    px_now = i.get("currentPrice") or i.get("regularMarketPrice") or i.get("previousClose")
    shares = (i["marketCap"] / px_now) if i.get("marketCap") and px_now else (i.get("sharesOutstanding") or 0)
    net_debt = debt - cash
    fwd_eps = i.get("forwardEps")
    L.append("")
    L.append("Fair-value arithmetic (peer multiples applied to this company; 25th / median / 75th percentile):")
    if qpe and fwd_eps and fwd_eps > 0:
        L.append(f"- Forward EPS {fwd_eps:.2f} x peer forward P/E {qpe[0]:.1f} / {qpe[1]:.1f} / {qpe[2]:.1f} = "
                 f"{fwd_eps * qpe[0]:,.2f} / {fwd_eps * qpe[1]:,.2f} / {fwd_eps * qpe[2]:,.2f}")
    if qeb and ebitda and ebitda > 0 and shares:
        v = [(ebitda * m - net_debt) / shares for m in qeb]
        L.append(f"- Trailing EBITDA x peer EV/EBITDA {qeb[0]:.1f} / {qeb[1]:.1f} / {qeb[2]:.1f}, less net debt = "
                 f"{v[0]:,.2f} / {v[1]:,.2f} / {v[2]:,.2f}")
    if qsa and i.get("totalRevenue") and shares:
        v = [(i["totalRevenue"] * m - net_debt) / shares for m in qsa]
        L.append(f"- Trailing revenue x peer EV/sales {qsa[0]:.1f} / {qsa[1]:.1f} / {qsa[2]:.1f}, less net debt = "
                 f"{v[0]:,.2f} / {v[1]:,.2f} / {v[2]:,.2f}")
    if qpe and i.get("forwardPE"):
        L.append(f"- Priced at {i['forwardPE']:.1f}x forward earnings vs a peer median of {qpe[1]:.1f}x "
                 f"({(i['forwardPE'] / qpe[1] - 1) * 100:+.0f}%). Check that the forward EPS is clean of one-offs "
                 "before trusting any of these.")
    if not (qpe or qeb or qsa):
        L.append("- (too few peers with usable multiples; pass --peers)")
    L += ["", "## Analysts and calendar",
          f"- Targets: mean {num(i.get('targetMeanPrice'), 2)}, median {num(i.get('targetMedianPrice'), 2)}, "
          f"range {num(i.get('targetLowPrice'), 2)}-{num(i.get('targetHighPrice'), 2)} "
          f"({i.get('numberOfAnalystOpinions') or 0} analysts, {i.get('recommendationKey') or '-'})"]
    try:
        cal = t.calendar or {}
        ed = cal.get("Earnings Date")
        if ed:
            L.append(f"- Next earnings {', '.join(str(x) for x in ed)}: consensus EPS {num(cal.get('Earnings Average'), 2)} "
                     f"(range {num(cal.get('Earnings Low'), 2)}-{num(cal.get('Earnings High'), 2)}), revenue "
                     f"{fmt_money(cal.get('Revenue Average'))}")
    except Exception:  # noqa: BLE001
        pass
    L += ["", "## Deep dive (from the release, the 8-K exhibit, the call; cite sources)",
          "- What changed, in numbers, and how big relative to the company:",
          "- Firm vs contingent (orders, backlog, guidance ranges):",
          "- One-offs flattering or hurting the numbers:",
          "- Dilution and financing (shelf, offerings, warrants, converts):",
          "- Competition, customers, regulation:",
          "- What the current price assumes (implied multiple vs peers):",
          "- What decides the stock, and the next checkpoint:",
          "- Verdict for this challenge (ends Wed Nov 4 close): trade or not, trigger, stop, size:"]
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--peers", default="", help="comma-separated peer tickers (default: same industry, nearest size)")
    ap.add_argument("--save", action="store_true")
    a = ap.parse_args()
    sym = a.ticker.upper()
    text = build(sym, [p.strip().upper() for p in a.peers.split(",") if p.strip()] or None)
    print(text)
    if a.save:
        d = ROOT / "research" / "dossiers"
        d.mkdir(parents=True, exist_ok=True)
        f = d / f"{sym}-{pfm.et_date(pfm.now_utc()).isoformat()}.md"
        f.write_text(text)
        print(f"saved {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
