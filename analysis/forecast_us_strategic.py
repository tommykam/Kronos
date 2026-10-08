import os, sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import pandas as pd, numpy as np, yfinance as yf, torch
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from model import Kronos, KronosTokenizer, KronosPredictor

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
TICKERS = {"5401.T": "Nippon Steel", "INTC": "Intel", "MP": "MP Materials", "LAC": "Lithium Americas"}
LOOKBACK, PRED, SAMPLES = 400, 20, 20
torch.manual_seed(0); np.random.seed(0)

tok = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
mdl = Kronos.from_pretrained("NeoQuasar/Kronos-base")
pred = KronosPredictor(mdl, tok, device="cpu", max_context=512)

fig, axes = plt.subplots(2, 2, figsize=(14, 9)); rows = []
for ax, (t, name) in zip(axes.flat, TICKERS.items()):
    h = yf.Ticker(t).history(period="3y", interval="1d", auto_adjust=True)
    h = h.rename(columns=str.lower)[["open","high","low","close","volume"]].dropna()
    h["amount"] = h["volume"] * h[["open","high","low","close"]].mean(axis=1)
    h = h.tail(LOOKBACK); idx = h.index.tz_localize(None)
    future = pd.bdate_range(idx[-1] + pd.Timedelta(days=1), periods=PRED)
    paths = []
    for s in range(SAMPLES):
        p = pred.predict(df=h.reset_index(drop=True), x_timestamp=pd.Series(idx), y_timestamp=pd.Series(future),
                         pred_len=PRED, T=1.0, top_p=0.9, sample_count=1, verbose=False)
        paths.append(p["close"].values)
    paths = np.array(paths); last = h["close"].iloc[-1]
    med, lo, hi = np.median(paths,0), np.percentile(paths,10,0), np.percentile(paths,90,0)
    rows.append(dict(name=name, ticker=t, last_date=idx[-1].date(), last=round(last,2),
                     median_20d=round(med[-1],2), chg_pct=round((med[-1]/last-1)*100,1),
                     p10=round(lo[-1],2), p90=round(hi[-1],2), prob_up=round((paths[:,-1]>last).mean()*100)))
    ax.plot(idx[-120:], h["close"].values[-120:], color="#1f4e79", lw=1.4, label="History")
    ax.plot(future, med, color="#c0392b", lw=1.6, label="Kronos median")
    ax.fill_between(future, lo, hi, color="#c0392b", alpha=.2, label="10–90% band")
    ax.set_title(f"{name} ({t})"); ax.grid(alpha=.3); ax.legend(fontsize=8, loc="upper left")
    print(rows[-1], flush=True)
plt.tight_layout(); plt.savefig(f"{OUT}/kronos_forecast.png", dpi=110)
pd.DataFrame(rows).to_csv(f"{OUT}/kronos_forecast.csv", index=False)
print(pd.DataFrame(rows).to_string(index=False))
