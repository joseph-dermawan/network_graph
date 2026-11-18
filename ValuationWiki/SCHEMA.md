# ValuationWiki Schema & LLM Agent Operating Guidelines

Welcome to **ValuationWiki**, an institutional-grade knowledge compiler and valuation engine built using the **Karpathy LLM Wiki Pattern**. This directory sits between raw, immutable financial sources (SEC filings, FactSet data models, PDF reports) and the analyst, serving as a persistent, compounding knowledge base.

---

## 🏛️ Architecture Overview

The knowledge base consists of three distinct layers:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. RAW SOURCES (ValuationWiki/sources/)                                │
│    • Immutable source files (PDFs, SEC filings, FactSet exports, etc.)  │
│    • Read-only source of truth; never modified by the LLM agent.       │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 2. THE WIKI (ValuationWiki/wiki/)                                       │
│    • Interlinked markdown pages owned and maintained by the LLM agent. │
│    • Contains entity pages, valuation models, thesis drivers, and logs. │
│    • Obsidian-compatible wiki-links ([[Page_Name]]) & markdown links.  │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ 3. THE SCHEMA (ValuationWiki/SCHEMA.md)                                 │
│    • Configuration & operating standards for LLM agents.               │
│    • Ingestion, querying, modeling, visual rendering, and lint rules.  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ LLM Agent Conventions & Rules

When acting as a programmer/maintainer over **ValuationWiki**, the LLM agent MUST obey the following strict rules:

### 1. Financial Precision & Anti-Hallucination
* **No Superficial Fallbacks:** Never hardcode dummy numbers or swallow mathematical exceptions. Every financial metric (EBITDA, NOPAT, FCFF, WACC, Beta) must trace directly to SEC filings, FactSet exports, or exact formula derivations.
* **Exact Multiples & Shares:** Diluted share count = **36.55M**; Cash = **$633.56M**; Debt = **$2.52M**; Current Stock Price = **$218.73**.
* **Formula Syntax in OpenPyXL:** Always begin formula strings with `=` (e.g. `='INPUT'!B12+...`). Never write naked string expressions like `('INPUT'!B12+...)` which evaluate to `#VALUE!` or `#REF!` in Excel.
* **Row Offset Verification:** When generating background calculation sheets (like `SENSITIVITY_ENGINE`), explicitly trace row indices. Verify that Terminal Value references the Year 10 NOPAT row (Row 72) rather than Year 0 NOPAT (Row 42).

### 2. Markdown & Interlinking Rules
* **Wiki-Links:** Use Obsidian-style links `[[Page_Name]]` or standard markdown links `[Page Name](file:///path/to/page.md)` for cross-referencing between pages.
* **Header Hierarchy:** Follow strict `# Title`, `## Section`, `### Subsection` structure.
* **Citations:** Every claim, growth rate, or margin target must cite its authoritative source (e.g., *SEC Form 10-Q Q1 FY26*, *FactSet POWL-US.xlsx*, *Damodaran ERP 2026*).

### 3. Matplotlib & Data Visualization Standards
* **Brand Color Palette:** Primary Base Color = **`#0B5A3D`** (Powell Forest Green).
* **Secondary Colors:** Pale Green (`#DCFCE7`), Dark Slate (`#334155`), Accent Amber (`#D97706`), Accent Red (`#DC2626`), Gray Background (`#F8FAFC`).
* **Sidebar Standard Width:** Canvas width = **5.2 inches** (`figsize=(5.2, H)`), DPI = **300**.
* **Clean Header Layout:** Remove top plot titles (`ax.set_title` removed) when building narrow sidebar graphics to maximize vertical plot space.
* **Source Footers:** Every figure must include an italicized footnote: `Source: Unlimited Leverage` or explicit data provider.

---

## 🔄 Core Operating Workflows

### 📥 1. Ingestion Workflow
When a new document (e.g., quarterly SEC 10-Q, broker report, transcript) is dropped into `ValuationWiki/sources/`:
1. Read the source completely without truncation.
2. Discuss key takeaways, financial deltas, and strategic shifts with the user.
3. Create a new source summary page in `wiki/` (e.g. `wiki/Source_Q2_2026_10Q.md`).
4. Update relevant topic and entity pages across `wiki/` (e.g. update `DCF_Valuation_Model.md` and `WACC_Cost_of_Capital.md`).
5. Update `wiki/index.md` catalog and append an entry to `wiki/log.md`.

### 🔍 2. Query & Synthesis Workflow
When answering complex valuation or strategic queries:
1. Consult `wiki/index.md` first to locate all relevant pages.
2. Read the interlinked wiki pages and synthesize a comprehensive markdown response.
3. If the query yields a new persistent insight (e.g., a new sensitivity matrix or peer comparative analysis), save the output as a new page in `wiki/` and update `index.md`.

### 🧹 3. Lint & Health-Check Workflow
Periodically run health-checks over `ValuationWiki/`:
* Check for orphaned pages with no inbound links.
* Identify contradictions between historical financial filings and forward model projections.
* Verify that all figures in `output_figure/` match the evaluated figures in `powell_valuation_model_final.xlsx`.

### 🔄 4. Continuous Conversation & Link Directory Ingestion Protocol
* **Automatic Session Ingestion:** Every conversation turn involving valuation models, financial scripts, strategy logic, or dataset ingestion MUST be recorded into `ValuationWiki/wiki/log.md`.
* **Link Directory Maintenance:** All URLs (Google Sheets models, Damodaran courses, SEC filings, GitHub repositories, and local workspace artifacts) MUST be cataloged in `ValuationWiki/sources/valuation_links_directory.yaml` and interlinked in `ValuationWiki/wiki/Valuation_Links_Directory.md`.

### 📦 5. Repository Cleanliness & Archival Protocol
* **Archiving Run-Off Scripts:** To prevent clutter in the root and project directories, any single-use scripts, helper tools, test runs, or intermediate data build scripts MUST NOT be left loose.
* **Archive Storage:** Move all important run-off scripts into an `ARCHIVE/` subfolder (e.g., `ARCHIVE/` at workspace root or `POWELL/ARCHIVE/`).
* **Preservation Policy:** Prefer archiving over deleting scripts to preserve execution history and auditability.


