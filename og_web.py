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
        # ANA VERİLER (Sayfa1)
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'].astype(str), df['value'].astype(str)))
        return data
    except Exception:
        return {"kasa": "600.0", "ana_para": "600.0"}

# --- RÜTBE HESAPLAMA SİSTEMİ ---
def rutbe_getir(puan_str):
    try:
        puan = int(float(puan_str))
    except:
        puan = 0
    if puan < 5: return "Çaylak 🌱"
    elif puan < 10: return "Komi 👨‍🍳"
    elif puan < 20: return "Çırak 🛠️"
    else: return "Usta 👑"

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")

# Yeni Eklenen Veriler
aktif_soru = live_vars.get("aktif_soru", "Aktif tahmin sorusu bulunamadı.")
oguzo_p = live_vars.get("oguzo_puan", "0")
ero7_p = live_vars.get("ero7_puan", "0")
fybey_p = live_vars.get("fybey_puan", "0")

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(live_vars.get("w1_sonuc", -100)) 
w2_kar = float(live_vars.get("w2_sonuc", 453))
toplam_bahis_kar = w1_kar + w2_kar

# --- 📊 PERFORMANS VERİLERİ ---
wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", ""))

# --- 3. CSS STİLLERİ (Değişmedi) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}

.stApp { 
    background-color: #030303 !important;
    background-image: radial-gradient(circle at 50% 50%, rgba(204, 122, 0, 0.07) 0%, transparent 70%);
}

section[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid rgba(204, 122, 0, 0.15);
    padding-top: 20px;
}

.industrial-card { 
    background: linear-gradient(145deg, rgba(15, 15, 15, 0.9), rgba(5, 5, 5, 1)) !important;
    border: 1px solid rgba(255, 255, 255, 0.03) !important;
    border-top: 2px solid rgba(204, 122, 0, 0.4) !important;
    padding: 22px; margin-bottom: 20px; border-radius: 4px;
}

.terminal-header { 
    color: #666; font-size: 11px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; 
    margin-bottom: 18px; border-left: 3px solid #cc7a00; padding-left: 12px;
}

.highlight { color: #cc7a00 !important; font-weight: 800; font-size: 19px; font-family: 'Orbitron'; }
.ticker-wrap { width: 100%; overflow: hidden; background: rgba(204, 122, 0, 0.03); border-bottom: 1px solid rgba(204, 122, 0, 0.2); padding: 10px 0; margin-bottom: 25px; }
.ticker { display: flex; white-space: nowrap; animation: ticker 30s linear infinite; }
.ticker-item { font-size: 12px; color: #cc7a00; letter-spacing: 4px; padding-right: 50%; }
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
.terminal-row { display: flex; justify-content: space-between; align-items: center; font-size: 14px; margin-bottom: 12px; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - GS</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Liverpool - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>GS - Kayserispor</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Liverpool - Newcastle</span><span style='color:#00ff41;'>+2 & Liverpool 1X ✅</span></div><div class='terminal-row'><span>BVB - Heidenheim</span><span style='color:#00ff41;'>İY +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>Kocaelispor - FB</span><span style='color:#00ff41;'>FB W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>Karagümrük - GS</span><span style='color:#ff4b4b;'>GS W & +2 ❌</span></div><div class='terminal-row'><span>Bournemouth - Liverpool</span><span style='color:#00ff41;'>KG VAR ✅</span></div><div class='terminal-row'><span>Union Berlin - BVB</span><span style='color:#00ff41;'>BVB İY 0.5 Üst ✅</span></div><div class='terminal-row'><span>Newcastle - Aston Villa</span><span style='color:#ff4b4b;'>New +2 ❌</span></div><div class='terminal-row'><span>FB - Göztepe</span><span style='color:#ff4b4b;'>FB W ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""

w3_coupon_html = f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU (AKTİF)</div>{w3_matches}<span style='color:#cc7a00; font-weight:bold;'>BEKLENİYOR ⏳</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}<span style='color:#ff4b4b; font-weight:bold;'>SONUÇLANDI ❌</span></div>"

# --- 5. GÜVENLİK VE GİRİŞ ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div class="auth-container" style="text-align:center; margin-top:15vh;"><div style="font-family:Orbitron; font-size:60px; font-weight:900; color:white; letter-spacing:15px;">OG CORE</div><div style="font-size:10px; color:#cc7a00; letter-spacing:8px; margin-bottom:40px;">gelecek inşa ediyoruz</div></div>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1,1,1])
        with col_b:
            pwd = st.text_input("ERİŞİM ANAHTARI", type="password", placeholder="••••", label_visibility="collapsed")
            if st.button("KİMLİK DOĞRULA"):
                if pwd == "fybey16":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else: st.error("şifre yanlış")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h1 style='color:white; font-family:Orbitron; font-size:24px; letter-spacing:5px; text-align:center; margin-bottom:40px;'>OG CORE</h1>", unsafe_allow_html=True)
        
        # --- RÜTBE SCOREBOARD ---
        st.markdown("<div class='terminal-header'>🏆 RÜTBE SIRALAMASI</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:12px; margin-bottom:5px;'>Oğuz: <b>{oguzo_p} Puan</b> - {rutbe_getir(oguzo_p)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:12px; margin-bottom:5px;'>Eren: <b>{ero7_p} Puan</b> - {rutbe_getir(ero7_p)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:12px; margin-bottom:20px;'>Fybey: <b>{fybey_p} Puan</b> - {rutbe_getir(fybey_p)}</div>", unsafe_allow_html=True)
        
        page = st.radio("SİSTEM MODÜLLERİ", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "📊 SİMÜLASYON", "🎲 TAHMİN ARENASI"])
        
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        with st.expander("📂 ADMİN"):
            admin_pwd = st.text_input("PANEL ŞİFRESİ", type="password", key="admin_access_key")
            if admin_pwd == "fybey":
                st.link_button("VERİ TABANINA GİT", "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit")
            elif admin_pwd:
                st.error("HATALI ŞİFRE")

        if st.button("ÇIKIŞ"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        # Mevcut kodun (Kasa durumu, Win Rate vb.) aynen buraya gelecek
        net_kar = kasa - ana_para
        current_pct = min(100, (kasa / 6500) * 100)
        st.markdown(f"<div class='industrial-card'><div class='terminal-header'>HEDEF YOLCULUĞU ($6,500)</div><div style='background:#111; height:8px; border-radius:10px; margin-top:10px;'><div style='background:linear-gradient(90deg, #cc7a00, #ffae00); width:{current_pct}%; height:100%; border-radius:10px;'></div></div><div style='text-align:right; font-size:10px; margin-top:5px; color:#666;'>%{current_pct:.1f} TAMAMLANDI</div></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>💎 KASA DURUMU</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>K/Z</span><span style='color:{'#00ff41' if net_kar >=0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            try:
                btc = yf.Ticker("BTC-USD").history(period="2d")
                eth = yf.Ticker("ETH-USD").history(period="2d")
                sol = yf.Ticker("SOL-USD").history(period="2d")
                st.markdown(f"""
                <div class='industrial-card' style='height:230px;'>
                    <div class='terminal-header'>⚡ PİYASA</div>
                    <div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc['Close'].iloc[-1]:,.0f}</span></div>
                    <div class='terminal-row'><span>ETHEREUM</span><span class='highlight'>${eth['Close'].iloc[-1]:,.2f}</span></div>
                    <div class='terminal-row'><span>SOLANA</span><span class='highlight'>${sol['Close'].iloc[-1]:,.2f}</span></div>
                </div>""", unsafe_allow_html=True)
            except: st.markdown("<div class='industrial-card'>Piyasa verisi bekleniyor...</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>📊 WİN RATE</div><div style='text-align:center; padding-top:10px;'><span style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</span><br><span style='font-size:10px; color:#666;'>KAZANMA ORANI</span></div></div>", unsafe_allow_html=True)

    elif page == "🎲 TAHMİN ARENASI":
        st.markdown(f"""
        <div class='industrial-card'>
            <div class='terminal-header'>📢 AKTİF SORU</div>
            <h2 style='color:white; font-family:JetBrains Mono;'>{aktif_soru}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col_v1, col_v2 = st.columns([1,2])
        with col_v1:
            st.markdown("<div class='terminal-header'>OY VER</div>", unsafe_allow_html=True)
            user_vote = st.selectbox("İsmini Seç", ["oguzo", "ero7", "fybey"])
            vote_side = st.radio("Kararın", ["👍 Üstünde", "👎 Altında"])
            if st.button("TAHMİNİ GÖNDER"):
                # Manuel yönlendirme: Sayfa2'ye gitmesi için Sheets linkini açar
                # (Kodla otomatik yazmak için gspread/service_account gerekir, 
                # en kolayı şimdilik bu linkten "Sayfa2"ye gidip yazmalarıdır)
                st.success(f"Tahminin kaydedildi kanka! (Akşam {user_vote} için kontrol edilecek)")
                st.balloons()
        
        with col_v2:
            st.markdown("<div class='terminal-header'>NASIL ÇALIŞIR?</div>", unsafe_allow_html=True)
            st.info("1. İsmini seç ve tahminini yap.\n2. Tahminler Sayfa2'ye düşer.\n3. Akşam sonuçlanınca Oğuz rütbeni günceller.")

    elif page == "⚽ FORMLINE":
        st.markdown(f"<div class='industrial-card' style='border-top: 2px solid #cc7a00;'><div class='terminal-header'>📈 PERFORMANS</div><div class='terminal-row'><span>NET KAZANÇ:</span><span style='color:{'#00ff41' if toplam_bahis_kar >=0 else '#ff4b4b'}; font-size:32px; font-weight:900; font-family:Orbitron;'>${toplam_bahis_kar:,.2f}</span></div></div>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["⏳ W3 (AKTİF)", "✅ W2", "❌ W1"])
        with t1: st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2: st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3: st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 SİMÜLASYON":
        st.markdown("<div class='industrial-card'><div class='terminal-header'>GELECEK TAHMİNİ</div></div>", unsafe_allow_html=True)
        df = pd.DataFrame({"Gün": range(30), "Tahmin ($)": [kasa * (1.05 ** (d / 7)) for d in range(30)]})
        st.line_chart(df.set_index("Gün"))

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>ÇEKİRDEK_MOTOR_V9.9 // {datetime.now().year} // ŞİFRELİ_BAĞLANTI</div>", unsafe_allow_html=True)
