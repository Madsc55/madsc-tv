# K4 — Gerçek bağımsız yedek geri yükleme kabulü

Bu belge yalnızca **gerçek** GitHub dışı, tarihsel yedek için uygulanır. Örnek/sentetik TAR, aynı commit'ten oluşturulmuş Git arşivi veya başarılı Actions testi bu kabulü sağlamaz.

## Girdi ve yetki
- Yedek sorumlusu, bağımsız depolama sağlayıcısını ve yedeğin özgün nesne kimliğini (gizli erişim anahtarı olmadan) kayıt altına alır.
- Arşivin alındığı tarih/saat, saklama konumu, kaynak sistem/sürüm ve yedeğin oluşturulma yöntemi doğrulanır.
- İlgili tarihsel yedeğe ait, arşivden bağımsız olarak saklanmış SHA-256 manifesti sağlanır. Manifestin kaynağı ve güvenilirliği ayrıca incelenir.
- Korunan listeler, favoriler, logolar ve üretim dizinleri üzerinde yazma yetkisi kullanılmaz. Arşiv ve manifest mümkünse salt okunur bağlanır.

## İzole geri yükleme denemesi
1. Yetkili operatör yedeği geçici izole çalışma alanına alır; orijinal arşiv değişmez.
2. `python3 scripts/k4_external_restore_verify.py /guvenli/konum/yedek.tar.gz /guvenli/konum/manifest.json` çalıştırılır.
3. Komutun çıkış kodu ve JSON çıktısı, arşiv SHA-256 özeti, manifest SHA-256 özeti, depolama nesne kimliği, zaman damgası, operatör ve çalıştırılan kod commit'i kanıt paketine kaydedilir. Gizli anahtarlar, token'lar ve özel URL'ler rapora eklenmez.
4. Bağımsız yedeğin **tarihsel** sürüm içerdiği, yedek alma kayıtları veya sürüm bilgisiyle ayrıca doğrulanır. Üretim geri dönüşünün kabulü gerekiyorsa izole ortamda uygulama açılış/okuma kontrolleri de uygulanır.
5. Gerçek yedek içeriği, manifesti veya erişim bilgileri herkese açık PR'a yüklenmez.

## Kabul kapıları
| Kapı | Geçme şartı |
|---|---|
| Arşiv bütünlüğü | Doğrulayıcı çıkış kodu 0 ve `supplied_archive_integrity_verified=true` |
| Harici kopya | Bağımsız depolama kimliği ve kaynak kanıtı |
| Tarihsel geri dönüş | Tarih/sürüm ve tarihsel içerik kanıtı |
| Üretim kurtarma | Gerekliyse izole uygulama fonksiyon testleri |
| K1–K5 kabulü | Merkezi koordinatörün diğer sistemlerin ayrı test sonuçlarını doğrulaması |

**Önemli:** K4 doğrulayıcısının `external_backup_verified=false` ve `historical_recovery_verified=false` değerleri kasıtlıdır. Bu alanlar yalnızca bir TAR dosyası doğrulandığı için otomatik olarak `true` yapılmaz. Gerçek kabul, bağımsız kanıt paketi üzerinden ayrıca verilir.

## Mevcut durum
25 Ekim 2026 itibarıyla depoda doğrulanmış bağımsız tarihsel yedek ve manifest sunulmadı. Dolayısıyla gerçek geri yükleme kabulü **BEKLİYOR**; mevcut başarılı CI yalnız kod/regresyon testini doğrular.
