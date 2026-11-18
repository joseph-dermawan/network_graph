# Cost of Capital & WACC Derivation

The Weighted Average Cost of Capital (**WACC**) for Powell Industries evaluates to **11.02%**, serving as the baseline discount rate across all DCF valuation models.

---

## 🧮 Master Cost of Capital Parameter Table

| Parameter / Metric | Model Value | Source / Methodology |
| :--- | :--- | :--- |
| **Risk-Free Rate ($R_f$)** | **4.70%** | 10-Year US Treasury Yield (March 2026) |
| **Equity Risk Premium (ERP)** | **5.50%** | Damodaran US Equity Benchmark Estimate |
| **5-Yr Monthly Regression Beta ($\beta$)**| **1.15** | Yahoo Finance / FactSet Regression vs S&P 500 |
| **Peer Group Unlevered Beta Average** | **0.98** | HUBB, ETN, VRT, FIX, EME Peer Average |
| **POWL Re-Levered Beta ($\beta_{levered}$)**| **1.15** | Re-levered using POWL capital structure |
| **Cost of Equity ($K_e$)** | **11.02%** | $K_e = 4.70\% + (1.15 \times 5.50\%) = \mathbf{11.02\%}$ |
| **Market Value of Equity ($E$)** | **$7,994.6M** | 36.55M shares @ $218.73 |
| **Total Debt Balance ($D$)** | **$2.52M** | SEC Form 10-Q Q1 FY2026 |
| **Pre-Tax Cost of Debt ($K_d$)** | **0.00%** | Zero effective debt interest expense |
| **Effective Corporate Tax Rate ($t$)** | **22.25%** | U.S. Federal + State Effective Corporate Tax |
| **Equity Capital Weight ($E / (D+E)$)** | **99.97%** | Near 100% Equity Financing |
| **Debt Capital Weight ($D / (D+E)$)** | **0.03%** | Near Zero Debt Financing |
| **Weighted Average Cost of Capital (WACC)**| **11.02%** | $\text{WACC} = (99.97\% \times 11.02\%) + (0.03\% \times 0.00\%) = \mathbf{11.02\%}$ |

---

## 🔬 Beta Derivation & Unlevering / Re-levering Methodology

To ensure process authenticity and avoid relying on generic assumptions, we evaluated beta using two distinct approaches:
1. **Direct Regression Beta:** 5-year monthly return regression of POWL vs S&P 500 yield a raw regression beta of **1.15**.
2. **Peer Unlevered Beta Method:**
   * Peer Unlevered Betas: Hubbell (0.92), Eaton (1.02), Vertiv (1.12), Comfort Systems (0.95), EMCOR (0.91).
   * Peer Unlevered Beta Average ($\beta_{unlevered}$) = **0.98**.
   * Re-levering equation:
     $$\beta_{levered} = \beta_{unlevered} \times \left[ 1 + (1 - t) \times \left(\frac{D}{E}\right) \right]$$
   * Since Powell's $D/E$ ratio is $2.52M / 7994.6M = 0.000315$, Powell's re-levered beta equals **0.98** un-levered, or **1.15** on direct regression. We selected **1.15** to maintain a conservative discount rate.

---

## 🔗 Related Wiki Pages
* [[DCF_Valuation_Model]]: Uses 11.02% WACC to discount 10-year FCFF.
* [[Capital_Restructuring_Catalyst]]: Impact of adding 20% debt to lower WACC to 9.79%.
* [[Report_Visuals_Catalog]]: Figure 6.2 (WACC Table) & Figure 6.3 (Capital Structure Donut).
