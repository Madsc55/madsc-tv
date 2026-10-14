# MADSC — İki toplu kabul aşaması (14 Ekim 2026)

## Kullanıcı kararı
Tek tek küçük test döngüleri yerine kalan değişiklikler bir paket halinde hazırlanacak. Kullanıcıya her dosya sonrası test yaptırılmayacak. Gereksiz Actions koşuları ve tekrarlayan bildirimler önlenecek.

## Aşama 1 — Hazırlık ve toplu doğrulama
- 92 eski workflow için görev, script, tetik (cron/push/workflow_run/dispatch), izin, çıktı/artifact ve bağımlılık matrisi; eşleşmeyenler açıkça BLOCKED.
- Güvenlik, keşif, yayın/EPG/logo, arşiv/yedek ve genel bakım regresyonlarını aynı kabul zincirinde denetle.
- Kategori-5 işi ilk dört kategori sonucunu `needs` üzerinden okumalı. Önceki #15 yanlış negatifinin nedeni eksik `needs` idi; düzeltilmiş sürümün canlı sonucu ayrıca kontrol edilecek.
- Korunan CALISANLAR.m3u, favoriler, ⭐ YENİLER, logolar, kanal sırası ve yedekler değişmez. İşler salt okunur veya izole test edilir.
- Eksikler bir araya getirilip toplu commit hazırlanır. Her küçük dosya değişikliğinden sonra ayrı test talep edilmez.

## Aşama 2 — Tek nihai beşli kabul koşusu
- Tek `MADSC 05 - Genel Bakim Toplu` çalıştırması: Güvenlik → Keşif → Kanal Testi → Arşiv/Yedek → Genel Bakım.
- 5/5 jobs success; regresyon ve rapor adımları success; korunan dosya SHA256 kontrolü success; 5 rapor artifact'ı incelenir.
- 92 satırlık raporda `migration_blocked_count`, `behavioral_parity_verified_count`, eşleşmeyen betikler ve yüksek riskli eski otomasyonlar ayrıca değerlendirilir. Bunların sıfırlanmaması 5/5 CI başarısını '92 görev taşındı' anlamına getirmez.
- EPG→Pages, günde iki keşif, VOD, harici geri yükleme ve IBO cihaz onayı canlı kanıt olmadan tamamlanmış sayılmaz.
- Bir hata çıkarsa aynı kapsamlı denetim tekrar tekrar başlatılmaz: loglar toplanır, bütün ilişkili hatalar tek paketle düzeltilir, sonra kabul yeniden denenir.

## Geçiş kapısı
PR #71 ancak 92/92 görev davranışsal eşdeğerlik, eski üretim tetik ve yazma bağımlılıkları, harici restore ve kullanıcı onayı gerektiren alanlar için kanıtlar hazır olunca geçişe adaydır. Aksi halde eski 92 workflow çalışmaya devam eder; silinmez veya kapatılmaz.

## Şu an doğrulanmış durum
- Geçmiş 5/5 başarılı Actions koşusu mevcut.
- #15 koşusunda ilk dört kategori yeşil, beşinci kategoride yanlış negatif `needs` hatası kullanıcı ekranında doğrulandı.
- `needs` düzeltmesi kodda mevcut; son canlı koşunun başarısı burada doğrulanmış değildir.
- Kalan işlerin tek bir CI koşusunda *tamamlandığı* iddia edilmez; tek CI koşusu yalnız denetimi toplulaştırır.

## Sonraki toplu entegrasyon paketi (15 Ekim)
Bu paket mevcut kabul kosusu beklenirken hazirlanir. Her adimdan sonra kullanicidan test istenmez.

1. Canli uretim zinciri: EPG-Pages workflow_run, dokuz cron, push, yazma izinleri, artifact, secrets ve bagimliliklarin eski-yeni esdegerligi.
2. Guvenlik: 18 gorev ve 26 kural, yazma kapisi, korunan dosyalar ve yetki regresyonu.
3. Kesif: 75 aday, 4 alternatif, tekrar eleme, farkli saatlerde tekrar deneme ve gunde iki kesif tetigi; playlist'e yazma yok.
4. Kanal testleri: ffprobe/yayin, logo, kalite, EPG ve Pages yayin kaniti; IBO cihaz kabulunu ayrica koru.
5. Arsiv: izole geri yukleme, harici yedek kaniti, korunan backup'lara yazmadan geri donus provasi.
6. Genel bakim: dort kategori, 92 gorev esdegerlik matrisi ve cift tetik denetimini tek kabulde birlestir.
7. Tek toplu kabul: girdi, cikti, yan etki, izin ve tetik esdegerligi; ardindan 5/5 CI ve canli zincir kanitlari.

Her eski workflow icin yeni kategori sahibi, somut kod karsiligi, test veya canli kanit, rollback ve eksik gereksinimler yazilmadan durum BLOCKED kalir.
Betik ismi eslesmesi, yesil denetim veya bes kategoriye etiketleme eski gorevin tasindigini kanitlamaz.
EPG-Pages, harici restore ve IBO kabul kaniti olmadan PR birlestirilmez; eski workflow kapatilmaz.
Sonuc kullaniciya tek raporda: tasinan islev, eksikler, toplu test ve canli kabul gereksinimleri.
