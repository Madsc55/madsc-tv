# Sekiz görev — tek toplu çalışma denetimi (13 Ekim 2026)

Bu dosya bir tamamlama sertifikası değildir. Kullanıcı yeni kanal testlerinin bitmesini beklemeden sekiz işin birlikte geliştirilmesini istemiştir. **Ana liste, YENİLER, favoriler, sıralama ve yedekler izinsiz değiştirilemez.**

| Görev | Yapılan / mevcut altyapı | Eksik ve kabul koşulu |
|---|---|---|
| 1. Felaket koruması | Tek arşiv `MADSC-TUM-SISTEM-YEDEK.tar.gz`, SHA256 izole açma testi; Actions #38340513782 başarılı | 30 gün saklama, GitHub dışı bağımsız kopya ve secrets/IBO ayarları eksik; kullanıcı erteledi |
| 2. Kaynak envanteri | 156 tanımlı kaynak, hedef 155; keşif özetinde gerçek sayılar ve fark açıkça raporlanır | 156 kaynağın erişilebilirliği ve benzersizliği doğrulanmadan hedefi değiştirme; günlük keşif yalnız Türkçe kaynak alt kümesini tarar |
| 3. Türk kanal önceliği | Kaynak kimliği ve Türkçe dil ipucu keşif → üç aşama → son kontrol hattında korunur | Kaynak adı kanalın ülke/kimlik kanıtı değildir; diaspora ve yerel kanal kimliği ayrıca doğrulanmalı |
| 4. Test geçmişi | Eski check'ler korunur; aynı URL'nin birden fazla kaynak kimliği `source_history` altında birleştirilir | Kullanıcı IBO onayı ile teknik test ayrımı korunmalı; gerçek Actions sonucu gerekli |
| 5. Kanal kimliği | Teknik decode geçişi kanalın gerçekten belirtilen kanal olduğu anlamına gelmez | Görüntü/isim/logonun kimliği manuel veya güvenilir kanıtla onaylanmadan listeye ekleme yok |
| 6. Logo ve EPG | Aday logo/EPG raporları ve EPG üretimi mevcut | İsveç IBO cihazında EPG ve logo eşleşmesi henüz kanıtlanmadı |
| 7. Hukuki kaynak kontrolü | Kaynak kökeni ve şüpheli yayın ayrı değerlendirilir | Lisans/dağıtım hakkı doğrulanmayan adaylar onaylı/yasal olarak işaretlenmez |
| 8. Güvenlik | Korunan listelere onaysız son kontrol aktarımı PR #31 ile kaldırıldı; mevcut workflow sağlık testleri | Branch protection ve GitHub izinleri ayrıca gözden geçirilmeli; rapor yazma yarışları izlenmeli |

## Tek teslim kuralı
Geliştirme tek PR'da birleştirilir; her aşamanın gerçek Actions sonucu kaydedilir. Teknik başarı veya rapor oluşturulması **kullanıcının IBO Player cihazında çalışıyor** ya da **ana listeye eklemeye hazır** anlamına gelmez.

## 13 Ekim — doğrulanmış yeni durum

- Genel sistem sağlık ve güvenlik denetimi **#38343031174 ve #38343045889 SUCCESS**. 19 - Bütünleşik Güvenli Kontrol **#38343031177 ve #38343045881 SUCCESS**. Bu sonuçlar tanımlı otomatik testler içindir; tüm sistemin risksiz olduğunu kanıtlamaz.
- PR #35 ile teknik testten ayrı kimlik, lisans, logo ve İsveç IBO/EPG kanıt durumları eklendi. PR #36 ile çoklu kaynak geçmişinin final kuyruğunda korunmasına regresyon testi eklendi. PR #37-#40 ile workflow izin taraması ve test hataları düzeltildi.
- GitHub `main` branch protection API sorgusu **403 Resource not accessible by integration** döndürdü. Koruma ayarlarının etkinliği doğrulanamadı; **korunuyor** diye raporlanmamalı. Bu ayarları değiştirme izni de yok.
- GitHub Actions genel denetimi tüm dosyaların tüm içeriğini güvenlik açısından sertifikalandırmaz; mevcut kod, workflow, rapor ve liste bütünlüğü kontrollerini çalıştırır.
- Kullanıcı ertelediği GitHub dışı yedekleme ve cihaz/secrets aktarımı daha sonra ayrıca ele alınacak. Kimlik, hak sahipliği, logo ve İsveç IBO gerçek cihaz onayı eksik olduğu sürece otomatik listeye ekleme yok.
