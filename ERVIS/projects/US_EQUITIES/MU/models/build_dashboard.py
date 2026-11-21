import os
import json

def generate_micron_dashboard():
    with open("ERVIS/projects/US_EQUITIES/MU/models/gate4_valuation_outputs.json") as f:
        data = json.load(f)
        
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MU: Micron Technology | ERVIS Institutional Equity Research</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Inter', sans-serif;
      background-color: #FAF7F2;
      color: #1C1917;
    }}
    .font-serif-hdr {{ font-family: 'Newsreader', Georgia, serif; }}
    .font-mono-code {{ font-family: 'JetBrains Mono', monospace; }}
    .border-subtle {{ border-color: #E7E5E4; }}
    .bg-card {{ background-color: #FFFFFF; }}
    .bg-subtle {{ background-color: #F5F2EB; }}
    .text-muted {{ color: #78716C; }}
    .text-emerald-inst {{ color: #15803D; }}
    .text-amber-inst {{ color: #B45309; }}
    .text-crimson-inst {{ color: #B91C1C; }}
    .text-cyan-inst {{ color: #0E7490; }}
    .active-tab {{
      border-bottom: 2px solid #1C1917;
      color: #1C1917;
      font-weight: 600;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-amber-100 selection:text-amber-900">

  <!-- TOP INSTITUTIONAL NAV -->
  <header class="border-b border-subtle bg-[#FAF7F2]/90 backdrop-blur sticky top-0 z-50 px-6 py-3.5 transition-all">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <a href="../../index.html" class="text-xs font-mono-code font-semibold tracking-wider text-stone-600 hover:text-stone-900 transition-colors uppercase">&larr; ERVIS CENTRAL</a>
        <span class="text-stone-300">/</span>
        <span class="text-xs font-mono-code text-stone-500 uppercase tracking-wider">US EQUITIES</span>
        <span class="text-stone-300">/</span>
        <span class="text-xs font-mono-code font-bold text-stone-900 bg-stone-200/80 px-2 py-0.5 rounded">NASDAQ: MU</span>
        <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-mono-code font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-pulse"></span> GATES 1–5 COMPLETED
        </span>
      </div>
      <div class="flex items-center gap-6">
        <div class="text-right">
          <div class="text-[10px] font-mono-code text-stone-500 uppercase">Spot Market Price</div>
          <div class="text-sm font-mono-code font-bold text-stone-900">$594.51 <span class="text-xs text-crimson-inst font-normal">(-52.6% from ATH $1,255)</span></div>
        </div>
        <div class="h-6 w-px bg-stone-300"></div>
        <div class="text-right">
          <div class="text-[10px] font-mono-code text-stone-500 uppercase">DCF Fair Value Anchor</div>
          <div class="text-sm font-mono-code font-bold text-emerald-inst">$604.08 <span class="text-xs text-emerald-inst font-normal">(+1.6%)</span></div>
        </div>
        <div class="h-6 w-px bg-stone-300"></div>
        <div class="text-right">
          <div class="text-[10px] font-mono-code text-stone-500 uppercase">Blended Target Price</div>
          <div class="text-sm font-mono-code font-bold text-amber-inst">$573.32 <span class="text-xs font-normal bg-amber-100 text-amber-800 px-1.5 py-0.5 rounded ml-1">NEUTRAL / HOLD</span></div>
        </div>
      </div>
    </div>
  </header>

  <!-- MAIN CONTENT CONTAINER -->
  <main class="max-w-7xl mx-auto px-6 py-8 flex-1 w-full space-y-8">

    <!-- HERO HEADER -->
    <div class="border-b border-subtle pb-6 flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <div class="text-xs font-mono-code text-amber-700 font-semibold tracking-wider uppercase">Semi Memory Supercycle & AI HBM Valuation Forensic</div>
        <h1 class="text-3xl md:text-4xl font-serif-hdr font-medium text-stone-900 tracking-tight">Micron Technology, Inc.</h1>
        <p class="text-sm text-stone-600 max-w-3xl leading-relaxed">
          Comprehensive 5-Gate equity research valuation covering the post-peak de-rating from $1,255 to $594. Intrinsic fair value is anchored at <strong>$604.08/sh ($683.5B)</strong> under a disciplined mean-reverting margin schedule (74.6% &rarr; 35.0%), backed by an unencumbered <strong>$68.0 Billion Net Cash Fortress ($60.07/sh)</strong> and zero debt vulnerability.
        </p>
      </div>
      <div class="flex items-center gap-3">
        <a href="../models/model.xlsx" download class="inline-flex items-center gap-2 px-3 py-2 rounded border border-stone-300 bg-white hover:bg-stone-50 text-xs font-mono-code font-semibold text-stone-800 shadow-sm transition">
          <svg class="w-4 h-4 text-emerald-700" fill="currentColor" viewBox="0 0 20 20"><path d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"/></svg>
          DOWNLOAD EXCEL MODEL (.XLSX)
        </a>
      </div>
    </div>

    <!-- 6 KPI HERO CARDS -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
      <div class="bg-card p-4 rounded border border-subtle shadow-sm space-y-1">
        <div class="text-[10px] font-mono-code text-stone-500 uppercase tracking-wider">DCF Anchor (Plan A)</div>
        <div class="text-xl font-mono-code font-bold text-stone-900">$604.08</div>
        <div class="text-[11px] font-mono-code text-emerald-inst">+1.6% vs Spot ($594.51)</div>
      </div>
      <div class="bg-card p-4 rounded border border-subtle shadow-sm space-y-1">
        <div class="text-[10px] font-mono-code text-stone-500 uppercase tracking-wider">SOTP Multiple Value</div>
        <div class="text-xl font-mono-code font-bold text-stone-900">$501.54</div>
        <div class="text-[11px] font-mono-code text-stone-500">-15.6% (Conservative Haircut)</div>
      </div>
      <div class="bg-card p-4 rounded border border-subtle shadow-sm space-y-1">
        <div class="text-[10px] font-mono-code text-stone-500 uppercase tracking-wider">Net Cash Reserves</div>
        <div class="text-xl font-mono-code font-bold text-stone-900">+$68.0B</div>
        <div class="text-[11px] font-mono-code text-emerald-inst">$60.07/sh pure cash backing</div>
      </div>
      <div class="bg-card p-4 rounded border border-subtle shadow-sm space-y-1">
        <div class="text-[10px] font-mono-code text-stone-500 uppercase tracking-wider">FY26 Audited EBIT</div>
        <div class="text-xl font-mono-code font-bold text-stone-900">$99.34B</div>
        <div class="text-[11px] font-mono-code text-amber-inst">74.6% Peak Operating Margin</div>
      </div>
      <div class="bg-card p-4 rounded border border-subtle shadow-sm space-y-1">
        <div class="text-[10px] font-mono-code text-stone-500 uppercase tracking-wider">10-Yr Undisc. FCFF</div>
        <div class="text-xl font-mono-code font-bold text-stone-900">$524.3B</div>
        <div class="text-[11px] font-mono-code text-stone-500">$339.5B Discounted PV</div>
      </div>
      <div class="bg-card p-4 rounded border border-subtle shadow-sm space-y-1">
        <div class="text-[10px] font-mono-code text-stone-500 uppercase tracking-wider">Altman Z-Score</div>
        <div class="text-xl font-mono-code font-bold text-emerald-inst">10.70</div>
        <div class="text-[11px] font-mono-code text-emerald-inst">Safe Zone (>2.99 Safe)</div>
      </div>
    </div>

    <!-- INTERACTIVE SECTION TABS -->
    <div class="border-b border-subtle flex gap-6 text-xs font-mono-code uppercase tracking-wider text-stone-500 overflow-x-auto pb-px">
      <button onclick="switchTab('tab-thesis')" id="btn-tab-thesis" class="pb-3 active-tab">01. Variant Thesis & Triangulation</button>
      <button onclick="switchTab('tab-dcf')" id="btn-tab-dcf" class="pb-3 hover:text-stone-900 transition">02. 10-Yr Pro-Forma DCF</button>
      <button onclick="switchTab('tab-dupont')" id="btn-tab-dupont" class="pb-3 hover:text-stone-900 transition">03. DuPont 5-Point ROE</button>
      <button onclick="switchTab('tab-sotp')" id="btn-tab-sotp" class="pb-3 hover:text-stone-900 transition">04. SOTP Divisional Mix</button>
      <button onclick="switchTab('tab-mc')" id="btn-tab-mc" class="pb-3 hover:text-stone-900 transition">05. Monte Carlo Simulation</button>
      <button onclick="switchTab('tab-audit')" id="btn-tab-audit" class="pb-3 hover:text-stone-900 transition">06. Forensic Accounting Audit</button>
    </div>

    <!-- TAB 1: VARIANT THESIS & TRIANGULATION -->
    <div id="tab-thesis" class="space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-card p-6 rounded border border-subtle shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-subtle pb-3">
            <h2 class="text-lg font-serif-hdr font-medium text-stone-900">Executive Variant View: The $1,255 Peak De-Rating vs. Fundamental Reality</h2>
            <span class="text-xs font-mono-code text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">RESEARCH MEMO</span>
          </div>
          <div class="text-sm text-stone-700 leading-relaxed space-y-3">
            <p>
              <strong>1. The Downwind Narrative Purged Euphoria, Not Intrinsic Value:</strong> Micron’s severe stock retreat from its all-time peak of $1,255 down to $594.51 is a classic mid-cycle multiple de-rating. The market had previously priced Micron as if its extraordinary 74.6% operating margin and 256% revenue growth were permanent monopolistic features. Our Damodaran forensic model proves that even after aggressively degrading operating margins from 74.6% down to a normalized <strong>35.0% oligopoly baseline</strong>, intrinsic fair value holds firmly at <strong>$604.08</strong>.
            </p>
            <p>
              <strong>2. The $68.0B Net Cash Floor:</strong> Micron is not the debt-laden memory commoditizer of the 2008 or 2019 downturns. Across FY2025–FY2026, Micron generated over $60B in cumulative free cash flow, accumulating <strong>$73.45 Billion in liquid cash and marketable securities</strong> against only $5.49B in total debt and lease claims. Net cash represents <strong>$60.07 per share (10.1% of spot price)</strong>.
            </p>
            <p>
              <strong>3. High-Bandwidth Memory (HBM) Structural Moat:</strong> Memory consolidation has reduced global DRAM to three players (Samsung, SK Hynix, Micron). High-Bandwidth Memory (HBM3E / HBM4) is not a commodity chip bought on spot markets; it requires deep 18-month TSMC CoWoS advanced packaging qualification and custom base die co-design with Nvidia, Broadcom, and AMD. Micron’s capacity is 100% committed through calendar 2026.
            </p>
          </div>
        </div>

        <!-- TRIANGULATION TABLE -->
        <div class="bg-card p-6 rounded border border-subtle shadow-sm space-y-4">
          <div class="border-b border-subtle pb-3">
            <h2 class="text-lg font-serif-hdr font-medium text-stone-900">Valuation Triangulation</h2>
            <div class="text-xs font-mono-code text-stone-500">Dual-Engine Reconciled Outputs</div>
          </div>
          <div class="space-y-3 font-mono-code text-xs">
            <div class="flex justify-between items-center py-2 border-b border-stone-100">
              <span class="text-stone-600 font-medium">1. Base DCF (Plan A)</span>
              <span class="font-bold text-stone-900">$604.08 <span class="text-emerald-inst text-[11px]">(+1.6%)</span></span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-stone-100">
              <span class="text-stone-600 font-medium">2. SOTP Multiple Value</span>
              <span class="font-bold text-stone-900">$501.54 <span class="text-stone-500 text-[11px]">(-15.6%)</span></span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-stone-100">
              <span class="text-stone-600 font-medium">3. Monte Carlo Median (P50)</span>
              <span class="font-bold text-stone-900">$590.70 <span class="text-stone-500 text-[11px]">(-0.6%)</span></span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-stone-100">
              <span class="text-stone-600 font-medium">4. Monte Carlo Bull (P90)</span>
              <span class="font-bold text-stone-900">$860.25 <span class="text-emerald-inst text-[11px]">(+44.7%)</span></span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-stone-100">
              <span class="text-stone-600 font-medium">5. Monte Carlo Bear (P10)</span>
              <span class="font-bold text-stone-900">$426.70 <span class="text-crimson-inst text-[11px]">(-28.2%)</span></span>
            </div>
            <div class="flex justify-between items-center py-2">
              <span class="text-stone-600 font-medium">6. Liquidation Haircut Floor</span>
              <span class="font-bold text-stone-900">$58.68 <span class="text-crimson-inst text-[11px]">(-90.1%)</span></span>
            </div>
          </div>
          <div class="p-3 bg-subtle rounded border border-subtle text-xs space-y-1">
            <div class="font-bold text-stone-900">Blended Target Price: $573.32</div>
            <div class="text-stone-600">70% Weight on DCF ($604.08) + 30% Weight on SOTP ($501.54). Rating: <strong>NEUTRAL / HOLD</strong>.</div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: 10-YEAR PRO-FORMA DCF -->
    <div id="tab-dcf" class="hidden space-y-6">
      <div class="bg-card p-6 rounded border border-subtle shadow-sm space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-subtle pb-4">
          <div>
            <h2 class="text-lg font-serif-hdr font-medium text-stone-900">Plan A: Mean-Reverting Margin & FCFF Generation Trajectory</h2>
            <div class="text-xs font-mono-code text-stone-500">Operating margin step-down from peak 74.6% to sustainable 35.0% oligopoly baseline</div>
          </div>
          <div class="flex items-center gap-4 text-xs font-mono-code">
            <span class="inline-flex items-center gap-1.5"><span class="w-3 h-3 bg-amber-600 rounded-sm"></span> Revenue ($B)</span>
            <span class="inline-flex items-center gap-1.5"><span class="w-3 h-3 bg-emerald-700 rounded-sm"></span> FCFF Cash Flow ($B)</span>
            <span class="inline-flex items-center gap-1.5"><span class="w-3 h-0.5 bg-stone-900"></span> Operating Margin %</span>
          </div>
        </div>
        <div class="h-80 w-full">
          <canvas id="dcfChart"></canvas>
        </div>
      </div>

      <!-- PRO-FORMA TABLE -->
      <div class="bg-card p-6 rounded border border-subtle shadow-sm space-y-4 overflow-x-auto">
        <h3 class="text-sm font-mono-code font-bold uppercase tracking-wider text-stone-900">10-Year Discrete Pro-Forma Schedule (FY2027 – FY2036)</h3>
        <table class="w-full text-xs font-mono-code text-left border-collapse">
          <thead>
            <tr class="bg-stone-100 text-stone-700 border-b border-stone-200">
              <th class="p-2.5">Year</th>
              <th class="p-2.5">Period</th>
              <th class="p-2.5 text-right">Revenue ($M)</th>
              <th class="p-2.5 text-right">Growth %</th>
              <th class="p-2.5 text-right">Margin %</th>
              <th class="p-2.5 text-right">Adjusted EBIT ($M)</th>
              <th class="p-2.5 text-right">NOPAT ($M)</th>
              <th class="p-2.5 text-right">Reinvest ($M)</th>
              <th class="p-2.5 text-right">FCFF ($M)</th>
              <th class="p-2.5 text-right">Disc Factor</th>
              <th class="p-2.5 text-right">PV FCFF ($M)</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-stone-100">
            {"".join([f"""<tr class="hover:bg-stone-50">
              <td class="p-2 font-bold">{row['year']}</td>
              <td class="p-2 text-stone-600">FY{2026 + row['year']}</td>
              <td class="p-2 text-right">${row['rev']:,.1f}</td>
              <td class="p-2 text-right text-stone-600">{row['growth']*100:+.1f}%</td>
              <td class="p-2 text-right font-medium">{row['margin']*100:.1f}%</td>
              <td class="p-2 text-right">${row['ebit']:,.1f}</td>
              <td class="p-2 text-right">${row['nopat']:,.1f}</td>
              <td class="p-2 text-right text-stone-600">${row['reinvest']:,.1f}</td>
              <td class="p-2 text-right font-bold text-emerald-inst">${row['fcff']:,.1f}</td>
              <td class="p-2 text-right text-stone-500">{row['df']:.4f}</td>
              <td class="p-2 text-right font-bold">${row['pv_fcff']:,.1f}</td>
            </tr>""" for row in data['dcf']['table']])}
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 3: DUPONT 5-POINT ROE -->
    <div id="tab-dupont" class="hidden space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-card p-6 rounded border border-subtle shadow-sm space-y-4">
          <div class="border-b border-subtle pb-3">
            <h2 class="text-lg font-serif-hdr font-medium text-stone-900">DuPont 5-Point ROE Decomposition (FY22 – FY26)</h2>
            <div class="text-xs font-mono-code text-stone-500">Deconstructing Operational Efficiency vs Financial Leverage</div>
          </div>
          <div class="h-64">
            <canvas id="dupontChart"></canvas>
          </div>
        </div>

        <div class="bg-card p-6 rounded border border-subtle shadow-sm space-y-4">
          <div class="border-b border-subtle pb-3">
            <h2 class="text-lg font-serif-hdr font-medium text-stone-900">Solvency & Fundamental Health Audit</h2>
            <div class="text-xs font-mono-code text-stone-500">Quantitative Distress & Manipulation Battery</div>
          </div>
          <div class="space-y-4 text-xs font-mono-code">
            <div class="p-3 bg-stone-50 rounded border border-subtle flex justify-between items-center">
              <div>
                <div class="font-bold text-stone-900">Altman Z-Score: 10.70</div>
                <div class="text-[11px] text-stone-500">Benchmark: >2.99 Safe Zone</div>
              </div>
              <span class="px-2 py-1 bg-emerald-100 text-emerald-800 rounded font-bold">EXTREMELY SAFE</span>
            </div>
            <div class="p-3 bg-stone-50 rounded border border-subtle flex justify-between items-center">
              <div>
                <div class="font-bold text-stone-900">Piotroski F-Score: 9 / 9</div>
                <div class="text-[11px] text-stone-500">Benchmark: >=8 Highest Quality</div>
              </div>
              <span class="px-2 py-1 bg-emerald-100 text-emerald-800 rounded font-bold">FLAWLESS QUALITY</span>
            </div>
            <div class="p-3 bg-stone-50 rounded border border-subtle flex justify-between items-center">
              <div>
                <div class="font-bold text-stone-900">Beneish M-Score: -2.48</div>
                <div class="text-[11px] text-stone-500">Benchmark: <-1.78 Unmanipulated</div>
              </div>
              <span class="px-2 py-1 bg-emerald-100 text-emerald-800 rounded font-bold">NEGATIVE ACCRUALS</span>
            </div>
            <div class="p-3 bg-stone-50 rounded border border-subtle flex justify-between items-center">
              <div>
                <div class="font-bold text-stone-900">Interest Coverage: 952.8x</div>
                <div class="text-[11px] text-stone-500">Net interest income positive (+$978M)</div>
              </div>
              <span class="px-2 py-1 bg-emerald-100 text-emerald-800 rounded font-bold">AAA SYNTHETIC</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: SOTP DIVISIONAL MIX -->
    <div id="tab-sotp" class="hidden space-y-6">
      <div class="bg-card p-6 rounded border border-subtle shadow-sm space-y-4">
        <div class="border-b border-subtle pb-3">
          <h2 class="text-lg font-serif-hdr font-medium text-stone-900">Sum-of-the-Parts (SOTP) Divisional Multiple Valuation</h2>
          <div class="text-xs font-mono-code text-stone-500">Applying a 40% forward normalization haircut to peak FY26 divisional EBITDA</div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2">
          <div class="p-4 bg-stone-50 rounded border border-subtle space-y-2">
            <div class="text-xs font-mono-code text-amber-700 font-bold uppercase">CNBU (Compute & Networking)</div>
            <div class="text-lg font-mono-code font-bold text-stone-900">${data['sotp']['cnbu_ev_b']}B EV</div>
            <div class="text-xs text-stone-600 leading-tight">Server DRAM, HBM3E, HBM4. Peer multiple 8.5x normalized EBITDA ($43.1B).</div>
          </div>
          <div class="p-4 bg-stone-50 rounded border border-subtle space-y-2">
            <div class="text-xs font-mono-code text-stone-600 font-bold uppercase">MBU (Mobile Business Unit)</div>
            <div class="text-lg font-mono-code font-bold text-stone-900">${data['sotp']['mbu_ev_b']}B EV</div>
            <div class="text-xs text-stone-600 leading-tight">Smartphone LPDDR5X & mobile NAND. Peer multiple 6.5x normalized EBITDA ($9.6B).</div>
          </div>
          <div class="p-4 bg-stone-50 rounded border border-subtle space-y-2">
            <div class="text-xs font-mono-code text-stone-600 font-bold uppercase">SBU (Storage Business Unit)</div>
            <div class="text-lg font-mono-code font-bold text-stone-900">${data['sotp']['sbu_ev_b']}B EV</div>
            <div class="text-xs text-stone-600 leading-tight">Enterprise & client SSDs / 3D NAND flash. Peer multiple 5.5x normalized EBITDA ($6.9B).</div>
          </div>
          <div class="p-4 bg-stone-50 rounded border border-subtle space-y-2">
            <div class="text-xs font-mono-code text-stone-600 font-bold uppercase">EBU (Embedded Business Unit)</div>
            <div class="text-lg font-mono-code font-bold text-stone-900">${data['sotp']['ebu_ev_b']}B EV</div>
            <div class="text-xs text-stone-600 leading-tight">Automotive & industrial memory solutions. Peer multiple 7.5x normalized EBITDA ($4.4B).</div>
          </div>
        </div>
        <div class="p-4 bg-subtle rounded border border-subtle flex flex-wrap justify-between items-center gap-4 text-xs font-mono-code font-bold">
          <div>Total SOTP Operating EV: ${data['sotp']['total_ev_b']}B</div>
          <div>+ Net Cash on Balance Sheet: +$68.0B</div>
          <div>= SOTP Implied Equity Value: ${data['sotp']['equity_value_b']}B</div>
          <div class="text-amber-inst text-sm">SOTP Value Per Share: ${data['sotp']['per_share']} USD</div>
        </div>
      </div>
    </div>

    <!-- TAB 5: MONTE CARLO SIMULATION -->
    <div id="tab-mc" class="hidden space-y-6">
      <div class="bg-card p-6 rounded border border-subtle shadow-sm space-y-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-subtle pb-3">
          <div>
            <h2 class="text-lg font-serif-hdr font-medium text-stone-900">10,000-Trial Monte Carlo Stochastic Valuation Engine</h2>
            <div class="text-xs font-mono-code text-stone-500">Stochastic simulation across WACC (&plusmn;75 bps), Terminal Growth (&plusmn;50 bps), and Terminal Margin (&plusmn;400 bps)</div>
          </div>
          <div class="text-right">
            <div class="text-xs font-mono-code text-stone-500">Win Rate (> $594.51 Spot)</div>
            <div class="text-lg font-mono-code font-bold text-amber-inst">{data['monte_carlo']['win_rate_pct']}%</div>
          </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 py-2">
          <div class="p-3 bg-stone-50 rounded border border-subtle text-center">
            <div class="text-[10px] font-mono-code text-stone-500 uppercase">P10 Downside</div>
            <div class="text-xl font-mono-code font-bold text-crimson-inst">${data['monte_carlo']['p10']}</div>
          </div>
          <div class="p-3 bg-stone-50 rounded border border-subtle text-center">
            <div class="text-[10px] font-mono-code text-stone-500 uppercase">P50 Median</div>
            <div class="text-xl font-mono-code font-bold text-stone-900">${data['monte_carlo']['p50_median']}</div>
          </div>
          <div class="p-3 bg-stone-50 rounded border border-subtle text-center">
            <div class="text-[10px] font-mono-code text-stone-500 uppercase">Mean Fair Value</div>
            <div class="text-xl font-mono-code font-bold text-emerald-inst">${data['monte_carlo']['mean']}</div>
          </div>
          <div class="p-3 bg-stone-50 rounded border border-subtle text-center">
            <div class="text-[10px] font-mono-code text-stone-500 uppercase">P90 Bull Peak</div>
            <div class="text-xl font-mono-code font-bold text-emerald-inst">${data['monte_carlo']['p90']}</div>
          </div>
        </div>
        <div class="p-4 bg-stone-50 rounded border border-subtle text-xs text-stone-700 leading-relaxed">
          <strong>Institutional Interpretation:</strong> With a 49.1% empirical win rate against the $594.51 spot price and a median of $590.70, Micron is pricing in virtually zero sentimental premium or discount. The distribution proves that the market's downwind from $1,255 has settled squarely at the mathematical center of gravity of the business cycle.
        </div>
      </div>
    </div>

    <!-- TAB 6: FORENSIC ACCOUNTING AUDIT -->
    <div id="tab-audit" class="hidden space-y-6">
      <div class="bg-card p-6 rounded border border-subtle shadow-sm space-y-4">
        <div class="border-b border-subtle pb-3">
          <h2 class="text-lg font-serif-hdr font-medium text-stone-900">Gate 1–3 Forensic Accounting & Normalization Registry</h2>
          <div class="text-xs font-mono-code text-stone-500">Audited 10-K Reconciliation & Capitalization Mechanics</div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs font-mono-code">
          <div class="p-4 bg-stone-50 rounded border border-subtle space-y-2">
            <div class="font-bold text-stone-900 uppercase">1. R&D Capitalization Schedule (4-Year Straight Line)</div>
            <p class="text-stone-600">FY26 R&D ($5,650M) capitalized creating a <strong>$6,994.0M Research Asset</strong>. Amortization is $3,998.0M, generating an EBIT restatement adjustment of +$1,652.0M ($\text{{Adjusted EBIT}}_0 = \$100,992.0\text{{M}}$).</p>
          </div>
          <div class="p-4 bg-stone-50 rounded border border-subtle space-y-2">
            <div class="font-bold text-stone-900 uppercase">2. Off-Balance Sheet Synthetic Lease Debt</div>
            <p class="text-stone-600">Reported debt includes $2,387M capital lease liabilities. Additional operating lease commitments discounted at 5.54% pre-tax $K_d$ yield <strong>$310.0M synthetic debt</strong> (Total adjusted debt = $5,489.0M vs $73,453M cash).</p>
          </div>
          <div class="p-4 bg-stone-50 rounded border border-subtle space-y-2">
            <div class="font-bold text-stone-900 uppercase">3. Hamada Beta Re-Levering Engine</div>
            <p class="text-stone-600">Semiconductor memory unlevered beta $\beta_U = 1.210$. Re-levered via Hamada with $D/E = 0.00816$ and $t = 14.81\%$ yields $\beta_L = \mathbf{{1.218}}$. Cost of equity $K_e = 4.94\% + (1.218 \times 4.61\%) = \mathbf{{10.56\%}}$.</p>
          </div>
          <div class="p-4 bg-stone-50 rounded border border-subtle space-y-2">
            <div class="font-bold text-stone-900 uppercase">4. Moody's Synthetic Credit Profile</div>
            <p class="text-stone-600">All 6 industrial factors evaluate to <strong>Aaa/AAA</strong> (Interest coverage 952.8x, Debt/EBITDA 0.05x). Cyclical industry cap applied at Baa1 (135 bps). Debt weighting is 0.81%, giving WACC = <strong>10.51%</strong>.</p>
          </div>
        </div>
      </div>
    </div>

  </main>

  <!-- FOOTER -->
  <footer class="border-t border-subtle bg-white py-6 px-6 text-center text-xs font-mono-code text-stone-500">
    ERVIS: Equity Research & Valuation Investment System &bull; Micron Technology, Inc. (NASDAQ: MU) Coverage Dossier &bull; Damodaran Ginzu & NUS CFA Champion Pipeline
  </footer>

  <script>
    function switchTab(tabId) {{
      const tabs = ['tab-thesis', 'tab-dcf', 'tab-dupont', 'tab-sotp', 'tab-mc', 'tab-audit'];
      tabs.forEach(t => {{
        const el = document.getElementById(t);
        const btn = document.getElementById('btn-' + t);
        if (t === tabId) {{
          el.classList.remove('hidden');
          btn.classList.add('active-tab');
          btn.classList.remove('text-stone-500');
        }} else {{
          el.classList.add('hidden');
          btn.classList.remove('active-tab');
          btn.classList.add('text-stone-500');
        }}
      }});
    }}

    // Chart.js: DCF Trajectory
    const ctxDcf = document.getElementById('dcfChart').getContext('2d');
    new Chart(ctxDcf, {{
      type: 'bar',
      data: {{
        labels: ['FY26', 'FY27', 'FY28', 'FY29', 'FY30', 'FY31', 'FY32', 'FY33', 'FY34', 'FY35', 'FY36'],
        datasets: [
          {{
            type: 'line',
            label: 'Operating Margin %',
            data: [74.6, 70.0, 60.0, 50.0, 42.0, 38.0, 35.0, 35.0, 35.0, 35.0, 35.0],
            borderColor: '#1C1917',
            borderWidth: 2,
            pointBackgroundColor: '#1C1917',
            yAxisID: 'y1'
          }},
          {{
            type: 'bar',
            label: 'Revenue ($B)',
            data: [133.2, 143.8, 149.6, 149.6, 142.1, 145.0, 150.8, 156.8, 161.5, 166.3, 171.3],
            backgroundColor: '#D97706',
            borderRadius: 3,
            yAxisID: 'y'
          }},
          {{
            type: 'bar',
            label: 'FCFF Cash Flow ($B)',
            data: [59.0, 80.2, 72.6, 62.2, 49.2, 43.7, 40.1, 41.4, 42.9, 43.8, 45.1],
            backgroundColor: '#15803D',
            borderRadius: 3,
            yAxisID: 'y'
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        scales: {{
          y: {{
            beginAtZero: true,
            title: {{ display: true, text: 'USD Billions ($B)' }}
          }},
          y1: {{
            position: 'right',
            min: 0,
            max: 100,
            grid: {{ drawOnChartArea: false }},
            ticks: {{ callback: function(val) {{ return val + '%'; }} }}
          }}
        }}
      }}
    }});

    // Chart.js: DuPont
    const ctxDupont = document.getElementById('dupontChart').getContext('2d');
    new Chart(ctxDupont, {{
      type: 'line',
      data: {{
        labels: ['FY2022', 'FY2023', 'FY2024', 'FY2025', 'FY2026'],
        datasets: [
          {{
            label: 'ROE %',
            data: [17.7, -13.5, 1.8, 16.4, 61.4],
            borderColor: '#15803D',
            backgroundColor: 'rgba(21, 128, 61, 0.1)',
            fill: true,
            tension: 0.2
          }},
          {{
            label: 'Operating Margin %',
            data: [31.5, -34.8, 5.2, 26.1, 74.6],
            borderColor: '#D97706',
            borderDash: [5, 5],
            tension: 0.2
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        scales: {{
          y: {{
            ticks: {{ callback: function(val) {{ return val + '%'; }} }}
          }}
        }}
      }}
    }});
  </script>
</body>
</html>
"""
    # Write to local project report
    local_path = "ERVIS/projects/US_EQUITIES/MU/reports/dashboard.html"
    with open(local_path, "w") as f:
        f.write(html)
    print(f"Generated dashboard at {local_path}")
    
    # Write to ervis-terminal deployment
    deploy_dir = "/Users/worldofmadness/Documents/VS Code/Personal Projects/ervis-terminal/equities/micron"
    os.makedirs(deploy_dir, exist_ok=True)
    deploy_path = os.path.join(deploy_dir, "index.html")
    with open(deploy_path, "w") as f:
        f.write(html)
    print(f"Generated deployment dashboard at {deploy_path}")

if __name__ == "__main__":
    generate_micron_dashboard()
