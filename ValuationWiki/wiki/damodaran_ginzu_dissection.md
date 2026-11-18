# Damodaran Ginzu Model: Mathematical Derivations, Equation Blueprint & Sheet Architecture

This document provides a comprehensive dissection of Professor Aswath Damodaran's **Ginzu Valuation Model** (`fcffginzu.xlsx`). It details all underlying mathematical formulas, accounting adjustments, sheet logic layouts, cell dependencies, and design principles required to build a custom, institutional-grade Excel valuation model.

---

## 🏛️ 1. Architecture & Tab Interconnection Map

The Ginzu model is designed as a modular financial compiler where specialized accounting conversion sheets feed into a master input dashboard, which subsequently drives the pro-forma DCF evaluation engine.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                GINZU ARCHITECTURE MAP                                  │
│                                                                                        │
│  [R&D Converter]  ──► Capitalized R&D Asset & Amortization Add-back                        │
│                                                            │                           │
│  [Lease Converter] ──► Debt Value of Leases & Operating Income Adj. ──► [Master Inputs]  │
│                                                            │           (Dashboard)     │
│  [Ratings Estimator] ──► Synthetic Rating & Cost of Debt   │               │           │
│                                                            │               ▼           │
│  [Cost of Capital] ──► Bottom-up Beta & Geographic ERP ────┘       [Valuation Model]   │
│                                                                    (10-Yr FCFF Engine) │
│                                                                            │           │
│                                                                            ▼           │
│                                                                    [Option Value]      │
│                                                                    & Implied Share Px  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 2. Accounting Normalization & Converter Mathematics

### A. Research & Development (R&D) Capitalization Converter (`R&D converter`)
Under standard accounting (GAAP/IFRS), R&D is expensed immediately. Damodaran treats R&D as a long-term capital expenditure that creates an intangible **Research Asset**.

#### 1. Research Asset Value Calculation
Given an amortizable life of $n$ years (default = 5 years) and historical R&D expenses $RD_{-t}$ for $t = 1, \dots, n$:

$$\text{Unamortized Portion}_t = \frac{n - t}{n}$$

$$\text{Value of Research Asset} = \sum_{t=1}^{n} \left( RD_{-t} \times \frac{n - t}{n} \right)$$

#### 2. Amortization Expense of Research Asset
$$\text{Amortization of R\&D}_0 = \sum_{t=1}^{n} \left( \frac{RD_{-t}}{n} \right)$$

#### 3. Financial Statement Adjustments
* **Adjusted Operating Income (EBIT):**
  $$\text{EBIT}_{\text{adjusted}} = \text{EBIT}_{\text{reported}} + RD_0 - \text{Amortization of R\&D}_0$$
* **Adjusted Capital Expenditures (CapEx):**
  $$\text{CapEx}_{\text{adjusted}} = \text{CapEx}_{\text{reported}} + RD_0 - \text{Amortization of R\&D}_0$$
* **Adjusted Book Value of Equity:**
  $$\text{Equity}_{\text{adjusted}} = \text{Equity}_{\text{reported}} + \text{Value of Research Asset}$$

---

### B. Operating Lease Capitalization Converter (`Operating lease converter`)
Operating leases represent off-balance-sheet contractual debt obligations. Damodaran converts operating lease commitments into equivalent financial debt.

#### 1. Debt Value of Operating Leases
Given future annual lease commitments $L_t$ for $t = 1, \dots, 5$ and average annual commitment $L_{\text{avg}} = \frac{1}{5} \sum_{t=1}^{5} L_t$ for year $6+$:

$$n_{\text{extra}} = \text{ROUND}\left( \frac{L_{6+}}{L_{\text{avg}}} \right)$$

$$\text{Debt Value of Leases} = \sum_{t=1}^{5} \frac{L_t}{(1 + K_d)^t} + \sum_{t=6}^{5 + n_{\text{extra}}} \frac{L_{\text{avg}}}{(1 + K_d)^t}$$

*Where $K_d$ is the company's pre-tax cost of debt.*

#### 2. Financial Statement Adjustments
* **Adjusted Operating Income (EBIT):**
  $$\text{EBIT}_{\text{adjusted}} = \text{EBIT}_{\text{reported}} + \text{Lease Expense}_0 - \text{Depreciation of Lease Asset}_0$$
  *(Approximated as: $\text{EBIT}_{\text{adjusted}} = \text{EBIT}_{\text{reported}} + (\text{Debt Value of Leases} \times K_d)$)*
* **Adjusted Total Debt Balance:**
  $$\text{Total Debt}_{\text{adjusted}} = \text{Reported Debt} + \text{Debt Value of Leases}$$

---

## 🧮 3. Cost of Capital & Country Risk Mathematics (`Cost of capital worksheet`)

### A. Bottom-Up Business Beta & Re-Levering (Hamada Equation)
Instead of relying on noisy stock regression betas, Damodaran derives a bottom-up unlevered beta based on business segment revenue exposure:

1. **Weighted Unlevered Beta ($\beta_U$):**
   $$\beta_U = \sum_{i=1}^{m} \left( w_i \times \beta_{U, i} \right)$$
   *Where $w_i$ is the percentage of revenue/value from industry segment $i$, and $\beta_{U, i}$ is the peer unlevered beta.*

2. **Re-Levered Equity Beta ($\beta_L$):**
   $$\beta_L = \beta_U \times \left[ 1 + (1 - t) \times \left( \frac{D}{E} \right) \right]$$
   *Where $D/E$ is the market debt-to-equity ratio, and $t$ is the marginal corporate tax rate.*

---

### B. Geographic Revenue-Weighted Equity Risk Premium (ERP)
Instead of assigning a single country ERP based on incorporation location, Damodaran weights ERP by regional revenue generation:

$$\text{Blended ERP} = \sum_{j=1}^{k} \left( \text{Revenue Share}_j \times \text{ERP}_j \right)$$

$$\text{Cost of Equity } (K_e) = R_f + \left( \beta_L \times \text{Blended ERP} \right)$$

---

## 📈 4. Pro-Forma Growth & Reinvestment Engine (`Valuation Model`)

Damodaran's Ginzu model enforces strict fundamental links between growth, reinvestment, and Return on Invested Capital (ROIC).

### A. Fundamental Growth Equation
$$\text{Expected Operating Growth } (g) = \text{Reinvestment Rate} \times \text{ROIC}$$

Where:
$$\text{ROIC} = \frac{\text{NOPAT}}{\text{Invested Capital}} = \frac{\text{EBIT} \times (1 - t)}{\text{Book Value of Equity} + \text{Total Debt} - \text{Cash}}$$

$$\text{Reinvestment Rate} = \frac{\text{CapEx} - \text{D\&A} + \Delta\text{NWC}}{\text{EBIT} \times (1 - t)}$$

---

### B. Sales-to-Capital Ratio Reinvestment Model
When forecasting future growth $g_t$ across the 10-year projection period, Damodaran allows the model to compute required reinvestment using the **Sales-to-Capital Ratio** ($\text{S/C}$):

$$\Delta \text{Revenue}_t = \text{Revenue}_{t-1} \times g_t$$

$$\text{Required Reinvestment}_t = \frac{\Delta \text{Revenue}_t}{\text{Sales-to-Capital Ratio}}$$

$$\text{FCFF}_t = \text{EBIT}_t \times (1 - t_t) - \text{Required Reinvestment}_t$$

---

### C. 2-Stage Convergence Dynamics (High Growth $\rightarrow$ Stable Growth)

1. **High Growth Period (Years 1–5):**
   * Operating margins ($m_t$) move linearly from current margin $m_0$ toward target industry margin $m^*$.
   * Reinvestment rate is driven by Sales-to-Capital ratio.
   * Discount rate equals high-growth WACC.

2. **Transition & Stable Growth Period (Years 6–10):**
   * Growth rate $g_t$ scales down to equal risk-free rate $R_f$ by Year 10 ($g_{\text{stable}} = R_f$).
   * Target Stable Reinvestment Rate:
     $$\text{Reinvestment Rate}_{\text{stable}} = \frac{g_{\text{stable}}}{\text{ROIC}_{\text{stable}}}$$
     *(Assuming $\text{ROIC}_{\text{stable}} = \text{WACC}_{\text{stable}}$, then $\text{Reinvestment Rate}_{\text{stable}} = \frac{R_f}{\text{WACC}_{\text{stable}}}$).*

---

### D. Terminal Value & Equity Value Bridge

$$\text{Terminal Value}_n = \frac{\text{EBIT}_{n+1} \times (1 - t_{\text{stable}}) \times (1 - \text{Reinvestment Rate}_{\text{stable}})}{\text{WACC}_{\text{stable}} - g_{\text{stable}}}$$

$$\text{Enterprise Value} = \sum_{t=1}^{n} \frac{\text{FCFF}_t}{(1 + \text{WACC}_t)^t} + \frac{\text{Terminal Value}_n}{(1 + \text{WACC}_n)^n}$$

$$\text{Equity Value} = \text{Enterprise Value} + \text{Cash \& Equivalents} - \text{Total Debt} - \text{Options Outstanding} - \text{NCI} - \text{Pension Deficits}$$

$$\text{Value per Share} = \frac{\text{Equity Value}}{\text{Diluted Shares Outstanding}}$$

---

## 🎨 5. Sheet Logic Layout, Color Conventions & Excel Design Rules

To ensure clarity, auditability, and maintainability, Damodaran enforces strict spreadsheet design rules:

### A. Standard Color Coding System
* **Blue Text / Light Yellow Fill (`#FFFFCC`):** Hardcoded Input Cells (Only user inputs go here).
* **Black Text / White Fill (`#FFFFFF`):** Evaluated Formulas (No hardcoded values allowed).
* **Green Text / Light Green Fill (`#E2EFDA`):** Key Output & Calculated Valuation Targets.
* **Red Text / Pink Warning Fill (`#FCE4D6`):** Data Validation Checks & Error Warnings (e.g. $g > R_f$ or $K_d < R_f$).

### B. Cell Reference & Auditing Rules
1. **No Naked Strings:** Every formula string assigned via openpyxl must begin with `=` (e.g. `='Master Inputs Start here'!B12`).
2. **Dynamic Range Offsets:** Never hardcode cell locations in summary sheets; reference named ranges or exact lookup coordinates.
3. **Circular Reference Switches:** Disable circular references in Excel options by modeling interest expense based on prior-period debt balance ($D_{t-1}$) rather than current-period debt ($D_t$).

---

## 🔗 Related Wiki Pages
* [[model_valuation]]: Master 10-step institutional valuation framework.
* [[DCF_Valuation_Model]]: Powell Industries 10-year pro-forma DCF model.
* [[WACC_Cost_of_Capital]]: Cost of capital derivation.
