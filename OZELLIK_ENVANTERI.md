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
