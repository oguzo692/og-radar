import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG Core", page_icon="🛡️", layout="wide")

# --- GÜVENLİK KONTROLÜ ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.title("🔐 OG Core Login")
        pwd = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Yanlış şifre")
        return False
    return True

if check_password():
    # --- CSS TASARIM (HATASIZ) ---
    st.markdown("""
        <style>
        .main { background-color: #0d1117 !important; }
        :root { --soft-orange: #cc7a00; }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 8px;
            padding: 10px 15px !important;
            border: 1px solid var(--soft-orange);
            margin-bottom: 15px;
        }
        
        .coupon-card {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 12px;
            padding: 20px;
            border: 2px solid var(--soft-orange);
            margin-bottom: 20px;
        }
        
        .match-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 15px;
        }
        
        .status-win { color: #00ff41; font-weight: bold; }
        .status-loss { color: #ff4b4b; font-weight: bold; }
        .status-wait { color: #f1c40f; font-weight: bold; }
        
        h1, h2, h3 { color: var(--soft-orange) !important; margin: 0 !important; }
        section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid var(--soft-orange); }
        .stTable { background-color: transparent !important; }
        </style>
        """, unsafe_allow_html=True)

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        page = st.radio("🚀 MENÜ", ["⚡ Ultra Atak Fon", "⚽️ FormLine", "📊 DashDash"])
        st.divider()
        kasa = st.number_input("FON BAKİYESİ (USD)", value=600.0, step=10.0)
        st.info(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- SAYFA 1: ULTRA ATAK FON ---
    if page == "⚡ Ultra Atak Fon":
        
        # 1. BÖLÜM: CANLI FİYATLAR (EN ÜSTTE)
        st.subheader("🚀 Canlı Fiyatlar")
        
        try:
            tickers =
