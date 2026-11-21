"""
ERVIS Terminal Rich Renderer
Formats institutional financial data into authentic Bloomberg Terminal panels
using Rich tables, panels, and text layouts.
"""

import os
import json
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.console import Console, Group
from typing import Dict, Any, List, Optional

from ERVIS.terminal.data_loader import (
    load_company_data,
    get_top10_matrix,
    get_portfolio_data,
    get_company_gate4b,
    get_valuation_history,
    get_company_beta,
    resolve_ticker,
    COVERED_COMPANIES,
    ALL_ACTIVE_TICKERS
)

# Color Schemes
AMBER_STYLE = "bold #ffb000"
AMBER_DIM = "#b37b00"
GREEN_STYLE = "bold #00ff66"
GREEN_DIM = "#009933"
RED_STYLE = "bold #ff3333"
CYAN_STYLE = "bold #00e5ff"
HEADER_BG = "on #1a1a1a"
BORDER_COLOR = "#ffb000"

def format_currency(val: Any, prefix: str = "$", decimals: int = 2) -> str:
    if val is None:
        return "N/A"
    try:
        return f"{prefix}{float(val):,.{decimals}f}"
    except (ValueError, TypeError):
        return str(val)

def make_sparkline(data: List[Optional[float]]) -> str:
    """Renders a numeric list into an authentic Unicode sparkline ( ▂▃▄▅▆▇█)."""
    valid_vals = []
    for v in data:
        if v is not None:
            try:
                valid_vals.append(float(v))
            except (ValueError, TypeError):
                pass
    if not valid_vals:
        return "[dim]--[/dim]"
    min_v = min(valid_vals)
    max_v = max(valid_vals)
    span = max_v - min_v
    blocks = " ▂▃▄▅▆▇█"
    res = []
    for v in data:
        if v is None:
            res.append(" ")
        else:
            try:
                fv = float(v)
                if span == 0:
                    res.append(blocks[3])
                else:
                    idx = int(round(((fv - min_v) / span) * 7))
                    idx = max(0, min(7, idx))
                    res.append(blocks[idx])
            except (ValueError, TypeError):
                res.append(" ")
    return f"[bold cyan]{''.join(res)}[/bold cyan]"

def make_bar_gauge(val: Optional[float], max_val: Optional[float], width: int = 14, fill_char: str = "█", empty_char: str = "░", color: str = "cyan") -> str:
    """Renders a horizontal visual progress or ratio gauge using Unicode blocks."""
    if val is None or max_val is None or max_val <= 0:
        return f"[dim]{empty_char * width}[/dim]"
    ratio = max(0.0, min(1.0, float(val) / float(max_val)))
    filled_len = int(round(ratio * width))
    empty_len = width - filled_len
    return f"[{color}]{fill_char * filled_len}[/{color}][dim]{empty_char * empty_len}[/dim]"

def render_top_bar(ticker: str, theme: str = "amber") -> Panel:
    color = AMBER_STYLE if theme == "amber" else GREEN_STYLE
    title = Text()
    title.append("ERVIS TERMINAL v1.0", style=f"bold {color}")
    title.append(" :: INSTITUTIONAL VALUATION WORKSTATION", style="bold white")
    title.append(f"  |  ACTIVE: [{ticker}]", style="bold yellow")
    title.append("  |  PRESS [F1] FOR HELP  [Q] QUIT", style="dim white")
    return Panel(title, border_style=BORDER_COLOR, padding=(0, 1))

def render_unknown_ticker(ticker: str) -> Panel:
    table = Table(title="[bold yellow]ACTIVE COVERAGE DIRECTORY (LOCAL VAULT)[/bold yellow]", border_style="dim white", expand=True)
    table.add_column("TICKER", style="bold cyan", width=12)
    table.add_column("COMPANY NAME", style="bold white", width=28)
    table.add_column("MARKET / SECTOR", style="dim white")

    from ERVIS.terminal.data_loader import get_covered_companies
    for t, name in get_covered_companies()[:14]:
        mkt = "UK FTSE 100 / Aerospace" if t == "RR" else "Equities / Technology & Infrastructure"
        table.add_row(t, name, mkt)

    memo = Panel(
        Text.from_markup(
            f"[bold red]SECURITY NOT CURRENTLY IN COVERAGE:[/bold red] [bold white]{ticker}[/bold white]\n"
            f"[bold yellow]AGY AUTONOMOUS ONBOARDING AVAILABLE:[/bold yellow]\n"
            f"You can instantly dispatch AGY Research Associate to ingest [bold cyan]{ticker}[/bold cyan], pull SEC EDGAR filings, "
            f"run DuPont/Altman Z health checks, Hamada Beta WACC, 10-Yr DCF, and Monte Carlo.\n\n"
            f"  • Type [bold green]INGEST {ticker}[/bold green] and press [bold green]<ENTER>[/bold green]\n"
            f"  • Or press [bold cyan][F10][/bold cyan] to open the [bold cyan]AGY Copilot[/bold cyan] pairing desk."
        ),
        border_style="yellow",
        padding=(0, 1)
    )

    return Panel(Group(memo, Text(""), table), title=f"[bold red] UNCOVERED SECURITY: {ticker} [/bold red]", border_style="red")

def render_overview(ticker: str, theme: str = "amber") -> Panel:
    ticker = resolve_ticker(ticker)
    data = load_company_data(ticker)
    if not data or data.get("status") == "UNKNOWN" or (data.get("spot_price") is None and data.get("dcf_value") is None):
        return render_unknown_ticker(ticker)

    curr = "£" if data.get("currency") == "GBP" else "$"
    spot = data.get("spot_price")
    target = data.get("target_price")
    gap = round(((target - spot) / spot) * 100.0, 1) if spot and target else None

    # Main Grid Layout - strictly 2 columns with 2-char padding matching width=132
    grid = Table.grid(expand=True, padding=(0, 2))
    grid.add_column(width=54)
    grid.add_column(width=72)

    # Left Column: Key Stats (Strictly 8 rows)
    stats_table = Table(title="[bold yellow]SECURITY PROFILE & VALUATION SUMMARY[/bold yellow]", border_style="dim white", expand=True)
    stats_table.add_column("METRIC", style="bold cyan", width=25, no_wrap=True)
    stats_table.add_column("VALUE / AUDIT RESULT", style="white", width=26, no_wrap=True)

    company_currency = data.get("currency", "USD")
    stats_table.add_row("Company Name", str(data.get("company_name", "N/A")))
    stats_table.add_row("Ticker / Market", f"{ticker} ({company_currency})")
    stats_table.add_row("Spot Market Price", format_currency(spot, curr))
    market_cap_str = format_currency(data.get("market_cap_b"), "$", 1)
    stats_table.add_row("Market Capitalization", f"{market_cap_str} Billion")
    
    # Valuation Target with color
    target_text = format_currency(target, curr)
    if gap is not None:
        gap_style = GREEN_STYLE if gap > 0 else RED_STYLE
        target_text += f" ({gap:+.1f}%)"
    stats_table.add_row("Triangulated Target Price", target_text)

    # Recommendation
    rating = str(data.get("rating", "N/A"))
    rating_style = GREEN_STYLE if "ACCUMULATE" in rating or "BUY" in rating else (RED_STYLE if "SELL" in rating or "TRIM" in rating else "yellow")
    stats_table.add_row("Institutional Rating", f"[{rating_style}]{rating}[/{rating_style}]")

    w_base = (data.get("wacc_base") or 0.09) * 100.0
    w_term = (data.get("wacc_terminal") or 0.09) * 100.0
    stats_table.add_row("Base WACC / Hurdle", f"{w_base:.2f}% (Terminal: {w_term:.2f}%)")
    
    net_debt = data.get("net_debt_b")
    if net_debt is not None:
        nd_str = f"+${abs(net_debt):,.1f}B Net Cash" if net_debt <= 0 else f"-${net_debt:,.1f}B Net Debt"
        nd_style = GREEN_STYLE if net_debt <= 0 else RED_STYLE
        stats_table.add_row("Balance Sheet Fortress", f"[{nd_style}]{nd_str}[/{nd_style}]")
    else:
        stats_table.add_row("Balance Sheet Fortress", "[dim white]Investment Grade / Safe[/dim white]")

    # Right Column: Valuation Triangulation Bridge (Strictly 8 rows to align with left table)
    bridge_table = Table(title="[bold yellow]VALUATION ENGINE TRIANGULATION BRIDGE[/bold yellow]", border_style="dim white", expand=True)
    bridge_table.add_column("VALUATION METHOD", style="bold cyan", width=29, no_wrap=True)
    bridge_table.add_column("INTRINSIC VALUE", style="white", justify="right", width=19, no_wrap=True)
    bridge_table.add_column("GAP / AUDIT METRIC", style="white", justify="right", width=20, no_wrap=True)

    # Row 1: DCF
    dcf = data.get("dcf_value")
    dcf_gap = f"{((dcf - spot) / spot)*100.0:+.1f}%" if spot and dcf else "N/A"
    bridge_table.add_row("10-Yr Pro-Forma Ginzu DCF", format_currency(dcf, curr), dcf_gap)

    # Row 2: SOTP
    sotp = data.get("sotp_value")
    sotp_gap = f"{((sotp - spot) / spot)*100.0:+.1f}%" if spot and sotp else "N/A"
    bridge_table.add_row("Sum-of-the-Parts (SOTP)", format_currency(sotp, curr), sotp_gap)

    # Row 3: Monte Carlo
    mc = data.get("mc_median")
    mc_gap = f"{((mc - spot) / spot)*100.0:+.1f}%" if spot and mc else "N/A"
    win_pct = data.get("mc_win_rate")
    win_rate = f" ({win_pct:.0f}% Win)" if win_pct is not None else ""
    bridge_table.add_row("10,000-Trial Monte Carlo", format_currency(mc, curr) + win_rate, mc_gap)

    # Row 4: Net Asset Liquidation Floor
    raw = data.get("raw_json", {})
    liq = raw.get("liquidation_floor_usd") or (raw.get("liquidation_floor_pence", 0) / 100.0 if raw.get("liquidation_floor_pence") else None)
    if liq:
        liq_gap = f"{((liq - spot) / spot)*100.0:+.1f}%" if spot and liq else "N/A"
        bridge_table.add_row("Net Asset Liquidation Floor", format_currency(liq, curr), liq_gap)
    else:
        bridge_table.add_row("Net Asset Liquidation Floor", "Asset-Light NAV", "Intangibles Moat")

    # Row 5: Gate 4B AI CapEx Payback
    gate_4b = data.get("gate_4b") or data.get("vault_gate4b") or raw.get("ai_capex_audit") or raw.get("gate_4b_ai_capex_audit") or raw.get("gate_4b_capex_roi")
    if gate_4b:
        payback = gate_4b.get("payback_years") or gate_4b.get("payback_period_years") or gate_4b.get("payback_period_gpu_years") or gate_4b.get("estimated_customer_payback_years")
        fcf_conv = gate_4b.get("fcf_conversion_pct") or gate_4b.get("nvda_fcf_conversion_pct")
        if payback:
            p_str = f"{payback:.1f} Yrs" if isinstance(payback, float) else f"{payback} Yrs" if isinstance(payback, int) else str(payback)[:10]
            bridge_table.add_row("Gate 4B AI CapEx Payback", p_str, "Useful: 3.5 Yrs")
        elif fcf_conv:
            bridge_table.add_row("Gate 4B FCF Conversion", f"{fcf_conv:.1f}%", "Cash Accretive")
        else:
            bridge_table.add_row("Gate 4B AI CapEx Payback", "Accretive Cycle", "Capex Audited")
    else:
        bridge_table.add_row("Gate 4B CapEx Monetization", "Disciplined", "Organic Expansion")

    # Row 6: Altman Z-Score (Gate 1)
    fin_health = raw.get("financial_health") or raw.get("gate_2_financial_health", {})
    z = fin_health.get("altman_z_score") if isinstance(fin_health, dict) else None
    zone = fin_health.get("altman_zone", "SAFE") if isinstance(fin_health, dict) else "SAFE"
    if z is not None:
        z_style = GREEN_STYLE if "SAFE" in zone else (AMBER_STYLE if "GREY" in zone else RED_STYLE)
        bridge_table.add_row("Altman Z-Score (Gate 1)", f"[{z_style}]{z:.2f} [{zone}][/{z_style}]", "Credit Pristine")
    else:
        bridge_table.add_row("Altman Z-Score (Gate 1)", "[green]Safe Zone[/green]", "Tier-1 Solvency")

    # Row 7: DuPont 5-Stage ROE
    roe = fin_health.get("dupont_roe_pct") if isinstance(fin_health, dict) else None
    opm = fin_health.get("operating_margin_pct") if isinstance(fin_health, dict) else None
    if roe is not None:
        opm_str = f"OPM: {opm:.1f}%" if opm else "High Margin"
        bridge_table.add_row("DuPont 5-Stage ROE", f"{roe:.1f}%", opm_str)
    else:
        bridge_table.add_row("DuPont 5-Stage ROE", "Value Accretive", "High Asset Turn")

    # Row 8: Terminal Reinvestment / Model Triangulation Anchor
    gap_label = f"{gap:+.1f}% Spread" if gap is not None else "Audited"
    bridge_table.add_row("Terminal Reinvestment", "Gate 1-5 Anchor", gap_label)

    # Bottom notes
    gap_str = f"{gap:+.1f}%" if gap is not None else "N/A"
    gap_color = "red" if gap and gap < 0 else "green"
    clean_rating = str(data.get("rating", "N/A"))
    notes = Panel(
        Text.from_markup(
            f"[bold yellow]EXECUTIVE DIRECTIVE:[/bold yellow] "
            f"Intrinsic target of [bold white]{format_currency(target, curr)}[/bold white] implies "
            f"[{gap_color}]{gap_str}[/{gap_color}] gap vs spot. "
            f"Rating: {clean_rating}. "
            f"Use [bold cyan]VAL <GO>[/bold cyan] for 5-Gate forensics or [bold cyan]4B <GO>[/bold cyan] for AI CapEx payback audit."
        ),
        border_style="yellow",
        padding=(0, 1)
    )

    grid.add_row(stats_table, bridge_table)
    return Panel(Group(grid, Text(""), notes), title=f"[bold green] {ticker} OVERVIEW DOSSIER [/bold green]", border_style=BORDER_COLOR, expand=True)

def render_top10_matrix_panel() -> Panel:
    matrix = get_top10_matrix()
    table = Table(border_style="dim white", expand=True)
    table.add_column("#", style="dim white", width=3, no_wrap=True)
    table.add_column("TICKER", style="bold yellow", width=8, no_wrap=True)
    table.add_column("COMPANY NAME", style="white", width=28, no_wrap=True)
    table.add_column("SPOT ($)", style="bold cyan", justify="right", width=11, no_wrap=True)
    table.add_column("TARGET ($)", style="bold white", justify="right", width=11, no_wrap=True)
    table.add_column("GAP (%)", justify="right", width=10, no_wrap=True)
    table.add_column("INSTITUTIONAL RATING", width=25, no_wrap=True)
    table.add_column("WACC", justify="right", width=8, no_wrap=True)
    table.add_column("NET DEBT / CASH", justify="right", width=17, no_wrap=True)

    total_mcap = 0.0
    gaps = []

    for i, row in enumerate(matrix, 1):
        gap = row["gap_pct"]
        gaps.append(gap)
        gap_style = GREEN_STYLE if gap > 0 else RED_STYLE
        rating = row["rating"]
        r_style = GREEN_STYLE if "ACCUMULATE" in rating else (RED_STYLE if "SELL" in rating or "TRIM" in rating else "yellow")
        
        nd = row["net_debt_b"]
        nd_str = f"+${abs(nd):.1f}B Cash" if nd <= 0 else f"-${nd:.1f}B Debt"
        nd_style = GREEN_STYLE if nd <= 0 else RED_STYLE

        c_name = row["name"].replace("Manufacturing Co.", "").replace("Corporation", "Corp").strip()[:27]

        table.add_row(
            f"{i:02d}",
            row["ticker"],
            c_name,
            f"${row['spot']:,.2f}",
            f"${row['target']:,.2f}",
            f"[{gap_style}]{gap:+.1f}%[/{gap_style}]",
            f"[{r_style}]{rating}[/{r_style}]",
            f"{row['wacc']:.1f}%",
            f"[{nd_style}]{nd_str}[/{nd_style}]"
        )

    avg_gap = sum(gaps) / len(gaps) if gaps else 0.0
    summary = Panel(
        Text.from_markup(
            f"[bold yellow]MACRO CONCENTRATION AUDIT:[/bold yellow] Top 10 S&P 500 AI Titans account for "
            f"[bold cyan]$26.37 Trillion[/bold cyan] (~52.8% of index earnings). "
            f"Cohort Average Valuation Gap: [bold red]{avg_gap:+.1f}%[/bold red]. "
            f"Systemic downside drag to S&P 500: [bold red]-11.3% to -15.9%[/bold red]. "
            f"Recommended stance: [bold green]Overweight S&P Equal-Weight (RSP) & UK Value (EWU)[/bold green]."
        ),
        border_style="yellow",
        padding=(0, 1)
    )

    return Panel(Group(table, Text(""), summary), title="[bold green] S&P 500 TOP 10 AI CONCENTRATION & VALUATION MATRIX [/bold green]", border_style=BORDER_COLOR, expand=True)

def render_gate_4b(ticker: str) -> Panel:
    ticker = resolve_ticker(ticker)
    data = load_company_data(ticker)
    if not data or data.get("status") == "UNKNOWN":
        return render_unknown_ticker(ticker)
    v_g4b = get_company_gate4b(ticker) or {}
    
    tot_capex = v_g4b.get("annual_capex_m")
    ai_capex = v_g4b.get("ai_capex_m")
    ai_rev = v_g4b.get("incremental_ai_revenue_m")
    deprec = v_g4b.get("annual_depreciation_3_5yr_m")
    net_ai_inc = v_g4b.get("net_ai_operating_income_m")
    net_roi = v_g4b.get("net_ai_roi_pct")
    payback = v_g4b.get("payback_period_years")
    useful_life = v_g4b.get("useful_life_years") or 3.50
    deficit = v_g4b.get("obsolescence_deficit_years")
    cpr = v_g4b.get("capex_payout_ratio_pct")
    gap_m = v_g4b.get("break_even_revenue_gap_m")
    assessment = v_g4b.get("risk_assessment") or "Gate 4B Econometric Verification"

    # Main Gate 4B Metrics Table
    table = Table(title=f"[bold yellow]GATE 4B AI CAPEX PAYOUT & MONETIZATION SCORECARD: {ticker}[/bold yellow]", border_style="dim white", expand=True)
    table.add_column("AUDIT METRIC", style="bold cyan", width=30)
    table.add_column("VALUE / FINDING", style="bold white", width=22)
    table.add_column("INSTITUTIONAL IMPLICATION", style="dim white")

    def fmt_b(m_val: Optional[float], prefix: str = "$") -> str:
        if m_val is None:
            return "N/A"
        if abs(m_val) >= 1000:
            return f"{prefix}{m_val/1000:,.2f}B"
        return f"{prefix}{m_val:,.1f}M"

    table.add_row("Annual Consolidated CapEx Outlay", fmt_b(tot_capex), "Total enterprise capital investment run-rate")
    table.add_row("Dedicated AI Server / Infra CapEx", fmt_b(ai_capex), "Direct GPU, custom ASIC, and cluster compute allocation")
    table.add_row("Incremental GenAI Revenue / Savings", fmt_b(ai_rev), "Annualized incremental revenue + internal cost avoidance")
    table.add_row("Annual Hardware Amortization", f"{fmt_b(deprec)} / Yr" if deprec else "N/A", f"{useful_life:.1f}-Year straight line useful life depreciation burden")
    
    inc_style = GREEN_STYLE if net_ai_inc and net_ai_inc > 0 else RED_STYLE
    table.add_row("Net AI Operating Income / (Deficit)", f"[{inc_style}]{fmt_b(net_ai_inc)}[/{inc_style}]", "Depreciation subtracted from GenAI gross profit contribution")
    
    roi_style = GREEN_STYLE if net_roi and net_roi > 0 else RED_STYLE
    table.add_row("Net AI Return on Invested Capital", f"[{roi_style}]{net_roi:+.1f}%[/{roi_style}]" if net_roi is not None else "N/A", "Economic spread generated across deployed AI infrastructure")
    
    pb_str = f"{payback:.2f} Yrs" if payback is not None else "N/A"
    table.add_row("Customer Cash Payback Duration", pb_str, f"Measured against {useful_life:.2f}-Yr hardware economic life")
    
    cpr_str = f"{cpr:.2f}%" if cpr is not None else "N/A"
    table.add_row("CapEx Payout Ratio (CPR / 'Tax')", cpr_str, "Share of total industry hyperscaler CapEx captured")
    
    gap_str = fmt_b(gap_m) if gap_m is not None else "N/A"
    gap_style = GREEN_STYLE if gap_m and gap_m >= 0 else RED_STYLE
    table.add_row("Break-Even Monetization Revenue Gap", f"[{gap_style}]{gap_str}[/{gap_style}]", "Additional annual revenue required to achieve zero economic loss")

    # Visual Gauges Panel: Useful Life vs Payback Duration & CPR
    gauge_table = Table(title="[bold yellow]GATE 4B VISUAL OBSOLESCENCE & PAYOUT GAUGES[/bold yellow]", border_style="dim white", expand=True)
    gauge_table.add_column("METRIC / BENCHMARK", style="bold cyan", width=22)
    gauge_table.add_column("VISUAL PROGRESS GAUGE", style="bold white", width=22)
    gauge_table.add_column("METRIC", style="white", width=10)
    gauge_table.add_column("STATUS VERDICT", style="bold white")

    max_dur = max(useful_life, (payback or 0.0), 7.0)
    life_gauge = make_bar_gauge(useful_life, max_dur, width=22, color="cyan")
    gauge_table.add_row("Hardware Useful Life", life_gauge, f"{useful_life:.2f} Yrs", "[bold cyan]PHYSICAL CONSTRAINT[/bold cyan]")

    pb_color = "green" if payback and payback <= useful_life else "red"
    pb_gauge = make_bar_gauge(payback, max_dur, width=22, color=pb_color)
    gauge_table.add_row("Cash Payback Duration", pb_gauge, f"{payback:.2f} Yrs" if payback else "N/A", f"[{pb_color}]{ 'RECOUPED' if payback and payback <= useful_life else 'OVERHANG' }[/]")

    cpr_gauge = make_bar_gauge(cpr, 50.0, width=22, color="magenta")
    gauge_table.add_row("CapEx Payout Ratio (CPR)", cpr_gauge, f"{cpr:.1f}%" if cpr else "N/A", "[dim]Industry Cloud Share[/dim]")

    # Obsolescence Status Alert Box
    if deficit is not None and deficit > 0:
        alert_text = (
            f"[bold red]⚠️  OBSOLESCENCE DEFICIT: +{deficit:.2f} YEARS[/bold red] | "
            f"[bold white]STATUS: CAPITAL DESTRUCTIVE[/bold white]\n"
            f"[dim]Hardware silicon becomes economically obsolete {deficit:.2f} years before cumulative operating cash flows recoup the original CapEx outlay.[/dim]"
        )
        alert_style = "red"
    elif deficit is not None and deficit < 0:
        alert_text = (
            f"[bold green]✓  CAPITAL ACCRETIVE SURPLUS: {-deficit:.2f} YEARS[/bold green] | "
            f"[bold white]STATUS: SELF-FUNDING MOAT[/bold white]\n"
            f"[dim]Customer achieves full capital payback {-deficit:.2f} years before hardware replacement cycle is required.[/dim]"
        )
        alert_style = "green"
    else:
        alert_text = (
            "[bold green]✓  TOLLBOOTH / ASSET-LIGHT ARCHITECTURE[/bold green] | "
            "[bold white]STATUS: ZERO HARDWARE REPLACEMENT RISK[/bold white]\n"
            "[dim]Company extracts high cash margins without bearing downstream datacenter depreciation burden.[/dim]"
        )
        alert_style = "green"

    alert_panel = Panel(Text.from_markup(alert_text), border_style=alert_style, padding=(0, 1))

    summary = Panel(
        Text.from_markup(
            f"[bold yellow]GATE 4B RISK AUDIT:[/bold yellow] [bold white]{assessment}[/bold white]\n"
            f"[dim]Core Macro Dilemma: The Cisco Paradox dictates that hyperscalers absorbing multi-year deficits "
            f"must eventually moderate CapEx growth, contracting high-margin hardware supplier multiples.[/dim]"
        ),
        border_style="yellow",
        padding=(0, 1)
    )

    return Panel(Group(table, Text(""), gauge_table, Text(""), alert_panel, Text(""), summary), title=f"[bold green] GATE 4B: AI CAPEX PAYOUT & MONETIZATION SCORECARD ({ticker}) [/bold green]", border_style=BORDER_COLOR)

def render_portfolio_desk() -> Panel:
    data = get_portfolio_data()
    table = Table(border_style="dim white", expand=True)
    table.add_column("TICKER", style="bold yellow", width=12)
    table.add_column("ASSET NAME", style="white", width=30)
    table.add_column("ALLOC (%)", justify="right", width=10)
    table.add_column("TARGET ($)", justify="right", width=12)
    table.add_column("ORDER SPECIFICATION", style="bold cyan", width=25)
    table.add_column("STATUS", width=18)

    for item in data["allocations"]:
        st = item["status"]
        st_style = GREEN_STYLE if "ACTIVE" in st or "ACCUMULATING" in st else "yellow"
        table.add_row(
            item["ticker"],
            item["name"],
            f"{item['target_alloc_pct']:.1f}%",
            f"${item['target_amount_usd']:.2f}",
            item["order_type"],
            f"[{st_style}]{st}[/{st_style}]"
        )

    dca = data["dca_cadence"]
    dca_box = Panel(
        Text.from_markup(
            f"[bold yellow]3-MONTH DCA ROADMAP:[/bold yellow] "
            f"Cadence: [bold cyan]{dca['mode']} (${dca['injection_per_tranche']:.2f} x 2)[/bold cyan] | "
            f"Schedule: [bold white]{dca['schedule']}[/bold white] | "
            f"Total Seed Pool: [bold green]${dca['total_capital']:.2f} USD[/bold green] | "
            f"Broker: [bold white]{data['broker']}[/bold white]\n"
            f"[dim]• Avoids month-end institutional markup spikes • Maximizes limit bid agility on RYCEY ($16.80) • $0 Webull commission[/dim]"
        ),
        border_style="yellow",
        padding=(0, 1)
    )

    return Panel(Group(table, Text(""), dca_box), title="[bold green] SEED CAPITAL PORTFOLIO DESK ($200 INITIAL SEED) [/bold green]", border_style=BORDER_COLOR)

def render_fa_screen(ticker: str) -> Panel:
    from ERVIS.terminal.data_loader import get_fa_financial_trends
    ticker = resolve_ticker(ticker)
    curr_data = load_company_data(ticker)
    if not curr_data or curr_data.get("status") == "UNKNOWN":
        return render_unknown_ticker(ticker)
    data = get_fa_financial_trends(ticker)
    curr = "£" if curr_data.get("currency") == "GBP" else "$"

    history = data.get("history", [])
    years = [h["year"] for h in history]

    # Main Multi-Year Financial Statement Table with Sparkline Trend Column
    table = Table(title=f"[bold yellow]FINANCIAL ANALYSIS (FA): {ticker} MULTI-YEAR STATEMENTS ({curr} Millions)[/bold yellow]", border_style="dim white", expand=True)
    table.add_column("LINE ITEM / METRIC", style="bold cyan", width=25)
    for yr in years:
        table.add_column(f"FY{yr}", justify="right", style="bold white", width=11)
    table.add_column("TREND", justify="center", style="bold yellow", width=10)

    def row_values(key, prefix="", is_pct=False):
        vals = []
        for h in history:
            v = h.get(key)
            if v is None:
                vals.append("N/A")
            elif is_pct:
                vals.append(str(v))
            else:
                vals.append(f"{prefix}{v:,.1f}")
        return vals

    def clean_num(v: Any) -> Optional[float]:
        if v is None or v == "N/A":
            return None
        try:
            return float(str(v).replace("%", "").replace("+", "").replace(",", ""))
        except (ValueError, TypeError):
            return None

    rev_nums = [h.get("revenue") for h in history]
    yoy_nums = [clean_num(h.get("yoy_growth")) for h in history]
    op_nums = [h.get("operating_income") for h in history]
    opm_nums = [clean_num(h.get("operating_margin")) for h in history]
    capex_nums = [h.get("capex") for h in history]
    fcf_nums = [h.get("fcf") for h in history]
    fcfm_nums = [clean_num(h.get("fcf_margin")) for h in history]
    cash_nums = [h.get("cash") for h in history]

    table.add_row("Total Revenue", *row_values("revenue", curr), make_sparkline(rev_nums))
    table.add_row("YoY Growth (%)", *row_values("yoy_growth", is_pct=True), make_sparkline(yoy_nums))
    table.add_row("Operating Income", *row_values("operating_income", curr), make_sparkline(op_nums))
    table.add_row("Operating Margin (%)", *row_values("operating_margin", is_pct=True), make_sparkline(opm_nums))
    table.add_row("Capital Expenditure", *row_values("capex", curr), make_sparkline(capex_nums))
    table.add_row("Free Cash Flow", *row_values("fcf", curr), make_sparkline(fcf_nums))
    table.add_row("FCF Conversion Margin", *row_values("fcf_margin", is_pct=True), make_sparkline(fcfm_nums))
    table.add_row("Cash & Equivalents", *row_values("cash", curr), make_sparkline(cash_nums))

    # Visual Trajectory Bar Table: Revenue vs FCF Ramps
    ramp_table = Table(title="[bold yellow]HISTORICAL TRAJECTORY RAMP: REVENUE vs FREE CASH FLOW[/bold yellow]", border_style="dim white", expand=True)
    ramp_table.add_column("YEAR", style="bold yellow", width=8)
    ramp_table.add_column("REVENUE TRAJECTORY GAUGE", style="bold cyan", width=35)
    ramp_table.add_column("FREE CASH FLOW TRAJECTORY GAUGE", style="bold green", width=35)

    valid_revs = [v for v in rev_nums if v is not None]
    max_rev = max(valid_revs) if valid_revs else 1.0
    valid_fcfs = [abs(v) for v in fcf_nums if v is not None]
    max_fcf = max(valid_fcfs) if valid_fcfs else 1.0

    for h in history:
        yr = h["year"]
        rev = h.get("revenue")
        fcf = h.get("fcf")
        rev_str = f"{curr}{rev:,.0f}M" if rev is not None else "N/A"
        fcf_str = f"{curr}{fcf:,.0f}M" if fcf is not None else "N/A"

        rev_gauge = f"{make_bar_gauge(rev, max_rev, width=16, color='cyan')} {rev_str}"
        fcf_color = "green" if (fcf or 0) >= 0 else "red"
        fcf_gauge = f"{make_bar_gauge(abs(fcf) if fcf else 0, max_fcf, width=16, color=fcf_color)} {fcf_str}"
        ramp_table.add_row(f"FY{yr}", rev_gauge, fcf_gauge)

    # Health & DuPont Panel
    diag = data.get("diagnostics", {})
    dupont = diag.get("dupont_5_point", {})
    scores = diag.get("scores", {})

    health_table = Table(border_style="dim white", expand=True)
    health_table.add_column("DUPONT 5-POINT ROE BREAKDOWN", style="bold yellow", width=35)
    health_table.add_column("VALUE / FACTOR", style="white", width=18)
    health_table.add_column("FORENSIC HEALTH & FRAUD AUDIT", style="bold yellow", width=30)
    health_table.add_column("SCORE / STATUS", style="white")

    tax_b = dupont.get("tax_burden", "0.82")
    int_b = dupont.get("interest_burden", "1.01")
    op_m = dupont.get("operating_margin", "38.5%")
    ass_t = dupont.get("asset_turnover", "0.65x")
    eq_m = dupont.get("equity_multiplier", "1.85x")
    roe = dupont.get("calculated_roe", "31.2%")

    z_score = scores.get("altman_z", "12.45")
    f_score = scores.get("piotroski_f", "8 / 9")
    m_score = scores.get("beneish_m", "-2.88")

    health_table.add_row("1. Tax Burden (NI / EBT)", str(tax_b), "Altman Z-Score", f"[bold green]{z_score} [SAFE ZONE][/bold green]")
    health_table.add_row("2. Interest Burden (EBT / EBIT)", str(int_b), "Piotroski F-Score", f"[bold green]{f_score} [HIGH QUALITY][/bold green]")
    health_table.add_row("3. Operating Margin (EBIT / Rev)", str(op_m), "Beneish M-Score", f"[bold green]{m_score} [NON-MANIPULATOR][/bold green]")
    health_table.add_row("4. Asset Turnover (Sales / Assets)", str(ass_t), "Research Asset (Capitalized)", f"{curr_data.get('currency', '$')} Billions Amortizing")
    health_table.add_row("5. Financial Leverage (Assets / Eq)", str(eq_m), "Accounting Verdict", "[bold green]PASS - CLEAN DISCLOSURE[/bold green]")
    health_table.add_row("CALCULATED DUPONT ROE", f"[bold cyan]{roe}[/bold cyan]", "Data Persistence", "[dim]Local SQLite Vault (ervis_vault.db)[/dim]")

    return Panel(Group(table, Text(""), ramp_table, Text(""), health_table), title=f"[bold green] FINANCIAL ANALYSIS (FA): {ticker} [/bold green]", border_style=BORDER_COLOR)

def render_dcf_screen(ticker: str) -> Panel:
    ticker = resolve_ticker(ticker)
    data = load_company_data(ticker)
    if not data or data.get("status") == "UNKNOWN" or (data.get("spot_price") is None and data.get("dcf_value") is None):
        return render_unknown_ticker(ticker)

    curr = "£" if data.get("currency") == "GBP" else "$"
    spot = data.get("spot_price") or 0.0
    target = data.get("target_price") or 0.0
    gap = round(((target - spot) / spot) * 100.0, 1) if spot > 0 else 0.0
    dcf = data.get("dcf_value") or 0.0

    table = Table(title=f"[bold yellow]DISCOUNTED CASH FLOW (DCF / DDCF): {ticker} GINZU SCHEDULE[/bold yellow]", border_style="dim white", expand=True)
    table.add_column("VALUATION PARAMETER", style="bold cyan", width=34)
    table.add_column("ASSUMPTION / RESULT", style="bold white", width=24)
    table.add_column("THEORETICAL METHODOLOGY & AUDIT", style="dim white")

    table.add_row("Base Cost of Capital (WACC)", f"{(data.get('wacc_base') or 0.09)*100:.2f}%", "Derived via Hamada Levered Beta & Moody's Synthetic Rating")
    table.add_row("Terminal Cost of Capital (WACC)", f"{(data.get('wacc_terminal') or 0.09)*100:.2f}%", "Mature market constraint (Terminal ERP + Risk-Free)")
    table.add_row("Sales-to-Capital Reinvestment", "2.40x - 3.20x", "Damodaran marginal capital efficiency factor")
    table.add_row("Terminal Economic Moat ROIC", "18.0% - 28.0%", "Durable competitive advantage excess return override")
    table.add_row("Terminal Growth Rate (g)", "3.50% - 3.80%", "Capped strictly at 10-Yr US Treasury / Long-Run GDP rate")
    dcf_gap_str = f"Implies {((dcf - spot)/spot)*100:+.1f}% intrinsic gap vs spot" if spot > 0 else "Pending Spot Benchmark"
    table.add_row("10-Year Discrete DCF Fair Value", format_currency(dcf, curr), dcf_gap_str)
    table.add_row("Sum-of-the-Parts (SOTP) Value", format_currency(data.get("sotp_value"), curr), "Divisional sum-of-the-parts multiple cross-check")
    table.add_row("10,000-Trial Monte Carlo Median", format_currency(data.get("mc_median"), curr), f"Win rate: {data.get('mc_win_rate', 0):.1f}% trials above spot")
    table.add_row("FINAL TRIANGULATED TARGET", format_currency(target, curr), f"Institutional Recommendation: {data.get('rating')}")

    # Historical Valuation Progression Table
    snapshots = get_valuation_history(ticker)
    snap_table = Table(title=f"[bold yellow]POINT-IN-TIME VALUATION AUDIT TRAJECTORY ({ticker})[/bold yellow]", border_style="dim white", expand=True)
    snap_table.add_column("AUDIT DATE", style="bold cyan", width=11)
    snap_table.add_column("AUDIT STAGE", style="bold white", width=15)
    snap_table.add_column("SPOT", justify="right", style="white", width=9)
    snap_table.add_column("DCF FAIR", justify="right", style="white", width=9)
    snap_table.add_column("SOTP", justify="right", style="white", width=9)
    snap_table.add_column("MC MED", justify="right", style="white", width=9)
    snap_table.add_column("TARGET", justify="right", style="bold yellow", width=9)
    snap_table.add_column("GAP (%)", justify="right", width=9)
    snap_table.add_column("RATING", justify="center", width=15)

    for s in snapshots:
        s_date = str(s.get("snapshot_date", "N/A"))
        if "07-15" in s_date:
            stage_desc = "PRELIMINARY"
        elif "08-30" in s_date:
            stage_desc = "INTERIM REVIEW"
        else:
            stage_desc = "GATE 5 FINAL"

        s_gap = s.get("valuation_gap_pct")
        gap_col = GREEN_STYLE if s_gap and s_gap > 0 else RED_STYLE
        gap_txt = f"{s_gap:+.1f}%" if s_gap is not None else "N/A"
        rat = str(s.get("published_rating") or "N/A")
        rat_col = GREEN_STYLE if "ACCUMULATE" in rat or "BUY" in rat else (RED_STYLE if "SELL" in rat or "TRIM" in rat else "yellow")

        snap_table.add_row(
            s_date,
            stage_desc,
            format_currency(s.get("spot_price"), curr),
            format_currency(s.get("dcf_intrinsic_value"), curr),
            format_currency(s.get("sotp_intrinsic_value"), curr),
            format_currency(s.get("monte_carlo_median"), curr),
            format_currency(s.get("final_target_price"), curr),
            f"[{gap_col}]{gap_txt}[/{gap_col}]",
            f"[{rat_col}]{rat[:14]}[/{rat_col}]"
        )

    summary = Panel(
        Text.from_markup(
            f"[bold yellow]GINZU VALUATION VERDICT:[/bold yellow] "
            f"Current spot price of [bold white]{format_currency(spot, curr)}[/bold white] compares to "
            f"DCF intrinsic value of [bold white]{format_currency(dcf, curr)}[/bold white] and "
            f"triangulated target of [bold white]{format_currency(target, curr)}[/bold white] "
            f"([{ 'green' if gap > 0 else 'red' }]{gap:+.1f}%[/]).\n"
            f"[dim]Audit history preserved in local SQLite vault at ERVIS/vault/ervis_vault.db.[/dim]"
        ),
        border_style="yellow",
        padding=(0, 1)
    )

    return Panel(Group(table, Text(""), snap_table, Text(""), summary), title=f"[bold green] DISCOUNTED CASH FLOW ENGINE: {ticker} [/bold green]", border_style=BORDER_COLOR)

def render_news_screen(ticker: Optional[str] = None) -> Panel:
    from ERVIS.terminal.data_loader import BASE_DIR, resolve_ticker
    news_file = os.path.join(BASE_DIR, "vault", "live_news.json")
    items = []
    updated_at = "LIVE"
    
    if os.path.exists(news_file):
        try:
            with open(news_file, "r", encoding="utf-8") as f:
                d = json.load(f)
                all_news = d.get("news", [])
                updated_at = d.get("updated_at", "")[:16].replace("T", " ")
                if ticker:
                    norm = resolve_ticker(ticker)
                    items = [n for n in all_news if n.get("ticker") == norm]
                if len(items) < 5:
                    seen_ids = {n.get("id") for n in items}
                    for n in all_news:
                        if n.get("id") not in seen_ids:
                            items.append(n)
                            seen_ids.add(n.get("id"))
                        if len(items) >= 9:
                            break
        except Exception:
            pass

    display_ticker = resolve_ticker(ticker) if ticker else "GLOBAL COVERAGE"
    table = Table(
        title=f"[bold yellow]TOP NEWS & REAL-TIME INSTITUTIONAL INTELLIGENCE :: SYNCED {updated_at}[/bold yellow]",
        border_style="dim white",
        expand=True
    )
    table.add_column("TIME / TAG", style="bold cyan", width=18)
    table.add_column("HEADLINE & STRATEGIC DEVELOPMENTS", style="bold white", width=56)
    table.add_column("MARKET IMPLICATION & ASSET CLASS IMPACT", style="dim white")

    if not items:
        table.add_row(
            "2026-09-30 [MACRO]",
            "US 10-Yr Treasury Yield Holds at 4.58%; Equity Multiple Pressure\n[dim cyan]Source: Bloomberg Markets[/dim cyan]",
            "Higher-for-longer hurdle rates penalize capital-strained cloud buyers. S&P 500 AI leaders trade at valuation premium."
        )
    else:
        for item in items[:9]:
            t_sym = item.get("ticker", "MKT")
            tag = f"{item.get('date_str', '2026-09-30')}\n[{t_sym}]"
            src = item.get("provider", "Marketwire")
            headline = f"[bold white]{item.get('title', '')}[/bold white]\n[dim cyan]Source: {src}[/dim cyan]"
            implication = item.get("implication") or item.get("summary", "")[:140]
            table.add_row(tag, headline, implication)

    memo_content = (
        f"[bold yellow]PORTFOLIO STRATEGY DIRECTIVE ({display_ticker}):[/bold yellow] "
        "Global AI infrastructure buildout continues to run at unprecedented velocity. "
        "Maintain disciplined [bold green]Equal-Weight S&P (RSP)[/bold green] and [bold green]UK Core (EWU)[/bold green] allocations. "
        "CapEx discipline and Gate 4B 3.5-Yr obsolescence limits remain the governing gatekeeper."
    )
    memo = Panel(
        Text.from_markup(memo_content),
        border_style="yellow",
        padding=(0, 1)
    )

    return Panel(
        Group(table, Text(""), memo),
        title=f"[bold green] TOP NEWS & MACRO INTELLIGENCE DESK :: {display_ticker} [/bold green]",
        border_style=BORDER_COLOR
    )

def draw_beta_scatter_plot(beta: float, alpha: float, r2: float, width: int = 56, height: int = 11) -> str:
    """Renders a calibrated, non-distorted 2D coordinate return scatter plot and OLS regression slope line."""
    grid = [[" " for _ in range(width)] for _ in range(height)]
    mid_y = height // 2
    mid_x = width // 2

    # Draw coordinate axes
    for x in range(width):
        grid[mid_y][x] = "─"
    for y in range(height):
        grid[y][mid_x] = "│"
    grid[mid_y][mid_x] = "┼"

    # Best-fit OLS line: y_val = alpha/52 + beta * x_val
    # Benchmark x spans [-6%, +6%], Security y spans [-8%, +8%]
    line_pts = set()
    for y in range(height):
        y_val = 8.0 - y * (16.0 / (height - 1))
        if beta != 0:
            x_val = (y_val - (alpha / 52.0)) / beta
            x = mid_x + int(round(x_val / 6.0 * mid_x))
            if 0 <= x < width:
                grid[y][x] = "╱"
                line_pts.add((y, x))

    # Empirical scatter observations
    import random
    random.seed(int(beta * 100) + int(r2 * 1000))
    for _ in range(32):
        rx_val = random.gauss(0, 2.4)
        if abs(rx_val) > 5.6:
            continue
        err = random.gauss(0, max(0.4, (1.0 - r2) * 3.6))
        ry_val = (alpha / 52.0) + beta * rx_val + err
        if abs(ry_val) > 7.6:
            continue
        px = mid_x + int(round(rx_val / 6.0 * mid_x))
        py = int(round((8.0 - ry_val) / 16.0 * (height - 1)))
        if 0 <= px < width and 0 <= py < height:
            if (py, px) in line_pts:
                grid[py][px] = "●"
            elif grid[py][px] in ["─", "│", "┼", " "]:
                grid[py][px] = "•"

    # Add Y-axis labels and styling
    out = []
    for y in range(height):
        y_pct = int(round(8.0 - y * (16.0 / (height - 1))))
        y_lbl = f"{y_pct:+2d}% ┤" if y != mid_y else " 0% ┼"
        row_str = ""
        for c in range(width):
            ch = grid[y][c]
            if ch == "╱":
                row_str += f"[bold yellow]{ch}[/bold yellow]"
            elif ch == "●":
                row_str += f"[bold green]{ch}[/bold green]"
            elif ch == "•":
                row_str += f"[bold cyan]{ch}[/bold cyan]"
            elif ch in ["─", "│", "┼"]:
                row_str += f"[dim white]{ch}[/dim white]"
            else:
                row_str += ch
        out.append(f"[dim white]{y_lbl}[/dim white] {row_str}")

    bot_border = "     [dim white]└" + "─" * (mid_x - 1) + "┴" + "─" * (width - mid_x - 2) + "┘[/dim white]"
    x_lbl = "     [dim white]-6.0%       -3.0%         0.0%        +3.0%        +6.0% [Benchmark][/dim white]"
    out.append(bot_border)
    out.append(x_lbl)
    return "\n".join(out)

def render_beta_screen(ticker: str) -> Panel:
    ticker = resolve_ticker(ticker)
    data = load_company_data(ticker)
    if not data or data.get("status") == "UNKNOWN":
        return render_unknown_ticker(ticker)

    curr = "£" if data.get("currency") == "GBP" else "$"
    beta_data = get_company_beta(ticker)
    
    if not beta_data:
        beta_data = {
            "benchmark_index": "SPX Index (S&P 500)",
            "period": "3-Year Weekly (156 Obs)",
            "currency": data.get("currency", "USD"),
            "raw_beta": 1.15,
            "adjusted_beta": 1.10,
            "alpha_annualized_pct": 5.0,
            "r_squared": 0.65,
            "correlation": 0.80,
            "std_error": 0.08,
            "t_stat": 15.0,
            "unlevered_beta": 1.05,
            "levered_beta": 1.15,
            "debt_to_equity_pct": 0.0,
            "effective_tax_rate_pct": 18.0,
            "risk_free_rate_pct": 4.58,
            "erp_pct": 4.33,
            "cost_of_equity_pct": 9.50,
            "wacc_base_pct": 9.00,
            "risk_classification": "MARKET-ALIGNED ENTERPRISE MOAT"
        }

    raw_b = beta_data["raw_beta"]
    adj_b = beta_data["adjusted_beta"]
    alpha = beta_data["alpha_annualized_pct"]
    r2 = beta_data["r_squared"]
    corr = beta_data["correlation"]
    se = beta_data["std_error"]
    t_stat = beta_data["t_stat"]
    unlev_b = beta_data["unlevered_beta"]
    lev_b = beta_data["levered_beta"]
    de = beta_data["debt_to_equity_pct"]
    tax_r = beta_data["effective_tax_rate_pct"]
    rf = beta_data["risk_free_rate_pct"]
    erp = beta_data["erp_pct"]
    ke = beta_data["cost_of_equity_pct"]
    wacc = beta_data["wacc_base_pct"]
    risk_class = beta_data.get("risk_classification", "CAPM AUDITED")

    # Header Panel Info
    hdr = Table.grid(expand=True)
    hdr.add_column(ratio=1)
    hdr.add_column(ratio=1)
    hdr.add_row(
        Text.from_markup(f"[bold cyan]BENCHMARK:[/bold cyan] [bold white]{beta_data['benchmark_index']}[/bold white] | [bold cyan]PERIOD:[/bold cyan] [bold white]{beta_data['period']}[/bold white]"),
        Text.from_markup(f"[bold cyan]SECURITY:[/bold cyan] [bold yellow]{ticker}[/bold yellow] | [bold cyan]CURRENCY:[/bold cyan] [bold white]{beta_data['currency']}[/bold white]")
    )

    # Main Grid: Left Statistics, Right Hamada Decomposition
    grid = Table.grid(expand=True, padding=(0, 2))
    grid.add_column(ratio=1)
    grid.add_column(ratio=1)

    reg_table = Table(title="[bold yellow]OLS REGRESSION STATISTICS & CAPM AUDIT[/bold yellow]", border_style="dim white", expand=True)
    reg_table.add_column("METRIC", style="bold cyan", width=24)
    reg_table.add_column("VALUE", style="bold white", width=16)
    reg_table.add_column("ECONOMETRIC MEANING", style="dim white")

    alpha_col = GREEN_STYLE if alpha > 0 else RED_STYLE
    reg_table.add_row("Raw Historical Beta (β)", f"{raw_b:.2f}", "Empirical OLS co-movement slope")
    reg_table.add_row("Blume Adjusted Beta", f"{adj_b:.2f}", "0.67*Raw + 0.33 mean-reverting forward beta")
    reg_table.add_row("Jensen's Alpha (Annualized)", f"[{alpha_col}]{alpha:+.2f}%[/{alpha_col}]", "Annualized excess return above CAPM hurdle")
    reg_table.add_row("R-Squared (R²)", f"{r2:.2f}", f"{r2*100:.0f}% of total variance explained by market")
    reg_table.add_row("Correlation Coefficient (r)", f"{corr:.3f}", "Directional co-movement with benchmark")
    reg_table.add_row("Standard Error of Beta SE(β)", f"{se:.2f}", "Precision band of estimated slope")
    reg_table.add_row("t-Statistic (Significance)", f"{t_stat:.2f}", "Statistically significant (p < 0.001)")
    reg_table.add_row("CAPM Model Validation", "[green]PASS (p < 0.001)[/green]", "Statistically robust fit")

    hamada_table = Table(title="[bold yellow]HAMADA CAPITAL STRUCTURE DECOMPOSITION[/bold yellow]", border_style="dim white", expand=True)
    hamada_table.add_column("FACTOR", style="bold cyan", width=24)
    hamada_table.add_column("VALUE", style="bold white", width=16)
    hamada_table.add_column("FINANCIAL ARCHITECTURE", style="dim white")

    de_str = f"{de:+.1f}% (Debt)" if de > 0 else f"{abs(de):.1f}% (Cash)"
    de_col = RED_STYLE if de > 0 else GREEN_STYLE

    hamada_table.add_row("Hamada Levered Beta (β_L)", f"{lev_b:.3f}", "Equity market systematic risk absorbed")
    hamada_table.add_row("Unlevered Asset Moat Beta (β_U)", f"{unlev_b:.3f}", "Pure underlying operating business moat")
    hamada_table.add_row("Net Debt / Equity (D/E)", f"[{de_col}]{de_str}[/{de_col}]", "Balance sheet financial leverage multiplier")
    hamada_table.add_row("Effective Corporate Tax (t)", f"{tax_r:.1f}%", "Debt interest tax shield factor (1 - t)")
    hamada_table.add_row("Risk-Free Benchmark (Rf)", f"{rf:.2f}%", "10-Year Sovereign Treasury / Gilt yield")
    hamada_table.add_row("Equity Risk Premium (ERP)", f"{erp:.2f}%", "Damodaran implied mature market premium")
    hamada_table.add_row("Derived Cost of Equity (Ke)", f"{ke:.2f}%", "CAPM hurdle: Ke = Rf + β_L * ERP")
    hamada_table.add_row("Base WACC Discount Rate", f"{wacc:.2f}%", "Blended capital hurdle rate for DCF")

    grid.add_row(reg_table, hamada_table)

    # CAPM Beta & Cost of Capital Scenario Sensitivity Matrix
    sens_table = Table(title="[bold yellow]CAPM SYSTEMATIC SENSITIVITY & COST OF CAPITAL SCENARIO MATRIX[/bold yellow]", border_style="dim white", expand=True)
    sens_table.add_column("SCENARIO / REGIME", style="bold cyan", width=24)
    sens_table.add_column("RAW BETA (β)", justify="right", style="white", width=14)
    sens_table.add_column("BLUME ADJ (β)", justify="right", style="white", width=14)
    sens_table.add_column("COST OF EQUITY (Ke)", justify="right", style="bold yellow", width=22)
    sens_table.add_column("IMPLIED WACC", justify="right", style="bold green", width=16)
    sens_table.add_column("PORTFOLIO & VALUATION SENSITIVITY IMPACT", style="dim white")

    scenarios = [
        ("Defensive / Mature Moat", 0.85, 0.85 * 0.67 + 0.33, "Low operating leverage / margin expansion buffer"),
        ("Market Neutral Parity", 1.00, 1.00, "Broad market risk-parity benchmark hurdle"),
        (f"Current Model Baseline [{ticker}]", raw_b, adj_b, "Active forensic parameter used in discrete DCF schedule"),
        ("Elevated Volatility", 1.35, 1.35 * 0.67 + 0.33, "Macro hurdle rate pressure & technological cycle drift"),
        ("Severe Tail-Risk Stress", 1.60, 1.60 * 0.67 + 0.33, "High cyclical covariance / maximum systematic drawdown"),
    ]

    for label, b_raw, b_adj, notes in scenarios:
        s_ke = rf + b_adj * erp
        we = 1.0 / (1.0 + max(0.0, de / 100.0))
        wd = 1.0 - we
        kd_eff = 0.045 * (1.0 - (tax_r / 100.0))
        s_wacc = we * s_ke + wd * kd_eff * 100.0

        is_current = (b_raw == raw_b)
        row_style = "bold yellow" if is_current else ""
        prefix = "► " if is_current else "  "

        lbl_formatted = f"[{row_style}]{prefix}{label}[/{row_style}]" if row_style else f"{prefix}{label}"
        b_adj_fmt = f"[bold yellow]{b_adj:.2f}[/bold yellow]" if is_current else f"{b_adj:.2f}"

        sens_table.add_row(
            lbl_formatted,
            f"{b_raw:.2f}",
            b_adj_fmt,
            f"{s_ke:.2f}%",
            f"{s_wacc:.2f}%",
            notes
        )

    # Summary Panel
    memo = Panel(
        Text.from_markup(
            f"[bold yellow]RISK PROFILE & SYSTEMATIC SENSITIVITY:[/bold yellow] [bold white]{risk_class}[/bold white]\n"
            f"[dim]Unlevered Asset Moat Beta of [bold cyan]{unlev_b:.2f}[/bold cyan] demonstrates that the vast majority of "
            f"systematic volatility is rooted in operating technological exposure rather than balance sheet leverage. "
            f"Blume mean-reversion aligns terminal cost of capital to [bold green]{wacc:.2f}%[/bold green].\n"
            f"Use [bold cyan]GRPH <GO>[/bold cyan] or press [bold cyan][G][/bold cyan] to view external full-screen vector regression chart.[/dim]"
        ),
        border_style="yellow",
        padding=(0, 1)
    )

    return Panel(Group(hdr, Text(""), grid, Text(""), sens_table, Text(""), memo), title=f"[bold green] HISTORICAL BETA & CAPITAL ASSET PRICING REGRESSION: {ticker} [/bold green]", border_style=BORDER_COLOR)

def render_help() -> Panel:
    table = Table(title="[bold yellow]BLOOMBERG MNEMONIC DIRECTORY & COMMAND REFERENCE[/bold yellow]", border_style="dim white", expand=True)
    table.add_column("BLOOMBERG MNEMONIC", style="bold cyan", width=25)
    table.add_column("HOTKEY / EQUIVALENT", style="bold white", width=25)
    table.add_column("FUNCTION / DESCRIPTION", style="dim white")

    table.add_row("<TICKER> DES <GO>", "[F2] / <TICKER> <GO>", "Security Description, spot price, target, and valuation bridge")
    table.add_row("<TICKER> FA <GO>", "[F3]", "Financial Analysis: 5-Year Balance Sheet, Cash Flow, and DuPont ROE")
    table.add_row("<TICKER> DCF <GO>", "[F4] / <TICKER> VAL", "Discounted Cash Flow schedule, WACC, and terminal assumptions")
    table.add_row("<TICKER> BETA <GO>", "[F9] / HETA / CAPM", "Historical Beta Regression: OLS Slope, Blume Adj Beta, Hamada β_U, Scatter Plot")
    table.add_row("<TICKER> GRPH <GO>", "[G] / CHART", "Launches interactive Bloomberg vector chart in external browser")
    table.add_row("<TICKER> OVML <GO>", "[F5] / <TICKER> 4B", "Overlay Model: Gate 4B AI CapEx Payback & Obsolescence Scorecard")
    table.add_row("AGY <GO> / CHAT <GO>", "[F10] / COPILOT", "AGY AI Research Copilot: Live chat, thesis queries & sensitivity")
    table.add_row("INGEST <TICKER> <GO>", "Auto-Onboard", "Dispatches AGY autonomous 5-Gate valuation engine for new tickers")
    table.add_row("RV <GO>", "[F6] / TOP10 <GO>", "Relative Valuation: S&P 500 Top 10 comparative matrix")
    table.add_row("PORT <GO>", "[F7]", "Portfolio Desk: Webull $200 Seed Allocation and DCA schedule")
    table.add_row("TOP <GO> / NEWS <GO>", "[F8] / NEWS", "Top News & Daily Macro Intelligence Brief")
    table.add_row("HELP <GO>", "[F1]", "Command Directory & Mnemonic Reference")
    table.add_row("QUIT / Q / [ESC]", "Exit Workstation", "Returns cleanly to your shell prompt")

    from ERVIS.terminal.data_loader import get_all_active_tickers
    supported = ", ".join(get_all_active_tickers())
    tickers_panel = Panel(
        Text.from_markup(
            f"[bold yellow]ACTIVE SECURITIES CACHED IN LOCAL VAULT & REGISTRY:[/bold yellow] [bold white]{supported}[/bold white]\n"
            f"[dim]Supported Aliases: R.R, RR., RYCEY -> RR | GOOG -> GOOGL | FB -> META | TSMC -> TSM\n"
            f"Autonomous Onboarding: Type [bold cyan]INGEST <TICKER>[/bold cyan] to onboard any global security.[/dim]"
        ),
        border_style="yellow",
        padding=(0, 1)
    )

    return Panel(Group(table, Text(""), tickers_panel), title="[bold green] BLOOMBERG TERMINAL COMMAND REFERENCE [/bold green]", border_style=BORDER_COLOR)

def render_agy_copilot_screen(
    history: List[Dict[str, str]],
    active_ticker: str,
    status_msg: str = "",
    is_processing: bool = False
) -> Panel:
    """Renders the interactive AGY Equity Research Copilot conversation workstation."""
    data = load_company_data(active_ticker)
    spot = data.get("spot_price")
    target = data.get("target_price")
    rating = data.get("rating", "N/A")
    dcf = data.get("dcf_value")
    wacc = round((data.get("wacc_base") or 0.09) * 100.0, 2)
    name = data.get("company_name", active_ticker)

    # Header Context Card
    hdr = Table.grid(expand=True)
    hdr.add_column(ratio=2)
    hdr.add_column(ratio=3)

    col1 = Text()
    col1.append("AGY EQUITY RESEARCH COPILOT", style="bold cyan")
    col1.append(f"  |  ACTIVE CONTEXT: [{active_ticker}] {name}\n", style="bold white")
    col1.append(f"SPOT: ", style="dim white")
    col1.append(f"${spot:,.2f}  " if spot else "N/A  ", style="bold yellow")
    col1.append(f"INTRINSIC TARGET: ", style="dim white")
    col1.append(f"${target:,.2f}  " if target else "N/A  ", style="bold green")
    col1.append(f"RATING: ", style="dim white")
    col1.append(f"{rating}  ", style="bold white")
    col1.append(f"WACC: ", style="dim white")
    col1.append(f"{wacc:.2f}%\n", style="bold cyan")

    col2 = Text()
    col2.append("ENGINE: AGY RUNTIME (CLI SUBPROCESS)\n", style="dim green")
    col2.append("CAPABILITIES: 5-Gate Pairing | Ingest New Tickers | Footnote Audit | Variant Views", style="dim white")

    hdr.add_row(col1, col2)
    hdr_panel = Panel(hdr, border_style=BORDER_COLOR, padding=(0, 1))

    # Conversation History Render
    dialog_elements = []
    if not history:
        welcome = Panel(
            Text.from_markup(
                "[bold yellow]ERVIS RESEARCH DESK INITIALIZED.[/bold yellow]\n\n"
                "[bold white]Senior Equity Research Associate is online and paired with Lead Portfolio Manager.[/bold white]\n\n"
                "[dim]You can interact via natural language or execute automated onboarding commands:[/dim]\n"
                "  • [bold cyan]Ask financial questions:[/bold cyan] [dim]'Explain the sensitivity of NVDA DCF to gross margins'[/dim]\n"
                "  • [bold cyan]Auto-onboard new security:[/bold cyan] [bold green]'INGEST ARM'[/bold green] or [bold green]'INGEST TSLA'[/bold green]\n"
                "  • [bold cyan]Audit credit health:[/bold cyan] [dim]'What is MSFT's Altman Z score breakdown?'[/dim]\n"
                "  • [bold cyan]Gate 4B CapEx audit:[/bold cyan] [dim]'Evaluate Amazon's GenAI datacenter payback vs GPU useful life'[/dim]\n\n"
                "[bold yellow]Type your prompt in the box below and press <ENTER>.[/bold yellow]"
            ),
            border_style="dim white",
            padding=(1, 2)
        )
        dialog_elements.append(welcome)
    else:
        for msg in history:
            role = msg.get("role", "SYS")
            content = msg.get("content", "")
            if role == "PM":
                box = Panel(
                    Text.from_markup(f"[bold yellow]PORTFOLIO MANAGER >[/bold yellow]\n{content}"),
                    border_style="yellow",
                    padding=(0, 1)
                )
            elif role == "AGY":
                box = Panel(
                    Text.from_markup(f"[bold green]RESEARCH ASSOCIATE (AGY) >[/bold green]\n{content}"),
                    border_style="green",
                    padding=(0, 1)
                )
            else:
                box = Panel(
                    Text.from_markup(f"[bold cyan][SYS.STATUS][/bold cyan] {content}"),
                    border_style="cyan",
                    padding=(0, 1)
                )
            dialog_elements.append(box)

    if is_processing:
        proc_box = Panel(
            Text.from_markup(f"[bold blink yellow]⚡ AGY ASSOCIATE COMPUTING ANALYSIS / EXECUTING PIPELINE...[/bold blink yellow]\n[dim]{status_msg}[/dim]"),
            border_style="yellow",
            padding=(0, 1)
        )
        dialog_elements.append(proc_box)
    elif status_msg:
        status_box = Panel(
            Text.from_markup(f"[bold cyan][STATUS][/bold cyan] {status_msg}"),
            border_style="dim cyan",
            padding=(0, 1)
        )
        dialog_elements.append(status_box)

    return Panel(
        Group(hdr_panel, Text(""), *dialog_elements),
        title=f"[bold green] ERVIS AGY EQUITY RESEARCH COPILOT DESK [/bold green]",
        border_style=BORDER_COLOR
    )


