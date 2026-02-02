import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz

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
        .status-loss { color: var(--loss-red); font-weight: bold; }
        .status-wait { color: #f1c40f; font-weight: bold; }
        
        .terminal-header { 
            border-bottom: 2px solid var(--soft-orange); 
            padding-bottom: 5px; margin-bottom: 15px; 
            color: var(--soft-orange); font-size: 18px; font-weight: bold;
        }
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
        hedef_kasa = st.number_input("HEDEF KASA (USD)", value=1200.0)
        gunluk_kayip = st.slider("GÜNLÜK ORT. HARCAMA (USD)", 0, 100, 20)
        
        tr_tz = pytz.timezone('Europe/Istanbul')
        st.info(f"🕒 {datetime.now(tr_tz).strftime('%H:%M:%S')}")
        if st.button("🔴 ÇIKIŞ"):
            st.session_state["password_correct"] = False
            st.rerun()

    # --- 5. ULTRA FON (PERFORMANS & SS VERİLERİ) ---
    if page == "⚡ ULTRA FON":
        # Hesaplamalar
        usd_try = 33.50 
        toplam_tl = kasa * usd_try
        net_kar = kasa - ana_para
        kar_oranı = (net_kar / ana_para) * 100 if ana_para > 0 else 0
        ilerleme = min(kasa / hedef_kasa, 1.0) if hedef_kasa > 0 else 0
        
        # HTML Değişkenleri (Hata riskini sıfırlamak için)
        progress_bar = f"<div style='background:#333; height:10px; width:100%; margin-top:5px;'><div style='background:#cc7a00; height:100%; width:{ilerleme*100}%;'></div></div>"

        # Ana Ekran
        st.markdown(f"""
        <div class='industrial-card'>
            <div class='terminal-header'>💎 OG FundRoom — ULTRA ATAK KRİPTO FONU 2026</div>
            <h2 style='color:#fff !important;'>💰 TOPLAM KASA: {kasa:,.2f} USD (≈ {toplam_tl:,.0f} TL)</h2>
            <p class='terminal-text'>🎯 GÜNLÜK DURUM: <span class='highlight'>{net_kar:,.2f} USD (%{kar_oranı:.1f})</span></p>
            <div style='margin-top:20px;'>
                <p style='color:#fff;'>HEDEF FON MİKTARI: {hedef_kasa} USD</p>
                <p style='color:#fff;'>İLERLEME: %{ilerleme*100:.1f}</p>
                {progress_bar}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Bölüm: Canlı Fiyatlar & Ömür Sayacı
        c1, c2 = st.columns([2, 1])
        
        with c1:
            try:
                tickers = ["BTC-USD", "ETH-USD", "SOL-USD"]
                prices = yf.download(tickers, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
                btc_p, eth_p, sol_p = prices['BTC-USD'], prices['ETH-USD'], prices['SOL-USD']
            except:
                btc_p, eth_p, sol_p = 0.0, 0.0, 0.0
                
            st.markdown(f"""
            <div class='industrial-card'>
                <div class='terminal-header'>📊 PERFORMANS GÖSTERGELERİ</div>
                <div class='match-row'><span>BTC (Canlı)</span><span class='highlight'>${btc_p:,.1f}</span></div>
                <div class='match-row'><span>ETH (Canlı)</span><span class='highlight'>${eth_p:,.1f}</span></div>
                <div class='match-row'><span>SOL (Canlı)</span><span class='highlight'>${sol_p:,.1f}</span></div>
                <hr style='border-color:#333;'>
                <div class='match-row'><span>Piyasa Havası</span><span>Normal</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            # Survival Runway
            gun_sayisi = int(kasa / gunluk_kayip) if gunluk_kayip > 0 else 999
            durum_renk = "#ff4b4b" if gun_sayisi < 14 else "#00ff41"
            st.markdown(f"""
            <div class='industrial-card' style='border-color:{durum_renk}'>
                <div class='terminal-header' style='color:{durum_renk}'>💀 FON ÖMRÜ</div>
                <h1 style='font-size:40px !important; color:{durum_renk} !important;'>{gun_sayisi} GÜN</h1>
                <small class='terminal-text'>Günlük {gunluk_kayip}$ yakma hızıyla.</small>
            </div>
            """, unsafe_allow_html=True)

        # Ortaklık Dağılımı
        st.subheader("👥 KATILIM & KAR PAYLAŞIMI")
        pay = kasa / 3
        o1, o2, o3 = st.columns(3)
        
        # Kullanıcı Kartlarını Döngüyle Bas (Daha Temiz Kod)
        users = ["OGUZO", "FYBEY", "ERO7"]
        cols = [o1, o2, o3]
        for col, user in zip(cols, users):
            with col:
                st.markdown(f"""
                <div class='industrial-card'>
                    <small style='color:#8b949e'>{user}</small>
                    <h3>${pay:,.2f}</h3>
                    <small class='highlight'>Pay: %33.3</small>
                </div>
                """, unsafe_allow_html=True)

    # --- 6. FORM LINE ---
    elif page == "⚽ FORMLINE":
        st.title("⚽ FORMLINE ANALİZ")
        t1, t2, t3 = st.tabs(["🔥 W3 (8-9 Şub)", "✅ W2 (1-2 Şub)", "⏪ W1 (Geçmiş)"])

        with t1:
            st.markdown("""
            <div class='industrial-card'>
                <h3>🔥 W3 KUPONU</h3>
                <div class='match-row'><span>Analizler Bekleniyor...</span><span class='status-wait'>⏳</span></div>
                <p style='color:#8b949e; margin-top:10px;'>Cuma günü güncellenecektir.</p>
            </div>
            """, unsafe_allow_html=True)

        with t2:
            # HTML'i değişkene atayarak hatayı önlüyoruz
            w2_html = """
            <div class='industrial-card' style='border-color: #00ff41;'>
                <h3 style='color:#00ff41 !important;'>✅ W2 KUPONU - KAZANDI</h3>
                <div class='match-row'><span>GS - Kayserispor</span><span class='status-win'>GS W & +2.5 ÜST ✅</span></div>
                <div class='match-row'><span>Liverpool - Newcastle</span><span class='status-win'>KG VAR ✅</span></div>
                <div class='match-row'><span>BVB - Heidenheim</span><span class='status-win'>BVB İY 0.5 ÜST ✅</span></div>
                <div class='match-row'><span>Kocaelispor - FB</span><span class='status-win'>FB W & 1.5 ÜST ✅</span></div>
                <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 15px 0;'>
                <p><b>Oran: 5.40 | Bütçe: 100 USD | Durum: Sonuçlandı</b></p>
            </div>
            """
            st.markdown(w2_html, unsafe_allow_html=True)

        with t3:
            w1_html = """
            <div class='industrial-card' style='border-color: #ff4b4b;'>
                <h3 style='color:#ff4b4b !important;'>❌ W1 KUPONU - KAYBETTİ</h3>
                <div class='match-row'><span>Karagümrük - GS</span><span class='status-win'>GS W & +1.5 ÜST ✅</span></div>
                <div class='match-row'><span>Bournemouth - Liv</span><span class='status-win'>KG VAR ✅</span></div>
                <div class='match-row'><span>New - Aston Villa</span><span class='status-loss'>MS 1 ❌</span></div>
                <div class='match-row'><span>FB - Göztepe</span><span class='status-loss'>İY 0.5 ÜST ❌</span></div>
                <hr style='border: 1px solid rgba(255,255,255,0.05); margin: 15px 0;'>
                <p><b>Oran: 7.09 | Bütçe: 100 USD | Sonuç: -100 USD</b></p>
