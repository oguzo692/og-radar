import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

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
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")

# --- KİŞİSEL KASA VERİLERİ ---
og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

# --- RÜTBE VERİLERİ ---
og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "pazartesi günü çeyrek altın kuyumcu fiyatı ")
aktif_soru_2 = live_vars.get("aktif_soru2", "yeni soru geliyor...")

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 453))
toplam_bahis_kar = w1_kar + w2_kar

wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. GENEL CSS ---
common_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
[data-testid="stSidebar"] svg, [data-testid="stHeaderActionElements"], .st-emotion-cache-10trblm {display: none !important;}
[data-testid="stSidebar"] span, [data-testid="stSidebar"] small {font-size: 0 !important; color: transparent !important;}
[data-testid="stSidebar"] p {font-size: 14px !important; color: #d1d1d1 !important; visibility: visible !important;}

section[data-testid="stSidebar"] { background-color: rgba(5, 5, 5, 0.95) !important; border-right: 1px solid rgba(204, 122, 0, 0.15); padding-top: 20px; min-width: 340px !important; max-width: 340px !important;}
.stButton button, .stLinkButton a { width: 100% !important; background: rgba(204, 122, 0, 0.1) !important; border: 1px solid rgba(204, 122, 0, 0.3) !important; color: #cc7a00 !important; font-family: 'Orbitron' !important; padding: 12px !important; border-radius: 6px !important;}
body, [data-testid="stAppViewContainer"], p, div, span, button, input { font-family: 'JetBrains Mono', monospace !important; color: #d1d1d1 !important;}
.terminal-row { display: flex; justify-content: space-between; align-items: center; font-size: 14px; margin-bottom: 12px; line-height: 1.6;}
.industrial-card { background: rgba(15, 15, 15, 0.8) !important; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.03) !important; border-top: 2px solid rgba(204, 122, 0, 0.4) !important; padding: 22px; margin-bottom: 20px; border-radius: 4px;}
.terminal-header { color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px;}
.highlight { color: #FFFFFF !important; font-weight: 400; font-size: 14px; font-family: 'JetBrains Mono', monospace; }
.val-std { font-size: 22px !important; font-weight: 800 !important; font-family: 'Orbitron'; }
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; margin-bottom: 25px;}
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
.ticker-item { font-size: 12px; color: #cc7a00; letter-spacing: 4px; padding-right: 50%; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
</style>
"""

login_bg_css = """
<style>
.stApp { 
    background-image: url("https://raw.githubusercontent.com/oguzo692/og-radar/main/arkaplan.jpg") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}
/* Login Kutusu */
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(0, 0, 0, 0.5) !important;
    backdrop-filter: blur(20px) !important;
    padding: 40px 30px !important;
    border-radius: 15px !important;
    border: 1px solid rgba(204, 122, 0, 0.25) !important;
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    z-index: 9999 !important;
    width: 340px !important;
}

/* Şifre Inputu */
input[type="password"] {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(204, 122, 0, 0.3) !important;
    text-align: center !important;
    color: white !important;
    font-size: 18px !important;
    letter-spacing: 5px !important;
}

/* Giriş Yazısı (Buton) */
.stButton button {
    background: transparent !important;
    border: none !important;
    color: #cc7a00 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 11px !important;
    letter-spacing: 3px !important;
    margin-top: -15px !important; /* Kutunun dibine çek */
    text-align: center !important;
    width: 100% !important;
    padding: 0 !important;
    transition: 0.3s;
}
.stButton button:hover {
    color: white !important;
    background: transparent !important;
    text-shadow: 0 0 10px #cc7a00 !important;
}
/* Buton etrafındaki gereksiz Streamlit boşluklarını sil */
div[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w4_matches = ""
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div>"""
w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU</div>{w3_matches}</div>"
w2_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>✅ W2 KUPONU</div></div>"
w1_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>❌ W1 KUPONU</div></div>"
w4_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🆕 W4 KUPONU</div></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        
        # Header kısmı
        st.markdown("""<div style="text-align:center;">
            <p style="font-family:Orbitron; color:#cc7a00; font-size:16px; font-weight:900; letter-spacing:5px; margin-bottom:5px;">OG CORE</p>
            <p style="font-family:JetBrains Mono; color:#555; font-size:9px; margin-bottom:25px;">SECURE ACCESS REQUIRED</p>
        </div>""", unsafe_allow_html=True)
        
        # PIN Girişi
        pwd = st.text_input("şifre", type="password", placeholder="----", label_visibility="collapsed")
        
        # Giriş butonu (CSS ile metin gibi duruyor)
        if st.button("SİSTEME GİRİŞ YAP"):
            if pwd == "1608":
                st.session_state["password_correct"] = True
                st.rerun()
            else: 
                st.error("PIN REDDEDİLDİ")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    st.markdown("<style>.stApp { background: #030303 !important; background-image: none !important; }</style>", unsafe_allow_html=True)
    
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; letter-spacing:5px; text-align:center; margin-bottom:40px;'>OG CORE</h1>", unsafe_allow_html=True)
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE"])
        if st.button("ÇIKIŞ"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 KİŞİSEL KASA DAĞILIMI</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Oguzo</div><div class='highlight'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Ero7</div><div class='highlight'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Fybey</div><div class='highlight'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        t1, t2, t3, t4 = st.tabs(["⏳ W3", "✅ W2", "❌ W1", "🆕 W4"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)
        with t4: st.markdown(w4_coupon_html, unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG_CORE_V9.9 // {datetime.now().year}</div>", unsafe_allow_html=True)
