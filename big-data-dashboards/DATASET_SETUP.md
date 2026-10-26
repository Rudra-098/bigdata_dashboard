# Dataset Setup & Configuration Guide
## Subject: Big Data Analysis and Visualization

This guide provides instructions on where to acquire official public datasets, expected schemas, directory placement, and configurations for both dashboards.

---

# 1. Dashboard 1: Cybersecurity Threat Intelligence

### Preferred Official Benchmark: CIC-IDS2017
- **Host Institution:** Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB).
- **Catalogue URL:** [https://www.unb.ca/cic/datasets/ids-2017.html](https://www.unb.ca/cic/datasets/ids-2017.html)
- **Direct Zip Archive:** `GeneratedLabelledFlows.zip`

### Recommended File Choices
Any of the following extracted CSV files can be directly ingested into the dashboard:
1. `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` (High DDoS volumes)
2. `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv` (Port reconnaissance)
3. `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv` (SQL injection, XSS, Brute force)

### Expected Key Columns
- Target/Label: `Label` (or `label`, `class`)
- Timing: `Timestamp` (format: `dd/mm/yyyy hh:mm:ss` or standard ISO)
- Flow features: `Flow Duration`, `Total Fwd Packets`, `Total Backward Packets`, `Flow Bytes/s`, `Flow Packets/s`
- Network fields: `Protocol`, `Destination Port`, `Source IP`

### How to Configure & Ingest
1. **Option A (Instant Offline Testing):** Launch `streamlit run app.py` and leave the sidebar set to **"Synthetic Sample Fixture"**. The pre-packaged 1,500-record fixture will load instantly.
2. **Option B (Streamlit File Uploader):** Select **"Upload CSV File"** in the sidebar and browse to your extracted CIC-IDS2017 CSV file.
3. **Option C (Local Path):** Place your extracted CSV in `big-data-dashboards/cybersecurity-python/data/` and enter its absolute path in the **"Local File Path"** sidebar input.

---

# 2. Dashboard 2: Financial Market Analytics

### Preferred Public Source: Stooq / Yahoo Finance
- **Host Repository:** [Stooq Historical Daily Quotes](https://stooq.com) or [Yahoo Finance](https://finance.yahoo.com)
- **Asset Selection:** 4 leading US large-cap equities (`AAPL`, `MSFT`, `GOOGL`, `AMZN`) across the 2023 calendar trading year.

### Provided Ready-to-Use Datasets
For grading and evaluation, complete datasets are pre-generated and located in `big-data-dashboards/financial-powerbi/data/`:
- `AAPL.csv` (250 trading rows)
- `MSFT.csv` (250 trading rows)
- `GOOGL.csv` (250 trading rows)
- `AMZN.csv` (250 trading rows)
- `FactStockPrices_Combined.csv` (1,000 trading rows combining all 4 assets)
- `DimTicker.csv` (Company Name & Sector metadata)
- `DimDate.csv` (365 calendar days for 2023)

### How to Configure in Power BI Desktop
1. Open **Microsoft Power BI Desktop**.
2. Click **Get Data → Text/CSV**.
3. Select `FactStockPrices_Combined.csv`, `DimTicker.csv`, and `DimDate.csv`.
4. Click **Close & Apply**.
5. Switch to **Model View** and link `DimDate[Date] (1)` to `FactStockPrices[Date] (*)` and `DimTicker[Ticker] (1)` to `FactStockPrices[Ticker] (*)`.

---

## 🔒 Academic Licensing & Privacy Safeguards
- All data utilized in this project is strictly public, non-personal, and non-confidential.
- No real-time production credentials, API secret keys, or proprietary data are committed to the codebase.
