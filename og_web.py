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
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")

# --- KİŞİSEL KASA VERİLERİ ---
og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

# --- RÜTBE VERİLERİ ---
og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "pazartesi günü çeyrek altın kuyumcu fiyatı ")
aktif_soru_2 = live_vars.get("aktif_soru2", "bitcoin cuma gece 03:00 kapanışı")

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 453))
w3_kar = float(live_vars.get("w3_sonuc", 0)) 
w4_kar = float(live_vars.get("w4_sonuc", 0))
toplam_bahis_kar = w1_kar + w2_kar + w3_kar + w4_kar

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
.industrial-card { background: rgba(15, 15, 15, 0.8) !important; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.03) !important; border-top: 2px solid rgba(204, 122, 0, 0.4) !important; padding: 22px; margin-bottom: 20px; border-radius: 4px;}
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
    background-image: url("https://raw.githubusercontent.com/oguzo692/og-radar/main/arkaplan.jpg") !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(0, 0, 0, 0.6) !important;
    backdrop-filter: blur(25px) !important;
    padding: 50px 30px !important;
    border-radius: 20px !important;
    border: 1px solid rgba(204, 122, 0, 0.3) !important;
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    z-index: 9999 !important;
    width: 340px !important;
}
input[type="password"] {
    background: rgba(0, 0, 0, 0.4) !important;
    border: 1px solid rgba(204, 122, 0, 0.5) !important;
    text-align: center !important;
    color: #cc7a00 !important;
    font-size: 24px !important;
    letter-spacing: 10px !important;
}
.stButton { visibility: hidden; height: 0; margin: 0; padding: 0; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w4_matches = """
<div class='terminal-row'><span>Gala - Eyüpspor</span><span class='highlight'>gala w & 2+</span></div>
<div class='terminal-row'><span>Sunderland - Liverpool</span><span class='highlight'>kg var</span></div>
<div class='terminal-row'><span>Bvb - Mainz 05</span><span class='highlight'>bvb 1x & bvb 2+ & iy +1</span></div>
<div class='terminal-row'><span>Trabzonspor - FB</span><span class='highlight'>fb 2+</span></div>
<div class='terminal-row'><span>Spurs - Newcastle</span><span class='highlight'>kg var</span></div>
<hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'>
<div class='terminal-row'><span>Toplam Oran: 11.00</span><span>Tutar: 100 USD</span></div>
"""

w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst ✅</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst ✅</span></div><div class='terminal-row'><span>Rizespor - GS</span><span class='highlight'>gala w & 1.5 üst ✅</span></div><div class='terminal-row'><span>Liverpool - Man City</span><span class='highlight'>lıve gol atar ✅</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>GS - Kayserispor</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Liverpool - Newcastle</span><span style='color:#00ff41;'>+2 & Liverpool 1X ✅</span></div><div class='terminal-row'><span>BVB - Heidenheim</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Kocaelispor - FB</span><span style='color:#00ff41;'>FB W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Karagümrük - GS</span><span style='color:#ff4b4b;'>GS W & +2 ✅</span></div><div class='terminal-row'><span>Bournemouth - Liverpool</span><span style='color:#00ff41;'>KG VAR ✅</span></div><div class='terminal-row'><span>Union Berlin - BVB</span><span style='color:#00ff41;'>BVB İY 0.5 Üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>New +2 ❌</span></div><div class='terminal-row'><span>FB - Göztepe</span><span style='color:#ff4b4b;'>FB W ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""

w4_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W4 KUPONU (AKTİF)</div>{w4_matches}<span style='color:#cc7a00; font-weight:bold;'>BEKLENİYOR ⏳</span></div>"
w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU (AKTİF)</div>{w3_matches}<span style='color:#cc7a00; font-weight:bold;'>BEKLENİYOR ⏳</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}<span style='color:#ff4b4b; font-weight:bold;'>SONUÇLANDI ❌</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        # YAZI BLOĞU BURADAN KALDIRILDI
        pwd = st.text_input("PIN", type="password", placeholder="****", label_visibility="collapsed")
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
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE"])
        with st.expander("📂 ADMİN"):
            admin_pwd = st.text_input("PANEL ŞİFRESİ", type="password")
            if admin_pwd == "0644": st.link_button("Veriler", "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit")
        if st.button("Çıkış"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 KİŞİSEL KASA DAĞILIMI</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Oguzo Bakiye</div><div class='highlight'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Ero7 Bakiye</div><div class='highlight'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Fybey Bakiye</div><div class='highlight'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        
        st.divider()
        
        net_kar = kasa - ana_para
        current_pct = max(0, min(100, ((kasa - 600) / (6500 - 600)) * 100))
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>HEDEF YOLCULUĞU ($6,500)</div><div style='background:#111; height:8px; border-radius:10px;'><div style='background:linear-gradient(90deg, #cc7a00, #ffae00); width:{current_pct}%; height:100%; border-radius:10px;'></div></div><div style='text-align:right; font-size:10px; color:#555; margin-top:5px;'>%{current_pct:.1f}</div></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>💎 KASA</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>K/Z</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                eth = yf.Ticker("ETH-USD").history(period="1d")['Close'].iloc[-1]
                sol = yf.Ticker("SOL-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"""<div class='industrial-card' style='height:230px;'><div class='terminal-header'>⚡ PİYASA</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div><div class='terminal-row'><span>ETHEREUM</span><span style='color:#cc7a00;'>${eth:,.0f}</span></div><div class='terminal-row'><span>SOLANA</span><span style='color:#cc7a00;'>${sol:,.2f}</span></div></div>""", unsafe_allow_html=True)
            except: st.write("Piyasa verisi bekleniyor...")
        with col3: st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>📊 WİN RATE</div><div style='text-align:center;'><span style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</span></div></div>", unsafe_allow_html=True)
        
        st.markdown("### 📜 SON İŞLEMLER")
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>AKTİVİTE LOGLARI</div><p style='font-family:JetBrains Mono; color:#888;'>{son_islemler_raw}</p></div>", unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 GÜNCEL RÜTBE SIRALAMASI</div>", unsafe_allow_html=True)
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
            u_vote_1 = st.radio("Tahmin (Soru 1)", ["12.2k-12.4k", "12.4k-12.46","12.6k-12.8k", "12.8k-13k","+13k"], key="v1")
            final_link_1 = f"{base_url}?isim={u_name_1}&tahmin={u_vote_1}&soru=1"
            st.markdown(f"""<a href='{final_link_1}' target='_blank' style='text-decoration:none;'><div style='background:rgba(204, 122, 0, 0.2); border: 1px solid #cc7a00; color:#cc7a00; text-align:center; padding:15px; border-radius:5px; font-family:Orbitron; font-weight:bold; cursor:pointer;'>1. OYU ONAYLA</div></a>""", unsafe_allow_html=True)
        with q_col2:
            st.markdown(f"<div class='industrial-card equal-card'><div class='terminal-header'>📢 AKTİF SORU 2</div><h3 style='color:white; margin:0;'>{aktif_soru_2}</h3></div>", unsafe_allow_html=True)
            u_name_2 = st.selectbox("İsim (Soru 2)", ["oguzo", "ero7", "fybey"], key="n2")
            u_vote_2 = st.radio("Tahmin (Soru 2)", ["👍", "👎"], key="v2")
            final_link_2 = f"{base_url}?isim={u_name_2}&tahmin={u_vote_2}&soru=2"
            st.markdown(f"""<a href='{final_link_2}' target='_blank' style='text-decoration:none;'><div style='background:rgba(204, 122, 0, 0.2); border: 1px solid #cc7a00; color:#cc7a00; text-align:center; padding:15px; border-radius:5px; font-family:Orbitron; font-weight:bold; cursor:pointer;'>2. OYU ONAYLA</div></a>""", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 PERFORMANS</div><div class='terminal-row'><span>NET:</span><span style='color:#00ff41; font-size:32px; font-family:Orbitron;'>${toplam_bahis_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        t4, t1, t2, t3 = st.tabs(["🆕 W4", "⏳ W3", "✅ W2", "❌ W1"])
        with t4: st.markdown(w4_coupon_html, unsafe_allow_html=True)
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG_CORE_V9.9 // {datetime.now().year}</div>", unsafe_allow_html=True)
