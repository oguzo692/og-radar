import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG Core Retro", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align:center; color:#cc7a00; font-family:\"Courier New\", Courier, monospace;'>🔐 OG_CORE_RETRO_v5.0</h1>", unsafe_allow_html=True)
        pwd = st.text_input("ŞİFRE GİRİNİZ", type="password")
        if st.button("SİSTEME GİR"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ ERİŞİM ENGELLENDİ")
        return False
    return True

if check_password():
    # --- 2. PIXEL RETRO CSS ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        .main { background-color: #0d1117 !important; }
        
        /* Genel Font Ayarı */
        * { font-family: 'VT323', monospace !important; font-size: 20px !important; }

        :root { --retro-orange: #cc7a00; --retro-green: #00ff41; --retro-red: #ff4b4b; }

        /* Pixel Kartlar */
        .pixel-card {
            background: #000;
            border: 3px solid var(--retro-orange);
            box-shadow: 5px 5px 0px 0px rgba(204, 122, 0, 0.3);
            padding: 15px;
            margin-bottom: 15px;
            color: var(--retro-orange);
        }

        .pixel-header {
            border-bottom: 2px solid var(--retro-orange);
            margin-bottom: 10px;
            padding-bottom: 5px;
            font-size: 28px !important;
            text-transform: uppercase;
        }

        /* Kupon Satırları */
        .match-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px dashed rgba(204, 122, 0, 0.2);
        }

        .status-win { color: var(--retro-green) !important; font-weight: bold; }
        .status-loss { color: var(--retro-red) !important; font-weight: bold; }
        
        /* Sidebar Retro */
        section[data-testid="stSidebar"] { 
            background-color: #050505 !important; 
            border-right: 2px solid var(--retro-orange); 
        }

        /* Streamlit Butonlarını Retro Yap */
        .stButton>button {
            border-radius: 0px !important;
            background-color: #000 !important;
            border: 2px solid var(--retro-orange) !important;
            color: var(--retro-orange) !important;
            transition: 0.2s;
        }
        .stButton>button:hover {
            background-color: var(--retro-orange) !important;
            color: #000 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00;'>🛡️ OG_CORE</h2>", unsafe_allow_html=True)
        page = st.radio("SİSTEM_MENÜ", ["⚡ ULTRA_FON", "⚽ FORM_LINE", "📊 DASH_DASH"])
        st.divider()
        
        if page == "⚡ ULTRA_FON":
            kasa = st.number_input("KASA_USD", value=600.0, step=0.1)
        else:
            kasa = 600.0
            
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.info(f"🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}")
        
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FONU ---
    if page == "⚡ ULTRA_FON":
        st.markdown("<h1 style='color:#cc7a00;'>⚡ ULTRA_ATAK_FON</h1>", unsafe_allow_html=True)
        
        try:
            tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
            prices = yf.download(tickers, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except:
            prices = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        # Üst Panel - 3 Kişilik Paylaşım
        pay = kasa / 3
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='pixel-card'><div class='pixel-header'>OGUZO</div><h2>${pay:,.2f}</h2></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='pixel-card'><div class='pixel-header'>FYBEY</div><h2>${pay:,.2f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='pixel-card'><div class='pixel-header'>ERO7</div><h2>${pay:,.2f}</h2></div>", unsafe_allow_html=True)

        st.divider()
        
        # Canlı Fiyatlar
        st.markdown("### >> CANLI_PİYASA_VERİSİ")
        f1, f2, f3 = st.columns(3)
        with f1: st.markdown(f"<div class='pixel-card' style='border-color:#555;'>BTC<br><b>${prices.get('BTC-USD', 0):,.1f}</b></div>", unsafe_allow_html=True)
        with f2: st.markdown(f"<div class='pixel-card' style='border-color:#555;'>ETH<br><b>${prices.get('ETH-USD', 0):,.1f}</b></div>", unsafe_allow_html=True)
        with f3: st.markdown(f"<div class='pixel-card' style='border-color:#555;'>SOL<br><b>${prices.get('SOL-USD', 0):,.1f}</b></div>", unsafe_allow_html=True)

    # --- 5. FORM LINE ---
    elif page == "⚽ FORM_LINE":
        st.markdown("<h1 style='color:#cc7a00;'>⚽ FORM_LINE_ANALİZ</h1>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔥 W2_AKTİF", "⏪ W1_ARŞİV"])
        
        with t1:
            # İstediğin FB maçı artık yeşil yandı kanka
            st.markdown("""<div class='pixel-card'>
                <div class='pixel-header'>W2_KUPON - DURUM: KAZANDI</div>
                <div class='match-row'><span>GS - Kayseri</span><span class='status-win'>G_W & 2.5+ ✅</span></div>
                <div class='match-row'><span>Liv - Newcastle</span><span class='status-win'>KG_VAR ✅</span></div>
                <div class='match-row'><span>Kocaeli - FB</span><span class='status-win'>FB_W & 1.5+ ✅</span></div>
                <hr style='border: 1px solid #cc7a00;'>
                <p>TOPLAM_ORAN: 5.40 | BÜTÇE: 100 USD</p>
            </div>""", unsafe_allow_html=True)

    # --- 6. DASH DASH ---
    elif page == "📊 DASH_DASH":
        st.markdown("<h1 style='color:#cc7a00;'>📊 DASH_DASH_ANALYTICS</h1>", unsafe_allow_html=True)
        st.markdown("<div class='pixel-card'>PROTOTİP V5.0: GRAFİK MOTORU YÜKLENİYOR...</div>", unsafe_allow_html=True)

    st.caption(">> OG_CORE_DISCIPLINE_IS_PROFIT_2026")
