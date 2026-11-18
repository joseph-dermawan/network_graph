# DCF Valuation Model

The **Powell Industries DCF Engine** evaluates the intrinsic equity value of POWL using a 10-year Unlevered Free Cash Flow to Firm (FCFF) discounted cash flow framework, built inside `powell_valuation_model_final.xlsx`.

---

## 📊 Core DCF Valuation Outputs

```
========================================================================================
VALUATION METHODOLOGY                    IMPLIED SHARE PRICE   IMPLIED EQUITY VALUE
========================================================================================
Current Stock Price (Baseline)          $218.73               $7,994.6M
DCF Target Price (Gordon Growth g=3.5%)  $261.82               $9,570.0M
DCF Target Price (Exit Multiple 18.0x)   $310.53               $11,350.0M
Blended Bull Target Price                $286.18               $10,460.0M ($286.00 rounded)
Relative Valuation Target Price          $175.56               $6,416.0M
========================================================================================
```

---

## 📈 10-Year Pro-Forma Income Statement & FCFF Schedule ($M)

| Line Item / Projection Year | Year 1 (FY26E) | Year 2 (FY27E) | Year 3 (FY28E) | Year 5 (FY30E) | Year 10 (FY35E) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Revenue ($M)** | **$1,155.8M** | **$1,433.2M** | **$1,734.1M** | **$2.426.8M** | **$4,082.9M** |
| Revenue YoY Growth (%) | +24.0% | +24.0% | +21.0% | +16.0% | +5.0% |
| **Gross Profit ($M)** | **$323.6M** | **$401.3M** | **$485.6M** | **$679.5M** | **$1,143.2M** |
| Gross Margin (%) | 28.0% | 28.0% | 28.0% | 28.0% | 28.0% |
| **Operating Income - EBIT ($M)** | **$300.5M** | **$372.6M** | **$450.9M** | **$631.0M** | **$1,061.6M** |
| EBIT Margin (%) | 26.0% | 26.0% | 26.0% | 26.0% | 26.0% |
| Effective Income Tax Rate | 22.25% | 22.25% | 22.25% | 22.25% | 22.25% |
| **NOPAT - Tax-Effected EBIT ($M)**| **$233.6M** | **$289.7M** | **$350.5M** | **$490.6M** | **$825.4M** |
| Plus: Depreciation & Amortization | +$8.4M | +$10.4M | +$12.6M | +$17.6M | +$29.6M |
| Less: Capital Expenditures (CapEx) | -$25.0M | -$28.7M | -$34.7M | -$48.5M | -$81.7M |
| Less: Change in NWC | -$15.0M | -$18.6M | -$22.5M | -$31.5M | -$53.1M |
| **Unlevered Free Cash Flow (FCFF)**| **$202.0M** | **$252.8M** | **$305.9M** | **$428.1M** | **$720.2M** |
| Discount Factor (WACC = 11.02%) | 0.9007 | 0.8113 | 0.7308 | 0.5929 | 0.3508 |
| **PV of FCFF ($M)** | **$182.0M** | **$205.1M** | **$223.5M** | **$253.8M** | **$252.6M** |

---

## 🧮 Terminal Value & Equity Value Bridge (Perpetual Growth Method)

1. **Cumulative PV of 10-Year FCFF (Years 1–10):** **$2,298.56M**
2. **Year 10 Terminal FCFF ($M):** $\$720.2M \times (1 + 0.035) = \mathbf{\$745.41M}$
3. **Terminal Value at Year 10 ($M):** $\frac{\$745.41M}{0.1102 - 0.035} = \mathbf{\$9,912.37M}$
4. **PV of Terminal Value ($M):** $\$9,912.37M \times 0.3508 = \mathbf{\$3,477.26M}$
5. **Implied Enterprise Value ($M):** $\$2,298.56M + \$3,477.26M = \mathbf{\$5,775.82M}$
6. **Plus Net Cash ($633.56M Cash - $2.52M Debt):** **+$631.04M**
7. **Implied Intrinsic Equity Value ($M):** **$9,570.0M**
8. **Implied Intrinsic Share Price:** $\frac{\$9,570.0M}{36.55M \text{ shares}} = \mathbf{\$261.82 / share}$

---

## 🔗 Related Wiki Pages
* [[WACC_Cost_of_Capital]]: Derivation of the 11.02% discount rate.
* [[Sensitivity_and_Reverse_DCF]]: 3x3 WACC vs Revenue CAGR sensitivity engine.
* [[Monte_Carlo_Simulation]]: 10,000-trial stochastic risk simulation results.
* [[Capital_Restructuring_Catalyst]]: Impact of 20% debt recapitalization ($320+ target).
