"""
ERVIS Terminal Data Loader
Provides unified access to institutional valuation models, Gate 4B metrics,
macro tables, and seed portfolio tracking.
"""

import os
import json
import yaml
from typing import Dict, Any, List, Optional, Tuple

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REGISTRY_PATH = os.path.join(BASE_DIR, "kb", "registry", "company_sheets.yaml")

TOP10_TICKERS = ["NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META", "AVGO", "TSM", "AMD", "ORCL"]
ALL_ACTIVE_TICKERS = ["NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META", "AVGO", "TSM", "AMD", "ORCL", "RR"]

COVERED_COMPANIES = [
    ("NVDA", "NVIDIA Corp"),
    ("MSFT", "Microsoft Corp"),
    ("AAPL", "Apple Inc"),
    ("GOOGL", "Alphabet Inc"),
    ("AMZN", "Amazon.com Inc"),
    ("META", "Meta Platforms"),
    ("AVGO", "Broadcom Inc"),
    ("TSM", "Taiwan Semi (TSMC)"),
    ("AMD", "Adv Micro Devices"),
    ("ORCL", "Oracle Corp"),
    ("RR", "Rolls-Royce Holdings"),
]

def get_covered_companies() -> List[Tuple[str, str]]:
    """Returns dynamic list of all covered companies across registry and local project models."""
    res_dict = dict(COVERED_COMPANIES)
    reg = load_registry()
    for t, info in reg.items():
        if t not in res_dict and isinstance(info, dict):
            res_dict[t] = info.get("company_name", t)
    
    # Scan projects folder
    for mkt in ["US_EQUITIES", "UK_EQUITIES", "SG_EQUITIES"]:
        mkt_path = os.path.join(BASE_DIR, "projects", mkt)
        if os.path.exists(mkt_path):
            for entry in os.listdir(mkt_path):
                t_upper = entry.upper()
                if t_upper not in res_dict and os.path.isdir(os.path.join(mkt_path, entry)):
                    out_json = os.path.join(mkt_path, entry, "models", "valuation_engine_outputs.json")
                    if os.path.exists(out_json):
                        try:
                            with open(out_json, "r", encoding="utf-8") as f:
                                d = json.load(f)
                                res_dict[t_upper] = d.get("company_name", t_upper)
                        except Exception:
                            res_dict[t_upper] = t_upper
    return list(res_dict.items())

def get_all_active_tickers() -> List[str]:
    """Returns all active tickers available in the system."""
    return [t for t, _ in get_covered_companies()]


TICKER_ALIASES: Dict[str, str] = {
    "R.R": "RR",
    "RR.": "RR",
    "R.R.": "RR",
    "RYCEY": "RR",
    "ROLLS": "RR",
    "ROLLS-ROYCE": "RR",
    "ROLLS_ROYCE": "RR",
    "GOOG": "GOOGL",
    "FB": "META",
    "TSMC": "TSM",
    "2330": "TSM",
    "BRK.B": "BRK-B",
    "BRKB": "BRK-B",
}

def resolve_ticker(raw_ticker: str) -> str:
    """Normalizes raw input ticker string to canonical ERVIS ticker."""
    if not raw_ticker:
        return "NVDA"
    cleaned = raw_ticker.strip().upper().replace(" ", "")
    return TICKER_ALIASES.get(cleaned, cleaned)

MASTER_NET_DEBT_B = {
    "NVDA": -48.91,
    "MSFT": -2.03,
    "AAPL": -20.56,
    "GOOGL": -64.67,
    "AMZN": 39.46,
    "META": -25.22,
    "AVGO": 37.59,
    "TSM": -78.80,
    "AMD": -7.82,
    "ORCL": 118.85,
    "RR": 1.20
}

def load_registry() -> Dict[str, Any]:
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("COMPANIES", {})
        except Exception:
            pass
    return {}

def find_project_dir(ticker: str) -> Optional[str]:
    for mkt in ["US_EQUITIES", "UK_EQUITIES", "SG_EQUITIES"]:
        candidate = os.path.join(BASE_DIR, "projects", mkt, ticker.upper())
        if os.path.exists(candidate):
            return candidate
    return None

def load_company_data(ticker: str) -> Dict[str, Any]:
    ticker = resolve_ticker(ticker)
    proj_dir = find_project_dir(ticker)
    registry = load_registry()
    reg_entry = registry.get(ticker, {})

    result: Dict[str, Any] = {
        "ticker": ticker,
        "company_name": reg_entry.get("company_name", ticker),
        "status": reg_entry.get("current_status", "UNKNOWN"),
        "target_price": reg_entry.get("last_intrinsic_value", None),
        "rating": reg_entry.get("published_rating", "N/A"),
        "currency": reg_entry.get("currency", "USD"),
        "spot_price": None,
        "market_cap_b": None,
        "wacc_base": None,
        "wacc_terminal": None,
        "net_debt_b": None,
        "dcf_value": None,
        "sotp_value": None,
        "mc_median": None,
        "mc_win_rate": None,
        "gate_4b": {},
        "raw_json": {}
    }

    if not proj_dir:
        return result

    outputs_path = os.path.join(proj_dir, "models", "valuation_engine_outputs.json")
    if os.path.exists(outputs_path):
        try:
            with open(outputs_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                result["raw_json"] = d
                result["company_name"] = d.get("company_name", result["company_name"])
                
                # Spot price
                result["spot_price"] = d.get("spot_price_usd") or d.get("spot_price_gbp") or d.get("spot_price_pence")
                if "spot_price_pence" in d and result["currency"] == "GBP":
                    result["spot_price"] = d["spot_price_pence"] / 100.0

                # Market Cap in Billions
                mcap = d.get("market_cap_m")
                if mcap:
                    result["market_cap_b"] = round(mcap / 1000.0, 2)

                # WACC
                wacc = d.get("wacc_schedule") or d.get("gate_3_cost_of_capital") or {}
                if wacc:
                    result["wacc_base"] = wacc.get("base_wacc")
                    result["wacc_terminal"] = wacc.get("terminal_wacc")
                elif "wacc_base_pct" in d:
                    result["wacc_base"] = d["wacc_base_pct"] / 100.0
                    result["wacc_terminal"] = d.get("wacc_terminal_pct", 9.0) / 100.0

                # Net Debt / Cash
                if "forensics_gate_1" in d:
                    result["net_debt_b"] = round(d["forensics_gate_1"].get("net_debt_m", 0) / 1000.0, 2)
                elif "gate_1_forensic_normalization" in d:
                    nc = d["gate_1_forensic_normalization"].get("net_cash_cushion_m", 0)
                    result["net_debt_b"] = round(-nc / 1000.0, 2)
                elif "true_net_debt_m" in d:
                    result["net_debt_b"] = round(d["true_net_debt_m"] / 1000.0, 2)
                elif "dcf_schedule" in d and d["dcf_schedule"].get("net_debt_deduction_m"):
                    nd = d["dcf_schedule"].get("net_debt_deduction_m", 0)
                    result["net_debt_b"] = round(nd / 1000.0, 2)

                if (result["net_debt_b"] is None or result["net_debt_b"] == 0.0) and ticker in MASTER_NET_DEBT_B:
                    result["net_debt_b"] = MASTER_NET_DEBT_B[ticker]

                # DCF, SOTP, Monte Carlo
                if "dcf_schedule" in d:
                    dcf_val = (
                        d["dcf_schedule"].get("dcf_intrinsic_value_usd")
                        or d["dcf_schedule"].get("dcf_intrinsic_value_gbp")
                        or d["dcf_schedule"].get("dcf_intrinsic_gbp")
                    )
                    if dcf_val is None and "dcf_intrinsic_pence" in d["dcf_schedule"]:
                        dcf_val = d["dcf_schedule"]["dcf_intrinsic_pence"] / 100.0 if result["currency"] == "GBP" else d["dcf_schedule"]["dcf_intrinsic_pence"]
                    elif dcf_val is None and "dcf_intrinsic_value_pence" in d["dcf_schedule"]:
                        dcf_val = d["dcf_schedule"]["dcf_intrinsic_value_pence"] / 100.0 if result["currency"] == "GBP" else d["dcf_schedule"]["dcf_intrinsic_value_pence"]
                    result["dcf_value"] = dcf_val
                elif "dcf_intrinsic_value_usd" in d:
                    result["dcf_value"] = d["dcf_intrinsic_value_usd"]
                elif "gate_4_valuation" in d:
                    result["dcf_value"] = d["gate_4_valuation"].get("dcf_intrinsic_value_usd")

                if "sotp_divisional" in d:
                    sotp_val = d["sotp_divisional"].get("sotp_intrinsic_usd") or d["sotp_divisional"].get("sotp_intrinsic_gbp")
                    if sotp_val is None and "sotp_intrinsic_pence" in d["sotp_divisional"]:
                        sotp_val = d["sotp_divisional"]["sotp_intrinsic_pence"] / 100.0 if result["currency"] == "GBP" else d["sotp_divisional"]["sotp_intrinsic_pence"]
                    result["sotp_value"] = sotp_val
                elif "sotp_intrinsic_value_usd" in d:
                    result["sotp_value"] = d["sotp_intrinsic_value_usd"]
                elif "gate_4_valuation" in d:
                    result["sotp_value"] = d["gate_4_valuation"].get("sotp_intrinsic_value_usd") or d["gate_4_valuation"].get("sotp_fair_value_usd")

                if "monte_carlo_10k" in d:
                    mc_val = d["monte_carlo_10k"].get("median_usd") or d["monte_carlo_10k"].get("median_gbp")
                    if mc_val is None and "median_pence" in d["monte_carlo_10k"]:
                        mc_val = d["monte_carlo_10k"]["median_pence"] / 100.0 if result["currency"] == "GBP" else d["monte_carlo_10k"]["median_pence"]
                    result["mc_median"] = mc_val
                    result["mc_win_rate"] = d["monte_carlo_10k"].get("win_rate_percent")
                elif "monte_carlo_median_usd" in d:
                    result["mc_median"] = d["monte_carlo_median_usd"]
                    result["mc_win_rate"] = d.get("monte_carlo_win_rate_pct")
                elif "gate_4_valuation" in d:
                    g4 = d["gate_4_valuation"]
                    if "monte_carlo_10k" in g4:
                        result["mc_median"] = g4["monte_carlo_10k"].get("median_usd")
                        result["mc_win_rate"] = g4["monte_carlo_10k"].get("win_rate_pct")

                # Triangulated target price override if present
                if "final_triangulation" in d:
                    result["target_price"] = d["final_triangulation"].get("target_price_usd") or d["final_triangulation"].get("target_price_gbp") or result["target_price"]
                elif "final_target_price_usd" in d:
                    result["target_price"] = d["final_target_price_usd"]
                elif "gate_4_valuation" in d:
                    result["target_price"] = d["gate_4_valuation"].get("final_target_price_usd") or d["gate_4_valuation"].get("blended_target_price_usd") or result["target_price"]
                elif not result["target_price"]:
                    result["target_price"] = reg_entry.get("last_intrinsic_value")

                # Gate 4B
                g4b = d.get("ai_capex_audit") or d.get("gate_4b_ai_capex_audit") or d.get("gate_4b_ai_capex_roi") or {}
                result["gate_4b"] = g4b

        except Exception:
            pass

    # Vault fallback / enrichment for Gate 4B
    try:
        from ERVIS.vault.engine import get_gate4b_record
        v_g4b = get_gate4b_record(ticker)
        if v_g4b:
            result["vault_gate4b"] = v_g4b
    except Exception:
        pass

    return result

def get_top10_matrix() -> List[Dict[str, Any]]:
    matrix = []
    for ticker in TOP10_TICKERS:
        data = load_company_data(ticker)
        spot = data.get("spot_price") or 0.0
        target = data.get("target_price") or 0.0
        gap = round(((target - spot) / spot) * 100.0, 1) if spot > 0 else 0.0

        matrix.append({
            "ticker": ticker,
            "name": data.get("company_name", ticker),
            "spot": spot,
            "target": target,
            "gap_pct": gap,
            "rating": data.get("rating", "N/A"),
            "wacc": round((data.get("wacc_base") or 0.09) * 100.0, 2),
            "mcap_b": data.get("market_cap_b", 0.0),
            "net_debt_b": data.get("net_debt_b", 0.0)
        })
    return matrix

def get_portfolio_data() -> Dict[str, Any]:
    return {
        "cash_balance": 200.00,
        "currency": "USD",
        "broker": "Webull Singapore (Cash Account)",
        "allocations": [
            {
                "ticker": "EWU",
                "name": "iShares MSCI United Kingdom ETF",
                "target_alloc_pct": 40.0,
                "target_amount_usd": 80.00,
                "order_type": "Market Order (Fractional)",
                "status": "PENDING_APPROVAL",
                "thesis": "UK value resurgence, 11.5x P/E, 3.8% dividend yield, zero stamp duty."
            },
            {
                "ticker": "RYCEY",
                "name": "Rolls-Royce Holdings plc (ADR)",
                "target_alloc_pct": 25.0,
                "target_amount_usd": 50.00,
                "order_type": "GTC Limit Bid @ $16.80",
                "status": "LIMIT_BID_ACTIVE",
                "thesis": "Testing 200-day SMA ($16.80 / 1,285p). LTSA float engine, 35% 2-yr upside."
            },
            {
                "ticker": "RSP",
                "name": "Invesco S&P 500 Equal Weight ETF",
                "target_alloc_pct": 20.0,
                "target_amount_usd": 40.00,
                "order_type": "Market Order (Fractional)",
                "status": "PENDING_APPROVAL",
                "thesis": "Equal-weight shield against Top 10 AI concentration cliff."
            },
            {
                "ticker": "MONEYBULL",
                "name": "USD Cash Yield Auto-Sweep",
                "target_alloc_pct": 15.0,
                "target_amount_usd": 30.00,
                "order_type": "Auto-Sweep (4.5% - 4.8% APY)",
                "status": "ACCUMULATING",
                "thesis": "Dry powder float for opportunistic pullbacks."
            }
        ],
        "dca_cadence": {
            "mode": "Bi-Weekly",
            "injection_per_tranche": 100.00,
            "schedule": "Mid-Month (15th) + End-Month (30th)",
            "duration_months": 3,
            "total_capital": 800.00
        }
    }

def get_fa_financial_trends(ticker: str) -> Dict[str, Any]:
    """Retrieves multi-year financial statement time-series and health scores from the vault."""
    from ERVIS.vault.engine import get_connection
    ticker = ticker.upper()
    
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT fiscal_year, line_item, value_m 
            FROM financial_statements 
            WHERE ticker = ?
            ORDER BY fiscal_year ASC
        """, (ticker,))
        rows = cur.fetchall()

    raw_items: Dict[str, Dict[str, float]] = {}
    years_set = set()
    for yr, item, val in rows:
        years_set.add(yr)
        raw_items.setdefault(item, {})[yr] = val

    # Extract primary financial series
    rev_series = raw_items.get("Total Revenue") or raw_items.get("Operating Revenue") or {}
    op_inc_series = raw_items.get("Operating Income") or raw_items.get("Operating Profit") or {}
    fcf_series = raw_items.get("Free Cash Flow") or {}
    capex_series = raw_items.get("Capital Expenditure") or {}
    cash_series = raw_items.get("Cash And Cash Equivalents") or raw_items.get("Cash Financial") or {}

    valid_years = [yr for yr in sorted(list(years_set)) if rev_series.get(yr) is not None or op_inc_series.get(yr) is not None]
    if valid_years:
        years = valid_years[-4:]
    else:
        years = ["2023", "2024", "2025", "2026"]

    history_table = []
    prev_rev = None

    for yr in years:
        rev = rev_series.get(yr)
        op_inc = op_inc_series.get(yr)
        fcf = fcf_series.get(yr)
        capex = abs(capex_series.get(yr, 0.0)) if capex_series.get(yr) else None
        cash = cash_series.get(yr)

        yoy = f"{((rev - prev_rev) / prev_rev) * 100.0:+.1f}%" if rev and prev_rev and prev_rev > 0 else "N/A"
        op_margin = f"{(op_inc / rev) * 100.0:.1f}%" if rev and op_inc else "N/A"
        fcf_margin = f"{(fcf / rev) * 100.0:.1f}%" if rev and fcf else "N/A"

        history_table.append({
            "year": yr,
            "revenue": rev,
            "yoy_growth": yoy,
            "operating_income": op_inc,
            "operating_margin": op_margin,
            "capex": capex,
            "fcf": fcf,
            "fcf_margin": fcf_margin,
            "cash": cash
        })
        if rev:
            prev_rev = rev

    # Load diagnostics from company directory if available
    proj_dir = find_project_dir(ticker)
    diagnostics = {}
    if proj_dir:
        diag_path = os.path.join(proj_dir, "regressions", "diagnostics_audit.json")
        if os.path.exists(diag_path):
            try:
                with open(diag_path, "r", encoding="utf-8") as f:
                    diagnostics = json.load(f)
            except Exception:
                pass

    return {
        "ticker": ticker,
        "years": years,
        "history": history_table,
        "diagnostics": diagnostics
    }

def get_company_gate4b(ticker: str) -> Optional[Dict[str, Any]]:
    """Retrieves the Gate 4B AI CapEx Payback and Obsolescence record from the vault."""
    try:
        from ERVIS.vault.engine import get_gate4b_record
        return get_gate4b_record(ticker.upper())
    except Exception:
        return None

def get_valuation_history(ticker: str) -> List[Dict[str, Any]]:
    """Retrieves point-in-time historical valuation snapshots for a security."""
    try:
        from ERVIS.vault.engine import get_valuation_snapshots
        return get_valuation_snapshots(ticker.upper())
    except Exception:
        return []

def get_company_beta(ticker: str) -> Optional[Dict[str, Any]]:
    """Retrieves the Historical Beta Regression record from the vault."""
    try:
        from ERVIS.vault.engine import get_beta_record
        return get_beta_record(ticker.upper())
    except Exception:
        return None
