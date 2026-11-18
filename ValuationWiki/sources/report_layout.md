# Powell Industries (POWL): Valuation Report 2-Column Page Layout Guide

This layout guide details how to arrange the text paragraphs from `powell_valuation_writeup.txt` alongside the generated high-resolution figure assets in `output_figure/` to construct a 2-column report format (identical to the CFA Research Challenge NUS reference report).

All numbers are 100% verified against the master Excel model **[`POWELL/powell_valuation_model_final.xlsx`](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/POWELL/powell_valuation_model_final.xlsx)**.

---

## Page 1 Layout: Intrinsic DCF Valuation & Cost of Capital

### Left Column (Sidebar Graphics):
1. **Figure 6.1: Valuation Football Field** (`output_figure/figure_6_1_valuation_football_field.png`)
   * *Position:* Top left
   * *Caption:* Valuation summary comparing 52-Wk Range ($130–$250), Street Consensus ($235–$333), Comps ($175.42), DCF Perpetual ($261.82), DCF Exit Multiple ($310.53), and Blended Target ($286.00) against $218.73 Current Price.
2. **Figure 6.2: Master Cost of Capital & WACC Computation Matrix** (`output_figure/figure_6_2_cost_of_equity.png`)
   * *Position:* Middle left
   * *Caption:* Single comprehensive table combining Cost of Equity ($K_e = 11.02\%$), Beta derivation ($\beta = 1.15$, Peer Unlevered $\beta_u = 0.98$), Cost of Debt ($K_d = 0.00\%$), Tax Rate (22.25%), and WACC (11.02%).
3. **Figure 6.3: WACC & Capital Structure Donut** (`output_figure/figure_6_3_wacc_and_capital_structure.png`)
   * *Position:* Bottom left
   * *Caption:* Powell capital structure breakdown (99.97% Equity / 0.03% Debt) & WACC of 11.02%.

### Right/Center Column (Main Text Paragraphs):
* **Heading:** `6. Valuation`
* **Paragraph:** `Valuation Overview – Choice of Methodologies`
* **Paragraph:** `Intrinsic Valuation – Discounted Cash Flow Analysis`
* **Paragraph:** `Revenue and Cost Build`
* **Paragraph:** `Cost of Capital & WACC Derivation` *(Merged section covering Ke, Kd, Beta, and Capital Structure)*

---

## Page 2 Layout: Sensitivity, Scenario Analysis & Monte Carlo

### Left Column (Sidebar Graphics):
1. **Figure 6.4: Sensitivity Matrix Heatmap** (`output_figure/figure_6_4_sensitivity_matrix.png`)
   * *Position:* Top left
   * *Caption:* 3x3 WACC vs Growth sensitivity matrix with $261.77 Base Target highlighted (Range: $185.11 to $337.26).
2. **Figure 6.5: Valuation Bridge** (`output_figure/figure_6_5_valuation_bridge.png`)
   * *Position:* Middle left
   * *Caption:* Waterfall price bridge starting at $150 baseline showing execution from $218.73 Current Price $\rightarrow$ Backlog Execution (+$28.40) $\rightarrow$ Margin Expansion (+$22.50) $\rightarrow$ Multiple Re-Rating (+$16.55) $\implies$ $286.18 Target Price.
3. **Figure 6.6: Monte Carlo Simulation Distribution** (`output_figure/figure_6_6_monte_carlo_distribution.png`)
   * *Position:* Bottom left
   * *Caption:* 10,000-iteration Monte Carlo curve (86.78% win rate) with P10 ($213.64), Mean ($264.42), and P90 ($320.12).

### Right/Center Column (Main Text Paragraphs):
* **Sub-paragraph:** `Terminal Growth Rate and Exit Multiple`
* **Sub-paragraph:** `Sensitivity Analysis & Scenario Analysis`
* **Sub-paragraph:** `Monte Carlo Simulation`

---

## Page 3 Layout: Relative Valuation, Comps & Capital Restructuring

### Left Column (Sidebar Graphics):
1. **Figure 6.7: Trading Comparables Bar Chart** (`output_figure/figure_6_7_relative_valuation_comps.png`)
   * *Position:* Top left
   * *Caption:* Peer EV/EBITDA multiples (HUBB 15.2x, ETN 18.5x, FIX 17.8x, EME 14.9x, VRT 25.4x, Peer Median 19.2x) vs POWL target multiple (18.0x).
2. **Figure 6.8: Broker Consensus Target Distribution** (`output_figure/figure_6_8_broker_consensus.png`)
   * *Position:* Middle left
   * *Caption:* Wall Street Consensus Targets ($235 Low - $333 High, $276 Median) vs Our $286 Target.
3. **Figure 6.9: Capital Restructuring Impact Comparison** (`output_figure/figure_6_9_capital_restructuring_impact.png`)
   * *Position:* Bottom left
   * *Caption:* Leveraged recap scenario (20% Debt issue for $1.6B buyback) reducing WACC to 9.79% and unlocking +$35/share value.

### Right/Center Column (Main Text Paragraphs):
* **Paragraph:** `Relative Valuation – Comparable Companies Analysis`
* **Sub-paragraph:** `Peer Group Selection & Multiples`
* **Paragraph:** `Broker Consensus as further Sanity Check`
