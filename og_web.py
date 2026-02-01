import streamlit as st
import yfinance as yf
from datetime import datetime

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG VIP Radar", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.title("🔐 OG VIP Erişim Paneli")
        pwd = st.text_input("Panel Şifresini Giriniz", type="password")
        if st.button("Giriş Yap"):
            if pwd == "og2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ Hatalı Şifre!")
        return False
    return True

if check_password():
    # --- 2. ÖZEL TASARIM (CSS) ---
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        .coupon-card { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; margin-bottom: 15px; }
        .match-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #21262d; }
        .status-win { color: #00ff41 !important; font-weight: bold; }
        .status-loss { color: #ff4b4b !important; font-weight: bold; }
        .status-wait { color: #f1c40f !important; font-weight: bold; }
        .member-card { background-color: #1c2128; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.title("🛡️ OG Core Suite")
        page = st.radio("🚀 Hizmetler", ["🛡️ Trade Radar", "📈 OG FormLine", "📊 OG DashDash"])
        st.divider()
        if page == "🛡️ Trade Radar":
            st.subheader("⚙️ Portföy Kontrol")
            kasa = st.number_input("Güncel Kasa (USD)", value=1200.0, step=0.1)
        st.info(f"🕒 Sistem Saati: {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 Güvenli Çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. SAYFA: TRADE RADAR ---
    if page == "🛡️ Trade Radar":
        st.title("🛡️ OG Trade Discipline Radar")
        try:
            data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except: data = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        col1, col2, col3, col4 = st.columns(4)
        ana_para = 600.0
        net_kar = kasa - ana_para
        col1.metric("💰 TOPLAM KASA", f"${kasa:,.2f}", f"%{((net_kar/ana_para)*100):+.1f}")
        col2.metric("🟠 BTC/USDT", f"${data['BTC-USD']:,.1f}")
        col3.metric
