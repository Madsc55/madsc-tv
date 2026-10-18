# MADSC TV — YENİ SOHBET KESİN DEVİR — 19 EKİM 2026 01:20 (Europe/Stockholm)

## KULLANICININ EN SON VE BAĞLAYICI KARARI
**BEŞLİ SİSTEMİ SIFIRDAN KUR. ESKİ SİSTEMDEN HİÇBİR KODU, WORKFLOW'U, TETİĞİ, OTOMATİK İŞİ VEYA 92 ESKİ WORKFLOW'UN DAVRANIŞSAL EŞDEĞERLİK ZORUNLULUĞUNU TAŞIMA.** Eski sistemi sadece istenen fonksiyonların, kararların, koruma kurallarının, geçmiş sorunların ve verilerin **salt okunur bilgi kaynağı** olarak kullan. Yeni beşli sistemi yeni kod ve yeni beş merkezi otomasyon olarak tasarla. Kullanıcının bu son kararı, DEVAM_NOTU.md içindeki eski '92 workflow'u aynen taşı / davranışsal eşdeğerliği sağla' talimatını GEÇERSİZ KILAR. Yeni sistemin beş kategorisi eski belgelere göre gereksinim olarak çıkarılacak; eski kod taşınmayacak.

## KESİN KORUMALAR / YASAKLAR
- IBO Player Pro'daki mevcut kategorilere, HEPSİ'ne, FAVORİLER'e, çalışan kanallara, kanal adlarına/URL/ID/logo/sıra/kategorilerine DOKUNMA.
- CALISANLAR.m3u, YENILER.m3u, YEDEKLER, mevcut yabancı arşivler, geçmiş kullanıcı kararları, EPG ve üretim dosyalarına DOKUNMA; kullanıcı açık onayı olmadan hiçbirini silme/yeniden yazma/taşıma.
- Eski workflow'ları değiştirme, silme, emekliye ayırma veya tetiklerini kapatma. Eski otomatik işleri yeni sisteme kopyalama, bağlama veya tetikleme. Yeni sistem kendi izole dalında, otomatik üretim yazma yetkisi olmadan geliştirilir.
- main'e push, PR #71 merge, üretime geçiş ve IBO cihazına otomatik uygulama YOK.
- **Yeni IPTV M3U listesi sıfırdan, ESKİLERDEN AYRI, boş ve yeni bir dosya olarak kurulacak.** Yeni keşif/testlerden gelen adaylar otomatik olarak mevcut IBO listelerine girmez; açık kullanıcı onayı gerekir.
- 19 temel güvenlik kuralı ve sonradan tanımlanmış 26 güvenlik maddesi gereksinimdir. Fail-closed, salt okunur keşif, kontrollü aday bekletme, yazma kapısı, audit, başarısızlık devre kesici, yedek/geçmiş bütünlüğü yeni kodda sıfırdan uygulanıp test edilmelidir.
- Kullanıcı daha önce YEDEKLER'e ekleme iznini geri almıştır; yeniden izin varmış gibi davranma.

## BAŞVURU BELGELERİ / OKUNDU
- DEVAM_NOTU.md (691485 karakter; önceki devir notları ve K1–K5 kayıtları)
- 810 dosya notu.md (776974 karakter; eski kaynak denetimi)
- 810 dosya notu - 19 Ekim 2026 EK.md
- 810 dosya notu - 19 Ekim 2026 EK PARTI 2.md
- 810 dosya notu - 19 Ekim 2026 EK PARTI 3.md
- 810 dosya notu - 19 Ekim 2026 EK PARTI 4.md
- 810 dosya notu - 19 Ekim 2026 EK PARTI 5 100 DOSYA.md
- 810 dosya notu - 19 Ekim 2026 EK PARTI 6.md
- 810 dosya notu - 19 Ekim 2026 EK PARTI 7.md
- 810 dosya notu - 19 Ekim 2026 EK PARTI 8.md
- 810 dosya notu - 19 Ekim 2026 TEKIL ENVANTER SONUC.md
- GUVENLIK_KURALLARI.md; ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md; BES_SISTEM_GECIS_KONTROL.md
Not: eski belgelerdeki '92 workflow eşdeğerliği', eski cron ve eski otomasyonun aktarılması yönündeki görevler artık UYGULANMAYACAK; kullanıcı yeni sıfırdan tasarım istiyor. Belgelerden yalnızca hedef işlevler ve değişmez koruma kuralları çıkarılacak.

## ESKİ DENETİM SONUCU VE SINIRLARI
19 Ekim sabit kaynak envanterinde 823 dosya, 450 görsel olmayan dosya; tekil içerik okuması 450/450 olarak kayda alındı. 373 görsel tek tek incelenmedi. Kod incelemesi çalışma zamanı doğrulaması değildir; eski sistemin K1–K5 testlerinin başarısız/eksik sonuçları yeni sıfırdan sisteme otomatik başarı/başarısızlık olarak aktarılmaz. Eski kaynaklarda korunan playlist'e doğrudan yazan iptv_test.py, eski IBO betikleri ve git push/main riskleri bulunmuştur; yeni sistemde bunlar YASAK.

## SIRADAKİ İŞ — YENİ SOHBETTE
1. Bu devir belgesini oku. Kullanıcının son sıfırdan-kurulum kararını en üst öncelik kabul et.
2. Belgelerden yeni sistemin işlevsel gereksinimlerini çıkar; beş yeni merkezi alan: (i) güvenlik/sağlık ve koruma kapısı, (ii) kanal keşif ve aday kuyruğu, (iii) medya/kararlılık ve kimlik doğrulama, (iv) EPG/logo/oynatıcı uyumluluk (yalnız yeni liste için), (v) rapor/yedek/geçmiş ve merkezi orkestrasyon. Bu sınıflandırma bir taslak; belgelerdeki isim çatışmalarını yeni mimaride netleştir.
3. Sadece YENİ, İZOLE ve salt-okunur temelli dizin, beş yeni workflow ve boş ayrı IPTV M3U tasarla; önce güvenlik/korunan dosya testlerini yaz ve topluca çalıştır. Eski 92 workflow'tan otomasyon taşıma veya eski sistemle entegrasyon yapma.
4. Yeni otomasyonların mevcut eski otomasyonlarla çift tetiklenmesini önle. Varsayılan olarak yalnız manuel/izinli tetik ve yazmasız deneme; otomatik zamanlamaları ve yayınları kullanıcı onayına bırak.
5. GitHub'da önce çalışma dalını doğrula; main'e, PR #71'e veya korunan dosyalara dokunma. Kod değişikliği yapıldığında gerçek commit SHA ve Actions durumunu kontrol et. Kullanıcı kısa ve net durum ister.

## SON DURUM
Bu konuşmada yeni beşli sistem KODLANMADI; sadece kaynak notlar tekrar okundu ve kullanıcının son kararı kesinleştirildi. Bu dosya, yeni sohbet için birleştirilmiş devir notudur. Sonraki sohbette doğrudan bu belgeden devam et; aynı eski 92-workflow taşıma planına geri dönme.
