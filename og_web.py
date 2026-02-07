import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

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

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS (YÜKSEK İŞÇİLİK - NEON TERMINAL) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Orbitron:wght@400;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
.stApp { background-color: #030303 !important; }

/* Ana Kart Yapısı */
.industrial-card {
    background: rgba(10, 10, 10, 0.95);
    border: 1px solid rgba(204, 122, 0, 0.2);
    border-radius: 4px;
    padding: 25px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.terminal-header {
    color: #cc7a00;
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 900;
    margin-bottom: 30px;
    font-family: 'Orbitron';
}

/* --- GELİŞMİŞ PROGRESS SİSTEMİ --- */
.og-progress-wrapper {
    position: relative;
    padding: 40px 0 20px 0;
    margin: 20px 0;
}

.og-bar-container {
    height: 14px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 2px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    position: relative;
    box-shadow: inset 0 0 10px #000;
}

/* Izgara Deseni */
.og-bar-container::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 10% 100%;
    z-index: 1;
}

.og-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #804d00 0%, #cc7a00 50%, #ffae00 100%);
    position: relative;
    z-index: 2;
    transition: width 1.5s cubic-bezier(0.19, 1, 0.22, 1);
    box-shadow: 0 0 20px rgba(204, 122, 0, 0.4);
}

/* Tarama Çizgisi Efekti */
.og-bar-fill::after {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    width: 20%;
    animation: scan 2s infinite;
}

@keyframes scan {
    0% { left: -20%; }
    100% { left: 100%; }
}

/* Milestone Cam Paneller */
.ms-panel {
    position: absolute;
    top: -35px;
    transform: translateX(-50%);
    background: rgba(20, 20, 20, 0.8);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 4px 10px;
    border-radius: 3px;
    font-family: 'JetBrains Mono';
    font-size: 10px;
    color: #444;
    transition: all 0.5s;
}

.ms-panel.active {
    border-color: #cc7a00;
    color: #fff;
    box-shadow: 0 0 10px rgba(204, 122, 0, 0.3);
    background: rgba(204, 122, 0, 0.1);
}

.ms-line {
    position: absolute;
    top: 0; bottom: 0;
    width: 1px;
    background: rgba(204, 122, 0, 0.15);
    z-index: 3;
}

.val-display {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
    font-family: 'JetBrains Mono';
    font-size: 11px;
    color: #666;
}

</style>
"""

# --- 4. ANALİZ VE HESAPLAMA ---
start_val = 600
end_val = 1800
# Kasa 600 ise 0%, 1800 ise 100%
current_pct = max(0, min(100, ((kasa - start_val) / (end_val - start_val)) * 100))

# Milestone Pozisyonları (%)
m1_p = ((900 - start_val) / (end_val - start_val)) * 100
m2_p = ((1200 - start_val) / (end_val - start_val)) * 100
m3_p = 100 # 1800 tam sınır

# --- 5. ANA EKRAN ---
st.markdown(custom_css, unsafe_allow_html=True)

# Ticker (Duyuru)
st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

# Sidebar ve Navigasyon (Önceki kodun aynısı kalabilir)
with st.sidebar:
    st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; text-align:center;'>OG CORE</h1>", unsafe_allow_html=True)
    page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE"])

if page == "⚡ ULTRA ATAK":
    # Hedef Barı Bölümü
    bar_html = f"""
    <div class="industrial-card">
        <div class="terminal-header">CORE_OBJECTIVE_TRACKER // LIMIT: $1,800</div>
        
        <div class="og-progress-wrapper">
            <div class="ms-panel {'active' if kasa >= 900 else ''}" style="left: {m1_p}%;">
                PHASE 01: $900
            </div>
            <div class="ms-panel {'active' if kasa >= 1200 else ''}" style="left: {m2_p}%;">
                PHASE 02: $1200
            </div>
            <div class="ms-panel {'active' if kasa >= 1800 else ''}" style="left: {m3_p}%;">
                FINAL: $1800
            </div>
            
            <div class="og-bar-container">
                <div class="ms-line" style="left: {m1_p}%;"></div>
                <div class="ms-line" style="left: {m2_p}%;"></div>
                <div class="og-bar-fill" style="width: {current_pct}%;"></div>
            </div>
        </div>
        
        <div class="val-display">
            <span>BASE_ENTRY: $600.00</span>
            <span style="color:#cc7a00; font-weight:bold;">LIVE_STATUS: ${kasa:,.2f} ({current_pct:.1f}%)</span>
        </div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)

    # Alt Bilgi Kartları
    col1, col2, col3 = st.columns(3)
    net_kar = kasa - ana_para
    with col1:
        st.markdown(f"""<div class='industrial-card'>
            <div class='terminal-header'>💎 TOTAL_EQUITY</div>
            <div class='terminal-row'><span>NET PROFIT</span><span style="color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};" class='val-std'>${net_kar:,.2f}</span></div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        try:
            btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
            st.markdown(f"""<div class='industrial-card'>
                <div class='terminal-header'>⚡ MARKET_FEED</div>
                <div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div>
            </div>""", unsafe_allow_html=True)
        except: st.write("Feed Error")

    with col3:
        st.markdown(f"""<div class='industrial-card'>
            <div class='terminal-header'>📊 ALPHA_RATE</div>
            <div style='text-align:center;'><span class='val-std' style='color:#cc7a00;'>%{wr_oran}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 📜 ACTIVITY_LOG")
    st.markdown(f"<div class='industrial-card'><p style='font-family:JetBrains Mono; color:#888; font-size:12px;'>{son_islemler_raw}</p></div>", unsafe_allow_html=True)

# Geri kalan sayfaları (CHALLANGE vb.) önceki stabil kodunla birleştirebilirsin.
