# MADSC — 92 workflow eşdeğerlik kontrolü (2026-10-14)

## Doğrulanan
- PR #71 dalı: `madsc/bes-sistem-toplu-birlestirme`.
- GitHub Actions run `38630252033`, commit `a1473f868ff40b55740a751e8e39b759ddeec8a0`: beş kategori işi de `success`.
- Beş ayrı rapor artifact'i oluşmuş: güvenlik, keşif, kanal testleri, arşiv/yedek, genel bakım.
- Kanal test işi salt okunur 50 kanallık partiyi kontrol etmiş. Bu, tüm kanalların yayın doğrulaması değildir.

## Eşdeğerlik için zorunlu kapılar
1. Eski 92 workflow'un her biri için dosya adı, tetikleyici, zamanlama, izinler, okunan/yazılan dosyalar, dış bağımlılıklar, başarısızlık davranışı ve ürettiği artifact'leri envantere yaz.
2. Her eski workflow'u beş kategoriden birine eşle; birden fazla kategoriye giren işleri alt görevlere ayır. Eksik ve belirsizleri `ESDEGERLIK_BEKLIYOR` olarak işaretle.
3. Özellikle ana listeye yazabilen yedek geri yükleme, ayrı günlük EPG ve yalnızca bildirim veren otomatik devam işlerini manuel incele.
4. Her görev için aynı girişlerle eski/yeni çıktı karşılaştırması, hata durumları ve korunan dosya hash karşılaştırması yap.
5. Eski workflow'ları ancak kanıtlanmış eşdeğerlik ve açık kullanıcı onayı sonrası kapat; silme.

## Koruma
`CALISANLAR.m3u`, favoriler, ⭐ YENİLER, logo ve yedekler değiştirilmeyecek. Bu belge yalnızca izleme amaçlıdır; hiçbir eski workflow'u kapatmaz.

## Durum
Beşli toplu denetim: **GEÇTİ**. 92/92 görev eşdeğerliği: **HENÜZ KANITLANMADI**. Sonraki iş: dosya bazlı 92 satırlık envanter ve eşdeğerlik matrisi.
