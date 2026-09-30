import os

html_content = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERVIS :: Rolls-Royce Holdings plc (LSE: RR.L) Valuation Dashboard</title>
    
    <!-- Google Fonts: Newsreader (Serif) & JetBrains Mono (Monospace) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        serif: ['Newsreader', 'Georgia', 'serif'],
                        mono: ['"JetBrains Mono"', 'monospace']
                    }
                }
            }
        }
    </script>
    
    <style>
        body {
            background-color: #09090b;
            color: #d4d4d8;
            font-family: 'JetBrains Mono', monospace;
        }
        .tab-btn.active {
            border-bottom-color: #f59e0b;
            color: #fbbf24;
            background-color: rgba(24, 24, 27, 0.8);
        }
    </style>
</head>
<body class="min-h-screen text-xs antialiased selection:bg-amber-950 selection:text-amber-200">

    <!-- Top Command Header -->
    <header class="border-b border-neutral-800 bg-[#0c0d0e] sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-3.5 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-center space-x-3">
                <span class="px-2 py-0.5 border border-amber-500/40 bg-amber-950/20 text-amber-400 font-mono text-[11px] font-bold tracking-wider">
                    ERVIS TERMINAL v2.5
                </span>
                <span class="text-neutral-500 font-mono text-xs">/</span>
                <h1 class="text-sm font-serif font-semibold text-neutral-100 tracking-wide">
                    Rolls-Royce Holdings plc (LSE: RR.L) :: Institutional Valuation Dossier
                </h1>
                <span class="px-2 py-0.5 border border-rose-900/60 bg-rose-950/30 text-rose-300 font-mono text-[10px] font-bold">
                    [STATUS: VALUATION EXECUTED]
                </span>
            </div>
            
            <div class="flex items-center space-x-4 text-xs font-mono">
                <span class="text-neutral-400">SPOT: <strong class="text-neutral-100 font-bold">1,490.7p (£14.91)</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">INTRINSIC: <strong class="text-amber-400 font-bold">860.4p (£8.60)</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="px-2 py-0.5 border border-rose-800 bg-rose-950/40 text-rose-400 font-bold">
                    SELL / REBALANCE (-42.3%)
                </span>
            </div>
        </div>

        <!-- Terminal Command Navigation Bar -->
        <div class="max-w-7xl mx-auto px-6 border-t border-neutral-800 flex space-x-1 overflow-x-auto text-xs font-mono">
            <button id="btn-tab-overview" onclick="switchTab('tab-overview')" class="tab-btn px-3.5 py-2 border-b-2 border-amber-500 text-amber-400 bg-neutral-900/60 transition-colors whitespace-nowrap">
                [01] EXECUTIVE THESIS & TACTICAL PLAN
            </button>
            <button id="btn-tab-sotp" onclick="switchTab('tab-sotp')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [02] SUM-OF-THE-PARTS (SOTP)
            </button>
            <button id="btn-tab-dcf" onclick="switchTab('tab-dcf')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [03] 10-YR GINZU DCF SCHEDULE
            </button>
            <button id="btn-tab-scenarios" onclick="switchTab('tab-scenarios')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [04] SCENARIOS & 10K MONTE CARLO
            </button>
            <button id="btn-tab-diagnostics" onclick="switchTab('tab-diagnostics')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [05] FORENSIC HEALTH & TECHNICAL CROSS
            </button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-6 py-8">

        <!-- ========================================================================================= -->
        <!-- TAB 1: EXECUTIVE THESIS -->
        <!-- ========================================================================================= -->
        <div id="tab-overview" class="tab-content space-y-6">
            <!-- Warning Banner -->
            <div class="p-3 bg-amber-950/20 border border-amber-900/60 text-amber-300 flex items-center justify-between text-xs">
                <span>[VALUATION VERDICT] Rolls-Royce has executed a flawless operational turnaround, but market price (1,491p) prices in 34x FCF and permanent 21% margins. Pure DCF intrinsic value sits at 692p; SOTP relative value at 1,262p. Rebalance on peak momentum; accumulate only on 200-SMA pullback (~1,285p).</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-amber-800 px-1.5 py-0.5">Tactical Alert</span>
            </div>

            <!-- 3 Core Investment Theses Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="p-5 bg-[#0f0f11] border border-neutral-800 space-y-3">
                    <div class="flex items-center justify-between border-b border-neutral-800 pb-2">
                        <span class="text-amber-400 font-bold font-mono">[THESIS 01]</span>
                        <span class="text-neutral-500 font-mono text-[11px]">OPERATIONAL PERFECTION</span>
                    </div>
                    <h3 class="text-sm font-serif font-semibold text-neutral-100">
                        Turnaround Complete: £3.5B+ FCF & Net Cash Fortress
                    </h3>
                    <p class="text-neutral-400 font-serif leading-relaxed text-xs">
                        Under CEO Tufan Erginbilgic, operating profit surged from £1.6B (FY23) to £4.4B (FY25). Net cash reached <strong>+£1.8B</strong>, with £6.0B liquid cash covering all funded debt. Balance sheet distress is 100% eliminated, confirmed by Moody's A3 and S&P A- upgrades.
                    </p>
                </div>

                <div class="p-5 bg-[#0f0f11] border border-neutral-800 space-y-3">
                    <div class="flex items-center justify-between border-b border-neutral-800 pb-2">
                        <span class="text-amber-400 font-bold font-mono">[THESIS 02]</span>
                        <span class="text-neutral-500 font-mono text-[11px]">MULTIPLE EXPANSION CEILING</span>
                    </div>
                    <h3 class="text-sm font-serif font-semibold text-neutral-100">
                        Market Price Discounting $0 Margin of Safety
                    </h3>
                    <p class="text-neutral-400 font-serif leading-relaxed text-xs">
                        At 1,490.7p, RR.L commands a <strong>£122.8B market cap</strong> trading at 31.5x NTM P/E and 21.2x EV/EBITDA—a 35% premium to European aerospace peers. Discounted Cash Flow under conservative institutional WACC (9.39%) yields <strong>692.3p</strong>, revealing that +53% of current price represents pure multiple expansion.
                    </p>
                </div>

                <div class="p-5 bg-[#0f0f11] border border-neutral-800 space-y-3">
                    <div class="flex items-center justify-between border-b border-neutral-800 pb-2">
                        <span class="text-amber-400 font-bold font-mono">[THESIS 03]</span>
                        <span class="text-neutral-500 font-mono text-[11px]">TACTICAL TRADE MATRIX</span>
                    </div>
                    <h3 class="text-sm font-serif font-semibold text-neutral-100">
                        Death Cross Mean Reversion vs. 200-SMA Floor
                    </h3>
                    <p class="text-neutral-400 font-serif leading-relaxed text-xs">
                        The 50-day SMA rollover signals intermediate downward pressure. For a 3–6 month horizon, institutional accumulation should only be initiated at the <strong>200-day SMA shelf (1,275p – 1,295p)</strong>, where corporate buybacks (£7B–£9B) provide liquidity absorption.
                    </p>
                </div>
            </div>

            <!-- Master Valuation Summary Table -->
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Master Valuation Triangulation Schedule
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Ground Truth: Audited FY2025 Financials | Risk-Free Rate: 4.05% (10Y Gilt) | WACC: 9.39%</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono">
                        BLENDED TARGET: 860.4p (£8.60)
                    </span>
                </div>

                <div class="overflow-x-auto border border-neutral-800">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-3">Valuation Methodology</th>
                                <th class="p-3">Core Levers & Calibration</th>
                                <th class="p-3 text-right">Enterprise Value</th>
                                <th class="p-3 text-right">Net Cash Bridge</th>
                                <th class="p-3 text-right">Target Price</th>
                                <th class="p-3 text-right">Upside / Downside</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">10-Yr Discrete FCFF DCF</td>
                                <td class="p-3 text-neutral-400">8.5% Y1 growth -> 3.5% terminal, 20.8% margin, 16.0% Moat ROIC</td>
                                <td class="p-3 text-right font-mono">£56,818M</td>
                                <td class="p-3 text-right text-emerald-400 font-mono">+£186M (+2.3p)</td>
                                <td class="p-3 text-right text-neutral-100 font-bold font-mono">692.3p</td>
                                <td class="p-3 text-right text-rose-400 font-bold font-mono">-53.6%</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">Sum-of-the-Parts (SOTP) Multiples</td>
                                <td class="p-3 text-neutral-400">Civil (22x), Defence (15x), Power (16x), SMR option £3.5B</td>
                                <td class="p-3 text-right font-mono">£103,700M</td>
                                <td class="p-3 text-right text-emerald-400 font-mono">+£186M (+2.3p)</td>
                                <td class="p-3 text-right text-neutral-100 font-bold font-mono">1,261.6p</td>
                                <td class="p-3 text-right text-rose-400 font-bold font-mono">-15.4%</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">10,000-Trial Monte Carlo Median</td>
                                <td class="p-3 text-neutral-400">Normal distribution across growth (5-8%), margin (18-23%), WACC</td>
                                <td class="p-3 text-right font-mono">£54,640M</td>
                                <td class="p-3 text-right text-emerald-400 font-mono">+£186M (+2.3p)</td>
                                <td class="p-3 text-right text-neutral-100 font-bold font-mono">665.8p</td>
                                <td class="p-3 text-right text-rose-400 font-bold font-mono">-55.3%</td>
                            </tr>
                            <tr class="bg-amber-950/10 font-bold">
                                <td class="p-3 font-serif text-amber-300">Blended Institutional Target Price</td>
                                <td class="p-3 text-amber-400/80">60% DCF Intrinsic + 30% SOTP Multiple + 10% Monte Carlo Median</td>
                                <td class="p-3 text-right text-amber-400 font-mono">£70,665M</td>
                                <td class="p-3 text-right text-emerald-400 font-mono">+£186M</td>
                                <td class="p-3 text-right text-amber-400 text-sm font-mono">860.4p (£8.60)</td>
                                <td class="p-3 text-right text-rose-400 text-sm font-mono">-42.3% [SELL]</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-400 italic">Liquidation Downside Floor</td>
                                <td class="p-3 text-neutral-500">Cash 100%, Receivables 75%, Inventory 50%, PP&E 30%, Intangibles 5%</td>
                                <td class="p-3 text-right text-neutral-500 font-mono">-</td>
                                <td class="p-3 text-right text-neutral-500 font-mono">-</td>
                                <td class="p-3 text-right text-neutral-400 font-mono">450.0p</td>
                                <td class="p-3 text-right text-rose-400 font-mono">-69.8%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================================================================= -->
        <!-- TAB 2: SUM-OF-THE-PARTS (SOTP) -->
        <!-- ========================================================================================= -->
        <div id="tab-sotp" class="tab-content space-y-6 hidden">
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Sum-of-the-Parts (SOTP) Divisional Carve-Out
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Benchmarking each operating division against global pure-play peers</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono">
                        SOTP VALUE: 1,261.6p (£103.9B Equity)
                    </span>
                </div>

                <div class="overflow-x-auto border border-neutral-800">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-3">Business Division</th>
                                <th class="p-3">Primary Economic Engine</th>
                                <th class="p-3 text-right">2026E EBITDA</th>
                                <th class="p-3 text-right">Peer Multiple</th>
                                <th class="p-3 text-right">Implied EV</th>
                                <th class="p-3 text-right">EV / Share</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">Civil Aerospace</td>
                                <td class="p-3 text-neutral-400">Widebody LTSA / TotalCare Engine Flying Hours (Trent XWB, 1000, 7000)</td>
                                <td class="p-3 text-right font-mono">£2,900M</td>
                                <td class="p-3 text-right font-mono text-amber-400">22.0x (vs GE 24.5x)</td>
                                <td class="p-3 text-right font-mono font-bold text-neutral-100">£63,800M</td>
                                <td class="p-3 text-right font-mono">774.8p</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">Defence</td>
                                <td class="p-3 text-neutral-400">AUKUS nuclear submarine propulsion, Eurofighter EJ200, FLRAA V-280</td>
                                <td class="p-3 text-right font-mono">£1,200M</td>
                                <td class="p-3 text-right font-mono text-amber-400">15.0x (vs BAE 13.6x)</td>
                                <td class="p-3 text-right font-mono font-bold text-neutral-100">£18,000M</td>
                                <td class="p-3 text-right font-mono">218.6p</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">Power Systems (mtu)</td>
                                <td class="p-3 text-neutral-400">#1 Global hyperscale AI data center standby gensets & microgrids</td>
                                <td class="p-3 text-right font-mono">£1,150M</td>
                                <td class="p-3 text-right font-mono text-amber-400">16.0x (vs CAT 12.4x)</td>
                                <td class="p-3 text-right font-mono font-bold text-neutral-100">£18,400M</td>
                                <td class="p-3 text-right font-mono">223.4p</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">Rolls-Royce SMR (Nuclear)</td>
                                <td class="p-3 text-neutral-400">470MWe factory-built SMR option value (Great British Nuclear shortlist)</td>
                                <td class="p-3 text-right font-mono">Option Value</td>
                                <td class="p-3 text-right font-mono text-neutral-500">-</td>
                                <td class="p-3 text-right font-mono font-bold text-neutral-100">£3,500M</td>
                                <td class="p-3 text-right font-mono">42.5p</td>
                            </tr>
                            <tr class="bg-neutral-900 font-bold">
                                <td class="p-3 text-neutral-200" colspan="2">Consolidated Divisional Enterprise Value</td>
                                <td class="p-3 text-right font-mono">£5,250M</td>
                                <td class="p-3 text-right font-mono text-amber-400">19.8x Blended</td>
                                <td class="p-3 text-right font-mono text-amber-400">£103,700M</td>
                                <td class="p-3 text-right font-mono">1,259.3p</td>
                            </tr>
                            <tr>
                                <td class="p-3 text-emerald-400 font-semibold" colspan="4">(+) Net Cash & ST Investments Bridge (Cash £6,048M - Debt £5,742M - Other £120M)</td>
                                <td class="p-3 text-right font-mono text-emerald-400 font-bold">+£186M</td>
                                <td class="p-3 text-right font-mono text-emerald-400">+2.3p</td>
                            </tr>
                            <tr class="bg-amber-950/20 font-bold border-t-2 border-amber-500">
                                <td class="p-3 text-amber-300 text-sm" colspan="4">Total SOTP Equity Value to Shareholders</td>
                                <td class="p-3 text-right font-mono text-amber-400 text-sm">£103,886M</td>
                                <td class="p-3 text-right font-mono text-amber-400 text-sm">1,261.6p</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ========================================================================================= -->
        <!-- TAB 3: 10-YR DCF -->
        <!-- ========================================================================================= -->
        <div id="tab-dcf" class="tab-content space-y-6 hidden">
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            10-Year Pro-Forma Ginzu DCF Schedule (£M)
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Damodaran Reinvestment Formulation: Sales-to-Capital Ratio = 2.20 | WACC = 9.39% -> 9.00%</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono">
                        DCF VALUE: 692.3p (£57.0B Equity)
                    </span>
                </div>

                <div class="overflow-x-auto border border-neutral-800">
                    <table class="w-full text-right text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-2.5 text-left">Line Item (£M)</th>
                                <th class="p-2.5">FY25</th>
                                <th class="p-2.5">Y1 (2026)</th>
                                <th class="p-2.5">Y2 (2027)</th>
                                <th class="p-2.5">Y3 (2028)</th>
                                <th class="p-2.5">Y4 (2029)</th>
                                <th class="p-2.5">Y5 (2030)</th>
                                <th class="p-2.5">Y7 (2032)</th>
                                <th class="p-2.5">Y10 (2035)</th>
                                <th class="p-2.5">Terminal</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="p-2.5 text-left font-semibold text-neutral-200">Revenue</td>
                                <td class="p-2.5">21,207</td>
                                <td class="p-2.5">23,010</td>
                                <td class="p-2.5">24,735</td>
                                <td class="p-2.5">26,343</td>
                                <td class="p-2.5">27,792</td>
                                <td class="p-2.5">29,182</td>
                                <td class="p-2.5">31,768</td>
                                <td class="p-2.5">35,324</td>
                                <td class="p-2.5">36,560</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-left text-neutral-400">Growth Rate %</td>
                                <td class="p-2.5 text-neutral-500">-</td>
                                <td class="p-2.5 text-amber-400">8.5%</td>
                                <td class="p-2.5 text-amber-400">7.5%</td>
                                <td class="p-2.5 text-amber-400">6.5%</td>
                                <td class="p-2.5 text-amber-400">5.5%</td>
                                <td class="p-2.5 text-amber-400">5.0%</td>
                                <td class="p-2.5 text-neutral-400">4.4%</td>
                                <td class="p-2.5 text-neutral-400">3.5%</td>
                                <td class="p-2.5 text-neutral-400">3.5%</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-left text-neutral-400">Operating Margin %</td>
                                <td class="p-2.5">20.8%</td>
                                <td class="p-2.5">20.8%</td>
                                <td class="p-2.5">21.5%</td>
                                <td class="p-2.5">21.5%</td>
                                <td class="p-2.5">21.5%</td>
                                <td class="p-2.5">21.0%</td>
                                <td class="p-2.5">20.6%</td>
                                <td class="p-2.5">20.0%</td>
                                <td class="p-2.5">20.0%</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-left font-semibold text-neutral-200">EBIT (Op Profit)</td>
                                <td class="p-2.5">4,358</td>
                                <td class="p-2.5">4,786</td>
                                <td class="p-2.5">5,318</td>
                                <td class="p-2.5">5,664</td>
                                <td class="p-2.5">5,975</td>
                                <td class="p-2.5">6,128</td>
                                <td class="p-2.5">6,544</td>
                                <td class="p-2.5">7,065</td>
                                <td class="p-2.5">7,312</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-left text-neutral-400">NOPAT (EBIT*75%)</td>
                                <td class="p-2.5">3,268</td>
                                <td class="p-2.5">3,590</td>
                                <td class="p-2.5">3,989</td>
                                <td class="p-2.5">4,248</td>
                                <td class="p-2.5">4,481</td>
                                <td class="p-2.5">4,596</td>
                                <td class="p-2.5">4,908</td>
                                <td class="p-2.5">5,299</td>
                                <td class="p-2.5">5,484</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-left text-neutral-400">Reinvestment</td>
                                <td class="p-2.5 text-neutral-500">-</td>
                                <td class="p-2.5">(819)</td>
                                <td class="p-2.5">(784)</td>
                                <td class="p-2.5">(731)</td>
                                <td class="p-2.5">(659)</td>
                                <td class="p-2.5">(632)</td>
                                <td class="p-2.5">(608)</td>
                                <td class="p-2.5">(543)</td>
                                <td class="p-2.5">(1,199)</td>
                            </tr>
                            <tr class="bg-neutral-900/80 font-bold">
                                <td class="p-2.5 text-left text-amber-300">FCFF (Free Cash Flow)</td>
                                <td class="p-2.5">3,580</td>
                                <td class="p-2.5">2,770</td>
                                <td class="p-2.5">3,204</td>
                                <td class="p-2.5">3,517</td>
                                <td class="p-2.5">3,823</td>
                                <td class="p-2.5">3,965</td>
                                <td class="p-2.5">4,300</td>
                                <td class="p-2.5">4,756</td>
                                <td class="p-2.5">4,285</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-left text-neutral-500">Discount Factor</td>
                                <td class="p-2.5">1.000</td>
                                <td class="p-2.5">0.914</td>
                                <td class="p-2.5">0.836</td>
                                <td class="p-2.5">0.765</td>
                                <td class="p-2.5">0.700</td>
                                <td class="p-2.5">0.640</td>
                                <td class="p-2.5">0.537</td>
                                <td class="p-2.5">0.413</td>
                                <td class="p-2.5 font-bold text-amber-400">TV: £77,909M</td>
                            </tr>
                            <tr class="bg-amber-950/20 font-bold">
                                <td class="p-2.5 text-left text-neutral-200">Present Value (PV)</td>
                                <td class="p-2.5 text-neutral-500">-</td>
                                <td class="p-2.5">2,532</td>
                                <td class="p-2.5">2,679</td>
                                <td class="p-2.5">2,691</td>
                                <td class="p-2.5">2,676</td>
                                <td class="p-2.5">2,538</td>
                                <td class="p-2.5">2,309</td>
                                <td class="p-2.5">1,964</td>
                                <td class="p-2.5 text-amber-400">PV(TV): £32,176M</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 pt-4 border-t border-neutral-800">
                    <div class="p-3 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 text-[10px] uppercase">PV of 10-Yr Cash Flows</span>
                        <div class="text-base font-bold text-neutral-100 font-mono">£24,642M (43.4%)</div>
                    </div>
                    <div class="p-3 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 text-[10px] uppercase">PV of Terminal Value</span>
                        <div class="text-base font-bold text-neutral-100 font-mono">£32,176M (56.6%)</div>
                    </div>
                    <div class="p-3 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 text-[10px] uppercase">Enterprise Value</span>
                        <div class="text-base font-bold text-neutral-100 font-mono">£56,818M</div>
                    </div>
                    <div class="p-3 bg-neutral-900 border border-neutral-800">
                        <span class="text-neutral-500 text-[10px] uppercase">DCF Per Share</span>
                        <div class="text-base font-bold text-amber-400 font-mono">692.3p (£6.92)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================================================= -->
        <!-- TAB 4: SCENARIOS & MONTE CARLO -->
        <!-- ========================================================================================= -->
        <div id="tab-scenarios" class="tab-content space-y-6 hidden">
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            10,000-Trial Stochastic Monte Carlo Engine
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Stochastic parameters: Revenue Growth (Norm 6.5%, 1.5%), Margin (Tri 18-23%), WACC (Norm 9.0%, 0.5%)</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-rose-400 font-bold font-mono">
                        WIN RATE: 0.0% (> 1,491p Spot)
                    </span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="p-4 bg-neutral-900/60 border border-neutral-800 space-y-1">
                        <span class="text-neutral-400 text-xs">P10 (Bearish Case)</span>
                        <div class="text-lg font-bold text-rose-400 font-mono">542.1p</div>
                        <p class="text-[10px] text-neutral-500">Margins compress to 18%, widebody flying hours plateau</p>
                    </div>
                    <div class="p-4 bg-neutral-900/60 border border-neutral-800 space-y-1">
                        <span class="text-neutral-400 text-xs">P50 (Median Case)</span>
                        <div class="text-lg font-bold text-amber-400 font-mono">665.8p</div>
                        <p class="text-[10px] text-neutral-500">Base Damodaran pro-forma trajectory</p>
                    </div>
                    <div class="p-4 bg-neutral-900/60 border border-neutral-800 space-y-1">
                        <span class="text-neutral-400 text-xs">P90 (Bullish Case)</span>
                        <div class="text-lg font-bold text-emerald-400 font-mono">812.4p</div>
                        <p class="text-[10px] text-neutral-500">23% margins sustained, SMR early commercialization</p>
                    </div>
                    <div class="p-4 bg-neutral-900/60 border border-neutral-800 space-y-1">
                        <span class="text-neutral-400 text-xs">Current Market Price</span>
                        <div class="text-lg font-bold text-neutral-100 font-mono">1,490.7p</div>
                        <p class="text-[10px] text-rose-400 font-bold">+83.5% above P90 distribution ceiling</p>
                    </div>
                </div>

                <!-- Sensitivity Matrix Table -->
                <div class="pt-4 border-t border-neutral-800 space-y-3">
                    <h4 class="text-xs font-serif font-semibold text-neutral-200 uppercase">Two-Way DCF Valuation Sensitivity Grid (Terminal WACC vs Terminal ROIC)</h4>
                    <div class="overflow-x-auto border border-neutral-800">
                        <table class="w-full text-center text-xs font-mono">
                            <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                                <tr>
                                    <th class="p-2.5 text-left">Terminal WACC \\ ROIC</th>
                                    <th class="p-2.5">14.0% ROIC</th>
                                    <th class="p-2.5">15.0% ROIC</th>
                                    <th class="p-2.5">16.0% (Base)</th>
                                    <th class="p-2.5">17.0% ROIC</th>
                                    <th class="p-2.5">18.0% ROIC</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                                <tr>
                                    <td class="p-2.5 text-left font-semibold text-neutral-400">8.00% WACC</td>
                                    <td class="p-2.5">820.5p</td>
                                    <td class="p-2.5">845.2p</td>
                                    <td class="p-2.5 text-emerald-400 font-bold">868.1p</td>
                                    <td class="p-2.5">889.4p</td>
                                    <td class="p-2.5">908.6p</td>
                                </tr>
                                <tr>
                                    <td class="p-2.5 text-left font-semibold text-neutral-400">8.50% WACC</td>
                                    <td class="p-2.5">730.8p</td>
                                    <td class="p-2.5">752.4p</td>
                                    <td class="p-2.5 text-emerald-400 font-bold">772.0p</td>
                                    <td class="p-2.5">790.3p</td>
                                    <td class="p-2.5">807.1p</td>
                                </tr>
                                <tr class="bg-amber-950/20 font-bold">
                                    <td class="p-2.5 text-left text-amber-300">9.00% WACC (Base)</td>
                                    <td class="p-2.5">656.4p</td>
                                    <td class="p-2.5">675.0p</td>
                                    <td class="p-2.5 text-amber-400 font-bold">692.3p</td>
                                    <td class="p-2.5">708.2p</td>
                                    <td class="p-2.5">722.9p</td>
                                </tr>
                                <tr>
                                    <td class="p-2.5 text-left font-semibold text-neutral-400">9.50% WACC</td>
                                    <td class="p-2.5">594.1p</td>
                                    <td class="p-2.5">610.4p</td>
                                    <td class="p-2.5 text-rose-400">625.5p</td>
                                    <td class="p-2.5">639.4p</td>
                                    <td class="p-2.5">652.3p</td>
                                </tr>
                                <tr>
                                    <td class="p-2.5 text-left font-semibold text-neutral-400">10.00% WACC</td>
                                    <td class="p-2.5">541.2p</td>
                                    <td class="p-2.5">555.6p</td>
                                    <td class="p-2.5 text-rose-400">569.0p</td>
                                    <td class="p-2.5">581.3p</td>
                                    <td class="p-2.5">592.6p</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- ========================================================================================= -->
        <!-- TAB 5: FORENSIC HEALTH & TECHNICAL PROFILE -->
        <!-- ========================================================================================= -->
        <div id="tab-diagnostics" class="tab-content space-y-6 hidden">
            <!-- Health Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- DuPont Card -->
                <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                    <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                        DuPont 5-Point ROE Deconstruction
                    </h3>
                    <div class="space-y-2 text-xs font-mono">
                        <div class="flex justify-between py-1.5 border-b border-neutral-800">
                            <span class="text-neutral-400">Tax Burden (Net Income / EBT):</span>
                            <span class="text-neutral-100 font-bold">0.8151 (18.5% effective tax)</span>
                        </div>
                        <div class="flex justify-between py-1.5 border-b border-neutral-800">
                            <span class="text-neutral-400">Interest Burden (EBT / EBIT):</span>
                            <span class="text-neutral-100 font-bold">0.9315 (Minimal debt drag)</span>
                        </div>
                        <div class="flex justify-between py-1.5 border-b border-neutral-800">
                            <span class="text-neutral-400">Operating Margin (EBIT / Revenue):</span>
                            <span class="text-emerald-400 font-bold">20.80% (+1,050 bps turnaround)</span>
                        </div>
                        <div class="flex justify-between py-1.5 border-b border-neutral-800">
                            <span class="text-neutral-400">Asset Turnover (Revenue / Assets):</span>
                            <span class="text-neutral-100 font-bold">0.556x (High service velocity)</span>
                        </div>
                        <div class="flex justify-between py-1.5 border-b border-neutral-800">
                            <span class="text-neutral-400">Equity Multiplier (Assets / Equity):</span>
                            <span class="text-neutral-100 font-bold">13.98x (Rapid equity buildup)</span>
                        </div>
                        <div class="flex justify-between py-2 border-t border-neutral-700 text-amber-400 font-bold">
                            <span>Calculated Return on Equity (ROE):</span>
                            <span>123.1% (Reflects small post-restructure equity base)</span>
                        </div>
                    </div>
                </div>

                <!-- Altman Z & Financial Scores Card -->
                <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                    <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                        Institutional Solvency & Forensic Audit
                    </h3>
                    <div class="space-y-3">
                        <div class="p-3 bg-neutral-900 border border-neutral-800 flex items-center justify-between">
                            <div>
                                <span class="text-neutral-400 font-mono text-xs">Altman Z-Score</span>
                                <div class="text-lg font-bold font-mono text-emerald-400">3.19 (SAFE ZONE)</div>
                            </div>
                            <span class="px-2 py-1 bg-emerald-950/40 border border-emerald-800 text-emerald-300 text-[10px] font-bold">Z > 2.99 PASS</span>
                        </div>
                        <div class="p-3 bg-neutral-900 border border-neutral-800 flex items-center justify-between">
                            <div>
                                <span class="text-neutral-400 font-mono text-xs">Piotroski F-Score</span>
                                <div class="text-lg font-bold font-mono text-emerald-400">8 / 9 (VERY STRONG)</div>
                            </div>
                            <span class="px-2 py-1 bg-emerald-950/40 border border-emerald-800 text-emerald-300 text-[10px] font-bold">EXCELLENT</span>
                        </div>
                        <div class="p-3 bg-neutral-900 border border-neutral-800 flex items-center justify-between">
                            <div>
                                <span class="text-neutral-400 font-mono text-xs">Beneish M-Score</span>
                                <div class="text-lg font-bold font-mono text-neutral-200">-2.78 (NO MANIPULATION)</div>
                            </div>
                            <span class="px-2 py-1 bg-neutral-800 text-neutral-300 text-[10px] font-bold">M < -1.78 SAFE</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Technical Cross & Tactical Trade Execution Plan -->
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Technical Scope: Death Cross Setup & Tactical 3-6 Month Accumulation Plan
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Reconciling Lead PM's technical observation with institutional valuation reality</p>
                    </div>
                    <span class="px-2 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono">
                        ACTION: ACCUMULATE AT 1,285p (200-SMA)
                    </span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="p-4 bg-neutral-900/50 border border-neutral-800 space-y-2">
                        <span class="text-rose-400 font-mono font-bold text-xs">[PHASE 1: CYCLICAL PULLBACK]</span>
                        <h4 class="text-xs font-serif font-semibold text-neutral-100">50-Day MA Rolling Over Below Current Price</h4>
                        <p class="text-neutral-400 font-serif text-xs leading-relaxed">
                            Price is pressing below the 50-day SMA (1,475p). A 3-month window death cross will flush momentum momentum algorithms down toward the 100-day SMA (1,385p) and 200-day SMA (1,285p).
                        </p>
                    </div>

                    <div class="p-4 bg-neutral-900/50 border border-neutral-800 space-y-2">
                        <span class="text-amber-400 font-mono font-bold text-xs">[PHASE 2: INSTITUTIONAL FLOOR]</span>
                        <h4 class="text-xs font-serif font-semibold text-neutral-100">Rising 200-Day SMA Confluence (1,275p – 1,295p)</h4>
                        <p class="text-neutral-400 font-serif text-xs leading-relaxed">
                            At 1,285p, RR.L multiple contracts to 27.2x NTM P/E and FCF yield expands to 4.2%. Corporate share buyback bids (£7B–£9B) step in aggressively, establishing the prime entry shelf.
                        </p>
                    </div>

                    <div class="p-4 bg-neutral-900/50 border border-neutral-800 space-y-2">
                        <span class="text-emerald-400 font-mono font-bold text-xs">[PHASE 3: TARGET EXITS]</span>
                        <h4 class="text-xs font-serif font-semibold text-neutral-100">Monthly Laddered Exit Execution</h4>
                        <p class="text-neutral-400 font-serif text-xs leading-relaxed">
                            - <strong>Tranche 1 (30% Exit):</strong> 1,490p (Sell into broken 50-SMA retest, +15.9%)<br>
                            - <strong>Tranche 2 (50% Exit):</strong> 1,580p (Retest of ATH multiple ceiling, +22.9%)<br>
                            - <strong>Hard Stop:</strong> 1,180p (Weekly close breach of primary trend, -8.2%)
                        </p>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Interactive Tab Script -->
    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(function(el) {
                el.classList.add('hidden');
            });
            document.querySelectorAll('.tab-btn').forEach(function(btn) {
                btn.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                btn.classList.add('border-transparent', 'text-neutral-400');
            });
            
            const activeTab = document.getElementById(tabId);
            if (activeTab) {
                activeTab.classList.remove('hidden');
            }
            
            const activeBtn = document.getElementById('btn-' + tabId);
            if (activeBtn) {
                activeBtn.classList.add('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                activeBtn.classList.remove('border-transparent', 'text-neutral-400');
            }
        }
    </script>
</body>
</html>
"""

dashboard_path = "ERVIS/projects/UK_EQUITIES/RR/reports/dashboard.html"
with open(dashboard_path, "w") as f:
    f.write(html_content)

print("Saved interactive dashboard to:", dashboard_path)
