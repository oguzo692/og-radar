import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
import pytz

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. VERİ BAĞLANTISI (GOOGLE SHEETS) ---
def get_live_data():
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url)
        data = dict(zip(df['key'].astype(str), df['value'].astype(str)))
        return data
    except Exception:
        return {"kasa": "600.0", "ana_para": "600.0"}


# --- GÜNCELLENMİŞ RÜTBE FONKSİYONU ---
def rutbe_getir(puan_str):
    try:
        p = int(float(puan_str))
    except:
        p = 0

    if p <= 3: return "Hılez"
    elif p <= 6: return "Tecrübeli Hılez"
    elif p <= 9: return "Bu Abi Biri Mi?"
    elif p <= 11: return "Miço"
    else: return "Grand Miço"


live_vars = get_live_data()

kasa = float(live_vars.get("kasa", 600))
ana_para = float(live_vars.get("ana_para", 600))
duyuru_metni = live_vars.get("duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE V9.9")

# --- KASA ---
og_kasa = float(live_vars.get("oguzo_kasa", kasa / 3))
er_kasa = float(live_vars.get("ero7_kasa", kasa / 3))
fy_kasa = float(live_vars.get("fybey_kasa", kasa / 3))

# --- PUAN ---
og_p = live_vars.get("oguzo_puan", "0")
er_p = live_vars.get("ero7_puan", "0")
fy_p = live_vars.get("fybey_puan", "0")

aktif_soru_1 = live_vars.get("aktif_soru", "")
aktif_soru_2 = live_vars.get("aktif_soru2", "")

# --- FORMLINE ---
w1_kar = float(live_vars.get("w1_sonuc", -100))
w2_kar = float(live_vars.get("w2_sonuc", 453))
toplam_bahis_kar = w1_kar + w2_kar

wr_oran = live_vars.get("win_rate", "0")
son_islemler_raw = str(live_vars.get("son_islemler", "Veri yok"))


# =====================================================
# 🔐 YENİ PROFESYONEL LOGIN EKRANI (SIFIRDAN TASARIM)
# =====================================================

if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False


def check_password():

    if not st.session_state["password_correct"]:

        st.markdown("""
        <style>
        .stApp{
            background:#050505;
            background-image:
            radial-gradient(circle at center, rgba(204,122,0,0.12), transparent 70%);
        }

        .login-box{
            background:#0b0b0b;
            border:1px solid rgba(204,122,0,0.4);
            padding:40px;
            border-radius:8px;
            text-align:center;
        }

        .login-title{
            font-family:Orbitron;
            letter-spacing:4px;
            color:#cc7a00;
            font-size:22px;
            margin-bottom:25px;
        }

        .stButton>button{
            width:100%;
            background:#cc7a00 !important;
            color:black !important;
            font-weight:bold;
        }
        </style>
        """, unsafe_allow_html=True)

        # YATAY + DİKEY merkezleme (Streamlit-safe)
        top, center, bottom = st.columns([1,2,1])

        with center:

            st.markdown("<br><br><br>", unsafe_allow_html=True)

            st.markdown("<div class='login-box'>", unsafe_allow_html=True)
            st.markdown("<div class='login-title'>OG CORE</div>", unsafe_allow_html=True)

            pwd = st.text_input("", type="password", placeholder="ACCESS KEY")

            if st.button("ENTER"):
                if pwd == "1608":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")

            st.markdown("</div>", unsafe_allow_html=True)

        return False

    return True



# =====================================================
# ANA UYGULAMA
# =====================================================

if check_password():

    st.markdown("## 🛡️ OG CORE DASHBOARD")

    net_kar = kasa - ana_para

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Toplam Kasa", f"${kasa:,.2f}")

    with col2:
        st.metric("Kâr/Zarar", f"${net_kar:,.2f}")

    with col3:
        st.metric("Win Rate", f"%{wr_oran}")

    st.divider()

    st.write("### 👤 Kişisel Bakiyeler")
    st.write(f"Oguzo: ${og_kasa:,.2f}")
    st.write(f"Ero7: ${er_kasa:,.2f}")
    st.write(f"Fybey: ${fy_kasa:,.2f}")

    st.divider()

    st.write("### 🏆 Rütbeler")
    st.write(f"oguzo → {rutbe_getir(og_p)}")
    st.write(f"ero7 → {rutbe_getir(er_p)}")
    st.write(f"fybey → {rutbe_getir(fy_p)}")

    st.divider()

    st.write("### 📜 Son İşlemler")
    st.code(son_islemler_raw)

    st.markdown(
        f"<div style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>OG_CORE_V9.9 // {datetime.now().year}</div>",
        unsafe_allow_html=True
    )
