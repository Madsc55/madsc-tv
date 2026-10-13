# MADSC — 13 Ekim 2026 devam ve eksik kapanis kaydi

Bu not DEVAM_NOTU.md ve SEKIZ_GOREV_TOPLU_DENETIM.md ile birlikte okunur. Raporlar snapshot'tir, canli IBO testi degildir.

## Korunan kararlar
- Ana CALISANLAR.m3u, HEPSI, favoriler, YENILER, yedekler ve mevcut sira/metadata kullanici onayi olmadan degistirilmez.
- IBO Player cihaz testleri bu calismanin kapsaminda degildir. Teknik ffprobe basarisizligi IBO'da calismaz kaniti degildir.
- 740 yabanci aday YABANCI_KANALLAR.m3u arsivinde; IBO'da gorunur yabanci kategori acilmaz.
- Kanal kimligi, logo, EPG, kalite ve yayin haklari ayri kanit ister; teknik decode tek basina onay degildir.
- Kaynak hedefi 155 diye 156 farkli URL'den biri rastgele silinmez.

## Dogrulanan depo kayitlari
- madsc_kesif/ozet.json, 2026-10-13 13:59 UTC: 156 tanimli kaynak, 155 hedef, 14 otomatik taranan kaynak, 9576 bulunan kayit, 3514 tekrar, bu tur 0 aday, 0 test; ilyswch-TR icin HTTP 404 raporlanmis. 404 tarihsel snapshot, bugunku canli sonuc degil.
- madsc_son_kontrol/summary.json, 2026-10-13 09:22 UTC: 3175 tamamlanmis, 3082 kalmis, 901 icerik incelemesi, 1931 kimlik bekleyen teknik gecis, 195 sureklilik hatasi, 148 timeout, listeye hazir 0.
- SEKIZ_GOREV_TOPLU_DENETIM.md: bagimsiz GitHub disi yedek, kaynak erisimi, kanal kimligi, lisans, logo/EPG kaniti ve branch protection acik; cihaz testi kullanici istegiyle kapsam disi.
- Son merkezi Actions #38416932386 basarili; bu kod denetimi, yayinlarin canli/kimlik dogrulamasi degildir.

## Tekrarlanmadan yapilacaklar — oncelik
1. Devam eden son kontrol is akisini ve gercek kuyruk ilerlemesini son Actions/artifact verisiyle dogrula; tamamlanan 3175 kaydi yeniden test etme.
2. Kalan 3082 aday icin mevcut otomatik son kontrol mekanizmasinin durma nedenini ve izinlerini incele; izin varsa yalniz kaldigi yerden ilerlet, tekrarlayan fail durumunda dur.
3. 901 icerik incelemesi + 1931 kimlik bekleyeni ayri kanit kuyruğuna koy; kanal adini, logo ve stream kimligini otomatik dogrulanmis sayma.
4. 195 sureklilik hatasi ve 148 timeout icin IBO uyumlulugu belirsiz etiketini koru; calismiyor diye silme.
5. 156 kaynak benzersiz URL: 155 hedefini zorlamadan erisim, gercek kullanim ve kaynak kalitesiyle karar ver. ilyswch-TR 404 kaydini canli tekrar dogrula.
6. Tekrarlanan URL testlerini gecmis silmeden engelleyen kod ve durdurma davranisini test et.
7. Korunan playlist yazma kapisi, izole geri yukleme, bagimsiz dis yedek ve branch protection yetkilerini kanitla. Yetki yoksa engel olarak kaydet.
8. Logo/EPG, kalite, lisans ve kanal kimligi eksiklerini tek final inceleme raporunda birlestir; IBO cihaz testi yapma.
9. Bir tek toplu Actions dogrulamasiyla gercekten kapanan isleri ve dis kanit gerektirenleri ayir.

## Yapilmamasi gerekenler
- Her tur yeni rapor alanlari ekleyerek isi bitmis gibi gostermek.
- Kullanici onayi olmadan ana liste/YENILER/favori/yedek degistirmek.
- Bos yeni aday kuyrugunu butun eski testlerin bittigi seklinde yorumlamak.
- Teknik gecis veya yesil Actions sonucunu cihazda calisiyor ya da lisansli diye sunmak.

## Kritik kullanici dogrulamasi — IBO oynatma korunacak
- Kullanici, teknik testten gecen kanallarin bir kisminin IBO Player'da gercekten calistigini teyit etti. Bu gozlem kaybolmamalidir.
- Ayrica ffprobe/teknik testten gecemeyen bazi yayinlarin da IBO'da calistigi daha once gozlemlendi. Teknik hata = IBO'da calismiyor sonucuna varilmaz.
- IBO'da kullanicinin calisiyor dedigi belirli kanallar, kanala ait dogrulanmis eslesme varsa ayri KULLANICI_IBO_CALISIYOR kaydi olarak korunur. Hangi URL'lerin onaylandigi bilinmeden tum teknik gecisler IBO onayli sayilmaz.
- Otomatik testler, kullanici onayli oynatma sonucunu ezemez; kanal veya URL silinmez. Cihaz testlerini asistan yeniden yapmaz.

## Kullanici duzeltmesi — 740 yabanci kanal ve teknik false-negative (13 Ekim)
- Kullanici acikca bildirdi: sistem teknik testlerinden gecemeyen kanallarin cogu IBO Player'da oynuyor. Bu, teknik testlerin IBO uyumlulugunu eksik olctugune dair saha gozlemidir; tum teknik basarisizlar kesin bozuk sayilamaz.
- Somut ornek: 740 yabanci kanal bir donem IBO'da gorunur hale getirildi ve kullanici tarafindan denendi; bu deneme toplu bir IBO gozlemidir. Her 740 URL'nin ayri ayri basarili oldugu veya bugun canli oldugu iddia edilmez.
- 740 kanal daha sonra kullanici istegiyle YABANCI_KANALLAR.m3u arsivine tasindi. Arsivde olmalari yayinlarin calismadigi anlamina gelmez.
- ffprobe fail, timeout veya continuity fail sonucunu KESIN_CALISMIYOR etiketine donusturme. IBO'da calistigi kullanici tarafindan kanitlanan kanal URL eslesmelerini oncelikle koru, gecmisi ezme.
- Yeni otomatik tarama/temizlik, 740 arsiv kanalini veya kullanici onayli oynayan kanallari teknik sonuc nedeniyle silmemeli; kullanici izni olmadan ana listeye/YEDEKLER/YENILER'e yeniden eklememeli.
- Teknik test raporunda IBO false-negative riski ayrica gorunmeli; cihaz testi asistan tarafindan yapilmayacak.

## Kullanici onayli yabanci/Turk kanal is akisi
- YABANCI: Bulunan yabanci adaylar, teknik gecis veya basarisizlik fark etmeksizin ayri arsivde saklanir. IBO kullanici testine hazirlamak icin YEDEKLER'e otomatik tasinmaz; kullanici yabanci kanallari tek tek test etmeyecek. Yabanci kanal tespiti yalniz kaynak ulkesine gore kesinlestirilmez; belirsizler siniflandirma bekler.
- TURK: Yalniz ana listede bulunmayan yeni Turk kanallari sistem teknik testlerine alinir. Teknik testten gecen ve kanal kimligi yeterince dogrulanan adaylar kullanici IBO testine uygun YEDEKLER taslagi olarak hazirlanir. YEDEKLER'e fiili ekleme icin kullanici onayi gerekir.
- Kullanici IBO'da calisiyor derse CALISIYOR, calismiyor derse CALISMIYOR olarak ayri kullanici sonucu tutulur. Otomatik ffprobe bu sonucu ezmez.
- Teknik testten gecemeyen Turk adaylar silinmez, ayrik inceleme arsivinde kalir; kullanici IBO testine otomatik gonderilmez.
- Tum bulunan liste disi farkli URL'ler arsivlenmeli, ayni URL yeniden arama/teste sokulmamali; yeni URL alternatifi ayri tutulmali. Arama motorunun kaynaklari yeniden okumasiyla ayni URL'yi yeniden test etmek birbirinden farklidir.
- Bu bolum is akisi karari kaydidir; uygulama kodunun tam olarak bu sekilde calistigi iddia edilmez.

## 2026-10-13 - Guncel kullanici onayi, yapilanlar ve devam noktasi
- ONCEKI yabanci/Turk ayrimi is akisi kullanici tarafindan degistirildi: Ilk gunden beri bulunan, teknik test gecen/gecmeyen, Turk/yabanci/belirsiz tum yeni adaylar, ayni URL tekrar edilmeden YEDEKLER'e alinarak IBO Player'da kullanici tarafindan sinanacak. Kullanici calisiyor/calisimiyor/yabanci kararini bildirecek; sonuca gore YEDEKLER'den kaldirilip ilgili kalici arsivde kayit korunacak. Otomatik teknik fail kesin IBO fail degildir.
- 2026-10-13'te arsivden YEDEKLER'e tek seferlik aktarim Actions #38427474997 SUCCESS. Sonrasinda CALISANLAR.m3u: toplam 12636 kanal, YEDEKLER 11599, diger kategoriler 1037. Bu sayilar anlik kayit olup IBO'da yuklendigi dogrulanmadi.
- scripts/discovery_archive.py ve .github/workflows/madsc-birlesik-kesif.yml ile kalici arsiv ve gecmis tekrar kontrolu baglandi (74defba, ac1e259, da33c8e). Arsiv CSV dosyasi madsc_kesif/bulunan_kanal_arsivi.csv. Eski kayitlar korunmali.
- scripts/stage_archive_to_backups.py ve .github/workflows/madsc-arsiv-yedek-aktarim.yml eklendi (3cc21f7, 9589a30); tekrarli otomatik aktarim yapilmasin, diger kategorilere dokunulmasin.
- Toplu butunluk testi ilk #38428678653 FAILURE: kategoriler arasinda ayni URL bilincli bulunabilir. Test kodu duzeltildi (a401ba4, f883604), tekrar #38428822471 SUCCESS. Kanallar silinmedi.
- Son kontrol workflow'u otomatik push tetiklemesiyle calistirilmaya calisildi (9b74f49); #38429266062 FAILURE: 24. kural devre kesici onceki 3 basarisiz/zaman asimi calismasini gorup threshold=2 ile testleri guvenli durdurdu. Push tetikleyicisi kaldirildi (a6e4da5); guvenlik kilidi KALDIRILMADI.
- Kurtarma teshisi workflow'u eklendi (6515bb3), #38429767606 SUCCESS: unit testler, rapor dosyalari ve kilit gecmisi incelemesi adimlari basarili. Bu, yayinlarin yeniden test edildigi veya kilidin acildigi anlamina gelmez.
- madsc_son_kontrol/summary.json son bilinen zaman 2026-10-13T09:22:28Z, remaining=3082, selected=3175, completed=3175, ready_for_playlist=0; rapor tarihi eski ve sayilar tekrar dogrulanmadan guncel diye sunulmamali.
- KALAN: son kontrol zincirinin onceki gercek basarisizliklarini analiz et; sadece kontrollu manuel kurtarma calismasiyla (workflow_dispatch, mevcut guvenlik kodunda izinli) yeniden baslat; test raporlarini ve kalan kuyrugu dogrula; kullanicinin IBO geri bildirimlerini URL bazinda kalici kaydet ve YEDEKLER'den ancak kullanici talimatiyla tasima/silme yap; 11599 aday icin IBO oynatici performansi kullanici tarafindan dogrulanmali.
- Koruma: HEPSI/FAVORILER/YENILER/ULUSAL ve diger eski kategorilerin kanal adi, sirasi, URL, logo, ID ve grup bilgisi degistirilmez. IBO testi sadece kullaniciya aittir.

## 2026-10-13 - Tekrarlayan workflow zincirini kalici olarak azaltma
- Kullanici istegi: her seferinde yeni workflow acip birbirini tetiklemek yerine merkezi, tutarli, tekrarsiz ve toplu is akisi.
- .github/workflows/madsc-son-kontrol.yml son adiminda kendini tekrar workflow_dispatch ile baslatan otomatik zincir kaldirildi (a79c319). Gunluk planli kontrol ve kullanici tarafindan manuel kurtarma imkani duruyor.
- Her basarili batch sonunda kalan sayi yalniz raporlanir. final_validation.py daha once son kontrol sonucu kaydedilmis adaylari yeniden test etmez. Devre kesici / 24. kural guvenlik kilidi korunur.
- #38429767606 kurtarma teshisi SUCCESS, fakat bu son kontrolun kilidinin kalktigi veya bekleyen adaylarin test edildigi anlamina gelmez.
- Acik konu: son kontrolu manuel kurtarma modunda guvenli baslatip gercek sonucunu izlemek; gunluk otomasyonun ilerlemesini takip etmek; kullanicinin IBO gozlemleriyle arsiv siniflandirmasi yapmak.

## 2026-10-13 - Son durum, sekiz gorev ve kullanici talimati (son ek)
- Kullanici acik talimati: onceden onaylanmis isler icin tekrar tekrar soru SORMA; yetki dahilinde islemleri dogrudan yap, somut tamamlanma ve test kaniti sun; engeli acikla. Gerekli tum degisiklikleri ve kalanlari bu kayda ekle. Yeni gereksiz workflow ve tekrarlayan test uretme.
- Manuel kurtarma run #38430737866 (workflow_dispatch) gercekten baslatildi. Son sorguda STATUS=in_progress; '24. kural' SUCCESS, birim testleri SUCCESS, ffmpeg kurulumu SUCCESS, 'Bes dakikalik goruntu ses surekliligini dogrula' IN_PROGRESS. Sonuc tamamlanmis gibi sunulmayacak.
- Son kontrol zincirleme kendini tetikleme kaldirildi (a79c319); sonraki isler zamanlanmis veya kontrollu manuel calisma ile ilerler. Guvenlik kilidi korunur. Bu tek basina tum adaylari veya sekiz gorevi bitirmez.
- Son basarili kurtarma teshisi #38429767606 SUCCESS; toplu butunluk #38428822471 SUCCESS; YEDEKLER aktarim #38427474997 SUCCESS; genel saglik son gorulen #38430164504 SUCCESS.
- Sekiz gorev takibi: (1) merkezi denetim KISMEN, (2) 156 kaynak/155 hedef farki DOGRULAMA BEKLIYOR, (3) tekrar testlerini engelleme ve gecmis koruma KISMEN UYGULANDI, (4) yedek ve korunan listeler butunluk TESTI BASARILI, (5) logo/EPG/kimlik/kalite BITMEDI, (6) IBO aday hazirligi YEDEKLER AKTARILDI ama cihaz testi KULLANICIYA AIT, (7) tek yonetim paneli TAMAMLANDIGI DOGRULANMADI, (8) gunluk hata/sonuc raporu KISMEN.
- Kalan kritik: #38430737866 bitis sonucunu ve madsc_son_kontrol/summary.json yeni kalan sayisini kontrol et; varsa gercek hata adimini ve kanitini inceleyip guvenligi bozmadan duzelt. 3082 onceki kayittaki remaining sayisidir, guncel sayi gibi sunulmaz. Sekiz gorevin somut eksiklerini tek bir denetim planinda tamamla, eski dosyalari/raporlari silme. Her tamamlanan degisikligi bu kayda isle.
- Koruma: CALISANLAR.m3u, HEPSI, FAVORILER, YENILER, YEDEKLER, YABANCI_KANALLAR.m3u ve kullanici IBO test kararlari onaysiz degistirilmez. Kullaniciya yapilmayan isi yapildi diye soyleme.

## 2026-10-13 17:00 UTC - YEDEKLER'den yabanci kanallari ayirma, kullanici onayli
- Kullanici: "yedeklere attigin turk kanallarini haric yapancilari kaldir ve sistemimiz de klasinlar turk kanallari kalsin kontrol edeyim".
- scripts/keep_turkish_backups.py ve .github/workflows/madsc-yedek-turk-ayir.yml olusturuldu; run #38435159165 SUCCESS.
- Rapor: madsc_kesif/yedek_turk_ayirma_raporu.json. Baslangic YEDEKLER 11599, kalan 42, IBO listesinden ayrilan 11557. Bunlardan 740 kayit yabanci arsiv kanali ile eslesti; 10817 kanal Turk kimligi kesin olmadigindan SINIFLANDIRMA BEKLIYOR (bunlarin yabanci oldugu iddia edilmez).
- Ayrilan 11557 kanal kayipsiz olarak madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u dosyasinda saklandi. YABANCI_KANALLAR.m3u degistirilmedi. Diger kategori kayitlari ve sirasi korunmasi kod tarafindan dogrulandi.
- Dikkat: YEDEKLER'de kalan 42 kanalin kimligi kaynak/isim ipuclarina dayali adaydir; hepsinin Turkiye kanali oldugu veya IBO'da calistigi tek tek kanitlanmis degildir. 10817 belirsiz arasinda Turk kanali olabilir. Kayipsiz arsivden gelecekte kimlik dogrulamasiyla geri alinabilir; kullanici onayi olmadan toplu geri ekleme yapilmaz.
- Tek seferlik push tetiklemesi sonraki commitlerde yeniden calismaz. Son kontrol teknik run #38430737866 SUCCESS; ardindan yeni son kontrol run #38434936603 baslamis ve bu kayit aninda IN_PROGRESS idi.

## 2026-10-13 - Kullanici istegiyle 11599 YEDEKLER tam geri yuklendi
- Kullanici, tum 11599 aday kanalin YEDEKLER'e geri verilmesini, IBO'da kendisinin tek tek Turk/yabanci/calisiyor/calisimiyor olarak bildirmesini istedi.
- scripts/restore_all_11599_backups.py ve .github/workflows/madsc-11599-yedek-geri-yukle.yml olusturuldu. Run #38435960199.
- madsc_kesif/yedek_11599_geri_yukleme_raporu.json GitHub'da dogrulandi: before_backup=42, restored=11557, after_backup=11599, protected_categories=UNCHANGED, ibo_playback=NOT_TESTED.
- 11557 geri yuklenen kanalin hepsi Turk degildir; yabanci ve belirsiz adaylar kullanicinin siniflandirma istegiyle YEDEKLER'de yeniden gorunur. Kayip olmadan arşivleri korunur.
- Kullanici IBO sonucunu verdikce URL bazinda siniflandir, kullanici teyidini kaybetme. Kategori tasima veya silme sadece acik talimatla yapilir.

## 2026-10-13 - Kullanici sesli secimi 3-5281
- Kullanici 11367 kanallik GUNCEL YEDEKLER siralamasinda 3-5281 dahil araligi tek tek inceledi. Sozlu secilen Turk numaralari: 8,9,11,21-25,155-162,2370,2374,3362,3363,3570,3571,3665,5271-5274. 26 ve 165 acikca geri cekildi.
- scripts/apply_ibo_3_5281.py ve workflow madsc-ibo-3-5281.yml ile run #38442355557 baslatildi. Rapor madsc_kesif/ibo_3_5281_rapor.json olustu: 27 Turk kanal YEDEKLER'de tutuldu, 5252 kullanicinin yabanci olarak belirledigi kanal kayipsiz madsc_kesif/ibo_3_5281_ayrilanlar.m3u arsivine alindi. Yeni YEDEKLER toplam 6115. 1-2 ve eski 5282 sonrasi degismedi.
- 2370 ve 2374 calisiyor; 3362,3363,3570,3571,3665 calismiyor. Diger Turk kanallarin calisma durumu belirtilmedi. Yabancilarin calisma durumu belirtilmedi.
- Ses kaydinda '2280 Elektrik...' ifadesi belirsizdi ve Turk kanali olarak acikca belirtilmedi; bu nedenle 2280 secili 27 icine alinmadi; arsivde geri getirilebilir. Gerekirse kullanicinin net talimatina gore geri al.
- Sonraki numaralar icin YENI 6115 siralamasi ile ESKI 11367 siralamasi karistirilmamali.
