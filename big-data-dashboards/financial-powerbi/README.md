# Financial Market Analytics: Interactive Power BI Dashboard
## Multi-Asset Equity Performance & Volatility Analysis

An academic Business Intelligence dashboard engineered in **Microsoft Power BI Desktop** analyzing historical daily trading performance, returns, volume liquidity, and annualized volatility for large-cap equities.

---

## 📌 Project Overview

This Power BI project delivers a dimensional reporting architecture that models and visualizes historical stock market activity across multiple corporate equities (`AAPL`, `MSFT`, `GOOGL`, `AMZN`) for the full calendar year 2023.

### Key Analytical Deliverables
1. **Multi-Asset Performance:** Compare point-to-point capital returns and price trajectories across equities without falling into absolute-price scale biases.
2. **True Trading Day Return Engine:** Compute price variations strictly against preceding exchange trading sessions, properly handling market weekends and holidays.
3. **Volatility & Risk Metrics:** Standardize daily price deviations into annualized volatility percentages based on the established 252-trading-day convention.
4. **Liquidity Dynamics:** Track trading volume surges and correlate liquidity spikes with high-volatility market sessions.

> ⚠️ **Educational Disclaimer:** This dashboard and dataset are prepared strictly for academic evaluation and exploratory data visualization. It is **not** financial advice or a recommendation to buy or sell securities.

---

## 📁 Repository Structure

```text
financial-powerbi/
├── README.md                   # This project guide & execution manual
├── PROJECT_REPORT_NOTES.md     # Academic project report notes & methodology
├── data/
│   ├── README.md               # Dataset provenance, dictionary & rules
│   ├── AAPL.csv                # Apple Inc. 2023 daily OHLCV
│   ├── MSFT.csv                # Microsoft Corp. 2023 daily OHLCV
│   ├── GOOGL.csv               # Alphabet Inc. 2023 daily OHLCV
│   ├── AMZN.csv                # Amazon.com Inc. 2023 daily OHLCV
│   ├── FactStockPrices_Combined.csv # Pre-combined fact table (1,000 rows)
│   ├── DimTicker.csv           # Company name & economic sector dimension
│   └── DimDate.csv             # 365-day calendar dimension table
├── power-query/
│   └── M_CODE_GUIDE.md         # Step-by-step ETL & copyable M-Code scripts
├── measures/
│   └── DAX_MEASURES.md         # Copyable DAX measures with formatting rules
├── model/
│   └── DATA_MODEL.md           # Star Schema relationships & configuration
└── screenshots/
    └── README.md               # Visual wireframes, theme styling & layout grid
```

---

## 🚀 Step-by-Step Power BI Desktop Build Instructions

Since binary `.pbix` files require Microsoft Power BI Desktop GUI authoring, follow these straightforward steps to load and configure the project:

### Step 1: Open Power BI Desktop & Load Data
1. Open **Microsoft Power BI Desktop**.
2. Click **Home → Get Data → Text/CSV**.
3. Load the three core tables from the `data/` directory:
   - `FactStockPrices_Combined.csv` (Renamed to `FactStockPrices`)
   - `DimTicker.csv`
   - `DimDate.csv`
4. *(Optional Advanced ETL):* Alternatively, paste the provided M-Code from [`power-query/M_CODE_GUIDE.md`](./power-query/M_CODE_GUIDE.md) into the **Advanced Editor**.
5. Click **Close & Apply**.

---

### Step 2: Establish Star Schema Relationships
1. Switch to the **Model View** (left-hand sidebar in Power BI).
2. Connect the tables as detailed in [`model/DATA_MODEL.md`](./model/DATA_MODEL.md):
   - Drag `DimDate[Date]` → `FactStockPrices[Date]` *(1-to-many, Single direction)*.
   - Drag `DimTicker[Ticker]` → `FactStockPrices[Ticker]` *(1-to-many, Single direction)*.
3. Right-click `DimDate` → **Mark as date table** → Select `Date` column.

---

### Step 3: Create DAX Measures
1. Click **Home → Enter Data** to create a blank table named `_Measures`.
2. Open [`measures/DAX_MEASURES.md`](./measures/DAX_MEASURES.md) and copy each DAX measure formula.
3. In Power BI, click **New Measure**, paste the DAX expression, and assign the specified format string (e.g. Percentage, Currency, Whole Number).
4. Key measures to create first:
   - `[Total Trading Records]`
   - `[Latest Available Date]`
   - `[Total Trading Volume]`
   - `[Latest Close]`
   - `[Period Total Return %]`
   - `[Annualized Volatility %]`

---

### Step 4: Build Report Pages
Follow the wireframe layouts and chart configurations in [`screenshots/README.md`](./screenshots/README.md):
- **Page 1 (Market Overview):** Top KPI cards, Closing Price Line Chart, Total Volume Bar Chart, Period Return % Bar Chart, and Ticker/Date Slicers.
- **Page 2 (Price & Return Analysis):** Single-equity Close Line Chart, Daily Returns Timeline Bar Chart, Return Distribution Histogram, and Positive Return Days %.
- **Page 3 (Volume & Volatility):** Daily Volume Line Chart, Annualized Volatility Bar Chart by Ticker, Volume vs Return Scatter Plot, and Monthly Returns Matrix.

---

## 🎨 Theme & Visual Accessibility
- **Dark Theme:** High-contrast slate canvas (`#0f172a`) with dark charcoal card containers (`#1e293b`).
- **Semantic Accents:** Emerald Green (`#10b981`) for positive returns, Crimson Red (`#ef4444`) for negative returns, Cyan Teal (`#06b6d4`) for volume and neutral indicators.
- **Sync Slicers:** Synchronize the `Date` and `Ticker` slicers across all 3 pages (**View → Sync slicers**).
