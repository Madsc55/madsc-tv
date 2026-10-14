# MADSC — Beş Kategori Toplu İş Defteri
Tarih: 14 Ekim 2026. Kaynaklar: DEVAM_NOTU.md, TOPLU_DURUM_RAPORU.md, BES_SISTEM_GECIS_KONTROL.md ve 92 GitHub workflow tetik envanteri.
Bu defter kalan işleri korur; doğrulanmayan işleri bitmiş saymaz.

## Çalışma kararı
- Beş bağımsız kategori vardır. Her kategorinin bütün kontrol/test işleri **tek workflow_dispatch ile bir toplu koşuda** yürütülür.
- Kategorilerin tamamını bir kerede test etmek gerekirse tek merkezden 1→2→3→4→5 zinciri çalıştırılabilir; **her kategori ayrı rapor/artifact** üretir.
- Tek tek günlere yayılan tekrar testleri ve gereksiz push zincirleri istenmez. Ağır tarama yalnız gerekli olduğunda.
- Beşli paket PR #71 çalışma dalındadır; ana dala geçiş ancak kabul kapıları tamamlanınca.
- Korunan playlist, HEPSİ/favoriler, ⭐ YENİLER, kanal sırası/URL/kimliği, doğrulanmış PNG logolar ve arşivler izinsiz değişmez.

## 1 — Güvenlik (tek koşu)
- [x] Korunan dosyaların SHA256 kontrolü, yazma kapısı ve merkezi konsolidasyon regresyonları kategori workflow'una bağlandı.
- [ ] 92 workflow'un etkin izinlerini ve tüm dolaylı yazma yollarını tarayıp riskli işlere karar ver.
- [ ] 26 güvenlik kuralının uçtan uca kabul kanıtını kaydet.
- [ ] Canlı Actions başarı logu ve artifact'ını doğrula.

## 2 — Kanal keşfi (tek koşu)
- [x] Kaynak mutabakatı, tekrar ölçümü ve IBO aday kuyruğu mevcut merkezi betiklerle toplu denetime bağlandı.
- [ ] 06:00/18:00 UTC çalışan mevcut keşfin görevlerini yeni tek kategoriye kayıpsız taşı; eski cron'u eşdeğerlik olmadan kapatma.
- [ ] Kaynak canlılığı/lisansı, Türkçe-yabancı ayrımı, aday-alternatif ayrı değerlendirmesi, eksik aday PNG'leri ve kaynak/kimlik kanıtı.
- [ ] Keşif artefaktı ile aday havuzu güncelliğini ve otomatik tarama başarısını doğrula.

## 3 — Kanal testleri (tek koşu)
- [x] Kanal kimliği/EPG raporları, regresyonlar ve salt okunur 50 kanallık yayın sağlık partisi kategori workflow'una bağlandı.
- [ ] 75 adayın 51 farklı saat retesti ve 24 ffprobe başarısızının doğrulanması; 4 alternatif ayrı; sayılar farklı havuzlarla çakışabilir.
- [ ] Yayın, kalite HD/FHD, logo kimliği ve kanal bazında test sonucu; otomatik sonuçla kullanıcı IBO onayı ayrı.
- [ ] EPG XMLTV, 5 kanal pilotu, Pages yayın zinciri ve İsveç'teki IBO cihaz kabulünü ayrı doğrula (kullanıcı onayı bekliyor).
- [ ] Canlı stream testi kapsamı ve başarılı/başarısız kanıtını kontrol et.

## 4 — Arşiv ve yedekleme (tek koşu)
- [x] İzole Git restore, yedek kanıtı ve arşiv tutarlılığı denetimleri kategori workflow'una bağlandı.
- [ ] Çalışan/çalışmayan, kullanıcı onaylı/otomatik, alternatif ve yabancı listelerinin tarihsel kayıplara karşı kontrolü.
- [ ] Tarihsel 11762 kanal / 11742 URL sayımlarını güncel kaynaktan doğrula; sayılar kesin canlı kanal sayısı değildir.
- [ ] Ayın 1 ve 15'indeki yedek işlerini koordine et, harici bağımsız kopyayı ve gerçek geri yükleme kanıtını sağla.
- [ ] Korunan arşiv ve yedekleri silmeden/üzerine yazmadan bütünlük doğrulaması.

## 5 — Genel bakım ve raporlama (tek koşu)
- [x] Workflow envanteri, 18 görev, kalan iş analizi ve tek ekran raporu kategori workflow'una bağlandı.
- [ ] 92 workflow'un tam tetik/komut/artefakt/bağımlılık eşlemesi; mükerrer push, schedule ve workflow_run işlerini kanıtla.
- [ ] Ayın 1/15'inde güvenlik, sağlık, yedek ve bakımın tek koordinasyon zincirini doğrula.
- [ ] 18 görev, 26 güvenlik kuralı ve eski tüm talepler için eksiksiz kabul tablosu.
- [ ] Beş kategori canlı Actions sonucu, artifact'lar, başarısızlık kök nedeni ve tek Türkçe kapanış raporu.
- [ ] EPG/Pages/VOD ve bütün geçmiş işlevlerin yeni düzende kayıpsız çalıştığı kanıtlanınca eski tetiklerin geçişi.

## Kırmızı çizgiler ve durum
- **Henüz yapılmadı:** Beş kategori için başarılı canlı Actions koşusu, 92 görevin işlevsel eşdeğerliği, harici restore, tüm adayların canlı testleri, TV/IBO kabulü, eski 92 dosyanın beşe indirilmesi.
- **Yapıldı:** PR #71 üzerinde beş kategori için ayrı salt okunur toplu test girişleri ve tetik envanteri; ana liste ve korunan veriler değiştirilmedi.
- İş kapanışı için her satırın GitHub run/artifact veya kullanıcı cihaz kanıtı gereklidir. Yalnız dosya oluşturmak yeterli değildir.

## Canli CI kaniti — 14 Ekim 2026
- 5. Genel Bakim kategori workflow'u, commit d353918384b61629bfd0430f244028d7bd4ebf98 icin GitHub Actions run #38626522362 sonucunda **SUCCESS**. Run: https://github.com/Madsc55/madsc-tv/actions/runs/38626522362
- GitHub jobs API'de rapor kontrolleri, regresyon testleri, korunan dosya SHA256 kontrolu ve artifact yukleme adimlari ayri ayri **SUCCESS**.
- Bir onceki iki kategori-5 run'i da basarili (#38620022983, #38619953358).
- Bu yalniz kategori 5 icin CI kanitidir; kategori 1-4 canli testleri, 92 workflow islev esdegerligi, IBO EPG, harici restore ve 75 aday henuz tamamlandi sayilmaz.

## Yeni canli CI sonucu — 14 Ekim 2026
- GitHub Actions #38627233310 (commit 554cf2d6) **SUCCESS**; genel bakım job'u başarılı.
- Aynı koşuda 1 Güvenlik, 2 Keşif, 3 Kanal Testi, 4 Arşiv job'ları **SKIPPED**. Sebep: push olayı; bu dört iş sadece manuel workflow_dispatch ile başlıyor.
- Bu nedenle #38627233310 beşli tam toplu kabul kanıtı değildir. Eski 92 workflow'u silmek veya nihai geçiş yapmak için yeterli değildir.
- Kategori 1-4 bağımsız toplu workflow_dispatch ve workflow_call olarak hazır; 5. kategori manuel başlatıldığında bunları sırayla çağıracak şekilde bağlı. Canlı manuel başlatma ve sonuç kanıtı açık iş olarak kalır.

## Bes kategori gercek entegrasyon kaniti — 14 Ekim 2026
- **SUCCESS**: https://github.com/Madsc55/madsc-tv/actions/runs/38627719035 — commit c15b60f8.
- Github Actions jobs API'de 1 Guvenlik, 2 Kesif, 3 Kanal Testleri, 4 Arsiv/Yedek, 5 Genel Bakim job'larinin **besi de success**. Bu, bir merkezden sirayla cagrilabilen bes ayri kategori toplu workflow'unun teknik entegrasyonunu kanitlar.
- Bu sonucda var olan betiklerin rapor/regresyon kontrolleri ve kategori 3'un sinirli yayin saglik partisi calisti. Tum 92 eski workflow'un davranissal esdegerligi, 75 aday icin farkli saat testleri, bagimsiz offsite geri yukleme, IBO cihaz EPG kabulü veya ana dala gecis kaniti DEGILDIR.
- Sonraki adim: 92 workflow'un tek tek yeni kategori/gorev karsiligini ve eski otomatik tetik bagimliliklarini ispatla; ondan sonra kontrollu gecis yap.

## 14 Ekim — workflow envanterinin yeniden doğrulanması
- PR #71 dosya listesinde `scripts/five_category_92_workflow_audit.py` ve `BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md` bulundu ve içerikleri okundu.
- Statik betik 92 eski YAML bekler; sayısı değişirse hata verir, beş yeni `madsc-0N-` workflow'unu hariç tutar. Bu **çalıştırılmış envanter sonucu değil**, betik tasarımının doğrulanmasıdır.
- Tetik envanterinde dokuz cron workflow'u ve bir workflow_run Pages zinciri belgelenmiş. EPG, VOD, yedek ve çift tetiklenme riskleri eşdeğerlik kapısında açık kalır.
- Run #38630252033 için beş job `success` ve beş artifact kaydı GitHub API üzerinden doğrulandı. Bu yalnız toplu denetim başarısıdır.
- Sonraki kabul kapısı: üretilen `92_workflow_gorev_ve_kategori_haritasi.json` artifact'ının 92 kaydını ve yazma/tetik risklerini incele; her eski workflow için davranışsal eşdeğerlik kanıtını bağla. **Eski workflow kapatma/silme yetkisi verilmedi.**

## 14 Ekim — Toplu kategori eşleştirme hatası düzeltildi
- `scripts/central_workflow_inventory.py`: YEDEK_VE_KURTARMA artık kategori 4; EPG ve LOGO kategori 3. Güvenlik kategori 1 olarak korundu.
- `test_central_workflow_inventory.py`: bütün envanter öğelerinde bu eşleşmeleri zorunlu tutan regresyon testi eklendi.
- `.github/workflows/madsc-05-genel-bakim.yml`: yeni regresyon testi ve ilgili dosya değişiklikleri beşli toplu koşuya bağlandı; commit `0bcbcfeed3546b01052ad6a151a5c6d8f91a7242`.
- **CI kabulü bekliyor:** GitHub bağlayıcısı commit SHA için yalnız PR-tetikli koşuları listeleyebiliyor; push koşusunun en güncel sonucunu bu sorgudan kesinleştirmek mümkün değil. Eski run #38630252033 başarılı, ancak yeni kodu test etmiyor.
- Eski 92 workflow ve korunan kanal/yedek verileri değiştirilmedi. Davranışsal eşdeğerlik henüz onaylanmadı.

## 14 Ekim — Beşli testte çakışan push tetikleyicisi
- Kullanıcının GitHub ekranındaki Güvenlik regresyonu 30 testten 1 hata verdi: `scripts/central_workflow_inventory.py` değişimi hem `madsc-aylik-merkezi-denetim.yml` hem `madsc-05-genel-bakim.yml` tetikliyordu. Tek-merkez kuralı doğru olarak hata verdi.
- `madsc-05-genel-bakim.yml` push paths yalnız kendi YAML dosyasına indirildi; `workflow_dispatch` ve beşli çağrı zinciri korundu. Düzeltme `ab444fa1ce50f21f52f3452a715bcc25be4f2f1a`.
- CI sonucu henüz doğrulanmadan yeşil kabul edilmeyecek. Korunan dosyalar ve eski 92 workflow değiştirilmedi.
