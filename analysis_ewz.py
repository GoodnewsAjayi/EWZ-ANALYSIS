import argparse
import os
import logging

import yfinance as yf
import pandas as pd
import matplotlib
# Use a non-interactive backend so the script can run in CI (no display required)
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run_analysis(ticker: str, start: str, end: str, outdir: str):
    os.makedirs(outdir, exist_ok=True)

    logging.info(f"Downloading {ticker} from {start} to {end}")
    data = yf.download(ticker, start=start, end=end, progress=False)

    if data.empty:
        raise SystemExit(f"No data downloaded for {ticker} between {start} and {end}")

    data["Return"] = data["Close"].pct_change()

    # Save price plot
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["Close"], label="Close")
    plt.title(f"{ticker} Closing Price ({start}–{end})")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.legend()
    price_path = os.path.join(outdir, f"{ticker}_closing_price.png")
    plt.savefig(price_path, bbox_inches='tight')
    plt.close()

    # Save returns plot
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data["Return"], label="Daily Return")
    plt.title(f"{ticker} Daily Returns ({start}–{end})")
    plt.xlabel("Date")
    plt.ylabel("Return")
    plt.grid(True)
    plt.legend()
    returns_path = os.path.join(outdir, f"{ticker}_daily_returns.png")
    plt.savefig(returns_path, bbox_inches='tight')
    plt.close()

    # Save CSV
    csv_path = os.path.join(outdir, f"{ticker}_data.csv")
    data.to_csv(csv_path)

    # Save stats
    stats = data["Return"].describe().to_string()
    stats_path = os.path.join(outdir, f"{ticker}_return_stats.txt")
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write(stats)

    logging.info(f"Saved price plot to: {price_path}")
    logging.info(f"Saved returns plot to: {returns_path}")
    logging.info(f"Saved CSV to: {csv_path}")
    logging.info(f"Saved stats to: {stats_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download ETF data and produce analysis outputs")
    parser.add_argument("--ticker", default="EWZ", help="Ticker symbol (default: EWZ)")
    parser.add_argument("--start", default="2010-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", default="2020-01-01", help="End date (YYYY-MM-DD)")
    parser.add_argument("--outdir", default="outputs", help="Output directory (default: outputs)")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    run_analysis(args.ticker, args.start, args.end, args.outdir)
