import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

# --- 1. AYARLAR ---
st.set_page_config(page_title="OG Core", page_icon="🛡️", layout="wide")

# --- 2. GÜVENLİK ---
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
    # --- 3. CSS (TEK PARÇA, HATASIZ) ---
    st.markdown("""
        <style>
        .main { background-color: #0d1117 !important; }
        :root { --soft-orange: #cc7a00; }
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 8px;
            padding: 12px 18px;
            border: 1px solid var(--soft-orange);
            margin-bottom: 15px;
        }
        h1, h2, h3 { color: var(--soft-orange) !important; margin: 0 !important; }
        section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid var(--soft-orange); }
        .stTable { background-color: transparent !important; }
        </style>
    """, unsafe_allow_html=True)

    # --- 4. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        page = st.radio("🚀 MENÜ", ["⚡ Ultra Atak Fon", "⚽️ FormLine", "📊 DashDash"])
        st.divider()
        kasa_input = st.number_input("TOPLAM FON (USD)", value=600.0, step=10.0)
        st.info(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 5. ULTRA ATAK FON ---
    if page == "⚡ Ultra Atak Fon":
        # Canlı Fiyat Çekimi
        try:
            tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
            df_prices = yf.download(tickers, period="1d", interval="1m", progress=False)
            btc_p = df_prices['Close']['BTC-USD'].iloc[-1]
            eth_p = df_prices['Close']['ETH-USD'].iloc[-1]
            sol_p = df_prices['Close']['SOL-USD'].iloc[-1]
        except:
            btc_p, eth_p, sol_p = 0.0, 0.0, 0.0

        # Bölüm 1: Fiyatlar (En Üstte)
        st.subheader("🚀 Canlı Fiyatlar")
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown(f"<div class='glass-card'><small style='color:#888;'>BTC</small><h2>${btc_p:,.1f}</h2></div>", unsafe_allow_html=True)
        with f2:
            st.markdown(f"<div class='glass-card'><small style='color:#888;'>ETH</small><h2>${eth_p:,.1f}</h2></div>", unsafe_allow_html=True)
        with f3:
            st.markdown(f"<div class='glass-card'><small style='color:#888;'>SOL</small><h2>${sol_p:,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()

        # Bölüm 2: Toplam Bakiye ve Ortak Dağılımı
        st.title("⚡ Ultra Atak Fon")
        st.markdown(f"<h3 style='color: #888; margin-bottom: 20px;'>Toplam Bakiye: ${kasa_input:,.2f}</h3>", unsafe_allow_html=True)
