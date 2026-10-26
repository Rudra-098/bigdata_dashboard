# Financial Market Analytics Dataset Reference

This directory contains historical daily financial market data formatted for ingestion into **Microsoft Power BI Desktop**.

---

## 1. Dataset Contents

| File Name | Description | Rows | Date Coverage |
| :--- | :--- | :--- | :--- |
| `AAPL.csv` | Apple Inc. daily OHLCV trading records | 250 | 2023-01-03 to 2023-12-29 |
| `MSFT.csv` | Microsoft Corp. daily OHLCV trading records | 250 | 2023-01-03 to 2023-12-29 |
| `GOOGL.csv`| Alphabet Inc. daily OHLCV trading records | 250 | 2023-01-03 to 2023-12-29 |
| `AMZN.csv` | Amazon.com Inc. daily OHLCV trading records | 250 | 2023-01-03 to 2023-12-29 |
| `FactStockPrices_Combined.csv` | Appended historical fact table for all 4 tickers | 1,000 | 2023-01-03 to 2023-12-29 |
| `DimTicker.csv` | Dimension table with verified Company Name and Sector metadata | 4 | N/A |
| `DimDate.csv` | Standard 365-day calendar dimension for date-time intelligence | 365 | 2023-01-01 to 2023-12-31 |

---

## 2. Public Data Sources & Attribution

The schema and pricing structures are modeled on public daily equity data:
- **Primary Public Source:** [Stooq Historical Quotes](https://stooq.com) / [Yahoo Finance Historical](https://finance.yahoo.com).
- **Asset Universe:** S&P 500 leading large-cap equities (Technology, Consumer Discretionary, Communication Services).
- **Calendar Basis:** US Stock Exchange (NYSE / NASDAQ) business calendar 2023 (excluding 10 observed exchange holidays).

---

## 3. Data Dictionary

| Column Name | Data Type | Units / Format | Analytical Definition |
| :--- | :--- | :--- | :--- |
| `Date` | Date | `YYYY-MM-DD` | Official exchange trading session date. |
| `Ticker` | Text | 4-character symbol | Unique stock ticker identifier (e.g., `AAPL`, `MSFT`). |
| `Open` | Decimal Number | USD (\$) | Opening session price. |
| `High` | Decimal Number | USD (\$) | Peak intra-day trading price. |
| `Low` | Decimal Number | USD (\$) | Lowest intra-day trading price. |
| `Close` | Decimal Number | USD (\$) | Official closing price for the trading session. |
| `AdjustedClose` | Decimal Number | USD (\$) | Price adjusted for corporate splits and dividend distributions. |
| `Volume` | Whole Number | Shares traded | Total number of equity shares transacted during the session. |
| `DailyReturnPct` | Decimal Number | Percentage (%) | Daily percentage return relative to previous available trading close: \(\frac{\text{Close}_t - \text{Close}_{t-1}}{\text{Close}_{t-1}} \times 100\). |
| `DailyRangePct` | Decimal Number | Percentage (%) | Intra-day trading spread percentage: \(\frac{\text{High}_t - \text{Low}_t}{\text{Low}_t} \times 100\). |

---

## 4. Academic Data Quality & Handling Principles

1. **Non-Trading Days (Weekends & Holidays):**
   - Stock markets do not operate on weekends or exchange holidays. These dates are **not** missing records and **must not** be filled with artificial interpolated prices.
2. **Prior Trading Day Returns:**
   - Percentage returns are computed exclusively against the *previous valid market session*, never the prior calendar day.
3. **Price Comparability:**
   - Raw share prices (e.g. \$150 vs \$280) reflect arbitrary share counts and capitalization structures. Comparative cross-ticker visual analysis should utilize **Percentage Return** or **Indexed Performance (Base 100)**.
4. **Educational Disclaimer:**
   - All historical metrics are for academic exploratory data analysis and Power BI modeling demonstration. They do not constitute investment advice or trading recommendations.
