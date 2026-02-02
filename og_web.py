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
        st.markdown("<h1 style='text-align:center; color:#cc7a00;'>🛡️ OG_CORE AUTH</h1>", unsafe_allow_html=True)
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
    # --- 2. GÜNCEL INDUSTRIAL CSS ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
        .main { background-color: #0d1117 !important; }
        * { font-family: 'Inter', sans-serif !important; }
        :root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; }
        
        .industrial-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--soft-orange);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
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

    # --- 3. SIDEBAR ---
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

    # --- 4. ULTRA ATAK FONU ---
    if page == "⚡ ULTRA FON":
        st.title("⚡ ULTRA ATAK FONU")
        pay = kasa / 3
        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='industrial-card'><small>OGUZO</small><h3>${pay:,.2f}</h3></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='industrial-card'><small>FYBEY</small><h3>${pay:,.2f}</h3></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='industrial-card'><small>ERO7</small><h3>${pay:,.2f}</h3></div>", unsafe_allow_html=True)

    # --- 5. FORM LINE (MAÇLAR VE BAHİSLER BURADA) ---
    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE ANALİZLERİ")
        t1, t2, t3 = st.tabs(["🔥 W3 (8-9 Şub)", "✅ W2 (1-2 Şub)", "⏪ W1 (Geçmiş)"])

        with t1:
            st.markdown("""<div class='industrial-card'>
                <h3>🔥 W3 KUPONU (YÜKLENİYOR)</h3>
                <p style='color:#8b949e;'>Maç analizleri Cuma günü sisteme girilecektir.</p>
                <div class='match-row'><span>-- Bekleniyor --</span><span class='status-wait'>TBD</span></div>
                <div class='match-row'><span>-- Bekleniyor --</span><span class='status-wait'>TBD</span></div>
            </div>""", unsafe_allow_html=True)

        with t2:
            st.markdown("""<div class='industrial-card' style='border-color: #00ff41;'>
                <h3 style='color:#00ff41 !important;'>✅ W2 KUPONU - KAZANDI</h3>
                <div class='match-row'><span>Galatasaray - Kayserispor</span><span class='status-win'>MS 1 & 2.5 ÜST ✅</span></div>
                <div class='match-row'><span>Liverpool - Newcastle</span><span class='status-win'>KG VAR ✅</span></div>
                <div class='match-row'><span>B. Dortmund - Heidenheim</span><span class='status-win'>İY 0.5 ÜST ✅</span></div>
                <div class='match-row'><span>Kocaelispor - Fenerbahçe</span><span class='status-win'>MS 2 & 1.5 ÜST ✅</span></div>
                <hr style='border: 1px solid rgba
