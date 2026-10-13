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
