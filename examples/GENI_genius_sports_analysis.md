# Genius Sports (NYSE: GENI) — analysis notes

Sixth ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py). Compiled
2026-09-03 from public sources. **Research notes, not investment advice.**

## 1. The business

Genius Sports supplies official sports data and betting technology — most importantly the
**official NFL data feed** that FanDuel, BetMGM, Caesars and the other major US sportsbooks
depend on. That rights position is the moat: it is contractual, exclusive and expensive, which
cuts both ways (competitors cannot replicate it; renewals are a recurring risk).

The shape of the company changed on **2026-04-30**, when it closed the acquisition of **Legend**,
a gambling-media and affiliate-marketing business: **$900M up front** ($800M cash + $100M stock)
plus an earnout of up to **$300M** over two years — ~$1.2B headline. It was funded with an
**$825M term loan** and a $220M revolver. Media revenue rose **193%** in the first full quarter
post-close.

## 2. Q2 2026 (reported 2026-08-06)

| | Q2 2026 | vs guidance |
|---|---|---|
| Revenue | **$196M**, +65% YoY | guide $185M — beat |
| Adjusted EBITDA | **$53M** | guide $45M — beat |
| **GAAP net loss** | **$(77)M**, $(0.28)/share | consensus $(0.08) — big miss |

FY2026 guidance raised to revenue **$1.005–1.025B** and adjusted EBITDA **$285–295M** (~28.6%
margin at the midpoint).

**The $130M gap between +$53M adjusted EBITDA and a $(77)M GAAP loss is the whole analytical
question.** Management attributes it to transaction costs, acquisition financing and non-cash
purchase-accounting items from Legend.

This is the fourth name in this series where the reported bottom line describes financing rather
than operations — but it deserves **more** scepticism than the others, not less:

- Transaction costs are genuinely one-off. Fine to exclude.
- **Interest on $825M of term debt is neither one-off nor non-cash.** It recurs every quarter and
  consumes real money. Adjusted EBITDA excludes it by construction, so EBITDA now flatters this
  company in a way it did not before April.
- Amortisation of acquired intangibles is non-cash, but it represents ~$900M of capital actually
  spent. Excluding it forever is a choice, not a fact.

The right lens post-Legend is **free cash flow after interest**, or at minimum EBITDA less cash
interest and capitalised development costs — not headline adjusted EBITDA.

## 3. Valuation and the tape

- **~$7.28** (Sep 1, 2026), market cap **~$2.02B** on ~267.6M shares (+10.9% YoY, partly the
  Legend stock consideration).
- 52-week range roughly **$3.83 – $13.7**: about **47% below the high** and **90% above the low**.
  A stock that has tripled and then halved inside a year.
- Adding the ~$825M of acquisition debt gives an enterprise value near **$2.85B** (before netting
  cash), which is:
  - **~9.8x** FY26 adjusted EBITDA at the $290M midpoint
  - **~2.0x** FY26 revenue

Roughly 10x EBITDA for a business guiding to ~28.6% margins with a contractual moat is not an
expensive multiple — which is precisely why the leverage question matters. The market is pricing
in the risk that the EBITDA is worth less than it looks once cash interest is paid, and that
Legend's affiliate-marketing revenue is lower-quality and more cyclical than the data-rights
business it was bolted onto.

**What would resolve it:** two or three quarters of post-deal free cash flow after interest, and
evidence on whether the earnout is tracking toward payment (a good sign for Legend's performance,
a cash cost either way).

## 4. Modelling notes

GENI has traded since the 2021 SPAC merger — adequate history for the 512-bar context. Two
features matter for a price-only model:

- **Seasonality is real and structural.** Revenue and news flow track the sports calendar; the
  NFL season is the single largest driver, and management flagged NFL advertising activations as
  a second-half catalyst. Kronos's timestamp features (month, weekday) can pick up some of this,
  but a 21-bar horizon spanning a season boundary is not comparable to one that does not.
- **The April 2026 acquisition is a structural break.** The company on either side of that date
  is not the same company: different revenue mix, different leverage, different margin profile.
  A 512-bar lookback reaches back through it. Compare against a post-May-2026 context window and
  treat a large divergence as information about the break, not noise.

```shell
python examples/cbrs_cerebras_analysis.py --ticker GENI --start 2021-04-20 \
    --pred-len 21 --n-paths 128 --outdir geni_output
```

## Sources

- [Genius Sports Q2 2026 release](https://www.geniussports.com/newsroom/genius-sports-beats-second-quarter-guidance-and-raises-full-year-outlook/)
- [Investing.com — Q2 2026 slides, guidance raised](https://www.investing.com/news/company-news/genius-sports-q2-2026-slides-revenue-beats-guidance-raised-93CH-4842637)
- [TradingKey — Q2 revenue +65%, GAAP loss widens](https://www.tradingkey.com/news/earnings/262083235-tradingkey)
- [TipRanks — Legend close and $1.05B debt package](https://www.tipranks.com/news/company-announcements/genius-sports-closes-legend-acquisition-and-secures-1-05-billion-debt-package)
- [Sportico — Legend deal terms](https://www.sportico.com/business/sports-betting/2026/genius-sports-buys-legend-affiliate-marketing-1234883588/)
- [StockTitan — 20-F risks, rights and Legend deal](https://www.stocktitan.net/sec-filings/GENI/20-f-genius-sports-ltd-files-annual-report-foreign-issuer-ef31d0c8989d.html)
- [stockanalysis.com — GENI statistics](https://stockanalysis.com/stocks/geni/statistics/)
