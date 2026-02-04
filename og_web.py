import streamlit as st
import yfinance as yf
from datetime import datetime
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

# --- 2. GELİŞMİŞ CSS (CYBER-PUNK & INDUSTRIAL) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;700&display=swap');

/* ANA ARKA PLAN */
.main { background: radial-gradient(circle, #0f0f0f 0%, #050505 100%) !important; }

/* GENEL FONT */
body, [data-testid="stAppViewContainer"], p, div, span, h1, h2, h3, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
}

/* --- 📺 RETRO-FUTURE AUTH EKRANI --- */
.auth-container {
    padding: 3rem;
    background: rgba(20, 20, 20, 0.8);
    border: 1px solid #cc7a00;
    border-radius: 4px;
    box-shadow: 0 0 20px rgba(204, 122, 0, 0.15);
    text-align: center;
    margin-top: 50px;
    position: relative;
    overflow: hidden;
}

.auth-container::before {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #cc7a00, transparent);
    animation: scan 3s linear infinite;
}

@keyframes scan {
    0% { top: -10%; }
    100% { top: 110%; }
}

.auth-header {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 45px;
    font-weight: bold;
    color: #cc7a00;
    letter-spacing: 10px;
    margin-bottom: 10px;
    text-shadow: 0 0 10px rgba(204, 122, 0, 0.5);
}

.auth-status {
    font-size: 10px;
    color: #8b949e;
    letter-spacing: 4px;
    margin-bottom: 30px;
    text-transform: uppercase;
}

/* INPUT VE BUTONLAR */
.stTextInput > div > div > input {
    background-color: #000 !important;
    border: 1px solid #30363d !important;
    color: #00ff41 !important;
    text-align: center;
    font-size: 20px !important;
}

div.stButton > button {
    background: transparent !important;
    color: #cc7a00 !important;
    border: 1px solid #cc7a00 !important;
    border-radius: 0px !important;
    width: 100% !important;
    font-weight: bold !important;
    letter-spacing: 5px !important;
    transition: 0.3s;
    margin-top: 15px;
}

div.stButton > button:hover {
    background: #cc7a00 !important;
    color: #000 !important;
    box-shadow: 0 0 15px #cc7a00;
}

/* KARTLAR VE TABLOLAR */
.industrial-card { 
    background: rgba(255, 255, 255, 0.02); 
    border-left: 3px solid #cc7a00; 
    padding: 15px; 
    margin-bottom: 20px; 
}
.terminal-header { color: #cc7a00; font-size: 13px; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 5px; margin-bottom: 10px; }
.terminal-row { display: flex; justify-content: space-between; font-size: 13px; color: #e6edf3; margin-bottom: 4px; }
.highlight { color: #cc7a00; font-weight: bold; }

/* LOOT BAR */
.loot-track { background: #21262d; height: 12px; border-radius: 6px; width: 100%; position: relative; margin: 40px 0; }
.loot-fill { background: linear-gradient(90deg, #cc7a00, #ffae00); height: 100%; border-radius: 6px; box-shadow: 0 0 10px #cc7a00; }
.milestone { position: absolute; top: -25px; transform: translateX(-50%); font-size: 10px; color: #8b949e; text-align: center; }

</style>
"""

# --- 3. HTML KUPON ŞABLONLARI ---
def get_coupon_html(title, matches, footer_info, border_color="#cc7a00"):
    rows = "".join([f"<div class='terminal-row'><span>{m[0]}</span><span class='highlight'>{m[1]}</span></div>" for m in matches])
    return f"""
    <div class='industrial-card' style='border-left-color: {border_color};'>
        <div class='terminal-header'>{title}</div>
        {rows}
        <hr style='border: 0.5px solid #30363d; margin: 10px 0;'>
        <div class='terminal-row' style='opacity: 0.7;'>{footer_info}</div>
    </div>
    """

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        _, col_mid, _ = st.columns([1, 2, 1])
        with col_mid:
            st.markdown("""
                <div class="auth-container">
                    <div class="auth-header">OG_CORE</div>
                    <div class="auth-status">SECURITY LEVEL: ALPHA-V8</div>
                </div>
            """, unsafe_allow_html=True)
            
            pwd = st.text_input("ACCESS KEY", type="password", placeholder="PASSWORD")
            if st.button("INITIALIZE"):
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
    st.toast("SYSTEM UPDATED", icon="💾")

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    game_data = load_game_data()

    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00; font-family:Orbitron;'>🛡️ OG_CORE</h2>", unsafe_allow_html=True)
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("AKTİF KASA ($)", value=game_data["kasa"], step=10.0, key="kasa_input", on_change=save_game_data)
        ana_para = st.number_input("ANA SERMAYE", value=game_data["ana_para"], key="ana_input", on_change=save_game_data)
        yakim = st.slider("GÜNLÜK YAKIM", 0, 100, game_data["yakim"], key="yakim_input", on_change=save_game_data)
        
        st.divider()
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.markdown(f"<div style='text-align:center; color:#8b949e;'>{datetime.now(tr_tz).strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)
        if st.button("🔴 TERMINATE SESSION"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA FON":
        # Hesaplamalar
        net_kar = kasa - ana_para
        kar_pct = (net_kar / ana_para * 100) if ana_para > 0 else 0
        
        # Hedef Çubuğu
        targets = [1000, 2500, 5000]
        max_t = 6500
        prog = min(100, (kasa / max_t) * 100)
        
        m_html = "".join([f"<div class='milestone' style='left:{(v/max_t)*100}%'>{'✅' if kasa>=v else '🔒'}<br>${v}</div>" for v in targets])
        st.markdown(f"<div class='terminal-header'>TARGET TRACKER</div><div class='loot-track'><div class='loot-fill' style='width:{prog}%'></div>{m_html}</div>", unsafe_allow_html=True)

        # Ana Panel
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class='industrial-card'><div class='terminal-header'>FUND STATS</div>
            <div class='terminal-row'><span>TOTAL BALANCE</span><span class='highlight'>${kasa:,.2f}</span></div>
            <div class='terminal-row'><span>NET PROFIT</span><span style='color:{"#00ff41" if net_kar>=0 else "#ff4b4b"}'>${net_kar:,.2f} (%{kar_pct:.1f})</span></div>
            </div>""", unsafe_allow_html=True)
        
        with c2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"""<div class='industrial-card'><div class='terminal-header'>MARKET PULSE</div>
                <div class='terminal-row'><span>BITCOIN</span><span>${btc:,.2f}</span></div>
                <div class='terminal-row'><span>BURN RATE</span><span style='color:#ff4b4b;'>{yakim}$ / day</span></div>
                </div>""", unsafe_allow_html=True)
            except: st.warning("Market Offline")

        # Üye Payları
        st.markdown("<div class='terminal-header'>CORE MEMBERS DISTRIBUTION</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for col, user in zip(cols, ["oguzo", "ero7", "fybey"]):
            col.markdown(f"""<div class='industrial-card'><div class='terminal-header'>{user.upper()}</div>
            <div class='terminal-row'><span>SHARE</span><span class='highlight'>${kasa/3:,.2f}</span></div>
            </div>""", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE")
        t1, t2, t3 = st.tabs(["⏳ NEXT (W3)", "✅ WON (W2)", "❌ LOST (W1)"])
        with t1:
            m = [("Wolfsburg - Bvb", "BVB X2 & 1.5+"), ("Newcastle - Brentford", "NEW 1.5+"), ("Rizespor - Gala", "GS W & 1.5+")]
            st.markdown(get_coupon_html("🔥 W3 ACTIVE", m, "ODDS: 8.79 | STATUS: WAITING"), unsafe_allow_html=True)
        with t2:
            m = [("Gala - Kayseri", "GS W & 2.5+ ✅"), ("Live - Newcastle", "KG VAR ✅")]
            st.markdown(get_coupon_html("✅ W2 SETTLED", m, "RESULT: +540 USD", "#00ff41"), unsafe_allow_html=True)
        with t3:
            m = [("Fenerbahçe - Göztepe", "FB W ❌")]
            st.markdown(get_coupon_html("❌ W1 SETTLED", m, "RESULT: -100 USD", "#ff4b4b"), unsafe_allow_html=True)

    elif page == "📊 DASHDASH":
        st.title("📈 PROJECTION")
        h_oran = st.slider("Weekly Target (%)", 1, 50, 5)
        gun = st.slider("Timeline (Days)", 7, 90, 30)
        vals = [kasa * ((1 + h_oran/100) ** (d / 7)) for d in range(gun)]
        st.line_chart(pd.DataFrame({"Projected ($)": vals}))

    st.markdown("<br><hr><div style='text-align:center; opacity:0.3; font-size:10px;'>OG CORE SYSTEM v8.8 | ENCRYPTED BY FYBEY</div>", unsafe_allow_html=True)
