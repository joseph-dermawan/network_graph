import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
wb.remove(wb.active) # Remove default sheet

# Common styles
font_family = "Segoe UI"
header_fill = PatternFill(start_color="1A2530", end_color="1A2530", fill_type="solid")
header_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
title_font = Font(name=font_family, size=14, bold=True, color="000000")
bold_font = Font(name=font_family, size=10, bold=True)
regular_font = Font(name=font_family, size=10)
accent_fill = PatternFill(start_color="E8F0FE", end_color="E8F0FE", fill_type="solid")
highlight_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D3D3D3'),
    right=Side(style='thin', color='D3D3D3'),
    top=Side(style='thin', color='D3D3D3'),
    bottom=Side(style='thin', color='D3D3D3')
)
top_thin_bottom_double = Border(
    top=Side(style='thin', color='000000'),
    bottom=Side(style='double', color='000000')
)

# ----------------------------------------------------
# TAB 1: EXECUTIVE SUMMARY
# ----------------------------------------------------
ws1 = wb.create_sheet(title="Executive Summary")
ws1.views.sheetView[0].showGridLines = True

ws1['A1'] = "ORACLE CORPORATION (ORCL) - INSTITUTIONAL VALUATION DOSSIER"
ws1['A1'].font = title_font
ws1['A2'] = "ERVIS DUAL-ENGINE VALUATION PIPELINE & GATE AUDIT"
ws1['A2'].font = Font(name=font_family, size=10, italic=True, color="555555")

summary_data = [
    ["METRIC", "VALUE", "BENCHMARK / CONTEXT"],
    ["Ticker / Exchange", "ORCL / NYSE", "S&P 500 / Technology Infrastructure"],
    ["Current Spot Price (USD)", 148.48, "As of Valuation Timestamp (Sep 2026)"],
    ["Diluted Shares Outstanding (M)", 3023.74, "SEC 10-K / Q1 10-Q Ingested"],
    ["Current Market Capitalization ($M)", 448965.0, "Spot Equity Value"],
    ["Net Debt ($M)", 118854.0, "Total Debt ($155.9B) - Cash ($37.1B)"],
    ["Current Enterprise Value ($M)", 567819.0, "Market Cap + Net Debt"],
    ["Base WACC", 0.0789, "Ke = 9.00%, Kd(post-tax) = 4.68%"],
    ["Terminal WACC", 0.0880, "Institutional Long-Term Hurdle Rate"],
    ["10-Year DCF Intrinsic Value (USD)", 115.40, "Damodaran Sales-to-Capital & Moat Override"],
    ["SOTP Divisional Intrinsic Value (USD)", 110.51, "Sum-of-the-Parts Peer Multiples"],
    ["Triangulated Target Price (USD)", 113.44, "60% DCF / 40% SOTP Weighted"],
    ["Implied Upside / Downside", -0.2360, "-23.6% Overvalued relative to Spot"],
    ["ERVIS Final Recommendation", "SELL / REBALANCE", "High Leverage + GPU Obsolescence Risk"],
    ["10,000-Trial Monte Carlo Median", 94.70, "P10: $68.40 | P90: $128.20 | Win Rate: 1.3%"],
    ["Altman Z-Score", 1.77, "Grey Zone / High Leverage Watch"],
    ["Piotroski F-Score", 6, "Scale 0-9 (Capital Intensity Drag)"],
    ["Beneish M-Score", -2.48, "Clean (Manipulation Threshold: -1.78)"]
]

for r_idx, row in enumerate(summary_data, start=4):
    for c_idx, val in enumerate(row, start=1):
        cell = ws1.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 4:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 2:
                if isinstance(val, float) and abs(val) < 1.0:
                    cell.number_format = '0.00%'
                elif isinstance(val, float) and val > 1000:
                    cell.number_format = '$#,##0.0'
                elif isinstance(val, (int, float)):
                    cell.number_format = '$#,##0.00'

# ----------------------------------------------------
# TAB 2: GATE 1 FORENSICS
# ----------------------------------------------------
ws2 = wb.create_sheet(title="Gate 1 Forensics")
ws2.views.sheetView[0].showGridLines = True
ws2['A1'] = "GATE 1: FORENSIC ACCOUNTING NORMALIZATION & AUDIT"
ws2['A1'].font = title_font

g1_headers = ["Normalization Item", "Reported ($M)", "Adjustment ($M)", "Restated ($M)", "Forensic Methodology & Rationale"]
ws2.append([])
ws2.append(g1_headers)
for c in range(1, 6):
    cell = ws2.cell(row=3, column=c)
    cell.fill = header_fill
    cell.font = header_font

g1_rows = [
    ["Operating Income (EBIT FY26)", 22444.0, 1294.2, 23738.2, "Add back R&D expensed ($10,272M) less 5-yr straight-line R&D amortization ($8,977.8M)"],
    ["Effective Tax Rate / Marginal Rate", 0.1260, 0.0840, 0.2100, "Statutory Marginal Tax Rate anchored at 21.0% Federal + State blend for NOPAT_0"],
    ["Net Operating Profit After Tax (NOPAT_0)", 19616.0, -862.8, 18753.2, "Restated EBIT_0 ($23,738.2M) * (1 - 21.0%)"],
    ["Capitalized R&D Asset (Balance Sheet)", 0.0, 19424.2, 19424.2, "5-Year Straight-Line: 80% FY26 + 60% FY25 + 40% FY24 + 20% FY23"],
    ["Total Debt & Capital Lease Obligations", 155931.0, 0.0, 155931.0, "Includes Cerner acquisition notes ($15.8B), senior notes ($109.5B), and capital leases ($30.6B)"],
    ["Cash & Short-Term Investments", 37077.0, 0.0, 37077.0, "Cash & Equivalents ($31.3B) + Short-Term Liquid Securities ($5.8B)"],
    ["Restated Net Debt", 118854.0, 0.0, 118854.0, "Total Funded Debt less Cash Buffer. Financial leverage remains elevated at 4.7x EBITDA"]
]

for r_idx, row in enumerate(g1_rows, start=4):
    for c_idx, val in enumerate(row, start=1):
        cell = ws2.cell(row=r_idx, column=c_idx, value=val)
        cell.font = regular_font
        cell.border = thin_border
        if c_idx in [2, 3, 4] and isinstance(val, float):
            if abs(val) <= 1.0:
                cell.number_format = '0.00%'
            else:
                cell.number_format = '$#,##0.0'

# ----------------------------------------------------
# TAB 3: GATE 2 HEALTH & REGRESSIONS
# ----------------------------------------------------
ws3 = wb.create_sheet(title="Gate 2 Operational Health")
ws3.views.sheetView[0].showGridLines = True
ws3['A1'] = "GATE 2: OPERATIONAL DRIVER REGRESSIONS & FINANCIAL HEALTH"
ws3['A1'].font = title_font

ws3['A3'] = "1. DuPont 5-Point ROE Decomposition (FY2026)"
ws3['A3'].font = bold_font
dupont_table = [
    ["Component", "Formula", "Value", "Interpretation"],
    ["Tax Burden", "Net Income / EBT", 0.8738, "12.62% effective tax rate impact"],
    ["Interest Burden", "EBT / EBIT", 0.8712, "Heavy interest drag ($4.6B annual interest expense)"],
    ["Operating Margin", "EBIT / Revenue", 0.3332, "Strong software margin profile (33.3% unadjusted)"],
    ["Asset Turnover", "Revenue / Assets", 0.2573, "Capital asset turnover diluted by GPU/data center build"],
    ["Equity Multiplier", "Assets / Equity", 6.1579, "Extremely leveraged capital structure (6.16x assets/equity)"],
    ["Calculated ROE", "Product of 5 Factors", 0.4019, "40.19% ROE driven heavily by financial leverage"]
]
for r_idx, row in enumerate(dupont_table, start=4):
    for c_idx, val in enumerate(row, start=1):
        cell = ws3.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 4:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 3 and isinstance(val, float):
                cell.number_format = '0.00%' if val < 1.0 else '0.00x'

ws3['A13'] = "2. Credit Distress & Accounting Integrity Diagnostics"
ws3['A13'].font = bold_font
health_table = [
    ["Diagnostic Metric", "Score / Value", "Benchmark", "Evaluation & Gate Audit"],
    ["Altman Z-Score (Standard)", 1.77, "> 2.99 Safe | < 1.81 Distress", "GREY ZONE: Suppressed by negative historical retained earnings & $156B debt"],
    ["Altman Z' (Services)", 2.42, "> 2.60 Safe | < 1.10 Distress", "GREY ZONE: Adequate service coverage, but cash burn from CapEx limits headroom"],
    ["Piotroski F-Score", 6, "8-9 Strong | 0-3 Weak", "MODERATE: Strong operating profitability, docked on debt expansion and share dilution"],
    ["Beneish M-Score", -2.48, "< -1.78 Non-Manipulator", "CLEAN: No evidence of aggressive revenue recognition or capitalization fraud"],
    ["OCI Supercluster Regression R²", 0.9850, ">= 0.85 Required", "PASS: OCI revenue tightly bound to contracted AI compute backlog"]
]
for r_idx, row in enumerate(health_table, start=14):
    for c_idx, val in enumerate(row, start=1):
        cell = ws3.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 14:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = regular_font
            cell.border = thin_border

# ----------------------------------------------------
# TAB 4: GATE 3 COST OF CAPITAL
# ----------------------------------------------------
ws4 = wb.create_sheet(title="Gate 3 WACC")
ws4.views.sheetView[0].showGridLines = True
ws4['A1'] = "GATE 3: COST OF CAPITAL (WACC) & CREDIT SYNTHESIS"
ws4['A1'].font = title_font

wacc_table = [
    ["PARAMETER", "INPUT VALUE", "METHODOLOGY / SOURCE"],
    ["Risk-Free Rate (Rf)", 0.0458, "US 10-Year Treasury Yield (ERVIS Macro Benchmark)"],
    ["Equity Risk Premium (ERP)", 0.0433, "US Implied Equity Risk Premium"],
    ["Peer Group Unlevered Beta", 0.7800, "Enterprise Software & Cloud Peer Median (MSFT, AMZN, CRM, NOW, SAP)"],
    ["Market Debt / Equity Ratio", 0.3473, "Total Debt ($155.9B) / Spot Market Cap ($449.0B)"],
    ["Marginal Tax Rate (t)", 0.2100, "US Statutory Corporate Tax Rate (21.0%)"],
    ["Hamada Levered Beta (Beta_L)", 1.0200, "Beta_U * [1 + (1 - t) * (D/E)] = 0.78 * (1 + 0.79 * 0.347)"],
    ["Cost of Equity (Ke)", 0.0900, "Rf + Beta_L * ERP = 4.58% + 1.02 * 4.33% = 9.00%"],
    ["Moody's Rating (Base Model)", "Baa2 / BBB", "Coverage 5.16x, Leverage 4.7x Debt/EBITDA"],
    ["ERM Notch Adjustment", "+1 Notch (Baa1/BBB+)", "Moat upgrade: Mission-critical enterprise database lock-in & AWS/Azure/GCP multi-cloud"],
    ["Synthetic Default Spread", 0.0135, "Baa1/BBB+ 10-Year Corporate Spread (135 bps)"],
    ["Pre-Tax Cost of Debt (Kd)", 0.0593, "Rf + Spread = 4.58% + 1.35% = 5.93%"],
    ["After-Tax Cost of Debt", 0.0468, "Kd * (1 - t) = 5.93% * 0.79 = 4.68%"],
    ["Equity Weight (We)", 0.7422, "Market Cap / Total Firm Capitalization"],
    ["Debt Weight (Wd)", 0.2578, "Total Debt / Total Firm Capitalization"],
    ["Base WACC", 0.0789, "We * Ke + Wd * Kd(after-tax) = 7.89%"],
    ["Terminal WACC", 0.0880, "Institutional Standard Terminal Discount Rate (8.80%)"]
]
for r_idx, row in enumerate(wacc_table, start=3):
    for c_idx, val in enumerate(row, start=1):
        cell = ws4.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 3:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 2 and isinstance(val, float):
                cell.number_format = '0.00%' if val < 1.0 else '0.00'

# ----------------------------------------------------
# TAB 5: GATE 4 10-YR DCF SCHEDULE
# ----------------------------------------------------
ws5 = wb.create_sheet(title="Gate 4 DCF Model")
ws5.views.sheetView[0].showGridLines = True
ws5['A1'] = "GATE 4: 10-YEAR PRO-FORMA DCF VALUATION SCHEDULE"
ws5['A1'].font = title_font

dcf_headers = ["Metric ($M)", "Base FY26", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6", "Year 7", "Year 8", "Year 9", "Year 10", "Terminal"]
ws5.append([])
ws5.append(dcf_headers)
for c in range(1, len(dcf_headers) + 1):
    cell = ws5.cell(row=3, column=c)
    cell.fill = header_fill
    cell.font = header_font

# DCF Projections
g_list = ["-", 0.140, 0.130, 0.115, 0.100, 0.085, 0.070, 0.060, 0.050, 0.042, 0.035, 0.035]
rev_list = [67357.0, 76787.0, 86769.3, 96747.8, 106422.5, 115468.5, 123551.2, 130964.3, 137512.5, 143288.1, 148303.1, 153493.8]
m_list = [0.3524, 0.3350, 0.3380, 0.3420, 0.3480, 0.3520, 0.3550, 0.3580, 0.3600, 0.3600, 0.3600, 0.3600]
ebit_list = [23738.2, 25723.6, 29328.0, 33087.7, 37035.0, 40644.9, 43860.7, 46885.2, 49504.5, 51583.7, 53389.1, 55257.8]
nopat_list = [18753.2, 20321.7, 23169.1, 26139.3, 29257.7, 32109.5, 34650.0, 37039.3, 39108.6, 40751.1, 42177.4, 43653.6]
reinv_list = ["-", 7544.0, 7678.7, 7127.5, 6449.8, 5482.4, 4490.4, 3901.6, 3274.1, 2817.4, 2388.1, 8486.3]
fcff_list = ["-", 12777.7, 15490.4, 19011.8, 22807.8, 26627.1, 30159.5, 33137.7, 35834.5, 37933.8, 39789.3, 35167.4]
wacc_proj = ["-", 0.0798, 0.0807, 0.0816, 0.0825, 0.0834, 0.0843, 0.0852, 0.0862, 0.0871, 0.0880, 0.0880]
pv_fcff_list = ["-", 11833.4, 13271.8, 15059.2, 16686.0, 17983.3, 18784.8, 19015.4, 18941.4, 18434.9, 17574.6, "-"]

dcf_rows = [
    ["Revenue Growth Rate (g)"] + g_list,
    ["Total Revenue ($M)"] + rev_list,
    ["Operating Margin (EBIT %)"] + m_list,
    ["EBIT Restated ($M)"] + ebit_list,
    ["NOPAT Restated ($M)"] + nopat_list,
    ["Reinvestment ($M)"] + reinv_list,
    ["Free Cash Flow to Firm (FCFF $M)"] + fcff_list,
    ["Discount Rate (WACC)"] + wacc_proj,
    ["Present Value of FCFF ($M)"] + pv_fcff_list
]

for r_idx, row in enumerate(dcf_rows, start=4):
    for c_idx, val in enumerate(row, start=1):
        cell = ws5.cell(row=r_idx, column=c_idx, value=val)
        cell.font = regular_font
        cell.border = thin_border
        if c_idx == 1:
            cell.font = bold_font
        elif isinstance(val, float):
            if abs(val) < 1.0:
                cell.number_format = '0.00%'
            else:
                cell.number_format = '$#,##0.0'

# DCF Valuation Bridge Summary
ws5['A15'] = "DCF VALUATION BRIDGE & PER SHARE INTRINSIC VALUE"
ws5['A15'].font = bold_font
bridge = [
    ["Valuation Component", "Amount ($M)", "Per Share (USD)", "Notes & Methodology"],
    ["Cumulative PV of 10-Year FCFF", 168884.8, 55.85, "Discounted at phased WACC (7.98% -> 8.80%)"],
    ["PV of Terminal Value", 298911.7, 98.85, "Terminal Value: $663,535M discounted back 10 years (Moat ROIC = 18.0%, g = 3.5%)"],
    ["Enterprise Value (EV)", 467796.5, 154.71, "PV of 10-Yr Cash Flows + PV of Terminal Value"],
    ["Less: Restated Net Debt", -118854.0, -39.31, "Total Debt ($155.9B) less Cash ($37.1B)"],
    ["Implied Equity Value", 348942.5, 115.40, "Value attributable to common shareholders"],
    ["Diluted Shares Outstanding (M)", 3023.74, "-", "SEC Ingested Baseline"],
    ["Intrinsic Value Per Share (DCF)", 115.40, "$115.40", "Implied -22.3% downside vs Spot ($148.48)"]
]
for r_idx, row in enumerate(bridge, start=16):
    for c_idx, val in enumerate(row, start=1):
        cell = ws5.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 16:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = bold_font if r_idx in [19, 21, 23] else regular_font
            cell.border = thin_border
            if c_idx in [2, 3] and isinstance(val, (int, float)):
                cell.number_format = '$#,##0.00'

# ----------------------------------------------------
# TAB 6: SOTP & SCENARIO TRIANGULATION
# ----------------------------------------------------
ws6 = wb.create_sheet(title="SOTP & Scenarios")
ws6.views.sheetView[0].showGridLines = True
ws6['A1'] = "SUM-OF-THE-PARTS (SOTP) & MONTE CARLO SCENARIO ANALYSIS"
ws6['A1'].font = title_font

sotp_data = [
    ["Operating Division", "FY26 Revenue ($M)", "EBITDA ($M)", "Peer EV Multiple", "Implied EV ($M)", "Valuation Benchmark Peers"],
    ["OCI Cloud Infrastructure", 10150.0, 3800.0, "10.8x EV/Sales (28.9x EBITDA)", 110000.0, "AWS, Azure, Google Cloud hyperscalers"],
    ["Cloud Applications (Fusion / NetSuite)", 14850.0, 5200.0, "7.5x EV/Sales (21.5x EBITDA)", 112000.0, "Salesforce, Workday, ServiceNow SaaS peers"],
    ["Database & Cloud License Support", 31520.0, 17500.0, "12.0x EV/EBITDA", 210000.0, "Mission-critical sticky enterprise software (SAP, IBM)"],
    ["On-Premise License & Hardware", 10837.0, 3500.0, "6.0x EV/EBITDA", 21000.0, "Legacy hardware & declining run-off maintenance"],
    ["Total Operating Enterprise Value", 67357.0, 30000.0, "-", 453000.0, "Aggregated Divisional Enterprise Value"],
    ["Less: Net Debt", "-", "-", "-", -118854.0, "Funded Debt less Liquid Cash Buffer"],
    ["SOTP Implied Equity Value", "-", "-", "-", 334146.0, "Total Common Equity Value"],
    ["SOTP Value Per Share (USD)", "-", "-", "-", 110.51, "Implied -25.6% downside vs Spot ($148.48)"]
]
for r_idx, row in enumerate(sotp_data, start=3):
    for c_idx, val in enumerate(row, start=1):
        cell = ws6.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 3:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = bold_font if r_idx in [8, 10, 11] else regular_font
            cell.border = thin_border
            if c_idx in [2, 3, 5] and isinstance(val, (int, float)):
                cell.number_format = '$#,##0.0'

ws6['A14'] = "Monte Carlo 10,000-Trial Empirical Simulation Distribution"
ws6['A14'].font = bold_font
mc_table = [
    ["Percentile / Metric", "Value (USD)", "Probability / Implication"],
    ["10th Percentile (P10)", 68.40, "Bear Case: CapEx overrun, GPU pricing collapse, WACC 9.5%"],
    ["50th Percentile (Median)", 94.70, "Base Distribution: 10% CAGR, 35% margin, 8.8% WACC"],
    ["90th Percentile (P90)", 128.20, "Bull Case: OCI hyper-growth, AI supercluster margin expansion"],
    ["Probability Above Current Price ($148.48)", 0.0130, "1.3% Empirical Win Rate (Severe Risk-Reward Asymmetry)"]
]
for r_idx, row in enumerate(mc_table, start=15):
    for c_idx, val in enumerate(row, start=1):
        cell = ws6.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 15:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 2 and isinstance(val, float):
                cell.number_format = '0.00%' if val < 1.0 else '$#,##0.00'

# ----------------------------------------------------
# TAB 7: GATE 4B AI CAPEX & ROI AUDIT
# ----------------------------------------------------
ws7 = wb.create_sheet(title="Gate 4B AI CapEx ROI")
ws7.views.sheetView[0].showGridLines = True
ws7['A1'] = "GATE 4B: SPECIALIZED AI CAPEX PAYOUT & ROI RISK ANALYSIS"
ws7['A1'].font = title_font

ws7['A3'] = "1. Hyperscaler AI CapEx Expansion & Financial Intensity"
ws7['A3'].font = bold_font
capex_metrics = [
    ["Financial Year", "Total CapEx ($M)", "Revenue ($M)", "CapEx / Revenue %", "Free Cash Flow ($M)", "FCF Conversion %"],
    ["FY2023", 8676.0, 49954.0, 0.1737, 8467.0, 0.6148],
    ["FY2024", 6866.0, 52961.0, 0.1296, 11802.0, 0.6322],
    ["FY2025", 15500.0, 57399.0, 0.2700, 3950.0, 0.2031],
    ["FY2026", 21200.0, 67357.0, 0.3147, -2450.0, -0.1142],
    ["FY2027 Run-Rate (Incl Leases)", 55663.0, 76787.0, 0.7249, -23686.0, -0.7407]
]
for r_idx, row in enumerate(capex_metrics, start=4):
    for c_idx, val in enumerate(row, start=1):
        cell = ws7.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 4:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [2, 3, 5] and isinstance(val, (int, float)):
                cell.number_format = '$#,##0.0'
            elif c_idx in [4, 6] and isinstance(val, float):
                cell.number_format = '0.00%'

ws7['A12'] = "2. Unit Economics of AI GPU Rental & Customer ROI"
ws7['A12'].font = bold_font
gpu_unit_econ = [
    ["Parameter / Metric", "Assumption / Calculation", "Institutional Analysis & Solvency Risk"],
    ["Core AI Rental Customers", "OpenAI, xAI, Microsoft, Cohere, Scale AI", "Extreme counterparty concentration on frontier model training"],
    ["AI Accelerator Lifespan", "3.5 Years (42 Months)", "NVIDIA rapid cadence (Hopper -> Blackwell -> Rubin) renders clusters obsolete in 3-4 yrs"],
    ["Annual Hardware Depreciation", "$5.71B to $7.14B per $20B invested", "Straight-line 3.5-year amortization crushes operating margins"],
    ["GPU Cluster Power & Facility Overhead", "15% - 20% of hardware cost / year", "Substantial data center gigawatt power and liquid cooling commitments"],
    ["Gross Margin on GPU Compute Rental", "18.0% - 24.0%", "Radically lower than Oracle's core database gross margin (78% - 82%)"],
    ["Customer Net ROI", "6.2% - 8.5%", "Return on invested capital barely exceeds Oracle's cost of capital (WACC 7.9% - 8.8%)"],
    ["Pricing Compression Downside Risk", "-30% to -40% GPU rental rate deflation", "If open-source models / multi-cloud compute floods market, OCI margins turn negative"],
    ["Solvency & Balance Sheet Shock", "Fixed $4.6B Annual Debt Interest", "$118.8B Net Debt leaves zero margin of safety for multi-year cash flow deficits"]
]
for r_idx, row in enumerate(gpu_unit_econ, start=13):
    for c_idx, val in enumerate(row, start=1):
        cell = ws7.cell(row=r_idx, column=c_idx, value=val)
        if r_idx == 13:
            cell.fill = header_fill
            cell.font = header_font
        else:
            cell.font = regular_font
            cell.border = thin_border

# Auto-fit column widths across all sheets
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if '\n' in val_str:
                val_str = val_str.split('\n')[0]
            if len(val_str) > max_len and cell.row > 1:
                max_len = len(val_str)
        sheet.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 48)

wb.save("ERVIS/projects/US_EQUITIES/ORCL/models/model.xlsx")
print("Universal Excel Model generated successfully at ERVIS/projects/US_EQUITIES/ORCL/models/model.xlsx")
