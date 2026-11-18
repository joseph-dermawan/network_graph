# Monte Carlo Stochastic Risk Simulation

To rigorously test valuation downside risk under macroeconomic uncertainty, we built a **10,000-Trial Monte Carlo Stochastic Model** (`powell_bullcase_monte_carlo.py`).

---

## 🎲 Simulation Parameters & Probability Distributions

The simulation randomized three core model drivers simultaneously across 10,000 trials:
1. **WACC Discount Rate:** Normal Distribution $\sim \mathcal{N}(\mu = 11.02\%, \sigma = 0.75\%)$, bounded between 9.0% and 13.5%.
2. **Terminal Growth Rate ($g$):** Normal Distribution $\sim \mathcal{N}(\mu = 3.50\%, \sigma = 0.38\%)$, bounded between 2.0% and 5.0%.
3. **5-Year Revenue CAGR:** Normal Distribution $\sim \mathcal{N}(\mu = 24.0\%, \sigma = 2.50\%)$, bounded between 15.0% and 32.0%.

---

## 📊 Statistical Output Breakdown (10,000 Trials)

```
========================================================================================
STATISTICAL METRIC                       INTRINSIC SHARE PRICE VALUE
========================================================================================
10th Percentile (P10 Bear Baseline)      $213.64
Median Intrinsic Value (P50)             $260.70
Mean Intrinsic Value (Expected Value)    $264.42
90th Percentile (P90 Bull Baseline)      $320.12
Current Stock Price Baseline             $218.73
Probability of Positive Return (> $218)  86.78% (Win Rate)
Standard Deviation ($\sigma$)            $42.15
========================================================================================
```

---

## 💡 Key Risk & Return Insights

1. **86.78% Positive Return Probability:** Out of 10,000 randomized market trials, **8,678 trials** evaluated to an intrinsic share price strictly above the current market price of **$218.73**.
2. **Asymmetric Risk/Reward Profile:** 
   * **Downside Risk (P10):** Under a 10th percentile outcome, intrinsic value is **$213.64** (-2.3% downside).
   * **Upside Potential (P90):** Under a 90th percentile outcome, intrinsic value expands to **$320.12** (+46.4% upside).
3. **Conclusion:** The stochastic risk distribution demonstrates an overwhelmingly favorable asymmetric risk-to-reward ratio, confirming Powell as an institutional-grade **BUY**.

---

## 🔗 Related Wiki Pages
* [[DCF_Valuation_Model]]: Deterministic base DCF target price ($261.82).
* [[Report_Visuals_Catalog]]: Figure 6.6 (Monte Carlo Distribution Histogram).
