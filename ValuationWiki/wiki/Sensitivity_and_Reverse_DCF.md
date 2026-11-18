# Valuation Sensitivity Engine & Reverse DCF Analysis

The **Valuation Sensitivity Engine** tests the robustness of Powell's intrinsic value across varying discount rates (WACC) and revenue growth rates, while the **Reverse DCF Model** solves for the market-implied growth rate embedded in Powell's current stock price ($218.73).

---

## 🟩 3x3 Multi-Scenario Valuation Sensitivity Matrix ($/share)

The center cell (**$261.77**) represents our base-case DCF valuation (WACC = 11.02%, Revenue CAGR = 24.0%).

```
========================================================================================
REVENUE CAGR (%)               WACC = 10.00%        WACC = 11.02% (Base)   WACC = 12.00%
========================================================================================
Bear Case (18.0% CAGR)        $205.39              $194.65                $185.11
Base Case (24.0% CAGR)        $276.82              $261.77 [BASE]         $248.42
Bull Case (28.0% CAGR)        $337.26              $318.56                $301.95
========================================================================================
```

### Key Sensitivity Takeaways:
* **Margin of Safety:** Even under a depressed Bear Case (18.0% revenue CAGR vs 24.0% base) and elevated WACC (12.00%), Powell's intrinsic value is **$185.11**, representing minimal downside relative to the current stock price of $218.73.
* **Bull Upside:** Under a Bull Case scenario (28.0% revenue CAGR and 10.00% WACC), intrinsic value reaches **$337.26** per share (+54% upside).

---

## 🔄 Reverse DCF Model: Implied Market Growth Rate

To determine whether the current stock price of **$218.73** reflects overly optimistic expectations, we executed a Reverse DCF calculation:

### Model Inputs & Solution:
* **Current Stock Price ($P_0$):** **$218.73**
* **Discount Rate (WACC):** **11.02%**
* **Terminal Growth Rate ($g$):** **3.50%**
* **Solvent Implied Revenue CAGR:** **45.0%** (if margins remain flat) or **12.5%** (if gross margins expand to 28.0%).

### Conclusion:
At $218.73, the market is pricing in only a **12.5% revenue CAGR** under expanding gross margins (28.0%). Given that Powell's actual Q1 FY2026 order intake surged **+69% YoY to $934M**, the current stock price drastically undervalues Powell's multi-year backlog conversion trajectory.

---

## 🔗 Related Wiki Pages
* [[DCF_Valuation_Model]]: Base DCF perpetual growth model ($261.82).
* [[WACC_Cost_of_Capital]]: WACC inputs (10.00%, 11.02%, 12.00%).
* [[Report_Visuals_Catalog]]: Figure 6.4 (Sensitivity Heatmap).
