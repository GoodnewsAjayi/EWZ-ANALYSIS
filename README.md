# EWZ ETF Analysis

Module 6 group project analyzing the iShares MSCI Brazil ETF (EWZ).

This repo contains a small script to download EWZ price data via `yfinance`, compute daily returns, and save plots and summary stats in `outputs/`.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
python analysis_ewz.py --ticker EWZ --start 2010-01-01 --end 2020-01-01 --outdir outputs
```

## CI

The repository includes a GitHub Actions workflow that runs the analysis on push and uploads artifacts under `ewz-outputs`.
