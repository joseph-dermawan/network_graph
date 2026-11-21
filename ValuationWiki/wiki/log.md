# ValuationWiki Chronological Activity Log

This log is an append-only timeline of all ingestion events, financial model builds, audit passes, and visual graphic updates.

---

## Log Entries

## [2026-08-14] ingest | FactSet & SEC 10-Q Initial Model Setup
* **Action:** Ingested `POWL-US.xlsx` and SEC 10-Q filings. Built master 10-year pro-forma income statement, FCFF schedule, and WACC engine.
* **Outputs Created:** `build_powell_final_model.py`, `powell_valuation_model_final.xlsx`.
* **Key Findings:** Unlevered beta = 0.98, Re-levered beta = 1.15, WACC = 11.02%, DCF Target Price = $261.82.

## [2026-08-16] audit | OpenPyXL Formula String Bug & Sensitivity Engine Fix
* **Action:** Diagnosed `#REF!` error in `SENSITIVITY_ENGINE` tab of master workbook.
* **Root Cause Identified:** Missing `=` prefix in formula string assigned to `margin_t_se` (`margin_t_se = f"='INPUT'!B12+..."`). Excel treated the formula as a literal text string, breaking arithmetic across the 3x3 matrix.
* **Fix Applied:** Added missing `=` prefix, re-compiled model, and verified clean evaluation ($261.77 center cell).

## [2026-08-17] simulation | 10,000-Trial Monte Carlo Stochastic Run
* **Action:** Executed 10,000 Monte Carlo stochastic trials varying WACC (11.02% ± 1.5%), Terminal Growth (3.5% ± 0.75%), and Revenue CAGR (24.0% ± 5.0%).
* **Key Results:** P10 = $213.64, Median = $260.70, Mean = $264.42, P90 = $320.12. Win Rate (Price > $218.73) = **86.78%**.

## [2026-08-18] graphics | 300-DPI Visual Suite Generation (Section 4 & Section 6)
* **Action:** Built scripts `generate_report_figures.py`, `generate_thesis_figures.py`, and `generate_more_figures.py`.
* **Assets Generated:** Figures 4.1 through 4.16 and Figures 6.1 through 6.9 in `POWELL/output_figure/`.
* **Design Revisions:** Formatted canvas width to 5.2 inches, applied brand color `#0B5A3D`, split dual-axis graphs into 2-panel subplots or standalone charts, and added `Source: Unlimited Leverage` footers to 100% of figures.

## [2026-08-18] excel | Standalone Friend Workbook & Appendix Setup
* **Action:** Generated `joseph_powell_fcff_valuation_summary.xlsx` with 3 dedicated tabs: `FCFF_VALUATION_SUMMARY`, `APPENDIX_A_PRO_FORMA_MODEL`, and `APPENDIX_E_PEER_BENCHMARKING`.

## [2026-08-23] structure | Karpathy LLM Wiki Architecture Consolidation
* **Action:** Restructured directory. Moved original network graph files into `NetworkGraph/`. Created `ValuationWiki/` directory containing `sources/`, `wiki/`, `SCHEMA.md`, `index.md`, `log.md`, and 10 detailed interlinked markdown pages.

## [2026-08-23] ingest | Ingestion of Team Report & T-NUS 2026 Model Answer Rubric
* **Action:** Ingested `TNUS Info Session 2026 (Participants' Copy) copy.pdf` and `Team Unlimited Leverage_Report.pdf`.
* **Files Relocated & Extracted:** Moved files to `ValuationWiki/sources/TNUS_Info_Session_2026_Model_Answer.pdf` and `ValuationWiki/sources/Team_Unlimited_Leverage_Report.pdf`. Extracted full text to `.txt` files.
* **New Pages Created:**
  - `wiki/Source_TNUS_Info_Session_2026_Model_Answer.md`
  - `wiki/Source_Team_Unlimited_Leverage_Report.md`
  - `wiki/End_to_End_Valuation_Mastery_and_Framework.md`

## [2026-08-23] ingest | Full Ingestion of NUS Global Champion Report & Master Model Guide Setup
* **Action:** Extracted and thoroughly ingested `ValuationWiki/sources/NUSTeam2022Rpt.pdf` (Sapphire Capital Analysis 21-page global champion report on SATS Ltd / SGX: S58).
* **Master Artifact Created:** `model_valuation.md` (saved at both `ValuationWiki/model_valuation.md` and `ValuationWiki/wiki/model_valuation.md`).
* **Key Methodology Generalized:** Comprehensive 10-step institutional pipeline, Moody's 6-metric synthetic credit rating matrix, Damodaran default spread lookup, DuPont 5-point ROE breakdown, Altman Z-Score distress model, $R^2$ revenue driver regression, Sum-of-the-Parts (SOTP) valuation, Liquidation Value Haircut model, 10,000 Monte Carlo stochastic trials, and NYU/MSCI ESG academic transmission.

## [2026-09-05] model | Universal Valuation Spreadsheet Model Build & Google Sheets Replication
* **Action:** Built a 7-tab institutional valuation spreadsheet model combining Damodaran's Ginzu framework with Sapphire Capital equity research standards. Replicated model live in Google Sheets via `gws` CLI.
* **Google Sheet Live Model:** `https://docs.google.com/spreadsheets/d/1wBFDDikiaw-9R-xu6ZKVLz-So3Ij2XNDnPtf951yF6k/edit#gid=0`
* **Local Excel Model:** `Universal_Institutional_Valuation_Model.xlsx`
* **Archival Action:** Created root `ARCHIVE/` folder and moved Python build scripts (`build_universal_valuation_model.py`, `populate_gsheet_valuation_full.py`, `format_gsheet_valuation.py`, `test_gsheet_setup.py`) to prevent workspace clutter while preserving audit history.
* **New Pages & Directories Created:**
  - `wiki/Universal_Institutional_Valuation_Spreadsheet_Model.md`
  - `wiki/Valuation_Links_Directory.md`
  - `sources/valuation_links_directory.yaml`
* **Ongoing Ingestion & Archival Rule:** Updated `SCHEMA.md` with Section 5 requiring continuous session ingestion and mandatory script archiving into `ARCHIVE/`.

## [2026-09-05] ingest | Damodaran Curriculum Modules 1 & 2 Ingestion
* **Action:** Created comprehensive institutional guide for Module 1 (Foundations & Valuation Philosophy) and Module 2 (Risk, Estimation & Cost of Capital).
* **Document Created:** `DAMODARAN_Wiki/module_01_and_02_foundations_and_cost_of_capital.md`.
* **Key Topics Synthesized:** Valuation vs. Pricing dichotomy, currency-matched risk-free rates, forward-looking implied ERP, geographic revenue-weighted CRP, Hamada bottom-up beta mechanics, Moody's synthetic credit rating grid, and market-weighted WACC derivation.
* **Enhancement (Master Edition):** Added full mathematical derivations, complete numerical walkthroughs (Uber narratives, Disney divisional bottom-up beta, Vale geographic ERP weighting, S&P 500 implied ERP solver, Moody's large vs. small firm rating grids, and coupon-bond debt PV estimation).

## [2026-09-05] ingest | Damodaran Curriculum Module 3 Ingestion
* **Action:** Created Master Edition institutional guide for Module 3 (Accounting Forensic Normalization: R&D Capitalization, Operating Lease Debt Conversion & Earnings Normalization).
* **Document Created:** `DAMODARAN_Wiki/module_03_accounting_forensic_normalization.md`.
* **Key Topics Synthesized:** Linear R&D capitalization schedule, Research Asset valuation, adjusted EBIT & CapEx formulas, proof of FCFF cash-flow invariance, operating lease contractual commitment present-value discounting, imputed interest and debt re-levering, interest coverage impact, and cyclical earnings normalization techniques.

## [2026-09-26] terminal | ERVIS Bloomberg Terminal v2.0 & BETA Screen Release
* **Action:** Built, tested, and deployed the ERVIS Bloomberg Terminal Workstation (`ervis`, `ervis-term`) backed by a local SQLite time-series vault (`ERVIS/vault/ervis_vault.db`).
* **Components Built & Integrated:**
  - Standard Bloomberg 4-letter mnemonics: `DES`, `FA`, `DCF`, `OVML`, `BETA`, `GRPH`, `RV`, `PORT`, `TOP`, `HELP`.
  - CAPM Econometric Regression Engine (`BETA <GO>` / `[F9]`): OLS slope, Blume mean-reverting forward beta ($\beta_{\text{adj}} = 0.67\beta + 0.33$), Jensen's Alpha, $R^2$, and $t$-Statistic.
  - Hamada Capital Structure Decomposition: Levered Beta ($\beta_L$), Unlevered Moat Beta ($\beta_U$), Net Debt/Equity ratio, tax rate, and Cost of Equity ($K_e$).
  - CAPM Systematic Sensitivity & Cost of Capital Matrix: Replaced low-resolution in-terminal ASCII scatter plot with multi-scenario stress table.
  - Ticker Normalization & Zero-Division Fix: Added canonical aliasing (`R.R`, `RR.`, `RYCEY` $\to$ `RR`, `GOOG` $\to$ `GOOGL`, `FB` $\to$ `META`), wrapped price divisions in defensive `spot > 0` guards, and added an institutional coverage exception screen.
  - Hybrid Terminal & Zero Vibe-Coding Vector Visualizer (`GRPH <GO>`): Standalone vector chart generator (`chart_generator.py`) adhering strictly to the Bloomberg Terminal aesthetic (0px border-radius, strict monospace fonts, black background, sharp 1px grid, zero neon glow or rounded SaaS pills).
* **New Wiki Pages & Updates:**
  - `wiki/ERVIS_Bloomberg_Terminal_and_Workstation_Architecture.md`
  - `wiki/Engineering_Learnings_and_Bugs.md` (Sections 5 & 6)
  - `wiki/index.md`
  - `wiki/log.md`

## [2026-11-18] model | Anthropic IPO Forensic Valuation, Damodaran Dissection, Valuation Almanac & Interactive Scenario Builder
* **Action:** Built, audited, calibrated, and deployed the complete Anthropic Pre-IPO valuation suite inside the ERVIS Workstation terminal (`equities/anthropic/damodaran.html` and `almanac.html`).
* **Components Built & Integrated:**
  - **Thought Process & Sheet Dissection (`★ THOUGHT PROCESS & SHEET DISSECTION`):** Added full-width institutional forensic analysis modeled after the NUS CFA Global Champion Report. Deconstructs Professor Aswath Damodaran's 12-step chronological valuation pipeline from GAAP normalization ($376.0B lease debt, $26.5B R&D intangible asset, synthetic BB cost of debt) to perpetual terminal value ($3.46T TV, 76.7% of EV) and the equity bridge ($437.85 – $439.24 / share vs $525.00 IPO ask price, confirming 16.3% overvaluation).
  - **Institutional Valuation Suite (Part II):** Added Multi-Scenario Sensitivity Matrix ($284.15 Bear / $439.24 Base / $682.40 Bull), Sum-of-the-Parts (SOTP) 4-division decomposition ($788.0B EV), Asset Liquidation Floor ($0.00 common recovery against $485.3B debt), and Monte Carlo 10,000-Trial Simulation (24.8% IPO win rate).
  - **Valuation Almanac (`almanac.html`):** Built a 5-tab educational glossary and studio covering 50+ variables with step-by-step mathematical DCF logic, alongside Tab 5 housing the 7 institutional valuation tools (DuPont 5-point, Moody's synthetic rating grid, Altman Z-Score $Z = 2.15$, Monte Carlo distribution).
  - **Interactive Scenario Builder (`★ SCENARIO BUILDER`):** Added dynamic tab with 12 interactive sliders across Growth, Margins, Reinvestment, WACC components, and Distress. Implemented deterministic real-time recalculation engine calibrated to Damodaran's base case ($437.85 / share), dynamic $0–$700 valuation range bar with live marker tracking, side-by-side Top Hero / WACC decomposition cards, and full equity bridge table.
  - **Engineering & Layout Post-Mortems:** Resolved JavaScript scope isolation bug where assigning functions to `window.func` without local declarations triggered a silent `ReferenceError`, freezing intrinsic values at `$0.00`. Fixed CSS Grid blowout bug where `1fr` trapped content on page zoom, applying `minmax(0, 1fr)` and matching tab bar's 14px padding. Added URL hash routing (`#scenario`, `#dissection`).
* **New Wiki Pages & Updates:**
  - `wiki/Anthropic_IPO_Valuation_Forensics_and_Scenario_Builder.md` (Master forensic valuation guide)
  - `wiki/Engineering_Learnings_and_Bugs.md` (Added Sections 7 & 8)
  - `wiki/index.md`
  - `wiki/log.md`

## [2026-11-21] empirical | Anthropic IPO Market Debut, YouTube Video Forensics & Jay Ritter Empirical Archive Ingestion
* **Action:** Ingested, modeled, and deployed Anthropic's first 48 hours of live trading (Nov 18–20, 2026), deconstructed the video analysis (`Y8KS_BF3AeU`), ingested Professor Jay R. Ritter's foundational empirical IPO datasets, and deployed Tab 06 inside the ERVIS Valuation Almanac (`almanac.html#empirical`) with a full Chart.js visual engine.
* **Components Built & Integrated:**
  - **Live Market Debut Forensics:** Priced at **$83.00** (above $70–$78 file band on >18x oversubscription). Retail opened at **$111.50 (+34.34% pop)**, hitting intraday peak of **$115.00 ($1.945T cap)** before closing Day 1 at **$97.17** on 846M shares volume (102.5% float turnover). Day 2 flushed to an intraday low of **$83.05**—testing Damodaran's **$83.69 Ginzu DCF fair value within 64 cents** and the $83.00 offer within 5 cents—rebounding to close at **$88.30** (+6.39% over offer).
  - **YouTube Video Analysis Ingestion (`Y8KS_BF3AeU`):** Deconstructed the two-tier retail exclusion barrier, underwriter gross spread ($82.44 net purchase vs $83.00 re-offer = $548.8M fee pool for Morgan Stanley syndicate), 15% greenshoe stabilization (123.75M shs), and $26.0B strategic private sidecar.
  - **Jay R. Ritter Empirical Archive:**
    - *Money Left on the Table League Table:* Anthropic ranked #1 in world history with **$11.69 Billion** left on the table on its 825M Class A float, surpassing Alibaba ($8.29B) and Visa ($5.08B).
    - *Ritter Table 1:* Mean first-day returns and aggregate money on table by era (1980–2026).
    - *Ritter Table 7:* Predictive power of file range revisions (Above range = +49.8% average pop).
    - *Ritter Table 18e:* Long-run style-adjusted BHAR by public float; proved sub-10% float IPOs (ANT: 4.88%) suffer severe -24.8% 3-year and -38.2% 5-year underperformance due to the Day-180 lockup supply cliff.
    - *Ritter Table 23 & 24:* Dual-class adoption in tech (48.4% by 2025) and -8.6% 5-year governance penalty.
  - **Granular Interactive Price & Schedule Tracker (`#priceTapeChart`):** Dual-axis Chart.js tracker with 17 granular intervals, interactive view filters (`[ALL 48H TAPE]`, `[DAY 1 DEBUT]`, `[DAY 2 DCF FLUSH]`, `[RITTER 180D LIFECYCLE]`), dynamic diagnostic card updating on hover/scrub, and wealth divergence drawdown waterfall.
  - **Header Cleanup:** Removed messy floating descriptions across all pages (`almanac.html`, `cockpit.html`, `index.html`, `prospectus.html`, `damodaran.html`).
* **New Wiki Pages & Updates:**
  - `wiki/Jay_Ritter_IPO_Empirical_Archive_and_Market_Debut_Forensics.md` (New master research document)
  - `wiki/Anthropic_IPO_Valuation_Forensics_and_Scenario_Builder.md` (Calibrated to post-split and live debut)
  - `wiki/index.md`
  - `wiki/log.md`






## [2026-11-21] thematic | Track 1: Thematic AI CapEx & Counterparty Circularity Matrix Forensics
* **Action:** Built, audited, calibrated, and deployed Track 1: Thematic AI CapEx & Counterparty Circularity Matrix across all 4 phases, modeling the closed-loop feedback flywheel between Anthropic, cloud hyperscalers (AWS, GCP, Azure, Meta), and upstream infrastructure providers (NVDA, AVGO, TSM, POWL).
* **Components Built & Integrated:**
  - **Phase 1 Data Repositories:** Created structured datasets inside `ERVIS/projects/THEMATIC_AI_CAPEX/data/`:
    - `commitments_matrix_anthropic_aws_gcp.json`: Full Note 13 schedule ($265.6B total, $164.7B AWS, $100.9B GCP, $26.0B IPO private sidecar, ARR contribution metrics).
    - `hyperscaler_capex_depreciation_timeseries.json`: 2020–2026E CapEx, D&A, CFO, and server useful life disclosures for AMZN, GOOGL, MSFT, and META.
    - `token_deflation_vs_gpu_amortization.json`: Token pricing history (Claude 1 $\to$ Claude 3.5 $\to$ DeepSeek) vs. H100 GPU amortization ($5.74/M token breakeven threshold).
  - **Phase 2 Circularity & Depreciation Calculation Engine:** Built `ai_capex_circularity_engine.py` and generated `data/model_outputs.json`:
    - *Cash Flow Circularity:* Proved that hyperscaler equity injected into Anthropic ($23B AMZN, $13B GOOGL) generates $164.7B (AWS) and $100.9B (GCP) in high-margin Cloud ARR. Capitalized at 8.5x–9.0x EV/Sales, this yields +$1,482B (AWS) and +$857.9B (GCP) in cumulative enterprise value—a **64.4x to 66.0x value multiplier** on the cash equity check.
    - *ASC 360 Depreciation Cliff:* Compared stated 5.5-year 10-K server useful lives against realistic 3.5-year AI GPU technological obsolescence across $394B (2026E) hyperscaler CapEx. Quantified unrecorded annual D&A gap rising from $5.1B (2024) to $21.1B (2026) and peaking at **$45.5B per year in 2028 (989 bps operating margin drag)**, with an unamortized balance sheet asset overhang of **$176.7 Billion**.
    - *Unit Token Inversion:* Derived H100 node all-in amortized hardware cost ($5.74 per 1M blended tokens) against market token price deflation ($1.37/M for DeepSeek and sub-$1 for next-gen), illustrating the acute negative gross margin impairment zone (-91% on Haiku, -319% on DeepSeek).
  - **Phase 3 Interactive Terminal Report (`thematic_capex.html`):** Deployed full institutional report in `THEMATIC_AI_CAPEX/reports/index.html`, `equities/anthropic/thematic_capex.html`, and `US_EQUITIES/ANTHROPIC/reports/thematic_capex.html`:
    - 4 interactive Chart.js modules: Circular Flow Bar/Sankey (`#circularFlowChart`), CapEx Supercycle 2021–2030E (`#capexSupercycleChart`), ASC 360 Depreciation Cliff (`#depreciationCliffChart`), and Token Deflation vs H100 Breakeven (`#tokenBreakevenChart`).
    - Dynamic Client-Side Sensitivity Simulator with real-time sliders for Commitment Drawdown (50%–100%), GPU Depreciable Life (2.5–5.5 yrs), and Token Deflation Shocker (-0% to -75%).
    - 3 Granular Forensic Audit Tables: Note 13 Annual Schedule, Upstream Value Chain Matrix (NVDA, AVGO, TSM, POWL), and Hyperscaler 10-K Useful Life Accounting Audit.
  - **Cross-Linking & Terminal Integration:** Added Module 06 to Anthropic Master Dossier (`equities/anthropic/index.html`), quick jump on Master Workstation (`index.html`), nav tab on DCF Cockpit (`cockpit.html`), and header link on Almanac (`almanac.html`).
* **New Wiki Pages & Updates:**
  - `wiki/Thematic_AI_Capex_Closed_Loop_Forensics.md` (Master institutional research document)
  - `wiki/index.md`
  - `wiki/log.md`

## [2026-11-21] network | Thematic AI Circularity Network, Leontief Input-Output Topology & CoreWeave Shadow Banking Forensics
* **Action:** Formulated, modeled, simulated, and deployed a formal graph-theoretical circularity network model (12 nodes, 24 directed capital flow edges, $480B+ cumulative flows) with Leontief Input-Output matrix mathematics, PageRank absorption centrality, and CoreWeave neo-cloud shadow banking contagion modeling.
* **Components Built & Integrated:**
  - **Workstation UI Refactor & Rebranding:** Renamed header to `ERVIS Central`, removed cluttered badges (`Damodaran Ginzu • CFA Champion Engine`, `📖 ALMANAC`, `>_ ERVIS TERMINAL`), organized workstation quick jump buttons into clean 3-button rows (`grid-cols-3 gap-2`) across Anthropic and Powell cards, and synchronized return breadcrumbs (`&larr; ERVIS CENTRAL`).
  - **Phase 1 Network Graph Dataset (`circularity_network_graph.json`):** 12 nodes across 4 tiers (Hyperscalers: AMZN, GOOGL, MSFT, META; AI Labs: ANT, OPENAI; Neo-Clouds & Credit: COREWEAVE, PRIVATE_CREDIT; Hardware Sinks: NVDA, AVGO, TSM, POWL) and 24 directed weighted edges tracking equity, debt, compute commitments, and hardware CapEx with margin capture rates and contract tenors.
  - **Phase 2 Leontief & Network Simulation Engine (`ai_circularity_network_engine.py`):**
    - Built adjacency matrix $A$ and Leontief flow matrix $(I - A)^{-1}$.
    - Computed circularity extraction ratio $\eta$: AWS achieves **7.16x** ($164.7B ARR on $23B equity) via pure direct captive infrastructure, whereas Google Cloud achieves a blended **3.96x** ($100.9B ARR on $25.5B total capital), suffering a **-49.0% capital efficiency haircut** due to its $12.5B CoreWeave lease commitments.
    - Derived PageRank absorption centrality: TSMC (**25.64%**), Nvidia (**21.48%**), and Powell Industries (**4.82%**) act as terminal absorbing sinks with zero outbound debt or customer financing obligations.
    - Modeled 4 dynamic shock scenarios: Base Case, Token Deflation & CoreWeave DSCR Covenant Breach (GPU rental collapse compresses CoreWeave DSCR from 2.78x to 0.98x), Upstream Hardware Supply Constraint (+25% pricing, TSMC margins expand to 58%), and Hyperscaler CapEx Retrenchment (-30% hyperscaler CapEx).
  - **Phase 3 Interactive SVG Visual Network Console (`thematic_capex.html`):**
    - Built a vector-rendered directed network topology graph with custom SVG markers, interactive node clicking, HUD diagnostic drawer showing In-Degree, Out-Degree, Centrality, and Inbound/Outbound breakdown.
    - Added scenario switcher buttons dynamically recalculating and rendering systemic contagion metrics.
    - Integrated head-to-head Google Cloud vs. AWS CoreWeave drag comparison table detailing why Google Cloud Q3'26 EBIT margins lagged (28.0% vs. 38.5%).
  - **Phase 4 Wiki & Model Ingestion:**
    - Authored `ValuationWiki/wiki/Thematic_AI_Circularity_Network_and_Coreweave.md`.
    - Synced all reports across `THEMATIC_AI_CAPEX/reports/index.html`, `US_EQUITIES/ANTHROPIC/reports/thematic_capex.html`, and `ervis-terminal/equities/anthropic/thematic_capex.html`.
* **New Wiki Pages & Updates:**
  - `wiki/Thematic_AI_Circularity_Network_and_Coreweave.md`
  - `wiki/index.md`
  - `wiki/log.md`
