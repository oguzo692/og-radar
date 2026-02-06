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
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")

og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "Gala maçı gala w ?")
aktif_soru_2 = live_vars.get("aktif_soru2", "BTC 7 Şubat günlük kapanış 70k")

w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 453))
toplam_bahis_kar = w1_kar + w2_kar
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS (MOBİL VE GÖRSEL DÜZELTMELER) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&family=Orbitron:wght@400;700&display=swap');
#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
[data-testid="stSidebarNav"] {display: none !important;}
[data-testid="stSidebar"] p {font-size: 14px !important; color: #d1d1d1 !important;}
/* Mobilde Sidebar Okunu Görünür Yap */
button[kind="headerNoContext"] svg { fill: #cc7a00 !important; visibility: visible !important; }
.stApp { background-color: #030303 !important; background-image: radial-gradient(circle at 50% 50%, rgba(204, 122, 0, 0.07) 0%, transparent 70%);}
section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid rgba(204, 122, 0, 0.15); min-width: 340px !important;}
@media (max-width: 768px) { section[data-testid="stSidebar"] { min-width: 100vw !important; } }
.stButton button { background: rgba(204, 122, 0, 0.1) !important; border: 1px solid rgba(204, 122, 0, 0.3) !important; color: #cc7a00 !important; font-family: 'Orbitron' !important;}
body, [data-testid="stAppViewContainer"], p, div, span { font-family: 'JetBrains Mono', monospace !important; color: #d1d1d1 !important;}
.industrial-card { background: linear-gradient(145deg, rgba(15, 15, 15, 0.9), rgba(5, 5, 5, 1)) !important; border-top: 2px solid rgba(204, 122, 0, 0.4) !important; padding: 20px; margin-bottom: 20px; border-radius: 4px;}
.terminal-header { color: #666; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; border-left: 3px solid #cc7a00; padding-left: 10px; margin-bottom: 15px;}
.terminal-row { display: flex; justify-content: space-between; margin-bottom: 10px;}
.highlight { color: #FFFFFF !important; }
.val-std { font-size: 22px !important; font-family: 'Orbitron'; }
.ticker-wrap { background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; overflow: hidden;}
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
</style>
""", unsafe_allow_html=True)

# --- 4. KUPON ŞABLONLARI ---
w3_matches = "<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5</span></div>"
w2_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>✅ W2 KUPONU</div><span style='color:#00ff41;'>SONUÇLANDI ✅</span></div>"
w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU</div>{w3_matches}<span>BEKLENİYOR ⏳</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False
def check_password():
    if not st.session_state["password_correct"]:
        st.markdown('<div style="text-align:center; margin-top:20vh; font-family:Orbitron; font-size:50px; color:white;">OG CORE</div>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1,1,1])
        with col_b:
            pwd = st.text_input("Şifre", type="password")
            if st.button("Giriş"):
                if pwd == "1608": 
                    st.session_state["password_correct"] = True
                    st.rerun()
                else: st.error("Hatalı!")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span>{duyuru_metni} &nbsp;&nbsp;&nbsp; {duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='text-align:center; font-family:Orbitron; color:white;'>OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("SİSTEM", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE"])
        if st.button("ÇIKIŞ"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 KİŞİSEL KASA</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='industrial-card' style='text-align:center;'>Oguzo<br><span class='highlight'>${og_kasa:,.2f}</span></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='industrial-card' style='text-align:center;'>Ero7<br><span class='highlight'>${er_kasa:,.2f}</span></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='industrial-card' style='text-align:center;'>Fybey<br><span class='highlight'>${fy_kasa:,.2f}</span></div>", unsafe_allow_html=True)

        st.divider()

        # --- HEDEF BARI (DÜZELTİLMİŞ) ---
        if kasa < 900: alt, ust, ikon = 600, 900, "🎯"
        elif kasa < 1200: alt, ust, ikon = 900, 1200, "🚀"
        else: alt, ust, ikon = 1200, 1800, "👑"
        
        yuzde = min((max(kasa, alt) - alt) / (ust - alt), 1.0) * 100
        c1 = "#cc7a00" if kasa >= 900 else "#444"
        c2 = "#cc7a00" if kasa >= 1200 else "#444"
        m2 = "#cc7a00" if yuzde >= 50 else "#333"

        # HTML'i f-string'den ayırarak hata riskini sıfıra indirdik
        bar_html = f"""
        <div class="industrial-card">
            <div style="display:flex; justify-content:space-between;">
                <span class="terminal-header">HEDEF BARI {ikon}</span>
                <span style="color:#cc7a00;">KASA: ${kasa:,.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:10px; margin-top:10px;">
                <span style="color:{c1}">L1 ($900)</span>
                <span style="color:{c2}">L2 ($1200)</span>
                <span style="color:#444">FINAL ($1800)</span>
            </div>
            <div style="background:#111; height:12px; border-radius:10px; margin-top:5px; position:relative; border:1px solid #222;">
                <div style="background:linear-gradient(90deg, #cc7a00, #ffae00); width:{yuzde}%; height:100%; border-radius:10px;"></div>
                <div style="position:absolute; left:50%; top:0; width:2px; height:100%; background:{m2};"></div>
            </div>
        </div>
        """
        st.markdown(bar_html, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        net_kar = kasa - ana_para
        col1.markdown(f"<div class='industrial-card'>💎 KASA<br><span class='highlight'>${kasa:,.2f}</span><br><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'}'>${net_kar:,.2f}</span></div>", unsafe_allow_html=True)
        
        try:
            btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
            col2.markdown(f"<div class='industrial-card'>⚡ PİYASA<br>BTC: <span class='highlight'>${btc:,.0f}</span></div>", unsafe_allow_html=True)
        except: col2.write("Veri bekleniyor...")
        
        col3.markdown(f"<div class='industrial-card'>📊 WIN RATE<br><span style='font-size:30px; color:#cc7a00;'>%{wr_oran}</span></div>", unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 RÜTBE SIRALAMASI</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        s1.markdown(f"<div class='industrial-card'>oguzo: {og_p}P<br>{rutbe_getir(og_p)}</div>", unsafe_allow_html=True)
        s2.markdown(f"<div class='industrial-card'>ero7: {er_p}P<br>{rutbe_getir(er_p)}</div>", unsafe_allow_html=True)
        s3.markdown(f"<div class='industrial-card'>fybey: {fy_p}P<br>{rutbe_getir(fy_p)}</div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'>📈 NET KAR: <span style='color:#00ff41;'>${toplam_bahis_kar:,.2f}</span></div>", unsafe_allow_html=True)
        st.markdown(w3_coupon_html, unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:30px;'>OG_CORE_V9.9 // {datetime.now().year}</div>", unsafe_allow_html=True)
