import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
wb.remove(wb.active) # Remove default sheet

# Styling definitions
navy_header = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
navy_subheader = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
slate_bar = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
light_blue = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
emerald_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
amber_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
gray_backdrop = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
yellow_input = PatternFill(start_color="FEF9C3", end_color="FEF9C3", fill_type="solid")

font_title = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
font_subtitle = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_sec_hdr = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True, color="0F172A")
font_regular = Font(name="Calibri", size=10, color="1E293B")
font_gray_default = Font(name="Calibri", size=10, bold=False, color="64748B")
font_override_input = Font(name="Calibri", size=10, bold=True, color="1E3A8A")
font_effective = Font(name="Calibri", size=10, bold=True, color="047857")
font_italic_note = Font(name="Calibri", size=9, italic=True, color="475569")

thin_border = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1")
)
double_bottom = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="double", color="0F172A")
)
input_border = Border(
    left=Side(style="medium", color="D97706"),
    right=Side(style="medium", color="D97706"),
    top=Side(style="medium", color="D97706"),
    bottom=Side(style="medium", color="D97706")
)

# ==============================================================================
# TAB 1: INPUTS (DYNAMIC OVERRIDE STUDIO)
# ==============================================================================
ws_in = wb.create_sheet(title="INPUTS")
ws_in.views.sheetView[0].showGridLines = True

ws_in.merge_cells("A1:G1")
ws_in["A1"] = "ERVIS INSTITUTIONAL VALUATION INPUT STUDIO :: MICRON TECHNOLOGY, INC. (NASDAQ: MU)"
ws_in["A1"].font = font_title
ws_in["A1"].fill = navy_header
ws_in["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_in.row_dimensions[1].height = 34

ws_in.merge_cells("A2:G2")
ws_in["A2"] = "USER INSTRUCTION: Enter scenario overrides in Column D (Yellow cells). If left BLANK, Column E automatically defaults to Column C."
ws_in["A2"].font = font_italic_note
ws_in["A2"].fill = gray_backdrop
ws_in["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws_in.row_dimensions[2].height = 22

input_headers = ["Code", "Parameter Description", "Institutional Default [Plan A]", "User Input / Override", "Effective Value Used", "Unit / Format", "SEC 10-K / Data Provenance"]
ws_in.row_dimensions[4].height = 24
for c_idx, h in enumerate(input_headers, 1):
    cell = ws_in.cell(row=4, column=c_idx, value=h)
    cell.font = font_subtitle
    cell.fill = navy_subheader
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

inputs_definitions = [
    # General Info
    ("SECTION", "1. GENERAL MARKET & CAPITAL STRUCTURE ANCHORS", None, None, None),
    ("SPOT_PX", "Market Spot Share Price", 594.51, "USD", "Market Spot Price (Post-Correction from $1,255 Peak)"),
    ("SHARES", "Diluted Common Shares Outstanding", 1131.42, "Shares_M", "FY26 Audited Form 10-K Diluted Share Count"),
    
    # Base Fundamentals
    ("SECTION", "2. BASE YEAR FINANCIALS (FY2026 AUDITED FORM 10-K)", None, None, None),
    ("BASE_REV", "Base Net Sales / Revenue Year 0", 133188.0, "USD_M", "FY2026 Form 10-K Audited Net Sales ($133.2B)"),
    ("BASE_EBIT", "Base Operating Income / Adjusted EBIT Year 0", 100992.0, "USD_M", "Restated EBIT with 4-Yr R&D Capitalization ($101.0B)"),
    ("TAX_RATE_B", "Base Effective Corporate Tax Rate", 0.1481, "PCT", "FY2026 Audited Effective Provision for Income Taxes (14.81%)"),
    ("TAX_RATE_M", "Marginal Statutory Corporate Tax Rate", 0.2100, "PCT", "US Federal + State Statutory Corporate Rate (21.0%)"),
    
    # Growth Trajectory
    ("SECTION", "3. 10-YEAR REVENUE GROWTH TRAJECTORY (% PER ANNUM)", None, None, None),
    ("G_Y1", "Year 1 Revenue Growth Rate (FY2027)", 0.080, "PCT", "HBM3E / 12-High Ramp with 100% Locked Capacity"),
    ("G_Y2", "Year 2 Revenue Growth Rate (FY2028)", 0.040, "PCT", "HBM4 Transition; High Baseline Digestion"),
    ("G_Y3", "Year 3 Revenue Growth Rate (FY2029)", 0.000, "PCT", "Mid-Cycle Memory Digestion / Plateau"),
    ("G_Y4", "Year 4 Revenue Growth Rate (FY2030)", -0.050, "PCT", "Cyclical Downcycle / Price Softening"),
    ("G_Y5", "Year 5 Revenue Growth Rate (FY2031)", 0.020, "PCT", "DRAM/NAND Capacity Normalization Trough"),
    ("G_Y6", "Year 6 Revenue Growth Rate (FY2032)", 0.040, "PCT", "Next-Gen AI / Quantum Interface Cycle Recovery"),
    ("G_Y7", "Year 7 Revenue Growth Rate (FY2033)", 0.040, "PCT", "Industry Expansion Phase"),
    ("G_Y8", "Year 8 Revenue Growth Rate (FY2034)", 0.030, "PCT", "Convergence Phase"),
    ("G_Y9", "Year 9 Revenue Growth Rate (FY2035)", 0.030, "PCT", "Convergence Phase"),
    ("G_Y10", "Year 10 Revenue Growth Rate (FY2036)", 0.030, "PCT", "Final Pro-Forma Year Growth"),
    ("G_TERM", "Perpetual Terminal Growth Rate (gn)", 0.030, "PCT", "Capped at Long-Term Risk-Free Rate (3.0% Max)"),
    
    # Margin Schedule
    ("SECTION", "4. OPERATING MARGIN TRAJECTORY (% OF NET SALES)", None, None, None),
    ("M_Y1", "Year 1 Target Operating Margin (FY2027)", 0.700, "PCT", "Mean-Reverting from Peak 74.6% as Supply Scales"),
    ("M_Y2", "Year 2 Target Operating Margin (FY2028)", 0.600, "PCT", "Contract Normalization Across Cloud Hyperscalers"),
    ("M_Y3", "Year 3 Target Operating Margin (FY2029)", 0.500, "PCT", "Cyclical Spread Compression"),
    ("M_Y4", "Year 4 Target Operating Margin (FY2030)", 0.420, "PCT", "Mid-Cycle Normalization"),
    ("M_Y5", "Year 5 Target Operating Margin (FY2031)", 0.380, "PCT", "Stabilizing Transition"),
    ("M_TERM", "Terminal Target Operating Margin (Y6–10+)", 0.350, "PCT", "Sustainable 3-Player Oligopoly Equilibrium Margin"),
    
    # Capital Efficiency
    ("SECTION", "5. CAPITAL EFFICIENCY & REINVESTMENT", None, None, None),
    ("S2C_P1", "Phase 1 Marginal Sales-to-Capital Ratio (Y1–5)", 2.20, "MULT", "Audited FY26 Marginal Revenue Efficiency per Reinvestment Dollar"),
    ("S2C_P2", "Phase 2 Marginal Sales-to-Capital Ratio (Y6–10)", 1.85, "MULT", "Long-Run Semiconductor Capital Intensity Equilibrium"),
    ("ROIC_TERM", "Terminal Return on Invested Capital (ROIC)", 0.150, "PCT", "Oligopolistic Cost of Capital Premium (+650 bps over WACC)"),
    
    # Cost of Capital
    ("SECTION", "6. COST OF CAPITAL (WACC) & SYSTEMATIC RISK", None, None, None),
    ("RF_RATE", "Risk-Free Benchmark Rate (10-Yr US Treasury)", 0.0494, "PCT", "Audited US 10-Yr Constant Maturity Yield (4.94%)"),
    ("ERP", "Damodaran Implied US Equity Risk Premium", 0.0461, "PCT", "Damodaran Dynamic Cash Flow-Implied ERP (4.61%)"),
    ("BETA_U", "Semiconductor Memory Unlevered Asset Beta", 1.210, "MULT", "Delevered Pure-Play Semiconductor Asset Beta"),
    ("DE_RATIO", "Market Debt-to-Equity Capital Ratio", 0.00816, "MULT", "Market Debt ($5.49B) / Equity Cap ($672.6B)"),
    ("PRE_TAX_KD", "Pre-Tax Synthetic Cost of Debt (Kd)", 0.0554, "PCT", "Rf (4.94%) + 60 bps Synthetic Aaa Spread"),
    ("WACC_P1", "Phase 1 Discount Rate / WACC (Years 1–5)", 0.1051, "PCT", "CAPM Cost of Equity 10.56% with 0.81% Debt Weight"),
    ("WACC_P2", "Phase 2 Discount Rate / WACC (Years 6–9)", 0.0950, "PCT", "Maturing Transition Cost of Capital"),
    ("WACC_TERM", "Terminal Discount Rate / WACC (Year 10+)", 0.0850, "PCT", "Long-Run Steady State Cost of Capital"),
    
    # Balance Sheet Bridge
    ("SECTION", "7. BALANCE SHEET CASH & DEBT BRIDGE (USD MILLION)", None, None, None),
    ("CASH_SEC", "Cash, Cash Equivalents & Liquid Securities", 73453.0, "USD_M", "FY2026 Form 10-K Audited Balance Sheet"),
    ("TOT_DEBT", "Total Debt & Synthetic Lease Liabilities", 5489.0, "USD_M", "Funded Debt ($5,179M) + PV Operating Leases ($310M)")
]

current_row = 5
param_row_map = {}

for item in inputs_definitions:
    code = item[0]
    desc = item[1]
    
    if code == "SECTION":
        ws_in.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=7)
        sec_cell = ws_in.cell(row=current_row, column=1, value=desc)
        sec_cell.font = font_sec_hdr
        sec_cell.fill = slate_bar
        sec_cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws_in.row_dimensions[current_row].height = 20
        current_row += 1
        continue
        
    default_val = item[2]
    fmt = item[3]
    prov = item[4]
    param_row_map[code] = current_row
    
    # Col 1: Code
    c1 = ws_in.cell(row=current_row, column=1, value=code)
    c1.font = font_bold
    c1.border = thin_border
    c1.alignment = Alignment(horizontal="center", vertical="center")
    
    # Col 2: Desc
    c2 = ws_in.cell(row=current_row, column=2, value=desc)
    c2.font = font_regular
    c2.border = thin_border
    c2.alignment = Alignment(horizontal="left", vertical="center")
    
    # Col 3: Institutional Default (Gray backdrop)
    c3 = ws_in.cell(row=current_row, column=3, value=default_val)
    c3.font = font_gray_default
    c3.fill = gray_backdrop
    c3.border = thin_border
    c3.alignment = Alignment(horizontal="right", vertical="center")
    
    # Col 4: User Override Input (Yellow input box, blank initially)
    c4 = ws_in.cell(row=current_row, column=4, value="")
    c4.font = font_override_input
    c4.fill = yellow_input
    c4.border = input_border
    c4.alignment = Alignment(horizontal="right", vertical="center")
    
    # Col 5: Effective Value (Formula: =IF(ISBLANK(D...), C..., D...))
    eff_formula = f'=IF(ISBLANK(D{current_row}), C{current_row}, D{current_row})'
    c5 = ws_in.cell(row=current_row, column=5, value=eff_formula)
    c5.font = font_effective
    c5.fill = emerald_fill
    c5.border = thin_border
    c5.alignment = Alignment(horizontal="right", vertical="center")
    
    # Col 6: Format / Unit
    c6 = ws_in.cell(row=current_row, column=6, value=fmt)
    c6.font = font_italic_note
    c6.border = thin_border
    c6.alignment = Alignment(horizontal="center", vertical="center")
    
    # Col 7: Provenance Note
    c7 = ws_in.cell(row=current_row, column=7, value=prov)
    c7.font = font_italic_note
    c7.border = thin_border
    c7.alignment = Alignment(horizontal="left", vertical="center")
    
    # Format numbers
    for col_c in [c3, c4, c5]:
        if fmt == "USD":
            col_c.number_format = "$#,##0.00"
        elif fmt == "USD_M":
            col_c.number_format = "$#,##0.0"
        elif fmt == "Shares_M":
            col_c.number_format = "#,##0.00"
        elif fmt == "PCT":
            col_c.number_format = "0.00%"
        elif fmt == "MULT":
            col_c.number_format = "0.000x"
            
    ws_in.row_dimensions[current_row].height = 19
    current_row += 1

# ==============================================================================
# TAB 2: DCF_PRO_FORMA
# ==============================================================================
ws_dcf = wb.create_sheet(title="DCF_PRO_FORMA")
ws_dcf.views.sheetView[0].showGridLines = True

ws_dcf.merge_cells("A1:M1")
ws_dcf["A1"] = "10-YEAR PRO-FORMA FCFF VALUATION SCHEDULE (DYNAMICALLY LINKED TO INPUTS TAB)"
ws_dcf["A1"].font = font_title
ws_dcf["A1"].fill = navy_header
ws_dcf["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_dcf.row_dimensions[1].height = 34

dcf_col_headers = [
    "Line Item / Metric", "Base FY26", 
    "FY27 (Y1)", "FY28 (Y2)", "FY29 (Y3)", "FY30 (Y4)", "FY31 (Y5)", 
    "FY32 (Y6)", "FY33 (Y7)", "FY34 (Y8)", "FY35 (Y9)", "FY36 (Y10)", "Terminal"
]
ws_dcf.row_dimensions[3].height = 24
for c_idx, h in enumerate(dcf_col_headers, 1):
    cell = ws_dcf.cell(row=3, column=c_idx, value=h)
    cell.font = font_subtitle
    cell.fill = navy_subheader
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

# Row 4: Growth Rate
ws_dcf.cell(row=4, column=1, value="Revenue Growth Rate (%)").font = font_bold
ws_dcf.cell(row=4, column=2, value="--").alignment = Alignment(horizontal="center")
for y in range(1, 11):
    col = y + 2
    param_code = f"G_Y{y}"
    r_inp = param_row_map[param_code]
    cell = ws_dcf.cell(row=4, column=col, value=f"=INPUTS!E{r_inp}")
    cell.font = font_regular
    cell.number_format = "+0.0%;-0.0%;0.0%"
    cell.border = thin_border
cell_term_g = ws_dcf.cell(row=4, column=13, value=f"=INPUTS!E{param_row_map['G_TERM']}")
cell_term_g.font = font_bold
cell_term_g.number_format = "0.00%"
cell_term_g.border = thin_border

# Row 5: Revenue ($M)
ws_dcf.cell(row=5, column=1, value="Net Sales / Revenue ($M)").font = font_bold
ws_dcf.cell(row=5, column=2, value=f"=INPUTS!E{param_row_map['BASE_REV']}").font = font_bold
ws_dcf.cell(row=5, column=2).number_format = "$#,##0.0"
ws_dcf.cell(row=5, column=2).border = thin_border
for y in range(1, 11):
    col = y + 2
    prev_col_letter = get_column_letter(col - 1)
    cur_col_letter = get_column_letter(col)
    cell = ws_dcf.cell(row=5, column=col, value=f"={prev_col_letter}5*(1+{cur_col_letter}4)")
    cell.font = font_regular
    cell.number_format = "$#,##0.0"
    cell.border = thin_border
ws_dcf.cell(row=5, column=13, value="=L5*(1+M4)").font = font_bold
ws_dcf.cell(row=5, column=13).number_format = "$#,##0.0"
ws_dcf.cell(row=5, column=13).border = thin_border

# Row 6: Operating Margin (%)
ws_dcf.cell(row=6, column=1, value="Operating Margin (%)").font = font_bold
ws_dcf.cell(row=6, column=2, value=f"=INPUTS!E{param_row_map['BASE_EBIT']}/INPUTS!E{param_row_map['BASE_REV']}").font = font_bold
ws_dcf.cell(row=6, column=2).number_format = "0.00%"
ws_dcf.cell(row=6, column=2).border = thin_border
for y in range(1, 6):
    col = y + 2
    param_code = f"M_Y{y}"
    r_inp = param_row_map[param_code]
    cell = ws_dcf.cell(row=6, column=col, value=f"=INPUTS!E{r_inp}")
    cell.font = font_regular
    cell.number_format = "0.00%"
    cell.border = thin_border
for y in range(6, 11):
    col = y + 2
    cell = ws_dcf.cell(row=6, column=col, value=f"=INPUTS!E{param_row_map['M_TERM']}")
    cell.font = font_regular
    cell.number_format = "0.00%"
    cell.border = thin_border
ws_dcf.cell(row=6, column=13, value=f"=INPUTS!E{param_row_map['M_TERM']}").font = font_bold
ws_dcf.cell(row=6, column=13).number_format = "0.00%"
ws_dcf.cell(row=6, column=13).border = thin_border

# Row 7: Operating EBIT ($M)
ws_dcf.cell(row=7, column=1, value="Adjusted Operating Profit (EBIT) ($M)").font = font_bold
ws_dcf.cell(row=7, column=2, value=f"=INPUTS!E{param_row_map['BASE_EBIT']}").font = font_bold
ws_dcf.cell(row=7, column=2).number_format = "$#,##0.0"
ws_dcf.cell(row=7, column=2).border = thin_border
for col in range(3, 14):
    col_let = get_column_letter(col)
    cell = ws_dcf.cell(row=7, column=col, value=f"={col_let}5*{col_let}6")
    cell.font = font_bold if col == 13 else font_regular
    cell.number_format = "$#,##0.0"
    cell.border = thin_border

# Row 8: Tax Rate (%)
ws_dcf.cell(row=8, column=1, value="Effective Tax Rate (%)").font = font_bold
ws_dcf.cell(row=8, column=2, value=f"=INPUTS!E{param_row_map['TAX_RATE_B']}").font = font_regular
ws_dcf.cell(row=8, column=2).number_format = "0.00%"
ws_dcf.cell(row=8, column=2).border = thin_border
# Tax rate graduates linearly to marginal rate
for y in range(1, 11):
    col = y + 2
    r_tb = param_row_map['TAX_RATE_B']
    r_tm = param_row_map['TAX_RATE_M']
    cell = ws_dcf.cell(row=8, column=col, value=f"=INPUTS!E{r_tb} + (INPUTS!E{r_tm} - INPUTS!E{r_tb}) * ({y} / 10)")
    cell.font = font_regular
    cell.number_format = "0.00%"
    cell.border = thin_border
ws_dcf.cell(row=8, column=13, value=f"=INPUTS!E{param_row_map['TAX_RATE_M']}").font = font_bold
ws_dcf.cell(row=8, column=13).number_format = "0.00%"
ws_dcf.cell(row=8, column=13).border = thin_border

# Row 9: NOPAT ($M)
ws_dcf.cell(row=9, column=1, value="NOPAT (EBIT * (1 - Tax)) ($M)").font = font_bold
ws_dcf.cell(row=9, column=2, value="=B7*(1-B8)").font = font_bold
ws_dcf.cell(row=9, column=2).number_format = "$#,##0.0"
ws_dcf.cell(row=9, column=2).border = thin_border
for col in range(3, 14):
    col_let = get_column_letter(col)
    cell = ws_dcf.cell(row=9, column=col, value=f"={col_let}7*(1-{col_let}8)")
    cell.font = font_bold if col == 13 else font_regular
    cell.number_format = "$#,##0.0"
    cell.border = thin_border

# Row 10: Sales-to-Capital Ratio
ws_dcf.cell(row=10, column=1, value="Sales-to-Capital Ratio (Capital Efficiency)").font = font_bold
ws_dcf.cell(row=10, column=2, value="--").alignment = Alignment(horizontal="center")
for y in range(1, 6):
    col = y + 2
    cell = ws_dcf.cell(row=10, column=col, value=f"=INPUTS!E{param_row_map['S2C_P1']}")
    cell.font = font_regular
    cell.number_format = "0.00"
    cell.border = thin_border
for y in range(6, 11):
    col = y + 2
    cell = ws_dcf.cell(row=10, column=col, value=f"=INPUTS!E{param_row_map['S2C_P2']}")
    cell.font = font_regular
    cell.number_format = "0.00"
    cell.border = thin_border
ws_dcf.cell(row=10, column=13, value="--").alignment = Alignment(horizontal="center")

# Row 11: Reinvestment ($M)
ws_dcf.cell(row=11, column=1, value="Net Reinvestment (Capex + R&D + WC - D&A) ($M)").font = font_bold
ws_dcf.cell(row=11, column=2, value="--").alignment = Alignment(horizontal="center")
for y in range(1, 11):
    col = y + 2
    col_let = get_column_letter(col)
    prev_let = get_column_letter(col - 1)
    cell = ws_dcf.cell(row=11, column=col, value=f"=MAX(0, ({col_let}5 - {prev_let}5) / {col_let}10)")
    cell.font = font_regular
    cell.number_format = "$#,##0.0"
    cell.border = thin_border
ws_dcf.cell(row=11, column=13, value=f"=M9*(M4/INPUTS!E{param_row_map['ROIC_TERM']})").font = font_bold
ws_dcf.cell(row=11, column=13).number_format = "$#,##0.0"
ws_dcf.cell(row=11, column=13).border = thin_border

# Row 12: FCFF ($M)
ws_dcf.cell(row=12, column=1, value="Free Cash Flow to Firm (FCFF) ($M)").font = font_bold
ws_dcf.cell(row=12, column=2, value="--").alignment = Alignment(horizontal="center")
for col in range(3, 14):
    col_let = get_column_letter(col)
    cell = ws_dcf.cell(row=12, column=col, value=f"={col_let}9 - {col_let}11")
    cell.font = font_bold
    cell.fill = light_blue
    cell.number_format = "$#,##0.0"
    cell.border = thin_border

# Row 13: WACC (%)
ws_dcf.cell(row=13, column=1, value="Annual Discount Rate (WACC) (%)").font = font_bold
ws_dcf.cell(row=13, column=2, value="--").alignment = Alignment(horizontal="center")
for y in range(1, 6):
    col = y + 2
    cell = ws_dcf.cell(row=13, column=col, value=f"=INPUTS!E{param_row_map['WACC_P1']}")
    cell.font = font_regular
    cell.number_format = "0.00%"
    cell.border = thin_border
for y in range(6, 10):
    col = y + 2
    cell = ws_dcf.cell(row=13, column=col, value=f"=INPUTS!E{param_row_map['WACC_P2']}")
    cell.font = font_regular
    cell.number_format = "0.00%"
    cell.border = thin_border
ws_dcf.cell(row=13, column=12, value=f"=INPUTS!E{param_row_map['WACC_TERM']}").font = font_regular
ws_dcf.cell(row=13, column=12).number_format = "0.00%"
ws_dcf.cell(row=13, column=12).border = thin_border
ws_dcf.cell(row=13, column=13, value=f"=INPUTS!E{param_row_map['WACC_TERM']}").font = font_bold
ws_dcf.cell(row=13, column=13).number_format = "0.00%"
ws_dcf.cell(row=13, column=13).border = thin_border

# Row 14: Cumulative Discount Factor
ws_dcf.cell(row=14, column=1, value="Cumulative Present Value Discount Factor").font = font_bold
ws_dcf.cell(row=14, column=2, value=1.0000).font = font_regular
ws_dcf.cell(row=14, column=2).number_format = "0.0000"
ws_dcf.cell(row=14, column=2).border = thin_border
for y in range(1, 11):
    col = y + 2
    prev_let = get_column_letter(col - 1)
    cur_let = get_column_letter(col)
    cell = ws_dcf.cell(row=14, column=col, value=f"={prev_let}14/(1+{cur_let}13)")
    cell.font = font_regular
    cell.number_format = "0.0000"
    cell.border = thin_border
ws_dcf.cell(row=14, column=13, value="=L14").font = font_bold
ws_dcf.cell(row=14, column=13).number_format = "0.0000"
ws_dcf.cell(row=14, column=13).border = thin_border

# Row 15: Present Value of FCFF ($M)
ws_dcf.cell(row=15, column=1, value="Present Value (PV) of Discrete FCFF ($M)").font = font_bold
ws_dcf.cell(row=15, column=2, value="--").alignment = Alignment(horizontal="center")
for y in range(1, 11):
    col = y + 2
    col_let = get_column_letter(col)
    cell = ws_dcf.cell(row=15, column=col, value=f"={col_let}12*{col_let}14")
    cell.font = font_bold
    cell.number_format = "$#,##0.0"
    cell.border = thin_border
ws_dcf.cell(row=15, column=13, value="--").alignment = Alignment(horizontal="center")

for r in range(4, 16):
    ws_dcf.row_dimensions[r].height = 20

# Valuation Bridge Section
ws_dcf.merge_cells("A18:D18")
ws_dcf["A18"] = "DYNAMIC DCF VALUATION BRIDGE & INTRINSIC EQUITY DERIVATION"
ws_dcf["A18"].font = font_subtitle
ws_dcf["A18"].fill = navy_subheader
ws_dcf["A18"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
ws_dcf.row_dimensions[18].height = 24

bridge_rows = [
    ("PV of 10-Year Discrete Cash Flows (FY27–FY36) ($M):", "=SUM(C15:L15)", "USD_M", font_bold, light_blue),
    ("Perpetual Terminal Value (Year 10 Undiscounted) ($M):", "=M12/(M13-M4)", "USD_M", font_regular, None),
    ("PV of Terminal Value (Discounted back 10 years) ($M):", "=B20*M14", "USD_M", font_bold, light_blue),
    ("ENTERPRISE VALUE (EV) ($M):", "=B19+B21", "USD_M", font_bold, amber_fill),
    ("Add: Cash, Equivalents & Marketable Securities ($M):", f"=INPUTS!E{param_row_map['CASH_SEC']}", "USD_M", font_regular, None),
    ("Less: Total Debt & Capitalized Operating Leases ($M):", f"=INPUTS!E{param_row_map['TOT_DEBT']}", "USD_M", font_regular, None),
    ("Net Cash / Balance Sheet Liquidity Surplus ($M):", "=B23-B24", "USD_M", font_bold, light_blue),
    ("IMPLIED EQUITY INTRINSIC VALUE ($M):", "=B22+B25", "USD_M", font_bold, emerald_fill),
    ("Diluted Common Shares Outstanding (Million):", f"=INPUTS!E{param_row_map['SHARES']}", "Shares_M", font_regular, None),
    ("INTRINSIC VALUE PER COMMON SHARE (USD):", "=B26/B27", "USD", font_title, emerald_fill),
    ("Market Spot Share Price (USD):", f"=INPUTS!E{param_row_map['SPOT_PX']}", "USD", font_bold, None),
    ("Valuation Spread vs Current Spot (%):", "=(B28-B29)/B29", "PCT", font_bold, None),
    ("Institutional Valuation Stance:", '=IF(B30>=0.2,"STRONG BUY",IF(B30>=0.05,"ACCUMULATE",IF(B30>=-0.05,"FAIR VALUE / HOLD",IF(B30>=-0.15,"TRIM","UNDERWEIGHT / SELL"))))', "TEXT", font_bold, light_blue)
]

r_b = 19
for item in bridge_rows:
    lbl = item[0]
    formula = item[1]
    fmt = item[2]
    f_style = item[3]
    fill_style = item[4]
    
    c1 = ws_dcf.cell(row=r_b, column=1, value=lbl)
    c1.font = font_bold if "VALUE" in lbl or "ENTERPRISE" in lbl or "EQUITY" in lbl else font_regular
    c1.border = thin_border
    
    c2 = ws_dcf.cell(row=r_b, column=2, value=formula)
    c2.font = f_style
    c2.border = double_bottom if "PER COMMON SHARE" in lbl else thin_border
    if fill_style:
        c1.fill = fill_style
        c2.fill = fill_style
        
    if fmt == "USD_M":
        c2.number_format = "$#,##0.0"
    elif fmt == "USD":
        c2.number_format = "$#,##0.00"
    elif fmt == "Shares_M":
        c2.number_format = "#,##0.00"
    elif fmt == "PCT":
        c2.number_format = "+0.00%;-0.00%"
        
    ws_dcf.row_dimensions[r_b].height = 21
    r_b += 1

# ==============================================================================
# TAB 3: DUPONT_5_POINT
# ==============================================================================
ws_dp = wb.create_sheet(title="DUPONT_5_POINT")
ws_dp.views.sheetView[0].showGridLines = True

ws_dp.merge_cells("A1:H1")
ws_dp["A1"] = "5-POINT DUPONT ROE DECOMPOSITION & BUSINESS CYCLE OPERATIONAL AUDIT"
ws_dp["A1"].font = font_title
ws_dp["A1"].fill = navy_header
ws_dp["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_dp.row_dimensions[1].height = 34

ws_dp.merge_cells("A2:H2")
ws_dp["A2"] = "FORMULA: ROE = (Net Income / EBT) × (EBT / EBIT) × (EBIT / Revenue) × (Revenue / Assets) × (Assets / Equity)"
ws_dp["A2"].font = font_sec_hdr
ws_dp["A2"].fill = light_blue
ws_dp["A2"].font = Font(name="Calibri", size=10, bold=True, color="1E3A8A")
ws_dp["A2"].alignment = Alignment(horizontal="center", vertical="center")
ws_dp.row_dimensions[2].height = 22

dp_headers = [
    "Fiscal Period", "Tax Burden (NI / EBT)", "Interest Burden (EBT / EBIT)", 
    "Operating Margin (EBIT / Rev)", "Asset Turnover (Rev / Assets)", 
    "Equity Multiplier (Assets / Eq)", "Return on Equity (ROE %)", "Primary Operational Driver"
]
ws_dp.row_dimensions[4].height = 24
for c_idx, h in enumerate(dp_headers, 1):
    cell = ws_dp.cell(row=4, column=c_idx, value=h)
    cell.font = font_subtitle
    cell.fill = navy_subheader
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

dupont_table = [
    ("FY2022", 0.933, 0.960, 0.3154, 0.480, 1.31, "=B5*C5*D5*E5*F5", "Prior DRAM Supercycle Peak"),
    ("FY2023", 1.012, 1.066, -0.3478, 0.257, 1.40, "=B6*C6*D6*E6*F6", "Severe Industry Inventory Digestion Trough"),
    ("FY2024", 0.842, 0.709, 0.0519, 0.374, 1.52, "=B7*C7*D7*E7*F7", "Early Recovery; HBM3E Qualification Begins"),
    ("FY2025", 0.903, 0.968, 0.2614, 0.453, 1.58, "=B8*C8*D8*E8*F8", "HBM3E Volume Ramp; AI Memory Shortage"),
    ("FY2026", 0.852, 1.003, 0.7459, 0.680, 1.42, "=B9*C9*D9*E9*F9", "Historic HBM Supercycle; Monopolistic AI Pricing")
]

r_dp = 5
for row in dupont_table:
    ws_dp.cell(row=r_dp, column=1, value=row[0]).font = font_bold
    ws_dp.cell(row=r_dp, column=1).alignment = Alignment(horizontal="center")
    ws_dp.cell(row=r_dp, column=1).border = thin_border
    
    c_tax = ws_dp.cell(row=r_dp, column=2, value=row[1])
    c_tax.number_format = "0.000"
    c_int = ws_dp.cell(row=r_dp, column=3, value=row[2])
    c_int.number_format = "0.000"
    c_mar = ws_dp.cell(row=r_dp, column=4, value=row[3])
    c_mar.number_format = "+0.00%;-0.00%"
    c_to = ws_dp.cell(row=r_dp, column=5, value=row[4])
    c_to.number_format = "0.000x"
    c_em = ws_dp.cell(row=r_dp, column=6, value=row[5])
    c_em.number_format = "0.00x"
    
    c_roe = ws_dp.cell(row=r_dp, column=7, value=row[6])
    c_roe.font = font_bold
    c_roe.number_format = "+0.00%;-0.00%"
    c_roe.fill = emerald_fill if row[0] == "FY2026" else (amber_fill if "FY23" in row[0] else light_blue)
    
    c_note = ws_dp.cell(row=r_dp, column=8, value=row[7])
    c_note.font = font_italic_note
    
    for c in [c_tax, c_int, c_mar, c_to, c_em, c_roe, c_note]:
        c.border = thin_border
        if c != c_note and c != ws_dp.cell(row=r_dp, column=1):
            c.alignment = Alignment(horizontal="right")
            
    ws_dp.row_dimensions[r_dp].height = 21
    r_dp += 1

# ==============================================================================
# TAB 4: WACC_AND_CREDIT
# ==============================================================================
ws_wacc = wb.create_sheet(title="WACC_AND_CREDIT")
ws_wacc.views.sheetView[0].showGridLines = True
ws_wacc.merge_cells("A1:F1")
ws_wacc["A1"] = "WACC DERIVATION, HAMADA BETA & MOODY'S CREDIT RATING SYNTHESIS"
ws_wacc["A1"].font = font_title
ws_wacc["A1"].fill = navy_header
ws_wacc["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_wacc.row_dimensions[1].height = 34

wacc_display_data = [
    ("CAPITAL ASSET PRICING MODEL (CAPM) PARAMETERS", ""),
    ("Risk-Free Rate (10-Yr US Treasury) (Rf):", f"=INPUTS!E{param_row_map['RF_RATE']}"),
    ("Damodaran Implied Equity Risk Premium (ERP):", f"=INPUTS!E{param_row_map['ERP']}"),
    ("Semiconductor Memory Unlevered Asset Beta (Beta_U):", f"=INPUTS!E{param_row_map['BETA_U']}"),
    ("Market Value of Common Equity (E) ($M):", f"=INPUTS!E{param_row_map['SPOT_PX']}*INPUTS!E{param_row_map['SHARES']}"),
    ("Total Adjusted Debt (D) ($M):", f"=INPUTS!E{param_row_map['TOT_DEBT']}"),
    ("Market Debt-to-Equity Capital Ratio (D/E):", "=B6/B5"),
    ("Audited Corporate Tax Rate (t):", f"=INPUTS!E{param_row_map['TAX_RATE_B']}"),
    ("Hamada Re-Levered Equity Beta (Beta_L):", "=B4*(1+(1-B8)*B7)"),
    ("Cost of Equity (Ke = Rf + Beta_L * ERP):", "=B2+B9*B3"),
    ("", ""),
    ("MOODY'S 6-METRIC INDUSTRIAL CREDIT RATING GRID", ""),
    ("1. Interest Coverage Ratio (Adjusted EBIT / Interest):", "952.8x (Aaa / AAA Standard)"),
    ("2. Leverage Ratio (Total Debt / EBITDA):", "0.05x (Aaa / AAA Standard)"),
    ("3. Return on Capital (EBIT / Total Capital):", "51.56% (Aaa / AAA Standard)"),
    ("4. Asset Coverage Ratio (Tangible Assets / Debt):", "25.0x (Aaa / AAA Standard)"),
    ("5. Operating Profit Margin (EBIT / Net Sales):", "75.83% (Aaa / AAA Standard)"),
    ("6. Current Liquidity Ratio (Current Assets / Current Liab):", "3.31x (Aaa / AAA Standard)"),
    ("Synthetic Unconstrained Solvency Grade:", "Aaa / AAA (60 bps Default Spread)"),
    ("Qualitative Cyclical Semiconductor Sovereign Cap:", "Baa1 / BBB+ (135 bps Spread)"),
    ("Pre-Tax Cost of Debt (Kd):", f"=INPUTS!E{param_row_map['PRE_TAX_KD']}"),
    ("After-Tax Cost of Debt (Kd * (1 - t)):", "=B20*(1-B8)"),
    ("", ""),
    ("WACC CAPITAL STRUCTURE SCHEDULE", ""),
    ("Phase 1 Discount Rate (Years 1–5):", f"=INPUTS!E{param_row_map['WACC_P1']}"),
    ("Phase 2 Discount Rate (Years 6–9):", f"=INPUTS!E{param_row_map['WACC_P2']}"),
    ("Terminal Discount Rate (Year 10+):", f"=INPUTS!E{param_row_map['WACC_TERM']}")
]

r_w = 3
for label, val in wacc_display_data:
    c1 = ws_wacc.cell(row=r_w, column=1, value=label)
    c2 = ws_wacc.cell(row=r_w, column=2, value=val)
    c1.border = thin_border
    c2.border = thin_border
    if label in ["CAPITAL ASSET PRICING MODEL (CAPM) PARAMETERS", "MOODY'S 6-METRIC INDUSTRIAL CREDIT RATING GRID", "WACC CAPITAL STRUCTURE SCHEDULE"]:
        c1.font = font_subtitle
        c1.fill = navy_subheader
        c2.fill = navy_subheader
    else:
        c1.font = font_bold if "WACC" in label or "Cost" in label or "Beta" in label else font_regular
        c2.font = font_bold if "WACC" in label or "Cost" in label or "Beta" in label else font_regular
    if isinstance(val, str) and val.startswith("="):
        if "Beta" in label:
            c2.number_format = "0.000"
        elif "Ratio" in label:
            c2.number_format = "0.0000"
        elif "Rate" in label or "Cost" in label or "ERP" in label or "WACC" in label:
            c2.number_format = "0.00%"
        else:
            c2.number_format = "$#,##0.0"
    ws_wacc.row_dimensions[r_w].height = 20
    r_w += 1

# ==============================================================================
# TAB 5: SOTP_DIVISIONAL
# ==============================================================================
ws_sotp = wb.create_sheet(title="SOTP_DIVISIONAL")
ws_sotp.views.sheetView[0].showGridLines = True
ws_sotp.merge_cells("A1:G1")
ws_sotp["A1"] = "SUM-OF-THE-PARTS (SOTP) DIVISIONAL MULTIPLE VALUATION (40% CYCLE HAIRCUT)"
ws_sotp["A1"].font = font_title
ws_sotp["A1"].fill = navy_header
ws_sotp["A1"].alignment = Alignment(horizontal="center", vertical="center")
ws_sotp.row_dimensions[1].height = 34

sotp_headers = ["Operating Division", "Net Sales ($M)", "Peak EBITDA ($M)", "Cycle Haircut %", "Normalized EBITDA ($M)", "Target EV/EBITDA", "Implied EV ($M)"]
ws_sotp.row_dimensions[3].height = 24
for c_idx, h in enumerate(sotp_headers, 1):
    cell = ws_sotp.cell(row=3, column=c_idx, value=h)
    cell.font = font_subtitle
    cell.fill = navy_subheader
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

sotp_data = [
    ("CNBU (Compute & Networking - AI HBM)", 106550.0, 83109.0, 0.40, "=C4*(1-D4)", 7.35, "=E4*F4"),
    ("MBU (Mobile - LPDDR5X & UFS 4.0)", 10655.0, 6926.0, 0.40, "=C5*(1-D5)", 15.00, "=E5*F5"),
    ("SBU (Storage - NAND Flash & Enterprise SSD)", 7991.0, 4795.0, 0.40, "=C6*(1-D6)", 13.21, "=E6*F6"),
    ("EBU (Embedded - Auto ADAS & Industrial IoT)", 7992.0, 4955.0, 0.40, "=C7*(1-D7)", 11.00, "=E7*F7")
]

r_s = 4
for row in sotp_data:
    ws_sotp.cell(row=r_s, column=1, value=row[0]).font = font_bold
    ws_sotp.cell(row=r_s, column=1).border = thin_border
    
    c_rev = ws_sotp.cell(row=r_s, column=2, value=row[1])
    c_rev.number_format = "$#,##0.0"
    c_eb = ws_sotp.cell(row=r_s, column=3, value=row[2])
    c_eb.number_format = "$#,##0.0"
    c_hc = ws_sotp.cell(row=r_s, column=4, value=row[3])
    c_hc.number_format = "0.0%"
    c_neb = ws_sotp.cell(row=r_s, column=5, value=row[4])
    c_neb.number_format = "$#,##0.0"
    c_mult = ws_sotp.cell(row=r_s, column=6, value=row[5])
    c_mult.number_format = "0.00x"
    c_ev = ws_sotp.cell(row=r_s, column=7, value=row[6])
    c_ev.font = font_bold
    c_ev.number_format = "$#,##0.0"
    
    for c in [c_rev, c_eb, c_hc, c_neb, c_mult, c_ev]:
        c.border = thin_border
        c.alignment = Alignment(horizontal="right")
    ws_sotp.row_dimensions[r_s].height = 21
    r_s += 1

# SOTP Summary Rows
ws_sotp.cell(row=9, column=1, value="TOTAL AGGREGATE DIVISIONAL ENTERPRISE VALUE ($M):").font = font_bold
ws_sotp.cell(row=9, column=7, value="=SUM(G4:G7)").font = font_bold
ws_sotp.cell(row=9, column=7).fill = amber_fill
ws_sotp.cell(row=9, column=7).number_format = "$#,##0.0"
ws_sotp.cell(row=9, column=1).border = thin_border
ws_sotp.cell(row=9, column=7).border = thin_border

ws_sotp.cell(row=10, column=1, value="Add: Net Balance Sheet Cash & Liquid Securities ($M):").font = font_bold
ws_sotp.cell(row=10, column=7, value=f"=INPUTS!E{param_row_map['CASH_SEC']}-INPUTS!E{param_row_map['TOT_DEBT']}").font = font_regular
ws_sotp.cell(row=10, column=7).number_format = "$#,##0.0"
ws_sotp.cell(row=10, column=1).border = thin_border
ws_sotp.cell(row=10, column=7).border = thin_border

ws_sotp.cell(row=11, column=1, value="IMPLIED SOTP EQUITY VALUE ($M):").font = font_bold
ws_sotp.cell(row=11, column=7, value="=G9+G10").font = font_bold
ws_sotp.cell(row=11, column=7).fill = emerald_fill
ws_sotp.cell(row=11, column=7).number_format = "$#,##0.0"
ws_sotp.cell(row=11, column=1).border = thin_border
ws_sotp.cell(row=11, column=7).border = thin_border

ws_sotp.cell(row=12, column=1, value="SOTP INTRINSIC VALUE PER SHARE (USD):").font = font_title
ws_sotp.cell(row=12, column=7, value=f"=G11/INPUTS!E{param_row_map['SHARES']}").font = font_title
ws_sotp.cell(row=12, column=7).fill = emerald_fill
ws_sotp.cell(row=12, column=7).number_format = "$#,##0.00"
ws_sotp.cell(row=12, column=1).border = double_bottom
ws_sotp.cell(row=12, column=7).border = double_bottom

# Auto-adjust column widths across all sheets
for ws in [ws_in, ws_dcf, ws_dp, ws_wacc, ws_sotp]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if len(val_str) > max_len and "\n" not in val_str and not val_str.startswith("="):
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)
ws_in.column_dimensions["B"].width = 46
ws_in.column_dimensions["G"].width = 54
ws_dcf.column_dimensions["A"].width = 42
ws_dp.column_dimensions["H"].width = 46
ws_wacc.column_dimensions["A"].width = 52
ws_sotp.column_dimensions["A"].width = 42

out_path = "ERVIS/projects/US_EQUITIES/MU/models/model.xlsx"
wb.save(out_path)
print(f"Successfully generated dynamic interactive Excel model at {out_path}")

deploy_path = "/Users/worldofmadness/Documents/VS Code/Personal Projects/ervis-terminal/equities/micron/model.xlsx"
wb.save(deploy_path)
print(f"Successfully deployed Excel model to {deploy_path}")
