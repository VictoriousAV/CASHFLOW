"""Phase 1 components — bright high-contrast cards."""
import streamlit as st
from src.config import format_naira


def metric_card(title: str, value: int, sub: str = ""):
    st.markdown(f"""
    <div style="background:#fff;border:2px solid #000;border-radius:16px;
                padding:16px;box-shadow:4px 4px 0 #000">
      <div style="font-size:12px;font-weight:800;letter-spacing:.06em">{title.upper()}</div>
      <div style="font-size:28px;font-weight:800">{format_naira(value)}</div>
      <div style="font-size:12px;font-weight:600">{sub}</div>
    </div>""", unsafe_allow_html=True)


def forecast_banner(balance: int, avg_daily: float, days_left):
    msg = f"~{days_left} days" if days_left is not None else "—"
    st.markdown(f"""
    <div style="background:#00C853;color:#000;border:2px solid #000;
                border-radius:16px;padding:18px;box-shadow:4px 4px 0 #000">
      <small><b>ESTIMATED REMAINING</b></small>
      <div style="font-size:26px;font-weight:800">{msg}</div>
      <small><b>{format_naira(balance)} ÷ {format_naira(int(avg_daily))}/day • estimate, not guarantee</b></small>
    </div>""", unsafe_allow_html=True)


def ai_insight_card(text: str):
    st.markdown(f"""
    <div style="background:#E3F2FF;border:2px solid #000;border-radius:16px;padding:16px">
      🤖 <b>AI Insight</b><br/>{text}
    </div>""", unsafe_allow_html=True)
