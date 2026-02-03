import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz

# --- 1. AYARLAR ---
st.set_page_config(page_title="OG Core v7.1", page_icon="🛡️", layout="wide")

# --- 2. CSS STİLLERİ (Değişken olarak tanımlandı - HATA RİSKİ SIFIR) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
.main { background-color: #0d1117 !important; }
* { font-family: 'JetBrains Mono', monospace !important; }
:root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; --terminal-gray: #8b949e; }

.industrial-card {
    background: rgba(255, 255, 255, 0.02);
    border-left: 3px solid var(--soft-orange);
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 20px;
}
.terminal-header { 
    color: var(--soft-orange); 
    font-size: 14px; 
    font-weight: bold; 
    border-bottom: 1px dashed #30363d; 
    padding-bottom: 5px; 
    margin-bottom: 10px;
    text-transform: uppercase;
}
.terminal-row {
    display: flex; justify-content: space-between;
    font-size: 13px; color: #e6edf3; margin-bottom: 6px;
}
.highlight { color: var(--soft-orange); }
.win { color: var(--win-green); }
.loss { color: var(--loss-red); }
.dim { color: var(--terminal-gray); }

h1, h2, h3 { color: #e6edf3 !important; }
section[data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
</style>
"""

# --- 3. HTML ŞABLONLARI (Kuponlar vb.) ---
# W2 Kuponu HTML'i
w2_coupon_html = """
<div class='industrial-card' style='border-left-color: #00ff41;'>
    <div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU - KAZANDI</div>
    <div class='terminal-row'><span>GS - Kayserispor</span><span class='win'>GS W & +2.5 ÜST ✅</span></div>
    <div class='terminal-row'><span>Liverpool - Newcastle</span><span class='win'>KG VAR ✅</span></div>
    <div class='terminal-row'><span>BVB - Heidenheim</span><span class='win'>BVB İY 0.5 ÜST ✅</span></div>
    <div class='terminal-row'><span>Kocaelispor - FB</span><span class='win'>FB W & 1.5 ÜST ✅</span></div>
    <hr style='border: 1px solid #30363d; margin: 10px 0;'>
    <div class='terminal-row'><span class='dim'>ORAN: 5.40</span><span class='dim'>BÜTÇE: 100 USD</span><span class='win'>DURUM: SONUÇLANDI +540 USD</span></div>
</div>
"""

# W1 Kuponu HTML'i
w1_coupon_html = """
<div class='industrial-card' style='border-left-color: #ff4b4b;'>
    <div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU - KAYBETTİ</div>
    <div class='terminal-row'><span>Karagümrük - GS</span><span class='win'>GS W & +1.5 ÜST ✅</span></div>
    <div class='terminal-row'><span>Bournemouth - Liv</span><span class='win'>KG VAR ✅</span></div>
    <div class='terminal-row'><span>New - Aston Villa</span><span class='loss'>MS 1 ❌</span></div>
    <div class='terminal-row'><span>FB - Göztepe</span><span class='loss'>İY 0.5 ÜST ❌</span></div>
    <hr style='border: 1px solid #30363d; margin: 10px 0;'>
    <div class='terminal-row'><span class='dim'>ORAN: 7.09</span><span class='dim'>BÜTÇE: 100 USD</span><span class='loss'>SONUÇ: -100 USD</span></div>
</div>
"""

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align:center; color:#cc7a00; font-family:monospace;'>🛡️ OG_CORE AUTH</h1>", unsafe_allow_html=True)
        pwd = st.text_input("ŞİFRE", type="password")
        if st.button("SİSTEME GİR"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ ERİŞİM REDDEDİLDİ")
        return False
    return True

# --- 5. ANA UYGULAMA ---
if check_password():
    # CSS'i yükle
    st.markdown(custom_css, unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00;'>🛡️ OG CORE v7.1</h2>", unsafe_allow_html=True)
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("TOPLAM KASA (USD)", value=600.0, step=10.0)
        ana_para = st.number_input("BAŞLANGIÇ SERMAYESİ", value=500.0)
        gunluk_yakim = st.slider("GÜNLÜK ORT. HARCAMA ($)", 0, 100, 20)
        
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.info(f"🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}")
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # SAYFA 1: ULTRA FON (v7.1 Dashboard)
    if page == "⚡ ULTRA FON":
        # Hesaplamalar
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        tl_karsiligi = kasa * 33.50
        
        # 1. BÖLÜM: ÜST BİLGİ PANELİ
        st.markdown(f"""
        <div class='industrial-card'>
            <div class='terminal-header'>💎 OG TRADE RADAR — v7.1</div>
            <div class='terminal-row'><span>🕒 SON GÜNCELLEME</span><span>{datetime.now(tr_tz).strftime('%H:%M:%S')}</span></div>
            <div class='terminal-row'><span>💰 TOPLAM KASA</span><span class='highlight'>${kasa:,.2f} (≈ {tl_karsiligi:,.0f} TL)</span></div>
            <div class='terminal-row'><span>🚀 NET KAR/ZARAR</span><span style='color:{"#00ff41" if net_kar >=0 else "#ff4b4b"}'>{net_kar:,.2f} USD (%{kar_yuzdesi:.1f})</span></div>
        </div>
        """, unsafe_allow_html=True)

        # 2. BÖLÜM: PİYASA VE ÖLÜM KALIM
        col_piyasa, col_omur = st.columns([2, 1])
        
        with col_piyasa:
            # Fiyatları çekmeye çalış, hata verirse 0 bas
            try:
                tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
                prices = yf.download(tickers, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
                btc = prices['BTC-USD']
                eth = prices['ETH-USD']
                sol = prices['SOL-USD']
            except:
                btc, eth, sol = 0, 0, 0
            
            st.markdown(f"""
            <div class='industrial-card'>
                <div class='terminal-header'>📊 PİYASA NABZI</div>
                <div class='terminal-row'><span>🟠 BTC</span><span>${btc:,.2f}</span></div>
                <div class='terminal-row'><span>🔵 ETH</span><span>${eth:,.2f}</span></div>
                <div class='terminal-row'><span>🟣 SOL</span><span>${sol:,.2f}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_omur:
            # Survival Runway Hesaplama
            gun_omru = int(kasa / gunluk_yakim) if gunluk_yakim > 0 else 999
            renk_durumu = "#ff4b4b" if gun_omru < 14 else "#00ff41"
            
            st.markdown(f"""
            <div class='industrial-card' style='border-left-color: {renk_durumu};'>
                <div class='terminal-header' style='color:{renk_durumu};'>💀 FON ÖMRÜ</div>
                <h2 style='text-align:center; color:{renk_durumu}; margin:10px 0;'>{gun_omru} GÜN</h2>
                <div style='text-align:center; font-size:11px; color:#8b949e;'>Yakma hızı: ${gunluk_yakim}/gün</div>
            </div>
            """, unsafe_allow_html=True)

        # 3. BÖLÜM: HEDEF ANALİZİ & PAYLAŞIM
        st.subheader("🎯 HEDEF ANALİZİ & ÜYE PAYLARI")
        pay = kasa / 3
        kisi_basi_kar = net_kar / 3
        
        c1, c2, c3 = st.columns(3)
        users = ["oguzo", "ero7", "fybey"]
        cols = [c1, c2, c3]
        
        for col, user in zip(cols, users):
            with col:
                st.markdown(f"""
                <div class='industrial-card'>
                    <div class='terminal-header'>{user.upper()}</div>
                    <div class='terminal-row'><span>PAY</span><span class='highlight'>${pay:,.2f}</span></div>
                    <div class='terminal-row'><span>KAR</span><span style='color:{"#00ff41" if kisi_basi_kar>=0 else "#ff4b4b"}'>{kisi_basi_kar:+.2f}</span></div>
                </div>
                """, unsafe_allow_html=True)

    # SAYFA 2: FORM LINE
    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE ANALİZ")
        tab1, tab2, tab3 = st.tabs(["🔥 W3 (8-9 Şub)", "✅ W2 (1-2 Şub)", "⏪ W1 (Geçmiş)"])
        
        with tab1:
            with tab1:
            # --- W3 KUPON GİRİŞİ BAŞLANGIÇ ---
            w3_html = """
            <div class='industrial-card'>
                <div class='terminal-header'>🔥 W3 KUPONU (8-9 ŞUBAT)</div>
                
                <div class='terminal-row'>
                    <span>Takım A - Takım B</span>
                    <span class='highlight'>MAÇ SONUCU 1</span>
                </div>

                <div class='terminal-row'>
                    <span>Takım C - Takım D</span>
                    <span class='highlight'>2.5 ÜST</span>
                </div>

                <div class='terminal-row'>
                    <span>Takım E - Takım F</span>
                    <span class='highlight'>KG VAR</span>
                </div>

                <hr style='border: 1px solid #30363d; margin: 10px 0;'>
                
                <div class='terminal-row'>
                    <span class='dim'>ORAN: 4.50</span>
                    <span class='dim'>BÜTÇE: 100$</span>
                    <span class='status-wait'>DURUM: OYNANIYOR ⏳</span>
                </div>
            </div>
            """
            
            st.markdown(w3_html, unsafe_allow_html=True)
            # --- W3 KUPON GİRİŞİ BİTİŞ ---
            
        with tab2:
            st.markdown(w2_coupon_html, unsafe_allow_html=True)
            
        with tab3:
            st.markdown(w1_coupon_html, unsafe_allow_html=True)

    # SAY
