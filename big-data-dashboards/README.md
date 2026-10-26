# Big Data Analysis & Visualization — Academic Dashboard Suite
## Course: Big Data Analysis and Visualization

This repository contains two complete, professionally engineered, academically presentable dashboards built in accordance with the course specifications:

1. **Dashboard 1: Cybersecurity Threat Intelligence Dashboard**
   - **Stack:** Python 3.10+ | Streamlit | Plotly Express & Graph Objects | Pandas | Pytest
   - **Data Domain:** Network intrusion detection flow telemetry conforming to the **CIC-IDS2017** benchmark.
   - **Status:** Fully executable locally with a synthetic offline test fixture and full compatibility with real CIC-IDS2017 public CSVs. Includes 12 automated unit tests.

2. **Dashboard 2: Financial Market Analytics Dashboard**
   - **Stack:** Microsoft Power BI Desktop | Power Query (M Language) | DAX | Dimensional Modeling (Star Schema)
   - **Data Domain:** Historical daily equity OHLCV market feeds across 4 large-cap equities (`AAPL`, `MSFT`, `GOOGL`, `AMZN`) for 2023.
   - **Status:** Complete production-ready data assets, Power Query M transformation guides, copyable DAX measure formulas, Star Schema relational definitions, and 3-page visual wireframes.

---

## 🗂️ Repository Architecture

```text
big-data-dashboards/
├── README.md                               # This master documentation
├── DASHBOARD_1_CYBERSECURITY_PYTHON.md     # Detailed specification for Dashboard 1
├── DASHBOARD_2_FINANCIAL_POWERBI.md        # Detailed specification for Dashboard 2
├── DATASET_SETUP.md                        # Provenance, download links, and path setups
├── DATA_DICTIONARY.md                      # Detailed data dictionary across all fields
│
├── cybersecurity-python/                   # Dashboard 1 Implementation
│   ├── app.py                              # Streamlit application UI
│   ├── requirements.txt                    # Python dependencies
│   ├── README.md                           # Python project guide & run steps
│   ├── PROJECT_REPORT_NOTES.md             # Academic report notes & methodology
│   ├── .gitignore                          # Git exclusions
│   ├── data/
│   │   ├── README.md                       # CIC-IDS2017 data guide
│   │   └── synthetic_ids_sample.csv        # Offline test fixture (1,500 records)
│   ├── src/
│   │   ├── __init__.py
│   │   ├── data_loader.py                  # Ingestion, encoding fallback, row sampling
│   │   ├── data_cleaning.py                # Normalization, inf coercion, deduplication
│   │   ├── metrics.py                      # Pure mathematical aggregations & KPIs
│   │   └── charts.py                       # Plotly dark navy theme figures
│   └── tests/
│       ├── __init__.py
│       └── test_metrics.py                 # Automated unit tests (12 tests)
│
└── financial-powerbi/                      # Dashboard 2 Implementation
    ├── README.md                           # Power BI setup and build guide
    ├── PROJECT_REPORT_NOTES.md             # Academic report notes & methodology
    ├── data/
    │   ├── README.md                       # Data provenance & financial dictionary
    │   ├── AAPL.csv                        # Apple Inc. 2023 trading records
    │   ├── MSFT.csv                        # Microsoft Corp. 2023 trading records
    │   ├── GOOGL.csv                       # Alphabet Inc. 2023 trading records
    │   ├── AMZN.csv                        # Amazon.com Inc. 2023 trading records
    │   ├── FactStockPrices_Combined.csv    # Combined fact table (1,000 rows)
    │   ├── DimTicker.csv                   # Company and sector lookup dimension
    │   └── DimDate.csv                     # 365-day calendar dimension table
    ├── power-query/
    │   └── M_CODE_GUIDE.md                 # Power Query ETL & M script reference
    ├── measures/
    │   └── DAX_MEASURES.md                 # Copyable DAX formulas with format strings
    ├── model/
    │   └── DATA_MODEL.md                   # Star Schema architecture & date marking
    └── screenshots/
        └── README.md                       # 3-Page visual layouts & theme palette
```

---

## ⚡ Quickstart Guide

### 🚀 Running Dashboard 1 (Python / Streamlit)
```powershell
# 1. Navigate to the Python dashboard folder
cd big-data-dashboards\cybersecurity-python

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install requirements
pip install -r requirements.txt

# 4. Run automated test suite
python -m pytest tests/test_metrics.py -v

# 5. Launch the Streamlit application
streamlit run app.py
```
*The browser will open to `http://localhost:8501`. By default, the app boots instantly with the offline synthetic fixture (`synthetic_ids_sample.csv`). To evaluate full research data, select "Upload CSV File" or "Local File Path" in the sidebar.*

---

### 📊 Building Dashboard 2 (Power BI Desktop)
1. Launch **Microsoft Power BI Desktop**.
2. Click **Get Data → Text/CSV** and select the pre-formatted tables in `financial-powerbi/data/`:
   - `FactStockPrices_Combined.csv` (Renamed to `FactStockPrices`)
   - `DimTicker.csv`
   - `DimDate.csv`
3. Switch to **Model View** and establish 1:N single-direction relationships:
   - `DimDate[Date]` → `FactStockPrices[Date]`
   - `DimTicker[Ticker]` → `FactStockPrices[Ticker]`
4. Right-click `DimDate` → **Mark as date table**.
5. Create a `_Measures` table and paste the DAX expressions from [`financial-powerbi/measures/DAX_MEASURES.md`](./financial-powerbi/measures/DAX_MEASURES.md).
6. Assemble the 3 report pages (**Market Overview**, **Price & Return Analysis**, **Volume & Volatility**) using the layout wireframes in [`financial-powerbi/screenshots/README.md`](./financial-powerbi/screenshots/README.md).

---

## 🛡️ Academic Integrity & Quality Standards

- **Zero Hard-Coded Metrics:** Every metric in both dashboards is computed dynamically from loaded datasets.
- **Transparent Data Cleaning:** Non-finite flow rates (`Infinity`), missing values, duplicates, and unparseable timestamps are explicitly reported in an audit view.
- **Non-Trading Day Safeguard:** Financial returns are strictly calculated against the *preceding trading session* rather than arbitrary calendar dates, avoiding weekend distortion.
- **Single-Ticker Price Guard:** Absolute equity price comparison is suppressed when multiple tickers are selected to prevent mathematical fallacies.
- **Educational Disclaimers:** Visible notices clearly state that Dashboard 1 is a retrospective study (not a live SOC detector) and Dashboard 2 is an academic exploration (not investment advice).
