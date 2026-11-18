# Model Valuation Framework & Institutional Pitch Guide (`model_valuation.md`)

This document is the **Institutional Master Valuation Blueprint & Reference Guide**, derived from the global championship-winning pitch report by **Sapphire Capital Analysis (NUS Team 2022)** on SATS Ltd (SGX: S58). It synthesizes the complete, end-to-end process required to value ANY company, detailing the **10-step institutional pipeline**, authoritative **sources of truth**, reference **mathematical formulas**, and **forensic accounting calculations**.

---

## 🏛️ Executive Overview & The 10-Step Institutional Pipeline

To perform an institutional-grade, end-to-end company valuation, an analyst must execute a 10-step pipeline that bridges raw macro data and micro financial filings to intrinsic target price derivation.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                           10-STEP INSTITUTIONAL VALUATION PIPELINE                       │
│                                                                                          │
│ 1. Executive Summary Hook   ──► 2. Business & Revenue Breakdown ──► 3. Macro & Industry Drivers  │
│                                                                                │         │
│ 6. Forensic Financials      ◄── 5. Variant View Theses        ◄── 4. Competitive Moat    │
│    (DuPont & Altman Z-Score)                                           (Porter's 5 Forces)│
│            │                                                                             │
│            ▼                                                                             │
│ 7. WACC & Synthetic Credit  ──► 8. Multi-Valuation Suite      ──► 9. Risk & Downside     │
│    Rating Grid (Moody's)           (DCF, SOTP, Monte Carlo)          Liquidation Floor   │
│                                                                                │         │
│                                                                                ▼         │
│                                                                  10. ESG Academic        │
│                                                                      Transmission &      │
│                                                                      Governance Audit    │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Section 1: Authoritative Sources of Truth Registry

An institutional valuation report is only as credible as its underlying data sources. Never guess financial figures or rely on generic templates; verify every line item against these primary sources of truth:

| Data Category | Primary Source of Truth | Purpose & Application |
| :--- | :--- | :--- |
| **Financial Statements** | SEC Form 10-K / 10-Q (US), SGX Annual Reports / Financial Results (SG) | Read-only source of truth for revenue, EBIT, net debt, lease liabilities, non-controlling interest (NCI), cash flows. |
| **Financial Database / Multiples** | S&P Capital IQ, Bloomberg, Refinitiv | Peer trading comparables, precedent transactions, historical multiple bands, Bloomberg ESG disclosure scores. |
| **Macro & Sovereign Benchmarks** | EIU (Economist Intelligence Unit), IMF, FitchConnect, Sovereign Treasury Yields | Real GDP growth projections, risk-free rates ($R_f$), 30-year sovereign bond yields (proxy for terminal growth rate $g$). |
| **Cost of Capital & Credit Ratings** | Professor Aswath Damodaran (NYU Stern), Moody's Financial Metrics | Default spreads by synthetic credit rating, Equity Risk Premium (ERP) benchmarks, Damodaran synthetic rating lookup tables. |
| **Industry & Macro Guidance** | WHO, IATA, McKinsey & Company, Industry Association Filings | Passenger traffic projections, meal volume demand, industry capacity utilization, macro reopening milestones. |
| **Academic ESG Transmission** | NYU Stern ESG Metastudies (1,272 studies), MSCI ESG Research, MDPI Finance | Linking ESG disclosure scores to financial performance, alpha outperformance, and cost-of-capital discount rates. |

---

## 🔬 Section 2: Detailed 10-Step Methodology & Reference Calculations

---

### Step 1: Executive Summary & High-Impact Hook
* **Core Goal:** Grab immediate reader attention with a clear stock recommendation, target price, investment horizon, and risk-reward profile.
* **Key Components:**
  1. *Investment Recommendation:* BUY / HOLD / SELL with explicit percentage upside/downside relative to last closed price.
  2. *Investment Horizon:* Standard 3 to 5-year investment horizon.
  3. *Risk-Return Profile:* Asymmetric Upside, Moderate/Low Risk.
  4. *Summary Valuation Bridge:* Summarize primary DCF and SOTP outputs into a single target price.

---

### Step 2: Business Description & Unit Segment Decomposition
* **Core Goal:** Dissect how the company generates revenue and profit across different business divisions and geographic regions.
* **Methodology:**
  * Break down revenue and operating margins by segment (e.g. *Food Solutions* vs. *Gateway Services* for SATS; *Power Control Rooms* vs. *Switchgear* for POWL).
  * Map geographical exposure (Domestic core vs International growth regions).
  * Analyze joint ventures, associates, and non-controlling interests (NCI).

---

### Step 3: Industry Analysis & Statistical Driver Regression ($R^2$)
* **Core Goal:** Identify macro growth drivers and prove their statistical validity using regression analysis.
* **Methodology & Formula:**
  * Evaluate industry TAM, structural supply/demand dynamics, and volume growth.
  * Run linear regression between historical revenue ($y$) and physical volume drivers ($x$, e.g., gross meals produced, passengers handled, data center CapEx).
  * Calculate Coefficient of Determination ($R^2$):
    $$R^2 = \left[ \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2 \sum_{i=1}^{n} (y_i - \bar{y})^2}} \right]^2$$
  * *Criterion:* $R^2 > 0.85$ confirms that the physical volume metric is a statistically valid driver for pro-forma financial projections.

---

### Step 4: Competitive Positioning & Moat Analysis (Porter's 5 Forces)
* **Core Goal:** Quantify the strength of the company's economic moat and competitive advantages.
* **Quantitative Scoring Matrix (1 to 5 Scale):**
  1. *Bargaining Power of Buyers (1-5):* High customization and long-term contracts lower buyer power.
  2. *Bargaining Power of Suppliers (1-5):* Diversified supply chain and farm-to-fork vertical integration mitigate supplier power.
  3. *Degree of Competitive Rivalry (1-5):* Dominant market share (e.g. 80%+ gateway market share) minimizes local rivalry.
  4. *Threat of New Entrants (1-5):* Capital intensity, regulatory/airport safety certifications create high barriers.
  5. *Threat of Substitutes (1-5):* Essential infrastructure services cannot be easily substituted.

---

### Step 5: Investment Theses & Variant View Formulation
* **Core Goal:** Formulate 3 distinct, forward-looking theses that challenge sell-side market consensus.
* **Thesis Architecture:**
  * **Thesis 1 (Mispricing / Reversion):** Buying opportunity created by temporary market pessimism or earnings timing misses.
  * **Thesis 2 (Operational Transformation):** Structural efficiency upgrades, technological automation, and margin expansion post-crisis.
  * **Thesis 3 (Balance Sheet War Chest):** Yielding returns from an underappreciated cash balance and strategic M&A capacity.
* **Investment Catalysts:** Identify 3 specific near-term triggers (e.g. border reopenings, CapEx expansion online date, major contract awards) that will force the market to recognize intrinsic value.

---

### Step 6: Forensic Financial Analysis & Credit Health

#### A. DuPont 5-Point ROE Profitability Decomposition
Deconstruct historical Return on Equity (ROE) across 5 distinct financial ratios to verify whether return growth is driven by operational efficiency or financial leverage:

$$\text{ROE} = \underbrace{\frac{\text{Net Income}}{\text{EBT}}}_{\text{Tax Burden}} \times \underbrace{\frac{\text{EBT}}{\text{EBIT}}}_{\text{Interest Burden}} \times \underbrace{\frac{\text{EBIT}}{\text{Revenue}}}_{\text{EBIT Margin}} \times \underbrace{\frac{\text{Revenue}}{\text{Total Assets}}}_{\text{Asset Turnover}} \times \underbrace{\frac{\text{Total Assets}}{\text{Equity}}}_{\text{Equity Multiplier}}$$

* *Diagnostic Interpretation:* If ROE declines during a crisis (e.g., from 15.7% to -5.1%), check if asset turnover and margins caused the drop while the equity multiplier remained conservative (e.g. 1.44x to 2.00x). Fast ROE recovery (back to 15%+) without issuing heavy debt confirms high earnings quality.

#### B. Altman Z-Score Financial Distress Modeling
Assess bankruptcy risk and balance sheet safety using the Altman Z-Score model for manufacturing/services:

$$Z = 1.2 X_1 + 1.4 X_2 + 3.3 X_3 + 0.6 X_4 + 0.999 X_5$$

Where:
* $X_1 = \frac{\text{Working Capital}}{\text{Total Assets}}$ (Liquidity)
* $X_2 = \frac{\text{Retained Earnings}}{\text{Total Assets}}$ (Cumulative Profitability)
* $X_3 = \frac{\text{EBIT}}{\text{Total Assets}}$ (Operating Efficiency)
* $X_4 = \frac{\text{Market Value of Equity}}{\text{Total Liabilities}}$ (Solvency / Leverage)
* $X_5 = \frac{\text{Revenue}}{\text{Total Assets}}$ (Asset Turnover)

* **Z-Score Zones:**
  * $Z > 2.99$: **Safe Zone** (Minimal financial distress risk).
  * $1.81 < Z < 2.99$: **Grey Zone** (Moderate distress risk).
  * $Z < 1.81$: **Distress Zone** (High probability of bankruptcy).

---

### Step 7: WACC & Synthetic Credit Rating Engine

To calculate a mathematically rigorous Weighted Average Cost of Capital (WACC), avoid guessing credit ratings or cost of debt. Use Moody's 6-metric rating grid combined with Damodaran default spreads.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                        SYNTHETIC CREDIT RATING & WACC PIPELINE                           │
│                                                                                          │
│ 1. Evaluate 6 Moody's Ratios (Coverage, Leverage, ROA, Cash Flow/Debt, Profitability)   │
│                                            │                                             │
│                                            ▼                                             │
│ 2. Determine Base Synthetic Rating  ──►  3. Apply ERM Adjustment (+2 Notch Upgrade)       │
│                                            │                                             │
│                                            ▼                                             │
│ 4. Map Final Synthetic Rating (Ba1) ──►  5. Add Damodaran Default Spread to Risk-Free Rate │
│                                            │                                             │
│                                            ▼                                             │
│ 6. Re-Lever Peer Beta (Hamada)      ──►  7. Compute Cost of Equity (CAPM) & Final WACC    │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

#### A. Moody's Synthetic Credit Rating Matrix
Evaluate company financial ratios against Moody's industrial rating metrics:

| Financial Ratio | Calculation Formula | Moody's Benchmark Metric Grid |
| :--- | :--- | :--- |
| **Interest Coverage** | $\text{EBIT} / \text{Interest Expense}$ | Aaa ($>16.0x$), Aa ($8.6x$), A ($5.4x$), Baa ($3.7x$), Ba ($1.9x$), B/Caa ($0.7x$) |
| **Leverage** | $\text{Total Liabilities} / \text{Equity}$ | Aaa ($31.6\%$), Aa ($41.7\%$), Baa ($49.8\%$), Ba ($68.7\%$), Caa ($92.2\%$) |
| **Return on Assets (ROA)** | $\text{Net Income} / \text{Total Assets}$ | Aaa ($11.6\%$), Aa ($7.5\%$), Baa ($4.4\%$), Ba ($1.7\%$), Caa ($-2.1\%$) |
| **Asset Coverage** | $\text{Total Assets} / \text{Total Liabilities}$ | Aaa ($3.70x$), Aa ($2.40x$), Baa ($2.00x$), Ba ($1.30x$), Caa ($1.00x$) |
| **Profitability** | $\text{Net Income} / \text{Revenue}$ | Aaa ($11.8\%$), Aa ($9.0\%$), Baa ($5.0\%$), Ba ($2.0\%$), Caa ($-2.6\%$) |
| **Current Ratio** | $\text{Current Assets} / \text{Current Liabilities}$ | Aaa ($2.65x$), Aa ($2.00x$), Baa ($1.50x$), Ba ($1.20x$) |

#### B. Enterprise Risk Management (ERM) Adjustment & Cost of Debt
1. Calculate average synthetic rating across the 6 metrics (e.g. initial score = **B1**).
2. Apply **Enterprise Risk Management (ERM)** notch adjustment (e.g. +2 notches for strong balance sheet, parent backing, or dominant market share $\rightarrow$ **Adjusted Synthetic Rating = Ba1**).
3. Lookup **Damodaran Default Spread** for Ba1 rating (e.g. $2.00\%$).
4. Calculate Pre-Tax Cost of Debt ($K_d$):
   $$K_d = R_f + \text{Default Spread}_{\text{Moody's Synthetic}} = 1.60\% + 2.00\% = \mathbf{3.60\%}$$
5. Sanity check $K_d$ against the Yield-to-Maturity (YTM) of existing issued corporate bonds (e.g. 2.60%–2.88%).

#### C. CAPM Cost of Equity & WACC Derivation
1. **Re-levered Beta ($\beta_L$) via Hamada Equation:**
   $$\beta_L = \beta_U \times \left[ 1 + (1 - t) \times \left(\frac{D}{E}\right) \right]$$
2. **Cost of Equity ($K_e$):**
   $$K_e = R_f + \beta_L \times \text{ERP}$$
3. **Final WACC Calculation:**
   $$\text{WACC} = \left(\frac{E}{D+E} \times K_e\right) + \left(\frac{D}{D+E} \times K_d \times (1 - t)\right)$$

---

### Step 8: Multi-Method Intrinsic Valuation & Scenario Suite

An institutional valuation report combines **Discounted Cash Flow (DCF)**, **Sum-of-the-Parts (SOTP)**, **Multi-Scenario Modeling**, **Monte Carlo Simulations**, and a **Liquidation Floor Analysis**.

#### A. DCF Unlevered Free Cash Flow (FCFF) Model
1. **10-Year FCFF Schedule:**
   $$\text{FCFF}_t = \text{NOPAT}_t + \text{D\&A}_t - \text{CapEx}_t - \Delta\text{NWC}_t$$
2. **Terminal Value (Gordon Growth Method):**
   $$\text{TV}_n = \frac{\text{FCFF}_{n+1}}{\text{WACC} - g} = \frac{\text{FCFF}_n \times (1 + g)}{\text{WACC} - g}$$
   *Terminal growth rate $g$ must be benchmarked against 30-year sovereign bond yields (e.g. 2.10%) and long-term real GDP growth forecasts from EIU/IMF.*
3. **Enterprise Value to Equity Value Bridge:**
   $$\text{Implied Equity Value} = \text{PV of 10-Yr FCFF} + \text{PV of TV} + \text{Cash \& Equivalents} - \text{Total Debt} - \text{Non-Controlling Interests (NCI)}$$
4. **Implied Target Share Price:**
   $$\text{Target Share Price} = \frac{\text{Implied Equity Value}}{\text{Diluted Share Count}}$$

#### B. Sum-of-the-Parts (SOTP) Relative Valuation
When a business operates distinct divisions (e.g. *Food Solutions* vs *Gateway Services*), value each division independently using segment-specific peer trading multiples:

$$\text{Total Enterprise Value}_{\text{SOTP}} = \sum_{i=1}^{m} \left( \text{Segment EBITDA}_i \times \text{Peer Forward EV/EBITDA}_i \right)$$

$$\text{Implied Equity Value} = \text{Total Enterprise Value}_{\text{SOTP}} - \text{Total Debt} - \text{NCI} + \text{Cash}$$

#### C. Multi-Scenario Analysis (Bear / Base / Bull Matrix)
Vary assumptions for pandemic recovery speed, margin expansion, and productivity gains across 3 explicit scenarios:
* **Bear Case:** Slower recovery, higher wage inflation, limited margin expansion $\rightarrow$ Implied Price $3.39 (-11.2% downside).
* **Base Case:** Expected backlog burn, volume leverage, margin recovery $\rightarrow$ Implied Price $4.97 (+30.1% upside).
* **Bull Case:** Accelerated demand, successful M&A integration, high automation gains $\rightarrow$ Implied Price $7.12 (+84.9% upside).

#### D. Monte Carlo 10,000-Trial Stochastic Risk Simulation
Randomize three core drivers simultaneously across 10,000 trials using standard normal distributions:
1. Revenue CAGR ($\mu = 15.0\%, \sigma = 3.0\%$)
2. EBITDA Margin ($\mu = 18.5\%, \sigma = 2.0\%$)
3. WACC Discount Rate ($\mu = 6.66\%, \sigma = 0.50\%$)

* **Key Deliverables:** Calculate Mean, Median, P10 floor, P90 ceiling, and **Win Rate** ($\% \text{ of trials } > \text{ Current Share Price}$). A win rate $>85\%$ confirms an institutional BUY.

#### E. Liquidation Value Analysis (Downside Floor)
To establish absolute downside protection for investors, run an asset-by-asset haircut liquidation model:

| Balance Sheet Asset / Liability | Book Value ($M) | High Recovery Rate (%) | Low Recovery Rate (%) | Recoverable Value ($M) |
| :--- | :--- | :---: | :---: | :--- |
| **Cash & Cash Equivalents** | $879.8M | 100% | 95% | $835.9M – $879.8M |
| **Trade Receivables** | $291.5M | 85% | 70% | $204.1M – $247.8M |
| **Inventories** | $130.1M | 70% | 55% | $71.5M – $91.0M |
| **Property, Plant & Equipment (PPE)** | $519.7M | 40% | 25% | $129.9M – $207.9M |
| **Right-of-Use (ROU) Assets** | $187.7M | 30% | 15% | $28.2M – $56.3M |
| **Intangible Assets** | $410.7M | 10% | 5% | $20.5M – $41.1M |
| **Investments in JVs / Associates** | $578.7M | 80% | 65% | $376.1M – $462.9M |
| **Gross Liquidation Proceeds** | -- | -- | -- | **$1,666.2M – $1,986.9M** |
| *Less: Wind-Down & Admin Costs* | -- | -- | -- | -$52.7M – -$55.9M |
| *Less: Total Liabilities & Debt* | $873.4M | 100% | 100% | -$873.4M |
| **Proceeds Available for Equity** | -- | -- | -- | **$740.1M – $1,057.6M** |
| **Liquidation Value per Share** | -- | -- | -- | **$0.66 – $0.94 / share** |
| **Maximum Downside Floor** | -- | -- | -- | **-75.5% to -82.8% Max Floor** |

---

### Step 9: Investment Risk Matrix & Downside Protection
* **Categorization:** Separate **Market Risks** (macroeconomic, inflation, travel restrictions, raw material price shocks) from **Business Operations Risks** (labor shortages, acquisition execution risks, supply chain bottlenecks).
* **1-to-1 Risk Mitigations:** Pair every single identified risk with an explicit operational or financial hedge.
* **Sensitivity Impact:** Estimate the exact dollar/share impact on target price if a risk materializes (e.g. slower VTL travel recovery reduces target price by -$1.15/share).

---

### Step 10: ESG Academic Transmission & Board Governance Audit

#### A. Bloomberg ESG Disclosure Score Benchmarking
Compare company ESG disclosure scores against direct global peers across Environment, Social, Governance, and Total Bloomberg Disclosure metrics.

#### B. Academic ESG Financial Transmission Channels
Cite peer-reviewed academic literature to prove why strong ESG performance directly impacts corporate valuation:
1. **NYU Stern ESG Metastudy (2020):** Evaluated 1,272 corporate studies across 12 meta-analyses, proving a positive relationship between ESG and financial performance in **58% of corporate studies**.
2. **MSCI ESG Research (2024):** Demonstrated that companies in the top ESG quintile (top 20%) outperformed bottom-quintile peers in long-term financial returns and stock price performance.
3. **MDPI Finance (2024):** Proved that firms with higher ESG disclosure scores benefit from a statistically significant **lower Cost of Capital (WACC)**.

#### C. Board Governance & Independence Audit
Evaluate Board Governance against regional codes of corporate governance (e.g. Singapore Code of Corporate Governance - SCCG):
* *Separation of CEO & Chairman:* Ensures division of responsibilities (no single individual holds unfettered power).
* *Independent Directors:* Benchmark percentage of independent directors (e.g. 11 out of 12 directors independent = 91.7%, far exceeding 33% minimum requirement).
* *Board Diversity:* Evaluate age, gender, ethnicity, and specialized skill mix (industry specialists vs public accounting experts).

---

## 🔗 Related Wiki Pages
* [[Source_TNUS_Info_Session_2026_Model_Answer]]: Competition rubrics and guidelines.
* [[Source_Team_Unlimited_Leverage_Report]]: Team report ingestion summary.
* [[End_to_End_Valuation_Mastery_and_Framework]]: Synthesis of skills needed for complete company valuation.
* [[DCF_Valuation_Model]]: Base DCF valuation model.
* [[WACC_Cost_of_Capital]]: Detailed cost of capital derivation.
