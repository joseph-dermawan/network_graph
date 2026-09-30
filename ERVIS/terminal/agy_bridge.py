"""
ERVIS AGY Bridge Interface
Connects the ERVIS Bloomberg Terminal directly to the AGY (Antigravity) CLI runtime.
Enables real-time Equity Research Copilot dialogue and autonomous ticker onboarding across Gates 1-5.
"""

import os
import sys
import shutil
import asyncio
import subprocess
from typing import Dict, Any, Optional, Callable, List

from ERVIS.terminal.data_loader import load_company_data

AGY_CLI_CANDIDATES = [
    os.path.expanduser("~/.local/bin/agy"),
    "/usr/local/bin/agy",
    shutil.which("agy")
]

def find_agy_binary() -> Optional[str]:
    for path in AGY_CLI_CANDIDATES:
        if path and os.path.exists(path) and os.access(path, os.X_OK):
            return path
    return None

class AGYBridge:
    def __init__(self):
        self.cli_path = find_agy_binary()

    def is_available(self) -> bool:
        return self.cli_path is not None

    async def query(self, prompt: str, ticker: Optional[str] = None) -> str:
        """Queries AGY CLI with terminal context for equity research dialogue."""
        ctx_str = ""
        if ticker:
            data = load_company_data(ticker)
            spot = data.get("spot_price") or "N/A"
            target = data.get("target_price") or "N/A"
            rating = data.get("rating") or "N/A"
            wacc = round((data.get("wacc_base") or 0.09) * 100.0, 2)
            dcf = data.get("dcf_value") or "N/A"
            net_debt = data.get("net_debt_b") or "N/A"
            gate4b = data.get("gate_4b") or {}
            
            ctx_str = f"""
[ACTIVE TERMINAL CONTEXT]
TICKER: {ticker} ({data.get('company_name', ticker)})
MARKET SPOT PRICE: ${spot}
TARGET INTRINSIC PRICE: ${target}
PUBLISHED RATING: {rating}
COST OF CAPITAL (WACC): {wacc}%
DCF INTRINSIC VALUE: ${dcf}
NET DEBT: ${net_debt}B
GATE 4B RISK EVALUATION: {gate4b.get('structural_fragility_evaluation', 'N/A')}
"""

        system_instruction = f"""You are the Senior Equity Research Associate at ERVIS Institutional Asset Management.
You are pairing directly with the Lead Portfolio Manager in the Bloomberg Terminal.
{ctx_str}
Respond strictly in institutional research associate tone:
- Monospace Bloomberg Terminal aesthetic. Zero emojis.
- Concise, mathematically grounded, institutional equity research format.
- Use bracketed sections like [MEMO], [VALUATION SENSITIVITY], [CATALYSTS], [RISKS].
- If asked to onboard or ingest a new ticker, explain that the user can execute `INGEST <TICKER>` or explain the 5-Gate methodology.

Portfolio Manager Prompt:
{prompt}
"""

        if not self.is_available():
            return (
                f"[bold red][SYS.ERR] AGY CLI binary not found at ~/.local/bin/agy.[/bold red]\n"
                f"[dim]Please ensure Antigravity CLI is installed and in your PATH.[/dim]"
            )

        try:
            # Execute AGY CLI asynchronously non-interactively with optimized effort
            proc = await asyncio.create_subprocess_exec(
                self.cli_path,
                "--effort", "low",
                "-p",
                system_instruction,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            if proc.returncode == 0:
                resp = stdout.decode("utf-8").strip()
                return resp or "[SYS] AGY returned empty response."
            else:
                err_msg = stderr.decode("utf-8").strip()
                return f"[bold red][SYS.AGY_ERR][/bold red] Returncode {proc.returncode}: {err_msg}"
        except Exception as e:
            return f"[bold red][SYS.EXCEPTION][/bold red] Failed to communicate with AGY: {str(e)}"

    async def onboard_ticker(
        self,
        ticker: str,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """Runs the 5-Gate autonomous onboarding engine for an uncovered ticker."""
        ticker = ticker.strip().upper()
        if progress_callback:
            progress_callback(f"[SYS.01] Launching ERVIS 5-Gate Ingestion Engine for {ticker}...")

        from ERVIS.models.auto_onboard import run_auto_onboard

        loop = asyncio.get_running_loop()
        try:
            if progress_callback:
                progress_callback(f"[SYS.02] Querying SEC EDGAR & market feeds for {ticker} financials...")

            # Run in worker thread to prevent blocking Textual TUI
            outputs = await loop.run_in_executor(None, run_auto_onboard, ticker)

            if progress_callback:
                progress_callback(
                    f"[SYS.OK] 5-Gate pipeline completed. Intrinsic target: "
                    f"${outputs['final_triangulation'].get('target_price_usd')} "
                    f"({outputs['final_triangulation'].get('rating')})."
                )

            # Trigger AGY synthesis memo in background
            if self.is_available():
                if progress_callback:
                    progress_callback(f"[SYS.03] Synthesizing institutional research memo via AGY...")
                memo_prompt = f"Write an institutional 1-paragraph research thesis memo for {ticker} based on intrinsic value ${outputs['final_triangulation'].get('target_price_usd')} vs spot ${outputs.get('spot_price_usd')}."
                try:
                    memo_res = await self.query(memo_prompt, ticker=ticker)
                    outputs["agy_thesis_memo"] = memo_res
                except Exception:
                    pass

            return outputs
        except Exception as e:
            if progress_callback:
                progress_callback(f"[SYS.ERR] Failed to onboard {ticker}: {str(e)}")
            raise e

_BRIDGE_INSTANCE: Optional[AGYBridge] = None

def get_agy_bridge() -> AGYBridge:
    global _BRIDGE_INSTANCE
    if _BRIDGE_INSTANCE is None:
        _BRIDGE_INSTANCE = AGYBridge()
    return _BRIDGE_INSTANCE
