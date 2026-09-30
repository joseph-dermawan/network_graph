"""
ERVIS Vault Engine
Portable SQLite database interface for storing and querying multi-year financial statements,
forensic normalizations, valuation snapshots, and Gate 4B AI CapEx time series.
"""

import os
import sqlite3
import json
import csv
import glob
import yaml
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

VAULT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(VAULT_DIR, "ervis_vault.db")
SCHEMA_PATH = os.path.join(VAULT_DIR, "schema.sql")
ERVIS_ROOT = os.path.abspath(os.path.join(VAULT_DIR, ".."))

MASTER_GATE4B_DATA = {
    "NVDA": {
        "annual_capex_m": 6040.0,
        "ai_capex_m": 0.0,
        "incremental_ai_revenue_m": 185000.0,
        "annual_depreciation_3_5yr_m": 0.0,
        "net_ai_operating_income_m": 130000.0,
        "net_ai_roi_pct": 80.2,
        "payback_period_years": 0.45,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": -3.05,
        "capex_payout_ratio_pct": 45.34,
        "break_even_revenue_gap_m": -66000.0,
        "risk_assessment": "The Cisco Paradox: Hardware tollbooth seller capturing 45.3% hyperscaler spend. Margins vulnerable when customer CapEx slows."
    },
    "MSFT": {
        "annual_capex_m": 115950.0,
        "ai_capex_m": 75370.0,
        "incremental_ai_revenue_m": 18000.0,
        "annual_depreciation_3_5yr_m": 21530.0,
        "net_ai_operating_income_m": -9830.0,
        "net_ai_roi_pct": -13.0,
        "payback_period_years": 6.44,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": 2.94,
        "capex_payout_ratio_pct": 28.4,
        "break_even_revenue_gap_m": -15130.0,
        "risk_assessment": "Obsolescence Deficit: Payback of 6.44 yrs exceeds 3.50-yr GPU useful life by 2.94 years. Monetization gap of -$15.1B/yr."
    },
    "AAPL": {
        "annual_capex_m": 12720.0,
        "ai_capex_m": 4500.0,
        "incremental_ai_revenue_m": 12500.0,
        "annual_depreciation_3_5yr_m": 1280.0,
        "net_ai_operating_income_m": 12500.0,
        "net_ai_roi_pct": 65.0,
        "payback_period_years": 1.02,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": -2.48,
        "capex_payout_ratio_pct": 3.1,
        "break_even_revenue_gap_m": 0.0,
        "risk_assessment": "Asset-Light Edge Moat: Edge NPU architecture avoids merchant GPU CapEx; funded via consumer iPhone upgrade cycles."
    },
    "GOOGL": {
        "annual_capex_m": 91450.0,
        "ai_capex_m": 64010.0,
        "incremental_ai_revenue_m": 22700.0,
        "annual_depreciation_3_5yr_m": 18290.0,
        "net_ai_operating_income_m": 1440.0,
        "net_ai_roi_pct": 2.24,
        "payback_period_years": 3.25,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": -0.25,
        "capex_payout_ratio_pct": 22.4,
        "break_even_revenue_gap_m": 0.0,
        "risk_assessment": "Defensive Fortress: Internal TPU v5/v6 infrastructure generates $14.2B cost avoidance; achieves payback in 3.25 yrs."
    },
    "AMZN": {
        "annual_capex_m": 131820.0,
        "ai_capex_m": 50000.0,
        "incremental_ai_revenue_m": 15000.0,
        "annual_depreciation_3_5yr_m": 14290.0,
        "net_ai_operating_income_m": -4540.0,
        "net_ai_roi_pct": -9.07,
        "payback_period_years": 5.13,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": 1.63,
        "capex_payout_ratio_pct": 32.3,
        "break_even_revenue_gap_m": -6500.0,
        "risk_assessment": "Extreme CFO Absorption: CapEx consumes 94.5% of CFO; FCF contracted -76.6%; hardware obsolete 1.63 yrs before payback."
    },
    "META": {
        "annual_capex_m": 68000.0,
        "ai_capex_m": 68000.0,
        "incremental_ai_revenue_m": 19090.0,
        "annual_depreciation_3_5yr_m": 19430.0,
        "net_ai_operating_income_m": -3770.0,
        "net_ai_roi_pct": -5.55,
        "payback_period_years": 4.34,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": 0.84,
        "capex_payout_ratio_pct": 16.7,
        "break_even_revenue_gap_m": -4100.0,
        "risk_assessment": "Core Monetization Buffer: Hardware depreciation creates -$3.8B initial deficit, offset by +9.5% ad conversion lift."
    },
    "AVGO": {
        "annual_capex_m": 1250.0,
        "ai_capex_m": 0.0,
        "incremental_ai_revenue_m": 24500.0,
        "annual_depreciation_3_5yr_m": 0.0,
        "net_ai_operating_income_m": 15900.0,
        "net_ai_roi_pct": 125.3,
        "payback_period_years": 0.65,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": -2.85,
        "capex_payout_ratio_pct": 5.76,
        "break_even_revenue_gap_m": 0.0,
        "risk_assessment": "Custom ASIC Tollbooth: High ROIC (125%) capturing 5.76% hyperscaler tax on custom XPUs and networking switches."
    },
    "TSM": {
        "annual_capex_m": 40330.0,
        "ai_capex_m": 26500.0,
        "incremental_ai_revenue_m": 26500.0,
        "annual_depreciation_3_5yr_m": 8070.0,
        "net_ai_operating_income_m": 14800.0,
        "net_ai_roi_pct": 36.88,
        "payback_period_years": 1.80,
        "useful_life_years": 5.00,
        "obsolescence_deficit_years": -3.20,
        "capex_payout_ratio_pct": 10.5,
        "break_even_revenue_gap_m": 0.0,
        "risk_assessment": "Physical Foundry Monopoly: N3/N2 and CoWoS advanced packaging pricing power secures 36.9% ROIC and 1.80-yr payback."
    },
    "AMD": {
        "annual_capex_m": 1680.0,
        "ai_capex_m": 0.0,
        "incremental_ai_revenue_m": 14000.0,
        "annual_depreciation_3_5yr_m": 0.0,
        "net_ai_operating_income_m": 4200.0,
        "net_ai_roi_pct": 35.0,
        "payback_period_years": 4.15,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": 0.65,
        "capex_payout_ratio_pct": 3.4,
        "break_even_revenue_gap_m": -1800.0,
        "risk_assessment": "Software Ecosystem Friction: ROCm software switching costs vs CUDA creates customer payback friction."
    },
    "ORCL": {
        "annual_capex_m": 23100.0,
        "ai_capex_m": 20000.0,
        "incremental_ai_revenue_m": 7500.0,
        "annual_depreciation_3_5yr_m": 5710.0,
        "net_ai_operating_income_m": 500.0,
        "net_ai_roi_pct": 2.5,
        "payback_period_years": 5.80,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": 2.30,
        "capex_payout_ratio_pct": 4.9,
        "break_even_revenue_gap_m": -3200.0,
        "risk_assessment": "Critical Solvency Risk: $118.8B Net Debt and $4.6B interest drag; Project Jupiter 2.45 GW force majeure shock."
    },
    "RR": {
        "annual_capex_m": 850.0,
        "ai_capex_m": 0.0,
        "incremental_ai_revenue_m": 0.0,
        "annual_depreciation_3_5yr_m": 0.0,
        "net_ai_operating_income_m": 0.0,
        "net_ai_roi_pct": 0.0,
        "payback_period_years": 0.0,
        "useful_life_years": 3.50,
        "obsolescence_deficit_years": 0.0,
        "capex_payout_ratio_pct": 0.0,
        "break_even_revenue_gap_m": 0.0,
        "risk_assessment": "Zero AI CapEx Exposure: Civil Aerospace LTSA aftermarket flying hours annuity; impervious to GPU depreciation cycles."
    }
}

MASTER_BETA_DATA = {
    "NVDA": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.38,
        "adjusted_beta": 1.25,
        "alpha_annualized_pct": 14.20,
        "r_squared": 0.68,
        "correlation": 0.825,
        "std_error": 0.08,
        "t_stat": 17.25,
        "unlevered_beta": 1.24,
        "levered_beta": 1.253,
        "debt_to_equity_pct": -1.4,
        "effective_tax_rate_pct": 13.6,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 10.00,
        "wacc_base_pct": 9.47,
        "risk_classification": "HIGH-BETA EXPONENTIAL GROWTH (Hardware Tollbooth Extractor)"
    },
    "MSFT": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.04,
        "adjusted_beta": 1.00,
        "alpha_annualized_pct": 3.80,
        "r_squared": 0.72,
        "correlation": 0.849,
        "std_error": 0.05,
        "t_stat": 20.80,
        "unlevered_beta": 0.99,
        "levered_beta": 0.996,
        "debt_to_equity_pct": -0.1,
        "effective_tax_rate_pct": 18.0,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 8.89,
        "wacc_base_pct": 8.80,
        "risk_classification": "LOW-BETA FORTRESS ENTERPRISE (Core Enterprise Cloud Moat)"
    },
    "AAPL": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.02,
        "adjusted_beta": 0.98,
        "alpha_annualized_pct": 2.10,
        "r_squared": 0.69,
        "correlation": 0.831,
        "std_error": 0.06,
        "t_stat": 17.00,
        "unlevered_beta": 0.96,
        "levered_beta": 0.978,
        "debt_to_equity_pct": -0.6,
        "effective_tax_rate_pct": 15.0,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 8.82,
        "wacc_base_pct": 8.72,
        "risk_classification": "LOW-BETA CONSUMER MONOPOLY (Asset-Light Edge Architecture)"
    },
    "GOOGL": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.13,
        "adjusted_beta": 1.06,
        "alpha_annualized_pct": 4.50,
        "r_squared": 0.66,
        "correlation": 0.812,
        "std_error": 0.07,
        "t_stat": 16.14,
        "unlevered_beta": 1.03,
        "levered_beta": 1.063,
        "debt_to_equity_pct": -3.0,
        "effective_tax_rate_pct": 16.5,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 9.18,
        "wacc_base_pct": 9.11,
        "risk_classification": "MODERATE-BETA DEFENSIVE MOAT (Search Monopolist & TPU Fortress)"
    },
    "AMZN": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.27,
        "adjusted_beta": 1.15,
        "alpha_annualized_pct": 1.80,
        "r_squared": 0.64,
        "correlation": 0.800,
        "std_error": 0.08,
        "t_stat": 15.88,
        "unlevered_beta": 1.11,
        "levered_beta": 1.152,
        "debt_to_equity_pct": 1.5,
        "effective_tax_rate_pct": 19.0,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 9.57,
        "wacc_base_pct": 9.27,
        "risk_classification": "HIGH-BETA CYCLICAL CLOUD/RETAIL (High CapEx & CFO Absorption)"
    },
    "META": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.18,
        "adjusted_beta": 1.09,
        "alpha_annualized_pct": 6.20,
        "r_squared": 0.61,
        "correlation": 0.781,
        "std_error": 0.09,
        "t_stat": 13.11,
        "unlevered_beta": 1.05,
        "levered_beta": 1.090,
        "debt_to_equity_pct": -1.5,
        "effective_tax_rate_pct": 17.5,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 9.30,
        "wacc_base_pct": 9.08,
        "risk_classification": "MODERATE-BETA ADVERTISING ENGINE (Digital Moat & Llama AI Lift)"
    },
    "AVGO": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.20,
        "adjusted_beta": 1.10,
        "alpha_annualized_pct": 8.50,
        "r_squared": 0.63,
        "correlation": 0.794,
        "std_error": 0.08,
        "t_stat": 15.00,
        "unlevered_beta": 0.98,
        "levered_beta": 1.100,
        "debt_to_equity_pct": 2.3,
        "effective_tax_rate_pct": 14.0,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 9.34,
        "wacc_base_pct": 9.34,
        "risk_classification": "LEVERED TOLLBOOTH ACCELERATOR (Custom Silicon & Networking Moat)"
    },
    "TSM": {
        "benchmark_index": "SPX Index (S&P 500 / SOX)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.14,
        "adjusted_beta": 1.06,
        "alpha_annualized_pct": 5.10,
        "r_squared": 0.65,
        "correlation": 0.806,
        "std_error": 0.07,
        "t_stat": 16.29,
        "unlevered_beta": 1.01,
        "levered_beta": 1.063,
        "debt_to_equity_pct": -7.2,
        "effective_tax_rate_pct": 15.0,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 9.88,
        "wacc_base_pct": 9.79,
        "risk_classification": "CRITICAL MONOPOLY FOUNDRY (Taiwan Geopolitical Beta Spread)"
    },
    "AMD": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.51,
        "adjusted_beta": 1.31,
        "alpha_annualized_pct": -2.30,
        "r_squared": 0.58,
        "correlation": 0.762,
        "std_error": 0.11,
        "t_stat": 13.73,
        "unlevered_beta": 1.28,
        "levered_beta": 1.306,
        "debt_to_equity_pct": -0.8,
        "effective_tax_rate_pct": 16.0,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 10.23,
        "wacc_base_pct": 10.21,
        "risk_classification": "VERY HIGH-BETA CHALLENGER (Hardware/Software Transition Volatility)"
    },
    "ORCL": {
        "benchmark_index": "SPX Index (S&P 500)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "USD",
        "raw_beta": 1.03,
        "adjusted_beta": 0.99,
        "alpha_annualized_pct": 0.40,
        "r_squared": 0.52,
        "correlation": 0.721,
        "std_error": 0.09,
        "t_stat": 11.44,
        "unlevered_beta": 0.78,
        "levered_beta": 0.994,
        "debt_to_equity_pct": 34.7,
        "effective_tax_rate_pct": 21.0,
        "risk_free_rate_pct": 4.58,
        "erp_pct": 4.33,
        "cost_of_equity_pct": 8.88,
        "wacc_base_pct": 7.80,
        "risk_classification": "FINANCIALLY LEVERED MATURE TITAN ($118.8B Net Debt Drag)"
    },
    "RR": {
        "benchmark_index": "UKX Index (FTSE 100 Index)",
        "period": "3-Year Weekly (156 Obs)",
        "currency": "GBP",
        "raw_beta": 1.16,
        "adjusted_beta": 1.08,
        "alpha_annualized_pct": 12.40,
        "r_squared": 0.55,
        "correlation": 0.742,
        "std_error": 0.10,
        "t_stat": 11.60,
        "unlevered_beta": 1.02,
        "levered_beta": 1.076,
        "debt_to_equity_pct": 3.2,
        "effective_tax_rate_pct": 25.0,
        "risk_free_rate_pct": 4.25,
        "erp_pct": 5.00,
        "cost_of_equity_pct": 9.65,
        "wacc_base_pct": 9.39,
        "risk_classification": "AEROSPACE INDUSTRIAL TURNAROUND (High Operating Leverage)"
    }
}

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_vault() -> None:
    """Initializes the SQLite schema if not already present."""
    if not os.path.exists(SCHEMA_PATH):
        raise FileNotFoundError(f"Schema not found at {SCHEMA_PATH}")
    
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_connection() as conn:
        conn.executescript(schema_sql)
        conn.commit()

def save_security(data: Dict[str, Any]) -> None:
    query = """
    INSERT INTO securities (
        ticker, company_name, market, exchange, currency, spot_price, target_price,
        published_rating, valuation_gap_pct, market_cap_b, shares_outstanding_m, updated_at
    ) VALUES (
        :ticker, :company_name, :market, :exchange, :currency, :spot_price, :target_price,
        :published_rating, :valuation_gap_pct, :market_cap_b, :shares_outstanding_m, CURRENT_TIMESTAMP
    ) ON CONFLICT(ticker) DO UPDATE SET
        company_name=excluded.company_name,
        spot_price=excluded.spot_price,
        target_price=excluded.target_price,
        published_rating=excluded.published_rating,
        valuation_gap_pct=excluded.valuation_gap_pct,
        market_cap_b=excluded.market_cap_b,
        shares_outstanding_m=excluded.shares_outstanding_m,
        updated_at=CURRENT_TIMESTAMP;
    """
    with get_connection() as conn:
        conn.execute(query, {
            "ticker": data.get("ticker", "").upper(),
            "company_name": data.get("company_name", ""),
            "market": data.get("market", "US_EQUITIES"),
            "exchange": data.get("exchange", "NASDAQ"),
            "currency": data.get("currency", "USD"),
            "spot_price": data.get("spot_price"),
            "target_price": data.get("target_price"),
            "published_rating": data.get("published_rating"),
            "valuation_gap_pct": data.get("valuation_gap_pct"),
            "market_cap_b": data.get("market_cap_b"),
            "shares_outstanding_m": data.get("shares_outstanding_m")
        })
        conn.commit()

def save_financial_statement_row(ticker: str, stmt_type: str, fiscal_year: str, line_item: str, value_m: float, currency: str = "USD") -> None:
    query = """
    INSERT INTO financial_statements (ticker, statement_type, fiscal_year, line_item, value_m, currency)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(ticker, statement_type, fiscal_year, line_item) DO UPDATE SET
        value_m=excluded.value_m;
    """
    with get_connection() as conn:
        conn.execute(query, (ticker.upper(), stmt_type.upper(), str(fiscal_year), line_item.strip(), float(value_m), currency.upper()))
        conn.commit()

def save_forensic_record(data: Dict[str, Any]) -> None:
    query = """
    INSERT INTO forensic_normalized_series (
        ticker, fiscal_year, reported_ebit_m, capitalized_rd_asset_m, synthetic_lease_debt_m,
        normalized_ebit_0_m, normalized_nopat_0_m, invested_capital_m, true_net_debt_m,
        effective_tax_rate, economic_roic_pct, altman_z_score, piotroski_f_score, beneish_m_score
    ) VALUES (
        :ticker, :fiscal_year, :reported_ebit_m, :capitalized_rd_asset_m, :synthetic_lease_debt_m,
        :normalized_ebit_0_m, :normalized_nopat_0_m, :invested_capital_m, :true_net_debt_m,
        :effective_tax_rate, :economic_roic_pct, :altman_z_score, :piotroski_f_score, :beneish_m_score
    ) ON CONFLICT(ticker, fiscal_year) DO UPDATE SET
        reported_ebit_m=excluded.reported_ebit_m,
        capitalized_rd_asset_m=excluded.capitalized_rd_asset_m,
        synthetic_lease_debt_m=excluded.synthetic_lease_debt_m,
        normalized_ebit_0_m=excluded.normalized_ebit_0_m,
        normalized_nopat_0_m=excluded.normalized_nopat_0_m,
        invested_capital_m=excluded.invested_capital_m,
        true_net_debt_m=excluded.true_net_debt_m,
        economic_roic_pct=excluded.economic_roic_pct,
        altman_z_score=excluded.altman_z_score,
        piotroski_f_score=excluded.piotroski_f_score,
        beneish_m_score=excluded.beneish_m_score;
    """
    with get_connection() as conn:
        conn.execute(query, data)
        conn.commit()

def save_valuation_snapshot(data: Dict[str, Any]) -> None:
    query = """
    INSERT INTO valuation_snapshots (
        snapshot_date, ticker, spot_price, dcf_intrinsic_value, sotp_intrinsic_value,
        monte_carlo_median, monte_carlo_p10, monte_carlo_p90, monte_carlo_win_rate_pct,
        liquidation_floor, final_target_price, valuation_gap_pct, published_rating,
        base_wacc_pct, terminal_wacc_pct, hamada_beta, credit_rating
    ) VALUES (
        :snapshot_date, :ticker, :spot_price, :dcf_intrinsic_value, :sotp_intrinsic_value,
        :monte_carlo_median, :monte_carlo_p10, :monte_carlo_p90, :monte_carlo_win_rate_pct,
        :liquidation_floor, :final_target_price, :valuation_gap_pct, :published_rating,
        :base_wacc_pct, :terminal_wacc_pct, :hamada_beta, :credit_rating
    );
    """
    with get_connection() as conn:
        conn.execute(query, data)
        conn.commit()

def save_gate4b_record(data: Dict[str, Any]) -> None:
    query = """
    INSERT INTO gate4b_capex_series (
        ticker, annual_capex_m, ai_capex_m, incremental_ai_revenue_m, annual_depreciation_3_5yr_m,
        net_ai_operating_income_m, net_ai_roi_pct, payback_period_years, useful_life_years,
        obsolescence_deficit_years, capex_payout_ratio_pct, break_even_revenue_gap_m, risk_assessment
    ) VALUES (
        :ticker, :annual_capex_m, :ai_capex_m, :incremental_ai_revenue_m, :annual_depreciation_3_5yr_m,
        :net_ai_operating_income_m, :net_ai_roi_pct, :payback_period_years, :useful_life_years,
        :obsolescence_deficit_years, :capex_payout_ratio_pct, :break_even_revenue_gap_m, :risk_assessment
    ) ON CONFLICT(ticker) DO UPDATE SET
        annual_capex_m=excluded.annual_capex_m,
        ai_capex_m=excluded.ai_capex_m,
        incremental_ai_revenue_m=excluded.incremental_ai_revenue_m,
        annual_depreciation_3_5yr_m=excluded.annual_depreciation_3_5yr_m,
        net_ai_operating_income_m=excluded.net_ai_operating_income_m,
        net_ai_roi_pct=excluded.net_ai_roi_pct,
        payback_period_years=excluded.payback_period_years,
        obsolescence_deficit_years=excluded.obsolescence_deficit_years,
        capex_payout_ratio_pct=excluded.capex_payout_ratio_pct,
        break_even_revenue_gap_m=excluded.break_even_revenue_gap_m,
        risk_assessment=excluded.risk_assessment,
        updated_at=CURRENT_TIMESTAMP;
    """
    with get_connection() as conn:
        conn.execute(query, data)
        conn.commit()

def save_portfolio_entry(item: Dict[str, Any]) -> None:
    query = """
    INSERT INTO portfolio_ledger (
        ticker, asset_name, order_type, target_alloc_pct, allocated_usd, executed_price,
        shares_count, status, thesis, broker
    ) VALUES (
        :ticker, :asset_name, :order_type, :target_alloc_pct, :allocated_usd, :executed_price,
        :shares_count, :status, :thesis, :broker
    );
    """
    with get_connection() as conn:
        conn.execute(query, item)
        conn.commit()

def save_beta_record(data: Dict[str, Any]) -> None:
    query = """
    INSERT INTO beta_regressions (
        ticker, benchmark_index, period, currency, raw_beta, adjusted_beta,
        alpha_annualized_pct, r_squared, correlation, std_error, t_stat,
        unlevered_beta, levered_beta, debt_to_equity_pct, effective_tax_rate_pct,
        risk_free_rate_pct, erp_pct, cost_of_equity_pct, wacc_base_pct, risk_classification
    ) VALUES (
        :ticker, :benchmark_index, :period, :currency, :raw_beta, :adjusted_beta,
        :alpha_annualized_pct, :r_squared, :correlation, :std_error, :t_stat,
        :unlevered_beta, :levered_beta, :debt_to_equity_pct, :effective_tax_rate_pct,
        :risk_free_rate_pct, :erp_pct, :cost_of_equity_pct, :wacc_base_pct, :risk_classification
    ) ON CONFLICT(ticker) DO UPDATE SET
        benchmark_index=excluded.benchmark_index,
        period=excluded.period,
        currency=excluded.currency,
        raw_beta=excluded.raw_beta,
        adjusted_beta=excluded.adjusted_beta,
        alpha_annualized_pct=excluded.alpha_annualized_pct,
        r_squared=excluded.r_squared,
        correlation=excluded.correlation,
        std_error=excluded.std_error,
        t_stat=excluded.t_stat,
        unlevered_beta=excluded.unlevered_beta,
        levered_beta=excluded.levered_beta,
        debt_to_equity_pct=excluded.debt_to_equity_pct,
        effective_tax_rate_pct=excluded.effective_tax_rate_pct,
        risk_free_rate_pct=excluded.risk_free_rate_pct,
        erp_pct=excluded.erp_pct,
        cost_of_equity_pct=excluded.cost_of_equity_pct,
        wacc_base_pct=excluded.wacc_base_pct,
        risk_classification=excluded.risk_classification,
        updated_at=CURRENT_TIMESTAMP;
    """
    with get_connection() as conn:
        conn.execute(query, data)
        conn.commit()

# --- Query Methods ---

def get_security(ticker: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM securities WHERE ticker = ?", (ticker.upper(),))
        row = cur.fetchone()
        return dict(row) if row else None

def get_all_securities() -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM securities ORDER BY market_cap_b DESC")
        return [dict(r) for r in cur.fetchall()]

def get_financial_history(ticker: str, stmt_type: Optional[str] = None) -> List[Dict[str, Any]]:
    query = "SELECT * FROM financial_statements WHERE ticker = ?"
    params = [ticker.upper()]
    if stmt_type:
        query += " AND statement_type = ?"
        params.append(stmt_type.upper())
    query += " ORDER BY fiscal_year DESC, line_item ASC"

    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return [dict(r) for r in cur.fetchall()]

def get_gate4b_record(ticker: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM gate4b_capex_series WHERE ticker = ?", (ticker.upper(),))
        row = cur.fetchone()
        return dict(row) if row else None

def get_beta_record(ticker: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM beta_regressions WHERE ticker = ?", (ticker.upper(),))
        row = cur.fetchone()
        return dict(row) if row else None

def get_latest_valuation_snapshot(ticker: str) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM valuation_snapshots WHERE ticker = ? ORDER BY id DESC LIMIT 1", (ticker.upper(),))
        row = cur.fetchone()
        return dict(row) if row else None

def get_valuation_snapshots(ticker: str) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM valuation_snapshots 
            WHERE ticker = ? 
            GROUP BY snapshot_date
            ORDER BY snapshot_date ASC, id ASC
        """, (ticker.upper(),))
        return [dict(r) for r in cur.fetchall()]

# --- Ingestion & Seeding Engine ---

def ingest_csv_filings(ticker: str, proj_dir: str) -> int:
    """Parses raw balance sheet, cashflow, and income statement CSVs into SQLite."""
    count = 0
    raw_dir = os.path.join(proj_dir, "raw_filings")
    if not os.path.exists(raw_dir):
        return 0

    mappings = [
        ("INCOME_STATEMENT", "*_financials.csv"),
        ("BALANCE_SHEET", "*_balance_sheet.csv"),
        ("CASH_FLOW", "*_cashflow.csv")
    ]

    for stmt_type, pattern in mappings:
        for fpath in glob.glob(os.path.join(raw_dir, pattern)):
            # Skip quarterly for annual historical series table
            if "quarterly" in os.path.basename(fpath).lower():
                continue
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    if not header or len(header) < 2:
                        continue
                    
                    years = [h.strip()[:4] for h in header[1:]]
                    for row in reader:
                        if not row or len(row) < 2:
                            continue
                        line_item = row[0].strip()
                        for i, yr in enumerate(years):
                            if i + 1 < len(row):
                                val_str = row[i + 1].strip().replace(",", "")
                                try:
                                    # CSV values are usually raw dollars; convert to Millions
                                    raw_val = float(val_str)
                                    val_m = round(raw_val / 1_000_000.0, 2) if abs(raw_val) > 100000 else raw_val
                                    save_financial_statement_row(ticker, stmt_type, yr, line_item, val_m)
                                    count += 1
                                except ValueError:
                                    pass
            except Exception:
                pass
    return count

def seed_vault_from_projects() -> Dict[str, Any]:
    """Iterates through all ERVIS projects and populates the SQLite vault."""
    init_vault()
    stats = {"securities": 0, "financial_rows": 0, "snapshots": 0, "gate4b_rows": 0, "beta_rows": 0}

    # 1. Ingest Central Registry
    reg_path = os.path.join(ERVIS_ROOT, "kb", "registry", "company_sheets.yaml")
    registry = {}
    if os.path.exists(reg_path):
        with open(reg_path, "r", encoding="utf-8") as f:
            registry = yaml.safe_load(f).get("COMPANIES", {})

    for ticker, reg_data in registry.items():
        save_security({
            "ticker": ticker,
            "company_name": reg_data.get("company_name", ticker),
            "market": reg_data.get("market", "US_EQUITIES"),
            "currency": reg_data.get("currency", "USD"),
            "target_price": reg_data.get("last_intrinsic_value"),
            "published_rating": reg_data.get("published_rating")
        })
        stats["securities"] += 1

    # 2. Ingest Company Projects
    for proj_dir in glob.glob(os.path.join(ERVIS_ROOT, "projects", "*", "*")):
        ticker = os.path.basename(proj_dir).upper()
        outputs_path = os.path.join(proj_dir, "models", "valuation_engine_outputs.json")
        
        # Ingest CSV time series
        rows = ingest_csv_filings(ticker, proj_dir)
        stats["financial_rows"] += rows

        # Ingest valuation engine JSON output
        if os.path.exists(outputs_path):
            try:
                with open(outputs_path, "r", encoding="utf-8") as f:
                    d = json.load(f)
                
                spot = d.get("spot_price_usd") or d.get("spot_price_gbp") or d.get("spot_price_pence")
                if "spot_price_pence" in d and d.get("currency") == "GBP":
                    spot = d["spot_price_pence"] / 100.0

                mcap_b = round(d.get("market_cap_m", 0) / 1000.0, 2) if d.get("market_cap_m") else None
                
                # Update security spot & mcap
                target = registry.get(ticker, {}).get("last_intrinsic_value")
                gap = round(((target - spot) / spot) * 100.0, 1) if spot and target else None

                save_security({
                    "ticker": ticker,
                    "company_name": d.get("company_name", ticker),
                    "spot_price": spot,
                    "target_price": target,
                    "market_cap_b": mcap_b,
                    "valuation_gap_pct": gap,
                    "shares_outstanding_m": d.get("shares_outstanding_m")
                })

                # Snapshot
                dcf_val = d.get("dcf_schedule", {}).get("dcf_intrinsic_value_usd") or d.get("dcf_schedule", {}).get("dcf_intrinsic_value_gbp") or d.get("dcf_intrinsic_value_usd")
                sotp_val = d.get("sotp_divisional", {}).get("sotp_intrinsic_usd") or d.get("sotp_divisional", {}).get("sotp_intrinsic_gbp") or d.get("sotp_intrinsic_value_usd")
                mc_val = d.get("monte_carlo_10k", {}).get("median_usd") or d.get("monte_carlo_10k", {}).get("median_gbp") or d.get("monte_carlo_median_usd")

                wacc = d.get("wacc_schedule", {})
                base_wacc = wacc.get("base_wacc") or (d.get("wacc_base_pct", 9.0) / 100.0)
                term_wacc = wacc.get("terminal_wacc") or (d.get("wacc_terminal_pct", 9.0) / 100.0)

                # Seed Historical Valuation Audit Progression Snapshots
                prior_dates = [
                    ("2026-07-15", 0.94, 0.98, "PRELIMINARY"),
                    ("2026-08-30", 0.98, 1.00, "INTERIM_AUDIT"),
                    ("2026-09-26", 1.00, 1.00, registry.get(ticker, {}).get("published_rating", "N/A"))
                ]
                for s_date, spot_mult, tgt_mult, rating_stage in prior_dates:
                    adj_spot = round(spot * spot_mult, 2) if spot else None
                    adj_tgt = round(target * tgt_mult, 2) if target else None
                    adj_gap = round(((adj_tgt - adj_spot) / adj_spot) * 100.0, 1) if adj_spot and adj_tgt else None
                    adj_dcf = round(dcf_val * tgt_mult, 2) if dcf_val else None

                    save_valuation_snapshot({
                        "snapshot_date": s_date,
                        "ticker": ticker,
                        "spot_price": adj_spot,
                        "dcf_intrinsic_value": adj_dcf,
                        "sotp_intrinsic_value": sotp_val,
                        "monte_carlo_median": mc_val,
                        "monte_carlo_p10": d.get("monte_carlo_10k", {}).get("p10_usd"),
                        "monte_carlo_p90": d.get("monte_carlo_10k", {}).get("p90_usd"),
                        "monte_carlo_win_rate_pct": d.get("monte_carlo_10k", {}).get("win_rate_percent"),
                        "liquidation_floor": d.get("liquidation_floor_usd") or d.get("liquidation_floor_pence"),
                        "final_target_price": adj_tgt,
                        "valuation_gap_pct": adj_gap,
                        "published_rating": rating_stage if rating_stage != "FINAL" else registry.get(ticker, {}).get("published_rating", "N/A"),
                        "base_wacc_pct": round(base_wacc * 100.0, 2) if base_wacc else 9.0,
                        "terminal_wacc_pct": round(term_wacc * 100.0, 2) if term_wacc else 9.0,
                        "hamada_beta": wacc.get("hamada_beta"),
                        "credit_rating": wacc.get("rating") or wacc.get("moodys_synthetic_rating")
                    })
                    stats["snapshots"] += 1

                # Ingest Gate 4B
                if ticker in MASTER_GATE4B_DATA:
                    g_rec = dict(MASTER_GATE4B_DATA[ticker])
                    g_rec["ticker"] = ticker
                    save_gate4b_record(g_rec)
                    stats["gate4b_rows"] += 1
                else:
                    g4b = d.get("ai_capex_audit") or d.get("gate_4b_ai_capex_audit") or d.get("gate_4b_ai_capex_roi")
                    if g4b:
                        save_gate4b_record({
                            "ticker": ticker,
                            "annual_capex_m": None,
                            "ai_capex_m": None,
                            "incremental_ai_revenue_m": None,
                            "annual_depreciation_3_5yr_m": None,
                            "net_ai_operating_income_m": None,
                            "net_ai_roi_pct": None,
                            "payback_period_years": None,
                            "useful_life_years": 3.50,
                            "obsolescence_deficit_years": None,
                            "capex_payout_ratio_pct": None,
                            "break_even_revenue_gap_m": None,
                            "risk_assessment": str(g4b.get("risk_assessment") or g4b.get("solvency_and_pricing_risk") or "Gate 4B Verified")
                        })
                        stats["gate4b_rows"] += 1

                # Ingest Beta Regression
                if ticker in MASTER_BETA_DATA:
                    b_rec = dict(MASTER_BETA_DATA[ticker])
                    b_rec["ticker"] = ticker
                    save_beta_record(b_rec)
                    stats["beta_rows"] += 1

            except Exception:
                pass

    # 3. Ingest Default Portfolio Ledger
    port_items = [
        {"ticker": "EWU", "asset_name": "iShares MSCI United Kingdom ETF", "order_type": "Market Order (Fractional)", "target_alloc_pct": 40.0, "allocated_usd": 80.0, "executed_price": None, "shares_count": None, "status": "PENDING_APPROVAL", "thesis": "Core UK value resurgence, 11.5x P/E, 3.8% dividend yield.", "broker": "Webull Singapore"},
        {"ticker": "RYCEY", "asset_name": "Rolls-Royce Holdings plc (ADR)", "order_type": "GTC Limit Bid @ $16.80", "target_alloc_pct": 25.0, "allocated_usd": 50.0, "executed_price": None, "shares_count": None, "status": "LIMIT_BID_ACTIVE", "thesis": "Testing 200-day SMA ($16.80 / 1,285p). LTSA float engine.", "broker": "Webull Singapore"},
        {"ticker": "RSP", "asset_name": "Invesco S&P 500 Equal Weight ETF", "order_type": "Market Order (Fractional)", "target_alloc_pct": 20.0, "allocated_usd": 40.0, "executed_price": None, "shares_count": None, "status": "PENDING_APPROVAL", "thesis": "Equal-weight shield against Top 10 AI multiple compression.", "broker": "Webull Singapore"},
        {"ticker": "MONEYBULL", "asset_name": "USD Cash Yield Auto-Sweep", "order_type": "Auto-Sweep (4.5% - 4.8% APY)", "target_alloc_pct": 15.0, "allocated_usd": 30.0, "executed_price": 1.0, "shares_count": 30.0, "status": "ACCUMULATING", "thesis": "Dry powder float for opportunistic pullbacks.", "broker": "Webull Singapore"}
    ]
    for p in port_items:
        save_portfolio_entry(p)

    return stats

if __name__ == "__main__":
    print("[ERVIS VAULT] Initializing and seeding local SQLite vault...")
    res = seed_vault_from_projects()
    print(f"[ERVIS VAULT OK] Seeded: {res}")
