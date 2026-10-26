# Dashboard 2: Financial Market Analytics (Power BI)
## Technical Specification & Implementation Guide

---

## 📈 Overview & Objectives
The **Financial Market Analytics Dashboard** is an interactive Business Intelligence solution designed in **Microsoft Power BI Desktop**. It explores historical daily stock prices, capital returns, trading volume liquidity, and annualized volatility across multiple corporate equities (`AAPL`, `MSFT`, `GOOGL`, `AMZN`) across the 2023 calendar trading year.

### Core Analytical Capabilities
- **Multi-Asset Performance Modeling:** Benchmarks capital appreciation point-to-point without falling into absolute share-price scale distortion.
- **Trading Day Return Engine:** Formulates return calculations strictly relative to the preceding valid exchange session (\(t-1\)), preserving integrity across weekends and market holidays.
- **Quantitative Volatility Standards:** Transforms daily price dispersion into annualized volatility percentages based on the established 252-trading-day financial market convention.
- **Liquidity Analysis:** Examines volume spikes and correlates trading turnover with high-volatility sessions.

---

## 🌟 Dimensional Star Schema Architecture

The relational model implements a clean Star Schema:
- **`FactStockPrices` (Fact Table):** Contains 1,000 daily trading records with OHLCV prices, precomputed daily returns, and intraday spreads.
- **`DimDate` (Calendar Dimension):** Continuous 365-day calendar table enabling optimized VertiPaq time intelligence.
- **`DimTicker` (Equity Dimension):** Master lookup table containing ticker symbols, full corporate company names, and GICS economic sectors.

### Table Relationships:
- `DimDate[Date]` 1:N `FactStockPrices[Date]` *(Single-direction filter)*
- `DimTicker[Ticker]` 1:N `FactStockPrices[Ticker]` *(Single-direction filter)*

---

## 🛠️ Step-by-Step Power BI Desktop Build Instructions

### Step 1: Ingest Data via Power Query
1. Open **Microsoft Power BI Desktop**.
2. Click **Get Data → Text/CSV**.
3. Load the pre-configured datasets located in `big-data-dashboards/financial-powerbi/data/`:
   - `FactStockPrices_Combined.csv`
   - `DimTicker.csv`
   - `DimDate.csv`
4. Confirm delimiters (comma) and character encoding (UTF-8).
5. Review detailed transformation steps in [`power-query/M_CODE_GUIDE.md`](./financial-powerbi/power-query/M_CODE_GUIDE.md).
6. Click **Close & Apply**.

---

### Step 2: Establish Model Relationships & Date Marking
1. Navigate to **Model View** in Power BI.
2. Link `DimDate[Date]` to `FactStockPrices[Date]` *(1-to-many)*.
3. Link `DimTicker[Ticker]` to `FactStockPrices[Ticker]` *(1-to-many)*.
4. Right-click `DimDate` in the Fields pane → **Mark as date table** → Select `Date` column.

---

### Step 3: Implement DAX Measures
Create a dedicated `_Measures` table (**Home → Enter Data**) and insert the formulas detailed in [`measures/DAX_MEASURES.md`](./financial-powerbi/measures/DAX_MEASURES.md):
- `[Total Trading Records] = COUNTROWS(FactStockPrices)`
- `[Latest Available Date] = MAX(FactStockPrices[Date])`
- `[Total Trading Volume] = SUM(FactStockPrices[Volume])`
- `[Average Daily Return %] = AVERAGE(FactStockPrices[DailyReturnPct])`
- `[Latest Close] = IF(HASONEVALUE(FactStockPrices[Ticker]), CALCULATE(MAX(FactStockPrices[Close]), FactStockPrices[Date] = MAX(FactStockPrices[Date])), BLANK())`
- `[Period Total Return %] = ...` (Calculates point-to-point capital appreciation for single-ticker context)
- `[Annualized Volatility %] = STDEV.S(FactStockPrices[DailyReturnPct]) * SQRT(252)`

---

### Step 4: Construct Report Pages (3-Page Architecture)
Adhere to the layout geometry and color palette detailed in [`screenshots/README.md`](./financial-powerbi/screenshots/README.md):

1. **Page 1: Market Overview:**
   - Top KPI cards: Latest Available Date, Selected Ticker Count, Total Trading Records, Total Trading Volume.
   - Closing Price Trend Line Chart (Legend: Ticker).
   - Period Total Return % Clustered Bar Chart.
   - Cumulative Volume Clustered Column Chart.
   - Summary Asset Matrix Table.
   - Slicers: Date Range Slider and Ticker Dropdown.

2. **Page 2: Price & Return Analysis:**
   - Single-Equity Closing Price Line Chart.
   - Color-Coded Daily Returns Timeline Bar Chart (Green for positive, Red for negative).
   - Daily Return Distribution Histogram / Binned Column Chart.
   - KPI Cards: Highest Close, Lowest Close, Average Daily Return, Positive Return Days %.

3. **Page 3: Volume & Volatility:**
   - Daily Volume Spikes Line Chart.
   - Annualized Volatility % Bar Chart by Ticker.
   - Volume vs Daily Return % Bivariate Scatter Plot.
   - Monthly Return & Volume Matrix Table with green-red conditional formatting.

---

## 🎨 Design & Accessibility Guidelines
- Canvas Background: Slate Navy (`#0f172a`).
- Card Containers: Charcoal (`#1e293b`) with subtle borders (`#334155`).
- Sync Slicers across all 3 pages (**View → Sync slicers**).
- Mandatory footer on all pages: *"Historical data for educational analysis only. Not investment advice."*
