"""
metrics.py - Pure mathematical and statistical aggregation functions
for network traffic and cybersecurity threat analysis.
"""
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd


def calculate_kpis(
    df: pd.DataFrame,
    label_col: Optional[str] = None,
    normal_label: Optional[str] = None,
    src_ip_col: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calculate top-level summary KPIs with zero-division safety and schema guards.

    Returns:
    - records_analyzed: int
    - distinct_labels: int
    - attack_labeled_records: Optional[int]
    - attack_labeled_percentage: Optional[float]
    - unique_source_ips: Optional[int]
    - is_normal_identified: bool
    """
    kpis: Dict[str, Any] = {
        "records_analyzed": len(df),
        "distinct_labels": 0,
        "attack_labeled_records": None,
        "attack_labeled_percentage": None,
        "unique_source_ips": None,
        "is_normal_identified": False
    }

    if df.empty:
        return kpis

    # 1. Distinct Labels
    if label_col and label_col in df.columns:
        valid_labels = df[label_col].dropna()
        kpis["distinct_labels"] = int(valid_labels.nunique())

        # 2. Attack vs Benign calculation
        if normal_label is not None and not valid_labels.empty:
            kpis["is_normal_identified"] = True
            total_labeled = len(valid_labels)
            # Match exactly (string trimmed)
            attack_mask = valid_labels.astype(str) != str(normal_label)
            attack_count = int(attack_mask.sum())
            kpis["attack_labeled_records"] = attack_count
            if total_labeled > 0:
                kpis["attack_labeled_percentage"] = round((attack_count / total_labeled) * 100, 2)
            else:
                kpis["attack_labeled_percentage"] = 0.0

    # 3. Unique Source IPs
    if src_ip_col and src_ip_col in df.columns:
        valid_ips = df[src_ip_col].dropna()
        kpis["unique_source_ips"] = int(valid_ips.nunique())

    return kpis


def get_label_distribution(df: pd.DataFrame, label_col: str) -> pd.DataFrame:
    """
    Get record counts and percentages sorted descending by frequency.
    """
    if df.empty or label_col not in df.columns:
        return pd.DataFrame(columns=[label_col, "Count", "Percentage"])

    counts = df[label_col].fillna("Unknown").value_counts().reset_index()
    counts.columns = [label_col, "Count"]
    total = counts["Count"].sum()
    counts["Percentage"] = (counts["Count"] / total * 100).round(2) if total > 0 else 0.0
    return counts


def get_time_distribution(
    df: pd.DataFrame,
    timestamp_col: str,
    freq: str = "H"
) -> pd.DataFrame:
    """
    Aggregate record counts into time buckets (e.g. 'H' for hourly, 'D' for daily, '15min').
    """
    if df.empty or timestamp_col not in df.columns:
        return pd.DataFrame(columns=["Timestamp", "Count"])

    valid_ts = df.dropna(subset=[timestamp_col]).copy()
    if valid_ts.empty:
        return pd.DataFrame(columns=["Timestamp", "Count"])

    # Ensure valid datetime series
    valid_ts[timestamp_col] = pd.to_datetime(valid_ts[timestamp_col], errors="coerce")
    valid_ts = valid_ts.dropna(subset=[timestamp_col])
    if valid_ts.empty:
        return pd.DataFrame(columns=["Timestamp", "Count"])

    time_series = valid_ts.set_index(timestamp_col).resample(freq).size().reset_index()
    time_series.columns = ["Timestamp", "Count"]
    return time_series


def get_protocol_distribution(df: pd.DataFrame, proto_col: str) -> pd.DataFrame:
    """
    Map IANA protocol numbers to readable standard names and aggregate.
    """
    if df.empty or proto_col not in df.columns:
        return pd.DataFrame(columns=["Protocol", "Count", "Percentage"])

    iana_map = {
        6: "TCP (6)",
        17: "UDP (17)",
        1: "ICMP (1)",
        0: "HOPOPT (0)",
        2: "IGMP (2)",
        47: "GRE (47)",
        50: "ESP (50)",
        51: "AH (51)"
    }

    # Map if numeric or string representation of numbers
    def map_proto(val):
        try:
            val_int = int(float(val))
            return iana_map.get(val_int, f"Protocol {val_int}")
        except (ValueError, TypeError):
            return str(val)

    proto_series = df[proto_col].dropna().apply(map_proto)
    if proto_series.empty:
        return pd.DataFrame(columns=["Protocol", "Count", "Percentage"])

    counts = proto_series.value_counts().reset_index()
    counts.columns = ["Protocol", "Count"]
    total = counts["Count"].sum()
    counts["Percentage"] = (counts["Count"] / total * 100).round(2) if total > 0 else 0.0
    return counts


def get_weekday_hour_distribution(df: pd.DataFrame, timestamp_col: str) -> pd.DataFrame:
    """
    Create a 7x24 matrix of DayOfWeek vs Hour for activity density heatmaps.
    """
    if df.empty or timestamp_col not in df.columns:
        return pd.DataFrame()

    valid_ts = df.dropna(subset=[timestamp_col]).copy()
    valid_ts[timestamp_col] = pd.to_datetime(valid_ts[timestamp_col], errors="coerce")
    valid_ts = valid_ts.dropna(subset=[timestamp_col])

    if valid_ts.empty:
        return pd.DataFrame()

    valid_ts["Hour"] = valid_ts[timestamp_col].dt.hour
    valid_ts["DayName"] = valid_ts[timestamp_col].dt.day_name()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    pivot = valid_ts.pivot_table(
        index="DayName",
        columns="Hour",
        values=timestamp_col,
        aggfunc="count",
        fill_value=0
    )
    # Reindex to guarantee standard day order
    existing_days = [d for d in day_order if d in pivot.index]
    pivot = pivot.reindex(existing_days)
    return pivot


def get_protocol_by_label_distribution(
    df: pd.DataFrame,
    proto_col: str,
    label_col: str,
    top_n_labels: int = 6
) -> pd.DataFrame:
    """
    Crosstab of Protocol against Top N Labels to prevent visual overcrowding.
    """
    if df.empty or proto_col not in df.columns or label_col not in df.columns:
        return pd.DataFrame()

    # Filter to top N labels
    top_labels = df[label_col].value_counts().head(top_n_labels).index
    filtered = df[df[label_col].isin(top_labels)].copy()

    # Format protocol
    iana_map = {6: "TCP", 17: "UDP", 1: "ICMP"}
    def fmt_proto(v):
        try:
            return iana_map.get(int(float(v)), f"Proto {int(float(v))}")
        except Exception:
            return str(v)

    filtered["Protocol_Clean"] = filtered[proto_col].apply(fmt_proto)
    ct = pd.crosstab(filtered[label_col], filtered["Protocol_Clean"]).reset_index()
    return ct


def get_top_source_ips(
    df: pd.DataFrame,
    src_ip_col: str,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Get top N source IP addresses with count, percentage, and category notes.
    """
    if df.empty or src_ip_col not in df.columns:
        return pd.DataFrame(columns=["Source IP", "Record Count", "Traffic Share %", "Network Scope"])

    counts = df[src_ip_col].fillna("Unknown").value_counts().head(top_n).reset_index()
    counts.columns = ["Source IP", "Record Count"]
    total = len(df)
    counts["Traffic Share %"] = (counts["Record Count"] / total * 100).round(2) if total > 0 else 0.0

    def classify_ip_scope(ip: str) -> str:
        if ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.16."):
            return "Private / Lab Subnet (RFC 1918)"
        if ip == "127.0.0.1":
            return "Loopback"
        return "Public / External"

    counts["Network Scope"] = counts["Source IP"].apply(classify_ip_scope)
    return counts


def get_port_distribution(
    df: pd.DataFrame,
    port_col: str,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Aggregate top destination or source ports with service names.
    """
    if df.empty or port_col not in df.columns:
        return pd.DataFrame(columns=["Port", "Service", "Count"])

    port_names = {
        80: "HTTP (80)",
        443: "HTTPS (443)",
        21: "FTP (21)",
        22: "SSH (22)",
        23: "Telnet (23)",
        25: "SMTP (25)",
        53: "DNS (53)",
        8080: "HTTP-Alt (8080)",
        3389: "RDP (3389)",
        6667: "IRC (6667)"
    }

    counts = df[port_col].value_counts().head(top_n).reset_index()
    counts.columns = ["Port", "Count"]

    def map_service(p):
        try:
            return port_names.get(int(float(p)), f"Port {int(float(p))}")
        except Exception:
            return str(p)

    counts["Service"] = counts["Port"].apply(map_service)
    return counts[["Port", "Service", "Count"]]


def get_feature_summary_stats(
    df: pd.DataFrame,
    feature_col: str
) -> Dict[str, Any]:
    """
    Calculate statistical summary for a numeric feature:
    Count, Mean, Median, Std Dev, Min, Max, 25%, 75%, Skewness, Nulls, Infs.
    """
    stats: Dict[str, Any] = {
        "valid_count": 0,
        "null_count": 0,
        "mean": np.nan,
        "median": np.nan,
        "std": np.nan,
        "min": np.nan,
        "q25": np.nan,
        "q75": np.nan,
        "max": np.nan,
        "skewness": np.nan
    }

    if df.empty or feature_col not in df.columns:
        return stats

    series = pd.to_numeric(df[feature_col], errors="coerce")
    stats["null_count"] = int(series.isna().sum())
    clean_series = series.dropna()
    stats["valid_count"] = len(clean_series)

    if not clean_series.empty:
        stats["mean"] = round(float(clean_series.mean()), 4)
        stats["median"] = round(float(clean_series.median()), 4)
        stats["std"] = round(float(clean_series.std()), 4) if len(clean_series) > 1 else 0.0
        stats["min"] = round(float(clean_series.min()), 4)
        stats["q25"] = round(float(clean_series.quantile(0.25)), 4)
        stats["q75"] = round(float(clean_series.quantile(0.75)), 4)
        stats["max"] = round(float(clean_series.max()), 4)
        if len(clean_series) > 2 and stats["std"] > 0:
            stats["skewness"] = round(float(clean_series.skew()), 4)
        else:
            stats["skewness"] = 0.0

    return stats
