# 810 dosya notu — 19 Ekim 2026, ek parti 3

Önceki: 192/450, 258 kaldı. Yeni açılıp gerçek içeriği incelenen 14 farklı dosya:
madsc_kesif/ana_liste_saglik_raporu.csv
madsc_kesif/ana_liste_test_gecmisi.json
madsc_kesif/candidate_logos.json
madsc_kesif/eski_bozuk_linkler.csv
madsc_kesif/ibo_354_3_334_turk_calismaz_arsiv.m3u
madsc_kesif/ibo_3_5281_ayrilanlar.m3u
madsc_kesif/ibo_3_5281_kararlar.csv
madsc_kesif/ibo_6115_ikinci_ayrilanlar.m3u
madsc_kesif/ibo_6115_ikinci_kararlar.csv
madsc_kesif/tekrarlar.csv
madsc_son_kontrol/kimlik_devam_2026-10-12_1955.json
madsc_son_kontrol/kimlik_incelemesi_2026-10-12.json
madsc_son_kontrol/summary.json
madsc_dogrulama/summary.json

Bulgular: Ana liste sağlık raporu 1039 kanal satırı; test geçmişi channels nesnesinde kanal bazlı son test ve başarılı koşu saklanıyor. Eski bozuk linkler 4543 veri satırı, yeniden test arşivi; tekrarlar CSV 3510 veri satırı, AYNI_URL örnekleri var. 354 arşivinde 332 EXTINF; 3–5281 ayrılanlar 5252 EXTINF, karar CSV 5279 veri satırı; 6115 ikinci ayrılanlar 5585 EXTINF, karar CSV çok satırlı tırnaklı alanlar içerdiği için fiziksel 11930 satır sayısı kayıt sayısı değildir (CSV parser ile doğrulanmalı). 12 Ekim kimlik devam raporu 39 kayıt/35 yakalanan kare, yeniden stream testi değil. Kimlik incelemesi 36 görsel, 3 kare yok; IBO cihaz onayı ayrı. Son kontrol 3800 tamamlanan aday, 2574 kalan; 300 saniyelik kontrol, playlist-ready durum ayrıca değerlendirilir. Doğrulama özeti 7100 adayın üç denemesi tamamlandı; 6374 üç decode geçişi, 398 failed, 0 playlist-ready. Bu sonuçlar 14 Ekim tarihli tarihsel snapshot; kullanıcı onayı veya canlı IBO garantisi değil. Üretim ve yedek dosyaları değiştirilmedi.

**Yeni sayım 206/450, kalan 244.** Ana not büyük olduğu için bu ek aynı dalda ayrı commit ile tutulur.
