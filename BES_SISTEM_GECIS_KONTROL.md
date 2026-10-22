# MADSC — Beş ana otomasyona güvenli geçiş / çalışma sözleşmesi

Başlangıç: 14 Ekim 2026. Çalışma dalı: `madsc/bes-sistem-toplu-birlestirme`.

## Değişmez kabul koşulları
- Eski 92 workflow dosyası ve tüm görevleri incelenmeden hiçbir workflow silinmez veya devre dışı bırakılmaz.
- Ana liste `CALISANLAR.m3u`, HEPSİ, favoriler, ⭐ YENİLER, kanal kimlikleri, URL, sıralama, kategori, çalışan PNG logoları, yabancı arşivi ve korunan yedekler izinsiz değişmez.
- Eski otomasyonların işlevi, bağımlılıkları, tetikleri, yazma izinleri ve rapor/artifact çıktıları yeni görev karşılığında korunur; eşdeğerlik test edilmeden eski otomatik tetik kaldırılmaz.
- Güvenlik ve korunan veri yazma kapıları kaldırılmaz; yalnız işi gereksiz engelleyen teknik çakışmalar en dar kapsamda düzeltilir.
- Eski işler ve eksikler yok edilmez: DEVAM_NOTU.md ve TOPLU_DURUM_RAPORU.md açık görevlerin kaynaklarıdır.
- Kanallar kullanıcı onayı olmadan ana listeye veya ⭐ YENİLER'e eklenmez. TV/IBO EPG kabulü cihazda doğrulanana kadar açık kalır.

## Beş hedef workflow ve görev aileleri
1. **Güvenlik:** izinler, korunan yazma kapısı, kural denetimleri, güvenlik ve sağlık.
2. **Kanal keşfi:** günde iki kez 06:00/18:00 UTC kaynak arama, alternatifler, tekrar ayıklama, aday PNG hazırlığı.
3. **Kanal testleri:** canlı yayın, ffprobe, farklı saat retest, kalite, kimlik, logo/EPG teknik kanıtı; IBO kabulü ayrı.
4. **Arşiv ve yedek:** çalışan/çalışmayan/alternatif ayrımı, geçmiş, 1/15 yedekleme, harici kopya ve geri yükleme kanıtı.
5. **Genel bakım ve rapor:** ayın 1/15'i koordinasyon, test, bağımlılık, rapor, güncelleme ve açık görev kabulü.

## Bilinen somut açık işler
- 92 workflow'un güncel aktiflik ve schedule/push/workflow_run/dispatch envanteri; görevlerin eksiksiz, tekil eşleştirmesi.
- EPG günlük üretim ve Pages workflow_run yayın zincirini beş ana otomasyona kayıpsız taşımak.
- Ayın 1/15'inde çalışan farklı bakım/sağlık/yedek görevlerini çakışmadan koordine etmek.
- Harici ve tarihsel yedek ile gerçek geri yükleme kanıtı; yalnız izole Git HEAD testi yeterli değildir.
- 75 aday: 51 farklı saat tekrar testi bekleyen, 24 ffprobe geçmeyen; 4 alternatif; kimlik, kalite, logo ve kullanıcı cihazı onayı ayrı tutulur.
- EPG XMLTV beş kanal pilotunun teknik kanıtı ile TV/IBO onayı birbirine karıştırılmaz.
- 18 görev ve 26 güvenlik kuralı için nihai kabul kanıtı.

## Birleştirme kapıları
A. Tam envanter ve bağımlılık haritası.
B. Her eski workflow'un yeni beşli karşılığı ve aynı işi iki kere çalıştırmama kanıtı.
C. Eksik görevlerin kendi kategorisinde uygulanması ve doğrulanması.
D. Beş workflow üzerinde tek toplu CI testi, yayın/Pages/yedek ve korunan dosya kontrolleri.
E. Ancak A-D geçtikten sonra eski bağımsız tetikleri kapatma; geçmiş kodu ve kayıtları saklama.

Bu belge başlangıç çalışma sözleşmesidir; beş workflow'un kurulduğu veya açık işlerin tamamlandığı anlamına gelmez.
