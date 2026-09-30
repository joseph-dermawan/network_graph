import pandas as pd
import json

fin = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_financials.csv', index_col=0)
bs = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_balance_sheet.csv', index_col=0)
cf = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_cashflow.csv', index_col=0)
qfin = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_quarterly_financials.csv', index_col=0)
qbs = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_quarterly_balance_sheet.csv', index_col=0)
qcf = pd.read_csv('ERVIS/projects/US_EQUITIES/AAPL/raw_filings/aapl_quarterly_cashflow.csv', index_col=0)

print("Financials index:")
print(fin.index.tolist())

print("\nBalance sheet index:")
print(bs.index.tolist())

print("\nCashflow index:")
print(cf.index.tolist())

# Check latest 4 quarters
last4_q = ['2026-06-30', '2026-03-31', '2025-12-31', '2025-09-30']
print("\nQuarterly revenue:")
print(qfin.loc['Total Revenue', last4_q])

ttm_rev = qfin.loc['Total Revenue', last4_q].sum()
ttm_op_inc = qfin.loc['Operating Income', last4_q].sum()
ttm_ni = qfin.loc['Net Income', last4_q].sum()
ttm_rd = qfin.loc['Research And Development', last4_q].sum() if 'Research And Development' in qfin.index else 0
ttm_cfo = qcf.loc['Operating Cash Flow', last4_q].sum()
ttm_capex = qcf.loc['Capital Expenditure', last4_q].sum()

print(f"TTM Revenue: ${ttm_rev/1e6:.1f}M (${ttm_rev/1e9:.2f}B)")
print(f"TTM Operating Income: ${ttm_op_inc/1e6:.1f}M (${ttm_op_inc/1e9:.2f}B)")
print(f"TTM Net Income: ${ttm_ni/1e6:.1f}M (${ttm_ni/1e9:.2f}B)")
print(f"TTM R&D: ${ttm_rd/1e6:.1f}M (${ttm_rd/1e9:.2f}B)")
print(f"TTM CFO: ${ttm_cfo/1e6:.1f}M (${ttm_cfo/1e9:.2f}B)")
print(f"TTM CapEx: ${ttm_capex/1e6:.1f}M (${ttm_capex/1e9:.2f}B)")
print(f"TTM FCF: ${(ttm_cfo + ttm_capex)/1e6:.1f}M (${(ttm_cfo + ttm_capex)/1e9:.2f}B)")
