#!/usr/bin/env python3
"""
ERVIS EXCEL WORKBOOK GENERATOR :: BROADCOM INC. (AVGO)
Generates: ERVIS/projects/US_EQUITIES/AVGO/models/model.xlsx
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

PROJECT_DIR = "ERVIS/projects/US_EQUITIES/AVGO"
MODELS_DIR = f"{PROJECT_DIR}/models"
os.makedirs(MODELS_DIR, exist_ok=True)

# Spot & Audited Base Data
TICKER = "AVGO"
COMPANY_NAME = "Broadcom Inc."
MARKET = "US_EQUITIES"
SPOT_PRICE_USD = 358.15
SHARES_OUTSTANDING_M = 4773.63
MARKET_CAP_M = 1709675.6

TTM_REVENUE = 89104.0
TTM_GROSS_PROFIT = 58808.0
TTM_REPORTED_OP_INC = 43237.0
TTM_NET_INCOME = 38265.0
TTM_FREE_CASH_FLOW = 39403.0
TTM_CAPEX = 1250.0

Q3_CASH_AND_ST_INV = 23975.0
Q3_TOTAL_DEBT = 59419.0
Q3_TOTAL_ASSETS = 188148.0
Q3_CURRENT_ASSETS = 35240.0
Q3_CURRENT_LIABILITIES = 19120.0
Q3_STOCKHOLDERS_EQUITY = 99690.0
Q3_TOTAL_LIABILITIES = 88458.0
Q3_ACCOUNTS_RECEIVABLE = 9450.0
Q3_INVENTORY = 2850.0
Q3_NET_PPE = 5820.0
Q3_GOODWILL = 97801.0
Q3_INTANGIBLES = 32273.0

# Normalized Metrics
NORM_EBIT_0 = 46743.6
NORM_NOPAT_0 = 40433.2
TOTAL_ADJUSTED_DEBT = 61569.0
TRUE_NET_DEBT = 37594.0
INVESTED_CAPITAL = 166572.6
ROIC_0 = 24.27

# WACC
BASE_WACC = 0.0934
TERMINAL_WACC = 0.0900
RF_10Y = 0.0458
ERP = 0.0433
HAMADA_BETA = 1.1343
COST_OF_EQUITY = 0.0949
CREDIT_RATING = "Baa1 / BBB+ (Upgraded ERM to A3/A- profile)"
PRE_TAX_KD = 0.0603

# Valuation Outputs
DCF_VALUE_PER_SHARE = 213.73
SOTP_VALUE_PER_SHARE = 232.94
MC_MEDIAN = 495.76
MC_P10 = 193.29
MC_P90 = 625.45
MC_WIN_RATE = 65.4
TARGET_INTRINSIC_PRICE = 247.70
UPSIDE_PERCENT = -30.8
FINAL_RATING = "TRIM / TAKE PROFITS (-30.8%)"
LIQUIDATION_FLOOR = 0.00

wb = openpyxl.Workbook()
wb.remove(wb.active)

fill_navy = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
fill_hdr_accent = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
fill_target = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fill_alert = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")

font_title = Font(name="Segoe UI", size=15, bold=True, color="38BDF8")
font_sub = Font(name="Segoe UI", size=10, italic=True, color="94A3B8")
font_hdr = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Segoe UI", size=10, bold=True, color="000000")
font_data = Font(name="Segoe UI", size=10, bold=False, color="000000")

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

# Tab 0: 00_DASHBOARD
ws0 = wb.create_sheet(title="00_DASHBOARD")
ws0.views.sheetView[0].showGridLines = True
ws0["A1"] = f"ERVIS VALUATION EXECUTIVE DASHBOARD :: {COMPANY_NAME.upper()}"
ws0["A1"].font = font_title
ws0["A2"] = f"Institutional Dual-Engine Model | Ticker: {TICKER} | Spot: ${SPOT_PRICE_USD:.2f} | Base Rf: {RF_10Y*100:.2f}%"
ws0["A2"].font = font_sub

dash_rows = [
    ("VALUATION EXECUTIVE SUMMARY", "METRIC / VALUE", "STATUS / BENCHMARK"),
    ("Spot Trading Price (USD)", f"${SPOT_PRICE_USD:.2f}", "Active Market Quote"),
    ("Target Intrinsic Price (USD)", f"${TARGET_INTRINSIC_PRICE:.2f}", f"Upside: {UPSIDE_PERCENT:+.1f}%"),
    ("Institutional Recommendation", FINAL_RATING, "Dual-Engine Triangulation"),
    ("10-Yr Discrete Ginzu DCF Value", f"${DCF_VALUE_PER_SHARE:.2f}", "Sales-to-Capital Reinvestment Engine"),
    ("Sum-of-the-Parts (SOTP) Value", f"${SOTP_VALUE_PER_SHARE:.2f}", "Divisional Peer EBITDA Multiples"),
    ("Monte Carlo 10,000 Median", f"${MC_MEDIAN:.2f}", f"Win Rate: {MC_WIN_RATE:.1f}% (> Spot)"),
    ("Monte Carlo P10 / P90 Bands", f"${MC_P10:.2f} / ${MC_P90:.2f}", "80% Confidence Interval"),
    ("Liquidation Haircut Floor", f"${LIQUIDATION_FLOOR:.2f}", "Max Downside Asset Haircut"),
    ("Synthetic Credit Rating", CREDIT_RATING, "Interest Coverage > 11x"),
    ("Base WACC / Terminal WACC", f"{BASE_WACC*100:.2f}% / {TERMINAL_WACC*100:.2f}%", "Hamada Levered Beta: 1.134"),
    ("Altman Z-Score", "13.13", "SAFE ZONE (Z > 2.99, Pristine Solvency)"),
    ("Piotroski F-Score", "8 / 9", "Strong Solvency / Operational Rank"),
    ("Beneish M-Score", "-2.74", "Safe Zone (M < -2.22, Non-Manipulator)"),
    ("Hyperscaler CapEx Capture Ratio (CPR)", "5.76%", "AVGO Hardware Tax ($24.5B of $425B)"),
    ("Customer Net AI Operating ROI", "125.31%", "Custom ASIC Unit Cost Superiority"),
    ("Customer Payback Duration", "0.65 Years (7.8 Months)", "Obsolescence Gap: -2.85 Yrs (Accretive)")
]

for r_idx, row in enumerate(dash_rows, start=4):
    for c_idx, val in enumerate(row, start=1):
        cell = ws0.cell(row=r_idx, column=c_idx, value=val)
        cell.border = thin_border
        if r_idx == 4:
            cell.font = font_hdr
            cell.fill = fill_navy
        elif r_idx in [5, 6, 7]:
            cell.font = font_bold
            cell.fill = fill_alert
        else:
            cell.font = font_data

# Tab 1: 01_INPUTS_ASSUMPTIONS
ws1 = wb.create_sheet(title="01_INPUTS_ASSUMPTIONS")
ws1.views.sheetView[0].showGridLines = True
ws1["A1"] = f"{TICKER} :: MODEL INPUTS & AUDITED FINANCIALS"
ws1["A1"].font = font_title

inputs_data = [
    ("CORE INPUT PARAMETER", "VALUE ($M or %)", "SOURCE / METHODOLOGY"),
    ("Spot Stock Price (USD)", SPOT_PRICE_USD, "Market Data"),
    ("Shares Outstanding (M)", SHARES_OUTSTANDING_M, "10-Q SEC Filing (Post 10:1 Split)"),
    ("Market Capitalization ($M)", MARKET_CAP_M, "Calculated"),
    ("TTM Total Revenue ($M)", TTM_REVENUE, "SEC 10-K / 10-Q Reports"),
    ("TTM Gross Profit ($M)", TTM_GROSS_PROFIT, "SEC Reported"),
    ("TTM Reported Operating Income ($M)", TTM_REPORTED_OP_INC, "SEC Reported GAAP"),
    ("TTM Net Income ($M)", TTM_NET_INCOME, "SEC Reported GAAP"),
    ("TTM Free Cash Flow ($M)", TTM_FREE_CASH_FLOW, "CFO minus Physical CapEx"),
    ("Cash & Short-Term Investments ($M)", Q3_CASH_AND_ST_INV, "Balance Sheet (Q3 FY26)"),
    ("Reported Total Debt ($M)", Q3_TOTAL_DEBT, "Balance Sheet (Q3 FY26)"),
    ("Total Stockholders' Equity ($M)", Q3_STOCKHOLDERS_EQUITY, "Balance Sheet (Q3 FY26)"),
    ("Total Assets ($M)", Q3_TOTAL_ASSETS, "Balance Sheet (Q3 FY26)"),
    ("US 10-Year Risk-Free Rate (Rf)", f"{RF_10Y*100:.2f}%", "US Treasury Sovereign Yield"),
    ("Equity Risk Premium (ERP)", f"{ERP*100:.2f}%", "Damodaran Implied S&P 500 ERP"),
    ("Peer Unlevered Beta", 1.10, "Semiconductor & Software Peer Group"),
    ("Effective Corporate Tax Rate", "13.5%", "Broadcom Non-GAAP Operational Tax Rate")
]
for r_idx, row in enumerate(inputs_data, start=3):
    for c_idx, val in enumerate(row, start=1):
        cell = ws1.cell(row=r_idx, column=c_idx, value=val)
        cell.border = thin_border
        if r_idx == 3:
            cell.font = font_hdr
            cell.fill = fill_navy
        else:
            cell.font = font_bold if c_idx == 1 else font_data

# Tab 2: 02_NORMALIZATION_CONVERTERS
ws2 = wb.create_sheet(title="02_NORMALIZATION_CONVERTERS")
ws2.views.sheetView[0].showGridLines = True
ws2["A1"] = f"{TICKER} :: GATE 1 FORENSIC NORMALIZATION SCHEDULE"
ws2["A1"].font = font_title

norm_rows = [
    ("ACCOUNTING LINE ITEM", "REPORTED GAAP ($M)", "FORENSIC ADJUSTMENT ($M)", "NORMALIZED ECONOMIC ($M)", "RATIONALE"),
    ("Operating Income (EBIT)", TTM_REPORTED_OP_INC, 3377.0 + 129.6, NORM_EBIT_0, "Addback Net R&D Cap + Lease Interest"),
    ("R&D Expense vs Amortization", 11836.0, -8459.0, 3377.0, "5-Yr Straight-Line R&D Capitalization"),
    ("Capitalized Research Asset", 0.0, 29288.6, 29288.6, "Structural Knowledge Asset Capitalized"),
    ("Operating Lease Debt", 0.0, 2150.0, 2150.0, f"Discounted at Pre-tax Kd ({PRE_TAX_KD*100:.2f}%)"),
    ("Total Gross Debt", Q3_TOTAL_DEBT, 2150.0, TOTAL_ADJUSTED_DEBT, "Reported Debt + Operating Lease Obligations"),
    ("Cash & Equivalents", Q3_CASH_AND_ST_INV, 0.0, Q3_CASH_AND_ST_INV, "Liquid Cash & Treasury Bills"),
    ("True Net Debt", Q3_TOTAL_DEBT - Q3_CASH_AND_ST_INV, 2150.0, TRUE_NET_DEBT, "Adjusted Debt less Liquid Cash Buffer"),
    ("NOPAT (After-Tax EBIT)", TTM_REPORTED_OP_INC * (1-0.135), (3377.0 + 129.6) * (1-0.135), NORM_NOPAT_0, "True NOPAT at 13.5% Tax Rate"),
    ("Invested Capital", Q3_STOCKHOLDERS_EQUITY + Q3_TOTAL_DEBT - Q3_CASH_AND_ST_INV, 29288.6 + 2150.0, INVESTED_CAPITAL, "Equity + Net Debt + R&D Asset"),
    ("Economic ROIC (%)", f"{(TTM_REPORTED_OP_INC*(1-0.135)/(Q3_STOCKHOLDERS_EQUITY + Q3_TOTAL_DEBT - Q3_CASH_AND_ST_INV))*100:.2f}%", "-", f"{ROIC_0:.2f}%", "NOPAT_0 / Invested Capital")
]
for r_idx, row in enumerate(norm_rows, start=3):
    for c_idx, val in enumerate(row, start=1):
        cell = ws2.cell(row=r_idx, column=c_idx, value=val)
        cell.border = thin_border
        if r_idx == 3:
            cell.font = font_hdr
            cell.fill = fill_navy
        else:
            cell.font = font_bold if c_idx in [1, 4] else font_data

# Tab 3: 03_WACC_CREDIT_ENGINE
ws3 = wb.create_sheet(title="03_WACC_CREDIT_ENGINE")
ws3.views.sheetView[0].showGridLines = True
ws3["A1"] = f"{TICKER} :: GATE 3 WACC & MOODY'S CREDIT SYNTHESIS"
ws3["A1"].font = font_title

wacc_table = [
    ("COST OF CAPITAL COMPONENT", "VALUE", "FORMULA / BENCHMARK"),
    ("Risk-Free Rate (10-Yr US Treasury)", f"{RF_10Y*100:.2f}%", "Sovereign Yield Curve"),
    ("Equity Risk Premium (ERP)", f"{ERP*100:.2f}%", "Damodaran S&P 500 Implied Premium"),
    ("Peer Unlevered Beta (Beta_U)", "1.10", "Broadcom / Marvel / Qualcomm / Oracle Blend"),
    ("Market Debt / Equity (D/E)", "3.60%", "Total Adjusted Debt / Market Cap"),
    ("Effective Tax Rate (t)", "13.5%", "Operational Effective Tax"),
    ("Hamada Levered Beta (Beta_L)", f"{HAMADA_BETA:.4f}", "Beta_U * [1 + (1 - t) * (D/E)]"),
    ("Cost of Equity (Ke)", f"{COST_OF_EQUITY*100:.2f}%", "Rf + Beta_L * ERP"),
    ("Moody's Synthetic Credit Rating", CREDIT_RATING, "Coverage > 11x, Net Debt/EBITDA < 1.0x"),
    ("Default Spread", "145 bps", "Synthetic Spread over 10-Yr Treasury"),
    ("Pre-Tax Cost of Debt (Kd)", f"{PRE_TAX_KD*100:.2f}%", "Rf + Default Spread"),
    ("After-Tax Cost of Debt", "5.22%", "Kd * (1 - t)"),
    ("Weight of Equity (We)", "96.52%", "Market Cap / (Market Cap + Debt)"),
    ("Weight of Debt (Wd)", "3.48%", "Total Debt / (Market Cap + Debt)"),
    ("Base WACC", f"{BASE_WACC*100:.2f}%", "We * Ke + Wd * Kd_after_tax"),
    ("Terminal WACC", f"{TERMINAL_WACC*100:.2f}%", "Mature Capital Structure Benchmark")
]
for r_idx, row in enumerate(wacc_table, start=3):
    for c_idx, val in enumerate(row, start=1):
        cell = ws3.cell(row=r_idx, column=c_idx, value=val)
        cell.border = thin_border
        if r_idx == 3:
            cell.font = font_hdr
            cell.fill = fill_navy
        else:
            cell.font = font_bold if c_idx == 1 else font_data

# Tab 4: 04_PRO_FORMA_DCF_10YR
ws4 = wb.create_sheet(title="04_PRO_FORMA_DCF_10YR")
ws4.views.sheetView[0].showGridLines = True
ws4["A1"] = f"{TICKER} :: 10-YEAR PRO-FORMA GINZU DCF SCHEDULE ($M)"
ws4["A1"].font = font_title

growth_rates = [0.180, 0.150, 0.120, 0.095, 0.075, 0.060, 0.050, 0.045, 0.040, 0.038]
margins = [0.535, 0.550, 0.565, 0.560, 0.550, 0.540, 0.535, 0.530, 0.525, 0.520]
proj_years = [f"FY{2027+i}E" for i in range(10)]

proj_rev, proj_ebit, proj_ebit_at, proj_reinv, proj_fcff, proj_wacc, proj_df, proj_pv = [], [], [], [], [], [], [], []
curr_r = TTM_REVENUE
cum_df = 1.0

for i in range(10):
    g = growth_rates[i]
    m = margins[i]
    w = BASE_WACC + (TERMINAL_WACC - BASE_WACC) * (i / 9.0)
    r = curr_r * (1.0 + g)
    dr = r - curr_r
    eb = r * m
    eb_at = eb * (1.0 - 0.135)
    re = dr / 3.25
    fc = eb_at - re
    cum_df /= (1.0 + w)
    pv = fc * cum_df
    proj_rev.append(r)
    proj_ebit.append(eb)
    proj_ebit_at.append(eb_at)
    proj_reinv.append(re)
    proj_fcff.append(fc)
    proj_wacc.append(w)
    proj_df.append(cum_df)
    proj_pv.append(pv)
    curr_r = r

pv_10yr_fcff = sum(proj_pv)
term_rev = proj_rev[-1] * 1.038
term_ebit_at = term_rev * margins[-1] * (1.0 - 0.135)
term_reinv = term_ebit_at * (0.038 / 0.24)
term_fcff = term_ebit_at - term_reinv
term_val = term_fcff / (0.0900 - 0.0380)
pv_term_val = term_val * proj_df[-1]
ev_dcf = pv_10yr_fcff + pv_term_val
eq_dcf = ev_dcf - TRUE_NET_DEBT

dcf_headers = ["LINE ITEM ($M)"] + proj_years + ["TERMINAL YEAR"]
ws4.row_dimensions[3].height = 22
for col_idx, h in enumerate(dcf_headers, start=1):
    cell = ws4.cell(row=3, column=col_idx, value=h)
    cell.font = font_hdr
    cell.fill = fill_navy
    cell.alignment = Alignment(horizontal="center")
    cell.border = thin_border

dcf_rows_data = [
    ("Revenue Growth Rate (%)", [f"{g*100:.1f}%" for g in growth_rates] + ["3.8%"]),
    ("Total Revenue", [round(r, 1) for r in proj_rev] + [round(term_rev, 1)]),
    ("Operating Margin (%)", [f"{m*100:.1f}%" for m in margins] + [f"{margins[-1]*100:.1f}%"]),
    ("Operating Income (EBIT)", [round(eb, 1) for eb in proj_ebit] + [round(term_rev * margins[-1], 1)]),
    ("NOPAT (EBIT * [1 - t])", [round(at, 1) for at in proj_ebit_at] + [round(term_ebit_at, 1)]),
    ("Reinvestment", [round(re, 1) for re in proj_reinv] + [round(term_reinv, 1)]),
    ("Free Cash Flow to Firm (FCFF)", [round(fc, 1) for fc in proj_fcff] + [round(term_fcff, 1)]),
    ("Discount Rate (WACC %)", [f"{w*100:.2f}%" for w in proj_wacc] + ["9.00%"]),
    ("Cumulative Discount Factor", [round(df, 4) for df in proj_df] + [round(proj_df[-1], 4)]),
    ("Present Value of FCFF", [round(pv, 1) for pv in proj_pv] + [round(pv_term_val, 1)])
]

for r_offset, (row_label, vals) in enumerate(dcf_rows_data, start=4):
    cell_lbl = ws4.cell(row=r_offset, column=1, value=row_label)
    cell_lbl.font = font_bold
    cell_lbl.border = thin_border
    for c_offset, v in enumerate(vals, start=2):
        cell_v = ws4.cell(row=r_offset, column=c_offset, value=v)
        cell_v.font = font_data
        cell_v.border = thin_border

bridge_start = 16
ws4.cell(row=bridge_start, column=1, value="VALUATION BRIDGE ITEM").font = font_hdr
ws4.cell(row=bridge_start, column=1).fill = fill_hdr_accent
ws4.cell(row=bridge_start, column=2, value="VALUE ($M or USD)").font = font_hdr
ws4.cell(row=bridge_start, column=2).fill = fill_hdr_accent

bridge_data = [
    ("PV of 10-Year Discrete FCFF", f"${pv_10yr_fcff:,.1f}M"),
    ("Terminal Value", f"${term_val:,.1f}M"),
    ("PV of Terminal Value", f"${pv_term_val:,.1f}M"),
    ("Enterprise Value (DCF)", f"${ev_dcf:,.1f}M"),
    ("Less: True Net Debt", f"${TRUE_NET_DEBT:,.1f}M"),
    ("Equity Value (DCF)", f"${eq_dcf:,.1f}M"),
    ("Shares Outstanding (M)", f"{SHARES_OUTSTANDING_M:,.2f}M"),
    ("DCF Intrinsic Value per Share", f"${DCF_VALUE_PER_SHARE:.2f}"),
    ("Current Spot Stock Price", f"${SPOT_PRICE_USD:.2f}"),
    ("Implied DCF Downside", f"{((DCF_VALUE_PER_SHARE / SPOT_PRICE_USD) - 1.0)*100:+.1f}%")
]
for b_idx, (k, val) in enumerate(bridge_data, start=bridge_start+1):
    c1 = ws4.cell(row=b_idx, column=1, value=k)
    c2 = ws4.cell(row=b_idx, column=2, value=val)
    c1.border = thin_border
    c2.border = thin_border
    if b_idx in [bridge_start+8, bridge_start+10]:
        c1.font = font_bold
        c2.font = font_bold
        c1.fill = fill_alert
        c2.fill = fill_alert
    else:
        c1.font = font_bold
        c2.font = font_data

# Tab 5: 05_AI_CAPEX_HEALTH
ws5 = wb.create_sheet(title="05_AI_CAPEX_HEALTH")
ws5.views.sheetView[0].showGridLines = True
ws5["A1"] = f"{TICKER} :: GATE 4B CAPEX PAYOUT & CUSTOMER ROI AUDIT"
ws5["A1"].font = font_title

capex_table = [
    ("CAPEX PAYOUT & ROI METRIC", "VALUE", "STRATEGIC BENCHMARK / INTERPRETATION"),
    ("Broadcom Physical CapEx ($M)", f"${TTM_CAPEX:,.1f}M", "Annual CapEx Spend"),
    ("Broadcom CapEx Intensity (% Rev)", "1.40%", "Ultra-Asset-Light Fabless Semi + Software Model"),
    ("Free Cash Flow Conversion (% CFO)", "96.92%", "Cash Flow Conversion Prowess"),
    ("Internal Economic ROIC (%)", f"{ROIC_0:.2f}%", "Capitalized R&D + VMware Invested Capital"),
    ("Annual Shareholder Capital Payout ($M)", "$17,452.0M", "Dividends ($11.1B) + Buybacks ($6.3B)"),
    ("Shareholder Payout Ratio of FCF (%)", "44.29%", "Disciplined Free Cash Return"),
    ("Hyperscaler Total Annual CapEx ($B)", "$425.0B", "Combined 2026 Big 4 Cloud Spend"),
    ("Broadcom AI Silicon & Networking Revenue ($B)", "$24.5B", "Custom XPUs ($16.5B) + Networking ($8.0B)"),
    ("Customer CapEx Payout Ratio (CPR / Hardware Tax)", "5.76%", "Percentage of Hyperscaler CapEx Capture"),
    ("Customer Incremental Generative AI Revenue ($B)", "$58.0B", "Cloud AI APIs & Infrastructure Monetization"),
    ("Customer Cloud Software Gross Margin", "65.0%", "Hyperscaler Platform Gross Margin"),
    ("Customer Incremental Gross Profit ($B)", "$37.70B", "Realized Software Profit"),
    ("Annual Hardware Depreciation ($B)", "$7.00B", "Depreciated over 3.50 Years"),
    ("Customer Net AI Operating Income ($B)", "$30.70B", "Net AI Profit after Depreciation"),
    ("Customer Net AI Operating ROI (%)", "125.31%", "Enormous Return on Custom ASIC Investment"),
    ("Customer Payback Period (Years)", "0.65 Years", "Rapid Payback: 7.8 Months"),
    ("Hardware Useful Economic Life", "3.50 Years", "Hyperscaler Server Replacement Cycle"),
    ("Hardware Obsolescence Gap", "-2.85 Years", "Payback < Life (Negative Gap = VALUE ACCRETIVE)"),
    ("Obsolescence Deficit Status", "VALUE ACCRETIVE", "NO DEFICIT: Broadcom ASICs Yield Outstanding ROI")
]
for r_idx, row in enumerate(capex_table, start=3):
    for c_idx, val in enumerate(row, start=1):
        cell = ws5.cell(row=r_idx, column=c_idx, value=val)
        cell.border = thin_border
        if r_idx == 3:
            cell.font = font_hdr
            cell.fill = fill_navy
        else:
            cell.font = font_bold if c_idx in [1, 2] else font_data

# Tab 6: 06_LIQUIDATION_FLOOR
ws6 = wb.create_sheet(title="06_LIQUIDATION_FLOOR")
ws6.views.sheetView[0].showGridLines = True
ws6["A1"] = f"{TICKER} :: GATE 4 DOWNSIDE LIQUIDATION HAIRCUT FLOOR"
ws6["A1"].font = font_title

liq_rows = [
    ("BALANCE SHEET ASSET CLASS", "BOOK VALUE ($M)", "HAIRCUT RATIO (%)", "RECOVERABLE VALUE ($M)", "RATIONALE"),
    ("Cash & Short-Term Investments", Q3_CASH_AND_ST_INV, "100.0%", Q3_CASH_AND_ST_INV, "Immediate Liquid Value"),
    ("Accounts Receivable", Q3_ACCOUNTS_RECEIVABLE, "75.0%", Q3_ACCOUNTS_RECEIVABLE * 0.75, "Discount for Credit Default Risk"),
    ("Inventories (Finished Goods & WIP)", Q3_INVENTORY, "50.0%", Q3_INVENTORY * 0.50, "Fire-Sale Semiconductor Haircut"),
    ("Net Property, Plant & Equipment", Q3_NET_PPE, "30.0%", Q3_NET_PPE * 0.30, "Specialized Testing & Lab Equipment"),
    ("Goodwill & Intangible Assets", Q3_GOODWILL + Q3_INTANGIBLES, "5.0%", (Q3_GOODWILL + Q3_INTANGIBLES) * 0.05, "Severe Haircut on Acquired IP"),
    ("Total Realizable Asset Value", Q3_TOTAL_ASSETS, "-", 40738.2, "Sum of Realizable Assets"),
    ("Less: Total Liabilities", Q3_TOTAL_LIABILITIES, "100.0%", Q3_TOTAL_LIABILITIES, "Full Senior Claim Obligations"),
    ("Net Realizable Liquidation Equity", "-", "-", 0.0, "Realizable Assets minus Liabilities"),
    ("Liquidation Floor per Share (USD)", "-", "-", "$0.00", "Downside Floor in Catastrophic Distress")
]
for r_idx, row in enumerate(liq_rows, start=3):
    for c_idx, val in enumerate(row, start=1):
        cell = ws6.cell(row=r_idx, column=c_idx, value=val)
        cell.border = thin_border
        if r_idx == 3:
            cell.font = font_hdr
            cell.fill = fill_navy
        else:
            cell.font = font_bold if c_idx in [1, 4] else font_data

# Set auto column width
for ws in wb.worksheets:
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

wb.save(f"{MODELS_DIR}/model.xlsx")
print(f"[SUCCESS] Multi-tab Excel workbook successfully created at {MODELS_DIR}/model.xlsx")
