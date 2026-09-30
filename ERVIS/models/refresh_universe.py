#!/usr/bin/env python3
"""
ERVIS Live Market Data & News Refresh Pipeline
Refreshes live spot prices, market capitalizations, valuation gap percentages,
institutional ratings, and live breaking market news across all covered securities.
Synchronizes JSON project models, YAML registry, and SQLite vault.
"""

import os
import sys
import json
import math
import sqlite3
import yaml
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

try:
    import yfinance as yf
except ImportError:
    yf = None

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REGISTRY_PATH = os.path.join(BASE_DIR, "kb", "registry", "company_sheets.yaml")
VAULT_DB_PATH = os.path.join(BASE_DIR, "vault", "ervis_vault.db")
NEWS_CACHE_PATH = os.path.join(BASE_DIR, "vault", "live_news.json")

ACTIVE_SECURITIES = [
    {"ticker": "NVDA", "yf_symbol": "NVDA", "currency": "USD", "name": "NVIDIA Corporation", "market": "US_EQUITIES"},
    {"ticker": "MSFT", "yf_symbol": "MSFT", "currency": "USD", "name": "Microsoft Corporation", "market": "US_EQUITIES"},
    {"ticker": "AAPL", "yf_symbol": "AAPL", "currency": "USD", "name": "Apple Inc.", "market": "US_EQUITIES"},
    {"ticker": "GOOGL", "yf_symbol": "GOOGL", "currency": "USD", "name": "Alphabet Inc.", "market": "US_EQUITIES"},
    {"ticker": "AMZN", "yf_symbol": "AMZN", "currency": "USD", "name": "Amazon.com, Inc.", "market": "US_EQUITIES"},
    {"ticker": "META", "yf_symbol": "META", "currency": "USD", "name": "Meta Platforms, Inc.", "market": "US_EQUITIES"},
    {"ticker": "AVGO", "yf_symbol": "AVGO", "currency": "USD", "name": "Broadcom Inc.", "market": "US_EQUITIES"},
    {"ticker": "TSM", "yf_symbol": "TSM", "currency": "USD", "name": "Taiwan Semiconductor Manufacturing", "market": "US_EQUITIES"},
    {"ticker": "AMD", "yf_symbol": "AMD", "currency": "USD", "name": "Advanced Micro Devices, Inc.", "market": "US_EQUITIES"},
    {"ticker": "ORCL", "yf_symbol": "ORCL", "currency": "USD", "name": "Oracle Corporation", "market": "US_EQUITIES"},
    {"ticker": "RR", "yf_symbol": "RR.L", "currency": "GBP", "name": "Rolls-Royce Holdings plc", "market": "UK_EQUITIES"},
    {"ticker": "PLTR", "yf_symbol": "PLTR", "currency": "USD", "name": "Palantir Technologies Inc.", "market": "US_EQUITIES"},
]

def derive_institutional_rating(gap_pct: float) -> str:
    """Classifies valuation gap into institutional portfolio action rating."""
    if gap_pct >= 20.0:
        return f"ACCUMULATE / STRONG BUY ({gap_pct:+.1f}%)"
    elif gap_pct >= 8.0:
        return f"OVERWEIGHT / ACCUMULATE ({gap_pct:+.1f}%)"
    elif gap_pct >= -5.0:
        return f"NEUTRAL / HOLD ({gap_pct:+.1f}%)"
    elif gap_pct >= -15.0:
        return f"TRIM / TAKE PROFITS ({gap_pct:+.1f}%)"
    else:
        return f"UNDERWEIGHT / SELL ({gap_pct:+.1f}%)"

def derive_strategic_implication(ticker: str, title: str, summary: str) -> str:
    """Generates institutional asset class and valuation implication from news content."""
    text = (title + " " + summary).lower()
    if any(k in text for k in ["data center", "capex", "gpu", "infrastructure", "cloud", "capacity", "power"]):
        return f"AI Infrastructure CapEx: Directly impacts {ticker}'s capital intensity and multi-year depreciation run-rate."
    elif any(k in text for k in ["regulation", "antitrust", "investigation", "suit", "ban", "tariff", "export"]):
        return f"Regulatory & Geopolitical: Heightens hurdle rate / Gate 3 sovereign risk spread."
    elif any(k in text for k in ["earnings", "revenue", "margin", "guidance", "profit"]):
        return f"Operational Earnings: Signals revisions to Gate 4 discrete FCFF trajectory."
    elif any(k in text for k in ["dividend", "buyback", "cash flow", "repurchase"]):
        return f"Capital Allocation: Accretive to shareholder yield and net cash balance sheet fortress."
    else:
        return f"Market Momentum: Macro multiple adjustment across high-beta tech coverage."

def refresh_all_data():
    print(f"\n=======================================================")
    print(f"  ERVIS UNIVERSE REFRESH PIPELINE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=======================================================\n")

    if not yf:
        print("[ERROR] yfinance package is required for live data refresh.")
        return

    all_news_items = []
    summary_report = []

    conn = sqlite3.connect(VAULT_DB_PATH)
    cur = conn.cursor()

    # Load registry
    registry = {}
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                reg_data = yaml.safe_load(f)
                registry = reg_data.get("COMPANIES", {})
        except Exception as e:
            print(f"[WARN] Failed to read registry: {e}")

    for sec in ACTIVE_SECURITIES:
        ticker = sec["ticker"]
        yf_sym = sec["yf_symbol"]
        curr = sec["currency"]
        market = sec["market"]
        name = sec["name"]

        print(f"--> Refreshing {ticker} ({yf_sym})...", end=" ", flush=True)

        try:
            yt = yf.Ticker(yf_sym)
            fi = yt.fast_info
            
            spot_raw = fi.last_price or fi.previous_close
            prev_close = fi.previous_close or spot_raw
            mcap_raw = fi.market_cap

            if spot_raw is None or spot_raw <= 0:
                print(f"[FAILED: No live price returned]")
                continue

            # Currency normalization for UK pence (GBp -> GBP)
            if curr == "GBP" and fi.currency in ["GBp", "GBX"]:
                spot_price = round(spot_raw / 100.0, 4)
                mcap_b = round(mcap_raw / 1e9 / 100.0, 2) if mcap_raw else None
            else:
                spot_price = round(spot_raw, 2)
                mcap_b = round(mcap_raw / 1e9, 2) if mcap_raw else None

            # 1. Update Project Models JSON
            proj_dir = os.path.join(BASE_DIR, "projects", market, ticker)
            models_dir = os.path.join(proj_dir, "models")
            val_json_path = os.path.join(models_dir, "valuation_engine_outputs.json")

            target_price = None
            dcf_val = None
            sotp_val = None
            mc_val = None
            wacc_base = 0.09
            wacc_term = 0.09
            hamada_beta = 1.10

            if os.path.exists(val_json_path):
                with open(val_json_path, "r", encoding="utf-8") as f:
                    vdata = json.load(f)

                # Spot price update
                if curr == "GBP":
                    vdata["spot_price_gbp"] = spot_price
                    vdata["spot_price_pence"] = round(spot_price * 100.0, 2)
                else:
                    vdata["spot_price_usd"] = spot_price

                if mcap_b:
                    vdata["market_cap_m"] = round(mcap_b * 1000.0, 2)

                # Extract intrinsic targets
                if "final_triangulation" in vdata and vdata["final_triangulation"]:
                    target_price = vdata["final_triangulation"].get("target_price_usd") or vdata["final_triangulation"].get("target_price_gbp")
                elif "gate_4_valuation" in vdata and vdata["gate_4_valuation"]:
                    target_price = vdata["gate_4_valuation"].get("final_target_price_usd") or vdata["gate_4_valuation"].get("blended_target_price_usd")
                elif "final_target_price_usd" in vdata:
                    target_price = vdata["final_target_price_usd"]

                # Fallback to DCF if no blended target
                if not target_price:
                    if "dcf_schedule" in vdata and vdata["dcf_schedule"]:
                        target_price = vdata["dcf_schedule"].get("dcf_intrinsic_value_usd") or vdata["dcf_schedule"].get("dcf_intrinsic_value_gbp")
                    elif "dcf_intrinsic_value_usd" in vdata:
                        target_price = vdata["dcf_intrinsic_value_usd"]

                # If still None, look in registry
                if not target_price and ticker in registry:
                    target_price = registry[ticker].get("last_intrinsic_value")

                # If target price exists, recalculate gap and rating
                if target_price:
                    gap_pct = round(((target_price - spot_price) / spot_price) * 100.0, 2)
                    rating = derive_institutional_rating(gap_pct)

                    # Update final_triangulation
                    if "final_triangulation" not in vdata or not vdata["final_triangulation"]:
                        vdata["final_triangulation"] = {}
                    
                    if curr == "GBP":
                        vdata["final_triangulation"]["target_price_gbp"] = target_price
                    else:
                        vdata["final_triangulation"]["target_price_usd"] = target_price
                    
                    vdata["final_triangulation"]["upside_percent"] = gap_pct
                    vdata["final_triangulation"]["rating"] = rating
                    vdata["final_triangulation"]["updated_at"] = datetime.now().isoformat()

                    if "gate_4_valuation" in vdata and vdata["gate_4_valuation"]:
                        vdata["gate_4_valuation"]["final_rating"] = rating
                        vdata["gate_4_valuation"]["upside_pct"] = gap_pct

                # Extract components for vault
                if "dcf_schedule" in vdata and vdata["dcf_schedule"]:
                    dcf_val = vdata["dcf_schedule"].get("dcf_intrinsic_value_usd") or vdata["dcf_schedule"].get("dcf_intrinsic_value_gbp")
                elif "dcf_intrinsic_value_usd" in vdata:
                    dcf_val = vdata["dcf_intrinsic_value_usd"]
                elif "gate_4_valuation" in vdata and vdata["gate_4_valuation"]:
                    dcf_val = vdata["gate_4_valuation"].get("dcf_intrinsic_value_usd")

                if "sotp_divisional" in vdata and vdata["sotp_divisional"]:
                    sotp_val = vdata["sotp_divisional"].get("sotp_intrinsic_usd") or vdata["sotp_divisional"].get("sotp_intrinsic_gbp")
                elif "gate_4_valuation" in vdata and vdata["gate_4_valuation"]:
                    sotp_val = vdata["gate_4_valuation"].get("sotp_intrinsic_value_usd")

                if "monte_carlo_10k" in vdata and vdata["monte_carlo_10k"]:
                    mc_val = vdata["monte_carlo_10k"].get("median_usd") or vdata["monte_carlo_10k"].get("median_gbp")
                elif "gate_4_valuation" in vdata and vdata["gate_4_valuation"] and "monte_carlo_10k" in vdata["gate_4_valuation"]:
                    mc_val = vdata["gate_4_valuation"]["monte_carlo_10k"].get("median_usd")

                if "wacc_schedule" in vdata and vdata["wacc_schedule"]:
                    wacc_base = vdata["wacc_schedule"].get("base_wacc", 0.09)
                    wacc_term = vdata["wacc_schedule"].get("terminal_wacc", 0.09)
                elif "gate_3_cost_of_capital" in vdata and vdata["gate_3_cost_of_capital"]:
                    wacc_base = vdata["gate_3_cost_of_capital"].get("base_wacc", 0.09)
                    wacc_term = vdata["gate_3_cost_of_capital"].get("terminal_wacc", 0.09)
                    hamada_beta = vdata["gate_3_cost_of_capital"].get("hamada_levered_beta", 1.10)

                # Save updated JSON
                with open(val_json_path, "w", encoding="utf-8") as f:
                    json.dump(vdata, f, indent=2)

            else:
                # No project dir yet
                gap_pct = 0.0
                rating = "UNCOVERED"

            # 2. Update Registry YAML
            if ticker in registry:
                registry[ticker]["last_spot_price"] = spot_price
                if target_price:
                    registry[ticker]["last_intrinsic_value"] = target_price
                    registry[ticker]["published_rating"] = rating
                    registry[ticker]["last_published_at"] = datetime.now().isoformat()

            # 3. Synchronize SQLite Vault
            cur.execute("""
                INSERT INTO securities (ticker, company_name, market, currency, spot_price, target_price, published_rating, valuation_gap_pct, market_cap_b, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(ticker) DO UPDATE SET
                    spot_price = excluded.spot_price,
                    target_price = coalesce(excluded.target_price, securities.target_price),
                    published_rating = coalesce(excluded.published_rating, securities.published_rating),
                    valuation_gap_pct = coalesce(excluded.valuation_gap_pct, securities.valuation_gap_pct),
                    market_cap_b = coalesce(excluded.market_cap_b, securities.market_cap_b),
                    updated_at = CURRENT_TIMESTAMP
            """, (ticker, name, market, curr, spot_price, target_price, rating if target_price else None, gap_pct if target_price else None, mcap_b))

            if target_price:
                cur.execute("""
                    INSERT INTO valuation_snapshots
                    (snapshot_date, ticker, spot_price, final_target_price, valuation_gap_pct, published_rating, base_wacc_pct, terminal_wacc_pct, hamada_beta, dcf_intrinsic_value, sotp_intrinsic_value, monte_carlo_median)
                    VALUES (CURRENT_DATE, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    ticker, spot_price, target_price, gap_pct, rating,
                    round(wacc_base * 100.0, 2), round(wacc_term * 100.0, 2), hamada_beta,
                    dcf_val, sotp_val, mc_val
                ))

            # 4. Fetch Live News via yfinance
            try:
                raw_news = yt.news or []
                for n in raw_news:
                    c = n.get("content", {})
                    title = c.get("title") or n.get("title")
                    if not title:
                        continue
                    pub = c.get("pubDate") or n.get("pubDate") or datetime.now().isoformat()
                    summary = c.get("summary") or n.get("summary") or ""
                    url = c.get("canonicalUrl", {}).get("url") or c.get("clickThroughUrl", {}).get("url") or n.get("link") or ""
                    provider = c.get("provider", {}).get("displayName") or n.get("publisher") or "Marketwire"

                    all_news_items.append({
                        "id": n.get("id", str(hash(title))),
                        "ticker": ticker,
                        "title": title,
                        "pub_date": pub,
                        "date_str": pub[:10] if len(pub) >= 10 else datetime.now().strftime("%Y-%m-%d"),
                        "summary": summary,
                        "url": url,
                        "provider": provider,
                        "implication": derive_strategic_implication(ticker, title, summary)
                    })
            except Exception as e:
                print(f"[News Error: {e}]", end=" ")

            curr_sym = "£" if curr == "GBP" else "$"
            target_str = f"{curr_sym}{target_price:.2f}" if target_price else "N/A"
            gap_str = f"{gap_pct:+.1f}%" if target_price else "N/A"
            print(f"[OK] Spot: {curr_sym}{spot_price:,.2f} | Target: {target_str} | Gap: {gap_str} | News: {len(raw_news)}")

            summary_report.append({
                "ticker": ticker,
                "spot": spot_price,
                "target": target_price,
                "gap": gap_pct if target_price else None,
                "rating": rating if target_price else "UNCOVERED",
                "mcap": mcap_b,
                "currency": curr
            })

        except Exception as e:
            print(f"[ERROR: {e}]")

    conn.commit()
    conn.close()

    # Save registry YAML
    if registry:
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                full_yaml = yaml.safe_load(f) or {}
            full_yaml["COMPANIES"] = registry
            with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
                yaml.dump(full_yaml, f, sort_keys=False, default_flow_style=False)
            print(f"\n[REGISTRY] Synchronized company_sheets.yaml.")
        except Exception as e:
            print(f"[REGISTRY ERROR] {e}")

    # Process and save news feed
    # Deduplicate news by title
    seen_titles = set()
    unique_news = []
    for item in sorted(all_news_items, key=lambda x: x["pub_date"], reverse=True):
        if item["title"] not in seen_titles:
            seen_titles.add(item["title"])
            unique_news.append(item)

    with open(NEWS_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "count": len(unique_news),
            "news": unique_news
        }, f, indent=2)

    print(f"[NEWS DESK] Cached {len(unique_news)} real-time institutional intelligence reports to {NEWS_CACHE_PATH}")
    print(f"\n[DONE] ERVIS Universe successfully synchronized to live market data.\n")
    return summary_report

if __name__ == "__main__":
    refresh_all_data()
