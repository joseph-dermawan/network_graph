#!/usr/bin/env python3
"""
ERVIS :: SPECIALIZED VALUATION MODULE: CAPEX PAYOUT & CUSTOMER ROI ENGINE
========================================================================
Implements Gate 4B Extension across the Top 10 AI Titans:
1. Provider Internal Capital Engine (CapEx intensity, FCF conversion, ROIC, Shareholder Payout).
2. Customer CapEx Payout Ratio (CPR / "Hardware Tax").
3. Customer Net AI Operating ROI (Gross margin vs straight-line depreciation).
4. Customer Payback Period (T_payback) vs Hardware Obsolescence Window (L_useful).
5. Break-Even Monetization Equation (Required annual software revenue to hit target ROIC).
"""

import sys
import json

def run_capex_payout_and_roi(
    company_name,
    ticker,
    revenue_m,
    nopat_m,
    physical_capex_m,
    cfo_m,
    fcf_m,
    share_repurchases_m,
    dividends_m,
    invested_capital_m,
    hyperscaler_total_capex_b,
    ai_segment_revenue_b,
    customer_incremental_ai_rev_b,
    cloud_software_gross_margin=0.65,
    hardware_useful_life_years=3.50,
    customer_target_roic=0.15
):
    # 1. Provider Internal Metrics
    capex_intensity_pct = (physical_capex_m / revenue_m) * 100.0
    fcf_conversion_pct = (fcf_m / cfo_m) * 100.0 if cfo_m > 0 else 0.0
    internal_roic_pct = (nopat_m / invested_capital_m) * 100.0 if invested_capital_m > 0 else 0.0
    total_shareholder_payout_m = share_repurchases_m + dividends_m
    shareholder_payout_ratio_pct = (total_shareholder_payout_m / fcf_m) * 100.0 if fcf_m > 0 else 0.0

    # 2. Customer CapEx Payout Ratio (CPR)
    cpr_pct = (ai_segment_revenue_b / hyperscaler_total_capex_b) * 100.0

    # 3. Customer Economics & ROI
    customer_gross_profit_b = customer_incremental_ai_rev_b * cloud_software_gross_margin
    annual_hardware_depreciation_b = ai_segment_revenue_b / hardware_useful_life_years
    customer_net_ai_operating_income_b = customer_gross_profit_b - annual_hardware_depreciation_b
    customer_net_roi_pct = (customer_net_ai_operating_income_b / ai_segment_revenue_b) * 100.0

    # 4. Payback Period & Obsolescence Gap
    customer_payback_years = (ai_segment_revenue_b / customer_gross_profit_b) if customer_gross_profit_b > 0 else 999.0
    hardware_obsolescence_gap_years = customer_payback_years - hardware_useful_life_years
    is_deficit = hardware_obsolescence_gap_years > 0

    # 5. Break-Even Monetization
    required_operating_profit_b = ai_segment_revenue_b * customer_target_roic
    required_gross_profit_b = required_operating_profit_b + annual_hardware_depreciation_b
    required_end_customer_ai_rev_b = required_gross_profit_b / cloud_software_gross_margin
    annual_revenue_gap_b = required_end_customer_ai_rev_b - customer_incremental_ai_rev_b

    output = {
        "ticker": ticker,
        "company_name": company_name,
        "provider_internal": {
            "revenue_m": revenue_m,
            "physical_capex_m": physical_capex_m,
            "capex_intensity_pct": round(capex_intensity_pct, 2),
            "free_cash_flow_m": fcf_m,
            "fcf_conversion_pct": round(fcf_conversion_pct, 2),
            "internal_economic_roic_pct": round(internal_roic_pct, 2),
            "shareholder_payout_m": total_shareholder_payout_m,
            "payout_ratio_of_fcf_pct": round(shareholder_payout_ratio_pct, 2)
        },
        "customer_ecosystem": {
            "hyperscaler_total_capex_b": hyperscaler_total_capex_b,
            "ai_hardware_purchases_b": ai_segment_revenue_b,
            "capex_payout_ratio_pct": round(cpr_pct, 2),
            "customer_incremental_ai_rev_b": customer_incremental_ai_rev_b,
            "customer_ai_gross_profit_b": round(customer_gross_profit_b, 2),
            "annual_hardware_depreciation_b": round(annual_hardware_depreciation_b, 2),
            "customer_net_ai_operating_income_b": round(customer_net_ai_operating_income_b, 2),
            "customer_net_roi_pct": round(customer_net_roi_pct, 2),
            "customer_payback_years": round(customer_payback_years, 2),
            "hardware_useful_life_years": hardware_useful_life_years,
            "hardware_obsolescence_gap_years": round(hardware_obsolescence_gap_years, 2),
            "status": "OBSOLESCENCE DEFICIT" if is_deficit else "VALUE ACCRETIVE"
        },
        "breakeven_monetization": {
            "target_customer_roic_pct": customer_target_roic * 100.0,
            "required_annual_ai_rev_b": round(required_end_customer_ai_rev_b, 2),
            "actual_realized_ai_rev_b": customer_incremental_ai_rev_b,
            "annual_revenue_gap_deficit_b": round(annual_revenue_gap_b, 2)
        }
    }
    return output

if __name__ == "__main__":
    res = run_capex_payout_and_roi(
        company_name="NVIDIA Corporation",
        ticker="NVDA",
        revenue_m=215938.0,
        nopat_m=117707.0,
        physical_capex_m=6042.0,
        cfo_m=102718.0,
        fcf_m=96676.0,
        share_repurchases_m=32000.0,
        dividends_m=900.0,
        invested_capital_m=146371.0,
        hyperscaler_total_capex_b=408.0,
        ai_segment_revenue_b=185.0,
        customer_incremental_ai_rev_b=58.0
    )
    print(json.dumps(res, indent=2))
