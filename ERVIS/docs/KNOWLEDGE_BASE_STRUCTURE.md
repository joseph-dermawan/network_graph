# ERVIS Knowledge Base Structure & Data Topology (`KNOWLEDGE_BASE_STRUCTURE.md`)

---

## 1. The Dual-Layer Knowledge Architecture

A common failure mode in AI-powered valuation systems is **data contamination**: confusing enduring financial methodologies with stale historical numbers. 

ERVIS resolves this with a **bifurcated knowledge topology**:

```
                              [ERVIS AGENT BRAIN]
                                       │
         ┌─────────────────────────────┴─────────────────────────────┐
         ▼                                                           ▼
[TIER A: PERSISTENT METHODOLOGY KB]           [TIER B: COMPARTMENTALIZED DATA REPOS]
 - Immutable Formulas & Theory                 - Live SEC Filings & XBRL Cache
 - Statistical Validation Rules                - Dynamic Market Pricing & Tickers
 - Rating Conversion Grids                     - Sovereign Yield Curves (Rf)
 - Model Templates & MathJax Proofs            - Company Projects & Theses History
 (Re-used across all companies & markets)      (Strictly isolated by Market & Ticker)
```

---

## 2. Tier A: Persistent Central Methodology Knowledge Base (`ERVIS/kb/`)

The Central Knowledge Base stores **how** to value companies. It contains no company-specific time-sensitive assumptions.

* **`kb/methodology/damodaran_ginzu.md`:**
  * Operating lease capitalization equations and present value compounding.
  * R&D asset capitalization mechanics and straight-line amortization.
  * Sales-to-Capital reinvestment linking formula.
  * Zero-excess-return terminal reinvestment constraint ($g / \text{ROIC}_{\text{terminal}}$).
* **`kb/methodology/moodys_credit_grid.md`:**
  * Moody's 6-metric industrial financial ratio matrix.
  * Conversion algorithms from coverage and leverage ratios to alphanumeric ratings (`Aaa` to `Caa`).
  * Default spread lookup curves benchmarked to historical spreads.
* **`kb/methodology/dupont_and_altman.md`:**
  * 5-point DuPont ROE deconstruction formulas.
  * Altman Z-score calculation formulas and threshold boundaries ($Z > 2.99$ safe, $Z < 1.81$ distress).
* **`kb/methodology/econometric_drivers.md`:**
  * Ordinary Least Squares (OLS) regression rules.
  * Rejection threshold: $R^2 < 0.85$ or $p > 0.05$.
* **`kb/methodology/liquidation_haircuts.md`:**
  * Empirical asset haircut ranges for cash, receivables, inventories, PP&E, and intangibles.

---

## 3. Tier B: Compartmentalized Market & Company Data Repos (`ERVIS/projects/`)

To prevent cross-company hallucinations and manage confidential project notes, each equity under analysis receives an **isolated, self-contained project vault**:

```
ERVIS/projects/
├── US_EQUITIES/
│   ├── KO_CocaCola/
│   │   ├── raw_filings/           # Ingested 10-K, 10-Q JSON/XBRL files
│   │   ├── regressions/           # Volume driver regression plots and data
│   │   ├── model.xlsx             # Live Universal Valuation Spreadsheet
│   │   ├── dashboard.html         # Bloomberg-styled interactive dashboard
│   │   ├── thesis_dossier.md      # Variant view, catalysts, Porter's 5 forces
│   │   └── history_log.md         # Full audit trail of past valuation iterations
│   └── POWL_PowellIndustries/
└── SG_EQUITIES/
    └── SATS_S58/
```

### Benefits of Compartmentalization:
1. **Zero Context Bleed:** Ingesting a new SEC filing for Coca-Cola cannot contaminate or overwrite data for Powell Industries.
2. **Longitudinal Learning:** When re-valuing Coca-Cola next quarter, ERVIS loads `KO_CocaCola/history_log.md` to see what the previous valuation was, what variant view was taken, and what catalysts materialized.
3. **Reproducibility:** Every valuation run preserves its raw input data, calculated outputs, and model files in one folder.

---

## 4. The Recency Verification Protocol (Fresh Data Mandate)

Before ERVIS executes any valuation calculation, it runs the **Recency Engine**:

```
                                [VALUATION TRIGGERED]
                                          │
                                          ▼
                         [CHECK 1: LATEST SEC FILING DATE]
                       Is latest 10-Q/K timestamp < 90 days?
                                ├── YES ──► Proceed
                                └── NO  ──► Prompt: "Filing is >90 days old. Scrape latest 10-Q?"
                                          │
                                          ▼
                        [CHECK 2: RISK-FREE RATE FRESHNESS]
                     Is benchmark Rf updated within past 7 days?
                                ├── YES ──► Proceed
                                └── NO  ──► Execute scrapers/macro_treasury_fetch.py
                                          │
                                          ▼
                         [CHECK 3: MARKET PRICE FRESHNESS]
                       Is stock price from current trading date?
                                ├── YES ──► Proceed
                                └── NO  ──► Query live market API
                                          │
                                          ▼
                               [AUTHORIZE CALCULATION]
```

### Recency Audit Rules:
1. **Rule of 90 Days:** Quarterly financial statements older than 90 days are flagged as stale.
2. **Rule of 7 Days:** Sovereign risk-free rates ($R_f$) must be updated at least weekly.
3. **Rule of Intraday Price:** Current stock price ($P_0$) must reflect the latest trading session close.
