#!/usr/bin/env python3
"""
ERVIS Thematic AI CapEx & Counterparty Circularity Valuation Engine
Calculates:
1. Anthropic compute spend round-tripping into AWS and GCP revenue and operating income.
2. The Big 4 Hyperscaler Depreciation Cliff (3.5-yr realistic GPU obsolescence vs. 5.5-yr stated life).
3. Token deflation curve vs. GPU hardware amortization breakeven threshold.
"""

import json
import os
import math

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "model_outputs.json")

def load_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
        return json.load(f)

def run_circularity_analysis():
    commitments = load_json("commitments_matrix_anthropic_aws_gcp.json")
    hyperscalers = load_json("hyperscaler_capex_depreciation_timeseries.json")
    token_data = load_json("token_deflation_vs_gpu_amortization.json")

    # 1. Circularity Calculations
    schedule = commitments["anthropic_commitments_schedule"]
    aws_share = commitments["counterparty_breakdown"]["amazon_aws"]["nominal_share_pct"] / 100.0
    gcp_share = commitments["counterparty_breakdown"]["google_gcp"]["nominal_share_pct"] / 100.0

    annual_commitments = [
        {"year": 2027, "total": schedule["2027"]},
        {"year": 2028, "total": schedule["2028"]},
        {"year": 2029, "total": schedule["2029"]},
        {"year": 2030, "total": schedule["2030"]},
        {"year": 2031, "total": schedule["2031_2033"] / 3.0},
        {"year": 2032, "total": schedule["2031_2033"] / 3.0},
        {"year": 2033, "total": schedule["2031_2033"] / 3.0}
    ]

    circularity_results = []
    aws_ev_multiple = 9.0  # EV/Sales multiple applied to AWS
    gcp_ev_multiple = 8.5  # EV/Sales multiple applied to GCP
    aws_ebit_margin = 0.385
    gcp_ebit_margin = 0.280

    for item in annual_commitments:
        yr = item["year"]
        tot = item["total"]
        aws_rev = tot * aws_share
        gcp_rev = tot * gcp_share

        aws_ebit = aws_rev * aws_ebit_margin
        gcp_ebit = gcp_rev * gcp_ebit_margin

        aws_ev_uplift = aws_rev * aws_ev_multiple
        gcp_ev_uplift = gcp_rev * gcp_ev_multiple

        circularity_results.append({
            "year": yr,
            "anthropic_total_spend_usd_m": tot,
            "aws_revenue_usd_m": round(aws_rev, 1),
            "aws_ebit_usd_m": round(aws_ebit, 1),
            "aws_implied_ev_uplift_usd_b": round(aws_ev_uplift / 1000.0, 2),
            "gcp_revenue_usd_m": round(gcp_rev, 1),
            "gcp_ebit_usd_m": round(gcp_ebit, 1),
            "gcp_implied_ev_uplift_usd_b": round(gcp_ev_uplift / 1000.0, 2)
        })

    # Total over commitment horizon
    tot_aws_rev = sum(x["aws_revenue_usd_m"] for x in circularity_results)
    tot_gcp_rev = sum(x["gcp_revenue_usd_m"] for x in circularity_results)
    tot_aws_ebit = sum(x["aws_ebit_usd_m"] for x in circularity_results)
    tot_gcp_ebit = sum(x["gcp_ebit_usd_m"] for x in circularity_results)

    # 2. Hyperscaler Big 4 Depreciation Cliff Analysis
    # Compare 5.5-year stated life vs 3.5-year realistic AI GPU useful life
    # Projections 2024 to 2030
    capex_history = {
        2021: 126.5,
        2022: 151.0,
        2023: 141.2,
        2024: 223.6,
        2025: 312.5,
        2026: 394.0,
        2027: 430.0,
        2028: 460.0,
        2029: 485.0,
        2030: 500.0
    }

    depreciation_cliff_results = []
    # AI accelerator / server portion of total capex is estimated at 65%
    ai_ratio = 0.65
    
    for yr in range(2024, 2031):
        # Stated useful life: 5.5 years straight line (18.18% per year)
        # Realistic useful life: 3.5 years straight line (28.57% per year)
        # Facilities & non-compute infra (35%) depreciated over 15.0 years in both scenarios
        
        # Calculate AI server D&A under 5.5 years:
        stated_server_dna = 0.0
        for i in range(1, 6):
            c = capex_history.get(yr - i, 120.0) * ai_ratio
            stated_server_dna += c / 5.5
        # add half year for the 6th prior year
        stated_server_dna += (capex_history.get(yr - 6, 100.0) * ai_ratio) * 0.5 / 5.5

        # Calculate AI server D&A under 3.5 years:
        realistic_server_dna = 0.0
        for i in range(1, 4):
            c = capex_history.get(yr - i, 120.0) * ai_ratio
            realistic_server_dna += c / 3.5
        # add half year for the 4th prior year
        realistic_server_dna += (capex_history.get(yr - 4, 120.0) * ai_ratio) * 0.5 / 3.5

        # Infra D&A (35% of capex over 15 years):
        infra_dna = sum((capex_history.get(yr - i, 100.0) * 0.35) / 15.0 for i in range(1, 16))

        total_stated_dna = stated_server_dna + infra_dna
        total_realistic_dna = realistic_server_dna + infra_dna

        annual_gap = total_realistic_dna - total_stated_dna
        
        # Cumulative balance sheet asset overhang (Overstated Net PP&E under 5.5-yr schedule)
        # Stated net book value of AI servers:
        stated_nbv = sum(capex_history.get(yr - i, 120.0) * ai_ratio * max(0.0, (5.5 - i + 0.5) / 5.5) for i in range(1, 6))
        realistic_nbv = sum(capex_history.get(yr - i, 120.0) * ai_ratio * max(0.0, (3.5 - i + 0.5) / 3.5) for i in range(1, 4))
        cumulative_overhang = max(0.0, stated_nbv - realistic_nbv)

        hyperscaler_ebit_proxy = 320.0 + (yr - 2024) * 35.0  # Estimated combined Big 4 EBIT
        margin_drag_bps = (annual_gap / hyperscaler_ebit_proxy) * 10000.0

        depreciation_cliff_results.append({
            "year": yr,
            "annual_capex_usd_b": capex_history[yr],
            "stated_dna_usd_b": round(total_stated_dna, 1),
            "realistic_dna_usd_b": round(total_realistic_dna, 1),
            "annual_depreciation_gap_usd_b": round(annual_gap, 1),
            "cumulative_balance_sheet_overhang_usd_b": round(cumulative_overhang, 1),
            "operating_margin_drag_bps": round(margin_drag_bps, 0)
        })

    # 3. Token Deflation vs. Hardware Amortization Breakeven
    gpu_stats = token_data["gpu_hardware_amortization_unit_cost"]
    breakeven_cost = gpu_stats["breakeven_hardware_cost_per_m_tokens_usd"]

    token_margins = []
    for m in token_data["token_pricing_deflation_timeline"]:
        price = m["blended_price"]
        gross_profit = price - breakeven_cost
        gross_margin_pct = (gross_profit / price) * 100.0 if price > 0 else -100.0
        status = "HEALTHY_MARGIN" if gross_margin_pct > 40 else ("MARGIN_SQUEEZE" if gross_margin_pct > 0 else "NEGATIVE_GROSS_MARGIN_IMPAIRMENT")

        token_margins.append({
            "model": m["model"],
            "date": m["date"],
            "blended_price_usd": price,
            "hardware_cost_usd": breakeven_cost,
            "gross_profit_usd": round(gross_profit, 2),
            "gross_margin_pct": round(gross_margin_pct, 1),
            "economic_status": status
        })

    # Aggregate outputs
    output = {
        "status": "ENGINE_RUN_SUCCESSFUL",
        "circularity_summary": {
            "total_anthropic_spend_usd_m": schedule["total_nominal_commitments"],
            "aws_total_revenue_usd_m": round(tot_aws_rev, 1),
            "aws_total_ebit_usd_m": round(tot_aws_ebit, 1),
            "aws_cumulative_ev_uplift_usd_b": round((tot_aws_rev * aws_ev_multiple) / 1000.0, 2),
            "gcp_total_revenue_usd_m": round(tot_gcp_rev, 1),
            "gcp_total_ebit_usd_m": round(tot_gcp_ebit, 1),
            "gcp_cumulative_ev_uplift_usd_b": round((tot_gcp_rev * gcp_ev_multiple) / 1000.0, 2),
            "amazon_equity_invested_usd_m": 23000.0,
            "amazon_value_multiplier": round(((tot_aws_rev * aws_ev_multiple) / 1000.0) / 23.0, 2),
            "google_equity_invested_usd_m": 13000.0,
            "google_value_multiplier": round(((tot_gcp_rev * gcp_ev_multiple) / 1000.0) / 13.0, 2)
        },
        "annual_circularity_schedule": circularity_results,
        "depreciation_cliff_schedule": depreciation_cliff_results,
        "token_margin_trajectory": token_margins
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"[ENGINE SUCCESS] Output successfully written to {OUTPUT_FILE}")
    print(f"-> AWS Projected Cumulative ARR: ${tot_aws_rev/1000.0:.1f}B | EBIT: ${tot_aws_ebit/1000.0:.1f}B")
    print(f"-> GCP Projected Cumulative ARR: ${tot_gcp_rev/1000.0:.1f}B | EBIT: ${tot_gcp_ebit/1000.0:.1f}B")
    print(f"-> Big 4 Big CapEx 2026E: $394B | Peak Depreciation Gap (2027): ${depreciation_cliff_results[3]['annual_depreciation_gap_usd_b']}B")

if __name__ == "__main__":
    run_circularity_analysis()
