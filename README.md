# Big Data Analysis and Visualization — Project Workspaces

Welcome to the **Big Data Analysis & Visualization Dashboard Project**.

All source code, datasets, tests, Power BI assets, and documentation are located in the `big-data-dashboards/` directory:

```text
big-data-dashboards/
├── README.md                           # Master Project Overview & Setup Guide
├── DASHBOARD_1_CYBERSECURITY_PYTHON.md # Dashboard 1 (Python / Streamlit) Specifications
├── DASHBOARD_2_FINANCIAL_POWERBI.md    # Dashboard 2 (Power BI) Specifications
├── DATASET_SETUP.md                    # Data Provenance, Acquisition & Path Setup
├── DATA_DICTIONARY.md                  # Comprehensive Data Dictionary
├── cybersecurity-python/               # Python + Streamlit + Plotly Threat Intel Dashboard
└── financial-powerbi/                  # Microsoft Power BI Financial Analytics Dashboard
```

To run Dashboard 1:
```powershell
cd big-data-dashboards\cybersecurity-python
pip install -r requirements.txt
streamlit run app.py
```

To run unit tests:
```powershell
python -m pytest big-data-dashboards\cybersecurity-python\tests\test_metrics.py -v
```

For full details, please refer directly to [`big-data-dashboards/README.md`](./big-data-dashboards/README.md).
