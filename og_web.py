import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz
import json
import os

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core v8.8", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS STİLLERİ (MATTE BLACK & SOFT ORANGE) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;700&display=swap');

/* ANA ARKA PLAN - MATTE BLACK */
.main { background-color: #0a0a0a !important; }

/* GENEL FONT */
body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], p, div, span, h1, h2, h3, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
}

/* --- 📺 ANİMASYONLU AUTH EKRANI --- */
.auth-container {
    padding: 3rem;
    background: #0a0a0a;
    border: 1px solid rgba(204, 122, 0, 0.3); /* SOLUK TURUNCU */
    border-radius: 4px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
    text-align: center;
    margin-top: 50px;
    position: relative;
    overflow: hidden;
}

/* SCANLINE ANİMASYONU (SOLUK) */
.auth-container::before {
    content: " ";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 2px;
    background: rgba(204, 122, 0, 0.1);
    box-shadow: 0 0 8px rgba(204, 122, 0, 0.2);
    animation: scanline 6s linear infinite;
    z-index: 5;
}

@keyframes scanline {
    0% { top: 0%; }
    100% { top: 100%; }
}

/* BAŞLIK TİTREME (SOFT FLICKER) */
.auth-header {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 50px;
    font-weight: bold;
    color: rgba(204, 122, 0, 0.8); /* SOLUK TURUNCU */
    letter-spacing: 12px;
    margin-bottom: 10px;
    text-shadow: 0 0 10px rgba(204, 122, 0, 0.3);
    animation: flicker 3s infinite;
}

@keyframes flicker {
    0% { opacity: 0.8; }
    50% { opacity: 0.9; }
    100% { opacity: 0.8; }
}

.auth-status {
    font-size: 10px;
    color: #444;
    letter-spacing: 4px;
    margin-bottom: 40px;
    text-transform: uppercase;
}

/* INPUT VE BUTONLAR */
[data-testid="stHeader"] {display:none;}
.stTextInput label {display:none !important;} /* ACCESS KEY YAZISINI KALDIRIR */

.stTextInput > div > div > input {
    background-color: #111 !important;
    border: 1px solid #222 !important;
    color: #00ff41 !important;
    text-align: center;
    font-size: 18px !important;
    border-radius: 2px !important;
}

div.stButton > button {
    background-color: transparent !important;
    color: #888 !important;
    border: 1px solid #333 !important;
    border-radius: 2px !important;
    width: 100% !important;
    font-weight: bold !important;
    letter-spacing: 8px !important;
    height: 45px;
    transition: 0.5s;
    margin-top: 20px;
}

div.stButton > button:hover {
    border-color: rgba(204, 122, 0, 0.5) !important;
    color: #cc7a00 !important;
    box-shadow: 0 0 15px rgba(204, 122, 0, 0.1);
}

/* SIDEBAR & CARDS */
.industrial-card { 
    background: #111; 
    border-left: 2px solid rgba(204, 122, 0, 0.4); 
    padding: 15px; 
    margin-bottom: 20px;
}

.terminal-header { color: rgba(204, 122, 0, 0.7); font-size: 13px; font-weight: bold; border-bottom: 1px solid #222; padding-bottom: 5px; margin-bottom: 10px; text-transform: uppercase; }
.terminal-row { display: flex; justify-content: space-between; font-size: 13px; color: #888; margin-bottom: 6px; }
.highlight { color: #cc7a00; }

section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #111; }
</style>
"""

# --- 3. HTML KUPONLAR ---
w3_coupon_html = """<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU</div><div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>gala w & 1.5 üst</span></div><hr style='border: 0.1px solid #222; margin: 10px 0;'><div class='terminal-row'><span>oran: 8.79</span><span style='color:#cc7a00'>BEKLENİYOR ⏳</span></div></div>"""
w2_coupon_html = """<div class='industrial-card' style='border-left-color: #00ff41;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU - KAZANDI</div><div class='terminal-row'><span>Gala - Kayserispor</span><span style='color:#00ff41'>KAZANDI ✅</span></div><hr style='border: 0.1px solid #222; margin: 10px 0;'><div class='terminal-row'><span>oran: 5.40</span><span style='color:#00ff41'>+540 USD</span></div></div>"""
w1_coupon_html = """<div class='industrial-card' style='border-left-color: #ff4b4b;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU - KAYBETTİ</div><div class='terminal-row'><span>Karagümrük - Gala</span><span style='color:#ff4b4b'>KAYIP ❌</span></div><hr style='border: 0.1px solid #222; margin: 10px 0;'><div class='terminal-row'><span>oran: 7.09</span><span style='color:#ff4b4b'>-100 USD</span></div></div>"""

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        _, col_mid, _ = st.columns([1, 1.5, 1])
        with col_mid:
            st.markdown("""
                <div class="auth-container">
                    <div class="auth-header">OG_CORE</div>
                    <div class="auth-status">SYSTEM STATUS: ENCRYPTED // SECURITY: ALPHA-V8</div>
                </div>
            """, unsafe_allow_html=True)
            
            # ACCESS KEY yazısı CSS ile kaldırıldı, sadece input görünüyor
            pwd = st.text_input("", type="password", placeholder="PASSWORD")
            if st.button("GİRİŞ"):
                if pwd == "1":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
        return False
    return True

# --- 5. VERİ YÖNETİMİ ---
SAVE_FILE = "og_save_data.json"
def load_game_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f: return json.load(f)
        except: pass
    return {"kasa": 600.0, "ana_para": 500.0, "yakim": 20}

def save_game_data():
    data = {"kasa": st.session_state.kasa_input, "ana_para": st.session_state.ana_input, "yakim": st.session_state.yakim_input}
    with open(SAVE_FILE, "w") as f: json.dump(data, f)
    st.toast("💾 DATABASE SYNCED", icon="✅")

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    game_data = load_game_data()

    with st.sidebar:
        st.markdown("<h2 style='color:rgba(204,122,0,0.6); font-family:Orbitron;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("KASA (USD)", value=game_data["kasa"], step=10.0, key="kasa_input", on_change=save_game_data)
        ana_para = st.number_input("ANA PARA", value=game_data["ana_para"], key="ana_input", on_change=save_game_data)
        yakim = st.slider("GÜNLÜK YAKIM ($)", 0, 100, game_data["yakim"], key="yakim_input", on_change=save_game_data)
        
        if st.button("🔴 ÇIKIŞ"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA FON":
        net_kar = kasa - ana_para
        st.markdown(f"""
        <div class='industrial-card'>
            <div class='terminal-header'>💎 OG TRADE RADAR</div>
            <div class='terminal-row'><span>TOTAL FUND</span><span class='highlight'>${kasa:,.2f}</span></div>
            <div class='terminal-row'><span>PROFIT</span><span style='color:{"#00ff41" if net_kar >=0 else "#ff4b4b"}'>${net_kar:,.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)

        c_market, c_life = st.columns(2)
        with c_market:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card'><div class='terminal-header'>MARKET</div><div class='terminal-row'><span>BTC</span><span>${btc:,.2f}</span></div></div>", unsafe_allow_html=True)
            except: st.error("Market link error.")
        with c_life:
            omur = int(kasa / yakim) if yakim > 0 else 999
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>LIFE</div><h2 style='text-align:center; color:#888;'>{omur} GÜN</h2></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE")
        t1, t2, t3 = st.tabs(["⏳ W3", "✅ W2", "❌ W1"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 DASHDASH":
        st.title("📈 PROJECTION")
        h_oran = st.slider("Weekly %", 1, 50, 5)
        df = pd.DataFrame({"Tahmin": [kasa * ((1 + h_oran/100) ** (d / 7)) for d in range(30)]})
        st.line_chart(df)

    st.caption("OG Core v8.8 | Encrypted System")
