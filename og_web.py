import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core ✨", 
    page_icon="🌸", 
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
    if p <= 3: return "Tatlı Başlangıç 🎀"
    elif p <= 6: return "Parlayan Yıldız ✨"
    elif p <= 9: return "İkonik Kraliçe 💅"
    elif p <= 11: return "Prenses Modu 👑"
    else: return "Efsanevi Aşko 💖"

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE ✨")

og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "yeni soru hazırlanıyor..")
aktif_soru_2 = live_vars.get("aktif_soru2", "Gram altın bugün haftalık kapanışını 6.900 TL üzerinde mi yapacak?")

w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 453))
toplam_bahis_kar = w1_kar + w2_kar
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. AŞKO KUŞKO CSS STİLLERİ ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Quicksand:wght@300;500;700&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
[data-testid="stSidebarNav"] {display: none !important;}

/* Arka Plan */
.stApp { 
    background: linear-gradient(135deg, #fff5f8 0%, #ffe4ed 100%) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] { 
    background-color: #ffb6c1 !important; 
    border-right: 3px dashed #ff69b4;
    padding-top: 20px; 
    min-width: 340px !important;
}

/* Yazı Tipleri */
body, [data-testid="stAppViewContainer"], p, div, span, button, input, label { 
    font-family: 'Quicksand', sans-serif !important; 
    color: #ff1493 !important;
}

/* Kartlar */
.industrial-card { 
    background: white !important; 
    border: 2px solid #ffc0cb !important; 
    border-top: 5px solid #ff69b4 !important; 
    padding: 22px; 
    margin-bottom: 20px; 
    border-radius: 20px !important;
    box-shadow: 0 8px 15px rgba(255, 182, 193, 0.3);
}

.terminal-header { 
    color: #ff69b4; 
    font-family: 'Dancing Script', cursive;
    font-size: 22px; 
    font-weight: 800; 
    margin-bottom: 18px; 
    border-left: 5px solid #ff1493; 
    padding-left: 12px;
}

/* Butonlar */
.stButton button, .stLinkButton a { 
    width: 100% !important; 
    background: #ff69b4 !important; 
    border: none !important; 
    color: white !important; 
    font-family: 'Quicksand' !important; 
    padding: 12px !important; 
    border-radius: 30px !important;
    font-weight: bold !important;
    box-shadow: 0 4px 10px rgba(255, 105, 180, 0.3);
}

.stButton button:hover {
    background: #ff1493 !important;
    transform: scale(1.02);
}

/* Ticker */
.ticker-wrap { 
    width: 100%; 
    overflow: hidden; 
    background: #ff69b4; 
    border-bottom: 3px solid #ff1493; 
    padding: 10px 0; 
    margin-bottom: 25px;
}
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
.ticker-item { font-size: 14px; color: white; font-weight: bold; letter-spacing: 2px; padding-right: 50%; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

.highlight { color: #ff1493 !important; font-weight: bold; font-size: 16px; }
.val-std { font-size: 26px !important; font-weight: 800 !important; font-family: 'Dancing Script'; color: #ff69b4 !important; }

/* Tabs Özelleştirme */
.stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
.stTabs [data-baseweb="tab"] { color: #ff69b4 !important; font-weight: bold !important; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - GS</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Liverpool - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: #ffe4ed; margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>GS - Kayserispor</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Liverpool - Newcastle</span><span style='color:#00ff41;'>+2 & Liverpool 1X ✅</span></div><div class='terminal-row'><span>BVB - Heidenheim</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Kocaelispor - FB</span><span style='color:#00ff41;'>FB W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: #ffe4ed; margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Karagümrük - GS</span><span style='color:#ff4b4b;'>GS W & +2 ✅</span></div><div class='terminal-row'><span>Bournemouth - Liverpool</span><span style='color:#00ff41;'>KG VAR ✅</span></div><div class='terminal-row'><span>Union Berlin - BVB</span><span style='color:#00ff41;'>BVB İY 0.5 Üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>New +2 ❌</span></div><div class='terminal-row'><span>FB - Göztepe</span><span style='color:#ff4b4b;'>FB W ❌</span></div><hr style='border: 0; height: 1px; background: #ffe4ed; margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""
w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🌸 W3 KUPONU (AKTİF)</div>{w3_matches}<span style='color:#ff69b4; font-weight:bold;'>BEKLENİYOR ✨</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (MÜKEMMEL)</div>{w2_matches}<span style='color:#00ff41; font-weight:bold;'>BAŞARDIK TATLIM ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (ÜZDÜ)</div>{w1_matches}<span style='color:#ff4b4b; font-weight:bold;'>NAZAR DEĞDİ ❌</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False
def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; margin-top:10vh;">', unsafe_allow_html=True)
        st.markdown('<h1 style="font-family:\'Dancing Script\', cursive; font-size:80px; color:#ff69b4; text-shadow: 2px 2px #ffc0cb;">Og Core ✨</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:20px; color:#ff1493;">Hoş geldin aşkısı, şifreni girer misin? ✨💖</p>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1,1,1])
        with col_b:
            pwd = st.text_input("şifre", type="password", placeholder="Şifren buraya tatlım.. ✨", label_visibility="collapsed")
            if st.button("Sisteme Gir ✨"):
                if pwd == "1608": 
                    st.session_state["password_correct"] = True
                    st.rerun()
                else: st.error("Ay şaka mı? Yanlış şifre aşkım.. 💅")
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni} 🌸</span><span class="ticker-item">{duyuru_metni} ✨</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Dancing Script; font-size:35px; text-align:center;'>Og Core ✨</h1>", unsafe_allow_html=True)
        page = st.radio("MENÜ TATLIM", ["💖 PEMBE ATAK", "🌸 FORMLINE", "🎀 CHALLANGE"])
        with st.expander("📂 GİZLİ PANEL"):
            admin_pwd = st.text_input("Giriş Yap", type="password")
            if admin_pwd == "fybey": st.link_button("VERİ TABANI", "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit")
        if st.button("SİSTEMDEN ÇIK 💅"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "💖 PEMBE ATAK":
        st.markdown("<div class='terminal-header'>💕 KİŞİSEL CÜZDANLAR</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        k1.markdown(f"<div class='industrial-card' style='text-align:center;'>Oguzo 🌸<br><span class='highlight'>${og_kasa:,.2f}</span></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='industrial-card' style='text-align:center;'>Ero7 ✨<br><span class='highlight'>${er_kasa:,.2f}</span></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='industrial-card' style='text-align:center;'>Fybey 🎀<br><span class='highlight'>${fy_kasa:,.2f}</span></div>", unsafe_allow_html=True)

        st.divider()

        if kasa < 900: alt, ust, ikon = 600, 900, "🎀"
        elif kasa < 1200: alt, ust, ikon = 900, 1200, "✨"
        else: alt, ust, ikon = 1200, 1800, "👑"
        
        yuzde = min((max(kasa, alt) - alt) / (ust - alt), 1.0) * 100
        bar_html = f"""
        <div class='industrial-card'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div class='terminal-header' style='margin-bottom:0;'>HEDEFİMİZE AZ KALDI {ikon}</div>
                <span style='color:#ff1493; font-weight:bold;'>KASA: ${kasa:,.2f}</span>
            </div>
            <div style='background:#ffe4ed; height:15px; border-radius:10px; margin-top:15px; border:1px solid #ffc0cb;'>
                <div style='background:linear-gradient(90deg, #ffb6c1, #ff69b4); width:{yuzde}%; height:100%; border-radius:10px;'></div>
            </div>
        </div>
        """
        st.markdown(bar_html, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        net_kar = kasa - ana_para
        col1.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>💎 TOPLAM KASA</div><div class='terminal-row'><span>BİSİKLET</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>DURUM</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        try:
            btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
            eth = yf.Ticker("ETH-USD").history(period="1d")['Close'].iloc[-1]
            col2.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>💸 PİYASA TATLIM</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div><div class='terminal-row'><span>ETHEREUM</span><span style='color:#ff69b4;'>${eth:,.0f}</span></div></div>", unsafe_allow_html=True)
        except: col2.write("Yükleniyor aşkım...")
        col3.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>📊 BAŞARI ORANI</div><div style='text-align:center;'><span style='font-size:45px; color:#ff69b4; font-family:Dancing Script;'>%{wr_oran}</span></div></div>", unsafe_allow_html=True)

    elif page == "🎀 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 GÜZELLİK SIRALAMASI</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        s1.markdown(f"<div class='industrial-card'>Oguzo: {og_p}P<br>{rutbe_getir(og_p)}</div>", unsafe_allow_html=True)
        s2.markdown(f"<div class='industrial-card'>Ero7: {er_p}P<br>{rutbe_getir(er_p)}</div>", unsafe_allow_html=True)
        s3.markdown(f"<div class='industrial-card'>Fybey: {fy_p}P<br>{rutbe_getir(fy_p)}</div>", unsafe_allow_html=True)
        
        st.divider()
        q1, q2 = st.columns(2)
        base_url = "https://script.google.com/macros/s/AKfycbz0cvMHSrHchkksvFCixr9NDnMsvfLQ6T_K2jsXfohgs7eFXP5x-wxTX_YQej1EZhSX/exec"
        
        with q1:
            st.markdown(f"<div class='industrial-card' style='min-height:180px;'><div class='terminal-header'>📢 GÜNÜN SORUSU 1</div><h3 style='color:#ff1493;'>{aktif_soru_1}</h3></div>", unsafe_allow_html=True)
            u1 = st.selectbox("İsmin Ne Tatlım?", ["oguzo", "ero7", "fybey"], key="u1")
            v1 = st.radio("Kararın?", ["👍", "👎"], key="v1", horizontal=True)
            st.markdown(f"<a href='{base_url}?isim={u1}&tahmin={v1}&soru=1' target='_blank'><div style='background:#ff69b4; color:white; text-align:center; padding:10px; border-radius:30px; font-weight:bold;'>OYU GÖNDER ✨</div></a>", unsafe_allow_html=True)

        with q2:
            st.markdown(f"<div class='industrial-card' style='min-height:180px;'><div class='terminal-header'>📢 GÜNÜN SORUSU 2</div><h3 style='color:#ff1493;'>{aktif_soru_2}</h3></div>", unsafe_allow_html=True)
            u2 = st.selectbox("İsim Seç Aşkım", ["oguzo", "ero7", "fybey"], key="u2")
            v2 = st.radio("Seçimin?", ["👍", "👎"], key="v2", horizontal=True)
            st.markdown(f"<a href='{base_url}?isim={u2}&tahmin={v2}&soru=2' target='_blank'><div style='background:#ff69b4; color:white; text-align:center; padding:10px; border-radius:30px; font-weight:bold;'>OYU GÖNDER ✨</div></a>", unsafe_allow_html=True)

    elif page == "🌸 FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 TOPLAM KAZANÇ</div><span style='color:#00ff41; font-size:40px; font-family:Dancing Script;'>${toplam_bahis_kar:,.2f}</span></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🌸 GELECEK", "✅ BAŞARILI", "❌ ÜZÜCÜ"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; color:#ffb6c1; font-size:12px; margin-top:50px;'>💖 OG_CORE_SOFT_EDITION // {datetime.now().year} 💖</div>", unsafe_allow_html=True)
