# Routine runbook

Every scheduled run (and any manual check) follows these steps. Times are US Eastern.

Dashboard: https://claude.ai/artifact/28rMDx9DZwFEfXBjxWKkcJ (db collection `snapshots`, one new
doc per update, doc id = UTC timestamp, page shows the newest).

## 1. Refresh data

```bash
cd /home/user/Investment_Challenge && git pull -q --rebase origin main
```
Dispatch a fresh data run (GitHub MCP `actions_run_trigger`, workflow `market-data.yml`, ref `main`,
inputs `{"mode": "quotes" | "news" | "scan", "tickers": "<held + candidates>"}`), then:
```bash
python3 scripts/sync.py --wait 200     # waits for the new commit on market-data, copies data/ to .cache/
python3 scripts/review.py              # portfolio, stop/target alerts, focus movers, fresh headlines
```
Use `mode=news` at least once an hour during the session and `mode=scan` pre-market.

## 2. Decide

* Exit rules first: stop -15% (2x ETFs) / -12% (stocks) from entry, trim a third at +25% and move the
  stop to breakeven, never average down.
* Then entries per the latest `plan` entry in `ledger/journal.json`.
* Guardrails are enforced by `scripts/trade.py`: regular session only, fresh quote (<15 min),
  cash only, 60% max position at entry, 6 orders/day, 30 total, 3 day trades per 5 days,
  no sale of shares bought with unsettled proceeds before settlement (T+1).

## 3. Execute and log

```bash
python3 scripts/trade.py buy IONX --usd 300 --why "..." --tags momentum --stop 24.1 --target 36
python3 scripts/trade.py sell IONX --all --why "..."
python3 scripts/journal.py --kind trade --title "..." --body "..." --tickers IONX
git add -A && git commit -m "..." && git push -q origin main
```
Every order gets a journal entry explaining it. Also journal decisions not to trade when they matter.

## 4. Publish

```bash
python3 scripts/snapshot.py            # writes .cache/snapshot.json, prints doc_id
```
Then `ArtifactData set` with `collection: snapshots`, `doc_id: <printed id>`,
`file_path: /home/user/Investment_Challenge/.cache/snapshot.json`.
Update `config/watchlist.json` `strategy` (the dashboard's game-plan line) and `focus` when the plan changes.

## Schedule

* Weekdays 8:40 (pre-market plan), 9:40-15:40 every 30 minutes, 16:20 (post-close review).
* Sunday 7:00 PM review for Monday.
* Final day Mon Oct 5: liquidate everything at the 15:40 run; 16:20 run writes the final report,
  then delete the routines.
