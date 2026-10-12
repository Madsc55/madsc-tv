# TCL 55C655 / Ibo Player Pro 2128.0 — Salt Okunur Uyumluluk Denetimi

Tarih: 13 Ekim 2026. Kullanıcının ekran görüntüsü: uygulama adı **Ibo Player Pro**, sürüm **2128.0**, paket **com.storeahim.obiproplay**. Cihaz **TCL 55C655**, Google TV; kullanıcı İsveç'te.

## Doğrulanmış bulgular
- TCL teknik belge: https://aws-obg-image-lb-4.tcl.com/content/dam/brandsite/region/australia/AU_Mediacenter/download/55C655_Product_Specifications.pdf — USB ortam oynatımı için JPEG/PNG/BMP/HEIF, H.264/VP9/AV1 vb. listeleniyor. İsveç ürün kaynağı: https://www.elon.se/tcl-55-55c655-126858 — H.265 de listeleniyor. Bunlar Ibo Player Pro uygulamasının içindeki logo/kodek davranışını tek başına doğrulamaz.
- Aynı isimli farklı uygulamalar var: Google Play'de com.ibopro.iboplayerpro ve com.ibovpro.player görüldü; kullanıcının **com.storeahim.obiproplay** uygulamasıyla eşit tutulamaz. Farklı alan adlarındaki IBO açıklamaları bu paket için kesin geliştirici kanıtı değildir.
- CALISANLAR.m3u salt okunur envanteri: 944 tvg-id nitelikli kanal kaydı, 236 boş tvg-id, boş hariç 107 farklı tvg-id; tvg-logo içinde .webp uzantılı 35 bağlantı. Aynı tvg-id'nin kalite varyantlarında tekrar etmesi normal olabilir; hiçbir otomatik değişiklik önerilmez.
- Mevcut epg/report.json (2026-10-12T21:19:09Z) 1039 giriş, 728 kaynak eşleşmesi, 311 eşleşmeyen, 581 kullanılabilir playlist girişi, 17811 program, 6440179 byte EPG bildiriyor. Bu eski bir üretim anına aittir; güncel 944 kayıtla aynı anlık görüntü değildir. EPG kaynakları o üretimde erişilebilmiş, fakat IBO üzerinde EPG görünmemiştir.
- epg/ibo-test-epg.xml içinde TRT 1, TRT 2, SHOW TV, ATV, KANAL D kimlikleri ve program kayıtları bulunuyor. Test dosyasının varlığı IBO'nun bunu indirdiği anlamına gelmez.

## Öncelikli uygulanacak kontroller (önce salt okunur)
1. Aynı commit/snapshot üzerinden M3U ve XMLTV kanal kimliği/boş ID/çoklu eşleşme raporu oluştur; eski EPG raporuyla karıştırma.
2. XMLTV URL'si, HTTP durumu, Content-Type, XML parse, güncel program zamanları ve XMLTV ID eşleşmesini dışarıdan kontrol et. İndirmenin TV içinden başarılı olduğu ayrıca cihazda test edilmeli.
3. Logo URL erişimi ve gerçek Content-Type ile PNG/JPEG/WebP biçimlerini ayrı değerlendir. Sırf WebP diye mevcut logo değiştirme.
4. Akış kodek ve yayın sürekliliği raporunu cihazda onaylanan/başarısız diye ayır. GitHub bulut testi İsveç'teki TCL testi yerine geçmez.
5. IBO Player Pro 2128.0 ayarlarında ayrı EPG URL alanı ve yenileme davranışını kullanıcı ekranıyla doğrula; destek yanıtı gelmeden üretim EPG'sine dokunma.
6. Yalnız onaydan sonra bağımsız test playlisti veya kontrollü düzeltme planı hazırla; korunan listelere/iş akışlarına dokunma.

## Koruma
Bu dosya yalnızca araştırma ve salt okunur denetim kaydıdır. CALISANLAR.m3u, YENILER.m3u, FAVORİLER, HEPSİ, yedekler, mevcut EPG ve Actions otomasyonları değiştirilmedi.
