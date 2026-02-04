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

# --- 2. CSS STİLLERİ ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Orbitron:wght@400;900&display=swap');

.stApp { 
    background-color: #030303 !important;
    background-image: 
        radial-gradient(circle at 50% 50%, rgba(204, 122, 0, 0.05) 0%, transparent 60%),
        linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
    background-size: 100% 100%, 30px 30px, 30px 30px;
}

body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], p, div, span, h1, h2, h3, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
    color: #e0e0e0 !important;
}

.loot-wrapper {
    background: rgba(18, 18, 18, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 4px;
    padding: 30px 25px 60px 25px;
    margin-bottom: 30px;
    position: relative;
}

.loot-track {
    background: #111;
    height: 12px;
    border-radius: 6px;
    width: 100%;
    position: relative;
    margin-top: 40px;
    border: 1px solid #222;
}

.loot-fill { 
    background: linear-gradient(90deg, #cc7a00, #ffae00); 
    height: 100%;
    border-radius: 6px; 
    box-shadow: 0 0 15px rgba(204, 122, 0, 0.5);
}

.milestone {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 10;
}

.milestone-label {
    position: absolute;
    top: 25px;
    font-size: 10px;
    font-weight: bold;
    color: #888;
    text-align: center;
    white-space: nowrap;
}

.auth-container {
    padding: 4rem;
    background: linear-gradient(145deg, rgba(15,15,15,0.95) 0%, rgba(5,5,5,1) 100%);
    border: 1px solid rgba(204, 122, 0, 0.3);
    text-align: center;
    max-width: 650px;
    margin: 10vh auto;
    border-radius: 4px;
}

.auth-header {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 55px;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 12px;
}

.industrial-card { 
    background: rgba(18, 18, 18, 0.7) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-top: 2px solid rgba(204, 122, 0, 0.4) !important;
    padding: 25px; 
    margin-bottom: 25px;
}

.terminal-header { 
    color: #888; 
    font-size: 11px; 
    font-weight: 700; 
    letter-spacing: 3px;
    text-transform: uppercase; 
    margin-bottom: 20px;
}

.terminal-row { 
    display: flex; 
    justify-content: space-between; 
    font-size: 15px; 
    margin-bottom: 12px; 
    border-bottom: 1px solid rgba(255,255,255,0.02);
    padding-bottom: 8px;
}

.highlight { color: #cc7a00 !important; font-weight: 700; font-size: 18px; }

section[data-testid="stSidebar"] { 
    background-color: #050505 !important; 
    border-right: 1px solid rgba(204, 122, 0, 0.2); 
}

.time-widget { 
    padding: 15px; 
    font-size: 20px; 
    color: #cc7a00; 
    text-align: center; 
    background: rgba(204, 122, 0, 0.03); 
    border: 1px solid rgba(204, 122, 0, 0.1); 
}
</style>
"""

# --- 3. HTML ŞABLONLARI ---
common_matches = """
<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div>
<div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div>
<div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>gala w & 1.5 üst</span></div>
<div class='terminal-row'><span>Lıve - Man City</span><span class='highlight'>lıve gol atar</span></div>
<div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div>
<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'>
<div class='terminal-row'><span>oran: 8.79</span><span>bet: 100 USD</span></div>
"""

w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU</div>{common_matches}<span style='color:#cc7a00'>BEKLENİYOR ⏳</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU - KAZANDI</div>{common_matches}<span style='color:#00ff41'>SONUÇLANDI +879 USD ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU - KAYBETTİ</div>{common_matches}<span style='color:#ff4b4b'>SONUÇLANDI -100 USD ❌</span></div>"

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown("""
            <div class="auth-container">
                <div class="auth-header">OG_CORE</div>
                <div style="font-size: 10px; color: #cc7a00; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 40px; opacity: 0.8;">ARCHITECTING THE FUTURE OF WEALTH</div>
            </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("ERİŞİM ANAHTARI", type="password", placeholder="System key required...", label_visibility="collapsed")
        if st.button("TERMİNALİ INITIALIZE ET", use_container_width=True):
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
        st.markdown("<h2 style='color:#cc7a00; font-family:Orbitron; letter-spacing:4px; text-align:center;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("Modüller", ["⚡ Ultra Atak Fon", "⚽ Formlıne", "📊 Similasyon"])
        st.divider()
        kasa = st.number_input("KASA (USD)", value=game_data["kasa"], step=10.0, key="kasa_input", on_change=save_game_data)
        ana_para = st.number_input("ANA PARA", value=game_data["ana_para"], key="ana_input", on_change=save_game_data)
        yakim = st.slider("GÜNLÜK YAKIM ($)", 0, 100, game_data["yakim"], key="yakim_input", on_change=save_game_data)
        
        st.divider()
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.markdown(f"<div class='time-widget'>{datetime.now(tr_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
        if st.button("🔴 Çıkış", use_container_width=True): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ Ultra Atak Fon":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        
        # --- HEDEF İLERLEME SİSTEMİ ---
        targets = [
            {"val": 1000, "name": "TELEFON", "icon": "📱"}, 
            {"val": 2500, "name": "TATİL", "icon": "✈️"}, 
            {"val": 5000, "name": "ARABA", "icon": "🏎️"}
        ]
        max_target = 6500
        current_pct = min(100, (kasa / max_target) * 100)
        
        m_html = ""
        for t in targets:
            is_unlocked = kasa >= t['val']
            icon = t['icon'] if is_unlocked else "🔒"
            pos = (t['val'] / max_target) * 100
            m_html += f"<div class='milestone' style='left:{pos}%'><div style='font-size:22px;'>{icon}</div><div class='milestone-label'>{t['name']}<br>${t['val']}</div></div>"
            
        st.markdown(f"""
        <div class='loot-wrapper'>
            <div class='terminal-header'>TARGET PROGRESSION</div>
            <div class='loot-track'>
                <div class='loot-fill' style='width:{current_pct}%'></div>
                {m_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='industrial-card'>
            <div class='terminal-header'>💎 OG TRADE RADAR — V8.8</div>
            <div class='terminal-row'><span style='color:#888;'>NET KAR/ZARAR</span><span style='color:{"#00ff41" if net_kar >=0 else "#ff4b4b"}; font-size:22px; font-weight:900;'>${net_kar:,.2f} (%{kar_yuzdesi:.1f})</span></div>
            <div class='terminal-row' style='font-size:18px;'><span style='color:#888;'>TOPLAM KASA</span><span class='highlight'>${kasa:,.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)

        c_market, c_life = st.columns([2, 1])
        with c_market:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                eth = yf.Ticker("ETH-USD").history(period="1d")['Close'].iloc[-1]
                sol = yf.Ticker("SOL-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"""
                <div class='industrial-card'>
                    <div class='terminal-header'>GÜNCEL FİYATLAR</div>
                    <div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.2f}</span></div>
                    <div class='terminal-row'><span>ETHEREUM</span><span>${eth:,.2f}</span></div>
                    <div class='terminal-row'><span>SOLANA</span><span>${sol:,.2f}</span></div>
                </div>""", unsafe_allow_html=True)
            except: st.error("Market data link lost.")
            
        with c_life:
            omur = int(kasa / yakim) if yakim > 0 else 999
            st.markdown(f"<div class='industrial-card' style='text-align:center;'><div class='terminal-header'>FUND LIFESPAN</div><h1 style='color:#cc7a00; font-size:55px; margin:10px 0;'>{omur}</h1><p style='font-size:10px; color:#555; letter-spacing:2px;'>ESTIMATED DAYS REMAINING</p></div>", unsafe_allow_html=True)

        st.subheader("🎯 Pay Dağılımı")
        cols = st.columns(3)
        for col, user in zip(cols, ["oguzo", "ero7", "fybey"]):
            col.markdown(f"""<div class='industrial-card'><div class='terminal-header'>{user.upper()}</div><div class='terminal-row'><span>SHARE</span><span class='highlight'>${kasa/3:,.2f}</span></div><div class='terminal-row'><span>PROFIT</span><span>${(net_kar/3):,.2f}</span></div></div>""", unsafe_allow_html=True)

    elif page == "⚽ Formlıne":
        st.title("⚽ FORMLINE")
        t1, t2, t3 = st.tabs(["⏳ AKTİF (W3)", "✅ KAZANAN (W2)", "❌ KAYBEDEN (W1)"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 Similasyon":
        st.title("📈 Projeksiyon")
        h_oran = st.slider("Haftalık Hedef (%)", 1, 50, 5)
        sure = st.slider("Simülasyon (Gün)", 7, 120, 30)
        df = pd.DataFrame({"Gün": range(sure), "Tahmin ($)": [kasa * ((1 + h_oran/100) ** (d / 7)) for d in range(sure)]})
        st.line_chart(df.set_index("Gün"))

    st.caption("OG Core v8.8 | Fybey e aittir.")
