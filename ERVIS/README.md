# ERVIS :: Equity Research and Valuation Investment System
**Autonomous Agentic Equity Research & Institutional Valuation Co-Worker**

---

## 1. Executive Summary

**ERVIS (Equity Research and Valuation Investment System)** is an autonomous, human-in-the-loop agentic framework designed to conduct institutional-grade equity research and financial valuation in rapid, collaborative 2-to-3-hour interactive pairing sessions. 

ERVIS bridges the gap between:
1. **Professor Aswath Damodaran’s FCFF Ginzu Framework:** Methodological rigor, structural accounting normalizations (R&D and operating lease capitalization), fundamental reinvestment consistency (Sales-to-Capital ratio), and terminal moat economics.
2. **The NUS CFA Global Champion Valuation Standard (Sapphire Capital / Team 2022):** Granular operational econometric volume regressions ($R^2 > 0.85$), Sum-of-the-Parts (SOTP) multi-segment modeling, Moody's 6-metric synthetic credit matrices, 10,000-trial Monte Carlo stochastic simulations, and asset-by-asset liquidation haircut downside floors.

Rather than acting as a black-box generator, ERVIS acts as an **AI Co-Worker / Senior Research Associate**, debating narrative hypotheses, validating financial restatements, running econometric scripts, and presenting structured decision gates directly to the human lead analyst.

---

## 2. Core System Architecture

```
                                  [HUMAN LEAD ANALYST]
                                            │
                        ◄── Collaborative Pairing Interface ──►
                                            │
                                      [ERVIS AGENT]
                                            │
    ┌───────────────────────────────────────┼───────────────────────────────────────┐
    ▼                                       ▼                                       ▼
[CENTRAL METHODOLOGY KB]        [SCHEDULED DATA HARVESTERS]         [COMPARTMENTALIZED DATA]
 - Damodaran Ginzu Rules         - Antigravity /schedule Crons      - Market & Macro Dossiers
 - Moody's Credit Matrix         - SEC EDGAR 10-K/10-Q Feeds        - Industry Decile Benchmarks
 - Econometric Driver Suites     - US Treasury & Sovereign Yields   - Company Project Vaults
 - SOTP & Liquidation Rules      - Damodaran Annual Data Scrapes    - Live Model Workbooks (.xlsx)
                                            │
    ┌───────────────────────────────────────┴───────────────────────────────────────┐
    ▼                                                                               ▼
[ANALYTICAL ENGINES]                                                    [INSTITUTIONAL OUTPUTS]
 1. SEC Filing Parser & Normalizer                                       1. Universal Excel Model
 2. Econometric Volume Regressor (R² > 0.85)                             2. Interactive HTML Dashboard
 3. DuPont 5-Pt & Altman Z-Score Diagnostics                             3. 20-Page Pitch Research Memo
 4. Hamada WACC & Synthetic Rating Solver                                4. Monte Carlo Risk Curves
 5. Two-Stage FCFF & Moat TV Engine                                      5. Asset Liquidation Floor
 6. Monte Carlo 10,000-Trial Simulator                                   6. Variant Consensus Theses
```

---

## 3. The Central Rule: Recency Enforcement & Knowledge Decoupling

A foundational principle of ERVIS is the **strict decoupling of analytical methodology from temporal financial data**:

* **Immutable Reference Knowledge (Persistent KB):** Analytical formulas, econometric validation procedures, financial diagnostic rules, and historical qualitative narratives are stored permanently in the central knowledge repository.
* **Fresh Market & Filing Data (Dynamic Ingestion):** Past financial numbers must **never** be assumed current. Before any valuation session initiates, ERVIS executes an automated **Recency Gate**:
  1. Detects the latest 10-K, 10-Q, or 8-K filing timestamps.
  2. Queries current benchmark risk-free rates ($R_f$) from live sovereign yield curves.
  3. Verifies prevailing equity risk premiums (ERP) and credit default spreads.
  4. Explicitly flags any stale input cell exceeding 90 days of age.

---

## 4. Repository Directory Structure

```
ERVIS/
├── README.md                           # Master Project Architecture (This file)
├── docs/                               # System Specifications
│   ├── ARCHITECTURE.md                 # 5-Tier Technical Deep Dive
│   ├── WORKFLOW_PROTOCOL.md            # 2-to-3-Hour Human-in-the-Loop Session Script
│   ├── KNOWLEDGE_BASE_STRUCTURE.md     # Persistent vs Dynamic Storage Topology
│   └── SCRAPER_SCHEDULE.md             # Antigravity Automated Scraping Schedules
├── kb/                                 # Centralized Methodology Knowledge Base
│   ├── methodology/                    # Core Valuation Algorithms & Formulas
│   │   ├── damodaran_ginzu.md          # R&D, Leases, Sales-to-Capital, Moat Rules
│   │   ├── moodys_credit_grid.md       # 6-Metric Synthetic Rating & Spreads
│   │   ├── dupont_and_altman.md        # 5-Point ROE & Z-Score Equations
│   │   ├── econometric_drivers.md      # Linear Regression (R² > 0.85) Validation
│   │   └── liquidation_haircuts.md     # Asset Recovery Rate Guidelines
│   └── macro/                          # Global Sovereign & Industry Benchmarks
│       ├── sovereign_yields.yaml       # Live Risk-Free Rates by Currency
│       ├── country_risk_premiums.yaml  # Damodaran Country Default Spreads
│       └── industry_averages/          # Global Sector Betas & Margins
├── projects/                           # Compartmentalized Company Analysis Vaults
│   ├── US_EQUITIES/
│   │   ├── KO_CocaCola/                # Historical Valuation Dossier & Models
│   │   └── POWL_PowellIndustries/      # Operational Regressions & SOTP
│   └── SG_EQUITIES/
│       └── SATS_S58/                   # In-Flight Catering Volume Models
├── scrapers/                           # Automated Antigravity Harvesters
│   ├── sec_edgar_harvest.py            # Automated 10-K/10-Q Ingestion Script
│   ├── macro_treasury_fetch.py         # US Treasury & Sovereign Yield Scraper
│   └── damodaran_dataset_sync.py       # Annual Beta/ERP Table Ingestion
└── models/                             # Master Spreadsheet Templates
    └── Master_Institutional_Template.xlsx
```

---

## 5. End-to-End Pairing Session Phases (2 to 3 Hours)

| Phase | Duration | Agent Responsibilities | Human Analyst Gate |
| :--- | :---: | :--- | :--- |
| **Phase 1: Ingestion & Recency Gate** | 15 min | Scrapes SEC 10-K/Q, verifies sovereign yield $R_f$, builds raw financial database. | Sign-off on financial statement restatements and reporting period boundaries. |
| **Phase 2: Operational Regressions & Diagnostics** | 30 min | Runs volume-to-revenue regressions ($R^2$), calculates 5-point DuPont and Altman Z. | Selection of high-conviction physical operational drivers ($R^2 > 0.85$). |
| **Phase 3: Cost of Capital & Credit Synthesis** | 20 min | Solves Hamada beta, runs Moody's 6-metric credit matrix, computes blended WACC. | Approval of ERM notch adjustment and target debt-to-equity ratio. |
| **Phase 4: Valuation Modeling & Triangulation** | 45 min | Builds 10-Yr DCF, SOTP divisional pricing, and 10,000-trial Monte Carlo simulation. | Setting strategic levers: revenue CAGR, target margins, and terminal moat ROIC. |
| **Phase 5: Pitch Memo & Dashboard Compilation** | 30 min | Generates Excel model, Bloomberg-styled interactive HTML dashboard, and pitch memo. | Final investment verdict approval (BUY/HOLD/SELL target price). |

---

## 6. Getting Started

1. **Activate Automated Harvest:** Run `python3 scrapers/macro_treasury_fetch.py` to refresh macro baseline data.
2. **Launch a Valuation Session:** Invoke an Antigravity co-worker pairing session with the target ticker:
   ```bash
   # Example initiating analysis for a new ticker
   agy --task "Initiate ERVIS valuation session for TICKER: AAPL following ERVIS/docs/WORKFLOW_PROTOCOL.md"
   ```
3. **Inspect Output:** Review generated spreadsheets, interactive HTML dashboards, and thesis memos within `ERVIS/projects/[MARKET]/[TICKER]/`.
