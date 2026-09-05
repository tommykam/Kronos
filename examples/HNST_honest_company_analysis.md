# The Honest Company (NASDAQ: HNST) — analysis notes

Seventh ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py). Compiled
2026-09-03 from public sources. **Research notes, not investment advice.**

The odd one out in this set: a consumer-products company that is **profitable, debt-free and
cash-generative**, after several years in which it was none of those things.

## 1. Q2 2026 — read the organic line, not the headline

| | Q2 2026 |
|---|---|
| Revenue | **$83.3M, −10.9% YoY** |
| **Organic revenue** | **$80.2M, +6.7%** (from $75.1M) |
| Net income | **$10.7M** (from $3.9M) |
| EPS | $0.04 reported vs $0.02 expected |
| Cash / debt | **$105.9M cash, zero debt** (as of 2026-06-30) |

**The revenue decline is deliberate.** Reported revenue fell because of planned SKU and channel
exits under the "Powering Honest Growth" program, plus continued weakness in diapers. Strip
those and the underlying business grew **+6.7%**, led by wipes and personal care. A shrinking
top line that is *chosen* in order to lift margin is a different fact from a shrinking top line
that is imposed — and this is the former.

FY2026 guidance was **raised**: revenue **$319–325M**, organic growth **5–7%**, adjusted gross
margin in the **mid-40s%**, adjusted EBITDA **$23.0–25.0M**.

> **Data-quality flag.** The reported EPS and net income do not reconcile at the share count I
> have: ~107.3M shares × $0.04 ≈ $4.3M, against $10.7M of net income (which would imply
> ~$0.10/share). The likeliest explanations are that the $0.04 is an adjusted figure, that the
> $10.7M covers the half-year, or that a tax item sits between them. Check the
> [Q2 2026 8-K exhibit](https://www.sec.gov/Archives/edgar/data/0001530979/000162828026053315/honestcoq2-26exhibit991.htm)
> before relying on either number. The guidance and balance-sheet figures are firm.

## 2. Valuation

- **$5.71** (Sep 2, 2026), market cap **~$614M** on ~107.3M shares.
- 52-week range **$2.07 – $5.96**: within about **4% of the high**, and **+176% off the low**.
  This is the only name in the series trading near its highs.
- Net of $105.9M cash (17% of the market cap) and no debt, enterprise value is **~$508M**:
  - **~21x** FY26 adjusted EBITDA at the $24M midpoint
  - **~1.6x** EV/sales, ~1.9x price/sales

So the market is paying roughly 21x EBITDA for a mid-single-digit organic grower with expanding
margins. That is a **full but not absurd** multiple for consumer staples-adjacent growth — the
debate is whether mid-40s gross margin and 5–7% organic growth are a durable new baseline or the
easy part of a turnaround.

## 3. The bull and bear case, compactly

**Bull:** the turnaround is working on the metric that matters — margin — and it is self-funded.
No debt, growing cash, guidance raised rather than cut, and the portfolio pruning is nearly
through. Mid-40s adjusted gross margin in this category is respectable.

**Bear:** ~$614M of market cap on ~$24M of adjusted EBITDA leaves little room for a miss, the
stock has already tripled off the lows, diapers — historically the anchor category — are still
declining, and the company competes against Procter & Gamble and Kimberly-Clark, who can absorb
price competition indefinitely. The easy margin gains from exiting bad SKUs do not repeat.

## 4. Modelling notes

HNST is the **cleanest** series in this set for the forecasting pipeline, and worth using as a
second calibration point alongside AMZN:

- Public since the 2021 IPO — enough history for the 512-bar context.
- No leverage, no dilutive financing overhang, no regulatory binary events, no overnight foreign
  gap risk. The return distribution is closer to well-behaved than anything else here except
  AMZN, but at small-cap volatility rather than mega-cap.
- The one structural caveat is **liquidity**: a ~$614M small cap has wider spreads and thinner
  volume than the other names, so the `volume` and `amount` channels Kronos tokenizes are noisier
  and more prone to single-day spikes around earnings.

If `p10_p90_coverage` comes in near 0.80 on both AMZN (mega-cap, efficient) and HNST (small-cap,
clean), the harness is calibrated across the size spectrum, and the under-coverage seen on
CBRS/NNE/PCT can be attributed to those names' event risk rather than to the model.

```shell
python examples/cbrs_cerebras_analysis.py --ticker HNST --start 2021-05-05 \
    --pred-len 21 --n-paths 128 --outdir hnst_output
```

## Sources

- [StockTitan — Q2 2026 results and raised outlook](https://www.stocktitan.net/news/HNST/the-honest-company-reports-second-quarter-2026-kgyg6iceuoh2.html)
- [Form 8-K, Q2 2026 exhibit 99.1](https://www.sec.gov/Archives/edgar/data/0001530979/000162828026053315/honestcoq2-26exhibit991.htm)
- [StockTitan — 8-K, 2026 guidance lift and Q2 margins](https://www.stocktitan.net/sec-filings/HNST/8-k-honest-company-inc-reports-material-event-865b3937f31a.html)
- [Simply Wall St — balance sheet and financial health](https://simplywall.st/stocks/us/household/nasdaq-hnst/honest/health)
- [stockanalysis.com — HNST market cap](https://stockanalysis.com/stocks/hnst/market-cap/)
- [Form 8-K, Q1 2026 exhibit](https://www.sec.gov/Archives/edgar/data/0001530979/000162828026031240/honestcoq1-26exhibit991.htm)
