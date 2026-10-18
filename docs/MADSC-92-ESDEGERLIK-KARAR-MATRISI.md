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

**Sıradaki aktif iş: 02.**

### 18 Ekim 2026 — 13:09 CEST / güvenlik risk kapsama turu
- Dalın işlem öncesi doğrulanmış HEAD'i: `049bfabb25b68d79666af13169fd05a61ff7c4fd`. Bu SHA için Actions listesinde eşleşen koşu bulunmadı; 02 kapısı **açık**.
- Önceki SHA `8d9ed3d10df1f5609df69a53129509757450d17b`: K1 run `39115560402`, 1/1 job success, iki artifact. Önceki SHA `fd90ce3aef55ee05fed7ad5cf0a3e183db6ccab1`: MADSC 05 run `39114953442`, 5/5 job success, beş artifact. Job logları kontrol edildi. Bunlar yeni düzeltmenin CI kanıtı değildir.
- 04 kapsamında salt-okunur denetleyicilerde `gh workflow run/enable/disable`, `gh run rerun` mutasyon sinyali ve `CALISMAYANLAR.txt`, `YABANCI_KANALLAR.m3u`, `epg.xml`, HEPSI/FAVORILER/YEDEKLER/EPG/logo/arşiv korunan yol sinyali eklendi; iki regresyon dosyasında testler. Risk sinyali **gerçek yazma engeli veya davranışsal parity kanıtı değildir**.
- Bu turda hazırlanan değişiklik tek toplu commit olarak dalda yayımlanırsa yeni SHA ve Actions run ID'si **sonraki turda ayrıca doğrulanacak**; şu an için doğrulanmış yeni run ID **yok**. 02–04 açık, 92/92 davranışsal kabul **0/92**, IBO cihaz testi bekliyor. Eski workflow, korunan veri, main ve PR #71 değiştirilmedi.
 Bu listenin işaretleri yalnız doğrulanmış kanıtlarla güncellenir.

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

## Genişletilmiş uygulama kuyruğu — 51–100

Bu 50 madde, 00–50 sırasındaki mevcut işlerin devamıdır. Önceki bir maddeyle örtüşen işler ayrı tekrar koşu yerine aynı kanıtla birleştirilir. Otomatik koşulabilen kontroller GitHub Actions'a ayrıca bağlanmadıkça yalnız plan olarak kalır.

### Test altyapısı ve kanıt
- [ ] **51 — T:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **52 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **53 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **54 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **55 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **56 — f:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **57 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **58 — x:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **59 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **60 — u:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **61 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **62 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **63 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **64 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **65 — z:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **66 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **67 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **68 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **69 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **70 — y:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **71 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **72 — n:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **73 — u:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### İş akışı dayanıklılığı
- [ ] **74 — J:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **75 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **76 — b:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **77 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **78 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **79 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **80 — m:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **81 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **82 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **83 — u:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **84 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **85 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **86 — p:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **87 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **88 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **89 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **90 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **91 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **92 — k:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **93 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **94 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **95 — ı:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### Yayın veri hattı
- [ ] **96 — M:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **97 — 3:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **98 — U:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **99 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **100 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **101 — ö:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **102 — z:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **103 — d:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **104 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **105 — z:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **106 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **107 — m:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **108 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **109 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **110 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **111 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **112 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **113 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **114 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### Yedek ve veri yönetimi
- [ ] **115 — Y:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **116 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **117 — d:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **118 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **119 — k:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **120 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **121 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **122 — m:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **123 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **124 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **125 — k:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **126 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **127 — p:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **128 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **129 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **130 — m:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **131 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **132 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **133 — n:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **134 — v:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **135 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **136 — n:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **137 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **138 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **139 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **140 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### İşletim ve üretim kabulü
- [ ] **141 — O:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **142 — p:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **143 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **144 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **145 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **146 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **147 — y:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **148 — o:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **149 — n:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **150 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **151 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **152 — a:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **153 — ğ:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **154 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **155 — ı:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **156 — k:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **157 —  :** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **158 — g:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **159 — ö:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **160 — s:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **161 — t:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **162 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **163 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **164 — g:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **165 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **166 — l:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **167 — e:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **168 — r:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.
- [ ] **169 — i:** kapsamı doğrula, otomatik test/rapor ekle, koşu kimliği ve kabul kanıtı kaydet; üretim yazması varsa onay kapısı uygula.

### Çalıştırma ve bitiş koşulları

1. İlk açık, teknik olarak yapılabilir maddeyi al; önceki madde başarısızsa nedeni raporla ve güvenli şekilde dur.
2. Her değişiklik için test, Actions koşu kimliği, artifact ve commit kanıtı oluştur; doğrulanmamış işi tamamlandı diye işaretleme.
3. 92 eski workflow için tek tek davranışsal kanıt olmadan emeklilik yok; korunan playlist/EPG/logo/yedek dosyalarına izinsiz yazma yok.
4. Gerçek cihaz, default-branch üretim dağıtımı ve riskli yazmalar kullanıcı onayı gerektirir.
5. Bu belge bir iş planıdır; kendiliğinden gece boyunca çalışan ajan değildir. Mevcut beşli GitHub Actions zinciri kendi tanımlı görevlerini yürütür, tüm 100 maddeyi değil.

## Genişletilmiş toplu sıra — 101–200

100 ek kontrol, önceki sıranın devamıdır. Her kontrol somut kanıtla tamamlanır. Bunlar otomatik yürütücü değil, iş kuyruğudur.

### Güvenlik
- [ ] **101 — Güvenlik: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **102 — Güvenlik: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **103 — Güvenlik: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **104 — Güvenlik: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **105 — Güvenlik: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **106 — Güvenlik: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **107 — Güvenlik: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **108 — Güvenlik: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **109 — Güvenlik: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **110 — Güvenlik: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Keşif
- [ ] **111 — Keşif: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **112 — Keşif: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **113 — Keşif: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **114 — Keşif: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **115 — Keşif: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **116 — Keşif: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **117 — Keşif: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **118 — Keşif: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **119 — Keşif: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **120 — Keşif: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Kanal testleri
- [ ] **121 — Kanal testleri: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **122 — Kanal testleri: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **123 — Kanal testleri: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **124 — Kanal testleri: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **125 — Kanal testleri: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **126 — Kanal testleri: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **127 — Kanal testleri: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **128 — Kanal testleri: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **129 — Kanal testleri: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **130 — Kanal testleri: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### EPG
- [ ] **131 — EPG: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **132 — EPG: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **133 — EPG: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **134 — EPG: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **135 — EPG: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **136 — EPG: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **137 — EPG: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **138 — EPG: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **139 — EPG: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **140 — EPG: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Logo
- [ ] **141 — Logo: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **142 — Logo: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **143 — Logo: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **144 — Logo: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **145 — Logo: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **146 — Logo: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **147 — Logo: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **148 — Logo: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **149 — Logo: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **150 — Logo: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Yedek
- [ ] **151 — Yedek: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **152 — Yedek: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **153 — Yedek: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **154 — Yedek: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **155 — Yedek: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **156 — Yedek: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **157 — Yedek: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **158 — Yedek: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **159 — Yedek: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **160 — Yedek: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Actions
- [ ] **161 — Actions: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **162 — Actions: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **163 — Actions: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **164 — Actions: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **165 — Actions: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **166 — Actions: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **167 — Actions: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **168 — Actions: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **169 — Actions: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **170 — Actions: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Pages ve IBO
- [ ] **171 — Pages ve IBO: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **172 — Pages ve IBO: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **173 — Pages ve IBO: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **174 — Pages ve IBO: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **175 — Pages ve IBO: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **176 — Pages ve IBO: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **177 — Pages ve IBO: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **178 — Pages ve IBO: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **179 — Pages ve IBO: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **180 — Pages ve IBO: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Operasyon
- [ ] **181 — Operasyon: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **182 — Operasyon: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **183 — Operasyon: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **184 — Operasyon: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **185 — Operasyon: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **186 — Operasyon: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **187 — Operasyon: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **188 — Operasyon: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **189 — Operasyon: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **190 — Operasyon: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

### Geçiş kabulü
- [ ] **191 — Geçiş kabulü: girdi ve kapsam envanteri** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **192 — Geçiş kabulü: izin ve yetki doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **193 — Geçiş kabulü: tetikleme koşulları** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **194 — Geçiş kabulü: hata senaryosu testi** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **195 — Geçiş kabulü: yeniden deneme ve idempotency** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **196 — Geçiş kabulü: çıktı biçimi doğrulaması** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **197 — Geçiş kabulü: kanıt artifact toplama** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **198 — Geçiş kabulü: sınır durum regresyonu** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **199 — Geçiş kabulü: geri alma ve güvenlik kapısı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.
- [ ] **200 — Geçiş kabulü: uçtan uca kabul kanıtı** — İlgili kaynakları karşılaştır; uygulanabilir salt-okunur otomatik test ve rapor ekle; GitHub run/artifact/commit kanıtını kaydet. Korunan dosyalara yazma ve eski workflow kapatma için ayrıca onay gerekir.

**Yürütme:** İlk açık işten sırayla ilerle; güvenlik ve veri kaybı riski öne alınır. 92/92 davranışsal eşdeğerlik ve kullanıcı onayı olmadan eski workflow kapatılmaz. Gerçek cihaz testi uzaktan tamamlandı sayılmaz.

## 18 Ekim 2026 — 09:57 (Europe/Stockholm) doğrulanmış Actions durumu

- GitHub Actions run: https://github.com/Madsc55/madsc-tv/actions/runs/39082013826
- Beş job'ın tamamı `completed/success`: 01 Güvenlik, 02 Keşif, 03 Kanal testleri, 04 Arşiv-yedek, 05 Genel bakım.
- Beş artifact mevcut ve `expired=false`: `madsc-kesif-tek-kosu-rapor` (12119885163), `madsc-genel-bakim-tek-kosu-rapor` (12119322760), `madsc-guvenlik-tek-kosu-rapor` (12119232510), `madsc-arsiv-yedek-tek-kosu-rapor` (12119039361), `madsc-kanal-test-tek-kosu-rapor` (12118748759).
- Bu kanıt yalnız belirtilen koşunun beş aşamasının başarı durumunu doğrular; 92/92 davranışsal eşdeğerlik, canlı Pages dağıtımı, dış yedek restore ve gerçek IBO cihaz kabulü doğrulanmış değildir.
- Sıradaki açık kapı: 92 eski workflow'un yazma/API/dispatch risklerini artifact içeriğinden dosya bazında doğrula ve kabul matrisini güncelle. Eski workflow'ları kapatma veya korunan dosyalara yazma izni verilmedi.

## 18 Ekim 2026 — Risk kuyruğu kanıtı iyileştirmesi

- `085211b4b75380a8fa30e44dbd321a90dac81bf0`: 92-workflow yazma-risk kuyruğu artık `write_risk_commands` komut kanıtlarını da içeriyor; salt okunur rapor üretimi, korunan dosyaya yazma yok.
- `2f964bdceff62e4c0b4c328c2cee44bca5b3c1de`: API-only workflow fixture'ında komut kanıtının JSON'a taşındığını denetleyen regresyon assertion eklendi.
- **Bekleyen doğrulama:** bu iki commit sonrası GitHub Actions run ve regresyon sonucu henüz teyit edilmedi; eski 92 workflow için davranışsal eşdeğerlik onaylanmadı.

## 18 Ekim 2026 — Yazma-risk kuyruğu kabul alanları

- `bdc1601ed235049433721df6d876a7ff7ced71cc`: `92_workflow_yazma_risk_inceleme_kuyrugu.json` artık her riskli eski workflow için `review_priority`, `requires_protected_write_review`, `required_acceptance_checks` alanlarını taşır.
- `320fdc19e6df2d8b4ef74c57f1bb6f6964c0a689`: API-only workflow'un yüksek öncelik ve dispatch idempotency kabul kontrolünü doğrulayan regresyon assertion'ları eklendi.
- **Açık:** Bu commit'ler için Actions test sonucu henüz doğrulanmadı. Bu statik risk sınıflandırması 92/92 davranışsal eşdeğerlik kanıtı değildir.

## 18 Ekim 2026 — Güvenlik kategorisi: korunan yol risk tespiti

- `71c3ed359044db771526035718b8769b6981f47e`: eski workflow'ların yazma-risk denetimi `HEPSI`, `FAVORILER`, `EPG/`, `logolar/`, `arsiv/` ve mevcut korunan playlist/yedek işaretlerini kapsayacak şekilde genişletildi. Bu bir statik tespit iyileştirmesidir, otomatik yazma engelleme kanıtı değildir.
- `4ad5cbfb2d9e330dda83a9864fbeee72c47fe53d` ve `3e24cb28352c34914aef13cd9f0dc803dcbcadeb`: `FAVORILER` için regresyon fixture'ı eklendi ve satır sonları düzeltildi.
- **Bekleyen:** Bu SHA'lar için Actions koşusu ve test başarısı henüz doğrulanmadı. Güvenlik kategorisi tamamlandı sayılmaz; 92/92 davranışsal eşdeğerlik açık.

## 18 Ekim 2026 — Güvenlik önceliği: manuel API yazmaları

- `e75fe0a9d282f630fb343f7f810b16ff4ed9782b`: yazma/API/dispatch sinyali olan manuel workflow'lar da `HIGH` inceleme önceliği alıyor; zamanlayıcı olmaması yazma riskini ortadan kaldırmaz.
- `865903c5a49494440879cd588c487f4d62000f4e`: API-only regresyon testi yüksek öncelik beklentisini doğrulayacak şekilde güncellendi.
- **Test sonucu bekleniyor:** bu SHA için GitHub Actions koşusu doğrulanmadan güvenlik kategorisi tamamlandı sayılmaz.


### 18 Ekim 2026 — Güvenlik CI hata ve onarım kaydı
- `562b2477be7ac3d6b43ac0aea197586e8f0c7a04` commitinde K1 run `39122430755` (job `117660567798`) başarısız; MADSC 05 run `39122430776` güvenlik job `117660568357` başarısız. Gerçek log: `scripts/five_category_92_workflow_audit.py:18` Python `SyntaxError` (`//` açıklama satırı). Diğer kademe jobları atlandı; başarılı sayılmaz.
- Açıklama satırı Python `#` sözdizimine çevrildi; işlevsel kod ve regresyon testleri korunuyor. Yeni commitin run/job/artifact sonucu henüz doğrulanmadı. Önce bu CI düzeltmesini kontrol et, ardından 02–04 risk kuyruğuna dön. 92/92 davranışsal kabul 0/92.

## 18 Ekim 2026 20:05 CEST — 02/04 gerçek CI incelemesi (kabul açık)
- İncelenen dal HEAD: `dd5fcea532438cfa5ec431cd5398e5b4b0c5a9e9`. MADSC 05 run [39148820745](https://github.com/Madsc55/madsc-tv/actions/runs/39148820745): 5 jobdan **3 success, 2 failure** (K1 ve K5). Beş artifact mevcut; aynı SHA hızlı ön kontrol [39148820738](https://github.com/Madsc55/madsc-tv/actions/runs/39148820738) success, beşli kabul değildir.
- **04 güvenlik bağımlılık açığı:** merkezî K2–K4 çağrıları `always()` yüzünden K1 başarısız olsa da çalışmış. Mevcut `test_central_stages_stop_after_failed_dependency` regresyonu iki job logunda da başarısız. Öncelikli düzeltme: 2–4 kademelerinin `needs.<önceki>.result == 'success'` koşulu; K5 başarısızlığı ve kanıt artifact'larını toplamaya devam etmeli.
- **K1 kabul engeli:** 26 kuralın 26/26 üretim enforcement kanıtı yok; `runtime_enforcement_verified=false` kayıtları fail-closed. Statik envanter veya artifact, 92 workflow'un davranışsal eşdeğerliği değildir (**0/92**). Dört tarihsel korunan EPG farkı onaysız değiştirilmeyecek.
- Yeni commit sonrasında SHA/run ID'si henüz kanıtlanmadı. **02–04 açık**; 200 maddelik kuyruk kapanmadı. Sıradaki iş: yeni SHA Actions K1/K5 sonucu, 26 kural eksik kanıtları ve 92 risk artifact içerikleri. Korunan dosyalar, main ve PR #71 değiştirilmedi.


### 18 Ekim 2026 21:10 CEST — SHA 0a8ec784 için gerçek CI ve günlük kanal rotasyonu regresyonu
- İşlem öncesi HEAD: `0a8ec784748558c03cb44549b8aab48efd86c95a`. Hızlı ön kontrol run [39155725676](https://github.com/Madsc55/madsc-tv/actions/runs/39155725676) **failure** (job 117758435690); beşli run [39155725642](https://github.com/Madsc55/madsc-tv/actions/runs/39155725642) **failure**. K1 job 117758435348 failure, K2–K4 skipped, K5 job 117758502736 failure. Üç artifact mevcut: hızlı 12146309776, K1 12146806835, K5 12147041321; artifact varlığı başarı değildir.
- Hızlı/K1/K5 loglarında aynı statik regresyon: `test_central_shadow_schedules_preserve_legacy_cadence` eski `40 6 1,15 * *` cron'unu bekliyor, oysa K3 yeni salt-okunur günlük `40 6 * * *` rotasyonunu kullanıyor. Güvenli düzeltme: **yalnız test beklentisini gerçek günlük rotasyonla uyumlu yap**, 123 sentetik satırın üç günde birer kez kapsanmasını test et; eski 1/15 eşdeğerliğini onaylama. Workflow cron'u ve korunan veriler değiştirilmez.
- K1 raporu: **0/26 runtime verified, 14 kısmi, 12 kanıt eksik**; K1'in fail-closed kararı doğrudur, yeşile çevrilmez. K1 bütünlük logu **136 korunan dosya, changed_paths=[]**. K5 bağımlılık ve kategori kanıtı bu nedenle kapalıdır.
- Yeni test+not commitinin SHA ve gerçek Actions sonuçları bu kayıt yazılırken **henüz yoktur**; yeni SHA'nın run/job/log/artifact sonucu ayrıca doğrulanmalıdır. **İlk açık iş 02:** güncel SHA'da regresyonun sonucu; ardından 26 kuralın gerçek enforcement kanıtı, 92 eski workflow yazma/dispatch ve çift tetikleme denetimi (03–04). Davranışsal kabul **0/92**; IBO gerçek cihaz ve harici restore bekliyor. main, PR #71, eski 92 workflow, EPG, playlist, logo ve arşivler değiştirilmedi.
