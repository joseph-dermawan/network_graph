---
name: curriculum-extraction
description: Comprehensive procedural workflow for extracting, deconstructing, and synthesizing academic lecture slides, course materials, and financial curricula into institutional wiki documentation. Use whenever processing lecture slide decks, extracting course concepts, building curriculum study guides, or expanding documentation with in-depth mathematical derivations, numerical walkthroughs, and case studies.
---

# Academic & Curriculum Extraction Methodology Guide
## Procedural Workflow for Converting Raw Lecture Materials into Institutional Documentation

This skill outlines the standard operating procedure (SOP) for extracting, structuring, and synthesizing educational slide decks, lecture notes, and financial course curricula into rigorous, institutional-grade documentation. It defines the end-to-end extraction pipeline, progressive disclosure practices, mathematical formalization rules, case study decomposition methods, and repository persistence protocols.

---

## 🎯 1. Core Objective & Scope

The goal of this procedure is to transform unstructured, fragmented, or bullet-heavy lecture slides into clean, self-contained, and mathematically complete reference documentation without verbatim copying.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                          5-PHASE EXTRACTION LIFECYCLE                                  │
│                                                                                        │
│ [Phase 1: Intake & Pre-flight] ──► Inspect files, count assets, enforce .gitignore     │
│                                              │                                         │
│                                              ▼                                         │
│ [Phase 2: Pedagogical Deconstruction] ─► Map chronological sessions to thematic modules│
│                                              │                                         │
│                                              ▼                                         │
│ [Phase 3: Deep Technical Extraction] ──► Formulate derivations, cases & lookup grids   │
│                                              │                                         │
│                                              ▼                                         │
│ [Phase 4: Institutional Packaging] ────► Markdown styling, formula checks, auditing    │
│                                              │                                         │
│                                              ▼                                         │
│ [Phase 5: Wiki Ingestion & Archival] ──► Log timeline, update catalogs & archive runs  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 Phase 1: Intake, Cataloging & Pre-flight Inspection

Before reading or processing lecture slide files:

1. **Inventory & Asset Mapping:**
   * Scan the target reference directory to catalog all files (PDFs, PPTXs, spreadsheets, transcripts).
   * Note the numbering scheme, total slide counts, session splits, and auxiliary notes.
2. **Repository Cleanliness Check:**
   * Ensure large raw reference files (e.g. `references/`, slide downloads) are explicitly added to `.gitignore` to prevent repository bloat and accidental version control tracking.
3. **Extraction Mode & Compliance Check:**
   * Verify intellectual property boundaries: Do **NOT** perform raw verbatim copy-pasting of protected third-party presentation text.
   * Plan for **original synthesis**: Rewrite, derive, and explain all concepts, formulas, and frameworks in complete, authoritative technical language.

---

## 🗺️ Phase 2: Pedagogical Deconstruction & Modular Theming

Do not process lectures strictly as isolated, fragmented slide decks. Deconstruct the entire syllabus into logical thematic modules:

1. **Identify the Core Thematic Pillars:**
   * Group sequential sessions into coherent conceptual blocks (e.g., Foundations $\rightarrow$ Cost of Capital $\rightarrow$ Accounting Normalization $\rightarrow$ Cash Flows $\rightarrow$ Terminal State $\rightarrow$ Special Situations $\rightarrow$ Relative Valuation).
2. **Generate the Master Curriculum Outline:**
   * Create an initial high-level curriculum outline file (e.g., `curriculum_outline.md`).
   * For each module, list:
     * Module Name & Session Range.
     * Core Pedagogical Questions Addressed.
     * Foundational Principles Covered.
     * Required Input Data & Practical Modeling Takeaways.
3. **Establish User Alignment:**
   * Present the proposed module-by-module execution plan to the user.
   * Confirm the scope, depth, and priority order before generating full technical documentation.

---

## 🔬 Phase 3: Deep Technical Extraction & Expansion Protocol

When generating technical documentation for each module, execute the following deep extraction standards. If the user requests **more in-depth formulas, calculations, or case studies**, rigorously apply the enhancement protocols below.

### Step 3.1: Mathematical Formalization & Complete Equation Derivations
Never leave formulas as casual text descriptions or simplified approximations.
* **Full Variable Specification:** Define every variable, subscript, time index, and parameter in LaTeX notation.
* **Step-by-Step Derivation:** Write out the complete mathematical steps showing how the formula transitions from first principles to the final operational equation.
* **Accounting & Modeling Reconciliation:** Show how accounting line items map directly into the mathematical variables.

### Step 3.2: Concrete Numerical Walkthroughs & Worked Calculations
Every abstract formula must be accompanied by an end-to-end numerical calculation:
1. State the baseline assumptions and sample company input numbers clearly.
2. Show each intermediate calculation step with explicit arithmetic (e.g., step 1, step 2, step 3).
3. Compute the final output metric and explain its economic interpretation.
4. Contrast the result against standard rule-of-thumb benchmarks to illustrate reasonableness.

### Step 3.3: Case Study & Qualitative Narrative Decomposition
To capture the real-world application of the lecture material:
1. **Identify the Real-World Entity / Situation:** Extract the primary company, market event, or asset discussed in the lecture.
2. **Deconstruct the Narrative Variants:**
   * Break down how different strategic assumptions (e.g., conservative niche vs. aggressive platform expansion) impact the addressable market (TAM), market share, operating margins, and capital intensity.
3. **Demonstrate Valuation Sensitivity:** Show quantitatively how shifting the narrative directly moves the intrinsic target valuation.

### Step 3.4: Reference Tables, Lookup Grids & Empirical Matrices
When lectures reference empirical benchmark tables, rating grids, or lookup matrices:
* Reconstruct the full benchmark grid in clean Markdown table format.
* Include all classification thresholds, coverage bands, and corresponding spreads or multipliers.
* Document segment-specific distinctions (e.g., large-cap vs. small-cap parameters, mature vs. emerging market criteria).

### Step 3.5: Practitioner Traps & Model Audit Checklists
Identify the subtle errors, conceptual fallacies, and spreadsheet bugs highlighted by the instructor:
* **The Conceptual Fallacy:** Clearly explain the intuitive error analysts make in practice.
* **The Mathematical Consequence:** Demonstrate how the error distorts the output (e.g., artificially deflating discount rates or double-counting risk).
* **The Correct Institutional Treatment:** Provide the concrete modeling rule to prevent the mistake.

---

## 📦 Phase 4: Institutional Packaging & Document Architecture

Structure each module documentation file using standard institutional design patterns:

1. **Header Block & Meta Information:**
   * Clear title, module numbering, session coverage, and executive overview.
2. **Visual Workflow & Architecture Diagrams:**
   * Include ASCII or Mermaid flowcharts visualizing the pipeline, decision trees, or equation dependencies.
3. **Typographic & Notation Consistency:**
   * Standardize financial notations ($R_f, ERP, CRP, \beta_U, \beta_L, K_e, K_d, WACC, FCFF, NOPAT$).
   * Use formatted markdown callouts (`> [!NOTE]`, `> [!IMPORTANT]`, `> [!TIP]`) to highlight critical rules.
4. **Self-Contained Completeness:**
   * Ensure that an analyst reading the file can implement the financial model directly in Excel, Python, or Google Sheets without needing to consult external slides.

---

## 🗄️ Phase 5: Wiki Ingestion, Directory Cataloging & Archival

Upon completing each module extraction:

1. **Wiki Interlinking & Catalog Updates:**
   * Link the newly created module document in the master index (`index.md`) and curriculum outline.
   * Add cross-references to existing entity pages and spreadsheet models.
2. **Central Links & Resources Directory Maintenance:**
   * Catalog all newly referenced URLs, sovereign datasets, filing repositories, and local model files into the central YAML link directory (`valuation_links_directory.yaml`) and Markdown directory (`Valuation_Links_Directory.md`).
3. **Append Activity Timeline:**
   * Log the extraction event in the chronological activity log (`log.md`) with date, action type, documents generated, and core methodologies synthesized.
4. **Workspace Cleanliness & Run-Off Archiving:**
   * Verify that no temporary scripts, scratch files, or test runners remain loose in the workspace root.
   * Move all single-use code and execution run-offs into the designated `ARCHIVE/` folder.

---

## 🔄 Phase 6: Progressive Disclosure & Iterative User Alignment

When interacting with the user during a multi-session curriculum extraction:

1. **Iterate Module by Module:**
   * Deliver one complete module at a time rather than dumping an entire course at once.
2. **Review & Expand on Demand:**
   * Present the synthesized module and actively solicit user feedback on depth, coverage, and specific technical areas.
   * When the user requests more granular calculations, deeper mathematical proofs, or additional numerical case studies, execute the **Deep Technical Extraction Protocol (Phase 3)** to upgrade the module to a Master Edition.
3. **Confirm Readiness Before Advancement:**
   * Seek explicit user confirmation before advancing to the subsequent curriculum module.
