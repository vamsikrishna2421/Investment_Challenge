# Post-earnings drift, 2026-10-10

60 large caps (60 largest US stocks), 1204 earnings reactions (8-K item 2.02), 2021-11-08 to 2026-09-25; method in the `scripts/earnings_drift_backtest.py` docstring. Bought at the reaction day's close; returns % after slippage, ± 95% clustered by date; 'up' is the share above zero. Edge = bucket minus baseline; the 5-session edge also for each half of the dates (split 2024-04-17).

| reaction | n | +1 day | +3 days | +5 days | median (5) | up (5) | +10 days | edge 5 | edge 5 by half | edge 10 | +5 days, stop 1 ATR under (stopped) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline (every close) | 73500 | -0.05 ± 0.06 | +0.05 ± 0.10 | +0.15 ± 0.12 | 0.14 | 52% | +0.40 ± 0.17 | +0.00 | +0.00 / +0.00 | +0.00 | - |
| all earnings reactions | 1204 | +0.06 ± 0.16 | +0.25 ± 0.27 | +0.36 ± 0.32 | 0.25 | 53% | +0.69 ± 0.42 | +0.21 | +0.18 / +0.25 | +0.29 | +0.25 ± 0.26 (50%) |
| up 2+ ATR | 247 | +0.25 ± 0.32 | +0.62 ± 0.47 | +0.75 ± 0.55 | 0.36 | 58% | +1.37 ± 0.70 | +0.60 | +0.41 / +0.75 | +0.97 | +0.48 ± 0.49 (53%) |
| up 1-2 ATR | 155 | +0.06 ± 0.43 | +0.32 ± 0.64 | +0.61 ± 0.73 | 0.56 | 59% | +1.18 ± 1.13 | +0.46 | +0.25 / +0.77 | +0.78 | +0.52 ± 0.65 (46%) |
| within 1 ATR | 420 | +0.04 ± 0.23 | +0.21 ± 0.40 | +0.22 ± 0.46 | 0.09 | 51% | +0.29 ± 0.60 | +0.07 | +0.18 / -0.03 | -0.11 | +0.16 ± 0.39 (47%) |
| down 1-2 ATR | 155 | +0.09 ± 0.35 | +0.32 ± 0.61 | +0.66 ± 0.74 | 0.0 | 50% | +0.58 ± 0.89 | +0.51 | +0.91 / +0.11 | +0.18 | +0.39 ± 0.68 (49%) |
| down 2+ ATR | 227 | -0.13 ± 0.31 | -0.16 ± 0.54 | -0.18 ± 0.67 | -0.09 | 49% | +0.43 ± 0.80 | -0.33 | -0.76 / -0.02 | +0.03 | -0.14 ± 0.55 (54%) |
| down 1+ ATR (both down buckets) | 382 | -0.04 ± 0.23 | +0.04 ± 0.42 | +0.16 ± 0.52 | -0.02 | 49% | +0.49 ± 0.63 | +0.01 | -0.02 / +0.03 | +0.09 | +0.08 ± 0.43 (52%) |
| up 1+ ATR, closed in the top quarter | 183 | +0.26 ± 0.40 | +0.14 ± 0.57 | +0.60 ± 0.68 | 0.58 | 58% | +1.26 ± 0.96 | +0.45 | +0.47 / +0.45 | +0.86 | +0.42 ± 0.59 (54%) |
| down 1+ ATR, closed in the bottom quarter | 172 | -0.13 ± 0.38 | -0.11 ± 0.62 | +0.13 ± 0.75 | -0.09 | 49% | +0.47 ± 0.97 | -0.02 | -0.40 / +0.32 | +0.07 | -0.14 ± 0.65 (53%) |
| gapped down 1+ ATR, closed up from the open | 108 | +0.02 ± 0.42 | -0.37 ± 0.74 | -0.18 ± 0.84 | -0.03 | 48% | +0.31 ± 1.01 | -0.33 | -0.48 / -0.21 | -0.09 | -0.28 ± 0.63 (58%) |

## Reading

- Large caps show the textbook drift instead: reactions 2+ ATR up rose a further 0.75% over 5 sessions (edge +0.60, positive in both halves; 1-2 ATR up: +0.46), drops did not rebound (down 1+ ATR: +0.01 edge).
- Effects of about half a percent over 5 sessions, inside ±0.55-0.73: real in the literature (post-earnings drift), too small for the challenge's arithmetic.
