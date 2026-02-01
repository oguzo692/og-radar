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
    # --- 2. COMPACT INDUSTRIAL CSS ---
    st.markdown("""
        <style>
        .main { background-color: #000000 !important; }
        :root { --soft-orange: #cc7a00; }
        
        /* Yazılara sıfır, sıkıştırılmış dikdörtgenler */
        .glass-card {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(15px);
            border-radius: 8px;
            padding: 10px 15px; /* Boşluklar azaltıldı */
            border: 1px solid var(--soft-orange);
            margin-bottom: 10px;
            height: auto; /* Yazıya göre daralan yükseklik */
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        h1, h2, h3 { 
            color: var(--soft-orange) !important; 
            font-size: 22px !important; 
            margin: 0 !important; /* Başlık boşlukları sıfırlandı */
        }
        
        div[data-testid="stMetricValue"] {
            color: var(--soft-orange) !important;
            font-size: 26px !important;
            line-height: 1.2 !important;
        }
        
        section[data-testid="stSidebar"] {
            background-color: #050505 !important;
            border-right: 1px solid var(--soft-orange);
        }
        
        /* Tablo görünümü iyileştirme */
        .stTable {
            background: rgba(255, 255, 255, 0.01);
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        page = st.radio("🚀 ürün", ["⚡ Ultra Atak Fon", "⚽️ FormLine", "📊 DashDash"])
        st.divider()
        
        if page == "⚡ Ultra Atak Fon":
            kasa = st.number_input("fon bakiyesi (USD)", value=600.0, step=0.1)
        else:
            kasa = 600.0
            
        st.info(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FON ---
    if page == "⚡ Ultra Atak Fon":
        st.title("⚡ Ultra Atak Fon")
        
        try:
            data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except:
            data = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        # Üst Metrikler (Sıkıştırılmış)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f"<div class='glass-card'><small style='color:#888;'>FON TOPLAM</small><h2>${kasa:,.2f}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='glass-card'><small style='color:#888;'>BTC/USDT</small><h2>${data['BTC-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='glass-card'><small style='color:#888;'>ETH/USDT</small><h2>${data['ETH-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='glass-card'><small style='color:#888;'>SOL/USDT</small><h2>${data['SOL-USD']:,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()
        
        # İŞLEM GEÇMİŞİ (Boş turuncu kutu kaldırıldı)
        st.subheader("📑 İşlem Geçmişi")
        
        trades_df = pd.DataFrame([
            {"Coin": "BTC/USDT", "Tip": "🟢 Long", "K/Z": "+%2.4", "Durum": "Kapalı ✅"},
            {"Coin": "SOL/USDT", "Tip": "🔴 Short", "K/Z": "-%1.1", "Durum": "Kapalı ❌"},
            {"Coin": "ETH/USDT", "Tip": "🟢 Long", "K/Z": "+%0.8", "Durum": "Açık ⏳"}
        ])
        
        st.table(trades_df)

    # --- 5. FORM LINE ---
    elif page == "⚽️ FormLine":
        st.title("⚽️ FormLine Analizi")
        st.markdown("<div class='glass-card' style='height:auto;'>W2 - GS ✅ | Liv ✅ | BVB ✅ | FB ⏳</div>", unsafe_allow_html=True)

    # --- 6. DASH DASH ---
    elif page == "📊 DashDash":
        st.title("📊 Performans DashDash")
        st.markdown("<div class='glass-card' style='height:auto;'>Sistem metrikleri optimize ediliyor.</div>", unsafe_allow_html=True)

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
