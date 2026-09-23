"""
Forecast daily K-lines for a US-listed stock with Kronos.

Defaults to McDonald's (NYSE: MCD). Data is pulled from Yahoo Finance via
`yfinance`, or read from a local CSV with `--csv` for offline use.

Examples:
    python prediction_us_stock.py                       # forecast MCD 20 trading days ahead
    python prediction_us_stock.py --backtest            # hold out the last 20 days and compare
    python prediction_us_stock.py --ticker AAPL --pred-len 10
    python prediction_us_stock.py --csv ./data/MCD.csv  # columns: timestamps/date, open, high, low, close, volume

Requires: pip install yfinance (only when --csv is not given)
"""
import argparse
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from model import Kronos, KronosTokenizer, KronosPredictor

MODELS = {
    "mini": ("NeoQuasar/Kronos-mini", "NeoQuasar/Kronos-Tokenizer-2k", 2048),
    "small": ("NeoQuasar/Kronos-small", "NeoQuasar/Kronos-Tokenizer-base", 512),
    "base": ("NeoQuasar/Kronos-base", "NeoQuasar/Kronos-Tokenizer-base", 512),
}
# Approximates the NYSE calendar (federal holidays; ignores Good Friday and ad-hoc closures).
US_TRADING_DAY = CustomBusinessDay(calendar=USFederalHolidayCalendar())


def fetch_yahoo(ticker, period):
    try:
        import yfinance as yf
    except ImportError:
        sys.exit("yfinance is not installed. Run `pip install yfinance` or pass --csv.")

    raw = yf.download(ticker, period=period, interval="1d", auto_adjust=True, progress=False)
    if raw.empty:
        sys.exit(f"No data returned for {ticker}.")
    if isinstance(raw.columns, pd.MultiIndex):  # newer yfinance returns (field, ticker) columns
        raw.columns = raw.columns.get_level_values(0)

    df = raw.rename(columns=str.lower).reset_index().rename(columns={"Date": "timestamps"})
    return df[["timestamps", "open", "high", "low", "close", "volume"]]


def load_csv(path):
    df = pd.read_csv(path)
    df.columns = [c.lower() for c in df.columns]
    if "timestamps" not in df.columns:
        df = df.rename(columns={"date": "timestamps"})
    return df


def prepare(df):
    df = df.copy()
    df["timestamps"] = pd.to_datetime(df["timestamps"]).dt.tz_localize(None)
    df = df.dropna(subset=["open", "high", "low", "close"]).sort_values("timestamps")
    if "amount" not in df.columns:
        # Kronos expects a turnover column; dollar volume is a close proxy.
        df["amount"] = df["close"] * df["volume"]
    return df.reset_index(drop=True)


def plot(ticker, history, pred_df, actual=None, out_path=None):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, gridspec_kw={"height_ratios": [3, 1]})

    ax1.plot(history["timestamps"], history["close"], label="History", color="tab:blue", linewidth=1.3)
    if actual is not None:
        ax1.plot(actual["timestamps"], actual["close"], label="Actual", color="tab:green", linewidth=1.3)
    ax1.plot(pred_df.index, pred_df["close"], label="Kronos forecast", color="tab:red", linewidth=1.5)
    ax1.set_title(f"{ticker} daily close: Kronos forecast")
    ax1.set_ylabel("Close (USD)")
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3)

    ax2.bar(history["timestamps"], history["volume"], color="tab:blue", width=1.0)
    if actual is not None:
        ax2.bar(actual["timestamps"], actual["volume"], color="tab:green", width=1.0)
    ax2.bar(pred_df.index, pred_df["volume"], color="tab:red", width=1.0, alpha=0.7)
    ax2.set_ylabel("Volume")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    if out_path:
        plt.savefig(out_path, dpi=120)
        print(f"Saved chart to {out_path}")
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ticker", default="MCD", help="Ticker symbol (default: MCD, McDonald's)")
    parser.add_argument("--csv", help="Local OHLCV CSV instead of downloading from Yahoo Finance")
    parser.add_argument("--period", default="5y", help="Yahoo Finance history period (default: 5y)")
    parser.add_argument("--model", choices=MODELS, default="small")
    parser.add_argument("--lookback", type=int, default=400, help="Context length in trading days")
    parser.add_argument("--pred-len", type=int, default=20, help="Trading days to forecast")
    parser.add_argument("--samples", type=int, default=5, help="Sample paths averaged into the forecast")
    parser.add_argument("--T", type=float, default=1.0, help="Sampling temperature")
    parser.add_argument("--top-p", type=float, default=0.9)
    parser.add_argument("--device", default=None, help="e.g. cpu, cuda:0 (auto-detected if omitted)")
    parser.add_argument("--backtest", action="store_true", help="Hold out the last --pred-len days and score the forecast")
    parser.add_argument("--out-dir", default="./outputs", help="Where to write the forecast CSV and chart")
    parser.add_argument("--show", action="store_true", help="Show the chart instead of saving it")
    args = parser.parse_args()

    model_id, tokenizer_id, max_context = MODELS[args.model]
    lookback = min(args.lookback, max_context)
    ticker = args.ticker.upper()

    df = prepare(load_csv(args.csv) if args.csv else fetch_yahoo(ticker, args.period))

    if args.backtest:
        history, actual = df.iloc[:-args.pred_len], df.iloc[-args.pred_len:]
        y_timestamp = actual["timestamps"].reset_index(drop=True)
    else:
        history, actual = df, None
        future = pd.date_range(df["timestamps"].iloc[-1], periods=args.pred_len + 1, freq=US_TRADING_DAY)[1:]
        y_timestamp = pd.Series(future)

    context = history.iloc[-lookback:].reset_index(drop=True)
    if len(context) < lookback:
        print(f"Only {len(context)} days of history available; using all of it as context.")
    print(f"{ticker}: {len(context)} days of context "
          f"({context['timestamps'].iloc[0].date()} to {context['timestamps'].iloc[-1].date()}), "
          f"forecasting {args.pred_len} trading days with Kronos-{args.model}")

    tokenizer = KronosTokenizer.from_pretrained(tokenizer_id)
    model = Kronos.from_pretrained(model_id)
    predictor = KronosPredictor(model, tokenizer, device=args.device, max_context=max_context)

    pred_df = predictor.predict(
        df=context[["open", "high", "low", "close", "volume", "amount"]],
        x_timestamp=context["timestamps"],
        y_timestamp=y_timestamp,
        pred_len=args.pred_len,
        T=args.T,
        top_p=args.top_p,
        sample_count=args.samples,
        verbose=True,
    )

    last_close = context["close"].iloc[-1]
    final_close = pred_df["close"].iloc[-1]
    print(f"\nLast close {last_close:.2f} -> forecast close {final_close:.2f} on "
          f"{pred_df.index[-1].date()} ({(final_close / last_close - 1) * 100:+.2f}%)")

    if actual is not None:
        actual_close = actual["close"].to_numpy()
        pred_close = pred_df["close"].to_numpy()
        mape = (abs(pred_close - actual_close) / actual_close).mean() * 100
        hit = ((pred_close[-1] > last_close) == (actual_close[-1] > last_close))
        print(f"Backtest: MAPE {mape:.2f}%, actual final close {actual_close[-1]:.2f}, "
              f"direction {'correct' if hit else 'wrong'}")

    os.makedirs(args.out_dir, exist_ok=True)
    suffix = "backtest" if args.backtest else "forecast"
    csv_path = os.path.join(args.out_dir, f"{ticker}_{suffix}.csv")
    pred_df.to_csv(csv_path, index_label="timestamps")
    print(f"Saved forecast to {csv_path}")

    plot(ticker, context.iloc[-120:], pred_df, actual,
         out_path=None if args.show else os.path.join(args.out_dir, f"{ticker}_{suffix}.png"))


if __name__ == "__main__":
    main()
