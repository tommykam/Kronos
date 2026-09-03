# NANO Nuclear Energy (NASDAQ: NNE) — analysis notes

Second ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py), which is
ticker-agnostic apart from its defaults. Same structure as the
[CBRS notes](./CBRS_cerebras_analysis.md): the market context a price-only model cannot see,
plus what the model can and cannot contribute on this particular series.

Compiled 2026-09-03 from public sources (linked at the bottom). Aggregator figures disagree in
places — verify against the 10-Q and a live quote. **Research notes, not investment advice.**

> Naming collision worth flagging: NNE's flagship reactor is the **KRONOS MMR™**, unrelated to
> the Kronos forecasting model in this repository.

## 1. Company snapshot

NANO Nuclear is a pre-commercial microreactor developer with an adjacent nuclear fuel-cycle
business. It is not a chip-style growth story with a revenue line to extrapolate; it is an
option on regulatory milestones, funded by a very large cash pile relative to its size.

Reactor programs: **KRONOS MMR** (stationary high-temperature gas-cooled), **ZEUS** (portable
solid-core battery reactor), **LOKI MMR** (portable, space-focused). Fuel and logistics:
**HALEU Energy Fuel Inc.** (LEU/HALEU supply chain) and **Advanced Fuel Transportation**,
enlarged by the May 2026 acquisition of **Secured Transportation Services (STS)**.

IPO 2024-05-08 on Nasdaq at **$4.00**, a tiny $10.25M raise. Everything on the balance sheet
today came from subsequent offerings, which is the central tension in the stock.

## 2. Financials (fiscal year ends September 30)

| | Q2 FY26 (Mar 2026) | Q3 FY26 (Jun 2026) |
|---|---|---|
| Revenue | none (pre-revenue) | **$214,042** (first revenue, from STS) |
| Net loss | $(9.2)M | $(10.1)M — EPS $(0.19) |
| Cash + investments | ~$569M liquidity | **$580M** ($298.5M cash + $281.5M T-bills) |
| Total assets | — | $628.0M |

Nine-month FY26 net loss: **$(25.8)M**, improved from $(32)M a year earlier — helped by higher
interest income and lower equity-based compensation, not by operating leverage.

Three things follow from those numbers:

1. **Funding risk is low; dilution risk is the real one.** At roughly $10M of net loss per
   quarter against $580M of liquidity, runway is measured in years, not quarters. But the share
   count rose ~45% year over year (41.7M → ~52.1M), weighted-average shares rose ~34%, and a
   **$900M shelf** went effective in March 2026. Per-share loss held flat at $(0.19) only
   *because* the denominator grew as fast as the loss.
2. **Interest income masks the operating burn.** With ~$580M in cash and Treasuries, investment
   income plausibly runs several million per quarter, so the underlying operating loss is
   materially larger than the reported net loss. Read the operating line, not the bottom line.
3. **Revenue is real but immaterial to valuation.** $214K in a quarter annualizes to under $1M
   against a market cap near $0.9B. It is evidence that the fuel-logistics arm executes, not a
   basis for a multiple.

## 3. What the tape says (late August / early September 2026)

- Trading in the **mid-to-high teens** — roughly $15.91–$17.97 across late-August quotes —
  against a 52-week range of **$14.71–$60.87**. That is **~70–74% off the high**, and within
  ~10% of the 52-week low, while still ~3.5x the $4.00 IPO price.
- Market cap ≈ **$0.83–0.97B** on ~52–54M shares. Netting out the $580M of cash and Treasuries
  leaves an **enterprise value of roughly $250–385M**, i.e. **60–70% of the share price is
  cash**. The market is paying a few hundred million dollars for the reactor and fuel programs.
- **Short interest ~8.9M shares, ~17% of shares outstanding** — high enough that news-driven
  moves in either direction get amplified.
- Sell-side targets cluster far above spot: quoted figures include $34.40, $40.83 and a $45.00
  median (range $45–$50), on 3 Buy / 1 Hold. As with CBRS, the targets have been wrong-footed by
  the tape all year.

**Why it has de-rated** is not a mystery and not a fundamental break: regulatory progress has
not yet converted into signed commercial economics, and the market has repriced the gap between
milestones and orders while absorbing steady dilution.

## 4. Catalysts and the risk register

Achieved in 2026:

- **2026-03-31** — University of Illinois Urbana-Champaign submits the Construction Permit
  Application for a full-scale KRONOS MMR.
- **2026-05-20** — NRC formally **accepts the CPA for review**; the company believes KRONOS is
  the first commercially-ready microreactor to reach the CPA stage.
- **May 2026** — STS acquisition closes; STS subsequently supports DOE/NNSA missions including
  HALEU transport from Japan and HEU removal from Venezuela.
- Founding member of the **DOE HALEU consortium**; key subcontractor (with LIS Technologies) in
  the DOE **LEU Enrichment Acquisition Program**, ~$3.4B appropriated across six awardees.
- MOU with **Quadrant Nuclear Industries** on domestic HALEU supply.

Risks, in rough order of how much they move the stock:

1. **Milestones ≠ orders.** NRC acceptance starts a multi-year safety, environmental and
   technical review; a construction permit is not an operating licence, and a university
   demonstration unit is not a commercial order book.
2. **Dilution on a $900M shelf**, against a ~$0.9B market cap. Any raise near these levels is
   heavily accretive to share count.
3. **Schedule risk** in licensing and construction cost — the two failure modes that have
   historically defined this sector.
4. **Positioning.** 17% short interest plus a small float makes realized volatility far higher
   than the fundamentals alone would justify.

## 5. What Kronos can and cannot add here

Unlike CBRS, **NNE has enough history to use the model properly**: ~606 weekday sessions since
the May 2024 IPO, comfortably more than the 512-bar context window. The full default lookback
works on daily bars.

Two caveats specific to this series:

- **Regime instability is extreme.** A $4 → $60.87 → ~$16 path in ~28 months means the context
  window's normalization statistics depend heavily on where you start. Compare a 512-bar
  lookback against a 250-bar one; if the forecast distributions diverge sharply, that is the
  honest signal — the series has no stable dynamics to learn.
- **The distribution matters more than the median.** With 17% short interest and binary
  regulatory headlines, the realistic outcome set is bimodal; a unimodal ensemble median is the
  least informative statistic the script produces. Read `quantile_bands`,
  `terminal_return.p05/p95` and `prob_drawdown_worse_than_10pct`.

As always, the holdout backtest is the gate: `rmse_skill_vs_baseline` must be positive and
`p10_p90_coverage` should sit near 0.80 before the direction of the forecast is worth anything.

## 6. Running it

```shell
# full post-IPO daily history, 21 sessions ahead
python examples/cbrs_cerebras_analysis.py --ticker NNE --start 2024-05-08 \
    --pred-len 21 --n-paths 64 --outdir nne_output

# regime-sensitivity check: shorter context on the same data
python examples/cbrs_cerebras_analysis.py --ticker NNE --start 2024-05-08 \
    --lookback 250 --pred-len 21 --n-paths 64 --outdir nne_output
```

## Sources

- [stockanalysis.com — NNE overview](https://stockanalysis.com/stocks/nne/) and
  [statistics](https://stockanalysis.com/stocks/nne/statistics/)
- [WallStreetZen — NNE quote](https://www.wallstreetzen.com/stocks/us/nasdaq/nne)
- [Form 10-Q, quarter ended 2026-06-30](https://www.sec.gov/Archives/edgar/data/0001923891/000149315226037345/form10-q.htm)
- [TradingView — Q3 FY2026 10-Q summary](https://www.tradingview.com/news/tradingview:c36c40ce9c1b1:0-nano-nuclear-energy-inc-3q-2026-revenue-214k-eps-0-19-10-q-summary/)
- [StockTitan — Q3 FY2026 cash and segment detail](https://www.stocktitan.net/sec-filings/NNE/10-q-nano-nuclear-energy-inc-quarterly-earnings-report-7ec5db568e27.html)
- [Investing.com — Q3 FY2026 slides](https://www.investing.com/news/company-news/nano-nuclear-q3-2026-slides-nrc-accepts-reactor-permit-580m-liquidity-93CH-4856413)
- [NRC accepts KRONOS MMR construction permit application (2026-05-20)](https://nanonuclearenergy.com/nano-nuclears-kronos-mmr-and-the-university-of-illinois-urbana-champaign-advance-to-next-regulatory-milestone-as-u-s-nrc-formally-accepts-construction-permit-application-for-review/)
- [CPA submission (2026-04-02 release)](https://www.globenewswire.com/news-release/2026/04/02/3267309/0/en/NANO-Nuclear-s-KRONOS-MMR-Microreactor-Advances-to-Critical-Milestone-Toward-Reactor-Deployment-with-the-University-of-Illinois-Urbana-Champaign-Submission-of-a-Construction-Permit.html)
- [STS completes DOE/NNSA transport missions (2026-05-28)](https://www.globenewswire.com/news-release/2026/05/28/3302804/0/en/Recently-Acquired-NANO-Nuclear-Subsidiary-Secured-Transportation-Services-STS-Completes-Three-DOE-and-NNSA-Aligned-Nuclear-Materials-Transport-Missions.html)
- [DOE HALEU consortium founding member](https://nanonuclearenergy.com/nano-nuclear-energy-inc-selected-as-an-official-founding-member-of-the-u-s-department-of-energy-doe-new-high-assay-low-enriched-uranium-haleu-consortium-a-crucial-material-to-supply-fuel-for-th/)
- [Form S-3/A shelf registration](https://www.sec.gov/Archives/edgar/data/1923891/000149315226009303/forms-3a.htm)
- [IPO pricing, May 2024](https://nanonuclearenergy.com/nano-nuclear-energy-announces-pricing-of-initial-public-offering/)
