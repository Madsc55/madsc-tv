# IBO Player Pro için ayrı EPG denemesi

Hazırlık tarihi: 11 Ekim 2026. Bu paket ana listeyi, YENILER'i, yedekleri ve mevcut doğrulama akışını değiştirmez. Henüz IBO cihazına yüklenmemiştir.

Liste: https://raw.githubusercontent.com/Madsc55/madsc-tv/main/epg_deneme/liste.m3u

XMLTV: https://raw.githubusercontent.com/Madsc55/madsc-tv/main/epg_deneme/rehber.xml

TRT 1, TRT Haber, TRT Çocuk, TRT Avaz ve TRT Türk için mevcut listedeki kamuya açık TRT yayın bağlantıları ve tvg-id değerleri korunmuştur. EPG kaynağı açıkça seçilen kanal kimlikleriyle eşleştirilir; TRT 1/2 gibi numaralar silinerek yaklaşık eşleştirme yapılmaz. Kaynak XMLTV kimlikleri raporda bulunur. Bu eşleştirme içerik kimliğinin cihazda doğrulandığı anlamına gelmez.

Saatler XMLTV'de açık +0000 ile UTC olarak yazılır. Rapor Europe/Stockholm yaz/kış saatini kullanır; yayınların saatine elle bir saat kaydırma uygulanmaz. Sonbaharda saat değişimi de ZoneInfo ile hesaplanır.

rapor.json hazırlık anındaki eşleşmeyi, mevcut programı, süreyi, kaynakta reddedilen bozuk kayıtları, çakışmaları ve kapsam sonunu gösterir. Geçmiş/bozuk/aynı programın tekrar kayıtları deneme rehberine alınmaz. Kaynakta bozuk kayıt bulunması raporlanır; bunlar çıktıdaki programların geçerli olduğu kontrolüyle ayrı değerlendirilir.

Bu kaynak yalnız kısa süreli güncel program verisi veriyor: 11 Ekim akşamı kanal bazında 22:00–22:55 İsveç saatine kadar. Bu statik hazırlık paketini ileride kullanılmadan önce yeniden üretmek ve güncelliğini kontrol etmek gerekir. Günlük yenileme kurulmadı. Üç aşamalı doğrulama bitince cihaz denemesinden hemen önce Mahmut veriyi yenileyecek.

11 Ekim kontrolünde üretimdeki GitHub Pages XMLTV dosyası 135 kanal/10474 program içerirken depodaki dosya farklı ve daha günceldi. Üretim rehberindeki TRT 1 programları geçmişte bitmişti. Mevcut EPG oluşturucusunun birden çok isim eşleşmesinde en çok programı seçmesi ve belirsizlik alanını doldurmaması da ayrıca incelenmeli. Bu hazırlık mevcut rehberi veya yayımlama akışını düzeltmiş sayılmaz.

Sonraki başarı ölçütleri: mevcut üç denemeyi tamamlamak; tam cihaz/model, uygulama sürümü ve uygulamanın kendi destek adresine göre IBO Pro'ya ayrı deneme listesini bağlamak; beş kanalın doğru programını ve İsveç saatini cihazda görmek. Cihaza erişim olmadan cihazdaki görünürlük otomatik olarak doğrulanamaz. Bu paket yayın sürekliliği testi veya IBO başarı kanıtı değildir.

## 12 Ekim 2026 yenilemesi

Pilot güncel ana listedeki aynı kanal URL/ID değerleriyle yeniden üretildi. Üretim ana liste ve EPG değiştirilmedi. Kaynak akışta gece yarısından sonraki bitiş aynı güne yazılmıştı (ör. 20:00 → 00:15); yalnız aynı tarih/saat dilimindeki akşam → gece aralığı en çok 12 saat şartıyla sonraki güne çevrilir. Bu yorum raporun `source_time_repairs` alanında ilk değerleriyle saklanır; bağımsız yayın akışı veya IBO doğrulaması sayılmaz. Diğer ters süreler reddedilir. Beş kanalın teknik kimlik/saat/çakışma kontrolü geçti; cihaz görünürlüğü NOT_VERIFIED kalır. Güncel program ve kapsam süreleri `rapor.json` içindedir; paket kapsam bitince tekrar yenilenmelidir.
