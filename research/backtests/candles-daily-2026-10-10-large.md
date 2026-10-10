# Daily candlestick patterns, 2026-10-10

62 large caps (60 largest US stocks, SPY, QQQ), daily bars 2021-10-29 to 2026-10-01 (1235 sessions); method in the `scripts/candle_backtest.py` docstring (--daily). Bought at the next day's open; 'net' after slippage (5 bps a side at $20+, 20 at $5-20, 50 under $5), 'gross' before costs; means % ± 95% clustered by date. 'up' is the share that rose by the day's close (gross). Edge = signal minus baseline (gross), also for each half of the dates (split 2024-04-16).

| signal | n | per day | that day net | gross | up | 3 days gross | 5 days net | gross | edge 1 day | edge 1 day by half | edge 5 days | edge 5 days by half |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline (every day) | 76570 | 62.0 | -0.07 ± 0.05 | +0.03 ± 0.05 | 51% | +0.13 ± 0.09 | +0.13 ± 0.12 | +0.23 ± 0.12 | +0.00 | +0.00 / +0.00 | +0.00 | +0.00 / +0.00 |
| hammer | 1072 | 0.9 | +0.04 ± 0.14 | +0.14 ± 0.13 | 56% | +0.44 ± 0.27 | +0.47 ± 0.40 | +0.57 ± 0.40 | +0.11 | +0.14 / +0.08 | +0.34 | +0.41 / +0.26 |
| bullish engulfing | 1370 | 1.1 | -0.12 ± 0.19 | -0.02 ± 0.19 | 50% | +0.08 ± 0.27 | -0.19 ± 0.36 | -0.08 ± 0.36 | -0.05 | +0.03 / -0.13 | -0.32 | -0.47 / -0.15 |
| piercing line | 302 | 0.2 | -0.01 ± 0.26 | +0.10 ± 0.26 | 52% | +0.15 ± 0.38 | -0.35 ± 0.53 | -0.24 ± 0.53 | +0.07 | +0.30 / -0.15 | -0.48 | -0.57 / -0.40 |
| morning star | 433 | 0.4 | -0.22 ± 0.26 | -0.12 ± 0.26 | 46% | +0.03 ± 0.45 | -0.13 ± 0.56 | -0.02 ± 0.56 | -0.15 | -0.20 / -0.09 | -0.26 | -0.28 / -0.23 |
| bullish harami | 867 | 0.7 | +0.06 ± 0.14 | +0.16 ± 0.14 | 56% | +0.21 ± 0.31 | +0.23 ± 0.40 | +0.33 ± 0.40 | +0.13 | +0.21 / +0.06 | +0.10 | +0.04 / +0.13 |
| three white soldiers | 169 | 0.1 | -0.11 ± 0.20 | -0.01 ± 0.20 | 53% | -0.13 ± 0.47 | -0.03 ± 0.50 | +0.08 ± 0.50 | -0.04 | -0.25 / +0.13 | -0.16 | +0.33 / -0.56 |
| big green bar | 2793 | 2.3 | -0.07 ± 0.12 | +0.03 ± 0.12 | 51% | -0.01 ± 0.21 | -0.18 ± 0.28 | -0.08 ± 0.28 | +0.00 | -0.01 / +0.01 | -0.31 | -0.44 / -0.17 |
| shooting star | 1046 | 0.8 | -0.06 ± 0.13 | +0.04 ± 0.13 | 51% | +0.20 ± 0.29 | +0.23 ± 0.30 | +0.34 ± 0.30 | +0.01 | +0.02 / +0.01 | +0.10 | +0.21 / -0.01 |
| bearish engulfing | 1624 | 1.3 | -0.07 ± 0.11 | +0.03 ± 0.11 | 53% | +0.42 ± 0.19 | +0.31 ± 0.25 | +0.41 ± 0.25 | +0.00 | +0.05 / -0.04 | +0.18 | +0.24 / +0.12 |
| dark cloud cover | 357 | 0.3 | -0.22 ± 0.19 | -0.12 ± 0.19 | 46% | +0.08 ± 0.39 | +0.04 ± 0.53 | +0.14 ± 0.53 | -0.15 | -0.13 / -0.16 | -0.09 | +0.43 / -0.56 |
| evening star | 468 | 0.4 | -0.16 ± 0.16 | -0.06 ± 0.16 | 48% | +0.01 ± 0.40 | -0.19 ± 0.54 | -0.08 ± 0.54 | -0.09 | +0.02 / -0.23 | -0.32 | -0.47 / -0.11 |
| three black crows | 131 | 0.1 | +0.25 ± 0.45 | +0.35 ± 0.46 | 55% | +0.20 ± 0.65 | +0.23 ± 0.71 | +0.33 ± 0.71 | +0.32 | +0.68 / +0.08 | +0.10 | +0.18 / +0.03 |
| big red bar | 2726 | 2.2 | -0.00 ± 0.17 | +0.10 ± 0.17 | 53% | +0.29 ± 0.36 | +0.22 ± 0.39 | +0.32 ± 0.39 | +0.07 | +0.09 / +0.04 | +0.09 | +0.02 / +0.16 |

## Reading

- Hammer: +0.11% the next day and +0.34% over 5 days above the baseline, positive in both halves of the 5 years; bullish harami +0.13% the next day. Neither is distinguishable from noise (CIs ±0.13% next day, ±0.40% over 5 days), and bearish engulfing, the opposite signal, also beat the baseline over 5 days (+0.18%): what they share is a fall before the signal (short-term reversal), not the candle's shape.
- Bullish engulfing, piercing line, morning star and big green bar ran below the baseline over 5 days (-0.08% to -0.48%).
- At face value a large-cap hammer returns +0.47% over 5 days after costs, about one signal a day across the 62 names.
