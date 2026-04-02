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

# --- 2. VERİ BAĞLANTISI (GOOGLE SHEETS / CSV EXPORT) ---
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

# --- KİŞİSEL KASA VERİLERİ ---
og_kasa = float(get_num(live_vars, "oguzo_kasa", kasa / 3))
er_kasa = float(get_num(live_vars, "ero7_kasa", kasa / 3))
fy_kasa = float(get_num(live_vars, "fybey_kasa", kasa / 3))

# --- RÜTBE VERİLERİ ---
og_p = get_str(live_vars, "oguzo_puan", "0")
er_p = get_str(live_vars, "ero7_puan", "0")
fy_p = get_str(live_vars, "fybey_puan", "0")

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

.love-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 0 25px rgba(255,105,180,0.25);
    transition: all 0.25s ease;
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

.equal-card {
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

/* --- PORTFÖY V2 --- */
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

.portfolio-hero-try {
    margin-top: 12px;
    font-size: 18px;
    color: #8c8c8c !important;
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

.asset-mini-sub {
    margin-top: 8px;
    font-size: 12px;
    color: #8d8d8d !important;
}

.info-strip {
    display:flex;
    justify-content:space-between;
    gap:18px;
    flex-wrap:wrap;
    font-size:12px;
    color:#7a7a7a;
    letter-spacing:1px;
    padding-top: 4px;
}

.info-strip span strong {
    color:#c9c9c9 !important;
    font-weight: 500;
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

# --- LOVE FUND CSS ---
love_css = """
<style>
.love-shell {
    position: relative;
}

.love-shell::before {
    content: "";
    position: absolute;
    top: -20px;
    right: 40px;
    width: 240px;
    height: 240px;
    background: radial-gradient(circle, rgba(255,105,180,0.12), transparent 65%);
    filter: blur(18px);
    pointer-events: none;
}

.love-shell::after {
    content: "";
    position: absolute;
    bottom: 40px;
    left: 20px;
    width: 180px;
    height: 180px;
    background: radial-gradient(circle, rgba(255,182,193,0.10), transparent 70%);
    filter: blur(18px);
    pointer-events: none;
}

.love-wrap {
    background: linear-gradient(135deg, rgba(255,182,193,0.14), rgba(255,105,180,0.11), rgba(255,20,147,0.08));
    border: 1px solid rgba(255, 182, 193, 0.20);
    border-top: 2px solid rgba(255, 105, 180, 0.72);
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 18px;
    box-shadow: 0 10px 30px rgba(255, 105, 180, 0.10);
    min-height: 188px;
}

.love-cover {
    min-height: 188px;
    border-radius: 18px;
    padding: 22px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background:
        radial-gradient(circle at top right, rgba(255,182,193,0.16), transparent 35%),
        radial-gradient(circle at bottom left, rgba(255,105,180,0.14), transparent 40%),
        linear-gradient(135deg, rgba(255,192,203,0.08), rgba(255,20,147,0.08), rgba(20,10,20,0.95));
    border: 1px solid rgba(255, 182, 193, 0.14);
    border-top: 2px solid rgba(255, 105, 180, 0.38);
    box-shadow: 0 8px 24px rgba(255, 105, 180, 0.08);
    position: relative;
    overflow: hidden;
    margin-bottom: 18px;
}

.love-cover::after {
    content: "❤";
    position: absolute;
    right: 16px;
    bottom: 6px;
    font-size: 34px;
    color: rgba(255, 182, 193, 0.08);
}

.love-cover-mini {
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #ffc1db !important;
}

.love-cover-main {
    font-family: 'Orbitron', monospace !important;
    font-size: 34px;
    font-weight: 800;
    color: #fff4f8 !important;
    line-height: 1;
}

.love-cover-sub {
    font-size: 11px;
    color: #ffd3e5 !important;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.love-title {
    font-family: 'Orbitron', monospace !important;
    font-size: 12px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #ff9ac3 !important;
    margin-bottom: 12px;
}

.love-big {
    font-family: 'Orbitron', monospace !important;
    font-size: 44px;
    line-height: 1;
    font-weight: 900;
    color: #fff2f7 !important;
}

.love-sub {
    font-size: 13px;
    color: #ffd0e1 !important;
    margin-top: 10px;
}

.love-card {
    background: rgba(255, 182, 193, 0.08) !important;
    border: 1px solid rgba(255, 182, 193, 0.14) !important;
    border-top: 2px solid rgba(255, 105, 180, 0.42) !important;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0 4px 16px rgba(255, 20, 147, 0.08);
    transition: all 0.25s ease;
}

.love-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 0 25px rgba(255,105,180,0.16);
}

.love-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #ffb3d0 !important;
    margin-bottom: 10px;
}

.love-value {
    font-size: 24px;
    font-weight: 800;
    font-family: 'Orbitron', monospace !important;
    color: #fff5fa !important;
}

.love-note {
    color: #ffe3ee !important;
    font-size: 14px;
    line-height: 1.7;
}

.love-progress-outer {
    width: 100%;
    height: 14px;
    background: rgba(255,255,255,0.05);
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid rgba(255, 182, 193, 0.15);
}

.love-progress-inner {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #ff82ba, #ffb5d3, #ffe3ef);
    box-shadow: 0 0 16px rgba(255, 105, 180, 0.22);
}

.love-mini {
    font-size: 12px;
    color: #ffcade !important;
    margin-top: 8px;
}

.love-soft {
    font-size: 12px;
    color: #ffcfe0 !important;
    margin-top: 6px;
}

.love-pill {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #ffe6f0 !important;
    border: 1px solid rgba(255, 182, 193, 0.16);
    background: rgba(255,255,255,0.04);
}

.love-tiny-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

div[data-testid="stSidebar"] .love-side {
    color: #ffb6d8 !important;
}
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w10_matches = """<div class='terminal-row'><span>trabzonspor - gala</span><span class='highlight'>xxx</span></div><div class='terminal-row'><span>stuttgart - bvb</span><span class='highlight'>xxx</span></div><div class='terminal-row'><span>newcastle - maç yok</span><span class='highlight'>---</span></div><div class='terminal-row'><span>manchester city - liverpool</span><span class='highlight'>xxx</span></div><div class='terminal-row'><span>fenerbahçe - beşiktaş</span><span class='highlight'>xxx</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran:xxx</span><span>Tutar: 100 USD</span></div>"""
w9_matches = """<div class='terminal-row'><span>gala - maç oynamıyor</span><span class='highlight'>-</span></div><div class='terminal-row'><span>bvb - hamburg</span><span class='highlight'>bvb +2 & iy +1 ❌</span></div><div class='terminal-row'><span>newcastle - sunderland</span><span class='highlight'>newcastle +2</span></div><div class='terminal-row'><span>brighton - liverpool</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>fenerbahçe - gaziantep</span><span class='highlight'>fenerbahçe w & +3 ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 5.09</span><span>Tutar: 100 USD</span></div>"""
w8_matches = """<div class='terminal-row'><span>gala - başakşehir</span><span class='highlight'>gala 1x & +2 ✅</span></div><div class='terminal-row'><span>bvb - augsburg</span><span class='highlight'>bvb +2 & iy +1 ✅</span></div><div class='terminal-row'><span>chelsea - newcastle</span><span class='highlight'>kg ❌</span></div><div class='terminal-row'><span>liverpool - spurs</span><span class='highlight'>+3 ❌</span></div><div class='terminal-row'><span>karagümrük - fenerbahçe</span><span class='highlight'>fenerbahçe w & +2 ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 7.59</span><span>Tutar: 100 USD</span></div>"""
w7_matches = """<div class='terminal-row'><span>beşiktaş - gala</span><span class='highlight'>gala +1 ✅</span></div><div class='terminal-row'><span>köln - bvb</span><span class='highlight'>bvb +2 ✅</span></div><div class='terminal-row'><span>newcastle - manchester united</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>wolwes - liverpool</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>fenerbahçe - samsunspor</span><span class='highlight'>fenerbahçe w & +2 ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 6.50</span><span>Tutar: 100 USD</span></div>"""
w6_matches = """<div class='terminal-row'><span>gala - alanyasapor</span><span class='highlight'>gala w & +2 ✅</span></div><div class='terminal-row'><span>bvb - bayern</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>newcastle - everton</span><span class='highlight'>newcastle +2 ✅</span></div><div class='terminal-row'><span>liverpool - west ham</span><span class='highlight'>live w & 2+ ✅</span></div><div class='terminal-row'><span>antalyasapor - fenerbahçe </span><span class='highlight'>fenerbahçe w & iy +1 & +2 ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 8.89</span><span>Tutar: 100 USD</span></div>"""
w5_matches = """<div class='terminal-row'><span>konyaspor - gala</span><span class='highlight'>gala w & +2 ❌</span></div><div class='terminal-row'><span>leipzig - bvb</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>man city - newcastle</span><span class='highlight'>x1 & +2 ✅</span></div><div class='terminal-row'><span>forest - liverpool</span><span class='highlight'>live 2+ ❌</span></div><div class='terminal-row'><span>fenerbahçe - kasımpaşa</span><span class='highlight'>fenerbahçe w & iy +1 & +2 ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 8.26</span><span>Tutar: 100 USD</span></div>"""
w4_matches = """<div class='terminal-row'><span>gala - eyüpspor</span><span class='highlight'>gala w & 2+ ✅</span></div><div class='terminal-row'><span>sunderland - liverpool</span><span class='highlight'>kg ❌</span></div><div class='terminal-row'><span>bvb - mainz 05</span><span class='highlight'>bvb 1x & bvb 2+ & iy +1 ✅</span></div><div class='terminal-row'><span>trabzonspor - fenerbahçe</span><span class='highlight'>fb 2+ ✅</span></div><div class='terminal-row'><span>spurs - newcastle</span><span class='highlight'>kg ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Toplam Oran: 11.00</span><span>Tutar: 100 USD</span></div>"""
w3_matches = """<div class='terminal-row'><span>wolfsburg - bvb</span><span class='highlight'>bvb x2 & +2 ✅</span></div><div class='terminal-row'><span>newcastle - brentford</span><span class='highlight'>newcastle +2 ✅</span></div><div class='terminal-row'><span>rizespor - gala</span><span class='highlight'>gala w & +2 ✅</span></div><div class='terminal-row'><span>liverpool - man city</span><span class='highlight'>lıve +1 ✅</span></div><div class='terminal-row'><span>fenerbahçe - gençlerbirliği</span><span class='highlight'>fenerbahçe w & +3 ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>gala - kayserispor</span><span style='color:#00ff41;'>gala w & iy +1 & 2+ ✅</span></div><div class='terminal-row'><span>liverpool - newcastle</span><span style='color:#00ff41;'>+2 & liverpool 1x ✅</span></div><div class='terminal-row'><span>bvb - heidenheim</span><span style='color:#00ff41;'>bvb w & iy +1 & 2+ ✅</span></div><div class='terminal-row'><span>kocaelispor - fenerbahçe</span><span style='color:#00ff41;'>fenerbahçe w & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>karagümrük - gala</span><span style='color:#ff4b4b;'>gala w & +2 ✅</span></div><div class='terminal-row'><span>bournemouth - liverpool</span><span style='color:#00ff41;'>kg ✅</span></div><div class='terminal-row'><span>union berlin - bvb</span><span style='color:#00ff41;'>iy +1 ✅</span></div><div class='terminal-row'><span>newcastle - aston villa</span><span style='color:#ff4b4b;'>newcastle +2 ❌</span></div><div class='terminal-row'><span>fenerbahçe - göztepe</span><span style='color:#ff4b4b;'>fenerbahçe w ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""

w10_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>⏳ W10 KUPONU (BEKLİYOR)</div>{w10_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇ BEKLENİYOR 🔜</span></div>"
w9_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>❌ W9 KUPONU (BAŞARISIZ)</div>{w9_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ❌</span></div>"
w8_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>❌ W8 KUPONU (BAŞARISIZ)</div>{w8_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ❌</span></div>"
w7_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W7 KUPONU (BAŞARILI)</div>{w7_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w6_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>❌ W6 KUPONU (BAŞARISIZ)</div>{w6_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ❌</span></div>"
w5_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>❌ W5 KUPONU (BAŞARISIZ)</div>{w5_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ❌</span></div>"
w4_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>❌ W4 KUPONU (BAŞARISIZ)</div>{w4_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ❌</span></div>"
w3_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W3 KUPONU (BAŞARILI)</div>{w3_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}<span style='color:#ff4b4b; font-weight:bold;'>SONUÇLANDI ❌</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if "love_password_correct" not in st.session_state:
    st.session_state["love_password_correct"] = False

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

def check_love_password():
    st.markdown(love_css, unsafe_allow_html=True)

    if not st.session_state["love_password_correct"]:
        st.markdown(
            """
            <div class='love-wrap'>
                <div class='love-title'>AŞKIMLA ÖZEL FON ALANIMIZ</div>
                <div class='love-big'>💗 LOVE FUND</div>
                <div class='love-sub'>Bu sekme yalnızca bize özel ikinci şifre ile açılır.</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        love_pwd = st.text_input(
            "Love PIN",
            type="password",
            placeholder="sevgili olduğumuz tarih gün.ay",
            key="love_pwd_input"
        )

        if love_pwd:
            if love_pwd == "1701":
                st.session_state["love_password_correct"] = True
                st.rerun()
            else:
                st.error("yanlış şifre aşkım :(")

        return False

    return True

# --- PORTFÖY V2 YARDIMCI FONKSİYONLAR ---
def discover_dynamic_instruments(data, users):
    instrument_codes = set()

    for key in data.keys():
        if not isinstance(key, str):
            continue
        key = key.strip()
        if not key:
            continue
        if key.startswith("price_"):
            code = key.replace("price_", "", 1).strip()
            if code:
                instrument_codes.add(code)

    instruments = []
    for code in instrument_codes:
        label = get_str(data, f"label_{code}", code.upper())
        unit = get_str(data, f"unit_{code}", "adet")
        currency = get_str(data, f"currency_{code}", "TRY").upper()
        order = get_num(data, f"order_{code}", 999)
        show = int(get_num(data, f"show_{code}", 1))
        price = get_num(data, f"price_{code}", 0)

        if show == 0:
            continue

        has_any_user_key = any(f"{u}_{code}" in data for u in users)
        if not has_any_user_key:
            continue

        instruments.append({
            "code": code,
            "label": label,
            "unit": unit,
            "currency": currency,
            "price": price,
            "order": order,
        })

    return sorted(instruments, key=lambda x: (x["order"], x["label"]))

def build_legacy_fallback_instruments(data):
    return [
        {
            "code": "usd_cash",
            "label": "NAKİT",
            "unit": "USD",
            "currency": "USD",
            "price": 1.0,
            "order": 1,
            "legacy_map": {"oguzo": "oguzo_usd", "ero7": "ero7_usd", "fybey": "fybey_usd"},
        },
        {
            "code": "gram_altin",
            "label": "GRAM ALTIN",
            "unit": "gr",
            "currency": "TRY",
            "price": get_num(data, "gram_altin_fiyat", 7136),
            "order": 2,
            "legacy_map": {"oguzo": "oguzo_altin", "ero7": "ero7_altin", "fybey": "fybey_altin"},
        },
        {
            "code": "ceyrek",
            "label": "ÇEYREK",
            "unit": "adet",
            "currency": "TRY",
            "price": get_num(data, "ceyrek_altin_fiyat", 12417),
            "order": 3,
            "legacy_map": {"oguzo": "oguzo_ceyrek", "ero7": "ero7_ceyrek", "fybey": "fybey_ceyrek"},
        },
        {
            "code": "aft",
            "label": "AFT",
            "unit": "adet",
            "currency": "TRY",
            "price": get_num(data, "aft_fiyat_tl", 0.8295),
            "order": 4,
            "legacy_map": {"oguzo": "oguzo_aft_adet", "ero7": "ero7_aft_adet", "fybey": "fybey_aft_adet"},
        },
        {
            "code": "btc",
            "label": "BTC",
            "unit": "adet",
            "currency": "USD",
            "price": get_num(data, "btc_fiyat_usd", 84250),
            "order": 5,
            "legacy_map": {"oguzo": "oguzo_btc", "ero7": "ero7_btc", "fybey": "fybey_btc"},
        },
        {
            "code": "eth",
            "label": "ETH",
            "unit": "adet",
            "currency": "USD",
            "price": get_num(data, "eth_fiyat_usd", 2107.89),
            "order": 6,
            "legacy_map": {"oguzo": "oguzo_eth", "ero7": "ero7_eth", "fybey": "fybey_eth"},
        },
        {
            "code": "gumus",
            "label": "GÜMÜŞ",
            "unit": "gr",
            "currency": "TRY",
            "price": get_num(data, "gumus_fiyat_tl", 41.2),
            "order": 7,
            "legacy_map": {"oguzo": "oguzo_gumus", "ero7": "ero7_gumus", "fybey": "fybey_gumus"},
        },
    ]

def get_user_quantity_for_instrument(data, user, instrument):
    direct_key = f"{user}_{instrument['code']}"
    if direct_key in data:
        return get_num(data, direct_key, 0)

    if "legacy_map" in instrument and user in instrument["legacy_map"]:
        return get_num(data, instrument["legacy_map"][user], 0)

    return 0.0

def convert_to_try_and_usd(quantity, price, currency, usdtry):
    currency = (currency or "TRY").upper()

    if currency == "USD":
        total_usd = quantity * price
        total_try = total_usd * usdtry
    elif currency == "TRY":
        total_try = quantity * price
        total_usd = total_try / usdtry if usdtry > 0 else 0
    else:
        total_try = quantity * price
        total_usd = total_try / usdtry if usdtry > 0 else 0

    return total_try, total_usd

def build_user_portfolio(data, user, instruments, usdtry):
    rows = []

    for ins in instruments:
        qty = get_user_quantity_for_instrument(data, user, ins)
        total_try, total_usd = convert_to_try_and_usd(qty, ins["price"], ins["currency"], usdtry)

        rows.append({
            "code": ins["code"],
            "label": ins["label"],
            "unit": ins["unit"],
            "currency": ins["currency"],
            "price": ins["price"],
            "quantity": qty,
            "total_try": total_try,
            "total_usd": total_usd,
            "order": ins["order"],
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    return df.sort_values(["order", "label"]).reset_index(drop=True)

def render_top_asset_cards(df_nonzero):
    if df_nonzero.empty:
        return

    top_df = df_nonzero.sort_values("total_usd", ascending=False).head(4).copy()
    cols = st.columns(min(4, len(top_df)))

    for idx, (_, row) in enumerate(top_df.iterrows()):
        with cols[idx]:
            sub_value = fmt_money_usd(row["total_usd"]) if row["currency"] == "USD" else fmt_money_try(row["total_try"])
            qty_text = fmt_unit_value(row["quantity"], row["unit"])

            st.markdown(
                f"""
                <div class='industrial-card' style='text-align:center; min-height:118px;'>
                    <div class='asset-mini-title'>{row["label"]}</div>
                    <div class='asset-mini-value'>{qty_text}</div>
                    <div class='asset-mini-sub'>{sub_value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def render_secondary_asset_cards(df_nonzero):
    extra_df = df_nonzero.sort_values("total_usd", ascending=False).iloc[4:].copy()
    if extra_df.empty:
        return

    chunks = [extra_df.iloc[i:i+4] for i in range(0, len(extra_df), 4)]

    for chunk in chunks:
        cols = st.columns(len(chunk))
        for idx, (_, row) in enumerate(chunk.iterrows()):
            with cols[idx]:
                qty_text = fmt_unit_value(row["quantity"], row["unit"])
                sub_value = fmt_money_usd(row["total_usd"]) if row["currency"] == "USD" else fmt_money_try(row["total_try"])

                st.markdown(
                    f"""
                    <div class='industrial-card' style='text-align:center; min-height:105px; border-top:1px solid rgba(255,255,255,0.06) !important;'>
                        <div class='asset-mini-title'>{row["label"]}</div>
                        <div class='highlight' style='font-size:18px; margin-top:10px;'>{qty_text}</div>
                        <div class='asset-mini-sub'>{sub_value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

def render_breakdown_panel(df_nonzero):
    if df_nonzero.empty:
        st.markdown(
            """
            <div class='industrial-card'>
                <div class='terminal-header'>Varlık Kırılımı</div>
                <div class='highlight'>Aktif varlık bulunamadı.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    rows_html = ""

    for _, row in df_nonzero.iterrows():
        if row["currency"] == "USD":
            price_text = fmt_money_usd(row["price"])
            total_text = fmt_money_usd(row["total_usd"])
        else:
            price_text = fmt_money_try(row["price"])
            total_text = fmt_money_try(row["total_try"])

        qty_text = fmt_unit_value(row["quantity"], row["unit"])

        rows_html += f"""
        <div class="bd-row">
            <div class="bd-col bd-name">
                <div class="bd-title">{row["label"]}</div>
                <div class="bd-sub">{row["currency"]} bazlı / {row["unit"]}</div>
            </div>
            <div class="bd-col bd-qty">{qty_text}</div>
            <div class="bd-col bd-price">{price_text}</div>
            <div class="bd-col bd-total">{total_text}</div>
        </div>
        """

    total_usd = df_nonzero["total_usd"].sum()
    total_try = df_nonzero["total_try"].sum()

    html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: 'JetBrains Mono', monospace;
            color: #d1d1d1;
        }}

        .card {{
            background: rgba(15, 15, 15, 0.82);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-top: 2px solid rgba(204, 122, 0, 0.4);
            border-radius: 4px;
            padding: 22px;
            box-sizing: border-box;
        }}

        .header {{
            color: #8b8b8b;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2.8px;
            text-transform: uppercase;
            margin-bottom: 18px;
            border-left: 3px solid #cc7a00;
            padding-left: 12px;
        }}

        .head-row {{
            display: flex;
            justify-content: space-between;
            gap: 14px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            margin-bottom: 6px;
            color: #777;
            font-size: 11px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }}

        .bd-row {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 14px;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.045);
        }}

        .bd-col {{
            font-size: 13px;
        }}

        .bd-name {{
            flex: 1.6;
            min-width: 0;
        }}

        .bd-qty {{
            flex: 1;
            text-align: right;
            color: #d8d8d8;
        }}

        .bd-price {{
            flex: 1;
            text-align: right;
            color: #a8a8a8;
        }}

        .bd-total {{
            flex: 1.1;
            text-align: right;
            color: #ffffff;
            font-weight: 500;
        }}

        .bd-title {{
            color: #dedede;
            font-size: 14px;
            font-weight: 500;
        }}

        .bd-sub {{
            color: #7f7f7f;
            font-size: 12px;
            margin-top: 4px;
        }}

        .spacer {{
            height: 12px;
        }}

        .rule {{
            border: 0;
            height: 1px;
            background: rgba(255,255,255,0.06);
            margin: 8px 0 16px 0;
        }}

        .footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }}

        .footer-label {{
            font-weight: 700;
            color: #d0d0d0;
            font-size: 14px;
        }}

        .footer-total {{
            color: #cc7a00;
            font-family: 'Orbitron', monospace;
            font-size: 20px;
            font-weight: 800;
        }}
    </style>
    </head>
    <body>
        <div class="card">
            <div class="header">Varlık Kırılımı</div>

            <div class="head-row">
                <div style="flex:1.6;">Enstrüman</div>
                <div style="flex:1; text-align:right;">Miktar</div>
                <div style="flex:1; text-align:right;">Birim</div>
                <div style="flex:1.1; text-align:right;">Toplam</div>
            </div>

            {rows_html}

            <div class="spacer"></div>
            <hr class="rule">

            <div class="footer">
                <span class="footer-label">Toplam</span>
                <span class="footer-total">{fmt_money_usd(total_usd)} &nbsp;//&nbsp; {fmt_money_try(total_try)}</span>
            </div>
        </div>
    </body>
    </html>
    """

    row_count = len(df_nonzero)
    height = 145 + (row_count * 64)

    components.html(html, height=height, scrolling=False)

def render_allocation_panel(df_nonzero):
    if df_nonzero.empty:
        st.markdown(
            textwrap.dedent("""
                <div class='industrial-card'>
                    <div class='terminal-header'>Dağılım</div>
                    <div class='highlight'>Aktif enstrüman bulunamadı.</div>
                </div>
            """),
            unsafe_allow_html=True
        )
        return

    total_usd = df_nonzero["total_usd"].sum()
    if total_usd <= 0:
        total_usd = 1

    alloc_df = df_nonzero.sort_values("total_usd", ascending=False).copy()
    rows_html = ""

    for _, row in alloc_df.iterrows():
        pct = (row["total_usd"] / total_usd) * 100
        value_text = fmt_money_usd(row["total_usd"])

        rows_html += f"""
<div style='margin-bottom:14px;'>
    <div style='display:flex; justify-content:space-between; gap:12px; margin-bottom:7px; font-size:13px;'>
        <span style='color:#dedede;'>{row["label"]}</span>
        <span style='color:#cfcfcf;'>{pct:.1f}% &nbsp;//&nbsp; {value_text}</span>
    </div>
    <div style='width:100%; height:9px; border-radius:999px; background:rgba(255,255,255,0.05); overflow:hidden; border:1px solid rgba(255,255,255,0.03);'>
        <div style='height:100%; width:{pct:.2f}%; border-radius:999px; background:linear-gradient(90deg, rgba(204,122,0,0.95), rgba(255,174,0,0.95)); box-shadow:0 0 12px rgba(204,122,0,0.22);'></div>
    </div>
</div>
"""

    html = f"""
<div class='industrial-card'>
    <div class='terminal-header'>Dağılım Yüzdesi</div>
    {rows_html}
</div>
"""
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)

def render_info_strip(instruments, usdtry):
    parts = [f"<span>USD/TRY: <strong>₺{usdtry:.2f}</strong></span>"]

    for ins in instruments:
        price_text = fmt_money_usd(ins["price"]) if ins["currency"] == "USD" else fmt_money_try(ins["price"])
        parts.append(f"<span>{ins['label']}: <strong>{price_text}</strong></span>")

    html = f"<div class='info-strip'>{''.join(parts)}</div>"
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)

def render_portfolio_v2(data):
    st.markdown("<div class='terminal-header'>🏛️ PORTFÖY KOMUTA MERKEZİ</div>", unsafe_allow_html=True)

    users = ["oguzo", "ero7", "fybey"]
    user_labels = {"oguzo": "OGUZO", "ero7": "ERO7", "fybey": "FYBEY"}

    usdtry = get_num(data, "usdtry", 44.18)

    dynamic_instruments = discover_dynamic_instruments(data , users)
    instruments = dynamic_instruments if len(dynamic_instruments) > 0 else build_legacy_fallback_instruments(data)

    if len(instruments) == 0:
        st.error("Portföy enstrümanları bulunamadı.")
        return

    selected_user_label = st.selectbox("Kullanıcı Portföy Detayı:", [user_labels[u] for u in users])
    selected_user = [k for k, v in user_labels.items() if v == selected_user_label][0]

    df_user = build_user_portfolio(data, selected_user, instruments, usdtry)

    if df_user.empty:
        st.error("Seçilen kullanıcı için portföy verisi bulunamadı.")
        return

    total_usd = df_user["total_usd"].sum()
    total_try = df_user["total_try"].sum()
    df_nonzero = df_user[df_user["quantity"] > 0].copy()

    st.markdown(
        f"""
        <div class='portfolio-hero'>
            <div class='portfolio-hero-sub'>Toplam Portföy Değeri</div>
            <div class='portfolio-hero-main'>{fmt_money_usd(total_usd)}</div>
            <div class='portfolio-hero-try'>≈ {fmt_money_try(total_try)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    render_top_asset_cards(df_nonzero)
    render_secondary_asset_cards(df_nonzero)

    left, right = st.columns([1.18, 0.82])

    with left:
        render_breakdown_panel(df_nonzero)

    with right:
        render_allocation_panel(df_nonzero)

    st.divider()
    render_info_strip(instruments, usdtry)

# --- LOVE FUND RENDER ---
def render_love_fund(data):
    st.markdown(love_css, unsafe_allow_html=True)

    love_name = get_str(data, "love_name", "OGUZO & IKRA FUND")
    love_start = get_num(data, "love_start", 20000)
    love_target = get_num(data, "love_target", 40000)
    love_current = get_num(data, "love_current", love_start)
    love_monthly = get_num(data, "love_monthly", 3000)
    love_note = get_str(data, "love_note", "Birlikte kurduğumuz hedef için küçük ama düzenli adımlar atıyoruz.")
    love_goal_date = get_str(data, "love_goal_date", "2026 yaz")
    love_last_add = get_num(data, "love_last_add", 1000)
    love_status = get_str(data, "love_status", "aktif")
    love_focus = get_str(data, "love_focus", "yaz planı")

    goal_span = love_target - love_start
    current_gain = love_current - love_start

    progress = 0
    if goal_span > 0:
        progress = max(0, min(100, (current_gain / goal_span) * 100))

    remaining = max(0, love_target - love_current)

    months_left = 0
    if love_monthly > 0 and remaining > 0:
        months_left = int((remaining + love_monthly - 1) // love_monthly)

    st.markdown("<div class='love-shell'>", unsafe_allow_html=True)

    hero_left = st.container()

    with hero_left:
        st.markdown(
            f"""
            <div class='love-wrap'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap;'>
                    <div>
                        <div class='love-title'>Aşkımla Ortak Fon</div>
                        <div class='love-big'>₺{love_current:,.0f}</div>
                        <div class='love-sub'>Fon adı: {love_name}</div>
                        <div class='love-sub'>Başlangıç: ₺{love_start:,.0f} · Hedef: ₺{love_target:,.0f}</div>
                        <div class='love-sub'>Kalan: ₺{remaining:,.0f} · Hedef tarih: {love_goal_date}</div>
                    </div>
                    <div>
                        <span class='love-pill'>{love_status}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class='love-card'>
            <div class='love-label'>İlerleme</div>
            <div class='love-progress-outer'>
                <div class='love-progress-inner' style='width:{progress:.1f}%;'></div>
            </div>
            <div class='love-mini'>%{progress:.1f} tamamlandı</div>
            <div class='love-soft'>başlangıç ₺{love_start:,.0f} → hedef ₺{love_target:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class='love-card'>
                <div class='love-label'>Başlangıç</div>
                <div class='love-value'>₺{love_start:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class='love-card'>
                <div class='love-label'>Son Eklenen</div>
                <div class='love-value'>₺{love_last_add:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class='love-card'>
                <div class='love-label'>Kalan Tutar</div>
                <div class='love-value'>₺{remaining:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class='love-card'>
                <div class='love-label'>Toplam Hedef</div>
                <div class='love-value'>₺{love_target:,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    d1, d2 = st.columns([1.1, 0.9])

    with d1:
        eta_text = f"{months_left} ay kaldı" if months_left > 0 else "hedefe çok yakın"
        st.markdown(
            f"""
            <div class='love-card'>
                <div class='love-label'>Plan Özeti</div>
                <div class='love-tiny-grid'>
                    <div>
                        <div class='love-soft'>Aylık katkı</div>
                        <div class='love-value'>₺{love_monthly:,.0f}</div>
                    </div>
                    <div>
                        <div class='love-soft'>Tahmini süre</div>
                        <div class='love-value'>{eta_text}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with d2:
        st.markdown(
            f"""
            <div class='love-card'>
                <div class='love-label'>Not</div>
                <div class='love-note'>{love_note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("LOVE FUND OTURUMUNU KAPAT"):
        st.session_state["love_password_correct"] = False
        st.rerun()

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(common_css, unsafe_allow_html=True)
    st.markdown("<style>.stApp { background: #030303 !important; background-image: none !important; }</style>", unsafe_allow_html=True)
    st.markdown(
        f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>',
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown(
            "<h1 style='color:white; font-family:Orbitron; font-size:24px; letter-spacing:5px; text-align:center; margin-bottom:40px;'>OG CORE</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='margin-bottom:10px; color:#666; font-size:11px; letter-spacing:2px; font-weight:800;'>SİSTEM MODÜLLERİ</div>",
            unsafe_allow_html=True
        )

        page = st.radio(
            "Menu",
            ["⚡ ULTRA ATAK", "⚽ FORMLINE", "🎲 CHALLANGE", "📊 Portföy Takip", "💠 FTMO", "💗 LOVE FUND"],
            label_visibility="collapsed"
        )

        st.divider()
        st.markdown(
            "<div style='color:#666; font-size:11px; letter-spacing:2px; font-weight:800; margin-bottom:15px;'>📂 TERMİNAL ERİŞİMİ</div>",
            unsafe_allow_html=True
        )
        admin_pwd = st.text_input("PIN", type="password", placeholder="Admin PIN", label_visibility="collapsed")
        if admin_pwd == "0644":
            st.markdown(
                "<a href='https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit' target='_blank' style='text-decoration:none;'><div style='background:rgba(204, 122, 0, 0.2); border: 1px solid #cc7a00; color:#cc7a00; text-align:center; padding:10px; border-radius:4px; font-family:Orbitron; font-size:12px; font-weight:bold;'>VERİ TABANINA BAĞLAN</div></a>",
                unsafe_allow_html=True
            )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("SİSTEMDEN ÇIK"):
            st.session_state["password_correct"] = False
            st.session_state["love_password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK":
        st.markdown("<div class='terminal-header'>💰 Kişisel Kasa Dağılımı</div>", unsafe_allow_html=True)
        k1, k2, k3 = st.columns(3)

        with k1:
            st.markdown(
                f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Oguzo Bakiye</div><div class='highlight'>${og_kasa:,.2f}</div></div>",
                unsafe_allow_html=True
            )
        with k2:
            st.markdown(
                f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Ero7 Bakiye</div><div class='highlight'>${er_kasa:,.2f}</div></div>",
                unsafe_allow_html=True
            )
        with k3:
            st.markdown(
                f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>Fybey Bakiye</div><div class='highlight'>${fy_kasa:,.2f}</div></div>",
                unsafe_allow_html=True
            )

        st.divider()

        net_kar = kasa - ana_para
        current_pct = max(0, min(100, ((kasa - 600) / (1200 - 600)) * 100))

        st.markdown(
            f"""
            <div class='industrial-card'>
                <div class='terminal-header'>HEDEF YOLCULUĞU ($1.200)</div>
                <div style='background:#111; height:8px; border-radius:10px;'>
                    <div style='background:linear-gradient(90deg, #cc7a00, #ffae00); width:{current_pct}%; height:100%; border-radius:10px;'></div>
                </div>
                <div style='text-align:right; font-size:10px; color:#555; margin-top:5px;'>%{current_pct:.1f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>💎 KASA</div><div class='terminal-row'><span>TOPLAM</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>K/Z</span><span style='color:{'#00ff41' if net_kar >= 0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span></div></div>",
                unsafe_allow_html=True
            )

        with col2:
            try:
                if yf is not None:
                    btc = yf.Ticker("BTC-USD").history(period="1d")["Close"].iloc[-1]
                    eth = yf.Ticker("ETH-USD").history(period="1d")["Close"].iloc[-1]
                    sol = yf.Ticker("SOL-USD").history(period="1d")["Close"].iloc[-1]
                    st.markdown(
                        f"""
                        <div class='industrial-card' style='height:230px;'>
                            <div class='terminal-header'>⚡ PİYASA</div>
                            <div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.0f}</span></div>
                            <div class='terminal-row'><span>ETHEREUM</span><span style='color:#cc7a00;'>${eth:,.0f}</span></div>
                            <div class='terminal-row'><span>SOLANA</span><span style='color:#cc7a00;'>${sol:,.2f}</span></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    raise Exception("yfinance yok")
            except:
                st.markdown(
                    "<div class='industrial-card' style='height:230px;'><div class='terminal-header'>⚡ PİYASA</div><div class='highlight'>Piyasa verisi bekleniyor...</div></div>",
                    unsafe_allow_html=True
                )

        with col3:
            st.markdown(
                f"<div class='industrial-card' style='height:230px;'><div class='terminal-header'>📊 Win Rate</div><div style='text-align:center;'><span style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>%{wr_oran}</span></div></div>",
                unsafe_allow_html=True
            )

        st.markdown("### 📜 SON İŞLEMLER")
        st.markdown(
            f"<div class='industrial-card'><div class='terminal-header'>AKTİVİTE LOGLARI</div><p style='font-family:JetBrains Mono; color:#888;'>{son_islemler_raw}</p></div>",
            unsafe_allow_html=True
        )

    elif page == "🎲 CHALLANGE":
        st.markdown("<div class='terminal-header'>🏆 SIRALAMA</div>", unsafe_allow_html=True)

        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(
                f"<div class='industrial-card' style='padding:15px; text-align:center; border-top: 2px solid #cc7a00;'><div style='font-size:11px; color:#666;'>oguzo</div><div class='highlight'>{og_p} P</div><div style='font-size:12px;'>{rutbe_getir(og_p)}</div></div>",
                unsafe_allow_html=True
            )
        with s2:
            st.markdown(
                f"<div class='industrial-card' style='padding:15px; text-align:center; border-top: 2px solid #cc7a00;'><div style='font-size:11px; color:#666;'>ero7</div><div class='highlight'>{er_p} P</div><div style='font-size:12px;'>{rutbe_getir(er_p)}</div></div>",
                unsafe_allow_html=True
            )
        with s3:
            st.markdown(
                f"<div class='industrial-card' style='padding:15px; text-align:center; border-top: 2px solid #cc7a00;'><div style='font-size:11px; color:#666;'>fybey</div><div class='highlight'>{fy_p} P</div><div style='font-size:12px;'>{rutbe_getir(fy_p)}</div></div>",
                unsafe_allow_html=True
            )

        st.divider()
        q_col1, q_col2 = st.columns(2)
        base_url = "https://script.google.com/macros/s/AKfycbz0cvMHSrHchkksvFCixr9NDnMsvfLQ6T_K2jsXfohgs7eFXP5x-wxTX_YQej1EZhSX/exec"

        with q_col1:
            st.markdown(
                f"<div class='industrial-card equal-card'><div class='terminal-header'>📢 AKTİF SORU 1</div><h3 style='color:white; margin:0;'>{aktif_soru_1}</h3></div>",
                unsafe_allow_html=True
            )
            u_name_1 = st.selectbox("İsim (Soru 1)", ["oguzo", "ero7", "fybey"], key="n1")
            u_vote_1 = st.radio("Tahmin (Soru 1)", ["A", "B", "C", "D", "E"], key="v1")
            final_link_1 = f"{base_url}?isim={u_name_1}&tahmin={u_vote_1}&soru=1"
            st.markdown(
                f"<a href='{final_link_1}' target='_blank' style='text-decoration:none;'><div style='background:rgba(204, 122, 0, 0.2); border: 1px solid #cc7a00; color:#cc7a00; text-align:center; padding:15px; border-radius:5px; font-family:Orbitron; font-weight:bold; cursor:pointer;'>1. OYU ONAYLA</div></a>",
                unsafe_allow_html=True
            )

        with q_col2:
            st.markdown(
                f"<div class='industrial-card equal-card'><div class='terminal-header'>📢 AKTİF SORU 2</div><h3 style='color:white; margin:0;'>{aktif_soru_2}</h3></div>",
                unsafe_allow_html=True
            )
            u_name_2 = st.selectbox("İsim (Soru 2)", ["oguzo", "ero7", "fybey"], key="n2")
            u_vote_2 = st.radio("Tahmin (Soru 2)", ["A", "B", "C", "D", "E"], key="v2")
            final_link_2 = f"{base_url}?isim={u_name_2}&tahmin={u_vote_2}&soru=2"
            st.markdown(
                f"<a href='{final_link_2}' target='_blank' style='text-decoration:none;'><div style='background:rgba(204, 122, 0, 0.2); border: 1px solid #cc7a00; color:#cc7a00; text-align:center; padding:15px; border-radius:5px; font-family:Orbitron; font-weight:bold; cursor:pointer;'>2. OYU ONAYLA</div></a>",
                unsafe_allow_html=True
            )

    elif page == "⚽ FORMLINE":
        st.markdown(
            f"<div class='industrial-card'><div class='terminal-header'>📈 PERFORMANS</div><div class='terminal-row'><span>NET:</span><span style='color:#00ff41; font-size:32px; font-family:Orbitron;'>${toplam_bahis_kar:,.2f}</span></div></div>",
            unsafe_allow_html=True
        )

        t10, t9, t8, t7, t6, t5, t4, t1, t2, t3 = st.tabs(["🆕 W10", "❌ W9", "❌ W8", "✅ W7", "❌ W6", "❌ W5", "❌ W4", "✅ W3", "✅ W2", "❌ W1"])
        with t10:
            st.markdown(w10_coupon_html, unsafe_allow_html=True)
        with t9:
            st.markdown(w9_coupon_html, unsafe_allow_html=True)
        with t8:
            st.markdown(w8_coupon_html, unsafe_allow_html=True)
        with t7:
            st.markdown(w7_coupon_html, unsafe_allow_html=True)
        with t6:
            st.markdown(w6_coupon_html, unsafe_allow_html=True)
        with t5:
            st.markdown(w5_coupon_html, unsafe_allow_html=True)
        with t4:
            st.markdown(w4_coupon_html, unsafe_allow_html=True)
        with t1:
            st.markdown(w3_coupon_html, unsafe_allow_html=True)
        with t2:
            st.markdown(w2_coupon_html, unsafe_allow_html=True)
        with t3:
            st.markdown(w1_coupon_html, unsafe_allow_html=True)

    elif page == "📊 Portföy Takip":
        render_portfolio_v2(live_vars)

    elif page == "💠 FTMO":
        st.markdown("<div class='terminal-header'>💠 FTMO FON TAKİP</div>", unsafe_allow_html=True)

        bf_balance = float(get_num(live_vars, "bf_balance", 100000))
        bf_equity = float(get_num(live_vars, "bf_equity", 100000))
        bf_daily_loss = float(get_num(live_vars, "bf_daily_loss", 0.0))
        bf_target_pct = float(get_num(live_vars, "bf_target_pct", 10)) / 100
        bf_target_price = bf_balance * (1 + bf_target_pct)

        m1, m2, m3 = st.columns(3)
        bf_net_pnl = bf_equity - bf_balance
        bf_pnl_color = "#00ff41" if bf_net_pnl >= 0 else "#ff4b4b"

        with m1:
            st.markdown(
                f"<div class='industrial-card' style='text-align:center; border-top-color: #cc7a00;'><div style='font-size:11px; color:#666;'>GÜNCEL EQUITY</div><div class='highlight' style='font-size:24px;'>${bf_equity:,.2f}</div></div>",
                unsafe_allow_html=True
            )
        with m2:
            st.markdown(
                f"<div class='industrial-card' style='text-align:center; border-top-color: {bf_pnl_color};'><div style='font-size:11px; color:#666;'>NET K/Z</div><div style='color:{bf_pnl_color}; font-size:24px;' class='val-std'>${bf_net_pnl:,.2f}</div></div>",
                unsafe_allow_html=True
            )
        with m3:
            bf_limit_pct = (abs(bf_daily_loss) / (bf_balance * 0.05)) * 100 if bf_balance > 0 else 0
            st.markdown(
                f"<div class='industrial-card' style='text-align:center; border-top-color: #ff4b4b;'><div style='font-size:11px; color:#666;'>GÜNLÜK LİMİT DOLULUK</div><div class='highlight' style='font-size:24px;'>%{bf_limit_pct:.2f}</div></div>",
                unsafe_allow_html=True
            )

        bf_progress = max(0.0, min(1.0, (bf_equity - bf_balance) / (bf_target_price - bf_balance))) if (bf_target_price - bf_balance) != 0 else 0

        st.markdown(
            f"""
            <div class='industrial-card'>
                <div class='terminal-header'>🎯 HEDEF YOLCULUĞU (HEDEF: ${bf_target_price:,.0f})</div>
                <div style='background:#111; height:15px; border-radius:10px; border: 1px solid rgba(255,255,255,0.05);'>
                    <div style='background:linear-gradient(90deg, #00ff41, #008f11); width:{bf_progress*100}%; height:100%; border-radius:10px; box-shadow: 0 0 10px rgba(0,255,65,0.3);'></div>
                </div>
                <div style='display:flex; justify-content:space-between; margin-top:10px;'>
                    <span style='font-size:12px; color:#555;'>BAŞLANGIÇ: ${bf_balance:,.0f}</span>
                    <span style='font-size:14px; color:#00ff41; font-weight:bold;'>%{bf_progress*100:.1f} TAMAMLANDI</span>
                    <span style='font-size:12px; color:#555;'>HEDEF: ${bf_target_price:,.0f}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div class='terminal-header'>🎯 Hedefler & Limitler (100K Hesap)</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Phase 1 hedef</div><div class='highlight'>$10,000 Kazanç</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Phase 1 r</div><div class='highlight'>$250</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Günlük limit</div><div class='highlight'>$5,000 Kayıp</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Phase 2 hedef</div><div class='highlight'>$5,000 Kazanç</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Phase 2 r</div><div class='highlight'>$250</div></div>", unsafe_allow_html=True)
            st.markdown("<div class='industrial-card' style='border-top:1px solid #333;'><div style='font-size:11px; color:#666;'>Toplam limit</div><div class='highlight'>$10,000 Kayıp</div></div>", unsafe_allow_html=True)

    elif page == "💗 LOVE FUND":
        if check_love_password():
            render_love_fund(live_vars)

    st.markdown(f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG CORE // {datetime.now().year}</div>", unsafe_allow_html=True)
