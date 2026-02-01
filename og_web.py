import streamlit as st
import pandas as pd
from pybit.unified_trading import HTTP
import yfinance as yf

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG VIP Radar", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK: ŞİFRE KORUMASI ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "og2026": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔐 OG VIP Erişim Paneli")
        st.text_input("Lütfen Panel Şifresini Giriniz", type="password", on_change=password_entered, key="password")
        st.warning("Bu panel sadece lisanslı kullanıcılar içindir.")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Lütfen Panel Şifresini Giriniz", type="password", on_change=password_entered, key="password")
        st.error("❌ Hatalı Şifre! Lütfen OG ile iletişime geçin.")
        return False
    return True

if check_password():
    # --- 2. GÖRSEL TASARIM ---
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #00ff41 !important; }
        div[data-testid="stMetric"] { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. BYBIT VE PİYASA BAĞLANTISI ---
    try:
        # Streamlit Secrets'tan anahtarları çekiyoruz
        API_KEY = st.secrets["BYBIT_API_KEY"]
        API_SECRET = st.secrets["BYBIT_API_SECRET"]
        session = HTTP(testnet=False, api_key=API_KEY, api_secret=API_SECRET)
        
        # Canlı Bakiye Çekimi
        wallet = session.get_wallet_balance(accountType="UNIFIED")
        canli_kasa = float(wallet['result']['list'][0]['totalEquity'])
    except:
        st.error("⚠️ API Bağlantısı Başarısız! Lütfen Streamlit Secrets ayarlarını kontrol et.")
        canli_kasa = 0.0

    # Canlı Fiyatlar
    def get_market_data():
        data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close']
        return data.iloc[-1]
    
    prices = get_market_data()

    # --- 4. YÖNETİCİ AYARLARI (SIDEBAR) ---
    with st.sidebar:
        st.header("⚙️ Portföy Yönetimi")
        user = st.text_input("Aktif Kullanıcı", "ero7")
        st.write(f"📊 **Canlı Kasa:** ${canli_kasa:,.2f}")
        ana_para = 600.0
        hedef = 1500.0
        st.divider()
        if st.button("🔴 Güvenli Çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # Hesaplamalar
    net_kar = canli_kasa - ana_para
    kar_orani = (net_kar / ana_para) * 100 if ana_para != 0 else 0.0
    kisi_basi = net_kar / 3 if net_kar > 0 else 0.0

    # --- 5. ANA EKRAN ---
    st.title("🛡️ OG Trade Discipline Radar")
    st.caption(f"Yatırımcı: **{user}** | Sistem Durumu: **Canlı Veri Aktif ✅**")

    # Metrik Kartları
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 CANLI KASA", f"${canli_kasa:,.2f}", f"%{kar_orani:+.1f}")
    c2.metric("🟠 BTC/USDT", f"${prices['BTC-USD']:,.1f}")
    c3.metric("🔵 ETH/USDT", f"${prices['ETH-USD']:,.1f}")
    c4.metric("🟣 SOL/USDT", f"${prices['SOL-USD']:,.1f}")

    st.divider()

    # Kar Payları Bölümü
    st.subheader("👥 Ekip Kâr Dağıtımı")
    col_a, col_b = st.columns(2)
    with col_a:
        st.info(f"Kişi Başı Net Kâr: **${kisi_basi:.2f}**")
    with col_b:
        st.success(f"Toplam Alacak (Ana+Kar): **${(200 + kisi_basi):.2f}**")
    st.caption("Üyeler: oguzo | ero7 | fybey")

    # Hedef Barı
    st.divider()
    st.subheader("🎯 Finansal Hedef İlerlemesi")
    progress = min(max(canli_kasa/hedef, 0.0), 1.0)
    st.progress(progress)
    st.write(f"Hedefe Kalan: **${max(hedef-canli_kasa, 0):.1f}** | Başarı Oranı: **%{(canli_kasa/hedef)*100:.1f}**")

    # --- 6. FOOTER ---
    st.divider()
    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
