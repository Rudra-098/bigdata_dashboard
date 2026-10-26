# Dashboard 1: Cybersecurity Threat Intelligence Dashboard
## Technical Specification & Implementation Guide

---

## 🛡️ Overview & Objectives
The **Cybersecurity Threat Intelligence Dashboard** is an interactive analytical application built with **Python**, **Streamlit**, and **Plotly**. It provides retrospective big data analysis and visualization of network intrusion detection datasets conforming to the **CIC-IDS2017** benchmark schema.

### Core Analytical Capabilities
- **Volumetric Profiling:** Computes exact record counts, attack distributions, and distinct traffic classification shares.
- **Temporal Analysis:** Visualizes traffic flow velocity across user-selectable time windows (15-minute, hourly, daily) and maps diurnal density via weekday-hour heatmaps.
- **Protocol & Endpoint Footprints:** Attributes threat patterns to transport layer protocols (TCP, UDP, ICMP) and target destination ports.
- **Statistical Feature Exploration:** Surfaces univariate histograms, summary metrics (mean, median, standard deviation, skewness), and bivariate scatter comparisons across network flow metrics.
- **Data Quality Auditing:** Delivers transparent metrics on duplicate removal, non-finite flow rate replacements (`np.inf` to `NaN`), and timestamp parsing integrity.

---

## 🏗️ Architecture & Modules

The implementation is located inside `big-data-dashboards/cybersecurity-python/`:

| Module Path | Primary Responsibility |
| :--- | :--- |
| `app.py` | UI layout, sidebar controls, filter engines, metric cards, tab navigation, and CSV export. |
| `src/data_loader.py` | Multi-encoding CSV reading (`utf-8`, `latin-1`), file size safety checks, and deterministic row sampling. |
| `src/data_cleaning.py` | Column whitespace stripping, infinite value coercion, duplicate tracking, and benign baseline detection. |
| `src/metrics.py` | Pure mathematical and aggregation functions (testable without UI dependencies). |
| `src/charts.py` | High-contrast dark navy Plotly figures adhering to cybersecurity visualization design standards. |
| `tests/test_metrics.py` | Comprehensive Pytest unit tests (12 tests covering edge cases, nulls, and divisions). |

---

## 🚀 Execution Instructions

### 1. Environment Setup (PowerShell)
```powershell
cd big-data-dashboards\cybersecurity-python
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run Automated Pytest Suite
```powershell
python -m pytest tests/test_metrics.py -v
```

### 3. Launch Streamlit Application
```powershell
streamlit run app.py
```
Open `http://localhost:8501` in your web browser.

---

## 📊 Detailed Tab Specifications

1. **Tab 1: Overview:**
   - 5 KPI summary cards: Records Analyzed, Distinct Labels, Attack-Labeled Records, Attack Record Share %, and Unique Source IPs.
   - Categorical label frequency bar chart.
   - Protocol composition donut chart.
   - Resampled traffic volume timeline line chart.

2. **Tab 2: Traffic & Attack Patterns:**
   - Horizontal label distribution chart.
   - Protocol-by-label stacked composition bar chart.
   - Weekday vs Hour activity density heatmap.
   - Top 10 most active Source IP addresses (with private/lab subnet scope attribution).
   - Top destination ports with common network service mappings (80=HTTP, 443=HTTPS, 21=FTP, 22=SSH).

3. **Tab 3: Feature Analysis:**
   - Primary and secondary numeric flow feature selectors.
   - Comprehensive summary statistics table: Count, Mean, Median, Std Dev, Min/Max, and Skewness.
   - Feature distribution histogram with customizable binning.
   - Feature quartile distribution box plot comparing the top traffic classes.
   - Bivariate scatter plot with deterministic sampling to maintain browser fluidity.

4. **Tab 4: Data Quality & Preprocessing:**
   - Raw vs Cleaned record counts and duplicate tracking.
   - Attribute-level missing value counts and percentages.
   - Timestamp parsing audit metrics.
   - Preprocessing audit log documenting all normalization and infinite-value handling rules.

5. **Tab 5: Dataset Explorer:**
   - Interactive data table with custom column selection and row viewing caps.
   - Filtered dataset CSV export button.
