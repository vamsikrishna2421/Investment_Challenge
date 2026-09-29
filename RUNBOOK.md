# Routine runbook

Every scheduled run (and any manual check) follows these steps. Times are US Eastern.

Dashboards:
* Public: https://h1b-1k-challenge.vercel.app (Vercel project `h1b-1k-challenge`). Its data is
  `data/snapshot.json` on the `market-data` branch, rebuilt by the market-data workflow every 5 min
  during market hours and on every push to `main` that touches `ledger/`, `config/` or `scripts/`.
* Private: https://claude.ai/artifact/28rMDx9DZwFEfXBjxWKkcJ (db collection `snapshots`, one new
  doc per update, doc id = UTC timestamp, page shows the newest).

Page changes: edit `dashboard/index.html`, run `python3 scripts/build_site.py`, commit and push
(Vercel serves the new `site/index.html` within ~10 min), and republish the artifact from the same path.
Public check: dispatch `site-check.yml`; screenshots land on the `checks` branch.

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

* Read `ALERTS` in review.py first: new headlines since the last news run, movers (>=6% on the day or
  >=4% extended-hours) and discovery (trending tickers, top gainers, most actives). This is the
  news-trading feed; the Actions job refreshes it every 15 minutes from 6 AM to 8 PM ET.
* Exit rules: stop -15% (2x ETFs) / -12% (stocks) from entry, trim a third at +25% and move the stop
  to breakeven, never average down. In extended hours, judge stops on news, not on a thin print.
* Entries per the latest `plan` entry in `ledger/journal.json`, plus news trades: act on material,
  fresh news with confirmed volume; don't chase a spike that has already faded.
* Hard rules enforced by `scripts/trade.py`: sessions 4:00 AM-8:00 PM ET (pre, regular, after-hours;
  extended-hours orders need a live print), fresh quote (<15 min), cash only, no sale of shares bought
  with unsettled proceeds before settlement (T+1). Order counts are a runaway fuse only (25/day).
  No trade-count or position-size limits otherwise: H-1B restricts employment, not how often you
  trade your own account.

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

* Weekdays: :10 runs 7:10 AM-7:10 PM, :40 runs 8:40 AM-7:40 PM, :25 and :55 runs 9:25 AM-3:55 PM,
  16:20 post-close review, plus one-shot checks at scheduled catalysts (earnings, jobs report).
* Sunday 7:00 PM review for Monday.
* Final day Mon Oct 5: liquidate everything at the 15:40 run; 16:20 run writes the final report,
  then delete the routines.

Routine ids (for `delete_trigger` after the final report): see `config/schedule.json` `routine_ids`.
