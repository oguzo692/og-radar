import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz
import numpy as np

# --- 1. AYARLAR ---
st.set_page_config(page_title="OG Core v5.0", page_icon="🛡️", layout="wide")

# --- 2. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown("<h1 style='text-align:center; color:#cc7a00;'>🛡️ OG_CORE AUTH</h1>", unsafe_allow_html=True)
        pwd = st.text_input("ŞİFRE", type="password")
        if st.button("Giriş Yap"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Yanlış şifre")
        return False
    return True

if check_password():
    # --- 3. RETRO INDUSTRIAL CSS (v7.1 STYLE) ---
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        .main { background-color: #0d1117 !important; }
        * { font-family: 'JetBrains Mono', monospace !important; }
        :root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; --terminal-gray: #8b949e; }
        
        .industrial-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--soft-orange);
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .match-row {
            display: flex; justify-content: space-between;
            padding: 8px 0; border-bottom: 1px dashed rgba(255,255,255,0.05);
            font-size: 13px;
        }
        .status-win { color: var(--win-green); font-weight: bold; }
        .status-wait { color: #f1c40f; font-weight: bold; }
        
        .terminal-text { color: var(--terminal-gray); font-size: 12px; }
        .highlight { color: var(--soft-orange); font-weight: bold; }
        h1, h2, h3 { color: var(--soft-orange) !important; margin: 0 !important; }
        section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid var(--soft-orange); }
        </style>
    """, unsafe_allow_html=True)

    # --- 4. SIDEBAR ---
    with st.sidebar:
        st.title("🛡️ OG CORE")
        page = st.radio("MENÜ", ["⚡ ULTRA FON", "⚽ FORMLINE", "📊 DASHDASH"])
        st.divider()
        kasa = st.number_input("TOPLAM KASA (USD)", value=600.0, step=1.0)
        ana_para = st.number_input("ANA SERMAYE (USD)", value=500.0)
        gunluk_kayip = st.slider("ORT. GÜNLÜK KAYIP/GİDER (USD)", 1, 100, 20)
        
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.info(f"🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}")
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 5. ULTRA FON (PERFORMANS & SS VERİLERİ) ---
    if page == "⚡ ULTRA FON":
        st.title("💎 OG TRADE RADAR - v7.1")
        
        # TL Karşılığı ve Fark Hesaplama
        usd_try = 33.50 # Manuel veya API'den çekilebilir
        toplam_tl = kasa * usd_try
        net_kar = kasa - ana_para
        kar_oranı = (net_kar / ana_para) * 100

        # Üst Terminal Paneli
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"""
            <div class='industrial-card'>
                <p class='terminal-text'>💰 TOPLAM KASA: <span class='highlight'>${kasa:,.2f} (≈ {toplam_tl:,.0f} TL)</span></p>
                <p class='terminal-text'>🎯 NET KAR/ZARAR: <span style='color:{"#00ff41" if net_kar >=0 else "#ff4b4b"}'>{net_kar:,.2f} USD (%{kar_oranı:.1f})</span></p>
                <p class='terminal-text'>📅 SON GÜNCELLEME: {datetime.now(tr_tz).strftime('%H:%M:%S')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            # Ölüm Kalım Projeksiyonu (Runway)
            gun_sayisi = int(kasa / gunluk_kayip) if gunluk_kayip > 0 else 999
            color = "#ff4b4b" if gun_sayisi < 10 else "#00ff41"
            st.markdown(f"""
            <div class='industrial-card' style='border-color:{color}'>
                <p class='terminal-text'>💀 ÖLÜM KALIM PROJEKSİYONU</p>
                <h2 style='color:{color} !important;'>{gun_sayisi} GÜN</h2>
                <small class='terminal-text'>Mevcut yakma hızına göre.</small>
            </div>
            """, unsafe_allow_html=True)

        # Ortaklık & Kâr Payları (SS'teki gibi)
        st.subheader("👥 ÜYE KAR PAYLARI (oguzo | ero7 | fybey)")
        pay = kasa / 3
        kisi_basi_kar = net_kar / 3
        o1, o2, o3 = st.columns(3)
        for col, user in zip([o1, o2, o3], ["oguzo", "ero7", "fybey"]):
            with col:
                st.markdown(f"""
                <div class='industrial-card'>
                    <small class='terminal-text'>{user.upper()}</small>
                    <h3>${pay:,.2f}</h3>
                    <p style='font-size:12px; color:{"#00ff41" if kisi_basi_kar >=0 else "#ff4b4b"}'>
                        Kâr: {kisi_basi_kar:+,.2f} USD
                    </p>
                </div>
                """, unsafe_allow_html=True)

    # --- 6. FORM LINE ---
    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE ANALİZ")
        t1, t2, t3 = st.tabs(["🔥 W3 (8-9 Şub)", "✅ W2 (1-2 Şub)", "⏪ W1 (Geçmiş)"])
        # (Önceki kupon kodları buraya gelecek - Alan tasarrufu için kısa kestim)
        with t2:
            st.markdown("<div class='industrial-card' style='border-color:#00ff41;'><h3>✅ W2 - KAZANDI</h3><div class='match-row'><span>Kocaelispor -
