import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz

# --- 1. AYARLAR ---
st.set_page_config(page_title="OG Core v7.1", page_icon="🛡️", layout="wide")

# --- 2. CSS STİLLERİ (GİZLİLİK MODU - O YAZILARI SİLER) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
.main { background-color: #0d1117 !important; }
* { font-family: 'JetBrains Mono', monospace !important; }
:root { --soft-orange: #cc7a00; --win-green: #00ff41; --loss-red: #ff4b4b; --terminal-gray: #8b949e; }

/* --- GİZLİLİK MODU: O YAZIYI VE BUTONLARI YOK EDEN KISIM --- */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="stToolbar"] {visibility: hidden !important;}
[data-testid="stDecoration"] {display:none;}
[data-testid="stSidebarNav"] {border-right: 1px solid #30363d;}
/* ----------------------------------------------------------- */

.industrial-card {
    background: rgba(255, 255, 255, 0.02);
    border-left: 3px solid var(--soft-orange);
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 20px;
}
.terminal-header { 
    color: var(--soft-orange); 
    font-size: 14px; 
    font-weight: bold; 
    border-bottom: 1px dashed #30363d; 
    padding-bottom: 5px; 
    margin-bottom: 10px;
    text-transform: uppercase;
}
.terminal-row {
    display: flex; justify-content: space-between;
    font-size: 13px; color: #e6edf3; margin-bottom: 6px;
}
.highlight { color: var(--soft-orange); }
.win { color: var(--win-green); }
.loss { color: var(--loss-red); }
.dim { color: var(--terminal-gray); }
.status-wait { color: #f1c40f; font-weight: bold; }

h1, h2, h3 { color: #e6edf3 !important; }
section[data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }
</style>
"""

# --- 3. HTML ŞABLONLARI ---

# W3 Kuponu
w3_coupon_html = """
<div class='industrial-card'>
    <div class='terminal-header'>🔥 W3 KUPONU</div>
    <div class='terminal-row'><span>Wolfsburg - Bvb</span><span class='highlight'>bvb x2 & 1
