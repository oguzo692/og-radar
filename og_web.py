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
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")

# --- KİŞİSEL KASA VERİLERİ ---
og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

# --- RÜTBE VERİLERİ ---
og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "fenerbahçe-gençlerbirliği fenerbahçe gol sayısı ")
aktif_soru_2 = live_vars.get("aktif_soru2", "bitcoin cuma gece 03:00 kapanışı")

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 553))
w3_kar = float(live_vars.get("w3_sonuc", 0)) 
w4_kar = float(live_vars.get("w4_sonuc", 0))
toplam_bahis_kar = w1_kar + w2_kar + w3_kar + w4_kar

wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. YENİ GEÇİCİ TASARIM (CSS) ---
# Resim yerine modern bir gradient ve derinlik ekledim
common_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

/* Ana Arka Plan */
.stApp {
    background: radial-gradient(circle at top right, #0a0a0a, #030303) !important;
}

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
[data-testid="stSidebar"] svg, [data-testid="stHeaderActionElements"], .st-emotion-cache-10trblm {display: none !important;}
[data-testid="stSidebar"] span, [data-testid="stSidebar"] small {font-size: 0 !important; color: transparent !important;}
[data-testid="stSidebar"] p {font-size: 14px !important; color: #d1d1d1 !important; visibility: visible !important;}

section[data-testid="stSidebar"] { 
    background-color: rgba(10, 10, 10, 0.98) !important; 
    border-right: 1px solid rgba(204, 122, 0, 0.2);
}

.stButton button, .stLinkButton a { 
    width: 100% !important; 
    background: linear-gradient(135deg, rgba(204, 122, 0, 0.1), rgba(204, 122, 0, 0.05)) !important; 
    border: 1px solid rgba(204, 122, 0, 0.4) !important; 
    color: #cc7a00 !important; 
    font-family: 'Orbitron' !important; 
    text-transform: uppercase;
    letter-spacing: 1px;
}

body, [data-testid="stAppViewContainer"], p, div, span, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
    color: #e0e0e0 !important;
}

.industrial-card { 
    background: rgba(20, 20, 20, 0.6) !important; 
    backdrop-filter: blur(10px); 
    border: 1px solid rgba(255, 255, 255, 0.05) !important; 
    border-left: 4px solid #cc7a00 !important; 
    padding: 22px; 
    margin-bottom: 20px; 
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

.terminal-header { 
    color: #cc7a00; 
    font-size: 12px; 
    font-weight: 800; 
    letter-spacing: 2px; 
    text-transform: uppercase; 
    margin-bottom: 18px;
}

.highlight { color: #ffffff !important; font-weight: 700; }
.ticker-wrap { background: rgba(204, 122, 0, 0.05); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 12px 0; margin-bottom: 30px;}
.ticker-item { font-size: 13px; color: #cc7a00; font-family: 'Orbitron'; font-weight: bold;}
</style>
"""

login_bg_css = """
<style>
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(15, 15, 15, 0.95) !important;
    padding: 60px 40px !important;
    border-radius: 12px !important;
    border: 1px solid #cc7a00 !important;
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    box-shadow: 0 0 30px rgba(204, 122, 0, 0.2) !important;
}
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
w2_coupon_html = f"<div class='industrial-card' style='border-top: 1px solid #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}</div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top: 1px solid #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}</div>"

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
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; letter-spacing:5px; text-align:center; margin-bottom:40px;'>OG CORE</h1>", unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom:10px; color:#666; font-size:11px; letter-spacing:2px; font-weight:800;'>SİSTEM MODÜLLERİ</div>", unsafe_allow_html=True)
        page = st.radio("Menu", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip"], label_visibility="collapsed")
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
        with k1: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Oguzo Bakiye</div><div class='highlight' style='font-size:20px; color:#cc7a00 !important;'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Ero7 Bakiye</div><div class='highlight' style='font-size:20px; color:#cc7a00 !important;'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Fybey Bakiye</div><div class='highlight' style='font-size:20px; color:#cc7a00 !important;'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        
        st.divider()
        net_kar = kasa - ana_para
        current_pct = max(0, min(100, ((kasa - 600) / (1200 - 600)) * 100))
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>HEDEF YOLCULUĞU ($1.200)</div><div style='background:#111; height:12px; border-radius:10px; border:1px solid #333;'><div style='background:linear-gradient(90deg, #cc7a00, #ffae00); width:{current_pct}%; height:100%; border-radius:10px;'></div></div><div style='text-align:right; font-size:12px; color:#cc7a00; margin-top:8px; font-weight:bold;'>%{current_pct:.1f} Tamamlandı</div></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>💎 KASA DURUMU</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>KAR/ZARAR</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'}; font-size:22px; font-weight:bold;'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                eth = yf.Ticker("ETH-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>⚡ CANLI PİYASA</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div><div class='terminal-row'><span>ETHEREUM</span><span class='highlight'>${eth:,.0f}</span></div></div>", unsafe_allow_html=True)
            except: st.write("Veri bekleniyor...")
        with col3: st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>📊 PERFORMANS</div><div style='text-align:center; padding-top:20px;'><span style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</span><br><small style='color:#666;'>WIN RATE</small></div></div>", unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 RÜTBE SIRALAMASI</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>oguzo</div><div class='highlight' style='font-size:24px;'>{og_p} P</div><div style='color:#cc7a00;'>{rutbe_getir(og_p)}</div></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>ero7</div><div class='highlight' style='font-size:24px;'>{er_p} P</div><div style='color:#cc7a00;'>{rutbe_getir(er_p)}</div></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>fybey</div><div class='highlight' style='font-size:24px;'>{fy_p} P</div><div style='color:#cc7a00;'>{rutbe_getir(fy_p)}</div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 TOPLAM NET KAZANÇ</div><div style='color:#00ff41; font-size:42px; font-family:Orbitron; font-weight:900;'>${toplam_bahis_kar:,.2f}</div></div>", unsafe_allow_html=True)
        t4, t1, t2, t3 = st.tabs(["🆕 HAFTALIK", "⏳ BEKLEYENLER", "✅ GEÇMİŞ WINS", "❌ KAYIPLAR"])
        with t4: st.markdown(w4_coupon_html, unsafe_allow_html=True)
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 Portföy Takip":
        st.markdown("<div class='terminal-header'>🏛️ VARLIK YÖNETİM MERKEZİ</div>", unsafe_allow_html=True)
        try:
            usd_try = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]
            ons_gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            gram_altin = (ons_gold / 31.1035) * usd_try
            ceyrek_fiyat = gram_altin * 1.82 
            
            users = ["oguzo", "ero7", "fybey"]
            display_data = []
            for u in users:
                u_usd = float(live_vars.get(f"{u}_usd", 0))
                u_gr = float(live_vars.get(f"{u}_altin", 0))
                u_cy = float(live_vars.get(f"{u}_ceyrek", 0))
                t_usd = u_usd + (u_gr * gram_altin / usd_try) + (u_cy * ceyrek_fiyat / usd_try)
                display_data.append({"Kullanıcı": u.upper(), "USD": u_usd, "Gram": u_gr, "Çeyrek": u_cy, "TOPLAM_USD": t_usd})
            df_portfoy = pd.DataFrame(display_data)

            secilen_user = st.selectbox("Detaylı Görünüm:", ["OGUZO", "ERO7", "FYBEY"])
            u_row = df_portfoy[df_portfoy["Kullanıcı"] == secilen_user]
            total_val = u_row["TOPLAM_USD"].values[0]
            
            st.markdown(f"""
                <div class='industrial-card' style='text-align:center;'>
                    <div style='font-size:12px; color:#666;'>TOTAL PORTFOLIO VALUE</div>
                    <div style='font-size:60px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>${total_val:,.2f}</div>
                    <div style='font-size:20px; color:#555;'>≈ ₺{(total_val * usd_try):,.0f}</div>
                </div>
            """, unsafe_allow_html=True)
        except: st.error("Piyasa verilerine erişilemiyor.")

    st.markdown(f"<div style='text-align:center; color:#333; font-size:10px; margin-top:50px; letter-spacing:3px;'>OG CORE TERMINAL // {datetime.now().year}</div>", unsafe_allow_html=True)
