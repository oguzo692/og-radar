import streamlit as st
import yfinance as yf
from datetime import datetime

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG VIP Radar", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK: ŞİFRE KORUMASI ---
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
            else:
                st.error("❌ Hatalı Şifre!")
        return False
    return True

if check_password():
    # --- 2. ÖZEL TASARIM (CSS) ---
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #00ff41 !important; }
        .coupon-card { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; margin-bottom: 15px; }
        .match-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #21262d; }
        .status-win { color: #00ff41 !important; font-weight: bold; }
        .status-loss { color: #ff4b4b !important; font-weight: bold; }
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
        st.caption("Veri Kaynağı: Manuel Giriş + Canlı Borsa ✅")

        try:
            data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except:
            data = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        col1, col2, col3, col4 = st.columns(4)
        ana_para = 600.0
        net_kar = kasa - ana_para
        kar_orani = (net_kar / ana_para) * 100
        
        col1.metric("💰 TOPLAM KASA", f"${kasa:,.2f}", f"%{kar_orani:+.1f}")
        col2.metric("🟠 BTC/USDT", f"${data['BTC-USD']:,.1f}")
        col3.metric("🔵 ETH/USDT", f"${data['ETH-USD']:,.1f}")
        col4.metric("🟣 SOL/USDT", f"${data['SOL-USD']:,.1f}")
        
        st.divider()
        st.subheader("👥 Ekip Kâr Dağıtımı")
        k_kar = net_kar / 3 if net_kar > 0 else 0.0
        m1, m2, m3 = st.columns(3)
        for col, name in zip([m1, m2, m3], ["oguzo", "ero7", "fybey"]):
            with col:
                st.markdown(f"<div class='member-card'><h3 style='margin:0; color:#8b949e;'>{name.upper()}</h3><p style='margin:0; font-size:1.2rem; color:#00ff41;'>Alacak: ${200+k_kar:,.2f}</p></div>", unsafe_allow_html=True)

    # --- 5. SAYFA: OG FORMLINE ---
    elif page == "📈 OG FormLine":
        st.title("📈 OG FormLine | Kupon Analiz Merkezi")
        tab1, tab2 = st.tabs(["🔥 W2 Kuponu (1-2 Şubat)", "⏪ W1 Kuponu (24-25 Ocak)"])

        with tab1:
            st.markdown("""
            <div class='coupon-card' style='border-color: #ff4b4b;'>
                <h3 style='color: #ff4b4b;'>❌ W2 Kuponu (1-2 Şubat) - KAYBETTİ</h3>
                <div class='match-row'><span>GS - Kayserispor</span> <span class='status-win'>İY +0.5 & W & 2+ ✅</span></div>
                <div class='match-row'><span>Liv - Newcastle</span> <span class='status-win'>+2 & Liverpool 1X ✅</span></div>
                <div class='match-row'><span>BVB - Heidenheim</span> <span class='status-loss'>İY +0.5 & W & 2+ ❌</span></div>
                <div class='match-row'><span>Kocaelispor - FB</span> <span class='status-loss'>FB W & 2+ ❌</span></div>
                <br><p><b>Toplam Oran:</b> 5.53 | <b>Bütçe:</b> 100 USD | <b>Sonuç:</b> <span class='status-loss'>-100 USD</span></p>
            </div>""", unsafe_allow_html=True)

        with tab2:
            st.markdown("""
            <div class='coupon-card' style='border-color: #ff4b4b;'>
                <h3 style='color: #ff4b4b;'>❌ W1 Kuponu (24-25 Ocak) - KAYBETTİ</h3>
                <div class='match-row'><span>Karagümrük - GS</span> <span class='status-win'>GS W & +2 ✅</span></div>
                <div class='match-row'><span>Bournemouth - Liv</span> <span class='status-win'>KG VAR ✅</span></div>
                <div class='match-row'><span>Union Berlin - BVB</span> <span class='status-loss'>BVB İY 0.5 ÜST ❌</span></div>
                <div class='match-row'><span>New - Aston Villa</span> <span>NEW +2</span></div>
                <div class='match-row'><span>FB - Göztepe</span> <span>FB W</span></div>
                <br><p><b>Toplam Oran:</b> 7.09 | <b>Bütçe:</b> 100 USD | <b>Sonuç:</b> <span class='status-loss'>-100 USD</span></p>
            </div>""", unsafe_allow_html=True)

    # --- 6. SAYFA: OG DASHDASH ---
    elif page == "📊 OG DashDash":
        st.title("📊 OG DashDash")
        st.info("Bu sekme yakında aktif edilecek.")

    st.divider()
    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
