import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz
import json
import os
import streamlit.components.v1 as components

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core v8.8", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. KUPON ŞABLONLARI ---
w3_coupon_html = """<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU</div><div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Lıve - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 1px solid #30363d; margin: 10px 0;'><div class='terminal-row'><span class='dim'>oran: 8.79</span><span class='dim'>bet: 100 USD</span><span style='color:#f1c40f;'>BEKLENİYOR ⏳</span></div></div>"""
w2_coupon_html = """<div class='industrial-card' style='border-left-color: #00ff41;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU - KAZANDI</div><div class='terminal-row'><span>Gala - Kayserispor</span><span style='color:#00ff41;'>gala w & +2.5 üst ✅</span></div><div class='terminal-row'><span>Lıve - Newcastle</span><span style='color:#00ff41;'>kg var ✅</span></div><div class='terminal-row'><span>Bvb - Heidenheim</span><span style='color:#00ff41;'>bvb w & +1.5 üst ✅</span></div><div class='terminal-row'><span>Kocaelispor - Fenerbahçe</span><span style='color:#00ff41;'>fenerbahçe w & 1.5 üst ✅</span></div><hr style='border: 1px solid #30363d; margin: 10px 0;'><div class='terminal-row'><span class='dim'>oran: 5.40</span><span class='dim'>bet: 100 USD</span><span style='color:#00ff41;'>SONUÇLANDI +540 USD</span></div></div>"""
w1_coupon_html = """<div class='industrial-card' style='border-left-color: #ff4b4b;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU - KAYBETTİ</div><div class='terminal-row'><span>Karagümrük - Gala</span><span style='color:#00ff41;'>gala w & 1.5 üst ✅</span></div><div class='terminal-row'><span>Bournemouth - Lıve</span><span style='color:#00ff41;'>kg var ✅</span></div><div class='terminal-row'><span>Unıon Berlin - Bvb</span><span style='color:#00ff41;'>bvb 0.5 üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>newcastle 1.5 üst ❌</span></div><div class='terminal-row'><span>Fenerbahçe - Göztepe</span><span style='color:#ff4b4b;'>fenerbahçe w ❌</span></div><hr style='border: 1px solid #30363d; margin: 10px 0;'><div class='terminal-row'><span class='dim'>oran: 7.09</span><span class='dim'>bet: 100 USD</span><span style='color:#ff4b4b;'>SONUÇLANDI -100 USD</span></div></div>"""

# --- 3. CSS STİLLERİ ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
.main { background-color: transparent !important; }
[data-testid="stAppViewContainer"] { background-color: #050505 !important; }
body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], p, div, span, h1, h2, h3, button, input { font-family: 'JetBrains Mono', monospace !important; }

/* --- 📺 GİRİŞ PANELİ SABİTLEME --- */
.auth-wrapper {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    display: flex; align-items: center; justify-content: center;
    z-index: 9999;
    pointer-events: none;
}
.auth-container {
    width: 450px; text-align: center;
    padding: 50px 40px; background: rgba(10, 10, 10, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 4px;
    box-shadow: 0 0 50px rgba(0,0,0,1); backdrop-filter: blur(15px);
    pointer-events: auto;
}
.retro-title {
    font-size: 45px; font-weight: bold; letter-spacing: 15px; color: white;
    text-shadow: 0 0 15px rgba(255,255,255,0.5);
    border-bottom: 2px solid white; padding-bottom: 10px; margin-bottom: 40px;
}
.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.05) !important;
    border: 1px solid #444 !important; color: white !important;
    text-align: center; border-radius: 0px !important; font-size: 20px !important;
}
div.stButton > button {
    background-color: transparent !important; color: white !important;
    border: 1px solid white !important; border-radius: 0px !important;
    width: 100% !important; font-weight: bold !important; letter-spacing: 5px !important;
    height: 55px !important; transition: 0.3s;
}
div.stButton > button:hover { background-color: white !important; color: black !important; }

/* 💎 HEDEF YOLCULUĞU - CETVEL SİSTEMİ */
.loot-container { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 25px; position: relative; height: 180px; }
.progress-track { background: #21262d; height: 16px; border-radius: 8px; width: calc(100% - 60px); position: absolute; bottom: 55px; left: 30px; box-shadow: inset 0 0 5px #000; }
.progress-fill { background: linear-gradient(90deg, #cc7a00, #ffae00); height: 100%; border-radius: 8px; box-shadow: 0 0 10px rgba(255, 174, 0, 0.4); transition: width 1s ease-in-out; }
.tick { position: absolute; bottom: -8px; width: 1px; height: 8px; background: rgba(255,255,255,0.15); }
.tick-long { height: 12px; background: rgba(255,255,255,0.4); width: 2px; }
.tick-label { position: absolute; bottom: -25px; transform: translateX(-50%); font-size: 8px; color: #8b949e; font-weight: bold; }

.milestone-item { position: absolute; top: -65px; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; width: 100px; z-index: 5; }
.m-icon { font-size: 26px; margin-bottom: 2px; filter: grayscale(1); opacity: 0.3; transition: 0.5s; }
.milestone-item.achieved .m-icon { filter: grayscale(0); opacity: 1; text-shadow: 0 0 15px #ffae00; transform: scale(1.15); }

/* DİĞER TASARIMLAR */
:root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; --terminal-gray: #8b949e; }
#MainMenu, footer, .stDeployButton {visibility: hidden !important;}
[data-testid="stToolbar"], [data-testid="stDecoration"] {display:none;}
.industrial-card { background: rgba(255, 255, 255, 0.02); border-left: 3px solid var(--soft-orange); border-radius: 4px; padding: 15px; margin-bottom: 20px; }
.terminal-header { color: var(--soft-orange); font-size: 14px; font-weight: bold; border-bottom: 1px dashed #30363d; padding-bottom: 5px; margin-bottom: 10px; text-transform: uppercase; }
.terminal-row { display: flex; justify-content: space-between; font-size: 13px; color: #e6edf3; margin-bottom: 6px; }
.highlight { color: var(--soft-orange); }
section[data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
</style>
"""

# --- 4. HAREKETLİ ARKA PLAN ---
particles_js = """
<div id="particles-js" style="position: fixed; width: 100%; height: 100%; top: 0; left: 0; z-index: 1; background-color: #050505;"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
  "particles": {
    "number": { "value": 100, "density": { "enable": true, "value_area": 800 } },
    "color": { "value": "#ffffff" },
    "shape": { "type": "circle" },
    "opacity": { "value": 0.3, "random": false },
    "size": { "value": 2, "random": true },
    "line_linked": { "enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.1, "width": 1 },
    "move": { "enable": true, "speed": 0.8, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false }
  },
  "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": true, "mode": "grab" }, "onclick": { "enable": true, "mode": "push" } } },
  "retina_detect": true
});
</script>
"""

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        components.html(particles_js, height=2000)
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown('<div class="auth-container"><div class="retro-title">OG_CORE</div>', unsafe_allow_html=True)
            pwd = st.text_input("", type="password", placeholder="PASSWORD REQUIRED")
            if st.button("Giriş"):
                if pwd == "1":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# --- 6. VERİ YÖNETİMİ ---
SAVE_FILE = "og_save_data.json"
def load_game_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f: return json.load(f)
        except: pass
    return {"kasa": 600.0, "ana_para": 500.0, "yakim": 20}

def save_game_data():
    data = {"kasa": st.session_state.kasa_input, "ana_para": st.session_state.ana_input, "yakim": st.session_state.yakim_input}
    with open(SAVE_FILE, "w") as f: json.dump(data, f)
    st.toast("💾 VERİLER KAYDEDİLDİ", icon="✅")

# --- 7. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    game_data = load_game_data()

    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MODÜLLER", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("KASA (USD)", value=game_data["kasa"], step=10.0, key="kasa_input", on_change=save_game_data)
        ana_para = st.number_input("SERMAYE", value=game_data["ana_para"], key="ana_input", on_change=save_game_data)
        gunluk_yakim = st.slider("HARCAMA ($/GÜN)", 0, 100, game_data["yakim"], key="yakim_input", on_change=save_game_data)
        st.divider()
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.markdown(f"<div style='text-align:center; color:#8b949e; font-size:12px; background:#0d1117; padding:5px; border:1px solid #30363d; border-radius:4px;'>🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
        if st.button("🔴 ÇIKIŞ YAP", use_container_width=True): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA FON":
        targets = [{"val": 1000, "icon": "📱", "name": "TELEFON"}, {"val": 2500, "icon": "🏖️", "name": "TATİL"}, {"val": 5000, "icon": "🏎️", "name": "ARABA"}]
        max_t = 6500
        pct = min(100, (kasa / max_t) * 100)
        
        target_html = f"<div class='loot-container'><div class='terminal-header' style='border:none;margin:0;'>💎 HEDEF YOLCULUĞU</div><div class='progress-track'>"
        for i in range(0, 101, 10):
            tick_val = int((i / 100) * max_t)
            tick_class = "tick-long" if i % 20 == 0 else ""
            target_html += f"<div class='tick {tick_class}' style='left:{i}%'></div><div class='tick-label' style='left:{i}%'>${tick_val}</div>"
        target_html += f"<div class='progress-fill' style='width:{pct}%'></div>"
        for t in targets:
            pos = (t['val'] / max_t) * 100
            cls = "achieved" if kasa >= t['val'] else ""
            icon = t['icon'] if kasa >= t['val'] else "🔒"
            target_html += f"<div class='milestone-item {cls}' style='left:{pos}%'><div class='m-icon'>{icon}</div><div style='font-size:9px;color:#8b949e;'>{t['name']}</div></div>"
        target_html += "</div></div>"
        st.markdown(target_html, unsafe_allow_html=True)

        net_kar = kasa - ana_para
        tl_karsiligi = kasa * 33.50
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>💎 TRADE ANALİZİ</div><div class='terminal-row'><span>💰 TOPLAM KASA</span><span class='highlight'>${kasa:,.2f} (≈ {tl_karsiligi:,.0f} TL)</span></div><div class='terminal-row'><span>🚀 NET KAR/ZARAR</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'}'>{net_kar:,.2f} USD (%{(net_kar/ana_para*100) if ana_para > 0 else 0:.1f})</span></div></div>", unsafe_allow_html=True)

        col_piyasa, col_omur = st.columns([2, 1])
        with col_piyasa:
            try:
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                eth = yf.Ticker("ETH-USD").history(period="1d")['Close'].iloc[-1]
                st.markdown(f"<div class='industrial-card'><div class='terminal-header'>📊 PİYASA</div><div class='terminal-row'><span>🟠 BTC</span><span>${btc:,.2f}</span></div><div class='terminal-row'><span>🔵 ETH</span><span>${eth:,.2f}</span></div></div>", unsafe_allow_html=True)
            except: st.error("Veri çekilemedi")
        with col_omur:
            gun_omru = int(kasa / gunluk_yakim) if gunluk_yakim > 0 else 999
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>💀 FON ÖMRÜ</div><h2 style='text-align:center;'>{gun_omru} GÜN</h2></div>", unsafe_allow_html=True)

        st.subheader("🎯 Üye Payları")
        pay = kasa / 3
        c1, c2, c3 = st.columns(3)
        for col, u in zip([c1, c2, c3], ["OGUZO", "ERO7", "FYBEY"]):
            col.markdown(f"<div class='industrial-card'><div class='terminal-header'>{u}</div><div class='terminal-row'><span>PAY</span><span class='highlight'>${pay:,.2f}</span></div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE")
        tab1, tab2, tab3 = st.tabs(["⏳ W3", "✅ W2", "❌ W1"])
        with tab1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with tab2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with tab3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 DASHDASH":
        st.title("📈 Performans")
        st.line_chart(pd.DataFrame({"Kasa": [kasa * ((1.05)**(g/7)) for g in range(30)]}))

    st.caption("OG Core v8.8 | Fybey e aittir.")
