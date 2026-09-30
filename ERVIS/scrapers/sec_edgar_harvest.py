#!/usr/bin/env python3
"""
ERVIS SEC EDGAR Harvester
Pulls standardized financial statements and XBRL facts directly from the SEC EDGAR API.
Zero manual filing hunt required for US equities.
"""

import os
import sys
import json
import ssl
import urllib.request
from datetime import datetime

USER_AGENT = "ERVIS_Agent/1.0 (Equity Research & Valuation; admin@ervis.org)"
TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"

def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def get_cik_for_ticker(ticker):
    ticker = ticker.upper()
    req = urllib.request.Request(TICKERS_URL, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, context=get_ssl_context(), timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data.values():
                if item.get("ticker") == ticker:
                    cik = str(item.get("cik_str")).zfill(10)
                    title = item.get("title")
                    return cik, title
    except Exception as e:
        print(f"Notice: CIK lookup error ({e}). Using cached lookup.")
    # Standard cache for major tickers
    cache = {
        "KO": ("0000021344", "Coca-Cola Co"),
        "AAPL": ("0000320193", "Apple Inc"),
        "POWL": ("0000080420", "Powell Industries Inc"),
        "MSFT": ("0000789019", "Microsoft Corp")
    }
    return cache.get(ticker, (None, ticker))

def harvest_company_facts(ticker, output_dir=None):
    cik, company_name = get_cik_for_ticker(ticker)
    if not cik:
        print(f"Error: Could not resolve CIK for ticker {ticker}")
        return None

    print(f"[{datetime.now().isoformat()}] Fetching SEC EDGAR XBRL facts for {company_name} (CIK: {cik})...")
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(req, context=get_ssl_context(), timeout=15) as resp:
            raw_facts = json.loads(resp.read().decode("utf-8"))
            print(f"Successfully harvested {len(raw_facts.get('facts', {}).get('us-gaap', {}))} US-GAAP line item facts.")
            
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                out_path = f"{output_dir}/sec_facts_cik_{cik}.json"
                with open(out_path, "w") as f:
                    json.dump(raw_facts, f, indent=2)
                print(f"Saved SEC facts to: {out_path}")
            return raw_facts
    except Exception as e:
        print(f"Notice: SEC EDGAR query encountered ({e}).")
        return None

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "KO"
    dest = sys.argv[2] if len(sys.argv) > 2 else f"ERVIS/projects/US_EQUITIES/{t}/raw_filings"
    harvest_company_facts(t, dest)
