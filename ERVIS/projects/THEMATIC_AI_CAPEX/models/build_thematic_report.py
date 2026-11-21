import json
import os

def generate_thematic_html():
    # Load model outputs
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "model_outputs.json")
    with open(data_path, "r") as f:
        data = json.load(f)

    circ = data["circularity_summary"]
    annual_circ = data["annual_circularity_schedule"]
    depr = data["depreciation_cliff_schedule"]
    tokens = data["token_margin_trajectory"]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thematic AI CapEx & Counterparty Circularity Matrix — Anthropic PBC & Hyperscalers</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {{
            --bg-page: #FAF7F2;
            --bg-card: #FFFFFF;
            --bg-subtle: #F4EFEB;
            --bg-active: #EFE8DF;
            --border-main: #E5E0D8;
            --border-dark: #D8D2C5;
            --text-primary: #1C1917;
            --text-secondary: #57534E;
            --text-muted: #8C867A;
            --accent-amber: #B45309;
            --accent-green: #0B5A3D;
            --accent-red: #B91C1C;
            --accent-cyan: #0E7490;
            --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
            --font-serif: 'Newsreader', Georgia, serif;
            --font-mono: 'JetBrains Mono', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-page);
            color: var(--text-primary);
            font-family: var(--font-sans);
            font-size: 13.5px;
            line-height: 1.55;
            -webkit-font-smoothing: antialiased;
        }}

        .font-serif {{ font-family: var(--font-serif); }}
        .font-mono {{ font-family: var(--font-mono); }}
        .font-sans {{ font-family: var(--font-sans); }}

        .card {{
            background: var(--bg-card);
            border: 1px solid var(--border-main);
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}

        .fin-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: var(--font-mono);
            font-size: 11.5px;
        }}
        .fin-table th {{
            font-family: var(--font-sans);
            font-size: 10.5px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            padding: 8px 12px;
            border-bottom: 2px solid var(--border-dark);
            background-color: var(--bg-subtle);
            text-align: right;
            white-space: nowrap;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        .fin-table th:first-child {{
            text-align: left;
        }}
        .fin-table td {{
            padding: 7px 12px;
            border-bottom: 1px solid #ECE7DE;
            color: var(--text-primary);
            text-align: right;
            white-space: nowrap;
        }}
        .fin-table td:first-child {{
            text-align: left;
            font-family: var(--font-sans);
            font-size: 12px;
            color: var(--text-primary);
            white-space: normal;
        }}
        .fin-table tr:hover td {{
            background-color: #F8F5EE;
        }}
        .fin-table .row-highlight td {{
            background-color: #FFFDF8;
            font-weight: 600;
        }}

        .custom-scroll::-webkit-scrollbar {{
            height: 5px;
            width: 5px;
        }}
        .custom-scroll::-webkit-scrollbar-track {{
            background: var(--bg-page);
        }}
        .custom-scroll::-webkit-scrollbar-thumb {{
            background: var(--border-dark);
            border-radius: 3px;
        }}

        .slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 100%;
            height: 6px;
            background: #E5E0D8;
            border-radius: 3px;
            outline: none;
        }}
        .slider-thumb::-webkit-slider-thumb {{
            -webkit-appearance: none;
            appearance: none;
            width: 16px;
            height: 16px;
            background: #B45309;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
        }}
    </style>
</head>
<body class="min-h-screen">

    <!-- Top Command Header -->
    <header class="bg-[#FFFFFF] border-b border-[#E5E0D8] sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-6 py-3.5 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
                <!-- Institutional Reciprocal Breadcrumbs Chain -->
                <div class="flex items-center space-x-2 text-[10.5px] font-mono text-[#8C867A] mb-1">
                    <a href="../../index.html" class="text-[#B45309] font-bold hover:underline">&larr; ERVIS CENTRAL</a>
                    <span>/</span>
                    <a href="index.html" class="hover:underline text-[#57534E]">ANTHROPIC DOSSIER</a>
                    <span>/</span>
                    <a href="prospectus.html" class="hover:underline text-[#57534E]">S-1 AUDIT</a>
                    <span>/</span>
                    <a href="damodaran.html" class="hover:underline text-[#57534E]">DAMODARAN EXCEL</a>
                    <span>/</span>
                    <a href="cockpit.html" class="hover:underline text-[#57534E]">VALUATION COCKPIT</a>
                    <span>/</span>
                    <a href="../../almanac.html" class="hover:underline text-[#57534E]">ALMANAC</a>
                    <span>/</span>
                    <span class="text-[#1C1917] font-semibold">THEMATIC AI CAPEX</span>
                </div>
                <div class="flex items-baseline space-x-3">
                    <h1 class="text-xl font-serif font-bold text-[#1C1917] tracking-tight">
                        Thematic AI CapEx & Counterparty Circularity Matrix
                    </h1>
                    <span class="text-xs font-mono font-bold px-2 py-0.5 bg-[#FEF3C7] border border-[#FDE68A] rounded text-[#92400E]">
                        TRACK 1 FORENSIC ENGINE &bull; CLOSED-LOOP MACRO
                    </span>
                </div>
            </div>

            <!-- Top Ticker & Metric Strip -->
            <div class="flex items-center space-x-3 text-xs font-mono">
                <a href="../../almanac.html#empirical" class="px-3 py-1.5 bg-[#FAF7F2] hover:bg-[#EFE8DF] border border-[#B45309] text-[#B45309] rounded font-bold transition-colors flex items-center gap-1.5 shadow-sm text-xs">
                    <span>📖</span>
                    <span>ALMANAC TAB 06</span>
                </a>
                <div class="h-7 w-px bg-[#E5E0D8]"></div>
                <div class="text-right">
                    <div class="text-[10px] text-[#8C867A] uppercase tracking-wider">Note 13 Compute Debt</div>
                    <div class="text-xs font-bold text-[#B91C1C]">$265.6B <span class="text-[9.5px] font-normal text-[#8C867A]">($485.3B Cap)</span></div>
                </div>
                <div class="h-7 w-px bg-[#E5E0D8]"></div>
                <div class="text-right">
                    <div class="text-[10px] text-[#8C867A] uppercase tracking-wider">Equity Multiplier</div>
                    <div class="text-xs font-bold text-[#15803D]">64.4x AMZN <span class="text-[9.5px] font-normal text-[#8C867A]">&bull; 66.0x GOOGL</span></div>
                </div>
                <div class="h-7 w-px bg-[#E5E0D8]"></div>
                <div class="text-right">
                    <div class="text-[10px] text-[#8C867A] uppercase tracking-wider">Big 4 2026E CapEx</div>
                    <div class="text-xs font-bold text-[#1C1917]">$394.0B <span class="text-[9.5px] font-normal text-[#8C867A]">(78% OCF)</span></div>
                </div>
                <div class="h-7 w-px bg-[#E5E0D8]"></div>
                <div class="text-right">
                    <div class="text-[10px] text-[#8C867A] uppercase tracking-wider">H100 Breakeven</div>
                    <div class="text-xs font-bold px-2 py-0.5 bg-[#FEE2E2] border border-[#FECACA] rounded text-[#B91C1C]">
                        $5.74 / 1M Tok
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-6 py-7 space-y-8">

        <!-- Executive Case Overview Hero -->
        <div class="card p-6 border-l-4 border-l-[#B45309] space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-[#E5E0D8] pb-3">
                <div>
                    <span class="text-[10.5px] font-mono uppercase tracking-wider text-[#B45309] font-bold">
                        Institutional Macro Briefing & Forensic Circularity Audit
                    </span>
                    <h2 class="text-lg font-serif font-bold text-[#1C1917]">
                        The Anthropic $265.6B Compute Commitment & The Closed-Loop Hyperscaler Flywheel
                    </h2>
                </div>
                <span class="text-xs font-mono text-[#8C867A]">
                    Model Engine: v2.4 Active &bull; Valuation Gate: Gate 5 Institutional Sign-Off
                </span>
            </div>

            <p class="text-xs text-[#57534E] leading-relaxed">
                Beneath Anthropic's landmark $1.404T IPO lies the single largest contractual customer commitment structure in enterprise computing history: <strong>$265.6 Billion in multi-year take-or-pay cloud compute reservations</strong> disclosed in SEC Form S-1/A Note 13. When capitalized at Anthropic's 8.87% cost of capital, this obligation represents <strong>$485.3 Billion in synthetic debt claims senior to public equity</strong>, demanding $23.5B in annual imputed servicing. However, from the perspective of counterparties <strong>Amazon Web Services (AWS)</strong> and <strong>Google Cloud Platform (GCP)</strong>, these commitments create a self-reinforcing valuation flywheel: hyperscaler private equity checks are recycled directly into high-margin Cloud ARR, which public equity markets capitalize at 8.5x–9.0x EV/Sales, expanding hyperscaler market capitalizations by over <strong>60x the initial equity deployed</strong>. Meanwhile, upstream capital expenditures ($394B in 2026 across the Big 4) are absorbed by semiconductor leaders (NVDA, AVGO, TSM) and electrical power infrastructure providers (POWL), setting up an inevitable <strong>ASC 360 depreciation impairment cliff</strong> as inference token pricing drops below amortized hardware breakeven.
            </p>

            <!-- 4 Core Pillars KPI Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 font-mono text-xs pt-1">
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <span class="text-[9.5px] text-[#8C867A] uppercase block">Anthropic Compute Spend</span>
                    <strong class="text-[#B91C1C] text-sm font-bold">$265.6 Billion</strong>
                    <span class="text-[10px] text-[#57534E] block mt-0.5">Note 13 Contractual Minima</span>
                </div>
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <span class="text-[9.5px] text-[#8C867A] uppercase block">Hyperscaler EV Creation</span>
                    <strong class="text-[#15803D] text-sm font-bold">+$2,339.9 Billion</strong>
                    <span class="text-[10px] text-[#57534E] block mt-0.5">AWS: $1,482B | GCP: $858B</span>
                </div>
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <span class="text-[9.5px] text-[#8C867A] uppercase block">Peak Annual D&A Drag</span>
                    <strong class="text-[#B45309] text-sm font-bold">$45.5B / Year</strong>
                    <span class="text-[10px] text-[#57534E] block mt-0.5">989 bps Margin Compression (2028)</span>
                </div>
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <span class="text-[9.5px] text-[#8C867A] uppercase block">Inference Margin Inversion</span>
                    <strong class="text-[#B91C1C] text-sm font-bold">-319% Deficit</strong>
                    <span class="text-[10px] text-[#57534E] block mt-0.5">$1.37 Market vs $5.74 H100 Cost</span>
                </div>
            </div>

            <!-- Strategic Structural Thesis Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-[#57534E] pt-2 border-t border-[#ECE7DE]">
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <div class="text-[10.5px] font-mono font-bold text-[#15803D] uppercase mb-1">1. The Circular Equity-to-EV Multiplier</div>
                    <p class="leading-relaxed">Amazon's $23.0B equity check yields $164.7B in high-margin AWS revenue. At an 8.5x cloud sales multiple and 38.5% EBIT margin, public markets award AWS $1.48T in incremental EV—a 64.4x multiple on the initial cash check.</p>
                </div>
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <div class="text-[10.5px] font-mono font-bold text-[#B45309] uppercase mb-1">2. Upstream Hardware & Power Absorption</div>
                    <p class="leading-relaxed">Hyperscalers recycle cloud cash flows upstream: Nvidia (accelerators), Broadcom (custom TPU/Trainium ASICs), TSMC (3nm/2nm packaging), and Powell Industries (substation switchgear, MV transformers for 100MW+ data centers).</p>
                </div>
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <div class="text-[10.5px] font-mono font-bold text-[#B91C1C] uppercase mb-1">3. The ASC 360 Depreciation Trap</div>
                    <p class="leading-relaxed">Hyperscalers depreciate servers over 5.5 to 6.0 years, but AI clusters suffer technological obsolescence within 3.5 years. By 2028, this creates an unrecorded $45.5B annual D&A gap and a $176B balance sheet asset overhang.</p>
                </div>
            </div>
        </div>

        <!-- Section 1: Visual Interactive Charts (4 Grid Modules) -->
        <div class="space-y-6">
            <div class="flex items-baseline justify-between border-b border-[#E5E0D8] pb-2">
                <div>
                    <h2 class="text-base font-serif font-bold text-[#1C1917]">
                        Macro Forensics & Quantitative Visual Modules
                    </h2>
                    <p class="text-xs text-[#57534E]">
                        Four interactive charts mapping capital circularity, hyperscaler capex supercycles, depreciation gaps, and token margin inversion
                    </p>
                </div>
                <span class="text-[11px] font-mono text-[#8C867A]">Interactive Chart.js Suite</span>
            </div>

            <!-- Charts Row 1: Circular Flow & Capex Supercycle -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

                <!-- Chart 1: Circular Capital Flow & Multiplier -->
                <div class="card p-5 space-y-3">
                    <div class="flex items-center justify-between border-b border-[#E5E0D8] pb-2">
                        <div>
                            <span class="text-[10px] font-mono uppercase px-2 py-0.5 bg-[#FEF3C7] text-[#92400E] border border-[#FDE68A] rounded font-bold">
                                MODULE A &bull; CIRCULAR VALUE CREATION
                            </span>
                            <h3 class="text-sm font-serif font-bold text-[#1C1917] mt-1">
                                Cash Flow Circularity & Hyperscaler EV Multiplier
                            </h3>
                        </div>
                        <span class="text-[11px] font-mono text-[#15803D] font-bold">64x–66x Return on Cash</span>
                    </div>
                    <p class="text-xs text-[#57534E]">
                        Hyperscaler equity injected into Anthropic vs. Contractual Compute Spend captured vs. Resulting Enterprise Value expansion awarded by public markets (at 8.5x–9.0x EV/ARR).
                    </p>
                    <div class="h-64 w-full">
                        <canvas id="circularFlowChart"></canvas>
                    </div>
                    <div class="p-2.5 bg-[#FAF7F2] border border-[#E5E0D8] rounded font-mono text-[11px] text-[#57534E] flex justify-between">
                        <span>AWS ARR: <strong>$164.7B</strong> &bull; Implied EV: <strong>+$1,482B</strong></span>
                        <span>GCP ARR: <strong>$100.9B</strong> &bull; Implied EV: <strong>+$858B</strong></span>
                    </div>
                </div>

                <!-- Chart 2: Big 4 Capex Supercycle -->
                <div class="card p-5 space-y-3">
                    <div class="flex items-center justify-between border-b border-[#E5E0D8] pb-2">
                        <div>
                            <span class="text-[10px] font-mono uppercase px-2 py-0.5 bg-[#CFFAFE] text-[#155E75] border border-[#A5F3FC] rounded font-bold">
                                MODULE B &bull; HYPERSCALER SUPERCYCLE
                            </span>
                            <h3 class="text-sm font-serif font-bold text-[#1C1917] mt-1">
                                Big 4 Aggregate CapEx & Reinvestment Squeeze (2021–2030E)
                            </h3>
                        </div>
                        <span class="text-[11px] font-mono text-[#B45309] font-bold">$394B CapEx in 2026E</span>
                    </div>
                    <p class="text-xs text-[#57534E]">
                        Aggregate capital expenditure across Amazon, Google, Microsoft, and Meta. CapEx as a percentage of Operating Cash Flow surges from 45% (2021) to 78%+ (2026E).
                    </p>
                    <div class="h-64 w-full">
                        <canvas id="capexSupercycleChart"></canvas>
                    </div>
                    <div class="p-2.5 bg-[#FAF7F2] border border-[#E5E0D8] rounded font-mono text-[11px] text-[#57534E] flex justify-between">
                        <span>2021: <strong>$126.5B</strong> (45% CFO)</span>
                        <span>2026E: <strong>$394.0B</strong> (78% CFO)</span>
                        <span>2030E: <strong>$500.0B</strong></span>
                    </div>
                </div>

            </div>

            <!-- Charts Row 2: Depreciation Cliff & Token Deflation Inversion -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

                <!-- Chart 3: ASC 360 Depreciation Cliff -->
                <div class="card p-5 space-y-3">
                    <div class="flex items-center justify-between border-b border-[#E5E0D8] pb-2">
                        <div>
                            <span class="text-[10px] font-mono uppercase px-2 py-0.5 bg-[#FEE2E2] text-[#991B1B] border border-[#FECACA] rounded font-bold">
                                MODULE C &bull; ACCOUNTING IMPAIRMENT
                            </span>
                            <h3 class="text-sm font-serif font-bold text-[#1C1917] mt-1">
                                The ASC 360 Deferred Depreciation Cliff & Margin Drag
                            </h3>
                        </div>
                        <span class="text-[11px] font-mono text-[#B91C1C] font-bold">-$45.5B / yr Peak Headwind</span>
                    </div>
                    <p class="text-xs text-[#57534E]">
                        Stated D&A (5.5-yr straight line) vs. Realistic Economic D&A (3.5-yr GPU replacement cycle). By 2028, the unrecorded annual gap peaks at $45.5B, compressing cloud EBIT by 989 bps.
                    </p>
                    <div class="h-64 w-full">
                        <canvas id="depreciationCliffChart"></canvas>
                    </div>
                    <div class="p-2.5 bg-[#FAF7F2] border border-[#E5E0D8] rounded font-mono text-[11px] text-[#57534E] flex justify-between">
                        <span>2026 Gap: <strong>-$21.1B</strong> (540 bps)</span>
                        <span>2028 Peak Gap: <strong>-$45.5B</strong> (989 bps)</span>
                        <span>2028 Overhang: <strong>$176.7B</strong></span>
                    </div>
                </div>

                <!-- Chart 4: Inference Token Deflation vs Hardware Breakeven -->
                <div class="card p-5 space-y-3">
                    <div class="flex items-center justify-between border-b border-[#E5E0D8] pb-2">
                        <div>
                            <span class="text-[10px] font-mono uppercase px-2 py-0.5 bg-[#EDE9FE] text-[#5B21B6] border border-[#DDD6FE] rounded font-bold">
                                MODULE D &bull; COMMODITIZATION INVERSION
                            </span>
                            <h3 class="text-sm font-serif font-bold text-[#1C1917] mt-1">
                                Inference Token Deflation vs. H100 Amortization Breakeven
                            </h3>
                        </div>
                        <span class="text-[11px] font-mono text-[#B91C1C] font-bold">Breakeven: $5.74 / 1M Tok</span>
                    </div>
                    <p class="text-xs text-[#57534E]">
                        Blended token pricing has deflated 93% from Claude 1.0 ($20.00) to DeepSeek ($1.37). Specialized frontier inference faces severe gross margin impairment below the $5.74 H100 cost floor.
                    </p>
                    <div class="h-64 w-full">
                        <canvas id="tokenBreakevenChart"></canvas>
                    </div>
                    <div class="p-2.5 bg-[#FAF7F2] border border-[#E5E0D8] rounded font-mono text-[11px] text-[#57534E] flex justify-between">
                        <span>H100 Unit Cost: <strong>$5.74</strong></span>
                        <span>Claude 3.5 Sonnet: <strong>$9.00</strong> (+36%)</span>
                        <span>DeepSeek / Distill: <strong>$1.37</strong> (-319%)</span>
                    </div>
                </div>

            </div>
        </div>

        <!-- Section 2: Interactive Scenario Modeler / Sensitivity Scrubber -->
        <div class="card p-6 space-y-5 border-t-2 border-t-[#B45309]">
            <div class="flex flex-col sm:flex-row sm:items-baseline justify-between gap-2 border-b border-[#E5E0D8] pb-3">
                <div>
                    <span class="text-[10.5px] font-mono uppercase tracking-wider text-[#B45309] font-bold">
                        Dynamic Sensitivity Simulator
                    </span>
                    <h2 class="text-base font-serif font-bold text-[#1C1917]">
                        Closed-Loop Stress-Test: Commitment Drawdowns, Useful Lives & Token Commoditization
                    </h2>
                </div>
                <span class="text-xs font-mono text-[#8C867A]">Client-Side Real-Time Engine</span>
            </div>

            <!-- Sliders Grid -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

                <!-- Slider 1 -->
                <div class="p-4 bg-[#FAF7F2] border border-[#E5E0D8] rounded space-y-2">
                    <div class="flex justify-between text-xs font-mono">
                        <span class="text-[#57534E] font-medium">Anthropic Compute Drawdown</span>
                        <span id="sliderDrawdownVal" class="font-bold text-[#B45309]">100% ($265.6B)</span>
                    </div>
                    <input type="range" id="sliderDrawdown" min="50" max="100" value="100" step="5" class="slider-thumb" oninput="updateScenario()">
                    <div class="flex justify-between text-[10px] text-[#8C867A] font-mono">
                        <span>50% Minimum Take-or-Pay</span>
                        <span>100% Full Schedule</span>
                    </div>
                    <p class="text-[11px] text-[#8C867A] leading-tight pt-1">
                        Stress-tests hyperscaler cloud ARR if Anthropic negotiates contractual relief or fails to consume allocated clusters.
                    </p>
                </div>

                <!-- Slider 2 -->
                <div class="p-4 bg-[#FAF7F2] border border-[#E5E0D8] rounded space-y-2">
                    <div class="flex justify-between text-xs font-mono">
                        <span class="text-[#57534E] font-medium">AI Hardware Depreciable Life</span>
                        <span id="sliderLifeVal" class="font-bold text-[#B91C1C]">3.5 Years (Realistic)</span>
                    </div>
                    <input type="range" id="sliderLife" min="2.5" max="5.5" value="3.5" step="0.5" class="slider-thumb" oninput="updateScenario()">
                    <div class="flex justify-between text-[10px] text-[#8C867A] font-mono">
                        <span>2.5 Yrs (Rapid Obsolescence)</span>
                        <span>5.5 Yrs (Stated 10-K)</span>
                    </div>
                    <p class="text-[11px] text-[#8C867A] leading-tight pt-1">
                        Adjusts the useful life of AI accelerators and server blades to quantify unrecorded annual D&A and ASC 360 impairment.
                    </p>
                </div>

                <!-- Slider 3 -->
                <div class="p-4 bg-[#FAF7F2] border border-[#E5E0D8] rounded space-y-2">
                    <div class="flex justify-between text-xs font-mono">
                        <span class="text-[#57534E] font-medium">Token Price Deflation Shocker</span>
                        <span id="sliderDeflationVal" class="font-bold text-[#0E7490]">0% (Baseline Deflation)</span>
                    </div>
                    <input type="range" id="sliderDeflation" min="0" max="75" value="0" step="5" class="slider-thumb" oninput="updateScenario()">
                    <div class="flex justify-between text-[10px] text-[#8C867A] font-mono">
                        <span>0% Baseline</span>
                        <span>-75% Severe Open Squeeze</span>
                    </div>
                    <p class="text-[11px] text-[#8C867A] leading-tight pt-1">
                        Applies accelerated commoditization across proprietary API pricing (Claude 3.5 Sonnet / Opus) vs. open distilled models.
                    </p>
                </div>

            </div>

            <!-- Scenario Result Metrics Chips -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 font-mono text-xs pt-2">
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <span class="text-[9.5px] text-[#8C867A] uppercase block">Recalculated Cloud ARR</span>
                    <strong id="kpiRecalculatedARR" class="text-[#1C1917] text-sm font-bold">$265.6 Billion</strong>
                    <span id="kpiRecalculatedEBIT" class="text-[10px] text-[#15803D] block mt-0.5">AWS: $164.7B &bull; GCP: $100.9B</span>
                </div>
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <span class="text-[9.5px] text-[#8C867A] uppercase block">Peak Unrecorded D&A Gap</span>
                    <strong id="kpiPeakGap" class="text-[#B91C1C] text-sm font-bold">$45.5B / Year</strong>
                    <span id="kpiOverhang" class="text-[10px] text-[#57534E] block mt-0.5">$176.7B PP&E Overhang</span>
                </div>
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <span class="text-[9.5px] text-[#8C867A] uppercase block">Cloud Operating Margin Drag</span>
                    <strong id="kpiMarginDrag" class="text-[#B45309] text-sm font-bold">-989 bps</strong>
                    <span id="kpiEBITImpact" class="text-[10px] text-[#57534E] block mt-0.5">Peak Compression in 2028</span>
                </div>
                <div class="p-3 bg-[#FAF7F2] border border-[#E5E0D8] rounded">
                    <span class="text-[9.5px] text-[#8C867A] uppercase block">Sonnet Gross Margin Spread</span>
                    <strong id="kpiSonnetMargin" class="text-[#15803D] text-sm font-bold">+$3.26 / M (+36.2%)</strong>
                    <span id="kpiSonnetStatus" class="text-[10px] text-[#15803D] block mt-0.5">Healthy Above Breakeven</span>
                </div>
            </div>
        </div>

        <!-- Section 3: Granular Forensic Audit Tables -->
        <div class="space-y-6">
            <div class="flex items-baseline justify-between border-b border-[#E5E0D8] pb-2">
                <div>
                    <h2 class="text-base font-serif font-bold text-[#1C1917]">
                        Granular Accounting Audit Tables
                    </h2>
                    <p class="text-xs text-[#57534E]">
                        Audited Note 13 commitment schedules, upstream equipment value capture, and hyperscaler depreciable useful lives
                    </p>
                </div>
                <span class="text-[11px] font-mono text-[#8C867A]">SEC Form S-1/A & 10-K Forensic Data</span>
            </div>

            <!-- Table 1: Note 13 Annual Schedule -->
            <div class="card overflow-hidden">
                <div class="p-4 bg-[#FAF7F2] border-b border-[#E5E0D8] flex justify-between items-center">
                    <div>
                        <span class="text-[10px] font-mono uppercase px-2 py-0.5 bg-[#FEF3C7] text-[#92400E] border border-[#FDE68A] rounded font-bold">
                            TABLE 01 &bull; NOTE 13 CONTRACTUAL OBLIGATIONS
                        </span>
                        <h3 class="text-sm font-serif font-bold text-[#1C1917] mt-1">
                            Anthropic Take-or-Pay Cloud Compute Commitments by Year (2027–2033+)
                        </h3>
                    </div>
                    <span class="text-xs font-mono text-[#8C867A]">$265.6B Nominal &bull; $376.0B PV at 8.87% WACC</span>
                </div>
                <div class="overflow-x-auto custom-scroll">
                    <table class="fin-table">
                        <thead>
                            <tr>
                                <th>Commitment Fiscal Year</th>
                                <th>Anthropic Total Spend ($M)</th>
                                <th>AWS Revenue Captured ($M)</th>
                                <th>AWS Cloud EBIT ($M)</th>
                                <th>AWS Implied EV Uplift ($B)</th>
                                <th>GCP Revenue Captured ($M)</th>
                                <th>GCP Cloud EBIT ($M)</th>
                                <th>GCP Implied EV Uplift ($B)</th>
                            </tr>
                        </thead>
                        <tbody>
                            {"".join([f'''
                            <tr>
                                <td class="font-semibold">{row["year"]}</td>
                                <td class="text-[#B91C1C]">${row["anthropic_total_spend_usd_m"]:,.1f}</td>
                                <td class="text-[#15803D]">${row["aws_revenue_usd_m"]:,.1f}</td>
                                <td>${row["aws_ebit_usd_m"]:,.1f}</td>
                                <td class="font-bold text-[#15803D]">+${row["aws_implied_ev_uplift_usd_b"]:,.1f}B</td>
                                <td class="text-[#0E7490]">${row["gcp_revenue_usd_m"]:,.1f}</td>
                                <td>${row["gcp_ebit_usd_m"]:,.1f}</td>
                                <td class="font-bold text-[#0E7490]">+${row["gcp_implied_ev_uplift_usd_b"]:,.1f}B</td>
                            </tr>''' for row in annual_circ])}
                            <tr class="row-highlight bg-[#F4EFEB]">
                                <td class="font-bold">Total Cumulative Schedule (2027–2033+)</td>
                                <td class="font-bold text-[#B91C1C]">${circ["total_anthropic_spend_usd_m"]:,.1f}M</td>
                                <td class="font-bold text-[#15803D]">${circ["aws_total_revenue_usd_m"]:,.1f}M</td>
                                <td class="font-bold">${circ["aws_total_ebit_usd_m"]:,.1f}M</td>
                                <td class="font-bold text-[#15803D]">+${circ["aws_cumulative_ev_uplift_usd_b"]:,.1f}B</td>
                                <td class="font-bold text-[#0E7490]">${circ["gcp_total_revenue_usd_m"]:,.1f}M</td>
                                <td class="font-bold">${circ["gcp_total_ebit_usd_m"]:,.1f}M</td>
                                <td class="font-bold text-[#0E7490]">+${circ["gcp_cumulative_ev_uplift_usd_b"]:,.1f}B</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Table 2: Upstream Value Chain Absorption Matrix -->
            <div class="card overflow-hidden">
                <div class="p-4 bg-[#FAF7F2] border-b border-[#E5E0D8] flex justify-between items-center">
                    <div>
                        <span class="text-[10px] font-mono uppercase px-2 py-0.5 bg-[#CFFAFE] text-[#155E75] border border-[#A5F3FC] rounded font-bold">
                            TABLE 02 &bull; UPSTREAM VALUE CHAIN
                        </span>
                        <h3 class="text-sm font-serif font-bold text-[#1C1917] mt-1">
                            Upstream Equipment & Power Infrastructure Value Capture Matrix
                        </h3>
                    </div>
                    <span class="text-xs font-mono text-[#8C867A]">NVDA, AVGO, TSM, POWL</span>
                </div>
                <div class="overflow-x-auto custom-scroll">
                    <table class="fin-table">
                        <thead>
                            <tr>
                                <th>Company / Ticker</th>
                                <th>Primary Value Role</th>
                                <th>Hyperscaler CapEx Exposure</th>
                                <th>Gross Margin Structure</th>
                                <th>Order Book Backlog</th>
                                <th>Obsolescence / Cyclical Risk</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="font-semibold">Nvidia Corp (NASDAQ: NVDA)</td>
                                <td>Hopper (H100/H200) & Blackwell (B200) GPU Superclusters</td>
                                <td class="font-bold text-[#15803D]">~55–60% of Compute Spend</td>
                                <td>75.0% GAAP Gross Margin</td>
                                <td>12–18 Month Allocation Lead Times</td>
                                <td class="text-[#B91C1C]">High: 1-yr product cadences compress prior-gen asset valuations</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">Broadcom Inc (NASDAQ: AVGO)</td>
                                <td>Custom XPUs (Google TPU v5/v6, AWS Trainium 2/Inferentia) & Tomahawk 5 Switches</td>
                                <td class="font-bold text-[#0E7490]">~15–20% of AI CapEx</td>
                                <td>68.5% Adjusted Gross Margin</td>
                                <td>$30B+ Custom ASIC Pipeline</td>
                                <td class="text-[#15803D]">Moderate: Long sticky co-design cycles with hyperscalers</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">Taiwan Semiconductor (NYSE: TSM)</td>
                                <td>Sole Foundry for 3nm/2nm Silicon & CoWoS Packaging</td>
                                <td class="font-bold text-[#B45309]">~12–15% of Silicon BOM</td>
                                <td>53.5% Operating Margin</td>
                                <td>Full Fab Capacity booked through 2027</td>
                                <td class="text-[#57534E]">Low: Monopolistic packaging moat across both GPUs and ASICs</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">Powell Industries (NASDAQ: POWL)</td>
                                <td>Substation Transformers, Medium-Voltage Switchgear & Power Distribution for Gigawatt Campuses</td>
                                <td class="font-bold text-[#7C3AED]">~8–10% of Physical DC CapEx</td>
                                <td>27.5% Gross Margin (Expanding)</td>
                                <td>$1.4B+ Backlog (3.5x Book-to-Bill)</td>
                                <td class="text-[#15803D]">Very Low: Critical physical bottleneck with 2–4 year utility queues</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Table 3: Hyperscaler Useful Life Accounting Audit -->
            <div class="card overflow-hidden">
                <div class="p-4 bg-[#FAF7F2] border-b border-[#E5E0D8] flex justify-between items-center">
                    <div>
                        <span class="text-[10px] font-mono uppercase px-2 py-0.5 bg-[#FEE2E2] text-[#991B1B] border border-[#FECACA] rounded font-bold">
                            TABLE 03 &bull; FINANCIAL REPORTING FORENSICS
                        </span>
                        <h3 class="text-sm font-serif font-bold text-[#1C1917] mt-1">
                            Hyperscaler Stated Server Depreciable Lives vs. Technological Half-Life (ASC 360)
                        </h3>
                    </div>
                    <span class="text-xs font-mono text-[#8C867A]">10-K Footnote Audit</span>
                </div>
                <div class="overflow-x-auto custom-scroll">
                    <table class="fin-table">
                        <thead>
                            <tr>
                                <th>Hyperscaler / Ticker</th>
                                <th>Stated Server Useful Life</th>
                                <th>Historical Life Revision</th>
                                <th>Reported 2024 D&A ($B)</th>
                                <th>2026E CapEx ($B)</th>
                                <th>Economic GPU Life</th>
                                <th>ASC 360 Impairment Risk Trigger</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="font-semibold">Amazon.com (NASDAQ: AMZN)</td>
                                <td>5.0 Years (Servers)</td>
                                <td>Extended from 4.0 yrs in 2022 (+$3.6B EBIT benefit)</td>
                                <td>$48.7B</td>
                                <td class="font-bold text-[#B91C1C]">$115.0B</td>
                                <td class="text-[#B45309]">3.5 Years</td>
                                <td class="text-[#57534E]">When Trainium 2/H100 compute utilization drops post-B200 launch</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">Alphabet Inc (NASDAQ: GOOGL)</td>
                                <td>6.0 Years (Servers & Network)</td>
                                <td>Extended from 4.0 to 6.0 yrs in 2023 (+$3.9B EBIT benefit)</td>
                                <td>$11.5B</td>
                                <td class="font-bold text-[#B91C1C]">$85.0B</td>
                                <td class="text-[#B45309]">3.5 Years</td>
                                <td class="text-[#57534E]">When TPU v4/v5 hardware cannot match next-gen model training throughput</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">Microsoft Corp (NASDAQ: MSFT)</td>
                                <td>6.0 Years (Servers)</td>
                                <td>Extended from 4.0 to 6.0 yrs in 2023 (+$3.7B EBIT benefit)</td>
                                <td>$13.9B</td>
                                <td class="font-bold text-[#B91C1C]">$105.0B</td>
                                <td class="text-[#B45309]">3.0 Years</td>
                                <td class="text-[#57534E]">When OpenAI models migrate fully from Hopper to Blackwell architectures</td>
                            </tr>
                            <tr>
                                <td class="font-semibold">Meta Platforms (NASDAQ: META)</td>
                                <td>5.5 Years (Servers & Gear)</td>
                                <td>Extended from 4.0 to 5.0 yrs in 2022, then 5.5 yrs in 2024</td>
                                <td>$13.7B</td>
                                <td class="font-bold text-[#B91C1C]">$89.0B</td>
                                <td class="text-[#B45309]">3.5 Years</td>
                                <td class="text-[#57534E]">When open-source Llama 4/5 models demand Blackwell-tier FP4/FP6 compute</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

        <!-- Section 4: Mathematical Derivations & Accounting Rules -->
        <div class="card p-6 bg-[#FAF7F2] space-y-4">
            <h3 class="text-sm font-serif font-bold text-[#1C1917] border-b border-[#E5E0D8] pb-2">
                Quantitative Audit Rules & Derivation Methodology
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono text-[#57534E]">
                <div class="p-3 bg-[#FFFFFF] border border-[#E5E0D8] rounded space-y-1.5">
                    <strong class="text-[#B45309] block uppercase text-[10.5px]">1. Capitalized Lease/Debt Equivalence (ASC 842 / IFRS 16)</strong>
                    <p class="leading-relaxed font-sans text-xs">
                        Under Damodaran Ginzu DCF and GAAP rules, multi-year unconditional purchase obligations represent senior capitalized debt claims:
                    </p>
                    <code class="block p-2 bg-[#F4EFEB] rounded text-[11px] text-[#1C1917]">
                        PV_Debt = Sum [ Spend_t / (1 + WACC)^t ] = $376.0B (undiscounted $265.6B)
                    </code>
                    <p class="leading-relaxed font-sans text-xs">
                        Imputed Interest = PV_Debt &times; Pre-tax Cost of Debt (6.25%) = $23.5B / year subtracted from enterprise value before calculating equity claims.
                    </p>
                </div>

                <div class="p-3 bg-[#FFFFFF] border border-[#E5E0D8] rounded space-y-1.5">
                    <strong class="text-[#0E7490] block uppercase text-[10.5px]">2. Unit Token Amortization Breakeven Formula</strong>
                    <p class="leading-relaxed font-sans text-xs">
                        Hardware breakeven cost per million tokens measures all-in cluster capitalization divided by total inference throughput:
                    </p>
                    <code class="block p-2 bg-[#F4EFEB] rounded text-[11px] text-[#1C1917]">
                        Unit_Cost = (Cluster_Capex / Useful_Life_Hours + Power_Cost_hr) / Tokens_per_hr
                    </code>
                    <p class="leading-relaxed font-sans text-xs">
                        For an 8&times;H100 SXM5 node ($300k acquisition, 65% duty cycle, 3.5-yr useful life): Unit cost is $5.74 per 1M blended tokens.
                    </p>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-[#FFFFFF] border-t border-[#E5E0D8] py-6 px-6 mt-12 text-center text-xs font-mono text-[#8C867A]">
        Anthropic, PBC (NASDAQ: ANT) &bull; Thematic AI CapEx & Counterparty Circularity Matrix &bull; Gate 5 Research Suite
    </footer>

    <!-- Client-Side Engine & Charts Script -->
    <script>
        // Data payload from Python engine
        const circularityData = {json.dumps(circ)};
        const annualSchedule = {json.dumps(annual_circ)};
        const deprCliff = {json.dumps(depr)};
        const tokenMargins = {json.dumps(tokens)};

        // Chart 1: Circular Flow Chart
        const ctxCirc = document.getElementById('circularFlowChart').getContext('2d');
        const circularChart = new Chart(ctxCirc, {{
            type: 'bar',
            data: {{
                labels: ['Amazon (AWS)', 'Google (GCP)', 'Combined Hyperscaler'],
                datasets: [
                    {{
                        label: 'Equity Invested ($B)',
                        data: [23.0, 13.0, 36.0],
                        backgroundColor: '#B45309',
                        borderRadius: 4
                    }},
                    {{
                        label: 'Contractual Compute Spend ($B)',
                        data: [164.7, 100.9, 265.6],
                        backgroundColor: '#0E7490',
                        borderRadius: 4
                    }},
                    {{
                        label: 'Implied Enterprise Value Uplift ($B)',
                        data: [1482.0, 857.9, 2339.9],
                        backgroundColor: '#15803D',
                        borderRadius: 4
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'top', labels: {{ font: {{ family: 'Inter', size: 11 }} }} }}
                }},
                scales: {{
                    y: {{
                        type: 'logarithmic',
                        title: {{ display: true, text: 'USD Billions (Log Scale)', font: {{ family: 'Inter', size: 10 }} }},
                        grid: {{ color: '#ECE7DE' }}
                    }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        // Chart 2: CapEx Supercycle
        const ctxCapex = document.getElementById('capexSupercycleChart').getContext('2d');
        const capexChart = new Chart(ctxCapex, {{
            type: 'bar',
            data: {{
                labels: deprCliff.map(x => x.year),
                datasets: [
                    {{
                        type: 'bar',
                        label: 'Big 4 CapEx ($B)',
                        data: deprCliff.map(x => x.annual_capex_usd_b),
                        backgroundColor: '#1C1917',
                        borderRadius: 4,
                        yAxisID: 'y'
                    }},
                    {{
                        type: 'line',
                        label: 'Realistic Economic D&A ($B)',
                        data: deprCliff.map(x => x.realistic_dna_usd_b),
                        borderColor: '#B91C1C',
                        backgroundColor: 'rgba(185, 28, 28, 0.1)',
                        borderWidth: 2,
                        tension: 0.2,
                        fill: false,
                        yAxisID: 'y'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'top', labels: {{ font: {{ family: 'Inter', size: 11 }} }} }}
                }},
                scales: {{
                    y: {{
                        title: {{ display: true, text: 'USD Billions', font: {{ family: 'Inter', size: 10 }} }},
                        grid: {{ color: '#ECE7DE' }}
                    }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        // Chart 3: ASC 360 Depreciation Cliff
        const ctxCliff = document.getElementById('depreciationCliffChart').getContext('2d');
        const cliffChart = new Chart(ctxCliff, {{
            type: 'bar',
            data: {{
                labels: deprCliff.map(x => x.year),
                datasets: [
                    {{
                        type: 'bar',
                        label: 'Stated D&A (5.5-yr)',
                        data: deprCliff.map(x => x.stated_dna_usd_b),
                        backgroundColor: '#CBD5E1',
                        borderRadius: 3
                    }},
                    {{
                        type: 'bar',
                        label: 'Realistic D&A (3.5-yr)',
                        data: deprCliff.map(x => x.realistic_dna_usd_b),
                        backgroundColor: '#F87171',
                        borderRadius: 3
                    }},
                    {{
                        type: 'line',
                        label: 'Unrecorded Gap ($B)',
                        data: deprCliff.map(x => x.annual_depreciation_gap_usd_b),
                        borderColor: '#B91C1C',
                        borderWidth: 2.5,
                        tension: 0.2,
                        yAxisID: 'y'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'top', labels: {{ font: {{ family: 'Inter', size: 11 }} }} }}
                }},
                scales: {{
                    y: {{
                        title: {{ display: true, text: 'USD Billions', font: {{ family: 'Inter', size: 10 }} }},
                        grid: {{ color: '#ECE7DE' }}
                    }},
                    x: {{ grid: {{ display: false }} }}
                }}
            }}
        }});

        // Chart 4: Token Breakeven
        const ctxToken = document.getElementById('tokenBreakevenChart').getContext('2d');
        const tokenChart = new Chart(ctxToken, {{
            type: 'line',
            data: {{
                labels: tokenMargins.map(x => x.model.replace(' (Initial)', '')),
                datasets: [
                    {{
                        label: 'Blended Price ($ / 1M Tok)',
                        data: tokenMargins.map(x => x.blended_price_usd),
                        borderColor: '#0E7490',
                        backgroundColor: 'rgba(14, 116, 144, 0.15)',
                        borderWidth: 2.5,
                        fill: true,
                        tension: 0.1
                    }},
                    {{
                        label: 'H100 Breakeven Hardware Cost ($5.74)',
                        data: tokenMargins.map(() => 5.74),
                        borderColor: '#B91C1C',
                        borderWidth: 2,
                        borderDash: [6, 4],
                        pointRadius: 0
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{ position: 'top', labels: {{ font: {{ family: 'Inter', size: 11 }} }} }}
                }},
                scales: {{
                    y: {{
                        title: {{ display: true, text: 'USD / Million Tokens', font: {{ family: 'Inter', size: 10 }} }},
                        grid: {{ color: '#ECE7DE' }}
                    }},
                    x: {{
                        grid: {{ display: false }},
                        ticks: {{ maxRotation: 45, minRotation: 25, font: {{ size: 10 }} }}
                    }}
                }}
            }}
        }});

        // Scenario Slider Logic
        function updateScenario() {{
            const drawdown = parseFloat(document.getElementById('sliderDrawdown').value);
            const life = parseFloat(document.getElementById('sliderLife').value);
            const deflation = parseFloat(document.getElementById('sliderDeflation').value);

            document.getElementById('sliderDrawdownVal').innerText = drawdown + '% ($' + (265.6 * (drawdown / 100)).toFixed(1) + 'B)';
            document.getElementById('sliderLifeVal').innerText = life.toFixed(1) + ' Years';
            document.getElementById('sliderDeflationVal').innerText = '-' + deflation + '% Shocker';

            // Recalculate ARR
            const adjARR = 265.6 * (drawdown / 100);
            const adjAWS = 164.7 * (drawdown / 100);
            const adjGCP = 100.9 * (drawdown / 100);
            document.getElementById('kpiRecalculatedARR').innerText = '$' + adjARR.toFixed(1) + ' Billion';
            document.getElementById('kpiRecalculatedEBIT').innerText = 'AWS: $' + adjAWS.toFixed(1) + 'B • GCP: $' + adjGCP.toFixed(1) + 'B';

            // Recalculate Peak Gap based on life
            // Standard stated is 5.5 yrs. If life is 3.5, gap is 45.5. If life is 5.5, gap is 0.
            const lifeFactor = Math.max(0, (5.5 - life) / 2.0);
            const peakGap = 45.5 * lifeFactor;
            const overhang = 176.7 * lifeFactor;
            const marginDrag = Math.round(989 * lifeFactor);

            document.getElementById('kpiPeakGap').innerText = '$' + peakGap.toFixed(1) + 'B / Year';
            document.getElementById('kpiOverhang').innerText = '$' + overhang.toFixed(1) + 'B PP&E Overhang';
            document.getElementById('kpiMarginDrag').innerText = '-' + marginDrag + ' bps';

            // Recalculate Sonnet Margin
            const baseSonnetPrice = 9.0;
            const shockedSonnetPrice = baseSonnetPrice * (1 - deflation / 100);
            const h100Cost = 5.74;
            const spread = shockedSonnetPrice - h100Cost;
            const marginPct = (spread / shockedSonnetPrice) * 100;

            const kpiSpreadElem = document.getElementById('kpiSonnetMargin');
            const kpiStatusElem = document.getElementById('kpiSonnetStatus');

            if (spread >= 0) {{
                kpiSpreadElem.className = 'text-[#15803D] text-sm font-bold';
                kpiSpreadElem.innerText = '+$' + spread.toFixed(2) + ' (' + marginPct.toFixed(1) + '%)';
                kpiStatusElem.className = 'text-[10px] text-[#15803D] block mt-0.5';
                kpiStatusElem.innerText = 'Healthy Above Breakeven';
            }} else {{
                kpiSpreadElem.className = 'text-[#B91C1C] text-sm font-bold';
                kpiSpreadElem.innerText = '-$' + Math.abs(spread).toFixed(2) + ' (' + marginPct.toFixed(1) + '%)';
                kpiStatusElem.className = 'text-[10px] text-[#B91C1C] block mt-0.5';
                kpiStatusElem.innerText = 'GROSS MARGIN IMPAIRMENT';
            }}
        }}
    </script>
</body>
</html>"""

    # Output paths
    paths = [
        os.path.join(os.path.dirname(__file__), "..", "reports", "index.html"),
        os.path.join(os.path.dirname(__file__), "..", "..", "US_EQUITIES", "ANTHROPIC", "reports", "thematic_capex.html"),
        "/Users/worldofmadness/Documents/VS Code/Personal Projects/ervis-terminal/equities/anthropic/thematic_capex.html"
    ]

    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as out:
            out.write(html_content)
        print(f"[REPORT BUILT] {p}")

if __name__ == "__main__":
    generate_thematic_html()
