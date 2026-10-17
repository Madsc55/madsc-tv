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

## 18 Ekim 2026 — yeni sohbet, 17 JSON doğrulama turu

- Bu turda 17 JSON kaynak GitHub'dan yeniden okundu: arastirma/bes_site_katalog_2026-10-12.json; arastirma/lyngsat_arama_oncelikleri.json; arastirma/uydu_arama_oncelikleri.json; aday_hazirlik/ibo_alternatif_10_2026-10-12.json; epg_deneme/yayim_kontrol.json; logo_deneme/png_automation.json; madsc_kesif/candidate_logo_missing_report.json; vod/guncel-bolumler.json; liste_kontrol/rapor.json; raporlar/YEDEK_KATEGORI_LOGO_2026-10-12.json; madsc_kesif/DORT_ASAMA_TEK_RAPOR.json; madsc_dogrulama/summary.json; madsc_son_kontrol/summary.json; madsc_kesif/ibo_3_5281_rapor.json; madsc_kesif/ibo_6115_ikinci_rapor.json; madsc_kesif/ibo_530_399_sonrasi_rapor.json; logo_deneme/ozet.json.
- Bu dosyalar önceki kayıtların da kapsamındadır; **benzersiz yeni dosya sayısı kanıtlanmadığı için sayaç 361/810 (449 kalan) olarak korunuyor**. Son devirdeki yarım kalmış 17 dosyanın birebir aynı 17 yol olduğu kanıtlanmadı. Bir sonraki turda özgün tree üzerinden yol bazlı inceleme matrisi oluşturulmalı; çift sayım yapılmamalı.
- **YAPILACAK:** 75 adayın logo raporu: 13 indirme/dönüştürme hatası, 28 kaynak güvenlik incelemesi, 7 PNG hazırlığı, 27 PNG hazır ama kimlik onayı bekliyor. 7100 üç aşama tamamlanmış (6374 teknik 3/3), hazır liste adayı 0. Son kontrol raporunda 3800 tamamlanan ve 2574 kalan, listeye hazır 0. Bunlar 14 Ekim tarihli snapshot, canlı başarı değil. Kaynak/kimlik/IBO onaylarını ayır.
- **KANIT BEKLEYEN:** EPG Pages 11 Ekim başarılı tek yayın, günlük takip CONFIGURED_NOT_YET_OBSERVED; IBO NOT_VERIFIED. VOD bölüm takvimi oynatma bağlantısı değil. Keşif katalog adları yayın URL'si veya kimlik kanıtı değil. 92 eski workflow davranışsal eşdeğerliği halen açık.
- **YAPILMAYACAK:** Eski IBO 3-5281 / 6115 / 530 sıra kararlarını güncel YEDEKLER'e yeniden uygulama. 10 alternatif aday raporu SUPERSEDED_AFTER_IMAGE_IDENTITY_REVIEW, otomatik hazır sayma. Tarihsel FTV TÜRK / Red Bull TV kimlik uyumsuzluğuna bakmadan düzeltme/taşıma yapma. Korunan playlistler, workflow'lar, güvenlik ve PR #71 değişmedi.
- Bu tur salt okunur inceleme yaptı; yalnız bu not dosyasına inceleme kaydı ekleniyor. Sonraki iş: özgün 810 tree dosya yolları ile 361 sayacını uzlaştırıp gerçek yeni dosyalardan yaklaşık 50'lik tur.

## 18 Ekim 2026 — 10 belge yeniden kontrolü

- Salt okunur doğrulanan dosyalar: docs/MADSC-IKI-TOPLU-KABUL-PLANI.md; docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md; BES_SISTEM_TOPLU_IS_DEFTERI.md; BES_SISTEM_GECIS_KONTROL.md; GUVENLIK_KURALLARI.md; OZELLIK_ENVANTERI.md; kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md; kontrol_notlari/2026-10-12_ekol_basa_sarma.md; kontrol_notlari/DEVAM_GECMISI_2026-10-12_1947.md; MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md.
- Bu kaynaklar önceki incelemelerde zaten anılıyor; **yeni benzersiz dosya olarak sayılmadı**. Sayaç halen 361/810; 449 kalanın kesin listesi için özgün tree ile okunan-yol matrisi gerekiyor.
- YAPILACAK: 92 eski workflow'un davranışsal eşdeğerliğini girdi/çıktı/tetik/izin/artifact ile kanıtla; 26 güvenlik kuralı uçtan uca doğrulama; iki aşamalı toplu kabul; Ekol TV/Sports durgun HLS parça ilerleme testi; Eurostar resmî/uygun alternatif araştırması; harici yedek ve IBO kanıtını ayrı tut.
- YAPILMAYACAK: geçmiş Eurostar silme kararını tekrar uygulama; Ekol URL'lerini sırf HTTP 200 gördü diye sağlam sayma; eski 3082 kalan aday snapshot'ını güncel sayı olarak gösterme; kullanıcı izni olmadan playlist/YEDEKLER/workflow değişikliği, PR #71 merge yapma.
- KANIT BEKLEYEN: 14 Ekim 5/5 CI teknik zinciri, 92/92 parity veya canlı IBO kabulü anlamına gelmez. Özgün 810 envanterinin eksik yol listesi halen elde edilmedi. Bu tur kaynak kodunu değiştirmedi.

## 18 Ekim 2026 — özgün tree ile GERÇEK dosya içeriği incelemesi (28 dosya)

- Özgün tree SHA 14862b7cb894b375b51448a621490dd8f9ae1ea7 GitHub Git Trees API'den yeniden alındı: truncated=false, **810 blob**. Bu ilk defa somut 810 yol listesine erişim sağlar. Not içinde dosya yolu geçmemesi, dosyanın geçmişte hiç okunmadığını kanıtlamaz; bu nedenle 361/810 sayacına 28 otomatik eklenmedi. Benzersiz ilerleme için yol bazlı matris şart.
- Bu tur **içeriği okunmuş 28 dosya** (önceki notta tam yol olarak listelenmeyenlerden): .github/commands/aday-yedekleme.txt; .github/commands/genel-guncelleme.txt; BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md; CALISMAYANLAR.txt; DEVIR_NOTU_2026-10-15.md; IPTV_PROJE_HAFIZASI.md; MERKEZI_ARSIV_HARITASI.md; ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md; SEKIZ_GOREV_TOPLU_DENETIM.md; TOPLU_DURUM_RAPORU.md; docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md; docs/MADSC-92-WORKFLOW-ESDEGERLIK-KONTROL-2026-10-14.md; epg_deneme/README.md; epg_deneme/rapor.json; final_validation_manifest.json; liste_kontrol/README.md; logo_deneme/HAZIRLIK_NOTLARI.md; logo_deneme/README.md; logo_deneme/approved_repairs.json; logo_deneme/candidates/sources.json; logo_deneme/rapor.json; logo_deneme/verified_sources.json; logo_deneme/visual_review.json; madsc_kesif/NOT_EKSIK_TURK_KANALLARI.md; madsc_kesif/ibo_354_iki_kategori_rapor.json; madsc_kesif/ibo_364_355_364_rapor.json; madsc_kesif/ibo_398_16_49_rapor.json; madsc_kesif/ibo_ilk_239_ayirma_raporu.json.
- **İçerik elde edilemeyen, sayılmayan 2 dosya:** aday_bekletme/gecmis.json ve aday_hazirlik/uc_asama_2026-10-12_1037.json; fetch_file içerik uzunluğu 0 döndü. Daha küçük aralık veya Git blob SHA ile yeniden dene.
- **YAPILACAK:** BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md 92 eski workflow için 9 cron + EPG Pages workflow_run zincirini ayırıyor; 92/92 gerçek davranış eşdeğerliği kanıtı değil. EPG deneme raporunda gece yarısı taşması için tahmini program bitişi var; program çizelgesi bağımsız doğrulanmalı. Logo visual_review 9 kanalın frame'ini hazır tutuyor fakat 9/9 visual_match NOT_VERIFIED. logo_deneme/verified_sources.json boş nesne; otomatik logo kimliği onaylanamaz. CALISMAYANLAR.txt statik ad listesi; bugünkü IBO testi yerine geçmez.
- **KANIT BEKLEYEN:** logo_deneme/rapor.json 1039 girişli 12 Ekim snapshot; 32 sorunlu kayıt, teknik görüntü decode IBO veya doğru logo kanıtı değil. final_validation_manifest.json ilk 300 saniyelik öncelik partisi, tüm 6436 aday değil. EPG Pages'in günlük üretimden otomatik tetik zinciri eski hazırlık notunda GITHUB_TOKEN push kısıtı nedeniyle şüpheli; güncel workflow ve gerçek run ile teyit et.
- **YAPILMAYACAK:** Eski IBO 398→364→354→2 ayırma kayıtlarını bugünkü yedeklere yeniden uygulama. 354 raporundaki 332 'çalışmıyor' kullanıcı bildirimi teknik olarak yeniden test edilmiş sayılmaz. 364 raporundaki 10 ve 398 raporundaki 34 yabancı ayrımı da bugünkü liste için yeniden yazma izni değildir. Eski 89 workflow planı güncel 92'lik envanterin yerine geçmez. Mevcut playlistler, workflow'lar, PR #71 değişmedi.
- **Sonraki gerçek dosya grubu:** 810 tree içindeki önceki notta tam yol olarak geçmeyen kalan CSV/JSON/XML/MD dosyalarını içerik okuyarak sırayla işle; büyük dosyalar için satır aralığı/bloba göre parça okuma yap. 361 sayacını ancak tüm geçmiş okunan yol listesi uzlaştırılınca güncelle.

## 18 Ekim 2026 — doğrudan Python KODU inceleme, 20 dosya

- GitHub branch üzerinden **gerçek Python kaynak içeriği** okunup fonksiyon/IO/yan etki ve risk satırları incelendi: aday_bekletme.py; aday_hata_siniflandirma.py; aday_oncelik_raporu.py; aday_tekrar_raporu.py; akilli_tekrar_test_takvimi.py; altinci_aday_tekrar_test.py; arastirma/uydu_karsilastir.py; channel_name_normalization.py; discovery_m3u_parser.py; epg_deneme/build.py; final_validation.py; gelismis_medya_testi.py; genis_kanal_tara.py; iptv_test.py; kaynak_degisiklik_raporu.py; kaynak_guven_puani.py; kaynak_kesfet.py; liste_kontrol/build.py; logo_deneme/audit.py; madsc_akilli_kesif.py.
- **KRİTİK RİSK:** iptv_test.py doğrudan `Path('CALISANLAR.m3u').write_text(...)` içeriyor; açıklama satırları koruma dese de çalıştırmak ana listeyi yazabilir. Salt okunur diye güvenip yürütme. Yetki ve izole test olmadan çalıştırma.
- **YAPILACAK:** aday_bekletme.py geçmiş JSON ve durum CSV'sini yazar; salt okunur ifadesi yalnız ana liste için geçerlidir. altinci_aday_tekrar_test.py AST ile yeni_kanal_tara.py yardımcılarını çıkarıp çalıştırıyor; dinamik kod yürütme, bakım ve hata yayılımı açısından manuel güvenlik incelemesi gerektirir. madsc_akilli_kesif.py 155 kaynak hedefi ve tarama/ffprobe yanında madsc_kesif klasörüne çıktılar yazar; üretim etkisi ve yan etkiler ayrılmalı.
- **KANIT BEKLEYEN:** epg_deneme/build.py beş kanallık deneme rehberi/liste/rapor dosyalarını yazar; üretim ana listeye yazma kodu görünmedi, ama EPG bitiş zamanını otomatik düzeltme ve ağ kaynak güvenilirliği ayrıca doğrulanmalı. final_validation.py ffprobe/ffmpeg/thumbnail çalıştırıyor; 300 saniyelik testin tüm adaylara uygulanmış olduğu iddia edilmez. kaynak_kesfet.py GitHub token'ı ağ isteklerine koyuyor; log/çıktı ve yetki sınırı ayrıca incelenmeli.
- **YAPILMAYACAK:** salt okunur etiketini mutlak dosya yazmıyor anlamında kullanma; çıktı raporu yazan betikleri üretimde izinsiz koşturma; başarısız ffprobe sonucunu kullanıcı IBO kararı sayma; ana playlisti değiştiren iptv_test.py'yi çalıştırma.
- Sayaç **361/810** korunuyor; eski 190 Python'un ilk turda okunduğu bildirildiği için bu 20 dosyayı yeni benzersiz dosya olarak saymak yanıltıcı. Bu tur önceki özetlerden değil **kaynak kodundan** gerçek risk denetimidir. Kaynak kodu değiştirilmedi.

## 18 Ekim 2026 — 30 veri dosyasına doğrudan erişim, gerçek kalan envanter taraması

- Özgün 810 tree'de uzantılar: 190 py, 98 yml, 35 md, 27 m3u, 26 csv, 51 json, 3 xml, 7 txt, 330 png, 40 svg, 1 webp, 2 jpg. Önceki 361 sayımı 190 Python ve 98 workflow'u zaten kapsadığından **kalan iş ağırlıklı olarak veri/playlist/görsel varlıklar**; tekrar Python taramasını yeni ilerleme diye sayma.
- Bu tur **30 CSV/JSON yoluna** doğrudan fetch_file erişildi; **26'sı içerik döndürdü, 4'ü sıfır uzunluk döndü** (aday_bekletme/ADAY_ONCELIK_RAPORU.csv, madsc_kesif/bulunan_kanal_arsivi.csv, madsc_kesif/yedek_ulke_inceleme.csv, madsc_kesif/gecmis.json, madsc_dogrulama/state.json, madsc_son_kontrol/results.json — toplam 6 boş yanıt; dolayısıyla 24 içerikli/6 boş). Boş yanıtlar inceleme tamamlandı diye sayılmadı; blob SHA ile yeniden dene.
- **İçeriği görülen dosyalar:** aday_bekletme/ADAY_DURUM_RAPORU.csv; aday_bekletme/GELISMIS_MEDYA_TESTI.csv; aday_bekletme/KAYNAK_GUVEN_PUANLARI.csv; aday_bekletme/TEKRAR_EDEN_ADAYLAR.csv; madsc_kesif/adaylar.csv; madsc_kesif/alternatifler.csv; madsc_kesif/ana_liste_calismayanlar.csv; madsc_kesif/ana_liste_saglik_raporu.csv; madsc_kesif/arastirma_kaynaklari.csv; madsc_kesif/eski_bozuk_linkler.csv; madsc_kesif/ibo_3_5281_kararlar.csv; madsc_kesif/ibo_6115_ikinci_kararlar.csv; madsc_kesif/ibo_kullanici_kararlari.csv; madsc_kesif/kaynak_erisim_raporu.csv; madsc_kesif/kaynak_guncelligi.csv; madsc_kesif/player_uyumlulugu_belirsiz.csv; madsc_kesif/tekrarlar.csv; madsc_kesif/yuksek_kalite_alternatifleri.csv; madsc_kesif/ana_liste_test_gecmisi.json; madsc_kesif/candidate_logos.json; madsc_kesif/logo_candidates.json; madsc_kesif/ozet.json; madsc_son_kontrol/kimlik_incelemesi_2026-10-12.json; madsc_son_kontrol/kimlik_devam_2026-10-12_1955.json.
- **YAPILACAK:** 2668 satırlık aday durum CSV'sinde #EXTINF meta metninin KANAL alanına sızması örneği var; M3U parser veri kalitesi incelemesi. 19 satırlık kaynak güven CSV'sinde örneklerin 0 test kapsamına rağmen 50 puan alması 'VERI_YETERSIZ' etiketiyle korunmalı; güvenilir kaynak sanma. ana_liste_calismayanlar.csv 23 fiziksel satır, bazıları aynı kanalı farklı kategorilerde tekrar eder; kanal sayısı olarak raporlama. 11 Ekim/14 Ekim kaynak erişim ve güncellik snapshot'larını canlı kaynak doğrulaması sayma. Çok satırlı tırnaklı CSV'de fiziksel satır sayısı gerçek kayıt sayısı değildir (ibo_6115_ikinci_kararlar.csv örneği).
- **KANIT BEKLEYEN:** madsc_son_kontrol/kimlik_devam_2026-10-12_1955.json 39 kaydın 35 görüntüsünü incelemiş, playlist'e hazır 0; cihaz onayı yok. madsc_kesif/candidate_logos.json görsel eşleşme NOT_VERIFIED ve playlist_approved=false. madsc_kesif/ana_liste_test_gecmisi.json tarihsel teknik başarı, güncel IBO değildir. GELISMIS_MEDYA_TESTI.csv örneği VIDEO/SES BELIRSIZ ve DOGRULANAMADI.
- **YAPILMAYACAK:** 5281 ve 6115 eski IBO pozisyon CSV'lerinden güncel playlist/YEDEKLER üzerinde yeniden ayırma, yazma, silme yapma; teknik sonuç ile kullanıcı IBO kararı karıştırma. İnceleme sadece okuma, hiçbir kaynak betiği çalıştırılmadı.
- Bu 24 içerikli dosyanın önceki 361 içinde bulunup bulunmadığı tek tek doğrulanamadığı için ana sayaç 361/810 tutuldu; **bu tur yeni kaynak verilerinin içeriği gerçekten okundu**.

## 18 Ekim 2026 — 20 gerçek M3U/TXT dosyası içerik kontrolü

- İçerikleri doğrudan okunan 20 dosya: aday_hazirlik/ibo_alternatif_10_2026-10-12.m3u; aday_hazirlik/ibo_kimlik_destekli_2026-10-12.m3u; epg_deneme/liste.m3u; madsc_kesif/ibo_354_335_354_yabanci_arsiv.m3u; madsc_kesif/ibo_354_3_334_turk_calismaz_arsiv.m3u; madsc_kesif/ibo_364_355_364_yabanci_arsiv.m3u; madsc_kesif/ibo_398_16_49_yabanci_arsiv.m3u; madsc_kesif/ibo_530_399_sonrasi_yabanci_arsiv.m3u; tarama/iptv-org-tr-adaylar-2026-10-10.m3u; vod/TEST-FILMLER.m3u; yedekler/IBO_BAGIMSIZ_TEST_ADAYLARI_2026-10-10.m3u; yedekler/IBO_ESKI_CALISMAYANLAR_2026-10-09.m3u; yedekler/IBO_TEKNIK_TEST_GECMEYENLER_2026-10-09.m3u; yedekler/IBO_TUM_KONTROL_ADAYLARI_2026-10-09.m3u; yedekler/TARAMA-TEST-SONUCLARI.m3u; yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u; yedekler/TV5_ADAY_2026-10-09.m3u; yedekler/YENILER-SILINEN-TEST-ADAYLARI-2026-10-10.m3u; yedekler/ADAY_KANALLAR_2026-10-09.txt; yedekler/IBO_YEDEK_EKSIK_KANALLAR_2026-10-09.txt.
- Kayıt sayıları (M3U EXTINF): 3,3,5,20,332,10,34,132,149,1,5,82,295,306,86,390,1,77; ADAY_KANALLAR.txt içinde 18 EXTINF, IBO_YEDEK_EKSIK_KANALLAR.txt 52 fiziksel satır. Her M3U dosyasında EXTINF satırları görüldü ve URL satırı olmayan beklenmedik düz satır sayısı sıfır çıktı (bu yalnız yapısal ön kontroldür, URL oynatma testi değildir).
- **YAPILACAK:** aynı SHA'lı iki IBO 3-kanal dosyasını tek tarihsel karar olarak izle; önceki superseded/reddedilmiş ADA/KANAL D kararları korunmalı. 332 kayıt 'kullanıcı bildirimi çalışmıyor' teknik testten ayrı; 295 'teknik test geçmeyen' de IBO kararı değil. 306 IBO toplu kontrol, 390 tüm teknik aday, 86 tarama sonuç ve 149 tarihsel kaynak aday dosyaları canlı yayın olarak onaylanmış değildir. Eski yabancı arşivler 20+10+34+132 kayıt içeriyor, farklı tarihsel kesitlerdir ve bugünkü YEDEKLER durumu değildir.
- **KANIT BEKLEYEN:** epg_deneme/liste.m3u beş TRT kanalına ait ayrı EPG pilotu, cihazda gözlenmiş kabul değil. vod/TEST-FILMLER.m3u 1 adet kısa test klibi, tam VOD kütüphanesi değil. yedekler/IBO_YEDEK_EKSIK_KANALLAR_2026-10-09.txt ad eşleşmeyenler listesi; güncel eksik kanal kanıtı değil.
- **YAPILMAYACAK:** eski arşiv kayıtlarını bugünkü ana listeye/YEDEKLER'e otomatik taşıma; kullanıcı izni olmadan hiçbir playlisti düzenleme. Dosyalar okunmuş, oynatma veya betik çalıştırılmamıştır.
- Benzersiz sayaç 361/810 sabit; 361 eski yol listesi olmadığı için 20 dosyayı yeni benzersiz saymak kanıtsız olur. Kalanlar arasında görsel PNG/SVG varlıklar ağırlıkta; bunlar da içerik ve tür doğrulaması gerektirir.

## 18 EKİM — 50 DOSYA GERÇEK İÇERİK TARAMASI

İlk 810 dosyalık ağaçtaki JSON/MD/TXT/XML sıralamasında 34–83 indeksleri arasında **50 ayrı dosyanın blob içeriği GitHub'dan getirildi ve alanları/başlıkları kontrol edildi**. Bu, çok büyük JSON kayıtlarının her satırının elle incelendiği anlamına gelmez. Önceki 361/810 sayacı doğru ve benzersiz kabul edilirse yeni sayı **411/810, kalan 399**; ancak önceki 361 sayacında yeniden okunan belgeler olabileceğinden toplamın benzersiz yol listesiyle uzlaştırılması gerekir.

### YAPILACAK
- `madsc_dogrulama/summary.json`: 14 Ekim tarihli 7.100 adaydan 6.374'ü üç teknik decode başarısı almış; cihaz/kimlik onayı ayrı tutulmalı. `madsc_son_kontrol/results.json` (4,8 MB) ve `madsc_dogrulama/state.json` (5,9 MB) gibi büyük kayıtlar örnek değil kapsamlı otomatik tutarlılık kontrolü gerektirir.
- `logo_deneme/visual_review.json`: `FRAME_READY_FOR_REVIEW` durumunu `visual_match=NOT_VERIFIED` ile ayır; `logo_deneme/approved_repairs.json` eski izinleri yeni otomatik onay sanma.
- `madsc_kesif/DORT_ASAMA_TEK_RAPOR.json`: bağımsız dış yedek ve geri yükleme kanıtı eksik. `madsc_kesif/yedek_11599_geri_yukleme_raporu.json` geçmişte 11.557 kaydın geri alındığını belgeliyor; bağımsız kurtarma testi değildir.
- `kontrol_notlari/2026-10-12_ekol_basa_sarma.md`: Ekol Sports/TV yayınının başa sarma sorunu, yalnız ilk bağlantı başarısıyla anlaşılmaz; süreklilik kontrolünde ayrıca ele alınmalı.
- `madsc_kesif/candidate_logo_missing_report.json`: 75 adayda logo kaynağı, PNG hazırlığı ve kimlik onayı kategorileri var; ayrı güvenlik/kimlik incelemesi gerekir.
- `madsc_kesif/candidate_epg_logo_join.json`: 5 kanallı EPG pilotu tam üretim kapsamı değildir.
- `madsc_kesif/ana_liste_test_gecmisi.json` ve `madsc_kesif/gecmis.json`: tarihsel testler korunmalı; yeni çalışmanın sonucuyla karıştırılmamalı.
- `madsc_son_kontrol/kimlik_incelemesi_2026-10-12.json`: 36 görsel örnek incelenmiş, 3 adayda görüntü yok; bu durum IBO cihaz onayı yerine geçmez.

### YAPILMAYACAK
- `madsc_kesif/ibo_*_rapor.json` ve `reports/ibo-user-decisions-2026-10-13-session2.md` içindeki **eski liste sıralaması esaslı** IBO kararlarını güncel listeye yeniden uygulama.
- 12–14 Ekim tarihli raporları bugünün canlı yayın/cihaz sonucu gibi sunma; teknik geçişi kullanıcı onayı olarak gösterme.
- Korunan listelere, kanal isimlerine, logolara, yedeklere ve workflow'lara onaysız yazma.

### DEVAM

Özgün ağaçtaki JSON/MD/TXT/XML sıralamasında 84. indexten devam et. Görsel, M3U ve CSV dosyalarının içeriğini de gerçekten kontrol et; yalnız dosya adlarını listelemekle yetinme. Büyük dosyalar için örnekleme yapıldığını açıkça belirt, doğrulanmadığı halde tüm satırları incelendi deme.
