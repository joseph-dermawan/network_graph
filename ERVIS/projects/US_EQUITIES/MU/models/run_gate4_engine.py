import numpy as np

# -------------------------------------------------------------
# 1. 10-YEAR DISCRETE DCF (PLAN A)
# -------------------------------------------------------------
rf = 0.0494
erp = 0.0461
spot = 594.51
shares = 1131.42
net_cash = 67964.0 # $M
rev0 = 133188.0
ebit0 = 100992.0
sales_to_cap = 2.20
tg = 0.03
terminal_roic = 0.15

# WACC schedule: Y1-5: 10.51%, Y6-9: 9.50%, Y10+: 8.50%
wacc_schedule = [0.1051]*5 + [0.0950]*4 + [0.0850]
# Cumulative discount factor
df_list = []
cum_df = 1.0
for yr in range(10):
    cum_df /= (1.0 + wacc_schedule[yr])
    df_list.append(cum_df)

# Tax rate schedule: FY26 14.81% graduating to 21.0% statutory by Y10
tax_schedule = [0.1481 + (0.2100 - 0.1481) * (i / 9.0) for i in range(10)]

# Plan A Forecasts
g_a = [0.08, 0.04, 0.00, -0.05, 0.02, 0.04, 0.04, 0.03, 0.03, 0.03]
m_a = [0.70, 0.60, 0.50, 0.42, 0.38, 0.35, 0.35, 0.35, 0.35, 0.35]

curr_rev = rev0
dcf_table = []
pv_fcff_total = 0.0

for yr in range(1, 11):
    g = g_a[yr-1]
    curr_rev *= (1.0 + g)
    m = m_a[yr-1]
    ebit = curr_rev * m
    t = tax_schedule[yr-1]
    nopat = ebit * (1.0 - t)
    
    delta_rev = curr_rev * g / (1.0 + g) if g > 0 else 0.0
    reinvest = delta_rev / sales_to_cap
    fcff = nopat - reinvest
    
    df = df_list[yr-1]
    pv_fcff = fcff * df
    pv_fcff_total += pv_fcff
    
    dcf_table.append({
        'year': yr,
        'growth': g,
        'rev': curr_rev,
        'margin': m,
        'ebit': ebit,
        'tax': t,
        'nopat': nopat,
        'reinvest': reinvest,
        'fcff': fcff,
        'df': df,
        'pv_fcff': pv_fcff
    })

# Terminal Year (Year 11)
term_rev = curr_rev * (1.0 + tg)
term_ebit = term_rev * m_a[-1]
term_nopat = term_ebit * (1.0 - 0.21)
term_reinvest = term_nopat * (tg / terminal_roic)
term_fcff = term_nopat - term_reinvest
terminal_wacc = 0.0850
terminal_val = term_fcff / (terminal_wacc - tg)
pv_terminal_val = terminal_val * df_list[-1]

ev_dcf = pv_fcff_total + pv_terminal_val
eq_val_dcf = ev_dcf + net_cash
per_share_dcf = eq_val_dcf / shares

print("=== 10-YEAR DCF SUMMARY ===")
print(f"PV of 10-Yr Discrete FCFF: ${pv_fcff_total/1000:.1f}B")
print(f"PV of Terminal Value:     ${pv_terminal_val/1000:.1f}B")
print(f"Enterprise Value (EV):    ${ev_dcf/1000:.1f}B")
print(f"Net Cash:                 +${net_cash/1000:.1f}B")
print(f"Equity Intrinsic Value:   ${eq_val_dcf/1000:.1f}B")
print(f"DCF Value Per Share:      ${per_share_dcf:.2f}")

# -------------------------------------------------------------
# 2. SUM-OF-THE-PARTS (SOTP) DIVISIONAL VALUATION
# -------------------------------------------------------------
haircut = 0.60
cnbu_ev = (71853.0 * haircut) * 8.5 # $366.5B
mbu_ev = (15982.0 * haircut) * 6.5  # $62.3B
sbu_ev = (11506.0 * haircut) * 5.5  # $38.0B
ebu_ev = (7276.0 * haircut) * 7.5   # $32.7B
sotp_ev = cnbu_ev + mbu_ev + sbu_ev + ebu_ev
sotp_equity = sotp_ev + net_cash
sotp_per_share = sotp_equity / shares

print("\n=== SOTP DIVISIONAL VALUATION ===")
print(f"CNBU Enterprise Value:    ${cnbu_ev/1000:.1f}B")
print(f"MBU Enterprise Value:     ${mbu_ev/1000:.1f}B")
print(f"SBU Enterprise Value:     ${sbu_ev/1000:.1f}B")
print(f"EBU Enterprise Value:     ${ebu_ev/1000:.1f}B")
print(f"Total SOTP EV:            ${sotp_ev/1000:.1f}B")
print(f"SOTP Equity Value:        ${sotp_equity/1000:.1f}B")
print(f"SOTP Value Per Share:     ${sotp_per_share:.2f}")

# -------------------------------------------------------------
# 3. 10,000-TRIAL MONTE CARLO SIMULATION
# -------------------------------------------------------------
np.random.seed(42)
n_trials = 10000

wacc_trials = np.random.normal(0.1051, 0.0075, n_trials)
tg_trials = np.clip(np.random.normal(0.030, 0.005, n_trials), 0.015, 0.045)
tm_trials = np.clip(np.random.normal(0.35, 0.04, n_trials), 0.22, 0.48)
cagr_factor_trials = np.clip(np.random.normal(1.0, 0.12, n_trials), 0.70, 1.35)

mc_prices = []
for i in range(n_trials):
    w = wacc_trials[i]
    t_g = tg_trials[i]
    t_m = tm_trials[i]
    cf = cagr_factor_trials[i]
    
    base_pv_fcff = pv_fcff_total * cf * ((0.1051 / w) ** 5)
    term_w = max(w - 0.02, t_g + 0.02)
    tv = (term_rev * t_m * (1 - 0.21) * (1 - t_g/terminal_roic)) / (term_w - t_g)
    pv_tv = tv / ((1 + w) ** 10)
    
    sim_ev = base_pv_fcff + pv_tv
    sim_eq = sim_ev + net_cash
    sim_price = sim_eq / shares
    mc_prices.append(sim_price)

mc_prices = np.array(mc_prices)
p10 = np.percentile(mc_prices, 10)
p50 = np.percentile(mc_prices, 50)
p90 = np.percentile(mc_prices, 90)
mean_mc = np.mean(mc_prices)
win_rate = np.mean(mc_prices > spot) * 100.0

print("\n=== 10,000-TRIAL MONTE CARLO ===")
print(f"P10 Downside:             ${p10:.2f}")
print(f"P50 Median:               ${p50:.2f}")
print(f"Mean Intrinsic:           ${mean_mc:.2f}")
print(f"P90 Bullish:              ${p90:.2f}")
print(f"Win Rate (> $594.51):     {win_rate:.1f}%")

# -------------------------------------------------------------
# 4. LIQUIDATION HAIRCUT FLOOR
# -------------------------------------------------------------
liq_assets = 43434.0 + 28518.0 + (36197.0 * 0.75) + (10372.0 * 0.50) + (63310.0 * 0.30) + (12557.0 * 0.05)
total_liabilities = 57510.0
liq_equity = liq_assets - total_liabilities
liq_per_share = liq_equity / shares

print("\n=== LIQUIDATION HAIRCUT FLOOR ===")
print(f"Liquidation Asset Value:  ${liq_assets/1000:.1f}B")
print(f"Total Debt & Liabilities: ${total_liabilities/1000:.1f}B")
print(f"Liquidation Equity Floor: ${liq_equity/1000:.1f}B")
print(f"Floor Value Per Share:    ${liq_per_share:.2f}")

# Save full outputs to JSON
import json
output_payload = {
    "dcf": {
        "per_share": round(per_share_dcf, 2),
        "pv_fcff_usd_b": round(pv_fcff_total/1000, 2),
        "pv_terminal_usd_b": round(pv_terminal_val/1000, 2),
        "enterprise_value_usd_b": round(ev_dcf/1000, 2),
        "net_cash_usd_b": round(net_cash/1000, 2),
        "equity_value_usd_b": round(eq_val_dcf/1000, 2),
        "table": dcf_table
    },
    "sotp": {
        "per_share": round(sotp_per_share, 2),
        "cnbu_ev_b": round(cnbu_ev/1000, 2),
        "mbu_ev_b": round(mbu_ev/1000, 2),
        "sbu_ev_b": round(sbu_ev/1000, 2),
        "ebu_ev_b": round(ebu_ev/1000, 2),
        "total_ev_b": round(sotp_ev/1000, 2),
        "equity_value_b": round(sotp_equity/1000, 2)
    },
    "monte_carlo": {
        "p10": round(p10, 2),
        "p50_median": round(p50, 2),
        "mean": round(mean_mc, 2),
        "p90": round(p90, 2),
        "win_rate_pct": round(win_rate, 1)
    },
    "liquidation_floor": {
        "per_share": round(liq_per_share, 2),
        "liquidated_assets_b": round(liq_assets/1000, 2),
        "total_liabilities_b": round(total_liabilities/1000, 2),
        "net_equity_floor_b": round(liq_equity/1000, 2)
    }
}

with open("ERVIS/projects/US_EQUITIES/MU/models/gate4_valuation_outputs.json", "w") as f:
    json.dump(output_payload, f, indent=2)

print("Saved Gate 4 outputs to JSON successfully.")
