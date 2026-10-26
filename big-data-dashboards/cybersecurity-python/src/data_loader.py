"""
data_loader.py - Safe CSV and dataset loading for cybersecurity traffic data.
Handles local files, Streamlit uploaders, encodings, and size checks.
"""
from dataclasses import dataclass, field
from io import BytesIO, StringIO
import os
from typing import Optional, Union, List
import pandas as pd


@dataclass
class LoadResult:
    """Structured container returned by the data loader."""
    df: Optional[pd.DataFrame] = None
    original_rows: int = 0
    original_cols: int = 0
    is_sampled: bool = False
    source_name: str = ""
    file_size_mb: float = 0.0
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.error is None and self.df is not None and not self.df.empty


def load_dataset(
    source: Union[str, BytesIO, StringIO],
    file_name: str = "dataset.csv",
    row_limit: Optional[int] = None,
    random_sample: bool = False,
    random_seed: int = 42
) -> LoadResult:
    """
    Safely load a CSV file from a path or file-like buffer.

    Parameters:
    - source: File path string or file-like object (e.g. UploadedFile).
    - file_name: Display name of the source.
    - row_limit: Optional integer cap on rows loaded.
    - random_sample: If True and row_limit specified, downsamples randomly.
    - random_seed: Seed for deterministic sampling.

    Returns:
    - LoadResult with DataFrame, metadata, and any warnings.
    """
    result = LoadResult(source_name=file_name)
    warnings: List[str] = []

    # 1. Inspect source size
    file_size_bytes = 0
    if isinstance(source, str):
        if not os.path.exists(source):
            result.error = f"File not found at specified path: '{source}'"
            return result
        file_size_bytes = os.path.getsize(source)
    elif hasattr(source, "size"):
        file_size_bytes = getattr(source, "size", 0)
    elif hasattr(source, "getbuffer"):
        file_size_bytes = len(source.getbuffer())

    result.file_size_mb = round(file_size_bytes / (1024 * 1024), 2)
    if result.file_size_mb > 250:
        warnings.append(
            f"Dataset size is {result.file_size_mb:.1f} MB. "
            "Consider enabling row sampling to preserve browser responsiveness."
        )

    # 2. Multi-encoding reader fallback
    encodings_to_try = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
    df = None
    last_exception = None

    for enc in encodings_to_try:
        try:
            if hasattr(source, "seek"):
                source.seek(0)
            df = pd.read_csv(source, encoding=enc, low_memory=False)
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            last_exception = e
            break

    if df is None:
        result.error = (
            f"Failed to read CSV. Error: {str(last_exception) if last_exception else 'Encoding mismatch.'}"
        )
        return result

    if df.empty:
        result.error = "The provided CSV file contains no data rows."
        return result

    result.original_rows = len(df)
    result.original_cols = len(df.columns)

    # 3. Handle row capping / sampling
    if row_limit is not None and row_limit > 0 and len(df) > row_limit:
        if random_sample:
            df = df.sample(n=row_limit, random_state=random_seed).reset_index(drop=True)
            warnings.append(
                f"Dataset downsampled deterministically from {result.original_rows:,} to {row_limit:,} rows (Seed: {random_seed})."
            )
        else:
            df = df.iloc[:row_limit].reset_index(drop=True)
            warnings.append(
                f"Dataset capped to first {row_limit:,} rows out of {result.original_rows:,} total rows."
            )
        result.is_sampled = True

    result.df = df
    result.warnings = warnings
    return result
