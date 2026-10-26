# Power BI Report Page Layouts & Visual Wireframes

This document provides visual wireframes, layout coordinates, color palettes, and interaction configurations for the 3-page report in **Microsoft Power BI Desktop**.

---

## 🎨 Professional Financial Analytics Theme Palette

| UI Element | Color Name | Hex Code | Semantic Purpose |
| :--- | :--- | :--- | :--- |
| **Canvas Background** | Slate Navy | `#0f172a` | Executive, glare-free dark canvas |
| **Card / Visual Container** | Charcoal Container | `#1e293b` | Visual background with subtle border |
| **Container Borders** | Slate Border | `#334155` | 1px clean separator border |
| **Primary Positive Accent** | Emerald Green | `#10b981` | Positive returns & gains |
| **Primary Risk Accent** | Crimson Red | `#ef4444` | Negative returns & high volatility |
| **Primary Metric Accent** | Cyan Teal | `#06b6d4` | Volume, neutral metrics & cards |
| **Primary Typography** | Off-White Slate | `#f8fafc` | High-contrast readable headings |
| **Secondary Typography** | Muted Slate | `#94a3b8` | Captions, axis labels & legends |

---

## 📄 Page 1: Market Overview Wireframe

### Header & Slicer Bar (Top 120px)
```text
+---------------------------------------------------------------------------------------------------------+
| [TITLE] Financial Market Analytics: Market Overview                                                     |
| [Subtitle] Historical Daily Trading Performance & Volume Analysis (US Large-Cap Equities)                |
|                                                                                                         |
| [SLICER: Date Range Slider]           [SLICER: Ticker Dropdown]        [SLICER: Sector Dropdown]       |
| 2023-01-03 <===========> 2023-12-29   [All / AAPL / MSFT / GOOGL...]   [Technology / Discretionary...] |
+---------------------------------------------------------------------------------------------------------+
```

### KPI Cards Row (Height: 100px)
```text
+-------------------+  +-------------------+  +-------------------+  +-------------------+
| LATEST DATE       |  | TICKERS SELECTED  |  | TRADING RECORDS   |  | TOTAL VOLUME      |
| 2023-12-29        |  | 4                 |  | 1,000             |  | 45.24 B Shares    |
+-------------------+  +-------------------+  +-------------------+  +-------------------+
```

### Visuals Grid
```text
+-----------------------------------------------------+ +---------------------------------------------------+
| LINE CHART: Closing Price Trend Over Time           | | CLUSTERED BAR: Period Return % by Ticker          |
| Legend: Ticker                                      | | Axis: Ticker | Value: Period Total Return %       |
| X-Axis: DimDate[Date] | Y-Axis: FactStockPrices[Close] | Data labels enabled (+18.4%, +24.1%...)           |
+-----------------------------------------------------+ +---------------------------------------------------+
| CLUSTERED COLUMN: Cumulative Volume by Ticker       | | TABLE: Summary Asset Overview                   |
| X-Axis: Ticker | Y-Axis: Total Trading Volume       | | Columns: Ticker, Company, Sector, Latest Close, |
| Color: Cyan Teal                                    | | Total Volume, Annualized Volatility %           |
+-----------------------------------------------------+ +---------------------------------------------------+
```

---

## 📄 Page 2: Price & Return Analysis Wireframe

### Header & Filters
```text
+---------------------------------------------------------------------------------------------------------+
| [TITLE] Price Performance & Return Distributions                                                        |
| [SLICER: Date Range]                 [SLICER: Ticker Selector]          [Reset Filters Bookmark]        |
+---------------------------------------------------------------------------------------------------------+
```

### Return KPI Cards
```text
+-------------------+  +-------------------+  +-------------------+  +-------------------+
| HIGHEST CLOSE     |  | LOWEST CLOSE      |  | AVG DAILY RETURN  |  | POSITIVE DAYS %   |
| $198.11           |  | $129.42           |  | +0.12%            |  | 53.6%             |
+-------------------+  +-------------------+  +-------------------+  +-------------------+
```

### Visuals Grid
```text
+---------------------------------------------------------------------------------------------------------+
| LINE CHART: Daily Closing Price Trend (Selected Equities)                                               |
| X-Axis: DimDate[Date] | Y-Axis: FactStockPrices[Close] | Tooltip: High, Low, Volume, Daily Return %     |
+---------------------------------------------------------------------------------------------------------+
| BAR CHART: Daily Returns Timeline (% by Date)       | | COLUMN/HISTOGRAM: Daily Return Distribution     |
| Rules: Positive = Green (#10b981), Negative = Red  | | Bins: -3% to +3% in 0.5% intervals              |
| X-Axis: Date | Y-Axis: DailyReturnPct               | | Frequency histogram of price movements          |
+-----------------------------------------------------+ +---------------------------------------------------+
```

---

## 📄 Page 3: Volume & Volatility Wireframe

### Header & Slicers
```text
+---------------------------------------------------------------------------------------------------------+
| [TITLE] Market Liquidity, Volatility & Correlation                                                      |
| [SLICER: Year-Month]                 [SLICER: Ticker]                   [Disclaimer Footer]             |
+---------------------------------------------------------------------------------------------------------+
```

### Volatility KPI Cards
```text
+-------------------+  +-------------------+  +-------------------+  +-------------------+
| AVG DAILY VOLUME  |  | DAILY VOLATILITY  |  | ANNUAL VOLATILITY |  | AVG DAILY RANGE   |
| 45.24 M           |  | 1.58%             |  | 25.08% (252-day)  |  | 2.45%             |
+-------------------+  +-------------------+  +-------------------+  +-------------------+
```

### Visuals Grid
```text
+-----------------------------------------------------+ +---------------------------------------------------+
| AREA/LINE CHART: Daily Volume Spikes Over Time      | | BAR CHART: Annualized Volatility % by Ticker      |
| Highlights high-liquidity selloff or rally sessions | | Compares risk profile across equities             |
+-----------------------------------------------------+ +---------------------------------------------------+
| SCATTER PLOT: Trading Volume vs. Daily Return %     | | MATRIX: Monthly Performance Matrix                |
| X-Axis: Volume | Y-Axis: DailyReturnPct             | | Rows: Ticker, Columns: MonthName                  |
| Bubble Color: Ticker                                | | Values: Total Return %, Avg Volume               |
| Analyzes liquidity expansion during large swings    | | Conditional formatting: Green/Red gradient        |
+-----------------------------------------------------+ +---------------------------------------------------+
```

---

## 🔄 Interactivity & Slicer Syncing Settings
1. **Sync Slicers:** Go to **View → Sync slicers**. Enable sync between Page 1, Page 2, and Page 3 for the `Date` and `Ticker` slicers so user filtering persists seamlessly across tab switches.
2. **Visual Interactions:** Set `Edit interactions` on the Ticker bar chart to **Filter** rather than Highlight to update other cards dynamically upon clicking a specific company bar.
3. **Mandatory Educational Disclaimer:** Include a text card on all page footers:
   *"Historical data for academic exploratory analysis only. Not financial advice."*
