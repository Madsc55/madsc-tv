# MADSC TV — kaldığımız yer / devam notu

Güncelleme: 12 Ekim 2026, İsveç 17:26 sonrası.
Bu not GitHub main dosyaları, commitler ve Actions kayıtlarından yeniden oluşturuldu. Kaybolduğu bildirilen sohbetin tam metni bulunamadı; kaydedilmemiş son talimatlar bilinmiyor. Eski raporlar yerine bu snapshot ve gelecekteki güncel kaynaklar esas alınmalı.

## Şu anda kaldığımız iş
Kanal taşıma aşaması bitmiş. Son konu **logo güncellemesini otomatik bakım/kanal keşif sisteminde kullanma, sorunlu gerçek amblemleri görsel kanıtla doğrulama**. Öncü TV, Kanal 15 ve Manas TV'yi yeniden taşımak veya favori sıralamasını yeniden düzenlemek sıradaki iş değil.

Son kayıtlı commit:
7b68abd0d620dc61fdb8237da67f9400083c5bd8 — 12 Ekim 13:15:06 Stockholm — Automatically cache playlist artwork as PNG and audit logos.
Önceki: a2ca4877127110387455de1d62c29cf72d779e10 — 13:13:59 — Ulusal başlangıcına Favoriler 1 sırası; 281 kayıt korunmuş.

## GitHub'da korunmuş tamamlanan işler
- Kanal19 Çorum, Öncü, Konya Olay, KTV, TV41, Van65, OBB/Ordu, Hunat ve Show Max için logo dosyaları/bağlantılarıyla ilgili commitler duruyor.
- Öncü TV, Kanal 15 ve Manas TV Sinema'da; Hepsi kayıtları da duruyor.
- Automatically fill missing channel logos iş akışı oluşturuldu; #1–#4 gerçek push çalışmaları başarılı. #4: https://github.com/Madsc55/madsc-tv/actions/runs/38241332214
- Logo iş akışı: tüm ana listenin adreslerini denetler; boş logoya tam kanal kimliği veya tekil tam isimle kaynak adayı bulur; PNG hazırlar. Ekleme için verified_sources.json içinde görsel eşleşme ve doğru PNG SHA-256 koşulu var. Ad/URL/kategori/sıra değişikliğine karşı içerik kontrolü var.
- Mevcut dolu ama erişilemeyen logo adresleri otomatik yanlış resimle değiştirilmez; problem raporu ve yayın karesi inceleme işi oluşur.
- Son logo denetimi 13:14:19: 1029 kategori kaydı, 191 logo URL; boş logo alanı 0; 182 resim, 2 SVG açıldı; 7 HTTP hatası 35 kaydı etkiledi. Bu sayılar doğru amblem veya IBO görünürlüğü garantisi değil.
- Son visual_review.json: 9 kanal incelenmiş, 8 yayın karesi hazır, Baku.TV karesi alınamamış. Kare alındı olması logo eşleşmesinin onaylandığı anlamına gelmez.
- EPG Günlük Güncelleme #9 ardından Publish EPG to GitHub Pages #5 gerçekten çalışmış ve başarılı olmuş. #5: https://github.com/Madsc55/madsc-tv/actions/runs/38240344069
- İlk 6436 aday üç denemesini bitirmiş: 5750 üç geçiş; 439 iki; 109 bir; 138 sıfır. Ön kontrol geçmişi korunmuş.
- 39 öncelikli URL'nin ayrı beş dakikalık son kontrolü bitti: 29 işaretsiz geçiş, 6 içerik incelemesi, 2 süreklilik başarısız, 2 zaman aşımı. Tüm 6436 URL'nin son kontrolü bitmiş değil.
- Kullanıcının IBO'da yabancı dediği ADA/Kanal D kayıtları silinmiş ve karar geçmişine yazılmış. İlk görsel destek raporu kullanıcı onayını geçersiz kılamaz. Bunları yeniden ekleme.
- Şimdiki yedekler yalnız TRT 1 ve DHA. SAT 7 TÜRK üç farklı kalite etiketli URL ile Hepsi ve Dini'de. Etiketlerin tümünün gerçek çözünürlüğünün onayı aynı şey değil.

## Güncel ana liste snapshot
Blob: 042b280409a99d2d19dc379cad4b4889d7c391f8
- ⭐ FAVORİLER (65): 65 kayıt
- ⭐ FAVORİLER 1 (61): 61 kayıt
- ⭐ FAVORİLER 2 (1): 1 kayıt
- 📺 HEPSİ (371): 371 kayıt
- 🎬 SİNEMA (5): 5 kayıt
- 📺 HABER (72): 72 kayıt
- 🇹🇷 ULUSAL (281): 281 kayıt
- ⚽️ SPOR (19): 19 kayıt
- 🌍 BELGESEL (12): 12 kayıt
- 🧸 ÇOCUK (20): 20 kayıt
- 🎧 MÜZİK (33): 33 kayıt
- 📍 YEREL (70): 70 kayıt
- 🕌 DİNİ (17): 17 kayıt
- 📦 YEDEKLER (2): 2 kayıt
Bu rakamlar kategori kayıtlarıdır; benzersiz çalışan kanal sayısı değildir.

## Kurulu takvim (GitHub cron UTC; Stockholm yaz/kış saatine göre değişir)
- Logo bakım: 05:23 ve 17:23 UTC; main playlist/script/workflow değişince push tetiklenir.
- EPG günlük: 03:25 UTC; başarılı tamamlanınca Pages yayın.
- Birleşik keşif: 06:00 ve 18:00 UTC; yalnız yeni URL adayları. Tek otomatik devam yolu birleşik keşif akışının son adımında; ayrı tamamlanma akışı artık tur başlatmaz.
- Üç aşamalı doğrulama: her saat :17; en fazla 240 uygun URL, 12 eşzamanlı test, en az 6 saat aralık; uygun aday kalırsa otomatik devam.
- Güvenli yeni kaynak/kanal arama: 06:00 ve 18:00 UTC; salt okunur, rapor/artifact. Bu eski farklı iş akışı yeni tekrarsız birleşik keşif takvimiyle aynı kabul edilmemeli.
- Salt okunur kanal testi: 06:30 ve 18:30 UTC; eski MADSC_TV_47_LISTE_ADAY.m3u üzerinde çalışır, güncel ana listedeki her kanalı test ettiği iddia edilmez.
- Kararlılık takibi: 06:17 ve 18:17 UTC.

## Eksik ve sıradaki işler
1. Logo #4 artifact'indeki 8 yayın karesi ile ayrı aday logo resimlerinin gerçek amblemini karşılaştır; Baku için görüntü elde etme yeniden denemesi. Spacetoon, TRT Diyanet Çocuk, Dream Türk, PowerTürk Akustik/Slow/Taptaze, TRT EBA, TRT EBA Ortaokul, Baku listedeki görsel inceleme konuları.
2. Mevcut hata veren logo URL'leri için doğru alternatifleri hazırlayıp yalnız kullanıcıca izin verilen logo kapsamındaki değişiklikleri yap. Resim indirildi diye görsel onayı yazma.
3. Yeni kanal aday raporlarından logo hazırlama doğrudan entegrasyonunu kontrol et: kurulu logo workflow'unda discovery workflow_run bağlantısı yok; yalnız main playlist push ve günde iki bakım var. Yeni adaylar ana listeye alınmadan ayrı aday-logo raporu oluşturma bağlantısı gerekiyorsa kontrollü ekle. Ana listeye veya YENİLER'e otomatik yeni kanal ekleme.
4. Son 326 yeni adayın denemeleri ayrı bitirilecek: son kayıtlı durumda 293 iki deneme, 33 bir deneme. En erken uygun sonraki zaman 12 Ekim 18:21:47 Stockholm. Eski 6436 adayın hazırlığını bekletme.
5. Kullanıcının gerçek cihaz/sürümündeki IBO çalışma ve EPG görünürlüğü onaylarını ayrı tut. Beş kanallık EPG pilotunu güncelle; eşleşme/güncellik/İsveç saati/görünürlük birlikte doğrulansın.
6. Kararlaştırılan 11 geliştirme planını mevcut araçlarla karşılaştır; hepsi kurulmuş iddiası yapma. Son takvim aylık geniş tarama + günde iki yalnız yeni URL keşfi; mevcut testlere müdahale etmeme koşulunu koru.
7. Tekrar URL/alternatif, gerçek HD-FHD etiketi, eksik kimlik-kategori-isim, logo alternatifleri ertelenmiş görevlerini ayrı hazırlıkta tamamla.

## Kesin koruma ve kullanıcı talimatları
- Kanal URL/ID, kategori ve sıra değişiklikleri yalnız açık talimatın kapsamıyla.
- Favoriler, Favoriler 1/2/3 ve Hepsi'deki korunacak ilk 90 sıra değişmeden kalsın. Son commit Ulusal'la ilgili olduğundan Hepsi kuralıyla aynı sanma.
- YENİLER'e izinsiz ekleme yok; korunan dış yedeklere müdahale yok.
- Yeni kanal, aynı kanalın farklı URL'si, aynı URL kategori kopyası ayrı.
- Yeşil workflow = kod tamamlandı; doğru kanal/IBO kanıtı değil.
- Onaylanmamış logo eşleşmeleri NOT_VERIFIED; kullanıcı IBO sonucu önceliklidir.
- Bu sohbet yeniden başlayınca önce bu notu ve GÜNCEL GitHub dosyalarını oku; bitmiş kategori taşıma işlerini tekrar yapma.

## Yeniden başlatma cümlesi
Mahmut, Madsc55/madsc-tv içindeki DEVAM_NOTU.md dosyasını ve güncel Actions/raporları oku. Logo otomasyonunun görsel doğrulama ve ayrı kanal-adayı entegrasyonu işinden devam et. Tamamlanan işleri tekrarlama, koruma kurallarını uygula.

## 12 Ekim 2026 devam güncellemesi
- Kullanıcının son talimatı: ana listedeki dolu logo alanları korunacak; yalnız logosuz kayıtlar ele alınacak. Son yerel envanter 1029 kayıtta boş logo alanı olmadığını gösterdi. Erişim hatası dolu logoyu değiştirme izni değildir.
- Yeni keşif adaylarının logo adresleri ayrı metadata ve PNG hazırlama raporuna bağlandı. Aday görselleri yalnız madsc_kesif/candidate_pngs altında hazırlanır; mevcut logos/auto dosyaları değiştirilmez.
- Kamusal HTTPS logo kaynakları hazırlanır; kimlik bilgili veya sorgu parametreli kaynaklar indirilmeden incelemeye ayrılır. Yayın URL'leri bu yeni logo raporuna yazılmaz. PNG hazırlanması gerçek amblem veya kullanıcı onayı değildir.
- Yerel ağsız kontroller geçti: ayrı çıktı, onaysız durumlar, eksik/kısıtlı kaynak ayrımı, önbellek ve bozuk dosya yeniden hazırlama. GitHub Actions çalışması henüz doğrulanmadı.
- 326 adayın kalan doğrulaması, tüm adayların son kontrolü, cihaz/EPG doğrulaması ve takvim düzenlemesi açık kalır. Tamamlanan kanal taşıma ve sıralamalar tekrarlanmayacak.

## 12 Ekim 2026 — gereksiz tekrar düzeltmesi
- İki devam tetikleyicisinden ayrı workflow_run tetiklemesi kaldırıldı; rapor kaydı sonrası kalan yeni aday sayısını okuyan tek yol korundu.
- Her 15 dakikalık keşif yerine günde iki keşif (06:00/18:00 UTC).
- Ana liste sağlık kontrolü artık üç başarılı kontrolü tamamlanan kayıtları ve son kontrolü üzerinden altı saat geçmeyenleri atlar. Geçersiz tarih yeniden test nedeni sayılmaz.
- Keşif geçmişi bozuk veya okunamazsa sistem geçmişi sıfırlayıp yeniden taramaz; durur.
- Yerel kontrol: tamamlanmış, yakın zamanda denenmiş, zamanı gelmiş ve geçersiz tarihli kayıt senaryoları geçti. Yeni Actions sonucu henüz doğrulanmadı.
- Ana liste, mevcut logolar, YENİLER, favori sıraları ve yedek dosyaları bu düzeltmede değiştirilmedi.

## 12 Ekim 2026 — kalan testlerin sürdürülmesi
- Üç aşamalı doğrulama yeniden başlatıldı: kayıtlı 326 eksik aday (293 iki deneme, 33 bir deneme); yeni keşif geçmişinden ek uygun adaylar ayrıca alınabilir. İlk çalıştırma 38283156064 başladı; tamamlanan 6436 kaydı eligible kuralı atlar.
- Decoder kurulmadan önce kayıtlı ve yeni adayların uygunluğu kontrol edilir; boş tur test yapmaz. Altı saat aralık ve üç deneme sınırı korunur.
- final_validation.py artık 39 eski sonucu korur; başarılı/başarısız/zaman aşımı fark etmeksizin önce sonuçlanmış URL'yi yeniden test etmez. Yeni son kontrol en fazla 24 adaylık ayrı grup; yeni aday yalnız üç başarılı denemeden sonra seçilir.
- Son kontrol başarılı üç aşamalı workflow tamamlanmasına bağlandı; önceki sonuçları koruyan güncel main kullanılır. Bu, tüm 5711 bekleyen son kontrolün bittiği anlamına gelmez.
- Altı yerel test ve iki YAML kontrolü geçti; canlı son kontrollerin sonuçları henüz bekleniyor.
- Kanal kimliği, gerçek amblem, İsveç IBO ve EPG görünürlüğü otomatik teknik geçişle onaylanmaz. Ana liste, YENİLER, favoriler ve yedekler bu çalışmada değişmedi.
