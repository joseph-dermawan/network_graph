# Graph Centrality Momentum: Structural Alpha in US Equities

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Status](https://img.shields.io/badge/Status-Production-green)
![Domain](https://img.shields.io/badge/Domain-Quant%20Finance-orange)

### **Executive Summary**
This project implements a **Network Theory-based quantitative trading strategy** that outperforms the S&P 500 by **+65%** over a 4-year backtest period (Jan 2019 – Jun 2024). 

Unlike traditional momentum strategies that rely solely on price history, this model uses **Graphical Lasso (Glasso)** and **Eigenvector Centrality** to identify the *structural leaders* ("King Nodes") of the market. By constructing a portfolio of stocks that are both influential (Central) and trending (Momentum), the strategy captures regime-driving alpha while filtering out peripheral noise.

**Key Performance Highlights:**
* **Final Equity:** $3,066,837 (vs $1,847,121 Benchmark) from $1M initial capital.
* **CAGR:** 24.25% (vs 13% SPY).
* **Sharpe Ratio:** 0.84.
* **Beta:** 0.99 (Captures upside volatility efficiently).

---

### **1. The Theoretical Framework**

#### **The Problem: Correlation Breakdown**
Standard diversification relies on correlation matrices (Pearson). However, in financial markets:
1.  **Correlations are noisy:** Everything looks correlated during a rally.
2.  **Correlations lack structure:** A correlation matrix doesn't tell you if Tech is driving Energy, or if they are moving independently.
3.  **The "Dumb Momentum" Trap:** Buying everything that goes up exposes the portfolio to "dead cat bounces" in low-quality assets.

#### **The Solution: Graph Topology**
We model the market as a **Gaussian Markov Random Field**.
1.  **Sparse Inverse Covariance (Glasso):** We calculate the precision matrix to isolate *conditional dependence*. If Stock A is correlated to Stock B only because both are correlated to Stock C, Glasso removes the A-B edge, revealing the true "Backbone" of the market.
2.  **Eigenvector Centrality:** We measure the influence of each node. A stock with high centrality is a "King Node"—mathematically connected to the movement of the entire cluster.

---

### **2. Strategy Logic**

The strategy rotates capital into the **Structural Leaders** of the current market regime.

#### **Algorithm Steps:**
1.  **Universe:** 40 liquid large-cap US stocks across diverse sectors (Tech, Finance, Energy, Healthcare, Consumer).
2.  **Regime Lookback:** Rolling 60-day window.
3.  **Graph Construction:**
    * Center returns (remove market beta).
    * Fit Graphical Lasso to estimate the Precision Matrix.
    * Build a weighted undirected graph from partial correlations.
4.  **Signal Generation (The "Centrality Score"):**
    * Calculate **Eigenvector Centrality** ($C_i$) for each stock.
    * Calculate **Momentum** ($M_i$) (60-day total return).
    * **Final Score = $C_i \times M_i$**
5.  **Portfolio Construction:**
    * **Long Top 10:** Equal-weight allocation to the top 10 scoring stocks.
    * **Rebalance:** Monthly (Every 20 trading days) to minimize turnover costs.
    * **Transaction Costs:** 10bps (0.10%) per trade applied in backtest.

---

### **3. Performance Analysis**

The strategy demonstrates that **market structure precedes price action**. 
* **2020-2021 (Tech Rally):** The graph correctly identifies Big Tech (NVDA, MSFT) as central nodes, riding the bubble.
* **2022 (Regime Shift):** As Tech correlations broke, the graph topology shifted. Energy stocks (XOM, CVX) became central nodes, allowing the strategy to pivot into the new leaders.

| Metric | Strategy | Benchmark (S&P 500) |
| :--- | :--- | :--- |
| **Total Return** | **+206.7%** | +84.7% |
| **CAGR** | **24.25%** | ~13.00% |
| **Sharpe Ratio** | **0.84** | 0.60 |
| **Max Drawdown** | **-32.48%** | -33.92% |

> *Note: The strategy achieves nearly double the total return of the benchmark with a similar maximum drawdown profile.*

---

### **4. Repository Structure**

* `qg_final.py` - **Core Strategy Engine:** The production-grade backtest script containing the Glasso logic, signal generation, and performance metrics.
* `qg_dashboard_pdf.py` - **Reporting Tool:** Generates a frame-by-frame PDF dashboard comparing equity curves vs. the evolving network graph structure.
* `requirements.txt` - Dependencies (`networkx`, `sklearn`, `yfinance`, etc.).
