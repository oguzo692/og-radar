import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np
import pytz

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG Core", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.title("🔐 OG Core")
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
    # --- 2. PREMIUM INDUSTRIAL CSS (HATASIZ) ---
    st.markdown("""
        <style>
        .main { background-color: #0d1117 !important; }
        :root { --soft-orange: #cc7a00; }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 8px;
            padding: 8px 12px !important;
            border: 1px solid var(--soft-orange);
            margin-bottom: 10px;
            height: auto !important;
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
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 16px;
        }
