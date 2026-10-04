"""Plotly charts with graceful fallback (Phase 4/6)."""
from __future__ import annotations


def donut_figure(totals: dict, colors: dict | None = None):
    try:
        import plotly.graph_objects as go
    except ImportError:
        return None
    labels = list(totals.keys()) or ["No data"]
    values = list(totals.values()) or [1]
    marker = {"colors": [colors.get(k, "#9E9E9E") for k in labels]} if colors else None
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.55, marker=marker))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=300)
    return fig


def trend_figure(daily: dict):
    try:
        import plotly.graph_objects as go
    except ImportError:
        return None
    fig = go.Figure(go.Scatter(x=list(daily.keys()), y=list(daily.values()), mode="lines+markers"))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260)
    return fig


def forecast_figure(projection: list[tuple[int, int]]):
    try:
        import plotly.graph_objects as go
    except ImportError:
        return None
    fig = go.Figure(go.Scatter(x=[d for d, _ in projection], y=[v for _, v in projection],
                               mode="lines", fill="tozeroy"))
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260,
                      xaxis_title="Days", yaxis_title="₦")
    return fig
