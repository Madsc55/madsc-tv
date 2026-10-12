# MADSC-TV — Onaylı Güvenlik ve Kanal Koruma Kuralları
Onay: Kullanıcı, 13 Ekim 2026. Bu belge yeni kanal taşıma/silme/düzeltme izni değildir.

## Mevcut 19 kural
1. Ana listedeki hiçbir kanal açık kullanıcı komutu olmadan silinmez.
2. Mevcut kanal adı, URL, ID, logo ve kategori açık izin olmadan değişmez.
3. HEPSİ, FAVORİLER ve diğer korunmuş sıralamalar aynen kalır.
4. Kategori taşıma yalnız açık kullanıcı komutuyla yapılır.
5. ⭐ YENİLER'e onaysız kanal eklenmez; onaylı yeni kanallar alfabetik sıralanır.
6. Korunan yedekler izinsiz silinmez, değiştirilmez veya üzerine yazılmaz.
7. Silinen kanallar geri yüklenebilir geçmişte tutulur; veri kalıcı olarak kaybedilmez.
8. Kullanıcının IBO Player'da çalışıyor diye onayladığı kanallar ayrı kaydedilir.
9. Kullanıcının çalışmıyor dediği veya teknik testten geçemeyenler ayrı kaydedilir; geçmiş kaybolmaz.
10. Aynı URL'nin önceden yapılmış geçerli testi gereksiz tekrarlanmaz; geçmiş korunur. Zamanlı tekrar testi gerekiyorsa eski sonuç silinmez.
11. Aynı kanalın alternatif URL'leri ayrı aday incelenir; çalışan bağlantı otomatik üzerine yazılmaz.
12. Otomatik keşif yeni kanalları ve alternatiflerini araştırır, tekrarları ayıklar ve aday olarak kaydeder.
13. Teknik testte görüntü, ses, çözünürlük, süreklilik ve bağlantı durumu incelenir.
14. Yayın kimliği, teknik oynatma testinden ayrı doğrulanır.
15. Teknik başarı, kullanıcının İsveç'teki IBO Player cihazında çalıştığı anlamına gelmez; cihaz kararı ayrı tutulur.
16. Bekleyen adaylar otomatik sonraki gruplara geçer; bitmiş işler gereksiz tekrar edilmez.
17. Ana listeye ve korunan kategorilere ekleme, taşıma, düzeltme yalnız açık kullanıcı komutuyla yapılır.
18. Adaylar, başarılı/başarısız testler, kararlar ve değişiklik geçmişi saklanır.
19. Önemli adımlar ve sonraki işler DEVAM_NOTU.md'ye başlıklarıyla kaydedilir.

## Kullanıcı tarafından ayrıca onaylanan dört güvenlik önlemi
20. Onaylı düzenlemeden önce geri yüklenebilir dosya sürümü/yedeği alınır.
21. Keşif/test otomasyonlarının korunan listelere izinsiz yazması engellenir; denetim başarısız olmalıdır.
22. Onaylı düzenlemeden sonra M3U biçimi, kanal sayısı, sıra ve URL bütünlüğü kontrol edilir; beklenmeyen değişiklik yayımlanmaz.
23. Hata sonrası hangi sürüme dönüleceği kaydedilir; otomatik geri alma korunan kanalları sessizce değiştirmez.

## Uygulama durumu ve sınırlar
- Bu belge, 24 kuralın kullanıcı tarafından onaylanmış politika kaydıdır; her kuralın otomatik olarak teknik açıdan zorlandığı anlamına gelmez.
- test-39 mevcut durumda dosya varlığını ve M3U başlığını denetler; yazma izni kapısı değildir.
- test-31 yazma kabiliyetli iş akışlarını raporlar; gerçek izin kapısı değildir.
- GitHub branch ruleset / branch protection etkinliği ayrıca doğrulanmalıdır.
- Yeni güvenlik kodu geliştirilirken otomatik keşif, teknik test, rapor ve devam mekanizması bozulmamalı.
- Ek kurallar kullanıcıyla ayrıca değerlendirilebilir; otomatik olarak kabul edilmiş sayılmaz.

## 24. kural — Kullanıcı onayı: hata zincirini güvenle durdur
24. Aynı otomatik işlem art arda başarısız olduğunda sonsuz tekrar yapılmaz; ilgili iş güvenli biçimde durur, hata ve kaldığı aşama raporlanır. Ana liste, YENİLER, favoriler, HEPSİ sırası ve korunan yedekler değiştirilmez. Sorun giderildikten sonra geçmiş korunarak kaldığı yerden devam edilebilir.

**Uygulama incelemesi (13 Ekim 2026):** Son kontrol, birleşik keşif ve üç aşama iş akışlarında en fazla 10 git push denemesi ve hata halinde başarısız çıkış zaten vardır; son kontrolün otomatik devam adımı yalnız başarı halinde çalışır. Ancak bütün iş akışlarını kapsayan, birbirini izleyen başarısız çalışmaları sayıp otomatik durduran ortak devre kesici henüz doğrulanmadı. 24. kural politika olarak onaylandı; eksik teknik uygulama ayrıca test edilecektir.
