# Routine runbook

Every scheduled run (and any manual check) follows these steps for BOTH books. Times are US Eastern.

Books:
* `h1b`: the original H-1B challenge (US stocks and ETFs, cash account). Ledger `ledger/`, config `config/`.
* `free`: the Unrestricted book (stocks, ETFs, options, spot crypto; no visa limits; cash account, no margin
  at $1,000). Ledger, journal, config and watchlist in `books/free/`. Opened Tue Sep 29, 5:45 PM ET.
Both end at the Mon Oct 5, 4:00 PM ET close with the same $2,000 target.

Dashboards (one page shows both books: a two-card scoreboard, a shared race chart, per-book details):
* Public: https://h1b-1k-challenge.vercel.app. Data: `data/snapshot.json` and `data/snapshot_free.json` on the
  `market-data` branch, rebuilt by the market-data workflow on every dispatch and on every push to `main` that
  touches `ledger/`, `books/`, `config/` or `scripts/`.
* Private: https://claude.ai/artifact/28rMDx9DZwFEfXBjxWKkcJ (db collections `snapshots` for h1b and
  `snapshots_free` for free; one doc per update, doc id = UTC timestamp, the page shows the newest of each).

Page changes: edit `dashboard/index.html`, run `python3 scripts/build_site.py`, commit and push
(Vercel serves the new `site/index.html` within ~10 min), and republish the artifact from the same path.

## 1. Refresh data

```bash
cd /home/user/Investment_Challenge && git pull -q --rebase origin main
python3 scripts/sync.py --local --mode quotes          # direct fetch (~20 s): quotes, crypto, option chains
python3 scripts/sync.py --local --mode news            # adds headlines, discovery, alerts (use at least hourly)
python3 scripts/review.py                              # h1b: portfolio, alerts, focus, news
python3 scripts/review.py --book free --brief          # free: portfolio and positions
```
`--tickers A,B,NKE261002C00036000` adds symbols (an option contract pulls its underlying's chain).
Also dispatch the market-data workflow (GitHub MCP `actions_run_trigger`, workflow `market-data.yml`,
ref `main`) at each :40 run so the public dashboard's equity history stays fresh; no need to wait for it.
If the direct fetch fails, fall back to the dispatch plus `python3 scripts/sync.py --wait 200`.
Option chains: `.cache/options.json` (nearest two expiries for `books/free/watchlist.json` `options_watch`).

## 2. Decide

* Read `ALERTS` first: new headlines since the last news run, movers (>=6% on the day or >=4% extended-hours)
  and discovery (trending, top gainers, most actives). This is the news-trading feed for both books.
* Exit rules (both books): stop -15% (2x ETFs) / -12% (stocks) from entry, trim a third at +25% and move the
  stop to breakeven, never average down. In extended hours, judge stops on news, not a thin print.
  Options (free book): size so a total loss is acceptable; take profits in thirds at +50%, +100% and on the
  catalyst; close before expiry unless deep in the money; never hold a contract through its expiration close.
  Crypto (free book): stop -8% from entry unless the journal plan says otherwise.
* Entries per the latest `plan` entry in each book's journal, plus news trades: act on material, fresh news
  with confirmed volume; don't chase a spike that has already faded.
* Hard rules enforced by `scripts/trade.py`: stocks 4:00 AM-8:00 PM ET (extended hours need a live print);
  options in the regular session at the ask (buy) / bid (sell); crypto 24/7; fresh quotes; cash only; no sale
  of stock or options bought with unsettled proceeds before settlement (T+1). The h1b book cannot trade
  options or crypto.

## 3. Execute and log

```bash
python3 scripts/trade.py buy IONX --usd 300 --why "..." --tags momentum --stop 24.1 --target 36        # h1b
python3 scripts/trade.py --book free buy NKE261002C00038000 --qty 3 --why "..." --tags earnings           # 3 contracts
python3 scripts/trade.py --book free buy BTC-USD --usd 200 --why "..." --stop 76000
python3 scripts/trade.py --book free sell NKE261002C00038000 --all --why "..."
python3 scripts/journal.py [--book free] --kind trade --title "..." --body "..." --tickers NKE
git add -A && git commit -m "..." && git push -q origin main
```
Every order gets a journal entry in its own book. Also journal decisions not to trade when they matter.

## 4. Publish

```bash
python3 scripts/snapshot.py && python3 scripts/snapshot.py --book free
```
Then one `ArtifactData batch` with two `set` writes: collection `snapshots`, doc id printed by the first
command, `file_path: /home/user/Investment_Challenge/.cache/snapshot.json`; and collection `snapshots_free`,
doc id printed by the second, `file_path: /home/user/Investment_Challenge/.cache/snapshot_free.json`.
Update each book's watchlist `strategy` (the dashboard's game-plan line) and `focus` when the plan changes.

## Schedule

* Weekdays: :10 runs 7:10 AM-7:10 PM, :40 runs 8:40 AM-7:40 PM, :25 and :55 runs 9:25 AM-3:55 PM,
  16:20 post-close review, plus one-shot checks at scheduled catalysts (earnings, jobs report).
* Crypto watch (free book): weeknights 11:10 PM and weekends every 4 hours.
* Sunday 7:00 PM review for Monday.
* Final day Mon Oct 5: liquidate everything in both books at the 15:40 run; the 16:20 run writes the final
  report for both books, then deletes the routines.

Routine ids (for `delete_trigger` after the final report): see `config/schedule.json` `routine_ids`.
