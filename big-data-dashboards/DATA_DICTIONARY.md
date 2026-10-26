# Comprehensive Data Dictionary
## Subject: Big Data Analysis and Visualization

This document details all data fields, physical types, units, and analytical interpretations across both projects.

---

# Part 1: Cybersecurity Threat Intelligence Dataset (CIC-IDS2017 Benchmark)

Benchmark reference: Canadian Institute for Cybersecurity (CIC-IDS2017), University of New Brunswick.

| Field Name | Data Type | Units / Range | Nullable | Description & Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| `Destination Port` | Integer | `0` to `65535` | No | Service-layer port on target host (e.g. 80 for HTTP, 443 for HTTPS, 21 for FTP, 22 for SSH). |
| `Flow Duration` | Integer | Microseconds (\(\mu s\)) | No | Duration of bidirectional connection. A duration of 0 occurs during rapid SYN scans. |
| `Total Fwd Packets` | Integer | Count (\(\ge 0\)) | Yes (Sanitized) | Total packets transmitted from source to destination. |
| `Total Backward Packets` | Integer | Count (\(\ge 0\)) | No | Total packets returned from destination to source. |
| `Total Length of Fwd Packets` | Decimal | Bytes | No | Sum of payload and header lengths in forward direction. |
| `Total Length of Bwd Packets` | Decimal | Bytes | No | Sum of payload and header lengths in backward direction. |
| `Flow Bytes/s` | Decimal | Bytes/second | Yes (Infs Coerced) | Transfer rate. Evaluates to `Infinity` when Flow Duration is 0; coerced to `NaN` in cleaning pipeline. |
| `Flow Packets/s` | Decimal | Packets/second | Yes (Infs Coerced) | Packet velocity. Coerced to `NaN` when duration is 0. |
| `Flow IAT Mean` | Decimal | Microseconds (\(\mu s\)) | No | Mean inter-arrival time between consecutive packet transmissions. |
| `Average Packet Size` | Decimal | Bytes | Yes (Sanitized) | Mean size of all transmitted packets across the flow. |
| `SYN Flag Count` | Integer | `0` or `1` | No | Binary flag indicating TCP SYN (synchronize) connection attempt. |
| `ACK Flag Count` | Integer | `0` or `1` | No | Binary flag indicating TCP ACK (acknowledgment) reception. |
| `Protocol` | Integer / String | `6` (TCP), `17` (UDP), `1` (ICMP) | Yes | Transport protocol code per IANA assignments. |
| `Source IP` | String | IPv4 address | Yes | Originating host address. In datasets, IPs reflect lab/private subnets (e.g. `192.168.10.x`). |
| `Source Port` | Integer | `0` to `65535` | Yes | Ephemeral client port allocated by originating OS. |
| `Timestamp` | Datetime | `YYYY-MM-DD HH:MM:SS` | Yes (Coerced) | Date and time when network flow was captured. |
| `Label` | String | Categorical | No | Ground truth traffic classification (`BENIGN`, `DDoS`, `PortScan`, `Bot`, `FTP-Patator`). |

---

# Part 2: Financial Market Analytics Dataset (Historical Daily OHLCV)

Market reference: US Stock Exchanges (NYSE / NASDAQ) via public historical feeds (Stooq / Yahoo Finance).

| Field Name | Data Type | Units / Format | Nullable | Description & Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| `Date` | Date | `YYYY-MM-DD` | No | Valid exchange trading session date. (Excludes weekend days and observed market holidays). |
| `Ticker` | String | Uppercase Symbol | No | Equity ticker code (`AAPL`, `MSFT`, `GOOGL`, `AMZN`). |
| `Company` | String | Text | Yes | Formal legal name of the publicly traded corporation. |
| `Sector` | String | GICS Category | Yes | Global Industry Classification Standard economic sector. |
| `Open` | Decimal | USD (\$) | No | First traded price at market opening bell (09:30 EST). |
| `High` | Decimal | USD (\$) | No | Maximum executed transaction price during the daily session. |
| `Low` | Decimal | USD (\$) | No | Minimum executed transaction price during the daily session. |
| `Close` | Decimal | USD (\$) | No | Official closing auction price at market closing bell (16:00 EST). |
| `AdjustedClose`| Decimal | USD (\$) | No | Closing price adjusted for subsequent stock splits and cash dividend events. |
| `Volume` | Integer | Share Count | No | Total volume of equity shares traded throughout the official session. |
| `DailyReturnPct`| Decimal | Percentage (%) | No | Session-to-session percentage price change vs previous trading close: \(\frac{\text{Close}_t - \text{Close}_{t-1}}{\text{Close}_{t-1}} \times 100\). |
| `DailyRangePct` | Decimal | Percentage (%) | No | Intraday price volatility spread: \(\frac{\text{High}_t - \text{Low}_t}{\text{Low}_t} \times 100\). |
| `Year` | Integer | `2023` | No | Calendar year derived in `DimDate`. |
| `Quarter` | String | `Q1`, `Q2`, `Q3`, `Q4` | No | Calendar quarter derived in `DimDate`. |
| `MonthName` | String | Text (`January`, etc.) | No | Full month name derived in `DimDate`. |
| `MonthNumber` | Integer | `1` to `12` | No | Sequential month number for chronological sorting. |
| `DayOfWeek` | String | Text (`Monday`, etc.) | No | Day of the week. Used for trading cycle profiling. |
| `IsWeekend` | Integer | `0` or `1` | No | Calendar marker (Saturday/Sunday). In stock data, weekends have no trading records. |
