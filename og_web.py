import streamlit as st
import requests
import pandas as pd

# Sayfa Ayarları (Koyu Tema ve Genişlik)
st.set_page_config(page_title="OG Trade Radar", page_icon="📈", layout="wide")

# Özel Tasarım (CSS) - Kartları ve Yazıları Güzelleştirir
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 2rem !important; color: #58a6ff !important; }
    div[data-testid="stMetric"] { background-color: #161b22; border-radius: 10px; padding: 20px; border: 1px solid #30363d; }
    .stProgress > div > div > div > div { background-color: #238636; }
    </style>
    """, unsafe_allow_html=True)

# --- VERİ ÇEKME (BYBIT) ---
def get_f(s):
    try:
        r = requests.get(f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={s}USDT", timeout=5).json()
        price = float(r['result']['list'][0]['lastPrice'])
        change = float(r['result']['list'][0]['price24hPcnt']) * 100
        return price, change
    except: return 0.0, 0.0

# --- AYARLAR ---
with st.sidebar:
    st.header("⚙️ Panel Ayarları")
    user = st.text_input("Kullanıcı Adı", "ero7")
    kasa = st.number_input("Güncel Kasa (USD)", value=600.0)
    dunku_kasa = st.number_input("Dünkü Kasa (USD)", value=580.0)
    ana_para = 600.0
    hedef = 1200.0
    st.divider()
    st.write(f"🔑 Lisans: 2026-12-31 | **AKTİF**")

# Verileri Çek
btc_p, btc_c = get_f("BTC")
eth_p, eth_c = get_f("ETH")
sol_p, sol_c = get_f("SOL")

# Hesaplamalar
net_kar = kasa - ana_para
kar_yuzde = (net_kar / ana_para) * 100
gunluk_fark = kasa - dunku_kasa
gunluk_yuzde = (gunluk_fark / dunku_kasa) * 100 if dunku_kasa > 0 else 0

# --- ANA PANEL ---
st.title("🛡️ OG Trade Discipline Radar")
st.caption(f"v6.1 - Profesyonel Canlı Piyasa Takibi | Hoş geldin, {user}")

# Üst Bilgi Kartları (Renkli ve Büyük)
c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 GÜNCEL KASA", f"${kasa:,.1f}", f"{kar_yuzde:+.1f}%")
c2.metric("📈 GÜNLÜK FARK", f"${gunluk_fark:+.1f}", f"{gunluk_yuzde:+.1f}%")
c3.metric("🟠 BTC/USDT", f"${btc_p:,.1f}", f"{btc_c:+.2f}%")
c4.metric("🟣 SOL/USDT", f"${sol_p:,.1f}", f"{sol_c:+.2f}%")

st.divider()

# Orta Bölüm: Hedef ve Basit Grafik
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🎯 Hedef Yolculuğu")
    st.progress(min(kasa / hedef, 1.0))
    st.write(f"**Hedef:** ${hedef} | **Kalan:** ${max(hedef - kasa, 0):.1f}")
    st.info(f"👥 **Üye Kâr Payları:** oguzo | ero7 | fybey → Kişi Başı: **${(net_kar/3 if net_kar > 0 else 0):.1f} USD**")

with col_right:
    st.subheader("📊 Performans")
    # Temsili iki nokta arası grafik
    st.line_chart(pd.DataFrame([dunku_kasa, kasa], columns=["Kasa"]))

st.divider()

# Alt Tablo
st.subheader("🧪 Piyasa Nabzı (Bybit Live)")
df = pd.DataFrame({
    "Parite": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
    "Fiyat": [f"${btc_p:,.2f}", f"${eth_p:,.2f}", f"${sol_p:,.2f}"],
    "Değişim": [f"%{btc_c:+.2f}", f"%{eth_c:+.2f}", f"%{sol_c:+.2f}"]
})
st.table(df)

st.caption("Powered by OG Core - Discipline is Profit.")