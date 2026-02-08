import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import base64

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core Terminal", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. GÖRSELİ ARKAPLAN YAPMA SİSTEMİ ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# Resim dosyan kodla aynı klasörde olmalı
img_base64 = get_base64_of_bin_file("arkaplan.png")

# --- 3. CSS STİLLERİ (FULL REVİZE) ---
custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

/* Arka Plan: Senin Canva Tasarımın */
.stApp {{
    background-image: url("data:image/png;base64,{img_base64}") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}

/* Giriş Ekranı: Saydam Glassmorphism */
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {{
    background: rgba(0, 0, 0, 0.5) !important;
    backdrop-filter: blur(12px);
    padding: 50px !important;
    border-radius: 4px !important;
    border: 1px solid rgba(255, 75, 180, 0.2) !important;
    box-shadow: 0 15px 50px 0 rgba(0, 0, 0, 0.8);
    text-align: center;
}}

/* UI Temizliği */
#MainMenu, footer, header, .stAppDeployButton {{visibility: hidden;}}
[data-testid="stSidebar"] svg, [data-testid="stHeaderActionElements"] {{display: none !important;}}

/* Terminal Genel Fontları */
body, [data-testid="stAppViewContainer"], p, div, span, button, input {{ 
    font-family: 'JetBrains Mono', monospace !important; 
    color: #d1d1d1 !important;
}}

/* Sidebar ve Kartlar */
section[data-testid="stSidebar"] {{ 
    background-color: rgba(5, 5, 5, 0.95) !important; 
    border-right: 1px solid rgba(255, 75, 180, 0.15); 
}}

.industrial-card {{ 
    background: rgba(15, 15, 15, 0.85) !important; 
    border: 1px solid rgba(255, 255, 255, 0.03) !important; 
    border-top: 2px solid #ff4bb4 !important; 
    padding: 22px; 
    margin-bottom: 20px; 
    border-radius: 4px;
    backdrop-filter: blur(5px);
}}

.stButton button {{
    width: 100% !important;
    background: #ff4bb4 !important;
    color: white !important;
    border: none !important;
    font-weight: 800 !important;
    font-family: 'Orbitron' !important;
    padding: 12px !important;
    letter-spacing: 2px !important;
}}

.terminal-header {{ 
    color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; 
    text-transform: uppercase; margin-bottom: 18px; border-left: 3px solid #ff4bb4; padding-left: 12px;
}}
</style>
"""

# --- 4. VERİ VE RÜTBE FONKSİYONLARI ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
        return dict(zip(df['key'].astype(str), df['value'].astype(str)))
    except:
        return {"kasa": "600", "ana_para": "600"}

def rutbe_getir(puan_str):
    try: p = int(float(puan_str))
    except: p = 0
    if p <= 3: return "Hılez"
    elif p <= 6: return "Tecrübeli Hılez"
    elif p <= 11: return "Miço"
    else: return "Grand Miço"

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

# --- 5. GÜVENLİK VE GİRİŞ (ÖZEL TASARIM) ---
if "password_correct" not in st.session_state: 
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div style="height:35vh;"></div>', unsafe_allow_html=True)
        
        col_a, col_b, col_c = st.columns([1,1.5,1])
        with col_b:
            st.markdown("""
                <div style="text-align:center; margin-bottom:15px;">
                    <p style="font-family:JetBrains Mono; color:#ff4bb4; font-size:14px; font-weight:900; letter-spacing:3px;">
                        ÖZÜNDE DİSİPLİN, GELECEĞİNDE ÖZGÜRLÜK
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            pwd = st.text_input("ŞİFRE", type="password", placeholder="Erişim anahtarını gir...", label_visibility="collapsed")
            
            if st.button("TERMİNALİ BAŞLAT"):
                if pwd == "1608":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else: 
                    st.error("YETKİSİZ ERİŞİM")
        return False
    return True

# --- 6. ANA UYGULAMA DÖNGÜSÜ ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:22px; letter-spacing:5px; text-align:center;'>OG CORE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; font-size:10px; color:#ff4bb4;'>TERMINAL V9.9</p>", unsafe_allow_html=True)
        st.divider()
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE"])
        if st.button("GÜVENLİ ÇIKIŞ"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 KİŞİSEL KASA DAĞILIMI</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card'><div>Oguzo</div><div style='color:#ff4bb4; font-size:20px;'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card'><div>Ero7</div><div style='color:#ff4bb4; font-size:20px;'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card'><div>Fybey</div><div style='color:#ff4bb4; font-size:20px;'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)

        st.divider()
        
        col1, col2 = st.columns([2,1])
        with col1:
            net_kar = kasa - ana_para
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>💎 ANA KASA DURUMU</div><h2 style='color:white;'>${kasa:,.2f}</h2><p>Net Kâr: <span style='color:#00ff41;'>${net_kar:,.2f}</span></p></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📊 WIN RATE</div><h2 style='color:#ff4bb4;'>%{live_vars.get('win_rate', '0')}</h2></div>", unsafe_allow_html=True)

    # (Diğer sayfalar - FORMLINE ve CHALLANGE - mevcut mantığınla buraya eklenebilir)
    # Tasarımın ana hatları bu şekilde hazır kanka.
