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
        return dict(zip(df['key'].astype(str), df['value'].astype(str)))
    except:
        return {"kasa": "600.0", "ana_para": "600.0"}

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

# --- DEĞİŞKENLER ---
kasa = get_val("kasa") if get_val("kasa") > 0 else 600.0
ana_para = get_val("ana_para") if get_val("ana_para") > 0 else 600.0
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")
og_kasa = get_val("oguzo_kasa") if get_val("oguzo_kasa") > 0 else kasa / 3
er_kasa = get_val("ero7_kasa") if get_val("ero7_kasa") > 0 else kasa / 3
fy_kasa = get_val("fybey_kasa") if get_val("fybey_kasa") > 0 else kasa / 3
og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")
aktif_soru_1 = live_vars.get("aktif_soru", "Yeni soru geliyor...")
aktif_soru_2 = live_vars.get("aktif_soru2", "BTC cuma kapanış tahmini")
toplam_bahis_kar = get_val("w1_sonuc") + get_val("w2_sonuc") + get_val("w3_sonuc") + get_val("w4_sonuc")
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

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        pwd = st.text_input("PIN", type="password", placeholder="----")
        if pwd == "1608":
            st.session_state["password_correct"] = True
            st.rerun()
        return False
    return True

# --- 5. ANA UYGULAMA ---
if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    st.markdown("<style>.stApp { background: #030303 !important; }</style>", unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; text-align:center;'>OG CORE</h1>", unsafe_allow_html=True)
        page = st.radio("Menu", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip"], label_visibility="collapsed")
        st.divider()
        if st.button("SİSTEMDEN ÇIK"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 Kişisel Kasa Dağılımı</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card'><div>Oguzo</div><div class='highlight'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card'><div>Ero7</div><div class='highlight'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card'><div>Fybey</div><div class='highlight'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 PERFORMANS</div><div class='val-std'>${toplam_bahis_kar:,.2f}</div></div>", unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 RÜTBE SIRALAMASI</div>", unsafe_allow_html=True)

    elif page == "📊 Portföy Takip":
        try:
            # Canlı Fiyatlar (En Üstte)
            usd_try = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]
            ons_gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            gram_altin = (ons_gold / 31.1035) * usd_try
            ceyrek_fiyat = gram_altin * 1.82 

            m1, m2, m3 = st.columns(3)
            with m1: st.markdown(f"<div class='industrial-card' style='border-top-color:#cc7a00;'><div style='font-size:10px; color:#666;'>USD/TRY</div><div style='font-size:28px; color:#cc7a00; font-family:Orbitron;'>₺{usd_try:.2f}</div></div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div class='industrial-card' style='border-top-color:#cc7a00;'><div style='font-size:10px; color:#666;'>GRAM ALTIN</div><div style='font-size:28px; color:#cc7a00; font-family:Orbitron;'>₺{gram_altin:.0f}</div></div>", unsafe_allow_html=True)
            with m3: st.markdown(f"<div class='industrial-card' style='border-top-color:#cc7a00;'><div style='font-size:10px; color:#666;'>ÇEYREK ALTIN</div><div style='font-size:28px; color:#cc7a00; font-family:Orbitron;'>₺{ceyrek_fiyat:.0f}</div></div>", unsafe_allow_html=True)

            # Portföy Hesaplamaları
            users = ["oguzo", "ero7", "fybey"]
            display_data = []
            for u in users:
                u_usd = get_val(f"{u}_usd")
                u_gr = get_val(f"{u}_altin")
                u_cy = get_val(f"{u}_ceyrek")
                t_usd = u_usd + (u_gr * gram_altin / usd_try) + (u_cy * ceyrek_fiyat / usd_try)
                display_data.append({"Kullanıcı": u.upper(), "USD": u_usd, "Gram": u_gr, "Çeyrek": u_cy, "TOPLAM_USD": t_usd})
            df_portfoy = pd.DataFrame(display_data)

            secilen_user = st.selectbox("Kullanıcı Portföy Detayı:", ["OGUZO", "ERO7", "FYBEY"])
            u_row = df_portfoy[df_portfoy["Kullanıcı"] == secilen_user]
            total_val = u_row["TOPLAM_USD"].values[0]
            total_tl = total_val * usd_try
            doner_sayisi = total_tl / (get_val("doner_fiyat") if get_val("doner_fiyat") > 0 else 150.0)

            st.markdown(f"""<div class='industrial-card' style='text-align:center; border-top: 4px solid #cc7a00; padding: 20px;'><div style='font-size:12px; color:#666;'>TOPLAM PORTFÖY DEĞERİ</div><div style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>${total_val:,.2f}</div><div style='font-size:16px; color:#666;'>≈ ₺{total_tl:,.0f}</div><div style='font-size:18px; color:#ffae00; font-weight:bold; margin-top:15px; border-top: 1px dashed #333; padding-top:10px;'>🌯 {doner_sayisi:,.0f} Adet Yarım Ekmek Döner</div></div>""", unsafe_allow_html=True)

            # Grafikler
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("<div class='terminal-header' style='font-size:10px;'>🧠 AI PROJEKSİYONU</div>", unsafe_allow_html=True)
                aylar = ["Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]
                chart_df = pd.DataFrame({"Varlık ($)": [total_val * (1.10**i) for i in range(5)]}, index=aylar)
                st.area_chart(chart_df, color="#cc7a00", height=200)
            with c2:
                st.markdown("<div class='terminal-header' style='font-size:10px;'>📊 KOMPOZİSYON</div>", unsafe_allow_html=True)
                import plotly.graph_objects as go
                fig = go.Figure(data=[go.Pie(labels=['Nakit', 'Gram', 'Çeyrek'], values=[u_row['USD'].values[0], (u_row['Gram'].values[0]*gram_altin/usd_try), (u_row['Çeyrek'].values[0]*ceyrek_fiyat/usd_try)], hole=.5, marker=dict(colors=['#cc7a00', '#ffae00', '#333333']))])
                fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200, margin=dict(t=0,b=0,l=0,r=0))
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Hata: {e}")

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG CORE // {datetime.now().year}</div>", unsafe_allow_html=True)
