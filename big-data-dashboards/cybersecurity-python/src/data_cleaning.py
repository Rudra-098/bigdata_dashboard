"""
data_cleaning.py - Data cleaning, type harmonization, and quality profiling
for network intrusion datasets.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd


@dataclass
class CleaningReport:
    """Detailed audit metrics of the data cleaning pipeline."""
    original_row_count: int = 0
    cleaned_row_count: int = 0
    original_col_count: int = 0
    cleaned_col_count: int = 0
    duplicate_rows_detected: int = 0
    duplicate_rows_removed: int = 0
    infinite_values_replaced: int = 0
    unparseable_timestamps: int = 0
    missing_values_by_column: Dict[str, int] = field(default_factory=dict)
    detected_columns: Dict[str, Optional[str]] = field(default_factory=dict)
    detected_normal_label: Optional[str] = None
    warnings: List[str] = field(default_factory=list)


def detect_candidate_column(columns: List[str], candidate_keywords: List[str]) -> Optional[str]:
    """
    Find best matching column name based on normalized keyword matches.
    Prioritizes exact case-insensitive matches before substring matches.
    """
    col_map = {c.strip().lower(): c for c in columns}
    
    # 1. Exact match
    for kw in candidate_keywords:
        if kw.lower() in col_map:
            return col_map[kw.lower()]
            
    # 2. Substring match
    for kw in candidate_keywords:
        for norm_col, orig_col in col_map.items():
            if kw.lower() in norm_col:
                return orig_col
                
    return None


def detect_normal_label(labels: pd.Series) -> Optional[str]:
    """
    Detect normal/benign traffic category from unique labels.
    Returns the exact string label if matched, or None if inconclusive.
    """
    unique_vals = [str(x).strip() for x in labels.dropna().unique()]
    benign_keywords = ["benign", "normal", "clean", "legitimate", "background"]
    
    for val in unique_vals:
        val_lower = val.lower()
        for kw in benign_keywords:
            if kw == val_lower or kw in val_lower:
                return val
    return None


def clean_dataset(
    df: pd.DataFrame,
    label_col_override: Optional[str] = None,
    remove_duplicates: bool = False,
    normal_label_override: Optional[str] = None
) -> Tuple[pd.DataFrame, CleaningReport]:
    """
    Clean, harmonize, and profile the input network intrusion dataset.

    Parameters:
    - df: Raw input pandas DataFrame.
    - label_col_override: Optional user-selected column for traffic label.
    - remove_duplicates: If True, drops duplicate rows and reports count.
    - normal_label_override: Optional user-selected label designating benign traffic.

    Returns:
    - cleaned_df: Sanitized DataFrame ready for analysis.
    - report: CleaningReport dataclass capturing metrics.
    """
    report = CleaningReport(
        original_row_count=len(df),
        original_col_count=len(df.columns)
    )
    df_clean = df.copy()

    # 1. Trim leading/trailing whitespace and ensure unique column names
    clean_cols = []
    seen_cols = {}
    for c in df_clean.columns:
        norm = str(c).strip()
        if norm in seen_cols:
            seen_cols[norm] += 1
            unique_name = f"{norm}_{seen_cols[norm]}"
            clean_cols.append(unique_name)
            report.warnings.append(f"Disambiguated duplicate column '{norm}' to '{unique_name}'.")
        else:
            seen_cols[norm] = 0
            clean_cols.append(norm)
    df_clean.columns = clean_cols
    report.cleaned_col_count = len(df_clean.columns)

    # 2. Trim whitespace in string columns
    str_cols = df_clean.select_dtypes(include=["object", "string"]).columns
    for c in str_cols:
        df_clean[c] = df_clean[c].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # 3. Detect key columns
    detected = {}
    detected["label"] = label_col_override or detect_candidate_column(
        list(df_clean.columns), ["label", "class", "traffic_label", "category", "attack"]
    )
    detected["timestamp"] = detect_candidate_column(
        list(df_clean.columns), ["timestamp", "time", "datetime", "flow_start_time", "date"]
    )
    detected["protocol"] = detect_candidate_column(
        list(df_clean.columns), ["protocol", "proto"]
    )
    detected["source_ip"] = detect_candidate_column(
        list(df_clean.columns), ["source ip", "source_ip", "src_ip", "srcip", "sourceip"]
    )
    detected["destination_port"] = detect_candidate_column(
        list(df_clean.columns), ["destination port", "destination_port", "dst_port", "dstport", "dport"]
    )
    detected["source_port"] = detect_candidate_column(
        list(df_clean.columns), ["source port", "source_port", "src_port", "srcport", "sport"]
    )
    report.detected_columns = detected

    if not detected["label"]:
        report.warnings.append(
            "Could not automatically identify a label/classification column. "
            "Please specify one manually in the sidebar."
        )

    # 4. Handle duplicates
    dup_mask = df_clean.duplicated()
    dup_count = int(dup_mask.sum())
    report.duplicate_rows_detected = dup_count

    if remove_duplicates and dup_count > 0:
        df_clean = df_clean.drop_duplicates().reset_index(drop=True)
        report.duplicate_rows_removed = dup_count
        report.warnings.append(f"Removed {dup_count:,} duplicate rows from the dataset.")

    # 5. Handle non-finite numeric values (inf, -inf)
    # Exclude IP addresses and labels from numeric coercion
    exclude_from_numeric = set(filter(None, [
        detected["label"], detected["source_ip"], detected["timestamp"]
    ]))
    
    inf_count = 0
    numeric_cols = []

    for col in df_clean.columns:
        if col in exclude_from_numeric:
            continue
            
        # Try converting to numeric if it contains numbers or inf
        if df_clean[col].dtype == object:
            # Check sample to avoid converting pure string metadata
            sample = df_clean[col].dropna().head(20).astype(str)
            if sample.str.replace(".", "", regex=False).str.replace("-", "", regex=False).str.isnumeric().any():
                df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")
                
        if pd.api.types.is_numeric_dtype(df_clean[col]):
            numeric_cols.append(col)
            inf_mask = np.isinf(df_clean[col])
            col_inf_count = int(inf_mask.sum())
            if col_inf_count > 0:
                inf_count += col_inf_count
                # Replace inf with NaN for robust metrics and charting
                df_clean.loc[inf_mask, col] = np.nan

    report.infinite_values_replaced = inf_count
    if inf_count > 0:
        report.warnings.append(
            f"Handled {inf_count:,} non-finite (infinite) values by replacing them with NaN to preserve mathematical validity."
        )

    # 6. Parse Timestamp safely if present
    if detected["timestamp"] and detected["timestamp"] in df_clean.columns:
        ts_col = detected["timestamp"]
        ts_parsed = pd.to_datetime(df_clean[ts_col], errors="coerce", dayfirst=True)
        unparseable = int(ts_parsed.isna().sum()) - int(df_clean[ts_col].isna().sum())
        report.unparseable_timestamps = max(0, unparseable)
        if report.unparseable_timestamps > 0:
            report.warnings.append(
                f"{report.unparseable_timestamps:,} timestamp values could not be parsed into valid dates and were converted to NaT."
            )
        df_clean[ts_col] = ts_parsed

    # 7. Record Missing Values per column
    missing = df_clean.isna().sum().to_dict()
    report.missing_values_by_column = {k: int(v) for k, v in missing.items() if v > 0}

    # 8. Detect Normal/Benign Label
    if detected["label"] and detected["label"] in df_clean.columns:
        if normal_label_override:
            report.detected_normal_label = normal_label_override
        else:
            report.detected_normal_label = detect_normal_label(df_clean[detected["label"]])
            
        if not report.detected_normal_label:
            report.warnings.append(
                "No standard normal/benign category detected automatically. "
                "Attack vs Benign metrics will be disabled until a baseline is configured."
            )

    report.cleaned_row_count = len(df_clean)
    return df_clean, report
