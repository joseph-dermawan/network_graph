# Quantitative Module: Macaulay Duration & The AI CapEx Duration Mismatch
**Module: AI-CAPEX-FW-05 | ERVIS Thematic Research Desk**
*Author: ERVIS Quantitative & Corporate Finance Desk*
*Date: October 2026*

---

## 1. Mathematical Foundations of Macaulay Duration

In fixed income and corporate equity valuation, **Macaulay Duration ($D_{\text{Mac}}$)** represents the weighted average time until expected cash flows are received, where each cash flow is weighted by its present value relative to total enterprise value:

$$D_{\text{Mac}} = \frac{\sum_{t=1}^{T} \frac{t \cdot \text{CF}_t}{(1 + r)^t}}{\sum_{t=1}^{T} \frac{\text{CF}_t}{(1 + r)^t}} = \sum_{t=1}^{T} t \cdot w_t$$

Where:
* $\text{CF}_t$ = Net cash flow generated at period $t$.
* $r$ = Discount rate (Weighted Average Cost of Capital, $\text{WACC}$).
* $w_t = \frac{\text{PV}(\text{CF}_t)}{\text{Total PV}}$ = The present value weight of cash flow at time $t$ ($\sum_{t=1}^{T} w_t = 1$).

### The First Derivative: Modified Duration ($D_{\text{Mod}}$)
Modified Duration measures the percentage sensitivity of present value to changes in the cost of capital:

$$D_{\text{Mod}} = \frac{D_{\text{Mac}}}{1 + r} = -\frac{1}{V} \frac{dV}{dr}$$

$$\frac{\Delta V}{V} \approx - D_{\text{Mod}} \cdot \Delta r$$

* **Higher Duration = Exponential Vulnerability**: A project or equity stream with a Macaulay duration of 14 years experiences an approximate **12.7% reduction in intrinsic present value for every 100 bps (1.0%) rise in WACC**.

---

## 2. The AI Infrastructure Duration Mismatch: The Core Asymmetry

The fundamental financial distortion in the 2024–2026 AI supercycle is a **structural duration mismatch** between the physical capital asset and the revenue payback stream:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE STRUCTURAL DURATION MISMATCH                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. THE CAPITAL EXPENDITURE (The Physical Asset)                                        │
│ • Cash Outflow: 100% upfront at t = 0 (Paid to Nvidia, TSMC, Quanta, Supermicro).       │
│ • Physical/Economic Asset Duration: 3.0 to 3.5 Years (Severe thermal/power decay).     │
│ • Accounting Amortization Life: 5.0 to 6.0 Years (Artificially prolonged).             │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 2. THE REVENUE & CASH FLOW (The Payback Horizon)                                       │
│ • Cash Inflow: Back-loaded subscription ARR, API token usage, Copilot seat licenses.   │
│ • Macaulay Duration of Cash Inflows: 7.5 to 12.0 Years!                               │
│ • The Vulnerability: Hardware dies in Year 3.5; cash flows are weighted in Year 8.     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Numerical Simulation: Standalone Investment vs. The Treadmill

Consider a **$10.0 Billion AI Cluster Deployment** (e.g., ~250,000 advanced GPUs with power/cooling).

### Project Parameters:
* **Initial Hardware Outlay ($t=0$)**: $-\$10.0\text{B}$
* **Gross Margin on AI Cloud Services**: $65\%$
* **Annual Operating Revenue Ramp**:
  * Year 1: $\$2.0\text{B}$ (Net CF: $+\$1.3\text{B}$)
  * Year 2: $\$3.5\text{B}$ (Net CF: $+\$2.28\text{B}$)
  * Year 3: $\$4.5\text{B}$ (Net CF: $+\$2.93\text{B}$)
  * Year 4: $\$5.0\text{B}$ (Net CF: $+\$3.25\text{B}$)
  * Year 5: $\$5.0\text{B}$ (Net CF: $+\$3.25\text{B}$)
  * Years 6–10: $\$5.0\text{B}$ annually (Net CF: $+\$3.25\text{B}$/yr)

---

### Case A: The "One-Time Railroad" Assumption (Zero Hardware Replacement)
Assuming the cluster runs for 10 years without replacement:

| Metric | Low Rate Regime ($r = 6.0\%$) | High Rate Regime ($r = 9.79\%$) (Oct 2026 WACC) | Impact of Rate Spike |
|---|---|---|---|
| **Undiscounted Cash Inflows** | $\$25.76\text{B}$ | $\$25.76\text{B}$ | — |
| **Net Present Value ($\text{NPV}$)** | **$+\$8.63\text{B}$** | **$+\$4.38\text{B}$** | **-49.2% NPV Destruction** |
| **Macaulay Duration of Inflows** | **5.42 Years** | **4.98 Years** | Cash flows shifted sooner |
| **Undiscounted Payback Period** | **3.84 Years** | **3.84 Years** | Breaks even near Year 4 |
| **Discounted Payback Period** | **4.68 Years** | **5.82 Years** | Payback pushed to Year 6 |

---

### Case B: The "Treadmill Reality" (Hardware Replaced Every 3.5 Years)
Because GPU clusters suffer physical degradation and energy efficiency obsolescence, the firm **must reinvest** at $t = 3.5$ and $t = 7.0$ to sustain the $\$5.0\text{B}$ annual revenue:

$$\text{Reinvestment Outlays}: -\$10.0\text{B at } t=0, \quad -\$10.0\text{B at } t=3.5, \quad -\$10.0\text{B at } t=7.0$$

| Year ($t$) | Revenue ($B) | Operating CF ($B) | Hardware CapEx ($B) | Net Free Cash Flow ($B) | PV at $r = 9.79\%$ |
|---|---|---|---|---|---|
| **0.0** | — | — | **-$10.00** | **-$10.00** | **-$10.00** |
| **1.0** | $2.00 | +$1.30 | $0.00 | +$1.30 | +$1.18 |
| **2.0** | $3.50 | +$2.28 | $0.00 | +$2.28 | +$1.89 |
| **3.0** | $4.50 | +$2.93 | $0.00 | +$2.93 | +$2.21 |
| **3.5** | — | — | **-$10.00 (Gen 2 Refresh)**| **-$10.00** | **-$7.19** |
| **4.0** | $5.00 | +$3.25 | $0.00 | +$3.25 | +$2.23 |
| **5.0** | $5.00 | +$3.25 | $0.00 | +$3.25 | +$2.03 |
| **6.0** | $5.00 | +$3.25 | $0.00 | +$3.25 | +$1.85 |
| **7.0** | $5.00 | +$3.25 | **-$10.00 (Gen 3 Refresh)**| **-$6.75** | **-$3.51** |
| **8.0** | $5.00 | +$3.25 | $0.00 | +$3.25 | +$1.54 |
| **9.0** | $5.00 | +$3.25 | $0.00 | +$3.25 | +$1.40 |
| **10.0**| $5.00 | +$3.25 | $0.00 | +$3.25 | +$1.28 |
| **TOTAL**| **$43.00** | **+$27.69** | **-$30.00** | **-$2.31** | **-$7.09B (NPV < 0!)** |

### 💥 The Critical Mathematical Takeaway:
* Under the **One-Time Buildout** fiction, the project appeared to generate **+$4.38B in NPV**.
* Under the **3.5-Year Treadmill Reality**, the project generates a **negative NPV of -$7.09 Billion**!
* Every time the project approaches cumulative cash breakeven (Year 3.8), **a mandatory $10B refresh CapEx resets the cumulative cash deficit**, keeping the enterprise in a permanent state of cash drain.

---

## 4. Sensitivity of Duration to Cost of Capital ($WACC$)

The table below demonstrates how the Net Present Value ($NPV$) of a 10-year tech cash flow stream decays as global interest rates and risk premiums shift:

| Discount Rate ($WACC$) | Baseline Scenario ($r = 5.0\%$) | Post-ZIRP Normal ($r = 7.5\%$) | Current Reality ($r = 9.79\%$) | Bear / Inflation Shock ($r = 12.0\%$) |
|---|---|---|---|---|
| **$PV$ of $10-Year Inflow Stream** | $\$21.28\text{B}$ | $\$17.84\text{B}$ | **$\$14.38\text{B}$** | $\$12.15\text{B}$ |
| **NPV (Railroad / No Refresh)** | +$11.28B | +$7.84B | **+$4.38B** | +$2.15B |
| **NPV (3.5-Year Treadmill)** | +$0.45B | -$3.72B | **-$7.09B** | -$9.85B |
| **Macaulay Duration ($D_{\text{Mac}}$)** | 5.62 Yrs | 5.25 Yrs | **4.98 Yrs** | 4.65 Yrs |
| **Modified Duration ($D_{\text{Mod}}$)** | 5.35 Yrs | 4.88 Yrs | **4.54 Yrs** | 4.15 Yrs |

### Core Strategic Implication for the Valuation Desk:
When the cost of capital ($WACC$) rises above **8.0%**, an asset with a **3.5-year replacement cadence** requires an incremental annual operating cash yield of **$>35\%$ of initial CapEx** just to achieve an NPV of zero. None of the current Big 4 Hyperscalers are generating an operating cash yield on AI hardware remotely close to 35%.
