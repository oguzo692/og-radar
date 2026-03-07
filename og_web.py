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
@st.cache_data(ttl=60)
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
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

# Verileri Çek
live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")

# Kişisel Kasa
og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

# Puanlar
og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "yeni soru yakında...")
aktif_soru_2 = live_vars.get("aktif_soru2", "yeni soru yakında...")

# Bahis Kar/Zarar
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

# --- 3. CSS (Gelişmiş Terminal Görünümü) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');
#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #cc7a0033; min-width: 300px !important;}
body, [data-testid="stAppViewContainer"] { background-color: #030303 !important; font-family: 'JetBrains Mono', monospace !important; color: #d1d1d1 !important;}

.industrial-card { 
    background: rgba(15, 15, 15, 0.9); border: 1px solid rgba(255, 255, 255, 0.05); 
    border-top: 2px solid #cc7a00; padding: 20px; margin-bottom: 15px; border-radius: 4px;
}
.terminal-header { color: #666; font-size: 11px; letter-spacing: 2px; margin-bottom: 15px; border-left: 3px solid #cc7a00; padding-left: 10px; text-transform: uppercase;}
.highlight { color: #FFF; font-size: 16px; font-weight: 700; }
.val-std { font-size: 24px; font-weight: 800; font-family: 'Orbitron'; color: #cc7a00; }
.terminal-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px;}

/* Ticker Animasyonu */
.ticker-wrap { width: 100%; overflow: hidden; background: #cc7a0011; border-bottom: 1px solid #cc7a0033; padding: 10px 0; margin-bottom: 20px;}
.ticker { display: flex; white-space: nowrap; animation: ticker 40s linear infinite; }
.ticker-item { font-size: 12px; color: #cc7a00; letter-spacing: 3px; padding-right: 100px; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

@media (max-width: 768px){
    [data-testid="column"] { width: 100% !important; flex: 100% !important; }
}
</style>
""", unsafe_allow_html=True)

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        cols = st.columns([1, 1, 1])
        with cols[1]:
            st.markdown("<br><br><h2 style='text-align:center; font-family:Orbitron;'>ENTER PIN</h2>", unsafe_allow_html=True)
            pwd = st.text_input("", type="password", placeholder="****", label_visibility="collapsed")
            if pwd == "1608":
                st.session_state["password_correct"] = True
                st.rerun()
            elif pwd: st.error("DENIED")
        return False
    return True

if check_password():
    # Ticker
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; text-align:center;'>OG CORE</h1>", unsafe_allow_html=True)
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip", "💠 FTMO"])
        st.divider()
        if st.button("SİSTEMDEN ÇIK"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- SAYFA MANTIKLARI ---
    if page == "⚡ ULTRA ATAK":
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card'><div class='terminal-header'>Oguzo</div><div class='val-std'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card'><div class='terminal-header'>Ero7</div><div class='val-std'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card'><div class='terminal-header'>Fybey</div><div class='val-std'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)

        net_kar = kasa - ana_para
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>DURUM MERKEZİ</div><div class='terminal-row'><span>Toplam Kasa</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>Net Kar/Zarar</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};' class='highlight'>${net_kar:,.2f}</span></div><div class='terminal-row'><span>Win Rate</span><span class='highlight'>%{wr_oran}</span></div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>PERFORMANS</div><div class='val-std'>${toplam_bahis_kar:,.2f}</div></div>", unsafe_allow_html=True)
        tabs = st.tabs(["⏳ W7", "❌ W6", "❌ W5", "❌ W4", "✅ W3", "✅ W2", "❌ W1"])
        # İçerikler buraya gelecek (Senin orijinal HTML kupon yapıların)
        for i, t in enumerate(tabs):
            with t: st.write(f"W{7-i} Verileri Terminalden Okunuyor...")

    elif page == "📊 Portföy Takip":
        st.markdown("<div class='terminal-header'>🏛️ PORTFÖY KOMUTA MERKEZİ</div>", unsafe_allow_html=True)
        try:
            usd_try = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]
            ons_gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            gram_altin = (ons_gold / 31.1035) * usd_try
            
            user = st.selectbox("USER", ["OGUZO", "ERO7", "FYBEY"])
            u_usd = float(live_vars.get(f"{user.lower()}_usd", 0))
            u_altin = float(live_vars.get(f"{user.lower()}_altin", 0))
            total_usd = u_usd + (u_altin * gram_altin / usd_try)
            
            st.markdown(f"<div class='industrial-card' style='text-align:center;'><div class='terminal-header'>TOPLAM VARLIK</div><div style='font-size:48px;' class='val-std'>${total_usd:,.2f}</div></div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1: st.metric("Nakit", f"${u_usd:,.0f}")
            with c2: st.metric("Altın (Gr)", f"{u_altin} gr")
        except: st.error("Piyasa verisi alınamadı.")

    elif page == "💠 FTMO":
        st.markdown("<div class='terminal-header'>💠 FTMO TRACKER</div>", unsafe_allow_html=True)
        bf_equity = float(live_vars.get("bf_equity", 100000))
        bf_balance = float(live_vars.get("bf_balance", 100000))
        bf_target = bf_balance * 1.10
        
        progress = min(100.0, max(0.0, (bf_equity - bf_balance) / (bf_target - bf_balance) * 100))
        
        st.markdown(f"""
            <div class='industrial-card'>
                <div class='terminal-header'>HEDEF: ${bf_target:,.0f}</div>
                <div style='background:#111; height:20px; border-radius:10px;'>
                    <div style='background:linear-gradient(90deg, #00ff41, #008f11); width:{progress}%; height:100%; border-radius:10px;'></div>
                </div>
                <div style='display:flex; justify-content:space-between; margin-top:10px;'>
                    <span>Equity: ${bf_equity:,.2f}</span>
                    <span>%{progress:.1f}</span>
                </div>
            </div>
            <div class='industrial-card'>
                <div class='terminal-header'>LİMİTLER</div>
                <div class='terminal-row'><span>Günlük Limit (5%)</span><span style='color:#ff4b4b;'>$5,000</span></div>
                <div class='terminal-row'><span>Max Kayıp (10%)</span><span style='color:#ff4b4b;'>$10,000</span></div>
            </div>
        """, unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 GLOBAL RANKING</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div class='terminal-header'>OGUZO</div><div class='highlight'>{og_p} P</div><div>{rutbe_getir(og_p)}</div></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div class='terminal-header'>ERO7</div><div class='highlight'>{er_p} P</div><div>{rutbe_getir(er_p)}</div></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div class='terminal-header'>FYBEY</div><div class='highlight'>{fy_p} P</div><div>{rutbe_getir(fy_p)}</div></div>", unsafe_allow_html=True)
