import streamlit as st
import yfinance as yf
from datetime import datetime

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="OG VIP Radar", page_icon="🛡️", layout="wide")

# --- 1. GÜVENLİK ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "og2026": 
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.title("🔐 OG VIP Erişim Paneli")
        st.text_input("Şifre", type="password", on_change=password_entered, key="password")
        return False
    return True

if check_password():
    # --- 2. GÖRSEL TASARIM (DARK PREMIUM) ---
    st.markdown("""
        <style>
        .main { background-color: #0e1117; }
        div[data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #00ff41 !important; }
        .stProgress > div > div > div > div { background-color: #00ff41; }
        .member-card { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
        </style>
        """, unsafe_allow_html=True)

    # --- 3. SIDEBAR & VERİ GİRİŞİ ---
    with st.sidebar:
        st.header("⚙️ Portföy Kontrol")
        kasa = st.number_input("Güncel Kasa (USD)", value=1200.0, step=0.1) # Terminaldeki verini buraya yaz
        st.divider()
        st.info(f"🕒 Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")
        if st.button("🔴 Güvenli Çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    # Piyasa Verileri
    data = yf.download(["BTC-USD", "ETH-USD", "SOL-USD"], period="1d", interval="1m", progress=False)['Close'].iloc[-1]
    
    # --- 4. DASHBOARD ÜST KISIM ---
    st.title("🛡️ OG Trade Discipline Radar")
    
    col1, col2, col3, col4 = st.columns(4)
    ana_para = 600.0
    net_kar = kasa - ana_para
    kar_orani = (net_kar / ana_para) * 100
    
    col1.metric("💰 TOPLAM KASA", f"${kasa:,.2f}", f"%{kar_orani:+.1f}")
    col2.metric("🟠 BTC/USDT", f"${data['BTC-USD']:,.1f}")
    col3.metric("🔵 ETH/USDT", f"${data['ETH-USD']:,.1f}")
    col4.metric("🟣 SOL/USDT", f"${data['SOL-USD']:,.1f}")

    st.divider()

    # --- 5. EKİP KÂR DAĞITIMI (YENİ TASARIM) ---
    st.subheader("👥 Ekip Kâr Analizi")
    kisi_basi_kar = net_kar / 3 if net_kar > 0 else 0.0
    toplam_alacak = 200 + kisi_basi_kar
    
    m1, m2, m3 = st.columns(3)
    for col, name in zip([m1, m2, m3], ["oguzo", "ero7", "fybey"]):
        with col:
            st.markdown(f"""
            <div class="member-card">
                <h3 style='margin:0; color:#8b949e;'>{name.upper()}</h3>
                <p style='margin:0; font-size:1.2rem; color:#00ff41;'>Alacak: ${toplam_alacak:,.2f}</p>
                <p style='margin:0; font-size:0.8rem; color:#8b949e;'>Net Kar Payı: ${kisi_basi_kar:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- 6. HEDEF ANALİZİ (YENİ TASARIM) ---
    st.subheader("🎯 Finansal Hedef Stratejisi")
    hedef = 1500.0
    progress = min(max(kasa/hedef, 0.0), 1.0)
    
    h1, h2 = st.columns([2, 1])
    with h1:
        st.progress(progress)
        st.caption(f"Hedefe Gidiş: %{progress*100:.1f}")
    with h2:
        kalan = max(hedef - kasa, 0)
        st.warning(f"Hedefe Kalan: **${kalan:,.1f}**")

    # Alt Bilgi Kartları
    c1, c2, c3 = st.columns(3)
    c1.write(f"📈 **Büyüme Durumu:** {'🔥 Şahlanıyor' if kar_orani > 10 else '💎 Sabit'}")
    c2.write(f"🚀 **1500$ Hedefi:** %{((kasa/1500)*100):.1f} Tamamlandı")
    c3.write(f"🛡️ **Disiplin Puanı:** 10/10")

    st.caption("Powered by OG Core - 2026 Discipline is Profit.")
