import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- 1. AYARLAR ---
st.set_page_config(page_title="OG Core v5.0", page_icon="🛡️", layout="wide")

# --- 2. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align:center; color:#cc7a00;'>🛡️ OG_CORE AUTH</h1>", unsafe_allow_html=True)
        pwd = st.text_input("ŞİFRE", type="password")
        if st.button("Giriş Yap"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Yanlış şifre")
        return False
    return True

if check_password():
    # --- 3. RETRO INDUSTRIAL CSS ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        .main { background-color: #0d1117 !important; }
        * { font-family: 'Inter', sans-serif !important; }
        :root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; }
        
        .industrial-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--soft-orange);
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 4px 4px 0px 0px rgba(204, 122, 0, 0.2);
        }
        .match-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            font-size: 14px;
        }
        .status-win { color: var(--win-green); font-weight: bold; }
        .status-loss { color: var(--loss-red); font-weight: bold; }
        .status-wait { color: #f1c40f; font-weight: bold; }
        
        h1, h2, h3 { color: var(--soft-orange) !important; margin-bottom: 10px !important; }
        section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid var(--soft-orange); }
        </style>
    """, unsafe_allow_html=True)

    # --- 4. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG CORE")
        page = st.radio("MENÜ", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("TOPLAM KASA (USD)", value=600.0, step=0.1)
        
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.info(f"🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}")
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 5. ULTRA FON (3 KİŞİLİK PAYLAŞIM) ---
    if page == "⚡ ULTRA FON":
        st.title("⚡ ULTRA ATAK FONU")
        
        # Canlı Fiyat Takibi
        try:
            tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
            prices = yf.download(tickers, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
            btc_p, eth_p, sol_p = prices['BTC-USD'], prices['ETH-USD'], prices['SOL-USD']
        except:
            btc_p, eth_p, sol_p = 0.0, 0.0, 0.0

        st.subheader("🚀 Canlı Piyasalar")
        f1, f2, f3 = st.columns(3)
        with f1: st.markdown(f"<div class='industrial-card'><small>BTC</small><h2>${btc_p:,.1f}</h2></div>", unsafe_allow_html=True)
        with f2: st.markdown(f"<div class='industrial-card'><small>ETH</small><h2>${eth_p:,.1f}</h2></div>", unsafe_allow_html=True)
        with f3: st.markdown(f"<div class='industrial-card'><small>SOL</small><h2>${sol_p:,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()
        
        # Ortaklık Dağılımı (oguzo, fybey ve ero7)
        pay = kasa / 3
        st.subheader("👥 Ortaklık Dağılımı")
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='industrial-card'><small>OGUZO</small><h3>${pay:,.2f}</h3></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='industrial-card'><small>FYBEY</small><h3>${pay:,.2f}</h3></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='industrial-card'><small>ERO7</small><h3>${pay:,.2f}</h3></div>", unsafe_allow_html=True)

    # --- 6. FORM LINE (W1, W2, W3 TAM LİSTE) ---
    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE ANALİZLERİ")
        t1, t2, t3 = st.tabs(["🔥 W3 (8-9 Şub)", "✅ W2 (1-2 Şub)", "⏪ W1 (Geçmiş)"])

        with t1:
            st.markdown("""<div class='industrial-card'>
                <h3>🔥 W3 KUPONU</h3>
                <div class='match-row'><span>Analizler Bekleniyor...</span><span class='status-wait'>⏳</span></div>
                <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 15px 0;'>
                <p>Cuma günü güncellenecektir.</p>
            </div>""", unsafe_allow_html=True)

        with t2:
            st.markdown("""<div class='industrial-card' style='border-color: #00ff41;'>
                <h3 style='color:#00ff41 !important;'>✅ W2 KUPONU - KAZANDI</h3>
                <div class='match-row'><span>GS - Kayserispor</span><span class='status-win'>GS W & +2.5 ÜST ✅</span></div>
                <div class='match-row'><span>Liverpool - Newcastle</span><span class='status-win'>KG VAR ✅</span></div>
                <div class='match-row'><span>BVB - Heidenheim</span><span class='status-win'>BVB İY 0.5 ÜST ✅</span></div>
                <div class='match-row'><span>Kocaelispor - FB</span><span class='status-win'>FB W & 1.5 ÜST ✅</span></div>
                <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 15px 0;'>
                <p><b>Oran: 5.40 | Bütçe: 100 USD | Durum: Sonuçlandı</b></p>
            </div>""", unsafe_allow_html=True)

        with t3:
            st.markdown("""<div class='industrial-card' style='border-color: #ff4b4b;'>
                <h3 style='color:#ff4b4b !important;'>❌ W1 KUPONU - KAYBETTİ</h3>
                <div class='match-row'><span>Karagümrük - GS</span><span class='status-win'>GS W & +1.5 ÜST ✅</span></div>
                <div class='match-row'><span>Bournemouth - Liv</span><span class='status-win'>KG VAR ✅</span></div>
                <div class='match-row'><span>New - Aston Villa</span><span class='status-loss'>MS 1 ❌</span></div>
                <div class='match-row'><span>FB - Göztepe</span><span class='status-loss'>İY 0.5 ÜST ❌</span></div>
                <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 15px 0;'>
                <p><b>Oran: 7.09 | Bütçe: 100 USD | Sonuç: -100 USD</b></p>
            </div>""", unsafe_allow_html=True)

    # --- 7. DASH DASH ---
    elif page == "📊 DASHDASH":
        st.title("📊 DASHDASH ANALİZ")
        st.info("Haftalık performans grafikleri optimize ediliyor.")

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
