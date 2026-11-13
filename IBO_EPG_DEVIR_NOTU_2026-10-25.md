# IBO Player Pro EPG devir notu — 25 Ekim 2026

## Kanıtlı durum
- Kullanıcı: TiviMate ve UHF uygulamalarında EPG çalışıyor; IBO Player Pro URL'yi kabul ediyor fakat 'Bilgi yok' diyor.
- 25 Ekim 08:04 UTC EPG üretimi başarılı: 215 XMLTV kanalı, 22.747 program, 5/5 kaynak başarılı, 8.532.312 bayt.
- Eski `CALISANLAR.m3u` ile yeni `MADSC55_TV_IBO_CALISANLAR_TEST.m3u8` içerikleri birebir aynı (Git blob SHA b40aaf6615b120eac7bd936ccf022dc4a14025ae).
- Beş kanalın kimlikleri ana liste ile eşleşiyor: TRT 1 af0zo9et4xguwsk; TRT 2 nzdc0yd5xxv43yl; SHOW TV pvr08e5grfsebfw; ATV 2zkzbuscxwyjc4k; KANAL D bbwgmhsmhhoatzg.
- Pilot XMLTV'nin 25 Ekim üretiminde 5 kanalda program var; XMLTV'nin tek satır halinde yazılması biçimlendirme bakımından değiştirildi, ancak bunun IBO hatasının nedeni olduğu kanıtlanmadı.

## Bu dalda yapılanlar
- `scripts/build_epg.py`: gelecekteki program yoksa eski EPG'nin üzerine yazmayı reddet.
- `.github/workflows/epg-pages.yml`: süresi geçmiş EPG için yayın kontrolü.
- `scripts/build_ibo_epg_test.py`: XMLTV öğelerini ayrı satırlara yaz.
- `.github/workflows/epg-dns-yayin-teshisi.yml`: DNS/HTTP/XMLTV teşhis iş akışı.
- PR #75 taslak, main'e birleştirilmedi. Canlı IBO doğrulaması yok.

## Sonraki adımlar
1. PR #75 CI doğrulaması, yeni testler ve kod gözden geçirme; üretime onaysız merge yapma.
2. IBO'nun kaynak URL'yi indirip indirmediğini, EPG eşleştirme ayarlarını ve uygulama önbelleğini cihaz üzerinde kullanıcıyla doğrula.
3. Beş kanallık EPG'yi kontrollü yayınla; canlı Pages URL ve dosya içeriği doğrulandıktan sonra cihaz testi iste.
4. Gerekirse ayrı IBO-uyumlu XMLTV (minimal alanlar, UTC saat biçimi, id/name varyantları) hazırlayıp tek değişkenli karşılaştırma yap.

## Dokunulmayacaklar
Ana kanal listeleri, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, logo/yedekler; main'e merge yok; PR #71'e dokunma; IBO cihaz testi kullanıcıya ait.
