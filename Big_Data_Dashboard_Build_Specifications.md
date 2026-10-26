# Big Data Analysis & Visualization — Dashboard Build Specifications

> **Purpose:** This document is the implementation brief for an AI coding agent (such as Antigravity). Build two separate, polished, academically presentable dashboards:
>
> 1. **Cybersecurity Threat Intelligence Dashboard** — Python + Streamlit + Plotly.
> 2. **Financial Market Analytics Dashboard** — Power BI.
>
> The projects must be usable with public datasets, explain their data preparation and analysis, and avoid fabricated results. Build a working project, not just a mockup.

---

# Shared project standards

## Academic context

- Subject: Big Data Analysis and Visualization.
- Expected level: Intermediate.
- Main goals: data cleaning, exploratory analysis, aggregation, interactive visualizations, and communicating useful findings.
- Provide a README explaining the project, dataset, setup, data dictionary, analytical questions, limitations, and how to run/view the dashboard.
- Use public or properly licensed datasets. Cite the source and include the download instructions; do not redistribute a dataset if its license prohibits it.
- Do not hard-code KPI values or make up results. Calculate every metric from the loaded data.
- If the real dataset is not present, provide a clearly labeled small synthetic sample only for testing. Never present synthetic sample results as real-world findings.
- Include a `DATASET_SETUP.md` explaining where to obtain the data, expected file names, required columns, and how to configure paths.
- Include a `DATA_DICTIONARY.md` describing fields, units, types, and interpretations.
- Make missing data, duplicates, parsing problems, and invalid values visible in a data-quality summary.
- Include a clear note that correlation and descriptive patterns do not by themselves prove causation.
- Do not use private personal or financial data.
- Use accessible colors, readable labels, clear legends, meaningful chart titles, and tooltips.
- Filters should work and should affect relevant visuals consistently.
- Include error handling for missing files, missing columns, and invalid data.
- Add comments to complex transformations and measures.
- Do not claim that a dashboard is real-time unless it has a real live data source and refresh mechanism.

## Deliverables

Create a parent folder with this structure:

```text
big-data-dashboards/
├── README.md
├── DASHBOARD_1_CYBERSECURITY_PYTHON.md
├── DASHBOARD_2_FINANCIAL_POWERBI.md
├── DATASET_SETUP.md
├── DATA_DICTIONARY.md
├── cybersecurity-python/
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   ├── data/
│   │   └── README.md
│   ├── src/
│   │   ├── data_loader.py
│   │   ├── data_cleaning.py
│   │   ├── metrics.py
│   │   └── charts.py
│   ├── tests/
│   │   └── test_metrics.py
│   └── .gitignore
└── financial-powerbi/
    ├── README.md
    ├── data/
    │   └── README.md
    ├── power-query/
    │   └── M_CODE_GUIDE.md
    ├── measures/
    │   └── DAX_MEASURES.md
    ├── model/
    │   └── DATA_MODEL.md
    └── screenshots/
        └── README.md
```

Create a `.pbix` file if the environment has Power BI Desktop and automation support. If it does not, do not falsely claim a PBIX was generated. Instead, deliver complete step-by-step Power BI instructions, Power Query M guidance, DAX measures, model relationships, and page designs so the user can build it in Power BI Desktop.

---

# Dashboard 1 — Cybersecurity Threat Intelligence Dashboard

## 1. Project title

**Cybersecurity Threat Intelligence: Big Data Analysis and Visualization of Network Traffic**

## 2. Goal

Analyze a public network intrusion detection dataset to understand the distribution of traffic labels, changes in traffic over time, protocol patterns, and potentially suspicious traffic characteristics. Present the analysis in an interactive dashboard.

This is a retrospective dataset analytics project, not a live Security Operations Center (SOC) monitor. Do not imply that the dashboard detects live attacks.

## 3. Recommended stack

- Python 3.10 or newer (use a version compatible with all dependencies).
- Streamlit for the UI.
- Pandas for data processing in the default implementation.
- Plotly Express / Plotly Graph Objects for interactive charts.
- Pytest for basic tests.
- Optional extension: PySpark for larger files or a demonstrated distributed-processing comparison. Do not require Spark to run the baseline dashboard.
- Optional extension only if time allows: compare Pandas and PySpark processing time on the same sufficiently large input and document hardware, dataset size, and timing methodology.

## 4. Dataset

Preferred source: CIC-IDS2017 from the Canadian Institute for Cybersecurity.

Official dataset catalogue:
https://www.unb.ca/cic/datasets/

Use a relevant CIC-IDS2017 CSV file or a selected set of files from the dataset. The data can contain columns for timestamps, network flow features, protocol, source/destination IP addresses and ports, and a traffic label. Exact columns differ by file and export format.

### Dataset handling requirements

1. Do not assume every expected column exists.
2. At startup, inspect available columns and show a helpful error if the required label field cannot be identified.
3. Allow the user to upload a CSV using Streamlit's file uploader, as well as load a configured local file.
4. Include a dataset configuration option for the label column. Default to `Label` if present; otherwise look for case-insensitive candidates such as `label` or `class`. If no candidate exists, ask the user to select one.
5. Trim leading/trailing whitespace from column names and label strings.
6. Convert numeric-looking columns safely; do not convert IP addresses or labels into numbers.
7. Handle common infinite values in numeric fields and report how they were handled.
8. Make duplicate removal a visible option, not an undocumented silent change. Report the number of duplicates found and removed.
9. Do not load huge files entirely into memory without warning. Provide a documented row limit/sample option for constrained machines and clearly state when analysis uses a sample.
10. If multiple CSVs are supported, validate compatible columns before concatenating. Add a source-file field when combining files.
11. Keep a data-quality report containing original row count, cleaned row count, duplicate count, missing-value counts, and any rows excluded.
12. Never assume a particular benign-label spelling. Detect the likely normal/benign category from available labels, show the detected category to the user, and let them override it. If no normal category can be identified confidently, disable benign-versus-other metrics and explain why.

## 5. Main questions the dashboard should answer

- What is the total number of traffic records in the selected data?
- How are records distributed across the dataset's labels?
- How does traffic volume vary over time, if a usable timestamp exists?
- Which protocols occur most frequently, if a protocol field exists?
- Which network flow features show different distributions across labels?
- What data-quality issues were present?
- Which filters change the observed patterns?

Do not call a record a confirmed incident simply because its label is non-benign. Prefer terms such as “attack-labeled records” and “dataset label.”

## 6. UI / visual design

Create a polished, professional security analytics dashboard. Use a restrained dark navy/charcoal base, readable text, and teal/cyan accents; use amber or red sparingly for risk-related emphasis. Maintain sufficient contrast and avoid excessive neon effects.

### Header

- Title: **Cybersecurity Threat Intelligence Dashboard**
- Subtitle: **Big Data Analysis & Visualization of Network Traffic**
- A compact explanatory caption: “Retrospective analysis of the selected public dataset; not a live monitoring service.”
- Show selected dataset name and whether all rows or a sample are being analyzed.

### Sidebar controls

- CSV upload control.
- Dataset/file selector if multiple configured files are available.
- Label-column selector.
- Date/time range filter if a timestamp column is available and parses successfully.
- Traffic-label multiselect.
- Protocol multiselect if a protocol field exists.
- Duplicate-handling option.
- Optional row limit/sample control with a visible warning when sampling is enabled.
- “Reset filters” guidance or a reset mechanism.
- All controls must update the relevant metrics, charts, and table consistently.

### Page layout

Use Streamlit tabs or sections:

1. **Overview**
2. **Traffic & Attack Patterns**
3. **Feature Analysis**
4. **Data Quality**
5. **Dataset Explorer**

### Overview page

Show KPI cards calculated from the currently filtered records:

- Records analyzed.
- Attack-labeled records, only if a normal/benign category was confidently identified or manually selected.
- Percentage of attack-labeled records, under the same condition.
- Number of distinct labels.
- Optional unique source IP count if the column exists.

For every KPI, add a tooltip or caption clarifying the definition.

Visualizations:
- Bar chart of record counts by label; sort by count.
- Line chart of record count over time using a suitable time bucket if timestamp is available.
- Protocol distribution chart if a protocol field exists. Use a bar chart when categories are numerous; use a pie/donut chart only when there are few meaningful categories.

### Traffic & Attack Patterns page

- Horizontal bar chart of the most frequent labels.
- Time-series chart by hour/day depending on dataset span and record density.
- Heatmap of weekday versus hour only if timestamp data is valid and there are enough observations.
- Protocol-by-label stacked bar chart only if both fields exist and the number of categories remains readable.
- A top-source table only if source IP is present; explain that source IPs in a dataset may be private, anonymized, or lab-generated.
- Optional source/destination port analysis only if appropriate columns exist.
- Do not geolocate IP addresses by default. If a map is added later, document the geolocation source, uncertainty, and limitations.

### Feature Analysis page

- Let the user select one numeric feature and optionally a second feature.
- Show summary statistics: count, mean, median, standard deviation, minimum, and maximum, where valid.
- Show a histogram of the selected feature.
- Compare selected feature distributions across labels using box plots or violin plots. Limit displayed categories or let users select a small number to avoid unreadable charts.
- Optional scatter plot of two numeric features, colored by label, with sampling for performance and a clear sampling indicator.
- Handle heavily skewed values and extreme outliers without silently deleting them. Explain any log transformation or clipping.

### Data Quality page

Show:
- Original rows and columns.
- Cleaned rows and columns.
- Duplicates detected and removed.
- Missing values by column.
- Invalid or unparseable timestamps.
- Numeric columns with non-finite values.
- Number of rows excluded by filters or sampling, where measurable.
- Warnings for absent optional fields.
- A short generated quality summary based on actual computed results. Do not fabricate explanatory findings.

### Dataset Explorer page

- Searchable/filterable table with pagination or a sensible row cap.
- Let users choose displayed columns.
- Never render millions of rows at once.
- Display a clear note if the table is capped to a subset.
- Allow downloading the currently filtered subset as CSV, with sensible size limits and privacy/source caveats.
- Escape or safely display uploaded data; do not execute content from files.

## 7. Metrics and definitions

Implement metrics in a separate module so they can be tested.

- `records_analyzed`: number of records after the documented cleaning steps and active filters.
- `distinct_labels`: number of distinct non-null label values in the current view.
- `attack_labeled_records`: number of records whose label is not the selected normal/benign label, only when a normal label is selected.
- `attack_labeled_percentage`: attack-labeled records / total labeled records × 100. Guard against a zero denominator.
- `unique_source_ips`: distinct non-null source IP values, only if the field exists.
- `records_over_time`: counts per selected time bucket; only if a valid timestamp field exists.
- `records_by_protocol`: counts by protocol; only if a protocol field exists.
- `missing_values_by_column`: null count per column.
- `duplicate_rows`: duplicate count before optional removal.

Do not interpret dataset class counts as real-world attack rates unless the dataset sampling methodology supports that conclusion.

## 8. Suggested code responsibilities

- `src/data_loader.py`
  - Read local CSVs and uploaded CSVs.
  - Validate file size, parsing errors, encoding issues, and required fields.
  - Return a structured load result with warnings.
- `src/data_cleaning.py`
  - Normalize column names and strings.
  - Detect label, timestamp, protocol, source-IP, and numeric columns.
  - Make cleaning choices explicit and produce a data-quality report.
- `src/metrics.py`
  - Pure functions for counts, percentages, grouped summaries, and quality metrics.
- `src/charts.py`
  - Plotly figure functions; do not mix chart-building logic with data loading.
- `app.py`
  - Layout, sidebar controls, page navigation/tabs, filtered state, metric cards, and CSV download.
- `tests/test_metrics.py`
  - Test correct counts, empty datasets, missing labels, zero denominators, optional columns, and duplicate handling.

Use Streamlit caching carefully. Cache stable data loading/cleaning results only when cache keys account for file identity or upload content. Do not allow one uploaded file's results to appear for a different upload.

## 9. Robustness and accessibility

- Provide helpful messages rather than raw stack traces for common file and schema errors.
- Do not crash when optional columns are missing.
- Support empty filtered results gracefully.
- Use consistent number formatting.
- Include chart titles, axis titles, legends, and tooltips.
- Keep text readable and avoid relying only on color to communicate category.
- Use deterministic sampling for scatter plots so a refresh does not randomly change the displayed sample.
- Ensure the application starts with the supplied synthetic test fixture even if the full public dataset has not yet been downloaded; clearly label it as synthetic.
- Never silently invent data or claim the synthetic fixture represents CIC-IDS2017.

## 10. Run instructions

`requirements.txt` should list compatible versions or sensible minimum versions for Streamlit, Pandas, Plotly, and Pytest.

Document the following commands:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

If the selected dataset is not downloaded, explain how to obtain it from the official dataset catalogue and where to place it, or how to upload it through the UI.

## 11. Tests / acceptance criteria

The project is acceptable when:

- The app starts using the documented commands.
- It can load the synthetic fixture and a compatible real CSV.
- All metrics are computed from the actual data.
- Every available filter affects relevant visualizations.
- Missing optional columns do not crash the app.
- Invalid/missing label columns produce a helpful message.
- Empty filtered data displays a useful empty state.
- CSV download contains only the filtered subset.
- Data quality details are visible.
- Automated metric tests pass.
- README includes data source, methodology, limitations, and exact run steps.
- No fake “live” claims, invented results, or undocumented preprocessing remain.

## 12. Academic report material to generate

Create a short `PROJECT_REPORT_NOTES.md` with:
- Problem statement.
- Objectives.
- Dataset and citation.
- System architecture.
- Data preprocessing.
- Metrics and visualization rationale.
- Big data relevance and limitations.
- Actual findings populated only after a real dataset has been loaded.
- Future scope: Spark-based distributed processing, streaming ingestion, or validated anomaly detection.

---

# Dashboard 2 — Financial Market Analytics Dashboard (Power BI)

## 1. Project title

**Financial Market Analytics: Interactive Stock Performance and Volatility Dashboard**

## 2. Goal

Create an interactive Power BI report that explores historical stock prices, returns, trading volume, and volatility across multiple selected stocks. It is an educational historical-data analysis project, not financial advice or a trading recommendation.

## 3. Technology

- Microsoft Power BI Desktop.
- Power Query for data import and transformation.
- DAX for measures.
- Power BI relationships and a star-schema-style model where practical.
- Public historical stock data in CSV format.
- Optional Power BI Service publishing only if the user has access and is permitted to publish the data.

Official Power BI learning documentation:
https://learn.microsoft.com/power-bi/

## 4. Dataset plan

Use historical daily OHLCV data (Open, High, Low, Close, Volume) for a small selection of stocks or indices. Start with 3–5 well-known, non-sensitive symbols to keep the model manageable. The user may choose Indian or US securities depending on data availability and the assignment's scope.

Potential source: Stooq historical data or another reputable public source with a clear download method and terms. Verify the selected source and ticker availability before writing final dataset instructions. Do not hard-code a claim that a ticker or endpoint works without checking.

Data requirements:
- `Date`
- `Ticker` or `Symbol`
- `Open`
- `High`
- `Low`
- `Close` or adjusted close, if available
- `Volume`
- Optional `Company` and `Sector` lookup fields, only where verified.

If the chosen source provides one file per ticker, combine them in Power Query and add a ticker column before appending. Ensure all files use the same column names and units.

### Data quality rules

- Parse dates using the correct locale/format.
- Ensure prices are numeric and volume is numeric.
- Remove duplicate `(Date, Ticker)` rows only after reporting them.
- Handle missing prices explicitly; do not automatically fill missing trading dates with fabricated prices.
- Sort by ticker and date before computing previous trading-day comparisons.
- Do not treat non-trading days as missing data requiring interpolation.
- Be explicit about whether close or adjusted close is used.
- Explain that adjusted close may account for corporate actions, depending on source definitions.
- Do not compare absolute prices as if they were comparable across different companies without context.
- Do not make investment recommendations.

## 5. Data model

Create a fact table called `FactStockPrices` with:
- DateKey or Date
- TickerKey or Ticker
- Open
- High
- Low
- Close
- AdjustedClose, if available
- Volume
- DailyReturnPct, calculated carefully
- Optional DailyRangePct

Create a proper `DimDate` calendar table covering the minimum to maximum dates in the data. Include:
- Date
- Year
- Quarter
- MonthNumber
- MonthName
- YearMonth
- Day
- DayOfWeek
- IsWeekend (calendar attribute only; do not infer trading sessions from weekends alone).

Create a `DimTicker` table with unique ticker symbols and verified company/sector metadata where available.

Relationships:
- `DimDate[Date]` one-to-many to `FactStockPrices[Date]`.
- `DimTicker[Ticker]` one-to-many to `FactStockPrices[Ticker]`.
- Prefer single-direction filtering from dimensions to fact table.
- Ensure the date table is marked as a date table in Power BI.
- Avoid ambiguous many-to-many relationships unless explicitly justified.

If a simplified one-table model is needed, document the trade-off. Prefer the star schema for demonstrating data modeling.

## 6. Power Query procedure

Write detailed step-by-step instructions in `power-query/M_CODE_GUIDE.md`.

1. Use **Get Data → Text/CSV** to import the CSV files or use **Get Data → Folder** if each ticker has a separate file.
2. Preview the data and confirm delimiters, headers, and locale.
3. Promote headers if necessary.
4. Rename fields to consistent names.
5. Add a `Ticker` column for each source file if missing.
6. Set types: Date, Decimal Number for prices, Whole Number or appropriate numeric type for volume.
7. Trim text and clean ticker labels.
8. Check and report nulls.
9. Identify duplicate `(Date, Ticker)` pairs and report them before removing them.
10. Filter rows with invalid dates or impossible numeric parse results, reporting how many were excluded.
11. Do not replace missing prices with zero.
12. Append ticker files into a single fact table.
13. Create/reference a distinct ticker dimension.
14. Create a date dimension in DAX or Power Query and relate it to the fact table.
15. Close & Apply.
16. Document any source-specific adjustments and data exclusions.

Provide M-code examples where useful, but do not invent a source-specific URL that has not been verified.

## 7. DAX measures

Create `measures/DAX_MEASURES.md` with copyable DAX formulas and explanations. Adjust table/column names to match the final model. Include measures for:

### Basic metrics

```dax
Total Trading Records =
COUNTROWS(FactStockPrices)
```

```dax
Latest Available Date =
MAX(FactStockPrices[Date])
```

```dax
Selected Ticker Count =
DISTINCTCOUNT(FactStockPrices[Ticker])
```

```dax
Total Trading Volume =
SUM(FactStockPrices[Volume])
```

### Closing price measures

```dax
Latest Close =
VAR LatestDateInContext =
    MAX(FactStockPrices[Date])
RETURN
    CALCULATE(
        MAX(FactStockPrices[Close]),
        FactStockPrices[Date] = LatestDateInContext
    )
```

Important: For multiple tickers, a single card showing `Latest Close` can be ambiguous. Configure the card to require one selected ticker, or use a ticker-specific visual. Validate the measure with the chosen filter context.

### Daily return

Prefer calculating the previous available close for each ticker in Power Query or in a validated calculated-column pattern, after sorting/grouping by ticker and date. Avoid comparing to the previous calendar date when no trading record exists.

If `DailyReturnPct` is a decimal fraction, define the measure consistently, e.g.:

```dax
Average Daily Return % =
AVERAGE(FactStockPrices[DailyReturnPct]) * 100
```

If `DailyReturnPct` is already stored as percentage points (e.g., 1.5 for 1.5%), do not multiply by 100. Document the chosen storage convention.

### Price change

Provide a validated previous-close comparison that respects ticker and date context, or use a precomputed `DailyReturnPct`/`DailyChange` column generated per ticker in Power Query. Do not use an incorrect measure that simply subtracts the prior calendar date if the market was closed.

### Volatility

Provide a measure for the standard deviation of daily returns in the selected date range, and clearly state whether the result is daily volatility or annualized volatility. If annualizing, document the chosen convention and assumptions (for example, a commonly used 252 trading-day convention) rather than presenting it as a universal truth.

### Other useful measures

- Highest Close in Selected Period.
- Lowest Close in Selected Period.
- Average Trading Volume.
- Trading Days Count.
- Daily Range percentage if OHLC fields are available and values are valid.
- Percentage of positive-return trading days, with zero-denominator protection.
- Period start/end dates.

All measures must respect report filters unless a specific measure is intentionally designed otherwise. Include test/check steps for DAX measures.

## 8. Power BI report pages

Create a polished report with 3 pages, consistent formatting, meaningful titles, and a common slicer strategy.

### Page 1 — Market Overview

**Purpose:** Give a quick view of the selected market data.

KPI cards:
- Latest available date.
- Number of selected tickers.
- Total trading records.
- Total trading volume (with a clear unit/format).

Visuals:
- Line chart: closing price over time, with ticker as legend or a ticker selector. Do not put stocks with radically different price scales on the same axis without explaining the comparison.
- Bar chart: percentage return over the selected period by ticker.
- Bar chart: trading volume by ticker.
- Optional table: latest available date and close per ticker.

Slicers:
- Date range.
- Ticker.
- Optional sector only if verified sector metadata is present.

### Page 2 — Price & Return Analysis

Visuals:
- Line chart: closing or adjusted closing price over time.
- Line chart: cumulative return indexed to 100 at the beginning of the selected period, if implemented correctly.
- Bar chart: daily returns by date for a selected ticker.
- Histogram-like distribution of daily returns using a suitable binning approach if feasible in Power BI.
- KPI cards: highest close, lowest close, average daily return, and standard deviation of daily returns.
- Date and ticker filters.

Important: Clearly state whether close or adjusted close is used. Explain that different share prices do not directly indicate which stock performed better; compare percentage returns or indexed performance.

### Page 3 — Volume & Volatility

Visuals:
- Line chart: daily trading volume over time.
- Scatter chart: daily return versus volume, if the model supports the relationship cleanly.
- Bar chart: volatility by ticker for the selected period.
- Matrix: ticker by month with average return, trading volume, and volatility where available.
- Optional heatmap-like matrix of monthly returns, using conditional formatting.

Slicers:
- Date range.
- Ticker.
- Year/month.

### Interactions

- All slicers should work predictably across relevant pages.
- Use **View → Sync slicers** for date/ticker slicers where appropriate.
- Configure visual interactions so a selection filters or highlights relevant charts.
- Add report-page tooltips for definitions when useful.
- Add clear page navigation buttons.
- Include a reset-filters/bookmark option if feasible.
- Avoid overloading pages with too many charts.
- Use consistent number formats, units, and decimal precision.
- Use accessible contrast and do not rely on color alone.

## 9. Visual style

Use a premium financial analytics theme:
- Light neutral or dark navy base, but maintain readable contrast.
- One primary accent and limited secondary colors.
- Green/red may represent positive/negative returns, but include signs and labels so meaning is not color-only.
- KPI cards with concise titles.
- Consistent font hierarchy.
- No excessive gradients, decorative graphics, or 3D charts.
- Add a small footer: “Historical data for educational analysis only. Not investment advice.”

## 10. Data refresh and limitations

- The baseline dashboard is based on downloaded historical data and is not live.
- Document the date on which data was downloaded.
- Explain how to replace/append CSVs and refresh in Power BI.
- If Power BI Service is used, explain that scheduled refresh depends on data source accessibility, gateway requirements, and the user's account/workspace capabilities.
- Do not promise automatic refresh for local files without appropriate configuration.
- Do not scrape sites in ways that violate their terms.
- Do not use a stock-price API requiring credentials unless the user explicitly chooses it and can configure their own key securely.

## 11. Power BI acceptance criteria

- Power BI report contains three usable pages or complete instructions to create them.
- Data model and relationships are documented.
- Power Query transformations are reproducible.
- DAX measures have definitions and format instructions.
- Date and ticker slicers filter all relevant visuals.
- Returns are calculated against the previous available trading observation for the same ticker.
- Missing dates are not fabricated.
- Latest-close measures are validated for single-ticker and multi-ticker contexts.
- Visuals use clear units and avoid misleading price comparisons.
- Source and download date are documented.
- The report includes a visible educational-use disclaimer.
- Do not claim a `.pbix` file exists unless it was actually generated and verified.

## 12. Academic report material

Create `PROJECT_REPORT_NOTES.md` containing:
- Problem statement.
- Objectives.
- Data source and date downloaded.
- Data preparation in Power Query.
- Data model and relationships.
- DAX measure definitions.
- Visualization rationale.
- Actual findings based only on loaded source data.
- Limitations and future scope.

---

# Shared final checklist for the AI builder

Before declaring either dashboard complete:

1. Read this entire specification before coding.
2. Build both projects as separate implementations; do not mix Power BI steps into the Python app or vice versa.
3. Create every file listed in the structure or document clearly why a deliverable cannot be generated in the current environment.
4. Ensure the Python dashboard can run without a real dataset by using an explicitly synthetic test fixture; include a visible synthetic-data warning.
5. Do not claim Power BI Desktop automation or PBIX generation unless actually available.
6. Keep setup steps explicit for a Windows student environment.
7. Do not commit API keys, credentials, private data, or large datasets to source control.
8. Include `.gitignore` entries for virtual environments, caches, private configuration, and large downloaded datasets.
9. Validate calculations using small known test cases.
10. Check for broken imports, inconsistent column names, and incorrect paths.
11. Do not invent performance benchmarks, dataset sizes, or analytical conclusions.
12. Provide a final handoff summary listing files created, commands to run, dataset setup, what is complete, what needs manual Power BI steps, and any known limitations.
13. Prefer a working, modest, robust dashboard over unnecessary features that cannot be completed or tested.
14. If anything is blocked, explain the exact blocker and provide the next action; do not silently omit requirements.
