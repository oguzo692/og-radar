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

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 453))
toplam_bahis_kar = w1_kar + w2_kar

# --- 📊 PERFORMANS VERİLERİ ---
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", ""))

# --- 3. CSS STİLLERİ ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Orbitron:wght@400;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}

.stApp { 
    background-color: #030303 !important;
    background-image: radial-gradient(circle at 50% 50%, rgba(204, 122, 0, 0.05) 0%, transparent 60%);
}

/* Sekme Temizliği */
div[data-testid="stTabContent"], div[data-testid="stTabs"], .stTabs, [data-baseweb="tab-panel"], [data-baseweb="tab-list"] {
    background-color: transparent !important;
    border: none !important;
}
[data-baseweb="tab-highlight"] { background-color: #cc7a00 !important; }
[data-baseweb="tab"] { background-color: transparent !important; border: none !important; }

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
.ticker-item {
    font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #cc7a00;
    text-transform: uppercase; letter-spacing: 3px; padding-right: 100%;
}
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

.industrial-card { 
    background: rgba(18, 18, 18, 0.8) !important; backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.05) !important; border-top: 2px solid rgba(204, 122, 0, 0.5) !important;
    padding: 20px; margin-bottom: 20px; border-radius: 4px; 
}

.terminal-header { 
    color: #888; font-size: 12px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; 
    margin-bottom: 15px; border-left: 3px solid #cc7a00; padding-left: 10px;
}

.terminal-row { 
    display: flex; justify-content: space-between; align-items: center; font-size: 15px; margin-bottom: 8px; 
    border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 6px; 
}

.val-std { font-size: 20px !important; font-weight: 700 !important; }
.highlight { color: #cc7a00 !important; font-weight: 700; font-size: 20px; }

.loot-wrapper { background: rgba(18, 18, 18, 0.8); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 4px; padding: 25px; margin-bottom: 25px; position: relative; }
.loot-track { background: #111; height: 10px; border-radius: 5px; width: 100%; position: relative; margin-top: 35px; border: 1px solid #222; }
.loot-fill { background: linear-gradient(90deg, #cc7a00, #ffae00); height: 100%; border-radius: 5px; box-shadow: 0 0 10px rgba(204, 122, 0, 0.3); }

section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid rgba(204, 122, 0, 0.2); }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - GS</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Liverpool - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 10px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>Tarih: 1-2 Şubat</span><span>Bütçe: 100 USD</span></div><div class='terminal-row'><span>GS - Kayserispor</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Liverpool - Newcastle</span><span style='color:#00ff41;'>+2 & Liverpool 1X ✅</span></div><div class='terminal-row'><span>BVB - Heidenheim</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Kocaelispor - FB</span><span style='color:#00ff41;'>FB W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 10px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Tarih: 24-25 Ocak</span><span>Bütçe: 100 USD</span></div><div class='terminal-row'><span>Karagümrük - GS</span><span style='color:#00ff41;'>GS W & +2 ✅</span></div><div class='terminal-row'><span>Bournemouth - Liverpool</span><span style='color:#00ff41;'>KG VAR ✅</span></div><div class='terminal-row'><span>Union Berlin - BVB</span><span style='color:#00ff41;'>BVB İY 0.5 Üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>New +2 ❌</span></div><div class='terminal-row'><span>FB - Göztepe</span><span style='color:#ff4b4b;'>FB W ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 10px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""

w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU (AKTİF)</div>{w3_matches}<span style='color:#cc7a00'>BEKLENİYOR ⏳</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (1-2 ŞUBAT)</div>{w2_matches}<span style='color:#00ff41;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (24-25 OCAK)</div>{w1_matches}<span style='color:#ff4b4b;'>SONUÇLANDI ❌</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        pwd = st.text_input("ERİŞİM ANAHTARI", type="password", placeholder="Şifre...", label_visibility="collapsed")
        if st.button("Giriş"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("ERİŞİM REDDEDİLDİ")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # --- LOGO VE TİCKER DÜZENİ ---
    col_t1, col_t2 = st.columns([0.9, 0.1])
    with col_t1:
        st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)
    with col_t2:
        # Buraya kendi logo dosya yolunu yaz kanka
        try:
            st.image("logo.png", width=70)
        except:
            st.markdown("<div style='color:white; font-size:10px; text-align:right;'>[LOGO]</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00; font-family:Orbitron; letter-spacing:4px; text-align:center;'>OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MODÜLLER", ["⚡ ULTRA ATAK FON", "⚽ FORMLINE", "📊 SİMÜLASYON"])
        if st.button("Çıkış"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK FON":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        
        targets = [{"val": 1000, "name": "TELEFON", "icon": "📱"}, {"val": 2500, "name": "TATİL", "icon": "✈️"}, {"val": 5000, "name": "ARABA", "icon": "🏎️"}]
        max_target = 6500
        current_pct = min(100, (kasa / max_target) * 100)
        st.markdown(f"<div class='loot-wrapper'><div class='terminal-header'>HEDEF İLERLEME DURUMU</div><div class='loot-track'><div class='loot-fill' style='width:{current_pct}%'></div></div></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='industrial-card' style='height:210px;'><div class='terminal-header'>💎 TİCARET RADARI</div><div class='terminal-row'><span>NET K/Z</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span></div><div class='terminal-row'><span>GÜNCEL KASA</span><span class='highlight'>${kasa:,.2f}</span></div></div>", unsafe_allow_html=True)
        
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="2d")
                sol = yf.Ticker("SOL-USD").history(period="2d")
                b_price = btc['Close'].iloc[-1]
                s_price = sol['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card' style='height:210px;'><div class='terminal-header'>⚡ PİYASA NABZI</div><div class='terminal-row'><span>BITCOIN</span><span>${b_price:,.0f}</span></div><div class='terminal-row'><span>SOLANA</span><span>${s_price:,.2f}</span></div></div>", unsafe_allow_html=True)
            except: st.markdown("<div class='industrial-card'>Piyasa verileri bekleniyor...</div>", unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"<div class='industrial-card' style='height:210px;'><div class='terminal-header'>📊 İŞLEM BAŞARISI</div><div style='text-align:center; padding-top:15px;'><span style='font-size:50px; font-weight:900; color:#cc7a00;'>%{wr_oran}</span></div></div>", unsafe_allow_html=True)

        st.subheader("🎯 Pay Dağılımı")
        cols = st.columns(3)
        for col, user in zip(cols, ["oguzo", "ero7", "fybey"]):
            col.markdown(f"<div class='industrial-card'><div class='terminal-header'>{user.upper()}</div><div class='terminal-row'><span>HİSSE</span><span class='highlight'>${kasa/3:,.2f}</span></div><div class='terminal-row'><span>KÂR</span><span>${(net_kar/3):,.2f}</span></div></div>", unsafe_allow_html=True)

        son_islemler_html = "<div class='industrial-card'><div class='terminal-header'>🕒 SON İŞLEMLER</div>"
        if son_islemler_raw:
            for item in son_islemler_raw.split(','):
                parts = item.split('|') if '|' in item else item.strip().split(' ')
                coin = parts[0].strip()
                amount = parts[1].strip() if len(parts) > 1 else ""
                son_islemler_html += f"<div class='terminal-row'><span>{coin}</span><span style='font-weight:bold;'>{amount}</span></div>"
        son_islemler_html += "</div>"
        st.markdown(son_islemler_html, unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card' style='border-top: 2px solid #cc7a00;'><div class='terminal-header'>📈 GENEL PERFORMANS</div><div class='terminal-row'><span>NET BAHİS K/Z:</span><span style='color:{'#00ff41' if toplam_bahis_kar >=0 else '#ff4b4b'}; font-size:28px; font-weight:900;'>${toplam_bahis_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["⏳ AKTİF (W3)", "✅ KAZANAN (W2)", "❌ KAYBEDEN (W1)"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 SİMÜLASYON":
        st.title("📈 Gelecek Projeksiyonu")
        df = pd.DataFrame({"Gün": range(30), "Tahmin ($)": [kasa * (1.05 ** (d / 7)) for d in range(30)]})
        st.line_chart(df.set_index("Gün"))

    st.caption(f"OG Core v9.9 | Veriler merkezi sistemden çekilmektedir.")
