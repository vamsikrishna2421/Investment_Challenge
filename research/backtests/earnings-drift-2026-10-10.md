# Post-earnings drift, 2026-10-10

67 radar candidates, 981 earnings reactions (8-K item 2.02), 2021-11-08 to 2026-09-25; method in the `scripts/earnings_drift_backtest.py` docstring. Bought at the reaction day's close; returns % after slippage, ± 95% clustered by date; 'up' is the share above zero. Edge = bucket minus baseline; the 5-session edge also for each half of the dates (split 2024-04-17).

| reaction | n | +1 day | +3 days | +5 days | median (5) | up (5) | +10 days | edge 5 | edge 5 by half | edge 10 | +5 days, stop 1 ATR under (stopped) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline (every close) | 73575 | -0.22 ± 0.18 | +0.15 ± 0.32 | +0.55 ± 0.42 | -0.6 | 45% | +1.49 ± 0.61 | +0.00 | +0.00 / +0.00 | +0.00 | - |
| all earnings reactions | 981 | +0.54 ± 0.75 | +1.00 ± 1.08 | +1.14 ± 1.40 | -1.16 | 45% | +2.43 ± 2.11 | +0.59 | +1.40 / -0.15 | +0.94 | +1.00 ± 1.29 (49%) |
| up 2+ ATR | 144 | +0.51 ± 1.25 | +0.29 ± 1.62 | -0.37 ± 2.09 | -1.64 | 40% | +3.20 ± 3.41 | -0.92 | -0.79 / -0.93 | +1.71 | +0.32 ± 1.64 (64%) |
| up 1-2 ATR | 111 | +0.21 ± 1.46 | +1.58 ± 2.05 | +0.24 ± 2.21 | -0.15 | 49% | +1.81 ± 3.48 | -0.31 | +0.46 / -1.00 | +0.32 | -0.33 ± 1.94 (52%) |
| within 1 ATR | 457 | +0.11 ± 1.04 | +0.12 ± 1.50 | +0.25 ± 1.96 | -2.02 | 42% | +1.56 ± 3.33 | -0.30 | +0.19 / -0.79 | +0.07 | +0.24 ± 1.76 (49%) |
| down 1-2 ATR | 149 | +1.57 ± 1.42 | +2.97 ± 2.24 | +3.83 ± 2.69 | 1.48 | 54% | +4.79 ± 3.82 | +3.28 | +5.13 / +1.95 | +3.30 | +3.01 ± 2.75 (38%) |
| down 2+ ATR | 120 | +1.26 ± 2.31 | +2.22 ± 3.04 | +3.79 ± 4.63 | 0.04 | 50% | +2.44 ± 5.05 | +3.24 | +6.09 / +0.91 | +0.95 | +3.45 ± 4.55 (44%) |
| down 1+ ATR (both down buckets) | 269 | +1.43 ± 1.36 | +2.64 ± 1.94 | +3.81 ± 2.66 | 0.45 | 52% | +3.74 ± 3.18 | +3.26 | +5.62 / +1.52 | +2.25 | +3.21 ± 2.64 (41%) |
| up 1+ ATR, closed in the top quarter | 128 | +0.77 ± 1.37 | +1.09 ± 2.01 | -0.30 ± 2.16 | -1.18 | 41% | +3.07 ± 3.72 | -0.85 | +0.21 / -1.76 | +1.58 | +0.41 ± 1.76 (53%) |
| down 1+ ATR, closed in the bottom quarter | 142 | +1.63 ± 2.20 | +1.60 ± 2.95 | +3.73 ± 4.38 | -0.4 | 48% | +2.86 ± 4.84 | +3.18 | +4.56 / +2.01 | +1.37 | +3.21 ± 4.33 (44%) |
| gapped down 1+ ATR, closed up from the open | 49 | +1.68 ± 2.29 | -0.08 ± 3.10 | -0.14 ± 3.73 | -0.37 | 47% | +3.10 ± 5.86 | -0.69 | -1.00 / -0.81 | +1.61 | +0.80 ± 3.15 (53%) |

## Reading

- Earnings winners did not keep rising here: reactions of 1+ ATR up ran 0.3-0.9% under the baseline over 5 sessions.
- Earnings drops rebounded: closes 1+ ATR down on the reaction day rose 3.81% ± 2.66 over 5 sessions (median +0.45%, 52% up) against +0.55% for any close; +3.21% with a stop 1 ATR under the entry (41% stopped). The edge was +5.6% in the first half of the dates (Nov 2021 to Apr 2024) and +1.5% in the second, inside the noise.
- Replayed as a sleeve beside the live rules (research/replay/windows-2026-10-09-22-*-earnings*.md): no variant beat the live rules on both the mean and the worst of the 33 hourly windows without losing on the 5-minute windows (paper with no stop: mean +3.0% against +3.1%, worst -21.1% against -24.9%; real book with no stop: mean +2.8% both, worst -10.4% against -11.4%, worse on the 5-minute windows). Not adopted (RUNBOOK 2d).
