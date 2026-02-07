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
        data = dict(zip(df['key'].astype(str).str.strip(), df['value'].astype(str).str.strip()))
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

def safe_float(val, default=0.0):
    try: 
        return float(str(val).replace(',', '.'))
    except: 
        return default

# Değişkenleri Hazırlama
kasa = safe_float(live_vars.get("kasa", 600))
ana_para = safe_float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")

og_kasa = safe_float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = safe_float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = safe_float(live_vars.get("fybey_kasa", kasa / 3))

og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "Soru bekleniyor...")
aktif_soru_2 = live_vars.get("aktif_soru2", "Soru bekleniyor...")

w1_kar = safe_float(live_vars.get("w1_sonuc", 0)) 
w2_kar = safe_float(live_vars.get("w2_sonuc", 0))
toplam_bahis_kar = w1_kar + w2_kar

wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS STİLLERİ (F-String Kaçışları Yapıldı) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}

.stApp { 
    background-color: #030303 !important; 
    background-image: radial-gradient(circle at 50% 50%, rgba(204, 122, 0, 0.07) 0%, transparent 70%);
}

.login-card {
    background: rgba(10, 10, 10, 0.9);
    border: 1px solid rgba(204, 122, 0, 0.2);
    border-radius: 8px;
    padding: 40px;
    border-top: 3px solid #cc7a00;
}

section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid rgba(204, 122, 0, 0.15); }

.stButton button { width: 100% !important; background: rgba(204, 122, 0, 0.1) !important; border: 1px solid rgba(204, 122, 0, 0.3) !important; color: #cc7a00 !important; font-family: 'Orbitron' !important; }

body, [data-testid="stAppViewContainer"], p, div, span { font-family: 'JetBrains Mono', monospace !important; color: #d1d1d1 !important;}

.industrial-card { 
    background: linear-gradient(145deg, rgba(15, 15, 15, 0.9), rgba(5, 5, 5, 1)) !important; 
    border: 1px solid rgba(255, 255, 255, 0.03) !important; 
    border-top: 2px solid rgba(204, 122, 0, 0.4) !important; 
    padding: 22px; 
    margin-bottom: 20px; 
    border-radius: 4px;
}

.terminal-header { color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px;}
.terminal-row { display: flex; justify-content: space-between; align-items: center; font-size: 14px; margin-bottom: 12px; }
.highlight { color: #FFFFFF !important; }
.val-std { font-size: 22px !important; font-weight: 800 !important; font-family: 'Orbitron'; }

/* Ticker Animation */
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; margin-bottom: 25px;}
.ticker { display: flex; white-space: nowrap; animation: ticker_move 30s linear infinite; }
.ticker-item { font-size: 12px; color: #cc7a00; letter-spacing: 4px; padding-right: 50px; }
@keyframes ticker_move {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

/* PROGRESS BAR */
.prog-container {
    background: rgba(0, 0, 0, 0.6);
    border: 1px solid rgba(204, 122, 0, 0.2);
    height: 40px;
    border-radius: 4px;
    position: relative;
    margin-top: 30px;
}
.prog-fill {
    height: 100%;
    background: linear-gradient(90deg, #995c00, #ffae00);
    box-shadow: 0 0 15px rgba(204, 122, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
}
.ms-marker { position: absolute; top: -5px; width: 2px; height: 50px; background: rgba(204, 122, 0, 0.4); }
.ms-text { position: absolute; top: -25px; transform: translateX(-50%); font-size: 10px; font-family: 'Orbitron'; font-weight: bold; }
</style>
"""

# --- 4. KUPON ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - GS</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Liverpool - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>GS - Kayserispor</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Liverpool - Newcastle</span><span style='color:#00ff41;'>+2 & Liverpool 1X ✅</span></div><div class='terminal-row'><span>BVB - Heidenheim</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Kocaelispor - FB</span><span style='color:#00ff41;'>FB W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Karagümrük - GS</span><span style='color:#ff4b4b;'>GS W & +2 ✅</span></div><div class='terminal-row'><span>Bournemouth - Liverpool</span><span style='color:#00ff41;'>KG VAR ✅</span></div><div class='terminal-row'><span>Union Berlin - BVB</span><span style='color:#00ff41;'>BVB İY 0.5 Üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>New +2 ❌</span></div><div class='terminal-row'><span>FB - Göztepe</span><span style='color:#ff4b4b;'>FB W ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 1.2, 1])
        with col_b:
            st.markdown('<div class="login-card"><div style="text-align: center; margin-bottom: 30px;"><div style="font-size: 10px; color: #666; letter-spacing: 3px;">ENCRYPTED ACCESS</div><div style="font-family: \'Orbitron\'; font-size: 50px; font-weight: 900; color: white; letter-spacing: 12px; margin: 10px 0;">OG CORE</div></div></div>', unsafe_allow_html=True)
            pwd = st.text_input("şifre", type="password", placeholder="••••", label_visibility="collapsed")
            if st.button("SİSTEME GİRİŞ YAP"):
                if pwd == "1608":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("ERİŞİM REDDEDİLDİ")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; text-align:center;'>OG CORE</h1>", unsafe_allow_html=True)
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

        # --- HEDEF BAR HESAPLARI ---
        target = 6500.0
        safe_kasa = max(0.0, kasa)
        current_pct = min(100.0, (safe_kasa / target) * 100)
        m1, m2, m3 = (900/target)*100, (1200/target)*100, (1800/target)*100
        c1 = "#ffae00" if safe_kasa >= 900 else "#444"
        c2 = "#ffae00" if safe_kasa >= 1200 else "#444"
        c3 = "#ffae00" if safe_kasa >= 1800 else "#444"

        target_html = f"""
        <div class='industrial-card'>
            <div class='terminal-header'>HEDEF YOLCULUĞU (${target:,.0f})</div>
            <div class='prog-container'>
                <div class='ms-marker' style='left:{m1}%;'></div>
                <div class='ms-text' style='left:{m1}%; color:{c1};'>$900</div>
                <div class='ms-marker' style='left:{m2}%;'></div>
                <div class='ms-text' style='left:{m2}%; color:{c2};'>$1200</div>
                <div class='ms-marker' style='left:{m3}%;'></div>
                <div class='ms-text' style='left:{m3}%; color:{c3};'>$1800</div>
                <div class='prog-fill' style='width:{current_pct}%;'>
                    <span style='font-size:10px; font-family:Orbitron; color:white; font-weight:bold;'>%{current_pct:.1f}</span>
                </div>
            </div>
        </div>
        """
        st.markdown(target_html, unsafe_allow_html=True)
        
        net_kar = kasa - ana_para
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='industrial-card' style='height:200px;'><div class='terminal-header'>💎 KASA</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>K/Z</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card' style='height:200px;'><div class='terminal-header'>⚡ PİYASA</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div></div>", unsafe_allow_html=True)
            except: st.write("Piyasa Hatası")
        with col3: st.markdown(f"<div class='industrial-card' style='height:200px;'><div class='terminal-header'>📊 WİN RATE</div><div style='text-align:center;'><span style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</span></div></div>", unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 RÜTBE SIRALAMASI</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px;'>oguzo</div><div class='highlight'>{og_p} P</div><div>{rutbe_getir(og_p)}</div></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px;'>ero7</div><div class='highlight'>{er_p} P</div><div>{rutbe_getir(er_p)}</div></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px;'>fybey</div><div class='highlight'>{fy_p} P</div><div>{rutbe_getir(fy_p)}</div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 PERFORMANS</div><div class='terminal-row'><span>NET:</span><span style='color:#00ff41; font-size:32px; font-family:Orbitron;'>${toplam_bahis_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["⏳ W3", "✅ W2", "❌ W1"])
        with t1: st.markdown(f"<div class='industrial-card'><div class='terminal-header'>W3 AKTİF</div>{w3_matches}</div>", unsafe_allow_html=True)
        with t2: st.markdown(f"<div class='industrial-card' style='border-top-color:#00ff41;'>{w2_matches}</div>", unsafe_allow_html=True)
        with t3: st.markdown(f"<div class='industrial-card' style='border-top-color:#ff4b4b;'>{w1_matches}</div>", unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG_CORE_V9.9 // {datetime.now().year}</div>", unsafe_allow_html=True)
