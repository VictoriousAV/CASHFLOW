"""Phase 1 components — Complete UI color system (#064E3B / #D6B779)."""
import streamlit as st
from src.config import format_naira


def metric_card(title: str, value: int, sub: str = ""):
    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #E5E1D8;border-radius:16px;
                padding:16px;box-shadow:0 2px 8px rgba(6,78,59,.08);color:#202923">
      <div style="font-size:12px;font-weight:800;letter-spacing:.06em">{title.upper()}</div>
      <div style="font-size:28px;font-weight:800">{format_naira(value)}</div>
      <div style="font-size:12px;font-weight:600">{sub}</div>
    </div>""", unsafe_allow_html=True)


def forecast_banner(balance: int, avg_daily: float, days_left):
    msg = f"~{days_left} days" if days_left is not None else "—"
    st.markdown(f"""
    <div style="background:#064E3B;color:#FFFFFF;border:1px solid #043D2F;
                border-radius:16px;padding:18px">
      <small><b>ESTIMATED REMAINING</b></small>
      <div style="font-size:26px;font-weight:800">{msg}</div>
      <small><b>{format_naira(balance)} ÷ {format_naira(int(avg_daily))}/day • estimate, not guarantee</b></small>
    </div>""", unsafe_allow_html=True)


def ai_insight_card(text: str):
    st.markdown(f"""
    <div style="background:#FFFFFF;border:1px solid #D6B779;border-radius:16px;padding:16px;color:#202923">
      🤖 <b>AI Insight</b><br/>{text}
    </div>""", unsafe_allow_html=True)
