"""
app.py - Cybersecurity Threat Intelligence Dashboard
Big Data Analysis & Visualization of Network Traffic
Author: Big Data Analytics Student Project
"""
import os
import sys
from typing import Optional, List
import pandas as pd
import streamlit as st

# Add current folder to path so local imports work seamlessly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from src.data_loader import load_dataset, LoadResult
from src.data_cleaning import clean_dataset, CleaningReport
from src import metrics
from src import charts

# Streamlit Page Setup
st.set_page_config(
    page_title="Cybersecurity Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Security Theme CSS
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 12px 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700 !important;
        font-size: 1.7rem !important;
    }
    /* Tab headers */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 500;
    }
    /* Banner Callouts */
    .banner-warning {
        padding: 12px 16px;
        background-color: #451a03;
        border: 1px solid #b45309;
        border-radius: 6px;
        color: #fde68a;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .banner-info {
        padding: 10px 14px;
        background-color: #082f49;
        border: 1px solid #0284c7;
        border-radius: 6px;
        color: #bae6fd;
        margin-bottom: 1rem;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Loading dataset...")
def cached_load_file(file_bytes_or_path, file_name: str, row_limit: Optional[int], random_sample: bool) -> LoadResult:
    """Cache loaded data based on source representation."""
    return load_dataset(file_bytes_or_path, file_name=file_name, row_limit=row_limit, random_sample=random_sample)


def main():
    # Header Section
    st.title("🛡️ Cybersecurity Threat Intelligence Dashboard")
    st.subheader("Big Data Analysis & Visualization of Network Traffic")
    st.caption("🔍 Retrospective analysis of public network intrusion detection data. This is an academic research platform, not a live operational SOC monitor.")

    # Sidebar: Data Ingestion & Configuration
    with st.sidebar:
        st.header("⚙️ Data Configuration")

        source_option = st.radio(
            "Select Data Source:",
            ["Synthetic Sample Fixture", "Upload CSV File", "Local File Path"],
            help="Choose between the built-in synthetic test fixture or your downloaded CIC-IDS2017 dataset."
        )

        load_res: Optional[LoadResult] = None
        is_synthetic = False

        # Row Sampling Options
        enable_sampling = st.checkbox("Limit Rows (Constrained Devices)", value=False)
        row_limit = None
        if enable_sampling:
            row_limit = st.number_input("Max Rows to Load", min_value=500, max_value=2000000, value=25000, step=5000)
            st.warning("⚠️ Row sampling active. Visualizations represent a subset.")

        if source_option == "Synthetic Sample Fixture":
            default_path = os.path.join(CURRENT_DIR, "data", "synthetic_ids_sample.csv")
            load_res = cached_load_file(default_path, "synthetic_ids_sample.csv", row_limit, False)
            is_synthetic = True

        elif source_option == "Upload CSV File":
            uploaded_file = st.file_uploader("Upload Network Flow CSV (e.g. CIC-IDS2017)", type=["csv"])
            if uploaded_file is not None:
                load_res = cached_load_file(uploaded_file, uploaded_file.name, row_limit, True)
            else:
                st.info("Please upload a CSV file to begin analysis.")
                st.stop()

        else: # Local File Path
            local_path = st.text_input("Enter Absolute File Path:", value="")
            if local_path and os.path.exists(local_path):
                load_res = cached_load_file(local_path, os.path.basename(local_path), row_limit, False)
            else:
                if local_path:
                    st.error(f"Path does not exist: {local_path}")
                st.info("Enter a valid local CSV path to begin.")
                st.stop()

        if not load_res or not load_res.is_success:
            st.error(f"Error loading dataset: {load_res.error if load_res else 'Unknown error'}")
            st.stop()

        raw_df = load_res.df

        # Duplicate Handling Control
        st.markdown("---")
        st.subheader("🧹 Data Cleaning Options")
        remove_dups = st.checkbox("Deduplicate Dataset", value=False, help="Removes exact duplicate rows and reports count in the Data Quality tab.")

        # Schema Mapping Overrides
        with st.expander("🛠️ Column Role Mapping", expanded=False):
            all_cols = list(raw_df.columns)
            # Normalize for preview
            cleaned_cols = [str(c).strip() for c in all_cols]
            col_dict = dict(zip(cleaned_cols, all_cols))

            # Guess default label
            label_guess = next((c for c in cleaned_cols if "label" in c.lower() or "class" in c.lower()), cleaned_cols[0])
            sel_label = st.selectbox("Label Column", cleaned_cols, index=cleaned_cols.index(label_guess))

        # Perform initial clean
        cleaned_df, clean_report = clean_dataset(
            raw_df,
            label_col_override=sel_label,
            remove_duplicates=remove_dups
        )

        label_col = clean_report.detected_columns.get("label", sel_label)
        ts_col = clean_report.detected_columns.get("timestamp")
        proto_col = clean_report.detected_columns.get("protocol")
        src_ip_col = clean_report.detected_columns.get("source_ip")
        dst_port_col = clean_report.detected_columns.get("destination_port")

        # Benign / Normal Category Selection
        available_labels = sorted(cleaned_df[label_col].dropna().unique().tolist()) if label_col in cleaned_df else []
        detected_normal = clean_report.detected_normal_label
        normal_idx = available_labels.index(detected_normal) if (detected_normal and detected_normal in available_labels) else 0

        normal_category = st.selectbox(
            "Benign / Normal Baseline Label:",
            ["(None / Disable Attack Metrics)"] + available_labels,
            index=(normal_idx + 1) if (detected_normal and detected_normal in available_labels) else 0,
            help="Used to compute attack-labeled percentages. If set to None, attack metrics are disabled."
        )
        chosen_normal = None if normal_category.startswith("(") else normal_category

        # Dynamic Filters Section
        st.markdown("---")
        st.subheader("🔎 Interactive Filters")

        filtered_df = cleaned_df.copy()

        # 1. Label Filter
        selected_labels = st.multiselect(
            "Filter Traffic Labels:",
            options=available_labels,
            default=available_labels
        )
        if selected_labels and label_col in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[label_col].isin(selected_labels)]

        # 2. Protocol Filter
        if proto_col and proto_col in filtered_df.columns:
            protos = sorted(filtered_df[proto_col].dropna().unique().tolist())
            selected_protos = st.multiselect("Filter Protocol:", options=protos, default=protos)
            if selected_protos:
                filtered_df = filtered_df[filtered_df[proto_col].isin(selected_protos)]

        # 3. Timestamp Date Range Filter
        if ts_col and ts_col in filtered_df.columns and pd.api.types.is_datetime64_any_dtype(filtered_df[ts_col]):
            valid_dates = filtered_df[ts_col].dropna()
            if not valid_dates.empty:
                min_date = valid_dates.min().to_pydatetime()
                max_date = valid_dates.max().to_pydatetime()
                if min_date < max_date:
                    date_range = st.slider(
                        "Timestamp Filter Range:",
                        min_value=min_date,
                        max_value=max_date,
                        value=(min_date, max_date),
                        format="YYYY-MM-DD HH:mm"
                    )
                    filtered_df = filtered_df[
                        (filtered_df[ts_col] >= pd.Timestamp(date_range[0])) &
                        (filtered_df[ts_col] <= pd.Timestamp(date_range[1]))
                    ]

        st.caption(f"Filtered Records: **{len(filtered_df):,}** of **{len(cleaned_df):,}**")

    # Synthetic Data Warning Callout
    if is_synthetic:
        st.markdown("""
        <div class="banner-warning">
            ⚠️ <b>NOTICE — SYNTHETIC FIXTURE LOADED:</b> The dashboard is currently displaying an offline synthetic sample fixture (1,500 records) formatted to the CIC-IDS2017 schema. Numerical statistics and patterns are for software verification and grading demonstrations. To perform genuine forensic threat analysis, switch the data source in the sidebar to a full CIC-IDS2017 CSV file.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="banner-info">
            📁 <b>Active Dataset:</b> {load_res.source_name} ({load_res.original_rows:,} raw records, {load_res.file_size_mb:.2f} MB) | Filters Active: {len(filtered_df):,} records in current view.
        </div>
        """, unsafe_allow_html=True)

    # Empty State Guard
    if filtered_df.empty:
        st.warning("⚠️ No traffic records match the selected filter criteria. Please broaden your sidebar filters or reset them.")
        st.stop()

    # Calculate Top-Level KPIs
    kpis = metrics.calculate_kpis(
        filtered_df,
        label_col=label_col,
        normal_label=chosen_normal,
        src_ip_col=src_ip_col
    )

    # Main Tabs Layout
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 1. Overview",
        "🌐 2. Traffic & Attack Patterns",
        "🔬 3. Feature Analysis",
        "🧪 4. Data Quality",
        "🗂️ 5. Dataset Explorer"
    ])

    # -------------------------------------------------------------
    # TAB 1: OVERVIEW
    # -------------------------------------------------------------
    with tab1:
        st.markdown("### Executive Overview")
        st.caption("Key volume indicators and label distributions across the filtered session.")

        # KPI Metrics Cards
        kpi_cols = st.columns(5)
        with kpi_cols[0]:
            st.metric(
                label="Records Analyzed",
                value=f"{kpis['records_analyzed']:,}",
                help="Total traffic flow records currently loaded and filtered."
            )
        with kpi_cols[1]:
            st.metric(
                label="Distinct Labels",
                value=f"{kpis['distinct_labels']}",
                help="Count of unique traffic classifications present in active filter."
            )
        with kpi_cols[2]:
            val_txt = f"{kpis['attack_labeled_records']:,}" if kpis["is_normal_identified"] else "N/A"
            st.metric(
                label="Attack-Labeled Records",
                value=val_txt,
                help=f"Records categorized as non-{chosen_normal} in dataset ground truth."
            )
        with kpi_cols[3]:
            pct_txt = f"{kpis['attack_labeled_percentage']}%" if kpis["is_normal_identified"] else "N/A"
            st.metric(
                label="Attack Record Share",
                value=pct_txt,
                help="Attack-labeled records as a percentage of all labeled records."
            )
        with kpi_cols[4]:
            ips_txt = f"{kpis['unique_source_ips']:,}" if kpis["unique_source_ips"] is not None else "N/A"
            st.metric(
                label="Unique Source IPs",
                value=ips_txt,
                help="Distinct client/source IP addresses observed in traffic."
            )

        st.markdown("---")

        # Visualizations Row
        ov_col1, ov_col2 = st.columns([1, 1])

        with ov_col1:
            df_labels = metrics.get_label_distribution(filtered_df, label_col)
            fig_labels = charts.create_label_bar_chart(df_labels, label_col, chosen_normal)
            st.plotly_chart(fig_labels, use_container_width=True)

        with ov_col2:
            if proto_col and proto_col in filtered_df.columns:
                df_proto = metrics.get_protocol_distribution(filtered_df, proto_col)
                fig_proto = charts.create_protocol_chart(df_proto)
                st.plotly_chart(fig_proto, use_container_width=True)
            else:
                st.info("ℹ️ Protocol column not present in this dataset export.")

        # Temporal Volume Line Chart
        if ts_col and ts_col in filtered_df.columns and pd.api.types.is_datetime64_any_dtype(filtered_df[ts_col]):
            st.markdown("#### Traffic Volume Timeline")
            bucket_opt = st.selectbox("Timeline Aggregation Bucket:", ["15min", "Hour", "Day"], index=1)
            bucket_map = {"15min": "15min", "Hour": "h", "Day": "D"}
            df_time = metrics.get_time_distribution(filtered_df, ts_col, freq=bucket_map[bucket_opt])
            fig_time = charts.create_time_series_chart(df_time, freq_label=bucket_opt)
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("ℹ️ Valid timestamp field not detected or could not be parsed.")

    # -------------------------------------------------------------
    # TAB 2: TRAFFIC & ATTACK PATTERNS
    # -------------------------------------------------------------
    with tab2:
        st.markdown("### Traffic & Attack Patterns")
        st.caption("Deep-dive forensic perspectives across classifications, timing patterns, protocols, and network endpoints.")

        pat_col1, pat_col2 = st.columns([1, 1])
        with pat_col1:
            df_lbl = metrics.get_label_distribution(filtered_df, label_col)
            fig_hbar = charts.create_label_horizontal_bar(df_lbl, label_col, chosen_normal)
            st.plotly_chart(fig_hbar, use_container_width=True)

        with pat_col2:
            if proto_col and proto_col in filtered_df.columns:
                df_ct = metrics.get_protocol_by_label_distribution(filtered_df, proto_col, label_col)
                fig_ct = charts.create_protocol_by_label_chart(df_ct)
                st.plotly_chart(fig_ct, use_container_width=True)
            elif dst_port_col and dst_port_col in filtered_df.columns:
                df_ports = metrics.get_port_distribution(filtered_df, dst_port_col, top_n=10)
                fig_ports = charts.create_port_distribution_chart(df_ports, "Destination Ports")
                st.plotly_chart(fig_ports, use_container_width=True)

        # Activity Heatmap
        if ts_col and ts_col in filtered_df.columns and pd.api.types.is_datetime64_any_dtype(filtered_df[ts_col]):
            st.markdown("#### Temporal Activity Density (Day of Week vs. Hour)")
            st.caption("Highlights peak network activity hours and identifies anomalous off-hours bursts.")
            df_heat = metrics.get_weekday_hour_distribution(filtered_df, ts_col)
            fig_heat = charts.create_weekday_hour_heatmap(df_heat)
            st.plotly_chart(fig_heat, use_container_width=True)

        # Top Source IP Table & Port Analysis
        st.markdown("---")
        bot_col1, bot_col2 = st.columns([1, 1])
        with bot_col1:
            st.markdown("#### Most Active Source IP Addresses")
            st.caption("⚠️ **Dataset Disclaimer:** IPs in intrusion benchmark datasets may originate from simulated testbed subnets, automated bot scripts, or anonymized lab ranges.")
            if src_ip_col and src_ip_col in filtered_df.columns:
                df_src = metrics.get_top_source_ips(filtered_df, src_ip_col, top_n=10)
                st.dataframe(df_src, hide_index=True, use_container_width=True)
            else:
                st.info("Source IP field not present in dataset.")

        with bot_col2:
            st.markdown("#### Targeted Destination Ports & Services")
            st.caption("Common port bindings help attribute traffic toward web (80/443), file transfer (21), or remote administration (22/3389).")
            if dst_port_col and dst_port_col in filtered_df.columns:
                df_p = metrics.get_port_distribution(filtered_df, dst_port_col, top_n=10)
                fig_p = charts.create_port_distribution_chart(df_p, "Destination Ports")
                st.plotly_chart(fig_p, use_container_width=True)
            else:
                st.info("Destination port column not present.")

    # -------------------------------------------------------------
    # TAB 3: FEATURE ANALYSIS
    # -------------------------------------------------------------
    with tab3:
        st.markdown("### Network Flow Feature Analysis")
        st.caption("Statistical inspection and distribution comparisons across traffic categories.")

        # Identify numeric candidate features
        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
        # Remove ID or port columns from primary statistical feature selection if possible
        priority_features = [c for c in numeric_cols if not c.lower().endswith("port") and not c.lower().endswith("ip")]
        feat_choices = priority_features if priority_features else numeric_cols

        if not feat_choices:
            st.warning("No numeric flow features detected in this dataset.")
        else:
            f_col1, f_col2 = st.columns([1, 1])
            with f_col1:
                sel_feature_1 = st.selectbox("Primary Numeric Feature:", feat_choices, index=0)
            with f_col2:
                sec_default_idx = min(1, len(feat_choices) - 1)
                sel_feature_2 = st.selectbox("Secondary Feature (for Scatter):", feat_choices, index=sec_default_idx)

            # Summary Statistics Table
            stats = metrics.get_feature_summary_stats(filtered_df, sel_feature_1)
            st.markdown(f"#### Summary Statistics: `{sel_feature_1}`")
            s_cols = st.columns(6)
            s_cols[0].metric("Valid Observations", f"{stats['valid_count']:,}")
            s_cols[1].metric("Mean", f"{stats['mean']:,}")
            s_cols[2].metric("Median (Q2)", f"{stats['median']:,}")
            s_cols[3].metric("Std Deviation", f"{stats['std']:,}")
            s_cols[4].metric("Min / Max", f"{stats['min']} / {stats['max']}")
            s_cols[5].metric("Skewness", f"{stats['skewness']}")

            # Charts Row: Histogram & Box Plot
            ch_col1, ch_col2 = st.columns([1, 1])
            with ch_col1:
                fig_hist = charts.create_feature_histogram(filtered_df, sel_feature_1)
                st.plotly_chart(fig_hist, use_container_width=True)

            with ch_col2:
                fig_box = charts.create_feature_box_plot(filtered_df, sel_feature_1, label_col)
                st.plotly_chart(fig_box, use_container_width=True)

            # Scatter Plot
            if sel_feature_1 != sel_feature_2:
                st.markdown("#### Bivariate Feature Scatter")
                st.caption("Displays relationships between two network flow metrics colored by traffic classification.")
                fig_scatter = charts.create_feature_scatter_plot(
                    filtered_df, sel_feature_1, sel_feature_2, label_col
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 4: DATA QUALITY
    # -------------------------------------------------------------
    with tab4:
        st.markdown("### Data Quality & Preprocessing Audit")
        st.caption("Transparent reporting of cleaning transformations, duplicates, missingness, and schema validation.")

        dq_cols = st.columns(4)
        dq_cols[0].metric("Raw Record Count", f"{clean_report.original_row_count:,}")
        dq_cols[1].metric("Cleaned Record Count", f"{clean_report.cleaned_row_count:,}")
        dq_cols[2].metric("Duplicates Detected", f"{clean_report.duplicate_rows_detected:,}")
        dq_cols[3].metric("Infinite Values Sanitized", f"{clean_report.infinite_values_replaced:,}")

        st.markdown("---")
        q_c1, q_c2 = st.columns([1, 1])

        with q_c1:
            st.markdown("#### Missing Values per Attribute")
            if clean_report.missing_values_by_column:
                missing_df = pd.DataFrame(
                    list(clean_report.missing_values_by_column.items()),
                    columns=["Column Name", "Missing Count"]
                )
                missing_df["Missing %"] = (missing_df["Missing Count"] / clean_report.original_row_count * 100).round(2)
                st.dataframe(missing_df, hide_index=True, use_container_width=True)
            else:
                st.success("✅ No missing values (nulls) detected in the active dataset.")

            st.markdown("#### Timestamp Validation")
            if clean_report.unparseable_timestamps > 0:
                st.warning(f"⚠️ {clean_report.unparseable_timestamps:,} timestamp records failed standard datetime parsing and were coerced to NaT.")
            else:
                st.success("✅ All timestamp entries successfully parsed into valid date-time structures.")

        with q_c2:
            st.markdown("#### Preprocessing Narrative & Audit Log")
            st.markdown("""
            **Cleaning Pipeline Steps Executed:**
            1. **Whitespace Normalization:** Leading/trailing whitespace trimmed from all column headers and text fields.
            2. **Infinite Value Coercion:** Infinite flow rates (`np.inf`, `-np.inf`) common in zero-duration flows converted to `NaN`.
            3. **Type Guarding:** Preserved IP strings and categorical labels to avoid erroneous numerical casting.
            4. **Deduplication:** Duplicates identified and optionally dropped based on sidebar selection.
            5. **Ground Truth Validation:** Automated detection of benign baseline label with manual override fallback.
            """)

            if clean_report.warnings:
                st.markdown("##### System Audit Warnings:")
                for w in clean_report.warnings:
                    st.warning(f"• {w}")

    # -------------------------------------------------------------
    # TAB 5: DATASET EXPLORER
    # -------------------------------------------------------------
    with tab5:
        st.markdown("### Interactive Dataset Explorer")
        st.caption("Inspect and export records adhering to current filter parameters.")

        col_select = st.multiselect(
            "Select Columns to Display:",
            options=list(filtered_df.columns),
            default=list(filtered_df.columns)[:8]
        )

        row_cap = st.slider("Display Cap (Rows to Render):", min_value=50, max_value=2000, value=250, step=50)
        display_sub = filtered_df[col_select].head(row_cap) if col_select else filtered_df.head(row_cap)

        st.dataframe(display_sub, use_container_width=True)
        st.caption(f"Showing first {len(display_sub):,} of {len(filtered_df):,} matching rows to ensure high rendering performance.")

        # CSV Exporter
        st.markdown("---")
        st.markdown("#### Export Cleaned & Filtered Subset")
        export_limit = st.number_input("Max Rows to Export:", min_value=100, max_value=100000, value=10000, step=1000)
        csv_data = filtered_df.head(export_limit).to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name="filtered_network_traffic.csv",
            mime="text/csv",
            help="Download the currently filtered dataset subset for reporting or external modeling."
        )


if __name__ == "__main__":
    main()
