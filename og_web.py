import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG Core v5.0", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align:center; color:#cc7a00; font-family:monospace;'>🔐 OG_CORE_v5.0</h1>", unsafe_allow_html=True)
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
    # --- 2. OKUNAKLI INDUSTRIAL RETRO CSS ---
    st.markdown("""
        <style>
        /* Okunaklı Mono Fontlar */
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

        .main { background-color: #0d1117 !important; }
        
        /* Fontu jilet gibi yapıyoruz */
        * { font-family: 'JetBrains Mono', monospace !important; }

        :root { 
            --retro-orange: #cc7a00; 
            --retro-green: #00ff41; 
            --retro-red: #ff4b4b; 
            --card-bg: rgba(255, 255, 255, 0.03);
        }

        /* Endüstriyel Kartlar */
        .industrial-card {
            background: var(--card-bg);
            border: 1px solid var(--retro-orange);
            border-left: 5px solid var(--retro-orange); /* Sol tarafı kalın şeritli */
            padding: 15px;
            margin-bottom: 15px;
            color: #e6edf3;
        }

        .card-label {
            color: #8b949e;
            font-size: 12px !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .card-value {
            color: var(--retro-orange);
            font-size: 24px !important;
            font-weight: bold;
        }

        /* Kupon Satırları */
        .match-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .status-win { color: var(--retro-green) !important; font-weight: bold; }
        
        /* Sidebar */
        section[data-testid="stSidebar"] { 
            background-color: #050505 !important; 
            border-right: 1px solid var(--retro-orange); 
        }

        /* Butonlar */
        .stButton>button {
            border-radius: 4px !important;
            background-color: transparent !important;
            border: 1px solid var(--retro-orange) !important;
            color: var(--retro-orange) !important;
            width: 100%;
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
        page = st.radio("MENÜ", ["⚡ ULTRA_FON", "⚽ FORM_LINE", "📊 DASH_DASH"])
        st.divider()
        
        if page == "⚡ ULTRA_FON":
            # Fon bakiyesi oguzo, fybey ve ero7 arasında paylaştırılıyor
            kasa = st.number_input("TOPLAM KASA (USD)", value=600.0, step=0.1)
        else:
            kasa = 600.0
            
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.info(f"🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}")
        
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FONU ---
    if page == "⚡ ULTRA_FON":
        st.markdown("<h2 style='color:#cc7a00;'>⚡ ULTRA_ATAK_FON</h2>", unsafe_allow_html=True)
        
        try:
            tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
            prices = yf.download(tickers, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except:
            prices = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        # Üst Panel - 3 Kişilik Paylaşım (oguzo, fybey ve ero7)
        pay = kasa / 3
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='industrial-card'><div class='card-label'>oguzo</div><div class='card-value'>${pay:,.2f}</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='industrial-card'><div class='card-label'>fybey</div><div class='card-value'>${pay:,.2f}</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='industrial-card'><div class='card-label'>ero7</div><div class='card-value'>${pay:,.2f}</div></div>", unsafe_allow_html=True)

        st.divider()
        
        # Canlı Fiyatlar
        st.markdown("### >> CANLI_PİYASA_VERİSİ")
        f1, f2, f3 = st.columns(3)
        with f1: st.markdown(f"<div class='industrial-card'><div class='card-label'>BTC-USD</div><div class='card-value'>${prices.get('BTC-USD', 0):,.1f}</div></div>", unsafe_allow_html=True)
        with f2: st.markdown(f"<div class='industrial-card'><div class='card-label'>ETH-USD</div><div class='card-value'>${prices.get('ETH-USD', 0):,.1f}</div></div>", unsafe_allow_html=True)
        with f3: st.markdown(f"<div class='industrial-card'><div class='card-label'>SOL-USD</div><div class='card-value'>${prices.get('SOL-USD', 0):,.1f}</div></div>", unsafe_allow_html=True)

    # --- 5. FORM LINE ---
    elif page == "⚽ FORM_LINE":
        st.markdown("<h2 style='color:#cc7a00;'>⚽ FORM_LINE_ANALİZ</h2>", unsafe_allow_html=True)
        # W2 (1-2 Şubat) kuponu Kazandı olarak güncellendi
        st.markdown("""<div class='industrial-card' style='border-left-color: #00ff41;'>
            <div class='card-label'>W2_KUPON - DURUM: KAZANDI</div><br>
            <div class='match-row'><span>GS - Kayseri</span><span class='status-win'>G_W & 2.5+ ✅</span></div>
            <div class='match-row'><span>Liv - Newcastle</span><span class='status-win'>KG_VAR ✅</span></div>
            <div class='match-row'><span>Kocaeli - FB</span><span class='status-win'>FB_W & 1.5+ ✅</span></div>
            <hr style='border: 1px solid rgba(255,255,255,0.05);'>
            <p>TOPLAM_ORAN: 5.40 | BÜTÇE: 100 USD</p>
        </div>""", unsafe_allow_html=True)

    # --- 6. DASH DASH ---
    elif page == "📊 DASH_DASH":
        st.markdown("<h2 style='color:#cc7a00;'>📊 DASH_DASH</h2>", unsafe_allow_html=True)
        st.markdown("<div class='industrial-card'>Analitik veri akışı beklemede...</div>", unsafe_allow_html=True)

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
