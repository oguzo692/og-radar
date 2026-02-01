import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np

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
            else: st.error("❌ Götten sallama aq ya")
        return False
    return True

if check_password():
    # --- 2. REFINED INDUSTRIAL ORANGE CSS ---
    st.markdown("""
        <style>
        .main { background-color: #000000; }
        :root { --soft-orange: #cc7a00; }
        .glass-card {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(15px);
            border-radius: 10px;
            padding: 20px;
            border: 1px solid var(--soft-orange);
            box-shadow: 0 4px 15px rgba(204, 122, 0, 0.1);
            margin-bottom: 20px;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        h1, h2, h3 { 
            color: var(--soft-orange) !important; 
            font-size: 24px !important; 
            margin-bottom: 10px !important;
        }
        div[data-testid="stMetricValue"] {
            color: var(--soft-orange) !important;
            font-size: 28px !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid var(--soft-orange);
        }
        .table-container {
            border: 1px solid var(--soft-orange);
            border-radius: 10px;
            padding: 10px;
            background: rgba(255, 255, 25
