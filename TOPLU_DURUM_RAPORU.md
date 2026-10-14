# MADSC — Toplu Durum ve Kapanış Takibi
**Tarih:** 14 Ekim 2026  
**Depo:** Madsc55/madsc-tv  
**Son kullanıcı bildirimi:** Merkezi testler yeşil. Bu bilgi kullanıcı gözlemidir; burada bağımsız yeni Actions koşusu doğrulanmadı.  
**Nihai kabul:** HENÜZ ONAYLANMADI.

## Beş aşama: yapılanlar, açık kalanlar

| Aşama | Yapılan ve korunan | Kalan iş / kabul kanıtı | Öncelik |
|---|---|---|---|
| 1. Güvenlik | Korunan liste yazma kapısı, merkezi salt okunur denetim, izole Git geri yükleme kontrolü | Yazma yetkili tüm workflow'ların gözden geçirilmesi; bağımsız tarihsel yedek ve gerçek geri yükleme kanıtı | Yüksek |
| 2. Keşif | Günlük 06:00 UTC birleşik keşif, aday/alternatif ayrımı, tekrar ve kaynak raporları | Yeni kaynakların canlı erişimi, lisans/kullanım uygunluğu, adayların gerçek yayın ve kimlik kontrolü | Yüksek |
| 3. Kanal testleri | Döngüsel ana liste sağlık taraması, test geçmişi, hata ve tekrar analizi | Kanal bazında canlı teknik kanıtların tamamlanması; IBO Player sonuçlarıyla karşılaştırma | Yüksek |
| 4. Logo ve EPG | Ana listedeki doğrulanmış logolar korunuyor; otomatik ana PNG tekrarları kaldırıldı; yeni aday PNG hazırlığı keşifte; günlük EPG üretimi başarılı olduğunda Pages yayını | Yeni adayların eksik logolarını eşleştirme ve gerçek görsel/kimlik kontrolü; EPG kanal eşleştirmesi ve cihazda görünme kanıtı | Yüksek |
| 5. Arşiv ve kabul | Beş aşamalı tek merkez denetim, 18 görev haritası, sekiz görev raporu, yabancı arşiv ve kabul kapısı | Açık kanıtları tek tek kapatma; 26 güvenlik kuralının uçtan uca doğrulanması; kullanıcı onayı olmadan liste aktarımı yapmama | Yüksek |

## Tamamlanan otomasyon sadeleştirmeleri
- Belge kontrolü ve korunan yazma kapısının ayrı push tekrarları kaldırıldı; manuel denetimler korundu.
- Birleşik keşif, kod değişikliğiyle ağır tarama başlatmaz; günlük zamanlama ve manuel başlatma korunur.
- Ana listedeki mevcut PNG logoları günlük yeniden dönüştürülmez; manuel inceleme korunur.
- EPG üretimi ve Pages yayını, aynı verinin iki push yoluyla tekrar yayımlanmasını önleyen zincire bağlandı.
- PNG, EPG ve keşif kodu değişikliklerinin tek merkezi push denetimine gitmesi için regresyon testleri eklendi.
- Tek merkezi denetim raporları ve son 100 Actions koşusuna dayalı durum kanıtları üretilir; bu örneklem tüm geçmişin kanıtı değildir.

## Sıradaki toplu çalışma sırası
1. Gerçek aday havuzunu ve eksik logo raporunu son keşif artefaktından incele; isim, URL, logo ve kaynak kanıtlarını ayrı kaydet. Eksik logoyu otomatik olarak yanlış bir logoyla doldurma.
2. Yeni aday yayınlarını ve ana listedeki döngüsel sağlık sonuçlarını karşılaştır; ffprobe başarısızlığını doğrudan IBO başarısızlığı sayma.
3. Korunan yazma kapısında inceleme gerektiren workflow'ları ve harici yedek geri yükleme kanıtını tamamla.
4. EPG XML üretimi, kanal kimliği ve IBO eşleşmesini doğrula; cihazda görünmeyi kullanıcı onayı olmadan tamamlandı sayma.
5. Tek merkezde 18 görev/26 kural ve açık kabul ölçütlerini kapat; ancak gerçek kanıt olduğunda nihai kabulü güncelle.

## Değişmez kurallar
- Kullanıcı onayı olmadan `CALISANLAR.m3u`, HEPSİ, favoriler, ⭐ YENİLER, yabancı arşiv, korunan yedekler, kanal URL'leri, sıralama, kategori, isim veya logolar değiştirilmez.
- Kullanıcının doğruladığı ana liste logoları korunur. Logo araştırması **yeni bulunan adaylara** odaklanır.
- Aday, alternatif, teknik testten geçen/geçmeyen ve kullanıcının IBO'da onayladığı sonuçlar ayrı tutulur.
- Birden çok ilgili değişiklik **tek commit**, merkezi test ve **tek toplu durum raporu** olarak yönetilir; gerekli günlük veri üretimleri ayrı zamanlanabilir.
- Raporun varlığı, yeşil Actions, test kapsamı veya arşiv sayısı canlı yayın ve cihaz kabulü yerine geçmez.

## Canlı durum raporlarının kaynağı
Merkezi GitHub Actions koşusunun `madsc-aylik-merkezi-denetim` artefaktında: `madsc_kisa_durum_ozeti.md`, `toplu_tetikleme_ve_kabul_ozeti.md`, `bes_asama_bekleyen_isler.json`, `kalan_isler_tek_kosu_karar_tablosu.json`, `tek_islem_coklu_push_analizi.json` ve aday logo raporları. Buradaki belge, mevcut kod ve kullanıcı bildirimiyle hazırlanmış **kalıcı çalışma planıdır**; anlık kanal sayısı uydurulmaz.
