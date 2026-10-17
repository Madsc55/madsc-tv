# 810 DOSYA NOTU — MADSC TV

Tarih: 18 Ekim 2026. Depo: Madsc55/madsc-tv. Dal: madsc/bes-sistem-toplu-birlestirme. Taslak PR #71 birleştirilmeyecek (yeni açık izin olmadan).

## İnceleme ilerlemesi

Toplam 810 Git blobu. Şu ana kadar 361 dosya ilk tur içerik taramasından geçti (%44,6); 449 dosya kaldı. Kapsam: 98 workflow YAML, 190 Python, önceki oturumlardan 21 belge, bu oturumda 34 ek belge/veri ve diğer önceki içerik incelemeleri. **Sayım farklı dosyalar üzerinden tutulmalı; yeniden okunan dosyalar iki kere sayılmamalı.** İnceleme henüz tam satır-satır güvenlik denetimi değildir; özellikle büyük JSON/M3U/CSV dosyaları ayrıca doğrulanmalı. İnceleme anındaki Git tree: 14862b7cb894b375b51448a621490dd8f9ae1ea7.

## KESİN YAPILMAYACAKLAR

1. Kullanıcının yeni, açık izni olmadan CALISANLAR.m3u, YENILER.m3u, YEDEKLER, HEPSI, FAVORILER, YABANCI_KANALLAR.m3u, kanal URL/isim/ID/logo/kategori/sıralaması, güvenlik kuralları, workflow/cron veya başka dosyalar değiştirilmez. Bu not dosyasının oluşturulması, başka dosyaları değiştirme izni değildir.
2. Eski IBO kararları yeni liste sıra numaralarına otomatik uygulanmaz; geçmişte biten taşıma/silme/ayıklama tekrarlanmaz.
3. Teknik ffprobe/HLS/video+ses başarısı, doğru kanal kimliği, yayın hakkı, İsveç'teki gerçek IBO Player cihazında çalışma veya kullanıcı onayı yerine geçmez.
4. Yeşil GitHub Actions koşusu, bütün kanalların çalıştığı veya 92 eski workflow'un davranışsal eşdeğerliğinin tamamlandığı anlamına gelmez.
5. Eski workflow'lar görev eşdeğerliği, izinler, bağımlılıklar ve zamanlama kanıtlanmadan silinmez/devre dışı bırakılmaz. PR #71 otomatik birleştirilmez.
6. Git HEAD'den geçici geri açma, bağımsız harici yedek/uzun süreli felaket kurtarma kanıtı sayılmaz.
7. Gizli token ve URL parametreleri raporlara açık yazılmaz. Teknik testte DOGRULANAMADI sonucu silme gerekçesi değildir.

## YAPILACAKLAR / ÖNCELİKLER

1. 810 dosyanın tamamını içerik açısından incele; her tur yaklaşık 50 yeni dosya, bulgular ve güncel X/810 sayacı. Özellikle 330 PNG, 40 SVG, 27 M3U, 26 CSV, 51 JSON, 3 XML ve diğer belgelerin kapsamı ayrıca değerlendirilecek.
2. Beş merkezi sistemin (01 güvenlik, 02 keşif, 03 kanal testi, 04 arşiv/yedek, 05 genel bakım) 92 eski işin **gerçek davranışlarını** taşıdığını kanıtla. Yalnız tetik envanteri veya statik isim eşleştirmesi yeterli değil. Girdi/çıktı, cron, izin, artifact, hata davranışı, kullanıcı kararı ve bağımlılıkları karşılaştır.
3. Çok sayıda küçük Actions testi yerine mevcut toplu denetim altyapısını kullan; tek seferde beşli zincir ve iki aşamalı toplu kabul yaklaşımı. Tekrar/çakışan cronları araştır; ör. 1 ve 15'inde 06:40 UTC iki kanal sağlık akışı.
4. Eski workflow'ların contents:write, git push, workflow_run ve diğer dolaylı yazma yollarını korunan dosya kapısından geçir; geçmiş IBO kararlarını uygulayan scriptler, arşiv/restore ve YEDEKLER'e ekleme scriptleri otomatik çalıştırılmamalı.
5. Aday testlerinde üç aşama, beş dakikalık süreklilik, geçmiş ölçüm zamanı, 7/30 gün kararlılık, kimlik/EPG/logo ve IBO/kullanıcı onayını ayrı kanıt alanlarıyla göster. Eski birleşik aday raporu yeni test geçmişiyle uyumlu mu denetle.
6. Keşif geçmişi ve başarısız testleri koru; günlük/haftalık/aylık kaynak kapsamları beşli sistemde kaybolmasın; adaylar adı ve normalize URL ile tekrarsız raporlansın. İsveç IBO cihaz onayı ayrı beklesin.
7. EPG ve GitHub Pages yayın zincirini gerçek yayın içeriğiyle kontrol et: GITHUB_TOKEN ile push edilen değişiklikler beklenen workflow_run'ı tetiklemeyebilir. 14 Ekim EPG raporunda 1.039 kayıt, 730 eşleşen, 309 eşleşmeyen; bunlar güncel cihaz doğrulaması değil. Beş kanal pilotu ayrıca cihazda kontrol gerektirir.
8. Tam sistem yedeği, SHA256 manifest, izole geri yükleme, bağımsız dış kopya ve saklama süresini ayrı ayrı doğrula; 400 MB arşiv sınırını göz önünde bulundur.
9. Raporlarda kanıt kaynağı/run_id/commit/tarih ve artifact provenance kontrolü yap; eski rapor yeni koşu gibi görünmesin. Tek merkez ekranında tamamlanmayan işler ve onaylar açık kalsın.
10. URL'lerde kimlik bilgisi maskeleme, yazma kapısı, hata tekrarı durdurma ve başarısız koşu bildirimleri korunmalı.

## İNCELEMEDE GÖRÜLEN ÖZEL RİSKLER

- scripts/apply_ibo_*.py, scripts/archive_backups_*.py, scripts/restore_all_11599_backups.py, scripts/keep_turkish_backups.py, scripts/stage_archive_to_backups.py, scripts/recover_turkish_backups.py: tarihsel kullanıcı kararları / doğrudan liste değişikliği; çalıştırma yok.
- tools/yedekler_guvenli_ekle.py ve tools/son_kontrol_yedekler_aktar.py: teknik adayları YEDEKLER'e yazabilen yollar; onaysız çalıştırma yok.
- scripts/five_category_92_workflow_audit.py, scripts/central_consolidation_audit.py, test_five_category_92_workflow_audit.py: kapsam ve kabul testleri var ama gerçek davranışsal eşdeğerlik ayrıca kanıtlanmalı.
- scripts/category_evidence_collect.py ve test_five_category_evidence_transfer.py: farklı çalışmalardan gelen kanıtların köken doğrulaması önemli.
- scripts/central_isolated_git_restore.py: yalnız HEAD ile eşleşme; harici yedek değil.
- scripts/build_epg.py, epg/report.json, epg/ibo-test-epg.xml, epg_deneme/: XMLTV eşleşme ve IBO pilotu.
- tools/protected_write_gate.py, scripts/k1_workflow_risk_inventory.py, tests/test_k1_legacy_writer_guards.py: korunan yazma güvenliği.
- scripts/discovery_history_restore.py, scripts/category_stability_history.py, tools/genis_kaynak_taramasi.py: tarama ve kararlılık geçmişi.
- scripts/central_workflow_inventory.py: cron ve concurrency çakışmaları.

## Tarihsel veriler — güncel başarı diye gösterme

- 12 Ekim üç aşamalı snapshot: 3/3=5.750, 2/3=439, 1/3=109, 0/3=138, pending=293. Eski snapshot, canlı sonuç değil.
- 14 Ekim epg/report.json: playlist_entries=1.039, matched=730, unmatched=309, usable=583, programmes=23.702. Eski rapor.
- IBO Player ve TCL televizyon testinin son kararı kullanıcıdadır. Eurostar'ın önceki IBO başarısızlık kararı korunmalı.

## Sonraki tur

Henüz incelenmeyen dosyalara devam et; önceden okunan dosyaları sayma. Her yeni bulguyu YAPILACAK / YAPILMAYACAK / DOĞRULAMA BEKLEYEN olarak sınıflandır. İnceleme bulgularını bu dosyaya eklemek için ayrıca kullanıcı onayı alınması gerekip gerekmediğini kontrol et; bu dosyanın oluşturulmasıyla verilmiş izin kapsamını aşma.

## YENİ SOHBETE DEVİR — 18 Ekim 2026

- Kullanıcı sohbet değiştirmek istiyor. Yeni sohbet açıldığında önce bu dosyayı, AGENTS.md ve DEVAM_NOTU.md içindeki en güncel devir bölümünü oku; incelemeye kaldığı yerden devam et.
- Son kullanıcıya bildirilen sayaç: **361/810 incelendi, 449 kaldı**. Bu sayı önceki turlarda farklı dosya tekrarlarının sayılmış olabileceği için, yeni turda ağaçtaki benzersiz yollarla uzlaştırılmalı; yanlışsa açıkça düzelt. 190 Python ve 98 workflow ilk turda tarandı. Büyük dosyalar için tam satır-satır denetim yapıldığı iddia edilmesin.
- Son turda 34 belge/veri dosyası okundu; sıradaki tur `.json`, `.md`, `.txt`, `.xml` listesinin 34. indeksinden başlayacak şekilde planlandı, ancak bu son tur araç çağrısının sonucu alınmadan sohbet devrine geçildi. Bu 17 dosya **incelenmiş sayılmamalı**; yeniden fetch et.
- İlk 810 dosyalık ağaç SHA: `14862b7cb894b375b51448a621490dd8f9ae1ea7`. Not dosyasının eklenmesiyle dalın güncel toplam dosya sayısı 811 olabilir; ilerleme için özgün 810 dosyalık envanter baz alınır, yeni not dosyası kapsam dışında tutulur.
- Her tur yaklaşık 50 yeni dosyayı denetle; bulguları YAPILACAK, YAPILMAYACAK, BEKLEYEN KANIT şeklinde ayır. Bu notu güncellerken yalnızca bu dosyaya yaz; ana liste ve diğer dosyalara dokunma. Kullanıcıya kısa ve net rapor ver.
- Kullanıcının kısa devam komutu **D** olarak kararlaştırılmıştır.
