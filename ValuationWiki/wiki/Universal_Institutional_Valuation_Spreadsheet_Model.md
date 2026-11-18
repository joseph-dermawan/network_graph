# Universal Institutional Valuation Spreadsheet Model (`Universal_Institutional_Valuation_Spreadsheet_Model.md`)

This page documents the **Universal Institutional Valuation Spreadsheet Model**, created as part of Phase 2 of the master roadmap and replicated live in both **Microsoft Excel (`.xlsx`)** and **Google Sheets (`gws`)**.

---

## 🌐 1. Live Google Sheets & File References

* **Google Sheets Live Model:** [Universal Institutional Valuation Model (Google Sheets)](https://docs.google.com/spreadsheets/d/1wBFDDikiaw-9R-xu6ZKVLz-So3Ij2XNDnPtf951yF6k/edit#gid=0)
  * **Spreadsheet ID:** `1wBFDDikiaw-9R-xu6ZKVLz-So3Ij2XNDnPtf951yF6k`
* **Local Excel Workbook:** [Universal_Institutional_Valuation_Model.xlsx](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/Universal_Institutional_Valuation_Model.xlsx)
* **Master Python Build Scripts (Stored in `ARCHIVE/`):**
  * [build_universal_valuation_model.py](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ARCHIVE/build_universal_valuation_model.py) – Local openpyxl Excel compiler.
  * [populate_gsheet_valuation_full.py](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ARCHIVE/populate_gsheet_valuation_full.py) – Google Sheets API batch uploader (1,035 live formulas).
  * [format_gsheet_valuation.py](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ARCHIVE/format_gsheet_valuation.py) – Google Sheets cell styling & layout renderer (81 formatting rules).
  * [test_gsheet_setup.py](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ARCHIVE/test_gsheet_setup.py) – Google Sheets tab setup script.


---

## 🏛️ 2. Architectural Blueprint & 7-Tab Structure

The workbook is structured into 7 interlinked sheets:

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                           7-TAB VALUATION WORKBOOK LAYOUT                                │
│                                                                                          │
│ 1. [00_DASHBOARD] ──────────► Executive Target Price Bridge & Investment Recommendation  │
│ 2. [01_INPUTS_ASSUMPTIONS] ─► Central Input Command Sheet (Yellow Fills #FFFFCC)           │
│ 3. [02_NORMALIZATION] ──────► Capitalized R&D & Operating Lease Debt Converters           │
│ 4. [03_WACC_CREDIT] ────────► Moody's Synthetic 6-Metric Rating Grid & Hamada WACC        │
│ 5. [04_PRO_FORMA_DCF_10YR] ─► 10-Yr Unlevered FCFF Schedule & Intrinsic Share Price       │
│ 6. [05_FORENSIC_HEALTH] ────► DuPont 5-Point ROE Breakdown & Altman Z-Score Model         │
│ 7. [06_LIQUIDATION_FLOOR] ──► Asset Haircut Net Recovery Liquidation Downside Floor       │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 3. Detailed Tab Descriptions & Key Formulas

### Tab 1: `00_DASHBOARD`
* **Executive Summary Hook:** Displays current share price vs baseline DCF target intrinsic price.
* **Scenario Matrix:** Computes Bear Case Target Price (`=Baseline * 0.80`) and Bull Case Target Price (`=Baseline * 1.25`).
* **Margin of Safety:** `=(Target - Current) / Target`.
* **Recommendation Assessor:** `=IF(Target > Current * 1.15, "STRONG BUY", IF(Target > Current, "BUY", "HOLD / OVERVALUED"))`.

### Tab 2: `01_INPUTS_ASSUMPTIONS`
* Central repository for company inputs (Company Name, Ticker, Current Price, Share Count, Risk-Free Rate $R_f$, ERP, Peer Unlevered Beta $\beta_U$, Tax Rate).
* Historical 3-statement line items (Revenue, COGS, SG&A, Reported EBIT, Interest, Taxes, Assets, Debt, Equity, CapEx, D&A, $\Delta NWC$).
* Off-balance-sheet R&D history (5 years) and Operating Lease commitment schedule (Years 1–6+).
* 10-year revenue growth and operating margin forecast drivers.

### Tab 3: `02_NORMALIZATION_CONVERTERS`
* **R&D Capitalization Converter:** Converts historical expensed R&D into a capitalized intangible Research Asset ($n=5\text{ years}$ amortizable life). Computes adjusted EBIT add-back (`=Reported EBIT + R&D_t1 - Amortization`).
* **Operating Lease Debt Converter:** Discounts 6-year lease commitments at pre-tax cost of debt ($K_d$) to derive present value of Lease Debt (`=SUM(PV Year 1..6+)`) and adds to reported debt.

### Tab 4: `03_WACC_CREDIT_ENGINE`
* **Moody's Synthetic Credit Matrix:** Evaluates 6 ratios (Interest Coverage, Debt/Equity, ROA, Asset Coverage, Profitability, Current Ratio) to assign synthetic credit rating (e.g. Baa2) and default spread (1.80%).
* **Pre-Tax Cost of Debt ($K_d$):** `=Risk_Free_Rate + Default_Spread`.
* **Hamada Beta Re-levering ($\beta_L$):** `=\beta_U * (1 + (1 - Tax_Rate) * (Debt / Equity))`.
* **Blended WACC:** `=(Equity_Weight * Cost_of_Equity) + (Debt_Weight * After_Tax_Cost_of_Debt)`.

### Tab 5: `04_PRO_FORMA_DCF_10YR`
* 10-year pro-forma income statement, operating margins, NOPAT (`=EBIT * (1 - Tax_Rate)`), Sales-to-Capital reinvestment (`=Incremental_Revenue / Sales_to_Capital`), and Unlevered FCFF (`=NOPAT - Reinvestment`).
* Terminal Value via Gordon Growth method ($g = R_f$, stable reinvestment $= g / \text{ROIC}_{\text{stable}}$).
* Enterprise Value to Equity Value Bridge and Implied Baseline Target Share Price (`=Equity_Value / Shares`).

### Tab 6: `05_FORENSIC_HEALTH`
* **DuPont 5-Point ROE Decomposition:** Tax Burden $\times$ Interest Burden $\times$ Operating Margin $\times$ Asset Turnover $\times$ Financial Leverage.
* **Altman Z-Score Distress Model:** Evaluates $X_1$ to $X_5$ ratios to assign bankruptcy zone status (`SAFE ZONE` vs `GREY ZONE` vs `DISTRESS ZONE`).

### Tab 7: `06_LIQUIDATION_FLOOR`
* Asset haircut table (Cash: 100%, Receivables: 85%, Inventory: 65%, PPE: 35%, Research Asset: 10%).
* Net recoverable proceeds minus total liabilities to derive worst-case investor liquidation floor price per share.

---

## 🎨 4. Institutional Color & Formatting Standards

* **`#FFFFCC` Fill / Blue Text (`#0000FF`):** Hardcoded Input Cells (Edit for any stock).
* **`#FFFFFF` Fill / Black Text (`#000000`):** Evaluated Formulas.
* **`#E2EFDA` Fill / Dark Green Text (`#276749`):** Calculated Targets & Valuations.
* **`#0F172A` / `#1E293B` Fills / White Text:** Header Titles & Section Banners.

---

## 🔗 Related Wiki Pages
* [[Valuation_Links_Directory]]: Master URL catalog for spreadsheets and resources.
* [[damodaran_ginzu_dissection]]: Blueprint equations for Damodaran Ginzu converter logic.
* [[model_valuation]]: 10-step master institutional valuation framework.
* [[log]]: Activity timeline.
