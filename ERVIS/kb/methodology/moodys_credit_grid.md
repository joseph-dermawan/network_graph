# Methodology: Moody's 6-Metric Synthetic Rating & WACC Solver

---

## 1. Moody's Industrial Rating Benchmark Matrix

| Metric Name | Formula | Aaa | Aa | A | Baa | Ba | B / Caa |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Interest Coverage** | $\text{EBIT} / \text{Interest}$ | $>16.0\text{x}$ | $8.6\text{x}$ | $5.4\text{x}$ | $3.7\text{x}$ | $1.9\text{x}$ | $0.7\text{x}$ |
| **Debt / Equity Leverage** | $\text{Liabilities} / \text{Equity}$ | $31.6\%$ | $41.7\%$ | $45.0\%$ | $49.8\%$ | $68.7\%$ | $92.2\%$ |
| **Return on Assets (ROA)** | $\text{Net Income} / \text{Assets}$ | $11.6\%$ | $7.5\%$ | $5.5\%$ | $4.4\%$ | $1.7\%$ | $-2.1\%$ |
| **Asset Coverage** | $\text{Assets} / \text{Liabilities}$ | $3.70\text{x}$ | $2.40\text{x}$ | $2.20\text{x}$ | $2.00\text{x}$ | $1.30\text{x}$ | $1.00\text{x}$ |
| **Profitability Margin** | $\text{Net Income} / \text{Revenues}$ | $11.8\%$ | $9.0\%$ | $7.0\%$ | $5.0\%$ | $2.0\%$ | $-2.6\%$ |
| **Current Ratio** | $\text{Current Assets} / \text{Current Liab}$ | $2.65\text{x}$ | $2.00\text{x}$ | $1.80\text{x}$ | $1.50\text{x}$ | $1.20\text{x}$ | $0.90\text{x}$ |

---

## 2. Enterprise Risk Management (ERM) Adjustment Rules
1. Calculate the weighted baseline credit score across the 6 ratios.
2. Apply qualitative ERM adjustments:
   * **+1 Notch:** Dominant regional/global market share ($>40\%$) or robust balance sheet cash war chest ($>30\%$ of market cap).
   * **+2 Notches:** Sovereign backing (e.g. Temasek, Government entity $>30\%$ shareholder) or monopoly gateway infrastructure concession.
   * **-1 Notch:** Customer concentration (Single customer $>25\%$ revenue) or active patent litigation risk.

---

## 3. Damodaran Default Spread Mapping & Cost of Debt
* Look up rating in the Damodaran Default Spread Table:
  * `Aaa / AAA`: $+0.59\%$
  * `Aa2 / AA`: $+0.73\%$
  * `A1 / A+`: $+1.12\%$
  * `A2 / A`: $+1.30\%$
  * `Baa2 / BBB`: $+1.60\%$
  * `Ba1 / BB+`: $+2.00\%$
  * `B2 / B`: $+3.40\%$
  * `Caa / CCC`: $+8.20\%$
* Pre-Tax Cost of Debt: $K_d = R_f + \text{Default Spread}_{\text{Moody's Adjusted}}$
* Cross-check with secondary market corporate bond YTM.
