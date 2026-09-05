# Dominari Holdings (NASDAQ: DOMH) — analysis notes

Ninth ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py). Compiled
2026-09-04 from public sources. **Research notes, not investment advice.**

The smallest company in the series by an order of magnitude — a **~$66–71M micro-cap on ~22.6M
shares**. Data quality is correspondingly thin, and two figures below are inferred rather than
sourced; both are flagged.

## 1. What it is

Dominari operates wealth management, investment banking, sales and trading, and asset management
through **Dominari Financial / Dominari Securities**, alongside a **"Legacy AIkido"** segment —
the remains of AIkido Pharma, the pharmaceutical company this ticker used to be.

Two things drive the equity story far more than the brokerage does:

- **Donald Trump Jr. and Eric Trump joined the advisory board in February 2025** and together
  hold about **12%** of the stock. The shares rose ~1,118% from the start of 2025 on that news.
- **American Data Centers**, a Dominari-launched HPC/AI data-centre venture, partnered with
  **Hut 8** and became **American Bitcoin** (Eric Trump is co-founder and Chief Strategy
  Officer). Dominari retains an interest in that entity.

A crypto advisory board was added in 2026. The market treats DOMH substantially as a proxy for
those affiliations, not as a boutique broker-dealer.

## 2. Q2 2026 (quarter ended June 30)

| | Q2 2026 | Q2 2025 |
|---|---|---|
| Revenue | **$16.8M, −57%** | $38.9M |
| Operating costs | $17.9M, −67% | ~$53.8M |
| **Operating loss** | **$(1.1)M** | $(14.9)M |
| Net loss to common | $(5.4)M — $(0.24)/sh | — |
| Adjusted EPS | $(0.21) | — |
| Cash & securities | $25.0M cash + $2.4M marketable + $4.5M securities owned | — |

H1 2026: revenue **$52.59M** (+14% vs $46.28M), ARR up to **$1.7M** from $0.5M.

**The operating line is genuinely improving.** An operating loss of $1.1M against $14.9M a year
earlier, with costs down 67%, is a real cost-structure change. The revenue decline is explained
by fewer underwriting closings — lumpy, deal-dependent revenue — while year-to-date revenue is
still up on brokerage and commission activity.

## 3. The number that dominates everything — and an inference to verify

H1 2026 net loss was **$(62.34)M** against $(15.88)M a year earlier. Q2's net loss was only
$(5.4)M.

> **Inferred:** that implies a **Q1 2026 net loss near $(57)M** — roughly **86% of the company's
> entire current market capitalisation, in one quarter.** I did not source a Q1 figure directly;
> it is arithmetic from the H1 and Q2 numbers, so verify it in the 10-Q before relying on it.

> **Also inferred:** the most likely driver is a **mark-to-market loss on the American Bitcoin
> stake** rather than anything operational — the operating line was improving throughout. I could
> not source the composition, so treat the cause as a hypothesis, not a fact.

If that reading is right, DOMH joins every other name in this series where the reported bottom
line describes an investment position rather than the business — Cerebras (stock comp), Amazon
(Anthropic gain), PureCycle (capital structure), Strive (bitcoin marks). Even in Q2, $4.3M of the
$5.4M net loss sat **below** the $1.1M operating loss.

## 4. Valuation — and the unknown that blocks it

- **~$2.92–3.16/share**, market cap **$66–71M**, ~22.6M shares. Down **~45% over 52 weeks**.
- Cash, marketable securities and securities owned total **~$31.9M — about 48% of the market
  cap.** Netting those out leaves roughly **$34M** of enterprise value against annualised H1
  revenue near $105M, i.e. **~0.3x sales**.

That looks cheap, and on a broker-dealer with improving operating costs it might be. But the
valuation **cannot be completed from public summary data**, because the single largest swing
factor is the **current carrying value of the American Bitcoin position**, which I could not
source. Depending on that mark, the same share price implies a materially different premium or
discount to net assets. Anyone underwriting this name should start with that line item in the
10-Q, not with the P&L.

## 5. Modelling notes — the weakest fit for the pipeline so far

Three problems compound here, and the first two are the same species of error flagged for ASST:

1. **The ticker spans three different companies.** DOMH was **AIkido Pharma** — a pharmaceutical
   business — before the pivot to financial services, and the "Legacy AIkido" segment is the
   remnant. A long lookback conditions on a security that no longer exists in any meaningful
   sense. Start the window inside the current business.
2. **Check for corporate actions before trusting any bar.** Micro-caps of this history commonly
   carry reverse splits and name changes; I could not confirm DOMH's split history from public
   summaries. If the downloaded series is unadjusted across a split, every normalisation
   statistic Kronos computes is garbage. Verify the adjustment before the first run — this is a
   data-integrity check, not a modelling preference.
3. **A ~$66M cap with a 1,118% news-driven move in its recent past is event-dominated.** The
   `volume` and `amount` channels will show extreme spikes; realised volatility is not stationary
   in any useful sense; and the events that moved the stock — an advisory-board appointment, a
   subsidiary transaction — are unforecastable from price.

Honest expectation: wide bands, `p10_p90_coverage` well below 0.80, and no meaningful skill
against the random-walk baseline. That is not a reason to skip it — the holdout scorecard on a
name like this is a useful demonstration of where the harness stops working.

```shell
# verify split adjustment first; start inside the current business
python examples/cbrs_cerebras_analysis.py --ticker DOMH --start 2025-01-02 \
    --lookback 250 --pred-len 21 --n-paths 128 --outdir domh_output
```

## Sources

- [TradingView — Q2 2026 10-Q summary](https://www.tradingview.com/news/tradingview:37a61c6c703f7:0-dominari-holdings-inc-q2-2026-revenue-16-8m-eps-0-24-10-q-summary/)
- [StockTitan — Q2 operating loss narrows](https://www.stocktitan.net/news/DOMH/dominari-year-to-date-revenue-increases-by-14-over-vuf8tmahyhsi.html)
- [StockTitan — H1 2026 10-Q, $52.6M revenue](https://www.stocktitan.net/sec-filings/DOMH/10-q-dominari-holdings-inc-quarterly-earnings-report-78f0a08c9039.html)
- [PR Newswire — YTD revenue +14%](https://www.prnewswire.com/news-releases/dominari-year-to-date-revenue-increases-by-14-over-2025-302847720.html)
- [stockanalysis.com — DOMH statistics](https://stockanalysis.com/stocks/domh/statistics/)
- [PR Newswire — American Data Centers becomes American Bitcoin with Hut 8](https://www.prnewswire.com/news-releases/dominari-holdings-investment-american-data-centers-becomes-american-bitcoin-in-transformative-bitcoin-mining-deal-with-hut-8-302415473.html)
- [Data Centre Magazine — Dominari and the data-centre venture](https://datacentremagazine.com/technology-and-ai/dominari-how-the-trump-family-are-investing-in-data-centres)
- [Crypto Briefing — crypto advisory board](https://cryptobriefing.com/crypto-advisory-board-dominari-holdings/)
