import os
import openpyxl
import json

excel_path = "ERVIS/projects/US_EQUITIES/ANTHROPIC/models/AnthropicIPO_updated.xlsx"
wb_vals = openpyxl.load_workbook(excel_path, data_only=True)
wb_forms = openpyxl.load_workbook(excel_path, data_only=False)

sheets_to_extract = [
    "Valuation output",
    "Story Inputs",
    "Input sheet",
    "Operating lease converter",
    "R& D converter",
    "Cost of capital worksheet",
    "Failure Rate worksheet",
    "Option value",
    "Synthetic rating",
    "Diagnostics",
    "Trailing 12 month Worskheet"
]

# Build column letter lookup
def col2letter(col_idx):
    res = ""
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        res = chr(65 + remainder) + res
    return res

# Extract sheets data
extracted_sheets = {}

for sname in sheets_to_extract:
    sv = wb_vals[sname]
    sf = wb_forms[sname]
    
    # Determine bounds
    max_r = min(sv.max_row, 45 if sname != "R& D converter" else 32)
    max_c = min(sv.max_column, 14)
    
    # Filter empty trailing rows/cols
    grid = []
    for r in range(1, max_r + 1):
        row_cells = []
        has_val = False
        for c in range(1, max_c + 1):
            val = sv.cell(r, c).value
            form = sf.cell(r, c).value
            
            coord = f"{col2letter(c)}{r}"
            formula_str = str(form) if form and str(form).startswith("=") else None
            
            # Formatting checks
            val_type = "text"
            if isinstance(val, (int, float)):
                val_type = "number"
            
            if val is not None or formula_str is not None:
                has_val = True
                
            row_cells.append({
                "coord": coord,
                "r": r,
                "c": c,
                "col_letter": col2letter(c),
                "val": val,
                "formula": formula_str,
                "type": val_type
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

print(f"Extracted {len(extracted_sheets)} sheets successfully.")

# Comprehensive Knowledge Base of Derivation Methodologies
methodology_kb = {
    # ---------------- Valuation output ----------------
    "Valuation output!B20": {
        "label": "PV of Discrete Cash Flows (Yr 1–10)",
        "formula": "=SUM(C14:L14)",
        "category": "Core Output",
        "methodology": "Damodaran uses a 10-year discrete forecast period for exponential growth tech companies before assuming mature stable growth. This cell sums the annual Free Cash Flows to the Firm (FCFF) discounted at the time-varying cost of capital from Year 1 through Year 10.",
        "economic_intuition": "Early-stage AI companies experience extreme hyper-growth and massive negative cash flows before reaching profitability. A standard 5-year model is too short to capture the transition from cash-burning GPU cluster ramp to high-margin inference software monetization.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "C14:L14", "label": "Annual PV of FCFF (Yr 1 to 10)", "val": "$421,728.8 M"}
        ],
        "dependents": ["Valuation output!B21 (Sum of PV)"]
    },
    "Valuation output!B19": {
        "label": "PV of Terminal Value",
        "formula": "=B18*L13",
        "category": "Core Output",
        "methodology": "Discounts the Terminal Value ($3,459.5B) calculated in Year 10 back to present value using the cumulative 10-year discount factor (0.4014).",
        "economic_intuition": "Represents 80.7% of Anthropic's total going-concern operating assets. In high-growth platform tech, the vast majority of economic value resides in the terminal steady-state cash generation rather than early transition years.",
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
        "methodology": "Applies the Gordon Growth Model perpetuity formula: TV = Terminal Cash Flow / (Terminal Cost of Capital - Terminal Growth Rate). Terminal growth is constrained to the 10-year risk-free rate of 4.90% to prevent the company from mathematically outgrowing the aggregate macroeconomy.",
        "economic_intuition": "A firm cannot grow faster than the economy in perpetuity without becoming the economy itself. Constraining g to the risk-free rate (4.90%) enforces macroeconomic consistency.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B16", "label": "Terminal Cash Flow", "val": "$146,337.7 M"},
            {"sheet": "Valuation output", "coord": "B17", "label": "Terminal Cost of Capital", "val": "9.13%"}
        ],
        "dependents": ["Valuation output!B19 (PV of Terminal Value)"]
    },
    "Valuation output!B21": {
        "label": "Sum of Present Values (Going Concern EV)",
        "formula": "=B19+B20",
        "category": "Core Output",
        "methodology": "Combines the present value of the 10-year discrete free cash flows ($421.7B) and the present value of the terminal value ($1,388.7B) to determine total unadjusted going-concern enterprise value.",
        "economic_intuition": "This reflects the intrinsic enterprise value of Anthropic under the sole assumption that it survives as a going concern in perpetuity without failure or distress liquidation.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B20", "label": "PV of 10-Yr Cash Flows", "val": "$421,728.8 M"},
            {"sheet": "Valuation output", "coord": "B19", "label": "PV of Terminal Value", "val": "$1,388,747.6 M"}
        ],
        "dependents": ["Valuation output!B24 (Value of Operating Assets)"]
    },
    "Valuation output!B22": {
        "label": "Probability of Failure",
        "formula": "=Story Inputs!B27",
        "category": "Risk Parameter",
        "methodology": "Anchored to the 10-year cumulative historical default probability for BB-rated corporate bonds from S&P and Moody's credit grids (11.78%), adjusted for Anthropic's multi-year cash cushion. Damodaran selects 10.0%.",
        "economic_intuition": "Default risk in money-losing growth companies must be severed from the going-concern WACC. A discount rate assumes infinite survival. Mortality risk is explicitly modeled as a discrete probability of distress.",
        "precedents": [
            {"sheet": "Failure Rate worksheet", "coord": "B10", "label": "10-Yr Cumulative BB Default Rate", "val": "11.78%"},
            {"sheet": "Story Inputs", "coord": "B27", "label": "Selected Failure Probability", "val": "10.0%"}
        ],
        "dependents": ["Valuation output!B24 (Value of Operating Assets)"]
    },
    "Valuation output!B23": {
        "label": "Proceeds if Firm Fails (Distress Salvage)",
        "formula": "=0.5*B21",
        "category": "Risk Parameter",
        "methodology": "Estimates the recovery proceeds realized in distress liquidation as 50% of going-concern enterprise value ($905.2B). Reflects salvage value of proprietary model weights, software IP, trained checkpoints, and customer accounts in a fire-sale.",
        "economic_intuition": "Even if Anthropic defaults on hardware commitments, its intellectual property, enterprise customer base, and Claude code retain substantial asset value for acquirers (e.g. hyperscalers).",
        "precedents": [{"sheet": "Valuation output", "coord": "B21", "label": "Going Concern Sum of PV", "val": "$1,810,476.4 M"}],
        "dependents": ["Valuation output!B24 (Value of Operating Assets)"]
    },
    "Valuation output!B24": {
        "label": "Value of Operating Assets (Distress-Adjusted EV)",
        "formula": "=B21*(1-B22)+B23*B22",
        "category": "Core Output",
        "methodology": "Weighting going-concern value (90%) and distress liquidation proceeds (10%). Equation: Operating Assets = Sum of PV * (1 - P_fail) + P_fail * Proceeds. Takes an explicit $90.5B haircut (-5.3%) off operating assets.",
        "economic_intuition": "This is Damodaran's signature mechanism for pricing mortality risk without artificially distorting the cost of capital.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B21", "label": "Going Concern Sum of PV", "val": "$1,810,476.4 M"},
            {"sheet": "Valuation output", "coord": "B22", "label": "Probability of Failure", "val": "10.0%"},
            {"sheet": "Valuation output", "coord": "B23", "label": "Distress Proceeds", "val": "$905,238.2 M"}
        ],
        "dependents": ["Valuation output!B30 (Value of Equity)"]
    },
    "Valuation output!B25": {
        "label": "Total Debt (Reported + Capitalized Compute)",
        "formula": "=Input sheet!B15+Operating lease converter!C28",
        "category": "Capital Structure",
        "methodology": "Combines reported balance sheet debt ($109,316M) with the present value of non-cancelable compute and operating lease commitments ($376,003.8M).",
        "economic_intuition": "Anthropic's massive minimum commitments to AWS and GCP for GPU clusters have binding contractual standing. Treating them as operating expenses understates financial leverage and overstates operating margins.",
        "precedents": [
            {"sheet": "Input sheet", "coord": "B15", "label": "Reported Book Debt", "val": "$109,316 M"},
            {"sheet": "Operating lease converter", "coord": "C28", "label": "PV of Compute Commitments", "val": "$376,003.8 M"}
        ],
        "dependents": ["Valuation output!B30 (Value of Equity)"]
    },
    "Valuation output!B27": {
        "label": "Cash and Cash Equivalents",
        "formula": "=Input sheet!B22",
        "category": "Asset Bridge",
        "methodology": "Adds existing balance sheet cash and short-term liquid investments ($112,389M).",
        "economic_intuition": "Cash represents non-operating assets that must be added back to enterprise value to transition from operating assets to equity value. Anthropic's $112B cash provides an immediate 2-year liquidity runway.",
        "precedents": [{"sheet": "Input sheet", "coord": "B22", "label": "Cash & Liquid Holdings", "val": "$112,389 M"}],
        "dependents": ["Valuation output!B30 (Value of Equity)"]
    },
    "Valuation output!B28": {
        "label": "Expected Net IPO Proceeds",
        "formula": "=Input sheet!B18",
        "category": "Asset Bridge",
        "methodology": "Adds anticipated primary capital raised in the public offering ($100,000M).",
        "economic_intuition": "Primary capital infusions increase firm equity and cash balances dollar-for-dollar. When combined with existing cash, Anthropic will possess over $212B in liquid reserves.",
        "precedents": [{"sheet": "Input sheet", "coord": "B18", "label": "Expected IPO Proceeds", "val": "$100,000 M"}],
        "dependents": ["Valuation output!B30 (Value of Equity)"]
    },
    "Valuation output!B30": {
        "label": "Total Value of Equity",
        "formula": "=B24-B25-B26+B27+B28+B29",
        "category": "Core Output",
        "methodology": "Standard Corporate Finance equity bridge: Equity = Operating Assets - Debt - Minority Interest + Cash + IPO Proceeds + Non-Operating Assets.",
        "economic_intuition": "Calculates the total intrinsic equity value across all outstanding share classes before deducting employee option dilution overhang.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B24", "label": "Operating Assets", "val": "$1,719,952.6 M"},
            {"sheet": "Valuation output", "coord": "B25", "label": "Total Adjusted Debt", "val": "$485,319.8 M"},
            {"sheet": "Valuation output", "coord": "B27", "label": "Cash", "val": "$112,389 M"},
            {"sheet": "Valuation output", "coord": "B28", "label": "IPO Proceeds", "val": "$100,000 M"},
            {"sheet": "Valuation output", "coord": "B29", "label": "Non-Operating Assets", "val": "$3,929 M"}
        ],
        "dependents": ["Valuation output!B32 (Common Stock Equity)"]
    },
    "Valuation output!B31": {
        "label": "Value of Employee Options Overhang",
        "formula": "=Option value!B23",
        "category": "Dilution Overhang",
        "methodology": "Evaluates granted employee stock options using the Black-Scholes option pricing model ($472.3M) rather than arbitrary treasury stock exercise methods.",
        "economic_intuition": "Deducting option value from total equity separates the equity claim of option holders from common stockholders, preventing dilution double-counting.",
        "precedents": [{"sheet": "Option value", "coord": "B23", "label": "Total Value of Granted Options", "val": "$472.3 M"}],
        "dependents": ["Valuation output!B32 (Common Stock Equity)"]
    },
    "Valuation output!B32": {
        "label": "Value of Equity in Common Stock",
        "formula": "=B30-B31",
        "category": "Core Output",
        "methodology": "Total Equity ($1,450,950.8M) minus Option Value ($472.3M) = $1,450,478.5M ($1.450 Trillion).",
        "economic_intuition": "The net residual value that directly belongs to public common equity investors.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B30", "label": "Total Value of Equity", "val": "$1,450,950.8 M"},
            {"sheet": "Valuation output", "coord": "B31", "label": "Value of Options", "val": "$472.3 M"}
        ],
        "dependents": ["Valuation output!B34 (Estimated Value / Share)"]
    },
    "Valuation output!B33": {
        "label": "Diluted Shares Outstanding",
        "formula": "=Input sheet!B24+Option value!B20",
        "category": "Share Count",
        "methodology": "Combines base common shares on the balance sheet with unvested restricted stock units (RSUs) to establish diluted share count of 3,302.267 Million shares.",
        "economic_intuition": "Using diluted share count ensures that all equity claims are appropriately shared across public and insider ownership.",
        "precedents": [
            {"sheet": "Input sheet", "coord": "B24", "label": "Reported Shares", "val": "3,074.6 M"},
            {"sheet": "Option value", "coord": "B20", "label": "Restricted Shares Added", "val": "227.7 M"}
        ],
        "dependents": ["Valuation output!B34 (Estimated Value / Share)"]
    },
    "Valuation output!B34": {
        "label": "Estimated Intrinsic Value Per Share",
        "formula": "=B32/B33",
        "category": "Core Output",
        "methodology": "Common Equity Value ($1,450,478.5M) divided by 3,302.267M shares = $439.24 per share.",
        "economic_intuition": "The final intrinsic target fair value per share from Damodaran's 10-year Ginzu DCF model following the Q3 2026 leaked numbers update.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B32", "label": "Common Stock Equity", "val": "$1,450,478.5 M"},
            {"sheet": "Valuation output", "coord": "B33", "label": "Diluted Shares", "val": "3,302.267 M"}
        ],
        "dependents": ["Valuation output!B36 (Price as % of Value)"]
    },
    "Valuation output!B35": {
        "label": "Rumored IPO Offering Price",
        "formula": "525",
        "category": "Market Pricing",
        "methodology": "The rumored target offering price per share ($525.00) based on leaked investment banking roadshow previews.",
        "economic_intuition": "Implies a target market cap of $1.734 Trillion.",
        "precedents": [],
        "dependents": ["Valuation output!B36 (Price as % of Value)"]
    },
    "Valuation output!B36": {
        "label": "Price as % of Intrinsic Value",
        "formula": "=B35/B34",
        "category": "Pricing Misvaluation",
        "methodology": "IPO Price ($525.00) / Fair Value ($439.24) = 119.53%.",
        "economic_intuition": "Anthropic is priced at a 19.53% premium over Damodaran's intrinsic fair value (-16.33% downside). Investors paying $525 are pricing in even higher growth or zero failure risk.",
        "precedents": [
            {"sheet": "Valuation output", "coord": "B35", "label": "Offering Price", "val": "$525.00"},
            {"sheet": "Valuation output", "coord": "B34", "label": "Intrinsic Value", "val": "$439.24"}
        ],
        "dependents": []
    },

    # ---------------- Operating lease converter ----------------
    "Operating lease converter!C28": {
        "label": "Debt Value of Compute & Leases",
        "formula": "=SUM(C22:C27)",
        "category": "Forensic Debt",
        "methodology": "Sums the discounted present values of nominal contractual compute cluster commitments across Years 1 through 6+ ($468,232M nominal) discounted at 6.2828% pre-tax cost of debt.",
        "economic_intuition": "These commitments are legally binding contractual obligations for GPU hardware. Capitalizing them turns operating commitments into $376.0B of synthetic debt on the balance sheet.",
        "precedents": [{"sheet": "Operating lease converter", "coord": "C22:C27", "label": "Annual PV of Commitments", "val": "$376,003.8 M"}],
        "dependents": ["Valuation output!B25 (Total Debt)"]
    },
    "Operating lease converter!C15": {
        "label": "Pre-tax Cost of Debt for Leases",
        "formula": "=0.0494+0.013428",
        "category": "Discount Rate",
        "methodology": "Risk-free rate (4.94%) + BB+ synthetic rating default spread (1.34%) = 6.2828%.",
        "economic_intuition": "The discount rate used to capitalize operating leases must reflect the company's pre-tax borrowing cost for secured/unsecured term debt.",
        "precedents": [{"sheet": "Synthetic rating", "coord": "B14", "label": "BB+ Default Spread", "val": "1.34%"}],
        "dependents": ["Operating lease converter!C22:C27 (PV of Commitments)"]
    },
    "Operating lease converter!F31": {
        "label": "Depreciation on Operating Lease Asset",
        "formula": "=C28/7",
        "category": "Forensic Normalization",
        "methodology": "Calculates annual straight-line depreciation on the synthetic compute asset ($53,714.8M).",
        "economic_intuition": "Once leases are capitalized, the full lease payment is replaced on the income statement by depreciation of the asset and interest on the synthetic debt.",
        "precedents": [{"sheet": "Operating lease converter", "coord": "C28", "label": "Debt Value of Leases", "val": "$376,003.8 M"}],
        "dependents": ["Operating lease converter!F32 (Operating Earnings Adjustment)"]
    },
    "Operating lease converter!F32": {
        "label": "Adjustment to Operating Earnings (Leases)",
        "formula": "=B4-F31",
        "category": "Forensic Normalization",
        "methodology": "Current year lease expense ($52M) minus depreciation ($53,714.8M) = -$53,662.8M adjustment to pre-tax operating earnings.",
        "economic_intuition": "Capitalizing massive future compute commitments front-loads depreciation charges, significantly restating base-year operating income.",
        "precedents": [
            {"sheet": "Operating lease converter", "coord": "B4", "label": "Current Lease Expense", "val": "$52 M"},
            {"sheet": "Operating lease converter", "coord": "F31", "label": "Lease Depreciation", "val": "$53,714.8 M"}
        ],
        "dependents": ["Input sheet!B12 (Restated EBIT)"]
    },

    # ---------------- R& D converter ----------------
    "R& D converter!D24": {
        "label": "Value of Capitalized Research Asset",
        "formula": "=SUM(D24:D27)",
        "category": "Forensic Asset",
        "methodology": "Sums the unamortized portions of current and past 3 years R&D expenditures ($16,979M current at 100%, $12,645M Yr -1 at 66.7%, $3,366M Yr -2 at 33.3%) to create a $26,531M research asset.",
        "economic_intuition": "In GAAP/IFRS, R&D is expensed immediately. Damodaran treats R&D as capital investment, recognizing an amortizable intangible asset that creates multi-year cash-flow generating power.",
        "precedents": [{"sheet": "R& D converter", "coord": "B10:B13", "label": "Historical R&D Expenses", "val": "$33,582 M Total"}],
        "dependents": ["Input sheet!B14 (Restated Book Value of Equity)"]
    },
    "R& D converter!E24": {
        "label": "Amortization of Research Asset",
        "formula": "=SUM(E25:E27)",
        "category": "Forensic Normalization",
        "methodology": "Calculates current-year amortization expense across historical R&D tranches ($5,534.3M).",
        "economic_intuition": "Replaces expensed R&D with economic amortization. Since current R&D ($16,979M) exceeds amortization ($5,534M), base operating income is boosted by +$11,444.7M.",
        "precedents": [{"sheet": "R& D converter", "coord": "B11:B13", "label": "Past R&D Expenses", "val": "$16,603 M"}],
        "dependents": ["Input sheet!B12 (Restated EBIT)"]
    },

    # ---------------- Cost of capital worksheet ----------------
    "Cost of capital worksheet!B13": {
        "label": "Cost of Capital (WACC)",
        "formula": "=B52*B48+B56*B54",
        "category": "Hurdle Rate",
        "methodology": "Blended weighted average cost of capital: Cost of Equity (10.05%) * 94.7% weight + After-tax Cost of Debt (4.70%) * 5.3% weight = 9.74%.",
        "economic_intuition": "Represents the opportunity cost of capital for investing in Anthropic. Sits near the 90th percentile of US tech firms and transitions to 9.13% terminal.",
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
        "formula": "1.2482",
        "category": "Moat Risk",
        "methodology": "Average unlevered beta for US Software (System & Application) industry, eliminating the distortion of individual company regression noise.",
        "economic_intuition": "Measures the pure operating risk of Anthropic's enterprise software business without leverage.",
        "precedents": [{"sheet": "Industry Averages(US)", "coord": "C42", "label": "US Software Unlevered Beta", "val": "1.25"}],
        "dependents": ["Cost of capital worksheet!B47 (Levered Beta)"]
    },
    "Cost of capital worksheet!B24": {
        "label": "Macro Risk-Free Rate (Rf)",
        "formula": "0.0494",
        "category": "Macro Anchor",
        "methodology": "Yield on the US 10-year Treasury bond (4.94%) as of valuation date.",
        "economic_intuition": "The foundation of all opportunity costs in US dollars. A risk-free investment with zero default and reinvestment risk over a 10-year horizon.",
        "precedents": [],
        "dependents": ["Cost of capital worksheet!B48 (Cost of Equity)", "Operating lease converter!C15 (Cost of Debt)"]
    },
    "Cost of capital worksheet!B27": {
        "label": "Mature Market Equity Risk Premium (ERP)",
        "formula": "0.04",
        "category": "Macro Anchor",
        "methodology": "Mature equity risk premium (4.00% to 4.61%) backing out expected returns from S&P 500 cash flows.",
        "economic_intuition": "The incremental compensation required by institutional investors for holding equities instead of riskless treasuries.",
        "precedents": [],
        "dependents": ["Cost of capital worksheet!B48 (Cost of Equity)"]
    },

    # ---------------- Failure Rate worksheet ----------------
    "Failure Rate worksheet!B10": {
        "label": "10-Year Cumulative Failure Probability (BB)",
        "formula": "0.1178",
        "category": "Distress Anchor",
        "methodology": "Cumulative 10-year corporate default rate for BB-rated debt based on multi-decade S&P/Moody's credit default studies (11.78%).",
        "economic_intuition": "Empirical validation for Damodaran's 10% failure rate assumption in the core valuation bridge.",
        "precedents": [],
        "dependents": ["Valuation output!B22 (Probability of Failure)"]
    }
}

print(f"Loaded {len(methodology_kb)} key methodology nodes.")

# Save payload to JSON for inspection and embedding
payload = {
    "sheets": extracted_sheets,
    "methodologies": methodology_kb
}

with open("ERVIS/projects/US_EQUITIES/ANTHROPIC/scratch_drafts/extracted_model_data.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, default=str)

print("Saved extracted payload.")
