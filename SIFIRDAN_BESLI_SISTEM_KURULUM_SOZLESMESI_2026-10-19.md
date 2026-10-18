# MADSC TV — SIFIRDAN BEŞLİ SİSTEM KURULUM SÖZLEŞMESİ (19 Ekim 2026)

## Son kullanıcı kararı — önceki taşıma planlarının yerine geçer
Yeni beşli sistem **sıfırdan yazılacak**. Eski 92 workflow, onların otomatik tetikleri, betikleri veya mevcut otomasyon kodu **taşınmayacak, kopyalanmayacak, yeniden bağlanmayacak**. Eski sistem yalnızca *ne yapılmak istendiği*, koruma kuralları, kanal sınıfları ve geçmiş hata/kanıt kayıtlarını anlamak için **salt okunur referans**. Eski devam notlarındaki '92 workflow'u davranışsal olarak taşı' ifadeleri artık geçerli uygulama talimatı değildir. Eski otomasyonlar bu hazırlık aşamasında silinmeyecek veya kapatılmayacak; yeni sistem eski sistemden tetiklenmeyecek.

## Değişmez koruma sınırı
- IBO Player Pro'daki **bütün mevcut kategoriler, çalışan kanallar, kanal adları, URL, tvg-id, logo, sıra, HEPSİ, FAVORİLER ve cihaz favorileri** aynen kalır.
- CALISANLAR.m3u, YENILER, YEDEKLER, tüm eski M3U/M3U8, EPG, logolar, arşivler ve üretim yayın yollarına yazma **yasak**.
- Yeni IPTV M3U listesi **ayrı yeni dosya** olarak üretilecek. Önce aday/deneme listesi; kullanıcı ve gerçek cihaz onayı olmadan IBO'ya veya mevcut listeye bağlanmayacak.
- main, PR #71, eski workflow ve mevcut beşli çalışma dalına dokunulmayacak. Silme, eski tetik kapatma veya üretime alma yok.

## Beş yeni sistem — sıfırdan tasarım
1. **Güvenlik ve sağlık:** onaylı 26 kuralın fail-closed uygulanması, salt okunur korunan dosya hash/manifest, en az yetki, devre kesici, log ve kanıt.
2. **Kanal keşfi ve aday havuzu:** yasal/izinli kaynaklardan aday bulma, kaynak kimliği, tekrar önleme, karantina, geçmiş.
3. **Teknik doğrulama ve kararlılık:** URL/HTTP/HLS, codec, medya, zaman aşımı, tekrar testi, uzun dönem kanıt; başarı otomatik yayın değildir.
4. **Kimlik, EPG, logo ve IBO hazırlığı:** tvg-id, kanal eşleştirme, XMLTV ve logo doğrulama; cihaz testini kullanıcı yapar; EPG üretim değişikliği ertelenir.
5. **Yeni M3U üretimi, izole raporlama ve geri dönüş:** yalnız yeni çıkış yolu; onaylı adaylar, kalite raporu, salt okunur kaynak arşiv, doğrulanabilir rollback.

Bu beşli ayrım yeni tasarım önerisidir; eski notlarda K4/K5 rol isimleri çakıştığından önceki kodu taşımadan bu belgede sabitlenmiştir.

## Başlangıç ve kabul sırası
1. DEVAM_NOTU.md, 810 dosya notu.md ve dokuz ek not; AGENTS.md, GUVENLIK_KURALLARI.md, YENIDEN_KURULUM_KORUMA_PLANI.md, BES_SISTEM_TOPLU_IS_DEFTERI.md referans alınır. Çelişkide **son açık kullanıcı kararı** geçerlidir.
2. Mevcut korunan dosyaların salt okunur SHA manifesti ve yeni sisteme ait izinli yazma yolları hazırlanır; gerçek yedek mevcut olduğu kanıtlanmadan silme yapılmaz.
3. Beş yeni modül sıfırdan yazılır; önce testler ve izole örnek veri, sonra güvenlik kanıtı. Eski betik/workflow çağrısı sıfır.
4. Her kategori kendi raporunu üretir; tek merkezli toplu kabul koşusu, korunan dosyaların değişmediğini kanıtlar.
5. Yeni M3U ayrı adla hazırlanır. Üretim ve IBO bağlantısı yalnız kullanıcı onayıyla; gerçek cihaz testini kullanıcı yapar.

## Kanıt durumu
Bu belge yalnız **yeni çalışma sözleşmesidir**. Yeni beşli kod, 26/26 çalışma zamanı güvenlik kanıtı, M3U ve cihaz testi henüz yapılmış sayılmaz. Üretim dosyalarına dokunulmadı.
