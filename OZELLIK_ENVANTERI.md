# MADSC-TV — Özellik Envanteri ve Tekrar Önleme Kapısı
Güncelleme: 13 Ekim 2026. **Bu dosya bir özellik icat etmez; mevcut kod/iş akışı kanıtlarını gösterir.** Başarı durumu her zaman son Actions koşusu ile doğrulanır.

| İşlev | Mevcut uygulama | Kapsam ve sınır |
|---|---|---|
| Günde iki kez kanal keşfi | `.github/workflows/madsc-birlesik-kesif.yml`, `madsc_akilli_kesif.py` | UTC 06:00, 18:00; aday tarama ve yayın testleri |
| Aday logo PNG hazırlığı | `scripts/candidate_logo_report.py`, `scripts/automatic_png_logos.py` | Hazırlık görsel kanal kimliğini kanıtlamaz |
| Aday logo + EPG birleşik raporu | `scripts/candidate_epg_logo_join.py`, birleşik keşif workflow | Bağımsız test #38321948143 SUCCESS; tam günlük keşif koşusu henüz doğrulanmadı; beş kanallık pilot EPG ile sınırlı |
| Tam ana liste EPG üretimi | `scripts/build_epg.py`, `.github/workflows/epg-gunluk.yml` | Her gün UTC 03:25; son bilinen rapor: 1039 giriş, 728 eşleşme, 17811 program; bu IBO cihazında görüntülendiği anlamına gelmez |
| EPG Pages yayını | `.github/workflows/epg-pages.yml` | XMLTV yayımlar ve yayımlanan içeriği doğrular |
| IBO 5 kanallı EPG pilotu | `scripts/build_ibo_epg_test.py`, `epg/ibo-test-epg.xml` | Sadece cihaz uyumluluk denemesi; üretim EPG'siyle karıştırma |
| Günde iki kez IBO EPG kimlik denetimi | `scripts/ibo_epg_kimlik_denetimi.py`, `.github/workflows/ibo-epg-kimlik-denetimi.yml` | UTC 06:23, 18:23; pilot karşılaştırması; run #38321599549 SUCCESS |
| Logo/EPG kalite uyarıları | `tools/logo_epg_audit.py`, `.github/workflows/test-15-logo-epg.yml` | Eksik logo/kimlik ve şüpheli URL uyarıları |
| Aday son kontrol | `.github/workflows/madsc-son-kontrol.yml` | Teknik başarı ile cihaz/kanal kimlik onayı ayrıdır |
| Ayda iki kez merkezi otomasyon denetimi | `.github/workflows/madsc-aylik-merkezi-denetim.yml`, `scripts/central_workflow_inventory.py`, `test_central_workflow_inventory.py` | 1/15 UTC 07:00; cron, concurrency, izin, kategori ve risk raporları; kod değişince main push testi. Salt okunur; tam orkestrasyon değildir, gerçek Actions sonucu ayrıca gerekir. |
| Altı konu tek merkezi rapor | `scripts/central_six_area_audit.py`, `.github/workflows/madsc-aylik-merkezi-denetim.yml` | Tek Actions koşusunda altı alanın salt okunur kanıt ve eksiklerini toplar; sorunları otomatik çözmez, IBO cihaz testi değildir. |
| Sekiz görev tek merkezi rapor | `scripts/central_eight_task_audit.py`, `test_central_eight_task_audit.py`, merkezi workflow | Sekiz işin kanıtını ve açık eksiklerini tek koşuda raporlar; henüz eksikleri otomatik çözmez. |
| Korunan listeler | `AGENTS.md`, `GUVENLIK_KURALLARI.md` | Ana liste, YENİLER, HEPSİ, favoriler, yedekler izinsiz değişmez |

## Her yeni işten ÖNCE zorunlu karar
1. `AGENTS.md`, `DEVAM_NOTU.md` ve bu envanteri oku.
2. İlgili script, workflow ve son Actions run'unu kontrol et; yalnız dosya varlığına bakarak **çalışıyor** deme.
3. **VAR + TEST BAŞARILI:** yeniden yazma; sıradaki eksik işe geç.
4. **VAR + EKSİK/ARIZALI:** mevcut sistemin sadece eksik bölümünü düzelt; eski başarılı işlevi ve veriyi koru.
5. **YOK:** önce mevcut araçlarla aynı işin yapılıp yapılmadığını ara; ancak gerçekten yoksa bağımsız, geri alınabilir geliştirme yap.
6. **CİHAZDA DOĞRULANMADI:** GitHub testini IBO Player gerçek yayın/EPG/kimlik onayı gibi sunma.
7. Her geliştirmeden sonra gerçek GitHub run ID, sonuç, değişen dosyalar ve kalan sınırlamaları `DEVAM_NOTU.md`ye kaydet. Başarısız/çalışan geçmişi silme.
8. Otomatik keşif ve raporlar kullanıcı onayı yerine geçmez; ana liste, YENİLER, logo ve yedekleri değiştirme.

## Önemli
Bu envanter **tekrar önleme kayıt kapısıdır**, tek başına tüm gelecekteki kod değişikliklerini teknik olarak bloke eden bir güvenlik mekanizması değildir. Değişiklik öncesi kontrol ve Actions kanıtı zorunlu çalışma prosedürüdür.

- **Merkezi logo/EPG/kimlik/geçmiş kanıt raporu:** `scripts/central_identity_epg_logo_audit.py` ve `test_central_identity_epg_logo_audit.py`; mevcut merkezi Actions testine bağlıdır. IBO cihaz onayı vermez, korunan listeleri değiştirmez.

- **Tek merkezi yönetim özeti:** `scripts/central_management_summary.py`, `test_central_management_summary.py`; yedi mevcut kanıt raporunu tek JSON içinde birleştirir, eksikleri açık gösterir. Canlı panel veya IBO onayı değildir.

- **Kısa durum özeti:** `scripts/central_short_status.py`, `test_central_short_status.py`; merkezi Actions artifact içinde `madsc_kisa_durum_ozeti.md` üretir. Günlük cron eklenmemiştir; mevcut zamanlama korunur.

- **Açık işler ve eksik kanıtlar:** `scripts/central_open_gaps.py`, `test_central_open_gaps.py`; merkezi Actions artifact içinde `acik_isler_ve_eksik_kanitlar.json` üretir. Rapor bulunması işi bitmiş saymaz.

- **Kalan sekiz iş tek koşu karar tablosu:** `scripts/central_all_remaining_tasks.py` ve `test_central_all_remaining_tasks.py`, `kalan_isler_tek_kosu_karar_tablosu.json`. Kanıt, eksik ve dış bağımlılıkları birlikte gösterir; tamamlanma sertifikası değildir.

- **İzole Git HEAD geri yükleme doğrulaması:** `scripts/central_isolated_git_restore.py` ve `test_central_isolated_git_restore.py`; üç korunan dosyanın Git HEAD sürümünü geçici dizinde geri açar, SHA256 ile doğrular. Harici veya tarihsel yedek kurtarma kanıtı değildir.

- **IBO aday inceleme kuyruğu:** `scripts/central_ibo_review_queue.py`, `test_central_ibo_review_queue.py`; aday kanıtı varsa tekrarsız CSV üretir, IBO onayı ve liste aktarımı yapmaz. Kaynak mutabakatında ham kaynak adı tekrarları da denetlenir.

## 15 Ekim 2026 — güncel kanıt ve iş kuyruğu
- MADSC 05 tetikleyici düzeltmesi: c7567e1, run 38694043295 SUCCESS.
- MADSC 03 sağlık raporu artifact kapsamı: 7e797fa, run 38694963696 SUCCESS; sağlık raporu kabul kontrolü: 439dc5b, run 38695730312 SUCCESS.
- MADSC 02 gerçek salt-okunur keşif taraması ve madsc_kesif artifact yolu: c2d28be, MADSC 05 run 38697244625 SUCCESS. Keşif adımı continue-on-error olduğu için adımın ve çıktıların ayrı doğrulanması şart.
- YEDEKLER'e otomatik kanal ekleme izni kullanıcının sonraki talimatıyla İPTAL edildi; eski devir notundaki izin geçersiz. Korunan listeler, logolar, yedekler değiştirilmeyecek; PR #71 birleştirilmeyecek.
- AÇIK İŞLER, sırayla: (1) gerçek keşif adımı ve artifact içeriği; (2) bağımsız 5 kategori hata yönetimi; (3) 92 eski workflow'un işlev/tetik/yan etki/artifact eşdeğerliğinin tek tek uygulanması (kanıtlı 0/92); (4) tarihsel ve harici yedek geri yükleme; (5) 1039 girişin sağlık kapsamı ve aday tekrar/kimlik/IBO testleri; (6) EPG/Pages ve PNG aday kimliği; (7) gerçek yazma koruması/devre kesici; (8) eski cron/çakışma ve rapor yükünün doğrulanması.
- 7/24 saatlik ChatGPT görevi tekrar etkin; bu, her saat bir çalışma turudur, kesintisiz gerçek zamanlı işlem değildir. Tamamlanmış denmeyen işlerin kanıtı toplanmaya devam eder.

- 16 Ekim K2: eski birlesik kesfin arsiv before/tarama/after ve dort asama sonuc zinciri K2'ye baglandi; izole gercek betik testi eklendi. Tam workflow/uretim parity kabul edilmedi; Actions kaniti DEVAM_NOTU.md'de izlenir.

- 16 Ekim K4: mevcut disaster_recovery_dry_run.py gecici bozulma/geri acma tatbikati K4'e baglandi; raporu artifact'ta. Harici/tarihsel backup onayi degil.
- 16 Ekim besli runtime koruma: k1_protected_integrity.py snapshot/check tum takip edilen korunan M3U/yedek/favori dosyalarini gercek calisma dizininde karsilastirir; bes kategoride always son kontrol. Yerel 43 dosya/0 fark; gercek Actions sonucu DEVAM_NOTU.md'de izlenir.

- 16 Ekim K2 kosular arasi gecmis: discovery_history_restore.py ayni dal/ata commit basarili 02 veya parent05 artifact gozlemlerini checkout kayitlarini silmeden birlestirir; bozuk veri/indirme/celiski taramayi durdurur. K2'ye bagli, runner disina push yapmaz. Yerel 8 davranis testi PASS; Actions kaniti DEVAM_NOTU.md'de izlenir.

- 16 Ekim K2 genis kaynak: mevcut tools/genis_kaynak_taramasi.py weekly/monthly modlari wide_source_scan.py ile K2'ye baglandi; manuel secim, kod degisikligi CI kabulunde both, normal cron'da none. Iki gecmis belgesi ata commit tabanli uc yonlu birlesir, artifact'ta korunur; main push/dispatch yok. Gercek Actions kaniti DEVAM_NOTU.md'de izlenir.

- 16 Ekim K3 logo/EPG kalite: mevcut tools/logo_epg_audit.py ve eski test15 uyari sozlesmesi K3'e tasindi. Tam M3U giris kapsam kontrolu, ayri JSON artifact ve zorunlu outcome kapisi; logo/EPG/liste duzeltmesi veya IBO kimlik onayi yapmaz. Gercek Actions kaniti DEVAM_NOTU.md'de.

- 16 Ekim K3 aday puanlama: category_candidate_scoring.py mevcut scorer/birlesik raporu K2'nin kabul edilmis artifact kanitiyla izole klasorde calistirir, ek probe0. Priority rapor adi eslesmesi ve bozuk kararlilik gecmisi sifirlama hatasi duzeltildi. Uzunlamasina state/probe entegrasyonu henuz kabul edilmedi; Actions kaniti DEVAM_NOTU.md'de.

- 16 Ekim K5 kanit devri: category_evidence_collect.py ayni run'in basariliK1..K4 artifact'lerinden sabitJSONraporlari provenance/SHAkontroluyle alir; ownerraporlari eskicheckout'la tekrar yazdirmaz. Yonetimozeti bagimliliklarindan sonra uretilir;24kaynakbolumu. Cihaz/harici/tam92kabul iddiasi yok; gercekCIsonucu DEVAM_NOTU.md'de.

- 16 Ekim K5 kanit aktarimi: af3d1dd / #38949404949 SUCCESS5/5. Ayni run'in4kategori17JSON kaniti provenance+hash ile merkezi rapora bagli;24baslikta eksik9->3. Tam92 kabul degil.
- 16 Ekim K5 Actions verisi: eski durum/hata raporlayicilarina GET envanter/son100kosu/enfazla20basarisizkosu job kaniti baglandi; mevcut run haric, otomatik ozet workflow+dal bazli. Gercek CI henuz bekliyor; DEVAM_NOTU izlenir.

- 16 Ekim priority upstream hata duzeltmesi: ffprobe basarisiz satir9alan/8baslik URL-source kaymasi giderildi. Iki fixtureCSV testi ve toplam58 five_categoryPASS; gercek eski priority/toplu Actions sonucu DEVAM_NOTU'de izlenecek. Playlist ve legacyworkflow dosyasi degismedi.

- 16 Ekim K3 kararlilik state: mevcut tracker gercek olcum zamani+tekillik destegi ve gecmisi saklama ile K2 olcumlerine baglandi. category_stability_history aynidal/ataSUCCESS03/05 artifact state+hash restore; entegrasyononcesi acikbootstrap, sonrasi eksikbozukfailclosed.7gunpencere/24saatteknikaralik,30gun/IBO/sureklioynatma degil.69five_category+21ilgiliyerelPASS;gercekCI DEVAM_NOTU'de izlenecek.

- K3 zamanli kararlilik gercekCI: c1683414 / MADSC05 #38952859393 SUCCESS5/5; eski KanalKararlilik #38952859152 SUCCESS. K3ilkbootstrap0medya/0gozlem/0kararli;K5eksikrapor0,43korunan0fark. Sonraki kosudan gercek state restore ve priority/genelmedya zamanli upstream kabul halenbekliyor; tam92parity0/92.

- 16 Ekim K3 öncelikli/genel medya: mevcut iki probe betiği gerçek OLCUM_ZAMANI üretir. category_candidate_media.py izole mevcut priority+genel30parti CLI ve yalnız-keşif modunu bağlar; aynı URL priority ölçümü genel taramada tekrar probe edilmez. Başarılı ata artifact'inden hash/şema/üretici sürümüyle 6saatlik reuse; scoring en yeni ölçümü kullanır. Yerel76kategori+31ilgiliPASS;gerçekCIbekliyor,DEVAM_NOTU izlenir. Tam92/IBO/liste onayı değil.

- K3 medya bağlantısı gerçekCI 1568187 / #38957224597 SUCCESS5/5; eskipriority #38957224570 ve eski genel #38957224651 SUCCESS. K3 102gerçekprobe/102gözlem/132tekilpuanlamaadayı,24hkararlı0;2ortakURLtekrarprobesiz. Ata kararlılık restore gerçekPASS. Cache sonraki gerçekreusekabulü bekliyor;79yerelkategoritestPASS.

- K3 medya reuse gerçekCI: 45c1729 / #38958162467 SUCCESS5/5. Önceki #38957224597'nin102gözlemi geri geldi; yeniadaymedyaprobe0/yenigözlem0, candidate_discovery_ran=false; statehash ve4kaynakraporhashi aynı.132tekilpuanlama/in 24hkararlı0;43korunan0fark,K5eksikrapor0.79yerelkategoritest ve K3gerçek40regresyonPASS. Genelmedya yalnız ilk30parti; tümadaykapsamı/gerçek24h/7gün/30gün ve tam92parity onayı değil.
