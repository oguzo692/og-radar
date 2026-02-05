import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core v9.9", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. VERİ BAĞLANTISI (GOOGLE SHEETS) ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'].astype(str), df['value'].astype(str)))
        return data
    except Exception:
        return {"kasa": "600.0", "ana_para": "600.0"}

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")

# --- 3. CSS STİLLERİ (KESİN ÇÖZÜM) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}

.stApp { 
    background-color: #030303 !important;
}

section[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid rgba(204, 122, 0, 0.15);
}

/* --- BOZUK İKON YAZILARINI SİLEN ANA CSS --- */
/* Expander içindeki arrow_down/arrow_right yazılarını ve SVG'leri tamamen yok eder */
[data-testid="stSidebar"] summary svg {
    display: none !important;
}

[data-testid="stSidebar"] summary span {
    font-size: 0 !important;
    color: transparent !important;
    line-height: 0 !important;
}

/* Başlığı manuel olarak tekrar görünür ve düzgün yap */
[data-testid="stSidebar"] summary p {
    font-size: 14px !important;
    color: #d1d1d1 !important;
    visibility: visible !important;
    display: block !important;
}

/* Sidebar genelindeki ham metin sızıntılarını engelle */
[data-testid="stSidebar"] .st-emotion-cache-p5msec {
    display: none !important;
}
/* -------------------------------------------- */

div[data-testid="stWidgetLabel"] p {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 2px;
    color: #888 !important;
}

[data-testid="stSidebar"] label {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    padding: 12px 15px !important;
    border-radius: 4px;
    margin-bottom: 8px !important;
}

body, [data-testid="stAppViewContainer"], p, div, span, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
    color: #d1d1d1 !important;
}

.industrial-card { 
    background: linear-gradient(145deg, rgba(15, 15, 15, 0.9), rgba(5, 5, 5, 1)) !important;
    border: 1px solid rgba(255, 255, 255, 0.03) !important;
    border-top: 2px solid rgba(204, 122, 0, 0.4) !important;
    padding: 22px; margin-bottom: 20px; border-radius: 4px;
}

.terminal-header { 
    color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; 
    margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px;
}

.highlight { color: #cc7a00 !important; font-weight: 800; font-family: 'Orbitron'; }

.stButton button, .stLinkButton a {
    width: 100% !important;
    background: rgba(204, 122, 0, 0.1) !important;
    border: 1px solid rgba(204, 122, 0, 0.3) !important;
    color: #cc7a00 !important;
    font-family: 'Orbitron' !important;
}
</style>
"""

# --- 4. GİRİŞ VE GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; margin-top:20vh;"><div style="font-family:Orbitron; font-size:50px; font-weight:900; color:white; letter-spacing:10px;">OG CORE</div></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            pwd = st.text_input("GİRİŞ", type="password", label_visibility="collapsed")
            if st.button("SİSTEME GİR"):
                if pwd == "1":
                    st.session_state["password_correct"] = True
                    st.rerun()
        return False
    return True

# --- 5. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='text-align:center; font-family:Orbitron;'>OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MENÜ", ["⚡ ULTRA ATAK", "⚽ KUPONLAR"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- ŞİFRELİ ADMİN PANELİ ---
        with st.expander("📂 ADMİN PANELİ"):
            admin_pwd = st.text_input("PANEL ŞİFRESİ", type="password", key="adm_pwd")
            if admin_pwd == "fybey":
                st.link_button("GOOGLE SHEETS'E GİT", "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit")
            elif admin_pwd:
                st.error("HATALI")

        if st.button("ÇIKIŞ YAP"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>💎 KASA DURUMU</div><div style='font-size:30px' class='highlight'>${kasa:,.2f}</div></div>", unsafe_allow_html=True)

    elif page == "⚽ KUPONLAR":
        st.write("Kuponlar yükleniyor...")
