# --- HEDEF YOLCULUĞU (KESİN ÇÖZÜM) ---
        target = 6500
        current_pct = min(100, (kasa / target) * 100)
        ms900_pct = (900 / target) * 100
        ms1200_pct = (1200 / target) * 100
        ms1800_pct = (1800 / target) * 100

        # Renkleri Python tarafında belirleyelim ki HTML içinde karmaşa çıkmasın
        c900 = "#ffae00" if kasa >= 900 else "#444"
        c1200 = "#ffae00" if kasa >= 1200 else "#444"
        c1800 = "#ffae00" if kasa >= 1800 else "#444"

        # HTML'i f-string yerine normal string birleştirme ile kuralım (en güvenlisi bu)
        progress_html = f"""
        <div class='industrial-card'>
            <div class='terminal-header'>HEDEF YOLCULUĞU (${target:,.0f})</div>
            <div class='prog-container'>
                <div class='ms-marker' style='left:{ms900_pct}%;'></div>
                <div class='ms-text' style='left:{ms900_pct}%; color:{c900};'>$900</div>
                
                <div class='ms-marker' style='left:{ms1200_pct}%;'></div>
                <div class='ms-text' style='left:{ms1200_pct}%; color:{c1200};'>$1200</div>
                
                <div class='ms-marker' style='left:{ms1800_pct}%;'></div>
                <div class='ms-text' style='left:{ms1800_pct}%; color:{c1800};'>$1800</div>
                
                <div class='prog-fill' style='width:{current_pct}%;'>
                    <span style='font-size:10px; font-family:Orbitron; color:white; font-weight:bold;'>%{current_pct:.1f}</span>
                </div>
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
