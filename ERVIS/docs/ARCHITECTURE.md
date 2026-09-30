# ERVIS System Architecture & Technical Specifications (`ARCHITECTURE.md`)

---

## 1. Architectural Philosophy: The Dual-Engine System

**ERVIS (Equity Research and Valuation Investment System)** unites two previously disparate disciplines in equity research:

1. **Top-Down Academic Valuation Rigor (Damodaran):**
   * Structural normalization of non-capitalized investments (converting R&D into a multi-year Research Asset and operating leases into debt).
   * Strict economic growth linkage via the **Sales-to-Capital ratio** ($\text{Reinvestment}_t = \Delta \text{Sales}_t / (S/C)$), eliminating unanchored CapEx guessing.
   * Perpetual growth governed by the **Economic Moat Condition**:
     $$\text{Reinvestment Rate}_{\text{terminal}} = \frac{g}{\text{ROIC}_{\text{terminal}}}$$
     Forcing zero excess returns ($\text{ROIC} = \text{WACC}$) in perpetuity unless a defensible competitive advantage exists.

2. **Bottom-Up Sell-Side Institutional Precision (NUS CFA Global Champion / Sapphire Capital):**
   * Multi-year historical volume regressions ($R^2 > 0.85$) against real-world physical capacity drivers (e.g. flight handling, meal volumes, gigawatt capacity).
   * DuPont 5-point ROE decomposition and Altman Z-score balance sheet distress testing.
   * Multivariate credit scoring using Moody's 6-metric matrix and Enterprise Risk Management (ERM) adjustments.
   * Multi-method triangulation: 10-Year DCF, Sum-of-the-Parts (SOTP), 10,000-trial Monte Carlo stochastic distributions, and an asset-by-asset liquidation haircut floor.

---

## 2. The 5-Tier Analytical Pipeline

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 TIER 1: INGESTION & RECENCY GATE                       │
│  - SEC EDGAR 10-K/10-Q Ingestion       - XBRL JSON Parser                              │
│  - Live Treasury Yield Scraping        - Freshness Audit (Timestamp < 90 Days)         │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                             TIER 2: FORENSIC NORMALIZATION & DIAGNOSTICS               │
│  - R&D Capitalization Engine           - Operating Lease Debt Converter                │
│  - 5-Point DuPont ROE Decomposition    - Altman Z-Score Bankruptcy Check               │
│  - Net Operating Loss (NOL) Tracker    - Trapped Offshore Cash Haircuts                │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              TIER 3: STATISTICAL DRIVERS & COST OF CAPITAL             │
│  - Volume-to-Revenue Regressions (R²)  - Moody's 6-Metric Credit Grid                  │
│  - Hamada Re-levered Beta              - CAPM & Two-Stage WACC Schedule                │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               TIER 4: MULTI-METHOD VALUATION SUITE                     │
│  - 10-Year Unlevered FCFF Engine       - Divisional Sum-of-the-Parts (SOTP) Multiples  │
│  - Gordon Growth Moat Terminal Value   - 10,000-Trial Stochastic Monte Carlo           │
│  - Asset Liquidation Haircut Model     - Master Enterprise-to-Equity Waterfall Bridge  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                           TIER 5: REPORTING & INTERACTIVE ARTIFACTS                    │
│  - Universal Excel Spreadsheet         - Bloomberg Terminal Themed HTML Dashboard      │
│  - 20-Page Institutional Research Memo - Variant View Theses & Catalyst Matrix         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Tier Mechanics

### Tier 1: Ingestion & Recency Enforcement
* **SEC EDGAR Scraping:** Uses the SEC EDGAR public REST API with a compliant `User-Agent` header (`ERVIS_Agent admin@ervis.org`). Downloads recent 10-K and 10-Q JSON/XBRL filings.
* **Macro Benchmarking:** Queries Treasury.gov / Federal Reserve API for live 10-year and 30-year US Treasury bond yields.
* **Recency Verification:** Compares the filing date against current system time. If the newest data is $>90$ days old, ERVIS flags an audit alert to verify if a new earnings release or 8-K was filed.

### Tier 2: Forensic Accounting Normalization
* **R&D Capitalization Engine:** Capitalizes past R&D over an asset life $N$ (typically 3–5 years for software, 10 years for pharma) using straight-line amortization:
  $$\text{ResearchAsset}_0 = \sum_{t=0}^{N-1} \text{RD}_{-t} \cdot \left(1 - \frac{t}{N}\right), \quad \Delta\text{EBIT} = \text{CurrentRD} - \text{Amortization}_0$$
* **Lease Capitalization:** Dissects future non-cancelable lease obligations, discounting commitments at the pre-tax cost of debt ($K_d$) to add synthetic lease debt to total debt and adjust operating margins.
* **DuPont 5-Point Analysis:**
  $$\text{ROE} = \left(\frac{\text{Net Income}}{\text{EBT}}\right) \times \left(\frac{\text{EBT}}{\text{EBIT}}\right) \times \left(\frac{\text{EBIT}}{\text{Revenue}}\right) \times \left(\frac{\text{Revenue}}{\text{Assets}}\right) \times \left(\frac{\text{Assets}}{\text{Equity}}\right)$$

### Tier 3: Statistical Driver Modeling & WACC
* **Econometric Driver Regression:** Evaluates candidate physical volume metrics (e.g. megawatt hours delivered, passenger boardings, active subscribers). Computes Ordinary Least Squares (OLS) regression against revenue. Only drivers with $R^2 > 0.85$ and $p < 0.05$ are approved for pro-forma projections.
* **Synthetic Credit Rating:** Evaluates 6 Moody's benchmark ratios:
  1. Interest Coverage ($\text{EBIT}/\text{Interest}$)
  2. Debt / Equity Leverage ($\text{Liabilities}/\text{Equity}$)
  3. Return on Assets ($\text{Net Income}/\text{Assets}$)
  4. Asset Coverage ($\text{Assets}/\text{Liabilities}$)
  5. Net Profit Margin ($\text{Net Income}/\text{Revenue}$)
  6. Current Ratio ($\text{Current Assets}/\text{Current Liabilities}$)
  Maps average rating to Damodaran default spread tables, adjusting $+1$ to $+2$ notches for ERM (market share, government affiliation, diversified cash reserves).

### Tier 4: Multi-Engine Valuation Suite
* **10-Year Discrete DCF:** Incorporates two-stage growth compounding, Sales-to-Capital reinvestment, and terminal moat constraints.
* **Sum-of-the-Parts (SOTP):** Values distinct divisional segments using forward EV/EBITDA multiples from peer cohorts.
* **Monte Carlo Simulation:** Runs 10,000 stochastic trials by randomizing Revenue CAGR ($\sigma \approx 2.5\%$), Operating Margin ($\sigma \approx 1.5\%$), and WACC ($\sigma \approx 0.40\%$). Yields the empirical probability distribution and "Win Rate" ($P(\text{Value} > \text{Market Price})$).
* **Liquidation Haircut Model:** Conservative tangible floor calculation assigning standard recovery haircut percentages:
  * Cash: $100\%$
  * Receivables: $70\% - 85\%$
  * Inventory: $50\% - 70\%$
  * PP&E: $25\% - 40\%$
  * Intangibles: $0\% - 10\%$

### Tier 5: Institutional Deliverables
* **Universal Excel Workbook (`.xlsx`):** Fully dynamic, multi-tab financial model linking inputs to output DCF schedules without hardcoded plug values.
* **Interactive HTML Dashboard:** Monochrome Bloomberg Terminal themed interface with real-time tab switching, MathJax mathematical proofs, and clean Mermaid architecture flowcharts.
* **Investment Memorandum:** Standard 20-page sell-side format detailing variant view theses, operational risks, catalyst calendars, and board governance audits.
