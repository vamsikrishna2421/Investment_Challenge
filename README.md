# H1B $1K One-Week Challenge

Paper-trading challenge: $1,000 of paper cash, US-listed stocks and ETFs, one week
(accepted Mon Sep 28, 2026 8:35 PM ET; final mark at the Mon Oct 5, 2026 close).
Goal: double it. Account profile: Indian citizen living in the US on an H-1B visa.

## How it works

| Piece | Where |
| --- | --- |
| Transaction ledger (source of truth) | `ledger/transactions.json` |
| Research and decision journal | `ledger/journal.json` |
| Rules, account model, execution model | `config/challenge.json` |
| Live quotes, equity curve (written every 5 min by GitHub Actions) | `market-data` branch, `data/` |
| Portfolio engine (FIFO lots, T+1 settlement, compliance flags) | `scripts/portfolio.py` |
| Order entry with guardrails | `scripts/trade.py` |
| Public dashboard | https://h1b-1k-challenge.vercel.app (Vercel function `vercel/api/index.js` serves `site/index.html` from `main`; the page reads `data/snapshot.json` from the `market-data` branch, rebuilt every 5 min) |
| Private dashboard | claude.ai artifact, fed from the `snapshots` collection at each routine run |

## Execution model

* Fills at the Yahoo Finance last trade price at execution time, plus slippage
  (5 bps above $20, 20 bps $5-$20, 50 bps under $5). $0 commission; SEC and FINRA TAF fees on sells.
* Regular session only (9:30 AM - 4:00 PM ET). Fractional shares allowed.

## H-1B and cash-account guardrails

* Passive investing in US securities is allowed on H-1B; running a trading business is not.
  Guardrails: at most 3 day trades per rolling 5 days, 6 orders per day, 30 orders total.
* Cash account: no margin (balance is below FINRA's $2,000 margin minimum), no shorting, no options.
* T+1 settlement: shares bought with unsettled proceeds are never sold before those proceeds settle
  (no good-faith violations).
* No OFAC NS-CMIC restricted securities (applies to anyone physically in the US).
* Tax: short-term gains are ordinary income for a US tax resident (Form 8949 / Schedule D);
  wash-sale candidates are flagged.
