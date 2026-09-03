# PureCycle Technologies (NASDAQ: PCT) — analysis notes

Fourth ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py), alongside
[CBRS](./CBRS_cerebras_analysis.md), [NNE](./NNE_nano_nuclear_analysis.md) and
[AMZN](./AMZN_amazon_analysis.md).

Compiled 2026-09-03 from public sources. **Data-quality warning specific to this name:** unlike
the other three, I could not pin a reliable current quote — aggregator figures spanned roughly
$6.87–$7.62 through mid-2026 with a ~$1.5B market cap, and the 52-week range on hand
($4.50–$17.37) is stale. The Q2 financials below are firm; the market data is indicative only.
Verify against a live quote. **Research notes, not investment advice.**

## 1. What the business is

PureCycle licenses and operates a purification process that turns waste polypropylene into
near-virgin resin, sold as **PureFive™**. The flagship plant is **Ironton, Ohio**, with expansion
at **Augusta, Georgia**. It is a commissioning-stage industrial company: the question is not
demand or technology in the abstract, it is whether the plants run at rate, reliably, at a cost
that leaves a margin.

## 2. Q2 2026 financials (quarter ended June 30, reported 2026-08-06)

| | Q2 2026 | Q2 2025 |
|---|---|---|
| Revenue | **$4.51M**, +173% YoY | ~$1.65M |
| Operating loss | $(41.3)M | $(45.6)M |
| **Net loss** | **$(142.2)M** — ~$(0.80)/share | $(144.2)M |
| Adjusted EBITDA | $(31.7)M | $(27.8)M |
| Liquidity | **$236.9M** + undrawn $200M revolver | — |
| PureFive production | 4.5M lbs (planned Ironton turnaround) | — |

Three observations that matter more than the headline:

1. **The bottom line is not an operating number.** Operating loss was $41.3M but net loss was
   $142.2M — roughly **$101M, about 71% of the loss, sits below the operating line** (financing
   costs and mark-to-market on the convertible/warrant structure). Same lesson as CBRS and AMZN
   in this series: the reported net loss says more about the capital structure than the plants.
   Read the operating line and adjusted EBITDA.
2. **Scale is still tiny.** $4.51M of revenue against a $142.2M net loss is a **~31x
   loss-to-revenue ratio**. Annualized, revenue is ~$18M against a ~$1.5B market cap — on the
   order of **80x sales**. The +173% growth is real but off a base near zero.
3. **The turnaround is arguably the quarter's best news.** Production of 4.5M lbs was *down*
   because of a planned Ironton turnaround — completed ahead of schedule and under budget,
   addressing reliability constraints, with record throughput after restart. For a commissioning
   story, reliability progress is worth more than a single quarter's volume.

## 3. Financing is the whole story

- The company raised **~$432M in equity and convertible notes** during the quarter, ending with
  $236.9M of liquidity plus a $200M undrawn revolver.
- On adjusted-EBITDA burn alone (~$31.7M/qtr), $236.9M is about **7.5 quarters (~1.9 years)** —
  and that is *before* growth capex and cash interest, which are the larger draws for a company
  building out Augusta. Real runway is shorter.
- Dilution is severe and ongoing: ~178M weighted shares, further **424B5 shelf takedowns** filed
  in 2026, and a June 2026 credit-agreement amendment executed specifically to permit an
  offering.
- **Short interest was ~51.5M shares, ~35% of float (as of 2026-04-30)**, ~16 days to cover.
  (One aggregator reports a far lower figure on a different basis; treat the exact level as
  uncertain, the direction as not.) At that level, financing headlines and production data move
  the stock far more than fundamentals justify, in both directions.
- Analyst targets have been **cut, not raised**: one house to $6 from $9, Cantor Fitzgerald to
  $12 from $14, with a ~$11.50 one-year target elsewhere. The dispersion — $6 to $12 — is itself
  the signal: this is a binary-outcome model, not a valuation consensus.

## 4. How to think about it

PCT is the same *shape* of risk as NNE: a pre-scale company whose equity value depends on
execution milestones, funded by dilution, with heavy short positioning amplifying every
headline. The difference is that PCT's milestones are **industrial** (plant uptime, throughput,
unit economics) rather than **regulatory**, so evidence arrives quarterly and continuously
rather than in discrete binary events.

What would actually change the thesis, in order:
1. Sustained Ironton throughput at rate post-turnaround — the reliability question answered with
   several quarters of data, not one.
2. Revenue crossing from "pilot" to material scale, with a **disclosed price per pound** that
   implies a workable gross margin. (Q2's $4.51M against 4.5M lbs is ~$1.00/lb, but volume and
   revenue in a turnaround quarter don't align cleanly enough to read margin from it.)
3. Augusta funded and on schedule **without** another large equity raise.

Failure mode: another turnaround, another raise at a lower price, another leg down in the
multiple.

## 5. What Kronos can and cannot add here

Data is adequate — PCT has traded since the 2021 SPAC merger, comfortably more than the 512-bar
context. But this is the **hardest** of the four names for a price-only model:

- ~35% short interest plus binary financing headlines produces fat-tailed, gap-driven returns.
  The ensemble will understate tail risk because the historical bars it conditions on do not
  contain the next dilutive raise.
- Equity raises are *structural* level shifts, not dynamics. Nothing in the price series
  anticipates a 424B5 takedown.
- Read `prob_drawdown_worse_than_10pct` and the p05 tail rather than the median path, and expect
  `p10_p90_coverage` to come in **below** 0.80 — under-coverage here is the honest result, and
  it quantifies exactly how much of this name's risk is outside the model.

```shell
python examples/cbrs_cerebras_analysis.py --ticker PCT --start 2021-03-18 \
    --pred-len 21 --n-paths 128 --outdir pct_output
```

## Sources

- [PureCycle Q2 2026 results](https://www.purecycle.com/blog/purecycle-technologies-reports-second-quarter-2026-results)
- [StockTitan — Q2 2026 10-Q, $4.5M revenue / $142M loss](https://www.stocktitan.net/sec-filings/PCT/10-q-pure-cycle-technologies-inc-quarterly-earnings-report-fe6bd196daf9.html)
- [StockTitan — Q2 2026 8-K, liquidity detail](https://www.stocktitan.net/sec-filings/PCT/8-k-pure-cycle-technologies-inc-reports-material-event-44eb3adb8e47.html)
- [Simply Wall St — liquidity and losses](https://simplywall.st/stocks/us/materials/nasdaq-pct/purecycle-technologies/news/purecycle-technologies-pct-stock-hinges-on-liquidity-as-loss)
- [Form 424B5 (2026 shelf takedown)](https://www.sec.gov/Archives/edgar/data/0001830033/000119312526266073/d156526d424b5.htm)
- [Fintel — PCT short interest](https://fintel.io/ss/us/pct)
- [TipRanks — PCT forecast and targets](https://www.tipranks.com/stocks/pct/forecast)
- [stockanalysis.com — PCT overview](https://stockanalysis.com/stocks/pct/)
