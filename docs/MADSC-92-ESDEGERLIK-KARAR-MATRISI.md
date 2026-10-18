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

## 18 Ekim 2026 — Sonraki aşamalar: 13–26 (mevcut 00–12 kuyruğunun devamı)

Bu maddeler uygulanacak iş sırasıdır, tamamlandı işareti değildir. 12 numaralı cihaz kabulünden sonra sırayla değerlendirilir. Güvenli, salt okunur testler otomatik yürütülebilir; yayın listesi, EPG, logo veya yedek yazmaları ayrı onay ve koruma kapısı gerektirir.

- [ ] **13 — Canlı kanal taraması:** kaynakların periyodik taranması, cron/dispatch ve çıktı kanıtı; otomatik yayın listesi değişikliği yok.
- [ ] **14 — Bozuk kanal tespiti:** çoklu ölçüm ve yanlış-pozitif filtresi; güvenli onarım önerileri, izinsiz kanal değiştirme yok.
- [ ] **15 — Yeni kanal adayları:** kaynak, oynatma, kimlik ve süreklilik doğrulaması; aday havuzuna kayıt, korunan listeye otomatik terfi yok.
- [ ] **16 — Tekrar ve eşleşme denetimi:** kanal ID, URL, ülke, EPG ve logo çakışmalarını raporla; otomatik silme yok.
- [ ] **17 — EPG ve logo güncelliği:** üretim, dağıtım, erişilebilirlik ve eksik görsel raporu; yazma için izin kapısı.
- [ ] **18 — IBO Player Pro uyumluluğu:** M3U, EPG, logo, kanal geçişi ve gerçek cihaz doğrulaması.
- [ ] **19 — Yayın listesi ve yedek bütünlüğü:** checksum, sürüm, erişim ve bozulma denetimi.
- [ ] **20 — Hata uyarısı ve güvenli kurtarma:** tekil hata raporu, tekrarlı alarm filtresi, izole geri yükleme; korunan dosyaya onaysız yazma yok.
- [ ] **21 — Günlük/haftalık/aylık bakım:** cron çakışmaları, tekrar eden işler, artifact saklama ve tek merkezden raporlama.
- [ ] **22 — Eski otomasyonları kontrollü emekliye ayır:** yalnız 92/92 davranışsal eşdeğerlik ve kullanıcı onayından sonra, geri alma planıyla.
- [ ] **23 — 24 saat kararlılık:** planlanan tetikler, hata oranı, yeniden denemeler ve yayın sağlığı kanıtı.
- [ ] **24 — 7 gün kararlılık:** günlük kanıtlar, kaçan cron'lar, yedek ve EPG erişilebilirliği.
- [ ] **25 — Son güvenlik ve performans:** asgari izinler, korunan yollar, işlem süreleri, gereksiz ağ çağrıları, restore provası.
- [ ] **26 — Üretim kabulü ve sürekli takip:** gerçek cihaz onayı, 7/24 takip göstergeleri ve olay müdahale kılavuzu.

### Otomasyon sınırları
- `madsc-05-genel-bakim.yml` mevcut beş aşamalı toplu test zinciridir; 13–26 maddeleri otomatik tamamlanmış değildir.
- 92/92 eşdeğerlik ve canlı üretim doğrulanmadan eski workflow'lar kapatılmaz.
- GitHub Actions cron tetikleri yalnız varsayılan dalda işler; özellik dalındaki cron tek başına 7/24 üretim kanıtı değildir.
- IBO gerçek cihaz kabulü ve riskli üretim değişiklikleri kullanıcı onayı gerektirir.

## Ek kabul ve operasyon kuyruğu — 27–34

Aşağıdaki işler 26'dan sonra uygulanır; öncesinde ilgili güvenlik bulgusu çıkarsa öne çekilir. İşaretler yalnız somut test kanıtıyla değişir.

- [ ] **27 — İş akışı izin matrisi:** GITHUB_TOKEN, üçüncü taraf sırlar, en az ayrıcalık ve fork/PR güvenlik sınırları.
- [ ] **28 — Bağımlılık ve tedarik zinciri:** action sürümlerini sabitleme, Python bağımlılıklarını tarama ve güncelleme testi.
- [ ] **29 — Gözlemlenebilirlik:** merkezi günlükler, başarısız aşama sınıflandırması, saklama süresi ve anlaşılır durum ekranı.
- [ ] **30 — Maliyet ve kota denetimi:** Actions dakika/artifact tüketimi, gereksiz paralel koşular, dış servis oran sınırları.
- [ ] **31 — Felaket kurtarma tatbikatı:** bağımsız dış yedekten izole kurtarma, geri dönüş süresi ve bütünlük kanıtı.
- [ ] **32 — Üretim geri alma planı:** workflow, yayın ve Pages için sürümlü rollback; yazma işlemleri onay kapılı.
- [ ] **33 — Belgeler ve devir notu:** kurulum, günlük işletim, hata müdahalesi, cihaz doğrulama ve yeni sohbetten devam kılavuzu.
- [ ] **34 — Periyodik yeniden kabul:** haftalık başarısızlık taraması, aylık eşdeğerlik ve erişim denetimi; yeni iş kuyruğuna ekleme.

**Tek kuyruk ilkesi:** Önce 02–12, ardından 13–26, ardından 27–34. GitHub Actions tek koşuda yalnız teknik olarak otomatik yapılabilen salt-okunur denetimleri yapar. Gerçek cihaz, üretim yazmaları ve eski workflow emekliliği için kullanıcı onayı şarttır. Bu belge zamanlayıcı değildir; yalnızca GitHub Actions'a açıkça bağlanan adımlar kendiliğinden çalışır.

## Tamamlayıcı iş kuyruğu — 35–50

Bu bölüm bilinen ek kabul konularını sıralar; keşfedilecek yeni sorunlar ilgili en erken aşamaya eklenir. Sıra otomatik çalıştırma garantisi değildir; her adımın kanıtı gerekir.

- [ ] **35 — Varsayılan dal ve dağıtım topolojisi:** aktif default branch, cron ve Pages yayın kaynağı kanıtı.
- [ ] **36 — GitHub Actions concurrency:** aynı anda tetiklenen push, cron, dispatch ve workflow_call yarışlarını engelleyen gruplar.
- [ ] **37 — Workflow çağrı zinciri:** reusable workflow inputs, outputs, needs, if/always ve hata yayılımı doğrulaması.
- [ ] **38 — Eşzamanlı dosya yazma çatışmaları:** yarış, kilit, atomik güncelleme ve tekrar denenebilirlik denetimi.
- [ ] **39 — Idempotency ve tekrar çalıştırma:** aynı girdiyle yinelenen koşunun güvenli ve tutarlı çıktı üretmesi.
- [ ] **40 — Sır ve kimlik bilgisi yaşam döngüsü:** sızıntı taraması, izin sınırları, yenileme prosedürü; sırları rapora yazma yok.
- [ ] **41 — Kaynak güvenilirliği ve erişim koşulları:** URL kaynaklarının yetki, oran limiti ve kararlılık değerlendirmesi.
- [ ] **42 — Ağ arızası ve timeout senaryoları:** 429, 5xx, DNS, bağlantı kesintisi, backoff ve kısmi sonuç davranışı.
- [ ] **43 — Çıktı şema ve veri kalite sözleşmeleri:** M3U/EPG/JSON/CSV doğrulama, encoding, sıralama ve bozuk veri karantinası.
- [ ] **44 — Kanal kimliği ve tarihçe tutarlılığı:** TVG ID, ülke, grup, URL değişimi, geçmiş ve tekrarların izlenmesi.
- [ ] **45 — EPG zaman dilimi ve veri tazeliği:** XMLTV doğruluğu, saat kayması, geçmiş ve gelecek program kapsamı.
- [ ] **46 — Logo dosyası ve erişim testi:** PNG/JPEG doğruluğu, kırık bağlantı, boyut, isimlendirme ve önbellek.
- [ ] **47 — Pages/CDN önbellek ve erişilebilirlik:** public URL, MIME, yönlendirme, HTTPS, önbellek ve güncelleme gecikmesi.
- [ ] **48 — Playlist istemci uyumluluğu:** IBO yanında standart M3U oynatıcılarla yalnız teknik ayrıştırma testi.
- [ ] **49 — Rapor tutarlılığı ve kanıt izi:** 92 görev için dosya, commit, run, artifact, karar, eksik kanıt ve sahibi alanları.
- [ ] **50 — Son açık işler taraması:** çözülmemiş bug, TODO, risk, başarısız test ve yeni gereksinimleri yeniden kuyruğa al.

**Öncelik kuralı:** Güvenlik açığı, veri kaybı veya üretim kesintisi saptanırsa numara sırasından önce güvenli durdurma/onarım yapılır. Riskli değişiklikler açık onay gerektirir. 02–34 maddelerinin bitmesi bu yeni maddelerin de bittiği anlamına gelmez.
