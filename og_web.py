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

# --- 2. VERİ KATMANI ---
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

# --- 3. FORMAT VE TEMEL YARDIMCILAR ---
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

# --- 4. ORTAK UI BİLEŞENLERİ ---
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

def render_animated_counter(label, value, prefix="", suffix="", decimals=2, subtitle="", accent="#c58a2c", height=152):
    safe_value = float(value or 0)
    card_html = f"""
    <div class="counter-card">
        <div class="counter-label">{html.escape(label)}</div>
        <div class="counter-value" id="counter">0</div>
        <div class="counter-subtitle">{html.escape(subtitle)}</div>
    </div>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&display=swap');
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
                linear-gradient(135deg, rgba(197,138,44,0.12), transparent 35%),
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
            font-family: 'JetBrains Mono', monospace;
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
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&display=swap');
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
                linear-gradient(135deg, rgba(197,138,44,0.10), transparent 26%),
                linear-gradient(180deg, rgba(18,18,18,0.96), rgba(8,8,8,0.96));
            border: 1px solid rgba(255,255,255,0.045);
            border-top: 2px solid rgba(197,138,44,0.72);
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
            font-family: 'JetBrains Mono', monospace;
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
            font-family: 'JetBrains Mono', monospace;
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

    grid_class = "smart-alert-grid single" if len(alerts) == 1 else "smart-alert-grid"
    cards = ""
    for level, title, body in alerts[:3]:
        cards += (
            f"<div class='smart-alert smart-alert-{level}'>"
            f"<div class='smart-alert-title'>{html.escape(title)}</div>"
            f"<div class='smart-alert-body'>{html.escape(body)}</div>"
            f"</div>"
        )

    st.markdown(
        f"<div class='{grid_class}'>{cards}</div>",
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

# --- 5. ULTRA ATAK KARAR PANELLERİ ---
def build_next_move(ultra_kasa, baslangic_kasa, aktif_hedef, current_pct, net_kar, risk_state, peak_value):
    selected_risk = risk_state.get("selected_risk", "Standart")
    drawdown = max(0, peak_value - ultra_kasa)
    drawdown_pct = (drawdown / peak_value * 100) if peak_value > 0 else 0

    if ultra_kasa < baslangic_kasa:
        return "KORU", "Başlangıç kasanın altındasın. Koruma modu ve düşük tempo daha doğru."
    if current_pct >= 85:
        return "KİLİTLE", f"Hedefe %{current_pct:.1f} yaklaşıldı. Risk artırmak yerine kârı koru."
    if drawdown_pct >= 8:
        return "TOPARLAN", f"Zirveden %{drawdown_pct:.1f} aşağıdasın. Öncelik zirveye dönüş olsun."
    if selected_risk == "Atak" and net_kar <= 0:
        return "RİSK DÜŞÜR", "Atak modu negatif bölgede pahalı kalır. Standart veya Koruma daha sağlıklı."
    if net_kar > 0 and selected_risk == "Koruma":
        return "STANDART SERBEST", "Kasa pozitif bölgede. İstersen Standart moda geçiş alanı var."

    remaining = max(0, aktif_hedef - ultra_kasa)
    return "STANDARTTA KAL", f"Akış dengeli. Aktif hedefe kalan {fmt_money_usd(remaining)}."

def render_ultra_decision_panels(data, ultra_kasa, baslangic_kasa, aktif_hedef, current_pct, net_kar, risk_state):
    history_df = parse_kasa_history(data)
    if history_df.empty:
        peak_value = max(ultra_kasa, baslangic_kasa)
    else:
        peak_value = max(float(history_df["Kasa"].max()), ultra_kasa)

    selected_risk = risk_state.get("selected_risk", "Standart")
    risk_rate = float(risk_state.get("risk_rate", 0.03))
    risk_limit = float(risk_state.get("risk_limit", ultra_kasa * risk_rate))

    move_title, move_body = build_next_move(
        ultra_kasa,
        baslangic_kasa,
        aktif_hedef,
        current_pct,
        net_kar,
        risk_state,
        peak_value,
    )

    safe_rate = 0.80
    growth_rate = max(0, 1 - safe_rate - risk_rate)
    safe_pool = ultra_kasa * safe_rate
    growth_pool = ultra_kasa * growth_rate

    recovery_needed = max(0, peak_value - ultra_kasa)
    recovery_pct = 100 if peak_value <= 0 else max(0, min(100, (ultra_kasa / peak_value) * 100))
    recovery_status = "ZİRVEDE" if recovery_needed <= 0 else "TOPARLANMA"

    panel_html = (
        "<div class='decision-grid'>"
        "<div class='decision-card decision-primary'>"
        "<div class='decision-kicker'>Sıradaki Hamle</div>"
        f"<div class='decision-title'>{html.escape(move_title)}</div>"
        f"<div class='decision-body'>{html.escape(move_body)}</div>"
        "</div>"
        "<div class='decision-card'>"
        "<div class='decision-kicker'>Kasa Dağılımı</div>"
        "<div class='vault-row'><span>Güvenli Kasa</span><strong>" + fmt_money_usd(safe_pool) + "</strong></div>"
        "<div class='vault-bar'><i style='width:80%;'></i></div>"
        f"<div class='vault-row'><span>Risk Payı · {html.escape(selected_risk)}</span><strong>{fmt_money_usd(risk_limit)}</strong></div>"
        f"<div class='vault-row'><span>Büyüme Payı</span><strong>{fmt_money_usd(growth_pool)}</strong></div>"
        "</div>"
        "<div class='decision-card'>"
        "<div class='decision-kicker'>Toparlanma Ölçeri</div>"
        f"<div class='decision-title'>{recovery_status}</div>"
        f"<div class='decision-body'>Zirve {fmt_money_usd(peak_value)} · Geri dönüş {fmt_money_usd(recovery_needed)}</div>"
        f"<div class='recovery-track'><i style='width:{recovery_pct:.1f}%;'></i></div>"
        f"<div class='recovery-label'>%{recovery_pct:.1f}</div>"
        "</div>"
        "</div>"
    )
    st.markdown(panel_html, unsafe_allow_html=True)

# --- 6. KASA GEÇMİŞİ ---
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
    low_value = float(history_df["Kasa"].min())
    change_value = last_value - first_value
    change_pct = (change_value / first_value * 100) if first_value > 0 else 0
    change_color = "#c58a2c"
    width = 900
    height = 230
    pad_x = 34
    pad_y = 26
    values = [float(v) for v in history_df["Kasa"].tolist()]
    dates = history_df["Tarih"].tolist()
    value_range = max(high_value - low_value, 1)
    point_count = len(values)

    points = []
    for idx, value in enumerate(values):
        x = pad_x if point_count == 1 else pad_x + (idx / (point_count - 1)) * (width - pad_x * 2)
        y = pad_y + (1 - ((value - low_value) / value_range)) * (height - pad_y * 2)
        points.append((x, y, value))

    line_points = " ".join([f"{x:.1f},{y:.1f}" for x, y, _ in points])
    area_points = f"{pad_x},{height - pad_y} {line_points} {width - pad_x},{height - pad_y}"
    circles = ""
    for x, y, value in points:
        circles += f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4.2' class='chart-dot'><title>{fmt_money_usd(value)}</title></circle>"

    first_label = dates[0].strftime("%d.%m") if dates else "-"
    last_label = dates[-1].strftime("%d.%m") if dates else "-"
    period_label = f"{len(history_df)} kayıt · {first_label} - {last_label}"
    trend_label = "POZİTİF" if change_value >= 0 else "NEGATİF"

    chart_html = f"""
    <div class="kasa-history-card">
        <div class="kasa-history-head">
            <div>
                <div class="kasa-eyebrow">Kasa Geçmişi</div>
                <div class="kasa-title">Performans İzleme</div>
            </div>
            <div class="kasa-badge">{trend_label}</div>
        </div>

        <div class="kasa-metrics">
            <div class="metric">
                <span>Güncel</span>
                <strong>{fmt_money_usd(last_value)}</strong>
            </div>
            <div class="metric">
                <span>Zirve</span>
                <strong>{fmt_money_usd(high_value)}</strong>
            </div>
            <div class="metric">
                <span>Değişim</span>
                <strong style="color:{change_color};">{fmt_money_usd(change_value)} / %{change_pct:.1f}</strong>
            </div>
        </div>

        <div class="chart-wrap">
            <svg viewBox="0 0 {width} {height}" preserveAspectRatio="none" role="img">
                <defs>
                    <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="rgba(197,138,44,0.26)" />
                        <stop offset="100%" stop-color="rgba(197,138,44,0.00)" />
                    </linearGradient>
                    <filter id="glow">
                        <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                        <feMerge>
                            <feMergeNode in="coloredBlur"/>
                            <feMergeNode in="SourceGraphic"/>
                        </feMerge>
                    </filter>
                </defs>
                <line x1="{pad_x}" y1="{pad_y}" x2="{pad_x}" y2="{height - pad_y}" class="grid-axis" />
                <line x1="{pad_x}" y1="{height - pad_y}" x2="{width - pad_x}" y2="{height - pad_y}" class="grid-axis" />
                <line x1="{pad_x}" y1="{pad_y + (height - pad_y * 2) * 0.33:.1f}" x2="{width - pad_x}" y2="{pad_y + (height - pad_y * 2) * 0.33:.1f}" class="grid-line" />
                <line x1="{pad_x}" y1="{pad_y + (height - pad_y * 2) * 0.66:.1f}" x2="{width - pad_x}" y2="{pad_y + (height - pad_y * 2) * 0.66:.1f}" class="grid-line" />
                <polygon points="{area_points}" class="chart-area" />
                <polyline points="{line_points}" class="chart-line" filter="url(#glow)" />
                {circles}
            </svg>
        </div>

        <div class="kasa-history-foot">
            <span>{period_label}</span>
            <span>Dip {fmt_money_usd(low_value)}</span>
        </div>
    </div>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&display=swap');
        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
        }}
        .kasa-history-card {{
            box-sizing: border-box;
            height: 100%;
            background:
                radial-gradient(circle at 12% 0%, rgba(197,138,44,0.12), transparent 28%),
                linear-gradient(180deg, rgba(16,16,16,0.96), rgba(7,7,7,0.96));
            border: 1px solid rgba(255,255,255,0.05);
            border-top: 2px solid rgba(197,138,44,0.72);
            border-radius: 6px;
            padding: 22px;
            font-family: 'JetBrains Mono', monospace;
            color: #d1d1d1;
            box-shadow: 0 18px 45px rgba(0,0,0,0.42);
            animation: panelIn 520ms ease-out both;
        }}
        .kasa-history-head,
        .kasa-history-foot {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 14px;
        }}
        .kasa-eyebrow {{
            color: #8b8b8b;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 2.8px;
            text-transform: uppercase;
            border-left: 3px solid #c58a2c;
            padding-left: 12px;
            margin-bottom: 8px;
        }}
        .kasa-title {{
            color: #f0f0f0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 22px;
            font-weight: 900;
        }}
        .kasa-badge {{
            border: 1px solid rgba(197,138,44,0.32);
            background: rgba(197,138,44,0.08);
            color: #c58a2c;
            border-radius: 999px;
            padding: 8px 12px;
            font-size: 10px;
            font-weight: 900;
            letter-spacing: 2px;
        }}
        .kasa-metrics {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: 18px 0 14px 0;
        }}
        .metric {{
            background: rgba(255,255,255,0.026);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 6px;
            padding: 14px;
        }}
        .metric span {{
            display: block;
            color: #777;
            font-size: 10px;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }}
        .metric strong {{
            display: block;
            color: #f0f0f0;
            font-family: 'JetBrains Mono', monospace;
            font-size: 18px;
            font-weight: 900;
            white-space: nowrap;
        }}
        .chart-wrap {{
            height: 210px;
            border: 1px solid rgba(255,255,255,0.035);
            background: rgba(0,0,0,0.18);
            border-radius: 6px;
            overflow: hidden;
        }}
        svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}
        .grid-axis {{
            stroke: rgba(255,255,255,0.13);
            stroke-width: 1;
        }}
        .grid-line {{
            stroke: rgba(255,255,255,0.06);
            stroke-width: 1;
            stroke-dasharray: 6 8;
        }}
        .chart-area {{
            fill: url(#areaFill);
        }}
        .chart-line {{
            fill: none;
            stroke: #c58a2c;
            stroke-width: 4;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}
        .chart-dot {{
            fill: #050505;
            stroke: #c58a2c;
            stroke-width: 3;
        }}
        .kasa-history-foot {{
            color: #858585;
            font-size: 11px;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            margin-top: 12px;
        }}
        @keyframes panelIn {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @media (max-width: 620px) {{
            .kasa-history-card {{
                padding: 16px;
            }}
            .kasa-history-head,
            .kasa-history-foot {{
                align-items: flex-start;
                flex-direction: column;
            }}
            .kasa-title {{
                font-size: 18px;
            }}
            .kasa-metrics {{
                grid-template-columns: 1fr;
                gap: 8px;
                margin: 14px 0;
            }}
            .metric {{
                padding: 12px;
            }}
            .metric strong {{
                font-size: 16px;
            }}
            .chart-wrap {{
                height: 170px;
            }}
        }}
    </style>
    """

    components.html(chart_html, height=440, scrolling=False)

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

# --- 7. CANLI VERİ DEĞİŞKENLERİ ---
live_vars = get_live_data()

kasa = float(get_num(live_vars, "kasa", 600))
ana_para = float(get_num(live_vars, "ana_para", 600))
duyuru_metni = get_str(live_vars, "duyuru", "SİSTEM ÇEVRİMİÇİ... OG CORE")

# Kişisel kasa verileri
og_kasa = float(get_num(live_vars, "oguzo_kasa", kasa / 1))

# Form takibi hesaplama
w1_kar = float(get_num(live_vars, "w1_sonuc", 0))
w2_kar = float(get_num(live_vars, "w2_sonuc", 0))
w3_kar = float(get_num(live_vars, "w3_sonuc", 0))
toplam_bahis_kar = w1_kar + w2_kar + w3_kar

wr_oran = get_str(live_vars, "win_rate", "0")
son_islemler_raw = get_str(live_vars, "son_islemler", "Veri yok")

# --- 8. STİL SİSTEMİ ---
common_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700;800&display=swap');

:root {
    --og-bg: #050505;
    --og-surface: rgba(15, 15, 15, 0.86);
    --og-surface-soft: rgba(255,255,255,0.026);
    --og-border: rgba(255,255,255,0.05);
    --og-accent: #c58a2c;
    --og-accent-soft: rgba(197,138,44,0.12);
    --og-text: #e6e2da;
    --og-muted: #8b867c;
    --og-radius: 6px;
}

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
    border-right: 1px solid rgba(197, 138, 44, 0.15);
    padding-top: 20px;
    min-width: 340px !important;
    max-width: 340px !important;
}

.stButton button, .stLinkButton a {
    width: 100% !important;
    background: var(--og-accent-soft) !important;
    border: 1px solid rgba(197, 138, 44, 0.30) !important;
    color: var(--og-accent) !important;
    font-family: 'JetBrains Mono', monospace !important;
    padding: 12px !important;
    border-radius: var(--og-radius) !important;
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
    color: var(--og-text) !important;
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
    background: var(--og-surface) !important;
    backdrop-filter: blur(5px);
    border: 1px solid var(--og-border) !important;
    border-top: 2px solid rgba(197, 138, 44, 0.48) !important;
    padding: 22px;
    margin-bottom: 20px;
    border-radius: var(--og-radius);
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    transition: all 0.25s ease;
}

.industrial-card:hover {
    transform: translateY(-3px);
    border-top-color: var(--og-accent) !important;
    background: rgba(21, 21, 21, 0.9) !important;
    box-shadow: 0 8px 22px rgba(197, 138, 44, 0.11);
}

.terminal-header {
    color: var(--og-muted);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    margin-bottom: 18px;
    border-left: 3px solid var(--og-accent);
    padding-left: 12px;
}

.highlight {
    color: var(--og-text) !important;
    font-weight: 500;
    font-size: 14px;
    font-family: 'JetBrains Mono', monospace;
    overflow-wrap: anywhere;
}

.val-std {
    font-size: 22px !important;
    font-weight: 800 !important;
    font-family: 'JetBrains Mono', monospace;
}

.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: linear-gradient(90deg, rgba(197, 138, 44, 0.10), rgba(255,255,255,0.025), rgba(197, 138, 44, 0.06));
    border-bottom: 1px solid rgba(197, 138, 44, 0.2);
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
    color: var(--og-accent) !important;
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

/* --- PORTFÖY TABLOSU --- */
.portfolio-table-card {
    background: var(--og-surface);
    border: 1px solid var(--og-border);
    border-radius: var(--og-radius);
    padding: 22px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.32);
}

.portfolio-table-title {
    color: var(--og-muted) !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2.8px;
    text-transform: uppercase;
    margin-bottom: 16px;
    border-left: 3px solid var(--og-accent);
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
    color: var(--og-text) !important;
    font-size: 16px;
    font-weight: 800;
}

.portfolio-row-name span,
.portfolio-row-value span {
    display: block;
    color: var(--og-muted) !important;
    font-size: 12px;
    margin-top: 6px;
}

.portfolio-row-value {
    text-align: right;
}

.portfolio-empty {
    color: var(--og-muted) !important;
    font-size: 14px;
    padding: 12px 0;
}

.smart-alert-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin: 4px 0 20px 0;
}

.smart-alert-grid.single {
    grid-template-columns: 1fr;
}

.smart-alert {
    background: var(--og-surface);
    border: 1px solid var(--og-border);
    border-left: 3px solid var(--og-accent);
    border-radius: var(--og-radius);
    padding: 16px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.28);
}

.smart-alert-good {
    border-left-color: var(--og-accent);
}

.smart-alert-warn {
    border-left-color: var(--og-accent);
}

.smart-alert-info {
    border-left-color: var(--og-accent);
}

.smart-alert-title {
    color: var(--og-text) !important;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.smart-alert-body {
    color: var(--og-muted) !important;
    font-size: 12px;
    line-height: 1.55;
}

.decision-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
    margin: 2px 0 20px 0;
}

.decision-card {
    background:
        linear-gradient(135deg, var(--og-accent-soft), transparent 34%),
        var(--og-surface);
    border: 1px solid var(--og-border);
    border-top: 2px solid rgba(197,138,44,0.54);
    border-radius: var(--og-radius);
    padding: 18px;
    min-height: 160px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.32);
}

.decision-primary {
    border-top-color: var(--og-accent);
}

.decision-kicker {
    color: var(--og-muted) !important;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 2.4px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.decision-title {
    color: var(--og-text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 24px;
    line-height: 1.08;
    font-weight: 900;
    margin-bottom: 12px;
}

.decision-body {
    color: var(--og-muted) !important;
    font-size: 12px;
    line-height: 1.55;
}

.vault-row {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    color: var(--og-muted) !important;
    font-size: 12px;
    margin: 10px 0;
}

.vault-row strong {
    color: var(--og-text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px;
    white-space: nowrap;
}

.vault-bar,
.recovery-track {
    width: 100%;
    height: 9px;
    border-radius: 999px;
    background: rgba(255,255,255,0.055);
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.035);
    margin: 12px 0;
}

.vault-bar i,
.recovery-track i {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #8f6426, var(--og-accent));
    box-shadow: 0 0 16px rgba(197,138,44,0.24);
}

.recovery-label {
    color: var(--og-accent) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 18px;
    font-weight: 900;
    text-align: right;
}

.ops-summary-card {
    background:
        linear-gradient(135deg, var(--og-accent-soft), transparent 34%),
        var(--og-surface);
    border: 1px solid var(--og-border);
    border-top: 2px solid rgba(197,138,44,0.62);
    border-radius: var(--og-radius);
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 12px 28px rgba(0,0,0,0.32);
}

.ops-summary-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
}

.ops-summary-item {
    background: var(--og-surface-soft);
    border: 1px solid var(--og-border);
    border-radius: var(--og-radius);
    padding: 14px;
}

.ops-summary-item span {
    display: block;
    color: var(--og-muted) !important;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.ops-summary-item strong {
    display: block;
    color: var(--og-text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 18px;
    font-weight: 900;
    white-space: nowrap;
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

    .decision-grid {
        grid-template-columns: 1fr;
    }

    .decision-card {
        min-height: auto;
    }

    .ops-summary-grid {
        grid-template-columns: 1fr 1fr;
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

    .decision-title {
        font-size: 20px;
    }

    .vault-row {
        font-size: 11px;
    }

    .ops-summary-card {
        padding: 16px;
    }

    .ops-summary-grid {
        grid-template-columns: 1fr;
    }

    .ops-summary-item strong {
        font-size: 16px;
    }
}
</style>
"""

login_bg_css = """
<style>
.stApp {
    background:
        radial-gradient(circle at 18% 24%, rgba(197,138,44,0.18), transparent 34%),
        radial-gradient(circle at 78% 72%, rgba(197,138,44,0.10), transparent 36%),
        linear-gradient(135deg, #030303 0%, #090806 44%, #020202 100%) !important;
    background-attachment: fixed !important;
}

.stApp::before {
    content: "";
    position: fixed !important;
    inset: 0 !important;
    pointer-events: none !important;
    z-index: 0 !important;
    background-image:
        linear-gradient(rgba(197,138,44,0.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(197,138,44,0.045) 1px, transparent 1px);
    background-size: 54px 54px;
    mask-image: radial-gradient(circle at center, rgba(0,0,0,0.82), transparent 72%);
    animation: loginGrid 18s linear infinite;
}

.stApp::after {
    content: "";
    position: fixed !important;
    width: 520px;
    height: 520px;
    right: 8vw;
    bottom: -140px;
    border-radius: 999px;
    background: radial-gradient(circle, rgba(197,138,44,0.13), transparent 64%);
    filter: blur(10px);
    pointer-events: none !important;
    z-index: 0 !important;
    animation: loginGlow 7s ease-in-out infinite alternate;
}

.block-container {
    max-width: none !important;
    padding: 0 !important;
}

.og-login-shell {
    position: fixed;
    top: 50%;
    left: 50%;
    z-index: 9998;
    width: min(920px, calc(100vw - 42px));
    min-height: 430px;
    transform: translate(-50%, -50%);
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 0;
    overflow: hidden;
    border-radius: 24px;
    border: 1px solid rgba(197,138,44,0.28);
    background:
        linear-gradient(135deg, rgba(197,138,44,0.16), transparent 33%),
        linear-gradient(180deg, rgba(15,15,15,0.90), rgba(4,4,4,0.92));
    box-shadow:
        0 34px 90px rgba(0,0,0,0.62),
        0 0 70px rgba(197,138,44,0.10);
    backdrop-filter: blur(26px);
    animation: loginPanelIn 680ms ease-out both;
}

.og-login-shell::before {
    content: "";
    position: absolute;
    inset: -1px;
    background: linear-gradient(115deg, transparent 0%, rgba(197,138,44,0.24) 36%, transparent 58%);
    opacity: 0.48;
    transform: translateX(-60%);
    animation: loginSweep 5.4s ease-in-out infinite;
    pointer-events: none;
}

.og-login-brand,
.og-login-panel {
    position: relative;
    z-index: 2;
    padding: 38px;
}

.og-login-brand {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-right: 1px solid rgba(255,255,255,0.06);
}

.og-login-eyebrow,
.og-login-pin-label,
.og-login-stat span {
    color: #8b867c !important;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 2.6px;
    text-transform: uppercase;
}

.og-login-title {
    margin-top: 18px;
    color: #f1eee8 !important;
    font-size: clamp(42px, 5vw, 68px);
    line-height: 0.95;
    font-weight: 900;
    letter-spacing: 7px;
}

.og-login-copy {
    max-width: 390px;
    margin-top: 20px;
    color: #a6a198 !important;
    font-size: 14px;
    line-height: 1.75;
}

.og-login-status {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    margin-top: 30px;
}

.og-login-stat {
    min-height: 76px;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    background: rgba(255,255,255,0.026);
    padding: 14px;
    box-sizing: border-box;
}

.og-login-stat strong {
    display: block;
    margin-top: 10px;
    color: #f1eee8 !important;
    font-size: 13px;
    font-weight: 900;
}

.og-login-panel {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.og-login-orb {
    width: 178px;
    height: 178px;
    margin: 0 auto 26px auto;
    border-radius: 999px;
    border: 1px solid rgba(197,138,44,0.22);
    background:
        radial-gradient(circle at 50% 50%, rgba(197,138,44,0.28), transparent 26%),
        conic-gradient(from 0deg, transparent, rgba(197,138,44,0.58), transparent, rgba(255,255,255,0.18), transparent);
    box-shadow: inset 0 0 42px rgba(0,0,0,0.55), 0 0 46px rgba(197,138,44,0.15);
    animation: loginOrbit 8s linear infinite;
}

.og-login-orb::after {
    content: "";
    display: block;
    width: 86px;
    height: 86px;
    margin: 45px auto;
    border-radius: 999px;
    background: rgba(3,3,3,0.78);
    border: 1px solid rgba(255,255,255,0.08);
}

.og-login-pin-copy {
    margin-top: 12px;
    color: #a6a198 !important;
    font-size: 13px;
    line-height: 1.6;
}

.og-login-input-slot {
    height: 62px;
    margin-top: 22px;
    border-radius: 15px;
    border: 1px solid rgba(197,138,44,0.18);
    background: rgba(0,0,0,0.22);
}

div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
    position: fixed !important;
    top: calc(50% + 106px) !important;
    left: calc(50% + 236px) !important;
    transform: translateX(-50%) !important;
    z-index: 10000 !important;
    width: min(342px, calc(100vw - 72px)) !important;
    padding: 0 !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}

div[data-testid="stTextInput"] {
    margin: 0 !important;
}

div[data-testid="stTextInput"] label {
    display: none !important;
}

input[type="password"] {
    height: 54px !important;
    background: rgba(9, 9, 9, 0.86) !important;
    border: 1px solid rgba(197, 138, 44, 0.55) !important;
    text-align: center !important;
    color: #f1eee8 !important;
    font-size: 24px !important;
    letter-spacing: 12px !important;
    padding: 12px 18px !important;
    border-radius: 14px !important;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.035), 0 14px 28px rgba(0,0,0,0.35) !important;
}

input[type="password"]:focus {
    border-color: rgba(197, 138, 44, 0.92) !important;
    box-shadow: 0 0 0 3px rgba(197,138,44,0.10), 0 16px 34px rgba(0,0,0,0.44) !important;
}

div[data-testid="stAlert"] {
    position: fixed !important;
    top: calc(50% + 176px) !important;
    left: calc(50% + 236px) !important;
    transform: translateX(-50%) !important;
    z-index: 10001 !important;
    width: min(342px, calc(100vw - 72px)) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

@keyframes loginPanelIn {
    from { opacity: 0; transform: translate(-50%, -46%) scale(0.98); }
    to { opacity: 1; transform: translate(-50%, -50%) scale(1); }
}

@keyframes loginSweep {
    0%, 45% { transform: translateX(-70%); }
    70%, 100% { transform: translateX(72%); }
}

@keyframes loginOrbit {
    to { transform: rotate(360deg); }
}

@keyframes loginGrid {
    from { background-position: 0 0, 0 0; }
    to { background-position: 54px 54px, 54px 54px; }
}

@keyframes loginGlow {
    from { opacity: 0.35; transform: translate3d(0, 0, 0) scale(0.95); }
    to { opacity: 0.78; transform: translate3d(-24px, -18px, 0) scale(1.05); }
}

@media (max-width: 760px) {
    .og-login-shell {
        width: calc(100vw - 28px);
        min-height: 620px;
        grid-template-columns: 1fr;
        border-radius: 20px;
    }

    .og-login-brand {
        border-right: 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        padding: 28px 24px 20px 24px;
    }

    .og-login-panel {
        padding: 24px;
        justify-content: flex-start;
    }

    .og-login-title {
        font-size: 40px;
        letter-spacing: 5px;
    }

    .og-login-copy {
        font-size: 12px;
        line-height: 1.6;
    }

    .og-login-status {
        grid-template-columns: 1fr;
        gap: 8px;
        margin-top: 18px;
    }

    .og-login-stat {
        min-height: auto;
        padding: 12px;
    }

    .og-login-orb {
        width: 118px;
        height: 118px;
        margin-bottom: 18px;
    }

    .og-login-orb::after {
        width: 58px;
        height: 58px;
        margin: 29px auto;
    }

    div[data-testid="stVerticalBlock"] > div:has(input[type="password"]) {
        top: calc(50% + 214px) !important;
        left: 50% !important;
        width: min(330px, calc(100vw - 66px)) !important;
    }

    div[data-testid="stAlert"] {
        top: calc(50% + 282px) !important;
        left: 50% !important;
        width: min(330px, calc(100vw - 66px)) !important;
    }

    input[type="password"] {
        font-size: 22px !important;
        letter-spacing: 9px !important;
    }
}

.stButton { visibility: hidden; height: 0; margin: 0; padding: 0; }
</style>
"""

# --- 9. STATİK HTML ŞABLONLARI ---
w3_matches = """<div class='terminal-row'><span>türkiye - xxx </span><span class='highlight'>türkiye kazanır</span></div><div class='terminal-row'><span>türkiye - aaa</span><span class='highlight'>türkiye kazanır</span></div><div class='terminal-row'><span>rizespor - gala</span><span class='highlight'></span></div><div class='terminal-row'><span></span><span class='highlight'></span></div><div class='terminal-row'><span></span><span class='highlight'></span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 8.79</span><span>Bahis: 100 USD</span></div>"""
w2_matches = """<div class='terminal-row'><span>gala - kayserispor</span><span class='highlight'>gala kazanır & iy +1 & 2+ ✅</span></div><div class='terminal-row'><span>liverpool - newcastle</span><span class='highlight'>+2 & liverpool 1x ✅</span></div><div class='terminal-row'><span>bvb - heidenheim</span><span class='highlight'>bvb kazanır & iy +1 & 2+ ✅</span></div><div class='terminal-row'><span>kocaelispor - fenerbahçe</span><span class='highlight'>fenerbahçe kazanır & 2+ ✅</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 5.53</span><span>Bahis: 100 USD</span></div>"""
w1_matches = """<div class='terminal-row'><span>karagümrük - gala</span><span class='highlight'>gala kazanır & +2 ✅</span></div><div class='terminal-row'><span>bournemouth - liverpool</span><span class='highlight'>kg ✅</span></div><div class='terminal-row'><span>union berlin - bvb</span><span class='highlight'>iy +1 ✅</span></div><div class='terminal-row'><span>newcastle - aston villa</span><span class='highlight'>newcastle +2 ❌</span></div><div class='terminal-row'><span>fenerbahçe - göztepe</span><span class='highlight'>fenerbahçe kazanır ❌</span></div><hr style='border: 0; height: 1px; background: rgba(255,255,255,0.05); margin: 15px 0;'><div class='terminal-row'><span>Oran: 7.09</span><span>Bahis: 100 USD</span></div>"""

w3_coupon_html = f"<div class='industrial-card' style='border-top-color: #c58a2c !important;'><div class='terminal-header'>✅ W3 KUPONU (BAŞARILI)</div>{w3_matches}<span class='highlight' style='font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w2_coupon_html = f"<div class='industrial-card' style='border-top-color: #c58a2c !important;'><div class='terminal-header'>✅ W2 KUPONU (BAŞARILI)</div>{w2_matches}<span class='highlight' style='font-weight:bold;'>SONUÇLANDI ✅</span></div>"
w1_coupon_html = f"<div class='industrial-card' style='border-top-color: #c58a2c !important;'><div class='terminal-header'>❌ W1 KUPONU (BAŞARISIZ)</div>{w1_matches}<span class='highlight' style='font-weight:bold;'>SONUÇLANDI ❌</span></div>"

# --- 10. GÜVENLİK ---
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

def check_password():
    if not st.session_state["password_correct"]:
        st.markdown(common_css, unsafe_allow_html=True)
        st.markdown(login_bg_css, unsafe_allow_html=True)
        st.markdown(
            textwrap.dedent("""
                <div class="og-login-shell">
                    <div class="og-login-brand">
                        <div>
                            <div class="og-login-eyebrow">Özel giriş alanı</div>
                            <div class="og-login-title">OG CORE</div>
                            <div class="og-login-copy">
                                Kasa, risk ve portföy ekranlarına güvenli erişim.
                                Canlı veri akışı yalnızca doğru kodla açılır.
                            </div>
                        </div>

                        <div class="og-login-status">
                            <div class="og-login-stat">
                                <span>Durum</span>
                                <strong>Hazır</strong>
                            </div>
                            <div class="og-login-stat">
                                <span>Veri</span>
                                <strong>Canlı</strong>
                            </div>
                            <div class="og-login-stat">
                                <span>Koruma</span>
                                <strong>Aktif</strong>
                            </div>
                        </div>
                    </div>

                    <div class="og-login-panel">
                        <div class="og-login-orb"></div>
                        <div class="og-login-pin-label">Güvenlik PIN</div>
                        <div class="og-login-pin-copy">4 haneli kodu gir, çekirdek panel açılsın.</div>
                        <div class="og-login-input-slot"></div>
                    </div>
                </div>
            """),
            unsafe_allow_html=True
        )
        pwd = st.text_input("PIN", type="password", placeholder="----", label_visibility="collapsed")
        if pwd:
            if pwd == "0644":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("ERİŞİM REDDEDİLDİ")
        return False
    return True

# --- 11. PORTFÖY MOTORU ---
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
        <span style='color:var(--og-text);'>{row["label"]}</span>
        <span style='color:var(--og-muted);'>{pct:.1f}% &nbsp;//&nbsp; {value_text}</span>
    </div>
    <div style='width:100%; height:9px; border-radius:999px; background:rgba(255,255,255,0.05); overflow:hidden; border:1px solid rgba(255,255,255,0.03);'>
        <div style='height:100%; width:{pct:.2f}%; border-radius:999px; background:linear-gradient(90deg, #8f6426, var(--og-accent)); box-shadow:0 0 12px rgba(197,138,44,0.22);'></div>
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

# --- 12. ANA UYGULAMA ---
if not check_password():
    st.stop()

st.markdown(common_css, unsafe_allow_html=True)
st.markdown("<style>.stApp { background: #030303 !important; background-image: none !important; }</style>", unsafe_allow_html=True)
render_market_ticker(live_vars, duyuru_metni)

with st.sidebar:
    st.markdown(
        "<h1 style='color:var(--og-text); font-family:JetBrains Mono, monospace; font-size:24px; letter-spacing:5px; text-align:center; margin-bottom:40px;'>OG CORE</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div style='margin-bottom:10px; color:var(--og-muted); font-size:11px; letter-spacing:2px; font-weight:800;'>SİSTEM MODÜLLERİ</div>",
        unsafe_allow_html=True
    )
    page = st.radio("Menü", ["⚡ ULTRA ATAK", "⚽ FORM TAKİBİ", "📊 Portföy Takip"], label_visibility="collapsed")
    st.divider()
    st.markdown(
        "<div style='color:var(--og-muted); font-size:11px; letter-spacing:2px; font-weight:800; margin-bottom:15px;'>📂 TERMİNAL ERİŞİMİ</div>",
        unsafe_allow_html=True
    )
    admin_pwd = st.text_input("PIN", type="password", placeholder="Yönetici PIN", label_visibility="collapsed")
    if admin_pwd == "0644":
        st.markdown(
            "<a href='https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/edit' target='_blank' style='text-decoration:none;'><div style='background:rgba(197, 138, 44, 0.14); border: 1px solid rgba(197, 138, 44, 0.42); color:#c58a2c; text-align:center; padding:10px; border-radius:6px; font-family:JetBrains Mono, monospace; font-size:12px; font-weight:bold;'>VERİ TABANINA BAĞLAN</div></a>",
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
                    <div style='font-size:12px; color:var(--og-muted);'>Başlangıç Kasa</div>
                    <div style='font-size:22px; font-weight:800;'>${baslangic_kasa:,.2f}</div>
                </div>
                <div>
                    <div style='font-size:12px; color:var(--og-muted);'>Aktif Hedef</div>
                    <div style='font-size:22px; font-weight:900; color:#c58a2c;'>${aktif_hedef:,.2f}</div>
                </div>
                <div>
                    <div style='font-size:12px; color:var(--og-muted);'>Net Kâr</div>
                    <div style='font-size:22px; font-weight:900; color:#c58a2c;'>${net_kar:,.2f}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(int(current_pct))

    st.markdown(
        f"""
        <div style='margin-top:8px; font-size:13px; color:var(--og-muted); text-align:right;'>
            %{current_pct:.1f}
        </div>
        """,
        unsafe_allow_html=True
    )

    risk_state = render_risk_module(ultra_kasa)
    render_smart_alerts(build_ultra_alerts(ultra_kasa, baslangic_kasa, current_pct, net_kar, risk_state))
    render_ultra_decision_panels(live_vars, ultra_kasa, baslangic_kasa, aktif_hedef, current_pct, net_kar, risk_state)
    render_kasa_history_chart(live_vars, ultra_kasa)

    hedefe_kalan = max(0, aktif_hedef - ultra_kasa)
    st.markdown(
        f"""
        <div class='ops-summary-card'>
            <div class='terminal-header'>Operasyon Özeti</div>
            <div class='ops-summary-grid'>
                <div class='ops-summary-item'>
                    <span>Win Rate</span>
                    <strong>%{wr_oran}</strong>
                </div>
                <div class='ops-summary-item'>
                    <span>Risk Limiti</span>
                    <strong>{fmt_money_usd(risk_state["risk_limit"])}</strong>
                </div>
                <div class='ops-summary-item'>
                    <span>Hedefe Kalan</span>
                    <strong>{fmt_money_usd(hedefe_kalan)}</strong>
                </div>
                <div class='ops-summary-item'>
                    <span>Net K/Z</span>
                    <strong style='color:#c58a2c;'>{fmt_money_usd(net_kar)}</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📜 SON İŞLEMLER")
    st.markdown(
        f"""
        <div class='industrial-card'>
            <div class='terminal-header'>AKTİVİTE LOGLARI</div>
            <p style='font-family:JetBrains Mono; color:var(--og-muted);'>{son_islemler_raw}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

elif page == "⚽ FORM TAKİBİ":
    render_animated_counter(
        "Form Takibi Net",
        toplam_bahis_kar,
        prefix="$",
        decimals=2,
        subtitle="Toplam bahis performansı",
        accent="#c58a2c",
        height=150
    )

    if toplam_bahis_kar > 0:
        render_smart_alerts([("good", "Form takibi pozitif", f"Net sonuç {fmt_money_usd(toplam_bahis_kar)}. Seri kârlı bölgede.")])
    elif toplam_bahis_kar < 0:
        render_smart_alerts([("warn", "Form takibi negatif", f"Net sonuç {fmt_money_usd(toplam_bahis_kar)}. Risk seviyesini düşük tutmak daha mantıklı.")])

    t1, t2, t3 = st.tabs(["✅ W3", "✅ W2", "❌ W1"])

    with t1:
        st.markdown(w3_coupon_html, unsafe_allow_html=True)

    with t2:
        st.markdown(w2_coupon_html, unsafe_allow_html=True)

    with t3:
        st.markdown(w1_coupon_html, unsafe_allow_html=True)

elif page == "📊 Portföy Takip":
    render_portfolio_v2(live_vars)
