# Cybersecurity Threat Intelligence Dashboard
## Big Data Analysis & Visualization of Network Traffic

An interactive, modular analytical dashboard built with **Python**, **Streamlit**, and **Plotly** to inspect, profile, and visualize network intrusion detection data (specifically conforming to the **CIC-IDS2017** benchmark schema).

---

## 📌 Project Overview & Purpose

Modern enterprise networks generate millions of flow records per hour. Identifying anomalous patterns, protocol anomalies, and malicious signatures requires systematic big data preprocessing, robust aggregation, and accessible visualization.

This project delivers a complete retrospective analytics platform answering:
1. **Volume & Class Distribution:** What is the total volume of network flows, and how are records distributed across benign traffic and attack labels?
2. **Temporal Dynamics:** How does traffic burst across hours of the day and days of the week?
3. **Protocol & Port Fingerprints:** Which transport protocols (TCP, UDP, ICMP) and service ports dominate specific attack types?
4. **Flow Feature Discrepancies:** Which statistical network flow metrics (e.g., packet lengths, flow durations, inter-arrival times) distinguish anomalous flows from baseline operations?
5. **Data Quality Integrity:** What proportion of records contain missing attributes, duplicate transmissions, non-finite flow rates, or unparseable timestamps?

> ⚠️ **Academic Disclaimer:** This is an offline retrospective analytics tool for historical dataset evaluation and model exploration. It is **not** an operational Security Operations Center (SOC) live monitoring platform, nor does it conduct automated live packet sniffing.

---

## 🏗️ System Architecture & Codebase Layout

```text
cybersecurity-python/
├── app.py                      # Main Streamlit dashboard UI and layout
├── requirements.txt            # Python dependencies
├── README.md                   # System documentation & usage instructions
├── PROJECT_REPORT_NOTES.md     # Academic project report notes & methodology
├── .gitignore                  # Git exclusions for environments & raw datasets
├── data/
│   ├── README.md               # Dataset download & provenance guide
│   └── synthetic_ids_sample.csv# Offline test fixture (1,500 records)
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Safe CSV ingestion, size check, encoding fallback
│   ├── data_cleaning.py        # Normalization, type guards, inf/null handling
│   ├── metrics.py              # Pure mathematical functions & KPIs
│   └── charts.py               # Plotly dark-navy theme figures
└── tests/
    ├── __init__.py
    └── test_metrics.py         # Automated pytest unit test suite (12 tests)
```

---

## 🚀 Quickstart & Setup (Windows / macOS / Linux)

### 1. Prerequisites
- Python 3.10 or newer (tested on Python 3.14).

### 2. Create Virtual Environment
Open PowerShell (Windows) or Terminal (macOS/Linux):

```bash
# Navigate to the project folder
cd big-data-dashboards/cybersecurity-python

# Create virtual environment
python -m venv .venv
```

### 3. Activate Virtual Environment
**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```
*(If script execution is restricted on Windows, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`)*

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Dashboard
```bash
streamlit run app.py
```
Streamlit will automatically open your default browser to `http://localhost:8501`.

---

## 🧪 Running Automated Unit Tests

A comprehensive unit test suite validates metric calculations, zero-division guards, duplicate handling, and schema anomalies:

```bash
python -m pytest tests/test_metrics.py -v
```

All 12 test assertions verify:
- Standard and zero-denominator KPI calculations.
- Handling empty DataFrames and absent columns.
- Detection of non-finite (infinite) values.
- Leading/trailing whitespace stripping.
- IANA protocol number translation (TCP, UDP, ICMP).
- Automatic benign category detection.

---

## 📊 Dashboard Modules & Tabs

### 1. Overview
- **Top KPIs:** Records Analyzed, Distinct Labels, Attack-Labeled Records, Attack Record Share %, and Unique Source IPs.
- **Label Bar Chart:** Ordered counts and percentage share per traffic category.
- **Protocol Distribution:** Interactive donut or bar chart of observed protocols.
- **Timeline:** Resample network flow volume by 15-minute, hourly, or daily increments.

### 2. Traffic & Attack Patterns
- **Label Frequency:** Ranked horizontal visualization highlighting threat categories.
- **Protocol-by-Label Breakdown:** Stacked composition revealing transport protocols used by each attack type.
- **Temporal Activity Heatmap:** 7-day × 24-hour matrix identifying diurnal traffic cycles and off-peak anomalies.
- **Top Source IPs & Destination Ports:** Frequency ranking with private/lab subnet scope attribution.

### 3. Feature Analysis
- **Numeric Feature Selectors:** Dynamic exploration of network flow metrics.
- **Summary Statistics:** Count, Mean, Median, Standard Deviation, Min/Max, and Skewness.
- **Histograms & Box Plots:** Distribution spreads and quartile comparisons across traffic classifications.
- **Bivariate Scatter:** Deterministically sampled scatter plot with class color-coding.

### 4. Data Quality & Preprocessing
- **Audit Metrics:** Raw vs cleaned record counts, duplicate tracking, and non-finite value replacements.
- **Missing Value Breakdown:** Attribute-level null counts and percentages.
- **Timestamp Integrity:** Validation of date-time parsing with NaT coercion diagnostics.

### 5. Dataset Explorer
- **Interactive Viewer:** Paginated data view with selective column filtering.
- **CSV Exporter:** Download filtered and cleaned session data for external reporting.

---

## 🛡️ Robustness & Accessibility Standards
- **High-Contrast Dark Theme:** Uses a restrained `#0f172a` slate palette with `#06b6d4` cyan accents.
- **Graceful Error Handling:** Never crashes on missing optional fields (e.g., absent IPs or protocol headers).
- **Sampling Guard:** Deterministic downsampling preserves browser memory on large datasets.
