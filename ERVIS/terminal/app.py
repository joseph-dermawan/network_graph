"""
ERVIS Bloomberg Terminal TUI Application
Built with Textual & Rich for authentic institutional financial workstation experience.
Supports industry-standard Bloomberg 4-letter mnemonics (DES, FA, DCF, OVML, RV, PORT, TOP, HELP).
"""

import sys
import os
from datetime import datetime

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Input, Static, TabbedContent, TabPane, Label, Select
from textual.binding import Binding

from ERVIS.terminal.data_loader import (
    load_company_data,
    get_top10_matrix,
    get_portfolio_data,
    get_fa_financial_trends,
    resolve_ticker,
    get_covered_companies,
    get_all_active_tickers,
    COVERED_COMPANIES,
    ALL_ACTIVE_TICKERS
)
from ERVIS.terminal.chart_generator import open_beta_chart
from ERVIS.terminal.renderer import (
    render_overview,
    render_fa_screen,
    render_dcf_screen,
    render_beta_screen,
    render_gate_4b,
    render_top10_matrix_panel,
    render_portfolio_desk,
    render_news_screen,
    render_help,
    render_agy_copilot_screen,
    BORDER_COLOR
)
from ERVIS.terminal.agy_bridge import get_agy_bridge

APP_CSS = """
Screen {
    background: #0d0d0d;
    color: #ffffff;
}

#header_bar {
    dock: top;
    height: 3;
    background: #141414;
    border-bottom: solid #ffb000;
    padding: 0 1;
}

#header_title {
    color: #ffb000;
    text-style: bold;
    width: 28;
    padding-top: 1;
}

#header_status {
    color: #00ff66;
    text-style: bold;
    padding-top: 1;
    width: 25;
}

#header_clock {
    color: #00e5ff;
    text-align: right;
    padding-top: 1;
}

#cmd_bar {
    height: 3;
    background: #141414;
    border-bottom: solid #333333;
    padding: 0 1;
}

#cmd_label {
    width: 7;
    color: #ffb000;
    text-style: bold;
    padding-top: 1;
}

#cmd_input {
    width: 1fr;
    background: #0d0d0d;
    color: #ffffff;
    border: solid #ffb000;
    height: 3;
}

#ticker_select {
    width: 32;
    height: 3;
    margin-left: 1;
    background: #1a1a1a;
    border: solid #00e5ff;
}

#screen_select {
    width: 28;
    height: 3;
    margin-left: 1;
    background: #1a1a1a;
    border: solid #00ff66;
}

#main_container {
    height: 1fr;
    padding: 1;
}

TabbedContent {
    height: 1fr;
}

TabPane {
    padding: 0;
    height: 1fr;
}

.screen_panel {
    height: 1fr;
    width: 100%;
}

#agy_prompt_bar {
    dock: bottom;
    height: 3;
    background: #141414;
    border-top: solid #00e5ff;
    padding: 0 1;
}

#agy_prompt_label {
    width: 7;
    color: #00e5ff;
    text-style: bold;
    padding-top: 1;
}

#agy_input {
    width: 1fr;
    background: #0d0d0d;
    color: #ffffff;
    border: solid #00e5ff;
    height: 3;
}
"""

class ERVISTerminalApp(App):
    TITLE = "ERVIS INSTITUTIONAL TERMINAL v2.0"
    CSS = APP_CSS

    BINDINGS = [
        Binding("f1", "switch_tab('tab_help')", "HELP", show=True),
        Binding("f2", "switch_tab('tab_des')", "DES (Ovw)", show=True),
        Binding("f3", "switch_tab('tab_fa')", "FA (Fin Stmts)", show=True),
        Binding("f4", "switch_tab('tab_dcf')", "DCF (Val)", show=True),
        Binding("f5", "switch_tab('tab_ovml')", "OVML (AI 4B)", show=True),
        Binding("f6", "switch_tab('tab_rv')", "RV (Top 10)", show=True),
        Binding("f7", "switch_tab('tab_port')", "PORT (Seed)", show=True),
        Binding("f8", "switch_tab('tab_top')", "TOP (News)", show=True),
        Binding("f9", "switch_tab('tab_beta')", "BETA (CAPM)", show=True),
        Binding("f10", "switch_tab('tab_agy')", "AGY (Copilot)", show=True),
        Binding("g", "open_chart", "GRPH (Web)", show=True),
        Binding("escape", "focus_cmd", "CMD", show=True),
        Binding("q", "quit", "QUIT", show=True),
    ]

    def __init__(self, initial_ticker: str = "NVDA", initial_tab: str = "tab_des"):
        super().__init__()
        self.active_ticker = resolve_ticker(initial_ticker)
        self.initial_tab = initial_tab
        self.chat_history: List[Dict[str, str]] = []
        self.is_agy_busy: bool = False
        self.agy_status_msg: str = ""

    def compose(self) -> ComposeResult:
        # Top Header Bar
        with Horizontal(id="header_bar"):
            yield Label("ERVIS BLOOMBERG v2.0", id="header_title")
            yield Label(f"ACTIVE: [{self.active_ticker}]", id="header_status")
            yield Label(datetime.now().strftime("%Y-%m-%d %H:%M:%S SGT"), id="header_clock")

        # Bloomberg Command Line Bar with Dropdown Selectors
        covered = get_covered_companies()
        with Horizontal(id="cmd_bar"):
            yield Label("CMD >", id="cmd_label")
            yield Input(placeholder="Type command (e.g. NVDA BETA, INGEST ARM, AGY) & press ENTER", id="cmd_input")
            yield Select(
                options=[(f"{t:5s} - {name[:20]}", t) for t, name in covered],
                prompt="[SEC/TICKER]",
                value=self.active_ticker if any(t == self.active_ticker for t, _ in covered) else Select.BLANK,
                id="ticker_select",
                allow_blank=True,
            )
            yield Select(
                options=[
                    ("DES  [F2] - Overview", "tab_des"),
                    ("FA   [F3] - Financials", "tab_fa"),
                    ("DCF  [F4] - Cash Flow Val", "tab_dcf"),
                    ("BETA [F9] - Beta & CAPM", "tab_beta"),
                    ("OVML [F5] - Gate 4B AI CapEx", "tab_ovml"),
                    ("AGY  [F10] - Research Copilot", "tab_agy"),
                    ("RV   [F6] - Relative Val", "tab_rv"),
                    ("PORT [F7] - Portfolio Desk", "tab_port"),
                    ("TOP  [F8] - Macro Intelligence", "tab_top"),
                    ("HELP [F1] - Mnemonic Guide", "tab_help"),
                ],
                prompt="[SCREEN]",
                value=self.initial_tab,
                id="screen_select",
                allow_blank=False,
            )

        # Main Tabbed Viewports
        with Container(id="main_container"):
            with TabbedContent(initial=self.initial_tab, id="main_tabs"):
                with TabPane("DES [F2]", id="tab_des"):
                    with ScrollableContainer():
                        yield Static(id="des_content", classes="screen_panel")

                with TabPane("FA [F3]", id="tab_fa"):
                    with ScrollableContainer():
                        yield Static(id="fa_content", classes="screen_panel")

                with TabPane("DCF [F4]", id="tab_dcf"):
                    with ScrollableContainer():
                        yield Static(id="dcf_content", classes="screen_panel")

                with TabPane("OVML [F5]", id="tab_ovml"):
                    with ScrollableContainer():
                        yield Static(id="ovml_content", classes="screen_panel")

                with TabPane("BETA [F9]", id="tab_beta"):
                    with ScrollableContainer():
                        yield Static(id="beta_content", classes="screen_panel")

                with TabPane("AGY [F10]", id="tab_agy"):
                    with Vertical(classes="screen_panel"):
                        with ScrollableContainer(id="agy_scroll_container"):
                            yield Static(id="agy_content", classes="screen_panel")
                        with Horizontal(id="agy_prompt_bar"):
                            yield Label("AGY >", id="agy_prompt_label")
                            yield Input(placeholder="Ask AGY Copilot (or type 'INGEST <TICKER>') & press ENTER...", id="agy_input")

                with TabPane("RV [F6]", id="tab_rv"):
                    with ScrollableContainer():
                        yield Static(id="rv_content", classes="screen_panel")

                with TabPane("PORT [F7]", id="tab_port"):
                    with ScrollableContainer():
                        yield Static(id="port_content", classes="screen_panel")

                with TabPane("TOP [F8]", id="tab_top"):
                    with ScrollableContainer():
                        yield Static(id="top_content", classes="screen_panel")

                with TabPane("HELP [F1]", id="tab_help"):
                    with ScrollableContainer():
                        yield Static(id="help_content", classes="screen_panel")

        yield Footer()

    def on_mount(self) -> None:
        self.refresh_all_views()
        self.set_interval(1.0, self.update_clock)
        if self.initial_tab == "tab_agy":
            try:
                self.query_one("#agy_input", Input).focus()
            except Exception:
                self.query_one("#cmd_input", Input).focus()
        else:
            self.query_one("#cmd_input", Input).focus()

    def update_clock(self) -> None:
        clock = self.query_one("#header_clock", Label)
        clock.update(datetime.now().strftime("%Y-%m-%d %H:%M:%S SGT"))
        if self.is_agy_busy:
            self._refresh_agy_view()

    def refresh_all_views(self) -> None:
        # Update header
        header_status = self.query_one("#header_status", Label)
        header_status.update(f"ACTIVE: [{self.active_ticker}]")

        # DES
        des_widget = self.query_one("#des_content", Static)
        des_widget.update(render_overview(self.active_ticker))

        # FA
        fa_widget = self.query_one("#fa_content", Static)
        fa_widget.update(render_fa_screen(self.active_ticker))

        # DCF
        dcf_widget = self.query_one("#dcf_content", Static)
        dcf_widget.update(render_dcf_screen(self.active_ticker))

        # OVML (Gate 4B)
        ovml_widget = self.query_one("#ovml_content", Static)
        ovml_widget.update(render_gate_4b(self.active_ticker))

        # BETA
        beta_widget = self.query_one("#beta_content", Static)
        beta_widget.update(render_beta_screen(self.active_ticker))

        # RV (Top 10)
        rv_widget = self.query_one("#rv_content", Static)
        rv_widget.update(render_top10_matrix_panel())

        # PORT
        port_widget = self.query_one("#port_content", Static)
        port_widget.update(render_portfolio_desk())

        # TOP (News)
        top_widget = self.query_one("#top_content", Static)
        top_widget.update(render_news_screen())

        # HELP
        help_widget = self.query_one("#help_content", Static)
        help_widget.update(render_help())

        # AGY Copilot
        try:
            agy_widget = self.query_one("#agy_content", Static)
            agy_widget.update(render_agy_copilot_screen(
                self.chat_history,
                self.active_ticker,
                status_msg=self.agy_status_msg,
                is_processing=self.is_agy_busy
            ))
        except Exception:
            pass

        # Update dynamic ticker select options
        try:
            sel = self.query_one("#ticker_select", Select)
            covered = get_covered_companies()
            new_opts = [(f"{t:5s} - {name[:20]}", t) for t, name in covered]
            if len(sel._options) != len(new_opts):
                sel.set_options(new_opts)
        except Exception:
            pass

    def _refresh_agy_view(self) -> None:
        try:
            agy_widget = self.query_one("#agy_content", Static)
            agy_widget.update(render_agy_copilot_screen(
                self.chat_history,
                self.active_ticker,
                status_msg=self.agy_status_msg,
                is_processing=self.is_agy_busy
            ))
            container = self.query_one("#agy_scroll_container", ScrollableContainer)
            container.scroll_end(animate=False)
        except Exception:
            pass

    def handle_agy_prompt(self, prompt: str) -> None:
        p_upper = prompt.strip().upper()
        if p_upper.startswith("INGEST ") or p_upper.startswith("ONBOARD "):
            parts = p_upper.split()
            if len(parts) > 1:
                self.start_onboarding_worker(parts[1])
                return

        self.chat_history.append({"role": "PM", "content": prompt})
        self.is_agy_busy = True
        self.agy_status_msg = f"Consulting AGY Associate on {self.active_ticker}..."
        self._refresh_agy_view()
        self.run_agy_query_worker(prompt)

    @work(exclusive=False)
    async def run_agy_query_worker(self, prompt: str) -> None:
        bridge = get_agy_bridge()
        try:
            resp = await bridge.query(prompt, ticker=self.active_ticker)
            self.chat_history.append({"role": "AGY", "content": resp})
            self.agy_status_msg = ""
        except Exception as e:
            self.chat_history.append({"role": "SYS", "content": f"AGY Error: {str(e)}"})
            self.agy_status_msg = "Error encountered."
        finally:
            self.is_agy_busy = False
            self._refresh_agy_view()

    @work(exclusive=False)
    async def start_onboarding_worker(self, ticker: str) -> None:
        ticker = ticker.strip().upper()
        self.chat_history.append({"role": "PM", "content": f"INGEST {ticker}"})
        self.chat_history.append({"role": "SYS", "content": f"Dispatched AGY 5-Gate autonomous pipeline for {ticker}..."})
        self.is_agy_busy = True
        self.agy_status_msg = f"Starting Gate 1 Ingestion for {ticker}..."
        self._refresh_agy_view()

        bridge = get_agy_bridge()
        def progress_cb(msg: str):
            self.agy_status_msg = msg
            self._refresh_agy_view()

        try:
            outputs = await bridge.onboard_ticker(ticker, progress_callback=progress_cb)
            t_price = outputs['final_triangulation'].get('target_price_usd') or outputs['final_triangulation'].get('target_price_pence')
            rating = outputs['final_triangulation'].get('rating')
            self.chat_history.append({
                "role": "AGY",
                "content": f"[bold green]5-GATE VALUATION COMPLETE FOR {ticker}:[/bold green]\n\n"
                           f"• Security: {outputs.get('company_name')} ({ticker})\n"
                           f"• Market Spot: ${outputs.get('spot_price_usd', 'N/A')}\n"
                           f"• Intrinsic DCF Target: ${t_price} ({rating})\n"
                           f"• WACC: {outputs['wacc_schedule'].get('base_wacc') * 100:.2f}%\n"
                           f"• Altman Z-Score: {outputs['financial_health'].get('altman_z_score')} ({outputs['financial_health'].get('altman_zone')})\n\n"
                           f"[bold yellow]Screens hot-reloaded.[/bold yellow] Press [F2] for DES or [F4] for DCF."
            })
            self.active_ticker = ticker
            self.refresh_all_views()
            self._sync_ticker_select(ticker)
            self.notify(f"Onboarded {ticker} successfully! Intrinsic target: ${t_price}", severity="information", timeout=6.0)
        except Exception as e:
            self.chat_history.append({"role": "SYS", "content": f"Failed to onboard {ticker}: {str(e)}"})
            self.notify(f"Onboarding failed: {str(e)}", severity="error", timeout=6.0)
        finally:
            self.is_agy_busy = False
            self.agy_status_msg = ""
            self._refresh_agy_view()
    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "ticker_select" and event.value != Select.BLANK:
            chosen = resolve_ticker(str(event.value))
            if chosen != self.active_ticker:
                self.active_ticker = chosen
                self.refresh_all_views()
        elif event.select.id == "screen_select" and event.value != Select.BLANK:
            chosen_tab = str(event.value)
            tabs = self.query_one("#main_tabs", TabbedContent)
            tabs.active = chosen_tab
            if chosen_tab == "tab_agy":
                try:
                    self.query_one("#agy_input", Input).focus()
                except Exception:
                    pass
            else:
                try:
                    self.query_one("#cmd_input", Input).focus()
                except Exception:
                    pass

    def action_open_chart(self) -> None:
        """Launches interactive Bloomberg vector chart in external browser."""
        open_beta_chart(self.active_ticker)

    def action_switch_tab(self, tab_id: str) -> None:
        tabs = self.query_one("#main_tabs", TabbedContent)
        tabs.active = tab_id
        self._sync_screen_select(tab_id)
        if tab_id == "tab_agy":
            try:
                self.query_one("#agy_input", Input).focus()
            except Exception:
                pass
        else:
            try:
                self.query_one("#cmd_input", Input).focus()
            except Exception:
                pass

    def on_input_submitted(self, event: Input.Submitted) -> None:
        raw_cmd = event.value.strip()
        event.input.value = ""

        if not raw_cmd:
            return

        tabs = self.query_one("#main_tabs", TabbedContent)

        # 1. Input submitted from the AGY Chat Input Box
        if event.input.id == "agy_input":
            self.handle_agy_prompt(raw_cmd)
            return

        # 2. Input submitted from the Bloomberg Command Bar (#cmd_input)
        cmd = raw_cmd.upper().replace("<GO>", "").replace("GO", "").strip()

        # If currently on the AGY tab and command is NOT a global navigation mnemonic, route to AGY
        NAV_MNEMONICS = ["Q", "QUIT", "EXIT", "HELP", "?", "RV", "TOP10", "MATRIX", "PORT", "PORTFOLIO",
                         "TOP", "NEWS", "FA", "FINANCIALS", "DCF", "VAL", "OVML", "4B", "CAPEX", "BETA",
                         "CAPM", "GRPH", "CHART", "DES", "OVW", "OVERVIEW", "AGY", "CHAT"]
        if tabs.active == "tab_agy" and cmd not in NAV_MNEMONICS and not any(cmd.startswith(m + " ") for m in NAV_MNEMONICS):
            self.handle_agy_prompt(raw_cmd)
            return

        # Check for explicit AGY or INGEST commands
        if cmd.startswith("AGY ") or cmd.startswith("ASK "):
            prompt = raw_cmd[4:].strip()
            tabs.active = "tab_agy"
            self._sync_screen_select("tab_agy")
            self.handle_agy_prompt(prompt)
            return

        if cmd.startswith("INGEST ") or cmd.startswith("ONBOARD "):
            ticker_to_ingest = cmd.split()[1]
            tabs.active = "tab_agy"
            self._sync_screen_select("tab_agy")
            self.start_onboarding_worker(ticker_to_ingest)
            return

        # Detect natural language questions in CMD bar (e.g. "What is NVDA valuation?", "Explain DCF")
        QUESTION_STARTERS = ["WHAT", "WHY", "HOW", "IS", "ARE", "CAN", "COULD", "EXPLAIN", "TELL", "ANALYZE", "CHECK", "COMPARE", "SUMMARIZE", "VALUATION", "THESIS"]
        words = cmd.split()
        if "?" in raw_cmd or (len(words) > 2 and words[0] in QUESTION_STARTERS):
            tabs.active = "tab_agy"
            self._sync_screen_select("tab_agy")
            self.handle_agy_prompt(raw_cmd)
            return

        # Global navigation commands without ticker
        if cmd in ["Q", "QUIT", "EXIT"]:
            self.exit()
            return
        elif cmd in ["HELP", "?"]:
            tabs.active = "tab_help"
            self._sync_screen_select("tab_help")
            return
        elif cmd in ["AGY", "CHAT", "COPILOT", "AI"]:
            tabs.active = "tab_agy"
            self._sync_screen_select("tab_agy")
            try:
                self.query_one("#agy_input", Input).focus()
            except Exception:
                pass
            return
        elif cmd in ["RV", "TOP10", "MATRIX", "S&P", "SP500"]:
            tabs.active = "tab_rv"
            self._sync_screen_select("tab_rv")
            return
        elif cmd in ["PORT", "PORTFOLIO", "WEBULL", "SEED"]:
            tabs.active = "tab_port"
            self._sync_screen_select("tab_port")
            return
        elif cmd in ["TOP", "NEWS", "BRIEF"]:
            tabs.active = "tab_top"
            self._sync_screen_select("tab_top")
            return
        elif cmd in ["FA", "FINANCIALS"]:
            tabs.active = "tab_fa"
            self._sync_screen_select("tab_fa")
            return
        elif cmd in ["DCF", "DDCF", "VAL"]:
            tabs.active = "tab_dcf"
            self._sync_screen_select("tab_dcf")
            return
        elif cmd in ["OVML", "4B", "CAPEX"]:
            tabs.active = "tab_ovml"
            self._sync_screen_select("tab_ovml")
            return
        elif cmd in ["BETA", "HETA", "CAPM"]:
            tabs.active = "tab_beta"
            self._sync_screen_select("tab_beta")
            return
        elif cmd in ["GRPH", "CHART", "GRAPH"]:
            self.action_open_chart()
            return
        elif cmd in ["DES", "OVW", "OVERVIEW"]:
            tabs.active = "tab_des"
            self._sync_screen_select("tab_des")
            return

        # Ticker + Mnemonic or Ticker solo (e.g. "NVDA FA", "MSFT DCF", "AAPL", "RR", "R.R")
        parts = cmd.split()
        candidate_ticker = resolve_ticker(parts[0])

        active_tickers = get_all_active_tickers()
        if candidate_ticker not in active_tickers and load_company_data(candidate_ticker).get("spot_price") is None:
            self.active_ticker = candidate_ticker
            self.refresh_all_views()
            self._sync_ticker_select(candidate_ticker)
            self.notify(f"Ticker [{candidate_ticker}] not in registry. Type 'INGEST {candidate_ticker}' or press [F10].", severity="warning", timeout=6.0)
            return

        self.active_ticker = candidate_ticker
        self.refresh_all_views()
        self._sync_ticker_select(candidate_ticker)

        if len(parts) > 1:
            mnemonic = parts[1]
            if mnemonic in ["FA", "FIN"]:
                tabs.active = "tab_fa"
                self._sync_screen_select("tab_fa")
            elif mnemonic in ["DCF", "DDCF", "VAL"]:
                tabs.active = "tab_dcf"
                self._sync_screen_select("tab_dcf")
            elif mnemonic in ["OVML", "4B", "CAPEX"]:
                tabs.active = "tab_ovml"
                self._sync_screen_select("tab_ovml")
            elif mnemonic in ["AGY", "CHAT", "AI"]:
                tabs.active = "tab_agy"
                self._sync_screen_select("tab_agy")
                try:
                    self.query_one("#agy_input", Input).focus()
                except Exception:
                    pass
            elif mnemonic in ["BETA", "HETA", "CAPM"]:
                tabs.active = "tab_beta"
                self._sync_screen_select("tab_beta")
            elif mnemonic in ["GRPH", "CHART", "GRAPH"]:
                self.action_open_chart()
            elif mnemonic in ["DES", "OVW"]:
                tabs.active = "tab_des"
                self._sync_screen_select("tab_des")
        else:
            tabs.active = "tab_des"
            self._sync_screen_select("tab_des")

    def _sync_ticker_select(self, ticker: str) -> None:
        try:
            sel = self.query_one("#ticker_select", Select)
            covered = get_covered_companies()
            if any(t == ticker for t, _ in covered):
                sel.value = ticker
        except Exception:
            pass

    def _sync_screen_select(self, tab_id: str) -> None:
        try:
            sel = self.query_one("#screen_select", Select)
            sel.value = tab_id
        except Exception:
            pass

    def action_focus_cmd(self) -> None:
        self.query_one("#cmd_input", Input).focus()

def main():
    initial_ticker = "NVDA"
    initial_tab = "tab_des"

    # Command line argument support
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        if arg in ["RV", "TOP10", "MATRIX"]:
            initial_tab = "tab_rv"
        elif arg in ["PORT", "PORTFOLIO"]:
            initial_tab = "tab_port"
        elif arg in ["TOP", "NEWS"]:
            initial_tab = "tab_top"
        elif arg in ["HELP", "?"]:
            initial_tab = "tab_help"
        elif arg in ["AGY", "CHAT", "COPILOT", "AI"]:
            initial_tab = "tab_agy"
        elif arg in ["BETA", "HETA", "CAPM"]:
            initial_tab = "tab_beta"
        else:
            cand = resolve_ticker(arg)
            all_tickers = get_all_active_tickers()
            if cand in all_tickers or len(cand) <= 5:
                initial_ticker = cand
                if len(sys.argv) > 2:
                    sub = sys.argv[2].upper()
                    if sub in ["FA", "FIN"]:
                        initial_tab = "tab_fa"
                    elif sub in ["DCF", "VAL"]:
                        initial_tab = "tab_dcf"
                    elif sub in ["OVML", "4B", "CAPEX"]:
                        initial_tab = "tab_ovml"
                    elif sub in ["AGY", "CHAT", "AI"]:
                        initial_tab = "tab_agy"
                    elif sub in ["BETA", "HETA", "CAPM"]:
                        initial_tab = "tab_beta"
                    elif sub in ["GRPH", "CHART"]:
                        open_beta_chart(cand)
                        return

    app = ERVISTerminalApp(initial_ticker=initial_ticker, initial_tab=initial_tab)
    app.run()

if __name__ == "__main__":
    main()
