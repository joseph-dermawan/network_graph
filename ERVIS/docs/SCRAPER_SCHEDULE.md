# ERVIS Scheduled Data Harvesting via Antigravity (`SCRAPER_SCHEDULE.md`)

---

## 1. Overview: Autonomous Background Data Scraping

To guarantee that ERVIS always possesses fresh macro benchmarks and financial filings without manual analyst intervention, the system leverages Antigravity's **built-in background scheduling engine (`/schedule` tool)**.

The scheduling framework operates in the background:
* Executes automated Python scraper scripts.
* Updates local benchmark YAML registries.
* Alerts the analyst if a new material filing (10-K, 10-Q, 8-K) is detected for any watchlisted ticker.

---

## 2. Automated Harvesting Schedules

| Data Stream | Scraper Script | Frequency | Cron Expression | Output Target |
| :--- | :--- | :--- | :--- | :--- |
| **US Treasury Yield Curve** | `scrapers/macro_treasury_fetch.py` | Daily (Post-market close at 18:00 UTC) | `0 18 * * 1-5` | `ERVIS/kb/macro/sovereign_yields.yaml` |
| **SEC EDGAR Filing Watcher** | `scrapers/sec_edgar_harvest.py` | Every 6 hours | `0 */6 * * *` | `ERVIS/projects/[MARKET]/[TICKER]/raw_filings/` |
| **Damodaran Annual Datasets** | `scrapers/damodaran_dataset_sync.py` | Annual (January 15th at 09:00 UTC) | `0 9 15 1 *` | `ERVIS/kb/macro/industry_averages/` |

---

## 3. Launching Schedules via Antigravity Slash Commands

Analysts can launch or inspect background scraping tasks directly using Antigravity commands:

### A. Daily Treasury Yield Harvest
```bash
# Schedule daily Treasury yield update at 6:00 PM UTC Monday through Friday
/schedule CronExpression="0 18 * * 1-5" Prompt="Run scrapers/macro_treasury_fetch.py to refresh US Treasury yields and sovereign risk-free rates in ERVIS/kb/macro/sovereign_yields.yaml"
```

### B. SEC EDGAR Quarterly Watcher for Watchlist Tickers
```bash
# Poll SEC EDGAR every 6 hours for new 10-K, 10-Q, or 8-K filings
/schedule CronExpression="0 */6 * * *" Prompt="Check SEC EDGAR API for newly released 10-K, 10-Q, or 8-K filings for tickers in ERVIS watchlist. Ingest new filings into raw_filings/ and notify analyst if fresh statements are detected."
```

### C. One-Shot Refresh Ahead of a Valuation Session
```bash
# Refresh macro and SEC data immediately prior to an interactive pairing session
python3 ERVIS/scrapers/macro_treasury_fetch.py
python3 ERVIS/scrapers/sec_edgar_harvest.py --ticker KO --all
```

---

## 4. Scraper Scripts Architecture

### 1. `macro_treasury_fetch.py`
Pulls the daily Treasury par yield curve from the US Department of the Treasury XML/JSON feed. Extracts:
* 3-Month Bill Rate (Cash hurdle)
* 10-Year Constant Maturity Yield (Standard $R_f$ for DCF modeling)
* 30-Year Bond Yield (Benchmark for Terminal Growth $g$)

### 2. `sec_edgar_harvest.py`
Connects to the SEC EDGAR API (`data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`). Extracts:
* Standardized US-GAAP facts (Revenues, Cost of Goods Sold, EBIT, Interest Expense, Balance Sheet Debt, Cash & Short-term Investments, Shares Outstanding).
* Footnote schedules for Lease Commitments and R&D expenditures.
* Stores parsed financial series directly into JSON format ready for automated ingestion into model workbooks.

### 3. `damodaran_dataset_sync.py`
Ingests Professor Aswath Damodaran's authoritative annual corporate finance datasets published each January:
* `wacc.xls` (Industry average unlevered betas, cash/firm value ratios, and debt ratios).
* `ctryprem.xls` (Sovereign default spreads and Country Risk Premiums).
* `margin.xls` (Global operating and net margin deciles by sector).
