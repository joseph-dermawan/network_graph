# ERVIS Pairing Workflow Protocol (`WORKFLOW_PROTOCOL.md`)
**The 2-to-3-Hour Human-in-the-Loop Co-Worker Pairing Session**

---

## 1. Overview: The Co-Worker Operating Model

In an ERVIS pairing session, the AI agent acts as a **Senior Equity Research Associate**, while the human acts as the **Lead Portfolio Manager / Research Director**. 

Work is not done in a silo. The session proceeds through **5 discrete gates**. At each gate:
1. ERVIS computes mathematical outputs, analyzes SEC filings, and prepares diagnostic exhibits.
2. ERVIS presents structured options, highlighted anomalies, and narrative hypotheses.
3. The human analyst provides domain judgment, selects drivers, debates valuation levers, and authorizes the next phase.

```
[START: TICKER INPUT]
       │
       ▼
[GATE 1: INGESTION & FORENSICS] ────► Human Sign-Off on Restatements (Leases, R&D)
       │
       ▼
[GATE 2: OPERATIONAL DRIVERS]   ────► Human Selects Verified Regressors (R² > 0.85)
       │
       ▼
[GATE 3: WACC & CREDIT RATING]  ────► Human Decides ERM Notch Adjustments & Target D/E
       │
       ▼
[GATE 4: VALUATION & SCENARIOS] ────► Human Approves Strategic Levers & Moat Overrides
       │
       ▼
[GATE 5: PITCH MEMO & VERDICT]  ────► Final Investment Decision & Target Price Sign-Off
```

---

## 2. Minute-by-Minute Session Script

### Phase 1: Ingestion & Recency Audit (Minutes 0:00 – 0:15)
* **Agent Actions:**
  * Connects to SEC EDGAR API and pulls latest 10-K and 10-Q XBRL packages.
  * Queries US Treasury yields (10-Yr $R_f$) and current trading price.
  * Checks filing date against system date (Recency Gate).
  * Audits footnotes for off-balance sheet operating leases and capitalized R&D.
* **Co-Worker Prompt to Human:**
  > *"Filing data for TICKER ingested. Freshness confirmed (Latest 10-Q filed 28 days ago; 10-Yr Treasury yield is 4.58%). R&D is expensed at $450M/yr and operating lease commitments total $1.2B over 5 years. Do you authorize capitalizing R&D over a 5-year straight-line schedule and capitalizing leases at an estimated 5.7% pre-tax cost of debt?"*
* **Gate 1 Exit Criteria:** Human confirms accounting restatements and baseline numbers.

---

### Phase 2: Operational Driver Regressions & Financial Health (Minutes 0:15 – 0:45)
* **Agent Actions:**
  * Gathers historical segment volume metrics from annual reports (e.g., flight handling count, units shipped, backlog).
  * Executes OLS linear regressions against revenue and segment EBIT ($R^2$ calculation).
  * Calculates 5-Point DuPont ROE breakdown over a 5-year history.
  * Computes Altman Z-score components ($X_1$ through $X_5$).
* **Co-Worker Prompt to Human:**
  > *"Econometric regressions complete. Driver A (Backlog Burn Rate) yields R² = 0.89 (statistically significant); Driver B (Gross Headcount) yields R² = 0.42 (rejected). DuPont analysis indicates recent margin compression is operational (EBIT margin fell from 24% to 18%) rather than financial leverage. Altman Z-Score is 3.42 (Safe Zone). Shall we peg pro-forma revenue growth to Driver A at 6.5% CAGR for Years 1–5?"*
* **Gate 2 Exit Criteria:** Human validates verified operational regressors and financial distress safety.

---

### Phase 3: Cost of Capital (WACC) & Credit Synthesis (Minutes 0:45 – 1:05)
* **Agent Actions:**
  * Pulls peer group unlevered betas from global industry database.
  * Solves Hamada equation using company market leverage ($D/E$) and marginal tax rate.
  * Evaluates company metrics across Moody's 6-factor industrial rating grid.
  * Cross-checks synthetic default spread against actual traded corporate bond YTM.
* **Co-Worker Prompt to Human:**
  > *"Base Moody's 6-metric grid evaluates to Baa2 (spread 1.60%). However, given the company's 45% market share, parent backing, and $2B liquidity buffer, I propose an Enterprise Risk Management (ERM) upgrade of +1 notch to Baa1 (spread 1.35%). This gives Ke = 8.20%, Kd = 5.93%, and blended WACC = 7.65%. Do you agree with the ERM notch upgrade?"*
* **Gate 3 Exit Criteria:** Human approves cost of capital assumptions, beta re-levering, and rating adjustments.

---

### Phase 4: Valuation Engine & Scenario Triangulation (Minutes 1:05 – 1:50)
* **Agent Actions:**
  * Populates 10-year DCF schedule using Sales-to-Capital ratio for reinvestment.
  * Builds divisional Sum-of-the-Parts (SOTP) using peer forward EV/EBITDA multiples.
  * Executes 10,000-trial Monte Carlo stochastic simulation.
  * Computes asset-by-asset liquidation haircut downside floor.
* **Co-Worker Prompt to Human:**
  > *"Valuation models compiled:
  > - Base DCF Intrinsic Value: $54.20/share (+22% upside).
  > - SOTP Divisional Value: $58.10/share (+31% upside).
  > - Monte Carlo 10k Trials: Median $53.80/share, Win Rate = 88.4% (> Current Price of $44.50).
  > - Liquidation Floor: $18.40/share (-58% max downside).
  > In the Terminal Year, shall we assume a durable economic moat (Terminal ROIC = 15.0%) or default to Damodaran's zero-excess-return rule (ROIC = WACC = 7.65%)?"*
* **Gate 4 Exit Criteria:** Human decides terminal moat treatment and reconciles DCF vs SOTP weightings.

---

### Phase 5: Pitch Memo, Deliverables & Final Verdict (Minutes 1:50 – 2:20)
* **Agent Actions:**
  * Synthesizes 3 variant view investment theses and identified catalysts.
  * Generates the multi-tab Universal Excel Model (`.xlsx`).
  * Compiles the institutional Bloomberg-styled interactive HTML dashboard.
  * Drafts the 20-page institutional research memorandum.
* **Co-Worker Prompt to Human:**
  > *"All deliverables generated:
  > 1. Universal Excel Model saved to projects/US_EQUITIES/[TICKER]/model.xlsx
  > 2. Interactive Dashboard saved to projects/US_EQUITIES/[TICKER]/dashboard.html
  > 3. Pitch Memorandum drafted with Target Price $55.00 (BUY, +23.6% upside).
  > Please review the final executive summary and approve the target price."*
* **Gate 5 Exit Criteria:** Human gives final authorization on target price and investment rating.

---

## 3. Lifecycle Management: Draft Analysis vs. Published Release

To protect institutional integrity, ERVIS enforces a strict distinction between the **Working Draft Phase** and the **Published Release Phase**:

```
[WORKING DRAFT PHASE]                                    [PUBLISHED RELEASE PHASE]
- Location: projects/[MKT]/[TICKER]/                     - Location: projects/[MKT]/[TICKER]/published/vX.0/
- Scratchpad scripts & trial runs                        - Immutable, clean institutional deliverables
- Rapid parameter changes & iterations                   - Locked model snapshot & publication timestamp
- Unfinalized exploratory numbers                        - Registry updated in company_sheets.yaml
- Bound to active working GSheet                         - Production-ready dashboard & PDF memo
```

### The `publish` Command:
When the analyst and agent align on all valuation levers, the analyst runs:
```bash
./initiate-ervis publish [TICKER] --notes "Q3 2026 Base Valuation Finalized"
```
* **Actions Taken by ERVIS:**
  1. Creates an immutable version directory (`published/v1.0/`, `published/v2.0/`).
  2. Copies clean versions of the HTML dashboard, Excel workbook, and research dossier.
  3. Updates `ERVIS/kb/registry/company_sheets.yaml` with the publication timestamp, final intrinsic value, and investment rating.
  4. Preserves all working draft files and scratch calculations in the working workspace for future longitudinal reference.

---

## 4. Google Drive Address Book & Single-Sheet Binding

To avoid spreadsheet clutter, ERVIS employs a **One-Company, One-GSheet** policy:

* **Binding Google Drive Folder:** Set your shared Google Drive valuation folder once:
  ```bash
  ./initiate-ervis link-drive <GOOGLE_DRIVE_FOLDER_ID>
  ```
* **Persistent Address Book (`ERVIS/kb/registry/company_sheets.yaml`):** Tracks every ticker's unique Google Sheet ID and shareable URL.
* **Idempotent Company Re-Valuation:** When you revisit a company (e.g. running `./initiate-ervis KO` next quarter), ERVIS detects the existing entry, re-opens the bound Google Sheet, and updates the existing tabs rather than creating duplicate files.
* **List Active Portfolio Registry:** Run `./initiate-ervis list` at any time to view all company statuses, valuation outputs, and Google Sheets links.

---

## 5. Gate 4B Extension: The CapEx Payout & Customer ROI Engine

When evaluating capital-intensive technology hardware, cloud hyperscalers, or infrastructure providers (e.g. NVIDIA, Microsoft, Alphabet, Amazon, Meta, Broadcom, TSMC), the analyst can invoke the **CapEx Payout & ROI Engine**:

```bash
./initiate-ervis capex-roi [TICKER]
```

### Analytical Capabilities:
1. **Provider Internal Capital Engine:**
   * CapEx Intensity: $\text{Physical CapEx} / \text{Revenue}$.
   * Free Cash Flow Conversion: $\text{FCF} / \text{CFO}$.
   * Economic Return on Invested Capital: $\text{NOPAT} / \text{Invested Capital}$ (including capitalized R&D).
   * Shareholder Capital Payout: $(\text{Buybacks} + \text{Dividends}) / \text{FCF}$.
2. **Customer CapEx Payout Ratio (CPR / "Hardware Tax"):**
   * Computes the percentage of total customer/hyperscaler CapEx absorbed by the company:
     $$\text{CPR} = \frac{\text{Company Segment Silicon/Cloud Revenue}}{\sum \text{Customer Annual CapEx}}$$
3. **Customer Net Operating Return on Investment ($\text{ROI}_{\text{customer}}$):**
   * Compares incremental customer software revenue (at cloud gross margins) against annual straight-line hardware depreciation over the asset's economic useful life ($L_{\text{useful}} = 3.5\text{ years}$).
4. **Customer Payback Period & Obsolescence Deficit:**
   * Derives payback duration ($T_{\text{payback}}$) and flags the **Hardware Obsolescence Deficit** when $T_{\text{payback}} > L_{\text{useful}}$.
5. **The Break-Even Monetization Gap:**
   * Calculates the required annual enterprise software revenue to deliver an institutional hurdle rate (e.g. 15.0% ROIC) on cumulative hardware purchases.

