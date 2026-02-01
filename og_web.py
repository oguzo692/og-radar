ximport streamlit as st
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
            background: rgba(255, 255, 255, 0.01);
        }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR (İSİMLERİ SABİTLEDİK) ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        # Menüdeki isimler ile aşağıdaki IF kontrolleri tam eşleşmeli
        page = st.radio("🚀 ürün", ["⚡ Ultra Atak Fon", "⚽️ FormLine", "📊 DashDash"])
        st.divider()
        
        # Seçili sayfaya göre bakiye girişi göster
        if page == "⚡ Ultra Atak Fon":
            kasa = st.number_input("fon bakiyesi (USD)", value=600.0, step=0.1)
        
        st.info(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FON ---
    if page == "⚡ Ultra Atak Fon":
        st.title("⚡ Ultra Atak Fon")
        
        try:
            data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except: data = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='glass-card'>💰 FON TOPLAM<br><h2>${kasa:,.2f}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='glass-card'>🟠 BTC/USDT<br><h2>${data['BTC-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='glass-card'>🔵 ETH/USDT<br><h2>${data['ETH-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='glass-card'>🟣 SOL/USDT<br><h2>${data['SOL-USD']:,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()
        st.subheader("📑 işlem Geçmişi")
        trades = [
            {"Coin": "BTC/USDT", "Tip": "🟢 Long", "K/Z": "+%2.4", "Durum": "Kapalı ✅"},
            {"Coin": "SOL/USDT
