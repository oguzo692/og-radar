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
        st.markdown("<h1 style='text-align:center; color:#cc7a00; font-family:sans-serif;'>🛡️ OG_CORE AUTH</h1>", unsafe_allow_html=True)
        pwd = st.text_input("ŞİFRE", type="password")
        if st.button("SİSTEME GİR"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ ERİŞİM REDDEDİLDİ")
        return False
    return True

if check_password():
    # --- 2. PREMIUM CYBER-INDUSTRIAL CSS ---
    st.markdown("""
        <style>
        /* Okunaklı Modern Sans-Serif Font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        .main { background-color: #0d1117 !important; }
        
        * { font-family: 'Inter', sans-serif !important; }

        :root { 
            --neon-orange: #ff9f1a; 
            --deep-orange: #cc7a00;
            --neon-green: #00ff41; 
            --glass-bg: rgba(255, 255, 255, 0.05);
        }

        /* Modern Glass Card */
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 159, 26, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            transition: 0.3s;
        }
        .glass-card:hover {
            border-color: var(--neon-orange);
            box-shadow: 0 0 15px rgba(255, 159, 26, 0.1);
        }

        .label {
            color: #8b949e;
            font-size: 11px !important;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
        }

        .value {
            color: #ffffff;
            font-size: 26px !important;
            font-weight: 600;
        }

        .orange-text { color: var(--neon-orange) !important; }

        /* Sidebar */
        section[data-testid="stSidebar"] { 
            background-color: #050505 !important; 
            border-right: 1px solid rgba(255, 159, 26, 0.3); 
        }

        /* Custom Table */
        .stTable { 
            background: var(--glass-bg); 
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.markdown("<h2 style='color:#ff9f1a; font-weight:800;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MENÜ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        
        if page == "⚡ ULTRA ATAK":
            kasa = st.number_input("TOPLAM KASA", value=600.0, step=0.1)
        else:
            kasa = 600.0
            
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.info(f"🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}")
        
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FONU ---
    if page == "⚡ ULTRA ATAK":
        st.markdown("<h1 style='color:#ff9f1a; font-weight:800;'>⚡ ULTRA ATAK</h1>", unsafe_allow_html=True)
        
        try:
            tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
            prices = yf.download(tickers, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except:
            prices = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        # Üst Panel - Paylaşım (oguzo, fybey, ero7)
        pay = kasa / 3
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='glass-card'><div class='label'>OGUZO</div><div class='value'>${pay:,.2f}</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='glass-card'><div class='label'>FYBEY</div><div class='value'>${pay:,.2f}</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='glass-card'><div class='label'>ERO7</div><div class='value'>${pay:,.2f}</div></div>", unsafe_allow_html=True)

        st.divider()
        
        # Canlı Fiyatlar
        st.markdown("<h3 style='color:#8b949e; font-size:16px;'>>> PİYASA TAKİBİ</h3>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1: st.markdown(f"<div class='glass-card'><div class='label'>BTC-USD</div><div class='value orange-text'>${prices.get('BTC-USD', 0):,.1f}</div></div>", unsafe_allow_html=True)
        with f2: st.markdown(f"<div class='glass-card'><div class='label'>ETH-USD</div><div class='value orange-text'>${prices.get('ETH-USD', 0):,.1f}</div></div>", unsafe_allow_html=True)
        with f3: st.markdown(f"<div class='glass-card'><div class='label'>SOL-USD</div><div class='value orange-text'>${prices.get('SOL-USD', 0):,.1f}</div></div>", unsafe_allow_html=True)

    # --- 5. FORM LINE ---
    elif page == "⚽ FORMLINE":
        st.markdown("<h1 style='color:#ff9f1a; font-weight:800;'>⚽ FORMLINE</h1>", unsafe_allow_html=True)
        st.markdown(f"""<div class='glass-card' style='border-left: 4px solid #00ff41;'>
            <div class='label'>W2 KUPONU - KAZANDI</div>
            <div style='display:flex; justify-content:space-between; margin:10px 0;'><span>GS - Kayseri</span><span style='color:#00ff41;'>✅</span></div>
            <div style='display:flex; justify-content:space-between; margin:10px 0;'><span>Liv - Newcastle</span><span style='color:#00ff41;'>✅</span></div>
            <div style='display:flex; justify-content:space-between; margin:10px 0;'><span>Kocaeli - FB</span><span style='color:#00ff41;'>✅</span></div>
            <hr style='border-color:rgba(255,255,255,0.05)'>
            <div class='label'>ORAN: 5.40 | BÜTÇE: 100 USD</div>
        </div>""", unsafe_allow_html=True)

    # --- 6. DASH DASH ---
    elif page == "📊 DASHDASH":
        st.markdown("<h1 style='color:#ff9f1a; font-weight:800;'>📊 DASHDASH</h1>", unsafe_allow_html=True)
