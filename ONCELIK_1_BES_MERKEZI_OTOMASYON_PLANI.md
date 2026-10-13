# EN YUKSEK ONCELIKLI PLAN — 89 GITHUB IS AKISINI 5 MERKEZI OTOMASYONDA BIRLESTIRME

Tarih: 13 Ekim 2026
Durum: NOT EDILDI — UYGULAMA ICIN KULLANICININ SONRAKI TALIMATI BEKLENIYOR
Oncelik: 1 / EN ONEMLI SISTEM GELISTIRME PLANI

## Kullanici karari
- Madsc55/madsc-tv deposundaki mevcut 89 GitHub Actions is akisini analiz ederek, mumkun oldugunca **5 merkezi otomasyon** altinda toplamak.
- Her degisiklik icin yeni bir test ve workflow olusturma aliskanligini bitirmek.
- Ayni isi veya ayni testi iki kere yaptirmamak; gereksiz push/workflow_run/schedule zincirlerini kaldirmak.
- Gereksiz gunluk onlarca kontrol yerine, kapsamli denetimleri **ayda yaklasik 3–5 kez** yapmak.
- Kullanici talimatli kanal ekleme, silme, tasima gibi islemlerde **tek calistirma icinde gerekli kisa dogrulama** yapmak; koruma kontrolunu kaldirmamak.
- Tum dosyalar, kanal listeleri, yedekler, arşivler, test gecmisi, hata durumlari, eksik kalan isler ve otomasyonlar merkezi olarak denetlensin.
- Kisa, net, tek son rapor verilsin. Kullanici gereksiz ara raporlarla yorulmasin.

## Hedef 5 otomasyon (taslak; envanter tamamlaninca netlestirilecek)
1. **Merkezi sistem sagligi ve guvenlik:** dosyalar, korunan listeler, workflow sagligi, hatalar, eksikler, geri yukleme kanitlari; ayda 3–5 kapsamli denetim.
2. **Birlesik kanal kesfi ve aday testleri:** eksik Turk kanallari, resmî/yasal yayin kaynaklari, erisim testi, alternatifler ve tekrar ayiklama; belirlenen periyotta.
3. **Kanal kalite kontrolu:** yayin durumu, logo, EPG, kimlik ve kategori uyumu; uygun araliklarla ve ortak raporla.
4. **Yedek ve arsiv butunlugu:** yedeklerin korunmasi, arsiv dogrulama, sayi tutarliligi, geri donus guvencesi; merkezi plan.
5. **Kullanici onayli liste islemleri:** onayli kanal tasima/ekleme/cikarma ve ayni is icinde bir kerelik koruma/dogrulama; gereksiz ayri test yok.

## Zorunlu uygulama kurallari
- ONCE 89 workflow'un tetikleyicilerini (push, schedule, workflow_run, dispatch), izinlerini, yazdigi dosyalari, bagimliliklarini ve son calisma durumlarini envanterle.
- 5'e indirgemeden once eski otomasyonlarin kritik islevlerini kaybetmedigini dogrula; mevcut korumalar ve kullanici onay kapilari aynen korunacak.
- Tekrarlanan kontrolleri ayni is akisi icinde birlestir; ayni commit icin gereksiz ek is akisi calistirma.
- Gunluk otomatik kanal arama islevinin eski kullanici tercihlerine uygunlugu ayri kontrol edilmeli; kapsamli denetimle karistirilmamali.
- Veri kaybi riski varsa islemi durdur, yedek al, guvenli geri donus plani uygula.
- `CALISANLAR.m3u`, ⭐ YENİLER, FAVORİLER, YEDEKLER, arşivler ve korunan kategoriler onaysiz degistirilmeyecek.
- Once merkezi sistemin kapsam ve sonuc raporu dogrulanacak; sonra eski workflow'lar kademeli ve geri alinabilir sekilde pasiflestirilecek.
- Sadece test sayisini azaltmak degil, **daha az ama gercekten anlamli ve dogru kontrol** yapmak hedefleniyor.
- Islem tamamlaninca kullaniciya: 89'dan kac otomasyona inildigi, hangi islerin korundugu, hangi testlerin birlestigi, hangi sorunlarin kaldigi tek ozetle bildirilecek.

## Neden bu en onemli plan?
Kullanici mevcut sistemin her degisiklikte onlarca test uretmesinden ve uzun suren tekrarlardan yoruldu. Yeni kanal/ozellik gelistirmelerinden once bu sadeleştirme ve merkezi yonetim plani onceliklidir.

## Mevcut tespit
13 Ekim 2026 tarihinde .github/workflows altinda 89 dosya goruldu. Ayin 1 ve 15'inde calisan `madsc-aylik-merkezi-denetim.yml` zaten mevcut; onu yeniden kullanmak oncelikli. Bu not yeni otomasyon baslatmaz veya mevcutlari kapatmaz.


## 13 Ekim 2026 — Son görüşmede netleşen çalışma düzeni (öncelikli ek not)
Kullanıcı bu düzenin de kaydedilmesini ve sonraki çalışmada buradan devam edilmesini istedi.

### Hedef beş ana sistem ve önerilen takvim
1. **Güvenlik ve sistem sağlığı:** Kodlar, izinler, GitHub Actions, dosyalar, korunan kategoriler; haftalık kapsamlı kontrol.
2. **Birleşik kanal keşfi:** Listede olmayan ücretsiz Türk TV kanalları, resmî/yasal internet kaynakları, tekrar ayıklama; **günde bir kez**.
3. **Birleşik kanal kalite testleri:** Yayın bağlantısı, logo, EPG, kalite, alternatifler; haftalık toplu kontrol.
4. **Arşiv ve liste bütünlüğü:** Çalışanlar, çalışmayanlar, yabancılar, yedekler, arşivler, sayılar ve geri yükleme; 15 günde bir kapsamlı kontrol.
5. **Merkezi yönetim ve yapılacaklar:** Tamamlanan işler, yapılmayan işler, başarısız koşular, kalan eksikler, tek sonuç raporu; aylık özet.

Takvimler hedef taslaktır; aynı kapsamı farklı sıklıklarla iki kez çalıştırmayacak şekilde tüm tetikleyiciler incelendikten sonra kesinleştirilecek. Kanal keşfi günlük kalsın; kapsamlı sistem denetimleri gereksiz yere her gün tekrarlanmasın. Kullanıcı onaylı liste değişiklikleri yapılırken kısa güvenlik kontrolü değişikliğin içinde **bir kez** çalışsın.

### Uygulama sırası ve kayıt tutma
- Önce bütün workflow dosyalarının gerçek envanteri: neyi çalıştırıyor, ne zaman, neyi değiştiriyor, bağımlılıkları, geçmiş hataları ve gereksiz tekrarları.
- Sonra beş ana sistem altında ortak adımlar, tek rapor, iş durumu: **YAPILDI / YAPILMADI / HATALI / BEKLİYOR**.
- Mevcut güvenlik kuralları ve yedekleri koru; hiçbir korunan listeyi veya kanalı kullanıcı onayı olmadan değiştirme.
- Eski otomasyonları ancak eşdeğer işlevleri yeni sistemde doğrulandıktan sonra kademeli ve geri alınabilir şekilde kapat.
- Her yeni kanal/özellik için ayrı workflow oluşturmak yerine mevcut beş ana otomasyonun uygun adımını kullan.
- Kullanıcıya yalnızca kısa, somut sonuçları ve gerçek kalan işleri bildir; başarıyı doğrulamadan tamamlandı deme.

### Şu ana kadarki uygulama durumu
- GitHub'da `.github/workflows/madsc-birlesik-kesif.yml` keşif zamanlaması `0 6,18 * * *` yerine `0 6 * * *` olarak güncellendi (commit `b7896f195f44f3cf59da3f3855a5c1cdcb678288`).
- `.github/workflows/iptv-test.yml` için haftalık zamanlamaya geçiş denemesi güvenlik kontrolü tarafından engellendi; **değişiklik yapılmadı**.
- 89 workflow ilk sayımdı; sonradan yeni workflow eklenmiş olabilir, canlı envanterden güncel sayı tekrar doğrulanmalı.
- **Beş otomasyona birleştirme henüz yapılmadı.** Bu not uygulanmış değişiklik gibi gösterilmemeli.

### Kullanıcının ana amacı
'Kafamız karışmasın; ne yaptık, ne yapmadık, ne çalışıyor, ne eksik tek yerden belli olsun. Günlük arama bir kere çalışsın, gereksiz tekrar testleri olmasın. Kısa ve öz ilerleyelim.'
