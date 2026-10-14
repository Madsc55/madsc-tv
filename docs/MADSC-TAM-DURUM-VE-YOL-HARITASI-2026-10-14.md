# MADSC — Durum, hedefler ve sonraki aşama (14 Ekim 2026)

## Amaç ve değişmez kurallar
- 92 eski GitHub Actions workflow'unu görev kaybı olmadan beş ana kategori altında toplamak: 1 Güvenlik, 2 Kanal keşfi, 3 Kanal testleri (logo ve EPG dahil), 4 Arşiv/yedek, 5 Genel bakım.
- Kullanıcı tek tek test yaptırmak istemiyor: toplu düzenleme, tek beşli CI koşusu, hata varsa toplu düzeltme ve yalnız kanıtlı sonuç raporu.
- CALISANLAR.m3u, HEPSİ/favoriler, ⭐ YENİLER, URL, kimlik, sıra, kategoriler, doğrulanmış logolar ve bütün korunan arşiv/yedekler onaysız değiştirilmez.
- Kullanıcı onayı olmadan ana listeye veya ⭐ YENİLER'e kanal eklenmez; çalışan/çalışmayan, otomatik test ve kullanıcı IBO onayı ayrı tutulur.
- 92 eski workflow davranışsal eşdeğerlik ve bağımlılık kanıtı olmadan silinmez veya kapatılmaz.

## Doğrulanmış teknik kazanımlar
- PR #71 (madsc/bes-sistem-toplu-birlestirme) açık ve draft; beş yeni salt okunur workflow oluşturuldu.
- Beş kategori tek merkezden sıralı çalışabiliyor; GitHub Actions #38630252033 koşusunda 5/5 job success ve beş artifact kaydı doğrulandı. Bu geçmiş koşudur; sonraki değişikliklerin sonucu değildir.
- 92 eski workflow'u bekleyen ve sayısı değişirse hata veren statik envanter var; cron, push, workflow_run, izin ve betik eşleştirmesi raporlanıyor.
- central_workflow_inventory.py: yedek kategori 4, EPG/logo kategori 3; kategori regresyon testleri eklendi.
- Tek-merkez push çakışması nedeniyle 30 testte 1 hata görüldü; madsc-05 push paths yalnız kendi YAML dosyasına daraltıldı. Düzeltmenin yeni canlı CI kabulü henüz doğrulanmadı.
- Beşli kabul koşusuna tek-merkez regresyonu ve önceki dört kategorinin success olmasını zorunlu kılan adım eklendi.
- five_system_migration_audit.py migration_complete=False; sırf beş dosya var diye eşdeğerlik iddia edilmez.

## Sistem bugün neler yapıyor?
1. Güvenlik: SHA256, korunan yazma kapısı, statik risk ve regresyon raporları. Tam üretim güvenlik eşdeğerliği kanıtı yok.
2. Keşif: kaynak mutabakatı, tekrar denetimi, IBO aday kuyruğu raporları. Günde iki kez çalışan eski keşif üretiminin devri yok.
3. Test: kimlik/EPG/logo raporları, 50 kanallık salt okunur yayın sağlık partisi ve regresyonlar. 75 adayın tamamı, 51 retest, 24 ffprobe başarısızı, 4 alternatif ve IBO cihaz onayı tamamlanmadı.
4. Arşiv: izole Git restore, arşiv ve yedek kanıt raporları. Harici bağımsız geri yükleme ve tüm tarihsel kayıtlar kanıtlanmadı.
5. Bakım: envanter, 18 görev, açık iş ve toplu raporlar. 92/92 davranışsal eşdeğerlik ve otomatik tetik devri tamamlanmadı.

## Eski üretim bağımlılıkları
- 9 zamanlanmış eski workflow; günlük 06:00/18:00 UTC keşif, EPG günlük üretim, Pages workflow_run yayın, günlük VOD, aylık 1/15 sağlık/yedek ve diğer kontroller.
- Eski işlerin devam etmesi beşli sistemin bunların yerini aldığı anlamına gelmez.
- Yeni beşli testlerin hepsinin yeşil olması yalnız test edilen kapsamı kanıtlar; canlı cihaz, offsite restore ve üretim zinciri ayrı kapılardır.

## Sonraki güvenli ve ölçülebilir aşama
A. En güncel beşli Actions koşusunun 5 job ve step sonuçlarını doğrula; varsa hata logundan düzelt. Push run sorgusu sınırlıysa başarı uydurma.
B. 92 satır için eski komut, tetik, yazma izni, artifact, bağımlılık ve yeni kategoride gerçek karşılık matrisi üret. 'Yok', 'kısmi', 'eşleşen' ve 'canlı doğrulandı' durumlarını ayır; yalnız betik adı eşleşmesi davranış kanıtı değildir.
C. Önce eksik veya riskli otomatik işler: EPG→Pages, keşif 2/gün, VOD, yedek 1/15, workflow_run ve otomatik yazma izinleri. Korunan veriye yazmadan dry-run/izole test yap.
D. Canlı yayın ve IBO kabulü, offsite restore ve tarihsel listeler için ayrı kanıt topla.
E. A-D tamamlanınca tek beşli kabul koşusu ve onay; ancak bundan sonra kontrollü tetik geçişi, eski kod geçmişi korunur.

## Kabul durumu ve değer
- Teknik kurulum: var. Beşli entegrasyon: geçmişte 5/5 doğrulandı. Son değişikliklerin CI kabulü: doğrulanmadı. 92/92 üretim eşdeğerliği: tamamlanmadı. PR #71: açık/draft.
- Teknik değer: merkezi kontrol, tekrar tespiti, koruma ve raporlama altyapısı. Parasal değer: canlı kalite, haklar, maliyet ve kullanıcı kanıtı olmadan hesaplanamaz.
- İlerleme yüzdesi verilmez; sayısal bir yüzde, henüz ölçülmeyen görev eşdeğerliğini yanlış temsil eder.
