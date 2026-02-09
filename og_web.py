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

# --- GLOBAL YARDIMCI FONKSİYONLAR ---
live_vars = get_live_data()

def get_val(key_name): 
    try: return float(live_vars.get(key_name, 0))
    except: return 0.0

def rutbe_getir(puan_str):
    try:
        p = int(float(puan_str))
    except: p = 0
    if p <= 3: return "Hılez"
    elif p <= 6: return "Tecrübeli Hılez"
    elif p <= 9: return "Bu Abi Biri Mi?"
    elif p <= 11: return "Miço"
    else: return "Grand Miço"

# --- DEĞİŞKENLER (FULL LİSTE) ---
kasa = get_val("kasa") if get_val("kasa") > 0 else 600.0
ana_para = get_val("ana_para") if get_val("ana_para") > 0 else 600.0
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")

og_kasa = get_val("oguzo_kasa") if get_val("oguzo_kasa") > 0 else kasa / 3
er_kasa = get_val("ero7_kasa") if get_val("ero7_kasa") > 0 else kasa / 3
fy_kasa = get_val("fybey_kasa") if get_val("fybey_kasa") > 0 else kasa / 3

og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "yeni soru geliyor... ")
aktif_soru_2 = live_vars.get("aktif_soru2", "bitcoin cuma gece 03:00 kapanışı")

w1_kar = get_val("w1_sonuc")
w2_kar = get_val("w2_sonuc")
w3_kar = get_val("w3_sonuc")
w4_kar = get_val("w4_sonuc")
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
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; margin-bottom: 25px;}
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
.ticker-item { font-size: 12px; color: #cc7a00; letter-spacing: 4px; padding-right: 50%; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
</style>
"""

login_bg_css = """
<style>
.stApp { background-image: url("https://raw.githubusercontent.com/oguzo692/og-radar/main/arkaplan.jpg") !important; background-size: cover !important; background-position: center !important; background-attachment: fixed !important;}
div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) { background: rgba(0, 0, 0, 0.6) !important; backdrop-filter: blur(25px) !important; padding: 50px 30px !important; border-radius: 20px !important; border: 1px solid rgba(204, 122, 0, 0.3) !important; position: fixed !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%) !important; z-index: 9999 !important; width: 340px !important;}
input[type="password"] { background: rgba(0, 0, 0, 0.4) !important; border: 1px solid rgba(204, 122, 0, 0.5) !important; text-align: center !important; color: #cc7a00 !important; font-size: 24px !important; letter-spacing: 10px !important;}
.stButton { visibility: hidden; height: 0; margin: 0; padding: 0; }
</style>
"""

# --- 4. KUPON ŞABLONLARI (KAYIPSIZ) ---
w4_matches = "<div class='terminal-row'><span>Gala - Eyüpspor</span><span class='highlight'>gala w & 2+</span></div><div class='terminal-row'><span>Sunderland - Liverpool</span><span class='highlight'>kg var</span></div><div class='terminal-row'><span>Bvb - Mainz 05</span><span class='highlight'>bvb 1x & bvb 2+ & iy +1</span></div><div class='terminal-row'><span>Trabzonspor - FB</span><span class='highlight'>fb 2+</span></div><div class='terminal-row'><span>Spurs - Newcastle</span><span class='highlight'>kg var</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 11.00</span><span>Tutar: 100 USD</span></div>"
w3_matches = "<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst ✅</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst ✅</span></div><div class='terminal-row'><span>Rizespor - GS</span><span class='highlight'>gala w & 1.5 üst ✅</span></div><div class='terminal-row'><span>Liverpool - Man City</span><span class='highlight'>lıve gol atar ✅</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"
w2_matches = "<div class='terminal-row'><span>GS - Kayserispor</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Liverpool - Newcastle</span><span style='color:#00ff41;'>+2 & Liverpool 1X ✅</span></div><div class='terminal-row'><span>BVB - Heidenheim</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Kocaelispor - FB</span><span style='color:#00ff41;'>FB W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"
w1_matches = "<div class='terminal-row'><span>Karagümrük - GS</span><span style='color:#ff4b4b;'>GS W & +2 ✅</span></div><div class='terminal-row'><span>Bournemouth - Liverpool</span><span style='color:#00ff41;'>KG VAR ✅</span></div><div class='terminal-row'><span>Union Berlin - BVB</span><span style='color:#00ff41;'>BVB İY 0.5 Üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>New +2 ❌</span></div><div class='terminal-row'><span>FB - Göztepe</span><span style='color:#ff4b4b;'>FB W ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"

w4_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W4 KUPONU (AKTİF)</div>{w4_matches}<span style='color:#cc7a00; font-weight:bold;'>BEKLENİYOR ⏳</span></div>"
w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>✅ W3 KUPONU (BAŞARILI)</div>{w3_matches}<span style='color:#cc7a00; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}<span style='color:#ff4b4b; font-weight:bold;'>SONUÇLANDI ❌</span></div>"

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
    st.markdown("<style>.stApp { background: #030303 !important; }</style>", unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; text-align:center;'>OG CORE</h1>", unsafe_allow_html=True)
        page = st.radio("Menu", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip"], label_visibility="collapsed")
        st.divider()
        admin_pwd = st.text_input("Admin PIN", type="password", placeholder="Admin PIN", label_visibility="collapsed")
        if admin_pwd == "0644":
            st.markdown("<a href='https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit' target='_blank'><div style='background:rgba(204,122,0,0.2); border:1px solid #cc7a00; color:#cc7a00; text-align:center; padding:10px; border-radius:4px;'>VERİ TABANI</div></a>", unsafe_allow_html=True)
        if st.button("SİSTEMDEN ÇIK"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 Kişisel Kasa Dağılımı</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card'>Oguzo: ${og_kasa:,.2f}</div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card'>Ero7: ${er_kasa:,.2f}</div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card'>Fybey: ${fy_kasa:,.2f}</div>", unsafe_allow_html=True)
        
        net_kar = kasa - ana_para
        current_pct = max(0, min(100, ((kasa - 600) / (1200 - 600)) * 100))
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>HEDEF ($1.200)</div><div style='background:#111; height:8px; border-radius:10px;'><div style='background:linear-gradient(90deg, #cc7a00, #ffae00); width:{current_pct}%; height:100%; border-radius:10px;'></div></div></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown(f"<div class='industrial-card'>KASA: ${kasa:,.2f}<br>K/Z: ${net_kar:,.2f}</div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card'>BTC: ${btc:,.0f}</div>", unsafe_allow_html=True)
            except: st.write("...")
        with col3: st.markdown(f"<div class='industrial-card'>Win Rate: %{wr_oran}</div>", unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 RÜTBE SIRALAMASI</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='industrial-card'>oguzo: {og_p}P<br>{rutbe_getir(og_p)}</div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='industrial-card'>ero7: {er_p}P<br>{rutbe_getir(er_p)}</div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='industrial-card'>fybey: {fy_p}P<br>{rutbe_getir(fy_p)}</div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'>BAHİS NET: ${toplam_bahis_kar:,.2f}</div>", unsafe_allow_html=True)
        t4, t1, t2, t3 = st.tabs(["⏳ W4", "✅ W3", "✅ W2", "❌ W1"])
        with t4: st.markdown(w4_coupon_html, unsafe_allow_html=True)
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 Portföy Takip":
        try:
            usd_try = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]
            ons_gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            gram_altin = (ons_gold / 31.1035) * usd_try
            ceyrek_fiyat = gram_altin * 1.82 

            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f"<div class='industrial-card'>USD: ₺{usd_try:.2f}</div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div class='industrial-card'>GRAM: ₺{gram_altin:.0f}</div>", unsafe_allow_html=True)
            with m3: st.markdown(f"<div class='industrial-card'>ÇEYREK: ₺{ceyrek_fiyat:.0f}</div>", unsafe_allow_html=True)

            users = ["oguzo", "ero7", "fybey"]
            display_data = []
            for u in users:
                u_usd, u_gr, u_cy = get_val(f"{u}_usd"), get_val(f"{u}_altin"), get_val(f"{u}_ceyrek")
                t_usd = u_usd + (u_gr * gram_altin / usd_try) + (u_cy * ceyrek_fiyat / usd_try)
                display_data.append({"Kullanıcı": u.upper(), "USD": u_usd, "Gram": u_gr, "Çeyrek": u_cy, "T_USD": t_usd})
            
            df_portfoy = pd.DataFrame(display_data)
            secilen_user = st.selectbox("Detay Gör:", ["OGUZO", "ERO7", "FYBEY"])
            u_row = df_portfoy[df_portfoy["Kullanıcı"] == secilen_user]
            total_val = u_row["T_USD"].values[0]
            total_tl = total_val * usd_try
            doner = total_tl / (get_val("doner_fiyat") if get_val("doner_fiyat") > 0 else 150.0)

            st.markdown(f"<div class='industrial-card'>${total_val:,.2f}<br>₺{total_tl:,.0f}<br>🌯 {doner:,.0f} Döner</div>", unsafe_allow_html=True)

            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                aylar = ["Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]
                st.area_chart(pd.DataFrame({"$": [total_val * (1.10**i) for i in range(5)]}, index=aylar), height=200)
            with c2:
                import plotly.graph_objects as go
                fig = go.Figure(data=[go.Pie(labels=['USD', 'GR', 'CY'], values=[u_row['USD'].values[0], (u_row['Gram'].values[0]*gram_altin/usd_try), (u_row['Çeyrek'].values[0]*ceyrek_fiyat/usd_try)], hole=.5)])
                fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', height=200)
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e: st.write(e)

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG CORE // {datetime.now().year}</div>", unsafe_allow_html=True)
