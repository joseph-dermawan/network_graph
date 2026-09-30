#!/usr/bin/env python3
"""
ERVIS :: Interactive Bloomberg HTML Dashboard Generator for TSM
Generates: ERVIS/projects/US_EQUITIES/TSM/reports/dashboard.html
"""

import os

dashboard_html = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERVIS :: Taiwan Semiconductor Manufacturing Co. (NYSE: TSM) Valuation Dashboard</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
    
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
            border-bottom-color: #38bdf8;
            color: #38bdf8;
            background-color: rgba(24, 24, 27, 0.8);
        }
    </style>
</head>
<body class="min-h-screen text-xs antialiased selection:bg-cyan-950 selection:text-cyan-200">

    <!-- Top Command Header -->
    <header class="border-b border-neutral-800 bg-[#0c0d0e] sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-3.5 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-center space-x-3">
                <span class="px-2 py-0.5 border border-cyan-500/40 bg-cyan-950/20 text-cyan-400 font-mono text-[11px] font-bold tracking-wider">
                    ERVIS TERMINAL v2.5
                </span>
                <span class="text-neutral-500 font-mono text-xs">/</span>
                <h1 class="text-sm font-serif font-semibold text-neutral-100 tracking-wide">
                    Taiwan Semiconductor Manufacturing Company (NYSE: TSM) :: Institutional Valuation Dossier
                </h1>
                <span class="px-2 py-0.5 border border-cyan-900/60 bg-cyan-950/30 text-cyan-300 font-mono text-[10px] font-bold">
                    [AI TITANS CAMPAIGN #02]
                </span>
            </div>
            
            <div class="flex items-center space-x-4 text-xs font-mono">
                <span class="text-neutral-400">SPOT: <strong class="text-neutral-100 font-bold">$440.13</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">INTRINSIC: <strong class="text-cyan-400 font-bold">$290.23</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="px-2 py-0.5 border border-rose-800 bg-rose-950/40 text-rose-400 font-bold">
                    TRIM / TAKE PROFITS (-34.1%)
                </span>
            </div>
        </div>

        <!-- Terminal Command Navigation Bar -->
        <div class="max-w-7xl mx-auto px-6 border-t border-neutral-800 flex space-x-1 overflow-x-auto text-xs font-mono">
            <button id="btn-tab-overview" onclick="switchTab('tab-overview')" class="tab-btn px-3.5 py-2 border-b-2 border-cyan-500 text-cyan-400 bg-neutral-900/60 transition-colors whitespace-nowrap active">
                [01] EXECUTIVE THESIS & PHYSICAL CHOKE POINT
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
                [05] AI CAPEX AUDIT & HEALTH
            </button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-6 py-8">

        <!-- TAB 1: EXECUTIVE THESIS -->
        <div id="tab-overview" class="tab-content space-y-6">
            <div class="p-3 bg-cyan-950/20 border border-cyan-900/60 text-cyan-300 flex items-center justify-between text-xs">
                <span>[VALUATION VERDICT] TSMC is the indispensable physical bedrock of the generative AI compute stack (>90% share of sub-3nm silicon & 100% of CoWoS packaging), but at $2.28 Trillion ($440.13/ADR), current market valuation prices in permanent 25%+ revenue compounding and zero geopolitical friction. Institutional DCF intrinsic value is $264.86; SOTP relative value is $360.38. Triangulated Target Price: $290.23 (-34.1% downside).</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-cyan-800 px-1.5 py-0.5">Tactical Alert</span>
            </div>

            <!-- Top KPI Quad Grid -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="p-4 border border-neutral-800 bg-[#0e1013]">
                    <div class="text-neutral-500 font-mono text-[10px] uppercase">Market Cap / Spot ADR</div>
                    <div class="text-lg font-bold font-mono text-neutral-100 mt-1">$2,282.7B / $440.13</div>
                    <div class="text-[11px] text-neutral-400 mt-1">Shares: 5,186.5M ADRs (5:1 TW)</div>
                </div>
                <div class="p-4 border border-neutral-800 bg-[#0e1013]">
                    <div class="text-neutral-500 font-mono text-[10px] uppercase">Damodaran DCF Intrinsic</div>
                    <div class="text-lg font-bold font-mono text-cyan-400 mt-1">$264.86</div>
                    <div class="text-[11px] text-neutral-400 mt-1">Base WACC: 9.79% | Term WACC: 9.50%</div>
                </div>
                <div class="p-4 border border-neutral-800 bg-[#0e1013]">
                    <div class="text-neutral-500 font-mono text-[10px] uppercase">SOTP Divisional Relative</div>
                    <div class="text-lg font-bold font-mono text-neutral-100 mt-1">$360.38</div>
                    <div class="text-[11px] text-neutral-400 mt-1">Adv Nodes 24x | FinFET 18x | Mature 11x</div>
                </div>
                <div class="p-4 border border-neutral-800 bg-[#0e1013]">
                    <div class="text-neutral-500 font-mono text-[10px] uppercase">Triangulated Target / Rating</div>
                    <div class="text-lg font-bold font-mono text-rose-400 mt-1">$290.23 (-34.1%)</div>
                    <div class="text-[11px] text-rose-500 mt-1">TRIM / TAKE PROFITS</div>
                </div>
            </div>

            <!-- Strategic Thesis & Choke Point Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 border border-neutral-800 bg-[#0e1013] p-5 space-y-4">
                    <h3 class="font-serif text-sm font-semibold text-neutral-100 border-b border-neutral-800 pb-2">
                        Institutional Variant Perception: The Monopolist's Capital Trap
                    </h3>
                    <div class="space-y-3 text-neutral-300 leading-relaxed font-sans text-xs">
                        <p>
                            <strong>1. Absolute Physical Monopolization:</strong> TSMC manufactures virtually 100% of the world's merchant and custom AI training accelerators (NVIDIA Blackwell/Hopper, AMD MI300/325X, Google TPU v5/v6, AWS Trainium 2, Meta MTIA). Its proprietary <em>CoWoS</em> (Chip-on-Wafer-on-Substrate) packaging is the sole commercial medium capable of bridging High-Bandwidth Memory (HBM3e) to leading-edge compute dies.
                        </p>
                        <p>
                            <strong>2. Fab Capital Intensity ($40B+/year):</strong> Unlike fabless clients (NVIDIA capex intensity is 2.8%), TSMC must deploy $38B to $42B in annual physical CapEx to build cleanrooms and acquire ASML High-NA EUV lithography systems. Sales-to-Capital is tightly anchored at ~1.20x, requiring constant multi-billion reinvestment that limits FCF conversion to ~43.6%.
                        </p>
                        <p>
                            <strong>3. Overseas Fab Dilution & Geopolitical Discount:</strong> Expanding into Fab 21 (Arizona), Fab 23 (Kumamoto), and Dresden introduces a 30-50% operational cost penalty relative to western Taiwan GigaFabs. Concurrently, integrating a 65 bps Taiwan Country Risk Premium (CRP) results in a cost of equity of 9.88% and base WACC of 9.79%.
                        </p>
                    </div>
                </div>

                <div class="border border-neutral-800 bg-[#0e1013] p-5 space-y-4">
                    <h3 class="font-serif text-sm font-semibold text-neutral-100 border-b border-neutral-800 pb-2">
                        Balance Sheet Fortress & Health
                    </h3>
                    <div class="space-y-2.5 font-mono text-xs">
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Cash & ST Investments:</span>
                            <span class="text-neutral-100 font-bold">$113,430.0M</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Total Adjusted Debt:</span>
                            <span class="text-neutral-100 font-bold">$34,630.0M</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">True Net Cash Cushion:</span>
                            <span class="text-cyan-400 font-bold">+$78,800.0M</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Altman Z-Score:</span>
                            <span class="text-emerald-400 font-bold">16.95 (Safe Zone)</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Piotroski F-Score:</span>
                            <span class="text-neutral-100 font-bold">8 / 9</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Beneish M-Score:</span>
                            <span class="text-neutral-100 font-bold">-2.92 (Safe)</span>
                        </div>
                        <div class="flex justify-between py-1">
                            <span class="text-neutral-400">Synthetic Credit:</span>
                            <span class="text-neutral-100 font-bold">Aa3 / AA-</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: SOTP -->
        <div id="tab-sotp" class="tab-content hidden space-y-6">
            <div class="border border-neutral-800 bg-[#0e1013] p-5">
                <div class="flex justify-between items-center mb-4 border-b border-neutral-800 pb-3">
                    <div>
                        <h3 class="font-serif text-sm font-semibold text-neutral-100">Sum-of-the-Parts (SOTP) Divisional Multiples Valuation</h3>
                        <p class="text-neutral-500 font-mono text-[11px] mt-0.5">Segregated by Process Node Capability and Market Power</p>
                    </div>
                    <span class="px-2 py-0.5 border border-cyan-800 bg-cyan-950/40 text-cyan-300 font-mono font-bold text-xs">
                        IMPLIED SOTP: $360.38 / ADR
                    </span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono border-collapse">
                        <thead>
                            <tr class="border-b border-neutral-800 text-neutral-400 bg-neutral-900/40 text-[11px]">
                                <th class="py-2.5 px-3">Process Node Segment</th>
                                <th class="py-2.5 px-3">2026E Revenue ($M)</th>
                                <th class="py-2.5 px-3">EBITDA Margin</th>
                                <th class="py-2.5 px-3">2026E EBITDA ($M)</th>
                                <th class="py-2.5 px-3">Target EV/EBITDA</th>
                                <th class="py-2.5 px-3 text-right">Implied EV ($M)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-xs">
                            <tr>
                                <td class="py-3 px-3 font-medium text-neutral-100">Advanced HPC (&le;3nm & 2nm)</td>
                                <td class="py-3 px-3">$58,000.0</td>
                                <td class="py-3 px-3">65.0%</td>
                                <td class="py-3 px-3">$37,700.0</td>
                                <td class="py-3 px-3 font-bold text-cyan-400">24.0x</td>
                                <td class="py-3 px-3 text-right font-bold text-neutral-100">$904,800.0</td>
                            </tr>
                            <tr>
                                <td class="py-3 px-3 font-medium text-neutral-100">FinFET Advanced (5nm / 7nm)</td>
                                <td class="py-3 px-3">$62,000.0</td>
                                <td class="py-3 px-3">62.0%</td>
                                <td class="py-3 px-3">$38,440.0</td>
                                <td class="py-3 px-3 font-bold text-cyan-400">18.0x</td>
                                <td class="py-3 px-3 text-right font-bold text-neutral-100">$691,920.0</td>
                            </tr>
                            <tr>
                                <td class="py-3 px-3 font-medium text-neutral-100">Mature & Specialty (16nm, 28nm+)</td>
                                <td class="py-3 px-3">$32,000.0</td>
                                <td class="py-3 px-3">55.0%</td>
                                <td class="py-3 px-3">$17,600.0</td>
                                <td class="py-3 px-3 font-bold text-cyan-400">11.0x</td>
                                <td class="py-3 px-3 text-right font-bold text-neutral-100">$193,600.0</td>
                            </tr>
                            <tr class="bg-neutral-900/60 font-bold">
                                <td class="py-3 px-3 text-cyan-300">Total Operating Enterprise Value</td>
                                <td class="py-3 px-3">$152,000.0</td>
                                <td class="py-3 px-3">61.7%</td>
                                <td class="py-3 px-3">$93,740.0</td>
                                <td class="py-3 px-3 text-neutral-300">19.1x (Blended)</td>
                                <td class="py-3 px-3 text-right text-cyan-300">$1,790,320.0</td>
                            </tr>
                            <tr>
                                <td colspan="5" class="py-2.5 px-3 text-neutral-400">(+) True Net Cash Fortress (Cash $113.4B minus Debt $34.6B)</td>
                                <td class="py-2.5 px-3 text-right text-emerald-400 font-bold">+$78,800.0</td>
                            </tr>
                            <tr class="bg-neutral-950 font-bold border-t-2 border-neutral-700">
                                <td colspan="5" class="py-3 px-3 text-neutral-100 text-sm">Implied SOTP Total Equity Value</td>
                                <td class="py-3 px-3 text-right text-neutral-100 text-sm">$1,869,120.0</td>
                            </tr>
                            <tr class="bg-cyan-950/20 font-bold border-t border-cyan-800">
                                <td colspan="5" class="py-3 px-3 text-cyan-300 text-sm">Implied SOTP Value per Share (ADR USD)</td>
                                <td class="py-3 px-3 text-right text-cyan-400 text-base">$360.38</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: DCF -->
        <div id="tab-dcf" class="tab-content hidden space-y-6">
            <div class="border border-neutral-800 bg-[#0e1013] p-5">
                <div class="flex justify-between items-center mb-4 border-b border-neutral-800 pb-3">
                    <div>
                        <h3 class="font-serif text-sm font-semibold text-neutral-100">10-Year Discrete Ginzu DCF Schedule ($M USD)</h3>
                        <p class="text-neutral-500 font-mono text-[11px] mt-0.5">Damodaran Framework | Sales-to-Capital = 1.20 | Terminal ROIC = 22.0%</p>
                    </div>
                    <span class="px-2 py-0.5 border border-cyan-800 bg-cyan-950/40 text-cyan-300 font-mono font-bold text-xs">
                        DCF INTRINSIC VALUE: $264.86 / ADR
                    </span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono border-collapse text-[11px]">
                        <thead>
                            <tr class="border-b border-neutral-800 text-neutral-400 bg-neutral-900/40">
                                <th class="py-2 px-2.5">Line Item ($M)</th>
                                <th class="py-2 px-2.5">FY25A</th>
                                <th class="py-2 px-2.5">FY26E</th>
                                <th class="py-2 px-2.5">FY27E</th>
                                <th class="py-2 px-2.5">FY28E</th>
                                <th class="py-2 px-2.5">FY29E</th>
                                <th class="py-2 px-2.5">FY30E</th>
                                <th class="py-2 px-2.5">FY31E</th>
                                <th class="py-2 px-2.5">FY32E</th>
                                <th class="py-2 px-2.5">FY33E</th>
                                <th class="py-2 px-2.5">FY34E</th>
                                <th class="py-2 px-2.5">FY35E</th>
                                <th class="py-2 px-2.5">Terminal</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-xs">
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-300 font-medium">Revenue</td>
                                <td class="py-2 px-2.5">$119,800</td>
                                <td class="py-2 px-2.5">$148,552</td>
                                <td class="py-2 px-2.5">$178,262</td>
                                <td class="py-2 px-2.5">$206,784</td>
                                <td class="py-2 px-2.5">$231,598</td>
                                <td class="py-2 px-2.5">$252,442</td>
                                <td class="py-2 px-2.5">$271,376</td>
                                <td class="py-2 px-2.5">$287,658</td>
                                <td class="py-2 px-2.5">$302,041</td>
                                <td class="py-2 px-2.5">$314,727</td>
                                <td class="py-2 px-2.5">$326,686</td>
                                <td class="py-2 px-2.5 text-cyan-300">$339,101</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-400">Growth %</td>
                                <td class="py-2 px-2.5">-</td>
                                <td class="py-2 px-2.5 text-emerald-400">24.0%</td>
                                <td class="py-2 px-2.5 text-emerald-400">20.0%</td>
                                <td class="py-2 px-2.5 text-emerald-400">16.0%</td>
                                <td class="py-2 px-2.5">12.0%</td>
                                <td class="py-2 px-2.5">9.0%</td>
                                <td class="py-2 px-2.5">7.5%</td>
                                <td class="py-2 px-2.5">6.0%</td>
                                <td class="py-2 px-2.5">5.0%</td>
                                <td class="py-2 px-2.5">4.2%</td>
                                <td class="py-2 px-2.5">3.8%</td>
                                <td class="py-2 px-2.5 text-neutral-400">3.8%</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-400">EBIT Margin</td>
                                <td class="py-2 px-2.5">50.8%</td>
                                <td class="py-2 px-2.5">52.0%</td>
                                <td class="py-2 px-2.5">52.5%</td>
                                <td class="py-2 px-2.5">52.0%</td>
                                <td class="py-2 px-2.5">51.0%</td>
                                <td class="py-2 px-2.5">50.0%</td>
                                <td class="py-2 px-2.5">49.5%</td>
                                <td class="py-2 px-2.5">49.0%</td>
                                <td class="py-2 px-2.5">48.5%</td>
                                <td class="py-2 px-2.5">48.0%</td>
                                <td class="py-2 px-2.5">48.0%</td>
                                <td class="py-2 px-2.5">48.0%</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-300 font-medium">NOPAT (at 16%)</td>
                                <td class="py-2 px-2.5">$51,140</td>
                                <td class="py-2 px-2.5">$64,888</td>
                                <td class="py-2 px-2.5">$78,614</td>
                                <td class="py-2 px-2.5">$90,323</td>
                                <td class="py-2 px-2.5">$99,217</td>
                                <td class="py-2 px-2.5">$106,026</td>
                                <td class="py-2 px-2.5">$112,839</td>
                                <td class="py-2 px-2.5">$118,402</td>
                                <td class="py-2 px-2.5">$123,052</td>
                                <td class="py-2 px-2.5">$126,901</td>
                                <td class="py-2 px-2.5">$131,720</td>
                                <td class="py-2 px-2.5 text-cyan-300">$136,725</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-400">Reinvestment</td>
                                <td class="py-2 px-2.5">-</td>
                                <td class="py-2 px-2.5">$23,960</td>
                                <td class="py-2 px-2.5">$24,758</td>
                                <td class="py-2 px-2.5">$23,768</td>
                                <td class="py-2 px-2.5">$20,678</td>
                                <td class="py-2 px-2.5">$17,370</td>
                                <td class="py-2 px-2.5">$15,778</td>
                                <td class="py-2 px-2.5">$13,568</td>
                                <td class="py-2 px-2.5">$11,986</td>
                                <td class="py-2 px-2.5">$10,572</td>
                                <td class="py-2 px-2.5">$9,966</td>
                                <td class="py-2 px-2.5 text-rose-400">$23,612</td>
                            </tr>
                            <tr class="bg-neutral-900/40 font-bold">
                                <td class="py-2 px-2.5 text-neutral-100">FCFF</td>
                                <td class="py-2 px-2.5">$31,210</td>
                                <td class="py-2 px-2.5 text-emerald-400">$40,928</td>
                                <td class="py-2 px-2.5 text-emerald-400">$53,856</td>
                                <td class="py-2 px-2.5 text-emerald-400">$66,555</td>
                                <td class="py-2 px-2.5 text-emerald-400">$78,539</td>
                                <td class="py-2 px-2.5 text-emerald-400">$88,656</td>
                                <td class="py-2 px-2.5 text-emerald-400">$97,061</td>
                                <td class="py-2 px-2.5 text-emerald-400">$104,834</td>
                                <td class="py-2 px-2.5 text-emerald-400">$111,066</td>
                                <td class="py-2 px-2.5 text-emerald-400">$116,329</td>
                                <td class="py-2 px-2.5 text-emerald-400">$121,754</td>
                                <td class="py-2 px-2.5 text-cyan-300">$113,113</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-400">WACC %</td>
                                <td class="py-2 px-2.5">-</td>
                                <td class="py-2 px-2.5">9.79%</td>
                                <td class="py-2 px-2.5">9.76%</td>
                                <td class="py-2 px-2.5">9.73%</td>
                                <td class="py-2 px-2.5">9.70%</td>
                                <td class="py-2 px-2.5">9.66%</td>
                                <td class="py-2 px-2.5">9.63%</td>
                                <td class="py-2 px-2.5">9.60%</td>
                                <td class="py-2 px-2.5">9.57%</td>
                                <td class="py-2 px-2.5">9.53%</td>
                                <td class="py-2 px-2.5">9.50%</td>
                                <td class="py-2 px-2.5 text-neutral-400">9.50%</td>
                            </tr>
                            <tr class="bg-cyan-950/20 font-bold">
                                <td class="py-2 px-2.5 text-cyan-300">PV of FCFF</td>
                                <td class="py-2 px-2.5">-</td>
                                <td class="py-2 px-2.5">$37,277</td>
                                <td class="py-2 px-2.5">$44,699</td>
                                <td class="py-2 px-2.5">$50,332</td>
                                <td class="py-2 px-2.5">$54,166</td>
                                <td class="py-2 px-2.5">$55,758</td>
                                <td class="py-2 px-2.5">$55,679</td>
                                <td class="py-2 px-2.5">$54,845</td>
                                <td class="py-2 px-2.5">$53,006</td>
                                <td class="py-2 px-2.5">$50,683</td>
                                <td class="py-2 px-2.5">$48,432</td>
                                <td class="py-2 px-2.5 text-cyan-400">PV(TV): $770,016</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-neutral-800">
                    <div class="p-3 bg-neutral-900/60 border border-neutral-800">
                        <span class="text-neutral-500 text-[10px] block">CUMULATIVE PV (10-YR FCFF)</span>
                        <span class="text-base font-bold text-neutral-100">$504,877M (39.6%)</span>
                    </div>
                    <div class="p-3 bg-neutral-900/60 border border-neutral-800">
                        <span class="text-neutral-500 text-[10px] block">PV OF TERMINAL VALUE</span>
                        <span class="text-base font-bold text-neutral-100">$770,016M (60.4%)</span>
                    </div>
                    <div class="p-3 bg-cyan-950/30 border border-cyan-900/60">
                        <span class="text-cyan-400 text-[10px] block">ENTERPRISE VALUE + NET CASH</span>
                        <span class="text-base font-bold text-cyan-300">$1,373,693M -> $264.86/sh</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: SCENARIOS & MONTE CARLO -->
        <div id="tab-scenarios" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Monte Carlo Distribution -->
                <div class="border border-neutral-800 bg-[#0e1013] p-5 space-y-4">
                    <h3 class="font-serif text-sm font-semibold text-neutral-100 border-b border-neutral-800 pb-2">
                        Monte Carlo Simulation (10,000 Iterations)
                    </h3>
                    <div class="space-y-3 font-mono text-xs">
                        <div class="flex justify-between py-1.5 border-b border-neutral-800/60">
                            <span class="text-neutral-400">10th Percentile (Bear Floor):</span>
                            <span class="text-neutral-100 font-bold">$191.90</span>
                        </div>
                        <div class="flex justify-between py-1.5 border-b border-neutral-800/60">
                            <span class="text-neutral-400">50th Percentile (Stochastic Median):</span>
                            <span class="text-cyan-400 font-bold">$231.98</span>
                        </div>
                        <div class="flex justify-between py-1.5 border-b border-neutral-800/60">
                            <span class="text-neutral-400">90th Percentile (Bull Sky):</span>
                            <span class="text-neutral-100 font-bold">$280.72</span>
                        </div>
                        <div class="flex justify-between py-1.5 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Win Rate (% Trials &gt; $440.13 Spot):</span>
                            <span class="text-rose-400 font-bold">0.0% (Extreme Overvaluation)</span>
                        </div>
                    </div>
                    <div class="p-3 bg-neutral-900/40 border border-neutral-800 text-[11px] text-neutral-400 leading-relaxed font-sans">
                        Zero out of 10,000 stochastic trials supported the current market spot price of $440.13. Even under aggressive 18% revenue compounding and 54% sustained operating margins, the 90th percentile tops out at $280.72.
                    </div>
                </div>

                <!-- Downside Liquidation Floor -->
                <div class="border border-neutral-800 bg-[#0e1013] p-5 space-y-4">
                    <h3 class="font-serif text-sm font-semibold text-neutral-100 border-b border-neutral-800 pb-2">
                        Downside Liquidation Haircut Floor
                    </h3>
                    <div class="space-y-2 font-mono text-xs">
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Cash & ST Inv (100%):</span>
                            <span class="text-neutral-100">$113,430M</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Receivables (75% Haircut):</span>
                            <span class="text-neutral-100">$10,275M</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Inventories (50% Haircut):</span>
                            <span class="text-neutral-100">$6,100M</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Net PP&E & Fabs (30% Haircut):</span>
                            <span class="text-neutral-100">$35,337M</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Total Recoverable Assets:</span>
                            <span class="text-neutral-100 font-bold">$166,115M</span>
                        </div>
                        <div class="flex justify-between py-1 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Less: Total Liabilities:</span>
                            <span class="text-rose-400">-$92,800M</span>
                        </div>
                        <div class="flex justify-between py-1.5 bg-neutral-900/60 px-2 font-bold">
                            <span class="text-neutral-200">Liquidation Net Equity Floor:</span>
                            <span class="text-cyan-400">$73,315M ($14.16 / ADR)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: AI CAPEX & HEALTH -->
        <div id="tab-diagnostics" class="tab-content hidden space-y-6">
            <div class="border border-neutral-800 bg-[#0e1013] p-5 space-y-4">
                <div class="flex justify-between items-center border-b border-neutral-800 pb-3">
                    <div>
                        <h3 class="font-serif text-sm font-semibold text-neutral-100">Gate 4B: AI CapEx Payout, Tool Depreciation & Customer Sensitivity</h3>
                        <p class="text-neutral-500 font-mono text-[11px] mt-0.5">Stress Testing Fab Utilization & Operating Leverage under Hyperscaler Pauses</p>
                    </div>
                    <span class="px-2 py-0.5 border border-cyan-800 bg-cyan-950/40 text-cyan-300 font-mono font-bold text-xs">
                        FAB ECONOMIC ROIC: 36.9%
                    </span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono border-collapse text-xs">
                        <thead>
                            <tr class="border-b border-neutral-800 text-neutral-400 bg-neutral-900/40 text-[11px]">
                                <th class="py-2.5 px-3">Hyperscaler Demand Scenario</th>
                                <th class="py-2.5 px-3">Combined CapEx ($B)</th>
                                <th class="py-2.5 px-3">TSMC Leading Fab Util %</th>
                                <th class="py-2.5 px-3">Blended Gross Margin %</th>
                                <th class="py-2.5 px-3">Implied 2026E EPS ($/ADR)</th>
                                <th class="py-2.5 px-3">Operational Impact & Earnings Drag</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60">
                            <tr>
                                <td class="py-3 px-3 font-medium text-emerald-400">Base Case (Unchanged)</td>
                                <td class="py-3 px-3">$408.0B</td>
                                <td class="py-3 px-3">100.0%</td>
                                <td class="py-3 px-3 font-bold text-neutral-100">59.8%</td>
                                <td class="py-3 px-3 font-bold text-neutral-100">$13.39</td>
                                <td class="py-3 px-3 text-neutral-400">Baseline full allocation across N3 and CoWoS lines</td>
                            </tr>
                            <tr>
                                <td class="py-3 px-3 font-medium text-amber-400">Mild Digestion (-10% CapEx)</td>
                                <td class="py-3 px-3">$367.2B</td>
                                <td class="py-3 px-3">92.0%</td>
                                <td class="py-3 px-3 font-bold text-neutral-100">56.5%</td>
                                <td class="py-3 px-3 font-bold text-neutral-100">$11.95</td>
                                <td class="py-3 px-3 text-amber-300">-10.8% EPS drag; CoWoS remains 100% booked; minor 5nm slack</td>
                            </tr>
                            <tr>
                                <td class="py-3 px-3 font-medium text-rose-400">Severe Pause (-20% CapEx)</td>
                                <td class="py-3 px-3">$326.4B</td>
                                <td class="py-3 px-3">84.0%</td>
                                <td class="py-3 px-3 font-bold text-neutral-100">52.8%</td>
                                <td class="py-3 px-3 font-bold text-neutral-100">$10.15</td>
                                <td class="py-3 px-3 text-rose-400">-24.2% EPS drag; fixed tool depreciation ($8.1B/yr) burdens margins</td>
                            </tr>
                            <tr>
                                <td class="py-3 px-3 font-medium text-rose-600">Cyclical Winter (-30% CapEx)</td>
                                <td class="py-3 px-3">$285.6B</td>
                                <td class="py-3 px-3">76.0%</td>
                                <td class="py-3 px-3 font-bold text-neutral-100">48.2%</td>
                                <td class="py-3 px-3 font-bold text-neutral-100">$8.20</td>
                                <td class="py-3 px-3 text-rose-500">-38.8% EPS drag; gross margin drops below 50% strategic floor</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-neutral-800">
                    <div class="p-3 bg-neutral-900/60 border border-neutral-800">
                        <span class="text-neutral-500 font-mono text-[10px] block">TSMC HARDWARE CPR ("FOUNDRY TAX")</span>
                        <p class="text-neutral-300 font-sans text-xs mt-1">
                            Of the $408B in annual hyperscaler CapEx, TSMC directly captures <strong>$26.5B (~6.50%)</strong> in pure silicon and packaging revenues. While NVIDIA captures ~42% of customer hardware budgets, TSMC's lower CPR provides greater downside defensibility.
                        </p>
                    </div>
                    <div class="p-3 bg-neutral-900/60 border border-neutral-800">
                        <span class="text-neutral-500 font-mono text-[10px] block">5-YEAR DEPRECIATION HEADWIND</span>
                        <p class="text-neutral-300 font-sans text-xs mt-1">
                            Each vintage of ASML High-NA and standard EUV steppers creates an annual straight-line depreciation charge of <strong>$8.07 Billion</strong>. In a volume downturn, this fixed cost cannot be furloughed, creating rapid operating margin decay.
                        </p>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer Terminal Info -->
    <footer class="border-t border-neutral-800 py-6 text-neutral-500 font-mono text-center text-[11px] bg-[#0c0d0e]">
        ERVIS DUAL-ENGINE INSTITUTIONAL VALUATION TERMINAL &bull; TAIWAN SEMICONDUCTOR MANUFACTURING CO. (TSM) &bull; GATE 1-5 AUDITED
    </footer>

    <!-- Interactive Tabs Script -->
    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(function(el) {
                el.classList.add('hidden');
            });
            document.querySelectorAll('.tab-btn').forEach(function(el) {
                el.classList.remove('active', 'border-cyan-500', 'text-cyan-400');
                el.classList.add('border-transparent', 'text-neutral-400');
            });
            
            var activeTab = document.getElementById(tabId);
            if (activeTab) {
                activeTab.classList.remove('hidden');
            }
            
            var activeBtn = document.getElementById('btn-' + tabId);
            if (activeBtn) {
                activeBtn.classList.add('active', 'border-cyan-500', 'text-cyan-400');
                activeBtn.classList.remove('border-transparent', 'text-neutral-400');
            }
        }
    </script>
</body>
</html>
"""

report_path = "ERVIS/projects/US_EQUITIES/TSM/reports/dashboard.html"
with open(report_path, "w") as f:
    f.write(dashboard_html)

print(f"[SUCCESS] Interactive Bloomberg HTML Dashboard saved at: {report_path}")
