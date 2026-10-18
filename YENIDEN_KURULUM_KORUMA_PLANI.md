# MADSC TV — Sıfırdan Beşli Sistem Kurulumu: Koruma Sözleşmesi

Karar: 18 Ekim 2026. Kullanıcı eski sorunlu uygulamayı temizleyip beşli sistemi sıfırdan kurmak istiyor. Bu karar mevcut kanal ve proje verilerini silme yetkisi DEĞİLDİR.

## Silinmesi yasak / öncelikle korunacak
- `main` dalı, üretimdeki çalışan sistem ve geçmişi; ayrıca PR #71 ve eski dal geçmişi geri dönüş imkânı için.
- `DEVAM_NOTU.md` (tam tarihçe ve tüm kullanıcı kararları), `AGENTS.md`, `GUVENLIK_KURALLARI.md`, `OZELLIK_ENVANTERI.md`; beşli sistemin amaçları ve 26 kural.
- Bütün M3U/M3U8 kanal listeleri, URL'ler, kanal adları, sıra ve kategori eşleştirmeleri; çalışan/çalışmayan/yeni/yabancı listeleri.
- Favoriler, HEPSİ, IBO Player düzeni, EPG/XMLTV, logo/görseller, arşivler, yedekler ve geri yükleme kayıtları.
- Yukarıdakileri üretmek veya anlamlandırmak için tek kaynak olan yapılandırma ve veri dosyaları; içerikleri doğrulanmadan silinemez.

## Yeni mimari
Beş kategori yeniden tasarlanacak: (1) güvenlik ve koruma, (2) keşif ve aday denetimi, (3) kanal/kategori ve veri işleme, (4) EPG/logo ve yayın hazırlığı, (5) yedekleme, geri yükleme ve doğrulama. Eski 92 workflow yalnız görev gereksinimleri açısından envanter kaynağıdır; doğrudan 92 ayrı workflow olarak yeniden kurulması zorunlu değildir. Mevcut `OZELLIK_ENVANTERI.md` ve önceki beşli sistem hedefleri yeni tasarımın girdisidir; hiçbir özellik sessizce kaybolmaz.

## Temizlik ön koşulları
1. Korunan yolların dosya bazında tam envanteri, SHA-256 manifesti ve geri yüklenebilir bağımsız yedeği oluşturulur; geri yükleme sınanır.
2. Silinecek her yol ayrı listeye alınır; veri ve çalışan üretim bağımlılıklarıyla çakışmadığı doğrulanır.
3. Temizlik yalnız yeni izole yeniden-kurulum dalında yapılır; `main` ve mevcut beşli çalışma dalı değişmeden kalır.
4. Yeni beşli sistemin testleri ve eşdeğer davranış kontrolleri yeşil olmadan eski otomasyonların üretimdeki çalışması kesilmez.
5. Gerçek cihaz, çalışma zamanı ve Actions kanıtı olmadan 26/26 veya 92/92 kabul iddia edilmez.

## Durum
Koruma kararı kayıt altına alındı. Bu dosya tek başına yedek veya silme işlemi değildir. Silme henüz başlamadı.
