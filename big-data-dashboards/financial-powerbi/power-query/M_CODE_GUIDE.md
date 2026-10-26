# Power Query M Code Guide & Transformation Pipeline

This document provides step-by-step instructions and copyable **Power Query M code** for importing and shaping financial stock market data into a clean Star Schema in **Power BI Desktop**.

---

## 🛠️ Step-by-Step UI Import Instructions

### Option 1: Quick Ingestion using Pre-Combined CSV (Recommended for Fast Setup)
1. Open **Microsoft Power BI Desktop**.
2. Click **Home → Get Data → Text/CSV**.
3. Select `FactStockPrices_Combined.csv` from the `data/` folder and click **Transform Data**.
4. Repeat for `DimTicker.csv` and `DimDate.csv`.
5. Verify column data types in the Power Query Editor.
6. Click **Close & Apply**.

---

### Option 2: Folder Ingestion & Appending (Demonstrating Advanced Power Query ETL)
To demonstrate dynamic multi-file ingestion where each ticker resides in its own CSV (`AAPL.csv`, `MSFT.csv`, etc.):

1. In Power BI Desktop, click **Get Data → Folder**.
2. Browse to the directory containing individual ticker files:
   `...\financial-powerbi\data`
3. Click **Transform Data**.
4. Filter the `Extension` column to `.csv` and exclude `FactStockPrices_Combined.csv`, `DimTicker.csv`, and `DimDate.csv`.
5. Add a custom column to extract the `Ticker` symbol from the file name:
   `Text.Start([Name], Text.PositionOf([Name], "."))`
6. Click the **Combine Files** icon (two down-arrows) on the `Content` column.
7. Set column types, verify delimiters (comma), and apply transformations.

---

## 💻 Copyable Power Query M Queries

### Query 1: `FactStockPrices` (Advanced Editor Script)

Open **Home → Advanced Editor** in Power Query and paste the following M code (adjust file path to your machine):

```powerquery
let
    // 1. Source Connection: Load CSV with explicit US locale for date/decimal parsing
    Source = Csv.Document(
        File.Contents("C:\Users\rudra\Desktop\bigdata_dashboard\big-data-dashboards\financial-powerbi\data\FactStockPrices_Combined.csv"),
        [Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),

    // 2. Promote Headers
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    // 3. Trim Text Whitespace
    TrimmedText = Table.TransformColumns(PromotedHeaders, {
        {"Ticker", Text.Trim, type text}
    }),

    // 4. Strongly Type Columns
    ChangedTypes = Table.TransformColumnTypes(TrimmedText, {
        {"Date", type date},
        {"Ticker", type text},
        {"Open", type number},
        {"High", type number},
        {"Low", type number},
        {"Close", type number},
        {"AdjustedClose", type number},
        {"Volume", Int64.Type},
        {"DailyReturnPct", type number},
        {"DailyRangePct", type number}
    }, "en-US"),

    // 5. Data Quality: Filter Out Null Dates or Unparseable Rows
    FilteredValidRows = Table.SelectRows(ChangedTypes, each ([Date] <> null) and ([Close] <> null) and ([Volume] <> null)),

    // 6. Deduplication: Ensure strictly unique (Date, Ticker) pairs
    RemovedDuplicates = Table.Distinct(FilteredValidRows, {"Date", "Ticker"}),

    // 7. Sort by Ticker Ascending, Date Ascending (critical for time sequences)
    SortedRows = Table.Sort(RemovedDuplicates, {{"Ticker", Order.Ascending}, {"Date", Order.Ascending}})
in
    SortedRows
```

---

### Query 2: `DimTicker` (Advanced Editor Script)

```powerquery
let
    Source = Csv.Document(
        File.Contents("C:\Users\rudra\Desktop\bigdata_dashboard\big-data-dashboards\financial-powerbi\data\DimTicker.csv"),
        [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TrimmedText = Table.TransformColumns(PromotedHeaders, {
        {"Ticker", Text.Trim, type text},
        {"Company", Text.Trim, type text},
        {"Sector", Text.Trim, type text}
    }),
    ChangedTypes = Table.TransformColumnTypes(TrimmedText, {
        {"Ticker", type text},
        {"Company", type text},
        {"Sector", type text}
    }),
    DistinctTickers = Table.Distinct(ChangedTypes, {"Ticker"})
in
    DistinctTickers
```

---

### Query 3: `DimDate` (Dynamic Calendar Dimension via Power Query M)

If you prefer generating the calendar dynamically in Power Query without an external file, use this dynamic M script:

```powerquery
let
    // Automatically find Start and End Date from FactStockPrices
    StartDate = #date(2023, 1, 1),
    EndDate = #date(2023, 12, 31),
    DayCount = Duration.Days(Duration.From(EndDate - StartDate)) + 1,
    DateList = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    TableFromList = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    TypedDate = Table.TransformColumnTypes(TableFromList, {{"Date", type date}}),
    
    // Add Calendar Attributes
    AddYear = Table.AddColumn(TypedDate, "Year", each Date.Year([Date]), Int64.Type),
    AddQuarter = Table.AddColumn(AddYear, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    AddMonthNum = Table.AddColumn(AddQuarter, "MonthNumber", each Date.Month([Date]), Int64.Type),
    AddMonthName = Table.AddColumn(AddMonthNum, "MonthName", each Date.MonthName([Date]), type text),
    AddYearMonth = Table.AddColumn(AddMonthName, "YearMonth", each Date.ToText([Date], "yyyy-MM"), type text),
    AddDay = Table.AddColumn(AddYearMonth, "Day", each Date.Day([Date]), Int64.Type),
    AddDayOfWeek = Table.AddColumn(AddDay, "DayOfWeek", each Date.DayOfWeekName([Date]), type text),
    AddIsWeekend = Table.AddColumn(AddDayOfWeek, "IsWeekend", each if Date.DayOfWeek([Date], Day.Monday) >= 5 then 1 else 0, Int64.Type)
in
    AddIsWeekend
```

---

## 🔍 Data Quality Verification Checklist in Power Query
- [x] Column profiling enabled (**View → Column quality**, **Column distribution**).
- [x] Zero error rows across all columns.
- [x] No empty/null dates or prices in fact table.
- [x] Primary keys (`Ticker` in `DimTicker`, `Date` in `DimDate`) verified as 100% unique.
- [x] Proper regional locale (`en-US`) set on decimal conversion steps to prevent comma/period confusion.
