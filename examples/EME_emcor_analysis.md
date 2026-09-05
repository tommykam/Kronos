# EMCOR Group (NYSE: EME) — analysis notes

Eleventh ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py). Compiled
2026-09-04 from public sources. **Research notes, not investment advice.**

Read this together with the [STRL notes](./STRL_sterling_infrastructure_analysis.md) and the
[AMZN notes](./AMZN_amazon_analysis.md). All three are the same AI-infrastructure capex trade
seen from different positions: Amazon spends the money, Sterling and EMCOR receive it. The
comparison in §4 is the point of this file.

## 1. Q2 2026 (reported 2026-07-30) — a clean beat and raise

| | Q2 2026 |
|---|---|
| Revenue | **$5.15B, +19.8% YoY** (organic **+19.6%**) |
| Diluted EPS | **$9.06** vs $7.23 consensus |
| RPO (backlog) | record **$17.14B** |

FY2026 guidance raised to revenue **$20.0–20.5B** and diluted EPS **$32.00–33.25**.

Like Sterling, EMCOR is a company whose bottom line is simply the business — no marks, no
adjustment gymnastics. Two details are worth more than the headline:

- **The growth is organic.** Total revenue +19.8% against organic +19.6% means acquisitions
  contributed almost nothing to the quarter, despite five recent deals ($625M revenue and $105M
  EBITDA on a trailing-12-month basis, with $250–275M of contribution embedded in guidance).
  M&A is additive here, not load-bearing.
- **The demand thesis is quantified.** Management states that AI data centres require a
  **1.5x–2x multiplier** in mechanical and electrical content versus traditional facilities. That
  is the cleanest single articulation of why electrical and mechanical contractors are levered to
  AI capex rather than merely adjacent to it.

## 2. The detail buried in the backlog

Record RPO of $17.14B is the headline. The disclosure underneath it matters more: **only ~75–76%
of RPO is now expected to convert to revenue within 12 months, down from a historical ~85%**,
because projects are larger and mobilisation timelines longer.

That is roughly **$1.6B of revenue pushed beyond the twelve-month window** relative to the old
conversion rate. Headline RPO growth therefore **overstates near-term revenue growth**. It is not
a demand problem — bigger projects are a sign of winning larger work — but anyone modelling
forward revenue off backlog growth without adjusting the conversion rate will be too optimistic.

## 3. Valuation and capital returns

- **$754.16** (Sep 4, 2026), market cap **~$33.27B** on ~44.1M shares.
- 52-week range **$564.92 – $951.96** — a 1.69x span, **~21% below the high**, ~34% above the low.
- **~23.1x** FY26 guided EPS at the $32.62 midpoint (trailing P/E ~23.5x); **~1.64x** sales.
- RPO is **0.85x** guided annual revenue.

**Capital returns are a real part of the story, unlike anywhere else in this series.** EMCOR
raised its dividend and added **$500M** to the buyback authorisation; since July 2022 it has
repurchased **4.39M shares — about 9.3% of the company — for $1.31B**. A shrinking share count
compounds EPS independently of operations, which is precisely what none of the speculative names
in this collection can do (most are diluting instead).

## 4. STRL vs EME — the same trade, two very different instruments

| | **STRL** | **EME** |
|---|---|---|
| Price / market cap | $519.51 / $17.35B | $754.16 / $33.27B |
| FY26 revenue | $4.0–4.15B | **$20.0–20.5B** (5x larger) |
| Q2 revenue growth | **+90%** | +19.8% |
| Forward P/E | 26.0x adj / 29.6x GAAP | **23.1x** |
| Price / sales | 4.3x | **1.64x** |
| Backlog ÷ annual revenue | **1.37x** | 0.85x |
| Drawdown from 52-wk high | **−48%** | −21% |
| 52-week range span | 3.8x | 1.7x |
| Capital returns | — | dividend + buyback (−9.3% shares since 2022) |

The two express the same view with opposite risk profiles:

- **STRL** is the high-beta expression — far faster growth, higher backlog coverage, a richer
  multiple, and a chart that has halved from its high. You are paid more if data-centre
  construction runs hot, and punished harder if it does not.
- **EME** is the lower-beta expression — five times the revenue, a cheaper multiple, more
  diversified end markets, shareholder cash returns, and roughly half the drawdown.

**They are not diversification.** Both depend on the same hyperscaler capex cycle; holding both
concentrates that exposure rather than spreading it. If the question is "how do I own AI
infrastructure build-out," the honest answer is to pick a position size for the *theme* first and
then choose the instrument by how much volatility you want, not to hold both and call it balance.

## 5. Modelling notes

Together with AMZN and HNST, EME is among the better-behaved series in this collection:

- Long trading history, $33B cap, deep liquidity, no dilution overhang, no foreign-session gaps.
- Volatility is materially lower than STRL's — a 1.7x annual range against 3.8x — so ensemble
  bands should be tighter and `p10_p90_coverage` has a better chance of landing near 0.80.
- The **buyback is a slow structural drift** in the share count that price bars capture only
  indirectly. It does not break anything, but per-share dynamics are not purely market-driven.
- The earnings-date caveat from the STRL and AMZN notes applies unchanged: keep the horizon
  inside an inter-earnings window or expect one band breach.

Running EME and STRL through the pipeline **as a pair** is the more interesting experiment than
either alone: same underlying driver, very different volatility, so it tests whether the ensemble
widths scale sensibly with realised risk rather than just tracking each name's recent range.

```shell
python examples/cbrs_cerebras_analysis.py --ticker EME --start 2015-01-01 \
    --pred-len 21 --n-paths 128 --outdir eme_output
```

## Sources

- [Motley Fool — EMCOR Q2 2026 earnings call transcript](https://www.fool.com/earnings/call-transcripts/2026/08/03/emcor-eme-q2-2026-earnings-call-transcript/)
- [Investing.com — Q2 2026 beat and raised guidance](https://www.investing.com/news/transcripts/earnings-call-transcript-emcor-q2-2026-beats-estimates-raises-guidance-93CH-4825605)
- [BigGo — Q2 revenue $5.15B, record $17.14B RPO](https://finance.biggo.com/news/US_EME_2026-07-30)
- [Globe and Mail — Q2 deep dive, data centres and acquisitions](https://www.theglobeandmail.com/investing/markets/stocks/EME/pressreleases/3580733/eme-q2-deep-dive-data-center-demand-and-strategic-acquisitions-drive-growth/)
- [Simply Wall St — Q2 beat, raised guidance, record backlog](https://simplywall.st/stocks/us/capital-goods/nyse-eme/emcor-group/news/should-emcors-strong-q2-beat-raised-guidance-and-record-back)
- [Investing.com — dividend raise and $500M buyback addition](https://www.investing.com/news/company-news/emcor-to-raise-quarterly-dividend-and-adds-500-million-to-buyback-plan-93CH-4415187)
- [stockanalysis.com — EME statistics](https://stockanalysis.com/stocks/eme/statistics/)
