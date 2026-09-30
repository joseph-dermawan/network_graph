-- ==============================================================================
-- ERVIS DATA VAULT :: RELATIONAL TIME-SERIES SCHEMA
-- Portable SQLite Architecture for Local Financial Data Storage
-- ==============================================================================

-- 1. Master Securities Directory
CREATE TABLE IF NOT EXISTS securities (
    ticker TEXT PRIMARY KEY,
    company_name TEXT NOT NULL,
    market TEXT NOT NULL,
    exchange TEXT,
    currency TEXT DEFAULT 'USD',
    spot_price REAL,
    target_price REAL,
    published_rating TEXT,
    valuation_gap_pct REAL,
    market_cap_b REAL,
    shares_outstanding_m REAL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Multi-Year Financial Statements (Balance Sheets, Income Statements, Cash Flows)
CREATE TABLE IF NOT EXISTS financial_statements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    statement_type TEXT NOT NULL, -- 'INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW'
    fiscal_year TEXT NOT NULL,    -- e.g. '2021', '2022', '2023', '2024', '2025', 'TTM'
    line_item TEXT NOT NULL,      -- e.g. 'Total Revenue', 'Operating Income', 'Free Cash Flow'
    value_m REAL NOT NULL,        -- Value in Millions
    currency TEXT DEFAULT 'USD',
    FOREIGN KEY (ticker) REFERENCES securities(ticker),
    UNIQUE (ticker, statement_type, fiscal_year, line_item)
);

-- 3. Forensic Normalization & Quality Series (Gate 1 & Gate 2)
CREATE TABLE IF NOT EXISTS forensic_normalized_series (
    ticker TEXT NOT NULL,
    fiscal_year TEXT NOT NULL,
    reported_ebit_m REAL,
    capitalized_rd_asset_m REAL,
    synthetic_lease_debt_m REAL,
    normalized_ebit_0_m REAL,
    normalized_nopat_0_m REAL,
    invested_capital_m REAL,
    true_net_debt_m REAL,
    effective_tax_rate REAL,
    economic_roic_pct REAL,
    altman_z_score REAL,
    piotroski_f_score INTEGER,
    beneish_m_score REAL,
    PRIMARY KEY (ticker, fiscal_year),
    FOREIGN KEY (ticker) REFERENCES securities(ticker)
);

-- 4. Point-in-Time Valuation Snapshots (Gate 3, 4, 5)
CREATE TABLE IF NOT EXISTS valuation_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL,
    ticker TEXT NOT NULL,
    spot_price REAL,
    dcf_intrinsic_value REAL,
    sotp_intrinsic_value REAL,
    monte_carlo_median REAL,
    monte_carlo_p10 REAL,
    monte_carlo_p90 REAL,
    monte_carlo_win_rate_pct REAL,
    liquidation_floor REAL,
    final_target_price REAL,
    valuation_gap_pct REAL,
    published_rating TEXT,
    base_wacc_pct REAL,
    terminal_wacc_pct REAL,
    hamada_beta REAL,
    credit_rating TEXT,
    FOREIGN KEY (ticker) REFERENCES securities(ticker)
);

-- 5. Gate 4B AI CapEx Payback & Obsolescence Series
CREATE TABLE IF NOT EXISTS gate4b_capex_series (
    ticker TEXT PRIMARY KEY,
    annual_capex_m REAL,
    ai_capex_m REAL,
    incremental_ai_revenue_m REAL,
    annual_depreciation_3_5yr_m REAL,
    net_ai_operating_income_m REAL,
    net_ai_roi_pct REAL,
    payback_period_years REAL,
    useful_life_years REAL DEFAULT 3.50,
    obsolescence_deficit_years REAL,
    capex_payout_ratio_pct REAL,
    break_even_revenue_gap_m REAL,
    risk_assessment TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticker) REFERENCES securities(ticker)
);

-- 6. Portfolio Ledger & Execution Tickets
CREATE TABLE IF NOT EXISTS portfolio_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ticker TEXT NOT NULL,
    asset_name TEXT NOT NULL,
    order_type TEXT NOT NULL,
    target_alloc_pct REAL NOT NULL,
    allocated_usd REAL NOT NULL,
    executed_price REAL,
    shares_count REAL,
    status TEXT NOT NULL,
    thesis TEXT,
    broker TEXT DEFAULT 'Webull Singapore'
);

-- 7. Historical Beta & Capital Asset Pricing Regressions (BETA screen)
CREATE TABLE IF NOT EXISTS beta_regressions (
    ticker TEXT PRIMARY KEY,
    benchmark_index TEXT NOT NULL,       -- e.g. 'SPX Index (S&P 500)', 'UKX Index (FTSE 100)'
    period TEXT NOT NULL,                -- e.g. '3-Year Weekly (156 Obs)'
    currency TEXT DEFAULT 'USD',
    raw_beta REAL NOT NULL,              -- Historical OLS Slope
    adjusted_beta REAL NOT NULL,         -- Blume Adjusted: 0.67*raw + 0.33
    alpha_annualized_pct REAL NOT NULL,  -- Jensen's Alpha annualized
    r_squared REAL NOT NULL,             -- Coefficient of determination (0-1)
    correlation REAL NOT NULL,           -- Pearson correlation coefficient
    std_error REAL NOT NULL,             -- Standard error of beta
    t_stat REAL NOT NULL,                -- t-statistic for beta
    unlevered_beta REAL NOT NULL,        -- Hamada Pure Business Moat Beta
    levered_beta REAL NOT NULL,          -- Hamada Relevered Capital Structure Beta
    debt_to_equity_pct REAL NOT NULL,    -- Net Debt / Equity %
    effective_tax_rate_pct REAL NOT NULL,-- Marginal Tax Rate
    risk_free_rate_pct REAL NOT NULL,    -- 10-Yr Sovereign Yield (e.g. 4.58%)
    erp_pct REAL NOT NULL,               -- Equity Risk Premium (e.g. 4.33%)
    cost_of_equity_pct REAL NOT NULL,    -- CAPM Ke = Rf + Beta * ERP
    wacc_base_pct REAL NOT NULL,         -- Blended Hurdle Rate
    risk_classification TEXT,            -- e.g. 'HIGH-BETA EXPONENTIAL GROWTH'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticker) REFERENCES securities(ticker)
);

-- Indexes for ultra-fast query performance
CREATE INDEX IF NOT EXISTS idx_fin_stmt_query ON financial_statements(ticker, statement_type, fiscal_year);
CREATE INDEX IF NOT EXISTS idx_val_snapshot ON valuation_snapshots(ticker, snapshot_date);
CREATE INDEX IF NOT EXISTS idx_beta_reg ON beta_regressions(ticker);
