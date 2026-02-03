import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz
import json
import os

# --- 1. AYARLAR ---
st.set_page_config(page_title="OG Core v8.8", page_icon="🛡️", layout="wide")

# --- 2. CSS STİLLERİ ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
.main { background-color: #0d1117 !important; }
* { font-family: 'JetBrains Mono', monospace !important; }
:root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; --terminal-gray: #8b949e; }

/* GİZLİLİK MODU */
#MainMenu, header, footer, .stDeployButton {visibility: hidden !important;}
[data-testid="stToolbar"] {visibility: hidden !important;}
[data-testid="stDecoration"] {display:none;}
[data-testid="stSidebarNav"] {border-right: 1px solid #30363d;}

/* KART TASARIMI */
.industrial-card {
    background: rgba(255, 255, 255, 0.02);
    border-left: 3px solid var(--soft-orange);
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 20px;
}
.terminal-header { 
    color: var(--soft-orange); 
    font-size: 14px; font-weight: bold; border-bottom: 1px dashed #30363d; 
    padding-bottom: 5px; margin-bottom: 10px; text-transform: uppercase;
}
.terminal-row {
    display: flex; justify-content: space-between;
    font-size: 13px; color: #e6edf3; margin-bottom: 6px;
}
.highlight { color: var(--soft-orange); }
.win { color: var(--win-green); }
.loss { color: var(--loss-red); }
.dim { color: var(--terminal-gray); }
.status-wait { color: #f1c40f; font-weight: bold; }

/* --- 💎 LOOT BAR STİLİ (FIXED & SPACED) --- */
.loot-wrapper {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    /* İkonlar ve yazılar için üstten/alttan geniş padding */
    padding: 20px 25px 50px 25px; 
    margin-bottom: 25px;
    position: relative;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.loot-track {
    background: #21262d;
    height: 14px;
    border-radius: 7px;
    width: 100%;
    position: relative;
    /* Başlık ile bar arasına mesafe koyuyoruz ki ikonlar sıkışmasın */
    margin-top: 45px; 
}
@keyframes fillAnimation { from { width: 0%; } }
.loot-fill {
    background: linear-gradient(90deg, #cc7a00, #ffae00);
    height: 100%;
    border-radius: 7px;
    box-shadow: 0 0 15px rgba(204, 122, 0, 0.5);
    animation: fillAnimation 1.5s ease-out forwards;
}
.milestone {
    position: absolute;
    top: 50%; 
    transform: translate(-50%, -50%);
    width: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 10;
    pointer-events: none;
}
.milestone-icon { 
    position: absolute;
    bottom: 12px; /* Barın üstüne */
    font-size: 24px; 
    transition: all 0.3s ease;
}
.milestone-label { 
    position: absolute;
    top: 15px; /* Barın altına */
    font-size: 11px; 
    font-weight: bold; 
    color: #8b949e; 
    text-align: center;
    white-space: nowrap;
    transition: all 0.3s ease;
}
/* Aktif Hedef Efekti (Daha Sade Neon) */
.milestone.active .milestone-label { 
    color: #00ff41; 
    text-shadow: 0 0 5px rgba(0, 255, 65, 0.6); 
}
.milestone.active .milestone-icon { 
    transform: scale(1.1); /* Hafif büyüme */
    text-shadow: 0 0 10px rgba(255,255,255,0.4); 
}

h1, h2, h3 { color: #e6edf3 !important; }
section[data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }

/* --- COMPACT SIDEBAR --- */
section[data-testid="stSidebar"] div.stButton > button {
    padding-top: 0.3rem;
    padding-bottom: 0.3rem;
    font-size: 13px;
    border: 1px solid #30363d;
}
button[kind="primary"] {
    background-color: #cc7a00 !important;
    color: white !important;
    border: none !important;
}
.time-widget {
    display: block;
    width: 100%;
    padding: 0.3rem;
    font-size: 13px;
    font-weight: bold;
    color: #8b949e;
    text-align: center;
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 0.25rem;
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
}
</style>
"""

# --- 3. HTML ŞABLONLARI ---
w3_coupon_html = """
<div class='industrial-card'>
    <div class='terminal-header'>🔥 W3 KUPONU</div>
    <div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div>
    <div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div>
    <div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>gala w & 1.5 üst</span></div>
    <div class='terminal-row'><span>Lıve - Man City</span><span class='highlight'>lıve gol atar</span></div>
    <div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div>
    <hr style='border: 1px solid #30363d; margin: 10px 0;'>
    <div class='terminal-row'><span class='dim'>oran: 8.79</span><span class='dim'>bet: 100 USD</span><span class='status-wait'>BEKLENİYOR ⏳</span></div>
</div>
"""
w2_coupon_html = """
<div class='industrial-card' style='border-left-color: #00ff41;'>
    <div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU - KAZANDI</div>
    <div class='terminal-row'><span>Gala - Kayserispor</span><span class='win'>gala w & +2.5 üst ✅</span></div>
    <div class='terminal-row'><span>Lıve - Newcastle</span><span class='win'>kg var ✅</span></div>
    <div class='terminal-row'><span>Bvb - Heidenheim</span><span class='win'>bvb w & +1.5 üst ✅</span></div>
    <div class='terminal-row'><span>Kocaelispor - Fenerbahçe</span><span class='win'>fenerbahçe w & 1.5 üst ✅</span></div>
    <hr style='border: 1px solid #30363d; margin: 10px 0;'>
    <div class='terminal-row'><span class='dim'>oran: 5.40</span><span class='dim'>bet: 100 USD</span><span class='win'>SONUÇLANDI +540 USD</span></div>
</div>
"""
w1_coupon_html = """
<div class='industrial-card' style='border-left-color: #ff4b4b;'>
    <div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU - KAYBETTİ</div>
    <div class='terminal-row'><span>Karagümrük - Gala</span><span class='win'>gala w & 1.5 üst ✅</span></div>
    <div class='terminal-row'><span>Bournemouth - Lıve</span><span class='win'>kg var ✅</span></div>
    <div class='terminal-row'><span>Unıon Berlin - Bvb</span><span class='win'>bvb 0.5 üst ✅</span></div>
    <div class='terminal-row'><span>Newcastle - Aston Villa</span><span class='loss'>newcastle 1.5 üst ❌</span></div>
    <div class='terminal-row'><span>Fenerbahçe - Göztepe</span><span class='loss'>fenerbahçe w ❌</span></div>
    <hr style='border: 1px solid #30363d; margin: 10px 0;'>
    <div class='terminal-row'><span class='dim'>oran: 7.09</span><span class='dim'>bet: 100 USD</span><span class='loss'>SONUÇLANDI -100 USD</span></div>
</div>
"""

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False
def check_password():
    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align:center; color:#cc7a00; font-family:monospace;'>🛡️ OG_CORE AUTH</h1>", unsafe_allow_html=True)
        pwd = st.text_input("ŞİFRE", type="password")
        if st.button("SİSTEME GİR"):
            if pwd == "1": st.session_state["password_correct"] = True; st.rerun()
            else: st.error("❌ HATALI ŞİFRE")
        return False
    return True

# --- 5. SAVE GAME SİSTEMİ ---
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
    st.toast("💾 OYUN KAYDEDİLDİ", icon="✅")

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    game_data = load_game_data()

    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("TOPLAM KASA (USD)", value=game_data["kasa"], step=10.0, key="kasa_input", on_change=save_game_data)
        ana_para = st.number_input("BAŞLANGIÇ SERMAYESİ", value=game_data["ana_para"], key="ana_input", on_change=save_game_data)
        gunluk_yakim = st.slider("GÜNLÜK ORT. HARCAMA ($)", 0, 100, game_data["yakim"], key="yakim_input", on_change=save_game_data)
        st.write("") 
        
        st.markdown("---")
        if st.button("💾 AYARLARI KAYDET", type="primary", use_container_width=True, key="save_sidebar"): save_game_data()
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.markdown(f"<div class='time-widget'>🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
        if st.button("🔴 ÇIKIŞ", use_container_width=True, key="exit_sidebar"): st.session_state["password_correct"] = False; st.rerun()

    # SAYFA 1: ULTRA FON
    if page == "⚡ ULTRA FON":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        tl_karsiligi = kasa * 33.50
        
        # --- 💎 LOOT BAR FIX ---
        targets = [
            {"val": 1000, "icon": "📱", "name": "TELEFON"},
            {"val": 2500, "icon": "🏖️", "name": "TATİL"},
            {"val": 5000, "icon": "🏎️", "name": "ARABA"},
        ]
        # MATEMATİK FIX: Barın sonu, son hedefin 1.3 katı olsun (Ne çok boş ne çok dolu)
        max_target = targets[-1]["val"] * 1.3 
        current_pct = min(100, (kasa / max_target) * 100)
        
        markers_html = ""
        for t in targets:
            pos = (t["val"] / max_target) * 100
            is_active = "active" if kasa >= t["val"] else ""
            icon_display = t['icon'] if kasa >= t["val"] else "🔒"
            markers_html += f"<div class='milestone {is_active}' style='left: {pos}%;'><div class='milestone-icon'>{icon_display}</div><div class='milestone-label'>{t['name']} (${t['val']})</div></div>"
            
        # CSS FIX: Başlıkta border-bottom: none komutu eklendi.
        loot_bar_html = f"""
<div class='loot-wrapper'>
<div class='terminal-header' style='margin-bottom:0px; border-bottom:none;'>💎 HEDEF YOLCULUĞU</div>
<div class='loot-track'>
<div class='loot-fill' style='width: {current_pct}%;'></div>
{markers_html}
</div>
</div>
"""
        st.markdown(loot_bar_html, unsafe_allow_html=True)
        
        if st.button("💾 HIZLI KAYDET", key="save_main"): save_game_data()

        st.markdown(f"""
<div class='industrial-card'>
<div class='terminal-header'>💎 OG TRADE RADAR — v8.8 (FIXED)</div>
<div class='terminal-row'><span>🕒 SON GÜNCELLEME</span><span>{datetime.now(tr_tz).strftime('%H:%M:%S')}</span></div>
<div class='terminal-row'><span>💰 TOPLAM KASA</span><span class='highlight'>${kasa:,.2f} (≈ {tl_karsiligi:,.0f} TL)</span></div>
<div class='terminal-row'><span>🚀 NET KAR/ZARAR</span><span style='color:{"#00ff41" if net_kar >=0 else "#ff4b4b"}'>{net_kar:,.2f} USD (%{kar_yuzdesi:.1f})</span></div>
</div>
""", unsafe_allow_html=True)

        col_piyasa, col_omur = st.columns([2, 1])
        with col_piyasa:
            try:
                btc_data = yf.Ticker("BTC-USD").history(period="1d")
                eth_data = yf.Ticker("ETH-USD").history(period="1d")
                sol_data = yf.Ticker("SOL-USD").history(period="1d")
                btc = btc_data['Close'].iloc[-1] if not btc_data.empty else 0
                eth = eth_data['Close'].iloc[-1] if not eth_data.empty else 0
                sol = sol_data['Close'].iloc[-1] if not sol_data.empty else 0
            except: btc, eth, sol = 0, 0, 0
            
            st.markdown(f"""
<div class='industrial-card'>
<div class='terminal-header'>📊 PİYASA</div>
<div class='terminal-row'><span>🟠 BTC</span><span>${btc:,.2f}</span></div>
<div class='terminal-row'><span>🔵 ETH</span><span>${eth:,.2f}</span></div>
<div class='terminal-row'><span>🟣 SOL</span><span>${sol:,.2f}</span></div>
</div>
""", unsafe_allow_html=True)
            
        with col_omur:
            gun_omru = int(kasa / gunluk_yakim) if gunluk_yakim > 0 else 999
            renk_durumu = "#ff4b4b" if gun_omru < 14 else "#00ff41"
            st.markdown(f"""
<div class='industrial-card' style='border-left-color: {renk_durumu};'>
<div class='terminal-header' style='color:{renk_durumu};'>💀 FON ÖMRÜ</div>
<h2 style='text-align:center; color:{renk_durumu}; margin:10px 0;'>{gun_omru} GÜN</h2>
<div style='text-align:center; font-size:11px; color:#8b949e;'>Yakma hızı: ${gunluk_yakim}/gün</div>
</div>
""", unsafe_allow_html=True)

        st.subheader("🎯 Üye Payları")
        pay = kasa / 3
        kisi_basi_kar = net_kar / 3
        c1, c2, c3 = st.columns(3)
        users = ["oguzo", "ero7", "fybey"]
        for col, user in zip([c1, c2, c3], users):
            with col:
                st.markdown(f"""
<div class='industrial-card'>
<div class='terminal-header'>{user.upper()}</div>
<div class='terminal-row'><span>PAY</span><span class='highlight'>${pay:,.2f}</span></div>
<div class='terminal-row'><span>KAR</span><span style='color:{"#00ff41" if kisi_basi_kar>=0 else "#ff4b4b"}'>{kisi_basi_kar:+.2f}</span></div>
</div>
""", unsafe_allow_html=True)

    # SAYFA 2: FORMLINE
    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE")
        tab1, tab2, tab3 = st.tabs(["⏳ W3", "✅ W2", "❌ W1"])
        with tab1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with tab2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with tab3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    # SAYFA 3: DASHDASH
    elif page == "📊 DASHDASH":
        st.title("📈 Performans Simülatörü")
        col_inp1, col_inp2 = st.columns(2)
        with col_inp1: haftalik_oran = st.slider("Haftalık Hedef Kar (%)", 1.0, 50.0, 5.0)
        with col_inp2: sure = st.slider("Simülasyon Süresi (Gün)", 7, 120, 30)
        gelecek_degerler = [kasa * ((1 + haftalik_oran/100) ** (gun / 7)) for gun in range(sure)]
        df_chart = pd.DataFrame({"Gün": range(sure), "Kasa Tahmini ($)": gelecek_degerler})
        st.line_chart(df_chart.set_index("Gün"))
        st.success(f"🚀 {sure} gün sonraki tahmini kasa: **${gelecek_degerler[-1]:,.2f}** (Haftalık %{haftalik_oran} büyüme ile)")
        st.divider()
        st.markdown("""
<div class='industrial-card'>
<div class='terminal-header'>🏁 FORM VE SERİ (STREAK)</div>
<div class='terminal-row'><span>SON 5 İŞLEM</span><span>✅ ✅ ❌ ✅ ✅</span></div>
<div class='terminal-row'><span>MOMENTUM</span><span class='highlight'>+3 (GÜÇLÜ)</span></div>
</div>
""", unsafe_allow_html=True)

    st.caption("OG Core v8.8 | Fybey e aittir.")
