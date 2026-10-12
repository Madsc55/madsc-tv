# 11 geliştirme — mevcut uygulama ve kalan iş

12 Ekim 2026. Bu inceleme kod/rapor envanteridir; eski testleri yeniden çalıştırmaz. Bir dosyanın varlığı gerçek cihaz başarısı değildir.

| No | Plan | Mevcut kanıt | Durum ve eksik |
|---|---|---|---|
| 1 | Tek komutla birleşik kontrol | `.github/workflows/toplu-sistem-kontrol.yml` mevcut | Kısmi: kapsamlı depo kontrolü var; güncel üçlü/final/kimlik/EPG sonuçlarını birleştiren tek komut raporu eksik. |
| 2 | Kalıcı tekrarsız geçmiş | `madsc_kesif/gecmis.json`, `madsc_dogrulama/state.json`, `verification_pipeline.py`, `final_validation.py` | Kurulu: keşif geçmişi, üç deneme sınırı, altı saat aralık ve final sonuçlarını atlama var. Düzeltmenin canlı sonuçları ayrıca takip edilir. |
| 3 | Gerçek yayın kontrolü | `verification_pipeline.py`, `final_validation.py`, ilk 39 sonuç | Kurulu fakat kapsam tamamlanmadı: kalan URL'lerin ayrı son kontrolü bekliyor. Teknik geçiş kimlik onayı değildir. |
| 4 | Cihaz/sürüm bazlı IBO uyumluluğu | Kullanıcı karar kayıtları; sonuçlarda `ibo_sweden` alanı | Kısmi: tam cihaz/model/uygulama sürümü ve güncel kullanıcı sonucu eksik. Uzaktan geçiş yazılmaz. |
| 5 | Beş kanallık EPG | `epg_deneme/build.py`, `liste.m3u`, `rehber.xml`, `rapor.json` | Hazırlık kurulu; 12 Ekim için yenilendi. Kaynak gece yarısı tarih hataları açıkça raporlanır. Cihaz görünürlüğü ve gerçek program karşılaştırması bekliyor. |
| 6 | Gerçek logo denetimi | `logo_deneme/audit.py`, `scripts/candidate_logo_report.py`, görsel inceleme raporu | Kurulu: adres/PNG denetimi ve ayrı aday hazırlığı. Gerçek amblem eşleşmeleri tamamlanmadı. Ana listedeki dolu logolar korunur. |
| 7 | İşlem/açılış/geçiş hızı | Yayın decoder süreleri ve teknik kayıtlar | Eksik: decoder süresi IBO kanal açılış/geçiş süresi değildir; cihaz ölçümü gerekir. |
| 8 | Rapor yedeği ve geri dönüş | Actions artifact adımları, `scripts/restore_dry_run.py`, `scripts/disaster_recovery_dry_run.py` | Kısmi: arşivleme ve geçici alana geri dönüş araçları mevcut. Yeni rapor/state dosyalarının geri dönüş kapsamı ve son kanıtı ayrı denetlenmeli; korunan dosyalara yazma yok. |
| 9 | Korunan dosyalar/sınırlı yetki | Güvenlik workflow'ları 31–38, salt okunur görevler, rapor dizinine sınırlı git add | Kısmi: kapsam denetimleri mevcut; bütün üretim yazarlarının tek onay kapısı kullandığı iddia edilmez. Liste değişiklikleri kullanıcı iznine bağlı. |
| 10 | Yeni kanal/alternatif tek durum raporu | `tools/candidate_status_summary.py`, eski birleşik aday raporu | Kısmi: eski genel durum aracı güncel state/kimlik/IBO dosyalarını birleştirmiyor. Aynı isim doğru kanal kabul edilmeyecek; URL sayısı kanal sayısı diye verilmeyecek. |
| 11 | Önerileri aynı cihaz/sürümde doğrulama | Kullanıcı IBO kararları ayrı tutuluyor; ADA/Kanal D reddi kayıtlı | Kısmi: yeni önerilerin aynı cihaz/sürümde kullanıcı doğrulaması eksik. Eski retler tekrar geçerli sayılmaz veya silinmez. |

Takvim: birleşik yeni keşif günde iki (06:00/18:00 UTC); tek devam yolu kuruldu. Aylık geniş taramanın ayrı mod ve kapsamı henüz tamamlanmadı. Üçlü kontrol takvimi yeni keşif takvimi değildir.

Tekrar yapılmayacak: ilk 6436 adayın üç denemesi; ilk 39 URL'nin final testleri; sabah verilmiş kimlik kararları; uygulanmış kategori/sıra/kanal taşıma işlemleri; mevcut dolu logo değişiklikleri. Yalnız açık kalan kapsam tamamlanır.
