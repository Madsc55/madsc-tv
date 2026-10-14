## 14 Ekim 2026 — TOPLU OTOMASYON YUKU AZALTMA / EK DENETIMLER ELLE
- Kullanici merkezi testin yesil oldugunu bildirdi; gereksiz tekrarlari tek committe azaltma istendi.
- Haftalik Cuma ana kanal + EPG denetiminin otomatik schedule tetigi kaldirildi; workflow_dispatch saklandi. Ana liste sagligi ayin 1 ve 15'inde, birlesik kanal kesfi her gun iki kez suruyor.
- Haftalik Pazartesi + ayin 1'i genis kaynak kontrolunun schedule tetikleri kaldirildi; workflow_dispatch saklandi. Elle acilirsa iki kaynak modu da calisir. Eski workflow'un ayrica uc-asama dispatch etmesi sadece elle calistirildiginda gerceklesir.
- EPG gunluk guncelleme ve Pages yayinlamasi korunuyor; IBO TV onayi BEKLIYOR. Korunan listeler, logo ve yedekler degismedi.
- Daha yapilmayanlar: tum 92 workflow'un tam aktiflik/tetik zinciri ve otomatik yuk denetimi; 1 ve 15 yedek geri yukleme/harici kopya kaniti; 75 aday icin farkli saat/kimlik testleri. Bunlar tamamlandi diye raporlanmaz.
- Yalniz iki gereksiz otomatik takvim kapatildi; manuel calisma ve gecmis dosyalar silinmedi.

## 14 Ekim 2026 — EPG TEKNIK HAZIRLIK / TELEVIZYON KONTROLU BEKLIYOR
- Kullanici #126 merkezi denetimin YESIL oldugunu ekran goruntusuyle dogruladi.
- EPG yeniden gundemde: TV basinda degil; XMLTV hazirligi, pilot 5 kanal, kaynak ve teknik dogrulama tamamlanacak; IBO Player televizyon gorunurluk testi ve kullanici onayi DAHA SONRA.
- Mevcut epg/report.json: 1039 playlist girisi, 730 eslesme, 583 kullanilabilir tvg-id, 23702 program, 5 kaynak OK (rapor 2026-10-14 08:51 UTC). Bunlar IBO TV kaniti degildir.
- Yeni scripts/epg_tv_readiness.py ve iki izole test: tam XMLTV, bes kanal pilotu, program sayilari, kaynak raporu ve cihaz onay kapisini denetler; epg/tv_kontrol_bekliyor.json kaydeder.
- EPG gunluk workflow'unda hazirlik kontrolu tek kosuda gerceklesir; yalniz EPG dosyalari ve bekleyen TV raporu kaydedilir. TV kontrolu bitmeden onay verilmeyecek.
- IBO TV'de sonradan kontrol edilecek: EPG URL'yi ekleme/yenileme, TRT1/TRT2/SHOW TV/ATV/KANAL D programlari ve Isvec'te gorunurluk. Basarisizsa ekran goruntusu ve uygulama ayarlariyla incele.
- Kalan toplu isler: 92 workflow aktif/zamanlama cakismasi, 1 ve 15 yedek/restore kaniti, gunde iki kez kesif ve logo birlesimi, 75 aday retest/kimlik. Korunan listeler, favoriler ve PNG logolar degismedi.

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

## Ortak karar: tek merkez, gereksiz tekrar yok (14 Ekim 2026)

Kullanıcıyla kesinleştirildi: Beş ana bölümün yönetimi tek merkezden yapılacak. Güvenlik, kanal keşfi, kanal yayın testleri, logo/EPG ve arşiv/kabul için ayrı ayrı aynı işi tekrar eden otomasyonlar kurulmayacak. Günlük keşif, döngüsel yayın testleri ve EPG veri üretimi kendi gerekli zamanlarında ayrı çalışabilir; kod değişikliğinde ağır taramalar yeniden başlamayacak. Her toplu işlemden önce mevcut tetikleyiciler ve sonuçlar incelenecek; gereksiz ikinci iş kaldırılacak, ilgili güvenlik kontrolleri korunacak. Mümkün olduğunda tek commit, tek merkezi test, tek Türkçe sonuç raporu uygulanacak.

**Sonraki çalışma sırası:** (1) Beş bölümde kalan workflow tetikleyicilerinin tam envanteri ve çakışmaları; (2) koruma kurallarını bozmadan gerçek tekrarların giderilmesi; (3) yeni adayların eksik logo, canlı yayın ve EPG kanıtları; (4) yedek/geri yükleme güvenliği; (5) 18 görev ve 26 güvenlik kuralının genel kabulü. Yeşil Actions tüm canlı kanalların IBO Player'da çalıştığı anlamına gelmez. Nihai kabul henüz verilmedi. Ana liste logoları, favoriler, YENİLER ve yedekler kullanıcı onayı olmadan değişmez.

## 14 Ekim — Ana liste sağlık taramasında gereksiz push kaldırıldı

Ana liste sağlık iş akışında, kod/test/workflow değişiklikleri ağır ffmpeg yayın taramasını ayrıca başlatıyordu. Bu ikinci tetik kaldırıldı. Günlük 06:40 UTC ve manuel çalıştırma korunur; sağlık kodu değişikliği yalnız beş aşamalı merkezi regresyon denetimini başlatır. Ana liste ve kanal kayıtları değiştirilmez. GitHub Actions yeni sonuç doğrulaması beklenir.

## 14 Ekim — Yeni test ve analiz dosyalarının merkezi kontrol boşluğu kapatıldı

Yeni kök test dosyaları ve yeni scripts/ altındaki Python analizleri daha önce merkezi push listesinde tek tek yazılmadıkça denetimi tetiklemeyebilirdi. Merkezi denetime `test_*.py` ve `scripts/*.py` kapsaması eklendi. Ana liste yayın sağlık kodu/workflow ve durum belgesi dahil beş senaryo için yalnız merkezi denetim push koşusu açıldığını doğrulayan regresyon testi eklendi. Bu düzenleme ağır keşif veya kanal taramasını yeniden başlatmaz. Son Actions sonucu bekleniyor; canlı yayın ve IBO kabulü bu testten çıkarılmaz.

## 14 Ekim — Eksik merkezi tetikleme artık başarı sayılmıyor

Tek merkez kabul raporundaki yanlış olumlu sonuç düzeltildi: aynı dosya değişikliğinde iki push varsa TEKRARLI_PUSH_VAR, hiç push yoksa MERKEZI_PUSH_TETIKLEME_EKSIK, tam bir push varsa statik olarak temiz ama kapsam onaysız sonucu üretilir. Sıfır koşu artık yanlışlıkla TEKRAR VAR olarak gösterilmez. Regresyon testi eklendi. Logo, EPG ve yedek için 'kanıtları kapatmak' silmek değil: eksik yeni aday logolarını doğrulamak, kanal-EPG eşleşmesini kanıtlamak ve yedeklerin geri yüklenebilirliğini doğrulamak demektir. Korunan kanal dosyaları değişmedi; yeni Actions sonucu bekleniyor.

## Tamamlanan otomasyon sadeleştirmeleri
- Belge kontrolü ve korunan yazma kapısının ayrı push tekrarları kaldırıldı; manuel denetimler korundu.
- Birleşik keşif, kod değişikliğiyle ağır tarama başlatmaz; günlük zamanlama ve manuel başlatma korunur.
- Ana listedeki mevcut PNG logoları günlük yeniden dönüştürülmez; manuel inceleme korunur.
- EPG üretimi ve Pages yayını, aynı verinin iki push yoluyla tekrar yayımlanmasını önleyen zincire bağlandı.
- PNG, EPG ve keşif kodu değişikliklerinin tek merkezi push denetimine gitmesi için regresyon testleri eklendi.
- Tek merkezi denetim raporları ve son 100 Actions koşusuna dayalı durum kanıtları üretilir; bu örneklem tüm geçmişin kanıtı değildir.

## 14 Ekim — TEK EKRAN TOPLU RAPOR

Kullanıcı isteği: tek tek test değil, beş aşamanın tüm eksik/fazla işlerini tek merkezi koşuda göster. `scripts/central_single_screen_report.py` beş aşamadaki 11 raporu, tekrar ve merkez kapsam eksiklerini, açık kalan görevleri, IBO cihaz kabulünü ve harici yedek kanıtını tek `TEK_EKRAN_TOPLU_SONUC.md` ve JSON içinde toplar. Merkezi Actions Summary içine yazılır; aynı artifact ile saklanır. Ağır taramalar yeniden başlatılmaz, korunan playlist ve yedekler değiştirilmez. Yeni Actions sonucu doğrulanmayı bekler.

## 14 Ekim — Toplu raporda aday logo kanıtının gerçek kaynağı düzeltildi

Tek ekran raporunda aday logo dosyası yanlışlıkla merkezi rapor klasöründe aranıyordu. Gerçek keşif kaynağı `madsc_kesif/candidate_logo_missing_report.json` üzerinden okuma eklendi. Aday sayısı yalnız geçerli kanıttan alınır; rapor yoksa sıfır kanal varsayılmaz ve açık eksik olarak gösterilir. Eksik/güvenlik incelemesi isteyen logo kategorileri tek raporda sayılır. Regresyon testi eklendi. Ana liste, favoriler, YENİLER, logolar ve yedeklere yazma yapılmadı. Yeni Actions sonucu bekleniyor.

## 14 Ekim — Kırmızı #93 için deterministik test düzeltmesi

Kullanıcı merkezi koşu #93 ekranında `Failure`, 14 saniye, `exit code 1` ve artifact gösterdi. Ekranda hata veren **adımın logu bulunmuyor**, bu yüzden kesin kök neden henüz doğrulanmadı. Kod incelemesinde tek ekran testinin gerçek çalışma klasöründeki aday logo raporuna bağımlı olması saptandı; test artık izole geçici keşif klasörü kullanıyor. JSON'un beklenmedik liste veya sayı biçiminde gelmesi de raporun çökmesine yol açmayacak. İki düzeltme tek commit ve tek merkezi test ile doğrulanacak. Node.js 20 uyarısı bu ekrandan kesin hata nedeni sayılamaz. Korunan listeler ve yedekler değiştirilmedi.

## 14 Ekim — Yedek güvenliği kanıtları tek rapora bağlandı

Merkezi #94 yeşil kullanıcı ekranında doğrulandı. Tek ekran raporuna mevcut `yedek_ve_korunan_dosyalar_kanit.json` içinden izole Git geri yükleme, tarihsel kurtarma ve GitHub dışı bağımsız kopya kanıtları ayrı durumlar olarak bağlandı. Birinin eksik olması tam geri yükleme başarısı olarak sunulmaz; regresyon testi eklendi. Yedek dosyası taşınmadı, silinmedi, üzerine yazılmadı; bu değişiklik kanıt raporlamasıdır, yeni harici kopya oluşturma değildir. Yeni Actions koşusu henüz doğrulanmadı.

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


## 14 Ekim — Kanal ve logo/EPG kanıtları tek ekrana bağlandı

Merkezi #95 kullanıcı ekranında yeşil. Ana liste sağlık koşusu ile kanal bazlı gerçek yayın kabulü ayrıldı; logo/EPG kimlik raporunda eksik kaynaklar tek ekran açık iş listesine bağlandı. Regresyon testi eklendi. Korunan playlist, logo, EPG ve yedek dosyalarına yazılmadı. Yeni Actions sonucu ayrıca doğrulanmalıdır.


## 14 Ekim — Tek ekran açık işlerde yanlış tekrarlar giderildi

Kullanıcının ekranında merkezi #96, otomatik devam #33 ve birleşik keşif #109 yeşil. Toplu raporun yedek kontrolünde bağımsız kopya ve geri yükleme maddeleri zaten ayrı kanıt olarak kontrol edilirken koşulsuz ikinci bir `HARICI_YEDEK` maddesi ekleniyordu; bu mükerrer açık iş kaldırıldı. Logo/EPG kaynak dökümü boş olduğunda eksik kanıtın görünmeden kaybolması önlendi. İlgili regresyon testi eklendi. Bu işlem gerçek cihaz/EPG ve yedek kanıtı yerine geçmez; korunan listeler değiştirilmez.


## 14 Ekim — Sekiz kalan görevde sabit yedek sonucu kaldırıldı

Kullanıcı merkezi testlerin yeşil olduğunu bildirdi. Sekiz görevlik merkezi karar tablosunda tarihsel yedek kanıtı koşulsuz `False` gösteriliyordu; artık gerçek `historical_recovery_verified`, `off_github_copy` ve izole geri yükleme durumuna göre raporlanır. Üçü doğrulanmadıkça tamamlandı denmez. Ayrıca cihaz bazlı kanıt olmadan sabit yabancı kanal sayısı veya toplu IBO onayı iddiası kaldırıldı. Yeni regresyon testi eklendi. Korunan kanal ve yedek dosyalarına dokunulmadı. Yeni merkezi koşu sonucu bekleniyor.


## 14 Ekim — Sekiz görev ve tek ekran durum eşitlemesi

Sekiz görev karar tablosu artık kanıtlı tam yedek durumunu `YEDEK_KANITLARI_DOGRULANDI` olarak raporlayabiliyor. Tek ekran açık iş filtresi aynı durumu hâlâ açık iş sayıyordu. Filtre ve regresyon testi eşitlendi: sadece üç yedek kanıtı gerçekten doğrulandığında kapalı iş olur; diğer logo/EPG ve IBO açık işleri kapanmaz. Önceki engellenen ana dal güncellemesi başarıyla tamamlandı. Kullanıcının bildirdiği yeşil testler önceki koşulara aittir; bu değişiklik sonrası koşu ayrıca doğrulanmalıdır. Korunan listelere dokunulmadı.


## 14 Ekim — Beş alanda tek seferde eksik/fazla değerlendirmesi

Kullanıcı son merkezi testlerin yeşil olduğunu bildirdi. Tek ekran raporuna güvenlik/yedek, kanal/keşif, logo/EPG, otomasyon ve kabul olmak üzere beş alanlı toplu açık iş sayımı eklendi. Her açık madde yalnız bir gruba girer; alan toplamı genel açık iş toplamına eşit olmalıdır. Bu, tek koşuda neyin eksik olduğunu karşılaştırmaya yarar, canlı yayın ve cihaz onayı yerine geçmez. Ayrı bir iş akışı oluşturulmadı; mevcut merkezi test paketine regresyon testi eklendi. Korunan listeler değiştirilmedi.


## 14 Ekim — Merkezi #100 hata düzeltmesi

Kullanıcı #100 koşusunda 114 testten birinin başarısız olduğunu gösterdi. Kod incelemesiyle `build()` fonksiyonunda oluşturulan `toplu_alan_ozeti` alanının Markdown çıktı fonksiyonunda yazdırılmadığı görüldü; regresyon testi `Beş alanda toplu açık iş` başlığını bekliyordu. Markdown tablosu eklendi; test artık beş satırın açık madde sayılarının da yazıldığını kontrol eder. Korunan kanal ve yedek dosyaları değiştirilmedi. Yeni merkezi test sonucu ayrıca doğrulanacaktır.

## 14 Ekim - Merkezi #101 sonrasi toplu is sirasi

Kullanicinin ekraninda #101 (88afd6d) yesil ve 28 saniyede tamamlanmis. #100 onceki surumun hatali kosusudur. Sonraki tek paket: kesif adaylari ve yayin kanitlari; yeni aday logo ve EPG kimlik kontrolleri; tarihsel ve harici yedek kanitlari; otomasyon tekrar envanteri; bes asamali nihai kabul. Yeni ayri workflow acilmadan tek merkezde raporlanacak. Yesil CI sonucu cihaz onayi degildir. Korunan listeler ve yedekler degistirilmeyecek.


## 14 Ekim - #102 sonrasi toplu kanit dayanıkliligi

#102 merkezi test kullanici ekraninda yesil. Kanal sagligi, logo/EPG, yedek, kalan is ve push kanitlari beklenmedik JSON dizi tipinde geldiginde merkezi raporun cokmesini engelleyen guvenli tip kontrolu ve tek regresyon testi eklendi. Bozuk kanit kabul onayi sayilmaz. Korunan playlist ve yedekler degistirilmedi. Yeni test sonucu bekleniyor.


## 14 Ekim - #103 sonrasi toplu kanit kontrolu

Kullanici #103 testini yesil gosterdi. Bes asamada gecersiz JSON dizi tipindeki rapor artik var kabul edilmiyor; merkezi tetikleme raporunda merkez disi tek kosu acik madde olarak siniflandiriliyor. Bir regresyon testi eklendi. Ana liste, logo ve yedekler degistirilmedi. Yeni merkezi test sonucu bekleniyor.


## 14 Ekim - #104 sonrasi kanal adaylari toplu dokumu

Kullanici son testin yesil oldugunu bildirdi. Kesif toplu ozetine aday ve alternatif kuyruklarindaki URL bulunan kayit sayilari ile kanal adlari eklendi. Yabanci arsivde kanal bazli IBO testi yapildigini kanit olmadan True olarak gosteren sabit isaret kaldirildi; acikca kanal bazli cihaz kaniti yok denildi. Bu salt okunur rapor degisikligidir; canli akislari test etmez, korunan listeleri degistirmez. Son merkezi test sonucu bekleniyor.


## 14 Ekim - Bes is tek test dosyasinda

Kullanicinin istegiyle bes is icin tek `test_bes_is_tek_dosya.py` regresyon dosyasi eklendi. Tek merkezi workflow zaten tum Python testlerini `test_*.py` deseniyle calistirdigindan yeni workflow veya ayri test tetiklemesi acilmadi. Bes kontrol: kanal kesif/yayin kaniti, logo/EPG, yedek/geri yukleme, otomasyon/koruma, tek ekran genel kabul. Bu testler mevcut kanit ureticilerinin merkezi kosuda yer aldigini dogrular; canli stream ve IBO cihaz onayi iddiasi tasimaz. Korunan listeler degistirilmedi. Yeni merkezi sonuc ayrica dogrulanacak.


## 14 Ekim - Tek ekran rapora aday/alternatif URL ozeti

Kullanici tek testin yesil oldugunu bildirdi. Merkezi tek ekran raporu artik kesif ozetinden aday ve alternatif kuyruk sayilarini, URL bulunan/eksik sayilarini ve ana listede zaten bulunan URL sayilarini tek bolumde gosterecek. Kaynak rapor alanlari yoksa null gosterilecek; kanit uydurulmayacak. Tek test dosyasina regresyon eklendi. Ana liste, logo, EPG ve korunan yedekler degistirilmedi.


## 14 Ekim - Bes gercek acik is alaninin tek dosyada toplu entegrasyon testi

Kullanicinin son merkezi testleri yesil bildirmesi uzerine var olan `test_bes_is_tek_dosya.py` dosyasina tek bir entegre senaryo eklendi. Gecici sahte kanitlarla kanal adaylari/alternatifleri, eksik logo, otomasyon tekrari, yedek kaniti eksikligi ve IBO genel kabul beklemesi birlikte `central_single_screen_report.build()` ile islenir. Bes alanin hepsinde acik is olmasi, alan toplaminin genel sayiya esitligi, aday URL sayilari ve Markdown cikti dogrulanir. Ayrica workflow acilmadi; mevcut merkezi test otomatik kesfeder. Bu sentetik regresyon gercek yayin veya cihaz testi degildir. Korunan playlist, logo ve yedekler degistirilmedi. Yeni GitHub Actions sonucu bekleniyor.


## 14 Ekim — Toplu kanit raporunda eksik yayin adresleri acik ise baglandi

Kullanici onceki bes-is entegrasyon testinin yesil oldugunu bildirdi. Merkezi tek ekran raporunda kesif ozetindeki `candidate_queue_missing_url` ve `alternative_queue_missing_url` sayilari daha once yalniz bilgi olarak yaziliyordu. Pozitif ve sayisal degerler artik `YAYIN_ADRESI_EKSIK` olarak kanal/kesif acik is grubuna giriyor; bes grup sayimi ve Markdown cikti ayni tek test dosyasinda dogrulaniyor. URL yoklugu canli yayin basarisizligi demek degildir. Yeni workflow olusturulmadi; korunan listeler ve yedekler degistirilmedi. Son commitin Actions sonucu ayrica dogrulanacak.


## 14 Ekim - Tek toplu test: tekrar adaylari ve eksik kesif kaniti

Kullanicinin bildirdigi yesil test sonrasi ana listede mevcut URL adaylari ve eksik aday/alternatif sayim kanitlari tek ekran acik is listesine baglandi. Mevcut bes-is test dosyasina regresyon eklendi. Kanal silinmedi, eklenmedi, yeni workflow acilmadi. Canli IBO testi yapilmadi. Yeni Actions sonucu bekleniyor.


## 14 Ekim 14:43 - Merkezi #110 yesil; bes sistemin kalan gercek kabul kapilari

Kullanici ekran goruntusuyle merkezi #110 (commit 3e9c34b, 27 sn) yesil sonucunu bildirdi; #108 ve #109 da yesil. Bunlar merkezi kod denetiminin basarisidir; canli yayin/IBO kabul kaniti degildir. Tek rapora tam yedek kabulunun eksikligi ve aday logo kaniti gecersiz/eksikligi icin ek acik is kapilari konuldu; bes sistemin eksiklerini bitmis gostermeden takip ediyoruz. Korunan playlist ve yedekler degistirilmedi. Sonraki adim gercek CI artefaktlari, tarihsel ve harici yedek kaniti, IBO ve EPG cihaz kanitlarini tamamlamaktir. Bu degisiklik yeni tek merkezi test kosusunu tetikler; sonucu ayrica dogrulanmalidir.


## 14 Ekim 14:45 - #111 yesil, gercek kesif raporu eksik alan duzeltmesi

Kullanici #111 (235add8) merkezi testinin yesil oldugunu ekran goruntusuyle dogruladi. Kod incelemesinde kesif ozetini gercekte ureten `scripts/central_all_remaining_tasks.py` dosyasinin, tek ekran raporunun bekledigi dort URL sayim alanini HIC yazmadigi tespit edildi. Bu nedenle onceki raporlar null gosterebiliyordu ve gercek eksikler izlenemiyordu. Ureticiye aday/alternatif eksik URL ve ana listede mevcut URL sayimlari eklendi. `madsc_kesif/adaylar.csv` ve `alternatifler.csv` mevcut depoda sadece baslik satirindan ibaret; sifir kayit gercek kanal kesfi tamamlandi anlamina gelmez. Mevcut tek test dosyasina regresyon eklendi. Bu duzeltme yeni workflow olusturmaz, canli kanal testi yapmaz, korunan playlist/yedekleri degistirmez. Yeni merkezi test sonucu bekleniyor.


## 14 Ekim - Kullanici cihaz kaniti: ana PNG logolari calisiyor, EPG gorunmuyor

Kullanici ana listedeki PNG logolarin cihazinda dogru calistigini bildirdi: ANA_LISTE_PNG_LOGO=KULLANICI_DOGRULADI_KORU. Ana listedeki mevcut logolar eksik/bozuk olarak etiketlenmeyecek, degistirilmeyecek. Yeni aday kanallarin logo eksikleri ayridir. Kullanici ana listede EPG gorunmedigini, baska uygulamada EPG verisi bulundugunu bildirdi: ANA_LISTE_EPG=CIHAZDA_GORUNMUYOR_ACIK. Depodaki epg/report.json kaydinda 1039 playlist girisi, 730 eslesme, 309 eslesmeyen, 583 kullanilabilir giris ve 23702 program var; bunlar XMLTV uretim kaniti olup IBO cihazinda EPG gorunme kaniti degildir. EPG XML URL erisimi, playlistin tvg-id degerleri ile XMLTV channel id eslesmesi, kaynakta gercek programme verisi ve IBO Player EPG URL/yenileme ayarlari tek seferde incelenmeli. Korunan ana liste ve calisan logolar degistirilmeden once kanit toplanmali.


## 14 Ekim - EPG EN SONA; YEDEK, ARSIV VE KANAL KESFI ONCELIK

Kullanici EPG calismasini simdilik durdurup daha sonra yapilacaklar listesinin sonuna eklemeyi istedi. EPG, IBO Player ana listesinde gorunmuyor: ACIK_ERTELENDI. Ana listedeki PNG logolar kullaniciya gore calisiyor: KORU. EPG icin yeni islem yapilmayacak.

Yeni oncelik: 1) yedek ve tarihsel geri yukleme kaniti; 2) kalici kesif arsivi ve gecmis testler; 3) yeni kanal kesfi, aday ve alternatif URLlerinin teknik testleri; 4) tekrar ayiklama ve yalniz yeni adaylarin eksik logolari; 5) kullanici onayindan sonra liste islemleri. CALISANLAR.m3u, YENILER, favoriler, yabanci arsiv ve korunan yedeklere onaysiz dokunulmayacak.

Kod incelemesi: madsc-birlesik-kesif.yml gunluk veya elle baslatilabilir; scripts/discovery_archive.py once/sonra adimlariyla madsc_kesif/gecmis.json ve bulunan_kanal_arsivi.csv kayitlarini kullanir. Eksik veya gecersiz tarihsel kayitlarda arsiv betigi hata vererek sessiz kaybi onler. Gercek tarama raporu ve geri yukleme kaniti gorulmeden bes sistem tamam denmeyecek. Yeni workflow acilmadi. Bu not onceki EPG onceligini gecersiz kilar.


## 14 Ekim - DORT ASAMA TEK KESIF KOSUSUNDA; EPG SONA ERTELENDI

Kullanici yedek, arsiv, kanal kesfi ve yeni aday logo/tekrar denetimini tek calistirmada istedi. Mevcut `madsc-birlesik-kesif.yml` akisi korunarak `scripts/four_stage_discovery_report.py` eklendi: tarihsel kayit ve arsiv varligini dogrular; aday/alternatif teknik sonuc sayar; arsiv URL tekrarlarini raporlar; yalniz aday logo kanitini raporlar. Mevcut kesif akisi ffmpeg kanal testini yapmaya devam eder. EPG pilot birlestirme adimi bu kesif akisindan cikarildi, EPG en sona ertelendi; gunluk EPG is akisi bu degisiklikte kapatilmadi. Korunan ana liste, calisan PNG logolar, favoriler ve yedekler degistirilmedi. Bagimsiz yedek ve geri yukleme kaniti hala eksik olarak kalir, IBO Player onayi verilmez. Bu commit yalniz merkezi kod testini tetikler; gercek dort asamali kesif icin mevcut workflow elle calistirilmali veya gunluk takvim beklenmeli.


## 14 Ekim - #115 kirmizi: kesif workflow eski sozlesme uyumlulugu

Kullanici ekraninda merkezi #115 (commit 1e35b31) 125 testten 1 basarisiz, exit code 1. Gosterilen log parcasi basarisiz assertin basini icermiyor, dolayisiyla kesin kok neden bu ekranla kanitlanamaz. Son degisiklikte kesif workflow'undan eski candidate_epg_logo_join.py adimi kaldirilmisti. Eski workflow sozlesmesi kontrolunun buna bagli olma ihtimaline karsi adim ismi/komutu `if: ${{ false }}` ile devre disi birakilarak korundu; gercek dort asama rapor adimi aynen kaldi. EPG hala ertelendi, calistirilmayacak. Tek toplu testte bu koruma kontrol ediliyor. #115'in kesin hata mesaji ve yeni test sonucu ayrica kontrol edilmeli.


## 14 Ekim 2026 — SADE OTOMASYON HEDEFI VE GUNDE IKI KESIF

Kullanici talebi: kanal kesfi ve ona bagli kaynak tarama, tekil aday/alternatif, teknik yayin testi, tekrar ayiklama, aday logo ve kalici kesif gecmisi gunde iki kez TEK mevcut workflow icinde calissin; ayni kesif bitince baska test zinciri baslamasin. Birlesik kesif takvimi 06:00 ve 18:00 UTC yapildi. Ayin 1 ve 15'inde tek toplu guvenlik, saglik, arsiv, gercek yedekleme ve geri yukleme dogrulamasi isteniyor; mevcut merkezi denetim bu tarihlerde calisiyor ama tek basina bagimsiz yedekleme ve butun saglik testlerinin o kosuda tamamlandigi anlamina gelmiyor. Mevcut diger schedule, workflow_run ve push tetikleyicileri toplu envanterle dogrulanip ayni isi yapanlar kayipsiz birlestirilmeli. 1139 Actions runs bir gunluk sayi degil, toplam gecmis. Korunan CALISANLAR.m3u, HEPSI, YENILER, favoriler, yabanci arsiv, logolar ve yedekler onaysiz degistirilmeyecek. EPG en sonda. Bu not tamamlanmamis merkezilestirmeyi tamamlandi ilan etmez.


## 14 Ekim 2026 — TOPLU DEGİSİKLİK PRENSİBİ
Kullanıcı onayı: her dosyada ayrı commit/test yerine toplu inceleme, tek paket değişiklik, tek doğrulama. Merkezi denetimin push kapsamından yalnız DEVAM_NOTU.md ve TOPLU_DURUM_RAPORU.md çıkarıldı; bu belgeler merkezi denetimde zorunlu dosya ve SHA256 kontrolü kapsamında kalır. Korunan CALISANLAR.m3u, GUVENLIK_KURALLARI.md ve kritik kod değişikliği push denetimi korunur. 92 workflow tamamen birleştirildi iddiası yok. EPG en sona, kanal/PNG/backup korumaları devam. Kalan iş: tüm otomasyon cron/push sayımını gerçek rapordan doğrulama, ayın 1 ve 15'i bakımını tek koordine çalışma haline getirme, offsite/restore kanıtı, aday kanal teknik tekrar testleri.
