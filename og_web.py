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
        pwd = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if pwd == "og2026":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ Hatalı Şifre!")
        return False
    return True

if check_password():
    # --- 2. CSS TASARIM ---
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        .coupon-card { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; margin-bottom: 15px; }
        .match-row { display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #21262d; }
        .status-win { color: #00ff41; font-weight: bold; }
        .status-loss { color: #ff4b4b; font-weight: bold; }
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
        st.button("🔴 Güvenli Çıkış", on_click=lambda: st.session_state.update({"password_correct": False}))

    # --- 4. SAYFA: TRADE RADAR ---
    if page == "🛡️ Trade Radar":
        st.title("🛡️ OG Trade Discipline Radar")
        data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        
        col1, col2, col3, col4 = st.columns(4)
        ana_para = 600.0
        net_kar = kasa - ana_para
        col1.metric("💰 TOPLAM KASA", f"${kasa:,.2f}", f"%{((net_kar/ana_para)*100):+.1f}")
        col2.metric("🟠 BTC/USDT", f"${data['BTC-USD']:,.1f}")
        col3.metric("🔵 ETH/USDT", f"${data['ETH-USD']:,.1f}")
        col4.metric("🟣 SOL/USDT", f"${data['SOL-USD']:,.1f}")
        
        st.divider()
        st.subheader("👥 Ekip Kâr Dağıtımı")
        k_kar = net_kar / 3 if net_kar > 0 else 0.0
        m1, m2, m3 = st.columns(3)
        for c, name in zip([m1, m2, m3], ["oguzo", "ero7", "fybey"]):
            c.markdown(f"<div class='coupon-card'><h3>{name.upper()}</h3><p>Alacak: ${200+k_kar:,.2f}</p></div>", unsafe_allow_html=True)

    # --- 5. SAYFA: OG FORMLINE ---
    elif page == "📈 OG FormLine":
        st.title("📈 OG FormLine | Kupon Analiz Merkezi")
        
        tab1, tab2 = st.tabs(["🔥 Bu Haftanın Kuponu (W2)", "⏪ Geçen Hafta (W1)"])

        with tab1: # 1-2 ŞUBAT KUPONU
            st.markdown("""
            <div class='coupon-card'>
                <h3>🎯 W2 Kuponu (1-2 Şubat)</h3>
                <div class='match-row'><span>GS - Kayserispor</span> <span>İY +0.5 & W & 2+ (1.50)</span></div>
                <div class='match-row'><span>Liv - Newcastle</span> <span>+2 & Liverpool 1X (1.51)</span></div>
                <div class='match-row'><span>BVB - Heidenheim</span> <span>İY +0.5 & W & 2+ (1.64)</span></div>
                <div class='match-row'><span>Kocaelispor - FB</span> <span>FB W & 2+ (1.50)</span></div>
                <br>
                <p><b>Toplam Oran:</b> 5.53 | <b>Bütçe:</b> 100 USD | <b>Potansiyel:</b> 553 USD</p>
                <p><b>Durum:</b> ⏳ Beklemede</p>
            </div>
            """, unsafe_allow_html=True)

        with tab2: # 24-25 OCAK KUPONU
            st.markdown("""
            <div class='coupon-card' style='border-color: #ff4b4b;'>
                <h3 style='color: #ff4b4b;'>❌ W1 Kuponu (24-25 Ocak)</h3>
                <div class='match-row'><span>Karagümrük - GS</span> <span class='status-win'>GS W & +2 (1.44) ✅</span></div>
                <div class='match-row'><span>Bournemouth - Liv</span> <span class='status-win'>KG VAR (1.52) ✅</span></div>
                <div class='match-row'><span>Union Berlin - BVB</span> <span class='status-loss'>BVB İY 0.5 ÜST (1.20) ❌</span></div>
                <div class='match-row'><span>New - Aston Villa</span> <span>NEW +2 (1.79)</span></div>
                <div class='match-row'><span>FB - Göztepe</span> <span>FB W (1.51)</span></div>
                <br>
                <p><b>Toplam Oran:</b> 7.09 | <b>Sonuç:</b> -100 USD</p>
                <p class='status-loss'>DURUM: KAYBETTİ</p>
            </div>
            """, unsafe_allow_html=True)

    # --- 6. SAYFA: OG DASHDASH ---
    elif page == "📊 OG DashDash":
        st.title("📊 OG DashDash")
        st.info("Bu sekme çok yakında yeni analiz araçlarıyla aktif edilecek kanka!")

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
