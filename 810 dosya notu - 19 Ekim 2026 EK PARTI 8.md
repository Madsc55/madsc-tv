# 810 dosya notu — 19 Ekim 2026, ek parti 8 / büyük dosyalar ve kalan kodlar

Bu turda GitHub gerçek blob SHA ile daha önce boş dönen büyük dosyalar da içerik olarak açıldı. Kaynaklar:
- aday_bekletme/ADAY_DURUM_RAPORU.csv: 2668 fiziksel veri satırı, aday türü, teknik/medya test, kaynak, ilk/son görülme ve başarı sayıları.
- aday_bekletme/ADAY_ONCELIK_RAPORU.csv: 1.107.014 karakter, öncelik ve inceleme notu içeren CSV.
- aday_bekletme/gecmis.json: 2.034.390 karakter, URL bazlı first_seen/last_seen tarihsel aday geçmişi.
- madsc_kesif/bulunan_kanal_arsivi.csv: 11743 veri satırı; kanal, URL, kaynak, sınıf, teknik ve IBO durum, tarih alanları.
- madsc_kesif/gecmis.json: 4.800.877 karakter, history anahtarında kaynak/URL geçmişi.
- madsc_kesif/yedek_ulke_inceleme.csv: 11558 veri satırı, channel/url/status.
- madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u: 11557 EXTINF, eski YEDEKLER arşivi; otomatik yeniden uygulama yasak.
- madsc_son_kontrol/results.json: 3800 aday sonuç kaydı, güncel canlı IBO onayı değil.
- madsc_dogrulama/state.json: 5.962.243 karakter, channels bazlı doğrulama state.
- yedekler/CALISANLAR_ONCESI_YENILER_2026-10-10.m3u: 597 EXTINF, eski snapshot.
- yedekler/KORUMA_ONCESI_YEDEKLER_YENILER_2026-10-10.m3u: 935 EXTINF, eski snapshot.
- yedekler/YENILER_TARAMA_RAPORU_2026-10-09.csv: 2865 veri satırı, teknik ve medya test/kaynak alanları.
- yedekler/YENILER_TARAMA_RAPORU_2026-10-09_GRUP1.csv: 2665 veri satırı, ek LOGO_ADAY_URL alanı.
- aday_bekletme/TEKRAR_EDEN_ADAYLAR.csv: 470 veri satırı, tekrar sayısı/kanal adı/kaynak.
- epg/ibo-test-epg.xml: 125565 karakterlik beş kanallı tanılama XMLTV, prod EPG değil.
- TEST_RAPORU.csv: 637 veri satırı, kanal, teknik durum, kalite, codec ve URL.
- YENILER.m3u: 58 EXTINF; dosya korunur, değiştirilmedi.

Kalan kaynak kodlar ayrıca gerçek içerik olarak okundu:
aday_bekletme.py, aday_hata_siniflandirma.py, aday_oncelik_raporu.py, aday_tekrar_raporu.py, akilli_tekrar_test_takvimi.py, altinci_aday_tekrar_test.py, channel_name_normalization.py, discovery_m3u_parser.py, arastirma/uydu_karsilastir.py, epg_deneme/README.md, epg_deneme/build.py, verification_pipeline.py, yanlis_pozitif_koruma.py, yeni_aday_on_test.py, yeni_kanal_tara.py, test_five_category_wide_scan.py, test_five_system_migration_audit.py, test_sistem_saglik_denetimi.py, test_tek_merkez_tetikleme.py, test_toplu_durum_raporu.py, test_verification_pipeline.py, test_workflow_failure_gate.py, test_yedekler_teknik_aktar.py, docs/BESLI_SISTEM_GECIS_RUNBOOK.md, docs/MADSC-92-WORKFLOW-ESDEGERLIK-KONTROL-2026-10-14.md, docs/MADSC-IKI-TOPLU-KABUL-PLANI.md.

Bulgular: tekrar planlama süre dolumu, medya/yanlış pozitif koruma, kaynak normalizasyonu, beş kanal EPG denemesi ve 92 workflow geçiş kanıtı ile koruma koşulları ayrılmış. Testler çalıştırılmadı; statik kod/rapor incelemesi tamamlandı. Korunan üretim, YEDEKLER, favoriler, EPG ve workflow dosyaları değiştirilmedi.

ÖNEMLİ SAYIM DÜZELTMESİ: Önceki 86 kalan sayısı aritmetik partilerin eski 143 kaynakla çakışması kontrol edilmeden üretilmişti; güvenilir kalan sayı değildir. Kesin kalan, ilk 143'lük tarihsel yol listesinin ve ek parti 1–8 yol listelerinin tekilleştirilerek sabit 450 temel dosyayla karşılaştırılmasından sonra bildirilmelidir. Bu ek incelemelerden sonra sıfır kaldığı doğrulanmadı.
