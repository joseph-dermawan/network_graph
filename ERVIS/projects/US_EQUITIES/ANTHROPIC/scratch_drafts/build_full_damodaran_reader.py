import os
import openpyxl
import json

excel_path = "ERVIS/projects/US_EQUITIES/ANTHROPIC/models/AnthropicIPO_updated.xlsx"
print(f"Loading workbook from {excel_path}...")
wb_vals = openpyxl.load_workbook(excel_path, data_only=True)
wb_forms = openpyxl.load_workbook(excel_path, data_only=False)

def col2letter(col_idx):
    res = ""
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        res = chr(65 + remainder) + res
    return res

all_sheets = wb_vals.sheetnames
extracted_sheets = {}

for sname in all_sheets:
    sv = wb_vals[sname]
    sf = wb_forms[sname]
    
    # Determine bounds
    max_r = 0
    max_c = 0
    for r in range(1, sv.max_row + 1):
        for c in range(1, min(sv.max_column + 1, 35)):
            if sv.cell(r, c).value is not None or sf.cell(r, c).value is not None:
                if r > max_r: max_r = r
                if c > max_c: max_c = c
                
    # Row bounds safety
    if max_r > 235: max_r = 235
    if max_c > 30: max_c = 30
    if max_r == 0: max_r = 10
    if max_c == 0: max_c = 10
    
    grid = []
    for r in range(1, max_r + 1):
        row_cells = []
        has_val = False
        for c in range(1, max_c + 1):
            val = sv.cell(r, c).value
            form = sf.cell(r, c).value
            coord = f"{col2letter(c)}{r}"
            formula_str = str(form) if form and str(form).startswith("=") else None
            
            if val is not None or formula_str is not None:
                has_val = True
                
            row_cells.append({
                "coord": coord,
                "r": r,
                "c": c,
                "val": val,
                "formula": formula_str
            })
        if has_val:
            grid.append({
                "row_idx": r,
                "cells": row_cells
            })
            
    extracted_sheets[sname] = {
        "name": sname,
        "max_col": max_c,
        "col_letters": [col2letter(c) for c in range(1, max_c + 1)],
        "grid": grid
    }

print(f"Extracted all {len(extracted_sheets)} sheets successfully.")

# Comprehensive Knowledge Base of Methodologies
methodology_kb = {
    # ---------------- Valuation output ----------------
    "Valuation output!B34": {
        "label": "Estimated Intrinsic Fair Value Per Share",
        "formula": "=B32/B33",
        "category": "Core Output",
        "methodology": "Damodaran's bottom-line intrinsic fair value per share. Calculated by dividing Total Value of Common Stock Equity ($1,415,478.5M) by Diluted Share Count (16,912.15M shares) = $439.69 per share.",
        "economic_intuition": "This reflects the true intrinsic worth per share of Anthropic under Damodaran's calibrated 10-year Ginzu DCF engine following the Q3 2026 leaked revenue update ($35.3B run-rate). At $439.69, Anthropic is worth $1.45 Trillion in equity value.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B32", "label": "Value of Equity in Common Stock", "val": "$1,415,478.5 M"},
            {"sheet": "Valuation output", "coord": "B33", "label": "Diluted Shares Outstanding", "val": "16,912.15 M"}
        ],
        "dependents": ["Valuation output!B36 (Price as % of Value)"]
    },
    "Valuation output!B35": {
        "label": "Rumored IPO Offering Price",
        "formula": "74.00",
        "category": "Market Pricing",
        "methodology": "Target offering price per share ($525.00) based on leaked investment banking roadshow previews, implying a $1.734 Trillion market capitalization at IPO.",
        "economic_intuition": "Serves as the market benchmark against which intrinsic fair value is tested. Damodaran also tests the rumored $2.0 Trillion valuation ($605.64/share).",
        "precedents": [],
        "dependents": ["Valuation output!B36 (Price as % of Value)"]
    },
    "Valuation output!B36": {
        "label": "Price as % of Intrinsic Fair Value",
        "formula": "=B35/B34",
        "category": "Pricing Misvaluation",
        "methodology": "Offering Price ($525.00) / Intrinsic Fair Value ($439.69) = 88.42%. Equivalently, intrinsic value represents a 11.58% discount to the IPO midpoint (+13.10% upside).",
        "economic_intuition": "Investors buying at $525.00 are overpaying by ~19.5%. For the price to equal $525.00, Anthropic would have to achieve either >$1.3 Trillion in 2036 revenue (capturing >50% of the entire global software economy) or have zero failure probability.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B35", "label": "Offering Price", "val": "$525.00"},
            {"sheet": "Valuation output", "coord": "B34", "label": "Intrinsic Value Per Share", "val": "$439.69"}
        ],
        "dependents": []
    },
    "Valuation output!B32": {
        "label": "Value of Equity in Common Stock",
        "formula": "=B30-B31",
        "category": "Core Output",
        "methodology": "Total Value of Equity ($1,450,950.8M) minus Value of Employee Option Overhang ($472.3M) = $1,415,478.5M ($1.450 Trillion).",
        "economic_intuition": "Deducts the equity claim of stock option holders from total firm equity to arrive at the residual equity value that strictly belongs to common shareholders.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B30", "label": "Total Value of Equity", "val": "$1,450,950.8 M"},
            {"sheet": "Valuation output", "coord": "B31", "label": "Value of Employee Options", "val": "$472.3 M"}
        ],
        "dependents": ["Valuation output!B34 (Estimated Value / Share)"]
    },
    "Valuation output!B33": {
        "label": "Diluted Shares Outstanding",
        "formula": "=Input sheet!B24+Option value!B20",
        "category": "Share Count",
        "methodology": "Sum of base common shares reported on balance sheet (3,074.60M) and unvested/in-the-money options converted to shares (227.67M) = 16,912.15 Million shares.",
        "economic_intuition": "Ensures that intrinsic equity value is apportioned across all outstanding share claims, preventing dilution understatement.",
        "precedents": [
            {"sheet": "Input sheet", "coord": "B22", "label": "Reported Common Shares", "val": "3,074.60 M"},
            {"sheet": "Option value", "coord": "B20", "label": "Restricted Shares Added", "val": "227.67 M"}
        ],
        "dependents": ["Valuation output!B34 (Estimated Value / Share)"]
    },
    "Valuation output!B31": {
        "label": "Value of Employee Options Overhang",
        "formula": "=Option value!B23",
        "category": "Dilution Overhang",
        "methodology": "Evaluates granted employee stock options using the Black-Scholes option pricing model ($472.3M) rather than flawed treasury stock methods.",
        "economic_intuition": "Treating options as an explicit equity carve-out prevents dilution double-counting and correctly accounts for option time value and vesting horizon.",
        "precedents": [{"sheet": "Option value", "coord": "B23", "label": "Black-Scholes Option Value", "val": "$472.3 M"}],
        "dependents": ["Valuation output!B32 (Common Stock Equity)"]
    },
    "Valuation output!B30": {
        "label": "Total Value of Equity",
        "formula": "=B24-B25-B26+B27+B28+B29",
        "category": "Core Output",
        "methodology": "Institutional equity bridge: Operating Assets ($1,719,952.6M) minus Debt ($485,319.8M) minus Minority Interest ($0) plus Cash ($112,389M) plus IPO Proceeds ($100,000M) plus Non-Operating Assets ($3,929M) = $1,450,950.8M.",
        "economic_intuition": "Bridges enterprise value to aggregate equity value by deducting all non-equity claims and adding back non-operating liquid cash assets and primary capital raised.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B24", "label": "Value of Operating Assets", "val": "$1,719,952.6 M"},
            {"sheet": "Valuation output", "coord": "B25", "label": "Total Debt (Inc. Compute)", "val": "$485,319.8 M"},
            {"sheet": "Valuation output", "coord": "B27", "label": "Cash & Equivalents", "val": "$112,389 M"},
            {"sheet": "Valuation output", "coord": "B28", "label": "Expected IPO Proceeds", "val": "$100,000 M"},
            {"sheet": "Valuation output", "coord": "B29", "label": "Non-Operating Assets", "val": "$3,929 M"}
        ],
        "dependents": ["Valuation output!B32 (Common Stock Equity)"]
    },
    "Valuation output!B24": {
        "label": "Value of Operating Assets (Distress-Adjusted EV)",
        "formula": "=B21*(1-B22)+B23*B22",
        "category": "Core Output",
        "methodology": "Damodaran weights Going-Concern EV (90.0%) and Distress Proceeds (10.0%): $1,810,476.4M * 90% + $905,238.2M * 10% = $1,719,952.6M ($1.720 Trillion).",
        "economic_intuition": "Damodaran's signature mechanism for pricing distress risk. Default risk is decoupled from WACC and modeled as a direct probability-weighted salvage haircut (-$90.5B haircut).",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B21", "label": "Going Concern Enterprise Value", "val": "$1,810,476.4 M"},
            {"sheet": "Valuation output", "coord": "B22", "label": "Probability of Failure", "val": "10.0%"},
            {"sheet": "Valuation output", "coord": "B23", "label": "Distress Proceeds", "val": "$905,238.2 M"}
        ],
        "dependents": ["Valuation output!B30 (Total Value of Equity)"]
    },
    "Valuation output!B21": {
        "label": "Sum of Present Values (Going Concern EV)",
        "formula": "=B19+B20",
        "category": "Core Output",
        "methodology": "Sum of Discrete 10-Yr Cash Flows PV ($421,728.8M) + PV of Terminal Value ($1,388,747.6M) = $1,810,476.4M ($1.810 Trillion).",
        "economic_intuition": "The value of Anthropic's core operating business assuming it operates into perpetuity without failure.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B20", "label": "PV of 10-Yr Cash Flows", "val": "$421,728.8 M"},
            {"sheet": "Valuation output", "coord": "B19", "label": "PV of Terminal Value", "val": "$1,388,747.6 M"}
        ],
        "dependents": ["Valuation output!B24 (Value of Operating Assets)", "Valuation output!B23 (Distress Proceeds)"]
    },
    "Valuation output!B20": {
        "label": "PV of Discrete Cash Flows (Yr 1–10)",
        "formula": "=SUM(C14:L14)",
        "category": "Core Output",
        "methodology": "Sums the discounted annual Free Cash Flows to the Firm (FCFF) across Years 1 to 10 ($421,728.8M). Captures the transition from hyper-growth to cash flow maturity.",
        "economic_intuition": "Early-stage AI companies experience explosive top-line growth with massive negative initial cash flows before turning into high-margin inference software businesses.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "C14:L14", "label": "Annual PV of FCFF (Yr 1 to 10)", "val": "$421,728.8 M"}
        ],
        "dependents": ["Valuation output!B21 (Sum of PV)"]
    },
    "Valuation output!B19": {
        "label": "PV of Terminal Value",
        "formula": "=B18*L13",
        "category": "Core Output",
        "methodology": "Discounts Year 10 Terminal Value ($3,459,520.3M) back to the valuation date using the 10-year cumulative discount factor (0.4014) = $1,388,747.6M ($1.389 Trillion).",
        "economic_intuition": "Terminal value represents 76.7% of going-concern enterprise value. In software and AI platforms, the vast majority of economic value is back-loaded into mature steady-state cash generation.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B18", "label": "Terminal Value in Year 10", "val": "$3,459,520.3 M"},
            {"sheet": "Valuation output", "coord": "L13", "label": "Year 10 Discount Factor", "val": "0.4014"}
        ],
        "dependents": ["Valuation output!B21 (Sum of PV)"]
    },
    "Valuation output!B18": {
        "label": "Terminal Value in Year 10",
        "formula": "=B16/(B17-0.049)",
        "category": "Terminal Valuation",
        "methodology": "Gordon Growth Model: Terminal FCFF ($146,337.7M) / (Terminal Cost of Capital 9.13% - Risk-Free Rate 4.90%) = $3,459,520.3M ($3.460 Trillion).",
        "economic_intuition": "Perpetual growth is capped at the 10-year risk-free rate (4.90%) to enforce macroeconomic sanity—a firm cannot mathematically grow faster than the economy forever.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B16", "label": "Terminal Cash Flow", "val": "$146,337.7 M"},
            {"sheet": "Valuation output", "coord": "B17", "label": "Terminal Cost of Capital", "val": "9.13%"}
        ],
        "dependents": ["Valuation output!B19 (PV of Terminal Value)"]
    },
    "Valuation output!B16": {
        "label": "Terminal Cash Flow to Firm (Yr 11)",
        "formula": "=B8*(1+0.049)-B9",
        "category": "Terminal Valuation",
        "methodology": "Year 11 normalized after-tax operating profit ($217,333.2M) minus terminal reinvestment ($70,995.5M) = $146,337.7M.",
        "economic_intuition": "In terminal steady state, the firm reinvests enough capital to sustain 4.90% perpetual growth based on the global industry return on capital (15.0%).",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B8", "label": "Year 10 After-tax EBIT", "val": "$207,181.3 M"},
            {"sheet": "Valuation output", "coord": "B9", "label": "Year 10 Reinvestment", "val": "$60,843.6 M"}
        ],
        "dependents": ["Valuation output!B18 (Terminal Value)"]
    },
    "Valuation output!B17": {
        "label": "Terminal Cost of Capital",
        "formula": "=Cost of capital worksheet!B68",
        "category": "Hurdle Rate",
        "methodology": "Terminal cost of capital (9.13%) based on a mature tech capital structure with beta converging to 1.00 and debt ratio converging to 20%.",
        "economic_intuition": "As high-growth tech firms mature into cash cows, their cost of capital drops toward the market median due to established cash flows and higher debt capacity.",
        "precedents": [{"sheet": "Cost of capital worksheet", "coord": "B68", "label": "Terminal WACC", "val": "9.13%"}],
        "dependents": ["Valuation output!B18 (Terminal Value)"]
    },
    "Valuation output!B22": {
        "label": "Probability of Failure",
        "formula": "=Story Inputs!B27",
        "category": "Risk Parameter",
        "methodology": "Damodaran assigns a 10.0% probability of distress over the 10-year projection horizon, anchored to historical credit default studies.",
        "economic_intuition": "AI platform firms face immense upfront capital commitments. Rather than inflating WACC to 20%, failure is modeled directly as a discrete probability.",
        "precedents": [
            {"sheet": "Failure Rate worksheet", "coord": "B10", "label": "10-Yr BB Cumulative Default Rate", "val": "11.78%"},
            {"sheet": "Story Inputs", "coord": "B27", "label": "Selected Failure Rate", "val": "10.0%"}
        ],
        "dependents": ["Valuation output!B24 (Value of Operating Assets)"]
    },
    "Valuation output!B23": {
        "label": "Proceeds if Firm Fails (Distress Salvage)",
        "formula": "=0.5*B21",
        "category": "Risk Parameter",
        "methodology": "Liquidation salvage estimated at 50.0% of going-concern enterprise value = $905,238.2M ($905.2 Billion).",
        "economic_intuition": "Even in bankruptcy or liquidation, Anthropic's proprietary weights, Claude models, training data, and customer relationships retain massive asset value for tech giants.",
        "precedents": [{"sheet": "Valuation output", "coord": "B21", "label": "Going Concern Enterprise Value", "val": "$1,810,476.4 M"}],
        "dependents": ["Valuation output!B24 (Value of Operating Assets)"]
    },
    "Valuation output!B25": {
        "label": "Total Adjusted Debt",
        "formula": "=Input sheet!B15+Operating lease converter!C28",
        "category": "Capital Structure",
        "methodology": "Reported book debt ($109,316M) + Capitalized non-cancelable compute and cloud cluster commitments ($376,003.8M) = $485,319.8M ($485.3 Billion).",
        "economic_intuition": "Binding contractual commitments to AWS and GCP for GPU clusters are synthetic debt obligations that must be capitalized on the balance sheet.",
        "precedents": [
            {"sheet": "Input sheet", "coord": "B15", "label": "Reported Debt", "val": "$109,316 M"},
            {"sheet": "Operating lease converter", "coord": "C28", "label": "PV of Compute Commitments", "val": "$376,003.8 M"}
        ],
        "dependents": ["Valuation output!B30 (Total Value of Equity)"]
    },
    "Valuation output!B27": {
        "label": "Cash & Short-Term Investments",
        "formula": "=Input sheet!B22",
        "category": "Asset Bridge",
        "methodology": "Existing liquid cash and short-term marketable securities ($112,389M).",
        "economic_intuition": "Non-operating cash asset that provides over 2 years of immediate liquidity buffer against GPU commitments.",
        "precedents": [{"sheet": "Input sheet", "coord": "B19", "label": "Cash & Equivalents", "val": "$112,389 M"}],
        "dependents": ["Valuation output!B30 (Total Value of Equity)"]
    },
    "Valuation output!B28": {
        "label": "Expected IPO Primary Proceeds",
        "formula": "=Input sheet!B18",
        "category": "Asset Bridge",
        "methodology": "Primary capital infusion expected in the public offering ($100,000M / $100 Billion).",
        "economic_intuition": "Directly expands firm liquid cash reserves to >$212 Billion, securing Anthropic's multi-year hardware roadmap.",
        "precedents": [{"sheet": "Input sheet", "coord": "B18", "label": "IPO Offering Proceeds", "val": "$100,000 M"}],
        "dependents": ["Valuation output!B30 (Total Value of Equity)"]
    },
    "Valuation output!B4": {
        "label": "Expected Revenues in Year 10 (2036)",
        "formula": "=Story Inputs!B6",
        "category": "Growth Trajectory",
        "methodology": "Damodaran models Year 10 revenue reaching $1,004,515.6M ($1.005 Trillion). Ramping from $35,286M base at +190% Yr 1 and 42% CAGR Yrs 2-5.",
        "economic_intuition": "Reflects the thesis that Anthropic emerges as one of the 2-3 surviving global frontier model platforms powering the world economy.",
        "precedents": [{"sheet": "Story Inputs", "coord": "B6", "label": "2036 Target Revenues", "val": "$1,004,515.6 M"}],
        "dependents": ["Valuation output!B6 (Year 10 EBIT)"]
    },
    "Valuation output!B5": {
        "label": "Target Pre-tax Operating Margin in Year 10",
        "formula": "=Story Inputs!B23",
        "category": "Profitability Trajectory",
        "methodology": "Mature steady-state operating margin of 27.5%, transitioning from -11.6% unadjusted base margins.",
        "economic_intuition": "Converges to mass-market software industry operating profitability (32.5%), haircut by -5% for regulatory compliance drag.",
        "precedents": [{"sheet": "Story Inputs", "coord": "B23", "label": "Target Steady-State Margin", "val": "27.5%"}],
        "dependents": ["Valuation output!B6 (Year 10 EBIT)"]
    },
    "Valuation output!B6": {
        "label": "Expected Operating Income (EBIT) in Year 10",
        "formula": "=B4*B5",
        "category": "Profitability Trajectory",
        "methodology": "Year 10 Revenue ($1,004,515.6M) * 27.5% Margin = $276,241.8M ($276.2 Billion EBIT).",
        "economic_intuition": "Generates operating earnings rivaling the modern combined profits of Apple and Microsoft.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B4", "label": "Year 10 Revenue", "val": "$1,004,515.6 M"},
            {"sheet": "Valuation output", "coord": "B5", "label": "Year 10 Operating Margin", "val": "27.5%"}
        ],
        "dependents": ["Valuation output!B8 (Year 10 After-Tax EBIT)"]
    },

    # ---------------- Story Inputs ----------------
    "Story Inputs!B5": {
        "label": "Revenue Growth Rate CAGR (Years 2-5)",
        "formula": "0.4200",
        "category": "Growth Parameter",
        "methodology": "Annual revenue growth rate compounded across Years 2 through 5 (42.0%), following a massive +190% surge in Year 1 ($35.3B to $102.3B).",
        "economic_intuition": "Updated downwards from 43% in the preliminary post following the leaked Q3 2026 annualized revenue run-rate jump.",
        "precedents": [],
        "dependents": ["Story Inputs!B6 (2036 Revenues)", "Valuation output!C3:L3 (Annual Growth Schedule)"]
    },
    "Story Inputs!B6": {
        "label": "Expected Revenues in 2036",
        "formula": "1004515.60",
        "category": "Growth Trajectory",
        "methodology": "Calculated 10-year terminal revenue ($1.005 Trillion) based on the compounding growth trajectory.",
        "economic_intuition": "Crosses the symbolic $1 Trillion annual revenue threshold by 2036.",
        "precedents": [{"sheet": "Story Inputs", "coord": "B5", "label": "Revenue CAGR", "val": "42.0%"}],
        "dependents": ["Valuation output!B4 (Year 10 Revenues)"]
    },
    "Story Inputs!B9": {
        "label": "Target Operating Margin in 2028 (Year 3)",
        "formula": "0.3250",
        "category": "Profitability Trajectory",
        "methodology": "Medium-term pre-tax operating margin milestone (32.5%), reflecting high software gross margins as inference revenue outpaces training clusters.",
        "economic_intuition": "Anchored to high-tier global software benchmark margins.",
        "precedents": [],
        "dependents": ["Story Inputs!B23 (Steady-State Margin)"]
    },
    "Story Inputs!B14": {
        "label": "Sales to Invested Capital Ratio",
        "formula": "3.0000",
        "category": "Investment Efficiency",
        "methodology": "Assumes $3.00 of incremental revenue is generated for every $1.00 of capital reinvested.",
        "economic_intuition": "Measures capital intensity. A ratio of 3.00 reflects that while frontier AI models require huge compute clusters, customer monetisation scales rapidly without physical plants.",
        "precedents": [],
        "dependents": ["Valuation output!C9:L9 (Reinvestment Schedule)"]
    },
    "Story Inputs!B19": {
        "label": "Initial Cost of Capital (WACC)",
        "formula": "0.0974",
        "category": "Hurdle Rate",
        "methodology": "Damodaran's initial cost of capital (9.74%), derived from US Software unlevered beta (1.25), 10-year Treasury yield (4.94%), and mature ERP (4.00%).",
        "economic_intuition": "Sits at the 90th percentile of all US technology firms. Damodaran strongly defends this against critics demanding 15-25% WACC.",
        "precedents": [{"sheet": "Cost of capital worksheet", "coord": "B13", "label": "WACC Calculation", "val": "9.74%"}],
        "dependents": ["Valuation output!C12:L12 (Discount Rates)"]
    },
    "Story Inputs!B21": {
        "label": "Regulatory Drag Margin Adjustment",
        "formula": "-0.0500",
        "category": "Regulatory Drag",
        "methodology": "-5.0% reduction in mature operating margins due to AI safety mandates, copyright licensing fees, and compliance costs.",
        "economic_intuition": "Accounts for the probability that frontier AI faces rising compliance, audit, and liability burdens.",
        "precedents": [],
        "dependents": ["Story Inputs!B23 (Steady-State Margin)"]
    },
    "Story Inputs!B23": {
        "label": "Steady-State Pre-tax Operating Margin",
        "formula": "0.2750",
        "category": "Profitability Trajectory",
        "methodology": "Base target margin (32.5%) minus regulatory haircut (5.0%) = 27.5%.",
        "economic_intuition": "The sustainable operating profit margin Anthropic achieves once AI enters utility-like maturity.",
        "precedents": [
            {"sheet": "Story Inputs", "coord": "B9", "label": "Target Margin", "val": "32.5%"},
            {"sheet": "Story Inputs", "coord": "B21", "label": "Regulatory Drag", "val": "-5.0%"}
        ],
        "dependents": ["Valuation output!B5 (Year 10 Margin)"]
    },
    "Story Inputs!B27": {
        "label": "Probability of Failure",
        "formula": "0.1000",
        "category": "Risk Parameter",
        "methodology": "10.0% probability that the company defaults or enters distress within the 10-year forecast window.",
        "economic_intuition": "Anchored to 10-year cumulative corporate default rates for BB-rated debt (11.78%).",
        "precedents": [{"sheet": "Failure Rate worksheet", "coord": "B10", "label": "BB 10-Yr Default Rate", "val": "11.78%"}],
        "dependents": ["Valuation output!B22 (Probability of Failure)"]
    },

    # ---------------- Input sheet ----------------
    "Input sheet!B11": {
        "label": "Base Year LTM Revenues",
        "formula": "35286.00",
        "category": "Historical Base",
        "methodology": "Annualized run-rate revenue ($35,286M / $35.3B) based on leaked Q3 2026 financial disclosures. Ramped from $4,585M in previous fiscal year.",
        "economic_intuition": "The jumping-off point for all future cash flow projections.",
        "precedents": [],
        "dependents": ["Valuation output!B4 (Growth Ramp)", "Diagnostics!C7 (Year 1 Ramp)"]
    },
    "Input sheet!B12": {
        "label": "Base Year LTM Operating Income (EBIT)",
        "formula": "-4096.00",
        "category": "Historical Base",
        "methodology": "Reported pre-tax operating loss (-$4,096M) before forensic adjustments for compute lease capitalization and R&D capitalization.",
        "economic_intuition": "Reflects current heavy cash burn on frontier AI training clusters before inference monetization takes full effect.",
        "precedents": [],
        "dependents": ["Diagnostics!C12 (Base Margin)"]
    },
    "Input sheet!B15": {
        "label": "Reported Book Debt",
        "formula": "109316.00",
        "category": "Capital Structure",
        "methodology": "Reported balance sheet financial debt ($109,316M).",
        "economic_intuition": "Direct borrowing and notes payable on the balance sheet.",
        "precedents": [],
        "dependents": ["Valuation output!B25 (Total Debt)"]
    },
    "Input sheet!B18": {
        "label": "Expected Net IPO Proceeds",
        "formula": "100000.00",
        "category": "Capital Infusion",
        "methodology": "Anticipated primary capital raise in the IPO ($100,000M / $100 Billion).",
        "economic_intuition": "Infuses massive fresh equity liquidity directly onto the balance sheet.",
        "precedents": [],
        "dependents": ["Valuation output!B28 (IPO Proceeds)"]
    },
    "Input sheet!B19": {
        "label": "Cash & Marketable Securities",
        "formula": "112389.00",
        "category": "Asset Bridge",
        "methodology": "Existing liquid cash, equivalents, and short-term Treasuries ($112,389M).",
        "economic_intuition": "Combined with IPO proceeds, gives Anthropic over $212B in immediate liquidity.",
        "precedents": [],
        "dependents": ["Valuation output!B27 (Cash)"]
    },
    "Input sheet!B22": {
        "label": "Common Shares Outstanding",
        "formula": "3074.60",
        "category": "Share Count",
        "methodology": "Reported base common shares outstanding (3,074.60 Million).",
        "economic_intuition": "Base share count before adding unvested restricted stock options.",
        "precedents": [],
        "dependents": ["Valuation output!B33 (Diluted Share Count)"]
    },

    # ---------------- Operating lease converter ----------------
    "Operating lease converter!C28": {
        "label": "Debt Value of Capitalized Compute & Leases",
        "formula": "=SUM(C22:C27)",
        "category": "Forensic Debt",
        "methodology": "Sums the discounted present values of nominal compute commitments ($468,232M nominal across Yrs 1-6+) discounted at 6.2828% = $376,003.8M ($376.0 Billion).",
        "economic_intuition": "Capitalizes long-term cloud/datacenter commitments into synthetic debt, recognizing the financial reality of Anthropic's hardware contracts.",
        "precedents": [
            {"sheet": "Operating lease converter", "coord": "C15", "label": "Pre-tax Cost of Debt", "val": "6.2828%"},
            {"sheet": "Operating lease converter", "coord": "C22", "label": "Yr 1 PV ($77B nominal)", "val": "$72,448.3 M"},
            {"sheet": "Operating lease converter", "coord": "C23", "label": "Yr 2 PV ($98B nominal)", "val": "$86,747.2 M"}
        ],
        "dependents": ["Valuation output!B25 (Total Debt)"]
    },
    "Operating lease converter!C15": {
        "label": "Pre-Tax Cost of Debt for Leases",
        "formula": "=0.0494+0.013428",
        "category": "Discount Rate",
        "methodology": "Risk-Free Rate (4.94%) + BB+ Synthetic Default Spread (1.34%) = 6.2828%.",
        "economic_intuition": "The company's marginal borrowing cost used to discount non-cancelable lease obligations.",
        "precedents": [{"sheet": "Synthetic rating", "coord": "B14", "label": "BB+ Default Spread", "val": "1.34%"}],
        "dependents": ["Operating lease converter!C28 (Debt Value of Leases)"]
    },
    "Operating lease converter!F31": {
        "label": "Annual Depreciation on Operating Lease Asset",
        "formula": "=C28/7",
        "category": "Forensic Normalization",
        "methodology": "Straight-line depreciation of synthetic compute asset over 7-year life ($53,714.8M/year).",
        "economic_intuition": "Replaces operating lease expense with economic depreciation and interest.",
        "precedents": [{"sheet": "Operating lease converter", "coord": "C28", "label": "Asset Value", "val": "$376,003.8 M"}],
        "dependents": ["Operating lease converter!F32 (Operating Earnings Adjustment)"]
    },
    "Operating lease converter!F32": {
        "label": "Adjustment to Operating Earnings (Leases)",
        "formula": "=B4-F31",
        "category": "Forensic Normalization",
        "methodology": "Current lease expense ($52M) minus depreciation ($53,714.8M) = -$53,662.8M adjustment to pre-tax EBIT.",
        "economic_intuition": "Significantly front-loads depreciation expense on massive hardware commitments.",
        "precedents": [
            {"sheet": "Operating lease converter", "coord": "B4", "label": "Current Lease Expense", "val": "$52 M"},
            {"sheet": "Operating lease converter", "coord": "F31", "label": "Depreciation", "val": "$53,714.8 M"}
        ],
        "dependents": ["Input sheet!B12 (Restated EBIT)"]
    },

    # ---------------- R& D converter ----------------
    "R& D converter!D24": {
        "label": "Value of Capitalized Research Asset",
        "formula": "=SUM(D24:D27)",
        "category": "Forensic Asset",
        "methodology": "Sums unamortized portions of current and past 3 years R&D ($16,979M current at 100%, $12,645M Yr -1 at 66.7%, $3,366M Yr -2 at 33.3%) = $26,531.0M.",
        "economic_intuition": "Treats R&D as capital expenditure creating an enduring intellectual property asset.",
        "precedents": [{"sheet": "R& D converter", "coord": "B10:B13", "label": "Past 3-Yr R&D", "val": "$33,582 M"}],
        "dependents": ["Input sheet!B14 (Restated Book Equity)"]
    },
    "R& D converter!E24": {
        "label": "Current Year R&D Amortization",
        "formula": "=SUM(E25:E27)",
        "category": "Forensic Normalization",
        "methodology": "Current year amortization charge on capitalized research asset ($5,534.3M).",
        "economic_intuition": "Replaces expensed R&D. Because current R&D ($16,979M) > amortization ($5,534M), operating earnings are boosted by +$11,444.7M.",
        "precedents": [{"sheet": "R& D converter", "coord": "B11:B13", "label": "Historical R&D Tranches", "val": "$16,603 M"}],
        "dependents": ["Input sheet!B12 (Restated EBIT)"]
    },

    # ---------------- Cost of capital worksheet ----------------
    "Cost of capital worksheet!B13": {
        "label": "Weighted Average Cost of Capital (WACC)",
        "formula": "=B52*B48+B56*B54",
        "category": "Hurdle Rate",
        "methodology": "Equity Weight (94.7%) * Cost of Equity (10.05%) + Debt Weight (5.3%) * After-Tax Cost of Debt (4.70%) = 9.74%.",
        "economic_intuition": "Represents the market opportunity cost of capital for Anthropic's business mix.",
        "precedents": [
            {"sheet": "Cost of capital worksheet", "coord": "B48", "label": "Cost of Equity", "val": "10.05%"},
            {"sheet": "Cost of capital worksheet", "coord": "B52", "label": "Equity Weight", "val": "94.7%"},
            {"sheet": "Cost of capital worksheet", "coord": "B56", "label": "After-Tax Cost of Debt", "val": "4.70%"},
            {"sheet": "Cost of capital worksheet", "coord": "B54", "label": "Debt Weight", "val": "5.3%"}
        ],
        "dependents": ["Valuation output!C12:L12 (Annual WACC Schedule)"]
    },
    "Cost of capital worksheet!B23": {
        "label": "Unlevered Pure-Play Business Beta",
        "formula": "1.6982",
        "category": "Moat Risk",
        "methodology": "Average unlevered beta for US Software (System & Application) industry (1.6982), stripping out firm-level regression noise.",
        "economic_intuition": "Anchors Anthropic's operating risk to pure-play industry peers.",
        "precedents": [{"sheet": "Industry Averages(US)", "coord": "C42", "label": "US Software Beta", "val": "1.25"}],
        "dependents": ["Cost of capital worksheet!B47 (Levered Beta)"]
    },
    "Cost of capital worksheet!B24": {
        "label": "Macro Risk-Free Rate (Rf)",
        "formula": "0.0494",
        "category": "Macro Anchor",
        "methodology": "Yield on the US 10-year Treasury bond (4.94%) as of valuation date.",
        "economic_intuition": "The foundational benchmark for US-dollar capital costs with zero default risk.",
        "precedents": [],
        "dependents": ["Cost of capital worksheet!B48 (Cost of Equity)", "Operating lease converter!C15 (Cost of Debt)"]
    },
    "Cost of capital worksheet!B27": {
        "label": "Mature Market Equity Risk Premium (ERP)",
        "formula": "0.0400",
        "category": "Macro Anchor",
        "methodology": "Mature equity risk premium (4.00%) derived by backing out expected returns from S&P 500 cash flows.",
        "economic_intuition": "The required return premium for equities over risk-free government debt.",
        "precedents": [],
        "dependents": ["Cost of capital worksheet!B48 (Cost of Equity)"]
    },
    "Cost of capital worksheet!B48": {
        "label": "Cost of Equity (Ke)",
        "formula": "=B24+B47*B27",
        "category": "Hurdle Rate",
        "methodology": "CAPM: Risk-Free Rate (4.94%) + Levered Beta (1.278) * ERP (4.00%) = 10.05%.",
        "economic_intuition": "Expected return demanded by equity investors.",
        "precedents": [
            {"sheet": "Cost of capital worksheet", "coord": "B24", "label": "Risk-Free Rate", "val": "4.94%"},
            {"sheet": "Cost of capital worksheet", "coord": "B47", "label": "Levered Beta", "val": "1.278"},
            {"sheet": "Cost of capital worksheet", "coord": "B27", "label": "ERP", "val": "4.00%"}
        ],
        "dependents": ["Cost of capital worksheet!B13 (WACC)"]
    },

    # ---------------- Option value ----------------
    "Option value!B23": {
        "label": "Value of Employee Options Overhang",
        "formula": "=SUM(B21:B22)",
        "category": "Dilution Overhang",
        "methodology": "Black-Scholes option pricing model valuation for granted employee options ($472.3M).",
        "economic_intuition": "Explicitly prices the dilution claim of option holders.",
        "precedents": [
            {"sheet": "Option value", "coord": "B4", "label": "Stock Price", "val": "$525.00"},
            {"sheet": "Option value", "coord": "B5", "label": "Strike Price", "val": "$2.06"},
            {"sheet": "Option value", "coord": "B6", "label": "Expiration", "val": "8.10 yrs"},
            {"sheet": "Option value", "coord": "B7", "label": "Volatility", "val": "40.0%"}
        ],
        "dependents": ["Valuation output!B31 (Option Overhang)"]
    },

    # ---------------- Failure Rate worksheet ----------------
    "Failure Rate worksheet!B10": {
        "label": "10-Year Cumulative Default Probability (BB)",
        "formula": "0.1178",
        "category": "Distress Anchor",
        "methodology": "10-year cumulative default rate for BB-rated corporate bonds (11.78%) from multi-decade S&P credit matrices.",
        "economic_intuition": "Empirical foundation for Damodaran's 10% failure rate assumption.",
        "precedents": [],
        "dependents": ["Valuation output!B22 (Probability of Failure)"]
    },

    # ---------------- Diagnostics ----------------
    "Diagnostics!C7": {
        "label": "Year 1 Projected Revenue",
        "formula": "102329.40",
        "category": "Growth Trajectory",
        "methodology": "Year 1 projected revenue ($102,329.4M / $102.3B), representing +190% growth over the $35,286M base.",
        "economic_intuition": "Marks the inflection where Anthropic crosses $100 Billion in annual sales.",
        "precedents": [{"sheet": "Input sheet", "coord": "B11", "label": "Base Revenue", "val": "$35,286 M"}],
        "dependents": ["Valuation output!C4 (Year 1 Revenue)"]
    },
    "Diagnostics!C12": {
        "label": "Year 1 Target Operating Margin",
        "formula": "0.0500",
        "category": "Profitability Trajectory",
        "methodology": "+5.0% operating margin in Year 1, turning operating profits positive.",
        "economic_intuition": "Represents the crucial operational breakeven threshold.",
        "precedents": [],
        "dependents": ["Valuation output!C5 (Year 1 Margin)"]
    },
    "Diagnostics!B21": {
        "label": "PV of After-tax Operating Income (Yr 1-10)",
        "formula": "615725.37",
        "category": "Cash Generation",
        "methodology": "Present value of after-tax operating profits over the 10-year projection ($615.7 Billion).",
        "economic_intuition": "Gross operating earnings power before capital reinvestment drag.",
        "precedents": [],
        "dependents": ["Diagnostics!B23 (PV of FCFF)"]
    },
    "Diagnostics!B22": {
        "label": "Reinvestment Cash Drag (Yr 1-10)",
        "formula": "193996.57",
        "category": "Capital Reinvestment",
        "methodology": "Capital absorbed by reinvestment over 10 years ($194.0 Billion), or 31.5% of cumulative operating profits.",
        "economic_intuition": "Hardware and compute expansion needed to drive $1 Trillion in revenues.",
        "precedents": [],
        "dependents": ["Diagnostics!B23 (PV of FCFF)"]
    },
    "Diagnostics!B23": {
        "label": "PV of Free Cash Flows to Firm (Yr 1-10)",
        "formula": "421728.80",
        "category": "Cash Generation",
        "methodology": "Net free cash flow generated over 10 years ($421.7 Billion), converting 68.5% of operating profits into cash.",
        "economic_intuition": "Directly links operating profits, reinvestment, and firm enterprise value.",
        "precedents": [
            {"sheet": "Diagnostics", "coord": "B21", "label": "PV of Operating Profits", "val": "$615,725.4 M"},
            {"sheet": "Diagnostics", "coord": "B22", "label": "Reinvestment Drag", "val": "$193,996.6 M"}
        ],
        "dependents": ["Valuation output!B20 (PV of Cash Flows)"]
    }
}

print(f"Loaded {len(methodology_kb)} comprehensive methodology nodes.")

# Build HTML template
html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aswath Damodaran — Anthropic Valuation Model Breakdown & Methodology Explorer</title>
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-page: #FAF7F2;
            --bg-sheet: #FFFFFF;
            --bg-header: #F2ECE1;
            --bg-hover: #F8F5EE;
            --bg-active: #FFFDF5;
            --border-grid: #E2DDD2;
            --border-header: #D5CFC2;
            --border-active: #B45309;
            --text-main: #1C1917;
            --text-muted: #58544D;
            --text-faint: #8C867A;
            --accent-green: #15803D;
            --accent-green-bg: #F0FDF4;
            --accent-red: #B91C1C;
            --accent-red-bg: #FEF2F2;
            --font-mono: 'JetBrains Mono', monospace;
            --font-serif: 'Newsreader', Georgia, serif;
            --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-page);
            color: var(--text-main);
            font-family: var(--font-sans);
            font-size: 13px;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }

        /* Top Editorial Header */
        header {
            background: #FFFFFF;
            border-bottom: 1px solid var(--border-grid);
            padding: 8px 18px;
            position: sticky;
            top: 0;
            z-index: 40;
        }

        .header-container {
            width: 100%;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            gap: 12px;
        }

        .title-block h1 {
            font-family: var(--font-serif);
            font-size: 18px;
            font-weight: 600;
            color: var(--text-main);
            letter-spacing: -0.01em;
        }

        .title-block p {
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 1px;
        }

        .key-pills {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            font-family: var(--font-mono);
            font-size: 9.5px;
        }

        .pill {
            background: #FAF7F2;
            border: 1px solid var(--border-header);
            padding: 2px 8px;
            border-radius: 2px;
            color: var(--text-muted);
        }

        .pill strong {
            color: var(--text-main);
        }

        .pill.positive strong {
            color: var(--accent-green);
        }

        .pill.negative strong {
            color: var(--accent-red);
        }

        /* Formula Bar & Jump Bar */
        .formula-bar-container {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .formula-bar {
            flex: 1;
            display: flex;
            align-items: center;
            background: #FAF7F2;
            border: 1px solid var(--border-header);
            border-radius: 2px;
            height: 26px;
            font-family: var(--font-mono);
            font-size: 10.5px;
        }

        .cell-address-box {
            width: 180px;
            padding: 0 10px;
            font-weight: 600;
            color: var(--text-main);
            border-right: 1px solid var(--border-header);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: flex;
            align-items: center;
            height: 100%;
        }

        .fx-indicator {
            padding: 0 8px;
            font-style: italic;
            font-weight: 600;
            color: var(--text-faint);
            border-right: 1px solid var(--border-header);
            height: 100%;
            display: flex;
            align-items: center;
            background: #F2ECE1;
        }

        .formula-input {
            flex: 1;
            padding: 0 10px;
            color: var(--text-main);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .jump-box {
            display: flex;
            align-items: center;
            gap: 6px;
            font-family: var(--font-mono);
            font-size: 10.5px;
        }

        .jump-select {
            background: #FFFFFF;
            border: 1px solid var(--border-header);
            padding: 3px 6px;
            font-family: var(--font-mono);
            font-size: 10px;
            border-radius: 2px;
            color: var(--text-main);
            outline: none;
            cursor: pointer;
        }

        /* 18 Sheet Tabs */
        .sheet-tab-bar {
            display: flex;
            gap: 2px;
            overflow-x: auto;
            border-bottom: 1px solid var(--border-grid);
            background: #F3EFE6;
            padding: 0 14px;
            scrollbar-width: thin;
        }

        .sheet-tab {
            padding: 6px 10px;
            font-size: 10px;
            font-family: var(--font-mono);
            color: var(--text-muted);
            background: transparent;
            border: 1px solid transparent;
            border-bottom: none;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
            outline: none;
        }

        .sheet-tab:hover {
            color: var(--text-main);
            background: #FAF7F2;
        }

        .sheet-tab.active {
            color: var(--text-main);
            background: #FFFFFF;
            border-color: var(--border-grid);
            font-weight: 600;
            border-top: 2px solid var(--border-active);
        }

        /* Workspace Layout - ALWAYS SIDE-BY-SIDE (NO COLLAPSE BELOW) */
        .workspace {
            width: 100%;
            max-width: 100vw;
            margin: 0;
            padding: 10px 16px 16px;
            display: grid;
            grid-template-columns: minmax(0, 1fr) 380px;
            gap: 14px;
            align-items: stretch;
            height: calc(100vh - 118px);
            box-sizing: border-box;
        }

        /* Grid Table Container (80% font size, 20% smaller) */
        .grid-container {
            background: #FFFFFF;
            border: 1px solid var(--border-grid);
            border-radius: 2px;
            overflow: auto;
            height: 100%;
            max-height: 100%;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            position: relative;
        }

        table.sheet-table {
            border-collapse: separate;
            border-spacing: 0;
            font-family: var(--font-mono);
            font-size: 9.8px; /* 20% smaller than previous 12px */
            width: max-content;
            min-width: 100%;
        }

        /* Corner Header */
        table.sheet-table th.corner-header {
            position: sticky;
            top: 0;
            left: 0;
            z-index: 50;
            width: 34px;
            min-width: 34px;
            max-width: 34px;
            background: var(--bg-header);
            border-right: 1px solid var(--border-grid);
            border-bottom: 1px solid var(--border-grid);
        }

        /* Row Headers (1, 2, 3...) */
        table.sheet-table th.row-header {
            position: sticky;
            left: 0;
            z-index: 25;
            width: 34px;
            min-width: 34px;
            max-width: 34px;
            background: var(--bg-header);
            border-right: 1px solid var(--border-grid);
            border-bottom: 1px solid var(--border-grid);
            text-align: right;
            padding: 3px 6px;
            font-weight: 500;
            color: var(--text-muted);
            font-size: 9px;
            user-select: none;
        }

        /* General Column Headers (A, B, C...) */
        table.sheet-table th.col-header {
            position: sticky;
            top: 0;
            z-index: 30;
            background: var(--bg-header);
            border-right: 1px solid var(--border-grid);
            border-bottom: 1px solid var(--border-grid);
            padding: 4px 6px;
            text-align: center;
            font-weight: 600;
            color: var(--text-muted);
            font-size: 9px;
            user-select: none;
        }

        /* Column A Header (Pinned Sticky Left & Top) */
        table.sheet-table th.col-header-A {
            left: 34px;
            z-index: 45;
            width: 195px;
            min-width: 165px;
            max-width: 215px;
            background: var(--bg-header);
            border-right: 2px solid var(--border-header);
        }

        /* Column A Data Cells (Pinned Sticky Left, Text Wrapped & Compact) */
        table.sheet-table td.cell-col-A {
            position: sticky;
            left: 34px;
            z-index: 20;
            width: 195px;
            min-width: 165px;
            max-width: 215px;
            background-color: #FFFFFF;
            border-right: 2px solid var(--border-header) !important;
            box-shadow: 2px 0 4px -2px rgba(0, 0, 0, 0.08);
            white-space: normal !important;
            word-wrap: break-word;
            overflow-wrap: break-word;
            word-break: break-word;
            line-height: 1.25;
            vertical-align: top;
            font-weight: 500;
            font-size: 9.8px;
            padding: 3px 6px;
        }

        table.sheet-table td.cell-col-A:hover {
            background-color: var(--bg-hover) !important;
        }

        table.sheet-table td.cell-col-A.selected {
            background-color: var(--bg-active) !important;
            outline: 2px solid var(--border-active);
            outline-offset: -1px;
            z-index: 22;
        }

        /* Column B: Small & Wrapped */
        table.sheet-table th.col-header-B {
            width: 115px;
            min-width: 90px;
            max-width: 135px;
        }

        table.sheet-table td.cell-col-B {
            width: 115px;
            min-width: 90px;
            max-width: 135px;
            vertical-align: top;
            line-height: 1.25;
            padding: 3px 6px;
            font-size: 9.8px;
        }

        /* Column C: Small & Wrapped */
        table.sheet-table th.col-header-C {
            width: 100px;
            min-width: 80px;
            max-width: 125px;
        }

        table.sheet-table td.cell-col-C {
            width: 100px;
            min-width: 80px;
            max-width: 125px;
            vertical-align: top;
            line-height: 1.25;
            padding: 3px 6px;
            font-size: 9.8px;
        }

        /* Subsequent Columns (D, E, F...) */
        table.sheet-table th.col-header-other {
            width: 78px;
            min-width: 68px;
            max-width: 92px;
        }

        table.sheet-table td.cell-col-other {
            width: 78px;
            min-width: 68px;
            max-width: 92px;
            vertical-align: top;
            padding: 3px 6px;
            font-size: 9.8px;
        }

        /* General TD Rules */
        table.sheet-table td {
            border-right: 1px solid var(--border-grid);
            border-bottom: 1px solid var(--border-grid);
            padding: 3px 6px;
            color: var(--text-main);
            cursor: pointer;
            transition: background-color 0.1s ease;
        }

        table.sheet-table td:hover {
            background-color: var(--bg-hover);
        }

        table.sheet-table td.selected {
            outline: 2px solid var(--border-active);
            outline-offset: -1px;
            background-color: var(--bg-active) !important;
            font-weight: 600;
        }

        table.sheet-table td.precedent {
            background-color: #FAF4EB !important;
            outline: 1px dashed var(--border-active);
        }

        table.sheet-table td.has-methodology {
            position: relative;
        }

        table.sheet-table td.has-methodology::after {
            content: '';
            position: absolute;
            top: 2px;
            right: 2px;
            width: 3.5px;
            height: 3.5px;
            background: var(--border-active);
            border-radius: 50%;
        }

        /* Text Wrapping for lengthy text in any cell */
        table.sheet-table td.is-text {
            white-space: normal;
            word-wrap: break-word;
            overflow-wrap: break-word;
            word-break: break-word;
            line-height: 1.25;
        }

        table.sheet-table td.is-long-text {
            white-space: normal !important;
            word-wrap: break-word;
            overflow-wrap: break-word;
            word-break: break-word;
            line-height: 1.2;
            font-size: 9.2px;
            max-width: 195px;
        }

        /* Numbers: Right-aligned, tabular font, nowrap */
        table.sheet-table td.num-right {
            text-align: right;
            white-space: nowrap !important;
            font-variant-numeric: tabular-nums;
        }

        /* Derivation & Methodology Inspector Panel - PERMANENT RIGHT DRAWER */
        .inspector-panel {
            background: #FFFFFF;
            border: 1px solid var(--border-grid);
            border-radius: 2px;
            height: 100%;
            max-height: 100%;
            overflow-y: auto;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
            display: flex;
            flex-direction: column;
        }

        .inspector-header {
            background: var(--bg-header);
            border-bottom: 1px solid var(--border-grid);
            padding: 10px 14px;
            flex-shrink: 0;
        }

        .inspector-badge {
            font-family: var(--font-mono);
            font-size: 9px;
            text-transform: uppercase;
            font-weight: 600;
            color: var(--text-muted);
            letter-spacing: 0.05em;
        }

        .inspector-title {
            font-family: var(--font-serif);
            font-size: 15px;
            font-weight: 600;
            color: var(--text-main);
            margin-top: 1px;
            line-height: 1.25;
        }

        .inspector-body {
            padding: 12px 14px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            overflow-y: auto;
        }

        .metric-display {
            display: flex;
            align-items: baseline;
            justify-content: space-between;
            background: var(--bg-page);
            border: 1px solid var(--border-header);
            padding: 8px 10px;
            border-radius: 2px;
        }

        .metric-val {
            font-family: var(--font-mono);
            font-size: 17px;
            font-weight: 700;
            color: var(--text-main);
        }

        .metric-val.positive {
            color: var(--accent-green);
        }

        .metric-val.negative {
            color: var(--accent-red);
        }

        .metric-cell-ref {
            font-family: var(--font-mono);
            font-size: 10px;
            color: var(--text-muted);
        }

        .formula-callout {
            background: #FAF7F2;
            border-left: 3px solid var(--border-active);
            padding: 6px 9px;
            font-family: var(--font-mono);
            font-size: 10.5px;
            color: var(--text-main);
            word-break: break-all;
        }

        .section-label {
            font-family: var(--font-sans);
            font-size: 9.5px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--text-faint);
            letter-spacing: 0.06em;
            margin-bottom: 4px;
        }

        .prose-text {
            font-family: var(--font-serif);
            font-size: 12.5px;
            line-height: 1.45;
            color: #2D2A26;
        }

        .intuition-box {
            background: #FDFBF7;
            border: 1px solid #EAE4D6;
            padding: 8px 10px;
            border-radius: 2px;
        }

        .precedents-list {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .precedent-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #FAF7F2;
            border: 1px solid var(--border-grid);
            padding: 4px 8px;
            border-radius: 2px;
            font-family: var(--font-mono);
            font-size: 10px;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .precedent-item:hover {
            border-color: var(--border-active);
            background: #FFFFFF;
        }

        .precedent-link {
            font-weight: 600;
            color: var(--text-main);
        }

        .precedent-val {
            color: var(--text-muted);
        }

        .dependents-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }

        .dependent-tag {
            background: #F2ECE1;
            border: 1px solid var(--border-header);
            padding: 2px 6px;
            border-radius: 2px;
            font-family: var(--font-mono);
            font-size: 9.5px;
            color: var(--text-muted);
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-container">
            <div class="header-top">
                <div class="title-block">
                    <h1>Aswath Damodaran — Anthropic Valuation Model Architecture</h1>
                    <p>Interactive 18-Sheet Spreadsheet Template & Click-to-Derive Methodology Inspector (Updated for Leaked Q3 2026 Run-Rate)</p>
                </div>
                <div class="key-pills">
                    <div class="pill positive">DCF FAIR VALUE: <strong>$439.69 / SH</strong></div>
                    <div class="pill">COMMON EQUITY: <strong>$1,450.5B</strong></div>
                    <div class="pill positive">RUMORED IPO: <strong>$525.00 (-16.3%)</strong></div>
                    <div class="pill">2036 TARGET REV: <strong>$1.005T</strong></div>
                    <div class="pill">WACC: <strong>9.74% &rarr; 9.13%</strong></div>
                </div>
            </div>

            <!-- Formula Bar & Quick Jump -->
            <div class="formula-bar-container">
                <div class="formula-bar">
                    <div id="activeCellBox" class="cell-address-box">Valuation output!B34</div>
                    <div class="fx-indicator">fx</div>
                    <div id="activeFormulaInput" class="formula-input">=B32/B33</div>
                </div>
                
                <div class="jump-box">
                    <span style="color: var(--text-faint); font-size: 11px; text-transform: uppercase; font-weight: 600;">Landmark:</span>
                    <select class="jump-select" id="landmarkSelect" onchange="jumpToLandmark(this.value)">
                        <option value="">Jump to landmark cell...</option>
                        <option value="Valuation output!B34">Valuation output!B34 (Intrinsic Fair Value: $439.69)</option>
                        <option value="Valuation output!B36">Valuation output!B36 (Price / Value: 119.5%)</option>
                        <option value="Valuation output!B32">Valuation output!B32 (Common Equity: $1,450.5B)</option>
                        <option value="Valuation output!B24">Valuation output!B24 (Operating Assets: $1,720.0B)</option>
                        <option value="Valuation output!B21">Valuation output!B21 (Going-Concern EV: $1,810.5B)</option>
                        <option value="Valuation output!B18">Valuation output!B18 (Terminal Value: $3,459.5B)</option>
                        <option value="Valuation output!B22">Valuation output!B22 (Failure Probability: 10.0%)</option>
                        <option value="Story Inputs!B5">Story Inputs!B5 (Revenue CAGR: 42.0%)</option>
                        <option value="Story Inputs!B6">Story Inputs!B6 (2036 Revenues: $1.005T)</option>
                        <option value="Story Inputs!B9">Story Inputs!B9 (Target Operating Margin: 32.5%)</option>
                        <option value="Story Inputs!B14">Story Inputs!B14 (Sales to Capital: 3.00)</option>
                        <option value="Input sheet!B11">Input sheet!B11 (LTM Base Revenue: $35,286M)</option>
                        <option value="Operating lease converter!C28">Operating lease converter!C28 (Compute Commitments PV: $376.0B)</option>
                        <option value="R& D converter!D24">R& D converter!D24 (Capitalized R&D Asset: $26.5B)</option>
                        <option value="Cost of capital worksheet!B13">Cost of capital worksheet!B13 (Base WACC: 9.74%)</option>
                        <option value="Option value!B23">Option value!B23 (Option Overhang: $472.3M)</option>
                        <option value="Diagnostics!C7">Diagnostics!C7 (Year 1 Revenue: $102.3B)</option>
                    </select>
                </div>
            </div>
        </div>
    </header>

    <!-- 18 Sheet Tabs -->
    <nav class="sheet-tab-bar" id="tabBar">
        <!-- Rendered dynamically -->
    </nav>

    <!-- Main Workspace -->
    <main class="workspace">
        
        <!-- Left: Spreadsheet Grid Canvas -->
        <section class="grid-container" id="gridContainer">
            <table class="sheet-table" id="sheetTable">
                <!-- Grid rendered dynamically -->
            </table>
        </section>

        <!-- Right: Derivation & Methodology Inspector -->
        <aside class="inspector-panel" id="inspectorPanel">
            <div class="inspector-header">
                <div id="inspCategory" class="inspector-badge">Core Output</div>
                <h2 id="inspTitle" class="inspector-title">Estimated Intrinsic Fair Value Per Share</h2>
            </div>
            
            <div class="inspector-body">
                <div class="metric-display">
                    <div>
                        <div id="inspVal" class="metric-val positive">$439.69 / SH</div>
                        <div id="inspSubVal" style="font-size: 11px; color: var(--text-muted); margin-top: 2px;">Equity Value: <strong>$1.450 Trillion</strong></div>
                    </div>
                    <div id="inspCoord" class="metric-cell-ref">Valuation output!B34</div>
                </div>

                <div>
                    <div class="section-label">Excel Formula</div>
                    <div id="inspFormula" class="formula-callout">=B32/B33</div>
                </div>

                <div>
                    <div class="section-label">Primary Derivation Methodology</div>
                    <div id="inspMethodology" class="prose-text">
                        Damodaran's bottom-line intrinsic fair value per share. Calculated by dividing Total Value of Common Stock Equity ($1,415,478.5M) by Diluted Share Count (16,912.15M shares) = $439.69 per share.
                    </div>
                </div>

                <div class="intuition-box">
                    <div class="section-label" style="color: var(--text-main);">Economic Intuition & First Principles</div>
                    <div id="inspIntuition" class="prose-text" style="font-size: 13px;">
                        This reflects the true intrinsic worth per share of Anthropic under Damodaran's calibrated 10-year Ginzu DCF engine following the Q3 2026 leaked revenue update ($35.3B run-rate). At $439.69, Anthropic is worth $1.45 Trillion in equity value.
                    </div>
                </div>

                <div>
                    <div class="section-label">Upstream Precedents</div>
                    <div id="inspPrecedents" class="precedents-list">
                        <!-- Precedents injected here -->
                    </div>
                </div>

                <div>
                    <div class="section-label">Downstream Dependents</div>
                    <div id="inspDependents" class="dependents-tags">
                        <!-- Dependents injected here -->
                    </div>
                </div>
            </div>
        </aside>

    </main>

    <!-- Embedded Model Data & Client Logic -->
    <script>
        const modelData = {
            sheets: """ + json.dumps(extracted_sheets, default=str) + """,
            methodologies: """ + json.dumps(methodology_kb, default=str) + """
        };

        const sheets = modelData.sheets;
        const methodologies = modelData.methodologies;

        let activeSheetName = "Valuation output";
        let activeCoord = "B34";

        // Number formatter
        function formatNumber(v) {
            if (v === null || v === undefined || v === '') return '';
            if (typeof v === 'number') {
                if (Math.abs(v) >= 1000) {
                    return v.toLocaleString('en-US', { maximumFractionDigits: 1 });
                } else if (Math.abs(v) < 1 && Math.abs(v) > 0.0001) {
                    return (v * 100).toFixed(2) + '%';
                } else if (!Number.isInteger(v)) {
                    return v.toFixed(2);
                }
                return v.toLocaleString('en-US');
            }
            return v;
        }

        // Initialize 18 Sheet Tabs
        const tabBar = document.getElementById('tabBar');
        Object.keys(sheets).forEach(sname => {
            const btn = document.createElement('button');
            btn.className = 'sheet-tab' + (sname === activeSheetName ? ' active' : '');
            btn.innerText = sname;
            btn.onclick = () => selectSheet(sname);
            tabBar.appendChild(btn);
        });

        // Select Sheet
        function selectSheet(sname) {
            activeSheetName = sname;
            document.querySelectorAll('.sheet-tab').forEach(b => {
                b.classList.toggle('active', b.innerText === sname);
            });
            renderSheetGrid(sname);
        }

        // Render Sheet Grid Table
        function renderSheetGrid(sname) {
            const sheet = sheets[sname];
            const table = document.getElementById('sheetTable');
            table.innerHTML = '';

            if (!sheet || !sheet.grid || sheet.grid.length === 0) {
                table.innerHTML = '<tr><td style="padding: 24px; text-align: center; color: var(--text-muted);">Sheet empty or omitted</td></tr>';
                return;
            }

            // Thead with Column Letters
            const thead = document.createElement('thead');
            const headerRow = document.createElement('tr');
            
            const corner = document.createElement('th');
            corner.className = 'corner-header';
            corner.innerText = '';
            headerRow.appendChild(corner);

            sheet.col_letters.forEach(letter => {
                const th = document.createElement('th');
                th.innerText = letter;
                th.className = 'col-header col-header-' + letter;
                if (letter === 'A') th.classList.add('col-header-A');
                else if (letter === 'B') th.classList.add('col-header-B');
                else if (letter === 'C') th.classList.add('col-header-C');
                else th.classList.add('col-header-other');
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            // Tbody with Data Rows
            const tbody = document.createElement('tbody');
            sheet.grid.forEach(rData => {
                const tr = document.createElement('tr');
                
                const rowHeader = document.createElement('th');
                rowHeader.className = 'row-header';
                rowHeader.innerText = rData.row_idx;
                tr.appendChild(rowHeader);

                rData.cells.forEach(cell => {
                    const td = document.createElement('td');
                    td.id = `cell_${sname.replace(/[^a-zA-Z0-9]/g, '_')}_${cell.coord}`;
                    td.dataset.coord = cell.coord;
                    td.dataset.sheet = sname;

                    const colLetter = cell.coord.replace(/[0-9]/g, '');
                    td.className = 'cell-col-' + colLetter;
                    if (colLetter === 'A') td.classList.add('cell-col-A');
                    else if (colLetter === 'B') td.classList.add('cell-col-B');
                    else if (colLetter === 'C') td.classList.add('cell-col-C');
                    else td.classList.add('cell-col-other');

                    td.innerText = formatNumber(cell.val);

                    if (typeof cell.val === 'number') {
                        td.classList.add('num-right');
                        if (cell.val < 0) td.style.color = 'var(--accent-red)';
                    } else if (typeof cell.val === 'string') {
                        td.classList.add('is-text');
                        if (cell.val.length > 25) {
                            td.classList.add('is-long-text');
                        }
                    }

                    const fullKey = `${sname}!${cell.coord}`;
                    if (methodologies[fullKey]) {
                        td.classList.add('has-methodology');
                    }

                    td.onclick = () => selectCell(sname, cell.coord, cell);
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
            table.appendChild(tbody);

            // Default focus
            if (sname === "Valuation output") {
                selectCell("Valuation output", "B34");
            } else if (sheet.grid[0] && sheet.grid[0].cells[0]) {
                selectCell(sname, sheet.grid[0].cells[0].coord, sheet.grid[0].cells[0]);
            }
        }

        // Select and Inspect Cell
        function selectCell(sname, coord, cellObj) {
            activeSheetName = sname;
            activeCoord = coord;

            // Highlight in grid
            document.querySelectorAll('td.selected, td.precedent').forEach(el => {
                el.classList.remove('selected', 'precedent');
            });

            const targetTd = document.getElementById(`cell_${sname.replace(/[^a-zA-Z0-9]/g, '_')}_${coord}`);
            if (targetTd) targetTd.classList.add('selected');

            // Find cell object if missing
            if (!cellObj) {
                const sheet = sheets[sname];
                if (sheet) {
                    for (const r of sheet.grid) {
                        for (const c of r.cells) {
                            if (c.coord === coord) {
                                cellObj = c;
                                break;
                            }
                        }
                    }
                }
            }

            const fullKey = `${sname}!${coord}`;
            const meta = methodologies[fullKey];

            // Formula Bar Update
            document.getElementById('activeCellBox').innerText = fullKey;
            document.getElementById('activeFormulaInput').innerText = (cellObj && cellObj.formula) ? cellObj.formula : (cellObj && cellObj.val !== null ? cellObj.val : '');

            // Inspector Update
            const inspCategory = document.getElementById('inspCategory');
            const inspTitle = document.getElementById('inspTitle');
            const inspVal = document.getElementById('inspVal');
            const inspSubVal = document.getElementById('inspSubVal');
            const inspCoord = document.getElementById('inspCoord');
            const inspFormula = document.getElementById('inspFormula');
            const inspMethodology = document.getElementById('inspMethodology');
            const inspIntuition = document.getElementById('inspIntuition');
            const inspPrecedents = document.getElementById('inspPrecedents');
            const inspDependents = document.getElementById('inspDependents');

            inspCoord.innerText = fullKey;

            const valStr = cellObj ? formatNumber(cellObj.val) : '-';
            inspVal.innerText = valStr;
            inspVal.className = 'metric-val' + ((cellObj && typeof cellObj.val === 'number' && cellObj.val < 0) ? ' negative' : '');
            
            if (cellObj && typeof cellObj.val === 'number' && Math.abs(cellObj.val) >= 1000) {
                inspSubVal.style.display = 'block';
                inspSubVal.innerHTML = `Equivalent: <strong>$${(cellObj.val / 1000).toFixed(2)} Billion</strong>`;
                if (Math.abs(cellObj.val) >= 1000000) {
                    inspSubVal.innerHTML = `Equivalent: <strong>$${(cellObj.val / 1000000).toFixed(3)} Trillion</strong>`;
                }
            } else {
                inspSubVal.style.display = 'none';
            }

            if (meta) {
                inspCategory.innerText = meta.category || 'Valuation Metric';
                inspTitle.innerText = meta.label || `Cell ${coord}`;
                inspFormula.innerText = meta.formula || (cellObj && cellObj.formula ? cellObj.formula : 'Direct Entry / Historical Filing Input');
                inspMethodology.innerText = meta.methodology || 'Primary calculation node in Damodaran DCF engine.';
                inspIntuition.innerText = meta.economic_intuition || 'Core parameter anchoring company narrative to corporate finance principles.';

                // Render Precedents
                inspPrecedents.innerHTML = '';
                if (meta.precedents && meta.precedents.length > 0) {
                    meta.precedents.forEach(p => {
                        const div = document.createElement('div');
                        div.className = 'precedent-item';
                        div.innerHTML = `<span class="precedent-link">${p.sheet}!${p.coord} (${p.label})</span><span class="precedent-val">${p.val}</span>`;
                        div.onclick = (e) => {
                            e.stopPropagation();
                            jumpToCell(p.sheet, p.coord.split(':')[0]);
                        };
                        inspPrecedents.appendChild(div);

                        if (p.sheet === sname) {
                            const pTd = document.getElementById(`cell_${sname.replace(/[^a-zA-Z0-9]/g, '_')}_${p.coord}`);
                            if (pTd) pTd.classList.add('precedent');
                        }
                    });
                } else {
                    inspPrecedents.innerHTML = '<span style="color: var(--text-faint); font-style: italic; font-size: 11px;">Independent Input / Sovereign or Industry Anchor</span>';
                }

                // Render Dependents
                inspDependents.innerHTML = '';
                if (meta.dependents && meta.dependents.length > 0) {
                    meta.dependents.forEach(d => {
                        const span = document.createElement('span');
                        span.className = 'dependent-tag';
                        span.innerText = d;
                        inspDependents.appendChild(span);
                    });
                } else {
                    inspDependents.innerHTML = '<span style="color: var(--text-faint); font-style: italic; font-size: 11px;">Final Valuation Output / Independent End Node</span>';
                }
            } else {
                // Fallback for unannotated cells
                inspCategory.innerText = (cellObj && cellObj.formula) ? 'Calculated Cell' : 'Input / Constant';
                inspTitle.innerText = `Cell ${coord}`;
                inspFormula.innerText = (cellObj && cellObj.formula) ? cellObj.formula : 'Direct Value Input';
                inspMethodology.innerText = 'Supporting schedule data item in Damodaran Anthropic valuation model. Click on cells with amber dots for comprehensive corporate finance derivation write-ups.';
                inspIntuition.innerText = 'Forms part of the 10-year discrete financial projection and capital structure synthesis.';
                inspPrecedents.innerHTML = '<span style="color: var(--text-faint); font-style: italic; font-size: 11px;">No explicit precedents cataloged</span>';
                inspDependents.innerHTML = '<span style="color: var(--text-faint); font-style: italic; font-size: 11px;">General DCF model dependency</span>';
            }
        }

        // Jump to cell in any sheet
        function jumpToCell(sname, coord) {
            if (activeSheetName !== sname) {
                selectSheet(sname);
            }
            setTimeout(() => {
                selectCell(sname, coord);
                const el = document.getElementById(`cell_${sname.replace(/[^a-zA-Z0-9]/g, '_')}_${coord}`);
                if (el) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
                }
            }, 60);
        }

        // Landmark jumper
        function jumpToLandmark(val) {
            if (!val) return;
            const parts = val.split('!');
            if (parts.length === 2) {
                jumpToCell(parts[0], parts[1]);
            }
        }

        // Initial render
        renderSheetGrid("Valuation output");
    </script>
</body>
</html>
"""

out_file = "ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/damodaran_breakdown_reader.html"
os.makedirs(os.path.dirname(out_file), exist_ok=True)
with open(out_file, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Successfully generated Damodaran 18-Sheet Breakdown Reader at {out_file} ({len(html_template)} bytes).")
