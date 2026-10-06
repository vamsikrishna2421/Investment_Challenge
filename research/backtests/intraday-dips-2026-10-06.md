# Intraday dips: buy limits under the open or the prior close (2026-10-06)

61 of 67 radar candidates, hourly bars (last ~2 years), 39,536 sessions. Method: the `scripts/intraday_dip_backtest.py` docstring. Returns % after slippage, ± 95% clustered by date; no stop. "Back" = the session closed at or above the open (or prior close) the dip is measured from.

| Buy limit | Fills | Of sessions | Fill to close | Up at close | Back by the close | Fill to next close | Fill to 3 sessions |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline: buy every open | 39,536 | 100% | -0.34 ± 0.21 | 44% | | +0.02 ± 0.32 | +0.46 ± 0.45 |
| 3% under the open | 17,220 | 44% | -0.56 ± 0.22 | 41% | 17% | -0.12 ± 0.40 | +0.45 ± 0.58 |
| 4% under the open | 12,695 | 32% | -0.58 ± 0.23 | 41% | 12% | -0.10 ± 0.44 | +0.50 ± 0.64 |
| 5% under the open | 9,223 | 23% | -0.61 ± 0.25 | 41% | 9% | -0.13 ± 0.49 | +0.60 ± 0.74 |
| 7% under the open | 4,948 | 13% | -0.51 ± 0.31 | 42% | 5% | -0.01 ± 0.66 | +0.79 ± 0.95 |
| 10% under the open | 1,912 | 5% | -0.44 ± 0.44 | 46% | 3% | +0.27 ± 1.06 | +1.20 ± 1.44 |
| 3% under the prior close | 17,665 | 45% | -0.42 ± 0.24 | 43% | 17% | -0.07 ± 0.41 | +0.40 ± 0.59 |
| 5% under the prior close | 10,400 | 26% | -0.29 ± 0.30 | 44% | 10% | +0.13 ± 0.52 | +0.59 ± 0.74 |
| 10% under the prior close | 2,355 | 6% | +0.24 ± 0.56 | 52% | 4% | +0.74 ± 0.94 | +1.42 ± 1.37 |

**The 4% dip under the open, split**

| Group | Fills | Of sessions | Fill to close | Up at close | Back by the close | Fill to next close | Fill to 3 sessions |
|---|---:|---:|---:|---:|---:|---:|---:|
| filled 9:30-10:30 | 7,038 | 18% | -0.61 ± 0.33 | 42% | 18% | -0.13 ± 0.57 | +0.31 ± 0.81 |
| filled 10:30-12:30 | 3,185 | 8% | -0.60 ± 0.30 | 41% | 8% | -0.26 ± 0.60 | +0.41 ± 0.84 |
| filled 12:30-16:00 | 2,472 | 6% | -0.48 ± 0.17 | 38% | 2% | +0.20 ± 0.46 | +1.13 ± 0.74 |
| company news | 3,416 | 9% | -0.64 ± 0.30 | 41% | 16% | -0.22 ± 0.56 | +0.27 ± 0.78 |
| no company news | 9,279 | 23% | -0.56 ± 0.23 | 41% | 11% | -0.05 ± 0.45 | +0.58 ± 0.66 |
| no news, fill in the support band | 3,077 | 8% | -0.55 ± 0.23 | 40% | 9% | -0.10 ± 0.50 | +0.63 ± 0.75 |
| no news, not at support | 6,202 | 16% | -0.56 ± 0.27 | 41% | 12% | -0.03 ± 0.48 | +0.56 ± 0.70 |
| SPY down 1%+ that session | 2,039 | 5% | -2.59 ± 0.61 | 22% | 5% | -1.51 ± 1.45 | -0.88 ± 2.15 |
| SPY not down 1% | 10,656 | 27% | -0.20 ± 0.22 | 45% | 14% | +0.17 ± 0.44 | +0.76 ± 0.64 |
| ATR under 6% of the price | 1,735 | 4% | -0.35 ± 0.18 | 41% | 5% | +0.01 ± 0.38 | +0.40 ± 0.59 |
| ATR 6%+ of the price | 10,960 | 28% | -0.62 ± 0.25 | 41% | 13% | -0.12 ± 0.48 | +0.51 ± 0.69 |
