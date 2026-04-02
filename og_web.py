import streamlit as st
import pandas as pd

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core Elite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. VERİ BAĞLANTISI ---
@st.cache_data(ttl=20)
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
        df = df.dropna(subset=["key"])
        df["key"] = df["key"].astype(str).str.strip()
        df["value"] = df["value"].fillna("").astype(str).str.strip()
        return dict(zip(df["key"], df["value"]))
    except:
        return {"kasa": "600.0", "oguzo_kasa": "200.0"}

# Yardımcı Fonksiyonlar
def get_num(data, key, default=0.0):
    try: return float(str(data.get(key, default)).replace(",", ".").strip())
    except: return float(default)

def fmt_money_usd(x): return f"${x:,.2f}"

# --- 3. YENİ NESİL CSS (CYBER-DESIGN) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Orbitron:wght@400;900&display=swap');

/* Genel Arka Plan */
.stApp {
    background-color: #080808 !important;
    color: #e0e0e0 !important;
}

/* Sidebar Tasarımı */
[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid #cc7a0033;
}

/* Kart Tasarımları */
.cyber-card {
    background: linear-gradient(145deg, #0f0f0f, #151515);
    border: 1px solid #222;
    border-left: 4px solid #cc7a00;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 15px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

.cyber-card:hover {
    border-left: 4px solid #ffae00;
    box-shadow: 0 0 20px rgba(204, 122, 0, 0.2);
    transform: translateY(-2px);
}

/* Başlıklar */
.stat-label {
    font-size: 11px;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.stat-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 24px;
    color: #cc7a00;
    font-weight: 900;
}

/* Portföy Hero Alanı */
.hero-box {
    background: radial-gradient(circle at top right, #cc7a001a, transparent), #0f0f0f;
    border: 1px solid #cc7a0044;
    padding: 40px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 30px;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 50px;
    color: #fff;
    text-shadow: 0 0 15px rgba(204, 122, 0, 0.4);
}

/* Gizlemeler */
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Verileri Çek
live_vars = get_live_data()
kasa = get_num(live_vars, "kasa", 600)
og_kasa = get_num(live_vars, "oguzo_kasa", 200)
og_p = str(live_vars.get("oguzo_puan", "0"))

# Sidebar
st.sidebar.markdown("<h2 style='color:#cc7a00; font-family:Orbitron;'>OG CORE</h2>", unsafe_allow_html=True)
st.sidebar.write(f"Kullanıcı: **oguzo**")
st.sidebar.write(f"Puan: `{og_p}`")
menu = st.sidebar.radio("NAVİGASYON", ["ANA ÜS", "VARLIKLAR"])

if menu == "ANA ÜS":
    st.markdown("<div class='hero-box'><div class='stat-label'>TOPLAM KASA DEĞERİ</div><div class='hero-title'>" + fmt_money_usd(kasa) + "</div></div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div class='cyber-card'><div class='stat-label'>OGUZO ÖZEL KASA</div><div class='stat-value'>{fmt_money_usd(og_kasa)}</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='cyber-card'><div class='stat-label'>SİSTEM DURUMU</div><div class='stat-value' style='color:#00ff41;'>ONLINE</div></div>", unsafe_allow_html=True)

elif menu == "VARLIKLAR":
    st.markdown("<h2 style='font-family:Orbitron;'>🚀 VARLIK YÖNETİMİ</h2>", unsafe_allow_html=True)
    
    # Örnek Varlık Listeleme (Sadece Oguzo için dinamik yapı)
    varliklar = [
        {"isim": "USD NAKİT", "deger": get_num(live_vars, "oguzo_usd", 0), "birim": "$"},
        {"isim": "GRAM ALTIN", "deger": get_num(live_vars, "oguzo_altin", 0), "birim": "gr"},
        {"isim": "BTC", "deger": get_num(live_vars, "oguzo_btc", 0), "birim": "BTC"}
    ]
    
    # 3'lü grid düzeni
    cols = st.columns(3)
    for i, v in enumerate(varliklar):
        with cols[i % 3]:
            st.markdown(f"""
            <div class='cyber-card'>
                <div class='stat-label'>{v['isim']}</div>
                <div class='stat-value'>{v['deger']} <span style='font-size:12px; color:#666;'>{v['birim']}</span></div>
            </div>
            """, unsafe_allow_html=True)
