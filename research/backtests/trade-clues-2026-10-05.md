# Support-limit trades one by one: exits and clues (2023-12-19 to 2026-10-05)

2555 limit fills on 621 sessions (hourly bars). Under the live exit (stop 0.6 ATR under support, sell at the sell-zone bottom) 1421 (56%) were stopped within 3 sessions. Method and caveats: `scripts/trade_clues.py` docstring. ± is a 95% interval clustered by entry date.

## Exits on the same entries

| Exit | Average a trade | Median | Winners | Stopped | Sessions held | Average a session held |
|---|---:|---:|---:|---:|---:|---:|
| plan | +0.39 ± 0.67% | -4.03% | 21% | 79% | 5.0 | +0.077% |
| pct 3 | -0.17 ± 0.31% | -0.95% | 49% | 51% | 1.8 | -0.095% |
| pct 5 | -0.12 ± 0.36% | -2.92% | 40% | 60% | 2.3 | -0.053% |
| pct 8 | -0.14 ± 0.42% | -3.34% | 32% | 68% | 2.8 | -0.051% |
| pct 12 | +0.04 ± 0.49% | -3.64% | 27% | 73% | 3.4 | +0.012% |
| r 1 | -0.15 ± 0.37% | -2.84% | 42% | 58% | 2.2 | -0.066% |
| r 1.5 | +0.02 ± 0.42% | -3.28% | 36% | 64% | 2.6 | +0.006% |
| r 2 | +0.05 ± 0.47% | -3.52% | 32% | 68% | 3.0 | +0.018% |
| be | +0.05 ± 0.51% | -1.64% | 13% | 49% | 3.5 | +0.013% |
| time 3 | -0.12 ± 0.44% | -2.78% | 35% | 56% | 2.3 | -0.050% |

## Clues at entry: what the quick stop-outs had in common

First half 2023-12-19 to 2025-06-18 (1060 trades), second half 2025-06-18 to 2026-10-05 (1495). Quick stop: stopped within 3 sessions under the plan exit. Each cell: quick-stop rate, then the plan exit's average return.

| Clue | Tercile | First half: quick stops / return | Second half: quick stops / return | Same direction |
|---|---|---|---|---|
| open against the prior close, ATR | low (< -0.205) | 63% / -0.23% (n=353) | 64% / +0.26% (n=568) | yes, z -3.7 |
|  | mid | 50% / +0.11% (n=353) | 51% / +1.36% (n=490) |  |
|  | high (>= 0.0091) | 49% / +0.03% (n=354) | 55% / +0.47% (n=437) |  |
| entry against the prior close, ATR | low (< -0.432) | 62% / -0.21% (n=353) | 58% / +0.57% (n=606) | yes, z -2.8 |
|  | mid | 53% / +0.93% (n=353) | 56% / +0.60% (n=449) |  |
|  | high (>= -0.216) | 46% / -0.81% (n=354) | 56% / +0.91% (n=440) |  |
| S&P 500 (SPY) at the fill bar's start against its prior close, % | low (< -0.345) | 60% / -0.75% (n=349) | 59% / +0.40% (n=446) | yes, z -2.5 |
|  | mid | 56% / -0.21% (n=356) | 59% / -0.19% (n=472) |  |
|  | high (>= 0.072) | 45% / +0.85% (n=355) | 54% / +1.61% (n=577) |  |
| SPY prior close against its 20-day average, % | low (< 0.066) | 56% / -0.97% (n=351) | 53% / +0.73% (n=519) | no, z +0.5 |
|  | mid | 50% / +0.25% (n=354) | 60% / +0.03% (n=597) |  |
|  | high (>= 1.62) | 55% / +0.62% (n=355) | 58% / +1.64% (n=379) |  |
| SPY over the 5 sessions before, % | low (< -0.267) | 51% / +0.39% (n=352) | 58% / +0.11% (n=574) | no, z -0.1 |
|  | mid | 58% / -1.00% (n=348) | 57% / +1.37% (n=495) |  |
|  | high (>= 1.17) | 52% / +0.49% (n=360) | 56% / +0.65% (n=426) |  |
| stock's prior close against its 20-day average, % | low (< -6.5) | 47% / +0.30% (n=353) | 51% / +2.02% (n=463) | yes, z +4.1 |
|  | mid | 53% / -1.20% (n=353) | 57% / +0.23% (n=521) |  |
|  | high (>= 2.03) | 62% / +0.80% (n=354) | 62% / -0.08% (n=511) |  |
| stock's prior close against its 50-day average, % | low (< -7.91) | 49% / +0.77% (n=353) | 54% / +1.26% (n=536) | yes, z +2.4 |
|  | mid | 54% / -0.29% (n=353) | 56% / +0.02% (n=525) |  |
|  | high (>= 6.84) | 58% / -0.58% (n=354) | 62% / +0.76% (n=434) |  |
| stock over the 20 sessions before, % | low (< -8.81) | 53% / -1.00% (n=353) | 56% / +0.60% (n=513) | yes, z +1.0 |
|  | mid | 55% / +0.79% (n=353) | 55% / +0.79% (n=532) |  |
|  | high (>= 8.16) | 54% / +0.12% (n=354) | 60% / +0.64% (n=450) |  |
| stock over the 5 sessions before, ATR | low (< -0.78) | 48% / +0.30% (n=353) | 52% / +1.53% (n=525) | yes, z +4.6 |
|  | mid | 51% / +0.74% (n=353) | 54% / +1.05% (n=504) |  |
|  | high (>= 0.427) | 62% / -1.13% (n=354) | 65% / -0.68% (n=466) |  |
| stock minus SPY over the 20 sessions before, % | low (< -8.7) | 50% / -0.78% (n=353) | 55% / +0.90% (n=548) | yes, z +1.8 |
|  | mid | 55% / +0.78% (n=353) | 55% / +0.83% (n=486) |  |
|  | high (>= 6.22) | 56% / -0.09% (n=354) | 61% / +0.26% (n=461) |  |
| ATR as % of the price | low (< 6.89) | 61% / +0.28% (n=353) | 59% / +0.09% (n=637) | yes, z -3.9 |
|  | mid | 57% / +0.06% (n=353) | 57% / +0.92% (n=578) |  |
|  | high (>= 9.87) | 44% / -0.43% (n=354) | 53% / +1.52% (n=280) |  |
| prior day's close location in its range (0 = at the low, 1 = at the high) | low (< 0.222) | 51% / -0.13% (n=352) | 50% / +2.29% (n=426) | yes, z +2.2 |
|  | mid | 53% / +0.05% (n=354) | 61% / +0.05% (n=565) |  |
|  | high (>= 0.611) | 57% / -0.01% (n=354) | 58% / +0.02% (n=504) |  |
| prior day's volume against its 20-day average | low (< 0.699) | 47% / -0.17% (n=353) | 52% / +1.26% (n=417) | yes, z +3.0 |
|  | mid | 54% / +0.26% (n=353) | 59% / -0.25% (n=604) |  |
|  | high (>= 1.03) | 60% / -0.17% (n=354) | 58% / +1.35% (n=474) |  |
| swings in the support zone (times tested) | low (< 3) | 55% / +0.60% (n=312) | 57% / +0.62% (n=415) | yes, z -0.5 |
|  | mid | 52% / -0.04% (n=323) | 58% / +0.58% (n=455) |  |
|  | high (>= 5) | 54% / -0.48% (n=425) | 56% / +0.80% (n=625) |  |
| sessions since the price last touched the buy zone | low (< 1) | - | - | no, z +nan |
|  | mid | 50% / +0.45% (n=665) | 57% / +0.72% (n=976) |  |
|  | high (>= 3) | 59% / -0.84% (n=395) | 57% / +0.60% (n=519) |  |
| prior close above support, ATR | low (< 0.161) | 51% / -0.29% (n=353) | 61% / +0.57% (n=450) | no, z -0.3 |
|  | mid | 54% / +0.04% (n=353) | 55% / +1.04% (n=449) |  |
|  | high (>= 0.386) | 56% / +0.16% (n=354) | 56% / +0.49% (n=596) |  |
| R:R from the limit | low (< 3.43) | 56% / +0.24% (n=353) | 56% / +0.77% (n=542) | no, z +0.0 |
|  | mid | 52% / +1.34% (n=353) | 56% / +0.01% (n=418) |  |
|  | high (>= 4.54) | 53% / -1.67% (n=354) | 58% / +1.12% (n=535) |  |
| entry to the sell-zone bottom, ATR | low (< 2.08) | 55% / +0.58% (n=353) | 54% / +0.66% (n=502) | no, z +0.9 |
|  | mid | 52% / +1.09% (n=353) | 58% / +0.33% (n=458) |  |
|  | high (>= 2.79) | 54% / -1.75% (n=354) | 59% / +1.00% (n=535) |  |
| share of radar names under their prior close at the fill bar's start | low (< 0.476) | 46% / +0.93% (n=353) | 57% / +0.95% (n=459) | yes, z +2.0 |
|  | mid | 55% / +0.10% (n=353) | 55% / +1.07% (n=570) |  |
|  | high (>= 0.85) | 60% / -1.11% (n=354) | 59% / -0.06% (n=466) |  |
| radar limits filled the same session | low (< 3) | 41% / +1.51% (n=187) | 50% / +2.54% (n=137) | yes, z +3.5 |
|  | mid | 55% / +0.55% (n=504) | 57% / +0.79% (n=432) |  |
|  | high (>= 6) | 59% / -1.60% (n=369) | 58% / +0.36% (n=926) |  |

## Clues that held in both halves (|z| >= 2)

- stock over the 5 sessions before, ATR: quick stops 51% in the low tercile (< -0.78) against 64% in the high tercile (>= 0.427), z +4.6
- stock's prior close against its 20-day average, %: quick stops 49% in the low tercile (< -6.5) against 62% in the high tercile (>= 2.03), z +4.1
- ATR as % of the price: quick stops 60% in the low tercile (< 6.89) against 48% in the high tercile (>= 9.87), z -3.9
- open against the prior close, ATR: quick stops 64% in the low tercile (< -0.205) against 52% in the high tercile (>= 0.0091), z -3.6
- radar limits filled the same session: quick stops 45% in the low tercile (< 3) against 58% in the high tercile (>= 6), z +3.5
- prior day's volume against its 20-day average: quick stops 50% in the low tercile (< 0.699) against 59% in the high tercile (>= 1.03), z +3.0
- entry against the prior close, ATR: quick stops 60% in the low tercile (< -0.432) against 51% in the high tercile (>= -0.216), z -2.8
- S&P 500 (SPY) at the fill bar's start against its prior close, %: quick stops 59% in the low tercile (< -0.345) against 50% in the high tercile (>= 0.072), z -2.5
- stock's prior close against its 50-day average, %: quick stops 52% in the low tercile (< -7.91) against 60% in the high tercile (>= 6.84), z +2.4
- prior day's close location in its range (0 = at the low, 1 = at the high): quick stops 51% in the low tercile (< 0.222) against 58% in the high tercile (>= 0.611), z +2.2
- share of radar names under their prior close at the fill bar's start: quick stops 52% in the low tercile (< 0.476) against 59% in the high tercile (>= 0.85), z +2.0
