import streamlit as st
import yfinance as yf
from datetime import datetime
import pytz

# -------------------------------------------------
# SAYFA
# -------------------------------------------------
st.set_page_config(page_title="OG Core", page_icon="🛡️", layout="wide")


# -------------------------------------------------
# GLASS CARD COMPONENT (tekrar önlemek için)
# -------------------------------------------------
def glass_card(title, value):
    st.markdown(
        f"""
        <div class='glass-card'>
            <small style='color:#888'>{title}</small>
            <h2>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------------------------------
# GÜVENLİK
# -------------------------------------------------
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False


def check_password():
    if not st.session_state["password_correct"]:
        st.title("🔐 OG Core")

        pwd = st.text_input("Şifre", type="password")

        if st.button("Giriş Yap"):
            if pwd == "1":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Yanlış şifre")

        return False
    return True


# -------------------------------------------------
# ANA UYGULAMA
# -------------------------------------------------
if check_password():

    # -------------------------------------------------
    # CSS
    # -------------------------------------------------
    st.markdown("""
    <style>
    .main { background-color: #0d1117 !important; }

    :root { --soft-orange: #cc7a00; }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 8px 12px !important;
        border: 1px solid var(--soft-orange);
        margin-bottom: 10px;
    }

    h1, h2, h3 {
        color: var(--soft-orange) !important;
        margin: 0 !important;
        font-size: 22px !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid var(--soft-orange);
    }
    </style>
    """, unsafe_allow_html=True)


    # -------------------------------------------------
    # SIDEBAR
    # -------------------------------------------------
    with st.sidebar:
        st.title("🛡️ OG Core")

        page = st.radio(
            "🚀 ürün",
            ["⚡ Ultra Atak Fonu", "⚽️ FormLine", "📊 DashDash"]
        )

        st.divider()

        if page == "⚡ Ultra Atak Fonu":
            kasa = st.number_input("fon bakiyesi (USD)", value=600.0, step=0.1)
        else:
            kasa = 600.0

        tr_tz = pytz.timezone("Europe/Istanbul")
        tr_time = datetime.now(tr_tz).strftime("%H:%M:%S")
        st.info(f"🕒 Sistem Zamanı: {tr_time}")

        if st.button("🔴 çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()


    # -------------------------------------------------
    # ULTRA ATAK FONU
    # -------------------------------------------------
    if page == "⚡ Ultra Atak Fonu":

        st.title("⚡ Ultra Atak Fon")

        try:
            prices = yf.download(
                ["BTC-USD", "ETH-USD", "SOL-USD"],
                period="1d",
                interval="1m",
                progress=False
            )["Close"].iloc[-1]
        except:
            prices = {
                "BTC-USD": 0,
                "ETH-USD": 0,
                "SOL-USD": 0
            }

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            glass_card("TOPLAM", f"${kasa:,.2f}")

        with c2:
            glass_card("BTC", f"${prices['BTC-USD']:,.2f}")

        with c3:
            glass_card("ETH", f"${prices['ETH-USD']:,.2f}")

        with c4:
            glass_card("SOL", f"${prices['SOL-USD']:,.2f}")


    # -------------------------------------------------
    # DİĞER SAYFALAR (placeholder)
    # -------------------------------------------------
    elif page == "⚽️ FormLine":
        st.title("⚽️ FormLine")
        st.write("yakında")

    elif page == "📊 DashDash":
        st.title("📊 DashDash")
        st.write("yakında")
