import numpy as np

base_rev = 41305.0
tax_rate = 0.15
base_wacc = 0.1020
term_wacc = 0.0900
shares = 1632.48
net_cash = 7785.0

growth = [0.24, 0.20, 0.16, 0.12, 0.09, 0.07, 0.055, 0.045, 0.040, 0.038]
margins = [0.275, 0.290, 0.305, 0.315, 0.325, 0.328, 0.330, 0.330, 0.330, 0.330]
s_to_c = 3.20

rev = base_rev
cum_df = 1.0
pvs = []
revs = []
for i in range(10):
    g = growth[i]
    m = margins[i]
    w = base_wacc + (term_wacc - base_wacc) * (i / 9.0)
    next_rev = rev * (1.0 + g)
    delta_rev = next_rev - rev
    ebit = next_rev * m
    nopat = ebit * (1.0 - tax_rate)
    reinv = delta_rev / s_to_c
    fcff = nopat - reinv
    cum_df /= (1.0 + w)
    pv = fcff * cum_df
    pvs.append(pv)
    rev = next_rev
    revs.append(rev)

pv_fcff_10y = sum(pvs)
term_g = 0.038
term_roic = 0.20
term_reinv_rate = term_g / term_roic
term_rev = revs[-1] * (1.0 + term_g)
term_ebit = term_rev * margins[-1]
term_nopat = term_ebit * (1.0 - tax_rate)
term_fcff = term_nopat * (1.0 - term_reinv_rate)
tv = term_fcff / (term_wacc - term_g)
pv_tv = tv * cum_df

ev_dcf = pv_fcff_10y + pv_tv
eq_dcf = ev_dcf + net_cash
dcf_per_share = eq_dcf / shares

print(f"10y PV FCFF: ${pv_fcff_10y:,.1f}M")
print(f"PV TV: ${pv_tv:,.1f}M")
print(f"EV DCF: ${ev_dcf:,.1f}M")
print(f"Equity DCF: ${eq_dcf:,.1f}M")
print(f"DCF Value per share: ${dcf_per_share:.2f}")
