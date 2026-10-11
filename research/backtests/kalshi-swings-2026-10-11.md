# In-match swing trading on Kalshi tennis, 2026-10-11

300 settled ATP/WTA match markets with trade history, 2026-08-12 to 2026-10-11; method in the `scripts/swing_backtest.py` docstring. Returns per dollar of the first leg; ± 95% clustered by date. 'Fair odds' is the share that would reach the target if prices were fair: the actual entry price over the target, averaged (the first trade under the threshold is often well under it, after a jump).

## all matches: 300 matches

| buy at, sell at | matches entered | reached the target | fair odds | won when held | return gross | return net (spread and fees) |
|---|---|---|---|---|---|---|
| 30c, 60c | 300 | 39.7% | 42.8% | 0.0% | -5.2% ± 13.1 | -22.0% ± 10.8 |
| 20c, 40c | 300 | 47.0% | 47.2% | 0.0% | +5.6% ± 14.4 | -18.6% ± 10.7 |
| 30c, 50c | 300 | 51.7% | 51.3% | 0.0% | +4.0% ± 12.9 | -15.6% ± 10.2 |
| 40c, 60c | 300 | 48.3% | 51.7% | 0.0% | -4.5% ± 10.8 | -20.3% ± 8.7 |
| 10c, 30c | 300 | 32.7% | 32.5% | 0.0% | +4.5% ± 17.6 | -27.6% ± 12.1 |
| 20c, 60c | 300 | 31.0% | 31.5% | 0.0% | -0.9% ± 17.9 | -20.4% ± 14.3 |
| 15c, 20c | 300 | 69.3% | 69.7% | 0.0% | +12.0% ± 14.7 | -22.6% ± 8.7 |
| 15c, 25c | 300 | 58.3% | 55.8% | 0.0% | +15.1% ± 17.6 | -18.9% ± 10.6 |

## evenly matched (both opened 35-65 cents): 157 matches

| buy at, sell at | matches entered | reached the target | fair odds | won when held | return gross | return net (spread and fees) |
|---|---|---|---|---|---|---|
| 30c, 60c | 157 | 48.4% | 47.5% | 0.0% | +4.5% ± 18.0 | -12.7% ± 15.1 |
| 20c, 40c | 157 | 52.2% | 49.2% | 0.0% | +8.6% ± 16.7 | -14.8% ± 13.2 |
| 30c, 50c | 157 | 60.5% | 57.1% | 0.0% | +9.4% ± 15.6 | -9.8% ± 12.8 |
| 40c, 60c | 157 | 63.7% | 62.4% | 0.0% | +6.0% ± 12.2 | -9.7% ± 10.3 |
| 10c, 30c | 157 | 33.8% | 32.4% | 0.0% | +5.6% ± 22.9 | -26.4% ± 16.0 |
| 20c, 60c | 157 | 36.9% | 32.8% | 0.0% | +13.5% ± 24.4 | -8.1% ± 19.8 |
| 15c, 20c | 157 | 70.1% | 70.7% | 0.0% | +9.3% ± 18.5 | -24.7% ± 10.6 |
| 15c, 25c | 157 | 58.0% | 56.5% | 0.0% | +12.1% ± 23.9 | -21.4% ± 13.9 |

## clear favorite (opened outside 35-65 cents): 143 matches

| buy at, sell at | matches entered | reached the target | fair odds | won when held | return gross | return net (spread and fees) |
|---|---|---|---|---|---|---|
| 30c, 60c | 143 | 30.1% | 37.6% | 0.0% | -15.9% ± 18.6 | -32.2% ± 14.4 |
| 20c, 40c | 143 | 41.3% | 45.0% | 0.0% | +2.4% ± 22.3 | -22.8% ± 15.7 |
| 30c, 50c | 143 | 42.0% | 45.1% | 0.0% | -2.0% ± 16.9 | -22.1% ± 12.8 |
| 40c, 60c | 143 | 31.5% | 40.0% | 0.0% | -16.0% ± 17.5 | -32.0% ± 13.6 |
| 10c, 30c | 143 | 31.5% | 32.6% | 0.0% | +3.3% ± 24.0 | -29.0% ± 15.8 |
| 20c, 60c | 143 | 24.5% | 30.0% | 0.0% | -16.7% ± 22.9 | -34.0% ± 17.9 |
| 15c, 20c | 143 | 68.5% | 68.6% | 0.0% | +14.9% ± 19.4 | -20.3% ± 12.4 |
| 15c, 25c | 143 | 58.7% | 54.9% | 0.0% | +18.4% ± 20.3 | -16.2% ± 13.3 |

## Reading

- Swings happen at the rate the price implies: across all 300 matches each rule reached its target within a few points of fair odds (bought at 30 cents, reached 60: 39.7% against 42.8% fair; Vamsi's under-15-to-20: 69.3% against 69.7%). Before costs every rule is a wash (-5% to +15%, inside ±11-18).
- After the spread, Robinhood's 1 cent and Kalshi's fee on both legs, every rule lost 16-28% of the first leg (under-15-to-20: -22.6% ± 8.7).
- Evenly matched (157 matches, both opened 35-65 cents): comebacks a little more often than fair (30 to 60: 48.4% against 47.5%; 20 to 60: 36.9% against 32.8%), still -8% to -26% after costs. Clear favorites (143): the trailing player came back less often than priced (30 to 60: 30.1% against 37.6%), -16% to -34% after costs. Both differences sit inside the noise.
- Verdict: no trade. The price already holds the comeback odds; the costs of two legs decide the result.
