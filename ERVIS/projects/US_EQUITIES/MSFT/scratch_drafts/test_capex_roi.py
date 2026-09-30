# Gate 4B AI CapEx Payout & ROI Analysis
msft_capex_26 = 115.948 # $B
msft_fcf_26 = 66.987 # $B
msft_cfo_26 = 182.935 # $B
msft_rev_26 = 331.839 # $B

# AI CapEx breakdown
# Hyperscaler AI CapEx infrastructure split typically: ~65% GPU server hardware & accelerators, ~35% data center real estate, power, shells, networking
gpu_hardware_share = 0.65
ai_gpu_capex = msft_capex_26 * gpu_hardware_share # $75.366B

# Incremental AI Revenue:
# Azure AI consumption + M365 Copilot & GitHub Copilot seats = ~$18.0B
ai_rev_26 = 18.0 # $B
ai_gross_margin = 0.65 # 65% software & cloud gross margin
ai_gross_profit = ai_rev_26 * ai_gross_margin # $11.70B

# Depreciation over 3.5-Year Useful Life
gpu_depr_annual = ai_gpu_capex / 3.5 # $21.53B
total_capex_depr_annual = msft_capex_26 / 3.5 # $33.13B

# Net AI Operating Income
# Using GPU hardware depreciation:
net_ai_op_income_gpu = ai_gross_profit - gpu_depr_annual # 11.70 - 21.53 = -$9.83B
net_ai_roi_gpu = (net_ai_op_income_gpu / ai_gpu_capex) * 100 # -13.05%

# Using Total AI CapEx depreciation:
net_ai_op_income_tot = ai_gross_profit - total_capex_depr_annual # 11.70 - 33.13 = -$21.43B
net_ai_roi_tot = (net_ai_op_income_tot / msft_capex_26) * 100 # -18.48%

# Cash Payback Period (CapEx / AI Gross Profit)
payback_gpu_yrs = ai_gpu_capex / ai_gross_profit # 75.37 / 11.70 = 6.44 years
payback_tot_yrs = msft_capex_26 / ai_gross_profit # 115.95 / 11.70 = 9.91 years

# Hardware Obsolescence Deficit (Payback vs 3.5 yr useful life)
obsolescence_deficit_gpu = payback_gpu_yrs - 3.5 # +2.94 years
obsolescence_deficit_tot = payback_tot_yrs - 3.5 # +6.41 years

# Break-even Monetization Gap:
# To break even on operating income (Net AI Op Income = 0):
# Required AI Rev = Annual Depreciation / Gross Margin
req_rev_breakeven_gpu = gpu_depr_annual / ai_gross_margin # 21.53 / 0.65 = $33.13B
gap_breakeven_gpu = req_rev_breakeven_gpu - ai_rev_26 # $15.13B deficit

req_rev_breakeven_tot = total_capex_depr_annual / ai_gross_margin # 33.13 / 0.65 = $50.97B
gap_breakeven_tot = req_rev_breakeven_tot - ai_rev_26 # $32.97B deficit

# To achieve target 15% ROIC on AI capital:
target_roic = 0.15
req_op_inc_15 = msft_capex_26 * target_roic # $17.39B
req_gp_15 = req_op_inc_15 + total_capex_depr_annual # 17.39 + 33.13 = $50.52B
req_rev_15 = req_gp_15 / ai_gross_margin # 50.52 / 0.65 = $77.73B
gap_15 = req_rev_15 - ai_rev_26 # $59.73B monetization gap

print(f"MSFT Own Total AI CapEx: ${msft_capex_26:.3f}B")
print(f"AI GPU Hardware Component (65%): ${ai_gpu_capex:.3f}B")
print(f"Incremental AI Revenue: ${ai_rev_26:.2f}B (Gross Profit: ${ai_gross_profit:.2f}B)")
print(f"Annual GPU Depreciation (3.5-Yr Life): ${gpu_depr_annual:.2f}B/yr")
print(f"Net AI Operating Income: ${net_ai_op_income_gpu:.2f}B (Net ROI: {net_ai_roi_gpu:.1f}%)")
print(f"Payback Period: {payback_gpu_yrs:.2f} Years vs 3.5-Yr Life (Deficit: +{obsolescence_deficit_gpu:.2f} yrs)")
print(f"Break-even AI Revenue: ${req_rev_breakeven_gpu:.2f}B (Deficit: ${gap_breakeven_gpu:.2f}B)")
print(f"Required AI Revenue for 15% ROIC: ${req_rev_15:.2f}B (Deficit: ${gap_15:.2f}B)")
