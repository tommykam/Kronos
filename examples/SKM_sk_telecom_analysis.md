# SK Telecom (NYSE ADR: SKM / KRX: 017670) — analysis notes

Twelfth ticker studied with [`cbrs_cerebras_analysis.py`](./cbrs_cerebras_analysis.py). Compiled
2026-09-04 from public sources. **Research notes, not investment advice.**

Read alongside the [EWY notes](./EWY_korea_etf_analysis.md) — with one correction carried over,
in §1.

## 1. First, a correction if you came here from EWY

The EWY notes flagged that ~49% of that ETF is Samsung, SK hynix and **SK Square**, where SK
Square is the holding company for the SK hynix stake.

**SK Telecom is not that.** It is a separate SK Group affiliate; SK Square was spun *out of* SK
Telecom in 2021 and took the semiconductor assets with it. **Owning SKM gives you no SK hynix
exposure.** If you are building Korea exposure across EWY and SKM expecting to double down on
memory, you are not — you are buying a telecom with a data-centre option attached, which is a
genuinely different and largely uncorrelated bet inside the same corporate group.

The one indirect link: SKT committed ~$480M (KRW 738.4B) to SK hynix's US AI investment vehicle.
Real, but immaterial against a $13.9B market cap.

## 2. Q2 2026 — read the revenue line, not the profit line

| | Q2 2026 |
|---|---|
| Revenue | **KRW 4.3591T (~$3.18B), +0.5% YoY** |
| Operating income | **KRW 566.0B (~$0.41B), +67.3% YoY** |
| AI data centre revenue | KRW 136.2B (~$99M), **+92.5%** |

**The 67% profit growth is a base effect, not an acceleration.** In April 2025 SK Telecom
suffered a breach exposing SIM authentication keys, IMSI and phone numbers for **23.2 million
subscribers** — attackers had been inside since 2021. It drew a **record KRW 134.8B (~$97.2M)
privacy fine**, free SIM replacement for the entire customer base, dealer compensation and
subscriber losses. That wrecked the 2025 earnings base, and Q2 2026 is lapping it.

The honest summary of the quarter: **revenue +0.5%.** The telecom business is flat. The profit
recovery is real cash but it is a comparison against a disaster, not evidence of a new growth
rate.

**The same distortion runs through the multiple.** SKM's trailing P/E of ~58x looks like an AI
premium; much of it is simply a depressed denominator from the breach year. This is the mirror
image of the [AMZN](./AMZN_amazon_analysis.md) situation in this collection — there, a one-off
*gain* inflated E and made a ~34x stock screen at ~20x; here a one-off *hit* deflated E and makes
a telecom screen at ~58x. In both cases the screen number is an accounting artifact and the fix
is the same: rebuild the denominator on a clean year.

**And AI data centres are 3.1% of revenue.** Growing 92.5%, but off a base that cannot move a
KRW 4.36T quarter yet.

## 3. The AI pivot: what is actually committed, and by whom

Two entities, easily confused:

- **SK Hyper** — business development (land, substations, construction, customer acquisition).
  SKT commitment: **KRW 750B (~$548M) by 2030**. Targets **5GW phased from 2029** and **15GW by
  2035**.
- **SK Horizon** — the operating company, split out of SK Broadband, holding existing AIDCs and
  submarine cables.

**The KKR deal is the most valuable number here.** KKR and an IMM Investment / Stonebridge
consortium are investing **$2.23B (KRW 3.08T) for 29% + 20% = 49%** of SK Horizon, with SKT
retaining **51%** and control.

That implies:

| | |
|---|---|
| Implied SK Horizon valuation | **~$4.55B** ($2.23B ÷ 49%) |
| SKT's retained 51% | **~$2.32B** |
| As a share of SKT's $13.93B market cap | **~17%** |

This is an arm's-length price set by sophisticated outside capital, not a management projection —
which makes it the single most reliable input available for a sum-of-the-parts on this stock.

**Now the reality check on 15GW.** SKT's own committed capital is KRW 750B (~$548M). Building
15GW costs, at $10–20M per MW, somewhere between **$150B and $300B** — reported headline figures
for the Korean buildout run to ~$653B. **SKT's commitment is roughly 0.2–0.4% of the capital
required.**

That is not a gotcha; it is the *structure*. SKT is building this **off its own balance sheet
using partner capital**, keeping 51% and control while KKR and others fund it. That is the right
way for a company with a $13.9B market cap to chase a multi-hundred-billion-dollar buildout. But
it has a direct consequence for shareholders: **SKT captures a minority-diluted share of the
upside**, and the equity story depends on repeatedly finding partners willing to fund the next
phase at good terms.

And the timeline is long: **5GW phased from 2029, 15GW by 2035** — three and nine years out.
Nothing in today's numbers.

## 4. The Anthropic stake — the part a telecom screen never shows

SK Telecom invested **$100M in Anthropic in August 2023** (following an earlier investment via
SKTVC, its Silicon Valley venture arm), alongside a partnership to build a telco-customised
multilingual LLM. That bought roughly **2%** of Anthropic at the time; later issuance rounds have
diluted it to about **0.3%**.

Carried at a book value near **KRW 1.3T (~$970M)**, third-party estimates of current worth range
from **$1.0B to $2.6B** — a **10x to 26x** return on $100M in under three years. Reporting says
SKT **added to the position rather than exiting** ahead of the IPO.

Against SKT's ~$13.93B market cap:

| Assumed stake value | Share of SKM market cap | Anthropic exposure per $10,000 |
|---|---|---|
| $0.97B (book) | 7.0% | $696 |
| $1.0B (low estimate) | 7.2% | $718 |
| $2.0B (mid) | **14.4%** | **$1,436** |
| $2.6B (high / post-IPO) | 18.7% | $1,866 |

For comparison, Amazon's $190.4B stake against a $2.75T cap is **6.9%**, i.e. **$692 per
$10,000**. So at the middle of the estimate range **SKM carries roughly 2x the Anthropic exposure
per dollar that AMZN does** — and unlike a pre-IPO fund there is no NAV premium and no management
fee, plus a ~2.95% dividend while you wait.

**Four things keep this from being a free lunch:**

1. **The estimate range is a 2.6x spread.** $1.0B and $2.6B are third-party guesses against a
   private cap table that is not public. The company's own book value (~$970M) sits at the bottom
   of that range. Size the position off the *low* end.
2. **0.3% is small and has already been diluted heavily** — 2% to 0.3% in under three years
   through later rounds. Further issuance, including at IPO, dilutes it again.
3. **The gain is unrealised and sits in other comprehensive income**, not in net income. It never
   flows through reported earnings unless SKT sells — and if SKT sells, the exposure you bought
   the stock for is gone. The value reaches you only via a sum-of-the-parts re-rating, or a sale
   you would not want.
4. **This is not undiscovered.** SKM has already risen sharply on Anthropic-stake valuation news
   at least once. Whatever is left is a bet that the market still under-weights it, not a secret.

And the obvious point: at the mid estimate you are paying for **~86% flat Korean telecom** to own
**~14% Anthropic**. Section 2's revenue line (+0.5%) is what that 86% does.

## 5. The tape and the shape of the bet

- ADR **$34.88** (Aug 6, 2026), market cap **~$13.93B**. 52-week range **$19.66–$47.18** — a 2.4x
  span; **~26% below the high**, ~77% above the low.
- Dividend yield **~2.95%**, quarterly dividend held at KRW 830/share.
- Analyst average target ~$35.92 (range $31.00–$44.70) — essentially spot. Unlike most names in
  this collection, the sell-side is *not* pricing in large upside here.

So the bet decomposes cleanly into three parts, which is unusually legible:

1. **A flat, cash-generative Korean telecom** paying ~3%, with a repaired but reputationally
   damaged subscriber base.
2. **A ~$2.3B stake in an AI data-centre platform** that outside investors just priced — roughly
   17% of market cap, growing 92.5% but only 3.1% of revenue.
3. **A free option on 5–15GW** that requires capital SKT does not have and partners it must keep
   finding, paying off from 2029 at the earliest.
4. **A ~0.3% stake in Anthropic** worth an estimated $1.0–2.6B, or 7–19% of market cap — see §4.

If you want AI infrastructure exposure, the [EME](./EME_emcor_analysis.md) and
[STRL](./STRL_sterling_infrastructure_analysis.md) notes describe companies where that exposure
is 90%+ of the business today. SKM is a telecom with a 3% AI segment and a large, well-structured
ambition. Both can be reasonable; they are not the same trade, and the dividend plus the KKR
mark are what actually support SKM's floor.

## 6. Modelling notes

- **ADR mechanics.** SKM is an unhedged KRW-denominated claim: your USD return is the Korean
  return times the won move. USD/KRW ~1,369 with the won up ~5% in August (see the EWY notes) —
  and the won typically weakens in risk-off, so the currency and equity legs correlate in
  drawdowns.
- **Gap structure, same as EWY.** The Korean line trades while the US is closed, so most of SKM's
  daily move arrives as an overnight gap and the US session is largely arbitrage against 017670.
  Bar shapes do not mean what they mean for a US-primary listing. If you want cleaner dynamics,
  model **017670.KS** and treat the ADR as a currency-translated derivative of it.
- **Two structural breaks in recent history**: the April 2025 breach and the 2026 AI re-rating
  (a 2.4x annual range). A long lookback spans a regime where this was a defensive dividend stock
  and one where it trades as an AI infrastructure proxy. Compare a 512-bar and a 250-bar context.
- Lower expected volatility than EWY, higher than a US utility. Coverage near 0.80 is plausible
  here in a way it is not for CBRS, NNE, PCT or ASST.

```shell
python examples/cbrs_cerebras_analysis.py --ticker SKM --start 2015-01-01 \
    --pred-len 21 --n-paths 128 --outdir skm_output
```

## Sources

- [SK Telecom — Q2 2026 results](https://news.sktelecom.com/en/3218) and [Q1 2026 results](https://news.sktelecom.com/en/3039)
- [Investing.com — Q2 2026 slides, profit +67% on AI growth](https://www.investing.com/news/company-news/sk-telecom-q2-2026-slides-profit-surges-67-on-ai-growth-93CH-4836560)
- [Fierce Network — AI data-centre revenue +92.5%](https://www.fierce-network.com/cloud/sk-telecoms-ai-data-center-bet-gains-traction-925-revenue-growth)
- [SK Telecom — SK Horizon launch with KKR and IMM](https://news.sktelecom.com/en/3290) and the [PR Newswire release](https://www.prnewswire.com/news-releases/sk-telecom-launches-ai-data-center-infrastructure-company-sk-horizon-and-secures-investments-from-kkr-and-imm-302861694.html)
- [Investment Monitor — KKR/IMM $2.23bn for 49%](https://www.investmentmonitor.ai/news/kkr-imm-aidc-company-investment/)
- [Fierce Network — SK Hyper and the 15GW plan](https://www.fierce-network.com/cloud/sk-telecom-spins-sk-hyper-15gw-ai-data-center-buildout)
- [Form 6-K — 15GW long-term AI data centre plan](https://www.stocktitan.net/sec-filings/SKM/6-k-sk-telecom-co-ltd-current-report-foreign-issuer-6b95e0cd5f54.html)
- [Korea Herald — record privacy fine over the data breach](https://www.koreaherald.com/article/10563945)
- [CPO Magazine — breach detail, 23.2M affected](https://www.cpomagazine.com/data-protection/sk-telecom-hit-with-a-record-data-breach-fine-over-cybersecurity-failures-exposing-23-2m-people/)
- [SK Telecom — $100M investment in Anthropic (2023)](https://news.sktelecom.com/en/699)
- [Anthropic — SKT partnership announcement](https://www.anthropic.com/news/skt-partnership-announcement)
- [UPI — Anthropic IPO lifts outlook for the SK Telecom stake](https://www.upi.com/Top_News/World-News/2026/04/14/business-ipo-ai/9841776199967/)
- [Investing.com — SKM rises 12% on Anthropic stake valuation](https://www.investing.com/news/analyst-ratings/sk-telecom-stock-rises-12-on-anthropic-stake-valuation-93CH-4468023)
- [TechTimes — SKT adds to the stake ahead of the IPO](https://www.techtimes.com/articles/318131/20260610/sk-telecom-adds-anthropic-stake-rather-exit-ahead-965-billion-ipo.htm)
- [Investing.com — SKM quote](https://www.investing.com/equities/sk-telecom)
