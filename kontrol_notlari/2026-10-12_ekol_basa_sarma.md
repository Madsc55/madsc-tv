# Ekol yayın sürekliliği sorunu

Kontrol: 12 Ekim 2026, 00:52 Europe/Stockholm.

Kullanıcı bildirimi: Ulusal kategoride Ekol Sports ve Ekol TV yayınlarında program başladıktan sonra başa dönme. Kullanıcı sıra numaraları 55–59; güncel CALISANLAR.m3u dosyasında isimle eşleşen kayıtlar 57–61. Sıra farkı nedeniyle kayıtlar kanal adıyla belirlendi.

- EKOL SPORTS 1, EKOL SPORTS 2, EKOL SPORTS: aynı CDN ve ekolsport kaynağı. 1080p adresine autoplay=1 eklemek aynı içeriği döndürüyor. Ana adresin 1080p seçeneği de aynı adrese yönlendiriyor.
- EKOL TV 1, EKOL TV: aynı CDN ve ekoltv kaynağı. Ana adresin 1080p seçeneği aynı adrese yönlendiriyor.
- 22:52:04 ve 22:52:36 UTC örneklerinde beş adresin içerik özetleri değişmedi. 1080p yayın parça sıra numaraları sabit: Sports 2944135, TV 3591505.
- Her 1080p listede 180 parça, yaklaşık 30 dakika içerik var. ENDLIST işareti yok. Yanıt Last-Modified: 19 Haziran 2026. Son parça dosya adlarındaki Unix zamanları 25 Mayıs 2026 tarihine karşılık geliyor; bu adlandırma tek başına içerik tarihini kanıtlamaz.
- İki kaynağın son video parçaları HTTP 200 ile açıldı; dolayısıyla bağlantı açılması güncel canlı yayın olduğunu kanıtlamıyor.

Sonuç: Kullanıcı tarafından sorunlu bildirilen yayınlar. Kısa örneklerde canlı parça listeleri ilerlemiyor; durmuş/eski kaynak, başa sarma için güçlü açıklama. IBO cihazında tekrar anı ve tam döngü süresi burada gözlenmedi. Kesin tekrar süresi veya cihaz kaynaklı ek etki doğrulanmadı.

Ana liste ve kanal URL'leri değiştirilmedi. Mevcut üç aşamalı doğrulama değiştirilmedi. Bu kayıtları yalnızca kısa görüntü/ses testi geçti diye sorunsuz saymamak gerekiyor. Yeni kaynak bulunduğunda canlı parça ilerlemesi ve uzun süreli oynatma ayrıca doğrulanmalı; ana liste değişikliği kullanıcı onayı gerektirir.
