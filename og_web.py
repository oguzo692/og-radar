elif page == "📊 Portföy Takip":
    import requests
    from datetime import datetime, timedelta

    st.markdown("<div class='terminal-header'>🏛️ PORTFÖY KOMUTA MERKEZİ</div>", unsafe_allow_html=True)

    @st.cache_data(ttl=1800)
    def get_tefas_fund_price(fund_code="AFT"):
        """
        TEFAS'tan fonun son fiyatını çeker.
        Dönen değer: float fiyat (TL)
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=10)

            url = "https://www.tefas.gov.tr/api/DB/BindHistoryInfo"
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.tefas.gov.tr/"
            }

            data = {
                "fontip": "YAT",
                "bastarih": start_date.strftime("%d.%m.%Y"),
                "bittarih": end_date.strftime("%d.%m.%Y"),
                "fonunvantip": "",
                "sfontur": "",
                "fonkod": fund_code
            }

            r = requests.post(url, headers=headers, data=data, timeout=15)
            r.raise_for_status()

            js = r.json()
            items = js.get("data", [])

            if not items:
                return None

            # en güncel kaydı al
            latest = items[-1]

            # TEFAS bazen "price", bazen farklı alan döndürebiliyor, kontrollü okuyalım
            price = latest.get("FIYAT") or latest.get("fiyat") or latest.get("price")

            if price is None:
                return None

            return float(str(price).replace(",", "."))
        except Exception:
            return None

    try:
        usd_try = yf.Ticker("USDTRY=X").history(period="1d")["Close"].iloc[-1]
        ons_gold = yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1]
        gram_altin = (ons_gold / 31.1035) * usd_try
        ceyrek_fiyat = gram_altin * 1.74

        aft_price_tl = get_tefas_fund_price("AFT")

        def get_val(key):
            try:
                return float(live_vars.get(key, 0))
            except:
                return 0.0

        users = ["oguzo", "ero7", "fybey"]
        display_data = []

        for u in users:
            u_usd = get_val(f"{u}_usd")
            u_gr = get_val(f"{u}_altin")
            u_cy = get_val(f"{u}_ceyrek")
            u_aft = get_val(f"{u}_aft_adet")  # yeni alan: AFT adet

            aft_total_tl = u_aft * aft_price_tl if aft_price_tl else 0
            aft_total_usd = aft_total_tl / usd_try if usd_try else 0

            t_usd = (
                u_usd
                + (u_gr * gram_altin / usd_try)
                + (u_cy * ceyrek_fiyat / usd_try)
                + aft_total_usd
            )

            display_data.append({
                "Kullanıcı": u.upper(),
                "USD": u_usd,
                "Gram": u_gr,
                "Çeyrek": u_cy,
                "AFT_Adet": u_aft,
                "AFT_Fiyat_TL": aft_price_tl if aft_price_tl else 0,
                "AFT_Toplam_TL": aft_total_tl,
                "TOPLAM_USD": t_usd
            })

        df_portfoy = pd.DataFrame(display_data)

        if not df_portfoy.empty:
            secilen_user = st.selectbox("Kullanıcı Portföy Detayı:", ["OGUZO", "ERO7", "FYBEY"])
            u_row = df_portfoy[df_portfoy["Kullanıcı"] == secilen_user]
            total_val = float(u_row["TOPLAM_USD"].values[0])

            # Dev Kart
            st.markdown(
                f"""
                <div class='industrial-card' style='text-align:center; border-top: 4px solid #cc7a00;'>
                    <div style='font-size:14px; color:#666; letter-spacing:2px;'>TOPLAM PORTFÖY DEĞERİ</div>
                    <div style='font-size:55px; font-weight:900; color:#cc7a00; font-family:Orbitron;'>${total_val:,.2f}</div>
                    <div style='font-size:18px; color:#444;'>≈ ₺{(total_val * usd_try):,.0f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Varlık Dağılımı
            v1, v2, v3, v4 = st.columns(4)

            with v1:
                st.markdown(
                    f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>NAKİT</div><div class='highlight'>${u_row['USD'].values[0]:,.0f}</div></div>",
                    unsafe_allow_html=True
                )

            with v2:
                st.markdown(
                    f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>GRAM ALTIN</div><div class='highlight'>{u_row['Gram'].values[0]} gr</div></div>",
                    unsafe_allow_html=True
                )

            with v3:
                st.markdown(
                    f"<div class='industrial-card' style='text-align:center;'><div style='font-size:11px; color:#666;'>ÇEYREK ADET</div><div class='highlight'>{u_row['Çeyrek'].values[0]:,.0f}</div></div>",
                    unsafe_allow_html=True
                )

            with v4:
                st.markdown(
                    f"""
                    <div class='industrial-card' style='text-align:center;'>
                        <div style='font-size:11px; color:#666;'>AFT</div>
                        <div class='highlight'>{u_row['AFT_Adet'].values[0]:,.2f} adet</div>
                        <div style='font-size:12px; color:#888;'>₺{u_row['AFT_Fiyat_TL'].values[0]:,.4f} / pay</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # AFT detay kartı
            st.markdown(
                f"""
                <div class='industrial-card' style='text-align:center;'>
                    <div style='font-size:12px; color:#666;'>AFT TOPLAM DEĞERİ</div>
                    <div style='font-size:28px; font-weight:800; color:#cc7a00;'>₺{u_row['AFT_Toplam_TL'].values[0]:,.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # AI ÖNGÖRÜSÜ
            st.divider()
            st.markdown("<div class='terminal-header'>🧠 AI PROJEKSİYONU (HAZİRAN 2026)</div>", unsafe_allow_html=True)

            aylar = ["Şubat", "Mart", "Nisan", "Mayıs", "Haziran"]
            tahminler = [total_val]

            for i in range(1, len(aylar)):
                rastgele_sapma = np.random.uniform(-0.02, 0.02)
                yeni_deger = tahminler[-1] * (1.10 + rastgele_sapma)
                tahminler.append(yeni_deger)

            chart_df = pd.DataFrame({"Varlık ($)": tahminler}, index=aylar)
            c1, c2 = st.columns([1, 2])

            with c1:
                st.write(f"### {secilen_user} Hedef")
                st.markdown(f"<h1 style='color:#00ff41;'>${tahminler[-1]:,.0f}</h1>", unsafe_allow_html=True)
                st.caption("Mevcut gidişatla Haziran 2026 tahmini (Volatilite Dahil)")

            with c2:
                st.area_chart(chart_df, color="#cc7a00")

        # Piyasa Bilgi Bandı
        st.divider()
        p1, p2, p3, p4 = st.columns(4)
        p1.caption(f"USD/TRY: ₺{usd_try:.2f}")
        p2.caption(f"Gram Altın: ₺{gram_altin:.0f}")
        p3.caption(f"Çeyrek Altın: ₺{ceyrek_fiyat:.0f}")
        p4.caption(f"AFT Fiyatı: ₺{aft_price_tl:.4f}" if aft_price_tl else "AFT Fiyatı: Veri alınamadı")

    except Exception as e:
        st.error(f"Piyasa verileri çekilirken bir hata oluştu: {e}")
