# Daily candlestick patterns, 2026-10-10

68 radar candidates, daily bars 2021-10-29 to 2026-10-01 (1235 sessions); method in the `scripts/candle_backtest.py` docstring (--daily). Bought at the next day's open; 'net' after slippage (5 bps a side at $20+, 20 at $5-20, 50 under $5), 'gross' before costs; means % ± 95% clustered by date. 'up' is the share that rose by the day's close (gross). Edge = signal minus baseline (gross), also for each half of the dates (split 2024-04-16).

| signal | n | per day | that day net | gross | up | 3 days gross | 5 days net | gross | edge 1 day | edge 1 day by half | edge 5 days | edge 5 days by half |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline (every day) | 74296 | 60.2 | -0.46 ± 0.15 | -0.06 ± 0.15 | 46% | +0.33 ± 0.31 | +0.35 ± 0.42 | +0.76 ± 0.42 | +0.00 | +0.00 / +0.00 | +0.00 | +0.00 / +0.00 |
| hammer | 1008 | 0.8 | -0.23 ± 0.47 | +0.19 ± 0.48 | 47% | +0.83 ± 1.29 | +1.51 ± 2.14 | +1.94 ± 2.15 | +0.25 | +0.44 / +0.07 | +1.18 | +0.38 / +2.33 |
| bullish engulfing | 1433 | 1.2 | -0.68 ± 0.48 | -0.26 ± 0.48 | 46% | +0.67 ± 1.17 | +0.56 ± 2.69 | +0.99 ± 2.70 | -0.20 | -0.17 / -0.19 | +0.24 | -1.58 / +2.41 |
| piercing line | 327 | 0.3 | -1.05 ± 0.77 | -0.62 ± 0.78 | 42% | +0.65 ± 1.10 | -0.43 ± 1.55 | -0.01 ± 1.56 | -0.56 | +0.37 / -1.39 | -0.76 | -0.17 / -1.25 |
| morning star | 420 | 0.3 | +0.10 ± 0.75 | +0.55 ± 0.75 | 49% | +0.41 ± 1.26 | -0.22 ± 1.58 | +0.23 ± 1.59 | +0.61 | +0.66 / +0.56 | -0.52 | +0.70 / -1.59 |
| bullish harami | 840 | 0.7 | -0.33 ± 0.54 | +0.08 ± 0.54 | 47% | +0.75 ± 0.91 | +0.25 ± 1.17 | +0.66 ± 1.17 | +0.14 | +0.59 / -0.22 | -0.10 | +0.68 / -0.78 |
| three white soldiers | 108 | 0.1 | -0.93 ± 0.93 | -0.57 ± 0.94 | 43% | +0.15 ± 2.09 | -0.45 ± 3.21 | -0.10 ± 3.23 | -0.51 | +0.27 / -1.68 | -0.86 | +0.32 / -2.02 |
| big green bar | 2715 | 2.2 | -0.13 ± 0.33 | +0.25 ± 0.33 | 49% | +1.03 ± 0.79 | +1.10 ± 1.55 | +1.49 ± 1.55 | +0.31 | +0.44 / +0.19 | +0.73 | +0.42 / +0.96 |
| shooting star | 1137 | 0.9 | -0.54 ± 0.43 | -0.16 ± 0.43 | 44% | -0.28 ± 0.83 | -0.76 ± 1.09 | -0.38 ± 1.10 | -0.10 | +0.33 / -0.48 | -1.14 | +0.09 / -2.20 |
| bearish engulfing | 1593 | 1.3 | -0.35 ± 0.45 | +0.06 ± 0.45 | 46% | +0.81 ± 0.78 | +1.64 ± 1.15 | +2.06 ± 1.15 | +0.12 | -0.08 / +0.29 | +1.31 | +1.56 / +1.10 |
| dark cloud cover | 480 | 0.4 | -0.22 ± 0.56 | +0.23 ± 0.56 | 46% | +0.84 ± 1.09 | +1.18 ± 1.51 | +1.63 ± 1.53 | +0.29 | +0.12 / +0.42 | +0.87 | +1.83 / +0.05 |
| evening star | 365 | 0.3 | -0.04 ± 0.57 | +0.32 ± 0.57 | 49% | +0.65 ± 1.35 | +0.76 ± 1.67 | +1.11 ± 1.67 | +0.38 | +0.36 / +0.39 | +0.36 | +0.24 / +0.42 |
| three black crows | 223 | 0.2 | -0.78 ± 0.99 | -0.28 ± 1.01 | 46% | -0.43 ± 1.74 | -1.17 ± 2.53 | -0.69 ± 2.56 | -0.22 | -0.03 / -0.42 | -1.44 | -1.03 / -1.58 |
| big red bar | 2661 | 2.2 | -0.23 ± 0.44 | +0.17 ± 0.44 | 48% | +0.20 ± 0.81 | +0.36 ± 0.99 | +0.77 ± 0.99 | +0.23 | -0.23 / +0.69 | +0.01 | +0.80 / -0.65 |

## Reading

- Edges positive in both halves of the dates: morning star +0.61% the next day, big green bar +0.31% the next day and +0.73% over 5 days, evening star +0.38% the next day, bearish engulfing +1.31% over 5 days. CIs run ±0.3% to ±2.7%, so none is distinguishable from noise, and two of the four are bearish patterns followed by gains.
- The daily runs make 52 comparisons (13 patterns, 2 horizons, 2 universes); at 95% confidence two or three look good by chance alone. None here clears that bar together with a reason to exist.
