#!/usr/bin/env python3
"""
ERVIS DASHBOARD GENERATOR :: META PLATFORMS, INC. (NASDAQ: META)
Produces institutional Bloomberg Terminal styled HTML dashboard.
"""

import os
import json

PROJECT_DIR = "ERVIS/projects/US_EQUITIES/META"
REPORTS_DIR = f"{PROJECT_DIR}/reports"
MODELS_DIR = f"{PROJECT_DIR}/models"
REGRESSIONS_DIR = f"{PROJECT_DIR}/regressions"

with open(f"{MODELS_DIR}/valuation_engine_outputs.json") as f:
    val = json.load(f)

with open(f"{REGRESSIONS_DIR}/diagnostics_audit.json") as f:
    diag = json.load(f)

html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERVIS :: Meta Platforms, Inc. (NASDAQ: META) Institutional Valuation Dossier</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        serif: ['Newsreader', 'Georgia', 'serif'],
                        mono: ['"JetBrains Mono"', 'monospace']
                    }}
                }}
            }}
        }}
    </script>
    
    <style>
        body {{
            background-color: #09090b;
            color: #d4d4d8;
            font-family: 'JetBrains Mono', monospace;
        }}
        .tab-btn.active {{
            border-bottom-color: #f59e0b;
            color: #fbbf24;
            background-color: rgba(24, 24, 27, 0.8);
        }}
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
                    Meta Platforms, Inc. (NASDAQ: META) :: Institutional Valuation Dossier
                </h1>
                <span class="px-2 py-0.5 border border-blue-900/60 bg-blue-950/30 text-blue-300 font-mono text-[10px] font-bold">
                    [GATE 1-5 + 4B CERTIFIED]
                </span>
            </div>
            
            <div class="flex items-center space-x-4 text-xs font-mono">
                <span class="text-neutral-400">SPOT: <strong class="text-neutral-100 font-bold">${val['spot_price_usd']:.2f}</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">DCF: <strong class="text-amber-400 font-bold">${val['gate_4_valuation']['dcf_intrinsic_value_usd']:.2f}</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">TARGET: <strong class="text-emerald-400 font-bold">${val['gate_4_valuation']['final_target_price_usd']:.2f}</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="px-2 py-0.5 border border-emerald-800 bg-emerald-950/40 text-emerald-400 font-bold">
                    {val['gate_4_valuation']['final_rating']}
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
            <button id="btn-tab-capex" onclick="switchTab('tab-capex')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [05] GATE 4B: AI CAPEX & ROI AUDIT
            </button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-6 py-8">

        <!-- TAB 1: EXECUTIVE THESIS & FORENSICS -->
        <div id="tab-overview" class="tab-content space-y-6">
            <div class="p-3 bg-blue-950/20 border border-blue-900/60 text-blue-300 flex items-center justify-between text-xs">
                <span>[VALUATION VERDICT] Meta Platforms is valued at an intrinsic DCF of <strong>${val['gate_4_valuation']['dcf_intrinsic_value_usd']:.2f}/share</strong> and SOTP fair value of <strong>${val['gate_4_valuation']['sotp_intrinsic_value_usd']:.2f}/share</strong>. Blended target price is <strong>${val['gate_4_valuation']['final_target_price_usd']:.2f}</strong> (+4.0% upside), supporting an <strong>ACCUMULATE / HOLD</strong> rating. While core ad cash generation is monopolistic, near-term valuation is bounded by a $68B/year AI CapEx surge yielding an initial 0.84-year hardware payback deficit.</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-blue-800 px-1.5 py-0.5">Analyst Stance</span>
            </div>

            <!-- 3 Core Investment Theses Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="p-5 bg-[#0f0f11] border border-neutral-800 space-y-3">
                    <div class="flex items-center justify-between border-b border-neutral-800 pb-2">
                        <span class="text-amber-400 font-bold font-mono">[THESIS 01]</span>
                        <span class="text-neutral-500 font-mono text-[11px]">THE AD ALCHEMY ENGINE</span>
                    </div>
                    <h3 class="text-sm font-serif font-semibold text-neutral-100">
                        Advantage+ & Unconnected Feed Uplift
                    </h3>
                    <p class="text-neutral-400 font-serif leading-relaxed text-xs">
                        Meta's proprietary recommendation models have structurally decoupled ad growth from friend graphs. AI-driven unconnected recommendations drove Reels dwell time up +10%, while Advantage+ automated creative delivers <strong>+22% ROAS</strong>, driving $201.0B in FY25 revenue (+22.2% YoY).
                    </p>
                </div>

                <div class="p-5 bg-[#0f0f11] border border-neutral-800 space-y-3">
                    <div class="flex items-center justify-between border-b border-neutral-800 pb-2">
                        <span class="text-amber-400 font-bold font-mono">[THESIS 02]</span>
                        <span class="text-neutral-500 font-mono text-[11px]">THE OPEN-SOURCE PARADOX</span>
                    </div>
                    <h3 class="text-sm font-serif font-semibold text-neutral-100">
                        Zero Direct Revenue vs. Commoditizing Rivals
                    </h3>
                    <p class="text-neutral-400 font-serif leading-relaxed text-xs">
                        Llama produces <strong>$0 direct software licensing revenue</strong>. However, open-sourcing Llama commoditizes the foundational layer, destroying proprietary tollbooths from OpenAI and Google Cloud while ensuring Meta never pays third-party API rents on its 3.2B daily active users.
                    </p>
                </div>

                <div class="p-5 bg-[#0f0f11] border border-neutral-800 space-y-3">
                    <div class="flex items-center justify-between border-b border-neutral-800 pb-2">
                        <span class="text-amber-400 font-bold font-mono">[THESIS 03]</span>
                        <span class="text-neutral-500 font-mono text-[11px]">THE REALITY LABS BLEED</span>
                    </div>
                    <h3 class="text-sm font-serif font-semibold text-neutral-100">
                        -$17.8B Loss Drag Offset by Ray-Ban Option
                    </h3>
                    <p class="text-neutral-400 font-serif leading-relaxed text-xs">
                        Reality Labs burned -$17.8B in FY25 and -$16.1B in FY24. In our SOTP, we deduct <strong>-$100.0B</strong> in capitalized operational drag, partially offset by a <strong>+$25.0B</strong> strategic call option on the runaway viral success of Ray-Ban Meta AI smart glasses.
                    </p>
                </div>
            </div>

            <!-- Gate 1 Forensic Normalization Block -->
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Gate 1: Forensic Accounting Restatement Schedule
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Capitalizing 5-Year Straight-Line R&D and Operating Lease Commitments at 5.18% Pre-Tax Kd</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono">
                        NORMALIZED EBIT_0: ${val['gate_1_forensic_normalization']['normalized_ebit_0']:,.1f}M
                    </span>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="p-4 bg-[#141416] border border-neutral-800/80">
                        <span class="text-neutral-500 text-[11px] block">Reported GAAP Operating Income</span>
                        <span class="text-base font-bold text-neutral-100 font-mono mt-1 block">${val['gate_1_forensic_normalization']['reported_ebit_0']:,.1f}M</span>
                        <span class="text-[10px] text-neutral-500 mt-1 block">41.4% Reported Margin</span>
                    </div>
                    <div class="p-4 bg-[#141416] border border-neutral-800/80">
                        <span class="text-neutral-500 text-[11px] block">Capitalized R&D Asset</span>
                        <span class="text-base font-bold text-emerald-400 font-mono mt-1 block">${val['gate_1_forensic_normalization']['capitalized_rd_asset']:,.1f}M</span>
                        <span class="text-[10px] text-emerald-500/80 mt-1 block">EBIT Addback: +${val['gate_1_forensic_normalization']['rd_ebit_adjustment']:,.1f}M</span>
                    </div>
                    <div class="p-4 bg-[#141416] border border-neutral-800/80">
                        <span class="text-neutral-500 text-[11px] block">Synthetic Lease Debt</span>
                        <span class="text-base font-bold text-amber-400 font-mono mt-1 block">${val['gate_1_forensic_normalization']['operating_lease_discounted_debt']:,.1f}M</span>
                        <span class="text-[10px] text-amber-500/80 mt-1 block">Interest Addback: +${val['gate_1_forensic_normalization']['operating_lease_interest_addback']:,.1f}M</span>
                    </div>
                    <div class="p-4 bg-[#141416] border border-neutral-800/80">
                        <span class="text-neutral-500 text-[11px] block">True Net Cash Buffer</span>
                        <span class="text-base font-bold text-emerald-400 font-mono mt-1 block">+${val['gate_1_forensic_normalization']['net_cash_total']:,.1f}M</span>
                        <span class="text-[10px] text-emerald-500/80 mt-1 block">$109.1B Liquid vs $83.9B Debt</span>
                    </div>
                </div>
            </div>

            <!-- Master Valuation Summary Table -->
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Master Valuation Triangulation Schedule
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Ground Truth: FY2025 Audited 10-K | Rf = 4.58% | Base WACC = 9.08% | Terminal WACC = 9.00%</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono">
                        BLENDED TARGET: ${val['gate_4_valuation']['final_target_price_usd']:.2f} (+4.0%)
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
                                <td class="p-3 font-serif text-neutral-100 font-semibold">10-Yr Discrete Ginzu DCF</td>
                                <td class="p-3 text-neutral-400">16% Y1 growth -> 3.5% terminal, 48% -> 42% margin, 20.0% Moat ROIC</td>
                                <td class="p-3 text-right font-mono">${val['gate_4_valuation']['dcf_pv_discrete_fcff_m'] + val['gate_4_valuation']['dcf_pv_terminal_val_m']:,.1f}M</td>
                                <td class="p-3 text-right text-emerald-400 font-mono">+${val['gate_1_forensic_normalization']['net_cash_total']:,.0f}M (+${val['gate_1_forensic_normalization']['net_cash_total']/val['shares_outstanding_m']:.2f})</td>
                                <td class="p-3 text-right text-neutral-100 font-bold font-mono">${val['gate_4_valuation']['dcf_intrinsic_value_usd']:.2f}</td>
                                <td class="p-3 text-right text-emerald-400 font-bold font-mono">+1.3%</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">Sum-of-the-Parts (SOTP) Multiples</td>
                                <td class="p-3 text-neutral-400">FoA Core (15.5x EBITDA), WhatsApp (12.0x Sales), RL Drag (-$75B net)</td>
                                <td class="p-3 text-right font-mono">${val['gate_4_valuation']['sotp_foa_core_m'] + val['gate_4_valuation']['sotp_whatsapp_biz_m'] + val['gate_4_valuation']['sotp_reality_labs_drag_m']:,.1f}M</td>
                                <td class="p-3 text-right text-emerald-400 font-mono">+${val['gate_1_forensic_normalization']['net_cash_total']:,.0f}M (+${val['gate_1_forensic_normalization']['net_cash_total']/val['shares_outstanding_m']:.2f})</td>
                                <td class="p-3 text-right text-neutral-100 font-bold font-mono">${val['gate_4_valuation']['sotp_intrinsic_value_usd']:.2f}</td>
                                <td class="p-3 text-right text-emerald-400 font-bold font-mono">+9.1%</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">10,000-Trial Monte Carlo Median</td>
                                <td class="p-3 text-neutral-400">Stochastic trials across CAGR (5-22%), margins (32-50%), WACC (7.5-11.5%)</td>
                                <td class="p-3 text-right font-mono">$1,653,500M</td>
                                <td class="p-3 text-right text-emerald-400 font-mono">+${val['gate_1_forensic_normalization']['net_cash_total']:,.0f}M</td>
                                <td class="p-3 text-right text-neutral-100 font-bold font-mono">${val['gate_4_valuation']['monte_carlo_10k']['median_usd']:.2f}</td>
                                <td class="p-3 text-right text-rose-400 font-bold font-mono">-6.3%</td>
                            </tr>
                            <tr class="bg-amber-950/10 font-bold">
                                <td class="p-3 font-serif text-amber-300">Blended Institutional Target Price</td>
                                <td class="p-3 text-amber-400/80">65% Ginzu DCF Intrinsic + 35% SOTP Divisional Fair Value</td>
                                <td class="p-3 text-right text-amber-400 font-mono">${(0.65*1790122.8 + 0.35*1929750.0):,.1f}M</td>
                                <td class="p-3 text-right text-emerald-400 font-mono">+${val['gate_1_forensic_normalization']['net_cash_total']:,.0f}M</td>
                                <td class="p-3 text-right text-amber-400 text-sm font-mono">${val['gate_4_valuation']['final_target_price_usd']:.2f}</td>
                                <td class="p-3 text-right text-emerald-400 text-sm font-mono">+{val['gate_4_valuation']['upside_pct']:.1f}% [{val['gate_4_valuation']['final_rating']}]</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-400 italic">Downside Net Liquidation Floor</td>
                                <td class="p-3 text-neutral-500">Cash 100%, AFS 95%, AR 75%, PP&E 30%, Intangibles 5% less all debt</td>
                                <td class="p-3 text-right text-neutral-500 font-mono">-</td>
                                <td class="p-3 text-right text-neutral-500 font-mono">-</td>
                                <td class="p-3 text-right text-neutral-400 font-mono">${val['gate_4_valuation']['liquidation_haircut_floor_usd']:.2f}</td>
                                <td class="p-3 text-right text-rose-400 font-mono">-98.0%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 2: SUM-OF-THE-PARTS (SOTP) -->
        <div id="tab-sotp" class="tab-content space-y-6 hidden">
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Sum-of-the-Parts (SOTP) Divisional Carve-Out
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Multiples benchmarked against high-margin digital advertising and conversational SaaS peers</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono">
                        SOTP VALUE: ${val['gate_4_valuation']['sotp_intrinsic_value_usd']:.2f} ($1,955B Equity)
                    </span>
                </div>

                <div class="overflow-x-auto border border-neutral-800">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-3">Operating Segment</th>
                                <th class="p-3">Core Economic Driver</th>
                                <th class="p-3 text-right">FY26 Metric ($M)</th>
                                <th class="p-3 text-right">Valuation Multiple</th>
                                <th class="p-3 text-right">Enterprise Value</th>
                                <th class="p-3 text-right">EV / Share</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">Family of Apps Core (FB, IG, Messenger)</td>
                                <td class="p-3 text-neutral-400">Monopolistic social graph, Reels, Advantage+ AI ad auction engine</td>
                                <td class="p-3 text-right font-mono">$118,500M (EBITDA)</td>
                                <td class="p-3 text-right font-mono text-amber-400">15.5x EV/EBITDA</td>
                                <td class="p-3 text-right font-mono font-bold text-neutral-100">${val['gate_4_valuation']['sotp_foa_core_m']:,.1f}M</td>
                                <td class="p-3 text-right font-mono">${val['gate_4_valuation']['sotp_foa_core_m']/val['shares_outstanding_m']:.2f}</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">WhatsApp Business & Click-to-Message</td>
                                <td class="p-3 text-neutral-400">Enterprise Cloud API, Click-to-WhatsApp ads, merchant conversational CRM</td>
                                <td class="p-3 text-right font-mono">$14,000M (Sales)</td>
                                <td class="p-3 text-right font-mono text-amber-400">12.0x EV/Sales</td>
                                <td class="p-3 text-right font-mono font-bold text-neutral-100">${val['gate_4_valuation']['sotp_whatsapp_biz_m']:,.1f}M</td>
                                <td class="p-3 text-right font-mono">${val['gate_4_valuation']['sotp_whatsapp_biz_m']/val['shares_outstanding_m']:.2f}</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">Reality Labs (VR/AR & Smart Glasses)</td>
                                <td class="p-3 text-neutral-400">-$18.0B annual cash burn drag (-$100B) offset by Ray-Ban AI option (+$25B)</td>
                                <td class="p-3 text-right font-mono">-$18,000M (Losses)</td>
                                <td class="p-3 text-right font-mono text-rose-400">Net Drag + Option</td>
                                <td class="p-3 text-right font-mono font-bold text-rose-400">${val['gate_4_valuation']['sotp_reality_labs_drag_m']:,.1f}M</td>
                                <td class="p-3 text-right font-mono text-rose-400">-${abs(val['gate_4_valuation']['sotp_reality_labs_drag_m'])/val['shares_outstanding_m']:.2f}</td>
                            </tr>
                            <tr class="bg-neutral-900/40 font-bold">
                                <td class="p-3 font-serif text-neutral-100">Combined Segment Enterprise Value</td>
                                <td class="p-3 text-neutral-400">Sum of operating divisional values</td>
                                <td class="p-3 text-right font-mono">-</td>
                                <td class="p-3 text-right font-mono">-</td>
                                <td class="p-3 text-right font-mono font-bold text-neutral-100">${(val['gate_4_valuation']['sotp_foa_core_m'] + val['gate_4_valuation']['sotp_whatsapp_biz_m'] + val['gate_4_valuation']['sotp_reality_labs_drag_m']):,.1f}M</td>
                                <td class="p-3 text-right font-mono">${(val['gate_4_valuation']['sotp_foa_core_m'] + val['gate_4_valuation']['sotp_whatsapp_biz_m'] + val['gate_4_valuation']['sotp_reality_labs_drag_m'])/val['shares_outstanding_m']:.2f}</td>
                            </tr>
                            <tr class="text-emerald-400">
                                <td class="p-3 font-serif font-semibold">(+) Net Cash & Liquid Marketable Securities</td>
                                <td class="p-3 text-neutral-400">Cash & ST Inv ($81.6B) + AFS ($27.5B) - Adjusted Debt ($83.9B)</td>
                                <td class="p-3 text-right font-mono">-</td>
                                <td class="p-3 text-right font-mono">1.0x</td>
                                <td class="p-3 text-right font-mono font-bold">+${val['gate_1_forensic_normalization']['net_cash_total']:,.1f}M</td>
                                <td class="p-3 text-right font-mono">+${val['gate_1_forensic_normalization']['net_cash_total']/val['shares_outstanding_m']:.2f}</td>
                            </tr>
                            <tr class="bg-amber-950/20 font-bold text-amber-300">
                                <td class="p-3 font-serif text-sm">Total SOTP Equity Fair Value</td>
                                <td class="p-3 text-amber-400/80">Net Cash Bridge Adjusted Equity Fair Value</td>
                                <td class="p-3 text-right font-mono">-</td>
                                <td class="p-3 text-right font-mono">-</td>
                                <td class="p-3 text-right font-mono text-sm">${(val['gate_4_valuation']['sotp_foa_core_m'] + val['gate_4_valuation']['sotp_whatsapp_biz_m'] + val['gate_4_valuation']['sotp_reality_labs_drag_m'] + val['gate_1_forensic_normalization']['net_cash_total']):,.1f}M</td>
                                <td class="p-3 text-right font-mono text-sm">${val['gate_4_valuation']['sotp_intrinsic_value_usd']:.2f}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: 10-YR DCF SCHEDULE -->
        <div id="tab-dcf" class="tab-content space-y-6 hidden">
            <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            10-Year Pro-Forma Ginzu DCF Schedule
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Reinvestment parameterized via Sales-to-Capital = 1.45 | Terminal ROIC = 20.0% Moat Override</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono">
                        DCF INTRINSIC VALUE: ${val['gate_4_valuation']['dcf_intrinsic_value_usd']:.2f}
                    </span>
                </div>

                <div class="overflow-x-auto border border-neutral-800">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-2.5">Year</th>
                                <th class="p-2.5 text-right">Revenue ($M)</th>
                                <th class="p-2.5 text-right">Growth</th>
                                <th class="p-2.5 text-right">EBIT Margin</th>
                                <th class="p-2.5 text-right">NOPAT ($M)</th>
                                <th class="p-2.5 text-right">Reinvestment</th>
                                <th class="p-2.5 text-right">FCFF ($M)</th>
                                <th class="p-2.5 text-right">WACC</th>
                                <th class="p-2.5 text-right">PV of FCFF</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="p-2.5 font-bold text-neutral-400">Base (Yr 0)</td>
                                <td class="p-2.5 text-right font-mono">$200,966M</td>
                                <td class="p-2.5 text-right font-mono">+22.2%</td>
                                <td class="p-2.5 text-right font-mono">50.8% (norm)</td>
                                <td class="p-2.5 text-right font-mono">${val['gate_1_forensic_normalization']['normalized_nopat_0']:,.0f}M</td>
                                <td class="p-2.5 text-right font-mono">-</td>
                                <td class="p-2.5 text-right font-mono">-</td>
                                <td class="p-2.5 text-right font-mono">-</td>
                                <td class="p-2.5 text-right font-mono">-</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-neutral-300">Year 1</td>
                                <td class="p-2.5 text-right font-mono">$233,121M</td>
                                <td class="p-2.5 text-right text-emerald-400 font-mono">16.0%</td>
                                <td class="p-2.5 text-right font-mono">48.0%</td>
                                <td class="p-2.5 text-right font-mono">$91,750M</td>
                                <td class="p-2.5 text-right font-mono">$22,176M</td>
                                <td class="p-2.5 text-right font-mono text-emerald-400">$69,574M</td>
                                <td class="p-2.5 text-right font-mono">9.08%</td>
                                <td class="p-2.5 text-right font-mono font-bold">$63,783M</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-neutral-300">Year 2</td>
                                <td class="p-2.5 text-right font-mono">$266,923M</td>
                                <td class="p-2.5 text-right text-emerald-400 font-mono">14.5%</td>
                                <td class="p-2.5 text-right font-mono">47.5%</td>
                                <td class="p-2.5 text-right font-mono">$103,967M</td>
                                <td class="p-2.5 text-right font-mono">$23,312M</td>
                                <td class="p-2.5 text-right font-mono text-emerald-400">$80,655M</td>
                                <td class="p-2.5 text-right font-mono">9.07%</td>
                                <td class="p-2.5 text-right font-mono font-bold">$67,800M</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-neutral-300">Year 3</td>
                                <td class="p-2.5 text-right font-mono">$301,623M</td>
                                <td class="p-2.5 text-right text-emerald-400 font-mono">13.0%</td>
                                <td class="p-2.5 text-right font-mono">47.0%</td>
                                <td class="p-2.5 text-right font-mono">$116,245M</td>
                                <td class="p-2.5 text-right font-mono">$23,931M</td>
                                <td class="p-2.5 text-right font-mono text-emerald-400">$92,314M</td>
                                <td class="p-2.5 text-right font-mono">9.06%</td>
                                <td class="p-2.5 text-right font-mono font-bold">$71,152M</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-neutral-300">Year 4</td>
                                <td class="p-2.5 text-right font-mono">$334,802M</td>
                                <td class="p-2.5 text-right text-emerald-400 font-mono">11.0%</td>
                                <td class="p-2.5 text-right font-mono">46.0%</td>
                                <td class="p-2.5 text-right font-mono">$126,288M</td>
                                <td class="p-2.5 text-right font-mono">$22,882M</td>
                                <td class="p-2.5 text-right font-mono text-emerald-400">$103,406M</td>
                                <td class="p-2.5 text-right font-mono">9.05%</td>
                                <td class="p-2.5 text-right font-mono font-bold">$73,083M</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-neutral-300">Year 5</td>
                                <td class="p-2.5 text-right font-mono">$366,608M</td>
                                <td class="p-2.5 text-right text-emerald-400 font-mono">9.5%</td>
                                <td class="p-2.5 text-right font-mono">45.0%</td>
                                <td class="p-2.5 text-right font-mono">$135,278M</td>
                                <td class="p-2.5 text-right font-mono">$21,935M</td>
                                <td class="p-2.5 text-right font-mono text-emerald-400">$113,343M</td>
                                <td class="p-2.5 text-right font-mono">9.04%</td>
                                <td class="p-2.5 text-right font-mono font-bold">$73,430M</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 text-neutral-300">Year 6-10 (Fade)</td>
                                <td class="p-2.5 text-right font-mono">$482,967M (Y10)</td>
                                <td class="p-2.5 text-right text-neutral-400 font-mono">8.0% -> 3.5%</td>
                                <td class="p-2.5 text-right font-mono">44.0% -> 42.0%</td>
                                <td class="p-2.5 text-right font-mono">$166,334M (Y10)</td>
                                <td class="p-2.5 text-right font-mono">$11,263M (Y10)</td>
                                <td class="p-2.5 text-right font-mono text-emerald-400">$155,070M (Y10)</td>
                                <td class="p-2.5 text-right font-mono">9.00%</td>
                                <td class="p-2.5 text-right font-mono font-bold">$350,070M (Cum)</td>
                            </tr>
                            <tr class="bg-neutral-900/60 font-bold border-t border-neutral-700">
                                <td class="p-2.5 font-serif text-amber-300">PV of 10-Yr Discrete FCFF</td>
                                <td colspan="7" class="p-2.5 text-right text-neutral-400">Sum of 10 discrete projected discounted free cash flows</td>
                                <td class="p-2.5 text-right text-amber-400 font-mono font-bold text-sm">${val['gate_4_valuation']['dcf_pv_discrete_fcff_m']:,.1f}M</td>
                            </tr>
                            <tr class="bg-neutral-900/80 font-bold">
                                <td class="p-2.5 font-serif text-amber-300">Terminal Value (Moat ROIC=20%)</td>
                                <td colspan="7" class="p-2.5 text-right text-neutral-400">g = 3.50% | Reinvestment Rate = 3.5%/20% = 17.5% | Year 10 TV: $2,582,331M</td>
                                <td class="p-2.5 text-right text-amber-400 font-mono font-bold text-sm">${val['gate_4_valuation']['dcf_pv_terminal_val_m']:,.1f}M</td>
                            </tr>
                            <tr class="bg-amber-950/20 font-bold text-neutral-100 border-t-2 border-amber-500">
                                <td class="p-2.5 font-serif text-sm">DCF Equity Fair Value</td>
                                <td colspan="7" class="p-2.5 text-right text-neutral-300">Enterprise Value ($1,790,123M) + Net Cash ($25,219M)</td>
                                <td class="p-2.5 text-right text-emerald-400 font-mono text-sm font-bold">${(val['gate_4_valuation']['dcf_pv_discrete_fcff_m'] + val['gate_4_valuation']['dcf_pv_terminal_val_m'] + val['gate_1_forensic_normalization']['net_cash_total']):,.1f}M</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 4: SCENARIOS & MONTE CARLO -->
        <div id="tab-scenarios" class="tab-content space-y-6 hidden">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Monte Carlo Block -->
                <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                    <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            10,000-Trial Monte Carlo Engine
                        </h3>
                        <span class="px-2 py-0.5 bg-emerald-950/40 border border-emerald-800 text-emerald-400 font-mono text-[11px] font-bold">
                            WIN RATE: {val['gate_4_valuation']['monte_carlo_10k']['win_rate_pct']:.1f}%
                        </span>
                    </div>

                    <div class="space-y-3">
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <span class="text-neutral-400">Median Expected Value</span>
                            <span class="text-neutral-100 font-bold">${val['gate_4_valuation']['monte_carlo_10k']['median_usd']:.2f}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <span class="text-neutral-400">Mean Expected Value</span>
                            <span class="text-neutral-100 font-bold">${val['gate_4_valuation']['monte_carlo_10k']['mean_usd']:.2f}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <span class="text-neutral-400">10th Percentile (Stress Test Floor)</span>
                            <span class="text-rose-400 font-bold">${val['gate_4_valuation']['monte_carlo_10k']['p10_usd']:.2f}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <span class="text-neutral-400">90th Percentile (AI Bull Case)</span>
                            <span class="text-emerald-400 font-bold">${val['gate_4_valuation']['monte_carlo_10k']['p90_usd']:.2f}</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <span class="text-neutral-400">Net Liquidation Recovery Floor</span>
                            <span class="text-neutral-500 font-bold">${val['gate_4_valuation']['liquidation_haircut_floor_usd']:.2f}</span>
                        </div>
                    </div>
                </div>

                <!-- Forensic Health Audit Block -->
                <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                    <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Gate 2 Financial Distress & Quality Audit
                        </h3>
                        <span class="px-2 py-0.5 bg-emerald-950/40 border border-emerald-800 text-emerald-400 font-mono text-[11px] font-bold">
                            SAFE ZONE
                        </span>
                    </div>

                    <div class="space-y-3">
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <div>
                                <span class="text-neutral-200 block font-bold">Altman Z-Score</span>
                                <span class="text-[10px] text-neutral-500">Benchmark: Safe Zone &gt; 2.99</span>
                            </div>
                            <span class="text-emerald-400 font-bold text-sm font-mono">{diag['altman_z']['z_score']} (Ultra-Safe)</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <div>
                                <span class="text-neutral-200 block font-bold">Piotroski F-Score</span>
                                <span class="text-[10px] text-neutral-500">9 Fundamental Financial Signals</span>
                            </div>
                            <span class="text-emerald-400 font-bold text-sm font-mono">{diag['piotroski_f']['score']}/9 (Flawless)</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <div>
                                <span class="text-neutral-200 block font-bold">Beneish M-Score</span>
                                <span class="text-[10px] text-neutral-500">Benchmark: Non-Manipulator &lt; -1.78</span>
                            </div>
                            <span class="text-emerald-400 font-bold text-sm font-mono">{diag['beneish_m']['score']} (Clean)</span>
                        </div>
                        <div class="flex justify-between items-center py-2 border-b border-neutral-800/60 font-mono text-xs">
                            <div>
                                <span class="text-neutral-200 block font-bold">DuPont 5-Point ROE</span>
                                <span class="text-[10px] text-neutral-500">FY2025 Audited Efficiency</span>
                            </div>
                            <span class="text-neutral-100 font-bold text-sm font-mono">{diag['dupont_5point']['2025']['roe_pct']}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: AI CAPEX & ROI AUDIT (GATE 4B) -->
        <div id="tab-capex" class="tab-content space-y-6 hidden">
            <div class="p-3 bg-amber-950/20 border border-amber-900/60 text-amber-300 flex items-center justify-between text-xs">
                <span>[GATE 4B AUDIT] Meta's physical CapEx surged from $28.1B in FY23 to $37.3B in FY24 and <strong>$69.7B in FY25</strong> (guided to $65B-$72B run-rate). While Llama distributes weights for $0 direct software sales, indirect ad targeting efficiency (+9.5% lift) yields $19.1B gross revenue, falling -$3.8B short of the $19.4B annual hardware depreciation over a 3.5-year GPU useful life. Full justification requires an 18.0% cumulative ad lift ($36.1B/yr).</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-amber-800 px-1.5 py-0.5">CapEx Warning</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Internal Provider Capital Engine -->
                <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                    <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Provider Internal Capital Mechanics
                        </h3>
                        <span class="px-2 py-0.5 bg-neutral-900 border border-neutral-700 text-neutral-300 font-mono text-[11px]">
                            FY2025 AUDITED
                        </span>
                    </div>

                    <div class="space-y-3 font-mono text-xs">
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Physical CapEx Outlay</span>
                            <span class="text-neutral-100 font-bold">${val['gate_4b_ai_capex_roi']['annual_ai_capex_surge_m']:,.1f}M</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">CapEx Intensity (CapEx / Revenue)</span>
                            <span class="text-amber-400 font-bold">{val['gate_4b_ai_capex_roi']['capex_intensity_pct']:.1f}%</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Free Cash Flow Conversion (FCF / CFO)</span>
                            <span class="text-neutral-100 font-bold">{val['gate_4b_ai_capex_roi']['fcf_conversion_pct']:.1f}%</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Annual Hardware Depreciation (3.5-Yr Life)</span>
                            <span class="text-rose-400 font-bold">${val['gate_4b_ai_capex_roi']['annual_hardware_depreciation_m']:,.1f}M/yr</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Shareholder Capital Return (Buybacks + Div)</span>
                            <span class="text-emerald-400 font-bold">${val['gate_4b_ai_capex_roi']['shareholder_total_payout_m']:,.1f}M</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Shareholder Payout Ratio (% of FCF)</span>
                            <span class="text-emerald-400 font-bold">{val['gate_4b_ai_capex_roi']['shareholder_payout_ratio_fcf_pct']:.1f}%</span>
                        </div>
                    </div>
                </div>

                <!-- Customer / Advertiser Payback Engine -->
                <div class="bg-[#0f0f11] border border-neutral-800 p-6 space-y-4">
                    <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            The Open-Source AI Paradox & Payback Deficit
                        </h3>
                        <span class="px-2 py-0.5 bg-rose-950/40 border border-rose-800 text-rose-400 font-mono text-[11px] font-bold">
                            DEFICIT: +{val['gate_4b_ai_capex_roi']['obsolescence_deficit_years']:.2f} YRS
                        </span>
                    </div>

                    <div class="space-y-3 font-mono text-xs">
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Direct Llama Software Revenue</span>
                            <span class="text-neutral-500 font-bold">$0.00 (Open-Source Weights)</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Indirect Ad Conversion Uplift (Advantage+)</span>
                            <span class="text-emerald-400 font-bold">+9.5% base lift</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Incremental Ad Revenue Generated</span>
                            <span class="text-neutral-100 font-bold">${val['gate_4b_ai_capex_roi']['incremental_ad_revenue_base_m']:,.1f}M</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Incremental Ad Gross Profit (82% Margin)</span>
                            <span class="text-neutral-100 font-bold">${val['gate_4b_ai_capex_roi']['incremental_ad_gross_profit_base_m']:,.1f}M</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Net AI Operating Income (after deprec)</span>
                            <span class="text-rose-400 font-bold">${val['gate_4b_ai_capex_roi']['net_ai_operating_income_m']:,.1f}M</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Net AI Operating Return on Investment (ROI)</span>
                            <span class="text-rose-400 font-bold">{val['gate_4b_ai_capex_roi']['net_ai_roi_pct']:.2f}%</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Hardware Payback Period</span>
                            <span class="text-amber-400 font-bold">{val['gate_4b_ai_capex_roi']['payback_years']:.2f} Years (vs 3.5-Yr Life)</span>
                        </div>
                        <div class="flex justify-between py-2 border-b border-neutral-800/60">
                            <span class="text-neutral-400">Required Ad Revenue Lift for 15% ROIC</span>
                            <span class="text-emerald-400 font-bold">${val['gate_4b_ai_capex_roi']['required_break_even_ad_lift_m']:,.1f}M (+{val['gate_4b_ai_capex_roi']['required_break_even_ad_lift_pct']:.1f}%)</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Terminal Footer -->
    <footer class="border-t border-neutral-800 bg-[#0c0d0e] py-4 mt-12 text-center text-[11px] font-mono text-neutral-500">
        ERVIS INSTITUTIONAL TERMINAL v2.5 :: META PLATFORMS, INC. (NASDAQ: META) :: GATES 1-5 + 4B CERTIFIED
    </footer>

    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                btn.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                btn.classList.add('border-transparent', 'text-neutral-400');
            }});

            const targetContent = document.getElementById(tabId);
            if (targetContent) targetContent.classList.remove('hidden');

            const btnId = 'btn-' + tabId;
            const activeBtn = document.getElementById(btnId);
            if (activeBtn) {{
                activeBtn.classList.add('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                activeBtn.classList.remove('border-transparent', 'text-neutral-400');
            }}
        }}
    </script>
</body>
</html>
"""

with open(f"{REPORTS_DIR}/dashboard.html", "w") as f:
    f.write(html_content)

print(f"Successfully generated interactive HTML dashboard at {REPORTS_DIR}/dashboard.html")
