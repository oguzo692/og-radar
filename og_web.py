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
            else: 
                st.error("❌ Yanlış şifre")
        return False
    return True

if check_password():
    # --- 2. PREMIUM INDUSTRIAL CSS ---
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
        
        .match-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 16px;
        }
        
        h1, h2, h3 { color: var(--soft-orange) !important; margin: 0 !important; font-size: 22px !important; }
        section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid var(--soft-orange); }
        .block-container { padding-top: 1.5rem !important; }
        
        /* Tablo terminal stili */
        .stTable { background-color: transparent !important; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        page = st.radio("🚀 ürün", ["⚡ Ultra Atak Fon", "⚽️ FormLine", "📊 DashDash"])
        st.divider()
        kasa = st.number_input("Toplam Fon Bakiyesi (USD)", value=600.0, step=0.1)
        st.info(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FON ---
    if page == "⚡ Ultra Atak Fon":
        # 1. En Üst: Canlı Fiyatlar
        try:
            tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
            df_prices = yf.download(tickers, period="1d", interval="1m", progress=False)
            data = df_prices['Close'].iloc[-1]
        except:
            data = {"BTC-USD": 0.0, "ETH-USD": 0.0, "SOL-USD": 0.0}

        st.subheader("🚀 Canlı Fiyatlar")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='glass-card'><small style='color:#888;'>BTC</small><h2>${data['BTC-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='glass-card'><small style='color:#888;'>ETH</small><h2>${data['ETH-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='glass-card'><small style='color:#888;'>SOL</small><h2>${data['SOL-USD']:,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()

        # 2. Orta: Fon Bakiyesi ve Kişi Başı Dağılım
        st.title("⚡ Ultra Atak Fon")
        st.markdown(f"<h3 style='color: #888 !important; font-size: 18px !important; margin-top: -10px !important;'>Toplam Bakiye: ${kasa:,.2f}</h3>", unsafe_allow_html=True)
        
        # Kişi başı hesaplama
        kisi_basi = kasa / 3
        st.markdown("### 👥 Ortaklık Dağılımı")
        p1, p2, p3 = st.columns(3)
        with p1:
            st.markdown(f"<div class='glass-card' style='border-color:#555;'><small style='color:#888;'>oguzo</small><h3>${kisi_basi:,.2f}</h3></div>", unsafe_allow_html=True)
        with p2:
            st.markdown(f"<div class='glass-card' style='border-color:#555;'><small style='color:#888;'>fybey</small><h3>${kisi_basi:,.2f}</h3></div>", unsafe_allow_html=True)
        with p3:
            st.markdown(f"<div class='glass-card' style='border-color:#555;'><small style='color:#888;'>ero7</small><h3>${kisi_basi:,.2f}</h3></div>", unsafe_allow_html=True)

        st.divider()

        # 3. Alt: İşlem Geçmişi
        st.subheader("📑 İşlem Geçmişi")
        trades_df = pd.DataFrame([
            {"Coin": "BTC/USDT", "Tip": "🟢 Long", "K/Z": "+%2.4", "Durum": "Kapalı ✅"},
            {"Coin": "SOL/USDT", "Tip": "🔴 Short", "K/Z": "-%1.1", "Durum": "Kapalı ❌"},
            {"Coin": "ETH/USDT", "Tip": "🟢 Long", "K/Z": "+%0.8", "
