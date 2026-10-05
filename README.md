# Vamsi's Guided Strategy ($1K paper challenge)

One paper portfolio: $1,000 of paper cash opened Sat Oct 3, 2026, goal $2,000 by the Wed Nov 4, 2026 close
(Vamsi extended the original Oct 5 end by 30 days). Every trade follows Vamsi's direction. His current strategy:
high-volatility stocks, bought at tested support and sold at resistance, with a stop under support
(`RUNBOOK.md` section 2a).

The earlier books (an H-1B book in US stocks and ETFs and an Unrestricted book) ran Sep 28 - Oct 2 and were
dropped on Sat Oct 3; their records are in `archive/`.

## How it works

| Piece | Where |
| --- | --- |
| Transaction ledger (source of truth) | `books/guided/transactions.json` |
| Research and decision journal | `books/guided/journal.json` |
| Rules, account model, execution model | `books/guided/challenge.json` |
| Support/resistance radar (levels, stops, sell zones) | `config/radar.json`, built by `scripts/levels.py` |
| Live quotes, equity curve (written every 5 min by GitHub Actions) | `market-data` branch, `data/` |
| Portfolio engine (FIFO lots, T+1 settlement, compliance flags) | `scripts/portfolio.py` |
| Order entry with guardrails | `scripts/trade.py` |
| Routine steps | `RUNBOOK.md` |
| Public dashboard | https://h1b-1k-challenge.vercel.app (Vercel function `vercel/api/index.js` serves `site/index.html` from `main`; the page reads `data/snapshot_guided.json` from the `market-data` branch) |
| Private dashboard | claude.ai artifact, fed from the `snapshots_guided` collection at each routine run |

## Execution model

* Stocks and ETFs fill at the Yahoo Finance last trade plus slippage (5 bps above $20, 20 bps $5-$20,
  50 bps under $5; wider in extended hours). $0 commission; SEC and FINRA TAF fees on sells.
  4:00 AM - 8:00 PM ET; fractional shares allowed.
* Options: regular session only, at the ask to buy and the bid to sell, $0.03 per contract.
* Crypto: 24/7 at the last price plus a 0.30% spread.

## Account guardrails

* Cash account: no margin (below FINRA's $2,000 margin minimum), so no short selling and no naked option writing.
* T+1 settlement: positions bought with unsettled proceeds are never sold before those proceeds settle
  (no good-faith violations).
* No OFAC NS-CMIC restricted securities.
* Paper trading with simulated money; not investment advice.
