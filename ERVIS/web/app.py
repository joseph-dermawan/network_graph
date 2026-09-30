"""
ERVIS Institutional Web Workstation Backend
FastAPI server delivering Bloomberg Terminal aesthetic web application
with live AGY Equity Research Copilot integration and native text/clipboard operations.
"""

import os
import sys
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ERVIS.terminal.data_loader import (
    load_company_data,
    get_top10_matrix,
    get_portfolio_data,
    get_fa_financial_trends,
    resolve_ticker,
    get_covered_companies,
    get_all_active_tickers
)
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
    render_unknown_ticker
)
from rich.console import Console
from ERVIS.terminal.agy_bridge import get_agy_bridge

app = FastAPI(title="ERVIS Institutional Web Workstation", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    ticker: Optional[str] = "NVDA"

INDEX_HTML_PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    if os.path.exists(INDEX_HTML_PATH):
        with open(INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>ERVIS Web Workstation UI Template Initializing...</h1>"

@app.get("/api/companies")
async def list_companies():
    covered = get_covered_companies()
    result = []
    for t, name in covered:
        d = load_company_data(t)
        result.append({
            "ticker": t,
            "name": name,
            "spot_price": d.get("spot_price"),
            "target_price": d.get("target_price"),
            "rating": d.get("rating", "N/A"),
            "currency": d.get("currency", "USD"),
            "has_model": d.get("spot_price") is not None or d.get("dcf_value") is not None
        })
    return result

@app.get("/api/company/{ticker}")
async def get_company(ticker: str):
    norm_ticker = resolve_ticker(ticker)
    data = load_company_data(norm_ticker)
    if not data or (data.get("spot_price") is None and data.get("dcf_value") is None):
        # Unmodeled security
        return {
            "ticker": norm_ticker,
            "status": "UNMODELED",
            "message": f"Security {norm_ticker} is not yet in the valuation registry.",
            "data": data
        }
    return {
        "ticker": norm_ticker,
        "status": "LOADED",
        "data": data
    }

@app.get("/api/financials/{ticker}")
async def get_financials(ticker: str):
    norm_ticker = resolve_ticker(ticker)
    trends = get_fa_financial_trends(norm_ticker)
    return trends

@app.get("/api/matrix")
async def get_matrix():
    return get_top10_matrix()

@app.get("/api/portfolio")
async def get_portfolio():
    return get_portfolio_data()

@app.post("/api/chat")
async def chat_copilot(req: ChatRequest):
    bridge = get_agy_bridge()
    ticker = resolve_ticker(req.ticker) if req.ticker else "NVDA"
    try:
        response_text = await bridge.query(req.prompt, ticker=ticker)
        return {"response": response_text, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/onboard/{ticker}")
async def onboard_security(ticker: str):
    norm_ticker = resolve_ticker(ticker)
    bridge = get_agy_bridge()
    try:
        outputs = await bridge.onboard_ticker(norm_ticker)
        return {
            "status": "ok",
            "ticker": norm_ticker,
            "outputs": outputs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/render/{screen}/{ticker}")
async def render_terminal_screen(screen: str, ticker: str, width: int = 132):
    norm_ticker = resolve_ticker(ticker)
    screen_upper = screen.upper()
    
    # Allow width up to 260 characters to fill 100% of widescreen displays
    w = max(110, min(260, width))
    console = Console(record=True, width=w, height=60, force_terminal=True)
    
    if screen_upper in ["DES", "OVW"]:
        panel = render_overview(norm_ticker)
    elif screen_upper == "FA":
        panel = render_fa_screen(norm_ticker)
    elif screen_upper in ["DCF", "VAL"]:
        panel = render_dcf_screen(norm_ticker)
    elif screen_upper in ["BETA", "CAPM", "HETA"]:
        panel = render_beta_screen(norm_ticker)
    elif screen_upper in ["OVML", "4B"]:
        panel = render_gate_4b(norm_ticker)
    elif screen_upper in ["RV", "TOP10"]:
        panel = render_top10_matrix_panel()
    elif screen_upper == "PORT":
        panel = render_portfolio_desk()
    elif screen_upper in ["TOP", "NEWS"]:
        panel = render_news_screen()
    elif screen_upper == "HELP":
        panel = render_help()
    else:
        panel = render_overview(norm_ticker)
        
    console.print(panel)
    html_snippet = console.export_html(inline_styles=True, code_format="{code}")
    
    # Basic company stats for synchronized header display
    comp_data = load_company_data(norm_ticker) or {}
    
    return {
        "screen": screen_upper,
        "ticker": norm_ticker,
        "html": html_snippet,
        "stats": {
            "name": comp_data.get("company_name", norm_ticker),
            "spot": comp_data.get("spot_price"),
            "target": comp_data.get("target_price"),
            "rating": comp_data.get("rating", "N/A"),
            "currency": comp_data.get("currency", "USD"),
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("ERVIS.web.app:app", host="127.0.0.1", port=8000, reload=True)
