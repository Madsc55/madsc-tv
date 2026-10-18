# 810 dosya notu — 19 Ekim 2026, ek parti 6

Önceki beyan edilen sayım: 324/450, 126 kalan. Bu partide 40 farklı kök dizin test dosyasının gerçek kaynak içeriği okundu. Testler çalıştırılmadı, dolayısıyla sonuç PASS olarak sunulmaz.

1. `test_akilli_tekrar_test_takvimi.py`
2. `test_ana_liste_saglik.py`
3. `test_bes_is_tek_dosya.py`
4. `test_candidate_logo_missing_report.py`
5. `test_central_all_remaining_tasks.py`
6. `test_central_archive_consistency.py`
7. `test_central_backup_evidence.py`
8. `test_central_consolidation_audit.py`
9. `test_central_duplicate_test_audit.py`
10. `test_central_eight_task_audit.py`
11. `test_central_eighteen_task_audit.py`
12. `test_central_failure_stage_report.py`
13. `test_central_ibo_review_queue.py`
14. `test_central_identity_epg_logo_audit.py`
15. `test_central_isolated_git_restore.py`
16. `test_central_main_playlist_run_evidence.py`
17. `test_central_management_summary.py`
18. `test_central_open_gaps.py`
19. `test_central_protected_write_gate.py`
20. `test_central_run_status.py`
21. `test_central_short_status.py`
22. `test_central_single_screen_report.py`
23. `test_central_source_reconciliation.py`
24. `test_central_workflow_inventory.py`
25. `test_epg_pilot.py`
26. `test_epg_tv_readiness.py`
27. `test_final_validation.py`
28. `test_five_category_92_workflow_audit.py`
29. `test_five_category_actions_evidence.py`
30. `test_five_category_candidate_media.py`
31. `test_five_category_candidate_scoring.py`
32. `test_five_category_disaster_behavior.py`
33. `test_five_category_discovery_behavior.py`
34. `test_five_category_discovery_history.py`
35. `test_five_category_evidence_transfer.py`
36. `test_five_category_logo_quality.py`
37. `test_five_category_permission_gate.py`
38. `test_five_category_priority_csv.py`
39. `test_five_category_runtime_integrity.py`
40. `test_five_category_stability_history.py`

**İçerik bulguları:** Aday tekrar zamanlaması yalnız süresi dolanları seçiyor ve playlist değiştirmeme bekleniyor. Ana liste sağlık testi hata sonucunun otomatik silme kararı olmadığını, paralel probe sırasını ve salt rapor davranışını doğrulamak üzere yazılmış. Beş iş raporu keşif, logo/EPG/kimlik, yedek geri yükleme, otomasyon ve kabul kanıtını ayrı test ediyor. Logo testleri aynı isimli farklı logo otomatik onaylanmasın, PNG bağımlılığı koşullu olsun, kaynak güvenliği korunsun diyor. Merkezi rapor testleri eksik/bozuk JSON kanıtını başarı saymıyor, sekiz/on sekiz görev kapsamını ayrı tutuyor, korunan dosya değişikliğini yasaklıyor. K1/merkezi koruma testleri workflow job izinleri ve legacy yazma yollarını tespit etmeyi, otomatik kapatma/otomatik onay vermemeyi hedefliyor. EPG pilotu gece yarısı tarih taşması ve ters zaman aralığı, IBO cihaz onayı beklemesi testleri içeriyor. Son doğrulama testleri eksik kanıtın geçememesi, üç geçiş şartı, Türk kaynak önceliği, önceki terminal sonucun tekrar test edilmemesi, telif/kimlik onayının otomatik verilmemesi şartlarını kapsıyor. 92 workflow testleri eski workflow'ların tamamının risk kuyruğunda kalması ve davranış kanıtı olmadan eşdeğer kabul edilmemesini hedefliyor. Medya testleri timestamp/hash bozulmasında fail-closed, geçmişteki pozitifin yeni negatifle değiştirilmesi ve provenance kontrolü içeriyor. Geçmiş geri yükleme testleri eski başarısızlıkları silmeme, checkout dosyalarını bozmama ve hatalı indirmede geçmişi sıfırlamama şartlarını kapsıyor. Delil aktarımı testleri aynı commit/branch/repo/başarılı koşu, checksum, symlink reddi ve çakışan dosyayı ezmeme kontrolleri içeriyor. Runtime bütünlük testleri silinmiş/izlenmeyen/ignored korunan dosyaları da yakalamayı amaçlıyor. Stabilite testleri tek ölçümü 25 saatlik kanıt saymama, aradaki hata ve zaman çelişkisini fail-closed ele alma şartları içeriyor. Bu kaynak kod beklentileri canlı workflow koşusu veya cihaz onayı kanıtı değildir.

**Aritmetik devam sayımı: 364/450, 86 kaldı.** UYARI: Önceki partilerdeki 324 sayısının başlangıçtaki 143 dosyayla küme bazında çakışma denetimi ayrıca gereklidir; bu rakam önceki raporlar üstünden taşınan çalışma sayımıdır, kesin tekilleştirilmiş envanter sayımı değildir. Üretim playlist/EPG/YEDEKLER/workflow değişmedi.
