with c_market:
            try:
                # BTC, ETH ve SOL verilerini tek seferde çekiyoruz
                tickers = yf.Tickers("BTC-USD ETH-USD SOL-USD")
                btc = tickers.tickers["BTC-USD"].fast_info['last_price']
                eth = tickers.tickers["ETH-USD"].fast_info['last_price']
                sol = tickers.tickers["SOL-USD"].fast_info['last_price']
                
                st.markdown(f"""
                <div class='industrial-card'>
                    <div class='terminal-header'>MARKET DATA</div>
                    <div class='terminal-row'><span>BITCOIN</span><span class='highlight'>${btc:,.2f}</span></div>
                    <div class='terminal-row'><span>ETHEREUM</span><span class='highlight'>${eth:,.2f}</span></div>
                    <div class='terminal-row'><span>SOLANA</span><span class='highlight'>${sol:,.2f}</span></div>
                </div>
                """, unsafe_allow_html=True)
            except: 
                st.error("Market data link lost.")
