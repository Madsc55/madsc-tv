# 810 dosya notu — 19 Ekim 2026, 100 dosyalık toplu inceleme, ek parti 5

Önceki sayım: 224/450, kalan 226. Aşağıdaki 100 benzersiz kaynak dosyasının içeriği GitHub üzerinden ayrı ayrı okunup işlev ve yazma riski incelendi; dosyalar çalıştırılmadı. Üretim, YEDEKLER, EPG ve workflow değiştirilmedi.

1. `scripts/acceptance_26_92.py`
2. `scripts/akilli_aday_puanla.py`
3. `scripts/ana_liste_saglik.py`
4. `scripts/apply_ibo_3_5281.py`
5. `scripts/apply_ibo_6115_second.py`
6. `scripts/apply_ibo_decisions_group1.py`
7. `scripts/apply_ibo_first_239_decisions.py`
8. `scripts/apply_ibo_second_voice.py`
9. `scripts/apply_ibo_session2_6115.py`
10. `scripts/archive_backups_16_49.py`
11. `scripts/archive_backups_354_classified.py`
12. `scripts/archive_backups_355_364.py`
13. `scripts/archive_backups_399_onward.py`
14. `scripts/audit_workflow_security.py`
15. `scripts/automatic_png_logos.py`
16. `scripts/birlesik_aday_raporu.py`
17. `scripts/build_epg.py`
18. `scripts/build_ibo_epg_test.py`
19. `scripts/bulk_integrity_gate.py`
20. `scripts/candidate_epg_logo_join.py`
21. `scripts/candidate_logo_missing_report.py`
22. `scripts/candidate_logo_report.py`
23. `scripts/category_candidate_media.py`
24. `scripts/category_candidate_scoring.py`
25. `scripts/category_evidence_collect.py`
26. `scripts/category_stability_history.py`
27. `scripts/central_actions_evidence.py`
28. `scripts/central_all_remaining_tasks.py`
29. `scripts/central_archive_consistency.py`
30. `scripts/central_backup_evidence.py`
31. `scripts/central_consolidation_audit.py`
32. `scripts/central_duplicate_test_audit.py`
33. `scripts/central_eight_task_audit.py`
34. `scripts/central_eighteen_task_audit.py`
35. `scripts/central_failure_stage_report.py`
36. `scripts/central_ibo_review_queue.py`
37. `scripts/central_identity_epg_logo_audit.py`
38. `scripts/central_isolated_git_restore.py`
39. `scripts/central_main_playlist_run_evidence.py`
40. `scripts/central_management_summary.py`
41. `scripts/central_open_gaps.py`
42. `scripts/central_protected_write_gate.py`
43. `scripts/central_run_status.py`
44. `scripts/central_short_status.py`
45. `scripts/central_single_screen_report.py`
46. `scripts/central_six_area_audit.py`
47. `scripts/central_source_reconciliation.py`
48. `scripts/central_workflow_inventory.py`
49. `scripts/diagnose_11599_backups.py`
50. `scripts/disaster_recovery_dry_run.py`
51. `scripts/discovery_archive.py`
52. `scripts/discovery_history_restore.py`
53. `scripts/epg_tv_readiness.py`
54. `scripts/evidence_reader.py`
55. `scripts/export_ibo_two_stage_trial.py`
56. `scripts/five_category_92_workflow_audit.py`
57. `scripts/five_category_permission_gate.py`
58. `scripts/five_category_preflight.py`
59. `scripts/five_category_shared_controls.py`
60. `scripts/five_system_cutover_readiness.py`
61. `scripts/five_system_migration_audit.py`
62. `scripts/four_stage_discovery_report.py`
63. `scripts/full_system_backup.py`
64. `scripts/genel_aday_medya_test.py`
65. `scripts/ibo_bagimsiz_test_listesi.py`
66. `scripts/ibo_epg_kimlik_denetimi.py`
67. `scripts/k1_24_rule_evidence.py`
68. `scripts/k1_protected_integrity.py`
69. `scripts/k1_workflow_risk_inventory.py`
70. `scripts/kanal_kararlilik_takip.py`
71. `scripts/keep_turkish_backups.py`
72. `scripts/logo_visual_evidence.py`
73. `scripts/oncelikli_kanal_dogrula.py`
74. `scripts/protected_playlist_audit.py`
75. `scripts/recover_turkish_backups.py`
76. `scripts/repository_settings_inventory.py`
77. `scripts/restore_all_11599_backups.py`
78. `scripts/restore_dry_run.py`
79. `scripts/stage_archive_to_backups.py`
80. `scripts/sync_yedekler_category_count.py`
81. `scripts/test_kanal_adaylari.py`
82. `scripts/vod_guncelle.py`
83. `scripts/wide_source_scan.py`
84. `scripts/yedekler_yeniler_medya_kontrol.py`
85. `scripts/yeniler_aktar.py`
86. `madsc_akilli_kesif.py`
87. `madsc_uc_asama.py`
88. `final_validation.py`
89. `tests/test_channel_name_normalization.py`
90. `tests/test_discovery_m3u_parser.py`
91. `tests/test_evidence_reader.py`
92. `tests/test_five_category_92_workflow_audit.py`
93. `tests/test_five_category_shared_controls.py`
94. `tests/test_five_system_cutover_readiness.py`
95. `tests/test_gelismis_medya_zaman_asimi.py`
96. `tests/test_k1_24_rule_evidence.py`
97. `tests/test_k1_failure_gate.py`
98. `tests/test_k1_legacy_writer_guards.py`
99. `tests/test_k1_runtime_workflow_guard.py`
100. `tests/test_k1_workflow_risk_inventory.py`

**İçerik bulguları ve denetim sınırları:**
- 85 `scripts/*.py` dosyası: 26/92 kabul ve workflow güvenlik envanteri, K1 koruma kapıları, beş kategori entegrasyon raporları, keşif ve aday puanlama, EPG/XMLTV üretimi, logo PNG/kimlik raporları, yedek geri alma ve IBO karar arşivleme, bütünlük/restore, yayın hazırlığı, VOD ve kaynak tarama işlevleri. Kaynakta write_text, write_bytes, dosya yazımı veya push içeren çok sayıda komut bulundu; salt okunur audit ile mutasyon komutları aynı kefeye konulmamalı.
- Özellikle `apply_ibo_*`, `archive_backups_*`, `restore_all_11599_backups.py`, `keep_turkish_backups.py`, `recover_turkish_backups.py`, `stage_archive_to_backups.py`, `sync_yedekler_category_count.py`, `yeniler_aktar.py` kullanıcı onayı olmadan çalıştırılmamalı; YEDEKLER için eski izin geri alınmıştır.
- `build_epg.py` playlist/XMLTV eşleştirme ve kaynak indirme; `automatic_png_logos.py` PNG dönüşümü ve yalnız onaylı onarım mantığı; `five_category_92_workflow_audit.py` eski workflow izin/yazma analizidir, statik denetim canlı eşdeğerlik ispatı değildir.
- `central_protected_write_gate.py`, `k1_protected_integrity.py`, `five_category_permission_gate.py`, `five_system_cutover_readiness.py` koruma/izin ve kesim koşullarını inceler; mevcut kodun varlığı koşuların üretimde gerçekleştiğini kanıtlamaz.
- `madsc_akilli_kesif.py` kaynak araştırma, ayrıştırma, probe, logo ve rapor yazımı; `madsc_uc_asama.py` süreli test; `final_validation.py` öncelikli aday doğrulama ve bekleyenler için işlevler içerir.
- 12 `tests/test_*.py` dosyası kanal adı normalizasyonu, M3U parser, delil okuma, 92 workflow, ortak kontroller, cutover, medya zaman aşımı, K1 kural delili, ardışık başarısızlık devre kesici, eski writer guard, runtime guard ve risk envanteri negatif/pozitif testlerini kapsıyor. Bu turda testler ÇALIŞTIRILMADI, dolayısıyla PASS beyanı yok.
- Önemli: K1 testlerinde ardışık iki başarısızlıkta circuit açma, iptal durumunda seri sıfırlama, API hata durumunda fail-closed; legacy guard testlerinde main-ref ve commit sonrası rebase kontrolleri bulunuyor. Bunlar test beklentileridir, koşu kanıtı değil.
- Toplu incelemede kaynak dosyalarının gerçek içerikleri okundu; ancak ağ yayınlarının canlı oynatma testi ve cihaz IBO onayı yapılmadı.

**Güncel sayım: 324/450 incelendi, kalan 126.** Görseller kapsam dışı (373). Büyük GitHub dosyalarında boş dönenler bu 100'e dahil edilmedi. Ana 810 notu çok büyük olduğundan bu kayıt aynı daldaki bağlantılı ek nottur.
