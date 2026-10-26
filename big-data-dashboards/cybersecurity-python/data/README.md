# Network Traffic Datasets for Threat Intelligence Analysis

This directory stores datasets used by the **Cybersecurity Threat Intelligence Dashboard**.

---

## 1. Provided Synthetic Sample: `synthetic_ids_sample.csv`

> ⚠️ **NOTICE:** This file contains **synthetic, simulated network flow observations (1,500 records)** designed specifically for offline testing, UI verification, automated pytest execution, and academic grading. It faithfully mirrors the feature schema, column names, and data types of the Canadian Institute for Cybersecurity (CIC) CIC-IDS2017 benchmark.

### Purpose of the Synthetic Fixture
- Enables the application to boot immediately without requiring multi-gigabyte downloads.
- Embeds controlled edge cases:
  - Non-finite flow rates (`Infinity`, `-Infinity`) common to zero-duration connection attempts.
  - Missing attribute values (`NaN`).
  - Known duplicate rows to verify deduplication metrics.
  - Multi-class labels (`BENIGN`, `DDoS`, `PortScan`, `Bot`, `FTP-Patator`).

---

## 2. Real-World Benchmark: CIC-IDS2017 Dataset

For genuine forensic research and academic presentation findings, utilize the **CIC-IDS2017** benchmark dataset provided by the Canadian Institute for Cybersecurity, University of New Brunswick (UNB).

### Official Catalogue & Download
- **Dataset Home:** [https://www.unb.ca/cic/datasets/ids-2017.html](https://www.unb.ca/cic/datasets/ids-2017.html)
- **Direct CSV Download Package:** `GeneratedLabelledFlows.zip` (approx 2.8 GB compressed).

### Recommended Files for Evaluation
- `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv` (High volume DDoS vs Benign traffic).
- `Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv` (Port scanning reconnaissance activity).
- `Thursday-WorkingHours-Morning-WebAttacks.pcap_ISCX.csv` (Brute force and web injection flows).

### How to Use With the Dashboard
1. Download and extract the chosen CSV file.
2. Either:
   - **Method A (Upload):** Start the dashboard, choose **"Upload CSV File"** in the sidebar, and browse to the extracted file.
   - **Method B (Local Path):** Place the CSV inside this `data/` folder and enter its relative/absolute path in the **"Local File Path"** sidebar input.
3. For low-RAM student hardware (< 16 GB), enable the **"Limit Rows"** toggle in the sidebar to sample 25,000–50,000 rows for smooth interactivity.

---

## 3. License and Attribution

- **CIC-IDS2017 Citation:**
  > Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani, *"Toward Generating a New Intrusion Detection Dataset and Intrusion Traffic Characterization"*, 4th International Conference on Information Systems Security and Privacy (ICISSP), Portugal, January 2018.
- The raw dataset is licensed by UNB for academic and research purposes. Do not redistribute raw CSVs in public repositories.
