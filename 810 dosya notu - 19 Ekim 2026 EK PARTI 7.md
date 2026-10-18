# 810 dosya notu — 19 Ekim 2026, ek parti 7

Bu partide 63 kaynak dosyanın gerçek içeriği açıldı ve incelendi. Bazıları ilk 143'lük tarihsel denetimle çakışabilir; bu nedenle doğrulanmadan 63 yeni dosya sayılmamalıdır.

1. `tools/candidate_status_summary.py`
2. `tools/change_simulation.py`
3. `tools/channel_stability.py`
4. `tools/cuma_denetim_uyari_ozeti.py`
5. `tools/eksik_turk_kanal_takibi.py`
6. `tools/genel_sistem_bakimi.py`
7. `tools/genis_kaynak_taramasi.py`
8. `tools/guncel_test_durum_ozeti.py`
9. `tools/haftalik_ana_liste_denetimi.py`
10. `tools/kaynak_kapsam_denetimi.py`
11. `tools/logo_epg_audit.py`
12. `tools/protected_write_gate.py`
13. `tools/sistem_saglik_denetimi.py`
14. `tools/son_kontrol_yedekler_aktar.py`
15. `tools/test_adaylarini_yedege_hazirla.py`
16. `tools/workflow_failure_gate.py`
17. `tools/workflow_safety.py`
18. `tools/yedekler_guvenli_ekle.py`
19. `vod/IBO-AYRI-KURULUM.md`
20. `vod/README.md`
21. `vod/TEST-FILMLER.m3u`
22. `vod/guncel-bolumler.json`
23. `vod/katalog.json`
24. `vod/kategoriler.json`
25. `yedekler/ADAY_KANALLAR_2026-10-09.txt`
26. `yedekler/GECMIS_KANAL_KARARLARI_KORUMA_2026-10-09.md`
27. `yedekler/IBO_BAGIMSIZ_TEST_ADAYLARI_2026-10-10.m3u`
28. `yedekler/IBO_ESKI_CALISMAYANLAR_2026-10-09.m3u`
29. `yedekler/IBO_TEKNIK_TEST_GECMEYENLER_2026-10-09.m3u`
30. `yedekler/IBO_TUM_KONTROL_ADAYLARI_2026-10-09.m3u`
31. `yedekler/IBO_YEDEK_EKSIK_KANALLAR_2026-10-09.txt`
32. `yedekler/IBO_YEDEK_KALITE_RAPORU_2026-10-09.csv`
33. `yedekler/SOZCU_AKIT_OZEL_TEST_2026-10-09.csv`
34. `yedekler/TARAMA-TEST-SONUCLARI.m3u`
35. `yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u`
36. `yedekler/TV5_ADAY_2026-10-09.m3u`
37. `yedekler/YENILER-SILINEN-TEST-ADAYLARI-2026-10-10.m3u`
38. `yedekler/YENILER_KAYNAK_HATALARI_2026-10-09.txt`
39. `yedekler/YENILER_KAYNAK_HATALARI_2026-10-09_GRUP1.txt`
40. `yedekler/ibo_yedek_kalite_tespit.py`
41. `yedekler/sozcu_akit_ozel_test.py`
42. `yedekler/teknik_adaylari_aktar.py`
43. `yedekler/tekrar_test_390.py`
44. `tarama/iptv-org-tr-adaylar-2026-10-10.m3u`
45. `tarama/son-test-raporu.json`
46. `aday_bekletme/GELISMIS_MEDYA_TESTI.csv`
47. `aday_bekletme/KAYNAK_GUVEN_PUANLARI.csv`
48. `AGENTS.md`
49. `BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md`
50. `BES_SISTEM_GECIS_KONTROL.md`
51. `BES_SISTEM_TOPLU_IS_DEFTERI.md`
52. `CALISMAYANLAR.txt`
53. `DEVIR_NOTU_2026-10-15.md`
54. `GUVENLIK_KURALLARI.md`
55. `IPTV_PROJE_HAFIZASI.md`
56. `MADSC55_TV_YENI_KURULUM.md`
57. `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md`
58. `MERKEZI_ARSIV_HARITASI.md`
59. `ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md`
60. `OZELLIK_ENVANTERI.md`
61. `SEKIZ_GOREV_TOPLU_DENETIM.md`
62. `TOPLU_DURUM_RAPORU.md`
63. `YENIDEN_KURULUM_KORUMA_PLANI.md`

Bulgular: 18 tools dosyası aday özeti, değişim simülasyonu, stabilite, kaynak tarama, haftalık liste, logo/EPG, korunan yazma kapısı, sistem sağlığı, son kontrol yedek aktarımı, hata devre kesici ve kontrollü YEDEKLER ekleme işlevlerini kapsar; yedek aktarım/yazma araçları eski kullanıcı onayı olmadan çalıştırılmamalı. Altı VOD dosyası ana canlı TV listesinden ayrı pilot içerik ve katalog/takvimdir, güncel bölümler oynatma bağlantısı değildir. Yedekler dosyaları tarihsel kullanıcı/teknik aday listeleridir: 18 yeni aday, 5 bağımsız IBO adayı, 82 eski çalışmayan, 295 teknik geçmeyen, 306 IBO toplu aday, 390 tüm teknik aday, 77 kullanıcıca çıkarılan YENILER test adayı, 86 ilk HTTP/HLS geçen ama player doğrulanmayan akış, 1 TV5 aday; bu sayılar farklı anların örtüşebilen kayıtlarıdır, birleştirilmemeli. Kaynak hataları DNS çözümlenemeyen URL'leri içerir. 149 IPTV-org aday taraması, 86 HTTP/HLS geçen, player doğrulaması yok. İki aday_bekletme CSV'si medya ve kaynak güven puanları; canlı sonuç sayılmamalı. Kök belgelerde 92 workflow envanteri, beşli geçiş koşulları, 19 koruma kuralı, sekiz görev, eski devir notları, arşiv haritası ve yazma yetkisi sınırları incelendi. Bu turda dosyalar çalıştırılmadı, üretim dosyaları değiştirilmedi.

Büyük dosyalar: aday_bekletme/ADAY_DURUM_RAPORU.csv, ADAY_ONCELIK_RAPORU.csv, gecmis.json; yedekler/YENILER_TARAMA_RAPORU_2026-10-09.csv, ...GRUP1.csv, CALISANLAR_ONCESI_YENILER_2026-10-10.m3u, KORUMA_ONCESI_YEDEKLER_YENILER_2026-10-10.m3u ve diğer 1MB+ dosyalar bu partide okunmadı. Önceki 86 kalan sayısı eski partilerdeki çakışmalarla tam tekilleştirilmedi; kesin sıfır iddiası yok.
