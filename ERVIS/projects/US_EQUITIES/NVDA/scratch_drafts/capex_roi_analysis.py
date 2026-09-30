# NVIDIA Specialized CapEx Payout and ROI Analysis Script
import json

years = ['FY23', 'FY24', 'FY25', 'FY26']
rev = [26974.0, 60922.0, 130497.0, 215938.0]
ebit = [5577.0, 32972.0, 81453.0, 138479.0]
tax = 0.15
nopat = [e * (1 - tax) for e in ebit]
capex = [1833.0, 1069.0, 3236.0, 6042.0]
da = [1544.0, 1508.0, 1877.0, 2843.0]
net_capex = [c - d for c, d in zip(capex, da)]
rd_capex = [7339.0, 8675.0, 12914.0, 18497.0]
fcf = [3808.0, 27021.0, 60853.0, 96676.0]
buybacks = [10440.0, 9532.0, 15000.0, 32000.0]
dividends = [398.0, 395.0, 480.0, 900.0]
total_payout = [b + d for b, d in zip(buybacks, dividends)]
payout_ratio = [p / f * 100 for p, f in zip(total_payout, fcf)]

inv_cap = [
    22101 + 12031 - 13296 + 16800,
    42978 + 11056 - 25984 + 21500,
    79327 + 9982 - 43210 + 29000,
    157293 + 13612 - 62556 + 38022
]
roic = [n / ic * 100 for n, ic in zip(nopat, inv_cap)]

print("=== PART I: NVIDIA INTERNAL CAPEX & SHAREHOLDER PAYOUT ===")
for i, y in enumerate(years):
    print(f"{y}: Rev=${rev[i]:,.0f}M | NOPAT=${nopat[i]:,.0f}M | CapEx=${capex[i]:,.0f}M | ROIC={roic[i]:.1f}% | ShareholderPayout=${total_payout[i]:,.0f}M ({payout_ratio[i]:.1f}% of FCF)")

# Customer / Ecosystem Side:
hyperscaler_capex_26 = 408.0 # $B
nvda_dc_rev_26 = 185.0 # $B
payout_to_nvda = (nvda_dc_rev_26 / hyperscaler_capex_26) * 100
inc_ai_rev_26 = 58.0 # $B
inc_ai_gp = inc_ai_rev_26 * 0.65 # $B
gpu_deprec_annual = nvda_dc_rev_26 / 3.5 # $B
customer_net_ai_income = inc_ai_gp - gpu_deprec_annual
customer_roi = (customer_net_ai_income / nvda_dc_rev_26) * 100
customer_payback_yrs = nvda_dc_rev_26 / inc_ai_gp

print("\n=== PART II: HYPERSCALER CAPEX PAYOUT TO NVIDIA & CUSTOMER ROI ===")
print(f"Big 4 Hyperscaler Total Annual CapEx: ${hyperscaler_capex_26:.1f}B")
print(f"Hyperscaler CapEx Paid Out to NVDA: ${nvda_dc_rev_26:.1f}B ({payout_to_nvda:.1f}% of total hyperscaler capex!)")
print(f"Customer Incremental AI Revenue Generated: ${inc_ai_rev_26:.1f}B")
print(f"Customer AI Gross Profit (at 65% margin): ${inc_ai_gp:.1f}B")
print(f"Annual GPU Depreciation (3.5-Yr Useful Life): ${gpu_deprec_annual:.1f}B")
print(f"Customer Net AI Operating Income: ${customer_net_ai_income:.1f}B (Net ROI: {customer_roi:.1f}%)")
print(f"Customer Payback Period: {customer_payback_yrs:.2f} Years (vs. 3.5-Yr Hardware Life)")

# The Break-even revenue requirement
required_ai_rev_for_15pct_roi = (nvda_dc_rev_26 * 0.15 + gpu_deprec_annual) / 0.65
print(f"Required Annual AI Revenue to achieve a 15% Customer ROIC: ${required_ai_rev_for_15pct_roi:.1f}B")
print(f"Current Revenue Gap (Deficit): ${required_ai_rev_for_15pct_roi - inc_ai_rev_26:.1f}B")
