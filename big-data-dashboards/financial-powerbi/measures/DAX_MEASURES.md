# DAX Measures Reference & Formula Guide

This document contains copy-ready **Data Analysis Expressions (DAX)** formulas for the **Financial Market Analytics Dashboard** in Power BI Desktop.

---

## 🧮 Recommended Organization: Dedicated Measures Table
For clean data governance, store all DAX calculations inside a dedicated table called `_Measures`:
1. In Power BI Desktop, click **Home → Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Create each new measure inside `_Measures` via **New Measure**.
4. Delete the default dummy column `Column1`.

---

## 1. Volumetric & High-Level KPIs

### `[Total Trading Records]`
```dax
Total Trading Records = 
COUNTROWS(FactStockPrices)
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Total number of daily trading rows matching current slicer context.

---

### `[Latest Available Date]`
```dax
Latest Available Date = 
MAX(FactStockPrices[Date])
```
- **Format:** Short Date (`yyyy-mm-dd`)
- **Description:** Most recent market trading date in the selected filter period.

---

### `[Earliest Available Date]`
```dax
Earliest Available Date = 
MIN(FactStockPrices[Date])
```
- **Format:** Short Date (`yyyy-mm-dd`)
- **Description:** Starting trading date in the selected filter period.

---

### `[Selected Ticker Count]`
```dax
Selected Ticker Count = 
DISTINCTCOUNT(FactStockPrices[Ticker])
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Count of distinct equities currently being analyzed.

---

### `[Trading Days Count]`
```dax
Trading Days Count = 
DISTINCTCOUNT(FactStockPrices[Date])
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Count of active market session dates (excludes non-trading weekends and holidays).

---

### `[Total Trading Volume]`
```dax
Total Trading Volume = 
SUM(FactStockPrices[Volume])
```
- **Format:** Whole Number with Display Units (Millions `0.00 M` or Billions `0.00 B`)
- **Description:** Cumulative number of shares traded in the selected period.

---

### `[Average Trading Volume]`
```dax
Average Trading Volume = 
AVERAGE(FactStockPrices[Volume])
```
- **Format:** Whole Number with Display Units (`0.00 M`)
- **Description:** Mean daily trading volume per session.

---

## 2. Pricing & Valuation Measures

### `[Latest Close]`
> ⚠️ **Filter Context Guard:** Comparing raw closing prices across different stocks on a single KPI card is mathematically misleading. This measure automatically returns `BLANK()` if multiple tickers are selected without a single-ticker filter.

```dax
Latest Close = 
IF(
    HASONEVALUE(FactStockPrices[Ticker]),
    VAR LatestDateInContext = MAX(FactStockPrices[Date])
    RETURN
        CALCULATE(
            MAX(FactStockPrices[Close]),
            FactStockPrices[Date] = LatestDateInContext
        ),
    BLANK()
)
```
- **Format:** Currency (`$#,##0.00`)
- **Card Subtitle Guidance:** If blank, display *"Select a single ticker to view latest close"*.

---

### `[Highest Close in Period]`
```dax
Highest Close in Period = 
MAX(FactStockPrices[Close])
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Maximum observed closing price in the active date range.

---

### `[Lowest Close in Period]`
```dax
Lowest Close in Period = 
MIN(FactStockPrices[Close])
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Minimum observed closing price in the active date range.

---

## 3. Return & Performance Measures

> **Storage Convention Note:** `DailyReturnPct` is stored as percentage points (e.g., `1.50` represents `1.50%`). Formulas below respect this convention without redundant multiplication by 100.

### `[Average Daily Return %]`
```dax
Average Daily Return % = 
AVERAGE(FactStockPrices[DailyReturnPct])
```
- **Format:** Percentage or Decimal with `%` suffix (`+0.00%;-0.00%;0.00%`)
- **Description:** Arithmetic mean of daily returns across active trading sessions.

---

### `[Period Total Return %]`
Calculates the point-to-point percentage return between the first trading session and last trading session of the selected date interval.

```dax
Period Total Return % = 
IF(
    HASONEVALUE(FactStockPrices[Ticker]),
    VAR StartDate = MIN(FactStockPrices[Date])
    VAR EndDate = MAX(FactStockPrices[Date])
    VAR StartClose = CALCULATE(MAX(FactStockPrices[Close]), FactStockPrices[Date] = StartDate)
    VAR EndClose = CALCULATE(MAX(FactStockPrices[Close]), FactStockPrices[Date] = EndDate)
    RETURN
        IF(
            StartClose > 0,
            DIVIDE(EndClose - StartClose, StartClose) * 100,
            BLANK()
        ),
    BLANK()
)
```
- **Format:** Decimal Number (`+0.00;-0.00;0.00`) with `%` sign
- **Description:** Total capital appreciation over the selected timeframe for the selected asset.

---

### `[Positive Return Days Count]`
```dax
Positive Return Days Count = 
CALCULATE(
    COUNTROWS(FactStockPrices),
    FactStockPrices[DailyReturnPct] > 0
)
```
- **Format:** Whole Number (`#,##0`)

---

### `[Positive Return Days %]`
```dax
Positive Return Days % = 
DIVIDE(
    [Positive Return Days Count],
    [Total Trading Records],
    0
) * 100
```
- **Format:** Decimal Number (`0.0%`)
- **Description:** Proportion of trading sessions where the asset closed higher than the previous day.

---

## 4. Volatility & Risk Measures

### `[Daily Volatility %]`
```dax
Daily Volatility % = 
STDEV.S(FactStockPrices[DailyReturnPct])
```
- **Format:** Decimal Number (`0.00%`)
- **Description:** Sample standard deviation of daily percentage returns, capturing intra-day price dispersion.

---

### `[Annualized Volatility %]`
> 📚 **Financial Rationale:** Financial markets conventionally standardize daily volatility to an annual figure assuming **252 trading days per year** (the standard number of open NYSE/NASDAQ market sessions per calendar year).
> \[\sigma_{\text{ann}} = \sigma_{\text{daily}} \times \sqrt{252}\]

```dax
Annualized Volatility % = 
VAR DailyStdDev = STDEV.S(FactStockPrices[DailyReturnPct])
RETURN
    IF(
        NOT(ISBLANK(DailyStdDev)),
        DailyStdDev * SQRT(252),
        BLANK()
    )
```
- **Format:** Decimal Number (`0.00%`)
- **Description:** Annualized standard deviation of returns.

---

## 5. Intra-day Range Metrics

### `[Average Daily Range %]`
```dax
Average Daily Range % = 
AVERAGE(FactStockPrices[DailyRangePct])
```
- **Format:** Decimal Number (`0.00%`)
- **Description:** Average percentage spread between daily High and daily Low: \(\frac{\text{High} - \text{Low}}{\text{Low}} \times 100\).

---

## ✅ DAX Validation & Testing Checklist
1. **Single Ticker Test:** Select `AAPL` in slicer. Verify `Latest Close`, `Period Total Return %`, and `Annualized Volatility %` display exact computed values.
2. **Multi Ticker Test:** Select `All` tickers. Verify `Latest Close` cleanly evaluates to `BLANK()` without throwing an evaluation error.
3. **Date Slicer Test:** Narrow the date range to Q1 2023 (`2023-01-03` to `2023-03-31`). Verify `Trading Days Count` updates to ~62 days and all volume sums scale proportionally.
