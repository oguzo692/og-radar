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

# --- 2. VERİ BAĞLANTISI (GOOGLE SHEETS) ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'].astype(str), df['value'].astype(str)))
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
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")

og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "Gala maçı gala w ?")
aktif_soru_2 = live_vars.get("aktif_soru2", "BTC 7 Şubat günlük kapanış 70k")

w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 453))
toplam_bahis_kar = w1_kar + w2_kar
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))

# --- 3. CSS (YÜKSEK İŞÇİLİK SİSTEMİ) ---
custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {{visibility: hidden;}}
.stApp {{ background-color: #030303 !important; background-image: radial-gradient(circle at 50% 50%, rgba(204, 122, 0, 0.05) 0%, transparent 75%);}}

/* Sidebar Tasarımı */
section[data-testid="stSidebar"] {{ background-color: #050505 !important; border-right: 1px solid rgba(204, 122, 0, 0.15); min-width: 340px !important;}}
.stButton button {{ width: 100%; background: rgba(204, 122, 0, 0.1) !important; border: 1px solid rgba(204, 122, 0, 0.3) !important; color: #cc7a00 !important; font-family: 'Orbitron'; font-weight: bold; border-radius: 4px; transition: 0.3s;}}
.stButton button:hover {{ background: rgba(204, 122, 0, 0.3) !important; box-shadow: 0 0 15px rgba(204, 122, 0, 0.2);}}

/* Terminal Kartları */
.industrial-card {{ background: linear-gradient(145deg, rgba(15, 15, 15, 0.95), rgba(5, 5, 5, 1)) !important; border: 1px solid rgba(255, 255, 255, 0.03) !important; border-top: 2px solid #cc7a00 !important; padding: 22px; margin-bottom: 20px; border-radius: 4px; position: relative;}}
.terminal-header {{ color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px; font-family: 'Orbitron';}}
.terminal-row {{ display: flex; justify-content: space-between; align-items: center; font-size: 14px; margin-bottom: 12px; font-family: 'JetBrains Mono';}}
.highlight {{ color: #FFFFFF !important; font-family: 'JetBrains Mono';}}
.val-std {{ font-size: 24px !important; font-weight: 800 !important; font-family: 'Orbitron'; color: #cc7a00;}}

/* --- MASTER PROGRESS BAR (İŞÇİLİK BURADA) --- */
.progress-box {{ padding: 45px 15px 15px 15px; background: rgba(0,0,0,0.3); border-radius: 8px; border: 1px solid rgba(255,255,255,0.02); position: relative;}}
.bar-track {{ height: 16px; background: #0a0a0a; border-radius: 4px; border: 1px solid rgba(255,255,255,0.05); position: relative; box-shadow: inset 0 0 15px #000;}}
.bar-fill {{ height: 100%; border-radius: 4px; background: linear-gradient(90deg, #804d00, #cc7a00, #ffae00); box-shadow: 0 0 25px rgba(204, 122, 0, 0.3); transition: width 2s cubic-bezier(0.19, 1, 0.22, 1); position: relative; overflow: hidden;}}
.bar-fill::after {{ content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent); animation: sweep 3s infinite;}}
@keyframes sweep {{ 0% {{ transform: translateX(-100%); }} 100% {{ transform: translateX(100%); }} }}

/* Milestone Markers */
.m-tag {{ position: absolute; top: -35px; transform: translateX(-50%); font-family: 'Orbitron'; font-size: 10px; color: #444; text-align: center; white-space: nowrap; transition: 0.5s;}}
.m-tag.active {{ color: #cc7a00; text-shadow: 0 0 10px rgba(204, 122, 0, 0.5); font-weight: bold;}}
.m-line {{ position: absolute; top: 0; bottom: 0; width: 1px; background: rgba(255,255,255,0.1); z-index: 5;}}

/* Duyuru Bandı */
.ticker-wrap {{ width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 12px 0; margin-bottom: 25px;}}
.ticker {{ display: flex; white-space: nowrap; animation: ticker 40s linear infinite; font-family: 'Orbitron'; font-size: 12px; color: #cc7a00; letter-spacing: 2px;}}
@keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - GS</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Liverpool - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>GS - Kayserispor</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Liverpool - Newcastle</span><span style='color:#00ff41;'>+2 & Liverpool 1X ✅</span></div><div class='terminal-row'><span>BVB - Heidenheim</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Kocaelispor - FB</span><span style='color:#00ff41;'>FB W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Karagümrük - GS</span><span style='color:#ff4b4b;'>GS W & +2 ✅</span></div><div class='terminal-row'><span>Bournemouth - Liverpool</span><span style='color:#00ff41;'>KG VAR ✅</span></div><div class='terminal-row'><span>Union Berlin - BVB</span><span style='color:#00ff41;'>BVB İY 0.5 Üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>New +2 ❌</span></div><div class='terminal-row'><span>FB - Göztepe</span><span style='color:#ff4b4b;'>FB W ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""
w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU (AKTİF)</div>{w3_matches}</div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}</div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}</div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False
def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div style="text-align:center; margin-top:20vh;"><div style="font-family:Orbitron; font-size:60px; font-weight:900; color:white; letter-spacing:15px; text-shadow: 0 0 30px rgba(204,122,0,0.3);">OG CORE</div></div>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1,1,1])
        with col_b:
            pwd = st.text_input("ŞİFRE", type="password", placeholder="PASSWORD REQUIRED", label_visibility="collapsed")
            if st.button("AUTHENTICATE"):
                if pwd == "1608":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else: st.error("ACCESS DENIED")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span>{duyuru_metni} ••• {duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:26px; letter-spacing:4px; text-align:center; margin:30px 0;'>OG CORE</h1>", unsafe_allow_html=True)
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE"])
        st.divider()
        with st.expander("📂 ADMİN PANEL"):
            admin_pwd = st.text_input("MASTER KEY", type="password")
            if admin_pwd == "fybey": st.link_button("DATABASE", "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit")
        if st.button("DISCONNECT"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        # --- KASA DAĞILIMI ---
        st.markdown("<div class='terminal-header'>💰 KİŞİSEL KASA DAĞILIMI</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)
        with k1: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Oguzo Bakiye</div><div class='highlight' style='font-size:18px;'>${og_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k2: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Ero7 Bakiye</div><div class='highlight' style='font-size:18px;'>${er_kasa:,.2f}</div></div>", unsafe_allow_html=True)
        with k3: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>Fybey Bakiye</div><div class='highlight' style='font-size:18px;'>${fy_kasa:,.2f}</div></div>", unsafe_allow_html=True)

        # --- YENİ NESİL BAR SİSTEMİ ---
        start_v = 600
        end_v = 1800
        progress_pct = max(0, min(100, ((kasa - start_v) / (end_v - start_v)) * 100))
        m1_pct = ((900 - start_v) / (end_v - start_v)) * 100
        m2_pct = ((1200 - start_v) / (end_v - start_v)) * 100

        bar_html = f"""
        <div class="industrial-card">
            <div class="terminal-header">OBJECTIVE: $1,800 CHALLENGE</div>
            <div class="progress-box">
                <div class="m-tag {'active' if kasa >= 900 else ''}" style="left:{m1_pct}%">900 USD</div>
                <div class="m-tag {'active' if kasa >= 1200 else ''}" style="left:{m2_pct}%">1,200 USD</div>
                <div class="m-tag {'active' if kasa >= 1800 else ''}" style="left:100%">1,800 USD</div>
                
                <div class="bar-track">
                    <div class="m-line" style="left:{m1_pct}%"></div>
                    <div class="m-line" style="left:{m2_pct}%"></div>
                    <div class="bar-fill" style="width:{progress_pct}%"></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:15px; font-family:'JetBrains Mono'; font-size:11px; color:#444;">
                <span>START: $600</span>
                <span style="color:#cc7a00;">CURRENT: ${kasa:,.2f}</span>
                <span>TARGET: $1,800</span>
            </div>
        </div>
        """
        st.markdown(bar_html, unsafe_allow_html=True)

        # --- ALT İSTATİSTİKLER ---
        col1, col2, col3 = st.columns(3)
        net_kar = kasa - ana_para
        with col1: st.markdown(f"<div class='industrial-card' style='height:210px;'><div class='terminal-header'>💎 KASA ANALİZ</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>K/Z</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card' style='height:210px;'><div class='terminal-header'>⚡ MARKET DATA</div><div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div><div style='margin-top:10px; font-size:10px; color:#444;'>LIVE_TICKER_ACTIVE</div></div>", unsafe_allow_html=True)
            except: st.write("Feed Error")
        with col3: st.markdown(f"<div class='industrial-card' style='height:210px;'><div class='terminal-header'>📊 ALPHA WIN RATE</div><div style='text-align:center; padding-top:15px;'><span class='val-std'>%{wr_oran}</span></div></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='terminal-header'>📜 ACTIVITY LOGS</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='industrial-card'><p style='font-family:JetBrains Mono; color:#888; font-size:12px;'>{son_islemler_raw}</p></div>", unsafe_allow_html=True)

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 GLOBAL RANKING</div>", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>oguzo</div><div class='highlight'>{og_p} P</div><div style='font-size:12px; color:#cc7a00;'>{rutbe_getir(og_p)}</div></div>", unsafe_allow_html=True)
        with s2: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>ero7</div><div class='highlight'>{er_p} P</div><div style='font-size:12px; color:#cc7a00;'>{rutbe_getir(er_p)}</div></div>", unsafe_allow_html=True)
        with s3: st.markdown(f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>fybey</div><div class='highlight'>{fy_p} P</div><div style='font-size:12px; color:#cc7a00;'>{rutbe_getir(fy_p)}</div></div>", unsafe_allow_html=True)
        
        st.divider()
        q_col1, q_col2 = st.columns(2)
        base_script_url = "https://script.google.com/macros/s/AKfycbz0cvMHSrHchkksvFCixr9NDnMsvfLQ6T_K2jsXfohgs7eFXP5x-wxTX_YQej1EZhSX/exec"
        
        with q_col1:
            st.markdown(f"<div class='industrial-card' style='height:180px;'><div class='terminal-header'>📢 ACTIVE QUESTION 1</div><h3 style='color:white;'>{aktif_soru_1}</h3></div>", unsafe_allow_html=True)
            u1 = st.selectbox("OPERATOR", ["oguzo", "ero7", "fybey"], key="u1")
            v1 = st.radio("PREDICTION", ["👍", "👎"], horizontal=True, key="v1")
            if st.button("SUBMIT VOTE 1"): st.link_button("CONFIRM ACTION", f"{base_script_url}?isim={u1}&tahmin={v1}&soru=1")

        with q_col2:
            st.markdown(f"<div class='industrial-card' style='height:180px;'><div class='terminal-header'>📢 ACTIVE QUESTION 2</div><h3 style='color:white;'>{aktif_soru_2}</h3></div>", unsafe_allow_html=True)
            u2 = st.selectbox("OPERATOR", ["oguzo", "ero7", "fybey"], key="u2")
            v2 = st.radio("PREDICTION", ["👍", "👎"], horizontal=True, key="v2")
            if st.button("SUBMIT VOTE 2"): st.link_button("CONFIRM ACTION", f"{base_script_url}?isim={u2}&tahmin={v2}&soru=2")

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📈 NET PERFORMANCE</div><div class='val-std'>${toplam_bahis_kar:,.2f}</div></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["⏳ CURRENT (W3)", "✅ SUCCESS (W2)", "❌ FAILED (W1)"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    st.markdown(f"<div style='text-align:center; color:#333; font-size:10px; margin-top:100px; font-family:Orbitron;'>OG_CORE_TERMINAL_V9.9 // {datetime.now().year}</div>", unsafe_allow_html=True)
