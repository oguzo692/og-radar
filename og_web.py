import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG Core", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.title("🔐 OG Core")
        pwd = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else: st.error("❌ Götten sallama aq ya")
        return False
    return True

if check_password():
    # --- 2. PREMIUM CSS (GLASSMORPHISM) ---
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(135deg, #0d1117 0%, #000000 100%);
        }
        /* Cam Kart Efekti */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            margin-bottom: 20px;
        }
        /* Neon Metrikler */
        div[data-testid="stMetricValue"] {
            color: #00ff41 !important;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
        }
        .status-win { color: #00ff41; font-weight: bold; text-shadow: 0 0 5px rgba(0,255,65,0.5); }
        .status-loss { color: #ff4b4b; font-weight: bold; text-shadow: 0 0 5px rgba(255,75,75,0.5); }
        .status-wait { color: #f1c40f; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG Core")
        page = st.radio("🚀 Strateji Yönetimi", ["⚡ Ultra Atak Fon", "📈 OG FormLine", "📊 OG DashDash"])
        st.divider()
        if page == "⚡ Ultra Atak Fon":
            st.subheader("⚙️ Fon Yönetimi")
            kasa = st.number_input("Güncel Fon Bakiyesi (USD)", value=600.0, step=0.1)
        st.info(f"🕒 Sistem Zamanı: {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 Güvenli Çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 4. ULTRA ATAK FON (GÜNCELLENMİŞ TASARIM) ---
    if page == "⚡ Ultra Atak Fon":
        st.title("⚡ Ultra Atak Fon Yönetimi")
        st.caption("Premium Glassmorphism Interface v3.0 ✅")

        # Canlı Veri Çekme
        try:
            data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
        except: data = {"BTC-USD": 0, "ETH-USD": 0, "SOL-USD": 0}

        # Üst Metrik Kartları
        c1, c2, c3, c4 = st.columns(4)
        ana_para = 600.0
        net_kar = kasa - ana_para
        
        with c1: st.markdown(f"<div class='glass-card'>💰 FON TOPLAM<br><h2 style='color:#00ff41;'>${kasa:,.2f}</h2><small>%{((net_kar/ana_para)*100):+.1f}</small></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='glass-card'>🟠 BTC/USDT<br><h2 style='color:#f7931a;'>${data['BTC-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='glass-card'>🔵 ETH/USDT<br><h2 style='color:#627eea;'>${data['ETH-USD']:,.1f}</h2></div>", unsafe_allow_html=True)
        with c4: st.markdown(f"<div class='glass-card'>🟣 SOL/USDT<br><h2 style='color:#b457ff;'>${data['SOL-USD']:,.1f}</h2></div>", unsafe_allow_html=True)

        st.divider()

        # SON 5 İŞLEM LİSTESİ (PRO TABLO)
        st.subheader("📑 Son 3 İşlem")
        
        # Hayali veriler (Burayı istediğin zaman güncelleyebiliriz kanka)
        trades = [
            {"Coin": "BTC/USDT", "Tip": "🟢 Long", "Giriş": "$76,450", "K/Z": "+%2.4", "Durum": "Kapalı ✅"},
            {"Coin": "SOL/USDT", "Tip": "🔴 Short", "Giriş": "$102.1", "K/Z": "-%1.1", "Durum": "Kapalı ❌"},
            {"Coin": "ETH/USDT", "Tip": "🟢 Long", "Giriş": "$2,245", "K/Z": "+%0.8", "Durum": "Açık ⏳"},

        ]
        
        # Tabloyu cam kart içine gömme
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        df_trades = pd.DataFrame(trades)
        st.table(df_trades)
        st.markdown("</div>", unsafe_allow_html=True)

        # EKİP KÂR DAĞITIMI
        st.subheader("👥 Fon Kâr Paylaşımı")
        k_kar = net_kar / 3 if net_kar > 0 else 0.0
        m1, m2, m3 = st.columns(3)
        for col, name in zip([m1, m2, m3], ["oguzo", "ero7", "fybey"]):
            with col:
                st.markdown(f"<div class='glass-card' style='text-align:center;'><h3 style='margin:0; color:#8b949e;'>{name.upper()}</h3><p style='margin:0; font-size:1.5rem; color:#00ff41;'>${200+k_kar:,.2f}</p></div>", unsafe_allow_html=True)

    # --- 5. DİĞER SAYFALAR (Aynı Mantıkla Devam) ---
    elif page == "📈 OG FormLine":
        st.title("📈 OG FormLine")
        st.markdown("<div class='glass-card'>Kupon analizleri cam kart tasarımına taşındı.</div>", unsafe_allow_html=True)
    
    elif page == "📊 OG DashDash":
        st.title("📊 OG DashDash")
        st.markdown("<div class='glass-card'>Gelişmiş analitik grafikler hazırlanıyor...</div>", unsafe_allow_html=True)

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
