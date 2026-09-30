import os

html_content = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERVIS :: Apple Inc. (NASDAQ: AAPL) Valuation Dashboard</title>
    
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
                    Apple Inc. (NASDAQ: AAPL) :: Institutional Valuation Dossier
                </h1>
                <span class="px-2 py-0.5 border border-amber-900/60 bg-amber-950/30 text-amber-300 font-mono text-[10px] font-bold">
                    [CONSUMER TECH & ECOSYSTEM]
                </span>
            </div>
            
            <div class="flex items-center space-x-4 text-xs font-mono">
                <span class="text-neutral-400">SPOT: <strong class="text-neutral-100 font-bold">$337.30</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">INTRINSIC: <strong class="text-amber-400 font-bold">$176.57</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="px-2 py-0.5 border border-rose-800 bg-rose-950/40 text-rose-400 font-bold">
                    TRIM / TAKE PROFITS (-47.7%)
                </span>
            </div>
        </div>

        <!-- Terminal Command Navigation Bar -->
        <div class="max-w-7xl mx-auto px-6 border-t border-neutral-800 flex space-x-1 overflow-x-auto text-xs font-mono">
            <button id="btn-tab-overview" onclick="switchTab('tab-overview')" class="tab-btn px-3.5 py-2 border-b-2 border-amber-500 text-amber-400 bg-neutral-900/60 transition-colors whitespace-nowrap active">
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
                [05] AI CAPEX AUDIT & HEALTH
            </button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-6 py-8">

        <!-- TAB 1: EXECUTIVE THESIS -->
        <div id="tab-overview" class="tab-content space-y-6">
            <div class="p-3 bg-amber-950/20 border border-amber-900/60 text-amber-300 flex items-center justify-between text-xs">
                <span>[VALUATION VERDICT] Apple is the world's most resilient consumer monopoly ($98.8B FCF / 107.5% shareholder payout ratio), but at $4.92 Trillion ($337.30/sh), the stock trades at an extreme 44x P/E multiple. Intrinsic DCF fair value is $154.68; SOTP relative value is $231.84. Triangulated institutional target: $176.57 (-47.7% downside).</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-amber-800 px-1.5 py-0.5">Tactical Alert</span>
            </div>

            <!-- Key Financial Matrix Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="p-4 bg-neutral-900/60 border border-neutral-800">
                    <div class="text-neutral-400 text-[11px]">DCF INTRINSIC VALUE</div>
                    <div class="text-xl font-bold text-amber-400 font-mono mt-1">$154.68</div>
                    <div class="text-[10px] text-neutral-500 mt-1">10-Yr Ginzu FCFF / Moat ROIC 28.0%</div>
                </div>
                <div class="p-4 bg-neutral-900/60 border border-neutral-800">
                    <div class="text-neutral-400 text-[11px]">SOTP DIVISIONAL VALUE</div>
                    <div class="text-xl font-bold text-neutral-100 font-mono mt-1">$231.84</div>
                    <div class="text-[10px] text-neutral-500 mt-1">Services (26x) + iPhone (14x)</div>
                </div>
                <div class="p-4 bg-neutral-900/60 border border-neutral-800">
                    <div class="text-neutral-400 text-[11px]">MONTE CARLO 10K MEDIAN</div>
                    <div class="text-xl font-bold text-neutral-100 font-mono mt-1">$142.08</div>
                    <div class="text-[10px] text-neutral-500 mt-1">Win Rate > $337: 0.0%</div>
                </div>
                <div class="p-4 bg-neutral-900/60 border border-neutral-800">
                    <div class="text-neutral-400 text-[11px]">CREDIT / CAPITAL STRUCTURE</div>
                    <div class="text-xl font-bold text-emerald-400 font-mono mt-1">Aaa / AAA</div>
                    <div class="text-[10px] text-neutral-500 mt-1">Base WACC: 8.72% | Terminal: 9.00%</div>
                </div>
            </div>

            <!-- Gate 1 Forensic Normalization Display -->
            <div class="p-5 bg-neutral-900/40 border border-neutral-800">
                <h3 class="text-xs font-bold text-neutral-200 uppercase tracking-wider mb-4 border-b border-neutral-800 pb-2">
                    Gate 1 Forensic Normalization Reconciliation ($ Millions)
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono text-xs">
                        <thead>
                            <tr class="border-b border-neutral-800 text-neutral-400">
                                <th class="pb-2">Accounting Item</th>
                                <th class="pb-2">Reported GAAP</th>
                                <th class="pb-2">Forensic Adjustment</th>
                                <th class="pb-2">Normalized Base</th>
                                <th class="pb-2">Methodology / Notes</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="py-2 font-semibold">Operating Income (EBIT)</td>
                                <td>$133,050.0M</td>
                                <td class="text-emerald-400">+$6,432.4M</td>
                                <td class="font-bold text-neutral-100">$139,482.4M</td>
                                <td class="text-neutral-400">Lease interest (+$682.4M) + R&D capitalization (+$5,750M)</td>
                            </tr>
                            <tr>
                                <td class="py-2 font-semibold">NOPAT (After-Tax EBIT)</td>
                                <td>$112,826.0M</td>
                                <td class="text-emerald-400">+$5,456.8M</td>
                                <td class="font-bold text-neutral-100">$118,282.8M</td>
                                <td class="text-neutral-400">Effective corporate tax rate 15.2%</td>
                            </tr>
                            <tr>
                                <td class="py-2 font-semibold">Capitalized Research Asset</td>
                                <td>$0.0M</td>
                                <td class="text-emerald-400">+$92,478.2M</td>
                                <td class="font-bold text-neutral-100">$92,478.2M</td>
                                <td class="text-neutral-400">5-Year straight-line capitalization ($28,800M amort)</td>
                            </tr>
                            <tr>
                                <td class="py-2 font-semibold">Synthetic Lease Debt</td>
                                <td>$0.0M</td>
                                <td class="text-amber-400">+$13,200.0M</td>
                                <td class="font-bold text-neutral-100">$13,200.0M</td>
                                <td class="text-neutral-400">ASC 842 commitments discounted at Kd = 5.17%</td>
                            </tr>
                            <tr>
                                <td class="py-2 font-semibold">Total Liquid Reserves</td>
                                <td>$54,697.0M</td>
                                <td class="text-emerald-400">+$77,723.0M</td>
                                <td class="font-bold text-neutral-100">$132,420.0M</td>
                                <td class="text-neutral-400">Includes non-current marketable securities war chest</td>
                            </tr>
                            <tr>
                                <td class="py-2 font-semibold">Net Cash Position</td>
                                <td>-$43,960.0M</td>
                                <td class="text-emerald-400">+$64,523.0M</td>
                                <td class="font-bold text-emerald-400">+$20,563.0M</td>
                                <td class="text-neutral-400">Liquid reserves exceed all funded debt ($98.7B) + leases ($13.2B)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- 5-Point DuPont ROE Progression -->
            <div class="p-5 bg-neutral-900/40 border border-neutral-800">
                <h3 class="text-xs font-bold text-neutral-200 uppercase tracking-wider mb-4 border-b border-neutral-800 pb-2">
                    Gate 2 DuPont 5-Point ROE Decomposition (5-Year Historical Evolution)
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-5 gap-3 font-mono">
                    <div class="p-3 bg-neutral-950 border border-neutral-800">
                        <div class="text-neutral-400 font-bold text-[11px]">FY2021</div>
                        <div class="text-sm font-bold text-neutral-200 mt-1">ROE: 150.1%</div>
                        <div class="text-[10px] text-neutral-500 mt-1">Tax: 0.8670 | Int: 1.0024</div>
                        <div class="text-[10px] text-neutral-500">Margin: 29.8% | Turn: 1.04x</div>
                        <div class="text-[10px] text-neutral-500">Equity Multiplier: 5.56x</div>
                    </div>
                    <div class="p-3 bg-neutral-950 border border-neutral-800">
                        <div class="text-neutral-400 font-bold text-[11px]">FY2022</div>
                        <div class="text-sm font-bold text-neutral-200 mt-1">ROE: 197.0%</div>
                        <div class="text-[10px] text-neutral-500 mt-1">Tax: 0.8379 | Int: 0.9972</div>
                        <div class="text-[10px] text-neutral-500">Margin: 30.3% | Turn: 1.12x</div>
                        <div class="text-[10px] text-neutral-500">Equity Multiplier: 6.96x</div>
                    </div>
                    <div class="p-3 bg-neutral-950 border border-neutral-800">
                        <div class="text-neutral-400 font-bold text-[11px]">FY2023</div>
                        <div class="text-sm font-bold text-neutral-200 mt-1">ROE: 156.1%</div>
                        <div class="text-[10px] text-neutral-500 mt-1">Tax: 0.8528 | Int: 0.9951</div>
                        <div class="text-[10px] text-neutral-500">Margin: 29.8% | Turn: 1.09x</div>
                        <div class="text-[10px] text-neutral-500">Equity Multiplier: 5.67x</div>
                    </div>
                    <div class="p-3 bg-neutral-950 border border-neutral-800">
                        <div class="text-neutral-400 font-bold text-[11px]">FY2024</div>
                        <div class="text-sm font-bold text-neutral-200 mt-1">ROE: 164.6%</div>
                        <div class="text-[10px] text-neutral-500 mt-1">Tax: 0.7591 | Int: 1.0022</div>
                        <div class="text-[10px] text-neutral-500">Margin: 31.5% | Turn: 1.07x</div>
                        <div class="text-[10px] text-neutral-500">Equity Multiplier: 6.41x</div>
                    </div>
                    <div class="p-3 bg-neutral-950 border border-amber-900/40 bg-amber-950/10">
                        <div class="text-amber-400 font-bold text-[11px]">FY2025 (AUDITED)</div>
                        <div class="text-sm font-bold text-amber-300 mt-1">ROE: 151.9%</div>
                        <div class="text-[10px] text-neutral-400 mt-1">Tax: 0.8390 | Int: 1.0034</div>
                        <div class="text-[10px] text-neutral-400">Margin: 32.0% | Turn: 1.16x</div>
                        <div class="text-[10px] text-neutral-400">Equity Multiplier: 4.87x</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: SUM-OF-THE-PARTS -->
        <div id="tab-sotp" class="tab-content hidden space-y-6">
            <div class="p-5 bg-neutral-900/40 border border-neutral-800">
                <h3 class="text-xs font-bold text-neutral-200 uppercase tracking-wider mb-4 border-b border-neutral-800 pb-2">
                    Sum-of-the-Parts (SOTP) Divisional Valuation Schedule
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono text-xs">
                        <thead>
                            <tr class="border-b border-neutral-800 text-neutral-400">
                                <th class="pb-2">Division / Segment</th>
                                <th class="pb-2">FY25 Revenue</th>
                                <th class="pb-2">EBITDA Margin</th>
                                <th class="pb-2">Division EBITDA</th>
                                <th class="pb-2">Target Multiple</th>
                                <th class="pb-2">Implied EV ($M)</th>
                                <th class="pb-2">Peer Comparables</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="py-2.5 font-bold text-neutral-100">iPhone Hardware</td>
                                <td>$215,000.0M</td>
                                <td>35.0%</td>
                                <td>$75,250.0M</td>
                                <td class="text-amber-400 font-bold">14.0x</td>
                                <td class="font-bold text-neutral-100">$1,053,500.0M</td>
                                <td class="text-neutral-400">Premium Consumer Hardware (Samsung, Sony)</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-neutral-100">Services & Ecosystem</td>
                                <td>$105,000.0M</td>
                                <td>72.0%</td>
                                <td>$75,600.0M</td>
                                <td class="text-amber-400 font-bold">26.0x</td>
                                <td class="font-bold text-neutral-100">$1,965,600.0M</td>
                                <td class="text-neutral-400">Recurring Subscription Platforms (MSFT, GOOGL)</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-neutral-100">Wearables, Home & Acc.</td>
                                <td>$38,000.0M</td>
                                <td>28.0%</td>
                                <td>$10,640.0M</td>
                                <td class="text-amber-400 font-bold">14.0x</td>
                                <td class="font-bold text-neutral-100">$148,960.0M</td>
                                <td class="text-neutral-400">Smart Wearables & IoT Ecosystem (Garmin)</td>
                            </tr>
                            <tr>
                                <td class="py-2.5 font-bold text-neutral-100">Mac & iPad Client</td>
                                <td>$58,000.0M</td>
                                <td>28.0%</td>
                                <td>$16,240.0M</td>
                                <td class="text-amber-400 font-bold">12.0x</td>
                                <td class="font-bold text-neutral-100">$194,880.0M</td>
                                <td class="text-neutral-400">Personal Computing & Tablets (Dell, HP)</td>
                            </tr>
                            <tr class="bg-neutral-950 font-bold text-neutral-100">
                                <td class="py-3">TOTAL SOTP ENTERPRISE VALUE</td>
                                <td>$416,000.0M</td>
                                <td>-</td>
                                <td>$177,730.0M</td>
                                <td>18.9x (Blended)</td>
                                <td class="text-amber-400">$3,362,940.0M</td>
                                <td>-$3.36 Trillion EV</td>
                            </tr>
                            <tr class="text-emerald-400 font-bold">
                                <td class="py-2.5">(+) Net Cash Bridge</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>+$20,563.0M</td>
                                <td>Liquid cash war chest</td>
                            </tr>
                            <tr class="bg-neutral-900 text-amber-300 font-bold text-sm">
                                <td class="py-3">IMPLIED SOTP EQUITY VALUE</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>$3,383,503.0M</td>
                                <td>$231.84 / Share</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: 10-YR GINZU DCF SCHEDULE -->
        <div id="tab-dcf" class="tab-content hidden space-y-6">
            <div class="p-5 bg-neutral-900/40 border border-neutral-800">
                <h3 class="text-xs font-bold text-neutral-200 uppercase tracking-wider mb-4 border-b border-neutral-800 pb-2">
                    Damodaran Ginzu 10-Year Pro-Forma DCF Schedule ($ Millions)
                </h3>
                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono text-[11px]">
                        <thead>
                            <tr class="border-b border-neutral-800 text-neutral-400">
                                <th class="pb-2">Year</th>
                                <th class="pb-2">Revenue</th>
                                <th class="pb-2">Growth</th>
                                <th class="pb-2">Margin</th>
                                <th class="pb-2">EBIT</th>
                                <th class="pb-2">NOPAT</th>
                                <th class="pb-2">Reinvestment</th>
                                <th class="pb-2">FCFF</th>
                                <th class="pb-2">WACC</th>
                                <th class="pb-2">PV of FCFF</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="py-1.5 font-bold">FY25 (Base)</td>
                                <td>$416,161.0M</td>
                                <td>-</td>
                                <td>33.5%</td>
                                <td>$139,482.4M</td>
                                <td>$118,282.8M</td>
                                <td>-</td>
                                <td>$98,767.0M</td>
                                <td>8.72%</td>
                                <td>-</td>
                            </tr>
                            <tr><td>Year 1 (FY26)</td><td>$447,373.1M</td><td>+7.5%</td><td>33.2%</td><td>$148,527.9M</td><td>$125,951.6M</td><td>$7,803.0M</td><td>$118,148.6M</td><td>8.72%</td><td>$108,672.3M</td></tr>
                            <tr><td>Year 2 (FY27)</td><td>$477,794.4M</td><td>+6.8%</td><td>33.5%</td><td>$160,061.1M</td><td>$135,731.8M</td><td>$7,605.3M</td><td>$128,126.5M</td><td>8.75%</td><td>$108,359.8M</td></tr>
                            <tr><td>Year 3 (FY28)</td><td>$506,462.1M</td><td>+6.0%</td><td>33.5%</td><td>$169,664.8M</td><td>$143,875.8M</td><td>$7,166.9M</td><td>$136,708.8M</td><td>8.78%</td><td>$106,357.2M</td></tr>
                            <tr><td>Year 4 (FY29)</td><td>$532,798.1M</td><td>+5.2%</td><td>33.2%</td><td>$176,889.0M</td><td>$150,001.9M</td><td>$6,584.0M</td><td>$143,417.9M</td><td>8.81%</td><td>$102,526.4M</td></tr>
                            <tr><td>Year 5 (FY30)</td><td>$558,372.5M</td><td>+4.8%</td><td>33.0%</td><td>$184,262.9M</td><td>$156,255.0M</td><td>$6,393.6M</td><td>$149,861.4M</td><td>8.84%</td><td>$98,409.7M</td></tr>
                            <tr><td>Year 6 (FY31)</td><td>$582,940.8M</td><td>+4.4%</td><td>32.8%</td><td>$191,204.6M</td><td>$162,141.5M</td><td>$6,142.1M</td><td>$155,999.4M</td><td>8.88%</td><td>$94,078.6M</td></tr>
                            <tr><td>Year 7 (FY32)</td><td>$606,258.5M</td><td>+4.0%</td><td>32.5%</td><td>$197,034.0M</td><td>$167,084.8M</td><td>$5,829.4M</td><td>$161,255.4M</td><td>8.91%</td><td>$89,286.7M</td></tr>
                            <tr><td>Year 8 (FY33)</td><td>$629,296.3M</td><td>+3.8%</td><td>32.3%</td><td>$203,262.7M</td><td>$172,366.8M</td><td>$5,759.5M</td><td>$166,607.3M</td><td>8.94%</td><td>$84,657.4M</td></tr>
                            <tr><td>Year 9 (FY34)</td><td>$651,321.7M</td><td>+3.5%</td><td>32.0%</td><td>$208,422.9M</td><td>$176,742.7M</td><td>$5,506.3M</td><td>$171,236.3M</td><td>8.97%</td><td>$79,850.5M</td></tr>
                            <tr><td>Year 10 (FY35)</td><td>$674,117.9M</td><td>+3.5%</td><td>32.0%</td><td>$215,717.7M</td><td>$182,928.6M</td><td>$5,699.1M</td><td>$177,229.6M</td><td>9.00%</td><td>$75,826.9M</td></tr>
                            <tr class="bg-neutral-950 font-bold text-neutral-100">
                                <td class="py-2">PV of 10-Yr FCFF</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td class="text-amber-400">$948,025.5M</td>
                            </tr>
                            <tr class="bg-neutral-950 font-bold text-neutral-100">
                                <td class="py-2">PV of Terminal Value</td>
                                <td>$697,712.0M</td>
                                <td>+3.50%</td>
                                <td>32.0%</td>
                                <td>$223,267.8M</td>
                                <td>$189,331.1M</td>
                                <td>$23,666.4M</td>
                                <td>$165,664.7M</td>
                                <td>9.00%</td>
                                <td class="text-amber-400">$1,288,903.5M</td>
                            </tr>
                            <tr class="bg-neutral-900 text-amber-300 font-bold text-xs">
                                <td class="py-2.5">DCF ENTERPRISE VALUE</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>$2,236,929.0M</td>
                            </tr>
                            <tr class="bg-neutral-900 text-emerald-400 font-bold text-xs">
                                <td class="py-2">(+) Net Cash Cushion</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>+$20,563.0M</td>
                            </tr>
                            <tr class="bg-neutral-900 text-amber-300 font-bold text-xs">
                                <td class="py-2.5">DCF EQUITY FAIR VALUE</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>-</td>
                                <td>$2,257,492.0M ($154.68/sh)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 4: SCENARIOS & 10K MONTE CARLO -->
        <div id="tab-scenarios" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="p-4 bg-neutral-900/60 border border-neutral-800">
                    <div class="text-rose-400 font-bold text-xs">BEAR CASE :: ANTITRUST & SLOW REPLACEMENT</div>
                    <div class="text-xl font-bold font-mono text-neutral-100 mt-2">$118.50</div>
                    <div class="text-neutral-500 text-[11px] mt-1">Downside: -64.9%</div>
                    <ul class="text-[10px] text-neutral-400 space-y-1 mt-3 list-disc list-inside">
                        <li>Google search TAC ($20B) eliminated by DOJ remedy</li>
                        <li>EU DMA App Store fee compressed from 30% to 12%</li>
                        <li>iPhone upgrade cycle extends from 3.8 to 4.5 years</li>
                    </ul>
                </div>
                <div class="p-4 bg-amber-950/20 border border-amber-900/60">
                    <div class="text-amber-400 font-bold text-xs">BASE CASE :: TRIANGULATED TARGET</div>
                    <div class="text-xl font-bold font-mono text-amber-300 mt-2">$176.57</div>
                    <div class="text-neutral-400 text-[11px] mt-1">Downside: -47.7%</div>
                    <ul class="text-[10px] text-neutral-300 space-y-1 mt-3 list-disc list-inside">
                        <li>60% DCF Intrinsic ($154.68) + 30% SOTP ($231.84) + 10% MC ($142.08)</li>
                        <li>Apple Intelligence drives steady 7% top-line growth</li>
                        <li>Operating margin sustained at 32.5% via Services mix</li>
                    </ul>
                </div>
                <div class="p-4 bg-neutral-900/60 border border-neutral-800">
                    <div class="text-emerald-400 font-bold text-xs">BULL CASE :: ACCELERATED AI SUPERCYCLE</div>
                    <div class="text-xl font-bold font-mono text-neutral-100 mt-2">$248.90</div>
                    <div class="text-neutral-500 text-[11px] mt-1">Downside: -26.2%</div>
                    <ul class="text-[10px] text-neutral-400 space-y-1 mt-3 list-disc list-inside">
                        <li>iPhone 16/17 triggers 260M unit replacement supercycle</li>
                        <li>Services revenue reaches $150B+ driven by AI subscriptions</li>
                        <li>Terminal ROIC sustained at 35.0%</li>
                    </ul>
                </div>
            </div>

            <!-- Monte Carlo Statistics Table -->
            <div class="p-5 bg-neutral-900/40 border border-neutral-800 font-mono">
                <h3 class="text-xs font-bold text-neutral-200 uppercase tracking-wider mb-4 border-b border-neutral-800 pb-2">
                    10,000-Trial Monte Carlo Simulation Output
                </h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                    <div class="p-3 bg-neutral-950 border border-neutral-800">
                        <div class="text-neutral-500 text-[10px]">10TH PERCENTILE (P10)</div>
                        <div class="text-base font-bold text-rose-400 mt-1">$119.82</div>
                    </div>
                    <div class="p-3 bg-neutral-950 border border-neutral-800">
                        <div class="text-neutral-500 text-[10px]">50TH PERCENTILE (MEDIAN)</div>
                        <div class="text-base font-bold text-amber-400 mt-1">$142.08</div>
                    </div>
                    <div class="p-3 bg-neutral-950 border border-neutral-800">
                        <div class="text-neutral-500 text-[10px]">90TH PERCENTILE (P90)</div>
                        <div class="text-base font-bold text-emerald-400 mt-1">$168.95</div>
                    </div>
                    <div class="p-3 bg-neutral-950 border border-neutral-800">
                        <div class="text-neutral-500 text-[10px]">WIN RATE (> $337.30)</div>
                        <div class="text-base font-bold text-rose-500 mt-1">0.0%</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: AI CAPEX AUDIT & HEALTH -->
        <div id="tab-diagnostics" class="tab-content hidden space-y-6">
            <div class="p-5 bg-neutral-900/40 border border-neutral-800">
                <h3 class="text-xs font-bold text-neutral-200 uppercase tracking-wider mb-4 border-b border-neutral-800 pb-2">
                    Gate 4B: Apple Client Edge AI Architecture vs Hyperscaler GPU Cloud ($ Millions)
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono text-xs">
                    <div class="space-y-3">
                        <div class="p-3 bg-neutral-950 border border-neutral-800">
                            <div class="text-neutral-400 text-[11px] font-bold">APPLE PHYSICAL CAPEX INTENSITY</div>
                            <div class="text-lg font-bold text-emerald-400 mt-1">$12,715.0M (3.06% of Revenue)</div>
                            <div class="text-[10px] text-neutral-500 mt-1">Asset-light outsourced fabrication. Minimal direct datacenter footprint.</div>
                        </div>
                        <div class="p-3 bg-neutral-950 border border-neutral-800">
                            <div class="text-neutral-400 text-[11px] font-bold">PRIVATE CLOUD COMPUTE (PCC)</div>
                            <div class="text-sm font-bold text-neutral-100 mt-1">Custom Apple Silicon (M-Series Ultra)</div>
                            <div class="text-[10px] text-neutral-500 mt-1">Runs high-complexity inference on custom server chips with hardware-isolated security.</div>
                        </div>
                        <div class="p-3 bg-neutral-950 border border-neutral-800">
                            <div class="text-neutral-400 text-[11px] font-bold">CLIENT EDGE ON-DEVICE INFERENCE</div>
                            <div class="text-sm font-bold text-emerald-400 mt-1">85%+ Executed Locally</div>
                            <div class="text-[10px] text-neutral-500 mt-1">Local 3B parameter SLM models run directly on A17/A18/A19 Neural Engines. Zero cloud server cost.</div>
                        </div>
                    </div>

                    <div class="space-y-3">
                        <div class="p-3 bg-neutral-950 border border-neutral-800">
                            <div class="text-neutral-400 text-[11px] font-bold">CONSUMER HARDWARE SELF-FINANCING</div>
                            <div class="text-sm font-bold text-amber-300 mt-1">1.4 Billion Installed iPhone Pool</div>
                            <div class="text-[10px] text-neutral-400 mt-1">~80% of current iPhones lack 8GB RAM. Consumers spend $1,000+ per device to access Apple Intelligence, self-financing AI infrastructure!</div>
                        </div>
                        <div class="p-3 bg-neutral-950 border border-neutral-800">
                            <div class="text-neutral-400 text-[11px] font-bold">SHAREHOLDER CAPITAL RETURN ENGINE</div>
                            <div class="text-lg font-bold text-neutral-100 mt-1">$106,132.0M Total Payout</div>
                            <div class="text-[10px] text-neutral-400 mt-1">107.5% of Free Cash Flow ($98.8B) returned via $90.7B buybacks + $15.4B dividends.</div>
                        </div>
                        <div class="p-3 bg-neutral-950 border border-neutral-800">
                            <div class="text-neutral-400 text-[11px] font-bold">SOLVENCY & AUDIT SCORES</div>
                            <div class="text-sm font-bold text-emerald-400 mt-1">Altman Z: 12.83 | Piotroski: 8/9 | Beneish: -2.92</div>
                            <div class="text-[10px] text-neutral-500 mt-1">Pristine balance sheet health; zero manipulation hazard.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <footer class="border-t border-neutral-800 py-6 text-center text-neutral-500 font-mono text-[10px]">
        ERVIS TERMINAL v2.5 :: INSTITUTIONAL VALUATION SYSTEM :: STRICTLY CONFIDENTIAL FOR PORTFOLIO DESK USE
    </footer>

    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                btn.classList.add('border-transparent', 'text-neutral-400');
            });
            
            const activeContent = document.getElementById(tabId);
            if (activeContent) activeContent.classList.remove('hidden');
            
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

report_path = "ERVIS/projects/US_EQUITIES/AAPL/reports/dashboard.html"
with open(report_path, "w") as f:
    f.write(html_content)

print(f"Successfully generated interactive dashboard at: {report_path}")
