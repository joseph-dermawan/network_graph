import math

rf = 0.0494
erp = 0.0461
tax = 0.1481
shares = 1131.42
net_cash = 67964.0 # $M

# Beta: Micron raw beta ~ 1.25. De-levered/Hamada ~ 1.22
beta = 1.22
ke = rf + beta * erp # 0.0494 + 1.22 * 0.0461 = 0.1056 (10.56%)
wacc = ke # net cash company, weight of debt is minimal, WACC ~ 10.5%
terminal_wacc = 0.085 # 8.5% in terminal year
tg = 0.03 # 3.0% terminal growth

print(f"WACC: {wacc:.4f}, Terminal WACC: {terminal_wacc:.4f}")

def run_dcf(rev0, ebit0, rev_growth_path, margin_path, sales_to_cap=2.2):
    curr_rev = rev0
    pv_fcff = 0.0
    fcff_series = []
    
    for yr in range(1, 11):
        g = rev_growth_path[yr-1]
        curr_rev *= (1.0 + g)
        m = margin_path[yr-1]
        ebit = curr_rev * m
        nopat = ebit * (1.0 - tax)
        reinv = (curr_rev * g / (1.0 + g)) / sales_to_cap if g > 0 else 0.0
        fcff = nopat - reinv
        df = 1.0 / ((1.0 + wacc) ** yr)
        pv_fcff += fcff * df
        fcff_series.append((curr_rev, m, ebit, fcff))
        
    term_rev = curr_rev * (1.0 + tg)
    term_m = margin_path[-1]
    term_ebit = term_rev * term_m
    term_nopat = term_ebit * (1.0 - tax)
    # Terminal reinvestment assuming durable moat ROIC = 15%
    term_reinv = term_nopat * (tg / 0.15)
    term_fcff = term_nopat - term_reinv
    tv = term_fcff / (terminal_wacc - tg)
    pv_tv = tv / ((1.0 + wacc) ** 10)
    
    ev = pv_fcff + pv_tv
    eq_val = ev + net_cash
    per_share = eq_val / shares
    return per_share, ev, eq_val, pv_fcff, pv_tv, fcff_series

# PROPOSAL A: Mean-reverting margin schedule
# Start rev 133.19B, margins step down from 74.6% to 35%
g_a = [0.08, 0.04, 0.00, -0.05, 0.02, 0.04, 0.04, 0.03, 0.03, 0.03]
m_a = [0.70, 0.60, 0.50, 0.42, 0.38, 0.35, 0.35, 0.35, 0.35, 0.35]
ps_a, ev_a, eq_a, pvf_a, pvt_a, s_a = run_dcf(133188.0, 100992.0, g_a, m_a)

# PROPOSAL B: Normalized Base Earnings DCF
# Start rev 55.0B, margin 32.5%, growing 10% CAGR
g_b = [0.12, 0.10, 0.10, 0.08, 0.08, 0.06, 0.05, 0.04, 0.03, 0.03]
m_b = [0.325]*10
ps_b, ev_b, eq_b, pvf_b, pvt_b, s_b = run_dcf(55000.0, 17875.0, g_b, m_b)

# PROPOSAL C: Super-cycle persistence (Hyper-Bull)
# Start rev 133.19B, high margins 65-70% sustained
g_c = [0.15, 0.12, 0.10, 0.08, 0.06, 0.05, 0.04, 0.03, 0.03, 0.03]
m_c = [0.72, 0.70, 0.68, 0.65, 0.62, 0.60, 0.55, 0.50, 0.45, 0.40]
ps_c, ev_c, eq_c, pvf_c, pvt_c, s_c = run_dcf(133188.0, 100992.0, g_c, m_c)

print(f"PROPOSAL A Fair Value: ${ps_a:.2f} (EV: ${ev_a/1000:.1f}B, Eq: ${eq_a/1000:.1f}B, PV(FCFF): ${pvf_a/1000:.1f}B, PV(TV): ${pvt_a/1000:.1f}B)")
print(f"PROPOSAL B Fair Value: ${ps_b:.2f} (EV: ${ev_b/1000:.1f}B, Eq: ${eq_b/1000:.1f}B, PV(FCFF): ${pvf_b/1000:.1f}B, PV(TV): ${pvt_b/1000:.1f}B)")
print(f"PROPOSAL C Fair Value: ${ps_c:.2f} (EV: ${ev_c/1000:.1f}B, Eq: ${eq_c/1000:.1f}B, PV(FCFF): ${pvf_c/1000:.1f}B, PV(TV): ${pvt_c/1000:.1f}B)")
