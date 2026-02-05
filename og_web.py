import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz
import plotly.graph_objects as go

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core v8.8", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. VERİ BAĞLANTISI (GOOGLE SHEETS) ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'], df['value']))
        return data
    except Exception as e:
        return {"kasa": 600.0, "ana_para": 600.0}

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... VERİLER SENKRONİZE EDİLDİ... OG CORE V8.8 READY...")

# --- 🛠️ HATA KORUMALI GEÇMİŞ VERİ ÇEKİCİ ---
gecmis_raw = str(live_vars.get("gecmis_kasa", str(kasa)))
try:
    gecmis_liste = [float(x.strip()) for x in gecmis_raw.split(",") if x.strip()]
except:
    gecmis_liste = [kasa]

# --- 3. CSS STİLLERİ ---
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

/* Ticker */
.ticker-wrap {
    width: 100%; overflow: hidden; background: rgba(0, 0, 0, 0.6);
    border-bottom: 1px solid rgba(204, 122, 0, 0.3); padding: 12px 0;
    margin-bottom: 25px; backdrop-filter: blur(5px);
}
.ticker { display: flex; white-space: nowrap; animation: ticker 40s linear infinite; }
.ticker-item {
    font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #cc7a00;
    text-transform: uppercase; letter-spacing: 3px; padding-right: 100%;
}
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

/* Login */
.auth-container {
    padding: 4rem; background: linear-gradient(145deg, rgba(15,15,15,0.95) 0%, rgba(5,5,5,1) 100%);
    border: 1px solid rgba(204, 122, 0, 0.3); box-shadow: 0 0 60px rgba(0,0,0,1);
    text-align: center; max-width: 650px; margin: 10vh auto; border-radius: 4px;
}
.auth-header { font-family: 'Orbitron', sans-serif !important; font-size: 55px; font-weight: 900; color: #ffffff; letter-spacing: 12px; }

/* Industrial Cards */
.industrial-card { 
    background: rgba(18, 18, 18, 0.7) !important; backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.05) !important; border-top: 2px solid rgba(204, 122, 0, 0.4) !important;
    padding: 20px; margin-bottom: 25px; min-height: 100px; overflow: hidden;
}

.terminal-header { color: #888; font-size: 11px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 15px; }
.terminal-row { display: flex; justify-content: space-between; font-size: 15px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 8px; }
.highlight { color: #cc7a00 !important; font-weight: 700; font-size: 18px; }

/* Progress Bar */
.loot-wrapper {
    background: rgba(18, 18, 18, 0.8); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 4px; padding: 30px 25px 60px 25px; margin-bottom: 30px; position: relative;
}
.loot-track { background: #111; height: 12px; border-radius: 6px; width: 100%; position: relative; margin-top: 40px; border: 1px solid #222; }
.loot-fill { background: linear-gradient(90deg, #cc7a00, #ffae00); height: 100%; border-radius: 6px; box-shadow: 0 0 15px rgba(204, 122, 0, 0.5); }
.milestone { position: absolute; top: 50%; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; z-index: 10; }
.milestone-label { position: absolute; top: 25px; font-size: 10px; font-weight: bold; color: #888; text-align: center; white-space: nowrap; }

section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid rgba(204, 122, 0, 0.2); }
div.stButton > button { background: transparent !important; color: #cc7a00 !important; border: 1px solid #cc7a00 !important; letter-spacing: 5px !important; height: 50px; width: 100%; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Lıve - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 8.79</span><span>bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>Tarih: 1-2 şubat</span><span>Bütçe: 100 usd</span></div><div class='terminal-row'><span>gs - kayserispor</span><span style='color:#00ff41;'>iy +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>lıve - new</span><span style='color:#00ff41;'>+2 & liverpool 1x ✅</span></div><div class='terminal-row'><span>bvb - heidenheim</span><span style='color:#00ff41;'>iy +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>kocaelispor - fb</span><span style='color:#00ff41;'>fb W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 5.53</span><span>bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Tarih: 24-25 ocak</span><span>Bütçe: 100 usd</span></div><div class='terminal-row'><span>karagümrük - gs</span><span style='color:#00ff41;'>gs w & +2 ✅</span></div><div class='terminal-row'><span>bournemouth - lıve</span><span style='color:#00ff41;'>kg var ✅</span></div><div class='terminal-row'><span>unıon berlin - bvb</span><span style='color:#00ff41;'>bvb iy 0.5 üst ✅</span></div><div class='terminal-row'><span>new - aston villa</span><span style='color:#ff4b4b;'>new +2 ❌</span></div><div class='terminal-row'><span>fb - göztepe</span><span style='color:#ff4b4b;'>fb w ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 7.09</span><span>bet: 100 USD</span></div>"""

w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU (AKTİF)</div>{w3_matches}<span style='color:#cc7a00'>BEKLENİYOR ⏳</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important; min-height:auto;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (1-2 ŞUBAT)</div>{w2_matches}<span style='color:#00ff41;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important; min-height:auto;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (24-25 OCAK)</div>{w1_matches}<span style='color:#ff4b4b;'>SONUÇLANDI ❌</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div class="auth-container"><div class="auth-header">OG_CORE</div><div style="font-size: 10px; color: #cc7a00; letter-spacing: 5px; text-transform: uppercase; margin-bottom: 40px; opacity: 0.8;">ARCHITECTING THE FUTURE OF WEALTH</div></div>', unsafe_allow_html=True)
        pwd = st.text_input("ERİŞİM ANAHTARI", type="password", placeholder="System key required...", label_visibility="collapsed")
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
        page = st.radio("Modüller", ["⚡ Ultra Atak Fon", "⚽ Formlıne", "📊 Similasyon"])
        st.divider()
        admin_key = st.text_input("ADMİN ERİŞİMİ", type="password", placeholder="Admin Key...")
        if admin_key == "1":
            st.success("Admin Yetkisi Aktif")
            st.link_button("📊 Tabloyu Düzenle", "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit")
        st.divider()
        if st.button("🔴 Çıkış"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ Ultra Atak Fon":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        
        # Targets
        targets = [{"val": 1000, "name": "TELEFON", "icon": "📱"}, {"val": 2500, "name": "TATİL", "icon": "✈️"}, {"val": 5000, "name": "ARABA", "icon": "🏎️"}]
        max_target = 6500
        current_pct = min(100, (kasa / max_target) * 100)
        m_html = "".join([f"<div class='milestone' style='left:{(t['val']/max_target)*100}%'><div style='font-size:22px;'>{t['icon'] if kasa>=t['val'] else '🔒'}</div><div class='milestone-label'>{t['name']}<br>${t['val']}</div></div>" for t in targets])
        st.markdown(f"<div class='loot-wrapper'><div class='terminal-header'>TARGET PROGRESSION</div><div class='loot-track'><div class='loot-fill' style='width:{current_pct}%'></div>{m_html}</div></div>", unsafe_allow_html=True)
        
        # Upper Stats Section
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class='industrial-card'><div class='terminal-header'>💎 OG TRADE RADAR</div><div class='terminal-row'><span>NET KAR/ZARAR</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'}; font-size:22px;'>${net_kar:,.2f} (%{kar_yuzdesi:.1f})</span></div><div class='terminal-row'><span>TOPLAM KASA</span><span class='highlight'>${kasa:,.2f}</span></div></div>""", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                eth = yf.Ticker("ETH-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card'><div class='terminal-header'>GÜNCEL FİYATLAR</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.2f}</span></div><div class='terminal-row'><span>ETHEREUM</span><span>${eth:,.2f}</span></div></div>", unsafe_allow_html=True)
            except: st.error("Market data link lost.")

        # Shares Section
        st.subheader("🎯 Pay Dağılımı")
        cols = st.columns(3)
        for col, user in zip(cols, ["oguzo", "ero7", "fybey"]):
            col.markdown(f"<div class='industrial-card'><div class='terminal-header'>{user.upper()}</div><div class='terminal-row'><span>SHARE</span><span class='highlight'>${kasa/3:,.2f}</span></div><div class='terminal-row'><span>PROFIT</span><span>${(net_kar/3):,.2f}</span></div></div>", unsafe_allow_html=True)

        # --- 📉 SAYFA ALTI GRAFİK (TAM GENİŞLİK - DÜZENLENMİŞ) ---
        st.markdown("<div class='industrial-card' style='min-height:350px; padding: 20px 10px 10px 10px;'><div class='terminal-header' style='margin-bottom:5px;'>📊 KASA GELİŞİM SEYRİ (EQUITY CURVE)</div>", unsafe_allow_html=True)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=gecmis_liste, 
            mode='lines+markers',
            line=dict(color='#cc7a00', width=3),
            marker=dict(size=6, color='#ffae00', line=dict(color='#030303', width=1)),
            fill='tozeroy',
            fillcolor='rgba(204, 122, 0, 0.1)',
            hoverinfo='y'
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=30, b=10),
            height=280,
            autosize=True,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, fixedrange=True),
            yaxis=dict(
                showgrid=True, 
                gridcolor='rgba(255,255,255,0.05)', 
                tickfont=dict(color='#888', size=10), 
                zeroline=False,
                fixedrange=True,
                side="right"
            ),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "⚽ Formlıne":
        st.title("⚽ FORMLINE")
        t1, t2, t3 = st.tabs(["⏳ AKTİF (W3)", "✅ KAZANAN (W2)", "❌ KAYBEDEN (W1)"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 Similasyon":
        st.title("📈 Projeksiyon")
        h_oran = st.slider("Haftalık Hedef (%)", 1, 50, 5)
        sure = st.slider("Simülasyon (Gün)", 7, 120, 30)
        df = pd.DataFrame({"Gün": range(sure), "Tahmin ($)": [kasa * ((1 + h_oran/100) ** (d / 7)) for d in range(sure)]})
        st.line_chart(df.set_index("Gün"))

    st.caption("OG Core v8.8 | Veriler merkezi sistemden çekilmektedir.")
