# Methodology: Econometric Driver Regressions & Liquidation Floors

---

## 1. Econometric Driver Regression & Operational Validation ($R^2$)

To prevent speculative top-line revenue estimates, candidate operational volume drivers are evaluated via Ordinary Least Squares (OLS) linear regression:
$$y_i = \beta_0 + \beta_1 x_i + \epsilon_i$$
$$R^2 = \left[\frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2 \sum_{i=1}^{n} (y_i - \bar{y})^2}}\right]^2$$

### Institutional Acceptance Criteria:
* **$R^2 \ge 0.85$:** High explanatory power. The operational driver (e.g., flight handling count, gross meals served, backlog burn) is accepted as the core engine for revenue projections.
* **$0.70 \le R^2 < 0.85$:** Moderate explanatory power. May be used only in a multi-variable blended driver.
* **$R^2 < 0.70$:** Rejected. Driver exhibits inadequate statistical linkage to financial realization.

---

## 2. Asset-by-Asset Liquidation Haircut Floor

Calculates the net cash realization in an orderly 12-month asset liquidation:

| Balance Sheet Item | High Recovery Rate | Low Recovery Rate | Institutional Rationale |
| :--- | :---: | :---: | :--- |
| **Cash & Cash Equivalents** | $100\%$ | $95\%$ | Minor currency conversion / legal escrow leakage |
| **Short-Term Marketable Securities** | $98\%$ | $90\%$ | Slight market volatility and bid-ask spread |
| **Trade Accounts Receivable** | $85\%$ | $70\%$ | Allowance for doubtful collections in insolvency |
| **Inventories (Finished Goods)** | $70\%$ | $50\%$ | Discounted clearance pricing and storage costs |
| **Inventories (Raw Materials)** | $50\%$ | $30\%$ | Scrap value and commodity discounting |
| **Property, Plant & Equipment (PP&E)** | $40\%$ | $25\%$ | Auction disposal haircuts on specialized machinery |
| **Right-of-Use (ROU) Lease Assets** | $30\%$ | $10\%$ | Sub-lease discount or termination penalties |
| **Intangible Assets & Patents** | $10\%$ | $0\%$ | Fire-sale patent auction value (Goodwill is $0\%$) |
| **Equity Investments in JVs / Associates**| $80\%$ | $60\%$ | Minority discount and illiquidity penalty |

### Liquidation Equity Floor Formula:
$$\text{Gross Liquidation Proceeds} = \sum (\text{Book Asset}_i \times \text{Recovery Rate}_i)$$
$$\text{Net Proceeds for Equity} = \text{Gross Proceeds} - \text{Wind-Down Legal Admin Fees (3-5%)} - \text{Total Liabilities & Debt}$$
$$\text{Liquidation Floor Per Share} = \frac{\text{Net Proceeds for Equity}}{\text{Diluted Shares}}$$
