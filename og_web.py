import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- 1. AYARLAR & OTO YENİLEME ---
st.set_page_config(
    page_title="OG Core v9.0", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Her 60 saniyede bir verileri tazeler
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# --- 2. VERİ BAĞLANTISI (GOOGLE SHEETS) ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'], df['value']))
        return data
    except Exception:
        return {"kasa": 600.0, "ana_para": 600.0}

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SYSTEM ONLINE... CRYPTO MARKETS CONNECTED... V9.0 DEPLOYED...")

# --- 3. CSS STİLLERİ (PREMIUM STABİLİZE) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Orbitron:wght@400;900&display=swap');

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
.ticker { display: flex; white-space: nowrap; animation: ticker 50s linear infinite; }
.ticker-item {
    font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #cc7a00;
    text-transform: uppercase; letter-spacing: 3px; padding-right: 100%;
}
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

.auth-container {
    padding: 5rem; background: linear-gradient(145deg, rgba(15,15,15,0.98) 0%, rgba(0,0,0,1) 100%);
    border: 1px solid rgba(204, 122, 0, 0.4); box-shadow: 0 0 80px rgba(0,0,0,1);
    text-align: center; max-width: 700px; margin: 15vh auto; border-radius: 2px;
}
.auth-header { font-family: 'Orbitron', sans-serif !important; font-size: 60px; font-weight: 900; color: #ffffff; letter-spacing: 15px; }

.industrial-card { 
    background: rgba(18, 18, 18, 0.8) !important; backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.05) !important; border-top: 2px solid rgba(204, 122, 0, 0.5) !important;
    padding: 25px; margin-bottom: 25px; border-radius: 4px;
}

.terminal-header { color: #888; font-size: 11px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; }
.terminal-row { display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 8px; }
.highlight { color: #cc7a00 !important; font-weight: 700; font-size: 20px; }

.loot-wrapper { background: rgba(18, 18, 18, 0.8); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 4px; padding: 30px 25px 60px 25px; margin-bottom: 30px; position: relative; }
.loot-track { background: #111; height: 12px; border-radius: 6px; width: 100%; position: relative; margin-top: 40px; border: 1px solid #222; }
.loot-fill { background: linear-gradient(90deg, #cc7a00, #ffae00); height: 100%; border-radius: 6px; box-shadow: 0 0 15px rgba(204, 122, 0, 0.5); }
.milestone { position: absolute; top: 50%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; z-index: 10; }
.milestone-label { position: absolute; top: 25px; font-size: 10px; font-weight: bold; color: #888; text-align: center; white-space: nowrap; }

section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid rgba(204, 122, 0, 0.2); }
div.stButton > button { background: transparent !important; color: #cc7a00 !important; border: 1px solid #cc7a00 !important; letter-spacing: 5px !important; height: 50px; width: 100%; text-transform: uppercase; }
div.stButton > button:hover { background: #cc7a00 !important; color: #000 !important; }
</style>
"""

# --- 4. HTML ŞABLONLARI (KUPONLAR) ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Lıve - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 8.79</span><span>bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>Tarih: 1-2 şubat</span><span>Bütçe: 100 usd</span></div><div class='terminal-row'><span>gs - kayserispor</span><span style='color:#00ff41;'>iy +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>lıve - new</span><span style='color:#00ff41;'>+2 & liverpool 1x ✅</span></div><div class='terminal-row'><span>bvb - heidenheim</span><span style='color:#00ff41;'>iy +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>kocaelispor - fb</span><span style='color:#00ff41;'>fb W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 5.53</span><span>bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Tarih: 24-25 ocak</span><span>Bütçe: 100 usd</span></div><div class='terminal-row'><span>karagümrük - gs</span><span style='color:#00ff41;'>gs w & +2 ✅</span></div><div class='terminal-row'><span>bournemouth - lıve</span><span style='color:#00ff41;'>kg var ✅</span></div><div class='terminal-row'><span>unıon berlin - bvb</span><span style='color:#00ff41;'>bvb iy 0.5 üst ✅</span></div><div class='terminal-row'><span>new - aston villa</span><span style='color:#ff4b4b;'>new +2 ❌</span></div><div class='terminal-row'><span>fb - göztepe</span><span style='color:#ff4b4b;'>fb w ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 7.09</span><span>bet: 100 USD</span></div>"""

w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU (AKTİF)</div>{w3_matches}<span style='color:#cc7a00'>BEKLENİYOR ⏳</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (1-2 ŞUBAT)</div>{w2_matches}<span style='color:#00ff41;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (24-25 OCAK)</div>{w1_matches}<span style='color:#ff4b4b;'>SONUÇLANDI ❌</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div class="auth-container"><div class="auth-header">OG_CORE</div><div style="font-size: 10px; color: #cc7a00; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 40px; opacity: 0.8;">ARCHITECTING THE FUTURE OF WEALTH</div></div>', unsafe_allow_html=True)
        pwd = st.text_input("ERİŞİM ANAHTARI", type="password", placeholder="Enter System Key...", label_visibility="collapsed")
        if st.button("TERMİNALİ INITIALIZE ET"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00; font-family:Orbitron; letter-spacing:4px; text-align:center;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MODÜLLER", ["⚡ ULTRA ATAK FON", "⚽ FORMLINE", "📊 SIMULASYON"])
        st.divider()
        admin_key = st.text_input("ADMİN", type="password", placeholder="Admin Key...")
        if admin_key == "1":
            st.success("Admin Active")
            st.link_button("📊 Tabloyu Düzenle", "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit")
        st.divider()
        if st.button("🔴 SİSTEMDEN ÇIK"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK FON":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        
        # Targets
        targets = [{"val": 1000, "name": "TELEFON", "icon": "📱"}, {"val": 2500, "name": "TATİL", "icon": "✈️"}, {"val": 5000, "name": "ARABA", "icon": "🏎️"}]
        max_target = 6500
        current_pct = min(100, (kasa / max_target) * 100)
        m_html = "".join([f"<div class='milestone' style='left:{(t['val']/max_target)*100}%'><div style='font-size:22px;'>{t['icon'] if kasa>=t['val'] else '🔒'}</div><div class='milestone-label'>{t['name']}<br>${t['val']}</div></div>" for t in targets])
        st.markdown(f"<div class='loot-wrapper'><div class='terminal-header'>HEDEF İLERLEME DURUMU</div><div class='loot-track'><div class='loot-fill' style='width:{current_pct}%'></div>{m_html}</div></div>", unsafe_allow_html=True)
        
        # Kasa & Market
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class='industrial-card'><div class='terminal-header'>💎 TRADE RADAR V9.0</div><div class='terminal-row'><span>NET KAR/ZARAR</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'}; font-size:24px; font-weight:bold;'>${net_kar:,.2f} (%{kar_yuzdesi:.1f})</span></div><div class='terminal-row'><span>GÜNCEL KASA</span><span class='highlight'>${kasa:,.2f}</span></div></div>""", unsafe_allow_html=True)
        
        with col2:
            try:
                # Market Pulse (Isı Haritası Mantığı)
                btc_data = yf.Ticker("BTC-USD").history(period="2d")
                eth_data = yf.Ticker("ETH-USD").history(period="2d")
                
                btc_price = btc_data['Close'].iloc[-1]
                btc_change = ((btc_price - btc_data['Close'].iloc[-2]) / btc_data['Close'].iloc[-2]) * 100
                eth_price = eth_data['Close'].iloc[-1]
                eth_change = ((eth_price - eth_data['Close'].iloc[-2]) / eth_data['Close'].iloc[-2]) * 100

                st.markdown(f"""
                <div class='industrial-card'>
                    <div class='terminal-header'>⚡ MARKET PULSE (24H)</div>
                    <div class='terminal-row'><span>BITCOIN</span><span style='color:{'#00ff41' if btc_change >=0 else '#ff4b4b'}; font-weight:bold;'>${btc_price:,.0f} ({btc_change:+.2f}%)</span></div>
                    <div class='terminal-row'><span>ETHEREUM</span><span style='color:{'#00ff41' if eth_change >=0 else '#ff4b4b'}; font-weight:bold;'>${eth_price:,.0f} ({eth_change:+.2f}%)</span></div>
                </div>""", unsafe_allow_html=True)
            except: st.error("Market data connection lost.")

        # Shares Section
        st.subheader("🎯 Pay Dağılımı")
        cols = st.columns(3)
        for col, user in zip(cols, ["oguzo", "ero7", "fybey"]):
            col.markdown(f"<div class='industrial-card'><div class='terminal-header'>{user.upper()}</div><div class='terminal-row'><span>SHARE</span><span class='highlight'>${kasa/3:,.2f}</span></div><div class='terminal-row'><span>PROFIT</span><span>${(net_kar/3):,.2f}</span></div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE")
        t1, t2, t3 = st.tabs(["⏳ AKTİF (W3)", "✅ KAZANAN (W2)", "❌ KAYBEDEN (W1)"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 SIMULASYON":
        st.title("📈 Projeksiyon")
        h_oran = st.slider("Haftalık Hedef (%)", 1, 50, 5)
        sure = st.slider("Simülasyon (Gün)", 7, 120, 30)
        df = pd.DataFrame({"Gün": range(sure), "Tahmin ($)": [kasa * ((1 + h_oran/100) ** (d / 7)) for d in range(sure)]})
        st.line_chart(df.set_index("Gün"))

    st.caption(f"OG Core v9.0 | Son Senkronizasyon: {datetime.now().strftime('%H:%M:%S')}")
