# iShares MSCI South Korea ETF (NYSE Arca: EWY) — analysis notes

Fifth ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py), after
[CBRS](./CBRS_cerebras_analysis.md), [NNE](./NNE_nano_nuclear_analysis.md),
[AMZN](./AMZN_amazon_analysis.md) and [PCT](./PCT_purecycle_analysis.md).

First non-equity in the set: a fund, so there are no earnings to analyze. The analytical work
moves to **what the fund actually holds**, the **currency leg**, and the **market-structure
quirks** that make an international ETF behave differently from a US single stock.

Compiled 2026-09-03 from public sources. **Research notes, not investment advice.**

## 1. It is not a country fund — it is a memory-chip trade

| Holding | Weight |
|---|---|
| Samsung Electronics | 23.19% |
| SK hynix | 22.35% |
| SK Square | 3.27% |
| Samsung Electro-Mechanics | 2.38% |
| KB Financial Group | 2.12% |

Samsung and SK hynix alone are **~45.5%** of the fund. Add SK Square — a holding company whose
principal asset is its SK hynix stake — and roughly **49% of EWY is a direct bet on memory**,
before counting Samsung Electro-Mechanics and the rest of the supply chain.

Anyone buying EWY for "diversified Korea exposure" is, in practice, buying a leveraged position
in HBM demand for AI accelerators with a Korean-market wrapper. The financials, autos and
industrials in the remaining half are not large enough to change that.

Fund basics: **~$24B AUM**, **0.59% expense ratio** (~$142M/yr in aggregate fees), unhedged.

## 2. 2026 has been violent

- **Price ~$176.55** (Sep 1, 2026), down 2.4% on the day from a $180.86 close.
- **52-week range: $71.39 – $220.89.** That is a **3.1x** low-to-high span in twelve months.
  The fund sits **~20% below the high** and **~147% above the low**.
- Quoted year-to-date returns range from **+36% to +67%** depending on as-of date, with a
  1-year figure near +130%. The spread between those numbers is not a data error — it is the
  July crash sitting inside the measurement window. Any single YTD snapshot for this fund in
  2026 is close to meaningless without its date.

The underlying market told the same story more sharply:

- KOSPI **+44% for 2026**, past 6000, with Korea's market cap overtaking France's and Germany's.
- Then **−33% from the June peak through late July**, roughly **$2 trillion** of market value
  erased. Foreign investors pulled **₩18.5tn (~$13B)** from Korean equities in July alone, with
  forced liquidation of leveraged positions amplifying the move.
- Then a **>20% rebound in ten days**, including a **~14% single-day gain**, back into bull
  market territory by mid-August.

The trigger matters for interpretation. The late-July collapse began on news that **China had
started mass production of domestic deep-ultraviolet chipmaking tools** — a *competitive*
shock to the Korean semiconductor franchise, not a collapse in AI memory demand. Whether the
rebound is durable depends on which of those two readings turns out to be right, and that
question is not answerable from price data.

## 3. The currency leg

EWY is **unhedged**, so a USD holder's return is Korean equity return × KRW move. That leg has
been a tailwind recently: **USD/KRW at 1,368.88** (Sep 2), with the won up roughly **5% in
August** — its strongest since July 2025 — on exporter dollar-selling.

Two consequences worth holding onto:

1. The won typically **weakens** in global risk-off episodes, exactly when Korean equities fall.
   The two legs are positively correlated in drawdowns, so USD-based losses are amplified
   relative to the local-currency index. Sizing off KOSPI's volatility understates EWY's.
2. Some of 2026's headline USD return is currency, not equities. Compare EWY against the local
   KOSPI return before attributing performance to stock picking or the memory cycle.

## 4. What Kronos can and cannot add here

EWY is the most *technically* interesting series in this set, for a reason that has nothing to
do with Korea:

- **Data is abundant** — EWY has traded since 2000, far beyond the 512-bar context, with deep
  liquidity and no earnings-date jumps to corrupt the horizon.
- **But the bar structure is unusual.** Korea trades while the US is closed, so most of EWY's
  daily move arrives as an **overnight gap** at the US open; the US session is largely
  arbitrage against Korean futures and ADRs. Open-to-close and close-to-open returns therefore
  have very different distributions, and a model conditioned on OHLCV bars is learning that
  asymmetry whether or not you intended it. Interpret intraday bar shapes (the high-low range,
  the open-close body) accordingly — they do not mean what they mean for a US single stock.
- **2026 realized volatility is extreme and regime-switching**: a 3.1x annual range, a 33%
  index drawdown and a 14% single-day rally. Expect very wide ensemble bands. That width is the
  correct output, not a defect.

So the honest framing: run it, and read `forecast_vol_ann` and `p10_p90_coverage` rather than
the median path. If coverage lands near 0.80 through a year containing both the July crash and
the August melt-up, the ensemble is doing real work on tail risk. If it lands well below, the
model is under-representing exactly the gap risk that defines this fund.

```shell
python examples/cbrs_cerebras_analysis.py --ticker EWY --start 2010-01-01 \
    --pred-len 21 --n-paths 128 --outdir ewy_output

# stress the regime question: pre- vs post-July-2026 context
python examples/cbrs_cerebras_analysis.py --ticker EWY --start 2024-01-01 \
    --lookback 250 --pred-len 21 --n-paths 128 --outdir ewy_output
```

## Sources

- [iShares EWY fact sheet (as of 2026-06-30)](https://www.ishares.com/us/literature/fact-sheet/ewy-ishares-msci-south-korea-etf-fund-fact-sheet-en-us.pdf)
- [stockanalysis.com — EWY holdings](https://stockanalysis.com/etf/ewy/holdings/) and
  [overview](https://stockanalysis.com/etf/ewy/)
- [ETFdb — EWY profile](https://etfdb.com/etf/EWY/)
- [CNBC — Kospi meltdown to record rebound](https://www.cnbc.com/2026/07/31/south-korea-kospi-samsung-sk-hynix-meltdown-record-rebound.html)
- [CNBC — Kospi bull market, SK Hynix and Samsung surge](https://www.cnbc.com/2026/08/13/south-korea-kospi-bull-market-sk-hynix-samsung-surge.html)
- [Al Jazeera — Korean market plunge, July 2026](https://www.aljazeera.com/economy/2026/7/29/south-koreas-stock-market-plunges-as-ai-driven-boom-fades)
- [Fortune — Kospi rout and leveraged positioning](https://fortune.com/2026/08/02/kospi-rout-korea-stock-market-volatility-sk-hynix-samsung-ai-leveraged-etf/)
- [Bloomberg — Korean stocks rise 22% in ten days](https://www.bloomberg.com/news/articles/2026-08-13/korean-stocks-rise-22-in-ten-days-as-chip-rally-regains-steam)
- [TradingEconomics — South Korean won](https://tradingeconomics.com/south-korea/currency)
- [Investing.com — EWY quote](https://www.investing.com/etfs/ishares-south-korea-index)
