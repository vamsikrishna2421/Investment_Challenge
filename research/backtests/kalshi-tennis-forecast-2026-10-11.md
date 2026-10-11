# Tennis forecast strategy on Kalshi, 2026-10-11

Method: `scripts/tennis_forecast_backtest.py` docstring. Settled matches: ATP tour 4,648, WTA tour 4,590, ATP Challenger 9,250, WTA Challenger 2,016, ITF women 16,610, ITF men 18,275. Both players rated in 10+ earlier matches: 18,555; priced (an even sample by competition and month, with a quote 6 hours before the close): 6,893, 2025-07-26 to 2026-10-11. Return per bet after fees, ± 95% clustered by date; bankroll from $1,000 at 2% a bet.

## Is the forecast better than the market's price?

Log loss of the match result (lower is better) with the market's mid price as the forecast and with the Elo forecast; and the matches where they differ by 15+ points: how often the Elo side won.

| competition | matches | market log loss | Elo log loss | differ 15+ points | Elo's side won |
|---|---:|---:|---:|---:|---:|
| all | 6893 | 0.5918 | 0.6607 | 2498 | 33.9% |
| ATP tour | 1791 | 0.5925 | 0.6573 | 623 | 37.7% |
| WTA tour | 1695 | 0.5905 | 0.6354 | 478 | 38.7% |
| ATP Challenger | 1248 | 0.6085 | 0.7009 | 520 | 33.8% |
| WTA Challenger | 666 | 0.6452 | 0.6993 | 243 | 35.8% |
| ITF men | 718 | 0.5219 | 0.6268 | 293 | 22.5% |
| ITF women | 775 | 0.585 | 0.6572 | 341 | 29.0% |

Weight on Elo in the blend, by month (0 = the market alone predicted best):

- ATP Challenger: 2026-01 0.00, 2026-02 0.00, 2026-03 0.00, 2026-04 0.00, 2026-05 0.00, 2026-06 0.00, 2026-07 0.00, 2026-08 0.00, 2026-09 0.00, 2026-10 0.00
- ATP tour: 2025-07 0.00, 2025-08 0.00, 2025-09 0.00, 2025-10 0.00, 2025-11 0.00, 2025-12 0.00, 2026-01 0.00, 2026-02 0.00, 2026-03 0.00, 2026-04 0.00, 2026-05 0.00, 2026-06 0.00, 2026-07 0.00, 2026-08 0.00, 2026-09 0.00, 2026-10 0.00
- ITF men: 2026-05 0.00, 2026-06 0.00, 2026-07 0.00, 2026-08 0.00, 2026-09 0.00, 2026-10 0.00
- ITF women: 2026-05 0.00, 2026-06 0.00, 2026-07 0.05, 2026-08 0.00, 2026-09 0.05, 2026-10 0.10
- WTA Challenger: 2026-01 0.00, 2026-02 0.00, 2026-03 0.00, 2026-04 0.75, 2026-05 0.55, 2026-06 0.20, 2026-07 0.05, 2026-08 0.00, 2026-09 0.00, 2026-10 0.00
- WTA tour: 2025-08 0.00, 2025-09 0.00, 2025-10 0.15, 2025-11 0.10, 2026-01 0.10, 2026-02 0.05, 2026-03 0.10, 2026-04 0.10, 2026-05 0.10, 2026-06 0.10, 2026-07 0.05, 2026-08 0.05, 2026-09 0.05, 2026-10 0.00

## Betting the forecast's edge

Elo: my rating of each player. Blend: Elo mixed with the market's mid at the weight that predicted best in the months before. Calibration: the share of contracts at the same price that won before, in the same competition (the favorite-longshot bias, where a competition showed one).

| forecast, entry, minimum edge | bets | won | return per bet | $1,000 became | average month | months up |
|---|---:|---:|---:|---:|---:|---:|
| Elo forecast, at the ask, 0 cents | 5744 | 39.3% (needs 42.7%) | -10.0% ± 3.4 | $48 | -24.08% | 0/10 |
| Elo forecast, at the ask, 3 cents | 4785 | 37.9% (needs 41.4%) | -10.4% ± 3.8 | $48 | -24.88% | 0/10 |
| Elo forecast, at the ask, 5 cents | 4167 | 36.7% (needs 40.5%) | -11.1% ± 4.3 | $49 | -24.39% | 0/10 |
| Elo forecast, at the ask, 10 cents | 2822 | 34.1% (needs 38.5%) | -13.3% ± 5.2 | $47 | -20.97% | 1/11 |
| Elo forecast, limit 1 cent over the bid, 0 cents | 3713 | 39.6% (needs 41.9%) | -6.8% ± 4.4 | $47 | -19.49% | 1/13 |
| Elo forecast, limit 1 cent over the bid, 3 cents | 3089 | 38.4% (needs 40.8%) | -7.2% ± 4.9 | $49 | -23.10% | 0/11 |
| Elo forecast, limit 1 cent over the bid, 5 cents | 2697 | 37.7% (needs 40.2%) | -8.1% ± 5.2 | $49 | -22.71% | 0/11 |
| Elo forecast, limit 1 cent over the bid, 10 cents | 1850 | 35.0% (needs 38.3%) | -10.2% ± 6.1 | $48 | -20.96% | 0/12 |
| Elo blended with the price, at the ask, 0 cents | 192 | 32.8% (needs 37.5%) | -11.7% ± 18.2 | $593 | -5.16% | 2/8 |
| Elo blended with the price, at the ask, 3 cents | 91 | 37.4% (needs 39.4%) | -3.6% ± 29.9 | $901 | +0.30% | 1/4 |
| Elo blended with the price, at the ask, 5 cents | 68 | 36.8% (needs 40.3%) | -4.7% ± 32.1 | $914 | -0.40% | 1/2 |
| Elo blended with the price, at the ask, 10 cents | 29 | 31.0% (needs 36.4%) | -4.0% ± 47.2 | $967 | -1.28% | 1/2 |
| Elo blended with the price, limit 1 cent over the bid, 0 cents | 379 | 35.1% (needs 37.2%) | -4.7% ± 13.7 | $606 | -2.65% | 8/13 |
| Elo blended with the price, limit 1 cent over the bid, 3 cents | 58 | 32.8% (needs 37.2%) | -10.1% ± 33.1 | $871 | -2.13% | 1/6 |
| Elo blended with the price, limit 1 cent over the bid, 5 cents | 40 | 32.5% (needs 38.4%) | -10.7% ± 38.5 | $906 | -2.32% | 2/4 |
| Elo blended with the price, limit 1 cent over the bid, 10 cents | 14 | 28.6% (needs 39.7%) | -17.8% ± 64.9 | $947 | -2.66% | 0/2 |
| calibration forecast, at the ask, 0 cents | 3298 | 56.0% (needs 58.6%) | -6.8% ± 3.0 | $48 | -18.38% | 2/13 |
| calibration forecast, at the ask, 3 cents | 1457 | 57.7% (needs 58.7%) | -3.1% ± 4.5 | $315 | -5.39% | 5/15 |
| calibration forecast, at the ask, 5 cents | 710 | 55.9% (needs 58.8%) | -5.4% ± 6.8 | $407 | -5.22% | 4/14 |
| calibration forecast, at the ask, 10 cents | 53 | 35.8% (needs 52.6%) | -36.6% ± 24.1 | $671 | -5.26% | 2/7 |

By competition (at the ask, edges of 0 and 5 cents):

| forecast, competition, minimum edge | bets | won | return per bet | $1,000 became | average month | months up |
|---|---:|---:|---:|---:|---:|---:|
| Elo forecast, ATP tour, 0 cents | 1510 | 40.7% (needs 44.4%) | -11.1% ± 6.3 | $49 | -15.98% | 2/14 |
| Elo forecast, WTA tour, 0 cents | 1373 | 42.1% (needs 44.4%) | -7.5% ± 6.5 | $81 | -12.87% | 5/14 |
| Elo forecast, ATP Challenger, 0 cents | 1068 | 38.8% (needs 44.3%) | -14.1% ± 7.7 | $49 | -26.46% | 0/9 |
| Elo forecast, WTA Challenger, 0 cents | 557 | 43.8% (needs 43.9%) | -1.1% ± 9.7 | $765 | -0.08% | 5/10 |
| Elo forecast, ITF men, 0 cents | 588 | 31.8% (needs 37.9%) | -22.0% ± 13.2 | $48 | -36.52% | 0/6 |
| Elo forecast, ITF women, 0 cents | 648 | 34.3% (needs 35.8%) | -3.0% ± 14.4 | $456 | -5.62% | 2/6 |
| Elo forecast, ATP tour, 5 cents | 1050 | 39.0% (needs 42.3%) | -9.4% ± 7.8 | $97 | -12.68% | 3/15 |
| Elo forecast, WTA tour, 5 cents | 937 | 38.7% (needs 42.7%) | -11.3% ± 8.0 | $88 | -13.97% | 3/14 |
| Elo forecast, ATP Challenger, 5 cents | 826 | 36.3% (needs 42.5%) | -15.1% ± 9.0 | $50 | -26.40% | 0/9 |
| Elo forecast, WTA Challenger, 5 cents | 407 | 42.3% (needs 41.8%) | +0.7% ± 12.3 | $933 | +1.39% | 5/10 |
| Elo forecast, ITF men, 5 cents | 444 | 28.8% (needs 34.8%) | -26.9% ± 14.7 | $73 | -33.38% | 0/6 |
| Elo forecast, ITF women, 5 cents | 503 | 31.2% (needs 33.6%) | -3.3% ± 16.4 | $513 | -4.02% | 2/6 |
| Elo blended with the price, ATP tour, 0 cents | 0 | - | - | - | - | - |
| Elo blended with the price, WTA tour, 0 cents | 43 | 30.2% (needs 31.8%) | -6.8% ± 43.1 | $925 | -0.92% | 3/7 |
| Elo blended with the price, ATP Challenger, 0 cents | 0 | - | - | - | - | - |
| Elo blended with the price, WTA Challenger, 0 cents | 136 | 36.0% (needs 40.8%) | -8.3% ± 20.6 | $764 | -5.98% | 1/3 |
| Elo blended with the price, ITF men, 0 cents | 0 | - | - | - | - | - |
| Elo blended with the price, ITF women, 0 cents | 13 | 7.7% (needs 21.6%) | -63.5% ± 66.5 | $840 | -15.97% | 0/1 |
| Elo blended with the price, ATP tour, 5 cents | 0 | - | - | - | - | - |
| Elo blended with the price, WTA tour, 5 cents | 0 | - | - | - | - | - |
| Elo blended with the price, ATP Challenger, 5 cents | 0 | - | - | - | - | - |
| Elo blended with the price, WTA Challenger, 5 cents | 68 | 36.8% (needs 40.3%) | -4.7% ± 32.1 | $914 | -0.40% | 1/2 |
| Elo blended with the price, ITF men, 5 cents | 0 | - | - | - | - | - |
| Elo blended with the price, ITF women, 5 cents | 0 | - | - | - | - | - |
| calibration forecast, ATP tour, 0 cents | 744 | 57.3% (needs 62.2%) | -12.2% ± 6.4 | $144 | -11.69% | 1/15 |
| calibration forecast, WTA tour, 0 cents | 637 | 52.0% (needs 55.5%) | -7.9% ± 8.4 | $313 | -7.89% | 2/13 |
| calibration forecast, ATP Challenger, 0 cents | 777 | 65.5% (needs 66.3%) | -2.3% ± 4.8 | $640 | -3.41% | 4/9 |
| calibration forecast, WTA Challenger, 0 cents | 394 | 42.1% (needs 44.2%) | -7.2% ± 11.1 | $517 | -5.04% | 4/9 |
| calibration forecast, ITF men, 0 cents | 425 | 69.2% (needs 68.9%) | -0.9% ± 7.2 | $880 | -1.11% | 2/5 |
| calibration forecast, ITF women, 0 cents | 321 | 38.0% (needs 41.4%) | -10.1% ± 15.7 | $452 | -12.97% | 1/5 |
| calibration forecast, ATP tour, 5 cents | 52 | 46.2% (needs 62.4%) | -32.4% ± 19.9 | $708 | -4.15% | 1/8 |
| calibration forecast, WTA tour, 5 cents | 98 | 54.1% (needs 53.9%) | +8.3% ± 27.1 | $1,135 | +1.46% | 5/10 |
| calibration forecast, ATP Challenger, 5 cents | 279 | 65.6% (needs 65.6%) | -2.0% ± 8.3 | $867 | -1.11% | 3/8 |
| calibration forecast, WTA Challenger, 5 cents | 138 | 40.6% (needs 42.3%) | -3.3% ± 21.1 | $874 | -0.74% | 6/8 |
| calibration forecast, ITF men, 5 cents | 119 | 62.2% (needs 69.8%) | -12.6% ± 14.5 | $729 | -5.93% | 1/5 |
| calibration forecast, ITF women, 5 cents | 24 | 29.2% (needs 31.7%) | -17.9% ± 57.4 | $908 | -1.79% | 1/5 |

## Narrowing to the competitions where it worked

Walk-forward: each month, only the competitions whose bets made money over the two months before (10+ bets); the bets it kept against those it dropped. Hindsight: the competitions that made money over the whole test.

| forecast, minimum edge, version | bets | won | return per bet | $1,000 became | average month | months up |
|---|---:|---:|---:|---:|---:|---:|
| Elo forecast, 0 cents, walk-forward kept | 766 | 41.8% (needs 42.7%) | -4.1% ± 9.6 | $422 | -8.72% | 3/7 |
| Elo forecast, 0 cents, walk-forward dropped | 4887 | 39.1% (needs 42.8%) | -10.9% ± 3.8 | $49 | -25.56% | 1/9 |
| Elo forecast, 0 cents, hindsight (none) | 0 | - | - | - | - | - |
| Elo forecast, 3 cents, walk-forward kept | 642 | 39.6% (needs 40.9%) | -5.4% ± 10.2 | $407 | -13.01% | 1/6 |
| Elo forecast, 3 cents, walk-forward dropped | 4067 | 37.7% (needs 41.6%) | -11.0% ± 4.3 | $48 | -27.64% | 0/9 |
| Elo forecast, 3 cents, hindsight (WTA Challenger) | 461 | 43.2% (needs 42.6%) | +0.1% ± 11.2 | $883 | +1.00% | 5/10 |
| Elo forecast, 5 cents, walk-forward kept | 654 | 38.4% (needs 39.8%) | -4.3% ± 9.8 | $479 | -12.02% | 1/5 |
| Elo forecast, 5 cents, walk-forward dropped | 3443 | 36.5% (needs 40.8%) | -12.0% ± 5.0 | $46 | -27.73% | 0/9 |
| Elo forecast, 5 cents, hindsight (WTA Challenger) | 407 | 42.3% (needs 41.8%) | +0.7% ± 12.3 | $933 | +1.39% | 5/10 |
| Elo forecast, 10 cents, walk-forward kept | 539 | 35.4% (needs 39.6%) | -11.2% ± 10.4 | $252 | -12.79% | 3/8 |
| Elo forecast, 10 cents, walk-forward dropped | 2241 | 33.9% (needs 38.4%) | -13.4% ± 6.2 | $47 | -22.77% | 0/10 |
| Elo forecast, 10 cents, hindsight (none) | 0 | - | - | - | - | - |
| Elo blended with the price, 0 cents, walk-forward kept | 61 | 21.3% (needs 36.3%) | -42.4% ± 22.0 | $587 | -15.50% | 0/3 |
| Elo blended with the price, 0 cents, walk-forward dropped | 117 | 37.6% (needs 38.3%) | +1.7% ± 26.6 | $989 | +1.53% | 2/5 |
| Elo blended with the price, 0 cents, hindsight (none) | 0 | - | - | - | - | - |
| Elo blended with the price, 3 cents, walk-forward kept | 39 | 17.9% (needs 35.5%) | -55.2% ± 24.0 | $640 | -36.02% | 0/1 |
| Elo blended with the price, 3 cents, walk-forward dropped | 5 | 20.0% (needs 36.3%) | -40.3% ± 104.7 | $959 | -4.10% | 0/1 |
| Elo blended with the price, 3 cents, hindsight (none) | 0 | - | - | - | - | - |
| Elo blended with the price, 5 cents, walk-forward kept | 0 | - | - | - | - | - |
| Elo blended with the price, 5 cents, walk-forward dropped | 0 | - | - | - | - | - |
| Elo blended with the price, 5 cents, hindsight (none) | 0 | - | - | - | - | - |
| Elo blended with the price, 10 cents, walk-forward kept | 0 | - | - | - | - | - |
| Elo blended with the price, 10 cents, walk-forward dropped | 0 | - | - | - | - | - |
| Elo blended with the price, 10 cents, hindsight (none) | 0 | - | - | - | - | - |
| calibration forecast, 0 cents, walk-forward kept | 909 | 57.0% (needs 60.8%) | -9.2% ± 5.6 | $160 | -22.48% | 1/6 |
| calibration forecast, 0 cents, walk-forward dropped | 2294 | 55.9% (needs 58.0%) | -5.7% ± 4.0 | $45 | -19.08% | 3/13 |
| calibration forecast, 0 cents, hindsight (none) | 0 | - | - | - | - | - |
| calibration forecast, 3 cents, walk-forward kept | 699 | 56.5% (needs 58.7%) | -5.5% ± 6.8 | $401 | -6.69% | 4/9 |
| calibration forecast, 3 cents, walk-forward dropped | 694 | 60.5% (needs 60.0%) | +0.8% ± 6.9 | $1,002 | +1.15% | 6/13 |
| calibration forecast, 3 cents, hindsight (WTA tour) | 256 | 56.2% (needs 54.7%) | +3.4% ± 14.4 | $1,108 | +1.38% | 7/13 |
| calibration forecast, 5 cents, walk-forward kept | 209 | 52.2% (needs 52.8%) | -3.2% ± 14.5 | $834 | -1.03% | 4/8 |
| calibration forecast, 5 cents, walk-forward dropped | 468 | 58.1% (needs 62.2%) | -6.2% ± 8.1 | $522 | -4.85% | 4/12 |
| calibration forecast, 5 cents, hindsight (WTA tour) | 98 | 54.1% (needs 53.9%) | +8.3% ± 27.1 | $1,135 | +1.46% | 5/10 |
| calibration forecast, 10 cents, walk-forward kept | 0 | - | - | - | - | - |
| calibration forecast, 10 cents, walk-forward dropped | 35 | 22.9% (needs 42.5%) | -48.4% ± 32.0 | $706 | -6.38% | 1/5 |
| calibration forecast, 10 cents, hindsight (none) | 0 | - | - | - | - | - |

## Reading

- The forecast is worse than the price in every competition: log loss 0.661 against the market's 0.592 overall (0.627 against 0.522 in ITF men, where the gap is widest). Where the two differed by 15+ points (2,498 matches) the Elo side won 33.9% of the time: the bigger the disagreement, the more often the market was right.
- Betting the forecast's edge at the ask lost 10.0% a bet (± 3.4; 5,744 bets, 39.3% won against 42.7% needed); larger minimum edges lost more (10 cents: -13.3%). At 2% of the bankroll a bet, $1,000 fell to $48 over the test, down in every month but one, on a sample of a third of the rated matches (betting every match would lose faster).
- Limit orders 1 cent over the bid cut the loss to 6.8% a bet (± 4.4): they save about 3 cents of spread and fees, but they fill mostly when the price moves against the bet.
- Elo blended with the price at the weight that predicted best in the months before: the weight was 0 (the market alone) in 4 of 6 competitions throughout and at most 0.15 on the WTA tour; the few bets it made lost 3.6-11.7% a bet. Elo carries no information the price lacks.
- The market-calibration forecast (the favorite-longshot bias by competition and price band, walk-forward) lost 6.8% a bet at any edge (± 3.0) and 3.1% (± 4.5) with 3 cents of edge required.
- By competition, no forecast made money: the Elo forecast's best was WTA Challengers (-1.1% ± 9.7; +0.7% ± 12.3 with 5 cents of edge, 407 bets). Walk-forward narrowing to the competitions that had made money over the two months before cut the Elo loss to about 4% a bet ($1,000 to $422, -8.7% a month) against 11% for the competitions it dropped, still a loss; for the calibration forecast it helped at one edge and hurt at two. Only hindsight finds a winner (WTA tour calibration bets, +3.4% ± 14.4 on 256 bets), and nothing marked it in advance.
- No version is worth money. The book does not trade prediction markets (RUNBOOK 1g); no change.
