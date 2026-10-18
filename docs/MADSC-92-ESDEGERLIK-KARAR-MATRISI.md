# MADSC — 92 workflow eşdeğerlik karar matrisi (14 Ekim 2026)

## Gerçek denetim kanıtı
- GitHub run [38630252033](https://github.com/Madsc55/madsc-tv/actions/runs/38630252033): beş kategori job'u başarıyla tamamlandı.
- Genel bakım workflow'u `scripts/five_category_92_workflow_audit.py` çalıştırıyor ve `madsc_merkezi_denetim/92_workflow_gorev_ve_kategori_haritasi.json` raporunu artifact'e ekliyor.
- Bu betik 92 eski dosya dışında sayıda hata veriyor; başarılı koşu dolaylı olarak **92 dosyalık statik envanterin işlendiğine** kanıttır.
- Fakat bu denetim her dosya için `requires_manual_behavior_review: true` üretiyor. **92/92 davranışsal eşdeğerlik henüz onaylanmış değildir.**

## Karar kapıları
| Kontrol | Kanıt | Karar |
|---|---|---|
| Beş kategori zinciri | Run 38630252033: 5/5 success | GEÇTİ |
| Eski 92 dosyanın statik taraması | Aynı run, kategori 5 denetim adımı success | GEÇTİ |
| Eski 92 görevin komut/çıktı eşdeğerliği | Karşılaştırmalı davranış testleri yok | BEKLİYOR |
| Çift tetiklenme ve yazma yolları | Risk analizi gerekli | BEKLİYOR |
| EPG üretimi → Pages dağıtımı | Canlı eşdeğer zincir kanıtı yok | BEKLİYOR |
| İki günlük keşif tetikleyicisi | Yeni sistemde üretim eşdeğerliği kanıtlanmadı | BEKLİYOR |
| Yedekleme/geri yükleme | Harici geri yükleme testi yok | BEKLİYOR |
| IBO cihaz kabulü | Kullanıcı cihaz kanıtı yok | BEKLİYOR |

## Önemli hata riski
`scripts/five_system_migration_audit.py` içinde `migration_complete` yalnızca dosya sayısı beş ve eksik dispatch olmamasıyla doğru olabilir. Bu gösterge **işlevsel eşdeğerlik anlamına gelmez**; karar mekanizması olarak kullanılmamalı. Ayrıca `five_category_92_workflow_audit.py` dosya adına ve komut anahtar sözcüklerine göre **ön sınıflandırma** yapıyor; gerçek görev devri için tek başına yeterli değildir.

## Güvenli sonraki aşama
Artifact içindeki 92 satırlık JSON'u karşılaştırma tablosuna aktar. Özellikle `contents_write` + otomatik tetik, `workflow_run`, `dispatch`, cron ve protected-path yazma yollarını elle doğrula. Her workflow için aynı girdide eski/yeni komut ve çıktı karşılaştırması ile hata senaryosu kanıtı ekle. Bu kapılar geçilmeden hiçbir eski workflow kapatılmaz veya silinmez.

Korunan M3U, favoriler, YENİLER, PNG ve yedeklere dokunulmadı.

## 18 Ekim 2026 — Uygulama sırası (tek kuyruk)

Bu liste uygulama sırasıdır, tamamlandı iddiası değildir. Her madde kanıtla kapatılmadan sonraki riskli geçişe başlanmaz. Korunan yayın listelerine dokunulmaz; eski workflow'lar davranışsal kanıt oluşmadan devre dışı bırakılmaz.

- [x] **00 — Beş merkezi workflow dosyasını doğrula:** `madsc-01-guvenlik.yml`, `madsc-02-kesif.yml`, `madsc-03-kanal-test.yml`, `madsc-04-arsiv-yedek.yml`, `madsc-05-genel-bakim.yml` mevcut. Run 38630252033'te beş job success; bu eski koşunun kanıtıdır.
- [x] **01 — 92 yazma-risk raporunun JSON sonlandırmasını düzelt:** `scripts/five_category_92_workflow_audit.py`, commit `526d6e7c201858eddb3a620a345dc4ecaced6c36`. Yeni koşuda JSON ayrıştırması ayrıca doğrulanacak.
- [ ] **02 — Yeni commit için beşli toplu Actions koşusunu doğrula:** güncel run ID, beş job sonucu, her başarısız step ve artifact. PR-triggered sorgunun boş olması başarılı koşu anlamına gelmez.
- [ ] **03 — 92 workflow risk envanterini çıkar:** artifact'teki `92_workflow_gorev_ve_kategori_haritasi.json`, `92_workflow_yazma_risk_inceleme_kuyrugu.json`, `92_workflow_esdegerlik_kabul_matrisi.csv` dosyalarını ayrıştır; riskli dosya adlarını ve gerçek sayıları kaydet.
- [ ] **04 — Korunan yazma yolları ve çift tetiklemeleri kapat:** eski/yeni `contents: write`, push, force-push, API yazmaları, `workflow_run`, dispatch, cron ve path filtrelerini dosya bazında karşılaştır. Yetki/koruma kapısı testlerini toplu çalıştır.
- [ ] **05 — Güvenlik görevlerini davranışsal taşı:** eski güvenlik kontrollerinin girdilerini, hata davranışını ve çıktılarını `madsc-01-guvenlik.yml` ile karşılaştır; eksik işleri ekle, regresyonu doğrula.
- [ ] **06 — Keşif görevlerini davranışsal taşı:** zamanlama, iki günlük tarama, geniş tarama, geçmiş kurtarma, aday çıktıları ve yinelenen işleri `madsc-02-kesif.yml` ile eşleştir; korunan listelere otomatik yazma yok.
- [ ] **07 — Kanal testi, EPG ve Pages zincirini taşı:** `madsc-03-kanal-test.yml` ile eski test/EPG/logo işlerini karşılaştır; canlı EPG üretimi → Pages dağıtımı için ayrı uçtan uca kanıt üret. Teknik kontrol IBO cihaz kabulü değildir.
- [ ] **08 — Harici yedek ve geri yüklemeyi kanıtla:** `madsc-04-arsiv-yedek.yml` için harici yedekten izole restore; HEAD'den restore dış yedek kanıtı sayılmaz.
- [ ] **09 — Genel bakım ve tek orkestrasyon:** `madsc-05-genel-bakim.yml` bağımlılıkları, rapor/artifact toplama, hata kapıları ve tek toplu koşu testleri; aynı işin iki kez çalışmasını önle.
- [ ] **10 — Kalan 92/92 karşılaştırmayı kapat:** her eski workflow için eski/yeni komut, tetik, izin, çıktı, hata senaryosu ve kanıt URL'si; yalnız gerçek kanıt varsa kabul ver.
- [ ] **11 — Üretime geçiş kararı:** GitHub Actions schedule yalnız varsayılan dalda etkinleşir; dal/default-branch durumunu ve canlı cron kanıtını doğrula. Ancak tüm geçiş kapıları geçildikten ve kullanıcı onayından sonra eski workflow'ları kontrollü kapat.
- [ ] **12 — TCL 55C655 / Ibo Player Pro cihaz kabulü:** kullanıcıyla gerçek oynatma, EPG, logo ve kanal kararlılığı doğrulaması; onaysız 7/24 sorunsuz kabulü yok.

**Sıradaki aktif iş: 02.** Bu listenin işaretleri yalnız doğrulanmış kanıtlarla güncellenir.
