import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import pytz
import json
import os

# --- 1. AYARLAR ---
st.set_page_config(
    page_title="OG Core v8.8", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. CSS STİLLERİ (ANİMASYONLU SİBER TASARIM) ---
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;700&display=swap');

/* ANA ARKA PLAN */
.main { background-color: #050505 !important; }

/* GENEL FONT */
body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], p, div, span, h1, h2, h3, button, input { 
    font-family: 'JetBrains Mono', monospace !important; 
}

/* --- 📺 ANİMASYONLU AUTH EKRANI --- */
.auth-container {
    padding: 3rem;
    background: rgba(15, 15, 15, 0.95);
    border: 1px solid #cc7a00;
    border-radius: 4px;
    box-shadow: 0 0 30px rgba(204, 122, 0, 0.1);
    text-align: center;
    margin-top: 50px;
    position: relative;
    overflow: hidden;
}

/* SCANLINE ANİMASYONU */
.auth-container::before {
    content: " ";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 2px;
    background: rgba(204, 122, 0, 0.2);
    box-shadow: 0 0 10px #cc7a00;
    animation: scanline 4s linear infinite;
    z-index: 5;
}

@keyframes scanline {
    0% { top: 0%; }
    100% { top: 100%; }
}

/* BAŞLIK TİTREME (FLICKER) */
.auth-header {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 50px;
    font-weight: bold;
    color: #cc7a00;
    letter-spacing: 12px;
    margin-bottom: 10px;
    text-shadow: 0 0 15px rgba(204, 122, 0, 0.6);
    animation: flicker 2s infinite;
}

@keyframes flicker {
    0% { opacity: 0.9; }
    5% { opacity: 0.8; }
    10% { opacity: 1; }
    15% { opacity: 0.9; }
    25% { opacity: 1; }
    100% { opacity: 1; }
}

.auth-status {
    font-size: 11px;
    color: #8b949e;
    letter-spacing: 4px;
    margin-bottom: 30px;
    text-transform: uppercase;
}

/* INPUT VE BUTONLAR */
.stTextInput > div > div > input {
    background-color: rgba(0,0,0,0.5) !important;
    border: 1px solid #30363d !important;
    color: #00ff41 !important; /* Matrix Yeşili Yazı */
    text-align: center;
    font-size: 20px !important;
    transition: all 0.3s;
}

.stTextInput > div > div > input:focus {
    border-color: #cc7a00 !important;
    box-shadow: 0 0 10px rgba(204, 122, 0, 0.3) !important;
}

div.stButton > button {
    background-color: transparent !important;
    color: white !important;
    border: 1px solid #cc7a00 !important;
    border-radius: 0px !important;
    width: 100% !important;
    font-weight: bold !important;
    letter-spacing: 5px !important;
    height: 50px;
    transition: 0.4s;
}

div.stButton > button:hover {
    background-color: #cc7a00 !important;
    color: #000 !important;
    box-shadow: 0 0 20px #cc7a00;
}

/* SIDEBAR & CARDS */
.industrial-card { 
    background: rgba(255, 255, 255, 0.02); 
    border-left: 3px solid #cc7a00; 
    padding: 15px; 
    margin-bottom: 20px;
    transition: transform 0.2s;
}
.industrial-card:hover { transform: scale(1.01); }

.terminal-header { color: #cc7a00; font-size: 14px; font-weight: bold; border-bottom: 1px dashed #30363d; padding-bottom: 5px; margin-bottom: 10px; text-transform: uppercase; }
.terminal-row { display: flex; justify-content: space-between; font-size: 13px; color: #e6edf3; margin-bottom: 6px; }
.highlight { color: #cc7a00; font-weight: bold; }
.win { color: #00ff41; font-weight: bold; }
.loss { color: #ff4b4b; font-weight: bold; }

/* LOOT BAR */
.loot-wrapper { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px 25px 50px 25px; margin-bottom: 25px; position: relative; }
.loot-track { background: #21262d; height: 14px; border-radius: 7px; width: 100%; position: relative; margin-top: 45px; }
.loot-fill { 
    background: linear-gradient(90deg, #cc7a00, #ffae00); 
    height: 100%; border-radius: 7px; 
    box-shadow: 0 0 15px rgba(204, 122, 0, 0.5);
    transition: width 1s ease-in-out; 
}
.milestone { position: absolute; top: 50%; transform: translate(-50%, -50%); width: 120px; display: flex; flex-direction: column; align-items: center; z-index: 10; }
.milestone-label { position: absolute; top: 18px; font-size: 11px; font-weight: bold; color: #8b949e; text-align: center
