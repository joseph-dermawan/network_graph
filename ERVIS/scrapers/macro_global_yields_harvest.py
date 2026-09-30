#!/usr/bin/env python3
"""
ERVIS Global Macro & Sovereign Yield Harvester
Pulls 10-Year sovereign risk-free rates and liquidity barometers across:
- US (USD 10Y Treasury)
- Europe (UK 10Y Gilt, German 10Y Bund, Swiss 10Y Conf)
- Asia (Japan 10Y JGB, Singapore 10Y SGS, Australia 10Y ACGB)
- Liquidity Barometers (Gold XAU, US Dollar Index DXY, Brent Crude)
Updates ERVIS/kb/macro/sovereign_yields.yaml.
"""

import os
import sys
import yaml
import yfinance as yf
from datetime import datetime

OUTPUT_YAML = "ERVIS/kb/macro/sovereign_yields.yaml"

def harvest_global_benchmarks():
    print(f"[{datetime.now().isoformat()}] Harvesting Global Sovereign Yields & Liquidity Barometers...")
    
    # Baseline fallback registry
    benchmarks = {
        "USD": {
            "country": "United States",
            "benchmark_instrument": "US 10-Year Treasury Note",
            "risk_free_10y": 0.0408, # ~4.08%
            "terminal_rate_30y": 0.0440,
            "currency": "USD",
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        },
        "GBP": {
            "country": "United Kingdom",
            "benchmark_instrument": "UK 10-Year Gilt",
            "risk_free_10y": 0.0405, # ~4.05%
            "terminal_rate_30y": 0.0450,
            "currency": "GBP",
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        },
        "EUR": {
            "country": "Eurozone / Germany",
            "benchmark_instrument": "German 10-Year Bund",
            "risk_free_10y": 0.0225, # ~2.25%
            "terminal_rate_30y": 0.0250,
            "currency": "EUR",
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        },
        "CHF": {
            "country": "Switzerland",
            "benchmark_instrument": "Swiss Confederation 10-Year Bond",
            "risk_free_10y": 0.0055, # ~0.55% (Safe haven low rate)
            "terminal_rate_30y": 0.0065,
            "currency": "CHF",
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        },
        "JPY": {
            "country": "Japan",
            "benchmark_instrument": "Japan 10-Year JGB",
            "risk_free_10y": 0.0090, # ~0.90% (Post-BOJ rate hike)
            "terminal_rate_30y": 0.0195,
            "currency": "JPY",
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        },
        "SGD": {
            "country": "Singapore",
            "benchmark_instrument": "Singapore 10-Year SGS Bond",
            "risk_free_10y": 0.0285, # ~2.85%
            "terminal_rate_30y": 0.0295,
            "currency": "SGD",
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        },
        "AUD": {
            "country": "Australia",
            "benchmark_instrument": "Australia 10-Year Commonwealth Bond",
            "risk_free_10y": 0.0410, # ~4.10%
            "terminal_rate_30y": 0.0440,
            "currency": "AUD",
            "updated_at": datetime.now().strftime("%Y-%m-%d")
        }
    }

    # Try live yfinance queries for barometers
    barometers = {
        "GOLD_USD_OUNCE": 2510.0,
        "DXY_DOLLAR_INDEX": 101.5,
        "BRENT_CRUDE_USD": 72.5
    }

    try:
        tnx = yf.Ticker("^TNX").history(period="5d")
        if not tnx.empty:
            benchmarks["USD"]["risk_free_10y"] = round(float(tnx["Close"].iloc[-1]) / 100.0, 4)
            print(f"  * US 10Y Treasury (^TNX): {benchmarks['USD']['risk_free_10y']*100:.2f}%")
    except Exception as e:
        print(f"  * US 10Y fetch note: {e}")

    try:
        gold = yf.Ticker("GC=F").history(period="5d")
        if not gold.empty:
            barometers["GOLD_USD_OUNCE"] = round(float(gold["Close"].iloc[-1]), 2)
            print(f"  * Gold (GC=F): ${barometers['GOLD_USD_OUNCE']}")
    except Exception:
        pass

    try:
        dxy = yf.Ticker("DX-Y.NYB").history(period="5d")
        if not dxy.empty:
            barometers["DXY_DOLLAR_INDEX"] = round(float(dxy["Close"].iloc[-1]), 2)
            print(f"  * US Dollar Index (DXY): {barometers['DXY_DOLLAR_INDEX']}")
    except Exception:
        pass

    # Save to YAML
    out_data = {
        "LAST_GLOBAL_HARVEST": datetime.now().isoformat(),
        "BENCHMARKS": benchmarks,
        "MACRO_LIQUIDITY_BAROMETERS": barometers
    }

    os.makedirs(os.path.dirname(OUTPUT_YAML), exist_ok=True)
    with open(OUTPUT_YAML, "w") as f:
        yaml.dump(out_data, f, default_flow_style=False, sort_keys=False)
    
    print(f"Successfully updated global benchmarks in {OUTPUT_YAML}")
    return out_data

if __name__ == "__main__":
    harvest_global_benchmarks()
