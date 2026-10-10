# Hourly candlestick patterns, 2026-10-10

62 large caps (60 largest US stocks, SPY, QQQ), hourly bars 2023-11-10 to 2026-10-09 (730 sessions); method in the `scripts/candle_backtest.py` docstring. 'net' is after slippage on market fills (entry, stops, closes; 5 bps a side at $20+, 20 at $5-20, 50 under $5), 'gross' before any cost; means % ± 95% clustered by date. 'up' is the share of trades that rose (gross). Edge = signal minus baseline (gross), also for each half of the dates (split 2025-04-29).

## Next hour and the rest of the session (all sessions)

| signal | n | per day | next hour net | gross | up | to the close net | gross | next close net | edge 1h | edge 1h by half | edge to the close |
|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline (every bar) | 268874 | 368.3 | -0.10 ± 0.01 | +0.00 ± 0.01 | 51% | -0.09 ± 0.03 | +0.01 ± 0.03 | -0.01 ± 0.06 | +0.00 | +0.00 / +0.00 | +0.00 |
| hammer | 3837 | 5.3 | -0.10 ± 0.02 | +0.00 ± 0.02 | 49% | -0.10 ± 0.04 | -0.00 ± 0.04 | +0.03 ± 0.10 | +0.00 | +0.00 / +0.00 | -0.01 |
| bullish engulfing | 7600 | 10.4 | -0.09 ± 0.02 | +0.01 ± 0.02 | 50% | -0.07 ± 0.07 | +0.03 ± 0.07 | -0.07 ± 0.09 | +0.01 | +0.02 / +0.00 | +0.02 |
| piercing line | 1816 | 2.5 | -0.06 ± 0.05 | +0.04 ± 0.05 | 53% | -0.06 ± 0.06 | +0.04 ± 0.06 | -0.12 ± 0.14 | +0.04 | +0.06 / +0.01 | +0.03 |
| morning star | 1120 | 1.5 | -0.08 ± 0.03 | +0.02 ± 0.03 | 52% | -0.00 ± 0.18 | +0.10 ± 0.18 | -0.02 ± 0.18 | +0.02 | +0.01 / +0.02 | +0.09 |
| bullish harami | 3754 | 5.1 | -0.11 ± 0.02 | -0.01 ± 0.02 | 48% | -0.12 ± 0.04 | -0.01 ± 0.04 | -0.09 ± 0.10 | -0.01 | -0.03 / -0.00 | -0.02 |
| three white soldiers | 708 | 1.0 | -0.15 ± 0.04 | -0.05 ± 0.04 | 48% | -0.16 ± 0.06 | -0.06 ± 0.06 | -0.03 ± 0.19 | -0.05 | -0.06 / -0.05 | -0.07 |
| big green bar | 9513 | 13.0 | -0.09 ± 0.02 | +0.01 ± 0.02 | 51% | -0.09 ± 0.04 | +0.01 ± 0.04 | +0.01 ± 0.09 | +0.01 | -0.01 / +0.02 | -0.00 |
| shooting star | 3879 | 5.3 | -0.09 ± 0.02 | +0.01 ± 0.02 | 53% | -0.07 ± 0.04 | +0.03 ± 0.04 | -0.01 ± 0.09 | +0.01 | +0.02 / +0.01 | +0.02 |
| bearish engulfing | 8460 | 11.6 | -0.10 ± 0.01 | +0.00 ± 0.01 | 52% | -0.10 ± 0.03 | +0.00 ± 0.03 | +0.01 ± 0.09 | +0.00 | -0.00 / +0.00 | -0.01 |
| dark cloud cover | 1888 | 2.6 | -0.11 ± 0.02 | -0.01 ± 0.02 | 52% | -0.10 ± 0.04 | -0.00 ± 0.04 | -0.06 ± 0.12 | -0.01 | -0.00 / -0.01 | -0.01 |
| evening star | 1137 | 1.6 | -0.09 ± 0.03 | +0.01 ± 0.03 | 53% | -0.07 ± 0.05 | +0.03 ± 0.05 | -0.07 ± 0.14 | +0.01 | -0.00 / +0.03 | +0.02 |
| three black crows | 604 | 0.8 | -0.07 ± 0.06 | +0.03 ± 0.06 | 50% | -0.05 ± 0.11 | +0.05 ± 0.11 | +0.07 ± 0.29 | +0.03 | +0.03 / +0.02 | +0.04 |
| big red bar | 9321 | 12.8 | -0.11 ± 0.03 | -0.01 ± 0.03 | 52% | -0.10 ± 0.06 | +0.00 ± 0.06 | -0.00 ± 0.13 | -0.01 | -0.01 / -0.01 | -0.01 |

## The +0.5% scalp on 5-minute bars (2026-07-17 to 2026-10-09, 60 sessions)

Bought at the next hour's open; sold at +0.5%, else at the stop, else at the session close. 'both' is the share of trades whose stop and target fell inside one 5-minute bar (counted as the stop).

| signal | n | +0.5%/-0.5% net | gross | target / stop (both) | +0.5%/pattern low net | gross | target / stop | +0.5%/no stop net | gross | target hit |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline (every bar) | 22320 | -0.09 ± 0.02 | -0.00 ± 0.02 | 32.9% / 33.7% (0.1%) | - | - | -% / -% | -0.09 ± 0.04 | -0.01 ± 0.03 | 37.1% |
| hammer | 268 | -0.10 ± 0.05 | -0.02 ± 0.05 | 31.3% / 36.6% (0.0%) | -0.11 ± 0.06 | -0.02 ± 0.06 | 33.6% / 35.8% | -0.12 ± 0.08 | -0.04 ± 0.08 | 35.4% |
| bullish engulfing | 664 | -0.11 ± 0.04 | -0.03 ± 0.04 | 29.4% / 33.6% (0.0%) | -0.11 ± 0.05 | -0.03 ± 0.05 | 33.1% / 22.1% | -0.12 ± 0.06 | -0.03 ± 0.05 | 34.0% |
| piercing line | 162 | -0.15 ± 0.07 | -0.07 ± 0.06 | 27.2% / 39.5% (0.6%) | -0.17 ± 0.08 | -0.09 ± 0.08 | 29.6% / 28.4% | -0.17 ± 0.09 | -0.08 ± 0.08 | 30.9% |
| morning star | 88 | -0.17 ± 0.10 | -0.08 ± 0.09 | 27.3% / 43.2% (0.0%) | -0.24 ± 0.14 | -0.16 ± 0.14 | 30.7% / 17.0% | -0.25 ± 0.14 | -0.17 ± 0.14 | 30.7% |
| bullish harami | 354 | -0.06 ± 0.06 | +0.02 ± 0.06 | 37.3% / 34.5% (0.3%) | -0.04 ± 0.06 | +0.04 ± 0.06 | 37.6% / 41.2% | -0.05 ± 0.08 | +0.03 ± 0.07 | 41.5% |
| three white soldiers | 54 | -0.07 ± 0.10 | +0.02 ± 0.10 | 31.5% / 25.9% (0.0%) | -0.05 ± 0.15 | +0.03 ± 0.15 | 37.0% / 0.0% | -0.05 ± 0.15 | +0.03 ± 0.15 | 37.0% |
| big green bar | 736 | -0.13 ± 0.05 | -0.05 ± 0.04 | 35.2% / 44.4% (0.0%) | -0.14 ± 0.08 | -0.07 ± 0.08 | 42.8% / 12.1% | -0.15 ± 0.09 | -0.07 ± 0.08 | 42.8% |

## Reading

- No pattern moves the next hour more than 0.05% from the baseline (+0.00%, 51% up; CIs ±0.02-0.06%). The only one consistent in both halves is three white soldiers at -0.05%: a bullish pattern followed by a slight fall.
- The +0.5%/-0.5% scalp: a third of trades reach +0.5% first, a third -0.5%, a third neither by the close. Baseline -0.00% before costs, -0.09% after; patterns -0.08% to +0.02% before costs, all negative after.
- Verdict: no edge on large caps either; their small spreads only make the loss smaller.
