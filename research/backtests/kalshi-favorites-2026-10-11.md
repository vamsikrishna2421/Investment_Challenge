# Buying prediction-market favorites, 2026-10-11

Kalshi markets settled 2026-08-12 to 2026-10-11: 2737 sampled from 23 series, 2454 with usable hourly quotes. Method in the `scripts/favorites_backtest.py` docstring. Returns % of the money staked per contract held to settlement; 'net' after Robinhood's 1 cent and Kalshi's fee; ± 95% clustered by settlement date. Break-even is the win rate that returns zero after fees.

## The 87-92 cent strategy

| group | trades | won | break-even | avg price | return gross | return net | worst trade | 168 straight wins |
|---|---|---|---|---|---|---|---|---|
| all | 764 | 86.1% | 91.1% | 0.895 | -3.75 ± 2.39 | -5.50 ± 2.34 | -100.0% | 1.27e-11 |
| sports | 268 | 85.4% | 90.9% | 0.892 | -4.21 ± 4.32 | -5.98 ± 4.24 | -100.0% | 3.36e-12 |
| weather | 382 | 87.7% | 91.2% | 0.896 | -2.09 ± 3.24 | -3.86 ± 3.18 | -100.0% | 2.64e-10 |
| economic releases | 26 | 88.5% | 90.9% | 0.892 | -0.90 ± 22.91 | -2.73 ± 22.47 | -100.0% | 1.13e-09 |
| crypto and index | 88 | 80.7% | 91.6% | 0.900 | -10.39 ± 7.25 | -11.98 ± 7.11 | -100.0% | 2.18e-16 |

## Calibration: the favorite 24 hours before the close

| price band | markets | won | break-even | return gross | return net |
|---|---|---|---|---|---|
| 0.50-0.60 | 461 | 54.7% | 57.8% | -0.20 ± 7.57 | -4.95 ± 7.21 |
| 0.60-0.70 | 469 | 61.4% | 66.7% | -4.15 ± 7.27 | -7.91 ± 6.99 |
| 0.70-0.80 | 517 | 69.2% | 77.3% | -7.65 ± 5.27 | -10.42 ± 5.11 |
| 0.80-0.87 | 249 | 81.9% | 84.8% | -1.09 ± 5.89 | -3.41 ± 5.75 |
| 0.87-0.92 | 173 | 87.3% | 90.7% | -2.03 ± 6.74 | -3.84 ± 6.62 |
| 0.92-0.97 | 196 | 92.9% | 95.4% | -1.24 ± 3.70 | -2.68 ± 3.64 |
| 0.97-1.00 | 389 | 99.2% | 99.6% | +0.72 ± 0.88 | -0.39 ± 0.86 |

## Reading

- The 87-92 cent strategy lost: 764 trades in 60 days won 86.1% of the time against the 91.1% needed after fees; -3.8% a trade before fees and -5.5% after (± 2.3), negative in every group (crypto and index -12%). At an 86% win rate the chance of 168 straight wins is about 1 in 80 billion.
- Calibration: bought at the ask 24 hours before the close, favorites from 50 to 97 cents won slightly less often than their price; only 97-100 cents broke even before fees (+0.7%) and lost after them (-0.4%). The favorite-longshot bias Burgi, Deng and Whelan measured over 2021-2025 does not pay a buyer at the ask in this sample; their paper notes the bias is shrinking.
- Verdict: no trade. An edge would need a forecast better than the market's, proven on 30+ questions before any money (RUNBOOK 1g, forecasts.py).
