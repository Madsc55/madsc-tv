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
