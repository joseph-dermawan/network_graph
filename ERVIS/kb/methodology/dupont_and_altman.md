# Methodology: DuPont 5-Point ROE & Altman Z-Score Diagnostics

---

## 1. DuPont 5-Point Return on Equity Decomposition

$$\text{ROE} = \underbrace{\frac{\text{Net Income}}{\text{EBT}}}_{\text{Tax Burden (1 - t)}} \times \underbrace{\frac{\text{EBT}}{\text{EBIT}}}_{\text{Interest Burden}} \times \underbrace{\frac{\text{EBIT}}{\text{Revenue}}}_{\text{Operating Margin}} \times \underbrace{\frac{\text{Revenue}}{\text{Total Assets}}}_{\text{Asset Turnover}} \times \underbrace{\frac{\text{Total Assets}}{\text{Equity}}}_{\text{Equity Multiplier}}$$

### Diagnostic Rules:
* **Operating Recovery vs Leverage Distortion:** If ROE improves while the Equity Multiplier ($\text{Assets}/\text{Equity}$) drops or stays constant, the recovery is driven by real operational efficiency (Margins or Turnover).
* **Interest Drag:** If Interest Burden ($\text{EBT}/\text{EBIT}$) declines below $0.75$, debt service is heavily cannibalizing operating profits.

---

## 2. Altman Z-Score Financial Distress Modeling

For manufacturing and non-financial operating companies:
$$Z = 1.2 X_1 + 1.4 X_2 + 3.3 X_3 + 0.6 X_4 + 0.999 X_5$$

Where:
* $X_1 = \frac{\text{Working Capital}}{\text{Total Assets}}$ (Short-term balance sheet liquidity)
* $X_2 = \frac{\text{Retained Earnings}}{\text{Total Assets}}$ (Cumulative historical profitability)
* $X_3 = \frac{\text{EBIT}}{\text{Total Assets}}$ (Operating asset earning power)
* $X_4 = \frac{\text{Market Value of Equity}}{\text{Total Liabilities}}$ (Market solvency buffer)
* $X_5 = \frac{\text{Revenue}}{\text{Total Assets}}$ (Asset turnover efficiency)

### Z-Score Decision Thresholds:
* **$Z > 2.99$ — Safe Zone:** Negligible probability of financial distress within 24 months. Probability of failure $P_{\text{fail}} = 0.0\%$.
* **$1.81 \le Z \le 2.99$ — Grey Zone:** Moderate risk of distress. Perform liquidity stress-testing.
* **$Z < 1.81$ — Distress Zone:** High insolvency hazard. Model must activate the **Distress Truncation Engine** with $P_{\text{fail}} \ge 10\%$ and liquidation salvage proceeds.
