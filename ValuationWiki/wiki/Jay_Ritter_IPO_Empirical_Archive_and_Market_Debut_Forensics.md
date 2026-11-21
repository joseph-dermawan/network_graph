# Jay Ritter IPO Empirical Archive & Anthropic (NASDAQ: ANT) Market Debut Forensics

This document provides a rigorous, institutional reference manual synthesizing the market debut of **Anthropic, PBC (NASDAQ: ANT)** on November 18–20, 2026, the forensic analysis presented in the video deconstruction *"Anthropic Just Had the Biggest IPO Ever. You Couldn't Buy It at $83"* (YouTube ID: `Y8KS_BF3AeU`), and the foundational academic datasets published by **Professor Jay R. Ritter** (Warrington College of Business, University of Florida).

All models and datasets are mirrored in the live ERVIS Workstation terminal at [`almanac.html#empirical`](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/almanac.html#empirical).

---

## 🏛️ Part I: Anthropic Market Debut & 48-Hour Tape Forensics

### 1. Chronology & Offering Parameters

Anthropic filed Amendment No. 3 to its Form S-1 on November 17, 2026, setting an indicated price band of **$70.00 to $78.00 per share** ($74.00 midpoint) following a 10-for-1 forward stock split.

Due to intense institutional oversubscription (>18x covered on the book), the underwriting syndicate led by Morgan Stanley, Goldman Sachs, and J.P. Morgan officially priced the offering **above the range at $83.00 per share** on Wednesday evening, November 18, 2026.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   ANTHROPIC (NASDAQ: ANT) OFFERING SPECS                    │
├─────────────────────────────────────────────────────────────────────────────┤
│  Ticker: ANT (Nasdaq Global Select)     Listing Date: Thursday, Nov 19, 2026 │
│  Class A Common Shares Offered: 825.0M  Underwritten Purchase: $82.44 / sh  │
│  IPO Offering Price: $83.00 / share     Gross Underwriting Spread: $0.56/sh │
│  Total Primary Proceeds: $68.475 B      Syndicate Fee Pool: $548.8 Million  │
│  Diluted Shares Out: 16,912.15 M        Initial Public Float: 4.88%         │
│  Diluted Equity Value @ IPO: $1.4037 T  Greenshoe Option (15%): 123.75 M sh │
│  Damodaran Ginzu DCF Anchor: $83.69/sh  Strategic Sidecar: $26.0 B Private  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. The 48-Hour Tape Walkthrough: From Retail Euphoria to DCF Gravitational Parity

```
Price ($)
 120 ┼──────────────────────────────────────────────────────────────────
 115 ┼                      ┌── $115.00 (Day 1 Session High)
 110 ┼       $111.50 (Open) ┘
 105 ┼          ╲
 100 ┼           ╲                $97.17 (Day 1 Close: +17.07% vs Offer)
  95 ┼            ╲             ┌─┘
  90 ┼             ╲   Day 2   ╱  ┌── $88.30 (Day 2 Close: +6.39% vs Offer)
  85 ┼──────────────╲─────────┼───┼── $83.69 Damodaran DCF Intrinsic Anchor
  80 ┼  $83.00 (IPO) └── $83.05 (Day 2 Intraday Flush: Tested DCF by 64¢!)
     └─────┬──────────────┬──────────────┬──────────────┬───────────────
       Nov 18 (Priced)  Nov 19 (Open)  Nov 19 (Close)  Nov 20 (Low)  Nov 20 (Close)
```

1. **The Opening Cross (Nov 19, 9:30 AM EST):** 
   * Shares opened at **$111.50**, representing a **+34.34% opening pop** over the $83.00 offer price.
   * Peak intraday valuation briefly breached **$1.945 Trillion** at the session high of **$115.00**.
   * Day 1 trading volume reached **846 Million shares**, representing a **102.5% turnover of the entire 825M Class A public float** in a single 6.5-hour trading session.
2. **The Intraday Drift & Day 1 Settlement:**
   * Heavy institutional supply and dealer hedging compressed the tape from $115.00 down to **$94.50**, before settling at **$97.17** (+17.07% above offer, but **-12.85% below the retail opening print**).
3. **The Day 2 Flush & Gravitational Test (Nov 20, 2026):**
   * Morning algorithmic selling and retail stop-loss cascades flushed ANT shares to an intraday session low of **$83.05**.
   * **The DCF Anchor Held:** This low came within **5 cents of the $83.00 IPO offer price** and **within 64 cents of Professor Aswath Damodaran's Ginzu DCF intrinsic value ($83.69)**.
   * Value buyers stepped in aggressively at the $83.00–$83.69 support zone, driving a late-afternoon rally to close Day 2 at **$88.30** (+6.39% over offer, +5.51% over DCF fair value).

---

## 📹 Part II: YouTube Video Deconstruction (`Y8KS_BF3AeU`)

**Title:** *"Anthropic Just Had the Biggest IPO Ever. You Couldn't Buy It at $83."*  
**Channel Analysis Summary:**

### 1. The Two-Tier Access Asymmetry
The video deconstructs why everyday retail investors could not access Anthropic at $83.00:
* **The Institutional Club:** Morgan Stanley, Goldman Sachs, and J.P. Morgan allocated the 825M shares to preferred sovereign wealth funds, long-only asset managers, and tier-1 hedge funds at $83.00.
* **The Retail Trap:** Retail brokerages (Robinhood, Fidelity, Charles Schwab) could only execute market-on-open orders at the Nasdaq Opening Cross print of **$111.50**.
* **The Day 1 Loss:** Any retail investor buying at the $111.50 open was immediately down **-12.85%** at the Day 1 close ($97.17), and down **-25.52%** at the Day 2 low ($83.05).

### 2. Syndicate Economics & Gross Underwriting Spread
* **Purchase Price:** Underwriters bought shares from Anthropic at **$82.44 per share** (a $0.56 per share discount, or ~0.675% gross spread).
* **Syndicate Fee Revenue:** $0.56 $\times$ 825M shares = **$548.8 Million in underwriting fees** earned within 48 hours.
* **Greenshoe Over-Allotment:** The 15% greenshoe option (123.75M shares) gave underwriters naked short capacity to stabilize the stock at the $83.00 offer price without downside inventory risk.
* **Strategic Private Placement Sidecar:** $26.0B was raised simultaneously from cloud hyperscalers (Amazon, Google) in non-voting Class B/C equivalents, locking in long-term compute demand.

---

## 📊 Part III: Prof. Jay R. Ritter IPO Empirical Research Archive

The empirical data below is harvested from Professor Jay R. Ritter's published research datasets (Warrington College of Business, University of Florida):

### 1. All-Time League Table: Money Left on the Table in IPOs by Firm
*Source: Prof. Jay R. Ritter, "Money Left on the Table in IPOs by Firm" (Updated 12 Nov 2026).*

$$\text{Money Left on the Table} = (\text{Day 1 Closing Price} - \text{IPO Offer Price}) \times \text{Shares Offered}$$

| Rank | Company | Ticker | IPO Date | Offer Price | Day 1 Close | 1st-Day Pop | Shares Offered | Money Left on Table ($M) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **01** | **Anthropic, PBC** | **ANT** | **Nov 19, 2026** | **$83.00** | **$97.17** | **+17.07%** | **825.0M** | **$11,690.3M ($11.69B)** |
| 02 | Alibaba Group | BABA | Sep 19, 2014 | $68.00 | $93.89 | +38.07% | 320.1M | **$8,287.4M ($8.29B)** |
| 03 | Visa Inc. | V | Mar 19, 2008 | $44.00 | $56.50 | +28.41% | 406.0M | **$5,075.0M ($5.08B)** |
| 04 | Rivian Automotive | RIVN | Nov 10, 2021 | $78.00 | $100.73 | +29.14% | 153.0M | **$3,477.7M ($3.48B)** |
| 05 | Snowflake Inc. | SNOW | Sep 16, 2020 | $120.00 | $253.93 | +111.61% | 28.0M | **$3,749.9M ($3.75B)** |
| 06 | Airbnb Inc. | ABNB | Dec 10, 2020 | $68.00 | $144.71 | +112.81% | 51.5M | **$3,951.6M ($3.95B)** |
| 07 | United Parcel Service | UPS | Nov 10, 1999 | $50.00 | $67.25 | +34.50% | 109.4M | **$1,887.2M ($1.89B)** |
| 08 | Twitter Inc. | TWTR | Nov 07, 2013 | $26.00 | $44.90 | +72.69% | 70.0M | **$1,323.0M ($1.32B)** |
| 09 | Coupang, Inc. | CPNG | Mar 11, 2021 | $35.00 | $49.25 | +40.71% | 120.0M | **$1,710.0M ($1.71B)** |
| 10 | Meta Platforms | META | May 18, 2012 | $38.00 | $38.23 | +0.61% | 421.2M | **$96.9M ($0.10B)** |
| 11 | Alphabet (Google) | GOOG | Aug 19, 2004 | $85.00 | $100.34 | +18.05% | 19.6M | **$300.6M ($0.30B)** |

> [!IMPORTANT]
> **Anthropic shattered the all-time world record**, leaving **$11.69 Billion** on the table on its 825M Class A float ($13.89B if accounting for total syndicated distributions). Underwriters underpriced the company by $14.17 per share relative to Day 1 closing clearing prices.

---

### 2. Table 1: Historical IPO Underpricing & Money Left on Table (1980–2026)
*Source: Prof. Jay R. Ritter, "Initial Public Offerings: Updated Statistics" Table 1 (Warrington College of Business, Nov 2026).*

| Historical Era | IPO Sample Count | Aggregate Capital Raised ($B) | Mean First-Day Return (%) | Total Money Left on Table ($B) |
| :--- | :---: | :---: | :---: | :---: |
| **1980–1989** | 2,423 | $59.2 B | **7.4%** | $3.8 B |
| **1990–1998** | 4,142 | $251.7 B | **14.8%** | $27.4 B |
| **1999–2000 (Tech Bubble)** | 903 | $124.9 B | **65.0%** | **$66.4 B** |
| **2001–2019** | 2,198 | $458.1 B | **14.3%** | $47.1 B |
| **2020–2021 (Pandemic / SPAC Frenzy)** | 884 | $312.4 B | **31.7%** | **$39.2 B** |
| **2022–2025 (Tightening Cycle)** | 371 | $68.5 B | **13.5%** | $7.8 B |
| **2026 YTD (Anthropic Debut)** | 94 | $98.2 B | **17.1%** | **$18.4 B** |
| **All-Time Aggregate (1980–2026)** | **11,015** | **$1,373.0 B** | **18.9%** | **$210.1 B** |

---

### 3. Table 7: Predictive Power of Offer Price Relative to File Price Range
*Source: Prof. Jay R. Ritter, "Initial Public Offerings: Updated Statistics" Table 7 (Nov 2026).*

Ritter establishes that the revision of the offer price relative to the initial S-1 filing price range is the single most powerful predictor of first-day underpricing:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              RITTER TABLE 7: FIRST-DAY RETURN BY PRICING REGIME             │
├─────────────────────────────────────────────────────────────────────────────┤
│  Below File Range (< Low)   │ 28.4% of IPOs │ Mean 1st-Day Pop:  +3.2%      │
│  Within File Range          │ 48.8% of IPOs │ Mean 1st-Day Pop: +11.9%      │
│  Above File Range (> High)  │ 22.8% of IPOs │ Mean 1st-Day Pop: +49.8%  ★   │
└─────────────────────────────────────────────────────────────────────────────┘
```

* **Anthropic Positioning:** Initial range was $70.00–$78.00. Priced at **$83.00 (+6.4% above high end)**.
* **Empirical Validation:** Fits Ritter's "Above File Range" category (historical mean pop +49.8%). Anthropic opened at +34.34% and closed Day 1 at +17.07%.

---

### 4. Table 18e: Long-Run Returns by Public Float & The Lockup Cliff
*Source: Prof. Jay R. Ritter, "Updated Long-run Statistics" Table 18e (October 2026).*

Table 18e measures the **3-Year and 5-Year Buy-and-Hold Abnormal Returns (BHAR)** relative to size- and book-to-market matched style benchmark portfolios, categorized by initial public float percentage:

| Public Float Tier | % of IPO Deals | Mean 1st-Day Return | 3-Year Style BHAR | 5-Year Style BHAR | Lockup Expiration Volatility |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Micro-Float (< 10%)** | **14.2%** | **+38.4%** | **-24.8%** | **-38.2%** | **Severe (-8.4% week of day 180)** |
| **Moderate Float (10%–25%)** | 51.6% | +18.2% | -11.4% | -18.7% | Moderate (-3.2% week of day 180) |
| **Standard Float (25%–50%)** | 26.8% | +11.5% | -4.2% | -7.1% | Mild (-0.8% week of day 180) |
| **Broad Float (> 50%)** | 7.4% | +6.2% | **+3.1%** | **+5.4%** | Neutral (No abnormal drop) |

> [!WARNING]
> **Anthropic's Initial Public Float is only 4.88%** (825.0M shares floated / 16,912.15M diluted shares).
> 
> Ritter Table 18e demonstrates that **IPOs with float below 10% underperform their benchmark by -24.8% over 3 years and -38.2% over 5 years**.
> 
> The economic cause is the **180-Day Lockup Expiration Cliff**: when the 95.12% insider and private equity holdings become freely tradable, the massive expansion in supply overwhelms market liquidity.

---

### 5. Table 23 & 24: Dual-Class Governance Expansion & Valuation Discount
*Source: Prof. Jay R. Ritter, "Dual Class Structure of IPOs Through 2025" Table 23 & 24.*

| Decade / Era | Dual-Class Tech IPOs (%) | Dual-Class Non-Tech IPOs (%) | 5-Year BHAR Penalty (Dual vs Single) |
| :--- | :---: | :---: | :---: |
| **1980–1989** | 7.2% | 8.1% | -1.2% |
| **1990–1999** | 8.8% | 11.4% | -2.4% |
| **2000–2009** | 12.1% | 9.8% | -4.1% |
| **2010–2019** | 32.4% | 14.6% | -6.8% |
| **2020–2025** | **48.4%** | **17.2%** | **-8.6%** |

* **Anthropic Governance Structure:** Anthropic PBC features a 5-class equity architecture governed by the **Long-Term Benefit Trust (LTBT)** and the **Founder LLC Class P Golden Share** holding 50.1% voting control.
* **Empirical Penalty:** Ritter Table 24 demonstrates that dual-class tech enterprises suffer a **-8.6% 5-year return discount** compared to single-class governance structures due to entrenched agency costs and non-diversified controller incentives.

---

## 🎯 Part IV: Key Strategic Takeaways for Valuation Practitioners

1. **Damodaran's Intrinsic Gravity Holds:** Speculative momentum pushed Anthropic to $115.00 on Day 1 (+38.5% over offer), but institutional order flow violently corrected the stock back down to its fundamentals on Day 2, finding an exact bottom at **$83.05** against Damodaran's **$83.69 intrinsic DCF anchor**.
2. **Never Buy the Opening Cross:** Retail investors who purchased ANT at $111.50 suffered an immediate 25% drawdown within 24 hours. Underwriters deliberately leave money on the table to reward syndicate clients, while retail takes the drawdown.
3. **Beware Month 6 Lockup Expiry:** With only **4.88% float**, practitioners must anticipate severe supply pressure around May 2027 (180 days post-IPO) as 16.08 billion shares unlock, consistent with Ritter's Table 18e empirical findings.

---

## 🔗 Related Documentation & Models
* [Valuation Almanac Module 06 (Live HTML)](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/almanac.html#empirical)
* [Anthropic Valuation Cockpit](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/ervis_valuation_cockpit.html)
* [Damodaran 18-Sheet Excel Mirror](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/damodaran_breakdown_reader.html)
* [Anthropic S-1 Intelligence Dashboard](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/anthropic_prospectus_dashboard.html)
* [Anthropic Case File & Dossier Index](file:///Users/worldofmadness/Documents/VS%20Code/Personal%20Projects/NetworkGraph/ERVIS/projects/US_EQUITIES/ANTHROPIC/reports/index.html)
