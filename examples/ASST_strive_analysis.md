# Strive, Inc. (NASDAQ: ASST) — analysis notes

Eighth ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py). Compiled
2026-09-04 from public sources. **Research notes, not investment advice.**

**Read the ticker history warning in §4 before running any model on this symbol.** ASST is not
the company it was fifteen months ago, and the price series spans two entirely different
securities.

## 1. What ASST is now

ASST was **Asset Entities**, a micro-cap social-media business. In **September 2025** it merged
with **Strive Enterprises**, took the name **Strive, Inc.**, and became a **bitcoin treasury
company** — an entity whose purpose is to accumulate bitcoin and grow bitcoin-per-share. The
merger closed alongside ~**$750M** of equity financing, with a further ~$750M available on
warrant exercise.

The operating business is now a rounding error. Q2 2026 revenue was **$2.9M**. The balance sheet
is the company.

## 2. The bitcoin position and the capital stack

- **23,156 BTC**, ~**$1.85B** (as of 2026-09-04) — the **fifth-largest public bitcoin treasury**,
  up from 19,864 BTC (~$1.2B) at the end of Q2. Those two marks imply roughly **$60.4k/BTC at
  June 30** against **~$79.9k in early September** — bitcoin is up ~32% over the interval, which
  is most of the story in the stock.
- **SATA preferred**: ~7.83M shares, IPO'd November 2025 at **$80**, so roughly **$626M of face**,
  paying a **12.75% dividend** — about **$80M per year in cash**. Plus a $500M SATA ATM program.
- The company also holds ~$50M of Strategy's STRC preferred, so part of the balance sheet is a
  position in *another* treasury company's instrument.
- Common: 75.65M Class A + 9.79M Class B ≈ **85.4M shares**.

**The single most important number here:** that $80M annual preferred coupon is **~6.9x the
company's entire annualised revenue** (~$11.6M). It cannot be paid from operations. It is funded
by issuing more securities or selling bitcoin — which is the structural risk of the whole
leveraged-treasury model, and it does not go away in a bull market.

## 3. Valuation: mNAV is the only metric that matters

For a treasury company, the question is not earnings — it is what you pay for a dollar of
bitcoin, and who has a claim ahead of you.

At ~**$26.80** (a YTD high, up ~165% in six months), market cap on the common is **~$2.29B**:

| Measure | Value |
|---|---|
| Naive mNAV (market cap ÷ bitcoin) | **1.24x** |
| Bitcoin less SATA preferred face | ~$1.22B |
| **mNAV attributable to common** | **~1.87x** |
| At TD Cowen's $32 target | ~2.23x |

**The naive 1.24x is the number that gets quoted and it is misleading.** The preferred sits ahead
of the common, so the NAV backing each common share is bitcoin *minus* that $626M claim. On that
basis holders are paying nearly **1.9x** for the underlying bitcoin. (This is approximate: it
ignores cash, the STRC stake, other liabilities, and any accrued preferred amounts I could not
source. Directionally, the adjustment is large and it goes against the common.)

Why the premium can be rational — and why it is fragile:

- **Above 1x NAV, issuing equity is accretive** to bitcoin-per-share; the premium is the engine.
  Management is explicit that the goal is to outperform bitcoin per share, and TD Cowen models
  27,156 BTC by year-end.
- **Below 1x it reverses**: issuance dilutes, and the preferred coupon still has to be paid.
  Premium compression and a bitcoin drawdown arrive together, and the leverage works both ways.
- With the stock near the **~$27 warrant strike**, exercise brings cash for more bitcoin *and*
  meaningful new share supply. Expect that overhang to cap the premium around this level.

## 4. Earnings are a bitcoin chart

Q2 2026: revenue $2.9M, **GAAP net loss $(257.6)M, EPS $(3.77)**. The company itself discloses
that **$234.0M — 85.1%** — of the $275.0M adjusted net loss came from the **fair-value decline in
bitcoin and STRC holdings**.

This is the purest instance of the pattern running through every name in this series: the
reported bottom line describes something other than the business. For Cerebras it was stock comp,
for Amazon an investment gain, for PureCycle the capital structure. Here **the income statement
is a bitcoin price chart with an accounting wrapper**. Do not read the EPS as performance in
either direction — mark-to-market losses in a down quarter and gains in an up quarter tell you
about bitcoin, not about Strive.

## 5. Modelling notes — the most dangerous series in this set

- **The ticker's price history is not one instrument.** Before September 2025, ASST was Asset
  Entities: a micro-cap with a different business, different float and different volatility. A
  512-bar daily lookback reaches straight through the merger into that other company. **Start the
  data no earlier than the merger** — otherwise the normalisation statistics are computed across
  two unrelated securities and every output is contaminated.
- **What ASST actually is, statistically, is levered bitcoin plus a variable premium.** Its
  returns are roughly bitcoin's, amplified by mNAV changes and modulated by issuance. A model
  conditioned only on ASST's own OHLCV cannot see bitcoin, so it is fitting the composite blind.
  Forecasting BTC directly and modelling the premium separately is the more honest decomposition.
- **Bitcoin trades 24/7; ASST does not.** Weekend and overnight bitcoin moves arrive as Monday
  and morning gaps, the same structural issue flagged for EWY but continuous rather than
  session-based.
- Expect wide bands and expect `p10_p90_coverage` to come in **below** 0.80. Read the tails and
  `prob_drawdown_worse_than_10pct`, never the median path.

```shell
# start AFTER the September 2025 merger -- earlier data is a different company
python examples/cbrs_cerebras_analysis.py --ticker ASST --start 2025-09-15 \
    --lookback 200 --pred-len 21 --n-paths 128 --outdir asst_output
```

Note the reduced `--lookback`: only ~240 sessions of the current company exist, so the default
400/512-bar context cannot be filled without reaching back into Asset Entities.

## Sources

- [Strive Q2 2026 results](https://investors.strive.com/news-events/news-releases/news-details/2026/Strive-Inc--Announces-Second-Quarter-2026-Financial-Results/default.aspx)
- [TradingView — Q2 2026 10-Q summary](https://www.tradingview.com/news/tradingview:b1b5323d9630a:0-strive-inc-q2-2026-revenue-2-94m-eps-3-77-10-q-summary/)
- [Quiver — $257.6M Q2 net loss](https://www.quiverquant.com/news/Strive+Reports+$257.6+Million+Q2+Net+Loss+as+Bitcoin+Holdings+Grow)
- [The Block — fifth-largest public bitcoin treasury, TD Cowen target](https://www.theblock.co/news/business/2026-08-31-strive-fifth-largest-public-bitcoin-treasury-1800-btc-buy-td-cowen-lifts-asst-price-target-413112)
- [The Block — CEO on year-end holdings](https://www.theblock.co/news/markets/2026-09-03-strive-ceo-company-could-end-2026-second-largest-bitcoin-holder-asst-413455)
- [bitcointreasuries.net — Strive holdings](https://bitcointreasuries.net/public-companies/strive)
- [Strive — SATA Nasdaq listing and IPO](https://strive.com/article/strive_announces_nasdaq_listing_of_sata_and_closing_of_oversubscribed__upsized_ipo)
- [Strive — $500M SATA ATM program](https://www.globenewswire.com/news-release/2025/12/09/3202854/0/en/Strive-Announces-500-000-000-SATA-At-The-Market-Program.html)
- [Blockspace — SATA dividend raise, STRC purchase](https://blockspace.media/insight/strive-raises-sata-stock-dividend-acquires-50m-of-strategys-strc/)
- [Merger press release, 2025-09-12](https://www.sec.gov/Archives/edgar/data/0001920406/000121390025087278/ea025712901ex99-1_strive.htm)
