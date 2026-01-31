import streamlit as st
import requests
import pandas as pd

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG VIP Radar", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK: ŞİFRE KORUMASI ---
def check_password():
    def password_entered():
        # ŞİFREYİ BURADAN DEĞİŞTİREBİLİRSİN KANKA
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
    else:
        return True

# --- EĞER ŞİFRE DOĞRUYSA PANELİ AÇ ---
if check_password():
    
    # --- 2. GÖRSEL TASARIM (DARK MODE) ---
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #00ff41 !important; }
        div[data-testid="stMetric"] { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; }
        .stProgress > div > div > div > div { background-color: #00ff41; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. VERİ ÇEKME FONKSİYONU ---
    def get_f(s):
        try:
            r = requests.get(f"https://api.bybit.com/v5/market/tickers?category=linear&symbol={s}USDT", timeout=5).json()
            price = float(r['result']['list'][0]['lastPrice'])
            change = float(r['result']['list'][0]['price24hPcnt']) * 100
            return price, change
        except: return 0.0, 0.0

    # --- 4. YÖNETİCİ AYARLARI (SIDEBAR) ---
    with st.sidebar:
        st.header("⚙️ Portföy Yönetimi")
        user = st.text_input("Yatırımcı Adı", "ero7")
        kasa = st.number_input("Güncel Kasa (USD)", value=600.0)
        ana_para = 600.0
        hedef = 1500.0
        st.divider()
        if st.button("🔴 Güvenli Çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # Verileri Hazırla
    btc_p, btc_c = get_f("BTC")
    eth_p, eth_c = get_f("ETH")
    sol_p, sol_c = get_f("SOL")
    kar_oranı = ((kasa - ana_para) / ana_para) * 100

    # --- 5. ANA EKRAN ---
    st.title("🛡️ OG Trade Discipline Radar")
    st.caption(f"Yatırımcı: **{user}** | Sistem Durumu: **Aktif ✅**")

    # Metrik Kartları
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 TOPLAM KASA", f"${kasa:,.1f}", f"%{kar_oranı:+.1f}")
    c2.metric("🟠 BTC/USDT", f"${btc_p:,.1f}", f"{btc_c:+.2f}%")
    c3.metric("🔵 ETH/USDT", f"${eth_p:,.1f}", f"{eth_c:+.2f}%")
    c4.metric("🟣 SOL/USDT", f"${sol_p:,.1f}", f"{sol_c:+.2f}%")

    st.divider()

    # Hedef Barı
    st.subheader("🎯 Finansal Hedef İlerlemesi")
    progress = min(kasa/hedef, 1.0)
    st.progress(progress)
    st.write(f"Hedefe Kalan: **${max(hedef-kasa, 0):.1f}** | Başarı Oranı: **%{(kasa/hedef)*100:.1f}**")

    # --- 6. YASAL ZIRH (FOOTER) ---
    st.divider()
    st.error("⚠️ **ÖNEMLİ YASAL UYARI**")
    st.caption("""
    Bu yazılım sadece **kişisel takip, disiplin ve eğitim** amaçlıdır. İçerisinde yer alan veriler Bybit üzerinden çekilen anlık piyasa fiyatlarıdır. 
    Bu panelde yer alan hiçbir bilgi, grafik veya hesaplama **YATIRIM DANIŞMANLIĞI VEYA TAVSİYESİ KAPSAMINDA DEĞİLDİR.** Kullanıcı, finansal piyasalarda işlem yaparken tüm riskin kendisine ait olduğunu peşinen kabul eder.
    """)

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")