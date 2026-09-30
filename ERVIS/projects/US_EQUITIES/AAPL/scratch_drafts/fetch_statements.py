import yfinance as yf
import json
import pandas as pd
import os

project_dir = "ERVIS/projects/US_EQUITIES/AAPL"
raw_dir = f"{project_dir}/raw_filings"
os.makedirs(raw_dir, exist_ok=True)

ticker = yf.Ticker("AAPL")

# 1. Info
try:
    info = ticker.info
    with open(f"{raw_dir}/aapl_info.json", "w") as f:
        json.dump(info, f, indent=2, default=str)
    print("Saved aapl_info.json")
except Exception as e:
    print(f"Error saving info: {e}")

# 2. Financials
try:
    fin = ticker.financials
    fin.to_csv(f"{raw_dir}/aapl_financials.csv")
    print("Saved aapl_financials.csv")
except Exception as e:
    print(f"Error saving financials: {e}")

# 3. Balance Sheet
try:
    bs = ticker.balance_sheet
    bs.to_csv(f"{raw_dir}/aapl_balance_sheet.csv")
    print("Saved aapl_balance_sheet.csv")
except Exception as e:
    print(f"Error saving balance sheet: {e}")

# 4. Cash Flow
try:
    cf = ticker.cashflow
    cf.to_csv(f"{raw_dir}/aapl_cashflow.csv")
    print("Saved aapl_cashflow.csv")
except Exception as e:
    print(f"Error saving cashflow: {e}")

# 5. Quarterly statements
try:
    ticker.quarterly_financials.to_csv(f"{raw_dir}/aapl_quarterly_financials.csv")
    ticker.quarterly_balance_sheet.to_csv(f"{raw_dir}/aapl_quarterly_balance_sheet.csv")
    ticker.quarterly_cashflow.to_csv(f"{raw_dir}/aapl_quarterly_cashflow.csv")
    print("Saved quarterly statements.")
except Exception as e:
    print(f"Error saving quarterly statements: {e}")

print("Successfully saved all raw statements to:", raw_dir)
