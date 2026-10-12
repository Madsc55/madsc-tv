# Tüm listenin logo kontrolü — 12 Ekim 2026

Kontrol 12:53 Stockholm saatinde tamamlandı. Ana dosyadaki tüm kategoriler tarandı: **1.029 liste kaydı, 191 farklı logo adresi**. Kategorilerdeki tekrarlar kayıt sayısına dahildir.

- Logo adresi boş kayıt: **0**. Bu, tüm logoların IBO cihazında göründüğünü kanıtlamaz.
- Görsel dosyası açılan adres: **182**; 985 liste kaydında kullanılıyor.
- SVG yapısı doğrulanan adres: **1**; 2 kayıtta kullanılıyor.
- HTTP hatası alınan adres: **8**; **42 kaydı, 10 kanal adını** etkiliyor. 403/429 hataları kalıcı bozukluk veya cihazda görünmeme kanıtı değildir.

| Kanal | Resmî kaynakta bulunan aday | Yayın karesi / görsel doğrulama |
|---|---|---|
| TLC | PNG indirildi | Kare alınamadı; eşleşme bekliyor |
| Dream Türk | PNG indirildi | Kare alınamadı; eşleşme bekliyor |
| PowerTürk Akustik | PNG indirildi | Kare alınamadı; eşleşme bekliyor |
| PowerTürk Slow | PNG indirildi | Kare alınamadı; eşleşme bekliyor |
| PowerTürk Taptaze | PNG indirildi | Kare alınamadı; eşleşme bekliyor |
| Baku TV | Resmî WebP görseli PNG olarak kaydedildi | Kare alınamadı; eşleşme bekliyor |
| TRT Diyanet Çocuk | SVG indirildi; PNG hazırlığı bekliyor | Kare alınamadı; eşleşme bekliyor |
| Spacetoon Turkey | Doğru aday henüz doğrulanmadı | Kare alınamadı; eşleşme bekliyor |
| BBC First Türkiye | Doğru aday henüz doğrulanmadı | Kare alınamadı; eşleşme bekliyor |
| TRT EBA Ortaokul | Doğru aday henüz doğrulanmadı | Kare alındı; amblem eşleşmesi doğrulanmadı |

## Tamamlanan ve kalan işler

Hunat TV'nin yazılı ve renkli amblemli yatay PNG'si Hepsi ve Yerel'deki iki kayda bağlandı. Yukarıdaki adaylar ayrı tutuldu; mevcut logolar değiştirilmedi.

Otomatik işlem günde iki kez tüm listedeki logo adreslerini denetler. Logo adresi boş olan kanallar için tam kanal kimliği veya tekil tam isim eşleşmesiyle kaynak arar; PNG'yi tercih eder ve diğer kaynakları da dener. **Bir PNG'nin indirilmesi görsel eşleşme sayılmaz**. Otomatik ekleme için kaydedilmiş görsel doğrulama ve PNG dosyasının SHA-256 özeti gerekir. Doğrulanmayanlar isimleriyle raporlanır.

Sorunlu logo adreslerini kullanan kanallardan yayın karesi alma adımı eklendi. Kareler inceleme için saklanır; otomatik görsel eşleşme yapıldığı iddia edilmez. Kare alınamayanlar sonraki çalıştırmada yeniden denenir. Tüm kanalların görsel kimlik karşılaştırması henüz tamamlanmış değildir.

Kanal isimleri, yayın adresleri, kategoriler, sıralama ve mevcut logolar korunur. PNG adayları `logo_deneme/candidates/` içinde, kaynak adresleri `sources.json` dosyasında tutulur.
