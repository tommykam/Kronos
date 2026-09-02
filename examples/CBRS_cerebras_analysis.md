# Cerebras Systems (NASDAQ: CBRS) — analysis notes

Companion document to [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py), which runs a
Kronos forecast and a risk snapshot on CBRS. This file records the context a purely
statistical forecast cannot see: what the company is, what the tape has done since the IPO,
and where the model's assumptions break down for this particular ticker.

Compiled 2026-09-02 from public sources (linked at the bottom). Figures reported by
third-party aggregators disagree in places — verify against the 10-Q and a live quote before
relying on any number here. **Research notes, not investment advice.**

## 1. Company snapshot

Cerebras builds wafer-scale AI accelerators (the WSE / CS-series) and sells both systems and
hosted inference capacity. The pitch is latency: whole-wafer compute keeps model weights in
on-chip SRAM, which makes token generation dramatically faster than GPU clusters for
inference-heavy workloads. Revenue therefore arrives through two very different channels —
lumpy system sales, and a subscription-like cloud/services line.

- IPO 2026-05-14 at **$185.00/share**, above the raised $150–160 range, ~30M shares,
  **~$5.5B raised** (~$6.4B including the greenshoe per the Q1 call), fully diluted valuation
  ~$56.4B at the offer price. It opened at $385 (+108%) and closed day one at $311.
- **CS-4** launched 2026-08-18, marketed as the fastest AI accelerator in the industry.

## 2. Fundamentals as reported in 2026

| | Q1 2026 (Mar) | Q2 2026 (Jun) |
|---|---|---|
| Core revenue | $191.3M, +92% YoY | $209.9M, +103% YoY |
| GAAP revenue | $193.4M | $180.11M |
| Core gross margin | ~46.5% | 40.6% (≈45.6% ex rent-back) |
| Net loss / diluted EPS | — | $(450.5)M / $(2.98) |
| Adjusted EPS | — | $(0.05) vs $(0.17) expected |

Three details drive most of the debate around the stock:

1. **GAAP revenue fell below core revenue in Q2** because warrants issued to OpenAI are booked
   as contra-revenue. GAAP revenue declined sequentially while the underlying business grew
   ~10% QoQ — a reporting artifact that reads as a miss on a headline screen and helps explain
   the post-print drop despite beats on core metrics.
2. **Margins are being spent, deliberately.** Q2 core gross margin fell 590bps QoQ because
   Cerebras rented systems back from customers to serve demand. Guidance calls Q3 the trough:
   core gross margin 38–40%, core operating margin −25% to −23%; FY2026 gross margin 41–43%
   with operating margin still negative. Growth is not yet self-funding.
3. **Concentration is migrating rather than disappearing.** G42 fell from 64% of revenue a year
   earlier to 11% in Q1 2026 — but MBZUAI was 63% in the same quarter, and three customers were
   86% of receivables at 2026-03-31. The OpenAI agreement (750MW, >$20B, inside a ~$25B stated
   backlog) is the growth engine and the single largest concentration risk at once. The AWS
   Trainium-3-prefill / CS-3-decode partnership is largely a 2027 revenue story.

Balance sheet: ~$3.3B cash and equivalents at the end of Q1 *before* IPO proceeds landed, plus a
$1B working-capital loan from OpenAI. Funding risk is low for now; dilution risk is not
(share count grew ~61% YoY to ~237.6M shares outstanding).

## 3. What the tape says (as of 2026-09-02)

- Last quote around **$184.94**, with the session ranging $168.70–$185.50 and the prior close at
  $172.62 — i.e. round-trip to roughly the **$185 IPO price**, and about **−52% from the
  $386.34 52-week high** ($160.81 low).
- Q2 print (2026-08-12) knocked the stock down 12–17% immediately and ~26% over the following
  week.
- Sell-side consensus is "Strong Buy" with a ~$291.64 average target (Citi $340, Mizuho $300,
  Wedbush $270, Morgan Stanley $250) — a ~58% implied gap that has, so far, been wrong in
  direction since the IPO.
- Valuation on FY2026 core revenue guidance of $880–890M: **~$44B market cap on basic shares
  ≈ 50x sales**, or **~64x** on the ~305M fully diluted count implied by the IPO valuation.
  Third-party "87x" figures reflect higher price levels earlier in the year. Whatever the exact
  multiple, it prices multi-year execution against Nvidia with negative operating margins.
- **Supply overhang is the dominant near-term technical.** Lock-ups expire on the earlier of the
  second trading day after the Q3-2026 earnings release or 180 days after the prospectus
  (~mid-November 2026), releasing roughly **171.1M shares** — comparable to the entire current
  share count and multiples of the ~30M-share IPO float. Any model trained on ordinary price
  dynamics has no way to anticipate that event.

## 4. What Kronos can and cannot add here

Kronos forecasts the *distribution of price dynamics* conditioned on recent bars. On CBRS that
is a genuinely hard setting, and the script is built to expose that rather than hide it:

- **The history is short.** Roughly 77 trading sessions exist since the 2026-05-14 IPO, versus a
  512-bar context window and the 400-bar default lookback in the repo's examples. On daily bars
  the script automatically clips the lookback to what exists; for a real context window, run it
  on hourly bars (`--interval 60m --pred-len 39`).
- **Post-IPO price discovery is not stationary.** A +108% first day, a −52% drawdown and an
  earnings gap inside 4 months means the normalization statistics Kronos computes over the
  context window are dominated by a regime that may not repeat.
- **Scheduled events dominate.** The lock-up release and the Q3 print are the two largest
  expected moves in the horizon, and neither is in the price series.

Practical consequences, encoded in the script:

- Never read the median path alone. Read `quantile_bands`, `terminal_return.p05/p95` and
  `prob_close_above_last`.
- The holdout backtest is the gate: `rmse_skill_vs_baseline` must be positive (the model beat a
  flat last-close forecast) and `p10_p90_coverage` should sit near 0.80. On a series this noisy,
  a negative skill score is a normal and informative result — it means use the bands as a
  volatility estimate and discard the direction.
- Ensemble dispersion is generated by replicating the series across the batch dimension with
  `sample_count=1`, because `KronosPredictor.predict` averages its internal samples and would
  otherwise collapse exactly the dispersion being measured.

## 5. Running it

```shell
pip install -r requirements.txt
pip install yfinance            # only needed for the download path

# 21 trading days ahead, 64 sample paths, full post-IPO history
python examples/cbrs_cerebras_analysis.py --pred-len 21 --n-paths 64

# hourly bars give Kronos a real context window
python examples/cbrs_cerebras_analysis.py --interval 60m --start 2026-06-01 \
    --pred-len 39 --lookback 480 --n-paths 64

# offline / air-gapped: bring your own OHLCV file, technical snapshot only
python examples/cbrs_cerebras_analysis.py --csv data/CBRS_daily.csv --no-forecast
```

Outputs land in `--outdir` (default `cbrs_output/`): a JSON report with the technical snapshot,
backtest scorecard and forecast distribution, plus a fan-chart PNG.

## Sources

- [Robinhood — CBRS quote](https://robinhood.com/us/en/stocks/CBRS/)
- [stockanalysis.com — CBRS overview](https://stockanalysis.com/stocks/cbrs/) and
  [statistics](https://stockanalysis.com/stocks/cbrs/statistics/)
- [Cerebras Q1 2026 results](https://investors.cerebras.ai/news-releases/news-release-details/cerebras-systems-announces-strong-first-quarter-2026-results)
- [Form 10-Q, quarter ended 2026-06-30](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026056357/cbrs-20260630.htm)
- [Form 10-Q, quarter ended 2026-03-31](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026044981/cbrs-20260331.htm)
- [Form 424B4 (IPO prospectus)](https://www.sec.gov/Archives/edgar/data/0002021728/000162828026035214/cerebras-424b4.htm)
- [CNBC — Q2 2026 earnings](https://www.cnbc.com/2026/08/12/cerebras-cbrs-q2-earnings-report-2026.html)
- [TechCrunch — IPO raise and pricing](https://techcrunch.com/2026/05/14/cerebras-raises-5-5b-kicking-off-2026s-ipo-season-with-a-bang/)
- [MarketBeat — analyst forecasts](https://www.marketbeat.com/stocks/NASDAQ/CBRS/forecast/)
- [Seeking Alpha — IPO lock-up timing](https://seekingalpha.com/article/4905797-cerebras-ipo-lockup-comes-fast)
