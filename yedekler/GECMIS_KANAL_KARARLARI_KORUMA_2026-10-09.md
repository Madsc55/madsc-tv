# IPTV KARAR VE TEST KAYITLARI — KORUMA RAPORU
Tarih: 2026-10-09
Durum: KISMİ ENVANTER; geçmişteki bütün kararların eksiksiz bulunduğu henüz doğrulanmadı.

## Kesin kurallar
- Kullanıcının İBO Player/TCL cihazında verdiği ÇALIŞIYOR/ÇALIŞMIYOR kararı ayrı ve öncelikli kayıttır.
- Teknik testte başarısızlık kullanıcı tarafından ÇALIŞMIYOR onayı anlamına gelmez.
- Ana CALISANLAR.m3u ve ⭐ YENİLER kategorisi açık komut olmadan değiştirilemez.
- Mevcut dosyalar silinmez, karar geçmişi üzerine yazılmaz.

## Geçmiş sohbetlerden geri kazanılan kullanıcı kararları
2026-10-07: Kullanıcı ⭐ YENİLER'e konan şu 10 adayı İBO Player'da “hiçbiri çalışmıyor” diye reddetti:
TRT Spor; Akit TV; Sports TV; Tarım TV; Toprak TV; ON4 TV; BRT 2; Genç TV; Kanal T; Kıbrıs TV.
Durum: KULLANICI_CALISMIYOR. Önceki konuşmada listeden silindikleri bildirildi.
Önemli: Bu kayıtlar kanal adlarına ait tarihsel test kararlarıdır; o tarihteki kesin URL'ler burada doğrulanmadı. Aynı isimli başka URL'lere karar aktarılmaz.

## Önceki teknik test özetleri (bireysel kayıtlar henüz uzlaştırılmadı)
- Önceki bir taramada 635 bağlantı: 148 ana çalışan, 187 alternatif, 96 çalışmayan olarak raporlanmıştı.
- Başka testlerden 98 çalışmayan bağlantı raporlandığı belirtilmişti.
- 2026-10-09 teknik aday yedeği: yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u (390 kayıt). Bu 390 kayıt ÇALIŞMIYOR diye sınıflandırılmadı.
- Tekrar test iş akışı: .github/workflows/390-aday-tekrar-test.yml; beklenen rapor: yedekler/TEKRAR_TEST_2026-10-09.csv.

## GitHub'da kontrol edilenler
- CALISANLAR.m3u: 596 kayıt (2026-10-09 kontrolü).
- CALISMAYANLAR.m3u: kökte bulunamadı (404). Bu durum başka isimli arşiv olmadığını kanıtlamaz.
- Tüm kullanıcı retleri ve teknik retlerin tek arşivde bulunduğu henüz kanıtlanmadı.

## Yapılacak güvenli uzlaştırma
1. Geçmiş test artifact/raporlarından tam URL + test tarihi + teknik sonuçları çıkar.
2. Kullanıcının onay/retlerini URL ve tarihle eşleştir; eşleşmeyenleri 'KARAR_ESLESMEDI' olarak tut.
3. 'KULLANICI_CALISMIYOR', 'TEKNIK_BASARISIZ', 'DOGRULANAMADI' ve 'KULLANICI_CALISIYOR' ayrı sütunlarla sakla.
4. Sadece kanıtı olan kayıtları kesin sınıflandır; geçmiş verileri silme, ana listeyi değiştirme.

Bu rapor doğrulanmamış sayıları kesin kanal sayısı olarak göstermemek için tutulmuştur.
