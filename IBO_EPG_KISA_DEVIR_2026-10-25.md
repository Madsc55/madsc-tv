# IBO EPG devir notu — 2026-10-25

IBO sürümü: 2128.0; kod: 2128000.

Cihazda kanallar çalışıyor fakat EPG boş. TiviMate ve UHF EPG gösteriyor. TRT 2 yayın görüntüsündeki program yazısı EPG kanıtı değildir.

Test edilenler ve başarısız olanlar: ana XMLTV, 5 kanallı XMLTV, ayrı 5 kanallı M3U8, jsDelivr CDN, kısa ve eşleşen kanal kimlikleri. Kullanıcı yeniden yüklemeyi denedi.

Beş kanallı testte 309 program ve birebir tvg-id eşleşmesi mevcut. IBO'nun XMLTV dosyasını indirip indirmediği henüz kanıtlanmadı.

Sonraki adım: istek kayıtları görülebilen HTTPS sunucusunda XMLTV erişimini ölçmek; başarılı indirmeden sonra format uyumluluğunu araştırmak. Henüz çalışan çözüm doğrulanmadı.

Koruma: ana listeler, YEDEKLER, YENİLER, FAVORİLER ve cihaz favorileri değiştirilmeyecek. main'e kanıtsız merge ve PR #71 merge yok.
