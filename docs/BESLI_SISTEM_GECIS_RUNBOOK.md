# MADSC TV — Beşli sisteme güvenli geçiş işletim planı

Bu belge **geçiş yetkisi değildir**. Mevcut üretim listeleri, EPG, logo, yedek ve 92 eski workflow korunur. Ana dal ve PR #71 değiştirilmez.

## Mimari
- **K1 Güvenlik:** 26 kural, korunan dosya kapısı, yazma yetkileri, başarısızlık devre kesicisi.
- **K2 Keşif:** aday keşfi, geçmiş, geniş tarama; salt okunur gölge çalışma.
- **K3 Kanal testleri:** yayın/kimlik/EPG/logo/IBO aday raporları; cihaz kabulü otomatik sayılmaz.
- **K4 Arşiv ve yedek:** izole geri yükleme, hash ve harici kopya ayrımı.
- **K5 Genel bakım:** kategorileri sırayla çağırır, sonuçları ve kanıtları toplar, eksikleri raporlar.

## Gölgede çalıştırma
1. Dalda `madsc-05-genel-bakim.yml` workflow_dispatch ile çalıştırılır; kategori raporları ve `besli_sistem_gecis_hazirlik.json` artifact olarak incelenir.
2. Bir kategori başarısızsa sonraki salt okunur denetimler yine yürütülür; **genel kabul başarısız kalır**. K5'in dört başarılı kategori kanıtı istemesi geçiş için korunur.
3. Kanıtlar aynı commit SHA, aynı run ID, job sonuçları, rapor hash'leri ve gerçek çıkış kodlarıyla eşleştirilir. Önceki koşu yeni SHA için kabul sayılmaz.
4. `python3 scripts/five_system_cutover_readiness.py` ve `python3 -m unittest discover -s tests -p 'test_five_system_cutover_readiness.py' -v` geçiş engellerini raporlar. Raporun `cutover_allowed: false` değeri otomatik onay verilemeyeceğini gösterir.

## Üretime geçiş öncesi zorunlu kapılar
- K1 26/26 **gerçek uygulama kanıtı** ve korunan EPG farklarının yetkili çözümü.
- 92/92 eski workflow için aynı girdi, komut, tetik, izin, çıktı, hata davranışı ve bağımlılık eşdeğerliği; çift push ve cron yarışları incelenmiş olmalı.
- K2–K5 için güncel SHA üzerinde başarı; EPG üretimi → Pages dağıtımı ve gerçek erişim zinciri doğrulanmalı.
- Bağımsız **GitHub dışı** yedekten izole geri yükleme, checksum ve geri dönüş süresi kanıtı.
- IBO Player Pro cihazda kanal oynatma, ses, görüntü, EPG, logo ve kararlılık kullanıcı tarafından onaylanmalı.
- Varsayılan dalın cron davranışı, yetkiler, branch protection ve üretim dağıtımı doğrulanmalı.
- Kullanıcının **açık geçiş onayı** ve geri alma planı olmadan hiçbir legacy workflow kapatılmaz.

## Aşamalı geçiş ve geri alma
1. Gölge: yalnız rapor ve karşılaştırma, korunan dosyalara yazma yok.
2. Kanıt: kategori bazlı davranışsal karşılaştırma ve tekrarlı başarılı koşular.
3. Onay: her eski workflow için geçiş/geri dönüş eşlemesi; kullanıcı onayı.
4. Kontrollü devralma: yalnız onaylı tek bir üretim yazıcısı ve zamanlayıcısı; çakışma önleyici concurrency.
5. İzleme: en az 24 saat, ardından 7 gün üretim kanıtı ve cihaz testi.
6. Geri alma: yetkili karar ve kayıtlı SHA ile önceki workflow yapılandırmasına dön; **korunan listeleri, EPG'yi veya yedekleri otomatik resetleme**. Sorun halinde üretim yazımını durdur, mevcut çıktıları koru, kanıtları arşivle ve kullanıcı onayıyla ilerle.

## Mevcut açık durum — 18 Ekim 2026
- 26 kural: 0/26 gerçek çalışma kanıtı, 14 kısmi, 12 kanıt eksik (son incelenen artifact).
- 92 legacy davranışsal eşdeğerlik: onaylanmış 0/92.
- `epg/ibo-test-epg.xml`, `epg/madsc-epg.xml`, `epg/report.json`, `epg/tv_kontrol_bekliyor.json` dallar arasında farklı.
- Yeni kodun güncel GitHub Actions sonucu henüz doğrulanmadı. **Üretim geçişi engelli**.

## 18 Ekim 2026 — EPG erteleme ve mevcut durumu koruma kararı
Kullanıcı kararı: mevcut ve yeni EPG dosyaları **aynen korunacak**. EPG üretimi, dosya düzeltmesi, içerik güncellemesi, silme, reset ve EPG/Pages geçiş kabulü şimdilik **ERTELENDİ**. EPG ile ilgili önceden yapılmış işler geri alınmayacak. Korunan EPG farkları bilinen açık konu olarak raporda kalır; kullanıcı onayı olmadan çözüm amaçlı dosya değiştirilmez. EPG işlerini daha sonra aynı mevcut dosyalar üzerinden sürdür.

Öncelik K1/K2/K3/K4/K5'in EPG dışındaki altyapısı, 92 eski workflow'un davranışsal eşleştirmesi, CI ve yedek kanıtlarıdır. EPG gerektirmeyen gölge denetimler devam edebilir. EPG/Pages doğrulaması tamamlanmış gösterilmez ve nihai üretim geçişi otomatik onaylanmaz. Eski workflow'lar, main ve korunan yayın listeleri korunur.


## 18 Ekim 2026 — K1-K5 calisma devri ve sonraki isler
- Dal: `madsc/bes-sistem-toplu-birlestirme`. `main`, PR #71, eski uretim workflow'lari, korunan kanal listeleri, EPG, logolar ve arsivler degistirilmez.
- Ortak statik denetim: `scripts/five_category_shared_controls.py`. K1-K5 icin korunan dosya snapshot/check ve SHA-256 referanslari; K5 icin kategori kaniti ve gecis hazirligi referanslari kontrol edilir. `tests/test_five_category_shared_controls.py` regresyonlari hizli on kontrolde ve K5'te calistirilmak uzere baglidir.
- Son kaydedilen test: K2 snapshot eksikliginde BLOCKED, commit `bf60b5111a0835a3c4f1d9f9d87fc64c954f2a9c`. K3 checksum eksikligi testi `005a693f55210afed9fbcdd9114003cb5d488d7a`. K4 check eksikligi testi denendi ama guvenlik kontrolu engelledi, kaydedilmedi.
- Statik denetim gercek komut calistirma kaniti DEGILDIR; 26 kuralin gercek uygulama kaniti ve 92 legacy davranissal esdegerligi hala acik. Son bilinen 0/26 tam dogrulama ve 0/92 esdegerlik, yeni sonuc olarak yorumlanmaz.
- Guncel GitHub Actions basarisi dogrulanmadi. Commit workflow run sorgusu yalniz PR kaynakli kayitlari gosterebilir; bos sonuc CI calismadi anlamina gelmez.
- Sonraki odak: (1) gercek CI run/job/artifact kanitlarini ayni SHA ile teyit et; (2) ortak denetimin snapshot/check/sha256 komutlarini yalniz metin varligi degil gercek komut eslesmesi olarak dogrulamasini sagla; (3) 92 eski workflow icin tetik, izin, komut, cikti, hata, rollback ve uretim yazicisi esdegerligini kategori bazinda kanitla; (4) 26 K1 kuralini tek tek runtime kanitina bagla. K1 degisikliginin K2-K5 etkisini birlikte ele al; ufak tekrarci testlerle yetinme.
- EPG kapsam disi ertelenmistir; mevcut ve yeni EPG dosyalarina dokunma, farklarini dogrulanmis sayma. Nihai cutover, eski workflow kapatma ve uretim yazma izni verilmedi.

## 18 Ekim 2026 — K1'e geri dönüş
Kullanıcı kararı: beşli sistemin ilk kategorisi olan K1 Güvenlik ve Sağlık önceliklidir. K2-K5 ilerlemesi korunur. K5 test commitleri: 00d5ba7, d5c58a6, 47975af. K3 test commitleri: 90ea2bc, ed213a4, bffde80, 329fce3, 85747a4.

K1 öncelikleri: aynı SHA üzerinde Actions run ve artifact doğrulaması; 26 kuralın gerçek uygulama kanıtı; korunan dosya bütünlüğü ve yazma kapıları; hata zinciri ve sağlık denetimi; eksiklerin toplu kapatılması. Son bilinen gerçek doğrulama 0/26, eski iş akışı eşdeğerliği 0/92. CI başarı sonucu doğrulanmış değildir. EPG ertelenmiştir; korunan dosyalar, main ve eski üretim akışları değiştirilmez.
