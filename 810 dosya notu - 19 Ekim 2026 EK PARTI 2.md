# 810 dosya denetimi — 19 Ekim ek parti 2

Ana 810 notuna bağlı ek; aynı dalda korunur. Önceki toplam 161/450, kalan 289.

Bu partide gerçek içerikleri açılıp denetlenen 31 yeni yol:
madsc_kesif/DORT_ASAMA_TEK_RAPOR.json
madsc_kesif/NOT_EKSIK_TURK_KANALLARI.md
madsc_kesif/adaylar.csv
madsc_kesif/alternatifler.csv
madsc_kesif/ana_liste_calismayanlar.csv
madsc_kesif/arastirma_kaynaklari.csv
madsc_kesif/candidate_epg_logo_join.json
madsc_kesif/candidate_logo_missing_report.json
madsc_kesif/ibo_354_335_354_yabanci_arsiv.m3u
madsc_kesif/ibo_354_iki_kategori_rapor.json
madsc_kesif/ibo_364_355_364_rapor.json
madsc_kesif/ibo_364_355_364_yabanci_arsiv.m3u
madsc_kesif/ibo_398_16_49_rapor.json
madsc_kesif/ibo_398_16_49_yabanci_arsiv.m3u
madsc_kesif/ibo_3_5281_rapor.json
madsc_kesif/ibo_530_399_sonrasi_rapor.json
madsc_kesif/ibo_530_399_sonrasi_yabanci_arsiv.m3u
madsc_kesif/ibo_6115_ikinci_rapor.json
madsc_kesif/ibo_ilk_239_ayirma_raporu.json
madsc_kesif/ibo_kullanici_kararlari.csv
madsc_kesif/ibo_kullanici_secimi_2026-10-13_3-5281.md
madsc_kesif/kaynak_erisim_raporu.csv
madsc_kesif/kaynak_guncelligi.csv
madsc_kesif/kullanici_ibo_kararlari_2026-10-11.json
madsc_kesif/logo_candidates.json
madsc_kesif/ozet.json
madsc_kesif/player_uyumlulugu_belirsiz.csv
madsc_kesif/yedek_11599_geri_yukleme_raporu.json
madsc_kesif/yedek_turk_ayirma_raporu.json
madsc_kesif/yedek_turk_yeniden_inceleme_raporu.json
madsc_kesif/yuksek_kalite_alternatifleri.csv

Bulgular: DORT_ASAMA raporu yedek geri yükleme testi ve bağımsız dış kopya kanıtı eksik diyor; 11762 tarihsel giriş, 11742 arşiv URL'si; keşifte 75 aday ve 4 alternatif. Adaylar CSV 75 satır, alternatifler 4; 23 ana liste çalışmayan kayıt, kullanıcı kararı test ile karıştırılmamalı. Logo adayları 75; 13 indirme/dönüşüm hatası, 28 güvenlik incelemesi, 7 PNG bekliyor, 27 PNG hazır ama kimlik onayı bekliyor. candidate_epg_logo_join 0 aday sonucu ve 5 pilot EPG kanalı; tam üretim kapsamı değil. 354'ten 20 yabancı ayrıldı; 364'ten 10, 398'den 34, 530'dan 132 arşivlendi. 354 iki kategori raporunda 332 Türk kanalının çalışmadığı yalnız kullanıcı bildirimi, teknik retest yok. 3–5281 IBO kararında 5252 yabancı arşiv, 27 Türk tutuldu, önce 11367 sonra 6115 yedek; 6115 incelemesinde 5585 yabancı ayrıldı, 530 kaldı. İlk 11599'dan 232 ayrıldı (36 çalışmayan Türk, 196 yabancı/oynatımı bilinmeyen), sonra 11367 kaldı. Tarihsel 11599→42 ayırma işlemi 11557 arşiv, bunların 10817'si kimlik belirsiz; daha sonra 11557 geri yüklenmiş, oynatma testi yok. Bu farklı zamanların raporlarıdır; yeni silme/taşıma izni değildir. 75 logo adayının görsel kimlik doğrulaması gereklidir. Kaynak güncelliği CSV 157 kayıt, kaynak erişim 15 kayıt; kaynak sayıları canlı doğrulama değildir. Üretim dosyalarına dokunulmadı.

**Toplam: 192/450 incelendi; 258 kaldı.** Daha önce incelenen yollar tekrar sayılmadı.
