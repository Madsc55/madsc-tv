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
