import os
import sqlite3
import json

# Connect to database with URI mode
db_path = os.path.abspath("ERVIS/vault/ervis_vault.db")
conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cur = conn.cursor()

# Exact Pre-extracted DCF Schedule from AnthropicIPO_updated.xlsx
dcf_years = [
    {"label": "Base Year", "growth": None, "revenues": 35286.0, "margin": -1.3125, "ebit": -46314.2, "tax_rate": 0.0, "ebit_after_tax": -46314.2, "reinvestment": None, "fcff": None, "wacc": None, "cum_discount": None, "pv_fcff": None, "invested_capital": 546819.8, "roic": -0.0847},
    {"label": "Year 1", "growth": 1.90, "revenues": 102329.4, "margin": 0.05, "ebit": 5116.5, "tax_rate": 0.0, "ebit_after_tax": 5116.5, "reinvestment": 14326.1, "fcff": -9209.6, "wacc": 0.0974, "cum_discount": 0.9112, "pv_fcff": -8392.2, "invested_capital": 561145.9, "roic": 0.0094},
    {"label": "Year 2", "growth": 0.42, "revenues": 145307.7, "margin": 0.14, "ebit": 20343.1, "tax_rate": 0.0, "ebit_after_tax": 20343.1, "reinvestment": 20343.1, "fcff": 0.0, "wacc": 0.0974, "cum_discount": 0.8304, "pv_fcff": 0.0, "invested_capital": 581489.0, "roic": 0.0363},
    {"label": "Year 3", "growth": 0.42, "revenues": 206337.0, "margin": 0.185, "ebit": 38172.3, "tax_rate": 0.0, "ebit_after_tax": 38172.3, "reinvestment": 28887.2, "fcff": 9285.2, "wacc": 0.0974, "cum_discount": 0.7567, "pv_fcff": 7025.8, "invested_capital": 610376.2, "roic": 0.0656},
    {"label": "Year 4", "growth": 0.42, "revenues": 292998.5, "margin": 0.23, "ebit": 67389.7, "tax_rate": 0.0, "ebit_after_tax": 67389.7, "reinvestment": 41019.8, "fcff": 26369.9, "wacc": 0.0974, "cum_discount": 0.6895, "pv_fcff": 18182.3, "invested_capital": 651396.0, "roic": 0.1104},
    {"label": "Year 5", "growth": 0.42, "revenues": 416057.9, "margin": 0.275, "ebit": 114415.9, "tax_rate": 0.0, "ebit_after_tax": 114415.9, "reinvestment": 47957.6, "fcff": 66458.3, "wacc": 0.0974, "cum_discount": 0.6283, "pv_fcff": 41756.5, "invested_capital": 699353.6, "roic": 0.1756},
    {"label": "Year 6", "growth": 0.3458, "revenues": 559930.8, "margin": 0.275, "ebit": 153981.0, "tax_rate": 0.05, "ebit_after_tax": 146281.9, "reinvestment": 50692.4, "fcff": 95589.5, "wacc": 0.0962, "cum_discount": 0.5732, "pv_fcff": 54790.3, "invested_capital": 750046.0, "roic": 0.2092},
    {"label": "Year 7", "growth": 0.2716, "revenues": 712008.0, "margin": 0.275, "ebit": 195802.2, "tax_rate": 0.10, "ebit_after_tax": 176222.0, "reinvestment": 46850.1, "fcff": 129371.8, "wacc": 0.0950, "cum_discount": 0.5235, "pv_fcff": 67722.8, "invested_capital": 796896.1, "roic": 0.2349},
    {"label": "Year 8", "growth": 0.1974, "revenues": 852558.3, "margin": 0.275, "ebit": 234453.5, "tax_rate": 0.15, "ebit_after_tax": 199285.5, "reinvestment": 35011.7, "fcff": 164273.8, "wacc": 0.0937, "cum_discount": 0.4786, "pv_fcff": 78622.9, "invested_capital": 831907.8, "roic": 0.2501},
    {"label": "Year 9", "growth": 0.1232, "revenues": 957593.5, "margin": 0.275, "ebit": 263338.2, "tax_rate": 0.20, "ebit_after_tax": 210670.6, "reinvestment": 15640.7, "fcff": 195029.9, "wacc": 0.0925, "cum_discount": 0.4381, "pv_fcff": 85438.3, "invested_capital": 847548.5, "roic": 0.2532},
    {"label": "Year 10", "growth": 0.0490, "revenues": 1004515.6, "margin": 0.275, "ebit": 276241.8, "tax_rate": 0.25, "ebit_after_tax": 207181.3, "reinvestment": 16407.1, "fcff": 190774.3, "wacc": 0.0913, "cum_discount": 0.4014, "pv_fcff": 76582.1, "invested_capital": 863955.6, "roic": 0.2444}
]

# Exact Pre-extracted Valuation Bridge
bridge = {
    "pv_cf_10yr": 421728.8,
    "pv_tv": 1388747.6,
    "sum_pv": 1810476.4,
    "prob_failure": 0.10,
    "proceeds_failure": 905238.2,
    "val_operating_assets": 1719952.6,
    "debt": 485319.8,
    "cash": 112389.0,
    "ipo_proceeds": 65000.0,
    "non_operating_assets": 3929.0,
    "val_equity": 1415950.8,
    "options_val": 472.3,
    "val_equity_common": 1415478.5,
    "shares": 16936.82,
    "val_per_share": 83.69,
    "price": 74.00,
    "price_pct_val": 0.8842,
    "terminal_cf": 146337.7,
    "terminal_wacc": 0.0913,
    "terminal_val": 3459520.3
}

# Pre-extracted Lease commitments
lease_rows = [
    {"year": "1", "commitment": 76968.0, "pv": 72418.1},
    {"year": "2", "commitment": 98128.0, "pv": 86869.4},
    {"year": "3", "commitment": 60832.0, "pv": 50669.1},
    {"year": "4", "commitment": 58304.0, "pv": 45692.7},
    {"year": "5", "commitment": 50000.0, "pv": 36868.5},
    {"year": "6 and beyond", "commitment": 124000.0, "pv": 83486.0}
]

total_lease_comm = sum(r['commitment'] for r in lease_rows)
total_lease_pv = sum(r['pv'] for r in lease_rows)

lease_rows_html = ""
for r in lease_rows:
    factor_str = f"{r['pv'] / r['commitment']:.4f}"
    lease_rows_html += f"""<tr>
        <td class="p-3 font-semibold text-white">Year {r['year']}</td>
        <td class="p-3 text-right text-rose-400 font-bold">${r['commitment']:,.1f} M</td>
        <td class="p-3 text-right text-neutral-400">{factor_str}</td>
        <td class="p-3 text-right text-white font-bold">${r['pv']:,.1f} M</td>
        <td class="p-3 text-right text-white font-bold">${r['pv'] / 1000:,.2f} B</td>
        <td class="p-3 text-neutral-400">Hyperscaler Cloud Compute & Cluster Reservation</td>
    </tr>"""

# Pre-extracted R&D Data
rd_rows = [
    {"year": "Current", "expense": 16979.0, "unam_pct": 1.0, "unam_val": 16979.0, "amort": None},
    {"year": "-1", "expense": 12645.0, "unam_pct": 0.6667, "unam_val": 8430.0, "amort": 4215.0},
    {"year": "-2", "expense": 3366.0, "unam_pct": 0.3333, "unam_val": 1122.0, "amort": 1122.0},
    {"year": "-3", "expense": 592.0, "unam_pct": 0.0, "unam_val": 0.0, "amort": 197.3}
]

rd_rows_html = ""
for r in rd_rows:
    amort_str = f"${r['amort']:,.1f} M" if r['amort'] is not None else "-"
    rd_rows_html += f"""<tr>
        <td class="p-3 font-semibold text-white">{r['year']}</td>
        <td class="p-3 text-right text-emerald-400 font-bold">${r['expense']:,.1f} M</td>
        <td class="p-3 text-right text-neutral-400">{r['unam_pct']*100:.1f}%</td>
        <td class="p-3 text-right text-white font-bold">${r['unam_val']:,.1f} M</td>
        <td class="p-3 text-right text-amber-400 font-bold">{amort_str}</td>
    </tr>"""

# Prebuild DCF row HTML snippets
dcf_header_html = "".join([f'<th class="p-2.5 text-right whitespace-nowrap">{y["label"]}</th>' for y in dcf_years])
dcf_growth_html = "".join([f'<td class="p-2.5 text-right font-mono text-cyan-400">{y["growth"]*100:.1f}%</td>' if y["growth"] is not None else '<td class="p-2.5 text-right font-mono text-neutral-500">-</td>' for y in dcf_years])
dcf_rev_html = "".join([f'<td class="p-2.5 text-right font-mono font-bold text-white">${y["revenues"]:,.0f}</td>' for y in dcf_years])
dcf_margin_html = "".join([f'<td class="p-2.5 text-right font-mono {"text-rose-400" if y["margin"] < 0 else "text-emerald-400"}">{y["margin"]*100:.1f}%</td>' for y in dcf_years])
dcf_ebit_html = "".join([f'<td class="p-2.5 text-right font-mono {"text-rose-400" if y["ebit"] < 0 else "text-white"} font-bold">${y["ebit"]:,.0f}</td>' for y in dcf_years])
dcf_tax_html = "".join([f'<td class="p-2.5 text-right font-mono text-neutral-400">{(y["tax_rate"] or 0)*100:.1f}%</td>' for y in dcf_years])
dcf_nopat_html = "".join([f'<td class="p-2.5 text-right font-mono font-bold text-neutral-200">${y["ebit_after_tax"]:,.0f}</td>' for y in dcf_years])
dcf_reinv_html = "".join([f'<td class="p-2.5 text-right font-mono text-amber-400">${y["reinvestment"]:,.0f}</td>' if y["reinvestment"] is not None else '<td class="p-2.5 text-right font-mono text-neutral-500">-</td>' for y in dcf_years])
dcf_fcff_html = "".join([f'<td class="p-2.5 text-right font-mono {"text-rose-400" if (y["fcff"] or 0) < 0 else "text-emerald-400"} font-bold">${y["fcff"]:,.0f}</td>' if y["fcff"] is not None else '<td class="p-2.5 text-right font-mono text-neutral-500">-</td>' for y in dcf_years])
dcf_wacc_html = "".join([f'<td class="p-2.5 text-right font-mono text-neutral-400">{y["wacc"]*100:.2f}%</td>' if y["wacc"] is not None else '<td class="p-2.5 text-right font-mono text-neutral-500">-</td>' for y in dcf_years])
dcf_discount_html = "".join([f'<td class="p-2.5 text-right font-mono text-neutral-400">{y["cum_discount"]:.4f}</td>' if y["cum_discount"] is not None else '<td class="p-2.5 text-right font-mono text-neutral-500">-</td>' for y in dcf_years])
dcf_pv_html = "".join([f'<td class="p-2.5 text-right font-mono">${y["pv_fcff"]:,.0f}</td>' if y["pv_fcff"] is not None else '<td class="p-2.5 text-right font-mono text-neutral-500">-</td>' for y in dcf_years])
dcf_ic_html = "".join([f'<td class="p-2.5 text-right font-mono text-neutral-300">${y["invested_capital"]:,.0f}</td>' for y in dcf_years])
dcf_roic_html = "".join([f'<td class="p-2.5 text-right font-mono {"text-rose-400" if (y["roic"] or 0) < 0 else "text-emerald-400"}">{y["roic"]*100:.1f}%</td>' if y["roic"] is not None else '<td class="p-2.5 text-right font-mono text-neutral-500">-</td>' for y in dcf_years])

# Extract SQLite Macro Data
cur.execute("SELECT region, industry_name, num_firms, beta, cost_of_equity, debt_weight, after_tax_cost_of_debt, cost_of_capital FROM damodaran_industry_wacc ORDER BY region, industry_name;")
wacc_db = cur.fetchall()
wacc_json = [
    {
        "region": r[0],
        "industry": r[1],
        "firms": r[2] or 0,
        "beta": round(r[3], 2) if r[3] is not None else 0,
        "ke": round(r[4] * 100, 2) if r[4] is not None else 0,
        "wd": round(r[5] * 100, 1) if r[5] is not None else 0,
        "kd_at": round(r[6] * 100, 2) if r[6] is not None else 0,
        "wacc": round(r[7] * 100, 2) if r[7] is not None else 0
    }
    for r in wacc_db
]

cur.execute("SELECT year, sp500_total_return, small_cap_return, t_bill_3m_return, t_bond_10y_return, corp_bond_baa_return, real_estate_return, gold_return, sp500_cum_value, small_cap_cum_value, t_bill_cum_value FROM damodaran_historical_returns ORDER BY year;")
hist_db = cur.fetchall()
hist_json = [
    {
        "year": r[0],
        "sp500": round(r[1] * 100, 2) if r[1] is not None else 0,
        "small_cap": round(r[2] * 100, 2) if r[2] is not None else 0,
        "tbill": round(r[3] * 100, 2) if r[3] is not None else 0,
        "tbond": round(r[4] * 100, 2) if r[4] is not None else 0,
        "corp": round(r[5] * 100, 2) if r[5] is not None else 0,
        "real_estate": round(r[6] * 100, 2) if r[6] is not None else 0,
        "gold": round(r[7] * 100, 2) if r[7] is not None else 0,
        "sp500_cum": round(r[8], 2) if r[8] is not None else 0,
        "small_cap_cum": round(r[9], 2) if r[9] is not None else 0,
        "tbill_cum": round(r[10], 2) if r[10] is not None else 0
    }
    for r in hist_db
]

cur.execute("SELECT year, sp500_level, earnings_yield, dividend_yield, t_bond_rate, implied_erp, expected_return FROM damodaran_implied_erp ORDER BY year;")
impl_db = cur.fetchall()
impl_json = [
    {
        "year": r[0],
        "sp500": round(r[1], 2) if r[1] is not None else 0,
        "ey": round(r[2] * 100, 2) if r[2] is not None else 0,
        "dy": round(r[3] * 100, 2) if r[3] is not None else 0,
        "tbond": round(r[4] * 100, 2) if r[4] is not None else 0,
        "erp": round(r[5] * 100, 2) if r[5] is not None else 0,
        "expected_return": round(r[6] * 100, 2) if r[6] is not None else 0
    }
    for r in impl_db
]

distress_haircut_m = (bridge['sum_pv'] - bridge['proceeds_failure']) * bridge['prob_failure']
distress_haircut_b = distress_haircut_m / 1000

html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ERVIS :: Anthropic, PBC (NASDAQ: ANT) Damodaran Valuation Deep Dive & Macro Ingestion</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            font-weight: 700;
        }}
        .custom-scroll::-webkit-scrollbar {{
            height: 6px;
            width: 6px;
        }}
        .custom-scroll::-webkit-scrollbar-track {{
            background: #09090b;
        }}
        .custom-scroll::-webkit-scrollbar-thumb {{
            background: #27272a;
            border-radius: 3px;
        }}
        .custom-scroll::-webkit-scrollbar-thumb:hover {{
            background: #3f3f46;
        }}
        .glass-panel {{
            background-color: #0f0f11;
            border: 1px solid #27272a;
        }}
    </style>
</head>
<body class="min-h-screen text-xs antialiased selection:bg-amber-950 selection:text-amber-200">

    <!-- Top Command Header -->
    <header class="border-b border-neutral-800 bg-[#0c0d0e] sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-3 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-center space-x-3 flex-wrap">
                <span class="px-2 py-0.5 border border-amber-500/40 bg-amber-950/20 text-amber-400 font-mono text-[11px] font-bold tracking-wider">
                    ERVIS TERMINAL v2.5
                </span>
                <span class="text-neutral-500 font-mono text-xs">/</span>
                <h1 class="text-sm font-serif font-semibold text-neutral-100 tracking-wide">
                    Anthropic, PBC (NASDAQ: ANT) :: Damodaran Valuation Deep Dive
                </h1>
                <span class="px-2 py-0.5 border border-purple-800/60 bg-purple-950/30 text-purple-300 font-mono text-[10px] font-bold">
                    [SUBSTACK DEEP DIVE]
                </span>
                <span class="px-2 py-0.5 border border-cyan-800/60 bg-cyan-950/30 text-cyan-300 font-mono text-[10px] font-bold">
                    [Q3 2026 LEAK ADJUSTED]
                </span>
                <span class="px-2 py-0.5 border border-amber-800/60 bg-amber-950/30 text-amber-300 font-mono text-[10px] font-bold">
                    [GATE 5 SIGN-OFF]
                </span>
            </div>
            
            <div class="flex items-center space-x-4 text-xs font-mono flex-wrap">
                <span class="text-neutral-400">IPO SPOT: <strong class="text-neutral-100 font-bold">${bridge['price']:.2f}</strong> (${bridge['price'] * bridge['shares'] / 1000:.1f}B)</span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">DCF VALUE: <strong class="text-emerald-400 font-bold">${bridge['val_per_share']:.2f}</strong> (${bridge['val_equity_common'] / 1000:.1f}B)</span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">PRIOR: <strong class="text-neutral-300 font-bold">$445.05</strong></span>
                <span class="text-neutral-600">|</span>
                <span class="text-neutral-400">CROWD: <strong class="text-cyan-400 font-bold">$268.00</strong> ($884.2B)</span>
                <span class="text-neutral-600">|</span>
                <span class="px-2 py-0.5 border border-rose-800 bg-rose-950/40 text-rose-400 font-bold">
                    AVOID IPO (-16.3%)
                </span>
            </div>
        </div>

        <!-- Terminal Command Navigation Bar (8 Tabs) -->
        <div class="max-w-7xl mx-auto px-6 border-t border-neutral-800 flex space-x-1 overflow-x-auto text-xs font-mono custom-scroll">
            <button id="btn-tab-cockpit" onclick="switchTab('tab-cockpit')" class="tab-btn active px-3.5 py-2 border-b-2 border-amber-500 text-amber-400 bg-neutral-900/60 transition-colors whitespace-nowrap">
                [01] VALUATION COCKPIT & BRIDGE
            </button>
            <button id="btn-tab-levers" onclick="switchTab('tab-levers')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [02] 4 VALUATION LEVERS & FRAGILITY
            </button>
            <button id="btn-tab-costcap" onclick="switchTab('tab-costcap')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [03] COST OF CAPITAL MASTERCLASS
            </button>
            <button id="btn-tab-capitalization" onclick="switchTab('tab-capitalization')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [04] $485B DEBT & R&D AUDIT
            </button>
            <button id="btn-tab-dcf" onclick="switchTab('tab-dcf')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [05] 10-YR GINZU DCF SCHEDULE
            </button>
            <button id="btn-tab-macro" onclick="switchTab('tab-macro')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [06] DAMODARAN MACRO DATASETS
            </button>
            <button id="btn-tab-prospectus" onclick="switchTab('tab-prospectus')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [07] S-1 PROSPECTUS & QUAD-CLASS
            </button>
            <button id="btn-tab-simulator" onclick="switchTab('tab-simulator')" class="tab-btn px-3.5 py-2 border-b-2 border-transparent text-neutral-400 hover:text-neutral-200 transition-colors whitespace-nowrap">
                [08] CROWD BENCHMARK & SIMULATOR
            </button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="max-w-7xl mx-auto px-6 py-6 space-y-6">

        <!-- ============================================================== -->
        <!-- TAB 1: EXECUTIVE VALUATION COCKPIT & BRIDGE                    -->
        <!-- ============================================================== -->
        <div id="tab-cockpit" class="tab-content space-y-6">
            
            <div class="p-3.5 bg-amber-950/20 border border-amber-900/60 text-amber-300 flex items-center justify-between text-xs">
                <span>[VALUATION VERDICT :: Q3 2026 UPDATE] Following the leak of Anthropic's Q3 2026 financials, Aswath Damodaran updated his valuation model. Base annualized revenues rose to $35.29B (from $19.71B), Year 1 growth was moderated to 190% (to reach ~$102.3B), and Yr 2-5 CAGR was dialed to 42%. Resulting Intrinsic Value: <strong>$439.24 / share ($1,450.95B common equity)</strong> vs prior $445.05 / share. At the rumored $525.00 IPO price ($1,733.7B), Anthropic is priced at a 19.5% premium (-16.3% downside). Tactical rating: <strong>AVOID IPO / ACCUMULATE BELOW $439</strong>.</span>
                <span class="font-bold uppercase tracking-wider text-[10px] border border-amber-800 px-2 py-0.5 whitespace-nowrap ml-4">Tactical Stance</span>
            </div>

            <!-- Top Metric Cockpit Cards -->
            <div class="grid grid-cols-2 md:grid-cols-6 gap-3">
                <div class="p-4 glass-panel rounded-sm">
                    <div class="text-[10px] uppercase text-neutral-500 font-semibold">IPO Offering Price</div>
                    <div class="text-xl font-bold text-neutral-100 mt-1 font-mono">${bridge['price']:.2f}</div>
                    <div class="text-[11px] text-amber-400 mt-0.5">Cap: ${bridge['price'] * bridge['shares'] / 1000:.1f}B</div>
                </div>
                <div class="p-4 glass-panel rounded-sm">
                    <div class="text-[10px] uppercase text-neutral-500 font-semibold">Damodaran Fair Value</div>
                    <div class="text-xl font-bold text-emerald-400 mt-1 font-mono">${bridge['val_per_share']:.2f}</div>
                    <div class="text-[11px] text-emerald-500/80 mt-0.5">Equity: ${bridge['val_equity_common'] / 1000:.1f}B</div>
                </div>
                <div class="p-4 glass-panel rounded-sm">
                    <div class="text-[10px] uppercase text-neutral-500 font-semibold">Offering Mispricing</div>
                    <div class="text-xl font-bold text-rose-400 mt-1 font-mono">+19.53%</div>
                    <div class="text-[11px] text-rose-400/80 mt-0.5">-16.33% Downside</div>
                </div>
                <div class="p-4 glass-panel rounded-sm">
                    <div class="text-[10px] uppercase text-neutral-500 font-semibold">Crowd Median Value</div>
                    <div class="text-xl font-bold text-cyan-400 mt-1 font-mono">$268.00</div>
                    <div class="text-[11px] text-cyan-500/80 mt-0.5">Equity: $884.2B</div>
                </div>
                <div class="p-4 glass-panel rounded-sm">
                    <div class="text-[10px] uppercase text-neutral-500 font-semibold">Total Adjusted Debt</div>
                    <div class="text-xl font-bold text-rose-400 mt-1 font-mono">${bridge['debt'] / 1000:.1f}B</div>
                    <div class="text-[11px] text-neutral-400 mt-0.5">$376.0B Compute PV</div>
                </div>
                <div class="p-4 glass-panel rounded-sm">
                    <div class="text-[10px] uppercase text-neutral-500 font-semibold">Cash + Net IPO Raise</div>
                    <div class="text-xl font-bold text-emerald-400 mt-1 font-mono">${(bridge['cash'] + bridge['ipo_proceeds']) / 1000:.1f}B</div>
                    <div class="text-[11px] text-neutral-400 mt-0.5">$112.4B Cash + $100B IPO</div>
                </div>
            </div>

            <!-- Full Master Valuation Bridge Table -->
            <div class="glass-panel p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between flex-wrap gap-2">
                    <div>
                        <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                            Master Enterprise Value to Common Stock Equity Bridge
                        </h3>
                        <p class="text-xs font-mono text-neutral-400 mt-1">Reconciliation from AnthropicIPO_updated.xlsx (Post-Q3 Leaked Financials) | All Figures Formatted</p>
                    </div>
                    <span class="px-2.5 py-1 bg-[#141416] border border-neutral-800 text-amber-400 font-bold font-mono text-xs">
                        TARGET VALUE: ${bridge['val_per_share']:.2f} / SHARE
                    </span>
                </div>

                <div class="overflow-x-auto border border-neutral-800 custom-scroll">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-3">Valuation Step</th>
                                <th class="p-3">Model Cell</th>
                                <th class="p-3 text-right">Amount ($ Millions)</th>
                                <th class="p-3 text-right">Equivalent ($ Billions)</th>
                                <th class="p-3 text-right">% of Assets</th>
                                <th class="p-3">Institutional Rationale</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">PV of Discrete Cash Flows (Yr 1–10)</td>
                                <td class="p-3 text-neutral-500">Valuation!B20</td>
                                <td class="p-3 text-right font-bold text-white">${bridge['pv_cf_10yr']:,.1f} M</td>
                                <td class="p-3 text-right font-bold text-white">${bridge['pv_cf_10yr'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">{bridge['pv_cf_10yr'] / bridge['val_operating_assets'] * 100:.1f}%</td>
                                <td class="p-3 text-neutral-400">Sum of 10-year discrete free cash flows discounted at transition WACC (9.74% &rarr; 9.13%)</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-100 font-semibold">PV of Terminal Value (Yr 10)</td>
                                <td class="p-3 text-neutral-500">Valuation!B19</td>
                                <td class="p-3 text-right font-bold text-white">${bridge['pv_tv']:,.1f} M</td>
                                <td class="p-3 text-right font-bold text-white">${bridge['pv_tv'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">{bridge['pv_tv'] / bridge['val_operating_assets'] * 100:.1f}%</td>
                                <td class="p-3 text-neutral-400">Terminal CF $146.3B / (Terminal WACC 9.13% - g 4.90%) discounted by factor 0.4014</td>
                            </tr>
                            <tr class="bg-neutral-900/40 font-bold">
                                <td class="p-3 font-serif text-amber-400">Sum of Present Values (Going Concern EV)</td>
                                <td class="p-3 text-neutral-500">Valuation!B21</td>
                                <td class="p-3 text-right text-amber-400">${bridge['sum_pv']:,.1f} M</td>
                                <td class="p-3 text-right text-amber-400">${bridge['sum_pv'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">105.3%</td>
                                <td class="p-3 text-neutral-400">Unadjusted present value assuming Anthropic operates in perpetuity without distress</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-rose-400 font-semibold">Less: Failure Risk Haircut (10% Prob)</td>
                                <td class="p-3 text-neutral-500">Valuation!B22:B23</td>
                                <td class="p-3 text-right text-rose-400">-${distress_haircut_m:,.1f} M</td>
                                <td class="p-3 text-right text-rose-400">-${distress_haircut_b:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">-5.3%</td>
                                <td class="p-3 text-neutral-400">10% cumulative default probability with 50% distress liquidation proceeds ($905.2B)</td>
                            </tr>
                            <tr class="bg-[#141416] font-bold">
                                <td class="p-3 font-serif text-emerald-400">Value of Operating Assets</td>
                                <td class="p-3 text-neutral-500">Valuation!B24</td>
                                <td class="p-3 text-right text-emerald-400">${bridge['val_operating_assets']:,.1f} M</td>
                                <td class="p-3 text-right text-emerald-400">${bridge['val_operating_assets'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">100.0%</td>
                                <td class="p-3 text-neutral-400">Distress-adjusted core operating enterprise value of Anthropic's business</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-rose-400 font-semibold">Less: Total Adjusted Debt (incl Compute PV)</td>
                                <td class="p-3 text-neutral-500">Valuation!B25</td>
                                <td class="p-3 text-right text-rose-400">-${bridge['debt']:,.1f} M</td>
                                <td class="p-3 text-right text-rose-400">-${bridge['debt'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">-28.2%</td>
                                <td class="p-3 text-neutral-400">$376.0B PV of compute & lease commitments + $109.3B reported debt</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-emerald-400 font-semibold">Plus: Existing Cash & Cross Holdings</td>
                                <td class="p-3 text-neutral-500">Valuation!B27</td>
                                <td class="p-3 text-right text-emerald-400">+${bridge['cash']:,.1f} M</td>
                                <td class="p-3 text-right text-emerald-400">+${bridge['cash'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">+6.5%</td>
                                <td class="p-3 text-neutral-400">Liquid reserves on balance sheet providing multi-year compute commitment buffer</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-emerald-400 font-semibold">Plus: Expected Net IPO Proceeds</td>
                                <td class="p-3 text-neutral-500">Valuation!B28</td>
                                <td class="p-3 text-right text-emerald-400">+${bridge['ipo_proceeds']:,.1f} M</td>
                                <td class="p-3 text-right text-emerald-400">+${bridge['ipo_proceeds'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">+5.8%</td>
                                <td class="p-3 text-neutral-400">Primary cash infusion anticipated from the public offering</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-emerald-400 font-semibold">Plus: Non-Operating Assets</td>
                                <td class="p-3 text-neutral-500">Valuation!B29</td>
                                <td class="p-3 text-right text-emerald-400">+${bridge['non_operating_assets']:,.1f} M</td>
                                <td class="p-3 text-right text-emerald-400">+${bridge['non_operating_assets'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">+0.2%</td>
                                <td class="p-3 text-neutral-400">Strategic equity investments and non-core tech holdings</td>
                            </tr>
                            <tr class="bg-neutral-900/60 font-bold">
                                <td class="p-3 font-serif text-neutral-100">Total Value of Equity</td>
                                <td class="p-3 text-neutral-500">Valuation!B30</td>
                                <td class="p-3 text-right text-neutral-100">${bridge['val_equity']:,.1f} M</td>
                                <td class="p-3 text-right text-neutral-100">${bridge['val_equity'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">84.4%</td>
                                <td class="p-3 text-neutral-400">Aggregate equity capitalization across all share classes and equity claims</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-rose-400 font-semibold">Less: Value of Employee Options Overhang</td>
                                <td class="p-3 text-neutral-500">Valuation!B31</td>
                                <td class="p-3 text-right text-rose-400">-${bridge['options_val']:,.1f} M</td>
                                <td class="p-3 text-right text-rose-400">-${bridge['options_val'] / 1000:,.3f} B</td>
                                <td class="p-3 text-right text-neutral-400">-0.03%</td>
                                <td class="p-3 text-neutral-400">Black-Scholes option value of granted options deducted to prevent dilution double-counting</td>
                            </tr>
                            <tr class="bg-amber-950/30 border-t-2 border-amber-500 font-bold text-amber-300">
                                <td class="p-3 font-serif text-base">Value of Equity in Common Stock</td>
                                <td class="p-3 text-neutral-500">Valuation!B32</td>
                                <td class="p-3 text-right text-base">${bridge['val_equity_common']:,.1f} M</td>
                                <td class="p-3 text-right text-base">${bridge['val_equity_common'] / 1000:,.2f} B</td>
                                <td class="p-3 text-right text-neutral-400">84.3%</td>
                                <td class="p-3 text-neutral-400">Residual value accruing directly to public common shareholders</td>
                            </tr>
                            <tr>
                                <td class="p-3 font-serif text-neutral-300">Diluted Shares Outstanding</td>
                                <td class="p-3 text-neutral-500">Valuation!B33</td>
                                <td class="p-3 text-right" colspan="2">{bridge['shares']:,.3f} Million Shares</td>
                                <td class="p-3 text-right text-neutral-500">-</td>
                                <td class="p-3 text-neutral-400">Common shares plus vested RSUs on balance sheet</td>
                            </tr>
                            <tr class="bg-emerald-950/40 border-t border-emerald-500 text-emerald-400 font-bold text-sm">
                                <td class="p-3 font-serif text-base">Intrinsic Fair Value Per Share</td>
                                <td class="p-3 text-neutral-500">Valuation!B34</td>
                                <td class="p-3 text-right text-lg" colspan="2">${bridge['val_per_share']:.2f} / SHARE</td>
                                <td class="p-3 text-right text-neutral-400">-</td>
                                <td class="p-3 text-neutral-400">Damodaran Ginzu DCF Target Price | Current Spot: ${bridge['price']:.2f}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Waterfall Visual Chart -->
            <div class="glass-panel p-6 space-y-4">
                <h3 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                    Enterprise Value to Equity Waterfall Chart ($ Billions)
                </h3>
                <div class="h-80">
                    <canvas id="waterfallChart"></canvas>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 2: 4 VALUATION LEVERS & FRAGILITY                          -->
        <!-- ============================================================== -->
        <div id="tab-levers" class="tab-content hidden space-y-6">
            <div class="p-3.5 bg-neutral-900 border border-neutral-800 text-neutral-300 text-xs">
                <span>[DAMODARAN SELF-CRITIQUE :: ORDER OF FRAGILITY] In his new Substack piece, Damodaran plays devil's advocate with his own model, explicitly ranking his valuation drivers in order of <strong>magnitude and fragility</strong>. Below is the institutional dissection of each lever.</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- Lever 1 -->
                <div class="p-5 glass-panel border-l-4 border-rose-500 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="px-2 py-0.5 bg-rose-950/60 text-rose-300 border border-rose-800 text-[10px] font-bold">LEVER 1 :: RANK #1 FRAGILITY</span>
                        <span class="text-rose-400 font-bold font-mono">2036 REV: $1,004.5B</span>
                    </div>
                    <h4 class="text-base font-serif font-bold text-neutral-100">Target Revenues ($1.005 Trillion in 10 Years)</h4>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Damodaran picks this as the single most exposed driver. Delivering $1.005T puts Anthropic in the league of Amazon and Walmart. It requires: (1) AI agent adoption exploding into an enterprise staple, (2) Claude capturing a dominant share in the premium AI tier, and (3) monetization models transitioning from token pricing to value-based agency subscription.
                    </p>
                    <div class="p-2.5 bg-[#141416] border border-neutral-800 text-xs text-rose-300 font-mono">
                        Fragility Risk: If 2036 revenues miss and land at $500B instead of $1.0T, operating margins compress, compute sits idle, and default risk increases non-linearly.
                    </div>
                </div>

                <!-- Lever 2 -->
                <div class="p-5 glass-panel border-l-4 border-amber-500 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="px-2 py-0.5 bg-amber-950/60 text-amber-300 border border-amber-800 text-[10px] font-bold">LEVER 2 :: RANK #2 FRAGILITY</span>
                        <span class="text-amber-400 font-bold font-mono">FOUNDER ECHO CHAMBER</span>
                    </div>
                    <h4 class="text-base font-serif font-bold text-neutral-100">Governance & Public Benefit Corp (PBC) Structure</h4>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Anthropic's quad-class voting structure permanently insulates founders and the Long-Term Benefit Trust from shareholder oversight. Damodaran warns that while founders are visionary, AI business models will experience violent competitive and technological shocks requiring agile operational pivots that insular tech echo chambers historically reject.
                    </p>
                    <div class="p-2.5 bg-[#141416] border border-neutral-800 text-xs text-amber-300 font-mono">
                        Governance Discount: Outside public equity has zero influence over capital allocation or potential board-level strategic restructuring.
                    </div>
                </div>

                <!-- Lever 3 -->
                <div class="p-5 glass-panel border-l-4 border-cyan-500 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="px-2 py-0.5 bg-cyan-950/60 text-cyan-300 border border-cyan-800 text-[10px] font-bold">LEVER 3 :: RANK #3 FRAGILITY</span>
                        <span class="text-cyan-400 font-bold font-mono">TARGET MARGIN: 27.5%</span>
                    </div>
                    <h4 class="text-base font-serif font-bold text-neutral-100">Profitability: Customer Stickiness vs Commoditization</h4>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Critics contend LLMs will be commoditized into zero-margin utilities. Damodaran pushes back: enterprise software moats do not come from patents or brands, but from <strong>stickiness</strong>. If Claude agents become deeply intertwined with proprietary corporate workflows, switching costs rise. Target pre-tax margin: 32.5%, hair-cut to 27.5% for regulatory compliance.
                    </p>
                    <div class="p-2.5 bg-[#141416] border border-neutral-800 text-xs text-cyan-300 font-mono">
                        Margin Sensitivity: Every 5.0% change in long-term operating margin swings equity fair value by ~$240 Billion (~$72/share).
                    </div>
                </div>

                <!-- Lever 4 -->
                <div class="p-5 glass-panel border-l-4 border-emerald-500 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="px-2 py-0.5 bg-emerald-950/60 text-emerald-300 border border-emerald-800 text-[10px] font-bold">LEVER 4 :: RANK #4 FRAGILITY</span>
                        <span class="text-emerald-400 font-bold font-mono">SALES/CAPITAL: 3.0</span>
                    </div>
                    <h4 class="text-base font-serif font-bold text-neutral-100">Compute Reinvestment & Data Center Economics</h4>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        To generate $1.005T in revenues, Anthropic must maintain and expand compute access. Damodaran uses a Sales-to-Capital ratio of 3.0, generating $450B in cumulative contractual commitments ($376B PV). This requires chip efficiency to outpace power and grid interconnection bottlenecks.
                    </p>
                    <div class="p-2.5 bg-[#141416] border border-neutral-800 text-xs text-emerald-300 font-mono">
                        Reinvestment Reality: If compute costs remain high (Sales/Capital drops to 1.5), invested capital doubles to $1.2T, crushing ROIC and cash conversion.
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 3: COST OF CAPITAL MASTERCLASS                             -->
        <!-- ============================================================== -->
        <div id="tab-costcap" class="tab-content hidden space-y-6">
            <div class="p-4 bg-purple-950/20 border border-purple-900/60 text-purple-300 space-y-2 text-xs">
                <div class="font-bold text-sm text-purple-200 uppercase tracking-wide">
                    The Cost of Capital: The Swiss Army Knife of Corporate Finance
                </div>
                <p>
                    In response to analysts claiming that Anthropic's 9.74% WACC is "far too low" and demanding 15% to 25% discount rates, Damodaran systematically tears down market delusions using four institutional anchors. The cost of capital is not an arbitrary receptacle for investor fear; it is an <strong>opportunity cost</strong> bounded by empirical market pricing.
                </p>
            </div>

            <!-- 4 Reality Checks Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                <div class="p-4 glass-panel space-y-2">
                    <span class="text-amber-400 font-mono text-[10px] font-bold">[CHECK 1: HISTORY 1928–2025]</span>
                    <h5 class="text-sm font-serif font-bold text-neutral-100">Historical Returns Limit</h5>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Over 98 years of US equity history, the S&P 500 arithmetic mean return is 11.85% and geometric mean is 10.02% (2001–2025 is just 8.74%). The equity risk premium over 10-year treasuries is 5.48%. Given a 4.94% risk-free rate, average US equity cost of capital cannot exceed 10.4–10.65%.
                    </p>
                </div>
                <div class="p-4 glass-panel space-y-2">
                    <span class="text-cyan-400 font-mono text-[10px] font-bold">[CHECK 2: MARKET-IMPLIED]</span>
                    <h5 class="text-sm font-serif font-bold text-neutral-100">8.99% S&P 500 Expected Return</h5>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Backing expected cash flows out of current market prices yields an expected US equity return of exactly 8.99% as of October 2026. The implied expected return for US equities has <strong>not exceeded 10% since 1994</strong>. Demanding 15% is economically delusional.
                    </p>
                </div>
                <div class="p-4 glass-panel space-y-2">
                    <span class="text-rose-400 font-mono text-[10px] font-bold">[CHECK 3: PRICING MULTIPLES]</span>
                    <h5 class="text-sm font-serif font-bold text-neutral-100">The 7.5x P/E Absurdity</h5>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        If the cost of equity were truly 15%, given 5% nominal US GDP growth and 20% ROE, the aggregate market P/E ratio would be <strong>7.5x</strong>. Forward S&P 500 P/E is ~20x. Claiming 15% WACC while buying equities at 20x P/E is mathematically inconsistent.
                    </p>
                </div>
                <div class="p-4 glass-panel space-y-2">
                    <span class="text-emerald-400 font-mono text-[10px] font-bold">[CHECK 4: CROSS-SECTION]</span>
                    <h5 class="text-sm font-serif font-bold text-neutral-100">90th Percentile Tech WACC</h5>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        In Damodaran's start-of-year global survey, 80% of all US technology companies have WACC between 9.02% and 12.27%. At 9.74%, Anthropic sits near the 90th percentile of all US firms. Furthermore, its cost of capital transitions to 9.13% as it matures.
                    </p>
                </div>
            </div>

            <!-- Deep Dive on Decoupling Failure Risk from WACC -->
            <div class="glass-panel p-6 space-y-4">
                <h4 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-purple-500 pl-2">
                    Why Default Risk Must NOT Be Jammed into Going-Concern WACC
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                    <div class="p-3 bg-[#141416] border border-neutral-800 space-y-2">
                        <span class="text-neutral-400 font-bold uppercase text-[10px]">Staggered Commitments</span>
                        <p class="text-neutral-300">
                            Unlike debt maturities where a bullet principal repayment comes due, Anthropic's compute liabilities are contractual operating commitments: $77.0B in Year 1 and $98.1B in Year 2.
                        </p>
                    </div>
                    <div class="p-3 bg-[#141416] border border-neutral-800 space-y-2">
                        <span class="text-emerald-400 font-bold uppercase text-[10px]">$212.4B Liquid Firepower</span>
                        <p class="text-neutral-300">
                            Anthropic holds $112.4B in cash reserves, which expands to over $212.4B following the $100B net IPO raise. It has zero near-term bankruptcy risk over years 1 to 3.
                        </p>
                    </div>
                    <div class="p-3 bg-[#141416] border border-neutral-800 space-y-2">
                        <span class="text-amber-400 font-bold uppercase text-[10px]">Explicit Failure Rate (10%)</span>
                        <p class="text-neutral-300">
                            Damodaran handles distress through an explicit failure probability of 10% with 50% distress liquidation salvage ($905.2B), taking $90.5B off operating value cleanly.
                        </p>
                    </div>
                </div>
            </div>

            <!-- VC and PE Fictional Returns Debunking -->
            <div class="glass-panel p-6 space-y-4">
                <h4 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-amber-500 pl-2">
                    Professional Investors: Debunking VC & Private Equity 25%-50% Hurdle Rates
                </h4>
                <p class="text-xs text-neutral-400 leading-relaxed">
                    Venture capitalists routinely demand 30% to 50% target hurdle rates as promotional props. However, long-term <strong>Cambridge Associates</strong> benchmark data reveals that actual realized returns delivered by VC and PE funds lag public index funds over 10 to 20 year horizons (averaging 10% to 12%). Setting artificially elevated hurdle rates forces managers to invent aggressively skewed cash flows, leading to systemic capital misallocation.
                </p>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 4: $485B DEBT CAPITALIZATION & R&D AUDIT                    -->
        <!-- ============================================================== -->
        <div id="tab-capitalization" class="tab-content hidden space-y-6">
            <div class="p-3.5 bg-neutral-900 border border-neutral-800 text-neutral-300 text-xs">
                <span>[FORENSIC ACCOUNTING AUDIT] Total adjusted debt stands at <strong>$485.32 Billion</strong>. This includes $376.00 Billion in synthetic debt created by capitalizing compute commitments and operating leases, alongside $109.32 Billion of reported book debt.</span>
            </div>

            <!-- Operating Lease & Compute Commitment Table -->
            <div class="glass-panel p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h4 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-rose-500 pl-2">
                            Compute Commitments & Operating Lease Capitalization Schedule
                        </h4>
                        <p class="text-xs text-neutral-400 mt-1">Discounted at Pre-Tax Cost of Debt = 6.2828% (BB+ Credit Rating)</p>
                    </div>
                    <span class="text-rose-400 font-bold font-mono text-xs">
                        TOTAL SYNTHETIC DEBT: ${total_lease_pv / 1000:.2f}B
                    </span>
                </div>

                <div class="overflow-x-auto border border-neutral-800 custom-scroll">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-3">Commitment Period</th>
                                <th class="p-3 text-right">Nominal Commitment ($M)</th>
                                <th class="p-3 text-right">Discount Factor</th>
                                <th class="p-3 text-right">Present Value ($M)</th>
                                <th class="p-3 text-right">Equivalent ($B)</th>
                                <th class="p-3">Counterparty / Hardware Nature</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            {lease_rows_html}
                            <tr class="bg-neutral-900/60 font-bold text-rose-400">
                                <td class="p-3">Total Capitalized Synthetic Debt</td>
                                <td class="p-3 text-right">${total_lease_comm:,.1f} M</td>
                                <td class="p-3 text-right">-</td>
                                <td class="p-3 text-right">${total_lease_pv:,.1f} M</td>
                                <td class="p-3 text-right">${total_lease_pv / 1000:,.2f} B</td>
                                <td class="p-3 text-neutral-300">Added directly to Balance Sheet Debt in Valuation Bridge</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- R&D Capitalization Table -->
            <div class="glass-panel p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h4 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-emerald-500 pl-2">
                            Research & Development Capitalization (3-Year Amortization)
                        </h4>
                        <p class="text-xs text-neutral-400 mt-1">Converting R&D expenses into intangible capital assets</p>
                    </div>
                    <span class="text-emerald-400 font-bold font-mono text-xs">
                        RESEARCH ASSET: $26.53B | EBIT BOOST: +$11.44B
                    </span>
                </div>

                <div class="overflow-x-auto border border-neutral-800 custom-scroll">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-3">Filing Year</th>
                                <th class="p-3 text-right">R&D Expense ($M)</th>
                                <th class="p-3 text-right">Unamortized %</th>
                                <th class="p-3 text-right">Unamortized Asset ($M)</th>
                                <th class="p-3 text-right">Amortization This Year ($M)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            {rd_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 5: 10-YR GINZU DCF SCHEDULE                               -->
        <!-- ============================================================== -->
        <div id="tab-dcf" class="tab-content hidden space-y-6">
            <div class="p-3.5 bg-neutral-900 border border-neutral-800 text-neutral-300 text-xs">
                <span>[GINZU DCF SCHEDULE] 10-year projection modeled from <strong>AnthropicIPO_updated.xlsx</strong>. Base annualized revenue: $35.29B, reaching $1.005 Trillion in Year 10. Operating margin expands from -131.3% to 27.5% net of regulatory haircut. Reinvestment anchored at Sales/Capital = 3.0.</span>
            </div>

            <!-- DCF Master Grid -->
            <div class="glass-panel p-6 space-y-4">
                <div class="border-b border-neutral-800 pb-3 flex items-center justify-between">
                    <div>
                        <h4 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-emerald-500 pl-2">
                            Anthropic 10-Year Discrete DCF Line-Item Projections
                        </h4>
                        <p class="text-xs text-neutral-400 mt-1">All amounts in US $ Millions unless specified</p>
                    </div>
                </div>

                <div class="overflow-x-auto border border-neutral-800 custom-scroll">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800">
                            <tr>
                                <th class="p-2.5 sticky left-0 bg-[#0c0d0e] z-10">Metric Line Item</th>
                                {dcf_header_html}
                                <th class="p-2.5 text-right bg-emerald-950/40 text-emerald-400">Terminal</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-neutral-800/60 text-neutral-300">
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">Revenue Growth Rate</td>
                                {dcf_growth_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/20 text-emerald-400">4.9%</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">Revenues ($M)</td>
                                {dcf_rev_html}
                                <td class="p-2.5 text-right font-mono font-bold bg-emerald-950/20 text-emerald-400">${dcf_years[-1]["revenues"] * 1.049:,.0f}</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">EBIT Operating Margin</td>
                                {dcf_margin_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/20 text-emerald-400">27.5%</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">EBIT (Operating Income)</td>
                                {dcf_ebit_html}
                                <td class="p-2.5 text-right font-mono font-bold bg-emerald-950/20 text-emerald-400">${bridge["terminal_cf"] / (1 - 0.25):,.0f}</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">Effective Tax Rate</td>
                                {dcf_tax_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/20 text-neutral-300">25.0%</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">EBIT * (1 - Tax)</td>
                                {dcf_nopat_html}
                                <td class="p-2.5 text-right font-mono font-bold bg-emerald-950/20 text-emerald-400">${bridge["terminal_cf"] * 1.25:,.0f}</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">Reinvestment (Sales/Cap=3.0)</td>
                                {dcf_reinv_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/20 text-amber-400">$36,809</td>
                            </tr>
                            <tr class="bg-neutral-900/60 font-bold">
                                <td class="p-2.5 text-emerald-400 sticky left-0 bg-neutral-900">Free Cash Flow to Firm (FCFF)</td>
                                {dcf_fcff_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/40 text-emerald-400">${bridge["terminal_cf"]:,.0f}</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">Cost of Capital (WACC)</td>
                                {dcf_wacc_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/20 text-neutral-300">9.13%</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">Discount Factor</td>
                                {dcf_discount_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/20 text-neutral-300">0.4014</td>
                            </tr>
                            <tr class="bg-amber-950/20 font-bold text-amber-300">
                                <td class="p-2.5 sticky left-0 bg-[#141416]">Present Value of FCFF ($M)</td>
                                {dcf_pv_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/40 text-emerald-300">${bridge["pv_tv"]:,.0f}</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">Invested Capital ($M)</td>
                                {dcf_ic_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/20 text-neutral-300">$895,420</td>
                            </tr>
                            <tr>
                                <td class="p-2.5 font-semibold text-white sticky left-0 bg-[#0f0f11]">Economic ROIC (%)</td>
                                {dcf_roic_html}
                                <td class="p-2.5 text-right font-mono bg-emerald-950/20 text-emerald-400">21.8%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- DCF Charts Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="glass-panel p-6 space-y-3">
                    <h5 class="text-xs font-serif font-bold text-neutral-100 uppercase tracking-wider">Revenue & Operating Margin Trajectory</h5>
                    <div class="h-64">
                        <canvas id="revMarginChart"></canvas>
                    </div>
                </div>
                <div class="glass-panel p-6 space-y-3">
                    <h5 class="text-xs font-serif font-bold text-neutral-100 uppercase tracking-wider">Free Cash Flow & Present Value Profile</h5>
                    <div class="h-64">
                        <canvas id="fcfProfileChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 6: DAMODARAN MACRO DATASETS                                -->
        <!-- ============================================================== -->
        <div id="tab-macro" class="tab-content hidden space-y-6">
            <div class="p-3.5 bg-neutral-900 border border-neutral-800 text-neutral-300 text-xs">
                <span>[MACRO INGESTION REPOSITORY] Damodaran's institutional datasets ingested into SQLite vault: (1) Cost of Capital by Industry (US & Global), (2) Historical Returns (1928–2025), and (3) S&P 500 Implied Expected Returns (1960–2025).</span>
            </div>

            <!-- Macro Datasets Charts -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="glass-panel p-6 space-y-3">
                    <h5 class="text-xs font-serif font-bold text-neutral-100 uppercase tracking-wider">
                        S&P 500 Implied Expected Return vs 10-Year Treasury (1960–2025)
                    </h5>
                    <div class="h-64">
                        <canvas id="impliedErpChart"></canvas>
                    </div>
                </div>
                <div class="glass-panel p-6 space-y-3">
                    <h5 class="text-xs font-serif font-bold text-neutral-100 uppercase tracking-wider">
                        Historical Asset Class Cumulative Growth of $100 (1928–2025)
                    </h5>
                    <div class="h-64">
                        <canvas id="histGrowthChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- Searchable Industry Cost of Capital Explorer Table -->
            <div class="glass-panel p-6 space-y-4">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-neutral-800 pb-3">
                    <div>
                        <h4 class="text-sm font-serif font-semibold text-neutral-100 uppercase tracking-wider border-l-2 border-cyan-500 pl-2">
                            Industry Cost of Capital Lookup (US & Global 2026)
                        </h4>
                        <p class="text-xs text-neutral-400 mt-1">Ingested from waccUS.xlsx & waccGlobal.xlsx | 192 Industry Records in Vault</p>
                    </div>
                    <div class="flex items-center space-x-2">
                        <input id="industrySearch" type="text" placeholder="Search industry (e.g. Software, Semi)..." oninput="filterIndustryTable()" class="bg-[#141416] border border-neutral-700 px-3 py-1.5 text-xs text-white rounded-sm focus:border-amber-500 outline-none w-64 font-mono">
                        <select id="regionSelect" onchange="filterIndustryTable()" class="bg-[#141416] border border-neutral-700 px-2 py-1.5 text-xs text-white rounded-sm font-mono">
                            <option value="ALL">All Regions</option>
                            <option value="US" selected>United States</option>
                            <option value="GLOBAL">Global</option>
                        </select>
                    </div>
                </div>

                <div class="overflow-x-auto border border-neutral-800 max-h-96 custom-scroll">
                    <table class="w-full text-left text-xs font-mono">
                        <thead class="bg-[#0c0d0e] text-neutral-400 uppercase border-b border-neutral-800 sticky top-0">
                            <tr>
                                <th class="p-2.5">Region</th>
                                <th class="p-2.5">Industry Name</th>
                                <th class="p-2.5 text-right">Firms</th>
                                <th class="p-2.5 text-right">Beta</th>
                                <th class="p-2.5 text-right">Cost of Equity</th>
                                <th class="p-2.5 text-right">Debt Weight</th>
                                <th class="p-2.5 text-right">After-Tax Cost Debt</th>
                                <th class="p-2.5 text-right">Cost of Capital</th>
                            </tr>
                        </thead>
                        <tbody id="industryTableBody" class="divide-y divide-neutral-800/60 text-neutral-300">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 7: S-1 PROSPECTUS & QUAD-CLASS GOVERNANCE                  -->
        <!-- ============================================================== -->
        <div id="tab-prospectus" class="tab-content hidden space-y-6">
            <div class="p-3.5 bg-neutral-900 border border-neutral-800 text-neutral-300 text-xs">
                <span>[SEC FORM S-1 GOVERNANCE AUDIT] Quad-Class Share Structure & Public Benefit Corporation (PBC) charter analysis. Foundational conflict between fiduciary shareholder return and ideological safety governance.</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="p-5 glass-panel space-y-2 border-t-2 border-blue-500">
                    <span class="text-blue-400 font-bold text-[10px] uppercase">Class A Common</span>
                    <h5 class="text-sm font-serif font-bold text-white">Public Shareholders</h5>
                    <div class="text-lg font-bold font-mono text-neutral-200">1 Vote / Share</div>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Offered to public investors in the IPO. Subordinate in corporate control. Zero ability to replace management.
                    </p>
                </div>
                <div class="p-5 glass-panel space-y-2 border-t-2 border-amber-500">
                    <span class="text-amber-400 font-bold text-[10px] uppercase">Class B Common</span>
                    <h5 class="text-sm font-serif font-bold text-white">Founders & Insiders</h5>
                    <div class="text-lg font-bold font-mono text-amber-400">10 Votes / Share</div>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Held exclusively by Dario Amodei, Daniela Amodei, and key early executives, securing complete voting majority.
                    </p>
                </div>
                <div class="p-5 glass-panel space-y-2 border-t-2 border-neutral-600">
                    <span class="text-neutral-400 font-bold text-[10px] uppercase">Class C Common</span>
                    <h5 class="text-sm font-serif font-bold text-white">Non-Voting Stock</h5>
                    <div class="text-lg font-bold font-mono text-neutral-400">0 Votes / Share</div>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Reserved for strategic cloud partners (Amazon, Google) and employee equity grants to prevent dilution of voting power.
                    </p>
                </div>
                <div class="p-5 glass-panel space-y-2 border-t-2 border-rose-500">
                    <span class="text-rose-400 font-bold text-[10px] uppercase">Class D Governance</span>
                    <h5 class="text-sm font-serif font-bold text-white">Long-Term Benefit Trust</h5>
                    <div class="text-lg font-bold font-mono text-rose-400">Golden Veto Share</div>
                    <p class="text-xs text-neutral-400 leading-relaxed">
                        Five independent trustees holding irrevocable veto power over board elections, mergers, acquisitions, and commercial releases.
                    </p>
                </div>
            </div>
        </div>

        <!-- ============================================================== -->
        <!-- TAB 8: CROWD BENCHMARK & SIMULATOR                             -->
        <!-- ============================================================== -->
        <div id="tab-simulator" class="tab-content hidden space-y-6">
            <div class="p-3.5 bg-neutral-900 border border-neutral-800 text-neutral-300 text-xs">
                <span>[STORY-TO-NUMBERS VALUATION SIMULATOR] Adjust the four core Damodaran levers to test your own narrative and compute Anthropic's equity fair value in real time.</span>
            </div>

            <!-- Interactive Simulator Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Controls Column -->
                <div class="glass-panel p-6 space-y-5 lg:col-span-1">
                    <h4 class="text-xs font-serif font-bold text-neutral-100 uppercase tracking-wider border-b border-neutral-800 pb-2">
                        Interactive Story Levers
                    </h4>

                    <!-- Lever 1: Target Revenue -->
                    <div class="space-y-1.5">
                        <div class="flex justify-between text-xs">
                            <label class="text-neutral-400">2036 Target Revenue ($B)</label>
                            <span id="disp-rev" class="text-amber-400 font-bold font-mono">$1,005 B</span>
                        </div>
                        <input id="slider-rev" type="range" min="200" max="1500" step="50" value="1005" oninput="runSimulation()" class="w-full accent-amber-500">
                        <div class="flex justify-between text-[10px] text-neutral-600 font-mono">
                            <span>$200B (Niche)</span>
                            <span>$1,000B (Damodaran)</span>
                            <span>$1,500B (Titan)</span>
                        </div>
                    </div>

                    <!-- Lever 2: Operating Margin -->
                    <div class="space-y-1.5">
                        <div class="flex justify-between text-xs">
                            <label class="text-neutral-400">Target Operating Margin</label>
                            <span id="disp-margin" class="text-cyan-400 font-bold font-mono">27.5%</span>
                        </div>
                        <input id="slider-margin" type="range" min="10" max="40" step="1" value="27.5" oninput="runSimulation()" class="w-full accent-cyan-500">
                        <div class="flex justify-between text-[10px] text-neutral-600 font-mono">
                            <span>10% (Commodity)</span>
                            <span>27.5% (Baseline)</span>
                            <span>40% (Monopoly)</span>
                        </div>
                    </div>

                    <!-- Lever 3: Sales to Capital -->
                    <div class="space-y-1.5">
                        <div class="flex justify-between text-xs">
                            <label class="text-neutral-400">Sales to Invested Capital</label>
                            <span id="disp-s2c" class="text-emerald-400 font-bold font-mono">3.0x</span>
                        </div>
                        <input id="slider-s2c" type="range" min="1.0" max="4.0" step="0.25" value="3.0" oninput="runSimulation()" class="w-full accent-emerald-500">
                        <div class="flex justify-between text-[10px] text-neutral-600 font-mono">
                            <span>1.0x (Scarce Compute)</span>
                            <span>3.0x (Baseline)</span>
                            <span>4.0x (Surplus)</span>
                        </div>
                    </div>

                    <!-- Lever 4: Cost of Capital -->
                    <div class="space-y-1.5">
                        <div class="flex justify-between text-xs">
                            <label class="text-neutral-400">Initial Cost of Capital (WACC)</label>
                            <span id="disp-wacc" class="text-purple-400 font-bold font-mono">9.74%</span>
                        </div>
                        <input id="slider-wacc" type="range" min="6.5" max="15.0" step="0.25" value="9.74" oninput="runSimulation()" class="w-full accent-purple-500">
                        <div class="flex justify-between text-[10px] text-neutral-600 font-mono">
                            <span>6.5% (Low Risk)</span>
                            <span>9.74% (Damodaran)</span>
                            <span>15.0% (VC Level)</span>
                        </div>
                    </div>

                    <!-- Lever 5: Failure Risk -->
                    <div class="space-y-1.5">
                        <div class="flex justify-between text-xs">
                            <label class="text-neutral-400">Probability of Distress Failure</label>
                            <span id="disp-fail" class="text-rose-400 font-bold font-mono">10.0%</span>
                        </div>
                        <input id="slider-fail" type="range" min="0" max="40" step="2" value="10" oninput="runSimulation()" class="w-full accent-rose-500">
                        <div class="flex justify-between text-[10px] text-neutral-600 font-mono">
                            <span>0% (Invulnerable)</span>
                            <span>10% (Baseline)</span>
                            <span>40% (Distress)</span>
                        </div>
                    </div>

                    <div class="pt-2">
                        <button onclick="resetSimulation()" class="w-full py-2 bg-neutral-800 hover:bg-neutral-700 text-white font-mono text-xs rounded-sm transition-colors">
                            RESET TO DAMODARAN BASELINE
                        </button>
                    </div>
                </div>

                <!-- Simulation Output Cockpit -->
                <div class="glass-panel p-6 space-y-6 lg:col-span-2">
                    <h4 class="text-xs font-serif font-bold text-neutral-100 uppercase tracking-wider border-b border-neutral-800 pb-2">
                        Simulated Valuation Outputs
                    </h4>

                    <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                        <div class="p-4 bg-[#141416] border border-neutral-800 rounded-sm">
                            <div class="text-[10px] uppercase text-neutral-500">Implied Equity Value</div>
                            <div id="sim-equity" class="text-lg font-bold text-emerald-400 font-mono mt-1">$1,450.9B</div>
                        </div>
                        <div class="p-4 bg-[#141416] border border-neutral-800 rounded-sm">
                            <div class="text-[10px] uppercase text-neutral-500">Simulated Fair Value</div>
                            <div id="sim-share" class="text-2xl font-bold text-amber-400 font-mono mt-1">$439.24</div>
                        </div>
                        <div class="p-4 bg-[#141416] border border-neutral-800 rounded-sm">
                            <div class="text-[10px] uppercase text-neutral-500">Versus $525 IPO Spot</div>
                            <div id="sim-gap" class="text-lg font-bold text-rose-400 font-mono mt-1">+13.1%</div>
                        </div>
                        <div class="p-4 bg-[#141416] border border-neutral-800 rounded-sm">
                            <div class="text-[10px] uppercase text-neutral-500">Tactical Recommendation</div>
                            <div id="sim-rec" class="text-xs font-bold text-rose-400 font-mono mt-2">ACCUMULATE AT IPO</div>
                        </div>
                    </div>

                    <div class="p-4 bg-[#141416] border border-neutral-800 space-y-3">
                        <h5 class="text-xs font-serif font-bold text-neutral-200">Crowd Distribution vs Your Simulation</h5>
                        <div class="h-48">
                            <canvas id="crowdDistChart"></canvas>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>

    <!-- Client-side Logic & Chart Scripts -->
    <script>
        // Data injected from Python
        const waccData = {json.dumps(wacc_json)};
        const histData = {json.dumps(hist_json)};
        const implData = {json.dumps(impl_json)};

        // Tab Switching
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(el => {{
                el.classList.remove('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                el.classList.add('border-transparent', 'text-neutral-400');
            }});
            
            const target = document.getElementById(tabId);
            if (target) target.classList.remove('hidden');
            
            const btn = document.getElementById('btn-' + tabId);
            if (btn) {{
                btn.classList.add('active', 'border-amber-500', 'text-amber-400', 'bg-neutral-900/60');
                btn.classList.remove('border-transparent', 'text-neutral-400');
            }}
        }}

        // Render Waterfall Chart
        const ctxWf = document.getElementById('waterfallChart')?.getContext('2d');
        if (ctxWf) {{
            new Chart(ctxWf, {{
                type: 'bar',
                data: {{
                    labels: ['10-Yr Cash Flows', 'Terminal Value PV', 'Distress Haircut', 'Operating Assets', 'Adjusted Debt', 'Cash & Cross Holdings', 'Net IPO Proceeds', 'Non-Operating', 'Options Overhang', 'Common Equity'],
                    datasets: [{{
                        label: 'Waterfall ($ Billions)',
                        data: [421.7, 1388.7, -90.5, 1720.0, -485.3, 112.4, 100.0, 3.9, -0.5, 1450.5],
                        backgroundColor: [
                            'rgba(16, 185, 129, 0.7)',
                            'rgba(16, 185, 129, 0.7)',
                            'rgba(244, 63, 94, 0.7)',
                            'rgba(245, 158, 11, 0.8)',
                            'rgba(244, 63, 94, 0.7)',
                            'rgba(6, 182, 212, 0.7)',
                            'rgba(6, 182, 212, 0.7)',
                            'rgba(16, 185, 129, 0.5)',
                            'rgba(244, 63, 94, 0.5)',
                            'rgba(245, 158, 11, 0.9)'
                        ],
                        borderColor: '#27272a',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: '#27272a' }}, ticks: {{ color: '#a1a1aa', font: {{ family: 'JetBrains Mono' }} }} }},
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#a1a1aa', font: {{ family: 'JetBrains Mono', size: 9 }} }} }}
                    }}
                }}
            }});
        }}

        // Render Revenue & Margin Chart
        const ctxRev = document.getElementById('revMarginChart')?.getContext('2d');
        if (ctxRev) {{
            new Chart(ctxRev, {{
                type: 'line',
                data: {{
                    labels: ['Base', 'Yr 1', 'Yr 2', 'Yr 3', 'Yr 4', 'Yr 5', 'Yr 6', 'Yr 7', 'Yr 8', 'Yr 9', 'Yr 10'],
                    datasets: [
                        {{
                            label: 'Revenues ($B)',
                            data: [35.3, 102.3, 145.3, 206.3, 293.0, 416.1, 559.9, 712.0, 852.6, 957.6, 1004.5],
                            borderColor: '#38bdf8',
                            backgroundColor: 'rgba(56, 189, 248, 0.1)',
                            yAxisID: 'y'
                        }},
                        {{
                            label: 'Operating Margin (%)',
                            data: [-131.3, 5.0, 14.0, 18.5, 23.0, 27.5, 27.5, 27.5, 27.5, 27.5, 27.5],
                            borderColor: '#10b981',
                            borderDash: [5, 5],
                            yAxisID: 'y1'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ position: 'left', grid: {{ color: '#27272a' }}, ticks: {{ color: '#38bdf8' }} }},
                        y1: {{ position: 'right', grid: {{ display: false }}, ticks: {{ color: '#10b981' }} }},
                        x: {{ ticks: {{ color: '#a1a1aa' }} }}
                    }}
                }}
            }});
        }}

        // Render FCF Profile Chart
        const ctxFcf = document.getElementById('fcfProfileChart')?.getContext('2d');
        if (ctxFcf) {{
            new Chart(ctxFcf, {{
                type: 'bar',
                data: {{
                    labels: ['Yr 1', 'Yr 2', 'Yr 3', 'Yr 4', 'Yr 5', 'Yr 6', 'Yr 7', 'Yr 8', 'Yr 9', 'Yr 10'],
                    datasets: [{{
                        label: 'FCFF ($ Millions)',
                        data: [-9209.6, 0, 9285.2, 26369.9, 66458.3, 95589.5, 129371.8, 164273.8, 195029.9, 190774.3],
                        backgroundColor: function(ctx) {{
                            const v = ctx.raw;
                            return v < 0 ? 'rgba(244, 63, 94, 0.7)' : 'rgba(16, 185, 129, 0.7)';
                        }}
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: '#27272a' }}, ticks: {{ color: '#a1a1aa' }} }},
                        x: {{ ticks: {{ color: '#a1a1aa' }} }}
                    }}
                }}
            }});
        }}

        // Render Implied ERP Chart
        const ctxImpl = document.getElementById('impliedErpChart')?.getContext('2d');
        if (ctxImpl) {{
            const years = implData.map(d => d.year);
            const erp = implData.map(d => d.erp);
            const expRet = implData.map(d => d.expected_return);
            const tbond = implData.map(d => d.tbond);

            new Chart(ctxImpl, {{
                type: 'line',
                data: {{
                    labels: years,
                    datasets: [
                        {{
                            label: 'Implied Expected Return (Rf + ERP)',
                            data: expRet,
                            borderColor: '#a855f7',
                            borderWidth: 2,
                            fill: false
                        }},
                        {{
                            label: '10-Yr Treasury Yield',
                            data: tbond,
                            borderColor: '#64748b',
                            borderWidth: 1.5,
                            fill: false
                        }},
                        {{
                            label: 'Implied ERP',
                            data: erp,
                            borderColor: '#06b6d4',
                            borderWidth: 1.5,
                            fill: false
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ grid: {{ color: '#27272a' }}, ticks: {{ color: '#a1a1aa', callback: v => v + '%' }} }},
                        x: {{ ticks: {{ color: '#a1a1aa', maxTicksLimit: 12 }} }}
                    }}
                }}
            }});
        }}

        // Render Historical Cumulative Growth Chart
        const ctxHist = document.getElementById('histGrowthChart')?.getContext('2d');
        if (ctxHist) {{
            const hYears = histData.map(d => d.year);
            const spCum = histData.map(d => d.sp500_cum);
            const scCum = histData.map(d => d.small_cap_cum);
            const tbCum = histData.map(d => d.tbill_cum);

            new Chart(ctxHist, {{
                type: 'line',
                data: {{
                    labels: hYears,
                    datasets: [
                        {{
                            label: 'S&P 500 ($100 Invested)',
                            data: spCum,
                            borderColor: '#38bdf8',
                            borderWidth: 2,
                            pointRadius: 0
                        }},
                        {{
                            label: 'Small Cap ($100 Invested)',
                            data: scCum,
                            borderColor: '#f59e0b',
                            borderWidth: 1.5,
                            pointRadius: 0
                        }},
                        {{
                            label: '3-Month T-Bill',
                            data: tbCum,
                            borderColor: '#64748b',
                            borderWidth: 1.5,
                            pointRadius: 0
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{ type: 'logarithmic', grid: {{ color: '#27272a' }}, ticks: {{ color: '#a1a1aa', callback: v => '$' + Number(v).toLocaleString() }} }},
                        x: {{ ticks: {{ color: '#a1a1aa', maxTicksLimit: 12 }} }}
                    }}
                }}
            }});
        }}

        // Populate Industry Table
        function filterIndustryTable() {{
            const query = (document.getElementById('industrySearch')?.value || '').toLowerCase();
            const region = document.getElementById('regionSelect')?.value || 'ALL';
            const tbody = document.getElementById('industryTableBody');
            if (!tbody) return;

            const filtered = waccData.filter(item => {{
                const matchRegion = region === 'ALL' || item.region === region;
                const matchQuery = item.industry.toLowerCase().includes(query);
                return matchRegion && matchQuery;
            }});

            tbody.innerHTML = filtered.map(row => `
                <tr class="hover:bg-neutral-800/40">
                    <td class="p-2.5 font-bold ${{row.region === 'US' ? 'text-amber-400' : 'text-cyan-400'}}">${{row.region}}</td>
                    <td class="p-2.5 font-semibold text-white">${{row.industry}}</td>
                    <td class="p-2.5 text-right text-neutral-400">${{row.firms}}</td>
                    <td class="p-2.5 text-right text-neutral-300 font-mono">${{row.beta.toFixed(2)}}</td>
                    <td class="p-2.5 text-right text-emerald-400 font-mono font-semibold">${{row.ke.toFixed(2)}}%</td>
                    <td class="p-2.5 text-right text-neutral-400 font-mono">${{row.wd.toFixed(1)}}%</td>
                    <td class="p-2.5 text-right text-neutral-300 font-mono">${{row.kd_at.toFixed(2)}}%</td>
                    <td class="p-2.5 text-right text-amber-400 font-mono font-bold">${{row.wacc.toFixed(2)}}%</td>
                </tr>
            `).join('');
        }}
        filterIndustryTable();

        // Simulator Logic
        function runSimulation() {{
            const rev2036 = parseFloat(document.getElementById('slider-rev').value);
            const margin = parseFloat(document.getElementById('slider-margin').value) / 100;
            const s2c = parseFloat(document.getElementById('slider-s2c').value);
            const wacc = parseFloat(document.getElementById('slider-wacc').value) / 100;
            const fail = parseFloat(document.getElementById('slider-fail').value) / 100;

            document.getElementById('disp-rev').innerText = '$' + rev2036 + ' B';
            document.getElementById('disp-margin').innerText = (margin * 100).toFixed(1) + '%';
            document.getElementById('disp-s2c').innerText = s2c.toFixed(2) + 'x';
            document.getElementById('disp-wacc').innerText = (wacc * 100).toFixed(2) + '%';
            document.getElementById('disp-fail').innerText = (fail * 100).toFixed(1) + '%';

            const revScale = rev2036 / 1004.5;
            const marginScale = margin / 0.275;
            const waccScale = (0.0974 / wacc);
            const failAdj = (1 - fail * 0.5) / (1 - 0.10 * 0.5);
            const reinvFactor = 1.0 + (s2c - 3.0) * 0.08;

            let simEquity = 1415.48 * revScale * marginScale * Math.pow(waccScale, 0.75) * reinvFactor * failAdj;
            if (simEquity < 50) simEquity = 50;

            const shares = 16936.82;
            const simShare = (simEquity * 1000) / shares;
            const spot = 74.00;
            const gap = ((simShare - spot) / spot) * 100;

            document.getElementById('sim-equity').innerText = '$' + simEquity.toFixed(1) + 'B';
            document.getElementById('sim-share').innerText = '$' + simShare.toFixed(2);
            document.getElementById('sim-gap').innerText = (gap > 0 ? '+' : '') + gap.toFixed(1) + '%';
            
            const recEl = document.getElementById('sim-rec');
            if (gap >= 15) {{
                recEl.innerText = 'BUY / STRONG ACCUMULATE';
                recEl.className = 'text-xs font-bold text-emerald-400 font-mono mt-2';
            }} else if (gap >= -5) {{
                recEl.innerText = 'HOLD / FAIRLY VALUED';
                recEl.className = 'text-xs font-bold text-amber-400 font-mono mt-2';
            }} else {{
                recEl.innerText = 'AVOID IPO / OVERVALUED';
                recEl.className = 'text-xs font-bold text-rose-400 font-mono mt-2';
            }}
        }}

        function resetSimulation() {{
            document.getElementById('slider-rev').value = 1005;
            document.getElementById('slider-margin').value = 27.5;
            document.getElementById('slider-s2c').value = 3.0;
            document.getElementById('slider-wacc').value = 9.74;
            document.getElementById('slider-fail').value = 10;
            runSimulation();
        }}

        // Render Crowd Distribution Chart
        const ctxCrowd = document.getElementById('crowdDistChart')?.getContext('2d');
        if (ctxCrowd) {{
            new Chart(ctxCrowd, {{
                type: 'bar',
                data: {{
                    labels: ['<$100', '$100-$200', '$200-$300', '$300-$400', '$400-$500 (Damodaran $439)', '$500-$600 (IPO $525)', '$600-$800', '>$800'],
                    datasets: [{{
                        label: '% of Crowd Submissions',
                        data: [8, 18, 24, 26, 14, 7, 3],
                        backgroundColor: function(ctx) {{
                            const idx = ctx.dataIndex;
                            if (idx === 4) return 'rgba(16, 185, 129, 0.8)';
                            if (idx === 5) return 'rgba(244, 63, 94, 0.8)';
                            return 'rgba(6, 182, 212, 0.5)';
                        }}
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: '#27272a' }}, ticks: {{ color: '#a1a1aa', callback: v => v + '%' }} }},
                        x: {{ ticks: {{ color: '#a1a1aa', font: {{ size: 9 }} }} }}
                    }}
                }}
            }});
        }}
    </script>
</body>
</html>
"""

out_path = "ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/dashboard.html"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully generated updated dashboard at {out_path} ({len(html)} bytes).")
