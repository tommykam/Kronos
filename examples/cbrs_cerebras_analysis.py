"""Kronos-based forecast and risk analysis for Cerebras Systems (NASDAQ: CBRS).

The script runs a full, reproducible pipeline on a single ticker:

1. Load daily (or intraday) OHLCV bars, either from a CSV file or from Yahoo
   Finance via the optional ``yfinance`` package.
2. Compute a technical snapshot of the history (returns, realized volatility,
   ATR, RSI, drawdown, moving-average distances, liquidity).
3. Optionally run a walk-forward holdout: hide the last ``pred_len`` bars,
   forecast them with Kronos and score the forecast against the realized bars
   and against a random-walk baseline. A forecast that cannot beat a flat
   last-close baseline is not worth trading on, so this section is the
   calibration gate for everything below it.
4. Draw an ensemble of independent Kronos sample paths and turn them into
   quantile bands, a terminal-price distribution and probability estimates.
5. Write a JSON report and a fan-chart PNG.

CBRS is a young, high-volatility listing (IPO 2026-05-14): the usable history
is short and post-IPO price discovery is unusually noisy, so the holdout
metrics and the width of the ensemble bands matter more than the median path.

Examples
--------
    # Download the full post-IPO history and forecast 21 trading days ahead
    python examples/cbrs_cerebras_analysis.py --pred-len 21 --n-paths 64

    # Use a local CSV and skip the model (technical snapshot only)
    python examples/cbrs_cerebras_analysis.py --csv data/CBRS_daily.csv --no-forecast

This is research tooling, not investment advice.
"""

import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PRICE_COLS = ["open", "high", "low", "close"]
FEATURE_COLS = PRICE_COLS + ["volume", "amount"]
TRADING_DAYS_PER_YEAR = 252


# --------------------------------------------------------------------------- #
# Data loading
# --------------------------------------------------------------------------- #
def _to_numeric(series):
    """Coerce a column that may carry currency symbols or thousands separators."""
    if series.dtype.kind in "if":
        return series.astype(float)
    cleaned = (
        series.astype(str)
        .str.replace(r"[,$\s]", "", regex=True)
        .str.replace("−", "-", regex=False)
        .replace({"": np.nan, "-": np.nan, "nan": np.nan, "None": np.nan})
    )
    return pd.to_numeric(cleaned, errors="coerce")


def load_from_csv(path):
    """Load OHLCV bars from a CSV, tolerating common column-name variants."""
    df = pd.read_csv(path)
    df.columns = [str(c).strip().lower() for c in df.columns]

    aliases = {
        "timestamps": ["timestamps", "timestamp", "date", "datetime", "time", "trade_date"],
        "open": ["open", "open_price"],
        "high": ["high", "high_price"],
        "low": ["low", "low_price"],
        "close": ["close", "close_price", "adj close", "adj_close", "closing price"],
        "volume": ["volume", "vol", "turnover_volume"],
        "amount": ["amount", "turnover", "money"],
    }

    out = pd.DataFrame()
    for target, candidates in aliases.items():
        for candidate in candidates:
            if candidate in df.columns:
                out[target] = df[candidate]
                break
        if target not in out.columns and target in PRICE_COLS + ["timestamps"]:
            raise ValueError(f"CSV {path} is missing a '{target}' column (tried {candidates}).")

    out["timestamps"] = pd.to_datetime(out["timestamps"])
    for col in PRICE_COLS + [c for c in ["volume", "amount"] if c in out.columns]:
        out[col] = _to_numeric(out[col])

    return out


def load_from_yfinance(ticker, start, end, interval):
    """Download bars with yfinance. Kept optional so the CSV path has no deps."""
    try:
        import yfinance as yf
    except ImportError as exc:  # pragma: no cover - depends on the environment
        raise SystemExit(
            "yfinance is not installed. Install it (`pip install yfinance`) or pass "
            "--csv with a local OHLCV file."
        ) from exc

    raw = yf.download(
        ticker, start=start, end=end, interval=interval,
        auto_adjust=False, progress=False,
    )
    if raw is None or raw.empty:
        raise SystemExit(f"No data returned for {ticker}. Check the ticker and date range.")

    if isinstance(raw.columns, pd.MultiIndex):  # yfinance returns (field, ticker)
        raw.columns = raw.columns.get_level_values(0)

    raw = raw.rename(columns={c: str(c).strip().lower() for c in raw.columns})
    out = pd.DataFrame({"timestamps": pd.to_datetime(raw.index)})
    for col in PRICE_COLS + ["volume"]:
        if col not in raw.columns:
            raise SystemExit(f"Downloaded data for {ticker} has no '{col}' column.")
        out[col] = raw[col].to_numpy(dtype=float)
    return out


def prepare_frame(df):
    """Sort, de-duplicate, drop incomplete bars and derive `amount` if absent."""
    df = df.dropna(subset=PRICE_COLS).copy()
    df = df.sort_values("timestamps").drop_duplicates(subset="timestamps", keep="last")

    if "volume" not in df.columns:
        df["volume"] = 0.0
    df["volume"] = df["volume"].fillna(0.0)
    if "amount" not in df.columns or df["amount"].isna().all():
        # Dollar volume proxy: typical price * share volume.
        df["amount"] = df[PRICE_COLS].mean(axis=1) * df["volume"]
    df["amount"] = df["amount"].fillna(0.0)

    return df.reset_index(drop=True)


def infer_bar_spacing(timestamps):
    """Median spacing between bars, used for annualization and future stamps."""
    deltas = pd.Series(timestamps).diff().dropna()
    if deltas.empty:
        raise SystemExit("Need at least two bars to infer the sampling frequency.")
    return deltas.median()


def periods_per_year(spacing):
    if spacing >= pd.Timedelta(days=1):
        return float(TRADING_DAYS_PER_YEAR)
    # Intraday: ~6.5 trading hours per session.
    bars_per_session = pd.Timedelta(hours=6.5) / spacing
    return float(TRADING_DAYS_PER_YEAR * max(bars_per_session, 1.0))


def make_future_timestamps(last_timestamp, pred_len, spacing):
    """Future bar stamps: business days for daily data, fixed spacing intraday."""
    if spacing >= pd.Timedelta(days=1):
        stamps = pd.bdate_range(start=last_timestamp + pd.Timedelta(days=1), periods=pred_len)
    else:
        stamps = pd.date_range(start=last_timestamp + spacing, periods=pred_len, freq=spacing)
    return pd.Series(stamps, name="timestamps")


# --------------------------------------------------------------------------- #
# Technical analytics
# --------------------------------------------------------------------------- #
def max_drawdown(closes):
    closes = np.asarray(closes, dtype=float)
    if closes.size == 0:
        return 0.0
    running_max = np.maximum.accumulate(closes)
    return float(np.min(closes / running_max - 1.0))


def rsi(closes, window=14):
    closes = pd.Series(np.asarray(closes, dtype=float))
    if len(closes) <= window:
        return None
    delta = closes.diff()
    gain = delta.clip(lower=0.0).ewm(alpha=1.0 / window, adjust=False).mean()
    loss = (-delta.clip(upper=0.0)).ewm(alpha=1.0 / window, adjust=False).mean()
    last_loss = loss.iloc[-1]
    if last_loss == 0:
        return 100.0
    rs = gain.iloc[-1] / last_loss
    return float(100.0 - 100.0 / (1.0 + rs))


def average_true_range(df, window=14):
    if len(df) <= window:
        return None
    high, low = df["high"].to_numpy(float), df["low"].to_numpy(float)
    prev_close = df["close"].shift(1).to_numpy(float)
    true_range = np.nanmax(
        np.vstack([high - low, np.abs(high - prev_close), np.abs(low - prev_close)]), axis=0
    )
    return float(pd.Series(true_range).ewm(alpha=1.0 / window, adjust=False).mean().iloc[-1])


def _pct_change_over(closes, bars):
    if len(closes) <= bars:
        return None
    return float(closes[-1] / closes[-1 - bars] - 1.0)


def _realized_vol(log_returns, window, ppy):
    if window < 2 or len(log_returns) < window:
        return None
    return float(np.std(log_returns[-window:], ddof=1) * np.sqrt(ppy))


def technical_snapshot(df, ppy):
    """Descriptive statistics of the observed history (no model involved)."""
    closes = df["close"].to_numpy(float)
    log_returns = np.diff(np.log(closes))
    last_close = float(closes[-1])

    snapshot = {
        "last_close": last_close,
        "last_bar": str(df["timestamps"].iloc[-1]),
        "bars": int(len(df)),
        "return_1_bar": _pct_change_over(closes, 1),
        "return_5_bars": _pct_change_over(closes, 5),
        "return_21_bars": _pct_change_over(closes, 21),
        "return_63_bars": _pct_change_over(closes, 63),
        "return_since_first_bar": float(last_close / closes[0] - 1.0),
        "realized_vol_21_ann": _realized_vol(log_returns, 21, ppy),
        "realized_vol_63_ann": _realized_vol(log_returns, 63, ppy),
        "realized_vol_full_ann": _realized_vol(log_returns, len(log_returns), ppy),
        "max_drawdown": max_drawdown(closes),
        "rsi_14": rsi(closes, 14),
        "high_full_history": float(np.max(closes)),
        "low_full_history": float(np.min(closes)),
        "pct_below_history_high": float(last_close / np.max(closes) - 1.0),
        "pct_above_history_low": float(last_close / np.min(closes) - 1.0),
    }

    atr14 = average_true_range(df, 14)
    snapshot["atr_14"] = atr14
    snapshot["atr_14_pct_of_price"] = None if atr14 is None else float(atr14 / last_close)

    for window in (20, 50, 200):
        key = f"sma_{window}"
        if len(closes) >= window:
            sma = float(np.mean(closes[-window:]))
            snapshot[key] = sma
            snapshot[f"pct_vs_{key}"] = float(last_close / sma - 1.0)
        else:
            snapshot[key] = None
            snapshot[f"pct_vs_{key}"] = None

    if df["volume"].sum() > 0:
        recent = min(21, len(df))
        snapshot["avg_volume_21"] = float(df["volume"].tail(recent).mean())
        snapshot["avg_dollar_volume_21"] = float(df["amount"].tail(recent).mean())
    return snapshot


# --------------------------------------------------------------------------- #
# Kronos forecasting
# --------------------------------------------------------------------------- #
def build_predictor(args):
    """Import torch/Kronos lazily so the no-forecast path stays dependency-light."""
    import torch
    from model import Kronos, KronosTokenizer, KronosPredictor

    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    device = args.device
    if device is None:
        if torch.cuda.is_available():
            device = "cuda:0"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"

    tokenizer = KronosTokenizer.from_pretrained(args.tokenizer)
    model = Kronos.from_pretrained(args.model)
    model.eval()
    predictor = KronosPredictor(model, tokenizer, device=device, max_context=args.max_context)
    return predictor, device


def ensemble_paths(predictor, x_df, x_timestamp, y_timestamp, pred_len, args):
    """Draw `args.n_paths` independent Kronos sample paths.

    `KronosPredictor.predict` averages its `sample_count` draws internally, which
    destroys the very dispersion we want to measure. Replicating the series across
    the batch dimension with `sample_count=1` instead keeps each draw separate,
    because sampling is independent per batch row.
    """
    paths = []
    remaining = args.n_paths
    while remaining > 0:
        chunk = min(args.batch_size, remaining)
        pred_dfs = predictor.predict_batch(
            df_list=[x_df] * chunk,
            x_timestamp_list=[x_timestamp] * chunk,
            y_timestamp_list=[y_timestamp] * chunk,
            pred_len=pred_len,
            T=args.temperature,
            top_k=args.top_k,
            top_p=args.top_p,
            sample_count=1,
            verbose=args.verbose,
        )
        paths.extend(pred_df[FEATURE_COLS].to_numpy(dtype=float) for pred_df in pred_dfs)
        remaining -= chunk
    return np.stack(paths, axis=0)  # (n_paths, pred_len, n_features)


def forecast_summary(paths, last_close, y_timestamp, ppy, quantiles):
    """Turn the path ensemble into bands, a terminal distribution and probabilities."""
    close_idx = FEATURE_COLS.index("close")
    close_paths = paths[:, :, close_idx]  # (n_paths, pred_len)

    bands = {
        f"p{int(round(q * 100)):02d}": np.quantile(close_paths, q, axis=0).tolist()
        for q in quantiles
    }
    median_path = np.median(close_paths, axis=0)
    terminal = close_paths[:, -1]
    terminal_return = terminal / last_close - 1.0

    # Volatility of the simulated paths themselves, annualized for comparability
    # with the realized volatility in the technical snapshot.
    path_log_returns = np.diff(np.log(np.clip(close_paths, 1e-9, None)), axis=1)
    forecast_vol = float(np.mean(np.std(path_log_returns, axis=1, ddof=1)) * np.sqrt(ppy))

    path_drawdowns = [max_drawdown(path) for path in close_paths]

    return {
        "horizon_bars": int(close_paths.shape[1]),
        "horizon_start": str(y_timestamp.iloc[0]),
        "horizon_end": str(y_timestamp.iloc[-1]),
        "n_paths": int(close_paths.shape[0]),
        "last_close": float(last_close),
        "median_close_path": median_path.tolist(),
        "quantile_bands": bands,
        "timestamps": [str(ts) for ts in y_timestamp],
        "terminal_close": {
            "mean": float(np.mean(terminal)),
            "median": float(np.median(terminal)),
            "std": float(np.std(terminal, ddof=1)) if len(terminal) > 1 else 0.0,
            **{
                f"p{int(round(q * 100)):02d}": float(np.quantile(terminal, q))
                for q in quantiles
            },
        },
        "terminal_return": {
            "mean": float(np.mean(terminal_return)),
            "median": float(np.median(terminal_return)),
            "p05": float(np.quantile(terminal_return, 0.05)),
            "p95": float(np.quantile(terminal_return, 0.95)),
        },
        "prob_close_above_last": float(np.mean(terminal > last_close)),
        "prob_drawdown_worse_than_10pct": float(np.mean(np.asarray(path_drawdowns) <= -0.10)),
        "expected_max_drawdown_over_horizon": float(np.mean(path_drawdowns)),
        "forecast_vol_ann": forecast_vol,
    }


# --------------------------------------------------------------------------- #
# Holdout backtest
# --------------------------------------------------------------------------- #
def holdout_backtest(predictor, df, lookback, pred_len, args, ppy):
    """Forecast the last `pred_len` observed bars and score against reality.

    The random-walk baseline (hold the last observed close flat) is the bar the
    model has to clear: on short, noisy equity histories it is a hard one.
    """
    if len(df) < lookback + pred_len:
        return None

    split = len(df) - pred_len
    hist = df.iloc[split - lookback:split].reset_index(drop=True)
    actual = df.iloc[split:].reset_index(drop=True)

    paths = ensemble_paths(
        predictor,
        hist[FEATURE_COLS],
        hist["timestamps"],
        actual["timestamps"],
        pred_len,
        args,
    )
    close_idx = FEATURE_COLS.index("close")
    close_paths = paths[:, :, close_idx]
    median_path = np.median(close_paths, axis=0)

    actual_close = actual["close"].to_numpy(float)
    anchor = float(hist["close"].iloc[-1])
    baseline = np.full_like(actual_close, anchor)

    def _errors(pred):
        error = pred - actual_close
        return {
            "mae": float(np.mean(np.abs(error))),
            "rmse": float(np.sqrt(np.mean(error ** 2))),
            "mape": float(np.mean(np.abs(error / actual_close))),
            "terminal_abs_error": float(abs(error[-1])),
        }

    model_errors = _errors(median_path)
    baseline_errors = _errors(baseline)

    hit_rate = float(np.mean(np.sign(median_path - anchor) == np.sign(actual_close - anchor)))
    lo = np.quantile(close_paths, 0.10, axis=0)
    hi = np.quantile(close_paths, 0.90, axis=0)
    coverage = float(np.mean((actual_close >= lo) & (actual_close <= hi)))

    return {
        "lookback": int(lookback),
        "pred_len": int(pred_len),
        "window_start": str(actual["timestamps"].iloc[0]),
        "window_end": str(actual["timestamps"].iloc[-1]),
        "anchor_close": anchor,
        "model": model_errors,
        "random_walk_baseline": baseline_errors,
        "rmse_skill_vs_baseline": float(1.0 - model_errors["rmse"] / baseline_errors["rmse"]),
        "direction_hit_rate": hit_rate,
        "p10_p90_coverage": coverage,
        "realized_vol_ann_in_window": _realized_vol(
            np.diff(np.log(np.concatenate([[anchor], actual_close]))), pred_len, ppy
        ),
        "note": (
            "rmse_skill_vs_baseline > 0 means the Kronos median beat a flat "
            "last-close forecast on this window; p10_p90_coverage near 0.80 "
            "means the ensemble bands are well calibrated."
        ),
    }


# --------------------------------------------------------------------------- #
# Plot
# --------------------------------------------------------------------------- #
def plot_fan_chart(df, summary, ticker, out_path, history_bars=120):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    hist = df.tail(history_bars)
    future = pd.to_datetime(pd.Series(summary["timestamps"]))
    bands = summary["quantile_bands"]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    ax1.plot(hist["timestamps"], hist["close"], color="black", linewidth=1.4, label="History")
    if "p10" in bands and "p90" in bands:
        ax1.fill_between(future, bands["p10"], bands["p90"], color="tab:red", alpha=0.15,
                         label="Kronos p10-p90")
    if "p25" in bands and "p75" in bands:
        ax1.fill_between(future, bands["p25"], bands["p75"], color="tab:red", alpha=0.28,
                         label="Kronos p25-p75")
    ax1.plot(future, summary["median_close_path"], color="tab:red", linewidth=1.6,
             label="Kronos median")
    ax1.axhline(summary["last_close"], color="gray", linestyle="--", linewidth=0.9,
                label=f"Last close {summary['last_close']:.2f}")
    ax1.set_ylabel("Close")
    ax1.set_title(
        f"{ticker}: Kronos {summary['horizon_bars']}-bar forecast "
        f"({summary['n_paths']} paths), P(up) = {summary['prob_close_above_last']:.0%}"
    )
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(True, alpha=0.3)

    ax2.bar(hist["timestamps"], hist["volume"], color="tab:blue", alpha=0.6, width=0.8)
    ax2.set_ylabel("Volume")
    ax2.grid(True, alpha=0.3)

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Kronos forecast and risk analysis for Cerebras Systems (CBRS).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    data = parser.add_argument_group("data")
    data.add_argument("--ticker", default="CBRS", help="Ticker to download when --csv is absent.")
    data.add_argument("--csv", default=None, help="Local OHLCV CSV; skips the download.")
    data.add_argument("--start", default="2026-05-14", help="Download start date (CBRS IPO date).")
    data.add_argument("--end", default=None, help="Download end date (exclusive).")
    data.add_argument("--interval", default="1d", help="Bar interval for the download.")

    model = parser.add_argument_group("model")
    model.add_argument("--model", default="NeoQuasar/Kronos-small")
    model.add_argument("--tokenizer", default="NeoQuasar/Kronos-Tokenizer-base")
    model.add_argument("--device", default=None, help="cuda:0 / mps / cpu (auto-detected).")
    model.add_argument("--max-context", type=int, default=512)

    forecast = parser.add_argument_group("forecast")
    forecast.add_argument("--lookback", type=int, default=400,
                          help="Context bars fed to the model; clipped to the data available.")
    forecast.add_argument("--pred-len", type=int, default=21, help="Bars to forecast.")
    forecast.add_argument("--n-paths", type=int, default=64,
                          help="Independent sample paths behind the quantile bands.")
    forecast.add_argument("--batch-size", type=int, default=16,
                          help="Paths generated per forward pass; lower it if memory is tight.")
    forecast.add_argument("--temperature", "-T", type=float, default=1.0)
    forecast.add_argument("--top-p", type=float, default=0.9)
    forecast.add_argument("--top-k", type=int, default=0)
    forecast.add_argument("--seed", type=int, default=42)
    forecast.add_argument("--no-forecast", action="store_true",
                          help="Technical snapshot only; never loads torch.")
    forecast.add_argument("--no-backtest", action="store_true", help="Skip the holdout backtest.")

    output = parser.add_argument_group("output")
    output.add_argument("--outdir", default="cbrs_output")
    output.add_argument("--no-plot", action="store_true")
    output.add_argument("--verbose", action="store_true", help="Show autoregressive progress bars.")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.csv:
        df = load_from_csv(args.csv)
        source = f"csv:{args.csv}"
    else:
        df = load_from_yfinance(args.ticker, args.start, args.end, args.interval)
        source = f"yfinance:{args.ticker}:{args.interval}"
    df = prepare_frame(df)

    spacing = infer_bar_spacing(df["timestamps"])
    ppy = periods_per_year(spacing)
    print(f"Loaded {len(df)} bars for {args.ticker} "
          f"({df['timestamps'].iloc[0]} -> {df['timestamps'].iloc[-1]}, spacing {spacing}).")

    report = {
        "ticker": args.ticker,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": {
            "source": source,
            "bars": int(len(df)),
            "start": str(df["timestamps"].iloc[0]),
            "end": str(df["timestamps"].iloc[-1]),
            "median_bar_spacing": str(spacing),
            "periods_per_year": ppy,
        },
        "technical_snapshot": technical_snapshot(df, ppy),
        "backtest": None,
        "forecast": None,
        "disclaimer": (
            "Kronos output is a probabilistic simulation of price dynamics, not a "
            "statement about company fundamentals or a recommendation to trade."
        ),
    }

    os.makedirs(args.outdir, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = os.path.join(args.outdir, f"{args.ticker}_kronos_analysis_{stamp}.json")

    if not args.no_forecast:
        lookback = min(args.lookback, args.max_context)
        if len(df) < lookback + (0 if args.no_backtest else args.pred_len):
            lookback = max(32, len(df) - (0 if args.no_backtest else args.pred_len))
            print(f"History is short; using lookback={lookback}.")
        if len(df) < lookback:
            raise SystemExit(f"Need at least {lookback} bars, got {len(df)}.")

        predictor, device = build_predictor(args)
        report["model"] = {
            "name": args.model,
            "tokenizer": args.tokenizer,
            "device": device,
            "lookback": int(lookback),
            "max_context": int(args.max_context),
            "temperature": args.temperature,
            "top_p": args.top_p,
            "top_k": args.top_k,
            "n_paths": int(args.n_paths),
            "seed": int(args.seed),
        }

        if not args.no_backtest:
            print("Running holdout backtest ...")
            report["backtest"] = holdout_backtest(predictor, df, lookback, args.pred_len, args, ppy)
            if report["backtest"] is None:
                print("Not enough history for a holdout backtest; skipping.")

        print(f"Sampling {args.n_paths} forecast paths ...")
        hist = df.tail(lookback).reset_index(drop=True)
        y_timestamp = make_future_timestamps(df["timestamps"].iloc[-1], args.pred_len, spacing)
        paths = ensemble_paths(
            predictor, hist[FEATURE_COLS], hist["timestamps"], y_timestamp, args.pred_len, args
        )
        report["forecast"] = forecast_summary(
            paths, float(df["close"].iloc[-1]), y_timestamp, ppy,
            quantiles=(0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95),
        )

        if not args.no_plot:
            png_path = os.path.join(args.outdir, f"{args.ticker}_kronos_forecast_{stamp}.png")
            plot_fan_chart(df, report["forecast"], args.ticker, png_path)
            report["plot"] = png_path
            print(f"Chart written to {png_path}")

    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
    print(f"Report written to {json_path}")

    print_console_summary(report)
    return report


def _fmt_pct(value):
    return "n/a" if value is None else f"{value * 100:.2f}%"


def print_console_summary(report):
    snap = report["technical_snapshot"]
    print("\n" + "=" * 68)
    print(f"{report['ticker']} technical snapshot ({snap['last_bar']})")
    print("=" * 68)
    print(f"  last close              {snap['last_close']:.2f}")
    print(f"  return 5 / 21 bars      {_fmt_pct(snap['return_5_bars'])} / "
          f"{_fmt_pct(snap['return_21_bars'])}")
    print(f"  realized vol 21d (ann)  {_fmt_pct(snap['realized_vol_21_ann'])}")
    print(f"  ATR(14) as % of price   {_fmt_pct(snap['atr_14_pct_of_price'])}")
    print(f"  max drawdown            {_fmt_pct(snap['max_drawdown'])}")
    print(f"  vs history high / low   {_fmt_pct(snap['pct_below_history_high'])} / "
          f"{_fmt_pct(snap['pct_above_history_low'])}")
    rsi_14 = snap.get("rsi_14")
    print(f"  RSI(14)                 {'n/a' if rsi_14 is None else f'{rsi_14:.1f}'}")

    backtest = report.get("backtest")
    if backtest:
        print("\n" + "-" * 68)
        print(f"Holdout backtest {backtest['window_start']} -> {backtest['window_end']}")
        print("-" * 68)
        print(f"  Kronos RMSE / baseline  {backtest['model']['rmse']:.2f} / "
              f"{backtest['random_walk_baseline']['rmse']:.2f}")
        print(f"  skill vs random walk    {_fmt_pct(backtest['rmse_skill_vs_baseline'])}")
        print(f"  direction hit rate      {_fmt_pct(backtest['direction_hit_rate'])}")
        print(f"  p10-p90 coverage        {_fmt_pct(backtest['p10_p90_coverage'])} (target 80%)")

    forecast = report.get("forecast")
    if forecast:
        terminal = forecast["terminal_close"]
        print("\n" + "-" * 68)
        print(f"Forecast {forecast['horizon_bars']} bars -> {forecast['horizon_end']}")
        print("-" * 68)
        print(f"  median terminal close   {terminal['median']:.2f} "
              f"({_fmt_pct(forecast['terminal_return']['median'])})")
        print(f"  p05 / p95 terminal      {terminal['p05']:.2f} / {terminal['p95']:.2f}")
        print(f"  P(close > last close)   {_fmt_pct(forecast['prob_close_above_last'])}")
        print(f"  forecast vol (ann)      {_fmt_pct(forecast['forecast_vol_ann'])}")
        print(f"  expected max drawdown   {_fmt_pct(forecast['expected_max_drawdown_over_horizon'])}")
    print()


if __name__ == "__main__":
    main()
