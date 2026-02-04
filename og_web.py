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

# --- 2. CSS STİLLERİ (PURE BLACK & SİBER TASARIM) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;900&display=swap');

/* TAM SİYAH ARKA PLAN */
.main { 
    background-color: #000000 !important;
}

/* GENEL FONT */
body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], p, div, span, h1, h2, h3, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
}

/* --- 📺 GELİŞMİŞ SİBER AUTH EKRANI --- */
.auth-container {
    padding: 5rem 2rem;
    background: #000000;
    border: 1px solid rgba(204, 122, 0, 0.4);
    border-radius: 4px;
    box-shadow: 0 0 80px rgba(0, 0, 0, 1), inset 0 0 40px rgba(204, 122, 0, 0.03);
    text-align: center;
    margin-top: 30px;
    position: relative;
    overflow: hidden;
}

/* ARKA PLAN HAREKETLİ IZGARA (GRID) */
.auth-container::before {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 200%; height: 200%;
    background-image: linear-gradient(rgba(204, 122, 0, 0.03) 1px, transparent 1px), 
                      linear-gradient(90deg, rgba(204, 122, 0, 0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    animation: grid-move 20s linear infinite;
    z-index: -1;
    opacity: 0.4;
}

@keyframes grid-move {
    0% { transform: translate(0, 0); }
    100% { transform: translate(-40px, -40px); }
}

/* SCANLINE (TARAMA ÇİZGİSİ) */
.scanline {
    position: absolute;
    width: 100%; height: 4px;
    background: rgba(204, 122, 0, 0.15);
    box-shadow: 0 0 25px #cc7a00;
    animation: scanline-move 4s linear infinite;
    z-index: 10;
    pointer-events: none;
}

@keyframes scanline-move {
    0% { top: -10%; }
    100% { top: 110%; }
}

/* OG_CORE BAŞLIK (DETAYLI GLITCH VE FLOAT) */
.auth-header {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 70px;
    font-weight: 900;
    color: #ff8c00;
    letter-spacing: 20px;
    margin-bottom: 5px;
    position: relative;
    display: inline-block;
    text-shadow: 3px 3px 0px #331a00, 0 0 15px rgba(255, 140, 0, 0.4);
    animation: float 3.5s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.auth-status {
    font-size: 10px;
    color: #8b949e;
    letter-spacing: 8px;
    margin-bottom: 50px;
    text-transform: uppercase;
    border-top: 1px solid rgba(204, 122, 0, 0.2);
    display: inline-block;
    padding-top: 10px;
}

/* INPUT VE BUTONLAR */
.stTextInput > div > div > input {
    background-color: #000000 !important;
    border: 1px solid #222 !important;
    border-left: 5px solid #cc7a00 !important;
    color: #ff8c00 !important;
    text-align: center;
    font-size: 20px !important;
    border-radius: 0px !important;
}

div.stButton > button {
    background-color: transparent !important;
    color: #ff8c00 !important;
    border: 1px solid rgba(255, 140, 0, 0.5) !important;
    border-radius: 0px !important;
    width: 100% !important;
    font-weight: bold !important;
    letter-spacing: 10px !important;
    height: 60px;
    transition: 0.4s;
    margin-top: 20px;
}

div.stButton > button:hover {
    background-color: #ff8c00 !important;
    color: #000000 !important;
    box-shadow: 0 0 50px rgba(255, 140, 0, 0.7) !important;
}

/* --- 📊 SIDEBAR & CARDS (ORİJİNAL VERİ TASARIMI) --- */
section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #222; }

.industrial-card { 
    background: rgba(255, 255, 255, 0.02); 
    border-left: 3px solid #cc7a00; 
    padding: 15px; 
    margin-bottom: 20px;
    transition: transform 0.2s;
}
.industrial-card:hover { transform: scale(1.01); }

.terminal-header { color: #cc7a00; font-size: 14px; font-weight: bold; border-bottom: 1px dashed #30363d; padding-bottom: 5px; margin-bottom: 10px; text-transform: uppercase; }
.terminal-row { display: flex; justify-content: space-between; font-size: 13px; color: #e6edf3; margin-bottom: 6px; }
.highlight { color: #cc7a00; font-weight: bold; }
.win { color: #00ff41; font-weight: bold; }
.loss { color: #ff4b4b; font-weight: bold; }

/* LOOT BAR (GERİ GELDİ) */
.loot-wrapper { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px 25px 50px 25px; margin-bottom: 25px; position: relative; }
.loot-track { background: #21262d; height: 14px; border-radius: 7px; width: 100%; position: relative; margin-top: 45px; }
.loot-fill { 
    background: linear-gradient(90deg, #cc7a00, #ffae00); 
    height: 100%; border-radius: 7px; 
    box-shadow: 0 0 15px rgba(204, 122, 0, 0.5);
    transition: width 1s ease-in-out; 
}
.milestone { position: absolute; top: 50%; transform: translate(-50%, -50%); width: 120px; display: flex; flex-direction: column; align-items: center; z-index: 10; }
.milestone-label { position: absolute; top: 18px; font-size: 11px; font-weight: bold; color: #8b949e; text-align: center; }

.time-widget { display: block; width: 100%; padding: 0.5rem; font-size: 14px; font-weight: bold; color: #cc7a00; text-align: center; background-color: #0d1117; border: 1px solid #333; border-radius: 4px; }
</style>
"""

# --- 3. HTML ŞABLONLARI ---
w3_coupon_html = """<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU</div><div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Lıve - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 1px solid #30363d; margin: 10px 0;'><div class='terminal-row'><span>oran: 8.79</span><span>bet: 100 USD</span><span style='color:#cc7a00'>BEKLENİYOR ⏳</span></div></div>"""
w2_coupon_html = """<div class='industrial-card' style='border-left-color: #00ff41;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU - KAZANDI</div><div class='terminal-row'><span>Gala - Kayserispor</span><span class='win'>gala w & +2.5 üst ✅</span></div><div class='terminal-row'><span>Lıve - Newcastle</span><span class='win'>kg var ✅</span></div><div class='terminal-row'><span>Bvb - Heidenheim</span><span class='win'>bvb w & +1.5 üst ✅</span></div><div class='terminal-row'><span>Kocaelispor - Fenerbahçe</span><span class='win'>fenerbahçe w & 1.5 üst ✅</span></div><hr style='border: 1px solid #30363d; margin: 10px 0;'><div class='terminal-row'><span>oran: 5.40</span><span>bet: 100 USD</span><span class='win'>SONUÇLANDI +540 USD</span></div></div>"""
w1_coupon_html = """<div class='industrial-card' style='border-left-color: #ff4b4b;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU - KAYBETTİ</div><div class='terminal-row'><span>Karagümrük - Gala</span><span class='win'>gala w & 1.5 üst ✅</span></div><div class='terminal-row'><span>Bournemouth - Lıve</span><span class='win'>kg var ✅</span></div><div class='terminal-row'><span>Unıon Berlin - Bvb</span><span class='win'>bvb 0.5 üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span class='loss'>newcastle 1.5 üst ❌</span></div><div class='terminal-row'><span>Fenerbahçe - Göztepe</span><span class='loss'>fenerbahçe w ❌</span></div><hr style='border: 1px solid #30363d; margin: 10px 0;'><div class='terminal-row'><span>oran: 7.09</span><span>bet: 100 USD</span><span class='loss'>SONUÇLANDI -100 USD</span></div></div>"""

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
                    <div class="scanline"></div>
                    <div class="auth-header">OG_CORE</div><br>
                    <div class="auth-status">SİSTEM DURUMU: ŞİFRELENDİ // GÜVENLİK: ALPHA-V8</div>
                </div>
            """, unsafe_allow_html=True)
            pwd = st.text_input("GİRİŞ ANAHTARI", type="password", placeholder="ŞİFREYİ GİRİNİZ")
            if st.button("SİSTEMİ BAŞLAT"):
                if pwd == "1":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("ERİŞİM REDDEDİLDİ")
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
        st.markdown("<h2 style='color:#cc7a00; font-family:Orbitron;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("KASA (USD)", value=game_data["kasa"], step=10.0, key="kasa_input", on_change=save_game_data)
        ana_para = st.number_input("ANA PARA", value=game_data["ana_para"], key="ana_input", on_change=save_game_data)
        yakim = st.slider("GÜNLÜK YAKIM ($)", 0, 100, game_data["yakim"], key="yakim_input", on_change=save_game_data)
        
        st.divider()
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.markdown(f"<div class='time-widget'>{datetime.now(tr_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
        if st.button("🔴 OTURUMU KAPAT", use_container_width=True): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA FON":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        
        # HEDEF YOLCULUĞU (ANİMASYONLU BAR GERİ GELDİ)
        targets = [{"val": 1000, "name": "TELEFON"}, {"val": 2500, "name": "TATİL"}, {"val": 5000, "name": "ARABA"}]
        max_target = 6500
        current_pct = min(100, (kasa / max_target) * 100)
        
        m_html = "".join([f"<div class='milestone' style='left:{(t['val']/max_target)*100}%'><div style='font-size:20px;'>{'✅' if kasa>=t['val'] else '🔒'}</div><div class='milestone-label'>{t['name']}</div></div>" for t in targets])
        st.markdown(f"<div class='loot-wrapper'><div class='terminal-header'>HEDEF İLERLEMESİ</div><div class='loot-track'><div class='loot-fill' style='width:{current_pct}%'></div>{m_html}</div></div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='industrial-card'>
            <div class='terminal-header'>💎 OG TRADE RADAR — v8.8</div>
            <div class='terminal-row'><span>TOPLAM KASA</span><span class='highlight'>${kasa:,.2f}</span></div>
            <div class='terminal-row'><span>NET KAR/ZARAR</span><span style='color:{"#00ff41" if net_kar >=0 else "#ff4b4b"}'>${net_kar:,.2f} (%{kar_yuzdesi:.1f})</span></div>
        </div>
        """, unsafe_allow_html=True)

        c_market, c_life = st.columns([2, 1])
        with c_market:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card'><div class='terminal-header'>PİYASA VERİSİ</div><div class='terminal-row'><span>BITCOIN</span><span>${btc:,.2f}</span></div></div>", unsafe_allow_html=True)
            except: st.error("Market data link lost.")
            
        with c_life:
            omur = int(kasa / yakim) if yakim > 0 else 999
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>KASA ÖMRÜ</div><h2 style='text-align:center;'>{omur} GÜN</h2></div>", unsafe_allow_html=True)

        st.subheader("🎯 Pay Dağılımı")
        cols = st.columns(3)
        for col, user in zip(cols, ["oguzo", "ero7", "fybey"]):
            col.markdown(f"""<div class='industrial-card'><div class='terminal-header'>{user.upper()}</div><div class='terminal-row'><span>PAY</span><span class='highlight'>${kasa/3:,.2f}</span></div><div class='terminal-row'><span>KAR</span><span>${(net_kar/3):,.2f}</span></div></div>""", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE")
        t1, t2, t3 = st.tabs(["⏳ AKTİF (W3)", "✅ KAZANAN (W2)", "❌ KAYBEDEN (W1)"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 DASHDASH":
        st.title("📈 Projeksiyon")
        h_oran = st.slider("Haftalık Hedef (%)", 1, 50, 5)
        sure = st.slider("Simülasyon (Gün)", 7, 120, 30)
        df = pd.DataFrame({"Gün": range(sure), "Tahmin ($)": [kasa * ((1 + h_oran/100) ** (d / 7)) for d in range(sure)]})
        st.line_chart(df.set_index("Gün"))

    st.caption("OG Core v8.8 | Fybey'e aittir.")
