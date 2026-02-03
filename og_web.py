import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz
import json
import os

# --- 1. AYARLAR ---
st.set_page_config(page_title="OG Core v8.8", page_icon="🛡️", layout="wide")

# --- 2. CSS STİLLERİ ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
.main { background-color: #0d1117 !important; }
* { font-family: 'JetBrains Mono', monospace !important; }
:root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; --terminal-gray: #8b949e; }
#MainMenu, header, footer, .stDeployButton {visibility: hidden !important;}
[data-testid="stToolbar"] {visibility: hidden !important;}
.industrial-card {
    background: rgba(255, 255, 255, 0.02);
    border-left: 3px solid var(--soft-orange);
    border-radius: 4px; padding: 15px; margin-bottom: 20px;
}
.terminal-header { 
    color: var(--soft-orange); font-size: 14px; font-weight: bold; border-bottom: 1px dashed #30363d; 
    padding-bottom: 5px; margin-bottom: 10px; text-transform: uppercase;
}
.terminal-row { display: flex; justify-content: space-between; font-size: 13px; color: #e6edf3; margin-bottom: 6px; }
.highlight { color: var(--soft-orange); }
.win { color: var(--win-green); }
.loss { color: var(--loss-red); }
.loot-wrapper {
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 20px 25px 50px 25px; margin-bottom: 25px; position: relative;
}
.loot-track { background: #21262d; height: 14px; border-radius: 7px; width: 100%; position: relative; margin-top: 45px; }
.loot-fill { background: linear-gradient(90deg, #cc7a00, #ffae00); height: 100%; border-radius: 7px; }
.milestone { position: absolute; top: 50%; transform: translate(-50%, -50%); width: 120px; display: flex; flex-direction: column; align-items: center; z-index: 10; }
.milestone-icon { position: absolute; bottom: 12px; font-size: 24px; }
.milestone-label { position: absolute; top: 15px; font-size: 11px; font-weight: bold; color: #8b949e; white-space: nowrap; }
.milestone.active .milestone-label { color: #00ff41; }
.time-widget { display: block; width: 100%; padding: 0.3rem; font-size: 13px; font-weight: bold; color: #8b949e; text-align: center; background-color: #0d1117; border: 1px solid #30363d; border-radius: 0.25rem; }
</style>
"""

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False
def check_password():
    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align:center; color:#cc7a00;'>🛡️ OG_CORE AUTH</h1>", unsafe_allow_html=True)
        pwd = st.text_input("ŞİFRE", type="password")
        if st.button("SİSTEME GİR"):
            if pwd == "1": st.session_state["password_correct"] = True; st.rerun()
            else: st.error("❌ HATALI ŞİFRE")
        return False
    return True

# --- 5. SAVE GAME SİSTEMİ ---
SAVE_FILE = "og_save_data.json"
def load_game_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f: return json.load(f)
        except: pass
    return {"kasa": 600.0, "ana_para": 600.0, "yakim": 20}

def save_game_data():
    data = {"kasa": st.session_state.kasa_input, "ana_para": st.session_state.ana_input, "yakim": st.session_state.yakim_input}
    with open(SAVE_FILE, "w") as f: json.dump(data, f)
    st.toast("💾 OYUN KAYDEDİLDİ", icon="✅")

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    game_data = load_game_data()

    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        # --- SEKMELERİN OLDUĞU KRİTİK ALAN ---
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("TOPLAM KASA (USD)", value=game_data["kasa"], step=10.0, key="kasa_input")
        ana_para = st.number_input("BAŞLANGIÇ SERMAYESİ", value=game_data["ana_para"], key="ana_input")
        gunluk_yakim = st.slider("GÜNLÜK ORT. HARCAMA ($)", 0, 100, game_data["yakim"], key="yakim_input")
        if st.button("💾 AYARLARI KAYDET", type="primary", use_container_width=True): save_game_data()
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.markdown(f"<div class='time-widget'>🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

    if page == "⚡ ULTRA FON":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>💎 OG TRADE RADAR</div><div class='terminal-row'><span>💰 TOPLAM KASA</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>🚀 NET KAR/ZARAR</span><span style='color:{"#00ff41" if net_kar >=0 else "#ff4b4b"}'>{net_kar:,.2f} USD (%{kar_yuzdesi:.1f})</span></div></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("<div class='industrial-card'><div class='terminal-header'>📊 PİYASA</div>", unsafe_allow_html=True)
            for tick in ["BTC-USD", "ETH-USD", "SOL-USD"]:
                try:
                    price = yf.Ticker(tick).history(period="1d")['Close'].iloc[-1]
                    st.markdown(f"<div class='terminal-row'><span>{tick[:3]}</span><span>${price:,.2f}</span></div>", unsafe_allow_html=True)
                except: pass
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            omur = int(kasa / gunluk_yakim) if gunluk_yakim > 0 else 999
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>💀 FON ÖMRÜ</div><h2 style='text-align:center;'>{omur} GÜN</h2></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE")
        st.write("Kuponlar modülü aktif.")

    elif page == "📊 DASHDASH":
        st.title("📈 Performans Simülatörü")
        st.write("Simülatör aktif.")
