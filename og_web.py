import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz
import numpy as np

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. VERİ BAĞLANTISI ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'].astype(str), df['value'].astype(str)))
        return data
    except Exception:
        return {"kasa": "600.0", "ana_para": "600.0"}

def rutbe_getir(puan_str):
    try: p = int(float(puan_str))
    except: p = 0
    if p <= 3: return "Hılez"
    elif p <= 6: return "Tecrübeli Hılez"
    elif p <= 9: return "Bu Abi Biri Mi?"
    elif p <= 11: return "Miço"
    else: return "Grand Miço"

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")
og_kasa, er_kasa, fy_kasa = float(live_vars.get("oguzo_kasa", kasa/3)), float(live_vars.get("ero7_kasa", kasa/3)), float(live_vars.get("fybey_kasa", kasa/3))
og_p, er_p, fy_p = live_vars.get("oguzo_puan", "0"), live_vars.get("ero7_puan", "0"), live_vars.get("fybey_puan", "0")
aktif_soru_1, aktif_soru_2 = live_vars.get("aktif_soru", "yeni soru..."), live_vars.get("aktif_soru2", "yeni soru...")
toplam_bahis_kar = sum([float(live_vars.get(f"w{i}_sonuc", 0)) for i in range(1, 7)])
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS (GERÇEK RESPONSIVE MOD) ---
common_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
body, [data-testid="stAppViewContainer"] { background: #030303 !important; font-family: 'JetBrains Mono', monospace !important; color: #d1d1d1 !important;}

/* Flex Grid Sistemi (Mobilde Alt Alta, Masaüstünde Yan Yana) */
.flex-container {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    width: 100%;
    margin-bottom: 20px;
}
.flex-item {
    flex: 1;
    min-width: 300px; /* Mobilde 300px altına düşünce alt alta atar */
}
@media (max-width: 600px) {
    .flex-item { flex: 1 1 100%; }
}

.industrial-card { 
    background: rgba(15, 15, 15, 0.8); 
    border: 1px solid rgba(255, 255, 255, 0.03); 
    border-top: 2px solid #cc7a00; 
    padding: 20px; 
    border-radius: 4px;
    height: 100%;
}
.terminal-header { color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; border-left: 3px solid #cc7a00; padding-left: 10px;}
.highlight { color: #FFFFFF; font-size: 18px; font-weight: 800; font-family: 'Orbitron'; }
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.05); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; }
.ticker { display: flex; white-space: nowrap; animation: ticker 25s linear infinite; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

/* Sidebar Mobil Genişlik */
[data-testid="stSidebar"] { min-width: 250px !important; }
</style>
"""

login_bg_css = """
<style>
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(10, 10, 10, 0.9) !important;
    padding: 30px !important;
    border-radius: 15px !important;
    border: 1px solid #cc7a00 !important;
    position: fixed !important; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 90% !important; max-width: 350px !important; z-index: 9999;
}
</style>
"""

# --- GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        pwd = st.text_input("PIN", type="password", placeholder="----", label_visibility="collapsed")
        if pwd == "1608":
            st.session_state["password_correct"] = True
            st.rerun()
        return False
    return True

if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span style="color:#cc7a00; letter-spacing:4px; padding-right:50px;">{duyuru_metni}</span><span style="color:#cc7a00; letter-spacing:4px;">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='text-align:center; font-family:Orbitron; color:#cc7a00;'>OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MENÜ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip"])
        if st.button("ÇIKIŞ YAP"):
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        # Kişisel Kasa - Manuel Flex Yapısı
        st.markdown(f"""
        <div class="flex-container">
            <div class="flex-item"><div class="industrial-card"><div class="terminal-header">Oguzo</div><div class="highlight">${og_kasa:,.2f}</div></div></div>
            <div class="flex-item"><div class="industrial-card"><div class="terminal-header">Ero7</div><div class="highlight">${er_kasa:,.2f}</div></div></div>
            <div class="flex-item"><div class="industrial-card"><div class="terminal-header">Fybey</div><div class="highlight">${fy_kasa:,.2f}</div></div></div>
        </div>
        """, unsafe_allow_html=True)

        net_kar = kasa - ana_para
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>ANA KASA DURUMU</div><div style='display:flex; justify-content:space-between;'><span style='font-size:24px; color:#fff;'>${kasa:,.2f}</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'}; font-size:20px;'>K/Z: ${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"<div class='industrial-card' style='text-align:center;'><div class='terminal-header'>WIN RATE</div><div style='font-size:40px; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>LOGLAR</div><div style='font-size:11px; color:#888; overflow-y:auto; max-height:100px;'>{son_islemler_raw}</div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card' style='margin-bottom:20px;'><div class='terminal-header'>TOPLAM KAR</div><div style='font-size:32px; color:#00ff41; font-family:Orbitron;'>${toplam_bahis_kar:,.2f}</div></div>", unsafe_allow_html=True)
        st.info("Kupon detayları için sekmeleri kullanın.")
        # Kuponlar buraya gelecek (Tabs yapısı zaten mobilde fena değil)

    elif page == "📊 Portföy Takip":
        st.write("### 🏛️ Portföy Merkezi")
        # Portföy kodlarını buraya ekleyebilirsin, flex-item mantığıyla sarmalaman mobilde kurtaracaktır.

    st.markdown(f"<div style='text-align:center; color:#333; font-size:10px; margin-top:30px;'>OG CORE // 2026</div>", unsafe_allow_html=True)
