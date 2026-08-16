from __future__ import annotations

import html
import math
import re
from datetime import date, datetime

import pandas as pd
import streamlit as st


SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/15izevdpRjs8Om5BAHKVWmdL3FxEHml35DGECfhQUG_s/export?format=csv&gid=0"
APP_TITLE = "OG Core"
DEFAULT_PIN = "0644"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def get_secret(name: str, fallback: str) -> str:
    try:
        return str(st.secrets[name])
    except Exception:
        return fallback


ACCESS_PIN = get_secret("OG_CORE_PIN", DEFAULT_PIN)


@st.cache_data(ttl=45, show_spinner=False)
def get_live_data() -> dict[str, str]:
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        if "key" not in df.columns or "value" not in df.columns:
            raise ValueError("Sheet must contain key and value columns.")
        df = df[["key", "value"]].dropna(subset=["key"])
        df["key"] = df["key"].astype(str).str.strip()
        df["value"] = df["value"].fillna("").astype(str).str.strip()
        return dict(zip(df["key"], df["value"]))
    except Exception:
        return {
            "duyuru": "Canlı veri bekleniyor.",
            "kasa": "600",
            "ana_para": "600",
            "win_rate": "0",
            "w1_sonuc": "0",
            "w2_sonuc": "0",
            "w3_sonuc": "0",
            "son_islemler": "Sheet bağlantısı kurulunca kayıtlar burada görünecek.",
        }


def get_num(data: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        value = data.get(key, default)
        if value is None or str(value).strip() == "":
            return float(default)
        cleaned = str(value).replace("₺", "").replace("$", "").replace("%", "").replace(",", ".").strip()
        return float(cleaned)
    except Exception:
        return float(default)


def get_first_num(data: dict[str, str], keys: list[str], default: float = 0.0) -> float:
    for key in keys:
        if key in data and str(data.get(key, "")).strip() != "":
            return get_num(data, key, default)
    return float(default)


def get_str(data: dict[str, str], key: str, default: str = "") -> str:
    try:
        value = data.get(key, default)
        if value is None:
            return default
        return str(value).strip()
    except Exception:
        return default


def get_first_str(data: dict[str, str], keys: list[str], default: str = "") -> str:
    for key in keys:
        value = get_str(data, key, "")
        if value:
            return value
    return default


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def fmt_money_usd(value: float) -> str:
    return f"${value:,.2f}"


def fmt_money_try(value: float) -> str:
    return f"₺{value:,.0f}"


def fmt_pct(value: float) -> str:
    return f"{value:.1f}%"


def fmt_qty(quantity: float, unit: str) -> str:
    unit_clean = (unit or "").strip().lower()
    if unit_clean in {"usd", "dolar"}:
        return f"${quantity:,.0f}"
    if unit_clean in {"try", "tl"}:
        return fmt_money_try(quantity)
    if unit_clean == "gr":
        return f"{quantity:,.2f} gr"
    return f"{quantity:,.4f}".rstrip("0").rstrip(".")


def safe_text(value: object) -> str:
    return html.escape(str(value))


def parse_date(value: object, fallback: date | None = None) -> date:
    fallback = fallback or datetime.now().date()
    if value is None or str(value).strip() == "":
        return fallback

    raw = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y", "%Y_%m_%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(raw, fmt).date()
        except Exception:
            pass

    try:
        parsed = pd.to_datetime(raw, dayfirst=True, errors="coerce")
        if pd.isna(parsed):
            return fallback
        return parsed.date()
    except Exception:
        return fallback


def normalize_result(value: object, profit: float | None = None) -> str:
    raw = str(value or "").strip().lower().replace("ı", "i")
    if raw in {"won", "win", "w", "kazandi", "kazanç", "kar", "green", "geldi"}:
        return "won"
    if raw in {"lost", "loss", "l", "kaybetti", "kayip", "zarar", "red", "gelmedi"}:
        return "lost"
    if raw in {"void", "push", "refund", "iade", "iptal", "cancelled", "cancel"}:
        return "void"
    if raw in {"open", "pending", "bekliyor", "bekleyen", "aktif", "live"}:
        return "open"
    if profit is not None:
        if profit > 0:
            return "won"
        if profit < 0:
            return "lost"
    return "open"


def result_label(status: str) -> str:
    return {
        "won": "Kazandı",
        "lost": "Kaybetti",
        "void": "İade",
        "open": "Bekliyor",
    }.get(status, "Bekliyor")


def result_class(status: str) -> str:
    return {
        "won": "good",
        "lost": "bad",
        "void": "neutral",
        "open": "open",
    }.get(status, "open")


GLOBAL_CSS = """
<style>
:root {
    --bg: #f5f5f7;
    --panel: rgba(255, 255, 255, 0.86);
    --text: #1d1d1f;
    --muted: #6e6e73;
    --muted-2: #86868b;
    --line: rgba(0, 0, 0, 0.10);
    --line-soft: rgba(0, 0, 0, 0.06);
    --blue: #0071e3;
    --blue-soft: rgba(0, 113, 227, 0.10);
    --green: #1d8f4f;
    --green-soft: rgba(29, 143, 79, 0.10);
    --red: #d92d20;
    --red-soft: rgba(217, 45, 32, 0.10);
    --amber: #b56a00;
    --amber-soft: rgba(181, 106, 0, 0.10);
    --radius: 8px;
    --shadow: 0 18px 48px rgba(0, 0, 0, 0.08);
}

#MainMenu, footer, header, [data-testid="stSidebar"], .stDeployButton {
    visibility: hidden;
}

.stApp {
    background: linear-gradient(180deg, #fbfbfd 0%, #f5f5f7 48%, #eef1f5 100%) !important;
    color: var(--text);
}

.block-container {
    max-width: 1180px;
    padding: 26px 28px 56px 28px !important;
}

body, p, div, span, button, input, textarea, label {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "Segoe UI", sans-serif !important;
    letter-spacing: 0 !important;
}

h1, h2, h3 {
    color: var(--text) !important;
    letter-spacing: 0 !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 16px;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 18px;
    margin-bottom: 26px;
}

.brand-lockup {
    display: flex;
    align-items: center;
    gap: 13px;
}

.brand-mark {
    width: 38px;
    height: 38px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    background: #1d1d1f;
    color: #fff;
    font-size: 13px;
    font-weight: 750;
}

.brand-name {
    color: var(--text) !important;
    font-size: 18px;
    font-weight: 760;
    line-height: 1.1;
}

.brand-sub {
    color: var(--muted) !important;
    font-size: 13px;
    margin-top: 3px;
}

.data-pill {
    border: 1px solid var(--line);
    background: rgba(255, 255, 255, 0.72);
    color: var(--muted) !important;
    border-radius: 999px;
    padding: 9px 13px;
    font-size: 12px;
    white-space: nowrap;
}

.hero {
    border: 1px solid var(--line-soft);
    background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(255,255,255,0.76));
    box-shadow: var(--shadow);
    border-radius: var(--radius);
    padding: 30px;
    margin-bottom: 18px;
}

.hero-kicker {
    color: var(--blue) !important;
    font-size: 13px;
    font-weight: 680;
    margin-bottom: 12px;
}

.hero-title {
    color: var(--text) !important;
    font-size: 46px;
    line-height: 1.04;
    font-weight: 780;
    max-width: 760px;
}

.hero-copy {
    color: var(--muted) !important;
    font-size: 17px;
    line-height: 1.55;
    max-width: 760px;
    margin-top: 14px;
}

div[role="radiogroup"] {
    background: rgba(0, 0, 0, 0.055);
    border: 1px solid rgba(0,0,0,0.055);
    border-radius: 999px;
    padding: 4px;
    gap: 4px;
    width: fit-content;
}

div[role="radiogroup"] label {
    border-radius: 999px;
    padding: 8px 14px;
    min-height: 34px;
}

div[role="radiogroup"] label:has(input:checked) {
    background: #ffffff;
    box-shadow: 0 4px 18px rgba(0,0,0,0.10);
}

div[role="radiogroup"] p {
    color: var(--text) !important;
    font-size: 13px !important;
    font-weight: 620 !important;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin: 18px 0;
}

.metric-card {
    min-height: 132px;
    border-radius: var(--radius);
    border: 1px solid var(--line-soft);
    background: var(--panel);
    box-shadow: 0 12px 34px rgba(0, 0, 0, 0.06);
    padding: 18px;
    box-sizing: border-box;
}

.metric-label {
    color: var(--muted) !important;
    font-size: 12px;
    font-weight: 630;
    margin-bottom: 12px;
}

.metric-value {
    color: var(--text) !important;
    font-size: 29px;
    line-height: 1.05;
    font-weight: 780;
    white-space: nowrap;
}

.metric-caption {
    color: var(--muted-2) !important;
    font-size: 12px;
    line-height: 1.35;
    margin-top: 12px;
}

.metric-card.good .metric-value { color: var(--green) !important; }
.metric-card.bad .metric-value { color: var(--red) !important; }
.metric-card.blue .metric-value { color: var(--blue) !important; }
.metric-card.amber .metric-value { color: var(--amber) !important; }

.section-title {
    color: var(--text) !important;
    font-size: 22px;
    font-weight: 750;
    margin: 28px 0 12px 0;
}

.panel {
    border: 1px solid var(--line-soft);
    background: var(--panel);
    border-radius: var(--radius);
    padding: 20px;
    box-shadow: 0 12px 34px rgba(0, 0, 0, 0.055);
    margin-bottom: 16px;
}

.panel-title {
    color: var(--text) !important;
    font-size: 17px;
    font-weight: 720;
    margin-bottom: 14px;
}

.progress-shell {
    height: 9px;
    border-radius: 999px;
    background: rgba(0,0,0,0.08);
    overflow: hidden;
    margin: 14px 0 10px 0;
}

.progress-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #0071e3, #5ac8fa);
}

.split-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    color: var(--muted) !important;
    font-size: 13px;
    margin-top: 8px;
}

.status-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
}

.status-card {
    border: 1px solid var(--line-soft);
    border-radius: var(--radius);
    background: rgba(255,255,255,0.72);
    padding: 16px;
}

.status-title {
    color: var(--text) !important;
    font-size: 14px;
    font-weight: 720;
    margin-bottom: 8px;
}

.status-body {
    color: var(--muted) !important;
    font-size: 13px;
    line-height: 1.5;
}

.table-card {
    border: 1px solid var(--line-soft);
    background: var(--panel);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: 0 12px 34px rgba(0,0,0,0.055);
}

.table-row {
    display: grid;
    grid-template-columns: 1.1fr 1.6fr 1fr 0.8fr 0.9fr 0.9fr;
    gap: 12px;
    align-items: center;
    padding: 15px 18px;
    border-top: 1px solid var(--line-soft);
}

.table-row.header {
    border-top: 0;
    background: rgba(0,0,0,0.025);
    color: var(--muted) !important;
    font-size: 12px;
    font-weight: 680;
}

.table-cell-main {
    color: var(--text) !important;
    font-size: 14px;
    font-weight: 650;
}

.table-cell-sub {
    color: var(--muted) !important;
    font-size: 12px;
    margin-top: 4px;
}

.badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    padding: 6px 10px;
    font-size: 12px;
    font-weight: 680;
    width: fit-content;
}

.badge.good { color: var(--green) !important; background: var(--green-soft); }
.badge.bad { color: var(--red) !important; background: var(--red-soft); }
.badge.open { color: var(--blue) !important; background: var(--blue-soft); }
.badge.neutral { color: var(--muted) !important; background: rgba(0,0,0,0.06); }

.allocation-row {
    margin-bottom: 15px;
}

.allocation-head {
    display: flex;
    justify-content: space-between;
    gap: 14px;
    color: var(--text) !important;
    font-size: 14px;
    font-weight: 650;
    margin-bottom: 8px;
}

.allocation-sub {
    color: var(--muted) !important;
    font-size: 12px;
    font-weight: 500;
}

.asset-table-row {
    display: grid;
    grid-template-columns: 1.4fr 0.9fr 0.9fr 0.9fr 0.9fr;
    gap: 12px;
    align-items: center;
    padding: 15px 18px;
    border-top: 1px solid var(--line-soft);
}

.empty-state {
    border: 1px dashed rgba(0,0,0,0.16);
    background: rgba(255,255,255,0.62);
    border-radius: var(--radius);
    padding: 24px;
    color: var(--muted) !important;
    font-size: 14px;
}

.login-page .block-container {
    max-width: 1040px;
    padding-top: 8vh !important;
}

.login-shell {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 28px;
    align-items: stretch;
}

.login-hero {
    border-radius: var(--radius);
    padding: 42px;
    background: linear-gradient(180deg, rgba(255,255,255,0.94), rgba(255,255,255,0.70));
    border: 1px solid var(--line-soft);
    box-shadow: var(--shadow);
    min-height: 420px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.login-panel {
    border-radius: var(--radius);
    background: #1d1d1f;
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: var(--shadow);
    padding: 38px;
    color: #fff !important;
}

.login-eyebrow {
    color: var(--blue) !important;
    font-size: 13px;
    font-weight: 680;
    margin-bottom: 14px;
}

.login-title {
    color: var(--text) !important;
    font-size: 58px;
    line-height: 1;
    font-weight: 790;
}

.login-copy {
    color: var(--muted) !important;
    font-size: 17px;
    line-height: 1.58;
    max-width: 520px;
    margin-top: 18px;
}

.login-mini-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 36px;
}

.login-mini {
    border-radius: var(--radius);
    border: 1px solid var(--line-soft);
    background: rgba(255,255,255,0.72);
    padding: 14px;
}

.login-mini span {
    color: var(--muted) !important;
    font-size: 12px;
}

.login-mini strong {
    display: block;
    color: var(--text) !important;
    font-size: 15px;
    margin-top: 8px;
}

.login-panel-title {
    color: #fff !important;
    font-size: 26px;
    font-weight: 760;
    margin-bottom: 10px;
}

.login-panel-copy {
    color: rgba(255,255,255,0.66) !important;
    font-size: 14px;
    line-height: 1.55;
    margin-bottom: 28px;
}

input[type="password"] {
    border-radius: var(--radius) !important;
    border: 1px solid rgba(255,255,255,0.16) !important;
    background: rgba(255,255,255,0.08) !important;
    color: #ffffff !important;
    min-height: 48px !important;
    font-size: 18px !important;
    text-align: center !important;
    letter-spacing: 8px !important;
}

.stButton button {
    border-radius: 999px !important;
    background: var(--blue) !important;
    color: #fff !important;
    border: 0 !important;
    min-height: 42px !important;
    font-weight: 680 !important;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 16px !important;
        padding-right: 16px !important;
    }
    .topbar, .login-shell {
        grid-template-columns: 1fr;
        flex-direction: column;
        align-items: flex-start;
    }
    .hero {
        padding: 22px;
    }
    .hero-title, .login-title {
        font-size: 38px;
    }
    .metric-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
    .status-grid {
        grid-template-columns: 1fr;
    }
    .table-row,
    .asset-table-row {
        grid-template-columns: 1fr;
        gap: 7px;
    }
    .table-row.header,
    .asset-table-row.header {
        display: none;
    }
    .login-mini-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 520px) {
    .metric-grid {
        grid-template-columns: 1fr;
    }
    .metric-value {
        font-size: 25px;
    }
}
</style>
"""


def inject_css() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_topbar(data: dict[str, str]) -> None:
    announcement = get_str(data, "duyuru", "Canlı veri aktif")
    stamp = datetime.now().strftime("%d.%m.%Y %H:%M")
    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand-lockup">
                <div class="brand-mark">OG</div>
                <div>
                    <div class="brand-name">OG Core</div>
                    <div class="brand-sub">{safe_text(announcement)}</div>
                </div>
            </div>
            <div class="data-pill">Son kontrol: {safe_text(stamp)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label: str, value: str, caption: str = "", tone: str = "") -> str:
    return (
        f'<div class="metric-card {safe_text(tone)}">'
        f'<div class="metric-label">{safe_text(label)}</div>'
        f'<div class="metric-value">{safe_text(value)}</div>'
        f'<div class="metric-caption">{safe_text(caption)}</div>'
        "</div>"
    )


def render_metric_grid(cards: list[tuple[str, str, str, str]]) -> None:
    html_cards = "".join(render_metric_card(*card) for card in cards)
    st.markdown(f'<div class="metric-grid">{html_cards}</div>', unsafe_allow_html=True)


def render_login() -> bool:
    st.markdown('<div class="login-page">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="login-shell">
            <div class="login-hero">
                <div>
                    <div class="login-eyebrow">Private dashboard</div>
                    <div class="login-title">OG Core</div>
                    <div class="login-copy">
                        Bahis performansı ve portföy varlıkları için sade, hızlı ve güvenli takip alanı.
                    </div>
                </div>
                <div class="login-mini-grid">
                    <div class="login-mini"><span>Mod</span><strong>Takip</strong></div>
                    <div class="login-mini"><span>Veri</span><strong>Sheet</strong></div>
                    <div class="login-mini"><span>Erişim</span><strong>PIN</strong></div>
                </div>
            </div>
            <div class="login-panel">
                <div class="login-panel-title">Giriş</div>
                <div class="login-panel-copy">Devam etmek için özel PIN kodunu gir.</div>
        """,
        unsafe_allow_html=True,
    )
    pin = st.text_input("PIN", type="password", placeholder="----", label_visibility="collapsed")
    if pin:
        if pin == ACCESS_PIN:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("PIN hatalı.")
    st.markdown("</div></div></div>", unsafe_allow_html=True)
    return False


def discover_bet_row_ids(data: dict[str, str]) -> list[tuple[str, int]]:
    row_ids: set[tuple[str, int]] = set()
    for key in data:
        match = re.match(r"^(bet|bahis|kupon)_(\d+)_", str(key).strip(), re.IGNORECASE)
        if match:
            row_ids.add((match.group(1).lower(), int(match.group(2))))
    return sorted(row_ids, key=lambda item: (item[1], item[0]))


def row_field(data: dict[str, str], prefix: str, index: int, aliases: list[str], default: str = "") -> str:
    for alias in aliases:
        value = get_str(data, f"{prefix}_{index}_{alias}", "")
        if value:
            return value
    return default


def row_num(data: dict[str, str], prefix: str, index: int, aliases: list[str], default: float = 0.0) -> float:
    for alias in aliases:
        key = f"{prefix}_{index}_{alias}"
        if key in data and get_str(data, key, "") != "":
            return get_num(data, key, default)
    return default


def build_dynamic_bets(data: dict[str, str]) -> pd.DataFrame:
    records = []
    for prefix, index in discover_bet_row_ids(data):
        match_name = row_field(data, prefix, index, ["match", "mac", "maç", "event", "karsilasma"], "")
        league = row_field(data, prefix, index, ["league", "lig", "category"], "")
        market = row_field(data, prefix, index, ["market", "pazar", "secim", "seçim", "pick"], "")
        if not any([match_name, league, market]):
            continue

        stake = row_num(data, prefix, index, ["stake", "bahis", "miktar", "tutar"], 0)
        odds = row_num(data, prefix, index, ["odds", "oran"], 0)
        explicit_profit = row_num(data, prefix, index, ["profit", "kar", "kâr", "sonuc", "sonuç"], math.nan)
        result_raw = row_field(data, prefix, index, ["result", "status", "durum", "sonuc", "sonuç"], "")
        status = normalize_result(result_raw, None if math.isnan(explicit_profit) else explicit_profit)

        if math.isnan(explicit_profit):
            if status == "won" and stake > 0 and odds > 0:
                profit = stake * max(0, odds - 1)
            elif status == "lost" and stake > 0:
                profit = -stake
            else:
                profit = 0.0
        else:
            profit = explicit_profit

        records.append(
            {
                "id": f"{prefix.upper()}-{index}",
                "date": parse_date(row_field(data, prefix, index, ["date", "tarih"], "")),
                "league": league or "Genel",
                "match": match_name or "Kayıt",
                "market": market or "Seçim yok",
                "odds": odds,
                "stake": stake,
                "profit": profit,
                "status": status,
                "note": row_field(data, prefix, index, ["note", "not", "aciklama", "açıklama"], ""),
            }
        )

    return pd.DataFrame(records)


def build_legacy_bets(data: dict[str, str]) -> pd.DataFrame:
    rows = [
        {
            "id": "W3",
            "date": datetime.now().date(),
            "league": "Haftalık kupon",
            "match": get_str(data, "w3_maclar", "Başakşehir - Gala / Arsenal - Chelsea / BVB / Fenerbahçe"),
            "market": get_str(data, "w3_market", "Kupon"),
            "odds": get_num(data, "w3_oran", 0),
            "stake": get_num(data, "w3_bahis", 100),
            "profit": get_num(data, "w3_sonuc", 0),
            "status": normalize_result(get_str(data, "w3_durum", ""), get_num(data, "w3_sonuc", 0)),
            "note": get_str(data, "w3_not", ""),
        },
        {
            "id": "W2",
            "date": datetime.now().date(),
            "league": "Haftalık kupon",
            "match": get_str(data, "w2_maclar", "Gala - Göztepe / Chelsea - Brighton / BVB / Fenerbahçe"),
            "market": get_str(data, "w2_market", "Kupon"),
            "odds": get_num(data, "w2_oran", 0),
            "stake": get_num(data, "w2_bahis", 100),
            "profit": get_num(data, "w2_sonuc", 0),
            "status": normalize_result(get_str(data, "w2_durum", ""), get_num(data, "w2_sonuc", 0)),
            "note": get_str(data, "w2_not", ""),
        },
        {
            "id": "W1",
            "date": datetime.now().date(),
            "league": "Haftalık kupon",
            "match": get_str(data, "w1_maclar", "Erzurumspor - Gala / Fulham - Chelsea / Union Berlin - BVB / Fenerbahçe"),
            "market": get_str(data, "w1_market", "Kupon"),
            "odds": get_num(data, "w1_oran", 0),
            "stake": get_num(data, "w1_bahis", 100),
            "profit": get_num(data, "w1_sonuc", 0),
            "status": normalize_result(get_str(data, "w1_durum", ""), get_num(data, "w1_sonuc", 0)),
            "note": get_str(data, "w1_not", ""),
        },
    ]
    return pd.DataFrame(rows)


def build_bet_records(data: dict[str, str]) -> pd.DataFrame:
    dynamic_df = build_dynamic_bets(data)
    df = dynamic_df if not dynamic_df.empty else build_legacy_bets(data)
    df["date"] = pd.to_datetime(df["date"])
    df["odds"] = pd.to_numeric(df["odds"], errors="coerce").fillna(0.0)
    df["stake"] = pd.to_numeric(df["stake"], errors="coerce").fillna(0.0)
    df["profit"] = pd.to_numeric(df["profit"], errors="coerce").fillna(0.0)
    df["status"] = df["status"].fillna("open")
    return df.sort_values("date", ascending=False).reset_index(drop=True)


def calculate_bet_metrics(df: pd.DataFrame, data: dict[str, str]) -> dict[str, float | int | str]:
    settled = df[df["status"].isin(["won", "lost", "void"])].copy()
    decisive = df[df["status"].isin(["won", "lost"])].copy()
    open_df = df[df["status"] == "open"].copy()

    total_profit = float(settled["profit"].sum()) if not settled.empty else 0.0
    total_stake = float(settled["stake"].sum()) if not settled.empty else 0.0
    open_stake = float(open_df["stake"].sum()) if not open_df.empty else 0.0
    roi = (total_profit / total_stake * 100) if total_stake > 0 else 0.0
    win_rate = (len(decisive[decisive["status"] == "won"]) / len(decisive) * 100) if len(decisive) > 0 else get_num(data, "win_rate", 0)
    odds_df = settled.loc[settled["odds"] > 0]
    avg_odds = float(odds_df["odds"].mean()) if not odds_df.empty else 0.0

    starting_bankroll = get_first_num(data, ["bahis_baslangic_kasa", "bet_start_bankroll", "ana_para"], 1000)
    current_bankroll = get_first_num(data, ["bahis_kasa", "bet_bankroll", "kasa"], starting_bankroll + total_profit)
    target = get_first_num(data, ["bahis_hedef", "bet_target", "hedef"], max(current_bankroll, starting_bankroll) * 1.25)
    target_progress = (current_bankroll / target * 100) if target > 0 else 0.0

    ordered = settled.sort_values("date").copy()
    if ordered.empty:
        drawdown = 0.0
    else:
        ordered["equity"] = starting_bankroll + ordered["profit"].cumsum()
        ordered["peak"] = ordered["equity"].cummax()
        ordered["drawdown"] = ordered["peak"] - ordered["equity"]
        drawdown = float(ordered["drawdown"].max())

    streak_label = "Veri yok"
    streak_count = 0
    decisive_sorted = decisive.sort_values("date")
    if not decisive_sorted.empty:
        last_status = str(decisive_sorted.iloc[-1]["status"])
        streak_count = 0
        for status in reversed(decisive_sorted["status"].tolist()):
            if status == last_status:
                streak_count += 1
            else:
                break
        streak_label = f"{streak_count} maç {result_label(last_status).lower()}"

    discipline = 100.0
    if roi < 0:
        discipline -= min(32, abs(roi) * 1.4)
    if drawdown > 0 and current_bankroll > 0:
        discipline -= min(28, (drawdown / current_bankroll) * 100 * 1.8)
    if streak_label.endswith("kaybetti"):
        discipline -= min(18, streak_count * 6)

    return {
        "total_profit": total_profit,
        "total_stake": total_stake,
        "open_stake": open_stake,
        "roi": roi,
        "win_rate": win_rate,
        "avg_odds": avg_odds,
        "starting_bankroll": starting_bankroll,
        "current_bankroll": current_bankroll,
        "target": target,
        "target_progress": clamp(target_progress),
        "drawdown": drawdown,
        "streak_label": streak_label,
        "discipline": int(clamp(discipline, 0, 100)),
        "settled_count": int(len(settled)),
        "open_count": int(len(open_df)),
    }


def render_betting_table(df: pd.DataFrame) -> None:
    if df.empty:
        st.markdown('<div class="empty-state">Bahis kaydı bulunamadı.</div>', unsafe_allow_html=True)
        return

    rows_html = [
        """
        <div class="table-row header">
            <div>Tarih</div>
            <div>Karşılaşma</div>
            <div>Seçim</div>
            <div>Oran</div>
            <div>Stake</div>
            <div>Sonuç</div>
        </div>
        """
    ]
    for _, row in df.head(14).iterrows():
        status = str(row["status"])
        date_text = pd.to_datetime(row["date"]).strftime("%d.%m.%Y")
        profit_text = fmt_money_usd(float(row["profit"]))
        rows_html.append(
            f"""
            <div class="table-row">
                <div>
                    <div class="table-cell-main">{safe_text(date_text)}</div>
                    <div class="table-cell-sub">{safe_text(row["id"])}</div>
                </div>
                <div>
                    <div class="table-cell-main">{safe_text(row["match"])}</div>
                    <div class="table-cell-sub">{safe_text(row["league"])}</div>
                </div>
                <div>
                    <div class="table-cell-main">{safe_text(row["market"])}</div>
                    <div class="table-cell-sub">{safe_text(row["note"])}</div>
                </div>
                <div class="table-cell-main">{float(row["odds"]):.2f}</div>
                <div>
                    <div class="table-cell-main">{fmt_money_usd(float(row["stake"]))}</div>
                    <div class="table-cell-sub">{safe_text(profit_text)}</div>
                </div>
                <div><span class="badge {result_class(status)}">{safe_text(result_label(status))}</span></div>
            </div>
            """
        )

    st.markdown(f'<div class="table-card">{"".join(rows_html)}</div>', unsafe_allow_html=True)


def render_bet_status_panels(metrics: dict[str, float | int | str]) -> None:
    score = int(metrics["discipline"])
    if score >= 80:
        title = "Disiplin güçlü"
        body = "Kayıtlar kontrollü bir çizgide duruyor. Panel yalnızca takip ve ölçüm için çalışır."
    elif score >= 55:
        title = "Dikkat bölgesi"
        body = "Kâr/zarar ve seri etkisi izlenmeli. Stake büyütme kararı bu panelin konusu değildir."
    else:
        title = "Koruma bölgesi"
        body = "Drawdown veya negatif seri belirgin. Takip paneli riski görünür tutmak için sade kalır."

    panels = [
        (title, body),
        ("Açık pozisyon", f'{int(metrics["open_count"])} bekleyen kayıt, toplam açık stake {fmt_money_usd(float(metrics["open_stake"]))}.'),
        ("Seri durumu", str(metrics["streak_label"])),
    ]
    cards = "".join(
        f'<div class="status-card"><div class="status-title">{safe_text(t)}</div><div class="status-body">{safe_text(b)}</div></div>'
        for t, b in panels
    )
    st.markdown(f'<div class="status-grid">{cards}</div>', unsafe_allow_html=True)


def render_betting_page(data: dict[str, str]) -> None:
    df = build_bet_records(data)
    metrics = calculate_bet_metrics(df, data)

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Bahis Takip Sistemi</div>
            <div class="hero-title">Performans, kasa ve kupon akışı tek ekranda.</div>
            <div class="hero-copy">Sonuç odaklı kayıt, açık kupon görünümü, ROI, win rate ve kasa ilerlemesi.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    profit_tone = "good" if float(metrics["total_profit"]) >= 0 else "bad"
    render_metric_grid(
        [
            ("Bahis Kasası", fmt_money_usd(float(metrics["current_bankroll"])), f'Hedef {fmt_money_usd(float(metrics["target"]))}', "blue"),
            ("Net Sonuç", fmt_money_usd(float(metrics["total_profit"])), f'{int(metrics["settled_count"])} kapanan kayıt', profit_tone),
            ("ROI", fmt_pct(float(metrics["roi"])), f'Toplam stake {fmt_money_usd(float(metrics["total_stake"]))}', profit_tone),
            ("Win Rate", fmt_pct(float(metrics["win_rate"])), f'Ortalama oran {float(metrics["avg_odds"]):.2f}', "blue"),
        ]
    )

    progress = float(metrics["target_progress"])
    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">Kasa ilerlemesi</div>
            <div class="progress-shell"><div class="progress-fill" style="width:{progress:.1f}%;"></div></div>
            <div class="split-row">
                <span>{fmt_money_usd(float(metrics["current_bankroll"]))}</span>
                <span>{fmt_pct(progress)} / {fmt_money_usd(float(metrics["target"]))}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_bet_status_panels(metrics)

    chart_col, mix_col = st.columns([1.35, 0.65])
    settled = df[df["status"].isin(["won", "lost", "void"])].sort_values("date").copy()
    with chart_col:
        st.markdown('<div class="section-title">Kâr/Zarar Eğrisi</div>', unsafe_allow_html=True)
        if settled.empty:
            st.markdown('<div class="empty-state">Grafik için kapanan kayıt bekleniyor.</div>', unsafe_allow_html=True)
        else:
            curve = settled[["date", "profit"]].copy()
            curve["Kümülatif Sonuç"] = curve["profit"].cumsum()
            curve = curve.set_index("date")[["Kümülatif Sonuç"]]
            st.line_chart(curve, height=290)

    with mix_col:
        st.markdown('<div class="section-title">Sonuç Dağılımı</div>', unsafe_allow_html=True)
        counts = df["status"].map(result_label).value_counts()
        if counts.empty:
            st.markdown('<div class="empty-state">Dağılım verisi yok.</div>', unsafe_allow_html=True)
        else:
            st.bar_chart(counts, height=290)

    st.markdown('<div class="section-title">Kupon Kayıtları</div>', unsafe_allow_html=True)
    status_filter = st.segmented_control(
        "Filtre",
        options=["Tümü", "Bekliyor", "Kazandı", "Kaybetti", "İade"],
        default="Tümü",
        label_visibility="collapsed",
    )
    filtered = df.copy()
    reverse_labels = {"Bekliyor": "open", "Kazandı": "won", "Kaybetti": "lost", "İade": "void"}
    if status_filter != "Tümü":
        filtered = filtered[filtered["status"] == reverse_labels[status_filter]]
    render_betting_table(filtered)


def discover_dynamic_instruments(data: dict[str, str], users: list[str]) -> list[dict[str, object]]:
    instrument_codes = set()
    for key in data:
        if isinstance(key, str) and key.startswith("price_"):
            code = key.replace("price_", "", 1).strip()
            if code:
                instrument_codes.add(code)

    instruments = []
    for code in instrument_codes:
        show = int(get_num(data, f"show_{code}", 1))
        price = get_num(data, f"price_{code}", 0)
        has_user_key = any(f"{user}_{code}" in data for user in users)
        if show == 0 or not has_user_key:
            continue
        instruments.append(
            {
                "code": code,
                "label": get_str(data, f"label_{code}", code.upper()),
                "unit": get_str(data, f"unit_{code}", "adet"),
                "currency": get_str(data, f"currency_{code}", "TRY").upper(),
                "price": price,
                "order": get_num(data, f"order_{code}", 999),
            }
        )
    return sorted(instruments, key=lambda item: (float(item["order"]), str(item["label"])))


def build_legacy_instruments(data: dict[str, str]) -> list[dict[str, object]]:
    return [
        {"code": "usd_cash", "label": "Nakit", "unit": "USD", "currency": "USD", "price": 1.0, "order": 1, "legacy": {"oguzo": "oguzo_usd"}},
        {"code": "gram_altin", "label": "Gram Altın", "unit": "gr", "currency": "TRY", "price": get_num(data, "gram_altin_fiyat", 0), "order": 2, "legacy": {"oguzo": "oguzo_altin"}},
        {"code": "ceyrek", "label": "Çeyrek Altın", "unit": "adet", "currency": "TRY", "price": get_num(data, "ceyrek_altin_fiyat", 0), "order": 3, "legacy": {"oguzo": "oguzo_ceyrek"}},
        {"code": "aft", "label": "AFT", "unit": "adet", "currency": "TRY", "price": get_num(data, "aft_fiyat_tl", 0), "order": 4, "legacy": {"oguzo": "oguzo_aft_adet"}},
        {"code": "btc", "label": "Bitcoin", "unit": "adet", "currency": "USD", "price": get_num(data, "btc_fiyat_usd", 0), "order": 5, "legacy": {"oguzo": "oguzo_btc"}},
        {"code": "eth", "label": "Ethereum", "unit": "adet", "currency": "USD", "price": get_num(data, "eth_fiyat_usd", 0), "order": 6, "legacy": {"oguzo": "oguzo_eth"}},
        {"code": "gumus", "label": "Gümüş", "unit": "gr", "currency": "TRY", "price": get_num(data, "gumus_fiyat_tl", 0), "order": 7, "legacy": {"oguzo": "oguzo_gumus"}},
    ]


def portfolio_users(data: dict[str, str]) -> list[str]:
    configured = get_first_str(data, ["portfolio_users", "portfoy_users", "users"], "")
    if configured:
        users = [item.strip() for item in configured.split(",") if item.strip()]
        if users:
            return users
    return ["oguzo"]


def user_label(data: dict[str, str], user: str) -> str:
    return get_first_str(data, [f"label_{user}", f"{user}_label"], user.upper())


def quantity_for_instrument(data: dict[str, str], user: str, instrument: dict[str, object]) -> float:
    direct_key = f"{user}_{instrument['code']}"
    if direct_key in data:
        return get_num(data, direct_key, 0)
    legacy = instrument.get("legacy", {})
    if isinstance(legacy, dict) and user in legacy:
        return get_num(data, str(legacy[user]), 0)
    return 0.0


def convert_value(quantity: float, price: float, currency: str, usdtry: float) -> tuple[float, float]:
    if currency.upper() == "USD":
        total_usd = quantity * price
        return total_usd * usdtry, total_usd
    total_try = quantity * price
    total_usd = total_try / usdtry if usdtry > 0 else 0.0
    return total_try, total_usd


def build_portfolio(data: dict[str, str], user: str, instruments: list[dict[str, object]], usdtry: float) -> pd.DataFrame:
    rows = []
    for instrument in instruments:
        quantity = quantity_for_instrument(data, user, instrument)
        price = float(instrument["price"])
        total_try, total_usd = convert_value(quantity, price, str(instrument["currency"]), usdtry)
        rows.append(
            {
                "code": str(instrument["code"]),
                "label": str(instrument["label"]),
                "unit": str(instrument["unit"]),
                "currency": str(instrument["currency"]),
                "price": price,
                "quantity": quantity,
                "total_try": total_try,
                "total_usd": total_usd,
                "order": float(instrument["order"]),
            }
        )
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.sort_values(["order", "label"]).reset_index(drop=True)


def render_allocation(df: pd.DataFrame) -> None:
    total = float(df["total_usd"].sum())
    if total <= 0:
        st.markdown('<div class="empty-state">Dağılım için aktif varlık bekleniyor.</div>', unsafe_allow_html=True)
        return

    rows = []
    for _, row in df.sort_values("total_usd", ascending=False).iterrows():
        pct = float(row["total_usd"]) / total * 100
        rows.append(
            f"""
            <div class="allocation-row">
                <div class="allocation-head">
                    <span>{safe_text(row["label"])}</span>
                    <span class="allocation-sub">{fmt_pct(pct)} · {fmt_money_usd(float(row["total_usd"]))}</span>
                </div>
                <div class="progress-shell"><div class="progress-fill" style="width:{pct:.1f}%;"></div></div>
            </div>
            """
        )
    st.markdown(f'<div class="panel"><div class="panel-title">Portföy dağılımı</div>{"".join(rows)}</div>', unsafe_allow_html=True)


def render_asset_table(df: pd.DataFrame) -> None:
    if df.empty:
        st.markdown('<div class="empty-state">Aktif portföy varlığı bulunamadı.</div>', unsafe_allow_html=True)
        return

    rows = [
        """
        <div class="asset-table-row header table-row">
            <div>Varlık</div>
            <div>Miktar</div>
            <div>Birim Fiyat</div>
            <div>TRY</div>
            <div>USD</div>
        </div>
        """
    ]
    for _, row in df.sort_values("total_usd", ascending=False).iterrows():
        price_text = fmt_money_usd(float(row["price"])) if str(row["currency"]).upper() == "USD" else fmt_money_try(float(row["price"]))
        rows.append(
            f"""
            <div class="asset-table-row">
                <div>
                    <div class="table-cell-main">{safe_text(row["label"])}</div>
                    <div class="table-cell-sub">{safe_text(row["currency"])}</div>
                </div>
                <div class="table-cell-main">{safe_text(fmt_qty(float(row["quantity"]), str(row["unit"])))}</div>
                <div class="table-cell-main">{safe_text(price_text)}</div>
                <div class="table-cell-main">{safe_text(fmt_money_try(float(row["total_try"])))}</div>
                <div class="table-cell-main">{safe_text(fmt_money_usd(float(row["total_usd"])))}</div>
            </div>
            """
        )
    st.markdown(f'<div class="table-card">{"".join(rows)}</div>', unsafe_allow_html=True)


def render_portfolio_page(data: dict[str, str]) -> None:
    users = portfolio_users(data)
    labels = {user_label(data, user): user for user in users}
    selected_label = list(labels.keys())[0]
    if len(labels) > 1:
        selected_label = st.selectbox("Portföy", options=list(labels.keys()), label_visibility="collapsed")
    user = labels[selected_label]

    usdtry = get_num(data, "usdtry", 0)
    instruments = discover_dynamic_instruments(data, users)
    if not instruments:
        instruments = build_legacy_instruments(data)

    df = build_portfolio(data, user, instruments, usdtry)
    active = df[(df["quantity"] > 0) & (df["total_usd"] > 0)].copy() if not df.empty else pd.DataFrame()

    total_usd = float(active["total_usd"].sum()) if not active.empty else 0.0
    total_try = float(active["total_try"].sum()) if not active.empty else 0.0
    main_asset = "Yok"
    main_pct = 0.0
    if total_usd > 0:
        biggest = active.sort_values("total_usd", ascending=False).iloc[0]
        main_asset = str(biggest["label"])
        main_pct = float(biggest["total_usd"]) / total_usd * 100

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">Portföy Takip</div>
            <div class="hero-title">{safe_text(selected_label)} portföy görünümü.</div>
            <div class="hero-copy">Sadece izleme modu: varlık, miktar, dağılım ve toplam değer.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_metric_grid(
        [
            ("Toplam USD", fmt_money_usd(total_usd), f'{len(active)} aktif varlık', "blue"),
            ("Toplam TRY", fmt_money_try(total_try), f'USD/TRY {usdtry:.2f}', ""),
            ("Ana Varlık", main_asset, fmt_pct(main_pct), "blue"),
            ("Takip Modu", "Aktif", "Al/sat önerisi yok", "good"),
        ]
    )

    alloc_col, chart_col = st.columns([1, 1])
    with alloc_col:
        st.markdown('<div class="section-title">Dağılım</div>', unsafe_allow_html=True)
        render_allocation(active)
    with chart_col:
        st.markdown('<div class="section-title">Varlık Değeri</div>', unsafe_allow_html=True)
        if active.empty:
            st.markdown('<div class="empty-state">Grafik için aktif varlık bekleniyor.</div>', unsafe_allow_html=True)
        else:
            chart_df = active.sort_values("total_usd", ascending=False).set_index("label")[["total_usd"]]
            chart_df = chart_df.rename(columns={"total_usd": "USD Değer"})
            st.bar_chart(chart_df, height=330)

    st.markdown('<div class="section-title">Varlık Listesi</div>', unsafe_allow_html=True)
    render_asset_table(active)


def main() -> None:
    inject_css()
    data = get_live_data()

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        render_login()
        st.stop()

    render_topbar(data)
    nav_col, exit_col = st.columns([0.78, 0.22])
    with nav_col:
        page = st.radio(
            "Bölüm",
            ["Bahis Takibi", "Portföy"],
            horizontal=True,
            label_visibility="collapsed",
        )
    with exit_col:
        if st.button("Çıkış"):
            st.session_state["password_correct"] = False
            st.rerun()

    if page == "Bahis Takibi":
        render_betting_page(data)
    else:
        render_portfolio_page(data)


if __name__ == "__main__":
    main()
