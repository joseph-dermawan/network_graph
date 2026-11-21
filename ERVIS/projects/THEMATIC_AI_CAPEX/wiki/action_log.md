# AI-CAPEX Research Action Log & Movement Record
**Project: THEMATIC_AI_CAPEX | Wiki Framework**
*Maintainer: Lead Analyst (Joseph Hengky Dermawan) & Copilot Desk*

This document serves as the permanent chronological record of all movements, data acquisitions, analytical models, and hypothesis tests executed within the AI-CAPEX project.

---

### [2026-10-18 13:00] Phase 0: Project Initialization & Sunday Sprint Alignment
- **Movement**: Audited project repository structure and historical notes (`README.md`, `notes/reading_notes.md`, `DAMODARAN_Wiki/wiki/special_ai_capex_payout_and_roi_framework.md`).
- **Objective**: Establish the 4-Gate Sunday Research Canvas (Gate 1: Historical CapEx run-rates; Gate 2: Depreciation cliff; Gate 3: Economic hurdle / ROIC vs WACC; Gate 4: Synthesis story).
- **Hypotheses Staged**:
  1. *Depreciation Lag*: Big Tech GAAP profitability is artificially flattered by extended accounting lives (5-6 years) while underlying GPU clusters obsolesce in 3-4 years.
  2. *The Prisoner's Dilemma*: Over-investment is a rational Nash equilibrium to defend core monopolies against displacement.
  3. *The Monetization Deficit*: Run-rate software revenues lag hardware CapEx by >$400B-$500B annually.

---

### [2026-10-18 13:24] Phase 1: Damodaran October 2026 Ingestion & Asset Archival
- **Movement**:
  - Located Professor Aswath Damodaran's latest benchmark model file: `ERPOct26.xlsx` (1.5 MB).
  - Executed automated cloud synchronization via Google Workspace CLI (`gws drive +upload ./ERPOct26.xlsx`).
  - Successfully archived to Google Drive (Drive ID: `1TeNC_Kv7uhfDiRMcaoXA6lXS8vL64By3`, accessible via Google Sheets).
  - Harvested and forensically parsed Damodaran's October 8, 2026 Substack release: *"Earnings, Cashflows and Stock Prices: The AI Spending plays through!"*.
- **Key Empirical Extractions from Damodaran**:
  - *Treasury Shock*: 10-year US Treasury yield surged 54 bps in September 2026 from 4.75% to 5.29% (top 10% monthly increase since 1962).
  - *Equity Resilience*: Stock market added $2.5T in capitalization in September 2026, with $1.5T concentrated strictly in Technology.
  - *Capital Distortion*: Q2 2026 US CapEx up $133B annualized. Technology book equity expanded ~30% and total debt grew ~18.8% year-over-year.
  - *Cash Yield Divergence*: S&P 500 cash returned to shareholders (dividends + buybacks) dropped to **63% of net income** in LTM 2026—the lowest corporate cash payout ratio since 2004.
  - *The Accounting Lag Warning*: Damodaran explicitly states markets will penalize AI CapEx overbuilding months or years before accountants take formal impairment write-offs.

---

### [2026-10-18 13:26] Phase 2: Citation Standardization & Primary Document Registry
- **Movement**:
  - Formulated mandatory standard citation schema in `ERVIS/projects/THEMATIC_AI_CAPEX/citations.yaml`.
  - Established primary SEC EDGAR filing audit map in `ERVIS/projects/THEMATIC_AI_CAPEX/financial_documents_repository.md` covering 5 Hyperscalers (MSFT, GOOGL, META, AMZN, ORCL) and 3 Hardware Builders (NVDA, TSM, AVGO).
  - Mapped specific footnote audit checklists: Server useful life extensions, lease obligations, CapEx Payout Ratio (CPR).

---

### [2026-10-18 13:28] Phase 3: Multi-Disciplinary Theoretical Synthesis
- **Movement**:
  - Synthesized 5 theoretical frameworks beyond Damodaran:
    1. *Marathon Capital Cycle Theory* (Chancellor): Supply elasticity, capacity overshoot, and the capital turning point.
    2. *Game-Theoretic Real Options* (Dixit-Pindyck, Grenadier): Preemptive investment, fear of monopoly forfeiture, and negative standalone NPV acceptance.
    3. *Depreciation Amortization Wave & Cash Flow Duration Mismatch* (Casual Finance, Damodaran): Backward-looking convolution of capitalized PP&E and margin erosion.
    4. *Microeconomic Unit Economics*: Sunk training CapEx vs. variable inference cost commoditization.
    5. *Global Macro Capital Flows & Cross-Border WACC*: US yield shocks, Bank of Japan carry-trade unwind pressures, and sovereign balance sheet subsidies.
  - Built dedicated wiki modules under `wiki/frameworks/` and core analytical synthesis documents.

---

### [2026-10-18 13:42] Phase 4: Diagnostic & Resolution of Damodaran's `ERPOct26` Spreadsheet
- **Problem**: Opening the uploaded `ERPOct26.xlsx` in Google Sheets produced cascaded `#ERROR!` across 81+ critical calculation cells (including `Impl premium calculator` and `Buyback & Dividend computation`).
- **Root Cause Forensic Diagnosis**:
  1. *Local Path External Links*: In `Buyback & Dividend computation` (B85, C85, D85), Damodaran linked formulas to an external file on his local Mac (`/Users/Shared/.../Buyback&DividendsUpdater.xls`), referencing `[1]Aggregates!$BB$19`, `$BB$20`, `$BB$21`. When opened outside his machine, Google Sheets evaluated these to `#ERROR!`, breaking row 89, row 57, row 26, row 27, and subsequently cascading `#ERROR!` into all cash yield calculations in `Impl premium calculator`.
  2. *Excel Structured Table References*: In `Historical ERP` (Columns H, I, cell E99) and `Implied ERP (Monthly from 9-08)` (Column P), formulas utilized Excel-only structured table syntax (`=Table167[[#This Row],[ERP (T12m)]]+Table167[[#This Row],[T.Bond Rate]]` and `=Table2[[#This Row]...]`), which Google Sheets cannot evaluate.
  3. *Office Compatibility Mode vs. Native Sheet*: The file was originally hosted in Google Drive as an uncoverted binary `.xlsx`.
- **Remediation & Fix Executed**:
  1. Extracted exact cached growth rate constants from `xl/externalLinks/externalLink1.xml` (BB19 = +23.906%, BB20 = +6.472%, BB21 = -9.750%) and repaired B85, C85, D85 formulas.
  2. Converted all 193 structured table formulas in `Implied ERP (Monthly from 9-08)` to native Google Sheets/Excel dynamic coordinates (`=J{row}+C{row}`).
  3. Converted all 197 structured table formulas in `Historical ERP` to native cell coordinates (`=B{row}-C{row}`, `=B{row}-D{row}`, `=E98*(1+B99)`).
  4. Updated existing Drive file `1TeNC_Kv7uhfDiRMcaoXA6lXS8vL64By3` with the fixed `.xlsx` build.
  5. Created a **Native Google Spreadsheet** version (`1F8fYJbZuRUOY68KbMQWM5HFZ3Sn_o3WMvpZTZL6qN5o`), run through full API diagnostic verification: **0 ERRORS across all 9 sheets**.

---

### [2026-10-18 14:18] Phase 5: Duration Angle Deep Dive & Scientific Chip Lifecycle Telemetry
- **Movement**:
  - Authored dedicated quantitative module: `wiki/frameworks/macaulay_duration_ai_capex.md` covering:
    - Mathematical formulation of Macaulay Duration ($D_{\text{Mac}}$) and Modified Duration ($D_{\text{Mod}}$).
    - 10-year numerical simulation contrasting a "One-Time Railroad" buildout vs. a "3.5-Year Treadmill Reality".
    - Sensitivity tables across discount rates ($r = 5.0\%$ to $12.0\%$). Demonstrates that a 3.5-year replacement treadmill turns an apparently positive-NPV project (-$10\text{B}$ upfront yielding $+\$4.38\text{B}$ standalone NPV at $9.79\%$ WACC) into a deeply negative **-$7.09\text{B}$ Net Present Value**!
  - Harvested and cataloged peer-reviewed academic/scientific sources on GPU silicon degradation and lifecycle dynamics:
    - *Meta AI Research (Dubey et al., July 2024)*: Empirical telemetry from 16,384 H100s over 54 days of 405B Llama 3 training: 419 unexpected failures (1 failure every 3.1 hours), with GPUs/NVLink and HBM3 memory accounting for 58.7% of all unexpected crashes.
    - *Google Research (Jouppi et al., ACM/IEEE ISCA 2023)*: TPU v4 cluster efficiency scaling proving that datacenter power/megawatt caps force accelerator obsolescence every 2–3 years regardless of physical silicon longevity.
    - *Oak Ridge National Laboratory / IEEE (Nie et al., HPCA)*: Multi-year GPU error and thermal degradation studies on HPC production clusters.
  - Appended full citations to `citations.yaml`.
