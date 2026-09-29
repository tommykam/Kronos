"""Kronos forecast + holdout check for a list of US tickers (daily bars from Yahoo)."""
import sys, os, json
import numpy as np, pandas as pd, yfinance as yf, torch
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from model import Kronos, KronosTokenizer, KronosPredictor

TICKERS = sys.argv[1:] or ["HIVE", "FRMI", "HOST"]
PRED_LEN, N_PATHS, LOOKBACK = 20, 30, 400
OUT = os.path.dirname(os.path.abspath(__file__))
torch.manual_seed(0); np.random.seed(0)

tok = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
mdl = Kronos.from_pretrained("NeoQuasar/Kronos-small")
pred = KronosPredictor(mdl, tok, device="cpu", max_context=512)

def load(t):
    d = yf.download(t, period="5y", interval="1d", progress=False, auto_adjust=True)
    d.columns = [c[0].lower() if isinstance(c, tuple) else c.lower() for c in d.columns]
    d = d[["open", "high", "low", "close", "volume"]].dropna()
    d = d[d.volume > 0]
    d["amount"] = d.volume * d[["open", "high", "low", "close"]].mean(axis=1)
    d.index.name = "timestamps"
    return d.reset_index()

def paths(df, fut_ts):
    x = df[["open", "high", "low", "close", "volume", "amount"]]
    out = []
    for _ in range(N_PATHS):
        p = pred.predict(x, df.timestamps, pd.Series(fut_ts), PRED_LEN, T=1.0, top_p=0.9, sample_count=1, verbose=False)
        out.append(p.close.values)
    return np.array(out)

report = {}
for t in TICKERS:
    df = load(t)
    n = len(df)
    ctx = df.iloc[-LOOKBACK:].reset_index(drop=True)
    last = ctx.close.iloc[-1]
    fut = pd.bdate_range(ctx.timestamps.iloc[-1] + pd.Timedelta(days=1), periods=PRED_LEN)
    P = paths(ctx, fut)
    end = P[:, -1] / last - 1

    # holdout: forecast the last PRED_LEN known days from the bars before them
    hctx = df.iloc[-LOOKBACK - PRED_LEN:-PRED_LEN].reset_index(drop=True)
    htrue = df.close.iloc[-PRED_LEN:].values
    H = paths(hctx, df.timestamps.iloc[-PRED_LEN:].values)
    hmed = np.median(H, axis=0); hbase = hctx.close.iloc[-1]
    in_band = float(np.mean((htrue >= np.percentile(H, 10, 0)) & (htrue <= np.percentile(H, 90, 0))))

    r = np.log(df.close).diff().dropna()
    report[t] = dict(
        bars=n, first=str(df.timestamps.iloc[0].date()), last_date=str(ctx.timestamps.iloc[-1].date()), last_close=round(float(last), 3),
        ret_1m=round(float(df.close.iloc[-1] / df.close.iloc[-22] - 1), 4) if n > 22 else None,
        ret_3m=round(float(df.close.iloc[-1] / df.close.iloc[-64] - 1), 4) if n > 64 else None,
        ret_1y=round(float(df.close.iloc[-1] / df.close.iloc[-253] - 1), 4) if n > 253 else None,
        ann_vol_60d=round(float(r.iloc[-60:].std() * np.sqrt(252)), 4),
        max_drawdown_1y=round(float((df.close.iloc[-252:] / df.close.iloc[-252:].cummax() - 1).min()), 4),
        avg_dollar_vol_20d=round(float(df.amount.iloc[-20:].mean())),
        fc_median_20d=round(float(np.median(end)), 4), fc_p10=round(float(np.percentile(end, 10)), 4),
        fc_p90=round(float(np.percentile(end, 90)), 4), fc_prob_up=round(float(np.mean(end > 0)), 3),
        holdout_pred_ret=round(float(hmed[-1] / hbase - 1), 4), holdout_true_ret=round(float(htrue[-1] / hbase - 1), 4),
        holdout_mape=round(float(np.mean(np.abs(hmed - htrue) / htrue)), 4), holdout_in_p10_p90=round(in_band, 3),
    )
    print(t, json.dumps(report[t]), flush=True)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 4))
    h = df.iloc[-120:]
    a1.plot(h.timestamps, h.close, "k", lw=1.2, label="history")
    a1.fill_between(fut, np.percentile(P, 10, 0), np.percentile(P, 90, 0), color="C0", alpha=.25, label="p10–p90")
    a1.plot(fut, np.median(P, 0), "C0", lw=1.5, label="median forecast")
    a1.set_title(f"{t}: next {PRED_LEN} trading days"); a1.legend(); a1.grid(alpha=.3)
    ht = df.timestamps.iloc[-PRED_LEN:]
    a2.plot(df.timestamps.iloc[-80:], df.close.iloc[-80:], "k", lw=1.2, label="actual")
    a2.fill_between(ht, np.percentile(H, 10, 0), np.percentile(H, 90, 0), color="C1", alpha=.25)
    a2.plot(ht, hmed, "C1", lw=1.5, label="holdout forecast")
    a2.set_title(f"{t}: holdout (last {PRED_LEN} days)"); a2.legend(); a2.grid(alpha=.3)
    fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(os.path.join(OUT, f"{t}_forecast.png"), dpi=110); plt.close(fig)

json.dump(report, open(os.path.join(OUT, "report.json"), "w"), indent=2)
