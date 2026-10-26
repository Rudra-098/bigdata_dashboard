"""
charts.py - Professional Plotly visualizations for cybersecurity threat intelligence.
Uses a restrained dark navy/charcoal aesthetic with teal/cyan accents and clear typography.
"""
from typing import List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Design Palette Constants
BG_COLOR = "#0f172a"          # Slate 900
CARD_BG = "#1e293b"           # Slate 800
GRID_COLOR = "#334155"        # Slate 700
TEXT_COLOR = "#f1f5f9"        # Slate 100
TEXT_MUTED = "#94a3b8"        # Slate 400
TEAL_PRIMARY = "#06b6d4"      # Cyan 500
CYAN_ACCENT = "#14b8a6"       # Teal 500
AMBER_WARNING = "#f59e0b"     # Amber 500
RED_ALERT = "#ef4444"         # Red 500
BLUE_ACCENT = "#3b82f6"       # Blue 500

COLOR_SEQUENCE = [
    "#06b6d4", "#14b8a6", "#3b82f6", "#8b5cf6",
    "#ec4899", "#f59e0b", "#ef4444", "#10b981"
]


def apply_custom_theme(fig: go.Figure, title: str = "", height: int = 400) -> go.Figure:
    """Apply consistent dark-navy typography and geometry across Plotly charts."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>" if title else "",
            "y": 0.95,
            "x": 0.02,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"size": 15, "color": TEXT_COLOR, "family": "Inter, Segoe UI, sans-serif"}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_MUTED, "family": "Inter, Segoe UI, sans-serif", "size": 12},
        height=height,
        margin={"l": 40, "r": 30, "t": 55, "b": 40},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "font": {"color": TEXT_COLOR, "size": 11}
        },
        hoverlabel={
            "bgcolor": CARD_BG,
            "font_size": 12,
            "font_family": "Inter, Segoe UI, sans-serif",
            "font_color": TEXT_COLOR
        }
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=0.5,
        linecolor=GRID_COLOR,
        tickfont={"color": TEXT_MUTED}
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        gridwidth=0.5,
        linecolor=GRID_COLOR,
        tickfont={"color": TEXT_MUTED}
    )
    return fig


def create_label_bar_chart(
    df_labels: pd.DataFrame,
    label_col: str,
    normal_label: Optional[str] = None
) -> go.Figure:
    """Vertical bar chart of record counts by label, highlighting attack vs normal."""
    if df_labels.empty:
        fig = go.Figure()
        return apply_custom_theme(fig, "No Label Data Available")

    colors = []
    for l in df_labels[label_col]:
        if normal_label and str(l).strip() == str(normal_label).strip():
            colors.append(CYAN_ACCENT)
        else:
            colors.append(AMBER_WARNING)

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_labels[label_col],
                y=df_labels["Count"],
                text=[f"{c:,} ({p}%)" for c, p in zip(df_labels["Count"], df_labels["Percentage"])],
                textposition="auto",
                marker_color=colors,
                hovertemplate="<b>%{x}</b><br>Count: %{y:,}<br>Share: %{text}<extra></extra>"
            )
        ]
    )
    fig.update_layout(xaxis_title="Traffic Label", yaxis_title="Record Count")
    return apply_custom_theme(fig, "Traffic Records by Classification Label")


def create_label_horizontal_bar(
    df_labels: pd.DataFrame,
    label_col: str,
    normal_label: Optional[str] = None
) -> go.Figure:
    """Horizontal bar chart of labels ordered by frequency."""
    if df_labels.empty:
        fig = go.Figure()
        return apply_custom_theme(fig, "No Label Data Available")

    df_sorted = df_labels.sort_values(by="Count", ascending=True)
    colors = []
    for l in df_sorted[label_col]:
        if normal_label and str(l).strip() == str(normal_label).strip():
            colors.append(CYAN_ACCENT)
        else:
            colors.append(RED_ALERT if "ddos" in str(l).lower() or "bot" in str(l).lower() else AMBER_WARNING)

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_sorted["Count"],
                y=df_sorted[label_col],
                orientation="h",
                text=[f"{c:,} ({p}%)" for c, p in zip(df_sorted["Count"], df_sorted["Percentage"])],
                textposition="auto",
                marker_color=colors,
                hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>"
            )
        ]
    )
    fig.update_layout(xaxis_title="Record Count", yaxis_title="")
    return apply_custom_theme(fig, "Distribution of Dataset Traffic Labels", height=380)


def create_time_series_chart(df_time: pd.DataFrame, freq_label: str = "Hour") -> go.Figure:
    """Smooth line chart of traffic volume bucketed over time."""
    if df_time.empty:
        fig = go.Figure()
        return apply_custom_theme(fig, f"No Temporal Data Available ({freq_label} aggregation)")

    fig = go.Figure(
        data=[
            go.Scatter(
                x=df_time["Timestamp"],
                y=df_time["Count"],
                mode="lines+markers",
                line={"color": TEAL_PRIMARY, "width": 2.5, "shape": "spline"},
                marker={"size": 6, "color": CYAN_ACCENT},
                hovertemplate="<b>Time:</b> %{x|%Y-%m-%d %H:%M}<br><b>Volume:</b> %{y:,} flows<extra></extra>"
            )
        ]
    )
    fig.update_layout(
        xaxis_title="Timeline",
        yaxis_title="Observed Flows",
    )
    return apply_custom_theme(fig, f"Network Traffic Volume Over Time (per {freq_label})")


def create_protocol_chart(df_proto: pd.DataFrame) -> go.Figure:
    """Donut chart for protocol shares when categories are few; bar chart otherwise."""
    if df_proto.empty:
        fig = go.Figure()
        return apply_custom_theme(fig, "No Protocol Data Available")

    if len(df_proto) <= 4:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=df_proto["Protocol"],
                    values=df_proto["Count"],
                    hole=0.55,
                    marker={"colors": COLOR_SEQUENCE[:len(df_proto)]},
                    textinfo="label+percent",
                    hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>"
                )
            ]
        )
    else:
        fig = go.Figure(
            data=[
                go.Bar(
                    x=df_proto["Protocol"],
                    y=df_proto["Count"],
                    marker_color=BLUE_ACCENT,
                    text=df_proto["Count"],
                    textposition="auto",
                    hovertemplate="<b>%{x}</b>: %{y:,}<extra></extra>"
                )
            ]
        )
        fig.update_layout(xaxis_title="Protocol", yaxis_title="Flow Count")

    return apply_custom_theme(fig, "Traffic Distribution by Protocol")


def create_weekday_hour_heatmap(df_heatmap: pd.DataFrame) -> go.Figure:
    """Density heatmap of flows across Day-of-Week vs Hour-of-Day."""
    if df_heatmap.empty:
        fig = go.Figure()
        return apply_custom_theme(fig, "Insufficient Timestamp Data for Activity Heatmap")

    fig = go.Figure(
        data=[
            go.Heatmap(
                z=df_heatmap.values,
                x=[f"{h:02d}:00" for h in df_heatmap.columns],
                y=df_heatmap.index,
                colorscale=[
                    [0.0, "#0f172a"],
                    [0.2, "#1e3a5f"],
                    [0.5, "#0284c7"],
                    [0.8, "#06b6d4"],
                    [1.0, "#38bdf8"]
                ],
                colorbar={"title": "Flows", "tickfont": {"color": TEXT_MUTED}},
                hovertemplate="<b>Day:</b> %{y}<br><b>Hour:</b> %{x}<br><b>Flow Count:</b> %{z:,}<extra></extra>"
            )
        ]
    )
    fig.update_layout(xaxis_title="Hour of Day (UTC/Local)", yaxis_title="Day of Week")
    return apply_custom_theme(fig, "Temporal Activity Density (Day vs. Hour)", height=350)


def create_protocol_by_label_chart(df_crosstab: pd.DataFrame) -> go.Figure:
    """Stacked bar chart illustrating protocol shares per traffic label."""
    if df_crosstab.empty or len(df_crosstab.columns) < 2:
        fig = go.Figure()
        return apply_custom_theme(fig, "No Protocol-Label Overlap Data Available")

    label_col = df_crosstab.columns[0]
    proto_cols = df_crosstab.columns[1:]

    fig = go.Figure()
    for i, proto in enumerate(proto_cols):
        fig.add_trace(
            go.Bar(
                name=str(proto),
                x=df_crosstab[label_col],
                y=df_crosstab[proto],
                marker_color=COLOR_SEQUENCE[i % len(COLOR_SEQUENCE)],
                hovertemplate=f"<b>%{label_col}</b><br>{proto}: %{{y:,}}<extra></extra>"
            )
        )

    fig.update_layout(barmode="stack", xaxis_title="Traffic Label", yaxis_title="Flow Count")
    return apply_custom_theme(fig, "Protocol Usage by Top Traffic Categories")


def create_port_distribution_chart(df_ports: pd.DataFrame, title: str = "Destination Ports") -> go.Figure:
    """Bar chart of top ports and known network services."""
    if df_ports.empty:
        fig = go.Figure()
        return apply_custom_theme(fig, f"No Data for {title}")

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_ports["Service"],
                y=df_ports["Count"],
                marker_color=BLUE_ACCENT,
                text=df_ports["Count"],
                textposition="auto",
                hovertemplate="<b>%{x}</b><br>Flows: %{y:,}<extra></extra>"
            )
        ]
    )
    fig.update_layout(xaxis_title="Port / Common Service", yaxis_title="Flow Count")
    return apply_custom_theme(fig, f"Top {title} in Observed Traffic")


def create_feature_histogram(df: pd.DataFrame, feature_col: str, n_bins: int = 35) -> go.Figure:
    """Histogram with distribution metrics for numeric network flow features."""
    if df.empty or feature_col not in df.columns:
        fig = go.Figure()
        return apply_custom_theme(fig, "No Numeric Feature Data")

    series = pd.to_numeric(df[feature_col], errors="coerce").dropna()
    if series.empty:
        fig = go.Figure()
        return apply_custom_theme(fig, f"Feature '{feature_col}' has no valid numeric rows")

    fig = go.Figure(
        data=[
            go.Histogram(
                x=series,
                nbinsx=n_bins,
                marker_color=TEAL_PRIMARY,
                marker_line_color=CARD_BG,
                marker_line_width=1,
                opacity=0.85,
                hovertemplate="<b>Range:</b> %{x}<br><b>Count:</b> %{y:,}<extra></extra>"
            )
        ]
    )
    fig.update_layout(xaxis_title=feature_col, yaxis_title="Frequency")
    return apply_custom_theme(fig, f"Distribution Histogram: {feature_col}")


def create_feature_box_plot(
    df: pd.DataFrame,
    feature_col: str,
    label_col: str,
    selected_labels: Optional[List[str]] = None
) -> go.Figure:
    """Box plot comparing feature distributions across labels."""
    if df.empty or feature_col not in df.columns or label_col not in df.columns:
        fig = go.Figure()
        return apply_custom_theme(fig, "No Data for Feature Box Plot")

    subset = df.dropna(subset=[feature_col, label_col]).copy()
    subset[feature_col] = pd.to_numeric(subset[feature_col], errors="coerce")
    subset = subset.dropna(subset=[feature_col])

    if selected_labels:
        subset = subset[subset[label_col].isin(selected_labels)]
    else:
        top_labels = subset[label_col].value_counts().head(5).index
        subset = subset[subset[label_col].isin(top_labels)]

    fig = go.Figure()
    unique_lbls = subset[label_col].unique()

    for i, lbl in enumerate(unique_lbls):
        vals = subset[subset[label_col] == lbl][feature_col]
        fig.add_trace(
            go.Box(
                y=vals,
                name=str(lbl),
                marker_color=COLOR_SEQUENCE[i % len(COLOR_SEQUENCE)],
                boxmean=True,
                hovertemplate=f"<b>{lbl}</b><br>Value: %{{y}}<extra></extra>"
            )
        )

    fig.update_layout(xaxis_title="Traffic Label", yaxis_title=feature_col)
    return apply_custom_theme(fig, f"Feature Comparison Across Labels: {feature_col}")


def create_feature_scatter_plot(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    label_col: str,
    sample_limit: int = 1500,
    seed: int = 42
) -> go.Figure:
    """Deterministic sampled 2D scatter plot colored by label."""
    if df.empty or x_col not in df.columns or y_col not in df.columns or label_col not in df.columns:
        fig = go.Figure()
        return apply_custom_theme(fig, "Insufficient Variables for Scatter Plot")

    subset = df.dropna(subset=[x_col, y_col, label_col]).copy()
    subset[x_col] = pd.to_numeric(subset[x_col], errors="coerce")
    subset[y_col] = pd.to_numeric(subset[y_col], errors="coerce")
    subset = subset.dropna(subset=[x_col, y_col])

    if len(subset) > sample_limit:
        plot_df = subset.sample(n=sample_limit, random_state=seed)
        sub_title = f"{x_col} vs {y_col} (Sampled {sample_limit:,} points for UI speed)"
    else:
        plot_df = subset
        sub_title = f"{x_col} vs {y_col} ({len(plot_df):,} points)"

    fig = px.scatter(
        plot_df,
        x=x_col,
        y=y_col,
        color=label_col,
        color_discrete_sequence=COLOR_SEQUENCE,
        opacity=0.75,
        hover_data=[label_col]
    )
    fig.update_traces(marker={"size": 6})
    fig.update_layout(xaxis_title=x_col, yaxis_title=y_col)
    return apply_custom_theme(fig, sub_title)
