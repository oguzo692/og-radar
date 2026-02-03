import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- 1. AYARLAR (Geniş Ekran) ---
st.set_page_config(page_title="OG Core v7.3", page_icon="🛡️", layout="wide")

# --- 2. CSS STİLLERİ (DAHA MODERN & MOBİL DOSTU) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
.main { background-color: #0d1117 !important; }
* { font-family: 'JetBrains Mono', monospace !important; }

/* Renk Paleti */
:root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; --terminal-gray: #8b949e; }

/* Gereksizleri Gizle */
#MainMenu, header, footer, .stDeployButton {visibility: hidden !important;}

/* ÜST MENÜ STİLİ (MOBİL İÇİN KRİTİK) */
div[data-testid="stRadio"] > div {
    flex-direction: row; /* Yan yana diz */
    justify-content: center;
    background: #161b22;
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #30363d;
}
div[data-testid="stRadio"] label {
    font-size: 14px !important;
    background: transparent !important;
    color: #e6edf3 !important;
    padding: 5px 15px !important;
    border: 1px solid transparent;
}
div[data-testid="stRadio"] label:hover {
    color: var(--soft-orange) !important;
    border-color: var(--soft-orange);
}

/* KART TASARIMI */
.industrial-card {
    background: #161b22;
    border-left: 4px solid var(--soft-orange);
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.terminal-header { 
    color: var(--soft-orange); 
    font-size: 13px; font-weight: bold; letter-spacing: 1px;
    border-bottom: 1px solid #30363d; 
    padding-bottom: 8px; margin-bottom: 12px;
}
.row {
    display: flex; justify-content: space-between; align-items: center;
    font-size: 13px; color: #c9d1d9; margin-bottom: 8px;
    border-bottom: 1px dashed #21262d; padding-bottom: 4px;
}
.row:last-child { border-bottom: none; }

/* RENKLER */
.val-up { color: var(--win-green); font-weight: bold; }
.val-down { color: var(--loss-red); font-weight: bold; }
.val-neu { color: var(--soft-orange); font-weight: bold; }
.dim { color: #8b949e; font-size: 11px; }

/* MOBİL İÇİN FONT AYARI */
@media only screen and (max-width: 600px) {
    .row { font-size: 11px !important; }
    h1 { font-size: 18px !important; }
    .stMetric { font-size: 12px !important; }
}
</style>
"""

# --- 3. HTML ŞABLONLARI ---

def create_card(title, rows, color="#cc7a00"):
    html = f"<div class='industrial-card' style='border-left-color: {color};'><div class='terminal-header' style='color:{color};'>{title}</div>"
    for label, val, val_class in rows:
        html += f"<div class='row'><span>{label}</span><span class='{val_class}'>{val}</span></div>"
    html += "</div>"
    return html

# --- 4. GÜVENLİK ---
if "password_correct" not in st.session_state: st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown("<br><h2 style='text-align:center; color:#cc7a00;'>🛡️ OG CORE ACCESS</h2>", unsafe_allow_html=True)
        pwd = st.text_input("PASSWORD", type="password", label_visibility="collapsed")
        if st.button("LOGIN", use_container_width=True):
            if pwd == "1": st.session_state["password_correct"] = True; st.rerun()
            else: st.error("ACCESS DENIED")
        return False
    return True

# --- 5. ANA UYGULAMA ---
if check_password():
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # --- ÜST MENÜ (SIDEBAR DEĞİL, ANA EKRAN) ---
    st.markdown("<h3 style='text-align:center; color:#e6edf3;'>🛡️ OG CORE v7.3</h3>", unsafe_allow_html=True)
    
    # Menüyü yatay olarak en tepeye koyuyoruz
    selected_page = st.radio("", ["⚡ DASHBOARD", "⚽ FORMLINE", "📈 SIMULATOR"], horizontal=True, label_visibility="collapsed")
    st.markdown("---")

    # --- AYARLAR PANELİ (EXPANDER İÇİNE GİZLENDİ - TEMİZ GÖRÜNÜM) ---
    with st.expander("⚙️ AYARLAR & KASA YÖNETİMİ"):
        kasa = st.number_input("Güncel Kasa ($)", value=600.0, step=10.0)
        ana_para = st.number_input("Başlangıç ($)", value=500.0)
        gunluk_yakim = st.number_input("Günlük Gider ($)", value=20)
        if st.button("ÇIKIŞ YAP"): st.session_state["password_correct"] = False; st.rerun()

    # ZAMAN & HESAPLAMALAR
    tr_tz = pytz.timezone('Europe/Istanbul')
    net_kar = kasa - ana_para
    tl_val = kasa * 33.50

    # ==========================
    # SAYFA 1: DASHBOARD
    # ==========================
    if selected_page == "⚡ DASHBOARD":
        # 1. Ana Durum Kartı
        st.markdown(create_card("FİNANSAL DURUM", [
            ("TOPLAM KASA", f"${kasa:,.2f}", "val-neu"),
            ("TRY KARŞILIĞI", f"₺{tl_val:,.0f}", "dim"),
            ("NET KAR/ZARAR", f"{net_kar:+.2f} USD", "val-up" if net_kar >=0 else "val-down")
        ]), unsafe_allow_html=True)

        # 2. Piyasa & Ömür (Yan Yana)
        col1, col2 = st.columns(2)
        with col1:
            try:
                # Basit veri çekimi
                btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
                eth = yf.Ticker("ETH-USD").history(period="1d")['Close'].iloc[-1]
                sol = yf.Ticker("SOL-USD").history(period="1d")['Close'].iloc[-1]
            except: btc, eth, sol = 0,0,0
            
            st.markdown(create_card("KRİPTO", [
                ("BTC", f"${btc:,.0f}", "val-neu"),
                ("ETH", f"${eth:,.0f}", "val-neu"),
                ("SOL", f"${sol:,.1f}", "val-neu")
            ]), unsafe_allow_html=True)
            
        with col2:
            gun_omru = int(kasa/gunluk_yakim) if gunluk_yakim>0 else 999
            color_omur = "#00ff41" if gun_omru > 14 else "#ff4b4b"
            st.markdown(create_card("RUNWAY", [
                ("KALAN GÜN", f"{gun_omru}", "val-neu"),
                ("DURUM", "KRİTİK" if gun_omru<14 else "İYİ", "val-down" if gun_omru<14 else "val-up"),
                ("HARCAMA", f"-${gunluk_yakim}/gün", "dim")
            ], color=color_omur), unsafe_allow_html=True)

        # 3. Paylar
        pay = kasa / 3
        st.markdown(create_card("ORTAK PAYLARI", [
            ("OGUZO", f"${pay:,.2f}", "val-neu"),
            ("ERO7", f"${pay:,.2f}", "val-neu"),
            ("FYBEY", f"${pay:,.2f}", "val-neu")
        ]), unsafe_allow_html=True)

    # ==========================
    # SAYFA 2: FORMLINE
    # ==========================
    elif selected_page == "⚽ FORMLINE":
        # Sekmeler
        tab1, tab2, tab3 = st.tabs(["🔥 W3 (AKTİF)", "✅ W2 (WIN)", "❌ W1 (LOSS)"])
        
        with tab1:
            st.markdown(create_card("🔥 W3 KUPONU", [
                ("Wolfsburg - BVB", "BVB X2 & 1.5 ÜST", "val-neu"),
                ("Newcastle - Brentford", "NEW 1.5 ÜST", "val-neu"),
                ("Rizespor - GS", "GS W & 1.5 ÜST", "val-neu"),
                ("LIV - Man City", "LIV GOL ATAR", "val-neu"),
                ("FB - Gençlerbirliği", "FB W & 2.5 ÜST", "val-neu"),
                ("ORAN / DURUM", "8.79 / BEKLİYOR", "dim")
            ]), unsafe_allow_html=True)
            
        with tab2:
            st.markdown(create_card("✅ W2 KUPONU", [
                ("GS - Kayseri", "WON", "val-up"),
                ("LIV - New", "WON", "val-up"),
                ("BVB - Heidenheim", "WON", "val-up"),
                ("Kocaeli - FB", "WON", "val-up"),
                ("KAZANÇ", "+$540", "val-up")
            ], color="#00ff41"), unsafe_allow_html=True)
            
        with tab3:
            st.markdown(create_card("❌ W1 KUPONU", [
                ("Karagümrük - GS", "WON", "val-up"),
                ("New - Aston Villa", "LOST", "val-down"),
                ("KAYIP", "-$100", "val-down")
            ], color="#ff4b4b"), unsafe_allow_html=True)

    # ==========================
    # SAYFA 3: SIMULATOR
    # ==========================
    elif selected_page == "📈 SIMULATOR":
        st.markdown(create_card("HEDEF AYARLARI", [
            ("BAŞLANGIÇ", f"${kasa}", "val-neu"),
            ("SİMÜLASYON", "30 Günlük", "dim")
        ]), unsafe_allow_html=True)
        
        haftalik_hedef = st.slider("Haftalık Hedef Büyüme (%)", 1, 50, 5)
        
        # Hesaplama
        days = 30
        data = [kasa * ((1 + haftalik_hedef/100)**(d/7)) for d in range(days)]
        
        # Grafik
        st.line_chart(data, height=200)
        
        son_durum = data[-1]
        st.success(f"30 Gün Sonra Tahmini: ${son_durum:,.2f}")
        
        # Streak
        st.markdown(create_card("PERFORMANS", [
            ("SON 3 İŞLEM", "❌ ✅ ✅", "val-neu"),
            ("MOMENTUM", "YÜKSEK 🔥", "val-up")
        ]))

    st.markdown("<div style='text-align:center; color:#30363d; font-size:10px; margin-top:20px;'>OG CORE v7.3 MOBILE ULTIMATE</div>", unsafe_allow_html=True)
