# ERVIS Garage Calibration Mode (`GARAGE_CALIBRATION_MODE.md`)
**The Macroeconomic Instrument Tuning Workbench**

---

## 1. Overview: The "Mechanic in the Car Garage"

Before taking a race car onto the track, a mechanic tunes the engine timing, fuel injection, and tire pressures. 

Similarly, in institutional equity research, the analyst must not blindly accept default macro instruments. **ERVIS Garage Mode** is an interactive calibration workbench where the human analyst and AI co-worker audit and tweak the foundational instruments governing discount rates, sovereign spreads, and terminal boundaries.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                ERVIS GARAGE WORKBENCH                                  │
│                                                                                        │
│   [INSTRUMENT 1: ERP SOLVER]             ◄── Implied Forward-Looking S&P 500 DDM       │
│   [INSTRUMENT 2: SOVEREIGN SPREADS]      ◄── Credit Rating vs CDS vs Volatility CRP    │
│   [INSTRUMENT 3: RISK-FREE ANCHOR]       ◄── 10-Yr vs 30-Yr Sovereign Yield Curve      │
│   [INSTRUMENT 4: MOAT CONSTRAINTS]       ◄── Terminal ROIC Decoupling & Moat Duration  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The 4 Garage Instruments & Tuning Options

### Instrument 1: Equity Risk Premium (ERP) Tuning
* **Current Baseline:** Damodaran Implied ERP (`4.33%` - `4.60%`).
* **Garage Tuning Levers:**
  1. **Forward-Looking Implied Cash Flow Solver:** Solves for the internal discount rate ($r$) that equates current S&P 500 index price to the present value of trailing 12-month dividends and buybacks plus 5-year consensus earnings growth:
     $$\text{Index Price}_0 = \sum_{t=1}^{5} \frac{\text{Earnings}_0 (1 + g_t) \times \text{Payout}_t}{(1 + r)^t} + \frac{\text{Terminal Cash Flow}}{r - R_f}$$
     $$\text{Implied ERP} = r - R_f$$
  2. **Historical Realized Risk Premium:** Uses long-term historical returns (1928–Present):
     * Geometric Average: $\approx 4.3\%$ (Conservative / Academic favorite).
     * Arithmetic Average: $\approx 6.4\%$ (Standard sell-side investment bank default).
  3. **Survey & Consensus ERP:** Global institutional survey benchmarks (KPMG, Fernandez, PwC) averaging $5.0\% - 5.5\%$.

---

### Instrument 2: Country Risk Premium (CRP) Mechanics
For international companies operating outside the US/mature markets:
* **Option A — Sovereign Rating Default Spread:**
  $$\text{CRP} = \text{Sovereign Default Spread}$$
* **Option B — Relative Equity Volatility Adjusted Spread (Damodaran Standard):**
  $$\text{CRP} = \text{Sovereign Default Spread} \times \left(\frac{\sigma_{\text{Local Equity Market}}}{\sigma_{\text{Sovereign Government Bond}}}\right)$$
  *(Typically multiplies the sovereign bond spread by 1.2x to 1.5x to reflect the higher risk of equities relative to debt).*
* **Option C — Geographic Revenue Weighting:** If a company is incorporated in an emerging market but earns $70\%$ of its revenues in North America and Europe, the CRP is weighted by destination revenue rather than incorporation domicile.

---

### Instrument 3: Risk-Free Rate ($R_f$) & Maturity Matching
* **10-Year Constant Maturity Yield:** Default anchor for 10-year projection models. Matches the 10-year forecasting horizon.
* **30-Year Bond Yield:** Used as the conservative upper boundary for terminal growth rates ($g \le R_{f,30y}$).
* **Real Rate Decoupling:** In high-inflation regimes, the mechanic can decouple the nominal yield into expected inflation + real yield.

---

### Instrument 4: Moody's Synthetic Credit Matrix Tuning
* **Adjusting Rating Thresholds:** Tweak coverage multipliers to reflect stricter capital structures for small-cap vs large-cap firms.
* **ERM Notch Policies:** Set explicit rules for parental guarantees (e.g. Temasek in Singapore, Berkshire Hathaway in the US).

---

## 3. Entering Garage Mode via CLI

Run the Garage tuning tool to view or re-calibrate the master instruments:
```bash
./initiate-ervis garage
```
* Displays current calibration settings.
* Prompts the analyst with interactive tuning toggles.
* Updates `ERVIS/kb/macro/sovereign_yields.yaml` and `ERVIS/kb/macro/erp_settings.yaml`.
