import streamlit as st
import yfinance as yf
from datetime import datetime

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG Core Suite", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.title("🔐 OG Core Erişim Paneli")
        pwd = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if pwd == "og2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ Götten sallama aq ya")
        return False
    return True

if check_password():
    # --- 2. CSS TASARIM (Premium Dark) ---
    st.markdown("""
        <style>
        .main { background-color: #0d1117; }
        .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
        div[data-testid="stMetricValue"] { color: #00ff41 !important; }
        .coupon-card { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; margin-bottom: 15px; }
        .match-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #21262d; }
        .status-win { color: #00ff41 !important; font-weight: bold; }
        .status-loss { color: #ff4b4b !important; font-weight: bold; }
        .status-wait { color: #f1c40f !important; font-weight: bold; }
        .member-card { background-color: #1c2128; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR (OG CORE) ---
    with st.sidebar:
        st.title("🛡️ OG Core") # Panel Genel Adı Değişti
        # Sekme Adı "Ultra Atak Fon" Olarak Güncellendi
        page = st.radio("🚀 Strateji Yönetimi", ["⚡ Ultra Atak Fon", "📈 OG FormLine", "📊 OG DashDash"])
        st.divider()
        if page == "⚡ Ultra Atak Fon":
            st.subheader("⚙️ Fon Yönetimi")
            kasa = st.number_input("Güncel Fon Bakiyesi (USD)", value=1200.0, step=0.1)
        st.info(f"🕒 Sistem Zamanı: {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 Güvenli Çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FON (ESKİ TRADE RADAR) ---
    if page == "⚡ Ultra Atak Fon":
        st.title("⚡ Ultra Atak Fon Yönetimi")
        st.caption("Risk Seviyesi: Yüksek | Veri Kaynağı: Canlı Veri + Manuel Giriş ✅")

        try:
            data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except: data = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        c1, c2, c3, c4 = st.columns(4)
        ana_para = 600.0
        net_kar = kasa - ana_para
        c1.metric("💰 FON TOPLAM", f"${kasa:,.2f}", f"%{((net_kar/ana_para)*100):+.1f}")
        c2.metric("🟠 BTC/USDT", f"${data['BTC-USD']:,.1f}")
        c3.metric("🔵 ETH/USDT", f"${data['ETH-USD']:,.1f}")
        c4.metric("🟣 SOL/USDT", f"${data['SOL-USD']:,.1f}")
        
        st.divider()
        st.subheader("👥 Fon Kâr Paylaşımı")
        k_kar = net_kar / 3 if net_kar > 0 else 0.0
        m1, m2, m3 = st.columns(3)
        for col, name in zip([m1, m2, m3], ["oguzo", "ero7", "fybey"]):
            with col:
                st.markdown(f"<div class='member-card'><h3 style='margin:0; color:#8b949e;'>{name.upper()}</h3><p style='margin:0; font-size:1.2rem; color:#00ff41;'>Net Alacak: ${200+k_kar:,.2f}</p></div>", unsafe_allow_html=True)

    # --- 5. OG FOR
