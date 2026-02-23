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
w6_kar = float(live_vars.get("w6_sonuc", 0)) # Yeni Eklendi
toplam_bahis_kar = w1_kar + w2_kar + w3_kar + w4_kar + w5_kar + w6_kar

wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS STİLLERİ ---
common_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');
#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
section[data-testid="stSidebar"] { background-color: rgba(5, 5, 5, 0.95) !important; border-right: 1px solid rgba(204, 122, 0, 0.15); min-width: 340px !important;}
body, [data-testid="stAppViewContainer"] { font-family: 'JetBrains Mono', monospace !important; color: #d1d1d1 !important; background: #030303 !important;}
.industrial-card { background: rgba(15, 15, 15, 0.8); border: 1px solid rgba(255, 255, 255, 0.03); border-top: 2px solid rgba(204, 122, 0, 0.4); padding: 22px; margin-bottom: 20px; border-radius: 4px; transition: all 0.3s ease;}
.terminal-header { color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px;}
.terminal-row { display: flex; justify-content: space-between; align-items: center; font-size: 14px; margin-bottom: 12px;}
.highlight { color: #FFFFFF !important; }
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; margin-bottom: 25px;}
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
</style>
"""

login_bg_css = """
<style>
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(10, 10, 10, 0.75); padding: 55px; border-radius: 18px; border: 1px solid rgba(204, 122, 0, 0.35);
    position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 360px;
}
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w5_matches = """<div class='terminal-row'><span>leipzig - bvb</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>konyaspor - gala</span><span class='highlight'>gala ❌</span></div><hr><div class='terminal-row'><span>Bet: 100 USD</span></div>"""
w3_matches = """<div class='terminal-row'><span>rizespor - gala</span><span class='highlight'>gala w ✅</span></div><hr><div class='terminal-row'><span>Oran: 8.79</span></div>"""
w2_matches = """<div class='terminal-row'><span>gala - kayseri</span><span class='highlight'>w ✅</span></div><hr><div class='terminal-row'><span>Oran: 5.53</span></div>"""
w1_matches = """<div class='terminal-row'><span>karagümrük - gala</span><span class='highlight'>w ✅</span></div><hr><div class='terminal-row'><span>Sonuç: ❌</span></div>"""

w5_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W5 KUPONU</div>{w5_matches}</div>"
w4_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W4 KUPONU</div>{w5_matches}</div>"
w3_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W3 KUPONU</div>{w3_matches}</div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU</div>{w2_matches}</div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU</div>{w1_matches}</div>"

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
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span style="color:#cc7a00; letter-spacing:4px;">{duyuru_metni} --- </span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; text-align:center;'>OG CORE</h1>", unsafe_allow_html=True)
        page = st.radio("Menu", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip"], label_visibility="collapsed")
        st.divider()
        if st.button("SİSTEMDEN ÇIK"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 Kişisel Kasa Dağılımı</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Oguzo</div><div class='highlight'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Ero7</div><div class='highlight'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Fybey</div><div class='highlight'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        
        net_kar = kasa - ana_para
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='industrial-card'><div class='terminal-header'>💎 KASA</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>K/Z</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'}; font-weight:bold;'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card'><div class='terminal-header'>⚡ PİYASA</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div></div>", unsafe_allow_html=True)
            except: st.write("Piyasa verisi bekleniyor...")
        with col3: st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📊 Win Rate</div><div style='text-align:center; font-size:40px; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 PERFORMANS</div><div class='terminal-row'><span>NET Kâr/Zarar:</span><span style='color:#00ff41; font-size:32px; font-family:Orbitron;'>${toplam_bahis_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        
        t6, t5, t4, t3, t2, t1 = st.tabs(["🚀 W6", "❌ W5", "❌ W4", "✅ W3", "✅ W2", "❌ W1"])
        
        with t6:
            w6_status = "✅ BAŞARILI" if w6_kar > 0 else "❌ BAŞARISIZ" if w6_kar < 0 else "⏳ BEKLENİYOR"
            w6_color = "#00ff41" if w6_kar > 0 else "#ff4b4b" if w6_kar < 0 else "#cc7a00"
            st.markdown(f"""
                <div class='industrial-card' style='border-top-color: {w6_color} !important;'>
                    <div class='terminal-header' style='color:{w6_color};'>{w6_status} - WEEK 6</div>
                    <div class='terminal-row'><span>BVB - Leipzig</span><span class='highlight'>KG VAR ✅</span></div>
                    <div class='terminal-row'><span>Real Madrid - Atleti</span><span class='highlight'>2.5 ÜST ✅</span></div>
                    <hr>
                    <div class='terminal-row'><span>Haftalık Sonuç:</span><span style='color:white;'>${w6_kar}</span></div>
                </div>
            """, unsafe_allow_html=True)
        with t5: st.markdown(w5_coupon_html, unsafe_allow_html=True)
        with t4: st.markdown(w4_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t1: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 SIRALAMA</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='industrial-card'>oguzo: {og_p} P<br>{rutbe_getir(og_p)}</div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='industrial-card'>ero7: {er_p} P<br>{rutbe_getir(er_p)}</div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='industrial-card'>fybey: {fy_p} P<br>{rutbe_getir(fy_p)}</div>", unsafe_allow_html=True)

    elif page == "📊 Portföy Takip":
        st.markdown("<div class='terminal-header'>🏛️ PORTFÖY</div>", unsafe_allow_html=True)
        st.info("Portföy verileri Google Sheets üzerinden güncellenmektedir.")

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG CORE // {datetime.now().year}</div>", unsafe_allow_html=True)
