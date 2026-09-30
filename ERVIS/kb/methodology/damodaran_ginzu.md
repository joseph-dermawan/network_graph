# Methodology: Damodaran FCFF Ginzu Normalization & Valuation Rules

---

## 1. Operating Lease Capitalization Engine
Converts off-balance-sheet commitments into balance-sheet debt:
$$\text{Lease Debt} = \sum_{t=1}^{5} \frac{\text{Commitment}_t}{(1 + K_d)^t} + \frac{\text{Commitment}_{6+}}{K_d \cdot (1 + K_d)^5} \left[1 - \frac{1}{(1 + K_d)^N}\right]$$
* **EBIT Adjustment:** $\Delta \text{EBIT} = \text{Current Rental Expense} - \text{Depreciation}_{\text{LeaseAsset}}$
* **Balance Sheet Impact:** $\Delta \text{Total Debt} = +\text{Lease Debt}$, $\Delta \text{Invested Capital} = +\text{Lease Debt}$
* **Cash Flow Invariance:** $\Delta \text{FCFF} \equiv 0$

---

## 2. R&D Capitalization & Amortization Engine
Treats R&D as a long-term capital asset with amortizable life $N$:
$$\text{Research Asset}_0 = \sum_{t=0}^{N-1} \text{RD}_{-t} \left(1 - \frac{t}{N}\right), \quad \text{Amortization}_0 = \sum_{t=0}^{N-1} \frac{\text{RD}_{-t}}{N}$$
* **EBIT Adjustment:** $\Delta \text{EBIT} = \text{Current R&D} - \text{Amortization}_0$
* **Reinvestment Adjustment:** $\Delta \text{Reinvestment} = \text{Current R&D} - \text{Amortization}_0$
* **Invested Capital:** $\Delta \text{Invested Capital} = +\text{Research Asset}_0$

---

## 3. Sales-to-Capital Reinvestment Link
Reinvestment is locked to incremental top-line revenue expansion:
$$\text{Reinvestment}_t = \frac{\text{Revenues}_t - \text{Revenues}_{t-1}}{(\text{Sales} / \text{Capital})_t}$$
* Prevents the analyst error of projecting revenue growth with zero capital expenditures.
* Includes a 0-to-3 year gestation lag switch for multi-year capital projects.

---

## 4. The Terminal Moat Consistency Rule
In the perpetual stable growth phase, reinvestment must obey:
$$\text{Reinvestment Rate}_{\text{terminal}} = \frac{g}{\text{ROIC}_{\text{terminal}}}$$
$$\text{Terminal Value} = \frac{\text{NOPAT}_{11} \left(1 - \frac{g}{\text{ROIC}_{\text{terminal}}}\right)}{\text{WACC}_{\text{terminal}} - g}$$
* **Zero Excess Returns (No Moat):** $\text{ROIC}_{\text{terminal}} = \text{WACC}_{\text{terminal}}$.
* **Durable Economic Moat:** $\text{ROIC}_{\text{terminal}} > \text{WACC}_{\text{terminal}}$ (Requires explicit justification).
