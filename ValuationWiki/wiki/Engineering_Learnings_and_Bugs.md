# Engineering Learnings, Debugging Post-Mortems & Process Reflections

This document captures all technical lessons, financial modeling bugs, graphic rendering edge cases, and process authentications encountered during the building of the **Powell Industries Equity Research & Valuation Engine**.

---

## 🐞 1. The OpenPyXL Formula String Bug (`#REF!` Error Post-Mortem)

### Symptom:
During the initial build of `powell_valuation_model_final.xlsx`, cells in the `SENSITIVITY_ENGINE` tab displayed `#REF!` or evaluated as raw text strings rather than numeric dollar values.

### Diagnosis & Root Cause:
Using `python3 -c "import openpyxl..."`, we inspected the raw cell contents of line 282 and 356 in `build_powell_final_model.py`. The formula string string for margin calculation was written as:
```python
# BROKEN CODE:
margin_t_se = f"'INPUT'!B12+..." # Missing leading '=' character!
```
Because the string omitted the leading `=` sign, OpenPyXL wrote `'INPUT'!B12+...` as a literal text string into the cell. Downstream arithmetic formulas expecting numbers attempted to add text to numbers, triggering `#VALUE!` and `#REF!` cascading errors.

### Resolution & Rule Established:
Added the missing `=` character: `f"='INPUT'!B12+..."`.
* **Permanent Rule (SCHEMA):** *Every formula string assigned to an OpenPyXL cell MUST begin with an explicit `=` character.*

---

## 📐 2. Sensitivity Row Index Alignment Shift

### Symptom:
In `SENSITIVITY_ENGINE`, calculated terminal values differed from the main `DCF` tab.

### Diagnosis & Root Cause:
The background calculation engine generated 10-year pro-forma income statement blocks for each of the 9 sensitivity combinations. The formula for Terminal Value referenced row 42 (Year 0 NOPAT) instead of row 72 (Year 10 NOPAT) because the loop index offset did not account for the 3-line header gap between tables.

### Resolution & Rule Established:
Created `calc_matrix_exact.py` to print exact row indices for every cell in the sensitivity block. Aligned Year 10 Terminal Value formula to explicitly reference Row 72 (`NOPAT_Y10`).
* **Permanent Rule (SCHEMA):** *Always run explicit python test scripts (`audit_final_model.py`) to print formula strings and evaluated values before declaring model completion.*

---

## 📊 3. Data Visualization & Matplotlib Design Edge Cases

### Edge Case A: Dual Y-Axis Scale Mismatch (Figure 4.1)
* **Problem:** Plotting Global AI CapEx ($153B–$318B) and Powell Backlog ($1.3B–$2.4B) on dual y-axes in a single bar chart created confusing bar heights that lacked a common baseline.
* **Fix:** Converted Figure 4.1 into a clean, side-by-side 2-panel subplot (Subplot A for AI CapEx, Subplot B for Powell Backlog) and later focused Figure 4.1 purely on POWL Total Backlog Surge ($1.3B $\rightarrow$ $1.8B $\rightarrow$ $2.4B).

### Edge Case B: Text Clipping on Pie Chart Labels (Figure 4.9)
* **Problem:** In Figure 4.9, the top label `"Oil & Gas / Petrochem (38%)"` was clipped at the upper edge of the image canvas.
* **Fix:** Wrapped text onto three lines (`Oil & Gas /\nPetrochemical\n(38%)`), set `labeldistance=1.18`, and expanded canvas margins (`left=0.18, right=0.82`).

---

## 🛡️ 4. Process Authenticity vs. Generic Template Jargon

### Insight:
Initially, report writeups referenced generic screening tools like "Bloomberg Terminal S&P Capital IQ Screener".

### User Directive & Correction:
The user explicitly instructed: *"just keep it authentic and honest to our own process... don't just anyhow lift, like how is this true Screening Process... do we really do this? id remember doing bloomberg"*.

### Correction Applied:
Replaced template text with our actual project research steps: SEC Form 10-Q/10-K filings, FactSet `POWL-US.xlsx` workbook exports, Yahoo Finance 5-year monthly regression beta, and Damodaran 2026 ERP benchmarks.

---

## 💥 5. Ticker Normalization & `ZeroDivisionError` Bug Post-Mortem

### Symptom:
Typing `R.R` (or any unknown/unprovisioned ticker) in the ERVIS terminal command bar crashed the entire Textual runtime with:
```text
ZeroDivisionError: float division by zero
  in render_dcf_screen (renderer.py:497)
    table.add_row("10-Year Discrete DCF Fair Value", format_currency(dcf, curr), f"Implies {((dcf - spot)/spot)*100:+.1f}% intrinsic gap vs spot")
```

### Diagnosis & Root Cause:
1. `app.py` allowed any input $\le 5$ characters to set `self.active_ticker = candidate_ticker`.
2. When the user typed `R.R`, it was not recognized as the canonical key `RR` in the database, returning `spot_price = None` / `0.0`.
3. In `render_dcf_screen`, the formula `((dcf - spot) / spot)` had no `spot > 0` validation, triggering an unhandled `ZeroDivisionError`.

### Resolution & Rules Established:
1. **Canonical Ticker Aliasing**: Added `resolve_ticker(raw_ticker)` with mapping table (`R.R`, `RR.`, `RYCEY` $\to$ `RR`, `GOOG` $\to$ `GOOGL`, `FB` $\to$ `META`, `TSMC` $\to$ `TSM`).
2. **Defensive Division Guards**: All valuation gap calculations wrapped in `if spot > 0 else "Pending Spot Benchmark"`.
3. **Graceful Coverage Exception View**: When an unknown ticker is requested, render a styled institutional **Coverage Directory Panel** listing active tickers instead of throwing unhandled exceptions.
* **Permanent Rule (SCHEMA):** *Never divide by market price or balance sheet metrics without explicit `val > 0` defensive guards.*

---

## 🖥️ 6. Monospace Text Grids vs. Vector Rendering (Why In-Terminal ASCII Plots Look Wonky)

### Insight:
Attempting to draw a 2D coordinate scatter plot with OLS slope lines inside an 80x25 character terminal produced smeared, jagged lines (`╱╱╱╱╱╱╱╱╱╱`).

### Root Cause Analysis:
1. **Aspect Ratio Distortion**: Monospace terminal characters have a ~2:1 vertical-to-horizontal aspect ratio (characters are twice as tall as they are wide).
2. **Coarse Spatial Resolution**: An 80-column terminal cell grid cannot smoothly plot 156 weekly empirical observations without clustering and stair-step artifacts.
3. **User Feedback**: *"hmm still wonky, maybe can the scatterplot... i want the same terminal style layout and no vibe-coded neone strip design"*.

### Architectural Solution (The Hybrid Terminal Model):
1. **Can the In-Terminal Plot**: Replace the wonky ASCII plot in the terminal `[F9] BETA` tab with a crisp, high-density **CAPM Beta & WACC Sensitivity Matrix** table.
2. **Decouple Deep Graphics**: Create a standalone vector visualization command (`GRPH <GO>` / `[G]`) that renders all 156 points with true continuous coordinate precision in the browser.
3. **Zero Vibe-Coding Doctrine**: The external visualization strictly preserves the Bloomberg Terminal aesthetic: 0px border-radius, strict monospace fonts (`SF Mono`, `Menlo`), solid 1px borders, black background, and zero neon gradient glows.

---

## ⚡ 7. JavaScript Scope Isolation & Unqualified Function Hoisting in Standalone Dashboards

### Symptom:
In `damodaran.html`, upon opening the interactive **★ SCENARIO BUILDER** tab, the intrinsic fair value was frozen at `$0.00 / share`, and all deltas evaluated to zero. The model appeared unresponsive unless manually forced.

### Diagnosis & Root Cause:
Inside the scenario builder's Immediately Invoked Function Expression (IIFE):
```javascript
// BROKEN CODE:
window.syncSlider = function(key, val) { ... };
window.resetAll = function() {
    Object.entries(DEFAULTS).forEach(([k, v]) => {
        const sl = document.getElementById('s_' + k);
        if (sl) { sl.value = v; syncSlider(k, v); } // ReferenceError: syncSlider is not defined!
    });
    window.recompute();
};
```
1. In strict JavaScript execution, assigning `window.syncSlider = function(...)` does NOT create a local variable named `syncSlider` in lexical scope.
2. When `resetAll()` was called upon DOM load, invoking `syncSlider(k, v)` without qualifying `window.` triggered a silent uncaught `ReferenceError: syncSlider is not defined`.
3. Consequently, `recompute()` was never reached, leaving DOM elements at their static placeholder strings (`$0.00`).

### Resolution & Rule Established:
Declare internal functions natively with `function syncSlider(...)` and explicitly bind them to `window` for external inline HTML event handlers (`oninput`, `onclick`):
```javascript
// FIXED CODE:
function syncSlider(key, val) { ... }
function setSlider(key, val) { ... }
function resetAll() { ... }
function recompute() { ... }

window.syncSlider = syncSlider;
window.setSlider  = setSlider;
window.resetAll   = resetAll;
window.recompute  = recompute;
```
* **Permanent Rule (SCHEMA):** *Within standalone HTML application scripts, always define local named function declarations and explicitly export to `window`. Never call unqualified identifiers that are only bound as properties on `window`.*

---

## 📐 8. CSS Grid Blowout & Fluid Viewport Scaling (`minmax(0, 1fr)` vs `1fr`)

### Symptom:
When zooming into the browser (Ctrl+/Cmd+), the Scenario Builder and Thought Process tabs became horizontally "stuck". The right side had excessive empty whitespace, content failed to expand to the edges, and the layout did not match the alignment of the 18-tab top navigation bar (`.sheet-tab-bar`).

### Diagnosis & Root Cause:
1. **CSS Grid `1fr` Minimum Width Trap:** In the CSS Grid specification, `1fr` is shorthand for `minmax(auto, 1fr)`. If any descendant child element (tables, KaTeX equations, or slider ranges) has an intrinsic minimum content width, the `auto` constraint prevents the column from shrinking or scaling flexibly, causing the grid container to overflow or get stuck.
2. **Padding Misalignment:** `.sheet-tab-bar` used `padding: 0 14px`, whereas `.scenario-container` and `.dissection-container` used `padding: 28px 40px 80px`. The 40px left/right margins created an unnatural 26px indent on both sides, visually detaching the content cards from the tab bar.
3. **Workspace Grid Parent Constraint:** The spreadsheet container `<main class="workspace">` had a default side-by-side grid rule (`grid-template-columns: minmax(0, 1fr) 380px`). Without a breakout override, full-page viewports remained trapped inside the left column.

### Resolution & Rule Established:
1. **Defensive Grid Columns:** Replace all instances of raw `1fr` with `minmax(0, 1fr)` across all layout grids (`.scenario-layout`, `.output-top-grid`, `.dissection-steps-grid`). This forces the browser to allow columns to scale down smoothly without blowing out parent containers.
2. **Tab-Bar Padding Parity:** Set `.scenario-container` and `.dissection-container` padding to `16px 14px 60px 14px !important`, achieving exact edge-to-edge alignment with the 14px tab bar.
3. **Workspace Full-View Class:** When switching to full-screen tabs (`__scenario__` or `__dissection__`), apply `.workspace.full-view` (`display: block !important; padding: 0 !important; width: 100% !important; overflow-x: hidden !important;`) to cleanly break out of the spreadsheet split-grid.
* **Permanent Rule (SCHEMA):** *Never use unqualified `1fr` in responsive CSS grid layouts that contain tabular or mathematical data; always specify `minmax(0, 1fr)` to prevent grid blowout.*

---

## 🔗 Related Wiki Pages
* [[Anthropic_IPO_Valuation_Forensics_and_Scenario_Builder]]: Complete forensic breakdown and scenario model.
* [[ERVIS_Bloomberg_Terminal_and_Workstation_Architecture]]: Master architecture and mnemonic specification.
* [[DCF_Valuation_Model]]: Master financial model.
* [[Report_Visuals_Catalog]]: Visual catalog.

