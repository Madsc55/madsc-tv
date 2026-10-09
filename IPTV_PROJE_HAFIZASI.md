# IPTV PROJE HAFIZASI — Madsc55/madsc-tv

Son gözden geçirme: 2026-10-09. Bu dosya yeni sohbetlerde projenin devamlılığı için tutulur. **Gerçek durum için her zaman önce GitHub'daki güncel dosyaları yeniden oku.** Bu dosyadaki sayılar zamanla değişebilir.

## Proje
- GitHub deposu: `Madsc55/madsc-tv`
- Ana IBO Player çalma listesi: `CALISANLAR.m3u`
- Kullanıcı asistanına “Mahmut” diye hitap eder.
- Sohbet değişince bu dosyayı ve güncel ana listeyi oku; önceki kararları kaybetme.

## Kesin değişiklik kuralları
1. **Kullanıcı açıkça istemedikçe `CALISANLAR.m3u` dosyasını değiştirme.** “Kanal ara”, “tara”, “test et”, “genel güncelleme” araştırma/test/raporlama isteğidir; otomatik olarak listeye ekleme veya silme izni değildir. “Ekle”, “sil”, “taşı”, “sırala”, “değiştir” gibi açık talimatlar yalnızca belirtilen işlemi yetkilendirir.
2. Yeni adayları kullanıcı onayı olmadan **⭐ YENİLER** veya diğer kategorilere ekleme. Yedeklere aktarım da açıkça kararlaştırılan kurallara bağlıdır.
3. Mevcut kanalın yayın bağlantısını değiştirme veya aynı kanala yeni URL ekleme; kullanıcı açıkça isterse istisna.
4. Her değişiklikten önce güncel dosyayı ve blob SHA'yı GitHub'dan çek; ilgisiz satırları, TVG kimliklerini, logoları, URL'leri, kategorileri ve sıralamayı koru.
5. Gerçek kanal logosu kullan; yapay/uydurma logo kullanma. Bulunamayan logoyu bulunmuş gibi gösterme.
6. Bulunmuş bir M3U8 adresi **çalışan kanal kanıtı değildir**. HTTP erişimi, gerçek HLS segmentleri, 20–40 saniyelik görüntü/ses, doğru kanal kimliği ve coğrafi engel durumunu ayrı değerlendir. Ortam test yapamıyorsa “doğrulanamadı” de; “çalışıyor” deme.
7. Değişiklik sonrası hangi dosyanın değiştiğini, kaç kayıt etkilendiğini, toplam kayıt sayısını ve commit SHA'yı bildir.

## 2026-10-09 itibarıyla doğrulanmış liste durumu
Toplam **587 kanal kaydı**; farklı kategorilerde veya URL'lerde aynı istasyon tekrarlanabilir. Son kontrol edilen kategori sayıları:
- ⭐ FAVORİLER: 65
- ⭐ FAVORİLER 1: 1
- ⭐ FAVORİLER 2: 1
- ⭐ FAVORİLER 3: 1
- 🔄 ALTERNATİF: 89
- 📺 HABER: 74
- 🇹🇷 ULUSAL: 211 (**bayraktan sonra bir boşluk; ULUSAL büyük harf**)
- ⚽️ SPOR: 21
- 🌍 BELGESEL: 8
- 🧸 ÇOCUK: 19
- 🎧 MÜZİK: 27
- 🕌 DİNİ: 13
- 📍 YEREL: 56
- ⭐ YENİLER: 1 (yalnızca DHA CANLI 720P HD)

`HEPSİ` kategorisi kaldırıldı; kayıtları önceden ULUSAL ile birleştirildi. ULUSAL'da aynı kanalın alternatif yayınları yan yana tutuluyor. YENİLER'in adı **⭐ YENİLER**; izinsiz değiştirme.

## Kanal araştırması ve test
Öncelik sırası: eksik önemli **ULUSAL, HABER, SPOR, BELGESEL, ÇOCUK, MÜZİK**; yerel kanallar sonra.
Yalnız “Türkiye IPTV” arama; `tr.m3u`, `turkiye.m3u`, `IPTV-TR`, GitHub depoları, farklı ülke arşivleri ve resmi yayıncı kaynaklarını da tara.
Daha önce incelenen arşivler:
- `iptv-org/iptv` — `streams/tr.m3u`
- `omerdenizhan/IPTV-M3U` — `m3u/turkiye.m3u` ve `m3u/turkiye-iptv-org.m3u`
- `iptv-turk-tr/iptv` — `list.m3u`
- `discevisita/iptv` — `tr.m3u`
- `sayatsirinoglu/IPTV-List` — `tr.m3u`
- `ilyswch/IPTV-TR` — `box.m3u`

Araştırılmış ama **gerçek 20–40 saniyelik video/ses testiyle doğrulanmamış** adaylar: **Akit TV, GZT TV, TRT 3, Haber61 TV, Kanal D Drama, Sözcü TV, TV5, Show Max, Life TV**. İsimler ve kaynaklar güncel listede tekrar kontrol edilmeli. Önceki ağ erişim sorunları nedeniyle “bozuk” ya da “çalışıyor” sonucu çıkarılamadı. **Doğrulanmış yeni kanal: 0** (bu notun yazıldığı anda).

**Zaten listede bulunan** ve yanlışlıkla yeni sayılmaması gereken örnekler: TELE1, TRT KÜRDİ, TRT EBA yayınları, TGRT BELGESEL, TGRT HABER. Kanal adlarını normalleştirerek eşleştir; HD/QHD, farklı yazımlar ve boşluklar yanıltabilir.

## Otomasyon
GitHub Actions'ta `YENİLER Güvenli Kanal Arama` isimli iş akışı ve `yeniler-guvenli-arama.yml` dosyası kullanıcı ekranında görüldü. Bir çalıştırma “Success”, 11 saniye ve 1 artifact gösterdi; bu **kanalların 20–40 saniye video/ses testini geçtiği anlamına gelmez**. İş akışının YAML dosyasını ve rapor/artifact çıktısını incelemeden yetenekleri hakkında kesin konuşma. Günlük otomatik çalıştırma mı, yalnızca manuel mi olacağı henüz kullanıcı tarafından seçilmedi.

## Yeni sohbet başlangıç protokolü
1. Bu hafıza dosyasını oku.
2. `CALISANLAR.m3u` dosyasının güncel hâlini ve kategori/kayıt sayılarını kontrol et.
3. Kullanıcı otomasyon sorarsa ilgili `.github/workflows/*.yml` ve son çalıştırma raporlarını incele.
4. Son isteği ve yetki sınırını teyit ederek **yalnızca istenen işlemi** yap.
5. Yeni önemli kararları veya onaylı değişiklikleri bu hafıza dosyasına işle; fakat kanal listesine izinsiz dokunma.

Yeni sohbette söylenecek cümle: **“Mahmut, Madsc55/madsc-tv deposundaki IPTV_PROJE_HAFIZASI.md dosyasını oku ve kaldığımız yerden devam et.”**
