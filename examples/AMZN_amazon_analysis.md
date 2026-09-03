# Amazon.com (NASDAQ: AMZN) — analysis notes

Third ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py). Same
structure as the [CBRS](./CBRS_cerebras_analysis.md) and [NNE](./NNE_nano_nuclear_analysis.md)
notes. AMZN plays a different role from the other two: it is the **control ticker** for the
pipeline — deep, liquid and close to efficiently priced, so it is the series where a forecast
harness should show roughly *no* skill. If it shows a lot, the harness is broken.

Compiled 2026-09-03 from public sources (linked at the bottom). Aggregator figures disagree in
places — verify against the 10-Q and a live quote. **Research notes, not investment advice.**

## 1. Where the business is

Q2 2026 (quarter ended June 30, reported 2026-07-30):

| | Q2 2026 |
|---|---|
| Net sales | **$200.6B**, +20% YoY |
| Operating income | **$27.5B**, +43% YoY — 13.7% margin vs 11.4% |
| AWS net sales | **$42.2B, +36.7% YoY** — fastest in 18 quarters, 5th straight acceleration |
| AWS run rate / backlog | ~$169B annualized / **$496B** backlog, growing triple digits |
| GAAP EPS | **$5.75** |
| Adjusted EPS | **$1.97** vs $1.82 expected |
| Cash capex | $53.1B in the quarter; FY26 guided to **~$220B** (raised from ~$200B) |

Q3 2026 guidance: net sales **$197–202B**, operating income **$22.5–26.5B** — a midpoint ~11%
*below* Q2's $27.5B on flat-to-lower sales. Management is telling you margins compress from
here as depreciation on the capex cycle lands.

## 2. The bottom line is not the bottom line

The single most important thing about AMZN's current earnings is that **GAAP EPS is inflated by
a non-operating mark**. Q2's $5.75 includes a **$53.4B gain on the Anthropic investment**;
Q1 2026 included a $16.8B pre-tax gain from the same source. Adjusted EPS was $1.97.

That flows straight into the headline multiple. Working backwards from a ~$2.75T market cap and
a quoted ~20.5x P/E implies ~$134B of trailing net income. Strip roughly $70B of pre-tax
Anthropic marks (~$53–55B after tax) and trailing earnings are nearer **$79–81B — a P/E in the
mid-30s, not ~20x**. Treat the screen number as broken until the marks roll off.

The mirror image of the inflated profit line is the cash line:

- Trailing free cash flow went from ~$26B → $1.2B → **negative $7.6B**, even as operating cash
  flow rose ~33%. The entire gap is AI capex.
- FY26 capex of ~$220B is **roughly double** Q2 operating income annualized (~$110B).

So the honest one-line summary of Amazon right now: **the operating business is accelerating,
the reported profit is flattered by a paper gain, and the cash is going into the ground.**

## 3. P/E comparisons — and why the screen number is wrong

Every low P/E currently quoted for AMZN is contaminated by the Anthropic marks. Two independent
routes agree on the clean number:

- **Ex-gain arithmetic:** ~$2.75T cap at the quoted ~20.5x implies ~$134B trailing net income;
  removing ~$70.2B of pre-tax Anthropic gains (~$53–55B after tax) leaves ~$79–81B, i.e.
  **~34x**.
- **Sanity check against a clean year:** 2025 actual EPS of $7.17 against a ~$255 price is
  **~35.6x**.

| | Trailing P/E | Forward P/E | Note |
|---|---|---|---|
| **AMZN as quoted** | ~20.5x | ~20.4x | both distorted by investment marks |
| **AMZN, clean** | **~34x** | **~33x** on 2026E ($7.73), **~27x** on 2027E ($9.40) | use these |
| Apple | 36.2x | 32.9x | Aug 31 2026 |
| Meta | — | 33.1x | |
| Alphabet | ~32x | — | *also* holds Anthropic; its trailing figure is likely flattered too |
| Microsoft | 27.4x | 24.9x | Aug 31 2026 |
| Nvidia | — | <23x | different fiscal calendar; fastest earnings growth |
| S&P 500 | — | 23.6x | index reference |

What falls out of the table:

1. **AMZN is not a ~20x stock.** On a clean basis it sits in the low-to-mid 30s alongside Apple,
   Meta and Alphabet — a premium cohort — and well above Microsoft, Nvidia and the index.
2. **The Alphabet comparison is closer than it looks.** Alphabet carries the same Anthropic
   mark-to-market distortion, so its clean multiple is *higher* than the quoted ~32x. AMZN vs
   GOOGL on like-for-like earnings is roughly a wash, not a discount.
3. **Only the 2027 line makes AMZN look reasonable** (~27x on $9.40 consensus EPS), and that
   requires the ~$220B capex cycle to convert into earnings on schedule.
4. **Versus its own history it is unremarkable:** 31.7x at end-2025, 34.7x trailing / 32.1x
   forward in April 2026. Today's ~34x is mid-range for the last two years, not stretched.

**Caveat on the tool itself.** P/E is a poor lens for AMZN in this particular cycle. Depreciation
from ~$220B of capex is about to compress the E for several years, while free cash flow — the
usual fallback — is already negative, so FCF multiples fail too. The defensible comparisons here
are EV/EBITDA, or P/E on 2027 once the depreciation is inside the run rate. Any screen ranking
mega-caps by trailing P/E right now is ranking accounting artifacts: a one-off investment gain
inflates E and *lowers* the printed multiple, making the most distorted company look cheapest.

## 4. What the tape says (2026-09-02)

- ~**$255**, market cap ~**$2.75T**. 52-week range **$196.00–$287.20** — about **11% below the
  high** and **30% above the low**. This is a normal mega-cap drawdown, not a broken chart.
- The market has consistently looked through the FCF collapse, treating capex as AWS-cycle
  investment rather than value destruction. That is a *judgment*, and it is the thing that would
  reverse hardest if AWS growth decelerates while depreciation keeps rising.

**The bull and bear cases hinge on the same number.** AWS at +36.7% with a $496B backlog
justifies the spend; the same spend at +20% AWS growth would not. Watch the backlog conversion
rate and the operating-margin guide, not the EPS headline.

## 5. What Kronos can and cannot add here

AMZN is the opposite modeling problem from CBRS and NNE:

- **Data is not the constraint.** Nearly three decades of daily bars, far beyond the 512-bar
  context. Intraday bars are available and deeply liquid.
- **Efficiency is the constraint.** A $2.75T name with this much analyst and algorithmic
  coverage is about as close to a random walk as US equities get. The realistic expectation is
  `rmse_skill_vs_baseline` **near zero or negative** — the flat last-close baseline is very hard
  to beat.

That makes AMZN the right **calibration ticker** for this repo's pipeline, and the notes here
recommend running it as such:

- If the holdout shows large positive skill on AMZN, suspect a bug (lookahead in the split, a
  mis-aligned index, or a horizon that overlaps the context) before believing it.
- `p10_p90_coverage` near 0.80 on AMZN is the evidence that the ensemble bands are honest. Once
  that holds on a well-behaved series, coverage numbers on CBRS and NNE mean something.
- Where the model plausibly *does* add value on a name like this is **volatility, not
  direction**: `forecast_vol_ann` and the band width are the outputs worth reading.

Earnings dates are the one structural caveat: a quarterly print inside the forecast horizon is a
scheduled jump the price series cannot anticipate. Either keep the horizon inside an
inter-earnings window or expect the realized path to breach the bands on that one day.

## 6. Running it

```shell
# 21 sessions ahead on ~5 years of daily bars
python examples/cbrs_cerebras_analysis.py --ticker AMZN --start 2021-01-01 \
    --pred-len 21 --n-paths 64 --outdir amzn_output

# calibration check: does the harness beat a flat baseline on an efficient name?
# (expected answer: no — that is the point)
python examples/cbrs_cerebras_analysis.py --ticker AMZN --start 2015-01-01 \
    --lookback 512 --pred-len 21 --n-paths 128 --outdir amzn_output
```

## Sources

- [Amazon Q2 2026 earnings release](https://www.aboutamazon.com/news/company-news/amazon-earnings-q2-2026-report)
- [Form 10-Q, quarter ended 2026-06-30](https://www.sec.gov/Archives/edgar/data/0001018724/000101872426000026/amzn-20260630.htm)
- [CNBC — Q2 2026 earnings report](https://www.cnbc.com/2026/07/30/amazon-amzn-q2-earnings-report-2026.html)
- [Webull — Q2 2026 recap, AWS +37%](https://www.webull.com/blog/242-Amazon-AMZN-Q2-2026-Earnings-Recap)
- [Beancount.io — the $53B Anthropic gain and reported profit](https://beancount.io/blog/2026/07/31/amazon-fy2026-q2-earnings-analysis)
- [Motley Fool — FCF negative $7.6B on record capex](https://www.fool.com/investing/2026/08/23/amazons-free-cash-flow-went-negative-by-76-billion/)
- [GeekWire — AWS booming, FCF turns negative](https://www.geekwire.com/2026/aws-is-booming-but-amazons-free-cash-flow-turns-negative-on-record-ai-spending/)
- [TheNextWeb — Q1 2026 Anthropic gain, FCF down 95%](https://thenextweb.com/news/amazon-q1-2026-anthropic-aws-earnings)
- [Investing.com — AMZN quote](https://www.investing.com/equities/amazon-com-inc)
- [MarketBeat — AMZN forecast](https://www.marketbeat.com/stocks/NASDAQ/AMZN/forecast/)
- [GuruFocus — AMZN forward P/E](https://www.gurufocus.com/term/forward-pe-ratio/AMZN) and
  [AAPL forward P/E](https://www.gurufocus.com/term/forward-pe-ratio/AAPL)
- [stockanalysis.com — MSFT statistics](https://stockanalysis.com/stocks/msft/statistics/)
- [TIKR — Amazon P/E history and 2026/2027 EPS consensus](https://www.tikr.com/blog/amazon-pe-ratio)
- [financecharts — AAPL P/E history](https://www.financecharts.com/stocks/AAPL/value/pe-ratio)
- [Nasdaq — cheapest trillion-dollar stock comparison](https://www.nasdaq.com/articles/cheapest-trillion-dollar-stock-nvidia-microsoft-apple-amazon-alphabet-or-meta)
