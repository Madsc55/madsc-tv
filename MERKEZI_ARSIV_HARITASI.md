# MADSC TV — Merkezi Arşiv Haritası (salt okunur)

Bu harita hiçbir kanal dosyasını taşımaz, silmez veya değiştirmez. Kaynakları beş merkezi sistemin kullanacağı şekilde ayrı tutar.

| Bölüm | Kaynak | İlke |
|---|---|---|
| ÇALIŞANLAR | CALISANLAR.m3u | Ana TV listesi, onaysız değişmez |
| ÇALIŞMAYANLAR | CALISMAYANLAR.txt, yedekler/IBO_ESKI_CALISMAYANLAR_2026-10-09.m3u | IBO kararı teknik testten ayrı |
| YABANCILAR | YABANCI_KANALLAR.m3u, madsc_kesif/*yabanci_arsiv.m3u | Kimliği belirsiz otomatik yabancı sayılmaz |
| YEDEKLER | yedekler/, madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u | Orijinaller korunur |
| YENİLER / ADAYLAR | YENILER.m3u, aday_bekletme/, aday_hazirlik/, madsc_kesif/bulunan_kanal_arsivi.csv | Önceden açık onay olmadan yedek/test listesine bile ekleme yok |
| TEST KANITI | TEST_RAPORU.csv, madsc_dogrulama/, madsc_son_kontrol/, raporlar/ | Otomatik test IBO onayı değildir |
| GÜVENLİK | GUVENLIK_KURALLARI.md, DEVAM_NOTU.md | 24 kural ve geçmiş korunur |

## Beş merkezi sistem
K1 güvenlik ve izin; K2 keşif ve aday; K3 test ve kararlılık; K4 EPG/logo/kimlik; K5 arşiv ve bakım.

## IBO Player kabul akışı
Keşif -> rapor -> bulunan adet ve hedef listeyi kullanıcıya bildir -> önceden açık onay -> ayrı test listesi -> kullanıcının fiziksel IBO testi -> kullanıcı kararı -> yalnız onaylı işlem.

## Tarihsel mutabakat
13 Ekim: 11599 = 42 tutulan + 11557 arşive ayrılan. Bugün ana listede 2 yedek; 40 kayıt otomatik geri yüklenmez.

## Birleştirme sınırı
Dosyalar fiziksel olarak taşınmadı. 92 eski workflow için tetikleyici, izin, çıktı ve yazma eşdeğerliği doğrulanmadan kapatma veya silme yok.