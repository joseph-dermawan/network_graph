#!/usr/bin/env python3
import os
import json
import yfinance as yf
import pandas as pd

PROJECT_DIR = "ERVIS/projects/US_EQUITIES/AVGO"
RAW_DIR = f"{PROJECT_DIR}/raw_filings"
os.makedirs(RAW_DIR, exist_ok=True)

ticker = yf.Ticker("AVGO")

print(f"[INGESTION] Fetching financial statements for AVGO...")
info = ticker.info
with open(f"{RAW_DIR}/avgo_info.json", "w") as f:
    json.dump(info, f, indent=2, default=str)

# Financials
fin = ticker.financials
fin.to_csv(f"{RAW_DIR}/avgo_financials.csv")

q_fin = ticker.quarterly_financials
q_fin.to_csv(f"{RAW_DIR}/avgo_quarterly_financials.csv")

# Balance Sheet
bs = ticker.balance_sheet
bs.to_csv(f"{RAW_DIR}/avgo_balance_sheet.csv")

q_bs = ticker.quarterly_balance_sheet
q_bs.to_csv(f"{RAW_DIR}/avgo_quarterly_balance_sheet.csv")

# Cashflow
cf = ticker.cashflow
cf.to_csv(f"{RAW_DIR}/avgo_cashflow.csv")

q_cf = ticker.quarterly_cashflow
q_cf.to_csv(f"{RAW_DIR}/avgo_quarterly_cashflow.csv")

print("[INGESTION] Successfully saved all raw financial statements to:", RAW_DIR)
print(f"Current Price: {info.get('currentPrice') or info.get('regularMarketPrice')}")
print(f"Shares Outstanding: {info.get('sharesOutstanding')}")
print(f"Market Cap: {info.get('marketCap')}")
