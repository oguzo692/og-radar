import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz

# --- 1. AYARLAR ---
st.set_page_config(page_title="OG Core v7.1", page_icon="🛡️", layout="wide")

# --- 2. CSS STİLLERİ ---
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
.status-wait { color: #f1c40f; font-weight: bold; }

h1, h2, h3 { color: #e6edf3 !important; }
section[data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
</style>
"""

# --- 3. HTML ŞABLONLARI ---

# W3 Kuponu (Düzenlenmiş ve Hatasız)
w3_coupon_html = """
<div class='industrial-card'>
    <div class='terminal-header'>🔥 W3 KUPONU (8-9 ŞUBAT)</div>
    <div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>MS 2</span></div>
    <div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>Newcastle 1.5 üst</span></div>
    <div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>Gala w & 1.5 üst</span></div>
    <div class='terminal-row'><span>Lıve - Man City</span><span class='highlight'>Lıve gol atar</span></div>
    <div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>MS 1</span></div>
    <hr style='border: 1px solid #30363d; margin: 10px 0;'>
    <div class='terminal-row'><span class='dim'>ORAN: --</span><span class='dim'>bet: 100 USD</span><span class='status-wait'>BEKLENİYOR ⏳</span></div>
</div>
"""

w2_coupon_html = """
<div class='industrial-card' style='border-left-color: #00ff41;'>
    <div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU - kazandı</div>
    <div class='terminal-row'><span>Gala - Kayserispor</span><span class='win'>gala w & +2.5 üst ✅</span></div>
    <div class='terminal-row'><span>Lıve - Newcastle</span><span class='win'>kg var ✅</span></div>
    <div class='terminal-row'><span>Bvb - Heidenheim</span><span class='win'>bvb w & +1.5 üst ✅</span></div>
    <div class='terminal-row'><span>Kocaelispor - Fenerbahçe</span><span class='win'>fenerbahçe w & 1.5 üst ✅</span></div>
    <hr style='border: 1px solid #30363d; margin: 10px 0;'>
    <div class='terminal-row'><span class='dim'>ORAN: 5.40</span><span class='dim'>bet: 100 USD</span><span class='win'>SONUÇLANDI +540 USD</span></div>
</div>
"""

w1_coupon_html = """
<div class='industrial-card' style='border-left-color: #ff4b4b;'>
    <div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU - Kaybetti</div>
    <div class='terminal-row'><span>Karagümrük - Gala</span><span class='win'>Gala w & 1.5 üst ✅</span></div>
    <div class='terminal-row'><span>Bournemouth - Lıve</span><span class='win'>kg var ✅</span></div>
    <div class='terminal-row'><span>Unıon Berlin - Bvb</span><span class='win'>Bvb 0.5 üst ✅</span></div>
    <div class='terminal-row'><span>Newcastle - Aston Villa</span><span class='loss'>Newcastle 1.5 üst ❌</span></div>
    <div class='terminal-row'><span>Fenerbahçe - Göztepe</span><span class='loss'>Fnerbahçe w ❌</span></div>
    <hr style='border: 1px solid #30363d; margin: 10px 0;'>
    <div class='terminal-row'><span class='dim'>ORAN: 7.09</span><span class='dim'>bet: 100 USD</span><span class='loss'>SONUÇLANDI -100 USD</span></div>
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
    st.markdown(custom_css, unsafe_allow_html=True)

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

    if page == "⚡ ULTRA FON":
        net_kar = kasa - ana_para
        kar_yuzdesi = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        tl_karsiligi = kasa * 33.50
        
        st.markdown(f"""
        <div class='industrial-card'>
            <div class='terminal-header'>💎 OG TRADE RADAR — v7.1</div>
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
            gun_omru = int(kasa / gunluk_yakim) if gunluk_yakim > 0 else 999
            renk_durumu = "#ff4b4b" if gun_omru < 14 else "#00ff41"
            st.markdown(f"""
            <div class='industrial-card' style='border-left-color: {renk_durumu};'>
                <div class='terminal-header' style='color:{renk_durumu};'>💀 FON ÖMRÜ</div>
                <h2 style='text-align:center; color:{renk_durumu}; margin:10px 0;'>{gun_omru} GÜN</h2>
                <div style='text-align:center; font-size:11px; color:#8b949e;'>Yakma hızı: ${gunluk_yakim}/gün</div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("🎯 HEDEF ANALİZİ & ÜYE PAYLARI")
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

    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE ANALİZ")
        tab1, tab2, tab3 = st.tabs(["⏳ W3", "✅ W2", "❌ W1"])
        with tab1:
            st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with tab2:
            st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with tab3:
            st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 DASHDASH":
        st.title("📈 PERFORMANS SİMÜLATÖRÜ")
        col_inp1, col_inp2 = st.columns(2)
        with col_inp1:
            hedef_oran = st.slider("Günlük Hedef Kar (%)", 0.1, 5.0, 1.0)
        with col_inp2:
            sure = st.slider("Simülasyon Süresi (Gün)", 7, 90, 30)
        gelecek_degerler = [kasa * ((1 + hedef_oran/100) ** gun) for gun in range(sure)]
        df_chart = pd.DataFrame({"Gün": range(sure), "Kasa Tahmini ($)": gelecek_degerler})
        st.line_chart(df_chart.set_index("Gün"))
        st.success(f"🚀 {sure} gün sonraki tahmini kasa: **${gelecek_degerler[-1]:,.2f}**")
        st.divider()
        st.markdown("""
        <div class='industrial-card'>
            <div class='terminal-header'>🏁 FORM VE SERİ (STREAK)</div>
            <div class='terminal-row'><span>SON 5 İŞLEM</span><span>✅ ✅ ❌ ✅ ✅</span></div>
            <div class='terminal-row'><span>MOMENTUM</span><span class='highlight'>+3 (GÜÇLÜ)</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.caption("OG Core v7.1 | Discipline is Profit.")
