import streamlit as st
from datetime import datetime
import pandas as pd
import textwrap
import streamlit.components.v1 as components

try:
    import yfinance as yf
except:
    yf = None

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core",
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

        if "key" not in df.columns or "value" not in df.columns:
            raise Exception("Google Sheets tablosunda key/value kolonları yok")

        df = df.dropna(subset=["key"])
        df["key"] = df["key"].astype(str).str.strip()
        df["value"] = df["value"].fillna("").astype(str).str.strip()
        df = df[df["key"] != ""]

        return dict(zip(df["key"], df["value"]))

    except Exception as e:
        print("DATA ERROR:", e)
        return {"kasa": "600.0", "ana_para": "600.0"}

# --- YARDIMCI FONKSİYONLAR ---
def get_num(data, key, default=0.0):
    try:
        val = data.get(key, default)
        if val is None or str(val).strip() == "":
            return float(default)
        return float(str(val).replace(",", ".").strip())
    except:
        return float(default)

def get_str(data, key, default=""):
    try:
        val = data.get(key, default)
        if val is None:
            return default
        return str(val).strip()
    except:
        return default

def fmt_money_usd(x):
    return f"${x:,.2f}"

def fmt_money_try(x):
    return f"₺{x:,.0f}"

def fmt_unit_value(qty, unit):
    unit = (unit or "").strip().lower()
    if unit in ["adet", "lot"]:
        return f"{qty:,.4f}".rstrip("0").rstrip(".")
    elif unit == "gr":
        return f"{qty:,.2f} gr"
    elif unit == "usd":
        return f"${qty:,.0f}"
    elif unit == "eur":
        return f"€{qty:,.2f}"
    else:
        return f"{qty:,.4f}".rstrip("0").rstrip(".")

# --- RÜTBE FONKSİYONU ---
def rutbe_getir(puan_str):
    try:
        p = int(float(puan_str))
    except:
        p = 0
    if p <= 3:
        return "Hılez"
    elif p <= 6:
        return "Tecrübeli Hılez"
    elif p <= 9:
        return "Bu Abi Biri Mi?"
    elif p <= 11:
        return "Miço"
    else:
        return "Grand Miço"

live_vars = get_live_data()

kasa = float(get_num(live_vars, "kasa", 600))
ana_para = float(get_num(live_vars, "ana_para", 600))
duyuru_metni = get_str(live_vars, "duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")

# --- KİŞİSEL KASA VERİLERİ (Sadece Oguzo) ---
og_kasa = float(get_num(live_vars, "oguzo_kasa", kasa / 3))

# --- RÜTBE VERİLERİ (Sadece Oguzo) ---
og_p = get_str(live_vars, "oguzo_puan", "0")

aktif_soru_1 = get_str(live_vars, "aktif_soru", "yeni soru yakında...")
aktif_soru_2 = get_str(live_vars, "aktif_soru2", "yeni soru yakında...")

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(get_num(live_vars, "w1_sonuc", -100))
w2_kar = float(get_num(live_vars, "w2_sonuc", 553))
w3_kar = float(get_num(live_vars, "w3_sonuc", 879))
w4_kar = float(get_num(live_vars, "w4_sonuc", -100))
w5_kar = float(get_num(live_vars, "w5_sonuc", -100))
w6_kar = float(get_num(live_vars, "w6_sonuc", -100))
w7_kar = float(get_num(live_vars, "w7_sonuc", 650))
w8_kar = float(get_num(live_vars, "w8_sonuc", -100))
w9_kar = float(get_num(live_vars, "w9_sonuc", -100))
w10_kar = float(get_num(live_vars, "w10_sonuc", -100))
toplam_bahis_kar = w1_kar + w2_kar + w3_kar + w4_kar + w5_kar + w6_kar + w7_kar + w8_kar + w9_kar + w10_kar

wr_oran = get_str(live_vars, "win_rate", "0")
son_islemler_raw = get_str(live_vars, "son_islemler", "Veri yok")

# --- 3. CSS STİLLERİ ---
common_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');

#MainMenu, footer, header, .stAppDeployButton {visibility: hidden;}
[data-testid="stSidebar"] svg, [data-testid="stHeaderActionElements"], .st-emotion-cache-10trblm {display: none !important;}
[data-testid="stSidebar"] span, [data-testid="stSidebar"] small {font-size: 0 !important; color: transparent !important;}
[data-testid="stSidebar"] p {font-size: 14px !important; color: #d1d1d1 !important; visibility: visible !important;}

section[data-testid="stSidebar"] {
    background-color: rgba(5, 5, 5, 0.95) !important;
    border-right: 1px solid rgba(204, 122, 0, 0.15);
    padding-top: 20px;
    min-width: 340px !important;
    max-width: 340px !important;
}

.stButton button, .stLinkButton a {
    width: 100% !important;
    background: rgba(204, 122, 0, 0.1) !important;
    border: 1px solid rgba(204, 122, 0, 0.3) !important;
    color: #cc7a00 !important;
    font-family: 'Orbitron' !important;
    padding: 12px !important;
    border-radius: 6px !important;
}

body, [data-testid="stAppViewContainer"], p, div, span, button, input {
    font-family: 'JetBrains Mono', monospace !important;
    color: #d1d1d1 !important;
}

.terminal-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    margin-bottom: 12px;
    line-height: 1.6;
    gap: 12px;
}

.industrial-card {
    background: rgba(15, 15, 15, 0.82) !important;
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.03) !important;
    border-top: 2px solid rgba(204, 122, 0, 0.4) !important;
    padding: 22px;
    margin-bottom: 20px;
    border-radius: 4px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    transition: all 0.25s ease;
}

.industrial-card:hover {
    transform: translateY(-3px);
    border-top-color: #ffae00 !important;
    background: rgba(21, 21, 21, 0.9) !important;
    box-shadow: 0 8px 22px rgba(204, 122, 0, 0.11);
}

.terminal-header {
    color: #8b8b8b;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    margin-bottom: 18px;
    border-left: 3px solid #cc7a00;
    padding-left: 12px;
}

.highlight {
    color: #FFFFFF !important;
    font-weight: 500;
    font-size: 14px;
    font-family: 'JetBrains Mono', monospace;
}

.val-std {
    font-size: 22px !important;
    font-weight: 800 !important;
    font-family: 'Orbitron';
}

.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: rgba(204, 122, 0, 0.03);
    border-bottom: 1px solid rgba(204, 122, 0, 0.2);
    padding: 10px 0;
    margin-bottom: 25px;
}

.ticker {
    display: flex;
    white-space: nowrap;
    animation: ticker 30s linear infinite;
}

.ticker-item {
    font-size: 12px;
    color: #cc7a00;
    letter-spacing: 4px;
    padding-right: 50%;
}

@keyframes ticker {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

.portfolio-hero {
    background: linear-gradient(180deg, rgba(18,18,18,0.92), rgba(10,10,10,0.92));
    border: 1px solid rgba(255,255,255,0.03);
    border-top: 2px solid rgba(204,122,0,0.75);
    border-radius: 4px;
    padding: 30px 24px 26px 24px;
    margin-bottom: 22px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.45);
}

.portfolio-hero-sub {
    font-size: 13px;
    color: #7a7a7a !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.portfolio-hero-main {
    font-size: 62px;
    line-height: 1;
    font-family: 'Orbitron', monospace !important;
    color: #e5e5e5 !important;
    font-weight: 900;
}

.asset-mini-title {
    font-size: 11px;
    color: #7d7d7d !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.asset-mini-value {
    font-size: 22px;
    color: #f3f3f3 !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700;
}
</style>
"""

login_bg_css = """
<style>
.stApp {
    background: radial-gradient(circle at 20% 30%, rgba(204,122,0,0.15), transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(0,255,65,0.10), transparent 40%),
                linear-gradient(135deg, #050505 0%, #0b0b0b 40%, #111111 100%) !important;
    background-attachment: fixed !important;
}

div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    background: rgba(10, 10, 10, 0.75) !important;
    backdrop-filter: blur(30px) !important;
    padding: 55px 35px !important;
    border-radius: 18px !important;
    border: 1px solid rgba(204, 122, 0, 0.35) !important;
    box-shadow: 0 0 40px rgba(204,122,0,0.15);
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    z-index: 9999 !important;
    width: 360px !important;
}

input[type="password"] {
    background: rgba(0, 0, 0, 0.5) !important;
    border: 1px solid rgba(204, 122, 0, 0.6) !important;
    text-align: center !important;
    color: #cc7a00 !important;
    font-size: 26px !important;
    letter-spacing: 12px !important;
    padding: 12px !important;
    border-radius: 10px !important;
}

.stButton { visibility: hidden; height: 0; margin: 0; padding: 0; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w10_matches = """<div class='terminal-row'><span>trabzonspor - gala</span><span class='highlight'>xxx</span></div><div class='terminal-row'><span>stuttgart - bvb</span><span class='highlight'>xxx</span></div><div class='terminal-row'><span>newcastle - maç yok</span><span class='highlight'>---</span></div><div class='terminal-row'><span>manchester city - liverpool</span><span class='highlight'>xxx</span></div><div class='terminal-row'><span>fenerbahçe - beşiktaş</span><span class='highlight'>xxx</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran:xxx</span><span>Tutar: 100 USD</span></div>"""
w10_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>⏳ W10 KUPONU (BEKLİYOR)</div>{w10_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇ BEKLENİYOR 🔜</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        pwd = st.text_input("PIN", type="password", placeholder="----", label_visibility="collapsed")
        if pwd:
            if pwd == "1608":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED")
        return False
    return True

# --- PORTFÖY V2 YARDIMCI FONKSİYONLAR (Sadece Oguzo İçin) ---
def discover_dynamic_instruments(data, users=["oguzo"]):
    instrument_codes = set()
    for key in data.keys():
        if not isinstance(key, str): continue
        key = key.strip()
        if key.startswith("price_"):
            code = key.replace("price_", "", 1).strip()
            if code: instrument_codes.add(code)

    instruments = []
    for code in instrument_codes:
        label = get_str(data, f"label_{code}", code.upper())
        unit = get_str(data, f"unit_{code}", "adet")
        currency = get_str(data, f"currency_{code}", "TRY").upper()
        order = get_num(data, f"order_{code}", 999)
        show = int(get_num(data, f"show_{code}", 1))
        price = get_num(data, f"price_{code}", 0)

        if show == 0: continue
        if not any(f"{u}_{code}" in data for u in users): continue

        instruments.append({"code": code, "label": label, "unit": unit, "currency": currency, "price": price, "order": order})
    return sorted(instruments, key=lambda x: (x["order"], x["label"]))

def convert_to_try_and_usd(quantity, price, currency, usdtry):
    currency = (currency or "TRY").upper()
    if currency == "USD":
        total_usd = quantity * price
        total_try = total_usd * usdtry
    else:
        total_try = quantity * price
        total_usd = total_try / usdtry if usdtry > 0 else 0
    return total_try, total_usd

def build_user_portfolio(data, user, instruments, usdtry):
    rows = []
    for ins in instruments:
        direct_key = f"{user}_{ins['code']}"
        qty = get_num(data, direct_key, 0)
        total_try, total_usd = convert_to_try_and_usd(qty, ins["price"], ins["currency"], usdtry)
        rows.append({
            "code": ins["code"], "label": ins["label"], "unit": ins["unit"],
            "currency": ins["currency"], "price": ins["price"], "quantity": qty,
            "total_try": total_try, "total_usd": total_usd, "order": ins["order"]
        })
    df = pd.DataFrame(rows)
    return df.sort_values(["order", "label"]).reset_index(drop=True) if not df.empty else df

# --- ANA PROGRAM ---
if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown(f"### 🛡️ OG CORE v2.0")
    st.sidebar.markdown(f"**Hoş geldin, oguzo**")
    st.sidebar.markdown(f"Rütbe: {rutbe_getir(og_p)}")
    
    menu = st.sidebar.radio("SİSTEM ÜNİTELERİ", ["KASA & BAHİS", "ULTRA ATAK (PORTFÖY)"])

    usd_try_rate = get_num(live_vars, "usd_try", 34.50)

    if menu == "KASA & BAHİS":
        st.markdown(f"<div class='ticker-wrap'><div class='ticker'><div class='ticker-item'>{duyuru_metni}</div></div></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>TOPLAM KASA</div><div class='val-std'>{fmt_money_usd(kasa)}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>OGUZO ÖZEL KASA</div><div class='val-std'>{fmt_money_usd(og_kasa)}</div></div>", unsafe_allow_html=True)

        st.markdown("### 🏟️ AKTİF KUPONLAR")
        st.markdown(w10_coupon_html, unsafe_allow_html=True)

    elif menu == "ULTRA ATAK (PORTFÖY)":
        st.markdown("## 🚀 ULTRA ATAK / OGUZO")
        
        dyn_instruments = discover_dynamic_instruments(live_vars, ["oguzo"])
        df_og = build_user_portfolio(live_vars, "oguzo", dyn_instruments, usd_try_rate)
        
        total_og_usd = df_og["total_usd"].sum() if not df_og.empty else 0
        
        st.markdown(f"""
        <div class='portfolio-hero'>
            <div class='portfolio-hero-sub'>TOPLAM VARLIK DEĞERİ</div>
            <div class='portfolio-hero-main'>{fmt_money_usd(total_og_usd)}</div>
        </div>
        """, unsafe_allow_html=True)

        if not df_og.empty:
            for _, row in df_og[df_og["quantity"] > 0].iterrows():
                st.markdown(f"""
                <div class='industrial-card'>
                    <div class='terminal-row'>
                        <span class='highlight'>{row['label']}</span>
                        <span>{fmt_unit_value(row['quantity'], row['unit'])}</span>
                    </div>
                    <div class='terminal-row'>
                        <span style='color:#8b8b8b'>Değer:</span>
                        <span class='highlight'>{fmt_money_usd(row['total_usd'])}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
