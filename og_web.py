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
w6_kar = float(live_vars.get("w6_sonuc", -100))
w7_kar = float(live_vars.get("w7_sonuc", +650))
w8_kar = float(live_vars.get("w8_sonuc", -100))
toplam_bahis_kar = w1_kar + w2_kar + w3_kar + w4_kar + w5_kar + w6_kar + w7_kar + w8_kar

wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS STİLLERİ ---
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

.industrial-card { 
    background: rgba(15, 15, 15, 0.8) !important; 
    backdrop-filter: blur(5px); 
    border: 1px solid rgba(255, 255, 255, 0.03) !important; 
    border-top: 2px solid rgba(204, 122, 0, 0.4) !important; 
    padding: 22px; 
    margin-bottom: 20px; 
    border-radius: 4px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5); 
    transition: all 0.3s ease;
}

.industrial-card:hover { 
    transform: translateY(-5px); 
    border-top-color: #ffae00 !important;
    background: rgba(25, 25, 25, 0.9) !important;
    box-shadow: 0 8px 25px rgba(204, 122, 0, 0.15);
}

.terminal-header { color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px;}
.highlight { color: #FFFFFF !important; font-weight: 400; font-size: 14px; font-family: 'JetBrains Mono', monospace; }
.val-std { font-size: 22px !important; font-weight: 800 !important; font-family: 'Orbitron'; }
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; margin-bottom: 25px;}
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
.ticker-item { font-size: 12px; color: #cc7a00; letter-spacing: 4px; padding-right: 50%; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
.equal-card { min-height: 180px; display: flex; flex-direction: column; justify-content: space-between; }
</style>
"""

login_bg_css = """
<style>
.stApp {
    background: radial-gradient(circle at 20% 30%, rgba(204,122,0,0.15), transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(0,255,65,0.10), transparent 40%),
                linear-gradient(135deg, #050505 0%, #0b0b0b 40%, #111111 100%) !important;
    background-attachment: fixed !important;
}
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(10, 10, 10, 0.75) !important;
    backdrop-filter: blur(30px) !important;
    padding: 55px 35px !important;
    border-radius: 18px !important;
    border: 1px solid rgba(204, 122, 0, 0.35) !important;
    box-shadow: 0 0 40px rgba(204,122,0,0.15);
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    z-index: 9999 !important;
    width: 360px !important;
}
input[type="password"] {
    background: rgba(0, 0, 0, 0.5) !important;
    border: 1px solid rgba(204, 122, 0, 0.6) !important;
    text-align: center !important;
    color: #cc7a00 !important;
    font-size: 26px !important;
    letter-spacing: 12px !important;
    padding: 12px !important;
    border-radius: 10px !important;
}
.stButton { visibility: hidden; height: 0; margin: 0; padding: 0; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w8_matches = """<div class='terminal-row'><span>gala - başakşehir</span><span class='highlight'>gala 1x & +2</span></div><div class='terminal-row'><span>bvb - augsburg</span><span class='highlight'>bvb +2 & iy +1</span></div><div class='terminal-row'><span>chelsea - newcastle</span><span class='highlight'>kg</span></div><div class='terminal-row'><span>liverpool - spurs</span><span class='highlight'>+3</span></div><div class='terminal-row'><span>karagümrük - fenerbahçe</span><span class='highlight'>fenerbahçe w & +2 </span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 7.59</span><span>Tutar: 100 USD</span></div>"""
w7_matches = """<div class='terminal-row'><span>beşiktaş - gala</span><span class='highlight'>gala +1 ✅</span></div><div class='terminal-row'><span>köln - bvb</span><span class='highlight'>bvb +2 ✅</span></div><div class='terminal-row'><span>newcastle - manchester united</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>wolwes - liverpool</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>fenerbahçe - samsunspor</span><span class='highlight'>fenerbahçe w & +2 ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 6.50</span><span>Tutar: 100 USD</span></div>"""
w6_matches = """<div class='terminal-row'><span>gala - alanyasapor</span><span class='highlight'>gala w & +2 ✅</span></div><div class='terminal-row'><span>bvb - bayern</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>newcastle - everton</span><span class='highlight'>newcastle +2 ✅</span></div><div class='terminal-row'><span>liverpool - west ham</span><span class='highlight'>live w & 2+ ✅</span></div><div class='terminal-row'><span>antalyasapor - fenerbahçe </span><span class='highlight'>fenerbahçe w & iy +1 & +2 ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 8.89</span><span>Tutar: 100 USD</span></div>"""
w5_matches = """<div class='terminal-row'><span>konyaspor - gala</span><span class='highlight'>gala w & +2 ❌</span></div><div class='terminal-row'><span>leipzig - bvb</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>man city - newcastle</span><span class='highlight'>x1 & +2 ✅</span></div><div class='terminal-row'><span>forest - liverpool</span><span class='highlight'>live 2+ ❌</span></div><div class='terminal-row'><span>fenerbahçe - kasımpaşa</span><span class='highlight'>fenerbahçe w & iy +1 & +2 ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 8.26</span><span>Tutar: 100 USD</span></div>"""
w4_matches = """<div class='terminal-row'><span>gala - eyüpspor</span><span class='highlight'>gala w & 2+ ✅</span></div><div class='terminal-row'><span>sunderland - liverpool</span><span class='highlight'>kg ❌</span></div><div class='terminal-row'><span>bvb - mainz 05</span><span class='highlight'>bvb 1x & bvb 2+ & iy +1 ✅</span></div><div class='terminal-row'><span>trabzonspor - fenerbahçe</span><span class='highlight'>fb 2+ ✅</span></div><div class='terminal-row'><span>spurs - newcastle</span><span class='highlight'>kg ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 11.00</span><span>Tutar: 100 USD</span></div>"""
w3_matches = """<div class='terminal-row'><span>wolfsburg - bvb</span><span class='highlight'>bvb x2 & +2 ✅</span></div><div class='terminal-row'><span>newcastle - brentford</span><span class='highlight'>newcastle +2 ✅</span></div><div class='terminal-row'><span>rizespor - gala</span><span class='highlight'>gala w & +2 ✅</span></div><div class='terminal-row'><span>liverpool - man city</span><span class='highlight'>lıve +1 ✅</span></div><div class='terminal-row'><span>fenerbahçe - gençlerbirliği</span><span class='highlight'>fenerbahçe w & +3 ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>gala - kayserispor</span><span style='color:#00ff41;'>gala w & iy +1 & 2+ ✅</span></div><div class='terminal-row'><span>liverpool - newcastle</span><span style='color:#00ff41;'>+2 & liverpool 1x ✅</span></div><div class='terminal-row'><span>bvb - heidenheim</span><span style='color:#00ff41;'>bvb w & iy +1 & 2+ ✅</span></div><div class='terminal-row'><span>kocaelispor - fenerbahçe</span><span style='color:#00ff41;'>fenerbahçe w & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>karagümrük - gala</span><span style='color:#ff4b4b;'>gala w & +2 ✅</span></div><div class='terminal-row'><span>bournemouth - liverpool</span><span style='color:#00ff41;'>kg ✅</span></div><div class='terminal-row'><span>union berlin - bvb</span><span style='color:#00ff41;'>iy +1 ✅</span></div><div class='terminal-row'><span>newcastle - aston villa</span><span style='color:#ff4b4b;'>newcastle +2 ❌</span></div><div class='terminal-row'><span>fenerbahçe - göztepe</span><span style='color:#ff4b4b;'>fenerbahçe w ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""

w8_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>⏳ W8 KUPONU (BEKLİYOR)</div>{w8_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇ BEKLENİYOR ⏳</span></div>"
w7_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W7 KUPONU (BAŞARILI)</div>{w7_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w6_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>❌ W6 KUPONU (BAŞARISIZ)</div>{w6_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ❌</span></div>"
w5_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>❌ W5 KUPONU (BAŞARISIZ)</div>{w5_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ❌</span></div>"
w4_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>❌ W4 KUPONU (BAŞARISIZ)</div>{w4_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ❌</span></div>"
w3_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W3 KUPONU (BAŞARILI)</div>{w3_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}<span style='color:#ff4b4b; font-weight:bold;'>SONUÇLANDI ❌</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        pwd = st.text_input("PIN", type="password", placeholder="----", label_visibility="collapsed")
        if pwd:
            if pwd == "1608":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("ACCESS DENIED")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    st.markdown("<style>.stApp { background: #030303 !important; background-image: none !important; }</style>", unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; letter-spacing:5px; text-align:center; margin-bottom:40px;'>OG CORE</h1>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:10px; color:#666; font-size:11px; letter-spacing:2px; font-weight:800;'>SİSTEM MODÜLLERİ</div>", unsafe_allow_html=True)
        page = st.radio("Menu", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip", "💠 FTMO"], label_visibility="collapsed")
        st.divider()
        st.markdown("<div style='color:#666; font-size:11px; letter-spacing:2px; font-weight:800; margin-bottom:15px;'>📂 TERMİNAL ERİŞİMİ</div>", unsafe_allow_html=True)
        admin_pwd = st.text_input("PIN", type="password", placeholder="Admin PIN", label_visibility="collapsed")
        if admin_pwd == "0644":
            st.markdown("<a href='https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit' target='_blank' style='text-decoration:none;'><div style='background:rgba(204, 122, 0, 0.2); border: 1px solid #cc7a00; color:#cc7a00; text-align:center; padding:10px; border-radius:4px; font-family:Orbitron; font-size:12px; font-weight:bold;'>VERİ TABANINA BAĞLAN</div></a>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("SİSTEMDEN ÇIK"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 Kişisel Kasa Dağılımı</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Oguzo Bakiye</div><div class='highlight'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Ero7 Bakiye</div><div class='highlight'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Fybey Bakiye</div><div class='highlight'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        st.divider()
        net_kar = kasa - ana_para
        current_pct = max(0, min(100, ((kasa - 600) / (1200 - 600)) * 100))
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>HEDEF YOLCULUĞU ($1.200)</div><div style='background:#111; height:8px; border-radius:10px;'><div style='background:linear-gradient(90deg, #cc7a00, #ffae00); width:{current_pct}%; height:100%; border-radius:10px;'></div></div><div style='text-align:right; font-size:10px; color:#555; margin-top:5px;'>%{current_pct:.1f}</div></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>💎 KASA</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>K/Z</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                eth = yf.Ticker("ETH-USD").history(period="1d")['Close'].iloc[-1]
                sol = yf.Ticker("SOL-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"""<div class='industrial-card' style='height:230px;'><div class='terminal-header'>⚡ PİYASA</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div><div class='terminal-row'><span>ETHEREUM</span><span style='color:#cc7a00;'>${eth:,.0f}</span></div><div class='terminal-row'><span>SOLANA</span><span style='color:#cc7a00;'>${sol:,.2f}</span></div></div>""", unsafe_allow_html=True)
            except: st.write("Piyasa verisi bekleniyor...")
        with col3: st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>📊 Win Rate</div><div style='text-align:center;'><span style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</span></div></div>", unsafe_allow_html=True)
        st.markdown("### 📜 SON İŞLEMLER")
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>AKTİVİTE LOGLARI</div><p style='font-family:JetBrains Mono; color:#888;'>{son_islemler_raw}</p></div>", unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 SIRALAMA</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='industrial-card' style='padding:15px; text-align:center; border-top: 2px solid #cc7a00;'><div style='font-size:11px; color:#666;'>oguzo</div><div class='highlight'>{og_p} P</div><div style='font-size:12px;'>{rutbe_getir(og_p)}</div></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='industrial-card' style='padding:15px; text-align:center; border-top: 2px solid #cc7a00;'><div style='font-size:11px; color:#666;'>ero7</div><div class='highlight'>{er_p} P</div><div style='font-size:12px;'>{rutbe_getir(er_p)}</div></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='industrial-card' style='padding:15px; text-align:center; border-top: 2px solid #cc7a00;'><div style='font-size:11px; color:#666;'>fybey</div><div class='highlight'>{fy_p} P</div><div style='font-size:12px;'>{rutbe_getir(fy_p)}</div></div>", unsafe_allow_html=True)
        st.divider()
        q_col1, q_col2 = st.columns(2)
        base_url = "https://script.google.com/macros/s/AKfycbz0cvMHSrHchkksvFCixr9NDnMsvfLQ6T_K2jsXfohgs7eFXP5x-wxTX_YQej1EZhSX/exec"
        with q_col1:
            st.markdown(f"<div class='industrial-card equal-card'><div class='terminal-header'>📢 AKTİF SORU 1</div><h3 style='color:white; margin:0;'>{aktif_soru_1}</h3></div>", unsafe_allow_html=True)
            u_name_1 = st.selectbox("İsim (Soru 1)", ["oguzo", "ero7", "fybey"], key="n1")
            u_vote_1 = st.radio("Tahmin (Soru 1)", ["-","-", "-","-","-"], key="v1")
            final_link_1 = f"{base_url}?isim={u_name_1}&tahmin={u_vote_1}&soru=1"
            st.markdown(f"""<a href='{final_link_1}' target='_blank' style='text-decoration:none;'><div style='background:rgba(204, 122, 0, 0.2); border: 1px solid #cc7a00; color:#cc7a00; text-align:center; padding:15px; border-radius:5px; font-family:Orbitron; font-weight:bold; cursor:pointer;'>1. OYU ONAYLA</div></a>""", unsafe_allow_html=True)
        with q_col2:
            st.markdown(f"<div class='industrial-card equal-card'><div class='terminal-header'>📢 AKTİF SORU 2</div><h3 style='color:white; margin:0;'>{aktif_soru_2}</h3></div>", unsafe_allow_html=True)
            u_name_2 = st.selectbox("İsim (Soru 2)", ["oguzo", "ero7", "fybey"], key="n2")
            u_vote_2 = st.radio("Tahmin (Soru 2)", ["-", "-", "-", "-", "-"], key="v2")
            final_link_2 = f"{base_url}?isim={u_name_2}&tahmin={u_vote_2}&soru=2"
            st.markdown(f"""<a href='{final_link_2}' target='_blank' style='text-decoration:none;'><div style='background:rgba(204, 122, 0, 0.2); border: 1px solid #cc7a00; color:#cc7a00; text-align:center; padding:15px; border-radius:5px; font-family:Orbitron; font-weight:bold; cursor:pointer;'>2. OYU ONAYLA</div></a>""", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 PERFORMANS</div><div class='terminal-row'><span>NET:</span><span style='color:#00ff41; font-size:32px; font-family:Orbitron;'>${toplam_bahis_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        t8, t7, t6, t5, t4, t1, t2, t3 = st.tabs(["⏳ W8", "✅ W7", "❌ W6", "❌ W5", "❌ W4", "✅ W3", "✅ W2", "❌ W1"])

        with t8: st.markdown(w8_coupon_html, unsafe_allow_html=True)
        with t7: st.markdown(w7_coupon_html, unsafe_allow_html=True)
        with t6: st.markdown(w6_coupon_html, unsafe_allow_html=True)
        with t5: st.markdown(w5_coupon_html, unsafe_allow_html=True)
        with t4: st.markdown(w4_coupon_html, unsafe_allow_html=True)
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 Portföy Takip":
    import requests
    from datetime import datetime, timedelta

    st.markdown("<div class='terminal-header'>🏛️ PORTFÖY KOMUTA MERKEZİ</div>", unsafe_allow_html=True)

    @st.cache_data(ttl=1800)
    def get_tefas_fund_price(fund_code="AFT"):
        """
        TEFAS'tan fonun son fiyatını çeker.
        Dönen değer: float fiyat (TL)
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=10)

            url = "https://www.tefas.gov.tr/api/DB/BindHistoryInfo"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.tefas.gov.tr/"
            }

            data = {
                "fontip": "YAT",
                "bastarih": start_date.strftime("%d.%m.%Y"),
                "bittarih": end_date.strftime("%d.%m.%Y"),
                "fonunvantip": "",
                "sfontur": "",
                "fonkod": fund_code
            }

            r = requests.post(url, headers=headers, data=data, timeout=15)
            r.raise_for_status()

            js = r.json()
            items = js.get("data", [])

            if not items:
                return None

            # en güncel kaydı al
            latest = items[-1]

            # TEFAS bazen "price", bazen farklı alan döndürebiliyor, kontrollü okuyalım
            price = latest.get("FIYAT") or latest.get("fiyat") or latest.get("price")

            if price is None:
                return None

            return float(str(price).replace(",", "."))
        except Exception:
            return None

    try:
        usd_try = yf.Ticker("USDTRY=X").history(period="1d")["Close"].iloc[-1]
        ons_gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]
        gram_altin = (ons_gold / 31.1035) * usd_try
        ceyrek_fiyat = gram_altin * 1.74

        aft_price_tl = get_tefas_fund_price("AFT")

        def get_val(key):
            try:
                return float(live_vars.get(key, 0))
            except:
                return 0.0

        users = ["oguzo", "ero7", "fybey"]
        display_data = []

        for u in users:
            u_usd = get_val(f"{u}_usd")
            u_gr = get_val(f"{u}_altin")
            u_cy = get_val(f"{u}_ceyrek")
            u_aft = get_val(f"{u}_aft_adet")  # yeni alan: AFT adet

            aft_total_tl = u_aft * aft_price_tl if aft_price_tl else 0
            aft_total_usd = aft_total_tl / usd_try if usd_try else 0

            t_usd = (
                u_usd
                + (u_gr * gram_altin / usd_try)
                + (u_cy * ceyrek_fiyat / usd_try)
                + aft_total_usd
            )

            display_data.append({
                "Kullanıcı": u.upper(),
                "USD": u_usd,
                "Gram": u_gr,
                "Çeyrek": u_cy,
                "AFT_Adet": u_aft,
                "AFT_Fiyat_TL": aft_price_tl if aft_price_tl else 0,
                "AFT_Toplam_TL": aft_total_tl,
                "TOPLAM_USD": t_usd
            })

        df_portfoy = pd.DataFrame(display_data)

        if not df_portfoy.empty:
            secilen_user = st.selectbox("Kullanıcı Portföy Detayı:", ["OGUZO", "ERO7", "FYBEY"])
            u_row = df_portfoy[df_portfoy["Kullanıcı"] == secilen_user]
            total_val = float(u_row["TOPLAM_USD"].values[0])

            # Dev Kart
            st.markdown(
                f"""
                <div class='industrial-card' style='text-align:center; border-top: 4px solid #cc7a00;'>
                    <div style='font-size:14px; color:#666; letter-spacing:2px;'>TOPLAM PORTFÖY DEĞERİ</div>
                    <div style='font-size:55px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>${total_val:,.2f}</div>
                    <div style='font-size:18px; color:#444;'>≈ ₺{(total_val * usd_try):,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Varlık Dağılımı
            v1, v2, v3, v4 = st.columns(4)

            with v1:
                st.markdown(
                    f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>NAKİT</div><div class='highlight'>${u_row['USD'].values[0]:,.0f}</div></div>",
                    unsafe_allow_html=True
                )

            with v2:
                st.markdown(
                    f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>GRAM ALTIN</div><div class='highlight'>{u_row['Gram'].values[0]} gr</div></div>",
                    unsafe_allow_html=True
                )

            with v3:
                st.markdown(
                    f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>ÇEYREK ADET</div><div class='highlight'>{u_row['Çeyrek'].values[0]:,.0f}</div></div>",
                    unsafe_allow_html=True
                )

            with v4:
                st.markdown(
                    f"""
                    <div class='industrial-card' style='text-align:center;'>
                        <div style='font-size:11px; color:#666;'>AFT</div>
                        <div class='highlight'>{u_row['AFT_Adet'].values[0]:,.2f} adet</div>
                        <div style='font-size:12px; color:#888;'>₺{u_row['AFT_Fiyat_TL'].values[0]:,.4f} / pay</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # AFT detay kartı
            st.markdown(
                f"""
                <div class='industrial-card' style='text-align:center;'>
                    <div style='font-size:12px; color:#666;'>AFT TOPLAM DEĞERİ</div>
                    <div style='font-size:28px; font-weight:800; color:#cc7a00;'>₺{u_row['AFT_Toplam_TL'].values[0]:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # AI ÖNGÖRÜSÜ
            st.divider()
            st.markdown("<div class='terminal-header'>🧠 AI PROJEKSİYONU (HAZİRAN 2026)</div>", unsafe_allow_html=True)

            aylar = ["Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]
            tahminler = [total_val]

            for i in range(1, len(aylar)):
                rastgele_sapma = np.random.uniform(-0.02, 0.02)
                yeni_deger = tahminler[-1] * (1.10 + rastgele_sapma)
                tahminler.append(yeni_deger)

            chart_df = pd.DataFrame({"Varlık ($)": tahminler}, index=aylar)
            c1, c2 = st.columns([1, 2])

            with c1:
                st.write(f"### {secilen_user} Hedef")
                st.markdown(f"<h1 style='color:#00ff41;'>${tahminler[-1]:,.0f}</h1>", unsafe_allow_html=True)
                st.caption("Mevcut gidişatla Haziran 2026 tahmini (Volatilite Dahil)")

            with c2:
                st.area_chart(chart_df, color="#cc7a00")

        # Piyasa Bilgi Bandı
        st.divider()
        p1, p2, p3, p4 = st.columns(4)
        p1.caption(f"USD/TRY: ₺{usd_try:.2f}")
        p2.caption(f"Gram Altın: ₺{gram_altin:.0f}")
        p3.caption(f"Çeyrek Altın: ₺{ceyrek_fiyat:.0f}")
        p4.caption(f"AFT Fiyatı: ₺{aft_price_tl:.4f}" if aft_price_tl else "AFT Fiyatı: Veri alınamadı")

    except Exception as e:
        st.error(f"Piyasa verileri çekilirken bir hata oluştu: {e}")
        
    elif page == "💠 FTMO":
        st.markdown("<div class='terminal-header'>💠 FTMO FON TAKİP SEKMESİ</div>", unsafe_allow_html=True)
        
        # Verileri Google Sheets'ten çek
        bf_balance = float(live_vars.get("bf_balance", 100000))
        bf_equity = float(live_vars.get("bf_equity", 100000))
        bf_daily_loss = float(live_vars.get("bf_daily_loss", 0.0))
        bf_target_pct = float(live_vars.get("bf_target_pct", 10)) / 100
        bf_target_price = bf_balance * (1 + bf_target_pct)
        
        # Üst Metrikler
        m1, m2, m3 = st.columns(3)
        bf_net_pnl = bf_equity - bf_balance 
        bf_pnl_color = "#00ff41" if bf_net_pnl >= 0 else "#ff4b4b"
        
        with m1:
            st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>GÜNCEL EQUITY</div><div class='highlight' style='font-size:24px;'>${bf_equity:,.2f}</div></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: {bf_pnl_color};'><div style='font-size:11px; color:#666;'>NET K/Z</div><div style='color:{bf_pnl_color}; font-size:24px;' class='val-std'>${bf_net_pnl:,.2f}</div></div>", unsafe_allow_html=True)
        with m3:
            bf_limit_pct = (abs(bf_daily_loss) / (bf_balance * 0.05)) * 100 if bf_balance > 0 else 0
            st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: #ff4b4b;'><div style='font-size:11px; color:#666;'>GÜNLÜK LİMİT DOLULUK</div><div class='highlight' style='font-size:24px;'>%{bf_limit_pct:.2f}</div></div>", unsafe_allow_html=True)

        # Hedef Progress Bar
        bf_progress = max(0.0, min(1.0, (bf_equity - bf_balance) / (bf_target_price - bf_balance))) if (bf_target_price - bf_balance) != 0 else 0
        st.markdown(f"""
            <div class='industrial-card'>
                <div class='terminal-header'>🎯 HEDEF YOLCULUĞU (HEDEF: ${bf_target_price:,.0f})</div>
                <div style='background:#111; height:15px; border-radius:10px; border: 1px solid rgba(255,255,255,0.05);'>
                    <div style='background:linear-gradient(90deg, #00ff41, #008f11); width:{bf_progress*100}%; height:100%; border-radius:10px; box-shadow: 0 0 10px rgba(0,255,65,0.3);'></div>
                </div>
                <div style='display:flex; justify-content:space-between; margin-top:10px;'>
                    <span style='font-size:12px; color:#555;'>BAŞLANGIÇ: ${bf_balance:,.0f}</span>
                    <span style='font-size:14px; color:#00ff41; font-weight:bold;'>%{bf_progress*100:.1f} TAMAMLANDI</span>
                    <span style='font-size:12px; color:#555;'>HEDEF: ${bf_target_price:,.0f}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

     # --- HEDEFLER & LİMİTLER (FTMO 100K) ---
        st.markdown("<div class='terminal-header'>🎯 Hedefler & Limitler (100K Hesap)</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Phase 1 hedef</div><div class='highlight'>$10,000 Kazanç</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Phase 1 r</div><div class='highlight'>$250</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Günlük limit</div><div class='highlight'>$5,000 Kayıp</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Phase 2 hedef</div><div class='highlight'>$5,000 Kazanç</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Phase 2 r</div><div class='highlight'>$250</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Toplam limit</div><div class='highlight'>$10,000 Kayıp</div></div>", unsafe_allow_html=True)

        st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG CORE // {datetime.now().year}</div>", unsafe_allow_html=True)
