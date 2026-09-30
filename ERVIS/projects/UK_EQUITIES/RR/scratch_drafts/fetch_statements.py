import yfinance as yf
import json
import pandas as pd
import os

project_dir = "ERVIS/projects/UK_EQUITIES/RR"
raw_dir = f"{project_dir}/raw_filings"
os.makedirs(raw_dir, exist_ok=True)

ticker = yf.Ticker("RR.L")

# 1. Info
info = ticker.info
with open(f"{raw_dir}/rr_info.json", "w") as f:
    json.dump(info, f, indent=2, default=str)

# 2. Financials
fin = ticker.financials
fin.to_csv(f"{raw_dir}/rr_financials.csv")

# 3. Balance Sheet
bs = ticker.balance_sheet
bs.to_csv(f"{raw_dir}/rr_balance_sheet.csv")

# 4. Cash Flow
cf = ticker.cashflow
cf.to_csv(f"{raw_dir}/rr_cashflow.csv")

# 5. Quarterly statements
ticker.quarterly_financials.to_csv(f"{raw_dir}/rr_quarterly_financials.csv")
ticker.quarterly_balance_sheet.to_csv(f"{raw_dir}/rr_quarterly_balance_sheet.csv")
ticker.quarterly_cashflow.to_csv(f"{raw_dir}/rr_quarterly_cashflow.csv")

print("Successfully saved all raw statements to:", raw_dir)
