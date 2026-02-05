import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core v9.6", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. VERİ BAĞLANTISI ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'], df['value']))
        return data
    except Exception:
        return {"kasa": 600.0, "ana_para": 600.0}

live_vars = get_live_data()
kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SYSTEM ONLINE... PERFORMANCE TRACKING ACTIVE...")

# Formline Kar/Zarar Verileri (Sheets'ten çekiyoruz)
w1_kar = float(live_vars.get("w1_sonuc", -100)) # Varsayılan: Kaybeden kupon -100
w2_kar = float(live_vars.get("w2_sonuc", 453))  # Varsayılan: Kazanan kupon +453
toplam_formline_kar = w1_kar + w2_kar

# --- 3. CSS STİLLERİ ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Orbitron:wght@400;900&display=swap');

.stApp { 
    background-color: #030303 !important;
    background-image: radial-gradient(circle at 50% 50%, rgba(204, 122, 0, 0.05) 0%, transparent 60%);
}

body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], p, div, span, h1, h2, h3, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
    color: #e0e0e0 !important;
}

.ticker-wrap {
    width: 100%; overflow: hidden; background: rgba(0, 0, 0, 0.8);
    border-bottom: 1px solid rgba(204, 122, 0, 0.3); padding: 12px 0;
    margin-bottom: 25px; backdrop-filter: blur(10px);
}
.ticker { display: flex; white-space: nowrap; animation: ticker 50s linear infinite; }
.ticker-item {
    font-family: 'JetBrains Mono', monospace; font-size: 13px; color: #cc7a00;
    text-transform: uppercase; letter-spacing: 3px; padding-right: 100%;
}
@keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

.industrial-card { 
    background: rgba(18, 18, 18, 0.8) !important; backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.05) !important; border-top: 2px solid rgba(204, 122, 0, 0.5) !important;
    padding: 25px; margin-bottom: 25px; border-radius: 4px;
}

.terminal-header { color: #888; font-size: 11px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 20px; }
.terminal-row { display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.02); padding-bottom: 8px; }
.highlight { color: #cc7a00 !important; font-weight: 700; font-size: 20px; }

section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid rgba(204, 122, 0, 0.2); }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1.5 üst</span></div><div class='terminal-row'><span>Newcastle - Brentford</span><span class='highlight'>newcastle 1.5 üst</span></div><div class='terminal-row'><span>Rizespor - Gala</span><span class='highlight'>gala w & 1.5 üst</span></div><div class='terminal-row'><span>Lıve - Man City</span><span class='highlight'>lıve gol atar</span></div><div class='terminal-row'><span>Fenerbahçe - Gençlerbirliği</span><span class='highlight'>fenerbahçe w & 2.5 üst</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 8.79</span><span>bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>gs - kayserispor</span><span style='color:#00ff41;'>iy +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>lıve - new</span><span style='color:#00ff41;'>+2 & liverpool 1x ✅</span></div><div class='terminal-row'><span>bvb - heidenheim</span><span style='color:#00ff41;'>iy +0.5 & W & 2+ ✅</span></div><div class='terminal-row'><span>kocaelispor - fb</span><span style='color:#00ff41;'>fb W & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 5.53</span><span>bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>karagümrük - gs</span><span style='color:#00ff41;'>gs w & +2 ✅</span></div><div class='terminal-row'><span>bournemouth - lıve</span><span style='color:#00ff41;'>kg var ✅</span></div><div class='terminal-row'><span>unıon berlin - bvb</span><span style='color:#00ff41;'>bvb iy 0.5 üst ✅</span></div><div class='terminal-row'><span>new - aston villa</span><span style='color:#ff4b4b;'>new +2 ❌</span></div><div class='terminal-row'><span>fb - göztepe</span><span style='color:#ff4b4b;'>fb w ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>oran: 7.09</span><span>bet: 100 USD</span></div>"""

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown('<div style="padding:5rem; text-align:center;"><h1 style="font-family:Orbitron; font-size:60px; letter-spacing:15px;">OG_CORE</h1><p style="color:#cc7a00; letter-spacing:5px;">ARCHITECTING THE FUTURE OF WEALTH</p></div>', unsafe_allow_html=True)
        pwd = st.text_input("ERİŞİM ANAHTARI", type="password", placeholder="Enter System Key...", label_visibility="collapsed")
        if st.button("TERMİNALİ INITIALIZE ET"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED")
        return False
    return True

# --- 6. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="ticker-wrap"><div class="ticker"><span class="ticker-item">{duyuru_metni}</span><span class="ticker-item">{duyuru_metni}</span></div></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 style='color:#cc7a00; font-family:Orbitron; letter-spacing:4px; text-align:center;'>🛡️ OG CORE</h2>", unsafe_allow_html=True)
        page = st.radio("MODÜLLER", ["⚡ ULTRA ATAK FON", "⚽ FORMLINE", "📊 SIMULASYON"])
        st.divider()
        if st.button("🔴 ÇIKIŞ YAP"): 
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "⚡ ULTRA ATAK FON":
        # (Eski stabil kodun ultra fon içeriği buraya gelecek - temizlik için kısalttım)
        st.subheader("💎 Trade Radar V9.6")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>TOPLAM DURUM</div><div class='terminal-row'><span>KASA</span><span class='highlight'>${kasa:,.2f}</span></div><div class='terminal-row'><span>NET KAR</span><span style='color:#00ff41;'>${kasa-ana_para:,.2f}</span></div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='industrial-card'><div class='terminal-header'>FORMLINE P&L</div><div class='terminal-row'><span>BAHİS KAR</span><span style='color:{'#00ff41' if toplam_formline_kar >=0 else '#ff4b4b'}; font-weight:bold;'>${toplam_formline_kar:,.2f}</span></div><div class='terminal-row'><span>BAŞARI</span><span>%{ (1 if toplam_formline_kar > 0 else 0)*100 }</span></div></div>", unsafe_allow_html=True)

    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE PERFORMANCE")
        
        # --- YENİ EKLENEN KAR/ZARAR PANELİ ---
        st.markdown(f"""
        <div class='industrial-card' style='border-top: 2px solid #cc7a00;'>
            <div class='terminal-header'>📈 FORMLINE TOTAL PROFIT/LOSS</div>
            <div class='terminal-row'>
                <span style='font-size:14px; color:#888;'>W1 + W2 + W3 TOPLAM SONUÇ:</span>
                <span style='color:{'#00ff41' if toplam_formline_kar >=0 else '#ff4b4b'}; font-size:28px; font-weight:900; text-shadow: 0 0 10px rgba(0,255,65,0.3);'>
                    {'+' if toplam_formline_kar > 0 else ''}${toplam_formline_kar:,.2f}
                </span>
            </div>
            <div style='font-size:10px; color:#555; text-align:right; margin-top:10px;'>* Veriler Google Sheets üzerinden anlık güncellenmektedir.</div>
        </div>
        """, unsafe_allow_html=True)
        
        t1, t2, t3 = st.tabs(["⏳ AKTİF (W3)", "✅ KAZANAN (W2)", "❌ KAYBEDEN (W1)"])
        with t1: st.markdown(f"<div class='industrial-card'><div class='terminal-header'>🔥 W3 KUPONU</div>{w3_matches}<span style='color:#cc7a00'>BEKLENİYOR ⏳</span></div>", unsafe_allow_html=True)
        with t2: st.markdown(f"<div class='industrial-card' style='border-top-color:#00ff41;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU</div>{w2_matches}<span style='color:#00ff41;'>SONUÇLANDI: +${w2_kar}</span></div>", unsafe_allow_html=True)
        with t3: st.markdown(f"<div class='industrial-card' style='border-top-color:#ff4b4b;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU</div>{w1_matches}<span style='color:#ff4b4b;'>SONUÇLANDI: ${w1_kar}</span></div>", unsafe_allow_html=True)

    elif page == "📊 SIMULASYON":
        st.title("📈 Projeksiyon")
        df = pd.DataFrame({"Gün": range(30), "Tahmin ($)": [kasa * (1.05 ** (d / 7)) for d in range(30)]})
        st.line_chart(df.set_index("Gün"))

    st.caption(f"OG Core v9.6 | Sync: {datetime.now().strftime('%H:%M:%S')}")
