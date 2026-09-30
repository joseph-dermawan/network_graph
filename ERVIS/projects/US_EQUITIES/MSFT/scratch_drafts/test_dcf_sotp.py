import numpy as np

# Base Inputs
rev_0 = 331839.0 # FY2026 reported revenue ($M)
norm_ebit_0 = 161823.1 # FY2026 normalized EBIT ($M)
tax_rate = 0.180
shares = 7425.55 # Million shares
spot_price = 493.89
net_cash = 2025.0 # Cash ($76,651M) - Total Debt ($74,626M)

base_wacc = 0.0879
terminal_wacc = 0.0900

# 10-Year Pro-Forma Forecast
# Years 1-5: High-growth phase driven by enterprise AI adoption & Azure expansion
# Years 6-10: Maturing phase fading to terminal growth
growth_rates = [0.150, 0.135, 0.120, 0.105, 0.090, 0.075, 0.065, 0.055, 0.045, 0.035]
margins = [0.485, 0.485, 0.480, 0.480, 0.475, 0.470, 0.465, 0.460, 0.455, 0.450]
sales_to_cap = 2.40 # Capital turnover capturing data center buildout

proj_rev = []
proj_ebit = []
proj_nopat = []
proj_reinv = []
proj_fcff = []
proj_wacc = []
proj_df = []
proj_pv = []

curr_rev = rev_0
cum_df = 1.0

for i in range(10):
    g = growth_rates[i]
    m = margins[i]
    w = base_wacc + (terminal_wacc - base_wacc) * (i / 9.0)
    
    rev = curr_rev * (1.0 + g)
    delta_rev = rev - curr_rev
    ebit = rev * m
    nopat = ebit * (1.0 - tax_rate)
    reinv = delta_rev / sales_to_cap
    fcff = nopat - reinv
    
    cum_df /= (1.0 + w)
    pv = fcff * cum_df
    
    proj_rev.append(rev)
    proj_ebit.append(ebit)
    proj_nopat.append(nopat)
    proj_reinv.append(reinv)
    proj_fcff.append(fcff)
    proj_wacc.append(w)
    proj_df.append(cum_df)
    proj_pv.append(pv)
    
    curr_rev = rev

pv_10yr = sum(proj_pv)

# Terminal Value
g_term = 0.035 # 3.50% terminal growth
roic_term = 0.25 # 25.0% durable software & cloud moat
reinv_term = g_term / roic_term # 14.0%
term_rev = proj_rev[-1] * (1.0 + g_term)
term_ebit = term_rev * margins[-1]
term_nopat = term_ebit * (1.0 - tax_rate)
term_reinv = term_nopat * reinv_term
term_fcff = term_nopat - term_reinv

tv = term_fcff / (terminal_wacc - g_term)
pv_tv = tv * proj_df[-1]

ev_dcf = pv_10yr + pv_tv
eq_dcf = ev_dcf + net_cash
dcf_per_share = eq_dcf / shares

print(f"PV 10-Yr FCFF: ${pv_10yr:,.1f}M")
print(f"PV Terminal Value: ${pv_tv:,.1f}M (TV: ${tv:,.1f}M)")
print(f"Enterprise Value DCF: ${ev_dcf:,.1f}M")
print(f"Equity Value DCF: ${eq_dcf:,.1f}M")
print(f"DCF Intrinsic Value per share: ${dcf_per_share:.2f}")

# SOTP
# 1. Productivity & Business Processes: FY26 Rev $93.4B, EBITDA $53.2B @ 22x EV/EBITDA = $1,170.4B
# 2. Intelligent Cloud: FY26 Rev $145.8B, EBITDA $75.8B @ 26x EV/EBITDA = $1,970.8B
# 3. More Personal Computing: FY26 Rev $92.6B, EBITDA $38.2B @ 16x EV/EBITDA = $611.2B
sotp_pbp = 1170400.0
sotp_ic = 1970800.0
sotp_mpc = 611200.0
sotp_ev = sotp_pbp + sotp_ic + sotp_mpc
sotp_eq = sotp_ev + net_cash
sotp_per_share = sotp_eq / shares
print(f"\nSOTP EV: ${sotp_ev:,.1f}M -> SOTP Per Share: ${sotp_per_share:.2f}")

# Monte Carlo 10k
np.random.seed(42)
trials = 10000
sim_g = np.random.normal(0.09, 0.02, trials)
sim_m = np.random.triangular(0.42, 0.47, 0.52, trials)
sim_w = np.random.normal(0.090, 0.005, trials)
sim_r = np.random.uniform(0.20, 0.30, trials)

sim_vals = []
for i in range(trials):
    g_s = sim_g[i]
    m_s = sim_m[i]
    w_s = max(sim_w[i], 0.06)
    r_s = sim_r[i]
    
    rev_5 = rev_0 * ((1.0 + g_s)**5)
    nopat_5 = rev_5 * m_s * (1.0 - tax_rate)
    
    reinv_r = 0.035 / r_s
    t_fcff = (nopat_5 * 1.035) * (1.0 - reinv_r)
    t_val = t_fcff / max(w_s - 0.035, 0.015)
    pv_t = t_val / ((1.0 + w_s)**5)
    
    disc_s = sum([((rev_0 * ((1.0 + g_s)**y)) * m_s * (1.0 - tax_rate) * 0.86) / ((1.0 + w_s)**y) for y in range(1, 6)])
    ev_s = disc_s + pv_t
    eq_s = ev_s + net_cash
    sim_vals.append(eq_s / shares)

sim_vals = np.array(sim_vals)
mc_p10 = np.percentile(sim_vals, 10)
mc_med = np.percentile(sim_vals, 50)
mc_p90 = np.percentile(sim_vals, 90)
win_rate = np.mean(sim_vals > spot_price) * 100.0
print(f"\nMonte Carlo: P10=${mc_p10:.2f}, Median=${mc_med:.2f}, P90=${mc_p90:.2f}, Win Rate={win_rate:.1f}%")

# Triangulation: 60% DCF + 30% SOTP + 10% MC Median
target_price = (dcf_per_share * 0.60) + (sotp_per_share * 0.30) + (mc_med * 0.10)
upside = ((target_price / spot_price) - 1.0) * 100.0
print(f"\nTarget Price: ${target_price:.2f} (Spot: ${spot_price:.2f}, Upside: {upside:+.2f}%)")
