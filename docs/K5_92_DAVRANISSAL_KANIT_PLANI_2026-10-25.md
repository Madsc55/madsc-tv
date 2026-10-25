# K5 — 92 workflow davranışsal kanıt kabul planı (25 Ekim 2026)

Bu kayıt **üretim kabulü değildir**. K5'in mevcut 92 satırlık envanter kapısı tüm satırları BLOCKED_NEEDS_BEHAVIOR_EVIDENCE olarak doğruluyor. Bu kontrol, gerçek geçişin tamamlandığını göstermez.

## Kabul için satır başına zorunlu kanıt
- Eski workflow dosyası, tetikleyiciler, cron, concurrency, izinler, girişler, script çağrıları ve dış etkiler.
- K1–K5 karşılığı ve aynı girdilerde beklenen/gerçek çıktılar; başarısızlık, timeout, retry ve iptal davranışı.
- Korunan veri yazma yasağı, yetki kontrolü ve fail-closed negatif test.
- Aynı SHA'da gerçek GitHub Actions run/job/artifact kimliği, sonuç ve farklar.
- Cihaz, harici restore veya uzun süreli medya testi gereken işler için ilgili dış kanıt; statik tarama tek başına kabul değildir.

## Güvenli geçiş sırası
1. 92 satırın her birini kanıt bekleyen, test başarısız veya doğrulanmış olarak bağımsız sınıflandır.
2. Her doğrulanmış satır için tekrar üretilebilir test ve SHA-bağlı kanıt ekle. Kanıtsız satır BLOCKED kalır.
3. 26 runtime kuralı ve K1–K4 kapıları başarılı olmadan K5 tam kabul üretmez.
4. 92/92 ve 26/26 tamamlanmadan eski workflow kapatma, cron/izin değiştirme veya main merge yapılmaz.

## İlk incelemede tespit edilenler
- `.github/workflows/madsc-05-genel-bakim.yml` içindeki `audit_2` tüm 92 satırın BLOCKED olmasını sabit bekliyor.
- `audit_3` `migration_blocked_count == 92` ve `behavioral_parity_verified_count == 0` bekliyor.
- Bu iki kontrol, güvenli başlangıç durumunu korurken ileride kanıtlı kısmi kabulü de engeller. Değiştirilmeden önce satır-bazlı kanıt şeması, negatif testler ve fail-closed geçiş uygulanmalı.
- `scripts/acceptance_26_92.py` tam kabul için 92/92 ve K1 runtime kapısını ayrıca şart koşuyor; bu güvenlik şartı korunacak.

## Sınırlar
Ana liste, YENİLER, FAVORİLER, YEDEKLER, logolar, cihaz verisi ve arşiv değiştirilmez. PR #71 ve main birleştirilmez. IBO cihaz kabulü kullanıcıya aittir.

## Mevcut kanıt durumu
92/92 **doğrulanmadı**; K5 üretim kabulü **kapalı**. Bu doküman yalnız denetim ve uygulama sırasını kalıcılaştırır. Kod/test değişikliği yapılmadı.
