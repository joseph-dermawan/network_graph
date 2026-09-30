#!/usr/bin/env python3
"""
ERVIS Deliverables Generator for AMD
Generates:
  1. ERVIS/projects/US_EQUITIES/AMD/reports/amd_equity_research_memo.md
  2. ERVIS/projects/US_EQUITIES/AMD/reports/dashboard.html
"""

import os
import json

PROJECT_DIR = "ERVIS/projects/US_EQUITIES/AMD"
REPORTS_DIR = f"{PROJECT_DIR}/reports"
MODELS_DIR = f"{PROJECT_DIR}/models"
REGRESSIONS_DIR = f"{PROJECT_DIR}/regressions"

with open(f"{MODELS_DIR}/valuation_engine_outputs.json") as f:
    val_out = json.load(f)

with open(f"{REGRESSIONS_DIR}/diagnostics_audit.json") as f:
    diag_out = json.load(f)

# ==============================================================================
# 1. INSTITUTIONAL EQUITY RESEARCH MEMORANDUM (amd_equity_research_memo.md)
# ==============================================================================

memo_content = """# INSTITUTIONAL EQUITY RESEARCH MEMORANDUM // AI CHALLENGERS CAMPAIGN #02

```
========================================================================================
TICKER:             AMD (NASDAQ)
COMPANY:            Advanced Micro Devices, Inc.
MARKET CAP:         $1,003.8 Billion ($1.004 Trillion)
CURRENT SPOT PRICE: $614.88
TARGET PRICE:       $201.44 (Downside: -67.2%)
RATING:             TRIM / TAKE PROFITS (TACTICAL ACCUMULATION ZONE: $140 - $185)
DATE:               2026-09-21
ANALYST CO-WORKER:  Senior Equity Research Associate (ERVIS v2.5-PRO)
PORTFOLIO DESK:     Lead Portfolio Manager / Research Director
========================================================================================
```

---

## 1. Executive Summary & The AI Multiple Disconnect

Advanced Micro Devices, Inc. (`AMD`) represents the quintessential challenger franchise in modern computing. Under Dr. Lisa Su's leadership, AMD executed one of the greatest operational turnarounds in technology history, expanding from near-insolvency in 2015 into an x86 server CPU juggernaut (EPYC server share reaching **34.5%**) and the only credible merchant alternative to NVIDIA in generative AI accelerators (Instinct **MI300X, MI325X, and MI350X**).

Over the trailing twelve months (TTM ended Q2 2026), AMD generated **$41.31 Billion in revenue** (+28.2% YoY), reported **$6.49 Billion in operating income**, and delivered **$8.40 Billion in Free Cash Flow**. Furthermore, our Gate 1 forensic accounting restatement reveals that true economic earnings power is substantially higher: adding back non-cash Xilinx purchase accounting amortization (+$2.21B) and capitalizing R&D (+$2.43B) restates normalized economic operating earnings (**Normalized EBIT_0**) to **$11.19 Billion**.

However, our institutional dual-engine valuation reveals a staggering valuation disconnect:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   THE VALUATION GAP: EXPECTATIONS VS FUNDAMENTALS                      │
├──────────────────────────────────────┬─────────────────────────────────────────────────┤
│ CURRENT MARKET SPOT PRICE            │ $614.88 ($1,003.8 Billion Market Cap)           │
│ 10-YEAR GINZU DCF INTRINSIC VALUE    │ $201.66 (-67.2% vs Spot)                        │
│ SUM-OF-THE-PARTS (SOTP) RELATIVE EV  │ $219.93 (-64.2% vs Spot)                        │
│ MONTE CARLO 10K P50 MEDIAN           │ $157.60 (Win Rate: 0.0% across 10,000 trials)   │
│ TRIANGULATED 12-MO TARGET PRICE      │ $201.44 (Downside: -67.2%)                      │
│ RECOMMENDATION                       │ TRIM / TAKE PROFITS (Harvest Peak AI Multiples) │
└──────────────────────────────────────┴─────────────────────────────────────────────────┘
```

### The Variant Perceptions Driving Our Underweight / Trim Thesis:

1. **The Break-Even AI Revenue Impossibility ($58.5B Required):** At $614.88 per share, AMD's enterprise value is pricing in **>$58.5 Billion in annual AI GPU revenue by 2029-2030** (~28.5% global merchant AI silicon volume share). In reality, AMD's AI GPU run-rate is currently ~$14.0 Billion (~7% merchant share). To achieve market pricing, AMD would have to take over 20 points of share from NVIDIA while simultaneously defeating the aggressive internal ASIC substitution programs of Google (TPU v5/v6), Amazon (Trainium 2), and Meta (MTIA).
2. **The ROCm Software Friction Tax:** While AMD offers superior hardware memory density (MI325X packs 256GB HBM3e vs NVIDIA H200's 141GB) and a ~48% upfront hardware discount, the Total Cost of Ownership (TCO) advantage is heavily eroded by ROCm software engineering overhead. Cloud hyperscalers must deploy large teams of internal compiler and kernel engineers to optimize non-standard models, wiping out 15-20% of the raw hardware price savings.
3. **Customer AI CapEx Payback Risk:** Hyperscalers face an estimated **3.8 to 4.5 year payback period** on AMD Instinct clusters, which still exceeds the **3.5-year hardware obsolescence window**. If hyperscalers moderate their CapEx growth from 45% down to 10-15%, merchant chip providers without CUDA software lock-in will suffer severe volume cancellations first.
4. **Portfolio Manager Directive:** We advise portfolio managers to **harvest capital gains and trim AMD exposures aggressively**. AMD is fundamentally an exceptional enterprise, but its current stock price has detached from cash-flow reality, demanding perfection across every product line for the next decade.

---

## 2. Business Segment Architecture & Competitive Moat

AMD operates four synergistic reporting units anchored by common IP (Zen CPU cores, RDNA/CDNA GPU architectures, XDNA NPU engines, and Xilinx FPGA logic blocks):

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ADVANCED MICRO DEVICES ($41.3B TTM REVENUE)                     │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│       DATA CENTER        │          CLIENT          │        GAMING & EMBEDDED         │
│   (~$25.5B Rev / 61.7%)  │   (~$10.2B Rev / 24.7%)  │    (~$5.6B Combined / 13.6%)     │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ - EPYC Server CPUs       │ - Ryzen Desktop / Mobile │ - Semi-Custom (PS5 / Xbox Series)│
│   (Rome, Milan, Genoa,   │ - Ryzen AI 300 Series    │ - Radeon Discrete RX GPUs        │
│    Turin / Zen 5)        │   (Strix Point / Zen 5)  │ - Xilinx Versal Adaptive SoCs    │
│ - Instinct AI GPUs       │ - 50+ NPU TOPS Edge AI   │ - Automotive ADAS & Industrial   │
│   (MI300X, MI325X,       │ - Commercial Enterprise  │ - Cyclical Bottoming Phase       │
│    MI350X, MI400 CDNA 4) │   PC Fleet Upgrades      │ - High Free Cash Flow Harvesting │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

### The Three Pillars of AMD's Competitive Moat:
1. **The x86 Duopoly Structural Arbitrage:** AMD is the only entity on Earth besides Intel licensed to build high-performance 64-bit x86 processors. As Intel stumbled through manufacturing delays and architectural inefficiencies, AMD systematically expanded EPYC's server unit share from 2% in 2017 to **34.5% in 2026** (representing >42% revenue share due to premium core-count ASPs). This generates an unassailable cash cow funding AI R&D.
2. **Chiplet Architecture & Advanced Packaging Leadership:** AMD pioneered multi-die chiplet packaging (Infinity Fabric, 3D V-Cache, TSMC SoIC). By disaggregating large dies into modular compute and I/O chiplets, AMD achieves dramatically higher silicon yields and lower die manufacturing costs than monolithic designs.
3. **The Anti-Monopoly Merchant Hedge:** Hyperscalers (Microsoft, Meta, Oracle Cloud) refuse to remain captive to NVIDIA's 75%+ gross margins and CUDA hegemony. AMD serves as the primary strategic hedge, receiving guaranteed hyperscaler architectural co-design commitments and off-take agreements to preserve supply-chain pricing leverage.

---

## 3. Forensic Accounting Normalization (Gate 1 Audit)

GAAP financial statements heavily distort AMD's true economic performance due to the accounting treatment of the **$49 Billion Xilinx acquisition (February 2022)** and the expensing of multi-year semiconductor R&D. Our Gate 1 forensic audit reconciles GAAP operating profit to true normalized cash earning power:

```
GATE 1 FORENSIC RECONCILIATION SCHEDULE ($ Millions):
----------------------------------------------------------------------------------------
Line Item                                Reported TTM     Forensic Adjustments  Normalized Base
----------------------------------------------------------------------------------------
Operating Income (GAAP Reported)         $6,488.0M        -                     $6,488.0M
(+) Xilinx Intangibles Amortization      -                +$2,214.0M            -
(+) Operating Lease Interest Adjustment  -                +$59.4M               -
(+) Expensed R&D Add-Back                -                +$9,394.0M            -
(-) 5-Year Straight-Line R&D Amort       -                -$6,963.6M            -
----------------------------------------------------------------------------------------
RESTATED NORMALIZED EBIT_0               $6,488.0M        +$4,703.8M            $11,191.8M
Effective Corporate Tax Rate             15.0%            -                     15.0%
RESTATED NORMALIZED NOPAT_0              $5,514.8M        -                     $9,513.0M
----------------------------------------------------------------------------------------
Capitalized Research Asset (5-Yr Net)    -                -                     $23,090.2M
Reported Capital Lease Liabilities       $1,050.0M        -                     $1,050.0M
Synthetic Operating Lease Debt (PV)      -                +$1,010.1M            $1,010.1M
Book Debt (Senior Notes & Term Debt)     $4,276.0M        -                     $4,276.0M
TOTAL ADJUSTED GROSS DEBT                $5,326.0M        -                     $5,286.1M
Less: Cash & Short-Term Investments      $13,111.0M       -                     $13,111.0M
----------------------------------------------------------------------------------------
TRUE NET CASH WAR CHEST                  -                -                     +$7,824.9M
========================================================================================
```

### Forensic Takeaways:
- **EBIT Restatement (+72.5%):** Reported GAAP operating profit of $6.49B understates AMD's cash generating power by $4.70B. Eliminating non-cash purchase accounting amortization ($2.21B) and capitalizing long-term R&D creates a **$23.1B intangible research asset**, adding $2.43B to normalized EBIT.
- **Flawless Net Cash Fortress:** Total cash and liquid investments stand at **$13.11 Billion** against total funded and synthetic lease debt of **$5.29 Billion**, yielding **+$7.82 Billion in pure net cash** (zero refinancing risk).

---

## 4. Econometric Driver Regressions & Financial Health (Gate 2 Audit)

All four core revenue driver regressions exceed the institutional $R^2 \ge 0.85$ statistical threshold:

```
GATE 2 ECONOMETRIC REGRESSION SUITE:
----------------------------------------------------------------------------------------
Driver 1: Hyperscaler AI CapEx ($B) vs AMD Instinct AI GPU Revenue ($M)
  * Formula:   Instinct Rev = $51.35 * (Hyperscaler CapEx) - $7,025.4
  * R-Squared: R² = 0.9957 [PASS - Strong Institutional Linkage]
  * Insight:   Every $1.0B in incremental Big 4 CapEx yields ~$51.4M in AMD GPU sales.

Driver 2: x86 Server CPU Market Share (%) vs AMD EPYC Revenue ($M)
  * Formula:   EPYC Rev = $373.19 * (Server CPU Share %) - $1,617.8
  * R-Squared: R² = 0.9763 [PASS - Direct Volume/ASP Expansion]
  * Insight:   Every 100 bps gain in x86 server share adds ~$373M to AMD operating revenue.

Driver 3: Client PC & AI PC Volume Index vs AMD Ryzen Revenue ($M)
  * Formula:   Ryzen Rev = $176.42 * (Volume Index) - $10,876.2
  * R-Squared: R² = 0.9732 [PASS - High Elasticity on Zen 5 Refresh]

Driver 4: Console & Embedded Cyclical Index vs Gaming/Embedded Revenue ($M)
  * Formula:   Gaming/Embed Rev = $147.28 * (Cycle Index) - $5,542.1
  * R-Squared: R² = 0.9807 [PASS - Cyclical Troughing Rebound]
----------------------------------------------------------------------------------------
```

### DuPont 5-Point ROE Diagnostic (5-Year Historical Evolution):
- **2022:** ROE = 2.41% (Distorted by initial Xilinx share dilution and purchase accounting).
- **2023:** ROE = 1.53% (PC inventory correction trough, operating margin collapsed to 1.77%).
- **2024:** ROE = 2.85% (Client recovery, initial MI300X volume ramp).
- **2025:** ROE = 6.88% (Operating margin doubled to 10.66%, asset turnover rose to 0.45x).
- **TTM 2026:** ROE = **9.57%** (Tax Burden 0.9147 x Interest Burden 1.0842 x Operating Margin 15.71% x Asset Turnover 0.4890x x Equity Multiplier 1.2565x).
- **Core Diagnosis:** ROE expansion is driven entirely by **real operational leverage (margins and turnover)** rather than financial leverage.

### Financial Health Audit Scores:
- **Altman Z-Score = 36.23 [ULTRA-SAFE ZONE (Z >> 2.99)]:** Driven by $19.4B working capital buffer, $1.0T market capitalization over liabilities, and zero structural debt maturity wall.
- **Piotroski F-Score = 8 / 9:** Near-perfect quality rating; cash flow from operations ($10.08B) significantly exceeds GAAP net income ($6.43B).
- **Beneish M-Score = -2.68 [SAFE ZONE]:** Comfortably below the -1.78 threshold; zero evidence of revenue manipulation or aggressive expense deferral.

---

## 5. Cost of Capital (WACC) & Synthetic Credit Synthesis (Gate 3 Audit)

```
GATE 3 COST OF CAPITAL SCHEDULE:
----------------------------------------------------------------------------------------
Parameter                               Value       Methodological Derivation
----------------------------------------------------------------------------------------
Risk-Free Rate (Rf 10-Yr US Treasury)   4.58%       US Treasury Benchmark Curve
Damodaran Equity Risk Premium (ERP)     4.33%       Implied S&P 500 DDM Spread
Peer Unlevered Beta (Beta_U)            1.30        Semiconductor Peer Decile (NVDA, AVGO, QCOM)
Market Value of Equity                  $1,003.8B   1,632.48M shares @ $614.88
Total Adjusted Debt                     $5.29B      $4.28B funded debt + $1.01B synthetic lease
Market Debt-to-Equity Ratio (D/E)       0.53%       Negligible leverage
Hamada Levered Beta (Beta_L)            1.306       1.30 * [1 + (1 - 0.15) * 0.0053]
Cost of Equity (Ke)                     10.23%      4.58% + (1.306 * 4.33%)
Moody's Synthetic Credit Rating         A2 / A      Coverage 85.5x, Net cash war chest
Default Credit Spread                   1.30%       130 bps over 10-Yr Treasury
Pre-Tax Cost of Debt (Kd)               5.88%       4.58% + 1.30%
After-Tax Cost of Debt                  5.00%       5.88% * (1 - 0.15)
Equity Weight / Debt Weight             99.47% / 0.53%
BASE WACC (Years 1 - 5)                 10.21%      Blended capital cost
TERMINAL WACC (Years 6 - 10+)           9.00%       Beta fades to 1.05 in mature phase
----------------------------------------------------------------------------------------
```

---

## 6. Valuation Engine & Scenario Triangulation (Gate 4 Audit)

### A. 10-Year Discrete Pro-Forma DCF Schedule (Damodaran Sales-to-Capital Engine)

We project AMD's financials across a 10-year discrete forecast horizon, linking reinvestment directly to incremental revenue expansion via a **Sales-to-Capital ratio of 3.20**:

```
10-YEAR PRO-FORMA DCF VALUATION SCHEDULE ($ Millions):
------------------------------------------------------------------------------------------------------------------------
Metric              FY27        FY28        FY29        FY30        FY31        FY32        FY33        FY34        FY35        FY36
------------------------------------------------------------------------------------------------------------------------
Revenue Growth      24.0%       20.0%       16.0%       12.0%       9.0%        7.0%        5.5%        4.5%        4.0%        3.8%
Revenue             $51,218.2   $61,461.8   $71,295.7   $79,851.2   $87,037.8   $93,130.5   $98,252.6   $102,674.0  $106,781.0  $110,838.6
Operating Margin    27.5%       29.0%       30.5%       31.5%       32.5%       32.8%       33.0%       33.0%       33.0%       33.0%
EBIT                $14,085.0   $17,823.9   $21,745.2   $25,153.1   $28,287.3   $30,546.8   $32,423.4   $33,882.4   $35,237.7   $36,576.7
Effective Tax Rate  15.0%       15.0%       15.0%       15.0%       15.0%       15.0%       15.0%       15.0%       15.0%       15.0%
NOPAT               $11,972.3   $15,150.3   $18,483.4   $21,380.2   $24,044.2   $25,964.8   $27,559.9   $28,800.1   $29,952.1   $31,090.2
Reinvestment        $3,097.9    $3,201.1    $3,073.1    $2,673.6    $2,245.8    $1,904.0    $1,600.7    $1,381.7    $1,283.4    $1,268.0
FCFF                $8,874.4    $11,949.2   $15,410.3   $18,706.6   $21,798.4   $24,060.8   $25,959.2   $27,418.4   $28,668.6   $29,822.2
Discount Rate       10.21%      10.07%      9.94%       9.80%       9.67%       9.54%       9.40%       9.27%       9.13%       9.00%
Discount Factor     0.9073      0.8243      0.7498      0.6828      0.6226      0.5684      0.5195      0.4754      0.4356      0.3997
PV of FCFF          $8,052.0    $9,850.1    $11,554.2   $12,773.5   $13,572.2   $13,675.3   $13,486.2   $13,035.7   $12,489.1   $11,918.7
------------------------------------------------------------------------------------------------------------------------
```

### B. Terminal Value & Equity Bridge:
- **Terminal Growth Rate ($g$):** 3.80% (Long-term global GDP proxy).
- **Challenger Moat ROIC Override:** **20.00%** (Acknowledges AMD's durable x86 duopoly and AI hardware challenger moat).
- **Terminal Reinvestment Rate:** $g / \text{ROIC}_{\text{terminal}} = 3.80\% / 20.0\% = 19.00\%$.
- **Terminal NOPAT:** $\$110,838.6\text{M} \times 1.038 \times 33.0\% \times 0.85 = \$32,271.7\text{M}$.
- **Terminal FCFF:** $\$32,271.7\text{M} \times (1 - 0.19) = \$26,140.1\text{M}$.
- **Terminal Value ($TV_{10}$):** $\$26,140.1\text{M} / (0.0900 - 0.0380) = \$502,693.4\text{M}$.
- **PV of Terminal Value:** $\$502,693.4\text{M} \times 0.3997 = \$200,904.5\text{M}$.
- **Enterprise Value (DCF):** PV of 10-Yr FCFFs ($120,407.0M) + PV of TV ($200,904.5M) = **$321,311.5M**.
- **Equity Bridge:** EV + True Net Cash ($7,824.9M) = **$329,136.4M**.
- **DCF Intrinsic Value Per Share:** $\$329,136.4\text{M} / 1,632.48\text{M shares} = \mathbf{\$201.66}$.

---

### C. Sum-of-the-Parts (SOTP) Divisional Multiples Valuation

```
SOTP DIVISIONAL BREAKDOWN ($ Millions):
---------------------------------------------------------------------------------------------------
Operating Segment          Run-Rate Rev   EBITDA Margin  EBITDA ($M)  Target Multiple  Segment EV
---------------------------------------------------------------------------------------------------
1. Data Center (EPYC & AI) $25,500.0M     44.0%          $11,220.0M   25.0x            $280,500.0M
2. Client (Ryzen & AI PC)  $10,200.0M     24.0%          $2,448.0M    16.0x            $39,168.0M
3. Gaming (Radeon/Console) $3,200.0M      18.0%          $576.0M      12.0x            $6,912.0M
4. Embedded (Xilinx FPGA)  $3,600.0M      38.0%          $1,368.0M    18.0x            $24,624.0M
---------------------------------------------------------------------------------------------------
TOTAL SOTP ENTERPRISE VALUE (EV)                                                       $351,204.0M
Plus: True Net Cash War Chest                                                          +$7,824.9M
TOTAL SOTP IMPLIED EQUITY VALUE                                                        $359,028.9M
SOTP INTRINSIC VALUE PER SHARE (USD)                                                   $219.93
---------------------------------------------------------------------------------------------------
```

---

### D. 10,000-Trial Monte Carlo Stochastic Risk Simulation

Running 10,000 random trials varying revenue growth, operating margins, discount rates, and terminal ROIC yields:
- **10th Percentile (P10 - Bear Case):** **$125.37**
- **50th Percentile (P50 - Base Median):** **$157.60**
- **90th Percentile (P90 - Bull Sky):** **$198.59**
- **Win Rate vs Spot Price ($614.88):** **0.00%** (In zero out of 10,000 trials does fundamental DCF cash flow justify the current market price).

### E. Liquidation Haircut Downside Floor
Applying institutional liquidation salvage factors (Cash 100%, Receivables 75%, Inventory 50%, Net PP&E 30%, Intangibles/Goodwill 5%) nets $25,892.7M in realizable assets against $17,240.0M in total liabilities, establishing an ultimate liquidation downside floor of **$5.30 per share**.

### F. Final Valuation Triangulation:
- 50% DCF Intrinsic Value ($201.66) + 35% SOTP Multiple Value ($219.93) + 15% Monte Carlo Median ($157.60) = **$201.44**.
- **12-Month Institutional Target Price:** **$201.44** (Implied Downside: **-67.2%**).

---

## 7. Gate 4B: Specialized AI CapEx Payout & Customer ROI Analysis

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE DUAL-SIDED AI HARDWARE CAPITAL CYCLE                        │
│                                                                                        │
│     [BIG 4 HYPERSCALERS]                                  [AMD INSTINCT SILICON]       │
│   MSFT, Meta, GOOGL, AMZN                                 Fabless TSMC N3/N4 + CoWoS   │
│                                                                                        │
│   Combined CapEx: $408.0B                                 TTM Revenue: $41.3B          │
│         │                                                       │                      │
│         ▼                                                       ▼                      │
│   [CAPEX PAYOUT RATIO (CPR): 3.43%]                             Physical CapEx: $1.68B │
│   $14.0B Paid for AMD AI GPUs                                   Annual R&D:     $9.39B │
│         │                                                       │                      │
│         ▼                                                       ▼                      │
│   Customer Payback: 3.8 to 4.5 Years                      Free Cash Flow: $8.40B       │
│   Hardware Useful Life: 3.5 Years                                                      │
│         │                                                                              │
│         ▼                                                                              │
│   ⚠️ OBSOLESCENCE DEFICIT: 3.6 to 12.0 Months (Severe Hardware Replacement Risk)       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. Internal Capital Metrics (Fabless Efficiency):
- **Physical CapEx Intensity:** AMD spent **$1,677M in CapEx (4.06% of revenue)**, reflecting an ultra-asset-light fabless model relying on TSMC foundry and packaging fabs.
- **R&D Intensity:** AMD invested **$9,394M in R&D (22.74% of revenue)**, committing substantial engineering resources to bridge the ROCm software gap.
- **FCF Conversion Rate:** Converted **83.36% of operating cash flow ($8.40B FCF / $10.08B CFO)** into pure cash.

### 2. The Customer Total Cost of Ownership (TCO) Equation:
AMD offers compelling raw silicon hardware advantages over NVIDIA:
- **Acquisition Cost:** An 8-GPU Instinct MI300X/MI325X HGX-equivalent server costs **~$140,000 - $160,000**, compared to **~$280,000 - $320,000** for an NVIDIA H100/H200 system (a **~48% hardware CapEx discount**).
- **Memory Density:** MI325X features **256GB of HBM3e (6.0 TB/s bandwidth)** vs H200's **141GB (4.8 TB/s)**. For large LLM inference (e.g. Llama 3.1 70B/405B), an entire model can be loaded into an 8-GPU MI325X node without cross-node network hop latency.
- **The ROCm Software Friction Penalty:** Despite hardware cost advantages, ROCm 6.2 introduces non-trivial operational friction:
  1. *Kernel Optimization Overhead:* Non-standard transformer architectures frequently require custom Triton/C++ kernel rewrites.
  2. *Hyperscaler Engineering Costs:* Major customers (Microsoft, Meta, Oracle) must assign dedicated engineering teams to maintain ROCm clusters, which adds an estimated **$35,000 - $50,000 per node in lifecycle software maintenance**, erasing 15-20% of the raw hardware savings.

### 3. Customer Payback & The Obsolescence Deficit:
- **CapEx Payout Ratio (CPR):** AMD absorbs **3.43% ($14.0B / $408B)** of hyperscaler CapEx, compared to NVIDIA's **45.34% ($185B / $408B)**.
- **Customer Payback Duration ($T_{\text{payback}}$):** Between **3.8 and 4.5 years**.
- **Hardware Useful Life ($L_{\text{useful}}$):** **3.5 years** before Blackwell, Rubin, and MI350/MI400 make existing nodes economically uncompetitive.
- **The Obsolescence Deficit:** The customer experiences a **3.6 to 12.0 month deficit window** where hardware reaches obsolescence before generating cumulative free cash flow exceeding initial capital outlay.

### 4. Reverse DCF: Break-Even AI Revenue Analysis:
To justify AMD's current **$614.88 market price**, the market is implicitly assuming:
- AMD's AI GPU revenue must scale from $14.0B today to **>$58.5 Billion annually by 2029-2030**.
- AMD's global merchant AI accelerator market share must surge from **7.0% to 28.5%**.
- Operating margins must sustainably expand to **38.0%+**.

**Why This Expectation is Fatally Flawed:**
1. NVIDIA's Blackwell and Rubin architectures defend high-end training clusters with NVLink 5 and full-stack software lock-in.
2. Hyperscalers are aggressively accelerating **custom internal ASICs** (Google TPU v6 Trillium, AWS Trainium 2, Meta MTIA 2) for their own first-party workloads rather than switching to AMD.
3. Therefore, AMD's addressable merchant AI market share is fundamentally bounded between **10% and 15%**, mathematically capping long-term value well below $250.

---

## 8. Catalyst Calendar, Scenario Analysis & Investment Directive

```
CATALYST CALENDAR (NEXT 6 - 12 MONTHS):
----------------------------------------------------------------------------------------
Date / Event               Catalyst Description                      Valuation Impact
----------------------------------------------------------------------------------------
Q3 2026 Earnings           Instinct MI325X volume ramp confirmation  Short-term sentiment
Q4 2026 Hyperscaler Budget 2027 Cloud CapEx guidance announcements  Key indicator for AI cycle
Q1 2027 MI350X Launch      3nm CDNA 4 silicon debut vs Blackwell     Execution milestone
H1 2027 Enterprise Zen 5   Turin server refresh enterprise penetration Sustains base earnings
----------------------------------------------------------------------------------------
```

### Scenario Sensitivity Matrix:
- **Bull Case ($285.00 / -53.6%):** AMD captures 18% AI GPU market share ($32B revenue), EPYC server CPU share expands to 42%, ROCm friction drops to zero. Multiple: 28x EV/EBITDA.
- **Base Case ($201.44 / -67.2%):** AMD captures 11% AI GPU market share ($18B revenue), EPYC share plateaus at 36%, Client Zen 5 remains stable, normal semi cyclicality resumes. Target multiple: 22x EV/EBITDA.
- **Bear Case ($135.00 / -78.0%):** Hyperscaler CapEx cuts by 20%, CSP internal ASICs cannibalize merchant inference, Intel Xeon 6 clawback in enterprise servers. Multiple: 15x EV/EBITDA.

### Portfolio Desk Action:
```
========================================================================================
RECOMMENDATION:      TRIM / TAKE PROFITS (-67.2% TO INTRINSIC VALUE)
ACTIONABLE EXECUTION:Harvest gains; reallocate capital into underpriced infrastructure
TACTICAL ACCUM ZONE: $140.00 - $185.00 (Wait for cyclical sentiment overshoot)
RISK-REWARD ASYMMETRY:Downside -67% vs Upside under peak bull case -53% (Unfavorable)
========================================================================================
```
"""

with open(f"{REPORTS_DIR}/amd_equity_research_memo.md", "w") as f:
    f.write(memo_content)

print(f"  * Generated Institutional Equity Research Memo: {REPORTS_DIR}/amd_equity_research_memo.md")

# ==============================================================================
# 2. INTERACTIVE BLOOMBERG HTML DASHBOARD (dashboard.html)
# ==============================================================================

dashboard_html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERVIS :: Advanced Micro Devices, Inc. (NASDAQ: AMD) Valuation Dashboard</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        serif: ['Newsreader', 'Georgia', 'serif'],
                        mono: ['"JetBrains Mono"', 'monospace']
                    }}
                }}
            }}
        }}
    </script>
    
    <style>
        body {{
            background-color: #09090b;
            color: #d4d4d8;
            font-family: 'JetBrains Mono', monospace;
        }}
        .tab-btn.active {{
            border-bottom-color: #f59e0b;
            color: #fbbf24;
            background-color: rgba(24, 24, 27, 0.8);
        }}
        .bg-terminal-card {{
            background-color: #111215;
            border: 1px solid #27272a;
        }}
        .table-terminal th {{
            background-color: #18181b;
            border-bottom: 1px solid #3f3f46;
            color: #a1a1aa;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            padding: 8px 12px;
        }}
        .table-terminal td {{
            border-bottom: 1px solid #27272a;
            padding: 8px 12px;
            font-size: 11px;
        }}
    </style>
</head>
<body class="min-h-screen text-xs antialiased selection:bg-amber-950 selection:text-amber-200">

    <!-- Top Command Header -->
    <header class="border-b border-neutral-800 bg-[#0c0d0e] sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-3 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-center space-x-3">
                <span class="px-2 py-0.5 border border-amber-500/40 bg-amber-950/20 text-amber-400 font-mono text-[11px] font-bold tracking-wider">
                    ERVIS TERMINAL v2.5
                </span>
                <span class="text-neutral-500 font-mono text-xs">/</span>
                <h1 class="text-sm font-serif font-semibold text-neutral-100 tracking-wide">
                    Advanced Micro Devices, Inc. (NASDAQ: AMD) :: Institutional Valuation Dossier
                </h1>
                <span class="px-2 py-0.5 border border-amber-900/60 bg-amber-950/30 text-amber-300 font-mono text-[10px] font-bold">
                    [AI CHALLENGERS #02]
                </span>
            </div>
            
            <div class="flex items-center space-x-4 text-xs font-mono">
                <span class="text-neutral-400">SPOT: <strong class="text-neutral-100 font-bold">${val_out['spot_price_usd']:.2f}</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">INTRINSIC: <strong class="text-amber-400 font-bold">${val_out['final_triangulation']['target_price_usd']:.2f}</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="px-2 py-0.5 border border-rose-800 bg-rose-950/40 text-rose-400 font-bold">
                    {val_out['final_triangulation']['rating']}
                </span>
            </div>
        </div>

        <!-- Terminal Command Navigation Bar -->
        <div class="max-w-7xl mx-auto px-6 border-t border-neutral-800 flex space-x-1 overflow-x-auto text-xs font-mono">
            <button id="btn-tab-overview" onclick="switchTab('tab-overview')" class="tab-btn active px-3.5 py-2 border-b-2 border-amber-500 text-amber-400 bg-neutral-900/60 transition-colors whitespace-nowrap">
                [01] EXECUTIVE THESIS & CAPEX ROI AUDIT
            </button>
            <button id="btn-tab-sotp" onclick="switchTab('tab-sotp')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [02] SUM-OF-THE-PARTS (SOTP)
            </button>
            <button id="btn-tab-dcf" onclick="switchTab('tab-dcf')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [03] 10-YR GINZU DCF SCHEDULE
            </button>
            <button id="btn-tab-scenarios" onclick="switchTab('tab-scenarios')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [04] SCENARIOS & 10K MONTE CARLO
            </button>
            <button id="btn-tab-diagnostics" onclick="switchTab('tab-diagnostics')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [05] FORENSIC NORMALIZATION & HEALTH
            </button>
        </div>
    </header>

    <!-- Main Content Body -->
    <main class="max-w-7xl mx-auto px-6 py-6 space-y-6">

        <!-- TAB 1: EXECUTIVE THESIS & CAPEX ROI AUDIT -->
        <div id="tab-overview" class="tab-content space-y-6">
            <div class="p-3 bg-amber-950/20 border border-amber-900/60 text-amber-300 flex items-center justify-between text-xs">
                <span>[VALUATION VERDICT] AMD is an extraordinary computing turnaround franchise, boasting $11.19B in restated normalized EBIT and 34.5% x86 server share. However, at $614.88 ($1.004T market cap), the stock is discounting >$58.5B in annual AI GPU revenue (~28.5% global share), whereas actual run-rate is $14.0B (7% share). Intrinsic DCF value is $201.66; SOTP relative value is $219.93. Final target: $201.44 (-67.2% downside).</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-amber-800 px-1.5 py-0.5">Tactical Alert</span>
            </div>

            <!-- Top Metric Cards -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-terminal-card p-4">
                    <div class="text-neutral-500 uppercase text-[10px] tracking-wider mb-1">Target Intrinsic Value</div>
                    <div class="text-2xl font-bold text-amber-400">${val_out['final_triangulation']['target_price_usd']:.2f}</div>
                    <div class="text-[10px] text-rose-400 mt-1">{val_out['final_triangulation']['upside_percent']:+.1f}% vs Spot ${val_out['spot_price_usd']:.2f}</div>
                </div>
                <div class="bg-terminal-card p-4">
                    <div class="text-neutral-500 uppercase text-[10px] tracking-wider mb-1">Normalized EBIT_0</div>
                    <div class="text-2xl font-bold text-neutral-100">$11,191.8M</div>
                    <div class="text-[10px] text-emerald-400 mt-1">+72.5% vs Reported ($6.49B)</div>
                </div>
                <div class="bg-terminal-card p-4">
                    <div class="text-neutral-500 uppercase text-[10px] tracking-wider mb-1">Base WACC / Term WACC</div>
                    <div class="text-2xl font-bold text-neutral-100">{val_out['wacc_schedule']['base_wacc']*100:.2f}% <span class="text-xs text-neutral-500">/ 9.0%</span></div>
                    <div class="text-[10px] text-neutral-400 mt-1">Ke: {val_out['wacc_schedule']['cost_of_equity']*100:.2f}% | Beta: {val_out['wacc_schedule']['hamada_beta']:.3f}</div>
                </div>
                <div class="bg-terminal-card p-4">
                    <div class="text-neutral-500 uppercase text-[10px] tracking-wider mb-1">Net Cash Fortress</div>
                    <div class="text-2xl font-bold text-emerald-400">+${val_out['dcf_schedule']['equity_bridge_net_cash_m']:,.1f}M</div>
                    <div class="text-[10px] text-neutral-400 mt-1">Cash $13.1B vs Debt $5.3B</div>
                </div>
            </div>

            <!-- Gate 4B AI CapEx Payout Audit Section -->
            <div class="bg-terminal-card p-5 space-y-4">
                <div class="flex items-center justify-between border-b border-neutral-800 pb-3">
                    <h2 class="text-sm font-bold text-neutral-100 uppercase tracking-wider flex items-center gap-2">
                        <span class="text-amber-500">GATE 4B AUDIT:</span> AI CapEx Payout, Customer Payback & ROI Analysis
                    </h2>
                    <span class="text-[10px] text-neutral-500">Hyperscaler CapEx Pool: $408.0B</span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="p-3 bg-neutral-900/80 border border-neutral-800">
                        <div class="text-neutral-400 text-[11px] font-bold mb-2">[01] CAPEX PAYOUT RATIO (CPR)</div>
                        <div class="text-xl font-bold text-amber-400">{val_out['ai_capex_audit']['customer_payback_and_roi']['amd_capex_payout_ratio_pct']}%</div>
                        <p class="text-[10px] text-neutral-400 mt-2">
                            AMD's Data Center GPU revenue ($14.0B run-rate) absorbs only 3.43% of total hyperscaler CapEx ($408B), compared to NVIDIA's 45.34% monopoly tax ($185B).
                        </p>
                    </div>
                    <div class="p-3 bg-neutral-900/80 border border-neutral-800">
                        <div class="text-neutral-400 text-[11px] font-bold mb-2">[02] CUSTOMER PAYBACK PERIOD</div>
                        <div class="text-xl font-bold text-amber-400">3.8 to 4.5 Years</div>
                        <p class="text-[10px] text-rose-400 mt-2">
                            ⚠️ OBSOLESCENCE DEFICIT: Exceeds 3.5-year hardware useful life by 3.6 to 12.0 months. Servers reach technical obsolescence before full investment recovery.
                        </p>
                    </div>
                    <div class="p-3 bg-neutral-900/80 border border-neutral-800">
                        <div class="text-neutral-400 text-[11px] font-bold mb-2">[03] BREAK-EVEN AI REVENUE</div>
                        <div class="text-xl font-bold text-rose-400">$58.5 Billion</div>
                        <p class="text-[10px] text-neutral-400 mt-2">
                            Spot price $614.88 requires AMD capturing 28.5% global merchant AI share by 2029 (vs 7.0% today), an implausible assumption against CUDA and custom ASICs.
                        </p>
                    </div>
                </div>

                <!-- TCO Comparison Matrix -->
                <div class="overflow-x-auto">
                    <table class="w-full table-terminal">
                        <thead>
                            <tr>
                                <th>TCO / Silicon Dimension</th>
                                <th>AMD Instinct MI325X / MI350X</th>
                                <th>NVIDIA H200 / B200 HGX</th>
                                <th>Economic Evaluation & Friction Assessment</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="font-bold text-neutral-200">8-GPU Cluster Acquisition Cost</td>
                                <td class="text-emerald-400 font-bold">$140,000 - $160,000</td>
                                <td class="text-neutral-300 font-bold">$280,000 - $320,000</td>
                                <td class="text-emerald-400 font-medium">AMD provides a ~48% upfront hardware capital expenditure discount</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Memory Capacity & Bandwidth</td>
                                <td class="text-emerald-400 font-bold">256 GB HBM3e (6.0 TB/s)</td>
                                <td class="text-neutral-300">141 GB HBM3e (4.8 TB/s)</td>
                                <td class="text-emerald-400 font-medium">+81.6% memory allows full Llama 3.1 70B/405B inference on fewer nodes</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Software Ecosystem & Porting</td>
                                <td class="text-amber-400">ROCm 6.2 (PyTorch/vLLM native)</td>
                                <td class="text-emerald-400">CUDA 12.x (18-year optimized ecosystem)</td>
                                <td class="text-rose-400 font-medium">ROCm requires dedicated kernel engineering teams; erodes 15-20% of hardware savings</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Internal ASIC Substitution Risk</td>
                                <td class="text-rose-400 font-bold">High (CSP internal displacement)</td>
                                <td class="text-amber-400 font-bold">Moderate (Defended by NVLink)</td>
                                <td class="text-neutral-400">Hyperscalers prefer internal ASICs (TPU, Trainium, MTIA) for 1st-party inference</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 2: SUM-OF-THE-PARTS (SOTP) -->
        <div id="tab-sotp" class="tab-content space-y-6 hidden">
            <div class="bg-terminal-card p-5 space-y-4">
                <div class="flex items-center justify-between border-b border-neutral-800 pb-3">
                    <h2 class="text-sm font-bold text-neutral-100 uppercase tracking-wider">
                        Sum-of-the-Parts (SOTP) Divisional Multiples Valuation
                    </h2>
                    <span class="text-amber-400 font-bold">Implied SOTP Value: ${val_out['sotp_divisional']['sotp_intrinsic_usd']:.2f}</span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full table-terminal">
                        <thead>
                            <tr>
                                <th>Operating Reporting Segment</th>
                                <th>Revenue Run-Rate ($M)</th>
                                <th>EBITDA Margin</th>
                                <th>EBITDA ($M)</th>
                                <th>Target Multiple</th>
                                <th>Segment EV ($M)</th>
                                <th>Peer Valuation Anchor</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="font-bold text-neutral-200">Data Center (EPYC & Instinct AI)</td>
                                <td>$25,500.0M</td>
                                <td>44.0%</td>
                                <td>$11,220.0M</td>
                                <td class="text-amber-400 font-bold">25.0x</td>
                                <td class="font-bold text-neutral-100">${val_out['sotp_divisional']['data_center_ev_m']:,.1f}M</td>
                                <td class="text-neutral-400">Premium AI / Server silicon multiple (NVDA, AVGO)</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Client PC (Ryzen & AI PC APUs)</td>
                                <td>$10,200.0M</td>
                                <td>24.0%</td>
                                <td>$2,448.0M</td>
                                <td class="text-amber-400 font-bold">16.0x</td>
                                <td class="font-bold text-neutral-100">${val_out['sotp_divisional']['client_pc_ev_m']:,.1f}M</td>
                                <td class="text-neutral-400">Client PC processor peer multiple (INTC client, QCOM)</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Gaming (Radeon & Console SoCs)</td>
                                <td>$3,200.0M</td>
                                <td>18.0%</td>
                                <td>$576.0M</td>
                                <td class="text-amber-400 font-bold">12.0x</td>
                                <td class="font-bold text-neutral-100">${val_out['sotp_divisional']['gaming_ev_m']:,.1f}M</td>
                                <td class="text-neutral-400">Consumer hardware & discrete GPU multiple (Sony, NVDA Gaming)</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Embedded (Xilinx FPGAs & SoCs)</td>
                                <td>$3,600.0M</td>
                                <td>38.0%</td>
                                <td>$1,368.0M</td>
                                <td class="text-amber-400 font-bold">18.0x</td>
                                <td class="font-bold text-neutral-100">${val_out['sotp_divisional']['embedded_xilinx_ev_m']:,.1f}M</td>
                                <td class="text-neutral-400">Industrial & automotive FPGA multiple (ADI, MCHP)</td>
                            </tr>
                            <tr class="bg-neutral-900/80 font-bold text-neutral-100">
                                <td>TOTAL SOTP ENTERPRISE VALUE (EV)</td>
                                <td>$42,500.0M</td>
                                <td>36.7%</td>
                                <td>$15,612.0M</td>
                                <td>22.5x</td>
                                <td class="text-amber-400">${val_out['sotp_divisional']['total_sotp_ev_m']:,.1f}M</td>
                                <td>Consolidated Multi-Segment Aggregate</td>
                            </tr>
                            <tr class="bg-neutral-950 font-bold text-emerald-400">
                                <td colspan="5">Plus: True Net Cash War Chest (Cash $13.1B minus Debt $5.3B)</td>
                                <td>+${val_out['dcf_schedule']['equity_bridge_net_cash_m']:,.1f}M</td>
                                <td>Balance Sheet Bridge</td>
                            </tr>
                            <tr class="bg-amber-950/30 font-bold text-amber-400 text-sm">
                                <td colspan="5">SOTP IMPLIED EQUITY VALUE / VALUE PER SHARE</td>
                                <td class="text-base">${val_out['sotp_divisional']['sotp_intrinsic_usd']:.2f}</td>
                                <td>Diluted Shares: 1,632.48M</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: 10-YR GINZU DCF SCHEDULE -->
        <div id="tab-dcf" class="tab-content space-y-6 hidden">
            <div class="bg-terminal-card p-5 space-y-4">
                <div class="flex items-center justify-between border-b border-neutral-800 pb-3">
                    <h2 class="text-sm font-bold text-neutral-100 uppercase tracking-wider">
                        Damodaran Ginzu 10-Year Discrete FCFF Schedule
                    </h2>
                    <span class="text-amber-400 font-bold">DCF Intrinsic Value: ${val_out['dcf_schedule']['dcf_intrinsic_value_usd']:.2f}</span>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs mb-4">
                    <div class="p-2.5 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 block text-[10px]">PV of 10-Yr FCFFs</span>
                        <strong class="text-neutral-100 text-sm">${val_out['dcf_schedule']['pv_10yr_fcff_m']:,.1f}M</strong>
                    </div>
                    <div class="p-2.5 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 block text-[10px]">PV of Terminal Value</span>
                        <strong class="text-neutral-100 text-sm">${val_out['dcf_schedule']['pv_terminal_value_m']:,.1f}M</strong>
                    </div>
                    <div class="p-2.5 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 block text-[10px]">Enterprise Value (DCF)</span>
                        <strong class="text-neutral-100 text-sm">${val_out['dcf_schedule']['enterprise_value_m']:,.1f}M</strong>
                    </div>
                    <div class="p-2.5 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 block text-[10px]">Terminal ROIC Moat Constraint</span>
                        <strong class="text-amber-400 text-sm">20.00% (Reinv 19.0%)</strong>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full table-terminal">
                        <thead>
                            <tr>
                                <th>Schedule Metric ($M)</th>
                                <th>FY27</th>
                                <th>FY28</th>
                                <th>FY29</th>
                                <th>FY30</th>
                                <th>FY31</th>
                                <th>FY32</th>
                                <th>FY33</th>
                                <th>FY34</th>
                                <th>FY35</th>
                                <th>FY36</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="font-bold text-neutral-200">Revenue Growth</td>
                                <td>24.0%</td><td>20.0%</td><td>16.0%</td><td>12.0%</td><td>9.0%</td><td>7.0%</td><td>5.5%</td><td>4.5%</td><td>4.0%</td><td>3.8%</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Total Revenue</td>
                                <td>$51,218</td><td>$61,462</td><td>$71,296</td><td>$79,851</td><td>$87,038</td><td>$93,131</td><td>$98,253</td><td>$102,674</td><td>$106,781</td><td>$110,839</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Operating Margin</td>
                                <td>27.5%</td><td>29.0%</td><td>30.5%</td><td>31.5%</td><td>32.5%</td><td>32.8%</td><td>33.0%</td><td>33.0%</td><td>33.0%</td><td>33.0%</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">NOPAT (t=15%)</td>
                                <td>$11,972</td><td>$15,150</td><td>$18,483</td><td>$21,380</td><td>$24,044</td><td>$25,965</td><td>$27,560</td><td>$28,800</td><td>$29,952</td><td>$31,090</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Reinvestment (S/C=3.2)</td>
                                <td>$3,098</td><td>$3,201</td><td>$3,073</td><td>$2,674</td><td>$2,246</td><td>$1,904</td><td>$1,601</td><td>$1,382</td><td>$1,283</td><td>$1,268</td>
                            </tr>
                            <tr class="bg-neutral-900/60 font-bold text-emerald-400">
                                <td>Free Cash Flow (FCFF)</td>
                                <td>$8,874</td><td>$11,949</td><td>$15,410</td><td>$18,707</td><td>$21,798</td><td>$24,061</td><td>$25,959</td><td>$27,418</td><td>$28,669</td><td>$29,822</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">WACC Discount Rate</td>
                                <td>10.21%</td><td>10.07%</td><td>9.94%</td><td>9.80%</td><td>9.67%</td><td>9.54%</td><td>9.40%</td><td>9.27%</td><td>9.13%</td><td>9.00%</td>
                            </tr>
                            <tr class="bg-amber-950/20 font-bold text-amber-400">
                                <td>Present Value of FCFF</td>
                                <td>$8,052</td><td>$9,850</td><td>$11,554</td><td>$12,773</td><td>$13,572</td><td>$13,675</td><td>$13,486</td><td>$13,036</td><td>$12,489</td><td>$11,919</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 4: SCENARIOS & 10K MONTE CARLO -->
        <div id="tab-scenarios" class="tab-content space-y-6 hidden">
            <div class="bg-terminal-card p-5 space-y-4">
                <div class="flex items-center justify-between border-b border-neutral-800 pb-3">
                    <h2 class="text-sm font-bold text-neutral-100 uppercase tracking-wider">
                        10,000-Trial Monte Carlo Stochastic Risk Simulation
                    </h2>
                    <span class="text-rose-400 font-bold">Win Rate vs Spot: {val_out['monte_carlo_10k']['win_rate_percent']:.1f}%</span>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
                    <div class="p-3 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 block text-[10px]">10th Percentile (P10)</span>
                        <strong class="text-rose-400 text-xl font-bold">${val_out['monte_carlo_10k']['p10_usd']:.2f}</strong>
                        <p class="text-[10px] text-neutral-500 mt-1">Severe hyperscaler capex pause</p>
                    </div>
                    <div class="p-3 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 block text-[10px]">Median (P50 Base)</span>
                        <strong class="text-amber-400 text-xl font-bold">${val_out['monte_carlo_10k']['median_usd']:.2f}</strong>
                        <p class="text-[10px] text-neutral-500 mt-1">Expected institutional outcome</p>
                    </div>
                    <div class="p-3 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 block text-[10px]">90th Percentile (P90)</span>
                        <strong class="text-emerald-400 text-xl font-bold">${val_out['monte_carlo_10k']['p90_usd']:.2f}</strong>
                        <p class="text-[10px] text-neutral-500 mt-1">Aggressive 15%+ GPU share</p>
                    </div>
                    <div class="p-3 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 block text-[10px]">Liquidation Haircut Floor</span>
                        <strong class="text-neutral-400 text-xl font-bold">${val_out['liquidation_floor_usd']:.2f}</strong>
                        <p class="text-[10px] text-neutral-500 mt-1">Tangible balance sheet recovery</p>
                    </div>
                </div>

                <!-- Scenario Triangulation Table -->
                <div class="overflow-x-auto mt-4">
                    <table class="w-full table-terminal">
                        <thead>
                            <tr>
                                <th>Valuation Scenario</th>
                                <th>Probability</th>
                                <th>Key Operational Assumptions</th>
                                <th>Implied Value</th>
                                <th>Variance vs Spot ($614.88)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="font-bold text-emerald-400">Bull Sky Case</td>
                                <td>20%</td>
                                <td>AI GPU share reaches 18% ($32B rev); EPYC share hits 42%; Margins expand to 38%</td>
                                <td class="font-bold text-neutral-100">$285.00</td>
                                <td class="text-rose-400 font-bold">-53.6%</td>
                            </tr>
                            <tr class="bg-neutral-900/60">
                                <td class="font-bold text-amber-400">Base Institutional Case</td>
                                <td>60%</td>
                                <td>AI GPU share captures 11% ($18B rev); EPYC plateaus at 36%; Long-term margin 33%</td>
                                <td class="font-bold text-amber-400">$201.44</td>
                                <td class="text-rose-400 font-bold">-67.2%</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-rose-400">Bear Cyclical Shock</td>
                                <td>20%</td>
                                <td>Hyperscalers pause CapEx by 20%; CSP internal ASICs substitute inference; Margin 25%</td>
                                <td class="font-bold text-neutral-100">$135.00</td>
                                <td class="text-rose-400 font-bold">-78.0%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 5: FORENSIC NORMALIZATION & HEALTH -->
        <div id="tab-diagnostics" class="tab-content space-y-6 hidden">
            <div class="bg-terminal-card p-5 space-y-4">
                <div class="flex items-center justify-between border-b border-neutral-800 pb-3">
                    <h2 class="text-sm font-bold text-neutral-100 uppercase tracking-wider">
                        Forensic Accounting Normalization & Financial Health Audit
                    </h2>
                    <span class="text-emerald-400 font-bold">Altman Z: {diag_out['altman_z']['altman_z_score']:.2f} | Piotroski: {diag_out['piotroski_f_score']}/9</span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full table-terminal">
                        <thead>
                            <tr>
                                <th>Forensic Normalization Adjustment</th>
                                <th>Reported GAAP ($M)</th>
                                <th>Audit Adjustment ($M)</th>
                                <th>Normalized Base ($M)</th>
                                <th>Methodological Rationale</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="font-bold text-neutral-200">Operating Income</td>
                                <td>$6,488.0M</td>
                                <td>-</td>
                                <td>$6,488.0M</td>
                                <td class="text-neutral-400">Reported GAAP operating profit (TTM ended Q2 2026)</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Xilinx Intangibles Amortization Add-Back</td>
                                <td>$0.0M</td>
                                <td class="text-emerald-400 font-bold">+$2,214.0M</td>
                                <td>$2,214.0M</td>
                                <td class="text-neutral-400">Reverses non-cash purchase accounting write-offs from $49B Xilinx acquisition</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">5-Year Straight-Line R&D Capitalization</td>
                                <td>$0.0M</td>
                                <td class="text-emerald-400 font-bold">+$2,430.4M</td>
                                <td>$2,430.4M</td>
                                <td class="text-neutral-400">Converts R&D spend ($9.39B) into a $23.09B amortizable capital asset</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">Operating Lease Synthetic Interest</td>
                                <td>$0.0M</td>
                                <td class="text-emerald-400 font-bold">+$59.4M</td>
                                <td>$59.4M</td>
                                <td class="text-neutral-400">Synthetic interest on $1,010.1M discounted lease debt @ 5.88% Kd</td>
                            </tr>
                            <tr class="bg-amber-950/20 font-bold text-amber-400 text-sm">
                                <td>RESTATED NORMALIZED EBIT_0</td>
                                <td>$6,488.0M</td>
                                <td>+$4,703.8M</td>
                                <td>$11,191.8M</td>
                                <td>True normalized cash earning power (+72.5% vs GAAP)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- DuPont 5-Point ROE Evolution -->
                <div class="overflow-x-auto mt-4">
                    <table class="w-full table-terminal">
                        <thead>
                            <tr>
                                <th>Fiscal Year</th>
                                <th>Tax Burden</th>
                                <th>Interest Burden</th>
                                <th>Operating Margin</th>
                                <th>Asset Turnover</th>
                                <th>Equity Multiplier</th>
                                <th>DuPont ROE</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="font-bold text-neutral-200">FY2022</td>
                                <td>1.1149</td><td>0.9367</td><td>5.36%</td><td>0.3492x</td><td>1.2343x</td><td class="font-bold text-neutral-300">2.41%</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">FY2023</td>
                                <td>1.7358</td><td>1.2269</td><td>1.77%</td><td>0.3341x</td><td>1.2146x</td><td class="font-bold text-neutral-300">1.53%</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">FY2024</td>
                                <td>0.8250</td><td>0.9535</td><td>8.09%</td><td>0.3725x</td><td>1.2025x</td><td class="font-bold text-neutral-300">2.85%</td>
                            </tr>
                            <tr>
                                <td class="font-bold text-neutral-200">FY2025</td>
                                <td>1.0471</td><td>1.1207</td><td>10.66%</td><td>0.4503x</td><td>1.2211x</td><td class="font-bold text-neutral-300">6.88%</td>
                            </tr>
                            <tr class="bg-neutral-900/60 font-bold text-emerald-400">
                                <td>TTM 2026</td>
                                <td>0.9147</td><td>1.0842</td><td>15.71%</td><td>0.4890x</td><td>1.2565x</td><td>9.57%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <footer class="border-t border-neutral-800 bg-[#0c0d0e] py-4 text-center text-neutral-500 font-mono text-[11px]">
        ERVIS INSTITUTIONAL VALUATION SYSTEM // NUS CFA GLOBAL CHAMPION x DAMODARAN GINZU ENGINE // ADVANCED MICRO DEVICES (NASDAQ: AMD)
    </footer>

    <script>
        function switchTab(tabId) {{
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            // Remove active class from buttons
            document.querySelectorAll('.tab-btn').forEach(el => {{
                el.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                el.classList.add('border-transparent', 'text-neutral-400');
            }});
            
            // Show selected tab
            document.getElementById(tabId).classList.remove('hidden');
            // Activate button
            const btn = document.getElementById('btn-' + tabId);
            btn.classList.add('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
            btn.classList.remove('border-transparent', 'text-neutral-400');
        }}
    </script>
</body>
</html>
"""

with open(f"{REPORTS_DIR}/dashboard.html", "w") as f:
    f.write(dashboard_html)

print(f"  * Generated Interactive Bloomberg HTML Dashboard: {REPORTS_DIR}/dashboard.html")
print("  * All Institutional Deliverables Successfully Created!")
