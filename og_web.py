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

# --- 2. VERİ BAĞLANTISI (GOOGLE SHEETS) ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'].astype(str), df['value'].astype(str)))
        return data
    except Exception:
        return {"kasa": "600.0", "ana_para": "600.0"}

# --- RÜTBE FONKSİYONU ---
def rutbe_getir(puan_str):
    try:
        p = int(float(puan_str))
    except:
        p = 0
    if p <= 3: return "Hılez"
    elif p <= 6: return "Tecrübeli Hılez"
    elif p <= 9: return "Bu Abi Biri Mi?"
    elif p <= 11: return "Miço"
    else: return "Grand Miço"

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")

# --- KİŞİSEL KASA VERİLERİ ---
og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

# --- RÜTBE VERİLERİ ---
og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "yeni soru yakında...")
aktif_soru_2 = live_vars.get("aktif_soru2", "yeni soru yakında...")

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 553))
w3_kar = float(live_vars.get("w3_sonuc", 879)) 
w4_kar = float(live_vars.get("w4_sonuc", -100))
w5_kar = float(live_vars.get("w5_sonuc", -100))
w6_kar = float(live_vars.get("w6_sonuc", -100))
w7_kar = float(live_vars.get("w7_sonuc", -100))
toplam_bahis_kar = w1_kar + w2_kar + w3_kar + w4_kar + w5_kar + w6_kar + w7_kar

wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS STİLLERİ (SIDEBAR FIX) ---
common_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

/* --- Sidebar Mobil Açılma Sorunu Fix --- */
[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    z-index: 999999 !important;
    background: rgba(204, 122, 0, 0.2) !important;
    border-radius: 0 10px 10px 0 !important;
    color: #cc7a00 !important;
}

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}

/* Sidebar Genel Stil */
section[data-testid="stSidebar"] { 
    background-color: #050505 !important; 
    border-right: 1px solid rgba(204, 122, 0, 0.15); 
    padding-top: 20px;
}

/* Mobil Genişlik Ayarı */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        width: 280px !important;
    }
}
@media (min-width: 769px) {
    section[data-testid="stSidebar"] { 
        min-width: 340px !important; 
        max-width: 340px !important; 
    }
}

.stButton button, .stLinkButton a { width: 100% !important; background: rgba(204, 122, 0, 0.1) !important; border: 1px solid rgba(204, 122, 0, 0.3) !important; color: #cc7a00 !important; font-family: 'Orbitron' !important; padding: 12px !important; border-radius: 6px !important;}
body, [data-testid="stAppViewContainer"], p, div, span, button, input { font-family: 'JetBrains Mono', monospace !important; color: #d1d1d1 !important;}

.industrial-card { 
    background: rgba(15, 15, 15, 0.8) !important; 
    backdrop-filter: blur(5px); 
    border: 1px solid rgba(255, 255, 255, 0.03) !important; 
    border-top: 2px solid rgba(204, 122, 0, 0.4) !important; 
    padding: 18px; 
    margin-bottom: 20px; 
    border-radius: 4px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
    width: 100%;
}

.terminal-header { color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px;}
.highlight { color: #FFFFFF !important; font-weight: 400; font-size: 14px; font-family: 'JetBrains Mono', monospace; }
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; margin-bottom: 25px;}
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
.ticker-item { font-size: 12px; color: #cc7a00; letter-spacing: 4px; padding-right: 50%; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

.val-std { font-size: 22px !important; font-weight: 800 !important; font-family: 'Orbitron'; }
.terminal-row { display: flex; justify-content: space-between; align-items: center; font-size: 13px; margin-bottom: 12px;}
</style>
"""

login_bg_css = """
<style>
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(10, 10, 10, 0.75) !important;
    backdrop-filter: blur(30px) !important;
    padding: 40px 25px !important;
    border-radius: 18px !important;
    border: 1px solid rgba(204, 122, 0, 0.35) !important;
    margin: 50px auto !important;
    width: 90% !important;
    max-width: 360px !important;
}
input[type="password"] {
    background: rgba(0, 0, 0, 0.5) !important;
    border: 1px solid rgba(204, 122, 0, 0.6) !important;
    text-align: center !important;
    color: #cc7a00 !important;
    font-size: 26px !important;
    letter-spacing: 12px !important;
}
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w7_matches = """<div class='terminal-row'><span>BJK - GS</span><span class='highlight'>GS +1</span></div><div class='terminal-row'><span>KÖLN - BVB</span><span class='highlight'>BVB +2</span></div><div class='terminal-row'><span>NEW - MU</span><span class='highlight'>KG ✅</span></div><div class='terminal-row'><span>WOL - LIV</span><span class='highlight'>KG ✅</span></div><div class='terminal-row'><span>FB - SAM</span><span class='highlight'>FB W</span></div>"""
w3_matches = """<div class='terminal-row'><span>WOLF - BVB</span><span class='highlight'>BVB X2 ✅</span></div><div class='terminal-row'><span>RIZE - GS</span><span class='highlight'>GS W ✅</span></div>"""

w7_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>⏳ W7 KUPONU</div>{w7_matches}</div>"
w3_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W3 KUPONU</div>{w3_matches}</div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        pwd = st.text_input("PIN", type="password", placeholder="----", label_visibility="collapsed")
        if pwd == "1608":
            st.session_state["password_correct"] = True
            st.rerun()
        elif pwd: st.error("ACCESS DENIED")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    st.markdown("<style>.stApp { background: #030303 !important; }</style>", unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color:white; font-family:Orbitron; text-align:center;'>OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MENÜ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip", "💠 FTMO"])
        st.divider()
        if st.button("ÇIKIŞ YAP"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 Kasa Durumu</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='industrial-card'>Oguzo: ${og_kasa:,.0f}</div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='industrial-card'>Ero7: ${er_kasa:,.0f}</div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='industrial-card'>Fybey: ${fy_kasa:,.0f}</div>", unsafe_allow_html=True)

        net_kar = kasa - ana_para
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>TOPLAM KASA</div><h1 style='color:#00ff41; font-family:Orbitron;'>${kasa:,.2f}</h1><small>Net K/Z: ${net_kar:,.2f}</small></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        t1, t2 = st.tabs(["W7 (Aktif)", "Arşiv"])
        with t1: st.markdown(w7_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w3_coupon_html, unsafe_allow_html=True)
    
    # Diğer sayfalar (Challange, Portföy vb.) aynı mantıkla çalışır
    else:
        st.info(f"{page} sayfası aktif.")
