# IPTV çalışma ve sohbet devir kuralları

Her yeni sohbette işleme başlamadan DEVAM_NOTU.md içindeki SOHBET DEVRİ bölümünü ve ilgili güncel Actions/raporları oku. Eski tarihli bölümler geçmiş kaydıdır; son dosya içeriği ve cihaz kararları esastır.

- Tamamlanan testler, kategori taşıma/sıralama ve verilmiş kimlik kararları tekrar uygulanmaz. Yalnız eksik ve zamanı gelmiş denemeler yapılır; geçmiş silinmez.
- Ana liste, YENİLER, favoriler/Hepsi korunacak sıraları ve korunan yedekler yalnız açık kullanıcı izin kapsamıyla değişir. Ana listedeki dolu logo alanlarına dokunma; aday PNG hazırlığı ayrı tutulur.
- Teknik test, görsel kimlik ve kullanıcının İsveç IBO cihazı sonucu ayrıdır. Kullanıcı ADA/Kanal D reddi eski otomatik/görsel desteğin önündedir.
- Her önemli işlem/test sonucu/kullanıcı kararı sonrası DEVAM_NOTU.md güncel SOHBET DEVRİ bölümünü güncelle; ilgili commit/run/rapor kanıtı, tarih, tamamlananlar ve sıradaki iş dahil edilir.
- Kullanıcı sohbet dolduğunu/yeni sohbete geçeceğini veya devir notu istediğini belirtirse önce mevcut durumu kalıcı kaydet ve sonucu doğrula. Devir için test başlatma.
- Sohbetin kesin dolma eşiği veya kalan ChatGPT kota/mesaj/fotoğraf sayısı görünmüyorsa uydurma veya otomatik erken uyarı garantisi verme. Uzun çalışma bloklarında proaktif kısa kayıt yap.
- Kaydetme ya da yanıt iletimi başarısızsa işlem tamamlandı varsayma; yeni sohbet son doğrulanmış kalıcı kayıttan devam eder.

- Kullanıcının 13 Ekim'de onayladığı 23 maddelik koruma politikası `GUVENLIK_KURALLARI.md` dosyasındadır. Onaylı politika, ana listeyi değiştirme izni değildir. Yeni kurallar ayrıca kullanıcıya sorulur.

## Özellik tekrarı önleme — zorunlu ön kontrol
Yeni özellik önerilmeden, yeni script/workflow eklenmeden veya mevcut iş yeniden yazılmadan **OZELLIK_ENVANTERI.md** okunur; mevcut kod, ilgili iş akışı ve son gerçek Actions sonucu incelenir. Mevcut ve başarılı işi tekrar kurma. Eksikse yalnız eksik parçasını geliştir. Pilot EPG ile tam EPG'yi, kod testini gerçek cihaz testini birbirine karıştırma. İş bitince envanterin durumunu ve DEVAM_NOTU.md kanıtlarını güncelle. Bu kural korunan dosyaları değiştirme izni vermez.

## Kural 25: Değişiklik sonrası test
Her yeni değişiklikten sonra ilgili GitHub Actions testi tetiklenir. Gerçek run kimliği ve sonucu doğrulanmadan başarılı denmez. Korunan listeler izinsiz değiştirilmez.

## Kural 26: Test adları Türkçe
Bundan sonra eklenen veya düzenlenen GitHub Actions testlerinin kullanıcıya görünen workflow, iş (job) ve adım (step) adları Türkçe yazılır. Mevcut çalışan teknik dosya yolları, script adları, test fonksiyonları ve GitHub Actions anahtarları yalnız çeviri amacıyla değiştirilmez. Var olan testler yalnızca gerekli değişiklik yapıldığında Türkçeleştirilir; sırf isim değiştirmek için başarılı otomasyonlar yeniden kurulmaz. Her isim değişikliği Kural 25 kapsamında doğrulanır.
