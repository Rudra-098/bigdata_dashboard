"""
test_metrics.py - Unit test suite for cybersecurity dashboard metrics and cleaning.
Tests edge cases including empty DataFrames, missing labels, infinite values,
zero denominators, and optional schema variations.
"""
import numpy as np
import pandas as pd
import pytest

from src import metrics
from src.data_cleaning import clean_dataset, detect_candidate_column, detect_normal_label
from src.data_loader import load_dataset


def test_calculate_kpis_normal_case():
    """Verify standard KPI calculation with benign baseline."""
    df = pd.DataFrame({
        "Label": ["BENIGN", "BENIGN", "DDoS", "PortScan"],
        "Source IP": ["192.168.1.1", "192.168.1.2", "192.168.1.1", "10.0.0.1"]
    })
    kpis = metrics.calculate_kpis(df, label_col="Label", normal_label="BENIGN", src_ip_col="Source IP")

    assert kpis["records_analyzed"] == 4
    assert kpis["distinct_labels"] == 3
    assert kpis["attack_labeled_records"] == 2
    assert kpis["attack_labeled_percentage"] == 50.0
    assert kpis["unique_source_ips"] == 3
    assert kpis["is_normal_identified"] is True


def test_calculate_kpis_empty_dataset():
    """Verify empty DataFrame does not raise errors or divide by zero."""
    df = pd.DataFrame()
    kpis = metrics.calculate_kpis(df, label_col="Label", normal_label="BENIGN")

    assert kpis["records_analyzed"] == 0
    assert kpis["distinct_labels"] == 0
    assert kpis["attack_labeled_records"] is None
    assert kpis["attack_labeled_percentage"] is None
    assert kpis["unique_source_ips"] is None
    assert kpis["is_normal_identified"] is False


def test_calculate_kpis_missing_normal_label():
    """When normal label is None or unselected, attack metrics should remain None."""
    df = pd.DataFrame({
        "Label": ["ClassA", "ClassB", "ClassC"]
    })
    kpis = metrics.calculate_kpis(df, label_col="Label", normal_label=None)

    assert kpis["records_analyzed"] == 3
    assert kpis["distinct_labels"] == 3
    assert kpis["attack_labeled_records"] is None
    assert kpis["attack_labeled_percentage"] is None
    assert kpis["is_normal_identified"] is False


def test_calculate_kpis_missing_optional_columns():
    """Verify app handles datasets lacking source IP or protocol gracefully."""
    df = pd.DataFrame({
        "Label": ["BENIGN", "Bot"]
    })
    kpis = metrics.calculate_kpis(df, label_col="Label", normal_label="BENIGN", src_ip_col="NonExistentCol")

    assert kpis["records_analyzed"] == 2
    assert kpis["distinct_labels"] == 2
    assert kpis["attack_labeled_records"] == 1
    assert kpis["attack_labeled_percentage"] == 50.0
    assert kpis["unique_source_ips"] is None


def test_label_distribution():
    """Check label distribution percentage computation and sorting."""
    df = pd.DataFrame({
        "Label": ["BENIGN", "BENIGN", "BENIGN", "DDoS"]
    })
    dist = metrics.get_label_distribution(df, "Label")

    assert len(dist) == 2
    assert dist.iloc[0]["Label"] == "BENIGN"
    assert dist.iloc[0]["Count"] == 3
    assert dist.iloc[0]["Percentage"] == 75.0
    assert dist.iloc[1]["Label"] == "DDoS"
    assert dist.iloc[1]["Count"] == 1
    assert dist.iloc[1]["Percentage"] == 25.0


def test_protocol_distribution_mapping():
    """Check mapping of IANA numbers (6 -> TCP, 17 -> UDP) and percentages."""
    df = pd.DataFrame({
        "Protocol": [6, 6, 17, 1]
    })
    proto_dist = metrics.get_protocol_distribution(df, "Protocol")

    assert len(proto_dist) == 3
    tcp_row = proto_dist[proto_dist["Protocol"] == "TCP (6)"]
    assert not tcp_row.empty
    assert tcp_row.iloc[0]["Count"] == 2
    assert tcp_row.iloc[0]["Percentage"] == 50.0


def test_feature_summary_stats():
    """Check statistical summary accuracy."""
    df = pd.DataFrame({
        "Packet_Length": [10.0, 20.0, 30.0, 40.0, 50.0, np.nan]
    })
    stats = metrics.get_feature_summary_stats(df, "Packet_Length")

    assert stats["valid_count"] == 5
    assert stats["null_count"] == 1
    assert stats["mean"] == 30.0
    assert stats["median"] == 30.0
    assert stats["min"] == 10.0
    assert stats["max"] == 50.0


def test_data_cleaning_infinite_values():
    """Verify non-finite numeric values (inf, -inf) are replaced with NaN and reported."""
    df = pd.DataFrame({
        " Destination Port": [80, 443, 80],
        "Flow Bytes/s": [100.0, np.inf, -np.inf],
        " Label": ["BENIGN", "DDoS", "BENIGN"]
    })
    cleaned_df, report = clean_dataset(df)

    assert "Flow Bytes/s" in cleaned_df.columns
    assert "Destination Port" in cleaned_df.columns
    assert "Label" in cleaned_df.columns
    assert report.infinite_values_replaced == 2
    assert cleaned_df["Flow Bytes/s"].isna().sum() == 2


def test_data_cleaning_whitespace_stripping():
    """Verify leading/trailing spaces in headers and values are stripped."""
    df = pd.DataFrame({
        "  Flow Duration  ": [100, 200],
        " Label ": [" BENIGN ", " Bot "]
    })
    cleaned_df, report = clean_dataset(df)

    assert "Flow Duration" in cleaned_df.columns
    assert "Label" in cleaned_df.columns
    assert list(cleaned_df["Label"]) == ["BENIGN", "Bot"]


def test_data_cleaning_duplicate_handling():
    """Check duplicate rows detection and optional removal."""
    df = pd.DataFrame({
        "FeatureA": [1, 1, 2],
        "FeatureB": [10, 10, 20]
    })
    # Without removal
    _, report1 = clean_dataset(df, remove_duplicates=False)
    assert report1.duplicate_rows_detected == 1
    assert report1.duplicate_rows_removed == 0

    # With removal
    cleaned_df2, report2 = clean_dataset(df, remove_duplicates=True)
    assert report2.duplicate_rows_detected == 1
    assert report2.duplicate_rows_removed == 1
    assert len(cleaned_df2) == 2


def test_candidate_detection():
    """Verify heuristic column role identification."""
    cols = ["Flow_Duration", " Destination Port ", "Label_Class", "Timestamp_UTC"]
    lbl = detect_candidate_column(cols, ["label", "class"])
    ts = detect_candidate_column(cols, ["timestamp", "time"])
    port = detect_candidate_column(cols, ["destination port", "dst_port"])

    assert lbl == "Label_Class"
    assert ts == "Timestamp_UTC"
    assert port == " Destination Port "


def test_detect_normal_label():
    """Verify automated benign category detection across naming conventions."""
    s1 = pd.Series(["BENIGN", "DDoS", "PortScan"])
    s2 = pd.Series(["Normal", "Attack"])
    s3 = pd.Series(["Malicious", "Infiltration"])

    assert detect_normal_label(s1) == "BENIGN"
    assert detect_normal_label(s2) == "Normal"
    assert detect_normal_label(s3) is None
