# How AI is used in trading, and what it means for this challenge (2026-10-10)

Vamsi's question: research how people use AI effectively in trading, see if we can learn anything, and answer
straight whether any strategy makes profits.

## What the evidence says

Where AI has a measured edge: reading text.
- News headlines: GPT-4 scores of headlines published after its training cutoff matched the same-day price move
  about 90% of the time, a move nobody can trade, and also predicted the drift that followed, most for small
  stocks and bad news. The strategy's returns fell as LLM use spread (Lopez-Lira and Tang, latest revision
  Oct 2025: [arXiv 2304.07619](https://arxiv.org/abs/2304.07619v6)). The first version's "500%" was before costs
  and before others caught on.
- Financial statements: GPT-4 given anonymized statements called the direction of next year's earnings about 60%
  of the time, ahead of analysts, and a long-short portfolio on it earned double-digit annual alpha in the
  backtest (Kim, Muhn and Nikolaev, Chicago Booth working paper:
  [summary](https://www.chicagobooth.edu/research/fama-miller/finance-research/funding/a-demand-system-approach-for-fixed-income/financial-statement-analysis-with-large-language-models)).
- Earnings calls: retail trades lined up with AI-read call sentiment after ChatGPT's release, and less so during
  ChatGPT outages; no evidence that it made those traders richer
  ([WashU Olin](https://olin.washu.edu/about/news-and-media/news/2025/04/chatgpt-level-playing-field-retail-investors.php)).

Where it fails: trading on its own.
- Alpha Arena season 1 (Oct 18 to Nov 3, 2025; six LLMs, $10,000 each in real money, crypto): Qwen3 Max +22%,
  DeepSeek +5%, Claude -31%, Grok -45%, Gemini -57%, ChatGPT -63%. Every model won only 25-30% of its trades; fees
  from over-trading ate the gains (Gemini made 238 trades); the organizer said LLMs handle numeric price series
  poorly ([Protos](https://protos.com/llm-crypto-trading-contest-finds-llms-cant-trade-crypto/)).
- Contamination-free stock benchmarks: most LLM agents failed to beat buy-and-hold, and none did in a downturn
  ([StockBench](https://www.catalyzex.com/paper/stockbench-can-llm-agents-trade-stocks),
  [LiveTradeBench](https://arxiv.org/html/2511.03628v1)).
- Look-ahead bias: an LLM backtested on dates it was trained on knows what happened next; memorization inflates
  the apparent skill ([Glasserman and Lin](https://www.alphaxiv.org/abs/2309.17322v1),
  [Gao, Jiang and Yan](https://arxiv.org/html/2512.23847v1)).

How the big funds use it: as a research engine with humans deciding. Man Group's AlphaGPT proposes signals, writes
the code and backtests them for human approval; Bridgewater runs an ML-led fund since July 2024; Ken Griffin said
in Oct 2025 that generative AI had not yet meaningfully improved hedge-fund returns
([AI Street](https://www.ai-street.co/p/how-hedge-funds-and-market-makers),
[Founderland](https://www.founderland.ai/articles/the-race-to-build-fully-autonomous-ai-hedge-funds-mq6jgzt7)).

Base rate for active retail trading: in Brazil 97% of those who day-traded 300+ days lost money; in Taiwan under 1%
earned predictable profits after fees ([CNBC](https://www.cnbc.com/2020/11/20/attention-robinhood-power-users-most-day-traders-lose-money.html)).

## What we tested from it

- Candle patterns (Vamsi's question, the opposite of AI's strength: shapes in a price series): no edge on hourly
  or daily bars, radar names or large caps (`research/backtests/candles-2026-10-10*.md`).
- Post-earnings drift (the event the text-reading results trade, and Q3 reports fall inside the window;
  `research/backtests/earnings-drift-2026-10-10*.md`): radar names' earnings drops of 1+ ATR rebounded +3.8% in 5
  sessions over 5 years, but +1.5% since April 2024, inside the noise; large caps drift the textbook way (+0.6%
  after a 2+ ATR jump). Replayed beside the live rules it did not beat them (`research/replay/windows-2026-10-09-22-*-earnings*.md`): not adopted.
- Already in the rules and consistent with the research: an LLM reads every holding's and radar name's news at each
  run and an offering or material bad news cancels the entry (2a; dilution dips fell a further 1.1% in 3 sessions);
  stops and caps on trades per day; no leverage.

## Lessons

1. Use AI for what it is measured to do: read filings and news fast and flag bad news; never let it guess the
   next candle.
2. An edge in a backtest has to survive costs, both halves of the data and a replay of the whole book; most do not
   (this week: candles, earnings dips).
3. Edges decay once people trade them (headline sentiment, the earnings-dip rebound).
4. Over-trading is how the LLM traders lost; few trades with defined risk is the opposite.
