# Replay windows: 30 windows of 30 sessions ending 2026-08-26 to 2026-10-07, 5-minute bars

$1,000 each window. S&P 500 over the same windows: median +1.3%, -2.2% to +4.7%. The windows overlap, so they are not independent tests: the spread shows how much the start date moves the result.

| Rules | Median return | Mean | Worst window | Best window | Beat the S&P 500 | Doubled ($2,000) | Closed trades per window |
|---|---:|---:|---:|---:|---:|---:|---:|
| Live real-book rules (S&P gate, 1% gap allowance) | -2.9% | -1.5% | -8.9% | +10.3% | 7/30 | 0/30 | 9 |
| Real book + breadth gate 0.3 | -2.9% | -1.5% | -8.9% | +10.3% | 7/30 | 0/30 | 10 |
| Real book + breadth gate 0.5 | -2.9% | -1.5% | -8.9% | +10.3% | 7/30 | 0/30 | 9 |
| Real book + breadth gate 0.75 | -2.9% | -1.5% | -8.9% | +10.3% | 7/30 | 0/30 | 9 |
| Real book + no entry 1+ ATR down while SPY is up | -2.9% | -1.5% | -8.9% | +10.3% | 7/30 | 0/30 | 9 |
| Real book, run buys in the last half hour instead of limits | +0.8% | +1.5% | -12.1% | +21.4% | 15/30 | 0/30 | 12 |
| Real book, last half hour + breadth gate 0.5 | +0.7% | +1.2% | -10.7% | +15.1% | 10/30 | 0/30 | 11 |
