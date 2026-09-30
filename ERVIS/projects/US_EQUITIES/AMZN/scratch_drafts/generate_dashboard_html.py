#!/usr/bin/env python3
"""
ERVIS Terminal Dashboard Generator :: Amazon.com, Inc. (NASDAQ: AMZN)
Generates dark monochrome Bloomberg Terminal styled HTML dashboard.
"""

import os
import json

output_file = "ERVIS/projects/US_EQUITIES/AMZN/reports/dashboard.html"

html_content = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERVIS :: Amazon.com, Inc. (NASDAQ: AMZN) Valuation Dashboard</title>
    
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
        .b-border {
            border-color: #27272a;
        }
        .b-bg-card {
            background-color: #121215;
        }
        .b-bg-inner {
            background-color: #18181b;
        }
        .metric-label {
            color: #a1a1aa;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .metric-value {
            color: #f4f4f5;
            font-size: 1.15rem;
            font-weight: 700;
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
                    Amazon.com, Inc. (NASDAQ: AMZN) :: Institutional Valuation Dossier
                </h1>
                <span class="px-2 py-0.5 border border-amber-900/60 bg-amber-950/30 text-amber-300 font-mono text-[10px] font-bold">
                    [AI TITANS CAMPAIGN #02]
                </span>
            </div>
            
            <div class="flex items-center space-x-4 text-xs font-mono">
                <span class="text-neutral-400">SPOT: <strong class="text-neutral-100 font-bold">$255.70</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">TARGET: <strong class="text-amber-400 font-bold">$203.46</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="px-2 py-0.5 border border-rose-800 bg-rose-950/40 text-rose-400 font-bold">
                    TRIM / TAKE PROFITS (-20.4%)
                </span>
            </div>
        </div>

        <!-- Terminal Command Navigation Bar -->
        <div class="max-w-7xl mx-auto px-6 border-t border-neutral-800 flex space-x-1 overflow-x-auto text-xs font-mono">
            <button id="btn-tab-overview" onclick="switchTab('tab-overview')" class="tab-btn px-3.5 py-2 border-b-2 border-amber-500 text-amber-400 bg-neutral-900/60 transition-colors whitespace-nowrap">
                [01] EXECUTIVE THESIS & FORENSICS
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
            <button id="btn-tab-gate4b" onclick="switchTab('tab-gate4b')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [05] GATE 4B AI CAPEX AUDIT & ROI
            </button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-6 py-8">

        <!-- TAB 1: EXECUTIVE THESIS & FORENSICS -->
        <div id="tab-overview" class="tab-content space-y-6">
            <div class="p-3.5 bg-amber-950/20 border border-amber-900/60 text-amber-300 flex flex-col md:flex-row items-start md:items-center justify-between gap-2 text-xs">
                <span><strong>[VALUATION VERDICT]</strong> Amazon is an extraordinary secular commercial empire ($716.9B revenue / $110.7B restated EBIT_0), but market valuation at $255.70 ($2.76T) fully prices in frictionless AI monetization. While AWS ($128.7B rev) and Advertising ($68.4B rev) drive operating leverage, Amazon's unprecedented $131.8B annual CapEx cycle absorbs 94.5% of Operating Cash Flow, crushing FCF to $7.7B. Fair value under DCF is $186.84; SOTP value is $249.48; blended institutional target is $203.46 (-20.4% downside). Recommendation: TRIM / TAKE PROFITS into strength; tactical accumulation zone is $165.00 - $185.00.</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-amber-800 px-2 py-0.5 whitespace-nowrap">Tactical Rating: TRIM</span>
            </div>

            <!-- Key Metric KPI Strip -->
            <div class="grid grid-cols-2 md:grid-cols-6 gap-3">
                <div class="b-bg-card border b-border p-3">
                    <div class="metric-label">Target Price</div>
                    <div class="metric-value text-amber-400">$203.46</div>
                    <div class="text-[10px] text-rose-400 mt-1">-20.4% vs Spot</div>
                </div>
                <div class="b-bg-card border b-border p-3">
                    <div class="metric-label">10-Yr Ginzu DCF</div>
                    <div class="metric-value text-neutral-100">$186.84</div>
                    <div class="text-[10px] text-neutral-400 mt-1">WACC 9.27% -> 9.0%</div>
                </div>
                <div class="b-bg-card border b-border p-3">
                    <div class="metric-label">SOTP Relative Value</div>
                    <div class="metric-value text-sky-400">$249.48</div>
                    <div class="text-[10px] text-neutral-400 mt-1">Sum of 4 Divisions</div>
                </div>
                <div class="b-bg-card border b-border p-3">
                    <div class="metric-label">Monte Carlo Median</div>
                    <div class="metric-value text-neutral-200">$165.11</div>
                    <div class="text-[10px] text-neutral-400 mt-1">Win Rate: 0.1%</div>
                </div>
                <div class="b-bg-card border b-border p-3">
                    <div class="metric-label">Synthetic Rating</div>
                    <div class="metric-value text-emerald-400">A1 / AA</div>
                    <div class="text-[10px] text-neutral-400 mt-1">Coverage: 48.7x</div>
                </div>
                <div class="b-bg-card border b-border p-3">
                    <div class="metric-label">FY25 Physical CapEx</div>
                    <div class="metric-value text-rose-400">$131.8B</div>
                    <div class="text-[10px] text-rose-400/80 mt-1">94.5% of CFO absorbed</div>
                </div>
            </div>

            <!-- Forensic Normalization Table (Gate 1) -->
            <div class="b-bg-card border b-border p-4">
                <div class="flex items-center justify-between pb-3 border-b b-border mb-3">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider">
                        [GATE 1 FORENSIC AUDIT] R&D CAPITALIZATION & OPERATING LEASE DISCOUNTING ($M)
                    </h3>
                    <span class="text-[11px] text-neutral-500 font-mono">Damodaran Ginzu Methodology</span>
                </div>
                <table class="w-full text-left font-mono text-xs">
                    <thead>
                        <tr class="text-neutral-500 border-b b-border">
                            <th class="py-2">Forensic Adjustment Component</th>
                            <th class="py-2 text-right">Reported GAAP</th>
                            <th class="py-2 text-right">Forensic Restatement</th>
                            <th class="py-2">Methodology / Institutional Rationale</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-neutral-800/60">
                        <tr>
                            <td class="py-2 text-neutral-300 font-semibold">Operating Profit (EBIT_0)</td>
                            <td class="py-2 text-right text-neutral-400">$79,975.0</td>
                            <td class="py-2 text-right text-amber-400 font-bold">$110,717.1</td>
                            <td class="py-2 text-neutral-400">Restated +$30,742.1M (+38.4%) from R&D capitalization and lease interest add-back</td>
                        </tr>
                        <tr>
                            <td class="py-2 text-neutral-300 font-semibold">After-Tax Operating Profit (NOPAT_0)</td>
                            <td class="py-2 text-right text-neutral-400">$64,299.9</td>
                            <td class="py-2 text-right text-emerald-400 font-bold">$89,016.5</td>
                            <td class="py-2 text-neutral-400">Computed at 19.6% corporate effective tax rate on restated EBIT_0</td>
                        </tr>
                        <tr>
                            <td class="py-2 text-neutral-300 font-semibold">Capitalized Research Asset (Tech & Content)</td>
                            <td class="py-2 text-right text-neutral-400">$0.0</td>
                            <td class="py-2 text-right text-sky-400 font-bold">$271,220.8</td>
                            <td class="py-2 text-neutral-400">5-Year straight-line capitalization ($108.5B in '25, $88.5B in '24, $85.6B in '23, $73.2B in '22, $56.1B in '21)</td>
                        </tr>
                        <tr>
                            <td class="py-2 text-neutral-300 font-semibold">Current Year R&D Amortization</td>
                            <td class="py-2 text-right text-neutral-400">$108,520.0</td>
                            <td class="py-2 text-right text-neutral-300 font-bold">$82,389.4</td>
                            <td class="py-2 text-neutral-400">Net EBIT boost: $108,520M expensed minus $82,389.4M amortization = +$26,130.6M</td>
                        </tr>
                        <tr>
                            <td class="py-2 text-neutral-300 font-semibold">Synthetic Operating Lease Debt</td>
                            <td class="py-2 text-right text-neutral-400">Off-Income Stmt</td>
                            <td class="py-2 text-right text-neutral-300 font-bold">$87,339.0</td>
                            <td class="py-2 text-neutral-400">Fulfillment center and AWS datacenter leases discounted at 5.28% pre-tax Kd (Lease interest: $4,611.5M)</td>
                        </tr>
                        <tr>
                            <td class="py-2 text-neutral-300 font-semibold">Total Adjusted Debt & Lease Obligations</td>
                            <td class="py-2 text-right text-neutral-400">$75,148.0</td>
                            <td class="py-2 text-right text-rose-400 font-bold">$162,487.0</td>
                            <td class="py-2 text-neutral-400">Funded debt ($75.1B) + Capital/Operating lease liabilities ($87.3B)</td>
                        </tr>
                        <tr>
                            <td class="py-2 text-neutral-300 font-semibold">Cash, ST Inv & Liquid Reserves</td>
                            <td class="py-2 text-right text-neutral-300">$123,029.0</td>
                            <td class="py-2 text-right text-neutral-300 font-bold">$123,029.0</td>
                            <td class="py-2 text-neutral-400">Liquid reserves against funded debt and lease commitments</td>
                        </tr>
                        <tr>
                            <td class="py-2 text-neutral-300 font-semibold">Adjusted Net Debt Bridge</td>
                            <td class="py-2 text-right text-neutral-400">-$47,881.0 (Cash)</td>
                            <td class="py-2 text-right text-rose-400 font-bold">+$39,458.0 (Debt)</td>
                            <td class="py-2 text-neutral-400">Full inclusion of lease liabilities converts Amazon from net cash to $39.5B Net Debt</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Gate 2 Regressions & Health Diagnostics -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="b-bg-card border b-border p-4">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider pb-2 border-b b-border mb-3">
                        [GATE 2 ECONOMETRIC REGRESSIONS] (OLS THRESHOLD R² ≥ 0.85)
                    </h3>
                    <div class="space-y-3">
                        <div class="p-2.5 b-bg-inner border b-border">
                            <div class="flex justify-between items-center text-xs">
                                <span class="font-semibold text-neutral-200">AWS Cloud Rev vs Global Cloud Spend</span>
                                <span class="px-1.5 py-0.5 bg-emerald-950/40 text-emerald-400 border border-emerald-800 text-[10px]">R² = 0.9888 [PASS]</span>
                            </div>
                            <div class="text-[11px] text-neutral-400 mt-1">Slope: +0.3168 | Intercept: +7.13 | High correlation to enterprise infrastructure migration</div>
                        </div>
                        <div class="p-2.5 b-bg-inner border b-border">
                            <div class="flex justify-between items-center text-xs">
                                <span class="font-semibold text-neutral-200">AWS Operating Income vs AWS Revenue</span>
                                <span class="px-1.5 py-0.5 bg-emerald-950/40 text-emerald-400 border border-emerald-800 text-[10px]">R² = 0.9322 [PASS]</span>
                            </div>
                            <div class="text-[11px] text-neutral-400 mt-1">Slope: +0.4357 | Intercept: -$11.39 | Operating leverage accelerates as scale surpasses $100B</div>
                        </div>
                        <div class="p-2.5 b-bg-inner border b-border">
                            <div class="flex justify-between items-center text-xs">
                                <span class="font-semibold text-neutral-200">North America Retail vs US E-Commerce Spend</span>
                                <span class="px-1.5 py-0.5 bg-emerald-950/40 text-emerald-400 border border-emerald-800 text-[10px]">R² = 0.9988 [PASS]</span>
                            </div>
                            <div class="text-[11px] text-neutral-400 mt-1">Slope: +0.4208 | Intercept: -$83.69 | Near-perfect correlation to US macro online penetration</div>
                        </div>
                        <div class="p-2.5 b-bg-inner border b-border">
                            <div class="flex justify-between items-center text-xs">
                                <span class="font-semibold text-neutral-200">Advertising Services vs Digital Ad Market</span>
                                <span class="px-1.5 py-0.5 bg-emerald-950/40 text-emerald-400 border border-emerald-800 text-[10px]">R² = 0.9952 [PASS]</span>
                            </div>
                            <div class="text-[11px] text-neutral-400 mt-1">Slope: +0.1147 | Intercept: -$25.56 | Sponsored ads & Prime Video ad tier expansion</div>
                        </div>
                    </div>
                </div>

                <div class="b-bg-card border b-border p-4">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider pb-2 border-b b-border mb-3">
                        [GATE 2 FINANCIAL HEALTH & DUPONT 5-POINT BREAKDOWN]
                    </h3>
                    <div class="grid grid-cols-3 gap-2 mb-3">
                        <div class="p-2 b-bg-inner border b-border text-center">
                            <div class="text-[10px] text-neutral-400">Altman Z-Score</div>
                            <div class="text-sm font-bold text-emerald-400">5.70</div>
                            <div class="text-[9px] text-neutral-500">Safe Zone (>2.99)</div>
                        </div>
                        <div class="p-2 b-bg-inner border b-border text-center">
                            <div class="text-[10px] text-neutral-400">Piotroski F-Score</div>
                            <div class="text-sm font-bold text-emerald-400">8 / 9</div>
                            <div class="text-[9px] text-neutral-500">Strong Quality</div>
                        </div>
                        <div class="p-2 b-bg-inner border b-border text-center">
                            <div class="text-[10px] text-neutral-400">Beneish M-Score</div>
                            <div class="text-sm font-bold text-emerald-400">-2.74</div>
                            <div class="text-[9px] text-neutral-500">Non-Manipulator</div>
                        </div>
                    </div>
                    <div class="text-xs font-semibold text-neutral-300 mb-1.5">5-Year DuPont ROE Trend (2021 -> 2025):</div>
                    <table class="w-full text-left font-mono text-[11px]">
                        <thead>
                            <tr class="text-neutral-500 border-b b-border">
                                <th class="py-1">FY</th>
                                <th class="py-1 text-right">Tax B.</th>
                                <th class="py-1 text-right">Int B.</th>
                                <th class="py-1 text-right">Op Mgn</th>
                                <th class="py-1 text-right">Asset TO</th>
                                <th class="py-1 text-right">Eq Mult</th>
                                <th class="py-1 text-right text-neutral-200">ROE</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/40">
                            <tr><td>2021</td><td class="text-right">0.87</td><td class="text-right">1.53</td><td class="text-right">5.3%</td><td class="text-right">1.12x</td><td class="text-right">3.04x</td><td class="text-right font-bold text-emerald-400">24.1%</td></tr>
                            <tr><td>2022</td><td class="text-right">0.46</td><td class="text-right">-0.48</td><td class="text-right">2.4%</td><td class="text-right">1.11x</td><td class="text-right">3.17x</td><td class="text-right font-bold text-rose-400">-1.9%</td></tr>
                            <tr><td>2023</td><td class="text-right">0.81</td><td class="text-right">1.02</td><td class="text-right">6.4%</td><td class="text-right">1.09x</td><td class="text-right">2.61x</td><td class="text-right font-bold text-neutral-200">15.1%</td></tr>
                            <tr><td>2024</td><td class="text-right">0.86</td><td class="text-right">1.00</td><td class="text-right">10.8%</td><td class="text-right">1.02x</td><td class="text-right">2.19x</td><td class="text-right font-bold text-emerald-400">20.7%</td></tr>
                            <tr><td>2025</td><td class="text-right">0.80</td><td class="text-right">1.22</td><td class="text-right">11.2%</td><td class="text-right">0.88x</td><td class="text-right">1.99x</td><td class="text-right font-bold text-emerald-400">18.9%</td></tr>
                        </tbody>
                    </table>
                    <div class="text-[10px] text-neutral-500 mt-2 italic">*Note: 2021-2022 interest/tax burden impacted by Rivian equity valuation swings. Operational ROE quality is at an all-time high.</div>
                </div>
            </div>
        </div>

        <!-- TAB 2: SUM-OF-THE-PARTS (SOTP) -->
        <div id="tab-sotp" class="tab-content hidden space-y-6">
            <div class="b-bg-card border b-border p-4">
                <div class="flex items-center justify-between pb-3 border-b b-border mb-4">
                    <div>
                        <h3 class="text-xs font-bold text-neutral-200 tracking-wider">
                            [GATE 4 SUM-OF-THE-PARTS (SOTP) DIVISIONAL BREAKDOWN]
                        </h3>
                        <p class="text-[11px] text-neutral-400 mt-0.5">Disaggregating Amazon into its 4 autonomous economic engines</p>
                    </div>
                    <div class="text-right">
                        <div class="text-xs text-neutral-400">Implied SOTP Value:</div>
                        <div class="text-base font-bold text-sky-400 font-mono">$249.48 / share</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    <!-- AWS -->
                    <div class="p-3.5 b-bg-inner border border-sky-900/60 rounded">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="font-bold text-sky-400">1. AWS CLOUD & AI</span>
                            <span class="text-[10px] px-1.5 py-0.5 bg-sky-950 text-sky-300 border border-sky-800">22.0x EBITDA</span>
                        </div>
                        <div class="text-lg font-bold text-neutral-100 font-mono">$1,276.0 B</div>
                        <div class="text-[11px] text-neutral-400 mt-2 space-y-1">
                            <div>Revenue: <strong class="text-neutral-200">$128.7B</strong> (+20% YoY)</div>
                            <div>Operating EBIT: <strong class="text-neutral-200">$45.6B</strong> (35.4%)</div>
                            <div>Base EBITDA: <strong class="text-neutral-200">$58.0B</strong></div>
                            <div>Peer Benchmark: Microsoft Azure, Google Cloud, Oracle OCI</div>
                        </div>
                    </div>

                    <!-- 1P/3P Retail -->
                    <div class="p-3.5 b-bg-inner border border-amber-900/60 rounded">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="font-bold text-amber-400">2. 1P/3P RETAIL & STORES</span>
                            <span class="text-[10px] px-1.5 py-0.5 bg-amber-950 text-amber-300 border border-amber-800">12.0x EBITDA</span>
                        </div>
                        <div class="text-lg font-bold text-neutral-100 font-mono">$540.0 B</div>
                        <div class="text-[11px] text-neutral-400 mt-2 space-y-1">
                            <div>Revenue: <strong class="text-neutral-200">$446.0B</strong></div>
                            <div>Operating EBIT: <strong class="text-neutral-200">$34.3B</strong> (7.7%)</div>
                            <div>Base EBITDA: <strong class="text-neutral-200">$45.0B</strong></div>
                            <div>Peer Benchmark: Walmart, Costco, Target, Shopify</div>
                        </div>
                    </div>

                    <!-- Advertising -->
                    <div class="p-3.5 b-bg-inner border border-emerald-900/60 rounded">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="font-bold text-emerald-400">3. ADVERTISING SERVICES</span>
                            <span class="text-[10px] px-1.5 py-0.5 bg-emerald-950 text-emerald-300 border border-emerald-800">20.0x EBITDA</span>
                        </div>
                        <div class="text-lg font-bold text-neutral-100 font-mono">$720.0 B</div>
                        <div class="text-[11px] text-neutral-400 mt-2 space-y-1">
                            <div>Revenue: <strong class="text-neutral-200">$68.4B</strong> (+22% YoY)</div>
                            <div>Estimated EBIT: <strong class="text-neutral-200">$34.2B</strong> (~50%)</div>
                            <div>Base EBITDA: <strong class="text-neutral-200">$36.0B</strong></div>
                            <div>Peer Benchmark: Meta Platforms, Alphabet</div>
                        </div>
                    </div>

                    <!-- Subscription Prime -->
                    <div class="p-3.5 b-bg-inner border border-purple-900/60 rounded">
                        <div class="flex justify-between items-center text-xs mb-1">
                            <span class="font-bold text-purple-400">4. PRIME SUBSCRIPTIONS</span>
                            <span class="text-[10px] px-1.5 py-0.5 bg-purple-950 text-purple-300 border border-purple-800">4.0x EV/Sales</span>
                        </div>
                        <div class="text-lg font-bold text-neutral-100 font-mono">$194.4 B</div>
                        <div class="text-[11px] text-neutral-400 mt-2 space-y-1">
                            <div>Revenue: <strong class="text-neutral-200">$48.6B</strong> (+10% YoY)</div>
                            <div>Ecosystem Value: High-LTV Prime churn moat</div>
                            <div>Valuation Multiple: 4.0x EV / Subscription Sales</div>
                            <div>Peer Benchmark: Netflix, Apple Services, Spotify</div>
                        </div>
                    </div>
                </div>

                <!-- SOTP Enterprise to Equity Bridge Table -->
                <div class="p-3 b-bg-inner border b-border font-mono text-xs">
                    <div class="font-bold text-neutral-200 mb-2 border-b b-border pb-1">CONSOLIDATED SOTP VALUATION BRIDGE</div>
                    <div class="space-y-1.5 text-neutral-300">
                        <div class="flex justify-between"><span>Sum of Segment Enterprise Values:</span><strong class="text-neutral-100">$2,730,400 M ($2.730 Trillion)</strong></div>
                        <div class="flex justify-between text-rose-400"><span>Less: Adjusted Net Debt (Funded + Leases - Cash):</span><strong>-$39,458 M</strong></div>
                        <div class="flex justify-between border-t b-border pt-1.5 text-sky-400 font-bold"><span>Implied SOTP Equity Value:</span><span>$2,690,942 M ($2.691 Trillion)</span></div>
                        <div class="flex justify-between text-neutral-400"><span>Diluted Shares Outstanding:</span><span>10,786.31 Million</span></div>
                        <div class="flex justify-between border-t b-border pt-1.5 text-base font-bold text-amber-400"><span>Implied Intrinsic SOTP Value Per Share:</span><span>$249.48</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: 10-YR GINZU DCF SCHEDULE -->
        <div id="tab-dcf" class="tab-content hidden space-y-6">
            <div class="b-bg-card border b-border p-4">
                <div class="flex items-center justify-between pb-3 border-b b-border mb-3">
                    <div>
                        <h3 class="text-xs font-bold text-neutral-200 tracking-wider">
                            [GATE 4 10-YEAR DISCRETE GINZU DCF MODEL] ($M)
                        </h3>
                        <p class="text-[11px] text-neutral-400 mt-0.5">Damodaran Sales-to-Capital reinvestment with terminal durable moat constraint</p>
                    </div>
                    <div class="text-right">
                        <div class="text-xs text-neutral-400">DCF Intrinsic Value:</div>
                        <div class="text-base font-bold text-amber-400 font-mono">$186.84 / share</div>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left font-mono text-[11px] whitespace-nowrap">
                        <thead>
                            <tr class="text-neutral-500 border-b b-border">
                                <th class="py-2 pr-4">Metric ($M)</th>
                                <th class="py-2 text-right px-2">FY25</th>
                                <th class="py-2 text-right px-2">FY26E</th>
                                <th class="py-2 text-right px-2">FY27E</th>
                                <th class="py-2 text-right px-2">FY28E</th>
                                <th class="py-2 text-right px-2">FY29E</th>
                                <th class="py-2 text-right px-2">FY30E</th>
                                <th class="py-2 text-right px-2">FY31E</th>
                                <th class="py-2 text-right px-2">FY32E</th>
                                <th class="py-2 text-right px-2">FY33E</th>
                                <th class="py-2 text-right px-2">FY34E</th>
                                <th class="py-2 text-right px-2">FY35E</th>
                                <th class="py-2 text-right pl-2 text-amber-400">Terminal</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/40 text-neutral-300">
                            <tr>
                                <td class="py-2 font-semibold">Total Revenue</td>
                                <td class="text-right px-2">716,924</td>
                                <td class="text-right px-2">802,955</td>
                                <td class="text-right px-2">891,280</td>
                                <td class="text-right px-2">975,952</td>
                                <td class="text-right px-2">1,054,028</td>
                                <td class="text-right px-2">1,127,810</td>
                                <td class="text-right px-2">1,195,478</td>
                                <td class="text-right px-2">1,255,252</td>
                                <td class="text-right px-2">1,311,739</td>
                                <td class="text-right px-2">1,364,208</td>
                                <td class="text-right px-2">1,416,048</td>
                                <td class="text-right pl-2 text-amber-400 font-bold">1,469,858</td>
                            </tr>
                            <tr>
                                <td class="py-2 text-neutral-400">Growth Rate %</td>
                                <td class="text-right px-2">-</td>
                                <td class="text-right px-2">12.0%</td>
                                <td class="text-right px-2">11.0%</td>
                                <td class="text-right px-2">9.5%</td>
                                <td class="text-right px-2">8.0%</td>
                                <td class="text-right px-2">7.0%</td>
                                <td class="text-right px-2">6.0%</td>
                                <td class="text-right px-2">5.0%</td>
                                <td class="text-right px-2">4.5%</td>
                                <td class="text-right px-2">4.0%</td>
                                <td class="text-right px-2">3.8%</td>
                                <td class="text-right pl-2 text-amber-400">3.8%</td>
                            </tr>
                            <tr>
                                <td class="py-2 text-neutral-400">Operating Margin %</td>
                                <td class="text-right px-2">15.4%</td>
                                <td class="text-right px-2">15.6%</td>
                                <td class="text-right px-2">16.0%</td>
                                <td class="text-right px-2">16.4%</td>
                                <td class="text-right px-2">16.7%</td>
                                <td class="text-right px-2">17.0%</td>
                                <td class="text-right px-2">17.2%</td>
                                <td class="text-right px-2">17.4%</td>
                                <td class="text-right px-2">17.5%</td>
                                <td class="text-right px-2">17.5%</td>
                                <td class="text-right px-2">17.5%</td>
                                <td class="text-right pl-2 text-amber-400">17.5%</td>
                            </tr>
                            <tr>
                                <td class="py-2 font-semibold">Normalized EBIT</td>
                                <td class="text-right px-2">110,717</td>
                                <td class="text-right px-2">125,261</td>
                                <td class="text-right px-2">142,605</td>
                                <td class="text-right px-2">160,056</td>
                                <td class="text-right px-2">176,023</td>
                                <td class="text-right px-2">191,728</td>
                                <td class="text-right px-2">205,622</td>
                                <td class="text-right px-2">218,414</td>
                                <td class="text-right px-2">229,554</td>
                                <td class="text-right px-2">238,736</td>
                                <td class="text-right px-2">247,808</td>
                                <td class="text-right pl-2 text-amber-400 font-bold">257,225</td>
                            </tr>
                            <tr>
                                <td class="py-2 text-neutral-400">NOPAT (t=19.6%)</td>
                                <td class="text-right px-2">89,017</td>
                                <td class="text-right px-2">100,710</td>
                                <td class="text-right px-2">114,654</td>
                                <td class="text-right px-2">128,685</td>
                                <td class="text-right px-2">141,522</td>
                                <td class="text-right px-2">154,149</td>
                                <td class="text-right px-2">165,320</td>
                                <td class="text-right px-2">175,605</td>
                                <td class="text-right px-2">184,562</td>
                                <td class="text-right px-2">191,944</td>
                                <td class="text-right px-2">199,238</td>
                                <td class="text-right pl-2 text-amber-400 font-bold">206,809</td>
                            </tr>
                            <tr>
                                <td class="py-2 text-rose-400">Reinvestment (S/C 2.40)</td>
                                <td class="text-right px-2">-</td>
                                <td class="text-right px-2">35,846</td>
                                <td class="text-right px-2">36,802</td>
                                <td class="text-right px-2">35,280</td>
                                <td class="text-right px-2">32,532</td>
                                <td class="text-right px-2">30,742</td>
                                <td class="text-right px-2">28,195</td>
                                <td class="text-right px-2">24,906</td>
                                <td class="text-right px-2">23,536</td>
                                <td class="text-right px-2">21,862</td>
                                <td class="text-right px-2">21,600</td>
                                <td class="text-right pl-2 text-rose-400 font-bold">43,659</td>
                            </tr>
                            <tr class="bg-neutral-900/60 font-semibold">
                                <td class="py-2 text-emerald-400">Free Cash Flow (FCFF)</td>
                                <td class="text-right px-2">7,695</td>
                                <td class="text-right px-2 text-emerald-400">64,863</td>
                                <td class="text-right px-2 text-emerald-400">77,852</td>
                                <td class="text-right px-2 text-emerald-400">93,405</td>
                                <td class="text-right px-2 text-emerald-400">108,990</td>
                                <td class="text-right px-2 text-emerald-400">123,407</td>
                                <td class="text-right px-2 text-emerald-400">137,125</td>
                                <td class="text-right px-2 text-emerald-400">150,699</td>
                                <td class="text-right px-2 text-emerald-400">161,025</td>
                                <td class="text-right px-2 text-emerald-400">170,082</td>
                                <td class="text-right px-2 text-emerald-400">177,638</td>
                                <td class="text-right pl-2 text-emerald-400 font-bold">163,150</td>
                            </tr>
                            <tr>
                                <td class="py-2 text-neutral-400">Discount Factor (WACC)</td>
                                <td class="text-right px-2">1.000</td>
                                <td class="text-right px-2">0.915</td>
                                <td class="text-right px-2">0.838</td>
                                <td class="text-right px-2">0.767</td>
                                <td class="text-right px-2">0.703</td>
                                <td class="text-right px-2">0.644</td>
                                <td class="text-right px-2">0.590</td>
                                <td class="text-right px-2">0.541</td>
                                <td class="text-right px-2">0.496</td>
                                <td class="text-right px-2">0.455</td>
                                <td class="text-right px-2">0.418</td>
                                <td class="text-right pl-2 text-amber-400">PV(TV)</td>
                            </tr>
                            <tr class="font-bold text-neutral-100">
                                <td class="py-2">Present Value of FCFF</td>
                                <td class="text-right px-2">-</td>
                                <td class="text-right px-2">59,360</td>
                                <td class="text-right px-2">65,212</td>
                                <td class="text-right px-2">71,677</td>
                                <td class="text-right px-2">76,608</td>
                                <td class="text-right px-2">79,489</td>
                                <td class="text-right px-2">80,942</td>
                                <td class="text-right px-2">81,540</td>
                                <td class="text-right px-2">79,902</td>
                                <td class="text-right px-2">77,440</td>
                                <td class="text-right px-2">74,213</td>
                                <td class="text-right pl-2 text-sky-400 font-bold">$1,310,211 M</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- DCF Enterprise Value Bridge -->
                <div class="mt-4 grid grid-cols-1 md:grid-cols-5 gap-3 pt-3 border-t b-border text-xs font-mono">
                    <div class="p-2 b-bg-inner border b-border">
                        <div class="text-[10px] text-neutral-500">PV of 10-Yr Cash Flows</div>
                        <div class="text-sm font-bold text-neutral-200">$746,382 M</div>
                    </div>
                    <div class="p-2 b-bg-inner border b-border">
                        <div class="text-[10px] text-neutral-500">PV of Terminal Value</div>
                        <div class="text-sm font-bold text-neutral-200">$1,310,211 M</div>
                        <div class="text-[9px] text-neutral-500">63.7% of EV (ROIC 18%)</div>
                    </div>
                    <div class="p-2 b-bg-inner border b-border">
                        <div class="text-[10px] text-neutral-500">Enterprise Value (EV)</div>
                        <div class="text-sm font-bold text-neutral-100">$2,056,593 M</div>
                    </div>
                    <div class="p-2 b-bg-inner border b-border">
                        <div class="text-[10px] text-rose-400">Less: Net Debt Bridge</div>
                        <div class="text-sm font-bold text-rose-400">-$39,458 M</div>
                    </div>
                    <div class="p-2 b-bg-inner border b-border">
                        <div class="text-[10px] text-amber-400">DCF Value Per Share</div>
                        <div class="text-sm font-bold text-amber-400">$186.84</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: SCENARIOS & 10K MONTE CARLO -->
        <div id="tab-scenarios" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- 10,000 Trial Simulation -->
                <div class="b-bg-card border b-border p-4">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider pb-2 border-b b-border mb-3">
                        [10,000-TRIAL MONTE CARLO STOCHASTIC SIMULATION]
                    </h3>
                    <div class="grid grid-cols-2 gap-3 mb-4">
                        <div class="p-3 b-bg-inner border b-border">
                            <div class="metric-label">Monte Carlo Median</div>
                            <div class="text-lg font-bold text-neutral-100 font-mono">$165.11</div>
                            <div class="text-[10px] text-neutral-400 mt-1">50th percentile outcome</div>
                        </div>
                        <div class="p-3 b-bg-inner border b-border">
                            <div class="metric-label">Probability > Spot ($255.70)</div>
                            <div class="text-lg font-bold text-rose-400 font-mono">0.1%</div>
                            <div class="text-[10px] text-rose-400/80 mt-1">Severe asymmetric downside</div>
                        </div>
                    </div>
                    <div class="space-y-2 font-mono text-xs">
                        <div class="flex justify-between p-2 b-bg-inner border b-border"><span>10th Percentile (Downside Bear):</span><strong class="text-rose-400">$142.18 / share</strong></div>
                        <div class="flex justify-between p-2 b-bg-inner border b-border"><span>25th Percentile:</span><strong class="text-neutral-300">$152.94 / share</strong></div>
                        <div class="flex justify-between p-2 b-bg-inner border b-border"><span>50th Percentile (Median):</span><strong class="text-neutral-100">$165.11 / share</strong></div>
                        <div class="flex justify-between p-2 b-bg-inner border b-border"><span>75th Percentile:</span><strong class="text-neutral-300">$179.82 / share</strong></div>
                        <div class="flex justify-between p-2 b-bg-inner border b-border"><span>90th Percentile (Bull Case):</span><strong class="text-emerald-400">$196.45 / share</strong></div>
                    </div>
                </div>

                <!-- Liquidation Floor & Valuation Triangulation -->
                <div class="b-bg-card border b-border p-4">
                    <h3 class="text-xs font-bold text-neutral-200 tracking-wider pb-2 border-b b-border mb-3">
                        [LIQUIDATION HAIRCUT FLOOR & TARGET TRIANGULATION]
                    </h3>
                    <div class="space-y-3 font-mono text-xs">
                        <div class="p-3 b-bg-inner border b-border">
                            <div class="font-bold text-neutral-300 mb-1">Gate 4 Downside Liquidation Haircut:</div>
                            <div class="text-neutral-400 text-[11px] space-y-0.5">
                                <div>Cash (100%): $123,029M | Receivables (75%): $31,500M</div>
                                <div>Inventory (50%): $18,000M | Net PP&E (30%): $114,000M</div>
                                <div>Intangibles/R&D (5%): $13,561M | Total Recovery: $300,090M</div>
                                <div class="text-rose-400 font-semibold">Less Total Liabilities: $406,977M => Distressed Equity Floor: $0.00</div>
                            </div>
                        </div>

                        <div class="p-3 b-bg-inner border border-amber-900/60">
                            <div class="font-bold text-amber-400 mb-2">INSTITUTIONAL TRIANGULATION RECONCILIATION:</div>
                            <div class="space-y-1.5 text-[11px] text-neutral-300">
                                <div class="flex justify-between"><span>60% 10-Yr Ginzu DCF ($186.84):</span><strong>$112.10</strong></div>
                                <div class="flex justify-between"><span>30% SOTP Divisional Multiple ($249.48):</span><strong>$74.84</strong></div>
                                <div class="flex justify-between"><span>10% Monte Carlo Median ($165.11):</span><strong>$16.51</strong></div>
                                <div class="flex justify-between border-t b-border pt-1.5 text-amber-400 font-bold text-xs"><span>Final Institutional Target Price:</span><span>$203.46</span></div>
                                <div class="flex justify-between text-neutral-400"><span>Current Spot Market Price:</span><span>$255.70</span></div>
                                <div class="flex justify-between border-t b-border pt-1 text-rose-400 font-bold"><span>Implied Valuation Gap:</span><span>-20.4% (TRIM / TAKE PROFITS)</span></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: GATE 4B AI CAPEX AUDIT & ROI -->
        <div id="tab-gate4b" class="tab-content hidden space-y-6">
            <div class="b-bg-card border b-border p-4">
                <div class="flex items-center justify-between pb-3 border-b b-border mb-4">
                    <div>
                        <h3 class="text-xs font-bold text-neutral-200 tracking-wider">
                            [GATE 4B SPECIALIZED AI CAPEX PAYOUT & CUSTOMER ROI ENGINE]
                        </h3>
                        <p class="text-[11px] text-neutral-400 mt-0.5">Auditing Amazon's $131.8B CapEx supercycle and AWS generative AI payback vs 3.5-year obsolescence</p>
                    </div>
                    <div class="text-right">
                        <span class="px-2 py-0.5 border border-amber-800 bg-amber-950/40 text-amber-400 font-mono text-[10px] font-bold">
                            OBSOLESCENCE DEFICIT (+1.63 YRS)
                        </span>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <!-- CapEx Absorption -->
                    <div class="p-3.5 b-bg-inner border border-rose-900/60 rounded">
                        <div class="metric-label text-rose-400 font-bold">CASH FLOW ABSORPTION DRAG</div>
                        <div class="text-2xl font-bold text-rose-400 font-mono mt-1">94.5%</div>
                        <div class="text-[11px] text-neutral-400 mt-2 space-y-1">
                            <div>Operating Cash Flow: <strong class="text-neutral-200">$139.5B</strong></div>
                            <div>Capital Expenditure: <strong class="text-rose-400">$131.8B</strong></div>
                            <div>Realized FCF: <strong class="text-neutral-200">$7.7B</strong> (-76.6% YoY)</div>
                            <div>FCF Conversion: <strong>5.5%</strong> of CFO (down from 28.4%)</div>
                        </div>
                    </div>

                    <!-- Hardware Payback -->
                    <div class="p-3.5 b-bg-inner border border-amber-900/60 rounded">
                        <div class="metric-label text-amber-400 font-bold">HARDWARE PAYBACK PERIOD</div>
                        <div class="text-2xl font-bold text-amber-400 font-mono mt-1">5.13 Yrs</div>
                        <div class="text-[11px] text-neutral-400 mt-2 space-y-1">
                            <div>AI Hardware Purchases: <strong class="text-neutral-200">$50.0B</strong></div>
                            <div>GenAI Gross Profit (65%): <strong class="text-neutral-200">$9.75B</strong></div>
                            <div>Annual D&A (3.5 Yrs): <strong class="text-neutral-200">$14.29B</strong></div>
                            <div>Obsolescence Window: <strong class="text-rose-400">3.50 Years</strong></div>
                        </div>
                    </div>

                    <!-- Monetization Gap -->
                    <div class="p-3.5 b-bg-inner border border-sky-900/60 rounded">
                        <div class="metric-label text-sky-400 font-bold">ANNUAL MONETIZATION DEFICIT</div>
                        <div class="text-2xl font-bold text-sky-400 font-mono mt-1">$18.52 B</div>
                        <div class="text-[11px] text-neutral-400 mt-2 space-y-1">
                            <div>Target Customer ROIC: <strong class="text-neutral-200">15.0%</strong></div>
                            <div>Required GenAI Software Rev: <strong class="text-neutral-200">$33.52B</strong></div>
                            <div>Actual Realized Rev: <strong class="text-neutral-200">$15.00B</strong></div>
                            <div>Net AI Operating Income: <strong class="text-rose-400">-$4.54B</strong></div>
                        </div>
                    </div>
                </div>

                <!-- Deep Structural Analysis Table -->
                <div class="space-y-3 font-mono text-xs">
                    <div class="p-3 b-bg-inner border b-border">
                        <div class="font-bold text-neutral-200 mb-2 border-b b-border pb-1">GATE 4B CORE INSTITUTIONAL FINDINGS:</div>
                        <div class="space-y-2 text-neutral-300 text-[11px] leading-relaxed">
                            <p><strong class="text-amber-400">1. The CapEx Run-Rate Paradox:</strong> Amazon has scaled capital intensity to 18.4% of total revenue ($131.8B in FY25), with the vast majority (~$105B) allocated to AWS data center infrastructure, custom silicon (Trainium2, Inferentia2), and high-density Nvidia Blackwell clusters. While this preserves AWS's cloud leadership, it completely eliminates free cash flow generation in the intermediate term.</p>
                            <p><strong class="text-rose-400">2. Hardware Obsolescence vs Payback Deficit:</strong> At a 3.5-year hardware useful life, straight-line depreciation on Amazon's $50B generative AI hardware allocation is $14.29B per year. Even with $15.0B in estimated annualized GenAI revenue run-rate (Bedrock, Q Developer/Business, SageMaker genAI) generating $9.75B in gross profit, the segment generates a Net AI Operating Deficit of -$4.54B (-9.07% economic ROI) and requires 5.13 years to pay back—1.63 years past the hardware's useful life.</p>
                            <p><strong class="text-sky-400">3. The $18.5B Software Monetization Gap:</strong> To hit the institutional 15% ROIC benchmark, AWS enterprise customers and AWS native AI services must scale software revenue from $15.0B to $33.52B annually. Until enterprise application layer workflow adoption catches up, hyperscalers face continuous depreciation drag.</p>
                            <p><strong class="text-neutral-200">4. Zero Shareholder Cash Returns:</strong> Unlike Apple, Alphabet, or Meta, Amazon pays zero dividends and executed zero share repurchases in FY2025. Every dollar of cash generation is recycled into datacenter concrete, fiber, and compute silicon.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer Command Bar -->
    <footer class="border-t border-neutral-800 bg-[#0c0d0e] py-3 text-center text-neutral-500 font-mono text-[10px]">
        ERVIS TERMINAL v2.5 :: POWERED BY DAMODARAN GINZU & NUS CFA CHAMPION DUAL-ENGINE ARCHITECTURE :: US_EQUITIES/AMZN
    </footer>

    <!-- Interactive Tabs Logic -->
    <script>
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active', 'border-amber-500', 'text-amber-400');
                btn.classList.add('border-transparent', 'text-neutral-400');
            });
            
            const selectedTab = document.getElementById(tabId);
            if (selectedTab) selectedTab.classList.remove('hidden');
            
            const btnMap = {
                'tab-overview': 'btn-tab-overview',
                'tab-sotp': 'btn-tab-sotp',
                'tab-dcf': 'btn-tab-dcf',
                'tab-scenarios': 'btn-tab-scenarios',
                'tab-gate4b': 'btn-tab-gate4b'
            };
            
            const activeBtn = document.getElementById(btnMap[tabId]);
            if (activeBtn) {
                activeBtn.classList.add('active', 'border-amber-500', 'text-amber-400');
                activeBtn.classList.remove('border-transparent', 'text-neutral-400');
            }
        }
    </script>
</body>
</html>
"""

with open(output_file, "w") as f:
    f.write(html_content)

print(f"Successfully generated interactive Bloomberg HTML dashboard at: {output_file}")
