# Routine runbook

Every scheduled run (and any manual check) follows these steps. Times are US Eastern.

One book: `guided`, Vamsi's guided strategy, $1,000 opened Sat Oct 3. Stocks, ETFs, listed options and spot
crypto in a cash account (no margin at $1,000, so no short selling or naked option writing). Ledger, journal,
config and watchlist in `books/guided/`; it is the scripts' default book, so no `--book` flag is needed.
It trades only on Vamsi's instructions: he says where to look and how to trade. Journal each instruction (kind
`plan`, his words summarized, with the tickers) before the trade it produces, then the trade itself. Apply the
stops and exits he sets; where he sets none, the section 2 exit rules apply. No trade on my own initiative.
His current instruction is the support/resistance radar (section 2a).
It ends at the Wed Nov 4, 2026, 4:00 PM ET close with a $2,000 target (Vamsi extended the original Mon Oct 5
end by 30 days on Oct 5).
The H-1B and Unrestricted books were dropped on Sat Oct 3 on Vamsi's instruction, before any round 2 trade:
`archive/round1/` (Sep 28 - Oct 2 records) and `archive/round2-dropped/`.

Dashboards (one book: statement, goal track, chart against the S&P 500 and Nasdaq-100, holdings, trade log, radar,
journal, account rules):
* Public: https://h1b-1k-challenge.vercel.app. Data: `data/snapshot_guided.json` on the `market-data` branch,
  rebuilt by the market-data workflow on every dispatch and on every push to `main` that touches `books/`,
  `config/` or `scripts/`.
* Private: https://claude.ai/artifact/28rMDx9DZwFEfXBjxWKkcJ (db collection `snapshots_guided`; one doc per update,
  doc id = UTC timestamp, the page shows the newest).

Page changes: edit `dashboard/index.html`, run `python3 scripts/build_site.py`, commit and push
(Vercel serves the new `site/index.html` within ~10 min), and republish the artifact from the same path.

## 1. Refresh data

```bash
cd /home/user/Investment_Challenge && git pull -q --rebase origin main
python3 scripts/sync.py --local --mode quotes          # direct fetch (~20 s): quotes, crypto, option chains
python3 scripts/sync.py --local --mode news            # adds headlines, discovery, alerts (use at least hourly)
python3 scripts/review.py                              # portfolio, alerts, focus, news
python3 scripts/levels.py check                        # radar triggers (section 2a)
python3 scripts/wires.py                               # live catalyst feed (see 1c)
```
`--tickers A,B,NKE261002C00036000` adds symbols (an option contract pulls its underlying's chain).
Also dispatch the market-data workflow (GitHub MCP `actions_run_trigger`, workflow `market-data.yml`,
ref `main`) at each :40 run so the public dashboard's equity history stays fresh; no need to wait for it.
If the direct fetch fails, fall back to the dispatch plus `python3 scripts/sync.py --wait 200`.
Option chains: `.cache/options.json` (nearest two expiries for `books/guided/watchlist.json` `options_watch`).

## 1b. Big-mover catalyst scan (post-close daily, and the 8:40 run)

Round 2: research only. The scan finds new high-volatility candidates for the radar (add them to
`CANDIDATES` in `scripts/levels.py`); it no longer produces entries or day-two triggers.

```bash
python3 scripts/movers.py --min-move 15 --save          # today's big gainers, why they moved
python3 scripts/movers.py --min-move 15 --losers --save # big losers (puts / inverse ideas)
python3 scripts/movers.py --follow-up                   # how earlier scans' names did since
python3 scripts/sec.py TICKER --days 30                 # a company's filings, 8-K items decoded
```
Filters: NYSE/Nasdaq/NYSE American only (no OTC), market cap >= $30M, >= $1M traded on the day, no share-price
floor. Each name gets its one-year risk profile: annualized volatility, the number of +/-15% days, and the
jump in standard deviations of its own history (a 15% day is news for a stock that moves 2% a day, routine
for one that moves 8%). Noisy stocks (volatility >= 120% or >= 10 such days in the year) are skipped unless
`--include-noisy`: on 241 jumps in Aug-Sep 2026 they fell a median 16% vs SPY in the next 10 sessions, the
rest 4%. Market cap under $100M scores -3 (median -13% over 10 sessions). Also scored: share count growth
over the year (serial issuers), reverse splits in 18 months, price under $1 (exchange deficiency, usually
cured by a reverse split), and SEC filings around the
jump (8-K items: 1.01 material agreement, 2.02 results, 2.03 new debt, 3.02 unregistered share sale,
3.01 delisting notice, 4.02 unreliable financials; S-1/S-3/424B offerings; new 13D stakes).
SEC access needs `.secrets/sec_contact` (git-ignored, one line: the user's account email, which they approved
on Sep 29 for SEC requests only; it is sent to sec.gov and nowhere else). If a rebuilt container lost it,
recreate it from the account email.
Deep-dive the top 1-3 by score: read the release (what changed, how big relative to the company:
guidance change %, order value / revenue, debt removed / market cap), check dilution risk (shelf, offering
after the spike), valuation (EV/sales vs growth, analyst targets), and write verdicts to the journal.
Buy candidates need material news, a market cap of at least $100M, relative volume above 2, no takeover cap,
and day-two confirmation (holds above the prior close through the first 30-60 minutes). Skip no-news spikes,
de-SPACs and financings. A reported approach or takeover talks (tag `takeover-interest`, not capped) counts as
material news only once a primary source confirms it: an 8-K, a company statement or the bidder's statement. Check
the date of any search result before citing it; old takeover stories resurface in search.

To catch jumps from the last month that have not run yet (the "signal shown, rally not started" names):
```bash
python3 scripts/movers.py --lookback 30 --min-move 15 --save   # ~10 min: every >=15% day on >=2x volume in 30 sessions
                                                               # (same filters; noisy stocks counted but not researched)
```
It groups them by what the price did since: `holding` (kept the jump, has not run: the main list),
`extending` (drift under way), `fading`, `round-trip` (gave it all back: the market rejected it).
Run it on Sundays and whenever the daily scan is thin; deep-dive the top `holding` names like 1b.
`python3 scripts/jump_study.py --save` re-tests the idea on the same data (returns vs SPY 5 and 10 sessions
after each jump, by volatility, jump size, price, market cap, catalyst, and entry timing). On the Sep 29 run
no entry rule beat the market: the scan supplies research, not automatic entries.

## 1c. Live catalyst feed (every run)

`python3 scripts/wires.py [--hours 6]` pulls the newest company press releases from every wire (Stock Titan's
100-item feed plus PR Newswire), SEC EDGAR's live filings (8-Ks by item, 424B offerings, new 13D stakes),
Nasdaq trading halts and FDA press releases. Each release is tagged by type and
shown with market cap, the dollar figure in the headline as a share of market cap, and the price reaction
(regular and extended hours, relative volume). Order of reading: HOLDINGS / WATCHLIST (anything about what we own,
especially offerings), HALTS (T1 = news pending), SEC EVENTS, SEC WARNINGS (never buy a name in this list that
day), then CATALYSTS. NEW marks items first seen in this run.
For a real candidate, open the release: a raised guide, an order or contract worth >=10% of annual revenue, a
refinancing that removes a near-term maturity, an approval. Then apply the entry rules in 1b.

## 1d. Deep dive on every shortlisted stock (before any new position)

```bash
python3 scripts/dossier.py TICKER --save              # numbers: move, filings, insiders, peers, fair-value range
python3 scripts/dossier.py TICKER --peers A,B,C --save  # when the automatic industry peers are the wrong comparison
python3 scripts/sec.py TICKER --exhibit [--n 1]       # the press release behind the latest 8-K (primary source)
```
Then write the deep dive under the numbers in `research/dossiers/TICKER-<date>.md`, citing sources:
what changed and how big relative to the company; firm vs contingent (orders, backlog, guide ranges); one-offs that
flatter or hurt the numbers; dilution and financing; competition, customers, regulation; what the current price
assumes (implied multiple vs the right peers; for cyclicals, peak vs mid-cycle earnings); what decides the stock and
the next checkpoint; and the verdict for this challenge (trade or not, trigger, stop, size). For an earnings trade,
also compare the options' implied move (at-the-money straddle / spot) with the stock's past earnings reactions.
Journal a short summary. No new position without a written verdict (exits and stops don't wait).
The fair-value range is arithmetic on other companies' multiples, not a forecast; check the peer set and the
earnings base before quoting it.

## 1e. Social attention

`python3 scripts/social.py [--save]` lists Stocktwits' trending US stocks with size and whether a filing or wire
release sits behind the buzz; `python3 scripts/social.py IOVA MU` shows message rate and bull/bear tags. Use it
as a crowding gauge: most stock-picking accounts have negative skill on average (Kakhbod et al. 2023: 56% of
29,000 Stocktwits finfluencers at -2.3% a month; fading them earned 1.2% a month). A trending name with no
filing or release behind it is a pump-risk flag, never a buy reason. X accounts in `config/x_accounts.json` are read
only when `.secrets/x_bearer` holds a paid X API token ($0.005 per post read): `python3 scripts/social.py --x`.

## 1f. Robinhood connector (read-only)

The user connected Robinhood for information only: no real trading. Use its read tools (quotes, option chains and
quotes with Greeks, fundamentals, financials, earnings calendar and results, analyst ratings, historicals, scanner
previews, SEC filings) to cross-check prices and paper fills. Never call order, cancel, exercise, watchlist, alert or
scan-editing tools; they are denied in `.claude/settings.json`. Never read or publish the user's own account data
(accounts, positions, orders, P&L) unless the user asks, and never put it in the repo or on the dashboards: both are
public.
Uses that change decisions:
- Before any option paper trade: `get_option_instruments` (chain_symbol, expiration_dates, type) then `get_option_quotes`
  for the contract. Check bid/ask and sizes, IV, delta, theta, break-even and Robinhood's chance of profit. If
  Robinhood's ask is more than 5% above the ask in `.cache/options.json`, re-sync before trading, or skip.
- Overnight prices (Robinhood's 24-hour market, `last_non_reg_trade_price`) at the 7:10 and 8:40 runs to size the gap
  on holdings before the pre-market opens.
- Expiring options: Robinhood force-closes at 3:30 PM ET on expiration day (`sellout_datetime`), so the book sells any
  contract expiring that day by the 3:25 PM run at the latest.

## 1g. Prediction markets (read-only)

The Robinhood connector has no prediction-market tools yet, so its event contracts can't be seen or traded
through it. Kalshi's public API is readable without an account: `python3 scripts/kalshi.py [SERIES ...] [--save]`
prints each "above X" ladder with the market's probability per rung and the implied median (payrolls KXPAYROLLS,
unemployment KXU3, CPI KXCPI / KXCPIYOY, Fed KXFED). Use the implied median as the surprise benchmark for scheduled
releases: surprise = actual - median, snapshot before the market closes (--save logs to research/kalshi/). The book
does not trade prediction markets.
Forecast record (`scripts/forecasts.py`): for each scheduled release, write my own probability from the inputs
(claims, ADP, trend) before reading the market ladder, then log both with `add`; `resolve` after the release;
`score` compares Brier scores. Nothing is traded on these forecasts unless mine beat the market's over 30+
questions by more than costs.

## 2. Decide

* Read `ALERTS` first: new headlines since the last news run, movers (>=6% on the day or >=4% extended-hours)
  and discovery (trending, top gainers, most actives). Read it for news on holdings and radar names.
* Exit rules where Vamsi sets none: stop -15% (2x ETFs) / -12% (stocks) from entry, trim a third at +25% and move the
  stop to breakeven, never average down. In extended hours, judge stops on news, not a thin print. In the regular session a stop is a
  price level: once the stock trades at or below it, it is hit even if it bounces before the next run (review.py
  flags `STOP TRADED` from the day low); sell at that run.
  Options: size so a total loss is acceptable; take profits in thirds at +50%, +100% and on the
  catalyst; close before expiry unless deep in the money; never hold a contract through its expiration close.
  Crypto: stop -8% from entry unless the journal plan says otherwise.
* Entries only per Vamsi's latest instruction (`plan` entries in the journal); today that is section 2a.
* Hard rules enforced by `scripts/trade.py`: stocks 4:00 AM-8:00 PM ET (extended hours need a live print);
  options in the regular session at the ask (buy) / bid (sell); crypto 24/7; fresh quotes; cash only; no sale
  of stock or options bought with unsettled proceeds before settlement (T+1).

## 2a. Vamsi's strategy: support/resistance radar (Sat Oct 3)

Vamsi's rules: trade high-volatility stocks; buy at support, sell at resistance, stop under support. Keep at
least 20 names on the radar with support, resistance and stop levels ready; a name reaching its support is the
trigger. His names GPUS, IREN and BTDR stay on the radar even when they miss a filter (the page flags them).

```bash
python3 scripts/levels.py check            # every run after the sync: BUY ZONE, BOUNCE, NEAR, TARGET, BROKEN
python3 scripts/levels.py build --save     # 16:20 post-close and the Sunday review: rebuild the radar, commit it
```
* Radar: `config/radar.json` (one copy per day in `research/radar/`), from one year of daily bars. Filters: ATR at
  least 4% of the price, 20-day dollar volume at least $15M, a support tested at least twice, R:R at least 1.5.
  Method in the `scripts/levels.py` docstring; candidates in its `CANDIDATES` list. The dashboard shows the radar
  with each name's live status.
* Entry, at a regular-session run from 9:55 AM: a name whose status is BUY ZONE (inside the buy zone, above the
  stop) or BOUNCE (touched the zone this session and held, entry R:R at least 1.5); crypto-linked names only while
  the bitcoin gate is open (2c). Never on BROKEN (at or
  through the stop this session), on a day with an offering or material negative company news, or after 14:55
  on the final day (Wed Nov 4). Material means the company's own news that changes the business: an offering or
  other dilution, a guidance cut, a failed trial or rejection, a regulatory or legal hit, a delisting notice,
  an auditor or accounting problem. Sector-wide moves, analyst notes and recap headlines do not cancel an entry:
  a stock that falls too far on minor news is the dip Vamsi wants to buy (Oct 5). Buy only with settled cash, every day: a stock bought with unsettled proceeds can't be
  sold before T+1, which would block its stop (and the 15:40 liquidation on the final day).
* Size: at most 4 radar positions, each 25% of equity (about $250), cut so that its stop loses at most 1.5% of
  equity: `levels.py check` and `orders.py plan` print the size (a stop 10% under the entry gets 15%; from Oct 6,
  2d). Less when settled cash is short. At
  most 2 of them crypto-linked (`CRYPTO_LINKED` in `scripts/levels.py`: 13 of the first radar's 25 names move
  with bitcoin or ether, so four of them would be one bet; `check` tags them `[crypto]`). When more
  names trigger than slots or cash, take the deepest dip first: the price's distance below the prior close in
  ATR units, as `levels.py check` prints and sorts it (Vamsi, Oct 5: buy the stocks that dipped most on the day,
  for the recovery); equal dips go to the higher entry R:R. One position per name, no averaging down, no
  re-entry in a name stopped out the same day.
* Order: `trade.py buy TICKER --usd 250 --stop <radar stop> --target <sell-zone bottom> --tags radar
  --why "..."`, with the buy zone, stop, sell zone and entry R:R in the reason.
* Exit: sell at the first run where the price is in the sell zone (TARGET HIT), at the plan stop (a resting stop
  order since Oct 6: `orders.py fill` sells at the minute it trades, section 2c), or at the 15:40 liquidation on
  the final day (Wed Nov 4, after cancelling open orders); positions are held overnight until one of those. These replace the section 2
  stock stop and trim for radar trades.
* Every radar name is US-listed common stock; `trade.py` still blocks OFAC NS-CMIC names (`config/blocklist.json`).
* Backtest (`python3 scripts/sr_backtest.py --save`; `research/backtests/sr-2026-10-03.md`): over 5 years on the 61
  candidates, buying the touch averaged +0.02R a trade (random entries with the same stop and target: +0.01R) and
  -0.34% a trade when sold the same day; candle, trend and volume filters added nothing measurable, and results
  followed the market year by year. The radar sets where the stop and target sit; it is not a forecast. Any new
  level rule gets the same test (beat random entries with the same stop and target, after costs) before it trades.

* Opening-dip test (`python3 scripts/dip_backtest.py --save`, `research/backtests/dip-2026-10-06.md`; 66 candidates,
  returns after costs, sell at the prior close if reached, else the close): buying at the open after a gap down of
  0.5+ ATR averaged +0.5 to +1.1% a trade over 4 years (57% winners) against -0.3% for all open entries. Buying the
  dip later did not pay: down 0.5+ ATR at 10:30 averaged -0.1 to +0.2% over 2 years, and at 9:55 about 0% over the
  last 60 sessions (+0.8% +/- 1.25 inside the buy zone, 90 trades). Deep dips rarely got back to the prior close the
  same day (4-21%). The edge, where there is one, sits at the open.
* Trade review: when a position closes, journal a `review` entry: the entry's context (dip against the prior
  close in ATR, gap, sector, news), the best and worst price while held, the exit, and whether a rule should
  change. One trade changes nothing; a rule changes when the reviews and a backtest agree.

## 2b. Clue scan (Vamsi, Mon Oct 5)

Vamsi's instruction: when a watched name moves a lot, check whether it showed clues before the move and why the
routines missed them, then watch for those clues ahead of the next move.

```bash
python3 scripts/clues.py scan --save                  # 8:40 run: bounce setups, breakout watches, pre-market moves
python3 scripts/clues.py movers                       # any run: radar and candidate names moving 1+ ATR today
python3 scripts/clues.py postmortem --save --journal  # 16:20 run: today's big movers, their clues, why missed
```
* Clues and scoring are in the `scripts/clues.py` docstring: SUP, COIL, ACC, HL, RES and GAP, from bars through the
  last completed session; bounce score = SUP + COIL + ACC + HL. The universe is the radar plus its candidates.
* The 8:40 day plan lists the scan's bounce setups (score 3+) and breakout watches; every status line names any
  1+ ATR mover with its clues and why it was missed; the 16:20 post-mortem goes to the journal.
* Clues are alerts, not trade rules. Radar entries (2a) stay as they are until a clue beats random entries in the
  5-year backtest (`research/backtests/clues-*.md`). A breakout watch is never a radar buy; it goes to Vamsi.
* First test (`python3 scripts/clue_backtest.py --save`, `research/backtests/clues-2026-10-05.md`; 66 candidates,
  5 years, 37,553 name-days): no clue or score raised the odds of a 1+ ATR up-move the next session (base 8.1%;
  score 3+ 7.9%, SUP+HL 8.1%, breakout watch 6.3%). ACC raised moves both ways (up 10.6%, down 7.2% vs 5.4%),
  COIL lowered them (5.8% / 3.2%), SUP cut big drops (4.0%). Buying the next open and selling the close lost
  0.1-0.4% after costs in every group. So the scan describes setups; it does not forecast them.
* Screen fix from the first post-mortem (Oct 5): a tested zone within 0.1 ATR of the price counts as support when
  two of its swings are lows (`levels.py`); the strict "below the price" test had hidden GRAB's support at 3.075
  (lows of 3.07 twice). A zone at the price built from highs (INTR, STNE after Oct 5's spikes) stays resistance.
* Open positions keep the stop and target recorded at entry; the nightly radar rebuild does not move them.

## 2c. Resting orders (Vamsi, Mon Oct 5)

Vamsi's instruction: put buys at the support price so they fill by themselves when the price gets there, and the
book doesn't miss the dips that happen between runs.

```bash
python3 scripts/orders.py fill                          # every run, right after the sync: limit fills, stops, expiry
python3 scripts/orders.py plan --place [--skip A,B]     # 8:40 run: DAY buy limits for the free slots
python3 scripts/orders.py list                          # open orders; cancel with: orders.py cancel ID --why "..."
```
* Model in the `scripts/orders.py` docstring, limited to what a Robinhood cash account supports. Buy limits are DAY
  orders at support, the bottom of the buy zone (Vamsi, Oct 5), sized as in 2a (25% of equity, at most 1.5% of
  equity lost at the stop) and reserved from settled cash; at most 4 positions plus open orders, at most 2 crypto-linked; radar names within 8% of support
  with R:R 1.5+ measured from support, higher R:R first. A fill needs a 1-minute bar 1 cent through the limit; a
  gap down fills at the open, which can be under the stop.
* Bitcoin gate (Vamsi, Oct 5: no blind dip-buying in crypto-linked names): `plan` prints it; crypto-linked names
  get orders, and market buys at runs, only while bitcoin is above its 20-day average, down less than 2% on the
  day and less than 5% over 3 days.
* Every position's plan stop is a resting stop order: `orders.py fill` sells at the minute the stop trades (at
  the stop, or at a lower open, less slippage). Targets stay a run check (TARGET HIT: sell at the run with
  `trade.py`), because Robinhood holds shares for one sell order at a time.
* `--skip` names with an offering or material company news (2a); cancel an open order when such news appears
  before it fills. `fill` cancels a buy before the open when the pre-market price is at or under its stop.
* Market buys at runs (2a) still apply to names inside their zones when slots and settled cash remain.
* Test (`python3 scripts/limit_backtest.py --save`, `research/backtests/limits-2026-10-06.md`; 2 years of hourly
  bars, 5,832 days with a radar name within 5% of its zone): a limit at the zone top filled 63% of the time, a limit
  at support 42%, a run entry inside the zone 34%; per trade, 3 sessions later: -0.04%, -0.12% and -0.25% (all
  +/- 0.5). Resting orders trade more often, not better. A limit at support fills on deeper dips that often keep
  going: its 0.6-ATR stop was hit within 3 sessions 62% of the time (49% at the zone top); a stop 1.0 or 1.5 ATR
  under support cut that to 39% and 20% (+0.08% and +0.21% a trade, still inside the noise) at more risk a share.

## 2d. Replay practice (Vamsi, Mon Oct 5)

Vamsi's instruction: practice the rules on past sessions as if live, without looking at what happened next;
learn from the bad cases and refine the strategy.

```bash
python3 scripts/replay.py --grid --days 30 --save        # last 30 sessions, 5-minute bars, every rule variant, trade by trade
python3 scripts/replay.py --grid --windows --days 22 --step 22 --bars 1h --save   # 2.8 years, 33 separate 22-session windows
python3 scripts/replay.py --days 700 --bars 1h --analyze # trade returns by entry context, +/- 95%
python3 scripts/replay.py --grid --set stops|times|sizing ...                     # other variant sets
```
* Each session uses only what was known then: the radar from the prior closes, the 8:40 orders, the bitcoin gate
  at 8:40, fills and stops bar by bar, targets and dip-first entries at the runs, T+1 settlement. No news filter.
  Method and caveats in the `scripts/replay.py` docstring; reports in `research/replay/`.
* Results (Oct 6; `research/replay/*-2026-10-05-*`): the last 30 sessions (Aug 24-Oct 5) lost 6.4% under the
  Oct 6 rules (S&P 500 +1.2%): 14 closed trades, 13 stopped, 1 target (RKLB +21.6%, bought at the open on a
  0.83-ATR gap down). Over 2.8 years in 33 separate 22-session windows the same rules made a median +4.8% (mean
  +1.9%), from -30% to +28%, and beat the S&P 500 in 17. No variant doubled $1,000 in any 22-session window.
* What failed in the bad cases: support limits filled while the price fell through support (9 of 14 never rose
  0.5 ATR above the entry); 4 gapped through the stop overnight (RCAT, RGTI and SMR together on Sep 10: one
  speculative-tech bet, not three); GPUS lost 9-10% twice at full size because its stop sat 9-10% under the entry;
  GPUS also got an order at a "support" made of flat prints from a 6-session trading halt (Aug 17-24).
* Changes adopted Oct 6: (1) size from the stop: a position loses at most 1.5% of equity at its stop (2a); it cut
  the worst 22-session window from -30% to -21% and raised the mean of the hourly windows from +1.9% to +3.4%
  (median unchanged at +4.8%). (2) No entry in a name with a zero-volume session in the last 5 (`levels.py`
  marks it HALTED; `orders.py plan` skips it).
* Tested and rejected (worse or not better across the 5-minute and hourly windows): limits at the zone top; a
  3-session time exit (worse in every test); no bitcoin gate; ranking by R:R; buying every 0.5-ATR opening gap
  down and selling at the prior close; cancelling unfilled limits at 10:00; no entries after 10:30; stops 0.8-1.5
  ATR under support; GPUS, IREN and BTDR only with a tested support. Results swing with the start date: the best
  of 15 variants on the last 60 sessions (+7.8% median across its 31 overlapping windows) was ordinary over 2.8 years.
* Rule for future changes: a new rule trades only after it beats the live rules on the mean and the worst window
  of the separate hourly 22-session windows without losing on the 5-minute windows. One window proves nothing.

## 3. Execute and log

```bash
python3 scripts/trade.py buy UMAC --usd 250 --stop 20.79 --target 25.96 --tags radar --why "..."
python3 scripts/trade.py sell UMAC --all --why "..."
python3 scripts/trade.py buy NKE261002C00038000 --qty 3 --why "..."      # 3 option contracts
python3 scripts/trade.py buy BTC-USD --usd 200 --why "..." --stop 76000
python3 scripts/journal.py --kind trade --title "..." --body "..." --tickers UMAC
git add -A && git commit -m "..." && git push -q origin main
```
Every order gets a journal entry. Also journal decisions not to trade when they matter.

## 4. Publish

```bash
python3 scripts/snapshot.py
```
Then one `ArtifactData set` with the doc id it printed: collection `snapshots_guided`,
`file_path: /home/user/Investment_Challenge/.cache/snapshot_guided.json`.
Update the watchlist `strategy` (the dashboard's game-plan line) and `focus` when the plan changes.

## Schedule

* Weekdays: :10 runs 7:10 AM-7:10 PM, :40 runs 8:40 AM-7:40 PM, :25 and :55 runs 9:25 AM-3:55 PM,
  16:20 post-close review, plus one-shot checks at scheduled catalysts (earnings, jobs report).
* Crypto watch: weeknights 11:10 PM and weekends every 4 hours (only acts when the book holds crypto).
* Sunday 7:00 PM review for Monday: rebuild the radar (`levels.py build --save`) and journal Monday's triggers;
  replay the last 30 sessions (`replay.py --grid --days 30 --refresh --save`, 2d) and journal the week's bad cases.
* Clue scan (2b): `clues.py scan` at the 8:40 run, `clues.py movers` in every market-hours run, and
  `clues.py postmortem` at the 16:20 run.
* Resting orders (2c): `orders.py fill` first in every run after the sync; `orders.py plan --place` at the 8:40 run.
* Final day Wed Nov 4 (unless Vamsi extends it again): liquidate everything at the 15:40 run; the 16:20 run writes
  the final report, then deletes the routines.

Routine ids (for `delete_trigger` after the final report): see `config/schedule.json` `routine_ids`.
