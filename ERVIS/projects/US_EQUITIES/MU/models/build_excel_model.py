import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
wb.remove(wb.active) # Remove default sheet

# Colors
navy_header = PatternFill(start_color="1A365D", end_color="1A365D", fill_type="solid")
navy_subheader = PatternFill(start_color="2B6CB0", end_color="2B6CB0", fill_type="solid")
light_blue = PatternFill(start_color="EBF8FF", end_color="EBF8FF", fill_type="solid")
beige_fill = PatternFill(start_color="FAF7F2", end_color="FAF7F2", fill_type="solid")
gray_fill = PatternFill(start_color="F7FAFC", end_color="F7FAFC", fill_type="solid")

font_title = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
font_subtitle = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True)
font_regular = Font(name="Calibri", size=10)
font_italic = Font(name="Calibri", size=9, italic=True)

thin_border = Border(
    left=Side(style="thin", color="CBD5E0"),
    right=Side(style="thin", color="CBD5E0"),
    top=Side(style="thin", color="CBD5E0"),
    bottom=Side(style="thin", color="CBD5E0")
)
double_bottom = Border(
    top=Side(style="thin", color="CBD5E0"),
    bottom=Side(style="double", color="1A202C")
)

# -------------------------------------------------------------
# TAB 1: COVER_SUMMARY
# -------------------------------------------------------------
ws1 = wb.create_sheet(title="COVER_SUMMARY")
ws1.views.sheetView[0].showGridLines = True

ws1.merge_cells("A1:G1")
ws1["A1"] = "ERVIS INSTITUTIONAL EQUITY VALUATION MODEL: MICRON TECHNOLOGY, INC. (NASDAQ: MU)"
ws1["A1"].font = font_title
ws1["A1"].fill = navy_header
ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws1.row_dimensions[1].height = 35

summary_data = [
    ["EXECUTIVE VALUATION SUMMARY", "", "", "", "", ""],
    ["Ticker:", "MU", "", "Valuation Date:", "2026-11-21", ""],
    ["Company Name:", "Micron Technology, Inc.", "", "Spot Share Price:", 594.51, "USD"],
    ["Sector / Industry:", "Technology / Semiconductors", "", "Diluted Shares Out:", 1131.42, "Million"],
    ["Market Capitalization:", 672642.4, "USD M", "Enterprise Value:", 604678.4, "USD M"],
    ["", "", "", "", "", ""],
    ["VALUATION METHODOLOGY TRIANGULATION", "", "", "", "", ""],
    ["Methodology", "Per Share Value (USD)", "Implied Equity Value ($B)", "Spread vs Spot", "Status", ""],
    ["1. Base DCF (Plan A Mean-Reverting)", 604.08, 683.5, 0.0161, "FAIR VALUE ANCHOR", ""],
    ["2. SOTP Divisional Multiple Model", 501.54, 567.5, -0.1564, "CONSERVATIVE MULTIPLE", ""],
    ["3. Monte Carlo Median (P50)", 590.70, 668.3, -0.0064, "CENTRAL GRAVITY", ""],
    ["4. Monte Carlo Bull (P90)", 860.25, 973.3, 0.4470, "HBM PERSISTENCE", ""],
    ["5. Monte Carlo Bear (P10)", 426.70, 482.8, -0.2823, "CYCLICAL TROUGH", ""],
    ["6. Asset Haircut Liquidation Floor", 58.68, 66.4, -0.9013, "DOWNSIDE SOLVENCY FLOOR", ""],
    ["", "", "", "", "", ""],
    ["FINAL INVESTMENT RECOMMENDATION", "", "", "", "", ""],
    ["Blended Target Price (70% DCF / 30% SOTP):", 573.32, "USD", "Valuation Rating:", "NEUTRAL / HOLD", ""],
    ["Tactical Accumulation Range:", "$450.00 - $520.00", "", "Margin of Safety:", "Within Fair Value", ""]
]

r_idx = 3
for row in summary_data:
    for c_idx, val in enumerate(row, 1):
        cell = ws1.cell(row=r_idx, column=c_idx, value=val)
        cell.font = font_regular
        cell.border = thin_border
        if val in ["EXECUTIVE VALUATION SUMMARY", "VALUATION METHODOLOGY TRIANGULATION", "FINAL INVESTMENT RECOMMENDATION"]:
            cell.font = font_subtitle
            cell.fill = navy_subheader
        elif c_idx == 1 and val != "":
            cell.font = font_bold
        if isinstance(val, float) and c_idx in [2, 5]:
            cell.number_format = "$#,##0.00" if val < 1000 else "$#,##0.0"
        elif isinstance(val, float) and c_idx == 4:
            cell.number_format = "+0.0%;-0.0%"
    r_idx += 1

# -------------------------------------------------------------
# TAB 2: DCF_PRO_FORMA
# -------------------------------------------------------------
ws2 = wb.create_sheet(title="DCF_PRO_FORMA")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells("A1:K1")
ws2["A1"] = "10-YEAR PRO-FORMA FCFF VALUATION SCHEDULE (PLAN A MEAN-REVERTING MARGINS)"
ws2["A1"].font = font_title
ws2["A1"].fill = navy_header
ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws2.row_dimensions[1].height = 35

dcf_headers = ["Metric / Year", "FY26 Base", "FY27 (Y1)", "FY28 (Y2)", "FY29 (Y3)", "FY30 (Y4)", "FY31 (Y5)", "FY32 (Y6)", "FY33 (Y7)", "FY34 (Y8)", "FY35 (Y9)", "FY36 (Y10)"]
for c_idx, h in enumerate(dcf_headers, 1):
    cell = ws2.cell(row=3, column=c_idx, value=h)
    cell.font = font_subtitle
    cell.fill = navy_subheader
    cell.alignment = Alignment(horizontal="center", vertical="center")

proforma_rows = [
    ["Revenue ($M)", 133188.0, 143843.0, 149596.8, 149596.8, 142116.9, 144959.3, 150757.6, 156787.9, 161491.6, 166336.3, 171326.4],
    ["YoY Revenue Growth %", None, 0.08, 0.04, 0.00, -0.05, 0.02, 0.04, 0.04, 0.03, 0.03, 0.03],
    ["Operating EBIT Margin %", 0.7459, 0.7000, 0.6000, 0.5000, 0.4200, 0.3800, 0.3500, 0.3500, 0.3500, 0.3500, 0.3500],
    ["Adjusted EBIT ($M)", 100992.0, 100690.1, 89758.1, 74798.4, 59689.1, 55084.5, 52765.2, 54875.8, 56522.0, 58217.7, 59964.2],
    ["Effective Tax Rate %", 0.1481, 0.1550, 0.1618, 0.1687, 0.1756, 0.1824, 0.1893, 0.1962, 0.2031, 0.2100, 0.2100],
    ["NOPAT ($M)", 86035.1, 85085.1, 75231.7, 62180.2, 49209.6, 45035.1, 42776.2, 44108.6, 45042.4, 45992.0, 47371.8],
    ["Reinvestment ($M)", None, 4843.2, 2615.3, 0.0, 0.0, 1292.0, 2635.6, 2741.0, 2138.0, 2202.1, 2268.2],
    ["Free Cash Flow to Firm (FCFF)", None, 80241.9, 72616.4, 62180.2, 49209.6, 43743.1, 40140.6, 41367.6, 42904.4, 43789.9, 45103.5],
    ["Discount Factor (Cumulative)", 1.0, 0.9049, 0.8188, 0.7409, 0.6705, 0.6067, 0.5541, 0.5060, 0.4621, 0.4220, 0.3889],
    ["Present Value of FCFF ($M)", None, 72610.5, 59475.2, 46081.9, 33006.1, 26543.8, 22248.8, 20939.9, 19833.6, 18485.4, 17364.5]
]

for r_offset, r_data in enumerate(proforma_rows, 4):
    for c_idx, val in enumerate(r_data, 1):
        cell = ws2.cell(row=r_offset, column=c_idx, value=val)
        cell.font = font_bold if c_idx == 1 or r_data[0] in ["Present Value of FCFF ($M)", "Free Cash Flow to Firm (FCFF)"] else font_regular
        cell.border = thin_border
        if r_data[0] in ["Present Value of FCFF ($M)", "Free Cash Flow to Firm (FCFF)"]:
            cell.fill = light_blue
        if val is not None and isinstance(val, float):
            if "%" in r_data[0]:
                cell.number_format = "0.0%"
            elif "Discount Factor" in r_data[0]:
                cell.number_format = "0.0000"
            else:
                cell.number_format = "$#,##0.0"

# DCF Bridge Summary on Tab 2
dcf_bridge = [
    ["", ""],
    ["DCF VALUATION BRIDGE & PERPETUAL TERMINAL VALUE", ""],
    ["Cumulative Undiscounted 10-Yr FCFF ($M):", 524297.2],
    ["PV of 10-Year Discrete FCFF ($M):", 339529.7],
    ["Terminal Growth Rate (g):", 0.030],
    ["Terminal Cost of Capital (WACC):", 0.085],
    ["Terminal ROIC:", 0.150],
    ["Terminal Reinvestment Rate:", 0.200],
    ["Terminal Year FCFF ($M):", 39034.3],
    ["Terminal Value at Year 10 ($M):", 709715.1],
    ["PV of Terminal Value ($M):", 276079.2],
    ["ENTERPRISE VALUE (EV) ($M):", 615608.9],
    ["Audited Liquid Cash & Securities ($M):", 73453.0],
    ["Audited Funded & Synthetic Debt ($M):", -5489.0],
    ["NET CASH POSITION ($M):", 67964.0],
    ["IMPLIED EQUITY INTRINSIC VALUE ($M):", 683572.9],
    ["Diluted Common Shares Outstanding (M):", 1131.42],
    ["DCF INTRINSIC VALUE PER SHARE (USD):", 604.08]
]

r_b = 16
for label, val in dcf_bridge:
    if label == "":
        r_b += 1
        continue
    c1 = ws2.cell(row=r_b, column=1, value=label)
    c2 = ws2.cell(row=r_b, column=2, value=val)
    c1.border = thin_border
    c2.border = thin_border
    if label == "DCF VALUATION BRIDGE & PERPETUAL TERMINAL VALUE":
        c1.font = font_subtitle
        c1.fill = navy_subheader
        c2.fill = navy_subheader
    elif label in ["ENTERPRISE VALUE (EV) ($M):", "IMPLIED EQUITY INTRINSIC VALUE ($M):", "DCF INTRINSIC VALUE PER SHARE (USD):"]:
        c1.font = font_bold
        c2.font = font_bold
        c1.fill = light_blue
        c2.fill = light_blue
        c2.border = double_bottom
    else:
        c1.font = font_bold
        c2.font = font_regular
    if isinstance(val, float):
        if "Rate" in label or "ROIC" in label or "WACC" in label:
            c2.number_format = "0.0%"
        elif "PER SHARE" in label:
            c2.number_format = "$#,##0.00"
        else:
            c2.number_format = "$#,##0.0"
    r_b += 1

# -------------------------------------------------------------
# TAB 3: WACC_AND_CREDIT
# -------------------------------------------------------------
ws3 = wb.create_sheet(title="WACC_AND_CREDIT")
ws3.views.sheetView[0].showGridLines = True
ws3.merge_cells("A1:F1")
ws3["A1"] = "WACC DERIVATION, HAMADA BETA & MOODY'S CREDIT RATING SYNTHESIS"
ws3["A1"].font = font_title
ws3["A1"].fill = navy_header
ws3["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws3.row_dimensions[1].height = 35

wacc_data = [
    ["CAPITAL ASSET PRICING MODEL (CAPM) PARAMETERS", ""],
    ["Risk-Free Rate (10-Yr US Treasury) (Rf):", 0.0494],
    ["Damodaran Implied Equity Risk Premium (ERP):", 0.0461],
    ["Semiconductor Memory Unlevered Beta (Beta_U):", 1.210],
    ["Market Value of Equity (E) ($M):", 672642.4],
    ["Adjusted Total Debt (D) ($M):", 5489.0],
    ["Market Debt-to-Equity (D/E Ratio):", 0.00816],
    ["Audited Effective Tax Rate (t):", 0.1481],
    ["Hamada Re-Levered Beta (Beta_L):", 1.218],
    ["Cost of Equity (Ke):", 0.1056],
    ["", ""],
    ["MOODY'S 6-METRIC INDUSTRIAL CREDIT RATING GRID", ""],
    ["1. Interest Coverage Ratio (Adjusted EBIT / Interest):", "952.8x (Aaa / AAA)"],
    ["2. Leverage Ratio (Debt / EBITDA):", "0.05x (Aaa / AAA)"],
    ["3. Return on Assets (Adjusted EBIT / Total Assets):", "51.56% (Aaa / AAA)"],
    ["4. Asset Coverage Ratio (Tangible Assets / Debt):", "25.0x (Aaa / AAA)"],
    ["5. Operating Margin (Adjusted EBIT / Revenue):", "75.83% (Aaa / AAA)"],
    ["6. Liquidity Ratio (Current Assets / Current Liab):", "3.31x (Aaa / AAA)"],
    ["Synthetic Unconstrained Credit Rating:", "Aaa / AAA (Spread = 60 bps)"],
    ["Qualitative Industry Cyclical Rating Cap:", "Baa1 / BBB+ (Spread = 135 bps)"],
    ["Pre-Tax Cost of Debt (Kd):", 0.0554],
    ["After-Tax Cost of Debt (Kd * (1 - t)):", 0.0472],
    ["", ""],
    ["BLENDED COST OF CAPITAL (WACC) TERM STRUCTURE", ""],
    ["Capital Weight of Equity (We):", 0.9919],
    ["Capital Weight of Debt (Wd):", 0.0081],
    ["Phase 1 WACC (Years 1–5):", 0.1051],
    ["Phase 2 WACC (Years 6–9):", 0.0950],
    ["Terminal WACC (Year 10+):", 0.0850]
]

r_w = 3
for label, val in wacc_data:
    c1 = ws3.cell(row=r_w, column=1, value=label)
    c2 = ws3.cell(row=r_w, column=2, value=val)
    c1.border = thin_border
    c2.border = thin_border
    if label in ["CAPITAL ASSET PRICING MODEL (CAPM) PARAMETERS", "MOODY'S 6-METRIC INDUSTRIAL CREDIT RATING GRID", "BLENDED COST OF CAPITAL (WACC) TERM STRUCTURE"]:
        c1.font = font_subtitle
        c1.fill = navy_subheader
        c2.fill = navy_subheader
    else:
        c1.font = font_bold if "WACC" in label or "Cost" in label else font_regular
        c2.font = font_bold if "WACC" in label or "Cost" in label else font_regular
    if isinstance(val, float):
        if "Rate" in label or "Cost" in label or "ERP" in label or "WACC" in label or "Weight" in label:
            c2.number_format = "0.00%"
        elif "Beta" in label:
            c2.number_format = "0.000"
        elif "Ratio" in label:
            c2.number_format = "0.0000"
        else:
            c2.number_format = "$#,##0.0"
    r_w += 1

# Auto-adjust column widths across all sheets
for ws in [ws1, ws2, ws3]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if len(val_str) > max_len and "\n" not in val_str:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

wb.save("ERVIS/projects/US_EQUITIES/MU/models/model.xlsx")
print("Universal Excel Model built successfully at ERVIS/projects/US_EQUITIES/MU/models/model.xlsx")
