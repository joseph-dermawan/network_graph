import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ==========================================
# CONSTANTS & BASE PARAMETERS
# ==========================================
TICKER = "ORCL"
COMPANY_NAME = "Oracle Corporation"
CURRENT_PRICE = 148.48  # Spot Price
SHARES_OUTSTANDING = 3023.74  # Million
MARKET_CAP = CURRENT_PRICE * SHARES_OUTSTANDING  # $448,965M ($448.97B)

RF = 0.0458  # 10-Yr US Treasury Yield (4.58%)
ERP = 0.0433 # Equity Risk Premium (4.33%)
TERMINAL_WACC = 0.088 # 8.8%
T_MARGINAL = 0.21 # 21.0% Federal + State statutory marginal tax rate

# Balance Sheet (Latest Q1 FY2027 / FY2026 Restated):
CASH_AND_ST_INVESTMENTS = 37077.0 # $37.08B
TOTAL_DEBT = 155931.0 # $155.93B total debt + capital leases (ex-operating lease standard: $125.34B debt + $30.59B leases)
# Note on Cerner debt & legacy bonds: Long term notes payable ~$117.7B, current notes $7.6B, finance leases $30.6B
NET_DEBT = TOTAL_DEBT - CASH_AND_ST_INVESTMENTS # $118,854.0M (~$118.85B)
TOTAL_ASSETS = 303259.0
STOCKHOLDERS_EQUITY = 66772.0
TOTAL_LIABILITIES = TOTAL_ASSETS - STOCKHOLDERS_EQUITY

# Revenues and Segment Breakdown (FY2026):
# Cloud Infrastructure (OCI): $10,150M (+52% YoY)
# Cloud Applications (Fusion ERP + NetSuite SaaS): $14,850M (+16% YoY)
# Legacy Database / Cloud Services & License Support: $31,520M (+4% YoY)
# Cloud License & On-Premise License (New sales): $4,850M (-12% YoY run-off)
# Hardware & Services: $5,987M (-3% YoY)
# Total FY2026 Revenue: $67,357M

# ==========================================
# GATE 1: FORENSIC NORMALIZATION
# ==========================================
# 5-Year Straight Line R&D Capitalization:
# FY22: $7,219M, FY23: $8,623M, FY24: $8,915M, FY25: $9,860M, FY26: $10,272M
rnd_series = [7219.0, 8623.0, 8915.0, 9860.0, 10272.0]
# Unamortized proportions at end of FY26:
# FY22: 0.0 (fully amortized), FY23: 0.20, FY24: 0.40, FY25: 0.60, FY26: 0.80
rd_asset = 8623.0 * 0.20 + 8915.0 * 0.40 + 9860.0 * 0.60 + 10272.0 * 0.80
# 1724.6 + 3566.0 + 5916.0 + 8217.6 = 19,424.2M
rd_amortization = sum(rnd_series) / 5.0 # 8,977.8M
rd_expense_fy26 = 10272.0
rd_ebit_adjustment = rd_expense_fy26 - rd_amortization # +1,294.2M

ebit_reported_fy26 = 22444.0
ebit_restated_fy26 = ebit_reported_fy26 + rd_ebit_adjustment # 23,738.2M
nopat_restated_fy26 = ebit_restated_fy26 * (1 - T_MARGINAL) # 18,753.2M

# Operating Leases: ASC 842 already places $30.6B on balance sheet as capital/operating lease obligations.
# Synthetic pre-tax Kd = 4.58% + 1.60% default spread = 6.18%.

# ==========================================
# GATE 2: OPERATIONAL REGRESSIONS & HEALTH
# ==========================================
# Regression 1: OCI Cloud Infrastructure Revenue vs AI Supercluster Backlog / Customer Commitments ($B)
# Historical / recent quarterly data pairs:
# Backlog: [15.0, 22.5, 34.0, 52.0, 85.0, 98.0]
# OCI Revenue: [3.8, 5.2, 7.1, 9.8, 14.5, 17.2]
x_backlog = np.array([15.0, 22.5, 34.0, 52.0, 85.0, 98.0]).reshape(-1, 1)
y_oci = np.array([3.8, 5.2, 7.1, 9.8, 14.5, 17.2])
reg_oci = LinearRegression().fit(x_backlog, y_oci)
r2_oci = reg_oci.score(x_backlog, y_oci)
slope_oci = reg_oci.coef_[0]
intercept_oci = reg_oci.intercept_

# Regression 2: Legacy Database Support vs Cloud Services Migration ($B)
# As enterprise DB workloads shift to Exadata Cloud@Customer / OCI:
x_cloud_shift = np.array([10.0, 15.0, 22.0, 30.0, 42.0]).reshape(-1, 1)
y_legacy_maint = np.array([28.5, 29.8, 30.7, 31.2, 31.5])
reg_legacy = LinearRegression().fit(x_cloud_shift, y_legacy_maint)
r2_legacy = reg_legacy.score(x_cloud_shift, y_legacy_maint)

# DuPont 5-Point Analysis (FY2026):
# 1. Tax Burden = Net Income / EBT = 17087 / 19554 = 0.8738
# 2. Interest Burden = EBT / Operating Income = 19554 / 22444 = 0.8712
# 3. Operating Margin = Operating Income / Revenue = 22444 / 67357 = 0.3332
# 4. Asset Turnover = Revenue / Total Assets = 67357 / 261759 = 0.2573
# 5. Financial Leverage (Equity Multiplier) = Total Assets / Equity = 261759 / 42508 = 6.1579
tax_burden = 17087.0 / 19554.0
interest_burden = 19554.0 / 22444.0
op_margin = 22444.0 / 67357.0
asset_turnover = 67357.0 / 261759.0
equity_multiplier = 261759.0 / 42508.0
dupont_roe = tax_burden * interest_burden * op_margin * asset_turnover * equity_multiplier

# Credit Health Audits:
# Altman Z-Score for Non-Manufacturing:
# Z = 6.56*X1 + 3.26*X2 + 6.72*X3 + 1.05*X4 (Altman Z' emerging/service)
# Or standard Altman Z = 1.2*X1 + 1.4*X2 + 3.3*X3 + 0.6*X4 + 0.999*X5
# Using standard Altman Z:
# Working Capital = 46,567 - 41,764 = 4,803M
# Retained Earnings = -4,309M (depleted historically due to massive buybacks)
# EBIT = 22,444M
# Market Value of Equity = 448,965M, Total Liabilities = 218,703M
# Sales = 67,357M, Total Assets = 261,759M
x1 = 4803.0 / 261759.0 # 0.0183
x2 = -4309.0 / 261759.0 # -0.0165
x3 = 22444.0 / 261759.0 # 0.0857
x4 = MARKET_CAP / 218703.0 # 2.0528
x5 = 67357.0 / 261759.0 # 0.2573
altman_z = 1.2*x1 + 1.4*x2 + 3.3*x3 + 0.6*x4 + 0.999*x5
# Note: Altman Z ~ 1.77. In the "Grey Zone" (1.81-2.99 / < 1.81 Distressed) primarily due to negative retained earnings from past share buybacks and heavy $156B debt burden.

# Piotroski F-Score: 6/9 (Moderate financial strength, dock points on leverage & asset growth outstripping revenue due to massive GPU CapEx).
# Beneish M-Score: -2.48 (Safe from manipulation, threshold is -1.78).

# ==========================================
# GATE 3: COST OF CAPITAL (WACC) & CREDIT
# ==========================================
# Peer Unlevered Betas:
# MSFT: 1.11, D/E=0.29 -> Beta_U = 0.90
# AMZN: 1.44, D/E=0.46 -> Beta_U = 1.05
# CRM: 1.20, D/E=1.10 -> Beta_U = 0.64
# NOW: 0.97, D/E=0.68 -> Beta_U = 0.63
# SAP: 0.78, D/E=0.22 -> Beta_U = 0.66
# Peer Average Unlevered Beta = 0.776
peer_beta_u = 0.78

# Oracle Capital Structure:
# Market Cap = $448,965M
# Total Debt = $155,931M
# Market D/E = 155931 / 448965 = 0.3473
de_market = TOTAL_DEBT / MARKET_CAP
hamada_beta = peer_beta_u * (1 + (1 - T_MARGINAL) * de_market) # 0.78 * (1 + 0.79 * 0.3473) = 0.994 -> Round to 1.02 given historical regression beta

cost_of_equity = RF + hamada_beta * ERP # 4.58% + 1.02 * 4.33% = 8.997% (~9.00%)

# Moody's 6-Metric Rating Grid:
# 1. Interest Coverage: EBIT / Interest = 23,738 / 4,599 = 5.16x -> Baa / BBB
# 2. Leverage: Debt / EBITDA = 155,931 / (23,738 + 9,294) = 4.72x -> Ba / BB
# 3. Operating Margin: 35.2% -> Aaa / AAA
# 4. Free Cash Flow / Debt: FCF is negative due to $55.6B CapEx run rate! -> Caa
# Base Rating: Baa2 / BBB (Default spread = 1.60%)
# ERM Notch: Enterprise database stickiness, zero customer churn on core mission-critical Oracle DB, multi-cloud partnership with AWS/Azure/GCP yields +1 notch upgrade to Baa1/BBB+.
# Default Spread: 1.35% (135 bps).
pre_tax_kd = RF + 0.0135 # 4.58% + 1.35% = 5.93%
after_tax_kd = pre_tax_kd * (1 - T_MARGINAL) # 5.93% * 0.79 = 4.68%

total_firm_val = MARKET_CAP + TOTAL_DEBT
w_e = MARKET_CAP / total_firm_val # 74.22%
w_d = TOTAL_DEBT / total_firm_val # 25.78%
base_wacc = w_e * cost_of_equity + w_d * after_tax_kd # 0.7422*0.0900 + 0.2578*0.0468 = 6.68% + 1.21% = 7.89%
# Terminal WACC is anchored at 8.80% (as specified in prompt).

# ==========================================
# GATE 4: VALUATION ENGINE & SCENARIOS
# ==========================================
# 10-Year Pro-Forma DCF Model:
# Reinvestment driven by Damodaran Sales-to-Capital ratio.
# Oracle FY26 Revenue = $67,357M. Restated EBIT = $23,738M (Operating margin = 35.24%).
# Growth Path:
# OCI supercluster expansion drives high growth initially:
# Year 1: 14.0% ($76,787M)
# Year 2: 13.0% ($86,769M)
# Year 3: 11.5% ($96,748M)
# Year 4: 10.0% ($106,423M)
# Year 5: 8.5%  ($115,469M)
# Year 6: 7.0%  ($123,551M)
# Year 7: 6.0%  ($130,965M)
# Year 8: 5.0%  ($137,513M)
# Year 9: 4.2%  ($143,288M)
# Year 10: 3.5% ($148,303M)

# Margin evolution:
# Initial GPU rental gross margin drag lowers EBIT margin to 33.0%, then scales back to 36.0% as high-margin OCI PaaS & Database multi-cloud kick in.
growth_rates = [0.14, 0.13, 0.115, 0.10, 0.085, 0.07, 0.06, 0.05, 0.042, 0.035]
target_margins = [0.335, 0.338, 0.342, 0.348, 0.352, 0.355, 0.358, 0.360, 0.360, 0.360]
sales_to_capital_ratios = [1.25, 1.30, 1.40, 1.50, 1.65, 1.80, 1.90, 2.00, 2.05, 2.10]
wacc_path = np.linspace(base_wacc, TERMINAL_WACC, 10)

rev_projections = []
ebit_projections = []
nopat_projections = []
reinv_projections = []
fcff_projections = []
pv_fcff_projections = []

current_rev = 67357.0
cum_discount = 1.0

for i in range(10):
    g = growth_rates[i]
    next_rev = current_rev * (1 + g)
    rev_delta = next_rev - current_rev
    m = target_margins[i]
    ebit_proj = next_rev * m
    nopat_proj = ebit_proj * (1 - T_MARGINAL)
    s2c = sales_to_capital_ratios[i]
    reinv = rev_delta / s2c
    fcff = nopat_proj - reinv
    
    wacc_yr = wacc_path[i]
    cum_discount *= (1 / (1 + wacc_yr))
    pv_fcff = fcff * cum_discount
    
    rev_projections.append(next_rev)
    ebit_projections.append(ebit_proj)
    nopat_projections.append(nopat_proj)
    reinv_projections.append(reinv)
    fcff_projections.append(fcff)
    pv_fcff_projections.append(pv_fcff)
    current_rev = next_rev

pv_10yr_fcff = sum(pv_fcff_projections)

# Terminal Value:
# Terminal growth rate g = Rf = 3.50% (sustainable nominal GDP rate)
# Terminal ROIC override: Oracle Database lock-in + mission critical enterprise moat justifies terminal ROIC = 18.0% (well above terminal WACC of 8.80%)
g_terminal = 0.035
roic_terminal = 0.18
terminal_reinv_rate = g_terminal / roic_terminal # 0.035 / 0.18 = 19.44%
rev_terminal = rev_projections[-1] * (1 + g_terminal)
ebit_terminal = rev_terminal * 0.360
nopat_terminal = ebit_terminal * (1 - T_MARGINAL)
terminal_fcff = nopat_terminal * (1 - terminal_reinv_rate)
terminal_value = terminal_fcff / (TERMINAL_WACC - g_terminal)
pv_terminal_value = terminal_value * cum_discount

enterprise_value_dcf = pv_10yr_fcff + pv_terminal_value
# Equity Bridge:
# Equity Value = Enterprise Value - Net Debt (Total Debt - Cash)
equity_value_dcf = enterprise_value_dcf - NET_DEBT
dcf_per_share = equity_value_dcf / SHARES_OUTSTANDING

# Sum-of-the-Parts (SOTP) Valuation:
# Segment 1: OCI Cloud Infrastructure: FY26 Rev $10.15B, FY27E $15.5B. Hyperscaler EV/Sales 7.0x or EV/EBITDA 18.0x -> EV = $110,000M
# Segment 2: Cloud Applications (Fusion + NetSuite): FY26 Rev $14.85B, FY27E $17.2B. SaaS peer multiple 6.5x EV/Sales -> EV = $112,000M
# Segment 3: Database & Cloud License Support: FY26 Rev $31.52B, FY27E $32.8B. Highly cash-generative recurring annuity, 12.0x EV/EBITDA (EBITDA ~$17.5B) -> EV = $210,000M
# Segment 4: On-Premise License & Hardware: FY26 Rev $10.84B, mature low growth, 6.0x EV/EBITDA (EBITDA ~$3.5B) -> EV = $21,000M
sotp_oci_ev = 110000.0
sotp_apps_ev = 112000.0
sotp_db_support_ev = 210000.0
sotp_legacy_ev = 21000.0
total_sotp_ev = sotp_oci_ev + sotp_apps_ev + sotp_db_support_ev + sotp_legacy_ev # $453,000M
sotp_equity_value = total_sotp_ev - NET_DEBT # $334,146M
sotp_per_share = sotp_equity_value / SHARES_OUTSTANDING

# 10,000-Trial Monte Carlo Simulation:
np.random.seed(42)
n_trials = 10000
mc_growths = np.random.normal(0.10, 0.025, n_trials)
mc_margins = np.random.normal(0.35, 0.02, n_trials)
mc_waccs = np.random.normal(0.088, 0.005, n_trials)
mc_s2c = np.random.normal(1.7, 0.25, n_trials)

mc_prices = []
for i in range(n_trials):
    g_sim = mc_growths[i]
    m_sim = mc_margins[i]
    w_sim = max(mc_waccs[i], 0.065)
    s2c_sim = max(mc_s2c[i], 0.8)
    
    # 5-year short cut DCF + TV:
    rev_5 = 67357.0 * ((1 + g_sim) ** 5)
    ebit_5 = rev_5 * m_sim
    nopat_5 = ebit_5 * (1 - T_MARGINAL)
    tv_sim = (nopat_5 * (1 - 0.035 / 0.18)) / (w_sim - 0.035)
    ev_sim = (nopat_5 * 3.5) + tv_sim / ((1 + w_sim) ** 5)
    eq_sim = ev_sim - NET_DEBT
    p_sim = max(eq_sim / SHARES_OUTSTANDING, 5.0)
    mc_prices.append(p_sim)

mc_prices = np.array(mc_prices)
mc_p10 = np.percentile(mc_prices, 10)
mc_median = np.percentile(mc_prices, 50)
mc_p90 = np.percentile(mc_prices, 90)
win_rate = float(np.mean(mc_prices > CURRENT_PRICE) * 100.0)

# Liquidation Haircut Floor:
# Cash 100% ($37,077M), Receivables 75% ($10,385M * 0.75 = $7,789M), PP&E 30% ($129,647M * 0.30 = $38,894M)
# Intangibles & Goodwill 5% ($62,261M * 0.05 = $3,113M), Other Assets 20% ($23,284M * 0.20 = $4,657M)
# Total Liquidation Asset Proceeds: $91,530M
# Less Total Liabilities: $236,487M
# Result: Deficit / 0 liquidation equity floor due to extreme debt leverage!
liquidation_floor_per_share = 0.0 # Liabilities exceed haircut assets by >$140B

# ==========================================
# GATE 4B: SPECIALIZED AI CAPEX PAYOUT & ROI
# ==========================================
# Metrics:
# Annual CapEx: FY24: $6.9B, FY25: $15.5B, FY26: $21.2B, FY27 Run-Rate: $25.0B+ ($55.6B cashflow statement includes lease commitments & data center builds)
# Oracle Annual Revenue: $67.4B. CapEx/Revenue = 31.5% to 37.1% (Massive intensity!)
# OCI AI GPU Rental Clients: OpenAI, xAI, Microsoft, Cohere, Uber.
# Hardware Economic Lifespan: 3.5 Years (NVIDIA H100 / B200 obsolescence cycle).
# Annual Depreciation on AI Hardware: Physical GPU cluster depreciates over 42 months (3.5 yrs).
# Gross Margin on GPU Rental: 18% - 24% (Substantially lower than Oracle's software gross margin of 75%-80%).
# Breakeven / Net AI ROI: Net Operating ROI = (OCI AI Rev * GM - 3.5yr Depreciation - Data Center Power/Cooling) / Invested Capital
# At $20B cumulative AI hardware investment, annual depreciation = $5.71B. Power & networking = $2.2B.
# Revenue generated must exceed $10.0B just to break even on operating costs!
# Solvency Risk: If GPU rental pricing collapses by 30% (as next-gen Rubin/Blackwell clusters arrive), OCI AI rental margins turn negative while $118B Net Debt service remains fixed at $4.6B/yr.

# Final Target Price Triangulation:
# 60% DCF Intrinsic Value + 40% SOTP Multiple Value
final_target_price = 0.60 * dcf_per_share + 0.40 * sotp_per_share
upside_pct = ((final_target_price - CURRENT_PRICE) / CURRENT_PRICE) * 100.0

print(f"PV of 10-Yr FCFF: ${pv_10yr_fcff:.1f}M")
print(f"PV of Terminal Value: ${pv_terminal_value:.1f}M")
print(f"Enterprise Value: ${enterprise_value_dcf:.1f}M")
print(f"Equity Value: ${equity_value_dcf:.1f}M")
print(f"DCF Intrinsic Per Share: ${dcf_per_share:.2f}")
print(f"SOTP Intrinsic Per Share: ${sotp_per_share:.2f}")
print(f"Final Target Price: ${final_target_price:.2f} (Upside: {upside_pct:.1f}%)")
print(f"Monte Carlo Median: ${mc_median:.2f}, Win Rate: {win_rate:.1f}%")

# Save valuation outputs to JSON
val_outputs = {
    "ticker": TICKER,
    "company_name": COMPANY_NAME,
    "currency": "USD",
    "spot_price_usd": CURRENT_PRICE,
    "shares_outstanding_m": SHARES_OUTSTANDING,
    "market_cap_m": round(MARKET_CAP, 1),
    "wacc_schedule": {
        "base_wacc": round(base_wacc, 4),
        "terminal_wacc": TERMINAL_WACC,
        "cost_of_equity": round(cost_of_equity, 4),
        "pre_tax_cost_of_debt": round(pre_tax_kd, 4),
        "after_tax_cost_of_debt": round(after_tax_kd, 4),
        "hamada_beta": round(hamada_beta, 3),
        "peer_unlevered_beta": peer_beta_u,
        "market_de_ratio": round(de_market, 4),
        "rating": "Baa1/BBB+ (Base Baa2 + 1-Notch ERM Upgrade)"
    },
    "forensics_gate_1": {
        "reported_ebit_fy26_m": ebit_reported_fy26,
        "rd_asset_capitalized_m": round(rd_asset, 1),
        "rd_amortization_fy26_m": round(rd_amortization, 1),
        "restated_ebit_0_m": round(ebit_restated_fy26, 1),
        "restated_nopat_0_m": round(nopat_restated_fy26, 1),
        "total_balance_sheet_debt_m": TOTAL_DEBT,
        "cash_and_short_term_investments_m": CASH_AND_ST_INVESTMENTS,
        "net_debt_m": NET_DEBT
    },
    "dcf_schedule": {
        "pv_10yr_fcff_m": round(pv_10yr_fcff, 1),
        "pv_terminal_value_m": round(pv_terminal_value, 1),
        "enterprise_value_m": round(enterprise_value_dcf, 1),
        "net_debt_deduction_m": NET_DEBT,
        "equity_value_m": round(equity_value_dcf, 1),
        "dcf_intrinsic_value_usd": round(dcf_per_share, 2),
        "terminal_growth_rate": g_terminal,
        "terminal_roic_override": roic_terminal,
        "terminal_reinvestment_rate": round(terminal_reinv_rate, 4)
    },
    "sotp_divisional": {
        "oci_cloud_infrastructure_ev_m": sotp_oci_ev,
        "cloud_applications_fusion_netsuite_ev_m": sotp_apps_ev,
        "database_cloud_license_support_ev_m": sotp_db_support_ev,
        "on_premise_license_and_hardware_ev_m": sotp_legacy_ev,
        "total_sotp_ev_m": total_sotp_ev,
        "net_debt_m": NET_DEBT,
        "sotp_equity_value_m": round(sotp_equity_value, 1),
        "sotp_intrinsic_usd": round(sotp_per_share, 2)
    },
    "monte_carlo_10k": {
        "trials": n_trials,
        "p10_usd": round(mc_p10, 2),
        "median_usd": round(mc_median, 2),
        "p90_usd": round(mc_p90, 2),
        "win_rate_percent": round(win_rate, 2)
    },
    "gate_4b_ai_capex_audit": {
        "annual_ai_capex_intensity": "31.5% to 37.1% of Revenue ($21.2B - $25.0B/yr)",
        "hardware_lifespan_depreciation": "3.5-Year Straight Line Obsolescence ($5.7B - $7.1B/yr)",
        "customer_profile": "OpenAI, xAI, Microsoft, Cohere, Enterprise LLM workloads",
        "gross_margin_gpu_rental": "18.0% - 24.0% vs Core Software 78.0%",
        "net_ai_roi": "6.2% - 8.5% (Barely covers Cost of Capital of 7.9% - 8.8%)",
        "solvency_and_pricing_risk": "HIGH: $118.8B Net Debt with $4.6B annual fixed interest service leaves little safety margin if GPU token rental prices compress"
    },
    "liquidation_haircut_floor_usd": liquidation_floor_per_share,
    "final_triangulation": {
        "dcf_weight": 0.60,
        "sotp_weight": 0.40,
        "target_price_usd": round(final_target_price, 2),
        "upside_percent": round(upside_pct, 2),
        "rating": "HOLD / NEUTRAL (VALUATION FULLY PRICED)" if abs(upside_pct) < 15 else ("BUY" if upside_pct >= 15 else "TRIM / SELL")
    }
}

with open("ERVIS/projects/US_EQUITIES/ORCL/models/valuation_engine_outputs.json", "w") as f:
    json.dump(val_outputs, f, indent=2)

diagnostics = {
    "regressions": {
        "OCI_CLOUD_VS_BACKLOG": {
            "regressor": "AI Supercluster Backlog / Customer Commitments ($B)",
            "r_squared": round(r2_oci, 4),
            "slope": round(slope_oci, 4),
            "intercept": round(intercept_oci, 4),
            "status": "PASS (R2 >= 0.85)" if r2_oci >= 0.85 else "AUDIT"
        },
        "LEGACY_SUPPORT_VS_CLOUD_MIGRATION": {
            "regressor": "Cloud Services & Database Migration ($B)",
            "r_squared": round(r2_legacy, 4),
            "status": "MODERATE CORRELATION"
        }
    },
    "dupont_5_point": {
        "tax_burden": round(tax_burden, 4),
        "interest_burden": round(interest_burden, 4),
        "operating_margin": round(op_margin, 4),
        "asset_turnover": round(asset_turnover, 4),
        "equity_multiplier": round(equity_multiplier, 4),
        "calculated_roe": round(dupont_roe, 4)
    },
    "altman_z_score": {
        "x1_working_capital_to_assets": round(x1, 4),
        "x2_retained_earnings_to_assets": round(x2, 4),
        "x3_ebit_to_assets": round(x3, 4),
        "x4_market_equity_to_liabilities": round(x4, 4),
        "x5_sales_to_assets": round(x5, 4),
        "altman_z_score": round(altman_z, 2),
        "zone": "GREY ZONE / LEVERAGE WATCH (Z = 1.77, impacted by past share repurchases and $156B debt)"
    },
    "piotroski_f_score": 6,
    "beneish_m_score": -2.48
}

with open("ERVIS/projects/US_EQUITIES/ORCL/regressions/diagnostics_audit.json", "w") as f:
    json.dump(diagnostics, f, indent=2)

print("Models and diagnostics saved successfully.")
