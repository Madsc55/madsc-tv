# Ayrı logo denetimi

Bu denetim CALISANLAR.m3u dosyasını yalnız okur. Ana liste, YENILER, yedekler ve kanal doğrulama akışına yazmaz. Yinelenen logo adresleri ağda bir kez kontrol edilir; sonuç her ilgili liste kaydına bağlanır.

rapor.json kanal bazında, ozet.json toplamları içerir. IMAGE_OK gerçek raster resim açma ve çözme kontrolüdür. SVG_XML_OK yalnız SVG XML yapısını doğrular, görsel işleme veya cihaz desteğini kanıtlamaz. HTTP_ERROR, NETWORK_OR_TLS_ERROR, NOT_DECODABLE_IMAGE ve MISSING_LOGO ayrı raporlanır. Ağ hatası kalıcı bozuk logo kanıtı değildir.

Bir resmin açılması, doğru kanalın logosu olduğunu veya IBO Pro cihazında görüntüleneceğini kanıtlamaz. Bu alanlar NOT_VERIFIED olarak korunur. Yayın bağlantıları rapora alınmaz, logo adreslerinin sorgu parametreleri ve kullanıcı bilgileri maskelenir. Denetim sırasında logo değiştirilmez.

Yerel denetim için Python ve Pillow gerekir; yeni zamanlanmış iş kurulmamıştır.
