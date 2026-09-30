import os

dashboard_html = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERVIS :: Microsoft Corporation (NASDAQ: MSFT) Valuation Dashboard</title>
    
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
                    Microsoft Corporation (NASDAQ: MSFT) :: Institutional Valuation Dossier
                </h1>
                <span class="px-2 py-0.5 border border-cyan-900/60 bg-cyan-950/30 text-cyan-300 font-mono text-[10px] font-bold">
                    [AI TITANS CAMPAIGN #02]
                </span>
            </div>
            
            <div class="flex items-center space-x-4 text-xs font-mono">
                <span class="text-neutral-400">SPOT: <strong class="text-neutral-100 font-bold">$493.89</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">INTRINSIC: <strong class="text-amber-400 font-bold">$447.71</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="px-2 py-0.5 border border-amber-800 bg-amber-950/40 text-amber-400 font-bold">
                    HOLD / ACCUMULATE ON PULLBACK (-9.4%)
                </span>
            </div>
        </div>

        <!-- Terminal Command Navigation Bar -->
        <div class="max-w-7xl mx-auto px-6 border-t border-neutral-800 flex space-x-1 overflow-x-auto text-xs font-mono">
            <button id="btn-tab-overview" onclick="switchTab('tab-overview')" class="tab-btn px-3.5 py-2 border-b-2 border-amber-500 text-amber-400 bg-neutral-900/60 transition-colors whitespace-nowrap">
                [01] EXECUTIVE THESIS & CAPEX PARADOX
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
                [05] AI CAPEX AUDIT & HEALTH DIAGNOSTICS
            </button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-6 py-8">

        <!-- TAB 1: EXECUTIVE THESIS -->
        <div id="tab-overview" class="tab-content space-y-6">
            <div class="p-3 bg-amber-950/20 border border-amber-900/60 text-amber-300 flex items-center justify-between text-xs">
                <span>[VALUATION VERDICT] Microsoft represents the definitive institutional franchise with world-class enterprise software lock-in and a pristine Aaa/AAA sovereign-tier balance sheet ($2.0B net cash). However, annual CapEx has surged 312% in 3 years to $115.9B (34.9% of revenue), creating a $21.5B/yr GPU depreciation headwind against only ~$18.0B in current incremental AI monetization. Triangulated intrinsic target is $447.71 (-9.4% gap). Recommend HOLD with aggressive accumulation below $435.00.</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-amber-800 px-1.5 py-0.5">Tactical Alert</span>
            </div>

            <!-- Key Metric Cards Grid -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="p-4 bg-neutral-900/50 border border-neutral-800 rounded">
                    <div class="text-neutral-500 text-[10px] uppercase font-mono">Ginzu DCF Value</div>
                    <div class="text-xl font-bold font-mono text-neutral-100 mt-1">$434.43</div>
                    <div class="text-[11px] text-neutral-400 mt-1 font-mono">WACC: 8.80% | Term ROIC: 25.0%</div>
                </div>
                <div class="p-4 bg-neutral-900/50 border border-neutral-800 rounded">
                    <div class="text-neutral-500 text-[10px] uppercase font-mono">SOTP Divisional Value</div>
                    <div class="text-xl font-bold font-mono text-amber-400 mt-1">$505.61</div>
                    <div class="text-[11px] text-neutral-400 mt-1 font-mono">Intelligent Cloud EV: $1.97T</div>
                </div>
                <div class="p-4 bg-neutral-900/50 border border-neutral-800 rounded">
                    <div class="text-neutral-500 text-[10px] uppercase font-mono">Monte Carlo 10k Median</div>
                    <div class="text-xl font-bold font-mono text-cyan-400 mt-1">$353.64</div>
                    <div class="text-[11px] text-neutral-400 mt-1 font-mono">90% Conf: $299 - $419</div>
                </div>
                <div class="p-4 bg-neutral-900/50 border border-neutral-800 rounded">
                    <div class="text-neutral-500 text-[10px] uppercase font-mono">Target Intrinsic Price</div>
                    <div class="text-xl font-bold font-mono text-amber-300 mt-1">$447.71</div>
                    <div class="text-[11px] text-rose-400 mt-1 font-mono">-9.4% Premium vs Spot</div>
                </div>
            </div>

            <!-- Core Theses Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="p-5 bg-neutral-900/40 border border-neutral-800 rounded space-y-3">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider uppercase border-b border-neutral-800 pb-2">
                        Institutional Moat Pillars (The Bull Anchors)
                    </h3>
                    <ul class="space-y-2.5 text-neutral-300 text-xs">
                        <li class="flex items-start space-x-2">
                            <span class="text-emerald-400 font-bold">[+]</span>
                            <span><strong>Enterprise Workflow Monopoly:</strong> Over 400M paid Office 365 commercial seats and 28M+ Copilot enterprise users create unbreakable switching costs and pricing power.</span>
                        </li>
                        <li class="flex items-start space-x-2">
                            <span class="text-emerald-400 font-bold">[+]</span>
                            <span><strong>Azure Hyperscale Dominance:</strong> Intelligent Cloud generated $145.8B revenue with Azure growing >28% YoY, bolstered by OpenAI exclusive commercial compute partnerships.</span>
                        </li>
                        <li class="flex items-start space-x-2">
                            <span class="text-emerald-400 font-bold">[+]</span>
                            <span><strong>Aaa/AAA Sovereign-Tier Balance Sheet:</strong> One of only two US corporate entities with top credit ratings. Holds $76.7B in liquid reserves with net cash of $2.0B post-lease normalization.</span>
                        </li>
                    </ul>
                </div>

                <div class="p-5 bg-neutral-900/40 border border-neutral-800 rounded space-y-3">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider uppercase border-b border-neutral-800 pb-2">
                        Gate 4B: The AI CapEx Paradox & Depreciation Reality
                    </h3>
                    <ul class="space-y-2.5 text-neutral-300 text-xs">
                        <li class="flex items-start space-x-2">
                            <span class="text-rose-400 font-bold">[-]</span>
                            <span><strong>Hyper-Inflation in CapEx:</strong> Annual CapEx reached $115.9B (34.9% of rev), up from $28.1B in FY23. FCF conversion declined from 68% to 36.6%.</span>
                        </li>
                        <li class="flex items-start space-x-2">
                            <span class="text-rose-400 font-bold">[-]</span>
                            <span><strong>GPU Obsolescence Mismatch:</strong> With $75.4B in AI GPU clusters, annual depreciation over a 3.5-yr useful life is $21.5B/yr. Net AI operating profit is -$9.8B (ROI: -13.0%).</span>
                        </li>
                        <li class="flex items-start space-x-2">
                            <span class="text-amber-400 font-bold">[~]</span>
                            <span><strong>Monetization Gap:</strong> Microsoft must generate $33.1B in AI revenue just to cover GPU amortization, and $77.7B to earn a 15% ROIC, requiring significant acceleration from the current $18B run-rate.</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <!-- TAB 2: SUM-OF-THE-PARTS -->
        <div id="tab-sotp" class="tab-content hidden space-y-6">
            <div class="border border-neutral-800 bg-neutral-900/40 rounded p-4">
                <h3 class="text-sm font-semibold text-neutral-100 mb-3">Divisional Sum-of-the-Parts (SOTP) Valuation Breakdown</h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono text-xs">
                        <thead>
                            <tr class="border-b border-neutral-800 text-neutral-400">
                                <th class="py-2.5 px-3">Segment Name</th>
                                <th class="py-2.5 px-3">Key Products & Assets</th>
                                <th class="py-2.5 px-3 text-right">FY26 Rev ($M)</th>
                                <th class="py-2.5 px-3 text-right">FY26 EBITDA ($M)</th>
                                <th class="py-2.5 px-3 text-right">Target EV/EBITDA</th>
                                <th class="py-2.5 px-3 text-right">Implied EV ($M)</th>
                                <th class="py-2.5 px-3 text-right">% of Total</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60">
                            <tr>
                                <td class="py-2.5 px-3 font-bold text-neutral-200">Productivity & Business Processes</td>
                                <td class="py-2.5 px-3 text-neutral-400">Office 365 Commercial/Consumer, LinkedIn, Dynamics 365, Copilot Pro</td>
                                <td class="py-2.5 px-3 text-right">$93,400</td>
                                <td class="py-2.5 px-3 text-right">$53,200</td>
                                <td class="py-2.5 px-3 text-right text-amber-400">22.0x</td>
                                <td class="py-2.5 px-3 text-right font-bold text-neutral-100">$1,170,400</td>
                                <td class="py-2.5 px-3 text-right text-neutral-400">31.2%</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-bold text-neutral-200">Intelligent Cloud</td>
                                <td class="py-2.5 px-3 text-neutral-400">Azure Public Cloud, Azure AI, Windows Server, SQL Server, GitHub, Nuance</td>
                                <td class="py-2.5 px-3 text-right">$145,800</td>
                                <td class="py-2.5 px-3 text-right">$75,800</td>
                                <td class="py-2.5 px-3 text-right text-amber-400">26.0x</td>
                                <td class="py-2.5 px-3 text-right font-bold text-neutral-100">$1,970,800</td>
                                <td class="py-2.5 px-3 text-right text-neutral-400">52.5%</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 px-3 font-bold text-neutral-200">More Personal Computing</td>
                                <td class="py-2.5 px-3 text-neutral-400">Windows OEM & Commercial, Xbox Hardware & Game Pass, Activision Blizzard, Surface, Bing/Search Ads</td>
                                <td class="py-2.5 px-3 text-right">$92,600</td>
                                <td class="py-2.5 px-3 text-right">$38,200</td>
                                <td class="py-2.5 px-3 text-right text-amber-400">16.0x</td>
                                <td class="py-2.5 px-3 text-right font-bold text-neutral-100">$611,200</td>
                                <td class="py-2.5 px-3 text-right text-neutral-400">16.3%</td>
                            </tr>
                            <tr class="bg-neutral-800/30 font-bold">
                                <td class="py-2.5 px-3 text-neutral-100" colspan="5">Consolidated Sum-of-the-Parts Enterprise Value</td>
                                <td class="py-2.5 px-3 text-right text-amber-400">$3,752,400</td>
                                <td class="py-2.5 px-3 text-right text-neutral-100">100.0%</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-3 text-neutral-300" colspan="5">(+) Net Cash Surplus (Liquid Cash $76.7B - Total Debt $74.6B)</td>
                                <td class="py-2 px-3 text-right text-emerald-400">+$2,025</td>
                                <td></td>
                            </tr>
                            <tr class="bg-amber-950/20 font-bold border-t-2 border-amber-500/50">
                                <td class="py-3 px-3 text-amber-300" colspan="5">Implied Equity Value (SOTP) / Per Share Intrinsic Target</td>
                                <td class="py-3 px-3 text-right text-amber-300">$3,754,425M</td>
                                <td class="py-3 px-3 text-right text-amber-300 text-sm">$505.61</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: 10-YR GINZU DCF SCHEDULE -->
        <div id="tab-dcf" class="tab-content hidden space-y-6">
            <div class="border border-neutral-800 bg-neutral-900/40 rounded p-4">
                <h3 class="text-sm font-semibold text-neutral-100 mb-3">Damodaran FCFF Ginzu Dual-Engine 10-Year Discrete Schedule ($M)</h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono text-xs">
                        <thead>
                            <tr class="border-b border-neutral-800 text-neutral-400">
                                <th class="py-2 px-2.5">Line Item ($M)</th>
                                <th class="py-2 px-2 text-right">FY26 (0)</th>
                                <th class="py-2 px-2 text-right">FY27 (1)</th>
                                <th class="py-2 px-2 text-right">FY28 (2)</th>
                                <th class="py-2 px-2 text-right">FY29 (3)</th>
                                <th class="py-2 px-2 text-right">FY30 (4)</th>
                                <th class="py-2 px-2 text-right">FY31 (5)</th>
                                <th class="py-2 px-2 text-right">FY32 (6)</th>
                                <th class="py-2 px-2 text-right">FY33 (7)</th>
                                <th class="py-2 px-2 text-right">FY34 (8)</th>
                                <th class="py-2 px-2 text-right">FY35 (9)</th>
                                <th class="py-2 px-2 text-right">FY36 (10)</th>
                                <th class="py-2 px-2 text-right text-amber-400">Terminal</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/50">
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-300 font-semibold">Total Revenue</td>
                                <td class="py-2 px-2 text-right">$331,839</td>
                                <td class="py-2 px-2 text-right">$381,615</td>
                                <td class="py-2 px-2 text-right">$433,133</td>
                                <td class="py-2 px-2 text-right">$485,109</td>
                                <td class="py-2 px-2 text-right">$536,045</td>
                                <td class="py-2 px-2 text-right">$584,289</td>
                                <td class="py-2 px-2 text-right">$628,111</td>
                                <td class="py-2 px-2 text-right">$668,938</td>
                                <td class="py-2 px-2 text-right">$705,730</td>
                                <td class="py-2 px-2 text-right">$737,488</td>
                                <td class="py-2 px-2 text-right">$763,300</td>
                                <td class="py-2 px-2 text-right text-amber-400">$790,015</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-400">Revenue Growth %</td>
                                <td class="py-2 px-2 text-right">-</td>
                                <td class="py-2 px-2 text-right text-emerald-400">15.0%</td>
                                <td class="py-2 px-2 text-right text-emerald-400">13.5%</td>
                                <td class="py-2 px-2 text-right text-emerald-400">12.0%</td>
                                <td class="py-2 px-2 text-right text-emerald-400">10.5%</td>
                                <td class="py-2 px-2 text-right text-emerald-400">9.0%</td>
                                <td class="py-2 px-2 text-right">7.5%</td>
                                <td class="py-2 px-2 text-right">6.5%</td>
                                <td class="py-2 px-2 text-right">5.5%</td>
                                <td class="py-2 px-2 text-right">4.5%</td>
                                <td class="py-2 px-2 text-right">3.5%</td>
                                <td class="py-2 px-2 text-right text-amber-400">3.5%</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-400">Operating Margin %</td>
                                <td class="py-2 px-2 text-right">48.8%</td>
                                <td class="py-2 px-2 text-right">48.5%</td>
                                <td class="py-2 px-2 text-right">48.5%</td>
                                <td class="py-2 px-2 text-right">48.0%</td>
                                <td class="py-2 px-2 text-right">48.0%</td>
                                <td class="py-2 px-2 text-right">47.5%</td>
                                <td class="py-2 px-2 text-right">47.0%</td>
                                <td class="py-2 px-2 text-right">46.5%</td>
                                <td class="py-2 px-2 text-right">46.0%</td>
                                <td class="py-2 px-2 text-right">45.5%</td>
                                <td class="py-2 px-2 text-right">45.0%</td>
                                <td class="py-2 px-2 text-right text-amber-400">45.0%</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-300 font-semibold">Normalized EBIT</td>
                                <td class="py-2 px-2 text-right">$161,823</td>
                                <td class="py-2 px-2 text-right">$185,083</td>
                                <td class="py-2 px-2 text-right">$210,069</td>
                                <td class="py-2 px-2 text-right">$232,852</td>
                                <td class="py-2 px-2 text-right">$257,302</td>
                                <td class="py-2 px-2 text-right">$277,537</td>
                                <td class="py-2 px-2 text-right">$295,212</td>
                                <td class="py-2 px-2 text-right">$311,056</td>
                                <td class="py-2 px-2 text-right">$324,636</td>
                                <td class="py-2 px-2 text-right">$335,557</td>
                                <td class="py-2 px-2 text-right">$343,485</td>
                                <td class="py-2 px-2 text-right text-amber-400">$355,507</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-300 font-semibold">NOPAT (t=18.0%)</td>
                                <td class="py-2 px-2 text-right">$132,695</td>
                                <td class="py-2 px-2 text-right">$151,768</td>
                                <td class="py-2 px-2 text-right">$172,257</td>
                                <td class="py-2 px-2 text-right">$190,939</td>
                                <td class="py-2 px-2 text-right">$210,987</td>
                                <td class="py-2 px-2 text-right">$227,581</td>
                                <td class="py-2 px-2 text-right">$242,074</td>
                                <td class="py-2 px-2 text-right">$255,066</td>
                                <td class="py-2 px-2 text-right">$266,201</td>
                                <td class="py-2 px-2 text-right">$275,157</td>
                                <td class="py-2 px-2 text-right">$281,658</td>
                                <td class="py-2 px-2 text-right text-amber-400">$291,516</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-400">Reinvestment (S/C: 2.40x)</td>
                                <td class="py-2 px-2 text-right">-</td>
                                <td class="py-2 px-2 text-right">$20,740</td>
                                <td class="py-2 px-2 text-right">$21,466</td>
                                <td class="py-2 px-2 text-right">$21,657</td>
                                <td class="py-2 px-2 text-right">$21,223</td>
                                <td class="py-2 px-2 text-right">$20,102</td>
                                <td class="py-2 px-2 text-right">$18,259</td>
                                <td class="py-2 px-2 text-right">$17,011</td>
                                <td class="py-2 px-2 text-right">$15,330</td>
                                <td class="py-2 px-2 text-right">$13,232</td>
                                <td class="py-2 px-2 text-right">$10,755</td>
                                <td class="py-2 px-2 text-right text-amber-400">$40,812</td>
                            </tr>
                            <tr class="bg-neutral-800/20 font-bold">
                                <td class="py-2 px-2.5 text-neutral-100">Free Cash Flow (FCFF)</td>
                                <td class="py-2 px-2 text-right text-neutral-400">$66,987</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$131,028</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$150,791</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$169,282</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$189,764</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$207,479</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$223,815</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$238,055</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$250,871</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$261,924</td>
                                <td class="py-2 px-2 text-right text-emerald-400">$270,903</td>
                                <td class="py-2 px-2 text-right text-amber-400">$250,704</td>
                            </tr>
                            <tr>
                                <td class="py-2 px-2.5 text-neutral-400">Discount Factor (WACC)</td>
                                <td class="py-2 px-2 text-right">1.000</td>
                                <td class="py-2 px-2 text-right">0.919</td>
                                <td class="py-2 px-2 text-right">0.845</td>
                                <td class="py-2 px-2 text-right">0.776</td>
                                <td class="py-2 px-2 text-right">0.713</td>
                                <td class="py-2 px-2 text-right">0.655</td>
                                <td class="py-2 px-2 text-right">0.601</td>
                                <td class="py-2 px-2 text-right">0.552</td>
                                <td class="py-2 px-2 text-right">0.507</td>
                                <td class="py-2 px-2 text-right">0.465</td>
                                <td class="py-2 px-2 text-right">0.427</td>
                                <td class="py-2 px-2 text-right text-amber-400">0.427</td>
                            </tr>
                            <tr class="bg-amber-950/10 font-semibold">
                                <td class="py-2 px-2.5 text-amber-300">Present Value (PV of FCFF)</td>
                                <td class="py-2 px-2 text-right">-</td>
                                <td class="py-2 px-2 text-right">$120,432</td>
                                <td class="py-2 px-2 text-right">$127,358</td>
                                <td class="py-2 px-2 text-right">$131,452</td>
                                <td class="py-2 px-2 text-right">$135,321</td>
                                <td class="py-2 px-2 text-right">$135,849</td>
                                <td class="py-2 px-2 text-right">$134,570</td>
                                <td class="py-2 px-2 text-right">$131,399</td>
                                <td class="py-2 px-2 text-right">$127,159</td>
                                <td class="py-2 px-2 text-right">$121,885</td>
                                <td class="py-2 px-2 text-right">$115,627</td>
                                <td class="py-2 px-2 text-right text-amber-300">$1,944,102</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="mt-4 pt-4 border-t border-neutral-800 grid grid-cols-1 md:grid-cols-4 gap-4 text-xs font-mono">
                    <div>
                        <span class="text-neutral-500">Cumulative PV 10-Yr:</span>
                        <strong class="text-neutral-200 block">$1,280,752 M</strong>
                    </div>
                    <div>
                        <span class="text-neutral-500">PV of Terminal Value:</span>
                        <strong class="text-neutral-200 block">$1,944,102 M (60.3%)</strong>
                    </div>
                    <div>
                        <span class="text-neutral-500">Total Enterprise Value:</span>
                        <strong class="text-neutral-200 block">$3,224,854 M</strong>
                    </div>
                    <div>
                        <span class="text-neutral-500">DCF Intrinsic per Share:</span>
                        <strong class="text-amber-400 block text-sm">$434.43</strong>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: SCENARIOS & 10K MONTE CARLO -->
        <div id="tab-scenarios" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="p-4 bg-neutral-900/40 border border-neutral-800 rounded space-y-2">
                    <div class="text-neutral-500 text-[10px] uppercase font-mono">Bear Case (P10)</div>
                    <div class="text-2xl font-bold font-mono text-rose-400">$298.60</div>
                    <div class="text-xs text-neutral-400">Growth slows to 6.5%, AI capex ROI drags operating margins down to 42%, terminal WACC rises to 9.5%.</div>
                </div>
                <div class="p-4 bg-neutral-900/40 border border-amber-900/50 rounded space-y-2">
                    <div class="text-neutral-500 text-[10px] uppercase font-mono">Base Case (Median)</div>
                    <div class="text-2xl font-bold font-mono text-amber-400">$353.64</div>
                    <div class="text-xs text-neutral-400">Azure grows 18-22%, Copilot achieves 20% enterprise penetration, margins normalize at 47%, WACC 9.0%.</div>
                </div>
                <div class="p-4 bg-neutral-900/40 border border-neutral-800 rounded space-y-2">
                    <div class="text-neutral-500 text-[10px] uppercase font-mono">Bull Case (P90)</div>
                    <div class="text-2xl font-bold font-mono text-emerald-400">$419.09</div>
                    <div class="text-xs text-neutral-400">Copilot ARPU expansion accelerates, AI revenues exceed $50B by FY28, margins expand to 50%+, WACC drops to 8.5%.</div>
                </div>
            </div>

            <div class="p-4 bg-neutral-900/40 border border-neutral-800 rounded">
                <h4 class="text-xs font-bold text-neutral-200 uppercase tracking-wider mb-2">
                    10,000-Trial Stochastic Simulation Parameters & Findings
                </h4>
                <p class="text-xs text-neutral-400 leading-relaxed font-mono">
                    Running 10,000 randomized draws across revenue growth (mean 9.0%, std 2.0%), operating margins (triangular distribution 42% to 52%), and cost of capital (8.0% to 10.0%) yields a median intrinsic value of <strong>$353.64</strong>. Under current market pricing of $493.89, only <strong>0.7% of trials</strong> exceed spot price, proving that market sentiment is pricing in unprecedented terminal growth and flawless AI monetization without hardware margin decay.
                </p>
            </div>
        </div>

        <!-- TAB 5: AI CAPEX AUDIT & HEALTH -->
        <div id="tab-diagnostics" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- AI CapEx Reality -->
                <div class="p-5 bg-neutral-900/40 border border-neutral-800 rounded space-y-4">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider uppercase border-b border-neutral-800 pb-2">
                        Gate 4B: AI CapEx Payout & Hardware Payback Mechanics
                    </h3>
                    
                    <div class="space-y-3 font-mono text-xs">
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Microsoft Total Annual CapEx (FY26):</span>
                            <strong class="text-neutral-100">$115.95 Billion</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">AI GPU & Accelerator Hardware Share (65%):</span>
                            <strong class="text-neutral-100">$75.37 Billion</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Incremental AI Revenue Run-Rate:</span>
                            <strong class="text-emerald-400">$18.00 Billion</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">AI Gross Profit (@ 65% software margin):</span>
                            <strong class="text-neutral-100">$11.70 Billion</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Annual GPU Depreciation (3.5-Yr Life):</span>
                            <strong class="text-rose-400">$21.53 Billion / yr</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5 bg-rose-950/20 px-2 rounded">
                            <span class="text-rose-300 font-bold">Net AI Operating Income:</span>
                            <strong class="text-rose-400 font-bold">-$9.83 Billion / yr (ROI: -13.0%)</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Cash Flow Payback Duration:</span>
                            <strong class="text-amber-400 font-bold">6.44 Years</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">GPU Useful Life (Physical/Obsolescence):</span>
                            <strong class="text-neutral-300">3.50 Years</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5 bg-amber-950/20 px-2 rounded">
                            <span class="text-amber-300 font-bold">Hardware Obsolescence Deficit:</span>
                            <strong class="text-amber-400 font-bold">+2.94 Years past obsolescence</strong>
                        </div>
                        <div class="flex justify-between py-1.5">
                            <span class="text-neutral-400">Break-Even AI Revenue Target:</span>
                            <strong class="text-cyan-400">$33.13 Billion ($15.13B gap)</strong>
                        </div>
                    </div>
                </div>

                <!-- Forensic Health & Ratios -->
                <div class="p-5 bg-neutral-900/40 border border-neutral-800 rounded space-y-4">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider uppercase border-b border-neutral-800 pb-2">
                        Forensic Accounting & Credit Quality Audit
                    </h3>

                    <div class="space-y-3 font-mono text-xs">
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Moody's / S&P Synthetic Credit Rating:</span>
                            <strong class="text-emerald-400">Aaa / AAA (Sovereign Parity)</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Altman Z-Score (Manufacturing/General):</span>
                            <strong class="text-emerald-400">8.77 (GOD-TIER SAFE ZONE)</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Piotroski F-Score:</span>
                            <strong class="text-emerald-400">8 / 9 (Superior Balance Sheet)</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Beneish M-Score:</span>
                            <strong class="text-emerald-400">-2.78 (Non-Manipulator &lt; -1.78)</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">5-Yr DuPont ROE (FY22 vs FY26):</span>
                            <strong class="text-neutral-200">43.7% &rarr; 30.2%</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Capitalized Research Asset (5-Yr SL):</span>
                            <strong class="text-cyan-400">$95.04 Billion (Amort: $29.85B)</strong>
                        </div>
                        <div class="flex justify-between border-b border-neutral-800/40 py-1.5">
                            <span class="text-neutral-400">Operating Lease Synthetic Debt:</span>
                            <strong class="text-neutral-200">$17.80 Billion (@ 4.93% Kd)</strong>
                        </div>
                        <div class="flex justify-between py-1.5">
                            <span class="text-neutral-400">Liquidation Tangible Net Floor:</span>
                            <strong class="text-neutral-400">$0.00 / share (Liabilities &gt; Tangible)</strong>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Interactive Tab Controller Script -->
    <script>
        function switchTab(tabId) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(function(el) {
                el.classList.add('hidden');
            });
            // Remove active classes
            document.querySelectorAll('.tab-btn').forEach(function(el) {
                el.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                el.classList.add('border-transparent', 'text-neutral-400');
            });
            // Show targeted tab
            const target = document.getElementById(tabId);
            if (target) {
                target.classList.remove('hidden');
            }
            // Activate button
            const btn = document.getElementById('btn-' + tabId);
            if (btn) {
                btn.classList.add('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                btn.classList.remove('border-transparent', 'text-neutral-400');
            }
        }
    </script>
</body>
</html>
"""

report_path = "ERVIS/projects/US_EQUITIES/MSFT/reports/dashboard.html"
with open(report_path, "w") as f:
    f.write(dashboard_html.strip())

print(f"Interactive Bloomberg HTML Dashboard written successfully to: {report_path}")
