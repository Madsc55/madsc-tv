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
