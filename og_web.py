import streamlit as st
from datetime import datetime
import html
import json
import pandas as pd
import textwrap
import streamlit.components.v1 as components

try:
    import yfinance as yf
except Exception:
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
        df["key"] = df["key"].astype(str).str.strip()
        df["value"] = df["value"].astype(str).str.strip()
        return dict(zip(df["key"], df["value"]))
    except Exception:
        return {"kasa": "600.0", "ana_para": "600.0"}

# --- YARDIMCI FONKSİYONLAR ---
def get_num(data, key, default=0.0):
    try:
        val = data.get(key, default)
        if val is None or str(val).strip() == "":
            return float(default)
        return float(str(val).replace(",", ".").strip())
    except Exception:
        return float(default)

def get_str(data, key, default=""):
    try:
        val = data.get(key, default)
        if val is None:
            return default
        return str(val).strip()
    except Exception:
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

@st.cache_data(ttl=90)
def get_market_snapshot(data):
    snapshot = []

    if yf is not None:
        for symbol, label, decimals in [
            ("BTC-USD", "BTC", 0),
            ("ETH-USD", "ETH", 0),
            ("SOL-USD", "SOL", 2),
        ]:
            try:
                hist = yf.Ticker(symbol).history(period="1d")
                if not hist.empty:
                    price = float(hist["Close"].iloc[-1])
                    snapshot.append((label, f"${price:,.{decimals}f}"))
            except Exception:
                pass

    fallback_assets = [
        ("BTC", get_num(data, "btc_fiyat_usd", 0), "$", 0),
        ("ETH", get_num(data, "eth_fiyat_usd", 0), "$", 0),
        ("SOL", get_num(data, "sol_fiyat_usd", 0), "$", 2),
    ]

    existing_labels = {label for label, _ in snapshot}
    for label, price, prefix, decimals in fallback_assets:
        if label not in existing_labels and price > 0:
            snapshot.append((label, f"{prefix}{price:,.{decimals}f}"))

    usdtry = get_num(data, "usdtry", 0)
    gram_altin = get_num(data, "gram_altin_fiyat", 0)
    ceyrek_altin = get_num(data, "ceyrek_altin_fiyat", 0)

    if usdtry > 0:
        snapshot.append(("USD/TRY", f"₺{usdtry:.2f}"))
    if gram_altin > 0:
        snapshot.append(("GRAM", fmt_money_try(gram_altin)))
    if ceyrek_altin > 0:
        snapshot.append(("ÇEYREK", fmt_money_try(ceyrek_altin)))

    return snapshot

def render_market_ticker(data, announcement):
    market_items = [("DUYURU", announcement)] + get_market_snapshot(data)
    if len(market_items) == 1:
        market_items.append(("SİSTEM", "Piyasa verisi bekleniyor"))

    item_html = ""
    for label, value in market_items * 2:
        item_html += (
            "<span class='ticker-item'>"
            f"<span class='ticker-label'>{html.escape(str(label))}</span>"
            f"<span class='ticker-value'>{html.escape(str(value))}</span>"
            "</span>"
        )

    st.markdown(
        f"<div class='ticker-wrap'><div class='ticker'>{item_html}</div></div>",
        unsafe_allow_html=True
    )

def render_animated_counter(label, value, prefix="", suffix="", decimals=2, subtitle="", accent="#cc7a00", height=152):
    safe_value = float(value or 0)
    card_html = f"""
    <div class="counter-card">
        <div class="counter-label">{html.escape(label)}</div>
        <div class="counter-value" id="counter">0</div>
        <div class="counter-subtitle">{html.escape(subtitle)}</div>
    </div>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');
        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
        }}
        .counter-card {{
            height: {height - 4}px;
            box-sizing: border-box;
            background:
                linear-gradient(135deg, rgba(204,122,0,0.12), transparent 35%),
                rgba(15,15,15,0.86);
            border: 1px solid rgba(255,255,255,0.045);
            border-top: 2px solid {accent};
            border-radius: 6px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 14px 30px rgba(0,0,0,0.38);
            animation: counterIn 520ms ease-out both;
        }}
        .counter-label {{
            color: #858585;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2.6px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .counter-value {{
            color: #f2f2f2;
            font-family: 'Orbitron', monospace;
            font-size: 36px;
            line-height: 1;
            font-weight: 900;
            white-space: nowrap;
        }}
        .counter-subtitle {{
            color: #8d8d8d;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            margin-top: 12px;
        }}
        @media (max-width: 520px) {{
            .counter-card {{
                padding: 18px;
            }}
            .counter-label {{
                font-size: 10px;
                letter-spacing: 2px;
            }}
            .counter-value {{
                font-size: 28px;
            }}
            .counter-subtitle {{
                font-size: 11px;
            }}
        }}
        @keyframes counterIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>

    <script>
        const target = {safe_value};
        const prefix = {json.dumps(prefix)};
        const suffix = {json.dumps(suffix)};
        const decimals = {int(decimals)};
        const el = document.getElementById("counter");
        const start = performance.now();
        const duration = 950;

        function formatValue(value) {{
            const sign = value < 0 ? "-" : "";
            const absolute = Math.abs(value);
            const formatted = absolute.toLocaleString("en-US", {{
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            }});
            return sign + prefix + formatted + suffix;
        }}

        function tick(now) {{
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = formatValue(target * eased);
            if (progress < 1) requestAnimationFrame(tick);
        }}

        requestAnimationFrame(tick);
    </script>
    """
    components.html(card_html, height=height, scrolling=False)

def render_portfolio_hero_component(selected_user_label, total_usd, total_try, active_assets, main_asset_label, main_asset_pct, usdtry):
    hero_html = f"""
    <div class="portfolio-shell">
        <div class="portfolio-topline">
            <span>Portföy Sahibi</span>
            <strong>{html.escape(selected_user_label)}</strong>
        </div>

        <div class="portfolio-hero">
            <div>
                <div class="portfolio-hero-sub">Net Portföy Değeri</div>
                <div class="portfolio-hero-main" id="portfolio-usd">$0.00</div>
                <div class="portfolio-hero-try" id="portfolio-try">≈ ₺0</div>
            </div>

            <div class="portfolio-meta-grid">
                <div class="portfolio-meta-card">
                    <div class="portfolio-meta-label">Aktif Varlık</div>
                    <div class="portfolio-meta-value">{active_assets}</div>
                </div>
                <div class="portfolio-meta-card">
                    <div class="portfolio-meta-label">Ana Varlık</div>
                    <div class="portfolio-meta-value">{html.escape(main_asset_label)}</div>
                </div>
                <div class="portfolio-meta-card">
                    <div class="portfolio-meta-label">Yoğunluk</div>
                    <div class="portfolio-meta-value">%{main_asset_pct:.1f}</div>
                </div>
                <div class="portfolio-meta-card">
                    <div class="portfolio-meta-label">USD/TRY</div>
                    <div class="portfolio-meta-value">₺{usdtry:.2f}</div>
                </div>
            </div>
        </div>
    </div>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&family=Orbitron:wght@400;700;900&display=swap');
        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
        }}
        .portfolio-shell {{
            display: flex;
            flex-direction: column;
            gap: 18px;
            font-family: 'JetBrains Mono', monospace;
        }}
        .portfolio-topline {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            color: #7b7b7b;
            font-size: 11px;
            letter-spacing: 2.4px;
            text-transform: uppercase;
        }}
        .portfolio-topline strong {{
            color: #e2e2e2;
            font-weight: 800;
        }}
        .portfolio-hero {{
            display: grid;
            grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
            gap: 22px;
            background:
                linear-gradient(135deg, rgba(255,174,0,0.10), transparent 26%),
                linear-gradient(180deg, rgba(18,18,18,0.96), rgba(8,8,8,0.96));
            border: 1px solid rgba(255,255,255,0.045);
            border-top: 2px solid rgba(204,122,0,0.72);
            border-radius: 6px;
            padding: 30px;
            box-sizing: border-box;
            box-shadow: 0 18px 45px rgba(0,0,0,0.45);
            animation: heroIn 560ms ease-out both;
        }}
        .portfolio-hero-sub {{
            font-size: 12px;
            color: #858585;
            letter-spacing: 3px;
            text-transform: uppercase;
            margin-bottom: 14px;
        }}
        .portfolio-hero-main {{
            font-size: 58px;
            line-height: 1;
            font-family: 'Orbitron', monospace;
            color: #f0f0f0;
            font-weight: 900;
            white-space: nowrap;
        }}
        .portfolio-hero-try {{
            margin-top: 14px;
            font-size: 16px;
            color: #9a9a9a;
        }}
        .portfolio-meta-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }}
        .portfolio-meta-card {{
            background: rgba(255,255,255,0.025);
            border: 1px solid rgba(255,255,255,0.055);
            border-radius: 6px;
            padding: 16px;
            min-height: 88px;
            box-sizing: border-box;
        }}
        .portfolio-meta-label {{
            color: #777;
            font-size: 10px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .portfolio-meta-value {{
            color: #eeeeee;
            font-family: 'Orbitron', monospace;
            font-size: 18px;
            font-weight: 800;
            white-space: nowrap;
        }}
        @keyframes heroIn {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @media (max-width: 760px) {{
            .portfolio-hero {{
                grid-template-columns: 1fr;
                gap: 18px;
                padding: 20px;
            }}
            .portfolio-hero-main {{
                font-size: 34px;
            }}
            .portfolio-meta-grid {{
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }}
            .portfolio-meta-card {{
                min-height: 72px;
                padding: 12px;
            }}
            .portfolio-meta-label {{
                font-size: 9px;
                letter-spacing: 1.4px;
            }}
            .portfolio-meta-value {{
                font-size: 14px;
            }}
        }}
    </style>

    <script>
        const usdTarget = {float(total_usd or 0)};
        const tryTarget = {float(total_try or 0)};
        const usdEl = document.getElementById("portfolio-usd");
        const tryEl = document.getElementById("portfolio-try");
        const start = performance.now();
        const duration = 1050;

        function moneyUsd(value) {{
            return "$" + value.toLocaleString("en-US", {{
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }});
        }}

        function moneyTry(value) {{
            return "≈ ₺" + value.toLocaleString("en-US", {{
                maximumFractionDigits: 0
            }});
        }}

        function tick(now) {{
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            usdEl.textContent = moneyUsd(usdTarget * eased);
            tryEl.textContent = moneyTry(tryTarget * eased);
            if (progress < 1) requestAnimationFrame(tick);
        }}

        requestAnimationFrame(tick);
    </script>
    """
    components.html(hero_html, height=320, scrolling=False)

def render_smart_alerts(alerts):
    if not alerts:
        return

    cards = ""
    for level, title, body in alerts[:3]:
        cards += (
            f"<div class='smart-alert smart-alert-{level}'>"
            f"<div class='smart-alert-title'>{html.escape(title)}</div>"
            f"<div class='smart-alert-body'>{html.escape(body)}</div>"
            f"</div>"
        )

    st.markdown(
        f"<div class='smart-alert-grid'>{cards}</div>",
        unsafe_allow_html=True
    )

def build_ultra_alerts(ultra_kasa, baslangic_kasa, current_pct, net_kar, risk_state):
    alerts = []
    selected_risk = risk_state.get("selected_risk", "Standart")
    risk_limit = risk_state.get("risk_limit", ultra_kasa * 0.03)

    if ultra_kasa < baslangic_kasa:
        alerts.append(("warn", "Koruma bölgesi", "Kasa başlangıç seviyesinin altında. Koruma modu daha kontrollü kalır."))
    elif current_pct >= 90:
        alerts.append(("good", "Hedef kilidi", "Aktif hedefe çok yaklaşıldı. Kârı korumak burada daha değerli."))
    elif current_pct >= 70:
        alerts.append(("info", "Yaklaşan hedef", "Hedefin büyük kısmı tamamlandı. Risk artışı yerine istikrar daha mantıklı."))

    if selected_risk == "Atak" and current_pct >= 70:
        alerts.append(("warn", "Atak modu yüksek", f"Aktif limit {fmt_money_usd(risk_limit)}. Hedefe yakınken bu mod agresif kalabilir."))
    elif selected_risk == "Koruma":
        alerts.append(("info", "Düşük risk aktif", f"Aktif limit {fmt_money_usd(risk_limit)} ile kasa daha kontrollü ilerliyor."))

    if net_kar > 0:
        alerts.append(("good", "Pozitif bölge", f"Net kâr {fmt_money_usd(net_kar)}. Sistem başlangıcın üstünde çalışıyor."))

    if not alerts:
        alerts.append(("info", "Sistem dengede", "Kasa ve hedef akışı normal bölgede. Standart risk seviyesi yeterli görünüyor."))

    return alerts

def build_portfolio_alerts(active_assets, main_asset_pct, main_asset_label, total_usd):
    if total_usd <= 0:
        return [("warn", "Portföy boş", "Aktif varlık görünmüyor. Sheet tarafında miktar alanlarını kontrol et.")]

    alerts = []
    if active_assets == 1 and main_asset_pct >= 95:
        alerts.append(("warn", "Yoğun portföy", f"Portföy neredeyse tamamen {main_asset_label} üzerinde. Dağılım tek noktada toplanmış."))
    elif active_assets >= 3 and main_asset_pct <= 60:
        alerts.append(("good", "Dengeli yapı", "Portföy birden fazla varlığa yayılmış. Yoğunluk riski düşük görünüyor."))
    else:
        alerts.append(("info", "Portföy izleniyor", "Dağılım normal bölgede. Yeni varlık ekledikçe analiz daha anlamlı olur."))

    return alerts

def parse_kasa_history(data):
    rows = []

    for key, value in data.items():
        if not isinstance(key, str) or not key.startswith("kasa_"):
            continue

        raw_date = key.replace("kasa_", "", 1)
        try:
            date_value = datetime.strptime(raw_date, "%Y_%m_%d").date()
            raw_value = data.get(key, "")
            if raw_value is None or str(raw_value).strip() == "":
                continue
            kasa_value = float(str(raw_value).replace(",", ".").strip())
            rows.append({"Tarih": date_value, "Kasa": kasa_value})
        except Exception:
            continue

    if not rows:
        return pd.DataFrame(columns=["Tarih", "Kasa"])

    df = pd.DataFrame(rows).sort_values("Tarih").drop_duplicates("Tarih", keep="last")
    return df.reset_index(drop=True)

def render_kasa_history_chart(data, current_kasa):
    history_df = parse_kasa_history(data)

    if history_df.empty:
        st.markdown(
            """
            <div class='industrial-card'>
                <div class='terminal-header'>Kasa Geçmişi</div>
                <div class='highlight'>Grafik için Sheet'e kasa_YYYY_MM_DD satırları eklenmeli.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    today = datetime.now().date()
    if today not in set(history_df["Tarih"]):
        history_df = pd.concat(
            [history_df, pd.DataFrame([{"Tarih": today, "Kasa": current_kasa}])],
            ignore_index=True
        ).sort_values("Tarih").drop_duplicates("Tarih", keep="last")

    first_value = float(history_df["Kasa"].iloc[0])
    last_value = float(history_df["Kasa"].iloc[-1])
    high_value = float(history_df["Kasa"].max())
    change_value = last_value - first_value
    change_pct = (change_value / first_value * 100) if first_value > 0 else 0
    change_color = "#00ff41" if change_value >= 0 else "#ff4b4b"

    st.markdown(
        f"""
        <div class='industrial-card'>
            <div class='terminal-header'>Kasa Geçmişi</div>
            <div style='display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:14px; margin-bottom:18px;'>
                <div>
                    <div style='font-size:11px; color:#777; letter-spacing:2px;'>GÜNCEL</div>
                    <div style='font-size:22px; font-weight:900; font-family:Orbitron;'>{fmt_money_usd(last_value)}</div>
                </div>
                <div>
                    <div style='font-size:11px; color:#777; letter-spacing:2px;'>ZİRVE</div>
                    <div style='font-size:22px; font-weight:900; font-family:Orbitron;'>{fmt_money_usd(high_value)}</div>
                </div>
                <div>
                    <div style='font-size:11px; color:#777; letter-spacing:2px;'>DEĞİŞİM</div>
                    <div style='font-size:22px; font-weight:900; font-family:Orbitron; color:{change_color};'>{fmt_money_usd(change_value)} / %{change_pct:.1f}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    chart_df = history_df.copy()
    chart_df["Tarih"] = pd.to_datetime(chart_df["Tarih"])
    chart_df = chart_df.set_index("Tarih")
    st.line_chart(chart_df["Kasa"], height=260)

def render_risk_module(current_kasa):
    risk_profiles = {
        "Koruma": 0.015,
        "Standart": 0.03,
        "Atak": 0.05,
    }

    selected_risk = st.radio(
        "Risk Seviyesi",
        ["Koruma", "Standart", "Atak"],
        horizontal=True,
        key="ultra_risk_level"
    )

    risk_rate = risk_profiles[selected_risk]
    risk_limit = current_kasa * risk_rate

    st.markdown(
        f"""
        <div class='industrial-card'>
            <div class='terminal-header'>Risk Modülü</div>
            <div class='terminal-row'>
                <span>MOD</span>
                <span class='highlight'>{selected_risk}</span>
            </div>
            <div class='terminal-row'>
                <span>ORAN</span>
                <span class='highlight'>%{risk_rate * 100:.1f}</span>
            </div>
            <div class='terminal-row'>
                <span>AKTİF LİMİT</span>
                <span class='highlight'>{fmt_money_usd(risk_limit)}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    return {
        "selected_risk": selected_risk,
        "risk_rate": risk_rate,
        "risk_limit": risk_limit,
    }

live_vars = get_live_data()

kasa = float(get_num(live_vars, "kasa", 600))
ana_para = float(get_num(live_vars, "ana_para", 600))
duyuru_metni = get_str(live_vars, "duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")

# --- KİŞİSEL KASA VERİLERİ ---
og_kasa = float(get_num(live_vars, "oguzo_kasa", kasa / 1))

# --- 💰 FORMLINE HESAPLAMA ---
w1_kar = float(get_num(live_vars, "w1_sonuc", 0))
w2_kar = float(get_num(live_vars, "w2_sonuc", 0))
w3_kar = float(get_num(live_vars, "w3_sonuc", 0))
toplam_bahis_kar = w1_kar + w2_kar + w3_kar

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

.block-container {
    max-width: 1320px;
    padding-top: 1.2rem !important;
    padding-left: 2.2rem !important;
    padding-right: 2.2rem !important;
}

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

div[role="radiogroup"] {
    gap: 8px;
    flex-wrap: wrap;
}

div[role="radiogroup"] label {
    min-width: 0;
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
    min-width: 0;
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
    overflow-wrap: anywhere;
}

.val-std {
    font-size: 22px !important;
    font-weight: 800 !important;
    font-family: 'Orbitron';
}

.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: linear-gradient(90deg, rgba(204, 122, 0, 0.10), rgba(255,255,255,0.025), rgba(204, 122, 0, 0.06));
    border-bottom: 1px solid rgba(204, 122, 0, 0.2);
    border-top: 1px solid rgba(255,255,255,0.035);
    padding: 11px 0;
    margin-bottom: 25px;
}

.ticker {
    display: flex;
    white-space: nowrap;
    width: max-content;
    animation: ticker 38s linear infinite;
}

.ticker-item {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 12px;
    letter-spacing: 2.6px;
    padding-right: 42px;
    text-transform: uppercase;
}

.ticker-label {
    color: #8e8e8e !important;
    font-weight: 800;
}

.ticker-value {
    color: #ffae00 !important;
    font-weight: 900;
}

@keyframes ticker {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

.equal-card {
    min-height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

/* --- PORTFÖY PREMIUM --- */
.portfolio-shell {
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.portfolio-topline {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    color: #7b7b7b !important;
    font-size: 11px;
    letter-spacing: 2.4px;
    text-transform: uppercase;
}

.portfolio-topline strong {
    color: #e2e2e2 !important;
    font-weight: 800;
}

.portfolio-hero {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr);
    gap: 22px;
    background:
        linear-gradient(135deg, rgba(255,174,0,0.10), transparent 26%),
        linear-gradient(180deg, rgba(18,18,18,0.96), rgba(8,8,8,0.96));
    border: 1px solid rgba(255,255,255,0.045);
    border-top: 2px solid rgba(204,122,0,0.72);
    border-radius: 6px;
    padding: 30px;
    margin-bottom: 4px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.45);
}

.portfolio-hero-sub {
    font-size: 12px;
    color: #858585 !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.portfolio-hero-main {
    font-size: 58px;
    line-height: 1;
    font-family: 'Orbitron', monospace !important;
    color: #f0f0f0 !important;
    font-weight: 900;
}

.portfolio-hero-try {
    margin-top: 14px;
    font-size: 16px;
    color: #9a9a9a !important;
}

.portfolio-meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

.portfolio-meta-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 6px;
    padding: 16px;
    min-height: 88px;
}

.portfolio-meta-label {
    color: #777 !important;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.portfolio-meta-value {
    color: #eeeeee !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 18px;
    font-weight: 800;
}

.portfolio-table-card {
    background: rgba(14,14,14,0.88);
    border: 1px solid rgba(255,255,255,0.045);
    border-radius: 6px;
    padding: 22px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.32);
}

.portfolio-table-title {
    color: #8b8b8b !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    margin-bottom: 16px;
    border-left: 3px solid #cc7a00;
    padding-left: 12px;
}

.portfolio-row {
    display: grid;
    grid-template-columns: minmax(0, 1.3fr) minmax(160px, 0.7fr);
    gap: 18px;
    align-items: center;
    padding: 16px 0;
    border-top: 1px solid rgba(255,255,255,0.055);
}

.portfolio-row:first-of-type {
    border-top: 0;
}

.portfolio-row-name strong,
.portfolio-row-value strong {
    display: block;
    color: #f0f0f0 !important;
    font-size: 16px;
    font-weight: 800;
}

.portfolio-row-name span,
.portfolio-row-value span {
    display: block;
    color: #858585 !important;
    font-size: 12px;
    margin-top: 6px;
}

.portfolio-row-value {
    text-align: right;
}

.portfolio-empty {
    color: #a0a0a0 !important;
    font-size: 14px;
    padding: 12px 0;
}

.smart-alert-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin: 4px 0 20px 0;
}

.smart-alert {
    background: rgba(15, 15, 15, 0.82);
    border: 1px solid rgba(255,255,255,0.045);
    border-left: 3px solid #cc7a00;
    border-radius: 6px;
    padding: 16px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.28);
}

.smart-alert-good {
    border-left-color: #00ff41;
}

.smart-alert-warn {
    border-left-color: #ffae00;
}

.smart-alert-info {
    border-left-color: #4ea3ff;
}

.smart-alert-title {
    color: #f0f0f0 !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.smart-alert-body {
    color: #969696 !important;
    font-size: 12px;
    line-height: 1.55;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 0.75rem !important;
    }

    section[data-testid="stSidebar"] {
        min-width: min(320px, 88vw) !important;
        max-width: min(320px, 88vw) !important;
    }

    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 0 !important;
    }

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.75rem !important;
    }

    .industrial-card {
        padding: 18px;
        margin-bottom: 16px;
    }

    .industrial-card:hover {
        transform: none;
    }

    .terminal-row {
        align-items: flex-start;
        gap: 8px;
    }

    .terminal-header {
        font-size: 10px;
        letter-spacing: 2px;
        margin-bottom: 14px;
    }

    .ticker-wrap {
        margin-left: -1rem;
        margin-right: -1rem;
        width: calc(100% + 2rem);
        padding: 9px 0;
        margin-bottom: 18px;
    }

    .ticker-item {
        font-size: 10px;
        letter-spacing: 1.8px;
        padding-right: 28px;
        gap: 8px;
    }

    .portfolio-hero {
        grid-template-columns: 1fr;
        padding: 22px;
    }

    .portfolio-hero-main {
        font-size: 38px;
    }

    .portfolio-meta-grid {
        grid-template-columns: 1fr;
    }

    .portfolio-row {
        grid-template-columns: 1fr;
        gap: 8px;
    }

    .portfolio-row-value {
        text-align: left;
    }

    .smart-alert-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 520px) {
    .block-container {
        padding-left: 0.72rem !important;
        padding-right: 0.72rem !important;
    }

    section[data-testid="stSidebar"] {
        min-width: 86vw !important;
        max-width: 86vw !important;
    }

    section[data-testid="stSidebar"] h1 {
        font-size: 20px !important;
        letter-spacing: 4px !important;
        margin-bottom: 28px !important;
    }

    .stButton button, .stLinkButton a {
        padding: 10px !important;
        font-size: 12px !important;
    }

    .industrial-card {
        padding: 15px;
        border-radius: 6px;
    }

    .terminal-row {
        font-size: 12px;
    }

    .val-std {
        font-size: 18px !important;
    }

    .smart-alert {
        padding: 14px;
    }

    .smart-alert-title {
        font-size: 11px;
        letter-spacing: 1.4px;
    }

    .smart-alert-body {
        font-size: 11px;
    }

    .portfolio-table-card {
        padding: 16px;
    }

    .portfolio-table-title {
        font-size: 10px;
        letter-spacing: 2px;
    }

    .portfolio-row {
        padding: 14px 0;
    }

    .portfolio-row-name strong,
    .portfolio-row-value strong {
        font-size: 14px;
    }

    .portfolio-row-name span,
    .portfolio-row-value span {
        font-size: 11px;
        line-height: 1.45;
    }
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

@media (max-width: 520px) {
    div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
        width: calc(100vw - 34px) !important;
        padding: 42px 22px !important;
        border-radius: 14px !important;
    }

    input[type="password"] {
        font-size: 22px !important;
        letter-spacing: 9px !important;
    }
}

.stButton { visibility: hidden; height: 0; margin: 0; padding: 0; }
</style>
"""

# --- 4. HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>türkiye - xxx </span><span class='highlight'>türkiye w</span></div><div class='terminal-row'><span>türkiye - aaa</span><span class='highlight'>türkiye w</span></div><div class='terminal-row'><span>rizespor - gala</span><span class='highlight'></span></div><div class='terminal-row'><span></span><span class='highlight'></span></div><div class='terminal-row'><span></span><span class='highlight'></span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bet: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>gala - kayserispor</span><span style='color:#00ff41;'>gala w & iy +1 & 2+ ✅</span></div><div class='terminal-row'><span>liverpool - newcastle</span><span style='color:#00ff41;'>+2 & liverpool 1x ✅</span></div><div class='terminal-row'><span>bvb - heidenheim</span><span style='color:#00ff41;'>bvb w & iy +1 & 2+ ✅</span></div><div class='terminal-row'><span>kocaelispor - fenerbahçe</span><span style='color:#00ff41;'>fenerbahçe w & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bet: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>karagümrük - gala</span><span style='color:#ff4b4b;'>gala w & +2 ✅</span></div><div class='terminal-row'><span>bournemouth - liverpool</span><span style='color:#00ff41;'>kg ✅</span></div><div class='terminal-row'><span>union berlin - bvb</span><span style='color:#00ff41;'>iy +1 ✅</span></div><div class='terminal-row'><span>newcastle - aston villa</span><span style='color:#ff4b4b;'>newcastle +2 ❌</span></div><div class='terminal-row'><span>fenerbahçe - göztepe</span><span style='color:#ff4b4b;'>fenerbahçe w ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bet: 100 USD</span></div>"""

w3_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W3 KUPONU (BAŞARILI)</div>{w3_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #00ff41 !important;'><div class='terminal-header' style='color:#00ff41;'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}<span style='color:#00ff41; font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #ff4b4b !important;'><div class='terminal-header' style='color:#ff4b4b;'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}<span style='color:#ff4b4b; font-weight:bold;'>SONUÇLANDI ❌</span></div>"

# --- 5. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        pwd = st.text_input("PIN", type="password", placeholder="----", label_visibility="collapsed")
        if pwd:
            if pwd == "0644":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("ACCESS DENIED")
        return False
    return True

# --- PORTFÖY YARDIMCI FONKSİYONLAR ---
def discover_dynamic_instruments(data, users):
    instrument_codes = set()

    for key in data.keys():
        if isinstance(key, str) and key.startswith("price_"):
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
            "legacy_map": {"oguzo": "oguzo_usd"},
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
    st.markdown("<div class='terminal-header'>🏛️ PORTFÖY MERKEZİ</div>", unsafe_allow_html=True)

    users = ["oguzo"]
    user_labels = {"oguzo": "OGUZO"}

    usdtry = get_num(data, "usdtry", 44.18)

    dynamic_instruments = discover_dynamic_instruments(data, users)
    instruments = dynamic_instruments if len(dynamic_instruments) > 0 else build_legacy_fallback_instruments(data)

    if len(instruments) == 0:
        st.error("Portföy enstrümanları bulunamadı.")
        return

    if len(users) > 1:
        selected_user_label = st.selectbox("Portföy:", [user_labels[u] for u in users], label_visibility="collapsed")
        selected_user = [k for k, v in user_labels.items() if v == selected_user_label][0]
    else:
        selected_user = users[0]
        selected_user_label = user_labels[selected_user]

    df_user = build_user_portfolio(data, selected_user, instruments, usdtry)

    if df_user.empty:
        st.error("Seçilen kullanıcı için portföy verisi bulunamadı.")
        return

    total_usd = df_user["total_usd"].sum()
    total_try = df_user["total_try"].sum()
    df_nonzero = df_user[df_user["quantity"] > 0].copy()

    active_assets = len(df_nonzero)
    if df_nonzero.empty or total_usd <= 0:
        main_asset_label = "YOK"
        main_asset_pct = 0
    else:
        main_asset = df_nonzero.sort_values("total_usd", ascending=False).iloc[0]
        main_asset_label = main_asset["label"]
        main_asset_pct = (main_asset["total_usd"] / total_usd) * 100

    render_portfolio_hero_component(
        selected_user_label,
        total_usd,
        total_try,
        active_assets,
        main_asset_label,
        main_asset_pct,
        usdtry,
    )

    render_smart_alerts(build_portfolio_alerts(active_assets, main_asset_pct, main_asset_label, total_usd))

    if df_nonzero.empty:
        empty_html = (
            "<div class='portfolio-table-card'>"
            "<div class='portfolio-table-title'>Varlıklar</div>"
            "<div class='portfolio-empty'>Aktif varlık bulunamadı.</div>"
            "</div>"
        )
        st.markdown(empty_html, unsafe_allow_html=True)
        return

    rows_html = ""
    for _, row in df_nonzero.sort_values("total_usd", ascending=False).iterrows():
        qty_text = fmt_unit_value(row["quantity"], row["unit"])
        price_text = fmt_money_usd(row["price"]) if row["currency"] == "USD" else fmt_money_try(row["price"])
        value_text = fmt_money_usd(row["total_usd"])
        local_text = fmt_money_try(row["total_try"])

        rows_html += (
            f"<div class='portfolio-row'>"
            f"<div class='portfolio-row-name'>"
            f"<strong>{row['label']}</strong>"
            f"<span>{qty_text} · Birim {price_text}</span>"
            f"</div>"
            f"<div class='portfolio-row-value'>"
            f"<strong>{value_text}</strong>"
            f"<span>{local_text}</span>"
            f"</div>"
            f"</div>"
        )

    table_html = (
        f"<div class='portfolio-table-card'>"
        f"<div class='portfolio-table-title'>Varlıklar</div>"
        f"{rows_html}"
        f"</div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)

    if len(df_nonzero) > 1:
        render_allocation_panel(df_nonzero)

# --- 6. ANA UYGULAMA ---
if not check_password():
    st.stop()

st.markdown(common_css, unsafe_allow_html=True)
st.markdown("<style>.stApp { background: #030303 !important; background-image: none !important; }</style>", unsafe_allow_html=True)
render_market_ticker(live_vars, duyuru_metni)

with st.sidebar:
    st.markdown(
        "<h1 style='color:white; font-family:Orbitron; font-size:24px; letter-spacing:5px; text-align:center; margin-bottom:40px;'>OG CORE</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='margin-bottom:10px; color:#666; font-size:11px; letter-spacing:2px; font-weight:800;'>SİSTEM MODÜLLERİ</div>",
        unsafe_allow_html=True
    )
    page = st.radio("Menu", ["⚡ ULTRA ATAK", "⚽ FORMLINE", "📊 Portföy Takip"], label_visibility="collapsed")
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
        st.rerun()

if page == "⚡ ULTRA ATAK":
    st.markdown("<div class='terminal-header'>💰 Oguzo Kasa</div>", unsafe_allow_html=True)

    ultra_kasa = og_kasa
    baslangic_kasa = 2250
    hedefler = [4500, 9000, 14000, 18000, 22500]

    net_kar = ultra_kasa - baslangic_kasa
    aktif_hedef = next((h for h in hedefler if ultra_kasa < h), hedefler[-1])
    onceki_hedef = baslangic_kasa

    for hedef in hedefler:
        if ultra_kasa >= hedef:
            onceki_hedef = hedef
        else:
            break

    if ultra_kasa >= hedefler[-1]:
        current_pct = 100
        hedef_baslik = "Final Hedef Tamamlandı"
    else:
        hedef_aralik = max(1, aktif_hedef - onceki_hedef)
        current_pct = max(0, min(100, ((ultra_kasa - onceki_hedef) / hedef_aralik) * 100))
        hedef_baslik = f"Hedef Yolculuğu ({fmt_money_usd(aktif_hedef)})"

    render_animated_counter(
        "Oguzo Bakiye",
        ultra_kasa,
        prefix="$",
        decimals=2,
        subtitle=f"Net kâr: {fmt_money_usd(net_kar)}",
        height=148
    )

    st.divider()

    st.markdown(
        f"""
        <div class='industrial-card'>
            <div class='terminal-header'>{hedef_baslik}</div>
            <div style='display:flex; justify-content:space-between; gap:18px; flex-wrap:wrap; margin-bottom:18px;'>
                <div>
                    <div style='font-size:12px; color:#666;'>Başlangıç Kasa</div>
                    <div style='font-size:22px; font-weight:800;'>${baslangic_kasa:,.2f}</div>
                </div>
                <div>
                    <div style='font-size:12px; color:#666;'>Aktif Hedef</div>
                    <div style='font-size:22px; font-weight:900; color:#cc7a00;'>${aktif_hedef:,.2f}</div>
                </div>
                <div>
                    <div style='font-size:12px; color:#666;'>Net Kâr</div>
                    <div style='font-size:22px; font-weight:900; color:{'#00ff41' if net_kar >= 0 else '#ff4b4b'};'>${net_kar:,.2f}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(int(current_pct))

    st.markdown(
        f"""
        <div style='margin-top:8px; font-size:13px; color:#888; text-align:right;'>
            %{current_pct:.1f}
        </div>
        """,
        unsafe_allow_html=True
    )

    risk_state = render_risk_module(ultra_kasa)
    render_smart_alerts(build_ultra_alerts(ultra_kasa, baslangic_kasa, current_pct, net_kar, risk_state))
    render_kasa_history_chart(live_vars, ultra_kasa)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class='industrial-card' style='height:230px;'>
                <div class='terminal-header'>💎 KASA</div>
                <div class='terminal-row'>
                    <span>TOPLAM</span>
                    <span class='highlight'>${ultra_kasa:,.2f}</span>
                </div>
                <div class='terminal-row'>
                    <span>K/Z</span>
                    <span style='color:{'#00ff41' if net_kar >= 0 else '#ff4b4b'};' class='val-std'>${net_kar:,.2f}</span>
                </div>
            </div>
            """,
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

        except Exception:
            st.markdown(
                """
                <div class='industrial-card' style='height:230px;'>
                    <div class='terminal-header'>⚡ PİYASA</div>
                    <div class='highlight'>Piyasa verisi bekleniyor...</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col3:
        render_animated_counter(
            "Win Rate",
            get_num({"wr": wr_oran}, "wr", 0),
            prefix="%",
            decimals=0,
            subtitle="Performans göstergesi",
            height=230
        )

    st.markdown("### 📜 SON İŞLEMLER")
    st.markdown(
        f"""
        <div class='industrial-card'>
            <div class='terminal-header'>AKTİVİTE LOGLARI</div>
            <p style='font-family:JetBrains Mono; color:#888;'>{son_islemler_raw}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "⚽ FORMLINE":
    render_animated_counter(
        "Formline Net",
        toplam_bahis_kar,
        prefix="$",
        decimals=2,
        subtitle="Toplam bahis performansı",
        accent="#00ff41" if toplam_bahis_kar >= 0 else "#ff4b4b",
        height=150
    )

    if toplam_bahis_kar > 0:
        render_smart_alerts([("good", "Formline pozitif", f"Net sonuç {fmt_money_usd(toplam_bahis_kar)}. Seri kârlı bölgede.")])
    elif toplam_bahis_kar < 0:
        render_smart_alerts([("warn", "Formline negatif", f"Net sonuç {fmt_money_usd(toplam_bahis_kar)}. Risk seviyesini düşük tutmak daha mantıklı.")])

    t1, t2, t3 = st.tabs(["✅ W3", "✅ W2", "❌ W1"])

    with t1:
        st.markdown(w3_coupon_html, unsafe_allow_html=True)

    with t2:
        st.markdown(w2_coupon_html, unsafe_allow_html=True)

    with t3:
        st.markdown(w1_coupon_html, unsafe_allow_html=True)

elif page == "📊 Portföy Takip":
    render_portfolio_v2(live_vars)
