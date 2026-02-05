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

# --- 2. VERİ BAĞLANTISI ---
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
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... VERİLER SENKRONİZE EDİLDİ...")

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 453))
toplam_bahis_kar = w1_kar + w2_kar

# --- 📊 PERFORMANS VERİLERİ ---
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", ""))

# --- 3. CSS STİLLERİ (KAYMA ENGELLEYİCİ) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Orbitron:wght@400;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}

.stApp { 
    background-color: #030303 !important;
    background-image: radial-gradient(circle at 50% 50%, rgba(204, 122, 0, 0.05) 0%, transparent 60%);
}

body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], p, div, span, h1, h2, h3, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
    color: #e0e0e0 !important;
}

.ticker-wrap {
    width: 100%; overflow: hidden; background: rgba(0, 0, 0, 0.8);
    border-bottom: 1px solid rgba(204, 122, 0, 0.3); padding: 12px 0;
    margin-bottom: 25px; backdrop-filter: blur(10px);
}
.ticker { display: flex; white-space: nowrap; animation: ticker 40s linear infinite; }
.ticker-item { padding-right: 100%; color: #cc7a00; letter-spacing: 3px; font-size: 13px; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

.industrial-card { 
    background: rgba(18, 18, 18, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-top: 2px solid #cc7a00 !important;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 4px;
    min-height: 150px;
}

.terminal-header { 
    color: #888; font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; 
    margin-bottom: 15px; border-left: 3px solid #cc7a00; padding-left: 10px;
}

.terminal-row { 
    display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 10px; 
    border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 5px; 
}

.highlight { color: #cc7a00 !important; font-weight: 700; font-size: 22px; }

/* Progress Bar */
.loot-track { background: #111; height: 12px; border-radius: 6px; width: 100%; position: relative; margin-top: 40px; border: 1px solid #222; }
.loot-fill { background: linear-gradient(90deg, #cc7a00, #ffae00); height: 100%; border-radius: 6px; box-shadow: 0 0 15px rgba(204, 122, 0, 0.5); }
.milestone { position: absolute; top: 50%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; }
.milestone-label { position: absolute; top: 25px; font-size: 11px; color: #888; text-align: center; white-space: nowrap; }

div.stButton > button { background: transparent !important; color: #cc7a00 !important; border: 1px solid #cc7a00 !important; width: 100%; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - GS</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Liverpool - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 10px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>GS - Kayserispor</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Liverpool - Newcastle</span><span style='color:#00ff41;'>+2 & Liverpool 1X ✅</span></div><div class='terminal-row'><span>BVB - Heidenheim</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Kocaelispor - FB</span><span style='color:#00ff41;'>FB W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 10px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Karagümrük - GS</span><span style='color:#00ff41;'>GS W & +2 ✅</span></div><div class='terminal-row'><span>Bournemouth - Liverpool</span><span style='color:#00ff41;'>KG VAR ✅</span></div><div class='terminal-row'><span>Union Berlin - BVB</span><span style='color:#00ff41;'>BVB İY 0.5 Üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>New +2 ❌</span></div><div class='terminal-row'><span>FB - Göztepe</span><span style='color:#ff4b4b;'>FB W ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 10px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""

w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU (AKTİF)</div>{w3_matches}</div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (1-2 ŞUBAT)</div>{w2_matches}</div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (24-25 OCAK)</div>{w1_matches}</div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; padding:5rem;"><h1 style="font-family:Orbitron; font-size:55px; letter-spacing:10px;">OG_CORE</h1><p style="color:#cc7a00; letter-spacing:5px;">ARCHITECTING THE FUTURE</p></div>', unsafe_allow_html=True)
        pwd = st.text_input("ERİŞİM ANAHTARI", type="password", label_visibility="collapsed")
        if st.button("TERMİNALİ AÇ"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("REDDEDİLDİ")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00; font-family:Orbitron; text-align:center;'>OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MODÜLLER", ["⚡ ULTRA ATAK FON", "⚽ FORMLINE", "📊 SİMÜLASYON"])
        st.divider()
        if st.button("Çıkış"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK FON":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        
        # Targets
        current_pct = min(100, (kasa / 6500) * 100)
        st.markdown(f"<div style='background:rgba(18,18,18,0.8); padding:25px; border-radius:4px; margin-bottom:25px;'><div class='terminal-header'>HEDEF İLERLEME DURUMU</div><div class='loot-track'><div class='loot-fill' style='width:{current_pct}%'></div></div></div>", unsafe_allow_html=True)
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>💎 TİCARET RADARI</div><div class='terminal-row'><span>NET K/Z</span><span style='color:#00ff41; font-weight:bold;'>${net_kar:,.2f}</span></div><div class='terminal-row'><span>KASA</span><span class='highlight'>${kasa:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card'><div class='terminal-header'>⚡ PİYASA NABZI</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div><div class='terminal-row'><span>DURUM</span><span style='color:#00ff41;'>ONLINE</span></div></div>", unsafe_allow_html=True)
            except: st.markdown("<div class='industrial-card'>Senkronizasyon Hatası</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📊 BAŞARI ORANI</div><div style='text-align:center; padding-top:10px;'><span style='font-size:45px; font-weight:900; color:#cc7a00;'>%{wr_oran}</span></div></div>", unsafe_allow_html=True)

        st.subheader("🎯 Pay Dağılımı")
        c1, c2, c3 = st.columns(3)
        for c, u in zip([c1, c2, c3], ["oguzo", "ero7", "fybey"]):
            c.markdown(f"<div class='industrial-card' style='min-height:120px;'><div class='terminal-header'>{u.upper()}</div><div class='terminal-row'><span>HİSSE</span><span class='highlight'>${kasa/3:,.2f}</span></div></div>", unsafe_allow_html=True)

        # --- 🕒 SON İŞLEMLER ---
        st.markdown("<div class='industrial-card' style='min-height:100px;'><div class='terminal-header'>🕒 SON İŞLEMLER</div>", unsafe_allow_html=True)
        if son_islemler_raw:
            for item in son_islemler_raw.split(','):
                st.markdown(f"<div class='terminal-row'><span>{item.strip()}</span></div>", unsafe_allow_html=True)
        else: st.markdown("<div style='color:#555;'>İşlem bekleniyor...</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 TOPLAM PERFORMANS</div><div class='terminal-row'><span>NET BAHİS K/Z</span><span style='color:#00ff41; font-size:24px; font-weight:bold;'>${toplam_bahis_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["⏳ W3", "✅ W2", "❌ W1"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    st.caption(f"OG Core v9.9 | Central System Connection Established.")
