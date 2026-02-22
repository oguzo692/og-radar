import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import numpy as np

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. VERİ BAĞLANTISI (GOOGLE SHEETS) ---
@st.cache_data(ttl=60)  # Veriyi 60 saniyede bir tazeler
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        data = dict(zip(df['key'].astype(str), df['value'].astype(str)))
        return data
    except Exception:
        return {"kasa": "600.0", "ana_para": "600.0"}

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

# Veri Atamaları
og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))
og_p, er_p, fy_p = live_vars.get("oguzo_puan", "0"), live_vars.get("ero7_puan", "0"), live_vars.get("fybey_puan", "0")
aktif_soru_1 = live_vars.get("aktif_soru", "yeni soru yakında...")
aktif_soru_2 = live_vars.get("aktif_soru2", "yeni soru yakında...")
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS STİLLERİ ---
common_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');
#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
[data-testid="stSidebar"] svg, [data-testid="stHeaderActionElements"] {display: none !important;}
section[data-testid="stSidebar"] { background-color: rgba(5, 5, 5, 0.95) !important; border-right: 1px solid rgba(204, 122, 0, 0.15); min-width: 300px !important;}
.stButton button { width: 100% !important; background: rgba(204, 122, 0, 0.1) !important; border: 1px solid rgba(204, 122, 0, 0.3) !important; color: #cc7a00 !important; font-family: 'Orbitron' !important;}
body, [data-testid="stAppViewContainer"] { font-family: 'JetBrains Mono', monospace !important; color: #d1d1d1 !important; background: #030303 !important;}
.industrial-card { background: rgba(15, 15, 15, 0.8); border-top: 2px solid rgba(204, 122, 0, 0.4); padding: 22px; margin-bottom: 20px; border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); transition: 0.3s;}
.industrial-card:hover { transform: translateY(-5px); border-top-color: #ffae00; background: rgba(25, 25, 25, 0.9);}
.terminal-header { color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px;}
.highlight { color: #FFFFFF !important; font-size: 14px;}
.terminal-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;}
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0;}
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite;}
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
</style>
"""

login_bg_css = """
<style>
.stApp { background: linear-gradient(135deg, #050505 0%, #111 100%) !important; }
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(10, 10, 10, 0.9) !important; padding: 50px !important; border-radius: 15px !important;
    border: 1px solid rgba(204, 122, 0, 0.3); position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 999; width: 350px;
}
</style>
"""

# --- 4. KUPON HTML ŞABLONLARI ---
w5_matches = """<div class='terminal-row'><span>konyaspor - gala</span><span class='highlight'>gala w & +2 </span></div><div class='terminal-row'><span>leipzig - bvb</span><span class='highlight'>kg </span></div><div class='terminal-row'><span>man city - newcastle</span><span class='highlight'>x1 & +2</span></div><hr style='opacity:0.1'><div class='terminal-row'><span>Oran: 8.26</span><span>Tutar: 100 USD</span></div>"""
# (Diğer kuponları kodun içinde direkt değişkenlere atadık)

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        with st.container():
            pwd = st.text_input("SİSTEM GİRİŞİ (PIN)", type="password", placeholder="----")
            if pwd == "1608":
                st.session_state["password_correct"] = True
                st.rerun()
            elif pwd != "":
                st.error("ACCESS DENIED")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span style="color:#cc7a00; letter-spacing:4px;">{duyuru_metni} --- {duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:22px; text-align:center;'>OG CORE</h1>", unsafe_allow_html=True)
        st.divider()
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip"])
        st.divider()
        if st.button("SİSTEMDEN ÇIK"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 Kişisel Kasa Dağılımı</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Oguzo</div><div class='highlight'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Ero7</div><div class='highlight'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Fybey</div><div class='highlight'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        
        net_kar = kasa - ana_para
        current_pct = max(0, min(100, ((kasa - 600) / (1200 - 600)) * 100))
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>HEDEF YOLCULUĞU ($1.200)</div><div style='background:#111; height:8px; border-radius:10px;'><div style='background:linear-gradient(90deg, #cc7a00, #ffae00); width:{current_pct}%; height:100%; border-radius:10px;'></div></div><div style='text-align:right; font-size:10px; margin-top:5px;'>%{current_pct:.1f}</div></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='industrial-card' style='height:200px;'><div class='terminal-header'>💎 KASA</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>K/Z</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'}; font-weight:bold;'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                sol = yf.Ticker("SOL-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card' style='height:200px;'><div class='terminal-header'>⚡ PİYASA</div><div class='terminal-row'><span>BTC</span><span class='highlight'>${btc:,.0f}</span></div><div class='terminal-row'><span>SOL</span><span class='highlight'>${sol:,.2f}</span></div></div>", unsafe_allow_html=True)
            except: st.write("Piyasa Yükleniyor...")
        with col3: st.markdown(f"<div class='industrial-card' style='height:200px;'><div class='terminal-header'>📊 Win Rate</div><div style='text-align:center; font-size:40px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        toplam_bahis_kar = float(live_vars.get("w1_sonuc",0)) + float(live_vars.get("w2_sonuc",0)) + float(live_vars.get("w3_sonuc",0))
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 PERFORMANS</div><div style='font-size:32px; font-family:Orbitron; color:#00ff41;'>${toplam_bahis_kar:,.2f}</div></div>", unsafe_allow_html=True)
        t5, t4, t3 = st.tabs(["⏳ W5 (AKTİF)", "❌ W4", "✅ W3"])
        with t5: st.markdown(f"<div class='industrial-card'>{w5_matches}</div>", unsafe_allow_html=True)
        with t4: st.write("W4 Verileri Arşivlendi.")
        with t3: st.write("W3 Verileri Arşivlendi.")

    elif page == "📊 Portföy Takip":
        st.markdown("<div class='terminal-header'>🏛️ PORTFÖY KOMUTA MERKEZİ</div>", unsafe_allow_html=True)
        try:
            usd_try = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]
            ons_gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            gram_altin = (ons_gold / 31.1035) * usd_try
            
            users = ["oguzo", "ero7", "fybey"]
            u_choice = st.selectbox("Kullanıcı Seç:", [u.upper() for u in users])
            u_key = u_choice.lower()
            
            u_usd = float(live_vars.get(f"{u_key}_usd", 0))
            u_gr = float(live_vars.get(f"{u_key}_altin", 0))
            total_val = u_usd + (u_gr * gram_altin / usd_try)

            st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:14px; color:#666;'>TOPLAM DEĞER</div><div style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>${total_val:,.2f}</div><div style='color:#444;'>≈ ₺{(total_val * usd_try):,.0f}</div></div>", unsafe_allow_html=True)
            
            v1, v2 = st.columns(2)
            v1.markdown(f"<div class='industrial-card' style='text-align:center;'>Nakit: ${u_usd:,.0f}</div>", unsafe_allow_html=True)
            v2.markdown(f"<div class='industrial-card' style='text-align:center;'>Altın: {u_gr} gr</div>", unsafe_allow_html=True)

            # Projeksiyon Grafiği
            st.divider()
            st.markdown("<div class='terminal-header'>🧠 AI PROJEKSİYONU (HAZİRAN 2026)</div>", unsafe_allow_html=True)
            tahminler = [total_val * (1.1 ** i) for i in range(5)]
            st.area_chart(pd.DataFrame(tahminler, index=["Şub","Mar","Nis","May","Haz"]), color="#cc7a00")
        except: st.error("Finansal veriler çekilemedi.")

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG CORE TERMINAL // {datetime.now().year}</div>", unsafe_allow_html=True)
