# Sterling Infrastructure (NASDAQ: STRL) — analysis notes

Tenth ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py). Compiled
2026-09-04 from public sources. **Research notes, not investment advice.**

**This one breaks the pattern.** Every other name in this series has a reported bottom line that
describes something other than the business — stock comp at Cerebras, an investment mark at
Amazon and Dominari, bitcoin at Strive, the capital structure at PureCycle, deal accounting at
Genius Sports. Sterling's earnings are simply earnings. The GAAP-to-adjusted gap is about **12%**
of adjusted EPS, mostly amortisation. There is nothing to strip out.

## 1. The business, and its link to the rest of this collection

Sterling builds infrastructure, and the segment that matters is **E-Infrastructure**: site
development for **data centres, semiconductor campuses and large manufacturing plants**. More
than **92% of signed E-Infrastructure backlog** is that mission-critical work.

Read this alongside the [AMZN notes](./AMZN_amazon_analysis.md). Amazon's ~$220B of 2026 capex
and the hyperscaler build-out are, quite literally, where Sterling's backlog comes from. The two
tickers are the same trade viewed from opposite ends of the cash flow: Amazon is the company
whose free cash flow went negative funding the build, Sterling is among the companies the money
is spent with. If you hold a view on AI infrastructure capex, these two names express it in
opposite directions and should not be sized as independent bets.

## 2. Q2 2026 (reported 2026-08-10) — a genuine blowout

| | Q2 2026 |
|---|---|
| Revenue | **$1.17B, +90% YoY** |
| Adjusted diluted EPS | **$5.80, +116%** |
| E-Infrastructure revenue | **+192%**, margins ~**24%** |
| Signed backlog | **$4.3B, +116%** |
| Combined backlog | **$5.6B, +150%** |

FY2026 guidance, raised:

- Revenue **$4.00–4.15B**
- Diluted EPS **$17.25–17.85** (GAAP), adjusted **$19.70–20.30**
- EBITDA **$829–854M**, adjusted **$891–916M**

Combined backlog of $5.6B is about **1.37x** guided annual revenue — multi-year visibility, which
is rare in construction and is the strongest single argument for the stock.

## 3. And the market sold it

- **$519.51**, after a **−15.0% single session** (−$91.96 from $611.47). Market cap **~$17.35B**
  on roughly **33.4M shares**.
- 52-week range **$263.45 – $1,005.68** — a **3.8x** span. The stock sits **~48% below its high**
  and **~97% above its low**.
- Analyst consensus is "Strong Buy" with an average target near **$876**, roughly **+69%** from
  spot — a gap that has, as with CBRS and NNE in this series, been on the wrong side of the tape.

A triple beat plus raised guidance, sold hard. The stated concern is **mix**: E-Infrastructure at
+192% and 24% margins is spectacular, but it concentrates the company in data-centre construction
precisely as the market is repricing how long the hyperscaler capex cycle runs. Sterling is being
valued not on its backlog but on the market's confidence in the customers behind that backlog.

## 4. Valuation

| Basis | Multiple |
|---|---|
| P/E on FY26 GAAP EPS ($17.55 mid) | **29.6x** |
| P/E on FY26 adjusted EPS ($20.00 mid) | **26.0x** |
| Market cap / adjusted EBITDA ($903.5M mid) | 19.2x *(cap-based; I could not source net debt, so this is not a true EV multiple)* |
| Price / sales ($4.075B mid) | 4.3x |

Roughly **26x forward adjusted earnings for a business growing revenue 90% and EPS 116%**, with
1.37x revenue in backlog. On the growth alone that is not demanding. What you are actually paying
for is the durability of data-centre construction demand — and the 48% drawdown from the high says
the market's estimate of that durability has fallen by about half while the fundamentals improved.

That is the whole investment question, and it is not answerable from Sterling's own numbers. It is
answerable, if at all, from hyperscaler capex guidance — which is why the AMZN cross-reference in
§1 matters more than any multiple in this table.

## 5. Modelling notes

The most *forecastable* profile in this set after AMZN and HNST, with one large caveat:

- **Long history, real liquidity.** Sterling has traded for decades (formerly Sterling
  Construction); a $17B cap supports clean bars. No dilution overhang, no financing binaries, no
  foreign-session gap risk.
- **But 2026 realised volatility is extreme** — a 3.8x annual range and a 15% single-session move
  *on an earnings beat*. This is the clearest instance of the earnings-date problem flagged in the
  AMZN notes: a scheduled print inside the forecast horizon is an unforecastable jump, and here it
  moved the stock 15% in the "wrong" direction relative to the news. Keep the horizon inside an
  inter-earnings window, or expect a band breach on exactly one day.
- **Momentum and mean-reversion are fighting.** A stock that has doubled off a low and halved from
  a high inside twelve months has no stable drift for a lookback window to learn. Run both a
  512-bar and a 250-bar context and compare — divergence between them is the honest measure of how
  much the regime has shifted.

```shell
python examples/cbrs_cerebras_analysis.py --ticker STRL --start 2020-01-01 \
    --pred-len 21 --n-paths 128 --outdir strl_output

# regime check against the shorter window
python examples/cbrs_cerebras_analysis.py --ticker STRL --start 2020-01-01 \
    --lookback 250 --pred-len 21 --n-paths 128 --outdir strl_output
```

## Sources

- [Sterling — Q2 2026 results and raised guidance](https://www.strlco.com/news/sterling-reports-record-second-quarter-results-and-raises-full-year-2026-guidance/)
- [Form 8-K, Q2 2026 earnings release](https://www.sec.gov/Archives/edgar/data/0000874238/000087423826000100/q22026earningsreleaseppp.htm)
- [Investing.com — Q2 2026 slides, revenue +90%](https://www.investing.com/news/company-news/sterling-infrastructure-q2-2026-slides-revenue-surges-90-margins-expand-93CH-4835132)
- [Motley Fool — Q2 2026 earnings call transcript](https://www.fool.com/earnings/call-transcripts/2026/08/10/sterling-infrastructure-strl-q2-2026-earnings-call-transcript/)
- [Seeking Alpha — "a triple beat sold on the mix"](https://seekingalpha.com/article/4933724-sterling-infrastructure-q2-2026-review-a-triple-beat-sold-on-the-mix)
- [stockanalysis.com — STRL overview](https://stockanalysis.com/stocks/strl/)
- [MacroTrends — STRL price history](https://www.macrotrends.net/stocks/charts/STRL/sterling-infrastructure/stock-price-history)
