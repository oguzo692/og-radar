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
    # --- 2. BLACK & ORANGE PREMIUM CSS (GLASSMORPHISM) ---
    st.markdown("""
        <style>
        .main { background-color: #000000; }
        .glass-card {
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(15px);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid #ff9900;
            box-shadow: 0 4px 15px rgba(255, 153, 0, 0.15);
            margin-bottom: 20px;
        }
        h1, h2, h3 { color: #ff9900 !important; }
        div[data-testid="stMetricValue"] {
            color: #ff9900 !important;
            text-shadow: 0 0 10px rgba(255, 153, 0, 0.5);
        }
        section[data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #ff9900;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        page = st.radio("🚀 Strateji Yönetimi", ["⚡ Ultra Atak Fon", "📈 OG FormLine", "📊 OG DashDash"])
        st.divider()
        if page == "⚡ Ultra Atak Fon":
            st.subheader("⚙️ Fon Yönetimi")
            kasa = st.number_input("Güncel Fon Bakiyesi (USD)", value=600.0, step=0.1)
        st.info(f"🕒 Sistem Zamanı: {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 Güvenli Çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FON ---
    if page == "⚡ Ultra Atak Fon":
        st.title("⚡ Ultra Atak Fon Yönetimi")
        try:
            data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except: data = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        c1, c2, c3, c4 = st.columns(4)
        ana_para = 600.0
        net_kar = kasa - ana_para
        with c1: st.markdown(f"<div class='glass-card'>💰 FON TOPLAM<br><h2>${kasa:,.2f}</h2><small>%{((net_kar/ana_para)*100):+.1f}</small></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='glass-card'>🟠 BTC/USDT<br><h2>${data['BTC-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='glass-card'>🔵 ETH/USDT<br><h2>${data['ETH-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='glass-card'>🟣 SOL/USDT<br><h2>${data['SOL-USD']:,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()
        st.subheader("📑 Operasyon Geçmişi")
        trades = [
            {"Coin": "BTC/USDT", "Tip": "🟢 Long", "K/Z": "+%2.4", "Durum": "Kapalı ✅"},
            {"Coin": "SOL/USDT", "Tip": "🔴 Short", "K/Z": "-%1.1", "Durum": "Kapalı ❌"},
            {"Coin": "ETH/USDT", "Tip": "🟢 Long", "K/Z": "+%0.8", "Durum": "Açık ⏳"},
        ]
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.table(pd.DataFrame(trades))
        st.markdown("</div>", unsafe_allow_html=True)

    # --- 5. OG FORMLINE ---
    elif page == "📈 OG FormLine":
        st.title("📈 OG FormLine Analizi")
        st.markdown("<div class='glass-card'><h4>W2 - 3/4 TAMAM</h4>GS ✅ | Liv ✅ | BVB ✅ | FB ⏳</div>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'><h4>W1 - KAYBETTİ</h4>GS ✅ | Liv ✅ | BVB ✅ | New ❌ | FB ❌</div>", unsafe_allow_html=True)

    # --- 6. OG DASHDASH ---
    elif page == "📊 OG DashDash":
        st.title("📊 OG DashDash Performance")
        st.subheader("📈 Kasa Momentum Çizelgesi")
        chart_data = pd.DataFrame(np.random.randn(7, 1).cumsum() + 600, columns=['Kasa Değeri'])
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.area_chart(chart_data, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
