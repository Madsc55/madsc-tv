# MADSC TV — güncel devam notu

## SOHBET DEVRİ
Güncelleme: 12 Ekim 2026, Stockholm 20:44 sonrası MTürk logo ve Ton TV kontrolü. Yeni sohbet önce bu dosyayı, AGENTS.md'yi ve ilgili GÜNCEL raporları okur. Bu dosya kısa kontrol noktasıdır; bütün sohbetin dökümü değildir. Kaynak rapor daha yeniyse rapor esas alınır.

## Kesin kurallar
- Ana liste/YENİLER, favoriler ve Hepsi'nin korunacak ilk 90 sırası, korunan yedekler yalnız açık kullanıcı izin kapsamında değişir.
- Ana listedeki DOLU logo alanlarına dokunma. Yalnız logosuz kayıtları bul; gerçek PNG/kimlik hazırlığı ayrı aday raporunda kalır. Son envanterde boş logo 0/1029 kategori kaydı.
- Teknik geçiş, gerçek kanal/amblemi, İsveç IBO sonucu ve EPG görünürlüğü ayrı. Yeşil Actions cihaz onayı değildir.
- ADA/Kanal D için kullanıcının yabancı kanal reddi önceki görsel desteğin üstündedir; reddedilmiş URL'leri yeniden önerme/ekleme.
- Test geçmişi korunur; tamamlanmış üç deneme veya final sonucu (başarısız/zaman aşımı dahil) yeniden yapılmaz. Eksik denemelerde en az 6 saat.
- Yeni kanal, aynı kanalın farklı URL'si ve aynı URL'nin kategori kopyası ayrı değerlendirilir. URL sayısı kanal sayısı değildir.

## Son doğrulanmış sonuçlar
- Üçlü doğrulama: 6981 URL, 6729 tamamlanmış; dağılım 6028 3/3, 447 2/3, 112 1/3, 142 0/3. 252 eksik kayıt altı saat bekliyor; rapor anında uygun aday 0. Snapshot: 12 Ekim 17:35:46 UTC.
- İlk 6436 tamamlanmış test korunmuştur. Sonraki 326 içinden 293 kayıt üç denemeye ulaşmıştır; yeni keşiften 219 kayıt da ayrı eklenmiştir. 252 kalan kayıt, başlangıçtaki 33 + yeni 219'dur; zamanı state.json'dan yeniden hesapla.
- Final kontrol: önceki 39 + yeni 24 = 63 sonuç korunuyor. 48 teknik geçiş/kimlik bekliyor; 10 içerik incelemesi; 2 süreklilik başarısız; 3 zaman aşımı. Yeni 24'ün farkı: 19 teknik geçiş/kimlik bekliyor, 4 içerik incelemesi, 1 zaman aşımı. Snapshot: 12 Ekim 17:35:45 UTC. Rapordaki 5687 kalan eski snapshot; yeni üçlü geçişlerle kuyruk değişir.
- Başarılı runlar: üçlü #87 (38283156064), #89 (38284072474), #90 (38284962128); final #2 (38283388684). Eski kuyruktaki cancelled/skipped runlar kanal testi başarısızlığı sayılmaz. Yeni işlemden önce güncel run durumunu oku.
- İlk 39 kimlik raporunda 36 görüntü incelendi: 4 ilk görsel destek, 20 Türk hedef kimliği reddedilmiş/desteklenmemiş, 15 açık inceleme. Sonraki ADA/Kanal D kullanıcı reddi geçerli. Yeni 24 ve önceki 15 açık kimlik kaydı için 39 kayıt/35 kare ayrıca incelendi: 15 görsel etiket desteği, 6 yalnız marka/bölgesel hedef bekleyen, 14 kimlik yetersiz, 4 görüntüsüz. Bu cihaz veya ekleme onayı değildir. Ana liste blob'u 042b280409a99d2d19dc379cad4b4889d7c391f8 ile URL karşılaştırması: 11 mevcut aynı URL, 7 aynı isim/farklı URL (kimlik doğrulanmamış), 21 ayrı/listede olmayan aday. Raporlarda bu üç sınıfı ve isimleri kullanıcıya açıkça göster; hepsini yeni kanal diye anlatma. Ayrı kaynak: madsc_son_kontrol/kimlik_devam_2026-10-12_1955.json.
- EPG pilotu 12 Ekim yenilendi: TRT1/Haber/Çocuk/Avaz/Türk; kimlik/saat/çakışma kontrolü 5/5. Kaynak gece yarısı stop tarihi hatası dar kuralla yorumlandı; ilk değerler source_time_repairs içinde. Bağımsız yayın akışı/IBO görünürlüğü onayı değildir. Statik kapsam saatleri raporda; cihaz testinden önce gerekirse yeniden güncelle.
- 11 geliştirme mevcut kodla karşılaştırıldı; var olan araçlar yeniden kurulmadı. Kalanlar ayrı envanterde.

## Tekrarlanmayacak tamamlanan işler
Sabah 10:30–14:30 Stockholm: 55 commit, 10 başarılı Actions. İlk 39 final testi ve verilmiş kimlik kararları, kategori taşıma/sıralama, Öncü/Kanal15/Manas Sinema taşıması, logo değişiklikleri ve EPG Pages bağlantısı yapılmış. Ayrıntılar geçmiş dosyasında.
Kullanıcının 20:18 talimatıyla ayrı bulunan 21 aday YEDEKLER'e eklendi; TRT1 ve DHA ilk iki kayıt olarak korundu. YEDEKLER toplam 23 kayıt. Bunlar cihaz/kimlik onayı bekleyen adaylardır; yabancı kanallar ve zaman aşımı sonucu olan Az TV de kullanıcı incelemesi için dahil.  SAT7 Türk üç kalite etiketli URL Hepsi/Dini. Gerçek çözünürlük kanıtı eksik etiketler ayrı ele alınır.

## Son ana liste logo/kategori düzeltmesi
Kullanıcı 20:27'de ana listesindeki TRT Diyanet Çocuk (Çocuk 17), Deniz Postası (Sinema 2), BBC First Türkiye ve Baku.TV logolarının düzeltilmesini, Eurosport 1/2 Türkiye'nin Spor'a eklenmesini açıkça onayladı. Bunlar yeni aday/YEDEKLER talebi değildir.
- Dört kanalın gerçek markalı PNG'leri indirildi, görüntüleri incelendi ve logos/resmi-*-20261012.png altında önbelleklendi. Bu dört tam etiketin 10 kategori kaydında yalnız logo adresi değişti. Diğer Diyanet Çocuk varyantına dokunulmadı.
- İki Eurosport, Hepsi kayıtları/sıraları korunarak aynı URL/metadata ile Spor'un sonuna birer kez eklendi; Spor 19→21. Favoriler, Hepsi ilk 90, YEDEKLER ve yayın URL'leri korundu.
- automatic_png_logos.py artık logo_deneme/approved_repairs.json içinde açık onay verilmiş tam etiket/eski URL eşleşmesini ve yerel PNG SHA256'sını doğrulayarak dolu ama sorunlu adresleri düzeltebilir. Diğer dolu logolar değişmez; genel otomatik marka/on-air onayı verilmez.
- Doğrulama: izinli eski kaynak, PNG hash, ilgisiz kayıtları koruma ve tekrar çalışmada değişiklik yapmama geçti; playlist farkı yalnız izinli logo/Spor kapsamıyla sınırlı. Kullanıcı sonraki konuşmada dört logo düzeltmesinin IBO'da olduğunu bildirdi.
Kanıt: raporlar/ANA_LISTE_LOGO_SPOR_2026-10-12.json. Bu düzeltmeyi yeniden uygulama.

## Sıradaki işler — yalnız eksik kapsam
1. 252 eksik denemenin zamanı geldiğinde mevcut üçlü akış; geçmiş denemeler korunur.
2. Görsel etiket desteği olan 15 kayıtta IBO/gerçek kanal ve dil doğrulaması; 6 marka/bölgesel hedef ve 14 yetersiz kimlik kaydında bağımsız amblem/kanal kanıtı; 4 görüntüsüz kayıt otomatik geçer sayılmaz. 39 devam kaydı/35 kare incelemesi yapıldı; aynı kare incelemesini yeniden yapma.
3. Daha önce final sonucu bulunmayan adayları en çok 24'lük gruplarla ayrı son kontrole almak. Sonuç varsa atla; aynı görevi kuyrukta yeniden başlatma.
4. IBO cihaz/sürüm, kanal açılış/geçiş hızı ve güncel EPG görünürlüğü: kullanıcı cihaz kanıtı gerekir; otomatik onay yok.
5. Eksik kalite/kimlik/kategori/isim ve logosuz aday hazırlığı; ana listedeki dolu logolar korunur.
6. 11 geliştirme envanterinin eksik maddeleri ve aylık geniş tarama modu. Günde iki keşif/tek devam/tekrar koruması zaten kurulu.

## Kaynaklar
- madsc_dogrulama/state.json ve summary.json — ayrı denemeler/tarihler.
- madsc_son_kontrol/results.json ve summary.json — birikimli final sonuçları.
- madsc_son_kontrol/kimlik_incelemesi_2026-10-12.json — eski 39 kimlik kararları.
- madsc_son_kontrol/kimlik_devam_2026-10-12_1955.json — yalnız açık eski 15 + yeni 24 için tamamlanan kare incelemesi; önceki retler korunur.
- madsc_kesif/candidate_logos.json — ayrı PNG hazırlığı, görsel onay değildir.
- epg_deneme/rapor.json, liste.m3u, rehber.xml — ayrı kısa süreli pilot.
- raporlar/GELISTIRME_11_DURUM_2026-10-12.md — 11 geliştirme envanteri.
- kontrol_notlari/DEVAM_GECMISI_2026-10-12_1947.md — bu güncel özet öncesindeki tam kayıt; eski durumlar güncel kabul edilmez.
- Actions: https://github.com/Madsc55/madsc-tv/actions

## Takvim
Yeni keşif 06:00/18:00 UTC; üçlü doğrulama saatlik :17, en az 6 saat; logo bakımı 05:23/17:23 UTC; EPG günlük 03:25 UTC + Pages. Son kontrol üçlü başarı tamamlanmasına bağlı, 24'lük grup; bütün kuyruk bittiği iddia edilmez. Aylık geniş tarama henüz açık iş.

## Kayıt düzeni
Her mesaj değil; önemli karar, tamamlanan iş veya doğrulanmış sonuç sonrası bu kısa özet güncellenir. Eski ayrıntılar tarihli geçmiş dosyasına alınır; test verisi mevcut raporlarda kalır. Kaydetme doğrulanmadan “kaydedildi” denmez. Sohbetin kesin dolma eşiği/kalan kotası görülemediğinden eşik bazlı uyarı garantisi verilmez; son ana kadar beklenmez. Yanıt iletim hatası işlemin tamamlandığının kanıtı değildir.

## Yeni sohbet cümlesi
Mahmut, Madsc55/madsc-tv içindeki DEVAM_NOTU.md'nin SOHBET DEVRİ bölümünü, AGENTS.md'yi ve güncel Actions/raporları oku. Kaldığımız yerden devam et; tamamlananları tekrarlama, korunan listelere ve dolu logolara izinsiz dokunma.

## Son izinli ekleme
21 ayrı adayın URL'si mevcut ana dosyada yoktu; her biri yalnız YEDEKLER'e bir kez eklendi. Aynı URL'li 11 mevcut kayıt ve aynı isimli 7 alternatif bu talimat kapsamında yeniden eklenmedi. Mevcut 1029 kayıt, ad/ID/logo/URL/sıra korunarak bırakıldı; yalnız YEDEKLER grup sayacı 2→23 güncellendi. Dış yedekler/YENİLER/favoriler değişmedi. İsimler ve teknik/görsel durumlar: raporlar/YEDEKLERE_EKLENEN_ADAYLAR_2026-10-12.json. Logo kaynağı kesin olmayan yeni kayıtlarda boş alan kullanıldı; uydurma logo eklenmedi. Gerçek kalite etiketi mevcut ffprobe ölçümüne dayanır, IBO kalite/çalışırlık onayı değildir.

## Son kullanıcı onaylı YEDEKLER taşıması — 12 Ekim 2026
Kullanıcı önceki dört logo düzeltmesini cihazında doğruladı. Taşıma öncesi 23 kayıtlı YEDEKLER sırası sabitlendi: 7 CGTN DOCUMENTARY → BELGESEL; 9 FTV TÜRK etiketi/Red Bull TV kaynak URL'si → SPOR; 15 .SCI-FI → SİNEMA. Üçüne gerçek markalı PNG kondu; aynı URL/isim/kalite/ID ile HEPSİ sonuna birer kopya eklendi. Mevcut Hepsi sırası ve ilk 90/favoriler korunur. Bu üç kayıt YEDEKLER'den taşındı, diğer kayıtları korundu. Yeni sayılar: YEDEKLER 20, HEPSİ 374, BELGESEL 13, SPOR 22, SİNEMA 6.
9. kaydın rbmn-live/BoRB-AT bağlantısı iptv-org akış kaynağında RedBullTV.at ile eşleşir. Logo Red Bull TV'dir; kullanıcının isim değiştirme talimatı olmadığından FTV TÜRK etiketi korunmuştur, ad düzeltmesi açık iş. .SCI-FI yabancı yayın kullanıcı isteğiyle kabul edildi. Kategori/ekleme onayı teknik/kimlik/dil garantisi sayılmaz; geçmiş testler yeniden yapılmadı. Yeni logoların IBO görünürlüğü sonraki cihaz kontrolünü bekler.
Kanıt: raporlar/YEDEK_KATEGORI_LOGO_2026-10-12.json. Aynı taşıma yeni sohbetlerde tekrar uygulanmaz; yeni YEDEKLER sıraları önceki 7/9/15 ile karıştırılmaz.

## Son MTürk/Ton TV kontrolü
Kullanıcı Yerel 56/57 MTürk logo uyuşmazlığını düzeltme istedi. İki varyant aynı yayın URL'sini kullanıyor. Yayıncının https://www.mturktv.com/wp-content/uploads/2025/04/MTurkTV.png dosyası görsel olarak incelendi; logos/resmi-mturk-20261012.png olarak aynen saklandı. Bu iki tam etiketin toplam dört kategori kopyasında yalnız logo adresi eşitlendi (Hepsi/Belgesel/Yerel); isim/URL/ID/kategori/sıra değişmedi. Onaylı eski URL+PNG hash bakım kaydı eklendi. Canlı kare girişimi 5xx döndürdü; yayındaki amblem veya IBO görünümü kesin doğrulanmış yazılmadı. Kullanıcı cihaz kontrolü sonraki adım.
Ton TV Yerel 64: yayıncının resmi site/iletişim bilgileri Çanakkale merkezli bölgesel genel yayın olduğunu destekliyor. Yerel kategorisinde kalması uygun; taşınmadı. Önceki dört logo/Eurosport ve üç YEDEKLER taşıması tekrar yapılmadı.

## 12 Ekim 2026 — son sohbet işlemi: M2O taşıması
- Güncel YEDEKLER 9. kayıt M2O TV DJ STATION 720P HD olarak doğrulandı. İtalya m2o TV için iptv-org/Wikimedia'daki m2o 2019 markalı PNG adresi kullanıldı; yayın üstü amblem ve İsveç IBO cihaz görünümü henüz doğrulanmadı.
- Kullanıcının açık talimatıyla yalnız bu kayıt YEDEKLER'den çıkarılıp aynı akış URL'si/ID/isim/kaliteyle MÜZİK ve HEPSİ sonuna eklendi. YEDEKLER 20→19, MÜZİK 33→34, HEPSİ 374→375. Önceki Hepsi sıralaması, ilk 90 ve favoriler değişmedi.
- CALISANLAR.m3u commit: 6f0dcfc3714feb5d54fa6db081f34d28f0a83803. Önceki MTürk logo düzeltmesi ve Ton TV Yerel kararı zaten yapılmıştı; tekrar uygulanmadı. Kullanıcıdan IBO'da logo/akış görünümü beklenir.

## 12 Ekim — yeni sohbet, kullanıcı onaylı hızlandırma adımı
- Kullanıcı mevcut testleri tekrar etmeden 11 geliştirmede kalan işleri ilerletmeyi istedi. İlk adım olarak yalnız okuyan `tools/guncel_test_durum_ozeti.py` eklendi (commit `4440942728890237ec0c5e0b3a5a727b3fe58dba`), GitHub'dan tekrar okunarak doğrulandı. İki mevcut summary dosyasını birleştirir; snapshot zamanlarını ve URL/kanal ayrımını açıkça yazar; test başlatmaz, playlist değiştirmez. Actions üzerinde çalıştırılması henüz doğrulanmadı.
- Sıradaki işler: birleşik raporu otomatik Actions artifact akışına güvenli bağlama, aylık geniş tarama modunu ayrı ve tekrarsız uygulama, güncel Actions durumunu doğrulama. Tamamlanmış üçlü ve final testleri tekrar edilmez; 6 saat sınırı korunur.

## 12 Ekim — otomasyon sadeleştirme adımı
- Kullanıcı gereksiz yinelenen taramaları azaltma ve otomatik raporu onayladı. Salt okunur `.github/workflows/birlesik-durum-raporu.yml` eklendi (commit `193a54ea6330a7b3a93b2794d21a454013fdcede`); 06:40 ve 18:40 UTC zamanlı, ayrıca manuel tetiklemeli, sadece `tools/guncel_test_durum_ozeti.py` çalıştırıp 30 günlük artifact saklar. Ana liste/test geçmişi değiştirilmez. İlk Actions çalışmasının başarısı henüz doğrulanmadı.
- Eski güvenli kaynak araması ve birleşik keşif potansiyel örtüşmesi henüz workflow bazında denetlenmedi; hiçbir eski otomasyon kapatılmadı. Aylık geniş keşif henüz kurulmadı. Sonraki iş mevcut workflow dosyalarını karşılaştırıp güvenli biçimde tekilleştirmek; tamamlanmış testleri tekrar başlatmamak.
