import json
import os

with open("ERVIS/projects/US_EQUITIES/ANTHROPIC/scratch_drafts/extracted_model_data.json", "r", encoding="utf-8") as f:
    model_data = json.load(f)

sheets = model_data["sheets"]
methodologies = model_data["methodologies"]

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aswath Damodaran :: Anthropic Valuation Model Breakdown & Methodology Explorer</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-page: #FAF7F2;
            --bg-sheet: #FFFFFF;
            --bg-header: #F2ECE1;
            --bg-hover: #F8F5EE;
            --bg-active: #FFFDF5;
            --border-grid: #E2DDD2;
            --border-header: #D5CFC2;
            --border-active: #B45309;
            --text-main: #1C1917;
            --text-muted: #58544D;
            --text-faint: #8C867A;
            --accent-green: #15803D;
            --accent-green-bg: #F0FDF4;
            --accent-red: #B91C1C;
            --accent-red-bg: #FEF2F2;
            --font-mono: 'JetBrains Mono', monospace;
            --font-serif: 'Newsreader', Georgia, serif;
            --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-page);
            color: var(--text-main);
            font-family: var(--font-sans);
            font-size: 13px;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }

        /* Top Minimalist Header */
        header {
            background: #FFFFFF;
            border-bottom: 1px solid var(--border-grid);
            padding: 16px 28px;
            position: sticky;
            top: 0;
            z-index: 40;
        }

        .header-container {
            max-width: 1680px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            gap: 16px;
        }

        .title-block h1 {
            font-family: var(--font-serif);
            font-size: 20px;
            font-weight: 600;
            color: var(--text-main);
            letter-spacing: -0.01em;
        }

        .title-block p {
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .key-pills {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            font-family: var(--font-mono);
            font-size: 11px;
        }

        .pill {
            background: #FAF7F2;
            border: 1px solid var(--border-header);
            padding: 4px 10px;
            border-radius: 2px;
            color: var(--text-muted);
        }

        .pill strong {
            color: var(--text-main);
        }

        .pill.positive strong {
            color: var(--accent-green);
        }

        .pill.negative strong {
            color: var(--accent-red);
        }

        /* Formula Bar */
        .formula-bar {
            display: flex;
            align-items: center;
            background: #FAF7F2;
            border: 1px solid var(--border-header);
            border-radius: 2px;
            height: 32px;
            font-family: var(--font-mono);
            font-size: 12px;
        }

        .cell-address-box {
            width: 180px;
            padding: 0 12px;
            font-weight: 600;
            color: var(--text-main);
            border-right: 1px solid var(--border-header);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: flex;
            align-items: center;
            height: 100%;
        }

        .fx-indicator {
            padding: 0 10px;
            font-style: italic;
            font-weight: 600;
            color: var(--text-faint);
            border-right: 1px solid var(--border-header);
            height: 100%;
            display: flex;
            align-items: center;
            background: #F2ECE1;
        }

        .formula-input {
            flex: 1;
            padding: 0 12px;
            color: var(--text-main);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* Sheet Tabs */
        .sheet-tab-bar {
            display: flex;
            gap: 2px;
            overflow-x: auto;
            border-bottom: 1px solid var(--border-grid);
            background: #F3EFE6;
            padding: 0 16px;
        }

        .sheet-tab {
            padding: 8px 14px;
            font-size: 12px;
            font-family: var(--font-mono);
            color: var(--text-muted);
            background: transparent;
            border: 1px solid transparent;
            border-bottom: none;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
            outline: none;
        }

        .sheet-tab:hover {
            color: var(--text-main);
            background: #FAF7F2;
        }

        .sheet-tab.active {
            color: var(--text-main);
            background: #FFFFFF;
            border-color: var(--border-grid);
            font-weight: 600;
            border-top: 2px solid var(--border-active);
        }

        /* Main Workspace */
        .workspace {
            max-width: 1680px;
            margin: 0 auto;
            padding: 16px 28px 48px;
            display: grid;
            grid-template-columns: 1fr 420px;
            gap: 24px;
            align-items: start;
        }

        @media (max-width: 1200px) {
            .workspace {
                grid-template-columns: 1fr;
            }
        }

        /* Grid Table Container */
        .grid-container {
            background: #FFFFFF;
            border: 1px solid var(--border-grid);
            border-radius: 2px;
            overflow: auto;
            max-height: calc(100vh - 190px);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }

        table.sheet-table {
            border-collapse: collapse;
            font-family: var(--font-mono);
            font-size: 12px;
            width: 100%;
            table-layout: auto;
        }

        table.sheet-table th {
            background: var(--bg-header);
            color: var(--text-muted);
            font-weight: 500;
            text-align: center;
            border: 1px solid var(--border-grid);
            padding: 6px 10px;
            position: sticky;
            top: 0;
            z-index: 10;
            user-select: none;
            font-size: 11px;
        }

        table.sheet-table th.row-header {
            width: 44px;
            min-width: 44px;
            left: 0;
            z-index: 20;
            background: var(--bg-header);
            text-align: right;
            padding-right: 8px;
        }

        table.sheet-table th.corner-header {
            left: 0;
            top: 0;
            z-index: 30;
            width: 44px;
        }

        table.sheet-table td {
            border: 1px solid var(--border-grid);
            padding: 5px 8px;
            white-space: nowrap;
            color: var(--text-main);
            cursor: pointer;
            transition: background-color 0.1s ease;
        }

        table.sheet-table td:hover {
            background-color: var(--bg-hover);
        }

        table.sheet-table td.selected {
            outline: 2px solid var(--border-active);
            outline-offset: -1px;
            background-color: var(--bg-active) !important;
            font-weight: 600;
        }

        table.sheet-table td.precedent {
            background-color: #FAF4EB !important;
            outline: 1px dashed var(--border-active);
        }

        table.sheet-table td.has-methodology {
            position: relative;
        }

        table.sheet-table td.has-methodology::after {
            content: '';
            position: absolute;
            top: 2px;
            right: 2px;
            width: 4px;
            height: 4px;
            background: var(--border-active);
            border-radius: 50%;
        }

        .num-right {
            text-align: right;
        }

        .bold-row {
            font-weight: 600;
        }

        /* Derivation & Methodology Inspector Panel */
        .inspector-panel {
            background: #FFFFFF;
            border: 1px solid var(--border-grid);
            border-radius: 2px;
            position: sticky;
            top: 130px;
            max-height: calc(100vh - 160px);
            overflow-y: auto;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            display: flex;
            flex-direction: column;
        }

        .inspector-header {
            background: var(--bg-header);
            border-bottom: 1px solid var(--border-grid);
            padding: 14px 18px;
        }

        .inspector-badge {
            font-family: var(--font-mono);
            font-size: 10px;
            text-transform: uppercase;
            font-weight: 600;
            color: var(--text-muted);
            letter-spacing: 0.05em;
        }

        .inspector-title {
            font-family: var(--font-serif);
            font-size: 17px;
            font-weight: 600;
            color: var(--text-main);
            margin-top: 2px;
            line-height: 1.3;
        }

        .inspector-body {
            padding: 18px;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }

        .metric-display {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            background: var(--bg-page);
            border: 1px solid var(--border-header);
            padding: 12px 14px;
            border-radius: 2px;
        }

        .metric-val {
            font-family: var(--font-mono);
            font-size: 20px;
            font-weight: 700;
            color: var(--text-main);
        }

        .metric-val.positive {
            color: var(--accent-green);
        }

        .metric-val.negative {
            color: var(--accent-red);
        }

        .metric-cell-ref {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--text-muted);
        }

        .formula-callout {
            background: #FAF7F2;
            border-left: 3px solid var(--border-active);
            padding: 8px 12px;
            font-family: var(--font-mono);
            font-size: 12px;
            color: var(--text-main);
            word-break: break-all;
        }

        .section-label {
            font-family: var(--font-sans);
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--text-faint);
            letter-spacing: 0.06em;
            margin-bottom: 6px;
        }

        .prose-text {
            font-family: var(--font-serif);
            font-size: 14px;
            line-height: 1.6;
            color: #2D2A26;
        }

        .intuition-box {
            background: #FDFBF7;
            border: 1px solid #EAE4D6;
            padding: 12px 14px;
            border-radius: 2px;
        }

        .precedents-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .precedent-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #FAF7F2;
            border: 1px solid var(--border-grid);
            padding: 6px 10px;
            border-radius: 2px;
            font-family: var(--font-mono);
            font-size: 11px;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .precedent-item:hover {
            border-color: var(--border-active);
            background: #FFFFFF;
        }

        .precedent-link {
            font-weight: 600;
            color: var(--text-main);
        }

        .precedent-val {
            color: var(--text-muted);
        }

        .dependents-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .dependent-tag {
            background: #F2ECE1;
            border: 1px solid var(--border-header);
            padding: 2px 8px;
            border-radius: 2px;
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-container">
            <div class="header-top">
                <div class="title-block">
                    <h1>Aswath Damodaran :: Anthropic, PBC Valuation Model Architecture</h1>
                    <p>Interactive 18-Sheet Spreadsheet Explorer & Click-to-Derive Methodology Inspector (Post-Q3 2026 Leak Update)</p>
                </div>
                <div class="key-pills">
                    <div class="pill positive">DCF FAIR VALUE: <strong>$439.24 / SH</strong></div>
                    <div class="pill">COMMON EQUITY: <strong>$1,450.5B</strong></div>
                    <div class="pill negative">RUMORED IPO: <strong>$525.00 (-16.3%)</strong></div>
                    <div class="pill">2036 TARGET REV: <strong>$1.005T</strong></div>
                    <div class="pill">WACC: <strong>9.74% &rarr; 9.13%</strong></div>
                </div>
            </div>

            <!-- Formula Bar -->
            <div class="formula-bar">
                <div id="activeCellBox" class="cell-address-box">Valuation output!B24</div>
                <div class="fx-indicator">fx</div>
                <div id="activeFormulaInput" class="formula-input">=B21*(1-B22)+B23*B22</div>
            </div>
        </div>
    </header>

    <!-- Sheet Tabs -->
    <nav class="sheet-tab-bar" id="tabBar">
        <!-- Rendered dynamically -->
    </nav>

    <!-- Main Workspace -->
    <main class="workspace">
        
        <!-- Left: Spreadsheet Grid Canvas -->
        <section class="grid-container" id="gridContainer">
            <table class="sheet-table" id="sheetTable">
                <!-- Grid rendered dynamically -->
            </table>
        </section>

        <!-- Right: Methodology Inspector Drawer -->
        <aside class="inspector-panel" id="inspectorPanel">
            <div class="inspector-header">
                <div id="inspCategory" class="inspector-badge">Core Output</div>
                <h2 id="inspTitle" class="inspector-title">Value of Operating Assets (Distress-Adjusted EV)</h2>
            </div>
            
            <div class="inspector-body">
                <div class="metric-display">
                    <div>
                        <div id="inspVal" class="metric-val positive">$1,719,952.6 M</div>
                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Equivalent: <strong>$1.72 Trillion</strong></div>
                    </div>
                    <div id="inspCoord" class="metric-cell-ref">Valuation output!B24</div>
                </div>

                <div>
                    <div class="section-label">Excel Formula</div>
                    <div id="inspFormula" class="formula-callout">=B21*(1-B22)+B23*B22</div>
                </div>

                <div>
                    <div class="section-label">Primary Derivation Methodology</div>
                    <div id="inspMethodology" class="prose-text">
                        Damodaran calculates operating assets by taking the Going-Concern Enterprise Value and explicitly haircutting it by the probability of failure. Equation: Operating Assets = Sum of PV * (1 - Failure Rate) + Distress Proceeds * Failure Rate.
                    </div>
                </div>

                <div class="intuition-box">
                    <div class="section-label" style="color: var(--text-main);">Economic Intuition & First Principles</div>
                    <div id="inspIntuition" class="prose-text" style="font-size: 13px;">
                        Default risk in early-stage, capital-intensive firms should not be crammed into the going-concern WACC. A discount rate assumes the company survives forever. Instead, Damodaran explicitly separates valuation into a going-concern DCF and distress liquidation value.
                    </div>
                </div>

                <div>
                    <div class="section-label">Upstream Precedents</div>
                    <div id="inspPrecedents" class="precedents-list">
                        <!-- Precedents injected here -->
                    </div>
                </div>

                <div>
                    <div class="section-label">Downstream Dependents</div>
                    <div id="inspDependents" class="dependents-tags">
                        <!-- Dependents injected here -->
                    </div>
                </div>
            </div>
        </aside>

    </main>

    <!-- Embedded Model Data & Client Logic -->
    <script>
        const modelData = """ + json.dumps(model_data) + """;
        const sheets = modelData.sheets;
        const methodologies = modelData.methodologies;

        let activeSheetName = "Valuation output";
        let activeCoord = "B24";

        // Number formatter
        function formatNumber(v) {
            if (v === null || v === undefined || v === '') return '';
            if (typeof v === 'number') {
                if (Math.abs(v) >= 1000) {
                    return v.toLocaleString('en-US', { maximumFractionDigits: 1 });
                } else if (Math.abs(v) < 1 && Math.abs(v) > 0.0001) {
                    return (v * 100).toFixed(1) + '%';
                } else if (!Number.isInteger(v)) {
                    return v.toFixed(2);
                }
                return v.toLocaleString('en-US');
            }
            return v;
        }

        // Initialize Tab Bar
        const tabBar = document.getElementById('tabBar');
        Object.keys(sheets).forEach(sname => {
            const btn = document.createElement('button');
            btn.className = 'sheet-tab' + (sname === activeSheetName ? ' active' : '');
            btn.innerText = sname;
            btn.onclick = () => selectSheet(sname);
            tabBar.appendChild(btn);
        });

        // Select Sheet Function
        function selectSheet(sname) {
            activeSheetName = sname;
            document.querySelectorAll('.sheet-tab').forEach(b => {
                b.classList.toggle('active', b.innerText === sname);
            });
            renderSheetGrid(sname);
        }

        // Render Sheet Grid Table
        function renderSheetGrid(sname) {
            const sheet = sheets[sname];
            const table = document.getElementById('sheetTable');
            table.innerHTML = '';

            if (!sheet || !sheet.grid || sheet.grid.length === 0) {
                table.innerHTML = '<tr><td style="padding: 24px; text-align: center; color: var(--text-muted);">Sheet empty or omitted</td></tr>';
                return;
            }

            // Header row with column letters
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            
            const corner = document.createElement('th');
            corner.className = 'corner-header';
            corner.innerText = '';
            headerRow.appendChild(corner);

            sheet.col_letters.forEach(letter => {
                const th = document.createElement('th');
                th.innerText = letter;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            // Table body with data rows
            const tbody = document.createElement('tbody');
            sheet.grid.forEach(rData => {
                const tr = document.createElement('tr');
                
                // Row header
                const rowHeader = document.createElement('th');
                rowHeader.className = 'row-header';
                rowHeader.innerText = rData.row_idx;
                tr.appendChild(rowHeader);

                rData.cells.forEach(cell => {
                    const td = document.createElement('td');
                    td.id = `cell_${sname.replace(/[^a-zA-Z0-9]/g, '_')}_${cell.coord}`;
                    td.dataset.coord = cell.coord;
                    td.dataset.sheet = sname;

                    // Display value
                    td.innerText = formatNumber(cell.val);

                    if (typeof cell.val === 'number') {
                        td.classList.add('num-right');
                        if (cell.val < 0) td.style.color = 'var(--accent-red)';
                    }

                    // Check if methodology exists
                    const fullKey = `${sname}!${cell.coord}`;
                    if (methodologies[fullKey]) {
                        td.classList.add('has-methodology');
                    }

                    td.onclick = () => selectCell(sname, cell.coord, cell);
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
            table.appendChild(tbody);

            // Select default cell
            if (sname === "Valuation output") {
                selectCell("Valuation output", "B24");
            } else if (sheet.grid[0] && sheet.grid[0].cells[0]) {
                selectCell(sname, sheet.grid[0].cells[0].coord, sheet.grid[0].cells[0]);
            }
        }

        // Select and Inspect Cell
        function selectCell(sname, coord, cellObj) {
            activeSheetName = sname;
            activeCoord = coord;

            // Highlight in grid
            document.querySelectorAll('td.selected, td.precedent').forEach(el => {
                el.classList.remove('selected', 'precedent');
            });

            const targetTd = document.getElementById(`cell_${sname.replace(/[^a-zA-Z0-9]/g, '_')}_${coord}`);
            if (targetTd) targetTd.classList.add('selected');

            // Find cell object if not provided
            if (!cellObj) {
                const sheet = sheets[sname];
                if (sheet) {
                    for (const r of sheet.grid) {
                        for (const c of r.cells) {
                            if (c.coord === coord) {
                                cellObj = c;
                                break;
                            }
                        }
                    }
                }
            }

            const fullKey = `${sname}!${coord}`;
            const meta = methodologies[fullKey];

            // Update Formula Bar
            document.getElementById('activeCellBox').innerText = fullKey;
            document.getElementById('activeFormulaInput').innerText = (cellObj && cellObj.formula) ? cellObj.formula : (cellObj && cellObj.val !== null ? cellObj.val : '');

            // Update Inspector Panel
            const inspCategory = document.getElementById('inspCategory');
            const inspTitle = document.getElementById('inspTitle');
            const inspVal = document.getElementById('inspVal');
            const inspCoord = document.getElementById('inspCoord');
            const inspFormula = document.getElementById('inspFormula');
            const inspMethodology = document.getElementById('inspMethodology');
            const inspIntuition = document.getElementById('inspIntuition');
            const inspPrecedents = document.getElementById('inspPrecedents');
            const inspDependents = document.getElementById('inspDependents');

            inspCoord.innerText = fullKey;

            const valStr = cellObj ? formatNumber(cellObj.val) : '-';
            inspVal.innerText = valStr;
            inspVal.className = 'metric-val' + ((cellObj && typeof cellObj.val === 'number' && cellObj.val < 0) ? ' negative' : '');

            if (meta) {
                inspCategory.innerText = meta.category || 'Valuation Metric';
                inspTitle.innerText = meta.label || `Cell ${coord}`;
                inspFormula.innerText = meta.formula || (cellObj && cellObj.formula ? cellObj.formula : 'Direct Entry / Historical Filing Input');
                inspMethodology.innerText = meta.methodology || 'Primary calculation node in Damodaran DCF engine.';
                inspIntuition.innerText = meta.economic_intuition || 'Core parameter anchoring company narrative to corporate finance principles.';

                // Render Precedents
                inspPrecedents.innerHTML = '';
                if (meta.precedents && meta.precedents.length > 0) {
                    meta.precedents.forEach(p => {
                        const div = document.createElement('div');
                        div.className = 'precedent-item';
                        div.innerHTML = `<span class="precedent-link">${p.sheet}!${p.coord} (${p.label})</span><span class="precedent-val">${p.val}</span>`;
                        div.onclick = (e) => {
                            e.stopPropagation();
                            jumpToCell(p.sheet, p.coord.split(':')[0]);
                        };
                        inspPrecedents.appendChild(div);

                        // Highlight precedent if on same sheet
                        if (p.sheet === sname) {
                            const pTd = document.getElementById(`cell_${sname.replace(/[^a-zA-Z0-9]/g, '_')}_${p.coord}`);
                            if (pTd) pTd.classList.add('precedent');
                        }
                    });
                } else {
                    inspPrecedents.innerHTML = '<span style="color: var(--text-faint); font-style: italic; font-size: 11px;">Independent Input / Sovereign or Industry Anchor</span>';
                }

                // Render Dependents
                inspDependents.innerHTML = '';
                if (meta.dependents && meta.dependents.length > 0) {
                    meta.dependents.forEach(d => {
                        const span = document.createElement('span');
                        span.className = 'dependent-tag';
                        span.innerText = d;
                        inspDependents.appendChild(span);
                    });
                } else {
                    inspDependents.innerHTML = '<span style="color: var(--text-faint); font-style: italic; font-size: 11px;">Final Valuation Output / Independent End Node</span>';
                }
            } else {
                // Auto-generate generic inspector info for unannotated cells
                inspCategory.innerText = (cellObj && cellObj.formula) ? 'Calculated Cell' : 'Input / Constant';
                inspTitle.innerText = `Cell ${coord}`;
                inspFormula.innerText = (cellObj && cellObj.formula) ? cellObj.formula : 'Direct Value Input';
                inspMethodology.innerText = 'Supporting schedule data item in Damodaran Anthropic valuation model. Click on cells with indicators for comprehensive derivation write-ups.';
                inspIntuition.innerText = 'Forms part of the 10-year discrete financial projection and capital structure synthesis.';
                inspPrecedents.innerHTML = '<span style="color: var(--text-faint); font-style: italic; font-size: 11px;">No explicit precedents cataloged</span>';
                inspDependents.innerHTML = '<span style="color: var(--text-faint); font-style: italic; font-size: 11px;">General DCF model dependency</span>';
            }
        }

        // Jump to cell in any sheet
        function jumpToCell(sname, coord) {
            if (activeSheetName !== sname) {
                selectSheet(sname);
            }
            setTimeout(() => {
                selectCell(sname, coord);
                const el = document.getElementById(`cell_${sname.replace(/[^a-zA-Z0-9]/g, '_')}_${coord}`);
                if (el) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
                }
            }, 50);
        }

        // Initial render
        renderSheetGrid("Valuation output");
    </script>
</body>
</html>
"""

out_file = "ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/damodaran_breakdown_reader.html"
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Successfully generated Damodaran Breakdown Reader at {out_file} ({len(html_template)} bytes).")
