elif page == "📊 Portföy Takip":
        st.markdown("<div class='terminal-header'>🏛️ PORTFÖY KOMUTA MERKEZİ</div>", unsafe_allow_html=True)
        
        # --- 1. VERİLERİ ÇEK ---
        try:
            usd_try = yf.Ticker("USDTRY=X").history(period="1d")['Close'].iloc[-1]
            ons_gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            gram_altin = (ons_gold / 31.1035) * usd_try
            ceyrek_fiyat = gram_altin * 1.82 
            
            users = ["oguzo", "ero7", "fybey"]
            display_data = []
            for u in users:
                u_usd = get_val(f"{u}_usd")
                u_gr = get_val(f"{u}_altin")
                u_cy = get_val(f"{u}_ceyrek")
                t_usd = u_usd + (u_gr * gram_altin / usd_try) + (u_cy * ceyrek_fiyat / usd_try)
                display_data.append({
                    "Kullanıcı": u.upper(), "USD": u_usd, "Gram": u_gr, "Çeyrek": u_cy, "TOPLAM_USD": t_usd
                })
            df_portfoy = pd.DataFrame(display_data)
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
            df_portfoy = pd.DataFrame()

        # --- 2. KULLANICI SEÇİMİ VE ANA KART ---
        if not df_portfoy.empty:
            secilen_user = st.selectbox("Kullanıcı Portföy Detayı:", ["OGUZO", "ERO7", "FYBEY"])
            u_row = df_portfoy[df_portfoy["Kullanıcı"] == secilen_user]
            total_val = u_row["TOPLAM_USD"].values[0]
            total_tl = total_val * usd_try

            # Tavuk Döner Hesabı
            doner_fiyati = get_val("doner_fiyat")
            if doner_fiyati <= 0: doner_fiyati = 150.0 # Fallback fiyat
            doner_sayisi = total_tl / doner_fiyati

            # GÜNCELLENEN ÜST KART (DÖNERLİ)
            st.markdown(f"""
                <div class='industrial-card' style='text-align:center; border-top: 4px solid #cc7a00; padding: 20px;'>
                    <div style='font-size:12px; color:#666; letter-spacing:2px;'>TOPLAM PORTFÖY DEĞERİ</div>
                    <div style='font-size:45px; font-weight:900; color:#cc7a00; font-family:Orbitron; margin: 10px 0;'>${total_val:,.2f}</div>
                    <div style='font-size:16px; color:#666;'>≈ ₺{total_tl:,.0f}</div>
                    <div style='font-size:18px; color:#ffae00; font-weight:bold; margin-top:15px; border-top: 1px dashed #333; padding-top:10px;'>
                        🌯 {doner_sayisi:,.0f} Adet Yarım Ekmek Döner
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Varlık Kartları
            v1, v2, v3 = st.columns(3)
            with v1: st.markdown(f"<div class='industrial-card' style='text-align:center; padding:10px;'><div style='font-size:10px; color:#666;'>NAKİT</div><div class='highlight' style='font-size:16px;'>${u_row['USD'].values[0]:,.0f}</div></div>", unsafe_allow_html=True)
            with v2: st.markdown(f"<div class='industrial-card' style='text-align:center; padding:10px;'><div style='font-size:10px; color:#666;'>GRAM ALTIN</div><div class='highlight' style='font-size:16px;'>{u_row['Gram'].values[0]} gr</div></div>", unsafe_allow_html=True)
            with v3: st.markdown(f"<div class='industrial-card' style='text-align:center; padding:10px;'><div style='font-size:10px; color:#666;'>ÇEYREK ADET</div><div class='highlight' style='font-size:16px;'>{u_row['Çeyrek'].values[0]:,.0f}</div></div>", unsafe_allow_html=True)

        # --- 3. ANALİZ PANELİ (GRAFİKLER) ---
        st.divider()
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("<div class='terminal-header' style='font-size:10px;'>🧠 AI PROJEKSİYONU</div>", unsafe_allow_html=True)
            aylar = ["Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]
            tahminler = [total_val * (1.10**i) for i in range(len(aylar))]
            chart_df = pd.DataFrame({"Varlık ($)": tahminler}, index=aylar)
            st.area_chart(chart_df, color="#cc7a00", height=200)
            st.caption(f"Haziran Hedefi: ${tahminler[-1]:,.0f}")

        with col_right:
            st.markdown("<div class='terminal-header' style='font-size:10px;'>📊 KOMPOZİSYON</div>", unsafe_allow_html=True)
            try:
                import plotly.graph_objects as go
                fig = go.Figure(data=[go.Pie(
                    labels=['Nakit', 'Gram', 'Çeyrek'], 
                    values=[u_row['USD'].values[0], (u_row['Gram'].values[0]*gram_altin/usd_try), (u_row['Çeyrek'].values[0]*ceyrek_fiyat/usd_try)], 
                    hole=.5,
                    marker=dict(colors=['#cc7a00', '#ffae00', '#333333'])
                )])
                fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), height=200)
                st.plotly_chart(fig, use_container_width=True)
            except: st.write("Veri bekleniyor...")

        # --- 4. PİYASA BANDI ---
        st.divider()
        p1, p2, p3 = st.columns(3)
        p1.caption(f"USD: ₺{usd_try:.2f}")
        p2.caption(f"Gram: ₺{gram_altin:.0f}")
        p3.caption(f"Çeyrek: ₺{ceyrek_fiyat:.0f}")
