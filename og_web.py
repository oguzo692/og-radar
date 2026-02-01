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
            else: st.error("❌ Yanlış şifre")
        return False
    return True

if check_password():
    # --- 2. ZERO-GAP INDUSTRIAL CSS ---
    st.markdown("""
        <style>
        .main { background-color: #000000 !important; }
        :root { --soft-orange: #cc7a00; }
        
        /* Fiyat kutularını yazılara sıfırla */
        .glass-card {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(15px);
            border-radius: 6px;
            padding: 5px 12px !important; 
            border: 1px solid var(--soft-orange);
            margin-bottom: 5px;
            height: auto !important;
            min-height: 0px !important;
        }
        
        h1, h2, h3 { 
            color: var(--soft-orange) !important; 
            font-size: 20px !important; 
            margin: 0 !important;
            padding: 0 !important;
        }

        .match-row { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid rgba(204,122,0,0.2); }
        .status-win { color: #00ff41; font-weight: bold; }
        .status-loss { color: #ff4b4b; font-weight: bold; }
        .status-wait { color: #f1c40f; font-weight: bold; }
        
        section[data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 1px solid var(--soft-orange);
        }
        .block-container { padding-top: 1rem !important; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        page = st.radio("🚀 ürün", ["⚡ Ultra Atak Fon", "⚽️ FormLine", "📊 DashDash"])
        st.divider()
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
        with c1: st.markdown(f"<div class='glass-card'><small style='color:#666;'>TOPLAM</small><h2>${kasa:,.2f}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='glass-card'><small style='color:#666;'>BTC</small><h2>${data['BTC-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='glass-card'><small style='color:#666;'>ETH</small><h2>${data['ETH-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='glass-card'><small style='color:#666;'>SOL</small><h2>${data['SOL-USD']:,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()
        st.subheader("📑 İşlem Geçmişi")
        trades_df = pd.DataFrame([
            {"Coin": "BTC/USDT", "Tip": "🟢 Long", "K/Z": "+%2.4", "Durum": "Kapalı ✅"},
            {"Coin": "SOL/USDT", "Tip": "🔴 Short", "K/Z": "-%1.1", "Durum": "Kapalı ❌"},
            {"Coin": "ETH/USDT", "Tip": "🟢 Long", "K/Z": "+%0.8", "Durum": "Açık ⏳"}
        ])
        st.table(trades_df)

    # --- 5. FORM LINE (DETAYLAR GERİ GELDİ) ---
    elif page == "⚽️ FormLine":
        st.title("⚽️ FormLine Analizi")
        
        st.markdown("### 🔥 W2 Analizi (Güncel)")
        with st.container():
            st.markdown("""<div class='glass-card' style='height:auto;'>
                <div class='match-row'><span>GS - Kayserispor</span> <span class='status-win'>✅ İY +0.5 & W</span></div>
                <div class='match-row'><span>Liverpool - Newcastle</span> <span class='status-win'>✅ +2 & 1X</span></div>
                <div class='match-row'><span>BVB - Heidenheim</span> <span class='status-win'>✅ İY +0.5 & W</span></div>
                <div class='match-row'><span>Kocaelispor - FB</span> <span class='status-wait'>⏳ FB W & 2+</span></div>
                </div>""", unsafe_allow_html=True)
        
        st.markdown("### ⏪ W1 Analizi (Geçmiş)")
        with st.container():
            st.markdown("""<div class='glass-card' style='height:auto;'>
                <div class='match-row'><span>Karagümrük - GS</span> <span class='status-win'>✅ GS W</span></div>
                <div class='match-row'><span>New - Aston Villa</span> <span class='status-loss'>❌ NEW +2</span></div>
                <div class='match-row'><span>FB - Göztepe</span> <span class='status-loss'>❌ FB W</span></div>
                </div>""", unsafe_allow_html=True)

    # --- 6. DASH DASH ---
    elif page == "📊 DashDash":
        st.title
