# ERVIS Bloomberg Terminal & Workstation Architecture

The **Equity Research and Valuation Investment System (ERVIS) Bloomberg Terminal** is an institutional financial workstation designed to operate as a local, keyboard-driven application across macOS and Linux terminals. It provides rapid point-in-time financial statement forensics, discounted cash flow valuation, Gate 4B AI CapEx audits, portfolio tracking, and econometric CAPM beta regressions using industry-standard Bloomberg 4-letter mnemonics.

---

## 🏛️ 1. Architecture Overview & Design Doctrine

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION & COMMAND ENTRY                         │
│   • Global CLI: 'ervis', 'ervis-term', 'ervis --print <TICKER> <MNEMONIC>'      │
│   • Interactive TUI: Textual + Rich Terminal Workstation (Hotkeys [F1] - [F9])  │
│   • External Vector Graphics: 'ervis --chart <TICKER>', 'GRPH <GO>', [G]        │
└────────────────────────────────────────┬────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      ERVIS TERMINAL CONTROLLER & DISPATCHER                     │
│   • Router: 'ervis-term' (Bash symlink resolver & CLI argument dispatcher)      │
│   • Application Engine: 'ERVIS/terminal/app.py' (Textual reactive event loop)   │
│   • Normalizer: 'resolve_ticker()' (Canonical alias resolution for R.R, etc.)   │
└──────────────────┬──────────────────────────────────────────────┬───────────────┘
                   │                                              │
                   ▼                                              ▼
┌─────────────────────────────────────┐        ┌──────────────────────────────────┐
│        RENDERER & VIEWPORTS         │        │    DATA PERSISTENCE & VAULT      │
│  'ERVIS/terminal/renderer.py'       │        │  'ERVIS/vault/ervis_vault.db'    │
│   • DES  [F2]: Overview Dossier     │        │   • Time-series SQLite store     │
│   • FA   [F3]: Multi-Year Stmts     │◄───────┤   • 15 covered securities        │
│   • DCF  [F4]: 10-Yr Ginzu Schedule │        │   • 6,910 financial stmts rows   │
│   • OVML [F5]: Gate 4B AI CapEx     │        │   • Point-in-time valuation gaps │
│   • BETA [F9]: CAPM & Hamada Matrix │        │   • Econometric beta regressions │
│   • RV   [F6]: S&P 500 Top 10 Matrix│        │  'ERVIS/vault/engine.py'         │
│   • PORT [F7]: Seed Portfolio Desk  │        │   • Relational query engine      │
│   • TOP  [F8]: Macro Intelligence   │        └──────────────────────────────────┘
│   • HELP [F1]: Mnemonic Directory   │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                AUTHENTIC VECTOR VISUALIZER (GRPH <GO> / [G])                     │
│  'ERVIS/terminal/chart_generator.py'                                            │
│   • High-precision vector coordinates (156 empirical weekly returns)            │
│   • Pure Bloomberg Terminal aesthetic: 0px border-radius, strict monospace     │
│   • Zero vibe-coding / zero neon gradient glow; authentic dark monochrome       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### The Institutional Design Doctrine: Zero "Vibe-Coding"
The ERVIS terminal adheres strictly to Wall Street institutional aesthetic standards:
1. **Strict Monospace Typography**: All alphanumeric data, headers, and axes utilize monospace typefaces (`SF Mono`, `Menlo`, `Monaco`, `Courier New`).
2. **Sharp Rectangular Geometry**: 0px border radius, zero drop shadows, and zero translucent glassmorphism.
3. **High-Density Tabular Layouts**: Screen real estate is prioritized for financial ratios, forensic health scores, and valuation progression matrices rather than empty whitespace.
4. **Decoupled Visualization**: Monospace text consoles excel at dense tables and keystroke speed, but fail at diagonal coordinate geometry. Visual charts are decoupled into an authentic, standalone terminal-styled vector engine (`GRPH <GO>`).

---

## ⌨️ 2. Bloomberg Mnemonic Directory & Syntax

The terminal accepts both interactive hotkeys and Bloomberg command syntax:

| Bloomberg Mnemonic | Interactive Hotkey | CLI Command | Function & Description |
| :--- | :--- | :--- | :--- |
| `<TICKER> DES <GO>` | `[F2]` | `ervis --print <TICKER> DES` | **Security Description**: Spot market price, triangulated intrinsic target, valuation gap, and bridge. |
| `<TICKER> FA <GO>` | `[F3]` | `ervis --print <TICKER> FA` | **Financial Analysis**: 5-Year Balance Sheet, Income Statement, Cash Flow ramp, and DuPont 5-point ROE. |
| `<TICKER> DCF <GO>` | `[F4]` | `ervis --print <TICKER> DCF` | **Discounted Cash Flow**: 10-Year Pro-Forma Ginzu schedule, Sales-to-Capital reinvestment, and TV audit. |
| `<TICKER> OVML <GO>` | `[F5]` | `ervis --print <TICKER> 4B` | **Overlay Model (Gate 4B)**: Hyperscaler AI CapEx payback, GPU depreciation, and obsolescence scorecard. |
| `<TICKER> BETA <GO>` | `[F9]` | `ervis --print <TICKER> BETA` | **Historical Beta & CAPM**: OLS regression, Blume adjustment, Hamada decomposition, and WACC matrix. |
| `<TICKER> GRPH <GO>` | `[G]` | `ervis --chart <TICKER>` | **Vector Graphic Visualizer**: Standalone Bloomberg terminal-styled vector chart in default browser. |
| `RV <GO>` | `[F6]` | `ervis --print RV` | **Relative Valuation**: S&P 500 Top 10 AI concentration and valuation matrix. |
| `PORT <GO>` | `[F7]` | `ervis --print PORT` | **Portfolio Desk**: Seed portfolio allocation ($200 Webull float) and limit DCA execution schedule. |
| `TOP <GO>` / `NEWS` | `[F8]` | `ervis --print TOP` | **Top News**: Daily macro intelligence brief, utility bottlenecks, and rate commentary. |
| `HELP <GO>` | `[F1]` | `ervis --print HELP` | **Directory & Guide**: Complete command syntax, hotkey map, and active coverage list. |
| `QUIT` / `Q` | `[ESC]` | N/A | Exits the terminal workstation cleanly back to shell prompt. |

---

## 📈 3. The Beta & Capital Asset Pricing Engine (`BETA <GO>`)

### A. Econometric OLS Regression Formulation
The security's systematic sensitivity is estimated via ordinary least squares (OLS) regression over 156 weekly excess return observations ($N = 156$, 3-year historical window):

$$R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,\text{raw}} (R_{m,t} - R_{f,t}) + \epsilon_{i,t}$$

* **Raw Historical Beta ($\beta_{\text{raw}}$)**: Empirical slope parameter measuring covariance with primary benchmark (`SPX Index` for US equities, `UKX Index` for UK industrials).
* **Blume Adjusted Beta ($\beta_{\text{adj}}$)**: Bloomberg institutional standard reflecting empirical mean-reversion toward market average over long-term investment horizons:
  $$\beta_{\text{adj}} = 0.67 \cdot \beta_{\text{raw}} + 0.33$$
* **Jensen's Alpha ($\alpha$)**: Annualized excess risk-adjusted return above CAPM hurdle rate:
  $$\alpha_{\text{annual}} = \alpha_{\text{weekly}} \times 52$$
* **Coefficient of Determination ($R^2$)**: Proportion of security variance explained by systemic market variance ($R^2 = r^2$).
* **Standard Error ($\text{SE}(\beta)$) & $t$-Statistic**: Statistical precision testing null hypothesis ($H_0: \beta = 0$):
  $$t = \frac{\beta_{\text{raw}}}{\text{SE}(\beta)} \quad (p < 0.001)$$

### B. Hamada Capital Structure Decomposition
To separate pure technological operating exposure from balance sheet debt leverage, ERVIS implements the **Hamada Equation**:

$$\beta_L = \beta_U \left[ 1 + (1 - t) \left( \frac{D}{E} \right) \right] \iff \beta_U = \frac{\beta_L}{1 + (1 - t) \left( \frac{D}{E} \right)}$$

Where:
* $\beta_L$: Levered equity beta (empirically observed).
* $\beta_U$: Unlevered asset moat beta (pure business operating risk).
* $t$: Effective corporate tax rate.
* $D/E$: Net debt to market equity ratio.

For fortress balance sheet companies holding substantial net cash balances (e.g. NVDA net cash $-\$48.9\text{B}$, GOOGL $-\$64.7\text{B}$, AAPL $-\$20.6\text{B}$), $\beta_U \approx \beta_L$, demonstrating that systematic volatility is driven by technological disruption rather than default risk.

### C. CAPM Systematic Sensitivity & Scenario Matrix
In place of low-resolution ASCII coordinate plots, the terminal screen presents a multi-regime WACC stress matrix:

| Scenario / Regime | Raw Beta ($\beta$) | Blume Adj ($\beta$) | Cost of Equity ($K_e$) | Implied WACC | Portfolio & Valuation Impact |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Defensive Moat** | 0.85 | 0.90 | 8.47% | 8.47% | Low operating leverage / margin expansion buffer |
| **Market Parity** | 1.00 | 1.00 | 8.91% | 8.91% | Broad market risk-parity benchmark hurdle |
| **► Current Baseline** | **1.38** | **1.25** | **9.99%** | **9.99%** | Active forensic parameter used in discrete DCF |
| **Elevated Volatility** | 1.35 | 1.23 | 9.93% | 9.93% | Macro hurdle rate pressure & hardware cycle drift |
| **Severe Stress** | 1.60 | 1.40 | 10.65% | 10.65% | Maximum cyclical covariance / tail-risk drawdown |

---

## 🗄️ 4. Data Persistence & NAS Portability

All historical filings, model snapshots, Gate 4B metrics, and regression tables reside in a unified, portable SQLite database at:
```
ERVIS/vault/ervis_vault.db
```

### Relational Schema (`ERVIS/vault/schema.sql`)
1. **`securities`**: Master ticker registry, primary market exchange, currency, and sector.
2. **`financial_statements`**: 5-year standardized balance sheet, income statement, and cash flow items.
3. **`valuation_snapshots`**: Point-in-time intrinsic fair value audit trail across preliminary, interim, and Gate 5 final stages.
4. **`gate_4b_metrics`**: Physical hyperscaler CapEx, annual GPU depreciation (3.5-yr schedule), and net AI ROI.
5. **`beta_regressions`**: Econometric regression records across all 11 active coverage tickers.

### Portability for External NAS Deployment
* Zero absolute path dependencies: All application paths are resolved dynamically relative to the `ERVIS/` project root.
* The entire historical vault (`ervis_vault.db`), model sheets, and HTML reports can be copied or mounted onto an external Network Attached Storage (NAS) appliance without reconfiguration.

---

## 🔗 Related Wiki Documentation
* [[End_to_End_Valuation_Mastery_and_Framework]]: Synthesis of the 8 pillars of institutional valuation.
* [[Engineering_Learnings_and_Bugs]]: Post-mortem debugging reflections on ticker aliasing, zero-division hazards, and monospace graphics.
* [[Universal_Institutional_Valuation_Spreadsheet_Model]]: 7-tab cloud valuation spreadsheet model.
* [[module_01_and_02_foundations_and_cost_of_capital]]: Damodaran Foundations & WACC curriculum guide.
* [[model_valuation]]: Sapphire Capital NUS CFA Champion 10-step institutional blueprint.
