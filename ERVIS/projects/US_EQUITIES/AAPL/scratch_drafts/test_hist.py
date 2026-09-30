import json
import pandas as pd

# Let's inspect the historical financials in aapl_financials.csv and balance sheet
fin = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_financials.csv', index_col=0)
bs = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_balance_sheet.csv', index_col=0)
cf = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_cashflow.csv', index_col=0)

years = ['2022-09-30', '2023-09-30', '2024-09-30', '2025-09-30']
print("Financials summary:")
for y in years:
    rev = fin.loc['Total Revenue', y] if 'Total Revenue' in fin.index else None
    ebit = fin.loc['Operating Income', y] if 'Operating Income' in fin.index else None
    ni = fin.loc['Net Income', y] if 'Net Income' in fin.index else None
    cfo = cf.loc['Operating Cash Flow', y] if 'Operating Cash Flow' in cf.index else None
    capex = cf.loc['Capital Expenditure', y] if 'Capital Expenditure' in cf.index else None
    assets = bs.loc['Total Assets', y] if 'Total Assets' in bs.index else None
    equity = bs.loc['Stockholders Equity', y] if 'Stockholders Equity' in bs.index else None
    debt = bs.loc['Total Debt', y] if 'Total Debt' in bs.index else None
    cash = bs.loc['Cash Cash Equivalents And Short Term Investments', y] if 'Cash Cash Equivalents And Short Term Investments' in bs.index else None
    marketable = bs.loc['Available For Sale Securities', y] if 'Available For Sale Securities' in bs.index else None
    print(f"Year {y}: Rev={rev/1e9:.1f}B, EBIT={ebit/1e9:.1f}B, NI={ni/1e9:.1f}B, CapEx={capex/1e9:.2f}B, Assets={assets/1e9:.1f}B, Equity={equity/1e9:.1f}B, Cash+Sec={(cash+marketable)/1e9:.1f}B, Debt={debt/1e9:.1f}B")
