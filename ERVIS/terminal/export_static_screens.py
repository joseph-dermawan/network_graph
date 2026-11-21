#!/usr/bin/env python3
"""
ERVIS Terminal Static Screen & Model Exporter
Pre-renders all authentic Bloomberg Terminal screens (DES, FA, DCF, 4B, BETA, NEWS, RV, PORT, HELP)
into standalone HTML snippets and bundles them into a unified JSON file for Cloudflare Pages.
"""

import os
import sys
import json
from rich.console import Console

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ERVIS.terminal.data_loader import (
    get_covered_companies,
    load_company_data,
    get_top10_matrix,
    get_portfolio_data,
    resolve_ticker
)
from ERVIS.terminal.renderer import (
    render_overview,
    render_fa_screen,
    render_dcf_screen,
    render_beta_screen,
    render_gate_4b,
    render_news_screen,
    render_top10_matrix_panel,
    render_portfolio_desk,
    render_help
)

OUTPUT_FILE = os.path.join(BASE_DIR, "terminal_screens_cache.json")
ERVIS_DEPLOY_SCREENS = "/Users/worldofmadness/Documents/VS Code/Personal Projects/ervis-terminal/terminal/data/screens.json"

def export_all():
    print("[EXPORTER] Initializing Rich Terminal Console (width=132, force_terminal=False)...")
    console = Console(record=True, width=132, force_terminal=False, color_system="truecolor")
    
    covered = get_covered_companies()
    print(f"[EXPORTER] Discovered {len(covered)} covered companies.")
    
    payload = {
        "generated_at": "2026-11-21T10:50:00Z",
        "companies": [],
        "screens": {},
        "global_screens": {}
    }
    
    # 1. Export Global Screens
    print("[EXPORTER] Rendering Global Screens: RV, PORT, HELP...")
    for g_name, fn in [("RV", render_top10_matrix_panel), ("PORT", render_portfolio_desk), ("HELP", render_help)]:
        try:
            panel = fn()
            console.print(panel)
            html = console.export_html(inline_styles=True, code_format="{code}")
            payload["global_screens"][g_name] = html
            print(f"  ✓ Global {g_name} rendered successfully ({len(html)} bytes)")
        except Exception as e:
            print(f"  ✗ Failed to render global {g_name}: {e}")
            
    # 2. Export Per-Ticker Screens
    screen_funcs = [
        ("DES", render_overview),
        ("FA", render_fa_screen),
        ("DCF", render_dcf_screen),
        ("4B", render_gate_4b),
        ("BETA", render_beta_screen),
        ("NEWS", render_news_screen)
    ]
    
    for ticker, name in covered:
        norm_t = resolve_ticker(ticker)
        d = load_company_data(norm_t) or {}
        
        comp_summary = {
            "ticker": norm_t,
            "name": name,
            "spot_price": d.get("spot_price"),
            "target_price": d.get("target_price") or d.get("dcf_value"),
            "rating": d.get("rating", "N/A"),
            "currency": d.get("currency", "USD"),
            "market_cap_b": d.get("market_cap_b"),
            "wacc_base": d.get("wacc_base"),
            "net_debt_b": d.get("net_debt_b")
        }
        payload["companies"].append(comp_summary)
        
        print(f"[EXPORTER] Processing {norm_t} ({name})...")
        for s_name, fn in screen_funcs:
            key = f"{norm_t}_{s_name}"
            try:
                panel = fn(norm_t)
                console.print(panel)
                html = console.export_html(inline_styles=True, code_format="{code}")
                payload["screens"][key] = html
            except Exception as e:
                print(f"  ✗ Failed {key}: {e}")
                
    # Save output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f)
        
    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"[EXPORTER] Complete! Exported to {OUTPUT_FILE} ({size_mb:.2f} MB)")

    if os.path.exists(os.path.dirname(ERVIS_DEPLOY_SCREENS)):
        import shutil
        shutil.copy2(OUTPUT_FILE, ERVIS_DEPLOY_SCREENS)
        print(f"[EXPORTER] Synchronized to live deployment: {ERVIS_DEPLOY_SCREENS}")

    return OUTPUT_FILE

if __name__ == "__main__":
    export_all()
