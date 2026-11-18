# Institutional Dashboard UI & Data Visualization Design Standard

This document establishes the **default institutional design language and data visualization standard** for all interactive valuation dashboards, case files, financial statement viewers, and research tools across the workspace.

---

## 🏛️ 1. Core Philosophy: Editorial Elegance & "Show Don't Tell"

Financial research and valuation modeling are cognitively demanding. Complex spreadsheets and hundreds of pages of filings should not be recreated as dense, noisy data dumps.

Our default interface philosophy requires:
1. **Editorial Calm:** Warm, legible surfaces modeled after high-end economic periodicals and classic investment banking memoranda rather than neon terminal software.
2. **Minimal Cognitive Friction:** Numbers are formatted with deliberate institutional hierarchy. Quantitative proofs are displayed front and center; legal citations and qualitative details are available on demand via non-intrusive slide-overs and modal pop-ups.
3. **Show Don't Tell:** Financial mechanics (such as unit cost decoupling, operating leverage, and margin inflection) are visualized through minimalist dual-axis charts alongside audited schedules.

---

## 🎨 2. Design Tokens & Palette Specifications

### A. Surface Canvas Tokens (The Beige Standard)
All dashboards must employ the **warm beige editorial canvas** as the default foundation:

```css
:root {
    /* Canvas & Surfaces */
    --bg-page: #FAF7F2;          /* Primary Warm Beige Canvas */
    --bg-card: #FFFFFF;          /* Pure White Card Containers */
    --bg-subtle: #F4EFEB;        /* Subtle Row / Header Wash */
    --bg-active: #EFE8DF;        /* Active Tab / Selected Surface */
    
    /* Structural Borders */
    --border-main: #E5E0D8;      /* Default Card & Cell Dividers */
    --border-dark: #D8D2C5;      /* Header Bottom & Emphasized Dividers */
    
    /* Typography Palette */
    --text-primary: #1C1917;    /* Charcoal Black (Newsprint Primary) */
    --text-secondary: #57534E;  /* Warm Slate (Body & Explanations) */
    --text-muted: #8C867A;      /* Muted Sand (Metadata, Timestamps) */
    
    /* Semantic Status Accents */
    --accent-green: #15803D;    /* Positive Margins, Outperformance */
    --accent-green-light: #DCFCE7;
    --accent-red: #B91C1C;      /* Operating Losses, Drawdowns */
    --accent-red-light: #FEE2E2;
}
```

### B. Thematic Accent Color Liberty
While the background canvas, card architecture, borders, typography, and Chart.js design framework must **strictly adhere** to this default standard, analysts and project owners have **full liberty in selecting the thematic accent color** to match the sector, entity, or thesis:

| Entity / Asset Class | Recommended Theme Accent | Hex Code | Semantic Application |
| :--- | :--- | :--- | :--- |
| **Anthropic / Frontier AI** | Warm Terracotta / Amber | `#B45309` (`#FEF3C7`) | S-1 Prospectus Highlights, Tickers, Golden Shares |
| **Powell Industries / Energy** | Powell Forest Green | `#0B5A3D` (`#DCFCE7`) | Industrial Capacity, Capital Restructuring |
| **Semiconductors / Hardware** | Deep Electric Indigo | `#4338CA` (`#EEF2FF`) | Silicon Wafers, Hyperscaler CapEx |
| **Fintech / Payment Rails** | Cyber Slate / Cyan | `#0E7490` (`#CFFAFE`) | Transaction Velocity, Settlement Rails |
| **Macro / Distressed Debt** | Classic Crimson / Rust | `#991B1B` (`#FEE2E2`) | CDS Spreads, Synthetic Ratings, Haircut Floors |

---

## 🔤 3. Typographic Triad

Every view must maintain a disciplined typographic separation across three distinct typefaces:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TYPOGRAPHIC HIERARCHY                           │
│                                                                        │
│  1. EDITORIAL SERIF   ──► 'Newsreader', Georgia, serif                 │
│                           Document titles, section headers, quotes     │
│                                                                        │
│  2. CLEAN SANS        ──► 'Inter', system-ui, sans-serif               │
│                           Navigation tabs, UI buttons, descriptions    │
│                                                                        │
│  3. FINANCIAL MONO    ──► 'JetBrains Mono', monospace                  │
│                           All numbers, formulas, dates, tickers        │
└────────────────────────────────────────────────────────────────────────┘
```

* **Newsreader (Serif):** Used for entity titles (`h1`), module headers (`h2`, `h3`), and blockquoted prospectus excerpts. Provides institutional gravitas.
* **Inter (Sans):** Used for navigation tabs, interactive pills, micro-labels, and explanatory paragraphs. Ensures effortless UI readability.
* **JetBrains Mono (Monospace):** Non-negotiable for all financial statements, multiples, percentages, dates, and tabular columns. Tabular figures prevent misalignment when numbers change across quarters.

---

## 📊 4. Financial Statement Standard (SEC EDGAR & IB Conventions)

All financial statement tables (Income Statement, Balance Sheet, Cash Flow) must follow standard accounting presentation:
1. **Row Hierarchy:**
   * Category headers: Uppercase, bold, slight background tint (`#F4EFEB`), full row width.
   * Standard line items: Indented 24px (`.row-indent-1`) or 36px (`.row-indent-2`).
   * Subtotals: Top and bottom 1px border (`#D8D2C5`), bold text, subtle highlight (`#FAF6EF`).
   * Summary totals (e.g. Net Loss, Total Assets): Double bottom border (`3px double #1C1917`), bold text.
2. **Negative Figure Formatting:**  
   Negative numbers must **always** be wrapped in parentheses `(551)` rather than preceded by hyphens `-551`, and color-coded with subtle muted crimson (`#B91C1C`).
3. **Alignment Discipline:**  
   Line item descriptions are left-aligned; all numeric columns are strictly right-aligned with monospace digits.

---

## 📈 5. Chart.js Visualization Blueprint

Data visualizations must seamlessly blend into the beige paper aesthetic. Standard Chart.js configuration rules:

```javascript
// Universal Institutional Chart.js Defaults
const chartConfig = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            align: 'end',
            labels: {
                font: { family: "'JetBrains Mono', monospace", size: 10.5 },
                boxWidth: 12,
                usePointStyle: true,
                color: '#57534E'
            }
        },
        tooltip: {
            backgroundColor: '#FFFFFF',
            titleColor: '#1C1917',
            bodyColor: '#57534E',
            borderColor: '#D8D2C5',
            borderWidth: 1,
            titleFont: { family: "'Newsreader', Georgia, serif", size: 13, weight: 'bold' },
            bodyFont: { family: "'JetBrains Mono', monospace", size: 11 },
            padding: 10
        }
    },
    scales: {
        x: {
            grid: { display: false },
            ticks: { font: { family: "'JetBrains Mono', monospace", size: 10.5 }, color: '#57534E' }
        },
        y: {
            grid: { color: '#ECE7DE' },
            ticks: { font: { family: "'JetBrains Mono', monospace", size: 10 }, color: '#57534E' }
        },
        y1: {
            // Secondary dual-axis
            position: 'right',
            grid: { drawOnChartArea: false },
            ticks: { font: { family: "'JetBrains Mono', monospace", size: 10 }, color: '#B45309' }
        }
    }
};
```

* **Palette Matching:** Primary bar volume must use charcoal (`#1C1917`) or muted sand (`#D8D2C5`). Trend/margin lines must use the project theme accent (`#B45309`) with a white circular point border (`pointBackgroundColor: '#FFFFFF'`).
* **Dual-Axis Scaling:** When plotting absolute dollar volume alongside margin percentages, the secondary axis must disable canvas gridlines (`drawOnChartArea: false`) to avoid clutter.

---

## 🗂️ 6. Case File Consolidation Standard

Each covered entity in `ERVIS/projects/{ASSET_CLASS}/{TICKER}/` must feature a **Master Project Case File** (`anthropic_case_file.html` / `index.html`) serving as the central institutional landing pad, connecting:
1. **Filing & Prospectus Intelligence:** Deep-dive analysis of primary SEC disclosures, capitalization, and qualitative risk audits.
2. **Damodaran Valuation Reader:** Granular spreadsheet mirror displaying bottom-up formulas, converters, and cost-of-capital schedules.
3. **ERVIS Terminal Cockpit:** Master valuation cockpit featuring the 10-year DCF schedule, scenario fragility analysis, and macro ingestion.

---

## 🔗 Related Wiki Documentation
* [[Report_Visuals_Catalog]]: Visual catalog for Powell Industries and legacy asset graphics.
* [[ERVIS_Bloomberg_Terminal_and_Workstation_Architecture]]: Terminal architecture and command mnemonics.
* [[Universal_Institutional_Valuation_Spreadsheet_Model]]: Master 7-tab spreadsheet specifications.
* [[index]]: ValuationWiki master directory.
