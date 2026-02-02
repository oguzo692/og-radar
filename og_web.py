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
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 15px;
        }
        .status-win { color: #00ff41; font-weight: bold; }
        .status-loss { color: #ff4b4b; font-weight: bold; }
        .status-wait { color: #f1c40f; font-weight: bold; }
        h1, h2, h3 { color: var(--soft-orange) !important; margin: 0 !important; font-size: 22px !important; }
        section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid var(--soft-orange); }
        .block-container { padding-top: 1.5rem !important; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        page = st.radio("🚀 ürün", ["⚡ Ultra Atak Fonu", "⚽️ FormLine", "📊 DashDash"])
        st.divider()
        
        if page == "⚡ Ultra Atak Fonu":
            kasa = st.number_input("fon bakiyesi (USD)", value=600.0, step=0.1)
        else:
            kasa = 600.0
            
        try:
            tr_tz = pytz.timezone('Europe/Istanbul')
            tr_time = datetime.now(tr_tz).strftime('%H:%M:%S')
            st.info(f"🕒 Sistem Zamanı: {tr_time}")
        except:
            st.info(f"🕒 Zaman: {datetime.now().strftime('%H:%M:%S')}")

        if st.button("🔴 çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FONU ---
    if page == "⚡ Ultra Atak Fonu":
        st.title("⚡ Ultra Atak Fon")
        try:
            # Canlı fiyat çekimi
            data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except:
            data = {"BTC-USD": 0.0, "ETH-USD": 0.0, "SOL-USD": 0.0}

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='glass-card'><small style='color:#888;'>TOPLAM</small><h2>${kasa:,.2f}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='glass-card'><small style='color:#888;'>BTC</small><h2>${data.get('BTC-USD', 0):,.1f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='glass-card'><small style='color:#888;'>ETH</small><h2>${data.get('ETH-USD', 0):,.1f}</h2></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='glass-card'><small style='color:#888;'>SOL</small><h2>${data.get('SOL-USD', 0):,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()
        st.subheader("📑 İşlem Geçmişi")
        # Parantez hatalarını önlemek için temiz liste
        df_trades = pd.DataFrame([
            {"Coin": "BTC/USDT", "Yön": "🟢 Long", "K/Z": "+%2.4", "Sonuç": "Kapalı ✅"},
            {"Coin": "ETH/USDT", "Yön": "🟢 Long", "K/Z": "+%0.8", "Sonuç": "Açık ⏳"}
        ])
        st.table(df_trades)

    # --- 5. FORM LINE ---
    elif page == "⚽️ FormLine":
        st.title("⚽️ FormLine Analizi")
        t1, t2, t3 = st.tabs(["🔥 W3 (8-9 Şub)", "🔥 W2 (1-2 Şub)", "⏪ W1 (Geçmiş)"])
        
        with t1:
            st.markdown("<div class='glass-card'>W3 Kuponu Yakında...</div>", unsafe_allow_html=True)
        
        with t2:
            st.markdown("""<div class='coupon-card'>
                <h2 style='color:#f1c40f;'>✅ W2 - KAZANDI</h2><br>
                <div class='match-row'><span>GS - Kayserispor</span><span class='status-win'>GS W & +2.5 ÜST ✅</span></div>
                <div class='match-row'><span>Liverpool - Newcastle</span><span class='status-win'>KG VAR ✅</span></div>
                <div class='match-row'><span>BVB - Heidenheim</span><span class='status-win'>BVB İY 0.5 ÜST ✅</span></div>
                <div class='match-row'><span>Kocaelispor - FB</span><span class='status-win'>FB W & 1.5 ÜST ✅</span></div>
                <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 20px 0;'>
                <p><b>Toplam Oran: 5.40 | Bütçe: 100 USD | Durum: Sonuçlandı</b></p>
                </div>""", unsafe_allow_html=True)
                
        with t3:
            st.markdown("""<div class='coupon-card' style='border-color:#ff4b4b;'>
                <h2 style='color:#ff4b4b;'>❌ W1 - KAYBETTİ</h2><br>
                <div class='match-row'><span>Karagümrük - GS</span><span class='status-win'>GS W & +1.5 ÜST ✅</span></div>
                <div class='match-row'><span>Bournemouth - Liv</span><span class='status-win'>KG VAR ✅</span></div>
                <div class='match-row'><span>New - Aston Villa</span><span class='status-loss'>MS 1 ❌</span></div>
                <div class='match-row'><span>FB - Göztepe</span><span class='status-loss'>İY 0.5 ÜST ❌</span></div>
                <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 20px 0;'>
                <p><b>Toplam Oran: 7.09 | Bütçe: 100 USD | Sonuç: -100 USD</b></p>
                </div>""", unsafe_allow_html=True)

    # --- 6. DASH DASH ---
    elif page == "📊 DashDash":
        st.title("📊 DashDash")
        st.markdown("<div class='glass-card'>DashDash modülü optimize ediliyor.</div>", unsafe_allow_html=True)

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
