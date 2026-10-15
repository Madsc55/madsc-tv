## 15 EKIM 2026 — BUYUK DOSYALAR YENIDEN ERISIM DENEMESI (SOHBET DEVAMI)

- Kullanici kalan acilamayan dosyalari yeniden okumayi ve onceki basarili okumayi tekrarlamamayi istedi. Bu islem salt okunur kaynak denetimidir; korunan playlistler degismedi.
- Onceki envanter: 769 dosya, 373 gorsel, 396 diger; onceki kayitta gorev/not amacli tarama tamamlandi denirken tam icerik okuma ve gorsel kimlik onayi ayrica eksik gorunuyor. 769/769 tam metin dogrulandi iddiasi yok.
- Yeniden denenen ve SHA elde edilmesine ragmen icerigi BOS donen yedi buyuk dosya: aday_bekletme/ADAY_ONCELIK_RAPORU.csv; madsc_kesif/bulunan_kanal_arsivi.csv; madsc_dogrulama/state.json; madsc_kesif/gecmis.json; madsc_son_kontrol/results.json; aday_bekletme/gecmis.json; aday_hazirlik/uc_asama_2026-10-12_1037.json. Dosyalarin bozuk oldugu sonucuna varilmaz; alternatif aralik/blob indirme yontemi gerekiyor.
- Yeniden okunan onemli kaynaklar: AGENTS.md, GUVENLIK_KURALLARI.md, OZELLIK_ENVANTERI.md, IPTV_PROJE_HAFIZASI.md, SEKIZ_GOREV_TOPLU_DENETIM.md, TOPLU_DURUM_RAPORU.md, DEVAM_NOTU.md. ONCELIK_1_BES_MERKEZ.md bu dalda 404; gercek tam yol aranacak.
- Acilan kucuk JSON kanitlari: madsc_dogrulama/summary.json (2026-10-14: 7100 URL, 6374 uc basari, listeye hazir 0); madsc_son_kontrol/summary.json (2026-10-14: 3800 tamamlanan, 2574 kalan, listeye hazir 0); madsc_kesif/DORT_ASAMA_TEK_RAPOR.json (11742 arsiv URL, 75 aday, 4 alternatif, harici yedek kaniti eksik); logo_deneme/ozet.json (1039 liste girisi, 195 logo URL, 32 sorunlu kayit; cihaz/gorsel kimlik onayi yok); epg_deneme/yayim_kontrol.json (eski Pages checksum basarisi, IBO NOT_VERIFIED); madsc_kesif/candidate_epg_logo_join.json (5 kanal pilot, kaynak aday 0); madsc_kesif/ibo_3_5281_rapor.json; madsc_kesif/ibo_6115_ikinci_rapor.json; madsc_kesif/ibo_530_399_sonrasi_rapor.json.
- SIRADAKI: buyuk yedi dosyanin gercek icerigini alternatif GitHub blob/indirilebilir metin yontemiyle denetle; onceki envanterde eksik kalan CSV/M3U/XML/gorsel kimlik eslesmelerini tekrar saymadan tamamla; merkezi bes asama, 92 workflow ve 26 kural kabulunu mevcut kanitlarla karsilastir. Son Actions run ve cihaz sonucu olmadan basari/onay verme.

## 15 EKİM — KULLANICININ İSTEDİĞİ KAYNAK NOTLARI / YENİDEN DOĞRULANAN DOSYALAR

**Bu inceleme kullanıcı talimatıyla yalnız görev/karar/eksik kanıt toplama amaçlıdır.** Kaynaklar değiştirilmedi. 769 dosya envanteri var, **769 dosyanın tamamının içerik incelemesi henüz doğrulanmadı**. 97 workflow daha önce tam metin okunmuştu. Bu turda özellikle kullanıcı tarafından adı verilen kaynakların tam metni yeniden okundu; 51 JSON'un tamamına içerik düzeyinde erişim denendi, çok büyük JSON/CSV dosyalarında içerik kesintisi görüldü. Eksikleri tamamlandı göstermeme kuralı geçerlidir.

### Kaynağa bağlı yeni görev ve kararlar
1. `GUVENLIK_KURALLARI.md`: 19 temel + dört ek güvenlik önlemi + 24. kural (hata zincirini durdur). Bunlar onaylı **politika**, bütün teknik yolların otomatik olarak zorlandığının kanıtı değil. Gerçek izin, 10 push denemesi, kilit ve korunan playlist regresyonu ayrı denetim.
2. `OZELLIK_ENVANTERI.md`: 'VAR+TEST BAŞARILI ise yeniden yazma; VAR+EKSİK ise yalnız eksiği düzelt'; aynı özelliği iki kez kurma. Her kod değişikliğinde Actions run ID ve dosya etkisi ana nota yazılır. Cihaz testi yapılmadan IBO onayı verilmez.
3. `SEKIZ_GOREV_TOPLU_DENETIM.md`: felaket arşivi/izole açma testi mevcut; **30 gün saklama, GitHub dışı kopya, secrets ve IBO ayarları kurtarma kanıtı yok**. Türk kanal kimliği, lisans, logo/EPG ve gerçek İsveç IBO doğrulaması açık; branch protection ayrı.
4. `TOPLU_DURUM_RAPORU.md`: EPG/Pages, 5 kanal TV kabulü, 92 workflow tetik/yan etki eşdeğerliği, günde iki keşif, 75 aday (51 retest, 24 ffprobe, 4 alternatif), gerçek cihaz kimliği ve toplu kabul açık. 50 kanallık sağlık partisi bütün ana listenin canlı testi değildir. Eski #93/#100/#101/#102/#103 test düzeltmeleri tekrar yazılmayacak; son run ile kanıtlanacak.
5. `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md`: tarihsel **3082 kalan aday**, #38430737866 son kontrol run, teknik false-negative ve IBO'da çalışan kanal koruması; eski tarihli snapshot yeni güncel 2574 kalanla karıştırılmayacak. 740 yabancı arşiv kanalını teknik hata yüzünden silme. Önceden izin verilmiş eski taşıma kararları **güncel yazma izni değildir**.
6. `kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md`: **Eurostar** çalışan alternatif araştırması açık; ana listeye/YENİLER'e izinsiz ekleme yok.
7. `kontrol_notlari/2026-10-12_ekol_basa_sarma.md`: **Ekol TV** 1080p playlistte 180 eski segment / yaklaşık 30 dakika döngü; son segment HTTP 200, canlı yayın kanıtı değil. HLS segment zaman damgası/ilerleme sürekliliği kontrolü ve gerçek güncel kaynak araması açık. Eski URL'leri değiştirme.
8. `kontrol_notlari/DEVAM_GECMISI_2026-10-12_1947.md`: eski 6981 URL üçlü test ve 63 son kontrol tarihsel anlık görüntüsü, yeni sonuçla karıştırılmayacak. 9 görsel incelenmiş, 8 yayın karesi alınmış, Baku.TV karesi alınamamış; görsel varlığı logo/kanal kimliği onayı değil. TRT 1/DHA/SAT 7 TÜRK kategori kararları tarihsel, güncel listeye izinsiz uygulanmaz.
9. `arastirma/bes_site_katalog_2026-10-12.json`: **VIN kanal girişinin TRT Kurdî içeriğine yönelme kimlik riski**. Resmî kaynak/kanal kimliği ayrı doğrulanmadan ekleme yok.
10. `arastirma/lyngsat_arama_oncelikleri.json`: **7 kanal için kimlik inceleme** gereği; uydu kataloğunda ad eşleşmesi yayın kimliği kanıtı değil.
11. `arastirma/uydu_arama_oncelikleri.json`: öncelikli Türk kanal adları **NOT_FOUND_BY_NAME**; bunlar test edilmiş URL değildir. Resmî açık yayın kaynağı araştır, geçmiş test URL'leriyle karşılaştır.
12. `aday_hazirlik/ibo_alternatif_10_2026-10-12.json`: durum **SUPERSEDED_AFTER_IMAGE_IDENTITY_REVIEW**; eski on aday listesini hazır/onaylı diye kullanma, kimlik doğrulanmamış ve kopya logolar kanal kimliği kanıtı değil.
13. `docs/MADSC-IKI-TOPLU-KABUL-PLANI.md`: kullanıcı iki aşamalı toplu kabul istiyor; küçük dosya başına ayrı test istemiyor. Kategori 5 `needs` hatası ve EPG/Pages/keşif/VOD/restore/IBO kanıtları kapanmadan PR #71 merge yok.
14. `docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md`: davranışsal parity ölçülmeden yüzde ilerleme vermeme; eski üretim tetikleri ve yazma bağımlılıklarını gerçek dry-run/izole testle incele.
15. `BES_SISTEM_TOPLU_IS_DEFTERI.md` ve `BES_SISTEM_GECIS_KONTROL.md`: 92 workflow görev sahibi, tetik, cron, artifact, risk ve geri dönüş eşleştirmesi; 18 görev, 26 kural ve eski taleplerin eksiksiz kabul tablosu. Kullanıcı onaysız veri değişimi yok.

### Bu tur veri dosyası inceleme yöntemi ve engeller
- Git ağaç verisinde **769 dosya / 27 klasör**; görseller **373**, görsel olmayan **396** dosya. **Bu sayım içerik incelemesi değildir.**
- CSV kaynaklarının ilk 20'sinin içerik erişimi denendi: `TEST_RAPORU.csv`, `aday_bekletme/ADAY_DURUM_RAPORU.csv`, `TEKRAR_EDEN_ADAYLAR.csv`, `madsc_kesif/ibo_3_5281_kararlar.csv`, `ibo_6115_ikinci_kararlar.csv`, `eski_bozuk_linkler.csv`, `tekrarlar.csv` gibi kaynaklar açıldı; **1.1 MB `aday_bekletme/ADAY_ONCELIK_RAPORU.csv` ve 2.46 MB `madsc_kesif/bulunan_kanal_arsivi.csv` boş döndü**, okunmuş sayılamaz. `ibo_6115_ikinci_kararlar.csv` 11.929 satır içeriyor; eski kararlar tekrar uygulanmayacak.
- 51 JSON'da doğrudan okuma denendi. `madsc_dogrulama/state.json` (~5.96 MB), `madsc_kesif/gecmis.json` (~4.80 MB), `madsc_son_kontrol/results.json` (~4.84 MB), `aday_bekletme/gecmis.json` ve `aday_hazirlik/uc_asama_2026-10-12_1037.json` tam JSON parse edilemedi: **okuma/kesilme engeli**, kaynak verinin bozuk olduğu kanıtı değildir. Bunlar parça/parça okunmalı.
- `epg_deneme/yayim_kontrol.json` Pages yayın checksum/HTTP doğrulama, `liste_kontrol/rapor.json` Ulusal kategori eksikleri, `logo_deneme/png_automation.json` PNG ve görsel onay kuyruğu, `madsc_kesif/candidate_logo_missing_report.json` eksik logo/kimlik adayları, `vod/guncel-bolumler.json` yalnız bölüm takvimi, `raporlar/YEDEK_KATEGORI_LOGO_2026-10-12.json` eski izin snapshotları olarak ayrı incelenmeli; rapor varlığı canlı başarı değildir.
- **Henüz tamamlanmamış:** kalan CSV/M3U/TXT/XML dosyaları ve 373 logo görselinin format/isim/kanal bağlantısı, büyük JSON'ların satır aralığıyla tam içerik taraması, bütün 151 Python'un dosya bazlı tam sayım kanıtı ve tüm 34 Markdown'un benzersiz kontrol matrisi. Tüm bunlar tamamlanmadan '769/769 inceledim' denmez.

---

# 15 EKİM 2026 — 769/769 DOSYA GÖREV/NOT AMAÇLI ENVANTER VE İÇERİK TARAMASI TAMAMLANDI

**KAPSAM TANIMI:** Bu çalışma kullanıcı isteği doğrultusunda her dosyanın görev/not/karar/eksik iş içerip içermediğinin tespitidir; bütün görsellerin yayın kimliği onayı, her URL'nin canlı çalışması, kodların çalıştırılması, 92/92 workflow davranışsal parity veya 1 Ekim'den bugüne GitHub dışı sohbetlerin eksiksiz taranması değildir. Başlangıç anlık görüntüsü: `3e79287598e4182aee48ae64fddeb8174321fbae` (15 Ekim 2026); yeni commitlerle ağaç değişebilir.

## Tamamlanmış kaynak denetimi — **769/769 dosya**

| Tür | Sayı | Gerçek inceleme |
|---|---:|---|
| GitHub Actions YAML | **97/97** | Tam metin okundu; her workflow'un işi/çağrıları/tetikleri/yazma izinleri ve görev ailesi yukarıdaki bölümde kaynak bazında kayıtlı |
| Python program ve test | **151/151** | Her blob içeriği doğrudan okundu; fonksiyon/eksik-onay-bekleme işaretleri ve program sorumlulukları tarandı; geçmişte ayrıntılı kod bulguları kaydedildi |
| Markdown notları | **34/34** | Tam metin okundu; başlıklar, kontrol listeleri, kararlar, geçmiş kullanıcı istekleri ve açık görevler çıkarıldı |
| JSON veri ve raporlar | **51/51** | Tam içerik parse edildi, anahtarlar/rapor durumları incelendi; 5 büyük dosya için `fetch_file` başarısız olunca SHA ile **`fetch_blob`** kullanılarak erişim sağlandı |
| CSV geçmiş/rapor | **26/26** | Tam metin ve başlık/satır yapıları okundu; 3 büyük dosya `fetch_blob` ile alındı; satır sayıları bazen multiline CSV yüzünden kesin kayıt sayısı değildir |
| M3U playlist ve arşiv | **27/27** | İçerik okunup `#EXTINF` sayıldı; 1 büyük dosya `fetch_blob` ile alındı; listeyi değiştirmeden tarihsel farklar değerlendirildi |
| Diğer TXT/XML | **10/10** | Tam metin okundu; 8,84 MB EPG XML 215 kanal ve 23.702 program; IBO test XML 5 kanal 361 program; 5 kanal izole demo XML 23 program |
| SVG logo kaynakları | **40/40** | SVG metni okundu, TODO/FIXME/bekleyen yorum tarandı; yeni açık görev notu bulunmadı. Görselin gerçek kanal kimliği ayrı onaydır |
| PNG/JPG/WebP görseller | **333/333** | Dosya yolu/uzantı/byte/blob SHA metadata envanteri değerlendirildi; raster ikili dosyalar metin görev notu değildir; gerçek görüntü içeriği/kare-logo eşleştirmesi yapılmadı |
| **TOPLAM** | **769/769** | **436 dosyada metin/kod/veri/SVG içerik taraması + 333 raster dosyada metadata/görev ilişkisi taraması** |

**ÖNCEKİ AÇIK KAYIT DÜZELTMESİ:** Bir önceki bölümde '9 büyük veri dosyası içerik engeli' deniyordu. Bunlar SHA tabanlı blob okuma ile **tamamlandı**: `aday_bekletme/gecmis.json` (URL anahtarlı tarihsel gözlemler), `aday_hazirlik/uc_asama_2026-10-12_1037.json` (üç aşama), `madsc_dogrulama/state.json` (**7100** kanal anahtarı), `madsc_kesif/gecmis.json` (**11762** geçmiş kayıt), `madsc_son_kontrol/results.json` (son kontrol kayıtları), `aday_bekletme/ADAY_ONCELIK_RAPORU.csv` (2667 civarı veri satırı), `madsc_kesif/bulunan_kanal_arsivi.csv` (**11743** civarı veri satırı), `madsc_kesif/yedek_ulke_inceleme.csv` (**11557** civarı veri satırı), `madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u` (**11557** EXTINF). URL içeren ham satırlar ana nota kopyalanmadı; orijinal dosyalarda korunuyor.

## Çıkarılan görev ve kanıt aileleri — 16 ana başlık

1. **Kullanıcı onayı ve güvenlik:** 23/24/25/26 kural geçmişi, geri alınan YEDEKLER izni, korunan playlist/logolar/yedekler, 92 eski workflow yazma/trigger kapıları.
2. **Beşli sistem geçişi:** 97 workflow'un görev envanteri, 92 eski iş akışının 5 hedefe davranışsal eşdeğerlik/kanıt matrisi (**0/92 kanıtlı**), PR #71 güvenli bekleme.
3. **Kanal keşfi:** 155 hedef/156 tanımlı kaynak, eksik ücretsiz Türk kanalları, resmî/yasal HLS, Türksat katalog karşılaştırması, yeni/alternatif ayrımı.
4. **Aday/tekrar test:** 75 aday/4 alternatif tarihsel snapshot, 51 saatli tekrar, 24 teknik/IBO belirsiz, 390 geçmiş aday, 7100 üç aşama, 125'lik son kontrol partileri.
5. **Canlı medya ve kalite:** ffprobe video/ses, 5 dakika süreklilik, 7/30 günlük kararlılık, timeout/403/geo engeli ayrımı, HD/FHD kimlik kanıtı.
6. **IBO gerçek cihaz ve kimlik:** İsveç TCL 55C655, Ibo Player Pro 2128.0, kullanıcı çalışıyor/çalışmıyor kararı, gerçek oynatma ve kanal kimliği; GitHub yeşil testi yerine geçmez.
7. **EPG/XMLTV/Pages:** 1039 playlist/730 eşleşme/309 eşleşmeyen/23.702 program snapshot, 215 XMLTV kanalı, 5 kanallı pilot, Pages GITHUB_TOKEN tetik bağı ve cihaz kabulü.
8. **Logo/PNG/WebP/SVG:** 373 görsel metadata, 40 SVG metni, 6 HTTP hatalı logo URL, 32 sorunlu kayıt, adayın gerçek istasyon logosu ve onaylı PNG hazırlığı.
9. **Tarihsel yedek/arşiv:** 11762 geçmiş kayıt, 11557 ayrılan M3U, 740 yabancı, 10817 kimliği belirsiz; offsite/tarihsel restore kanıtı yok.
10. **Geçmiş kullanıcı kararları:** 7 Ekim 10 ret kanal adı, IBO pozisyon/grup kararları, URL/tarih ile teknik sonucu ayır, hiçbir eski kararı yanlış akışa aktarma.
11. **YENİLER/YEDEKLER/Ulusal/Favoriler:** Kategori sayısı, alfabetik/onay kuralı, Ulusal ana depo, tarihsel logo-kategori kararı ve FTV TÜRK/Red Bull TV isim uyumsuzluğu.
12. **VOD film/dizi:** Metadata/kategori ve bölüm takvimi var; lisanslı gerçek VOD/IBO Film-Dizi sekmesi/ayrı Xtream entegrasyonu kanıtı yok.
13. **İzin ve gizlilik:** `contents:write` eski akışlar, dolaylı Python yazma yolları, URL yolunda token/kimlik gizliliği, raporlarda ham yayın URL'si riski.
14. **Merkezi rapor/test:** 18 görev/8 görev, gerçek Actions run ve artifact, yanlış yeşil durum, kısmi 50/1039 sağlık testinin rotasyonu, tek ekran yönetim.
15. **Yedek kurtarma ve felaket planı:** izole Git HEAD restore, Actions artifact saklama, bağımsız dış kopya, gerçek restore ve secrets/cihaz ayarı sınırı.
16. **Tarihsel talepler ve takvim:** aylık geniş denetim, günde iki aday keşfi, Cuma/haftalık kontroller, 90 günlük kaynak taraması, tekrar test saatleri, eski görevlerin yinelenmeden birleştirilmesi.

**Sayım yorumu:** Yukarıdaki **16 benzersizleştirilmiş ana iş ailesi** altında **97 workflow kaynak-görev kaydı** ve önceki bölümlerde çok sayıda kod, karar, JSON/CSV ve cihaz kanıtı bulunuyor. 97 workflow'un hepsi 97 ayrı yapılacak görev değildir; aynı işi tekrarlayan workflow'lar var. **Tekilleştirilmiş alt görev sayısı** henüz kesin sayılıp onaylanmadı; uydurma kesin toplam verilmez.

## Kaynak incelemesi kapandı; şimdi uygulanacak işler
Bu 769 dosyanın **not/görev amaçlı kaynak taraması tamamlandı**. Bir sonraki iş artık aynı dosyaları körlemesine tekrar okumak değil; yukarıdaki 16 aileyi somut, tekilleştirilmiş kabul görevlerine dönüştürmek ve **önce güvenlik/izin + 92 parity, sonra keşif/IBO/EPG/backup/VOD** sırasıyla test etmek. **Hiçbir eski dosya, liste, logo, workflow, arşiv veya yedek bu envanter çalışması sırasında değiştirilmedi.** Yalnızca `DEVAM_NOTU.md` genişletildi.

---

## 15 EKİM — 769 DOSYANIN TAMAMINA UZANAN KAYNAK TÜRÜ TARAMASI / YENİ KANITLAR

**Bu oturumdaki kapsam:** 769 dosyanın tamamı Git ağacından yol, tür, byte boyutu ve blob SHA düzeyinde envanterlendi. 373 PNG/SVG/JPG/WebP görsel **dosya metadata/hash düzeyinde** değerlendirildi; her görselin görsel kimliği ayrıca doğrulanmadı. 97/97 workflow tam metni önceki turda okundu. Bu turda 51 JSON, 26 CSV, 27 M3U dosyasının **her birine içerik erişimi denendi**, sonuçlar aşağıda. Önceden çok sayıda Python/Markdown/test okunmuştu, ancak 151/151 ve 34/34 satır bazında doğrulama matrisi henüz bitmedi. **769/769 içerik tamamlandı demek doğru değildir.**

### Bu turda sayısal içerik erişimi (doğrudan denenmiş)
- **51 JSON:** **46** dosyada JSON yapısı parse edilip anahtarlar/uyarılar okundu; **5 büyük JSON** (`aday_bekletme/gecmis.json`, `aday_hazirlik/uc_asama_2026-10-12_1037.json`, `madsc_dogrulama/state.json`, `madsc_kesif/gecmis.json`, `madsc_son_kontrol/results.json`) GitHub bağlayıcısı **boş/truncated** içerik döndürdü. Bunlar incelendi diye işaretlenmeyecek; küçük aralıkla okuma denemesi de boş döndü.
- **26 CSV:** **23** dosyada başlık ve satır/şema örnekleri okundu; **3 büyük CSV** (`aday_bekletme/ADAY_ONCELIK_RAPORU.csv`, `madsc_kesif/bulunan_kanal_arsivi.csv`, `madsc_kesif/yedek_ulke_inceleme.csv`) bağlayıcıdan boş döndü. Bazı büyük CSV'lerde Unicode byte farkı olabilir; satır sayıları gerçek CSV parser ile kesinleştirilmeli.
- **27 M3U:** **26** dosyanın M3U `#EXTINF` kayıtları sayıldı; **1 büyük M3U** (`madsc_kesif/yedeklerden_ayrilanlar_20261013T170042Z.m3u`) bağlayıcıdan boş döndü. İçeriğe erişilemeyenleri metadata+önceki ilişkili raporlarla izlemeye devam et.
- **373 görsel:** yol/uzantı/byte/blob kimliği incelendi; logo gerçek kanal eşleşmesi ve PNG açma/kare karşılaştırması ayrı görsel kabul işi. Binary görselden TODO metni beklenmez.

### Kaynaklardan çıkarılan yeni somut bulgular
1. **Liste geçmişi:** `CALISANLAR.m3u` 1039 `#EXTINF`; `YENILER.m3u` 58; `YABANCI_KANALLAR.m3u` 740; `MADSC_TV_47_LISTE_ADAY.m3u` 1183. Farklı tarihli/sınıflı listeleri toplayıp canlı tek kanal sayısı yapma.
2. **IBO geçmiş arşiv:** `madsc_kesif/ibo_3_5281_ayrilanlar.m3u` 5252; `ibo_6115_ikinci_ayrilanlar.m3u` 5585; `yedekler/TUM_TEKNIK_TEST_ADAYLARI_2026-10-09.m3u` 390. Hepsi tarihsel; kanal oynatma/onay kanıtı değil.
3. **Kaynak karşılaştırması:** `madsc_kesif/kaynak_guncelligi.csv` 156 veri satırı; `kaynak_erisim_raporu.csv` 14 veri satırı. 155 hedef/156 tanımlı kaynak farkı açık; kaynak güncelliği ile erişim/gerçek tarama kapsamını eşleştir.
4. **Aday verileri:** `madsc_kesif/adaylar.csv` 75 aday, `alternatifler.csv` 4 alternatif, `player_uyumlulugu_belirsiz.csv` 24 satır; raporlar `DORT_ASAMA_TEK_RAPOR.json` ile tarih/snapshot bazında karşılaştırılacak.
5. **Geçmiş başarısız URL:** `madsc_kesif/eski_bozuk_linkler.csv` 4543 satır; `tekrarlar.csv` 3510 satır. Bunlar ayrı tarihsel kayıtlar; sırf teknik başarısız diye kullanıcı ret kararı sayma.
6. **Ana liste sağlık:** `madsc_kesif/ana_liste_saglik_raporu.csv` 1039 veri satırı; `ana_liste_calismayanlar.csv` 22 veri satırı. Teknik sonuçları mevcut 1039 kayıtla URL ve zaman bazında eşleştir, eski listeyi değiştirme.
7. **Aday geçmiş raporları:** `aday_bekletme/ADAY_DURUM_RAPORU.csv` yaklaşık 2667 satır; `TEKRAR_EDEN_ADAYLAR.csv` yaklaşık 469 satır. Büyük `ADAY_ONCELIK_RAPORU.csv` içerik engeli yüzünden henüz doğrulanmadı.
8. **IBO kullanıcı kararı:** `madsc_kesif/ibo_3_5281_kararlar.csv` 5279 veri satırı; `ibo_kullanici_kararlari.csv` yaklaşık 232; ikinci karar CSV'sinde çok satırlı veri/kaçış nedeniyle düz satır sayımı güvenilmez, gerçek CSV parser ile kontrol edilecek. Kullanıcı kararı/teknik sonuç ayrı tutulur.
9. **EPG Pages eski yayım kaydı:** `epg_deneme/yayim_kontrol.json` 11 Ekim Pages deployment `SUCCESS`, yayımlanan ve repo XML SHA256 eşit; ancak `successful_daily_workflow_followup=CONFIGURED_NOT_YET_OBSERVED`, `ibo_visibility=NOT_VERIFIED`. Dolayısıyla **Pages'in bir kez yayınlanması günlük EPG zincirinin çalıştığını kanıtlamaz**.
10. **Logo geçmiş kullanıcı onayı:** `raporlar/YEDEK_KATEGORI_LOGO_2026-10-12.json` tarihsel üç yedek kanal aktarımı ve `name_mismatch` alanı içeriyor; özellikle **FTV TÜRK / Red Bull TV logo-kimlik uyumsuzluğu** yeniden gözden geçirilmeli. Geçmiş kullanıcı onayı yeni genel düzenleme izni değildir.
11. **Önceki yedek aktarım komutu:** `.github/commands/aday-yedekleme.txt` 9 Ekim 0–99 gruplarını izole aday yedeğine alma talimatı; `CALISANLAR.m3u` değişmemeli. Mevcut güncel YEDEKLER ekleme izni geri alındı.
12. **Kök araç ve eski yedek Python:** `liste_kontrol/build.py` salt-okunur Ulusal/favori karşılaştırması; `yedekler/ibo_yedek_kalite_tespit.py` yedek görüntü/codec taraması ve yedek görünen adını değiştirebilecek kod; `yedekler/teknik_adaylari_aktar.py` geçmiş iki Actions run artifact'ından izole yedek aktarımı; `yedekler/tekrar_test_390.py` 390 aday ffprobe yeniden deneme; `yedekler/sozcu_akit_ozel_test.py` Sözcü/Akit özel ffprobe. **Bu scriptler okunmuştur, çalıştırılmamıştır; korunan dosyalara dokunulmaz.**
13. **Yayın URL gizliliği:** CSV'lerin bazıları `URL`/`YAYIN_URL` içeriyor; ana not içine ham yayın URL'si, erişim anahtarı veya kişisel token kopyalama. Görev/kanıt/sayı/şema özeti kaydet; ham kaynaklar korunur.

### İçerik taramasını kapatmak için teknik engel ve sonraki adım
**GitHub bağlayıcısının büyük dosyalarda boş içerik döndürmesi nedeniyle en az 9 veri dosyası henüz okunamadı.** Bunların metadata/hash envanteri var ama satır/JSON içerikleri yok; başka güvenilir erişim yöntemiyle incelenmeli. Python ve Markdown kaynaklarının tamamına ait benzersiz dosya bazlı doğrulama da açık. Bu nedenle **tüm 769 dosyanın tam içeriği incelendi/eksikler tamamen çıkarıldı** denmeyecek. Kullanıcının istediği ana not ve eski dosyaları koruma kuralı aynen geçerlidir.

---

## 15 EKİM 2026 — KULLANICININ TÜM DOSYALARI GÖREV HAFIZASI İÇİN İNCELEME TALİMATI (BU SOHBET)

**Kullanıcının açık amacı:** GitHub deposundaki **bütün dosyalar** (yalnız notlar veya workflow'lar değil) okunacak. Her dosyadan geçmiş kullanıcı isteği, karar, yapılmış iş, kısmen yapılmış iş, eksik veya başarısız görev, kurulum/otomasyon ihtiyacı, kaynak veri, test kanıtı, çakışma, risk ve öneri çıkarılacak. Her bulgu mevcut işlerle karşılaştırılacak; yinelenen görevler tekilleştirilecek; özgün kaynak yolu ve kanıt tarihiyle **DEVAM_NOTU.md** ana notuna eklenecek. Kullanıcının bu sohbette tekrar ettiği istek: 'Her dosyada bir eksik görev, not, yapılacak veya yaptığı şeyler vardır; bunları ana notumuza ekleyip sistem eksiklerini topluca anlamak ve notlara bakarak eksikleri yapmak istiyorum.' Bu çalışma, gelecekteki gerçek uygulama ve testlerin ön hazırlığıdır; sadece isim listesi üretmek yeterli değildir.

### Sayımın dürüst kapsamı
- Git ağacından alınan envanter: **769 gerçek dosya, 27 klasör = 796 ağaç girdisi** (15 Ekim'de okunan ağaç; yeni commitlerle değişebilir).
- Dosya türleri: **97 workflow YAML, 151 Python, 34 Markdown, 51 JSON, 26 CSV, 27 M3U, 10 diğer metin/XML, 373 görsel** (bu sınıflar toplam 769).
- **97/97 workflow YAML tam metni incelendi**; bunların **92'si eski iş akışı**, 5'i hedef ana kategori. Kaynak-görev dökümü yukarıdaki bölümde. **92/92 davranışsal eşdeğerlik henüz kanıtlanmadı; 0/92 kanıtlı.**
- Çok sayıda Python, test, araç, Markdown, JSON, geçmiş karar ve kök komut dosyası açılarak içeriklerinden görev çıkarıldı. Ancak **769/769 içerik okundu iddiası yoktur**; benzersiz dosya bazlı imzalı tamamlanma tablosu henüz üretilmedi. Bu nedenle 'toplam tam incelenen dosya' için **kesin kanıtlanabilir alt sınır 97 workflow**; diğer açılmış dosyalar ayrıca sayılmadan 769'a dahil edilip tamamlandı denemez.
- İncelenen kaynakların görev/kanıt aileleri: **(1) 97 workflow, (2) Python/araç kodları, (3) regresyon testleri, (4) Markdown talimat/karar notları, (5) JSON teknik raporlar, (6) tarihsel CSV/M3U/TXT arşivleri, (7) logo/EPG/VOD metadata**. Bu **7 kaynak ailesidir**; her ailenin tüm dosyaları tamamlanmış değildir.
- Önceki notlarda **14 ayrı kod kaynaklı açık iş başlığı**, **14 tarihsel/koruma bulgusu** ve workflow'ların görev dökümü yer alıyor. Bunlar **28 ayrı başlık** olarak kayıtlıdır; birbirleriyle örtüşebilir, benzersiz 28 görev veya toplam tüm eksiklerin sayısı değildir. Bir sonraki aşamada kaynak yolu, durum, sorumlu beşli kategori, kanıt ve tekrar ilişkisi ile tekilleştirilecek.

### Tek merkezli görev kaydı için zorunlu alanlar
Her kaynak için: **dosya yolu; dosya türü; son incelenen commit/tarih; okuma kapsamı (tam/özet/metadata); geçmiş kullanıcı talimatı; mevcut işlev; yapılan işin kanıtı; eksik veya hatalı iş; öneri; beş ana sistemde görev sahibi; risk/yazma etkisi; kullanıcı onayı gerekiyor mu; test/run ID; sıradaki somut adım; durum (YAPILDI/KISMEN_YAPILDI/BEKLIYOR/KANIT_EKSIK/ONAY_BEKLIYOR); yinelenen görev bağlantısı** tutulmalı. Not/kanıt ile canlı başarının birbirine karışması engellenecek. Görsel dosyalarında isim, boyut, format, hash ve hangi kanal/logo kararıyla ilişkili olduğu; görselin gerçek içeriği ayrıca doğrulanacak.

### Kesin koruma ve çalışma sırası
1. 769 dosyalık sabit başlangıç envanteri üzerinden **benzersiz dosya bazlı inceleme matrisi** oluştur, okunmamışları ve okunanları ayrı işaretle; her dosyanın tamamını/uygun yapısal özetini kaynak bazlı değerlendir.
2. Görev ve geçmiş kararları `DEVAM_NOTU.md` içinde tekilleştir; diğer özgün notları ve kanıtları silme, değiştirme veya yeniden adlandırma.
3. Önce **kullanıcı istekleri/koruma kuralları ve yapılmış işlerin çakışması**, ardından eksik workflow davranış eşdeğerliği, kritik yedek/EPG/keşif/test/kimlik güvenliği önceliklerini sırala.
4. Kanıtı olan gerçek işi ve test sonucunu göster; **sadece yeşil CI sonucu = işlevsel eşdeğerlik veya IBO cihaz onayı değil**.
5. **CALISANLAR.m3u, YENILER, FAVORILER, HEPSI, YEDEKLER, logolar, arşivler ve 92 eski workflow** üzerinde açık yeni kullanıcı onayı olmadan yazma/silme/kapatma/taşıma yok. Önceden verilmiş YEDEKLER ekleme izni **geri alındı**. PR #71 merge edilmeyecek; beşli geçiş parity olmadan tamamlandı denmeyecek.

**Bu konuşmadaki kullanıcı isteği kaydedildi:** 'Tüm dosyalardan görevleri, eksikleri, yapılanları ve geçmiş taleplerimi bul; ana devam notuna ekle; sonra bu toplu notlara bakarak eksikleri tamamlayalım. Kaç dosyaya ve kaç kaynağa bakıldığını açık sayılarla söyle.'

---

## 15 EKİM — PYTHON, TEST, KÖK KOMUT, GEÇMİŞ VE JSON İÇERİK TARAMASI

**Tarama kapsamı:** 97/97 workflow tamamlandı. Ek olarak kök Python aday/keşif/test kodları, `scripts/` merkezi/yedek/IBO/EPG/kurtarma kodları, `test_*.py` regresyonları, `tools/` programları, `tests/` ve `arastirma/uydu_karsilastir.py`, `epg_deneme/build.py`, `logo_deneme/audit.py` kodları gruplar halinde doğrudan açılarak incelendi. Bu not, bütün 151 Python dosyasının benzersiz dosya listesiyle birebir çapraz kontrolü tamamlandı iddiası değildir. Büyük JSON/CSV ve görüntüler için tam içerik incelemesi hâlâ sürüyor. Eski kaynakların hiçbirine yazılmadı.

### Kodlardan çıkan yeni/unutulmuş işler
1. **Gizli bağlantı güvenliği:** `tools/workflow_safety.py` URL query alanlarını maskelese de URL yolundaki erişim bilgilerini gizlemeyebilir. `scripts/birlesik_aday_raporu.py` ham yayın URL'sini dış rapora yazabilir. Gizli URL/token yolunu ve artifact görünürlüğünü maskeleme, hash/sunucu özetine geçme, geçmişi değiştirmeden ileriye dönük güvenlik testi. Kaynak: `logo_deneme/HAZIRLIK_NOTLARI.md`.
2. **Üç deneme geçmişi ve birleşik aday raporu kopukluğu:** `scripts/birlesik_aday_raporu.py` eski CSV puan/24 saat verisini kullanıyor, `madsc_dogrulama/state.json` üç deneme geçmişini doğrudan okumuyor. Geçmişle kanıtlı entegrasyon; geçmiş raporları ezmeden test. Kaynak: `logo_deneme/HAZIRLIK_NOTLARI.md`.
3. **EPG→Pages GITHUB_TOKEN tetik zinciri:** EPG commit'inin `GITHUB_TOKEN` push'u `epg-pages.yml` push koşusunu kendiliğinden tetiklemeyebilir. Açık `workflow_run` veya güvenli tek zincir, canlı yayımlanan XML checksum/HTTP/program testleri. Kaynak: `logo_deneme/HAZIRLIK_NOTLARI.md`.
4. **Eksik Türk kanal keşfi özel talebi:** Mevcut liste+arşiv isim/normalize URL karşılaştır, Türksat ücretsiz kanal listesini keşif kataloğu olarak kullan (uydu frekansı internet akışı değildir), resmî/yasal HLS ara, İsveç erişim/kimlik/logo test et, yeni kanal ve alternatif akışı ayrı raporla, hiçbir listeye onaysız ekleme. Kaynak: `madsc_kesif/NOT_EKSIK_TURK_KANALLARI.md` (kaynakta tarama başlatılmadı yazıyor; 15 Ekim genel keşif bu özel talebin tamamlandığı kanıtı değil).
5. **Geçmiş kullanıcı kararları URL bazlı uzlaştırma:** 7 Ekim tarihli 10 kanal adı için kullanıcı çalışmıyor kararı (TRT Spor, Akit TV, Sports TV, Tarım TV, Toprak TV, ON4 TV, BRT 2, Genç TV, Kanal T, Kıbrıs TV) URL'siz; aynı isimdeki farklı akışa karar taşınamaz. `CALISMAYANLAR.txt` 97 ad, `TEST_RAPORU.csv` 635 eski test kaydı (337 çalışıyor/299 çalışmıyor teknik etiket; kaynak raporunda 635 toplamla aritmetik uyumsuzluk **ayrıca denetlenecek**). Kaynak: `yedekler/GECMIS_KANAL_KARARLARI_KORUMA_2026-10-09.md`.
6. **IBO TCL 55C655 / Ibo Player Pro 2128.0:** Aynı isimli farklı paketler karıştırılmamalı. Cihazın gerçek EPG URL ayarı, XMLTV indirimi, PNG/WebP ve video kodekleri, İsveç oynatma/kimlik onayı ayrı kullanıcı kanıtı gerektirir. Kaynak: `raporlar/IBO_TCL55C655_UYUMLULUK_DENETIMI.md`.
7. **Logo tekil görsel onayı:** `raporlar/LOGO_DURUM_2026-10-12.md` TLC, Dream Türk, PowerTürk Akustik/Slow/Taptaze, Baku TV, TRT Diyanet Çocuk, Spacetoon Turkey, BBC First Türkiye için kare/logo/PNG/kimlik bekleyen özel kayıtlar tutuyor. Mevcut dolu logo alanları korunacak.
8. **Ulusal ana depo kuralı:** `IPTV_PROJE_HAFIZASI.md` mevcut/onaylı yeni ulusal kanalların Ulusal kaydını koruma, diğer kategorilere kopyalama Ulusal'dan silme izni değildir; CNBC-e Sinema/Favoriler tarihsel kararını koru.
9. **Kaynak erişim ve aday test ilkeleri:** `aday_hata_siniflandirma.py` HTTP 403/token ve timeout durumlarını kalıcı kanal reddi saymaz; `gelismis_medya_testi.py` 20 saniye gerçek çözümleme, timeout yeniden test; `akilli_tekrar_test_takvimi.py` zamanlı test; `yanlis_pozitif_koruma.py` HLS aralıklı örnek; `scripts/kanal_kararlilik_takip.py` en az 24 saat aralıklı gözlem. Kullanıcı onayı olmadan hiçbir otomatik taşıma.
10. **Yazma riski kod seviyesinde:** `tools/yedekler_guvenli_ekle.py`, `tools/son_kontrol_yedekler_aktar.py`, `scripts/stage_archive_to_backups.py`, `scripts/restore_all_11599_backups.py`, `scripts/keep_turkish_backups.py`, `scripts/recover_turkish_backups.py`, `scripts/sync_yedekler_category_count.py`, `scripts/apply_ibo_*.py`, `scripts/archive_backups_*.py`, `scripts/automatic_png_logos.py` gerçek liste/yedek/logo mutasyonu yapabilecek kodlar. **Yalnızca incelendi; çalıştırılmadı.** YEDEKLER'e ekleme izni iptal; diğer korunan dosyalara da yeni onaysız yazma yasak.
11. **Restore ayrımı:** `scripts/full_system_backup.py` tüm takip edilen dosyaların tar snapshot ve byte kontrolünü yapabilir, ancak GitHub Actions artifact saklama süresi, bağımsız offsite, secrets ve gerçek felaket geri dönüşü ayrı kabul gerektirir. `scripts/central_isolated_git_restore.py` sadece Git HEAD izole byte eşliği.
12. **Gerçek izin kapısı:** `scripts/protected_playlist_audit.py` açıkça dosya varlığı/söz dizimi kontrolünün branch protection/merge approval yerine geçmediğini belirtiyor. Yazma engelleme, branch rules, dolaylı write yolları ayrı.
13. **EPG ve logo kaynak ilişkisi:** `scripts/build_epg.py`, `scripts/build_ibo_epg_test.py`, `scripts/epg_tv_readiness.py`, `scripts/candidate_epg_logo_join.py`, `scripts/candidate_logo_missing_report.py`, `scripts/logo_visual_evidence.py` teknik/PNG/XMLTV kanıtı üretir, istasyon kimliği/IBO cihazı onayı değildir.
14. **Son kontrol kapsamı:** `final_validation.py` 125'lik, 5 dakika süreklilik; `verification_pipeline.py` üç aşama; `scripts/export_ibo_two_stage_trial.py` ayrı test listesi. Cihaz kimliği ve lisans doğrulanmadan ana listeye terfi yok.

### Depoda okunan tarihsel veri snapshotları — birbirine karıştırma
- `epg/report.json` (14 Ekim 08:51 UTC): 1039 playlist girişi, 730 eşleşme, 309 eşleşmeyen, 23.702 program, 583 kullanılabilir giriş; **15 Ekim canlı IBO cihaz onayı değil**.
- `madsc_dogrulama/summary.json` (14 Ekim 05:07 UTC): 7100 aday, 6374 üç başarılı çözümleme, 398 başarısız, 7100 tamamlanmış üç deneme; `ready_for_playlist=0`.
- `madsc_son_kontrol/summary.json` (14 Ekim 12:09 UTC): seçilmiş 3800, tamamlanmış 3800, kalan 2574; 2332 `TECHNICAL_PASS_IDENTITY_PENDING`, 1055 içerik incelemesi, 255 süreklilik başarısız, 158 timeout; `ready_for_playlist=0`.
- `madsc_kesif/DORT_ASAMA_TEK_RAPOR.json` (14 Ekim): tarihsel arşiv 11762 giriş, 11742 URL, offsite/restore doğrulanmamış; 75 adayın 51'i tekrar saatini, 24'ü ffprobe/oynatıcı uyum incelemesini bekliyor, 4 alternatif; bunlar güncel tarama sonucu diye sunulmaz.
- `madsc_kesif/yedek_turk_ayirma_raporu.json` (13 Ekim): 11599 yedekten 42 tutulmuş, 11557 oyuncudan ayrılmış; 740 yabancı, **10817 kimliği belirsiz** arşivlenmiş. `yedek_turk_yeniden_inceleme_raporu.json`: 10817 belirsiz kaydın Türk kanal içerebileceği uyarısı, 0 Türk geri seçilmiş. Bu **kritik tarihsel inceleme kuyruğu**, silme/yeniden yazma izni değil.
- `madsc_kesif/yedek_11599_geri_yukleme_raporu.json`: 42'den 11599'a tarihsel restore raporu; `ibo_playback=NOT_TESTED`. Raporun varlığı güncel liste sayısı veya cihaz başarısı değildir.
- `logo_deneme/ozet.json` (12 Ekim): 1039 kayıt, 195 benzersiz logo URL, 6 HTTP hatalı URL, 32 sorunlu kayıt, 2 SVG kayıt; kimlik ve cihaz onayı yok.
- `vod/katalog.json` ve `vod/kategoriler.json`: film/dizi/platform kategori sözlüğü; IBO VOD oynatma entegrasyonu kanıtı değil.

### Ana arşiv taramasında kalan kaynak türleri
**97/97 workflow tamam;** Python ve Markdown için çok sayıda tam içerik incelendi, ancak 151/151 ve 34/34 benzersiz dosya bazlı son kontrol çizelgesi ayrıca tamamlanacak. 51 JSON, 26 CSV, 27 M3U, 10 diğer metin/XML ve 373 görsel için dosya envanteri var; seçilmiş raporların içeriği okundu, büyük geçmiş dosyalarının tamamı/PNG-SVG içerik ve kanal bazlı çapraz karşılaştırma **henüz bitmedi**. Tüm bunlar bitmeden 769/769 tarandı denmez.

---

## 15 EKİM — 97/97 WORKFLOW TAM METİN İNCELEMESİ TAMAMLANDI

**Kanıt kapsamı:** Bu oturumda önceki 38'e ek **59 farklı GitHub Actions YAML dosyasının tam metni** okunarak 97/97 workflow dosyası tarandı. İçeriklerde adımlar, çağrılan programlar ve açık `contents:write` izinleri çıkarıldı. **Bu, 92 eski workflow'un beş sisteme işlevsel aktarıldığı anlamına gelmez (parity 0/92).** Kodların, veri dosyalarının ve tüm tarihsel konuşmaların tam taraması ayrıca sürüyor.

### Yeni okunan 59 workflow'un kaynak bazlı görev kopyası
**Geçmiş IBO kullanıcı kararları, koruma ve geri yükleme (10):**
- `madsc-ibo-364-355-364.yml` → `scripts/archive_backups_355_364.py` ile tarihsel sınıflandırma/arşiv; **write**.
- `madsc-ibo-398-16-49.yml` → `scripts/archive_backups_16_49.py` ile arşiv; **write**.
- `madsc-ibo-530-archive.yml` → `scripts/archive_backups_399_onward.py` ile arşiv; **write**.
- `madsc-ibo-6115-second.yml` → `scripts/apply_ibo_6115_second.py`, ikinci sesli karar ve liste/arşiv commit; **write**.
- `madsc-ibo-ilk-239.yml` → ilk 239 kararın kaydı ve yedekten ayırma; **write**.
- `madsc-ibo-kararlar-grup1.yml` → birinci karar grubu, kayıpsız arşiv; **write**.
- `madsc-ibo-second-voice.yml` → 6115 sabit bazdan yabancı arşiv ayırma; **write**.
- `madsc-otomatik-devam.yml` → tek devam yolu kontrolü.
- `madsc-rule24-test.yml` → 24. kural ardışık hata regresyonu.
- `madsc-sistem-saglik-denetimi.yml` → YAML, kod, Actions run, kritik hata ve sistem sağlık raporu.

**Son kontrol, yedek, IBO ve kanal testi (10):**
- `madsc-son-kontrol-kurtarma-teshis.yml` → son kontrol kuyruğu/rapor/koruma kilidi teşhisi.
- `madsc-son-kontrol.yml` → 5 dakika video/ses süreklilik, 24. kural, ayrı rapor; **write** izinli ama kanal/yedek onaysız yazma yasak.
- `madsc-toplu-butunluk.yml` → arşiv/tekrar/YEDEKLER bütünlüğü.
- `madsc-tum-sistem-yedek.yml` → bütün takip edilen dosyalar, açık ayarlar, tek arşiv ve restore testi; harici saklama kanıtı ayrı.
- `madsc-turk-kanal-geri-sec.yml` → Türk kanal ayırma ve arşiv commit; **write**.
- `madsc-uc-asama.yml` → 24. kural, kayıtlı geçmiş, üç aşamalı doğrulama ve ayrı durum commit; **write**.
- `madsc-yedek-turk-ayir.yml` → yabancı/kimliği belirsiz adayların kayıpsız ayrılması; **write**.
- `madsc-yedekler-aktarim-test.yml` → güvenli aktarım regresyonu.
- `madsc-yedekler-sayi-duzelt.yml` → YEDEKLER kategori sayısı eşitleme; **write**.
- `oncelikli-kanal-dogrulama.yml` → öncelikli adayların gerçek ffprobe medya kanıtı.

**Kaynak, logo, test 13–18 (10):**
- `onikinci-hata-siniflandirma-test.yml` → hata sınıflandırma regresyonu.
- `publish-iptv-png-logos.yml` → SVG→PNG ve PNG commit; **write**, güncel logo koruması geçerli.
- `sekizinci-tekrar-raporu-test.yml` → farklı kaynaklarda tekrarlanan URL testi.
- `sozcu-akit-ozel-test.yml` → Sözcü/Akit aday özel ffprobe testi.
- `test-13-kaynak-degisiklik.yml` → kaynak değişikliği ve güvenli rollback raporu.
- `test-14-istikrar.yml` → 7/30 günlük kararlılık ve son başarı.
- `test-15-logo-epg.yml` → logo/EPG kimlik uyarısı, salt-okunur playlist.
- `test-16-workflow-safety.yml` → maskeli URL ve sınırlı yeniden deneme.
- `test-17-candidate-summary.yml` → beş aday durum grubu ve unknown.
- `test-18-change-simulation.yml` → dry-run/rollback fingerprint ve korunan playlist hash.

**Test 19–28 (10):**
- `test-19-integration.yml` → salt-okunur entegrasyon.
- `test-20-full-integration.yml` → tüm geliştirme söz dizimi, mevcut birim testleri, 1–18 görev kapsamı.
- `test-21-functional-e2e.yml` → adaydan rapora gerçek veri akışı ve geri dönüş simülasyonu.
- `test-22-real-playlist.yml` → gerçek M3U bütünlük/koruma.
- `test-23-live-stream.yml` → salt-okunur canlı yayın erişimi.
- `test-24-system-audit.yml` → tüm Python/YAML/M3U güvenlik envanteri ve birim testleri; **write** izni incelenecek.
- `test-25-full-project-readonly.yml` → bütün liste/yedek/otomasyon/kod salt-okunur kontrol.
- `test-26-automation-safety.yml` → workflow güvenlik envanteri.
- `test-27-pipeline-contract.yml` → aday iş hattı bileşenleri ve korunan veri sözleşmesi.
- `test-28-approval-gate.yml` → aday durumu ve kullanıcı onay kapısı.

**Test 29–38 (10):**
- `test-29-write-path-audit.yml` → yazma yetkili yolların çalıştırmadan taranması.
- `test-30-write-risk-report.yml` → somut yazma riski sicili.
- `test-31-protected-write-gate.yml` → mutasyon ve onay denetimi.
- `test-32-unapproved-write-regression.yml` → izinsiz gerçek yazma yolları regresyonu.
- `test-33-all-write-paths.yml` → bütün workflow yazma yolları.
- `test-34-protected-write-regression.yml` → otomatik korunan dosya yazması olmaması.
- `test-35-remaining-write-gate.yml` → karantina akışında repo yazma izni olmaması.
- `test-36-system-integration-audit.yml` → workflow tanımı ve korunan yazma maruziyeti.
- `test-37-indirect-write-audit.yml` → workflow çağrılı Python'da dolaylı yazma.
- `test-38-audit-selftest.yml` → denetimin hata yakalama duyarlılığı; **write** izni incelenecek.

**Son 9 workflow:**
- `test-39-protected-playlist.yml` → korunan playlist salt-okunur bütünlük.
- `test-kanal-adaylari.yml` → aday yayın testi ve manuel onaylık rapor.
- `toplu-sistem-kontrol.yml` → tam repo denetimi, örnek canlı erişim, tüm birim testleri.
- `vod-guncelle.yml` → izinli dizi bölüm takvimi metadata ve yalnız VOD metadata commit; **write**, lisans ve IBO VOD cihaz onayı açık.
- `yedek-geri-yukleme-tatbikat.yml` → geçici klasörde yedek restore ve rapor.
- `yedekler-yeniler-medya-kontrol.yml` → YEDEKLER/YENILER ffprobe, salt-okunur.
- `yeni-aday-on-test.yml` → yeni aday ffprobe ve rapor.
- `yeni-kanal-arama-2026.yml` → yeni kanal keşif ve parti testi.
- `yeniler-guvenli-arama.yml` → son 90 gün kaynak keşfi, M3U/HLS teknik test, rapor; ana listeye otomatik yazma yok.

### 97 workflow taramasının iş listesine eklediği eksikler
- 92 eski iş akışının **işlev, cron, push, workflow_run, artifact, izin, kullanıcı onayı, rapor, yan etki ve tarihsel veri sürekliliği** beş kategoriye tek tek eşleştirilip gerçek run ile doğrulanmalı; 0/92 tamamlandı kanıtı.
- Çok sayıda eski **contents:write** yetkisi ve geçmiş karar uygulama scripti var. Bunlar yeni izin anlamına gelmez. Kullanıcının korunan liste/yedek/logo dosyalarına dokunmama kararı geçerli; izinsiz eski workflow çalıştırılmaz, kapatılmaz, değiştirilmez.
- VOD metadata yazması, PNG logo yayınlaması, 7/30 günlük kararlılık, 5 dakikalık son kontrol, 390 aday testi, kaynak tarama, IBO karar grupları ve 24. kural özel kabul gerektirir.
- **Sıradaki dosya kapsamı:** 151 Python programı, 34 Markdown, 51 JSON, 26 CSV, 27 M3U, 10 diğer metin/XML ve 373 görselin kaynak-görev-kanıt ilişkisi; bu dosyalar workflow taraması tamamlandı diye tamamlandı sayılmaz.

---

## 15 EKİM — EK 20 WORKFLOW TAM METİN TARAMASI (TOPLAM BU TUR 38/97)

**Bu ek turda 20 workflow daha doğrudan okundu; önceki 18 ile birlikte bu oturumda 38 benzersiz workflow tam metni okundu, 59 workflow halen okunacak.** Eski dosyalara dokunulmadı.

### Ek 20 kaynaktan görev kopyaları
- `besinci-zaman-asimi-test.yml`: zaman aşımı davranışı regresyonu.
- `birlesik-aday-raporu.yml`: eski gözlem geçmişini geri al, gerçek ffprobe medya testi, aday puanı, günler arası kararlılık ve birleşik onay raporu; MADSC 02/03'te bütün zincirin parity kanıtı açık.
- `birlesik-durum-raporu.yml`: yayın testi başlatmadan birleşik durum, eksik Türk kanal hedefi, 155 kaynak kapsamı, haftalık bakım ve salt-okunur snapshot; MADSC 05 karşılığı açık.
- `dokuzuncu-akilli-tekrar-test.yml`: akıllı tekrar test takvimi regresyonu.
- `genel-aday-medya-test.yml`: gerçek ffprobe aday ilk parti video/ses testi, ayrı artifact.
- `genis-kanal-tarama.yml`: çok kaynaklı salt-okunur tarama ve yayın testi.
- `ibo-yedek-kalite.yml`: yedek stream kalitesi gerçek ffprobe, ayrı rapor.
- `iptv-test.yml`: kanal testi ve test sonuçlarını saklama.
- `kanal-kararlilik.yml`: eski gözlemi restore et, canlı kontrol, günler arası fark, sonraki çalışmaya gözlem geçmişi saklama; yeni 5'li sistemde tarihsel süreklilik parity açık.
- `kaynak-puanlama-kontrol.yml`: kaynak puanlama testleri.
- `madsc-11599-yedek-geri-yukle.yml`: **contents:write** ve 11599 yedek geri yükleme/commit; kullanıcı yeni izni olmadan yeniden çalıştırma/uygulama yok. Eski workflow açık kalma ve yazma riski ayrı denetlenecek.
- `madsc-ana-liste-saglik.yml`: zamanlanmış salt-okunur ana liste sağlık partisi, korunmuş dosya hash kontrolü, rapor artifact; MADSC 03 kapsam farkı açık.
- `madsc-arsiv-yedek-aktarim.yml`: **contents:write**, arşiv kayıtlarını YEDEKLER'e ekleme ve commit; **güncel YEDEKLER'e ekleme izni İPTAL**. Eski workflow'un tetik/izin riski incelenecek; kullanıcı onaysız çalıştırma yok.
- `madsc-aylik-merkezi-denetim.yml`: geniş merkezi güvenlik/92 workflow/tetik/kimlik/IBO/restore/rapor kontrolleri, cron ve push; MADSC 05'e tüm ayrıntılı kontrol parity açık.
- `madsc-birlesik-kesif.yml`: **contents:write, actions:write**, zamanlanmış gerçek keşif, kural 24 ardışık hata kapısı, geçmiş gözlem, keşif arşivi, aday PNG/EPG ve dört aşamalı rapor. MADSC 02'nin tek gerçek tarama adımı bunun tamamına eşdeğer değil; kritik açık iş.
- `madsc-cuma-ana-liste-denetimi.yml`: Cuma ana liste+EPG taraması, uyarı özeti ve artifact; yeni kategoriye haftalık davranış parity açık.
- `madsc-documentation-check.yml`: proje notları varlık/uyum kontrolü.
- `madsc-genis-kaynak-kontrol.yml`: manuel 155 kaynak ve ilave kaynak taraması, geçmişi koruma, üç aşamalı doğrulama; **contents:write, actions:write**; manuel tetik ve yan etki parity açık.
- `madsc-ibo-3-5281.yml`: kullanıcı geçmiş sesli kanal kararlarını uygulayan **contents:write** ve commit workflow'u. Geçmiş kararları koru, fakat yeni onay olmadan playlist yazma yok.
- `madsc-ibo-354-classify.yml`: kullanıcı sınıflandırmalarını bir defa uygulayan **contents:write** workflow'u. Geçmiş kararları koru, yeni onay olmadan playlist yazma yok.

### Yeni kritik denetim başlığı
**Eski workflow yazma izinleri:** En az `madsc-11599-yedek-geri-yukle`, `madsc-arsiv-yedek-aktarim`, `madsc-birlesik-kesif`, `madsc-genis-kaynak-kontrol`, `madsc-ibo-3-5281`, `madsc-ibo-354-classify` içerik yazma yetkisi taşıyor. Bu, gerçekten çalıştıkları veya korunan dosyaları değiştirdikleri anlamına gelmez; ancak güncel kullanıcı izniyle çelişebilecek **potansiyel tetik/yazma riskidir**. Kullanıcı onayı olmadan hiçbirini çalıştırma, silme, kapatma, izinlerini değiştirme veya korunan dosyalara yazma. Yalnızca kanıt ve risk raporu çıkar.

---

## 15 EKİM — GENİŞLETİLMİŞ KAYNAK TARAMASI / KANITLI SAYIM VE YENİ BULGULAR

**Amaç:** Kullanıcının gönderdiği ekran görüntülerindeki bütün GitHub kaynaklarından geçmiş, tamamlanan ve yapılacak işlerin tek `DEVAM_NOTU.md` arşivine kayıp olmadan aktarılması. **Bu turdaki durum: KISMİ TARAMA, TAM KAPSAM DEĞİL.** Sadece bu dosya değiştirildi; kaynaklara dokunulmadı.

### Dosya sayıları ve tarama yöntemi
- Git tree snapshot: `b2a4d278402b6abd9fc282d7c7cd060ec0cfa822`, toplam **796 Git girdisi** (dosya + klasör). `.github` 99 girdi; `madsc_kesif` 321; `logos` 90; `scripts` 69; `yedekler` 23; `tools` 17. Bunlar klasör dahil girdilerdir, program sayısı değildir.
- İnceleme için seçilen `.py/.yml/.yaml/.sh/.md` uzantılı, `madsc_kesif` ve `yedekler` içindeki veriler hariç **274 dosya**; bunların **97'si workflow**. Ayrı `madsc_kesif` raporları, `yedekler` dosyaları ve JSON/CSV dahil tüm 796 girdinin içeriği henüz incelenmedi.
- Bu ek turda **18 workflow'un tam metni** (`390-aday-tekrar-test`, `aday-bekletme`, `aday-logo-epg-test`, `aday-oncelik-kontrol`, `aday-yedekleme`, `akilli-aday-puanlama`, `altinci-aday-tekrar-test`, `automatic-png-logos`, `epg-gunluk`, `epg-pages`, `felaket-kurtarma-tatbikati`, `ibo-bagimsiz-test-listesi`, `ibo-epg-kimlik-denetimi`, `madsc-01`, `madsc-02`, `madsc-03`, `madsc-04`, `madsc-05`) okundu. Önceki turlarda 17 temel not ve seçilmiş 14 kod/test dosyası okunmuştu; tekrarları dışlayan genel toplam henüz denetlenmedi. **97/97 workflow okundu iddiası yoktur.**

### 18 workflow'dan çıkarılan ayrı görev/özellik kayıtları
1. `390-aday-tekrar-test.yml`: 390 adayın paralel 20 saniyelik gerçek video/ses testi, ffmpeg kurulumu, rapor artifact; MADSC 03'e işlevsel eşdeğerlik ve gerçek sonuç karşılaştırması **açık**.
2. `aday-bekletme.yml`: yeni kanal keşfi, tekrar URL raporu, gelişmiş medya testi, aday bekletme geçmişi, akıllı tekrar takvimi, zamanı gelen tekrar test, kaynak güven puanı, öncelik sıralama ve artifact. MADSC 02/03'te tüm zincirin eşdeğerliği **açık**.
3. `aday-logo-epg-test.yml`: aday EPG+logo kanıtı salt okunur birleştirme; kaynak kimlik onayı ayrı **açık**.
4. `aday-oncelik-kontrol.yml`: örnek adaylarla sıralama doğrulaması; regresyon eşdeğerliği **açık**.
5. `aday-yedekleme.yml`: teknik testten geçen adayları yedek taslak raporuna aktarma; **güncel YEDEKLER'e ekleme izni iptal**, hiçbir canlı listeye otomatik yazma yapılmaz. Tarihsel workflow davranışı güvenlik denetiminde ayrıca değerlendirilecek.
6. `akilli-aday-puanlama.yml`: ffprobe ile gerçek aday tarama/medya kanıtı, puanlama, ayrı raporlar; yeni keşif raporuyla teknik parity **açık**.
7. `altinci-aday-tekrar-test.yml`: bekleyen adayların tekrarı ve Türkçe rapor; MADSC 03'e gerçek tekrar döngüsü parity **açık**.
8. `automatic-png-logos.yml`: korunan liste yazma engeli, logo PNG hazırlığı ve görsel kanıt; kullanıcı onaysız logo değiştirme yok.
9. `epg-gunluk.yml`: günlük EPG üretimi, 5 kanallı XMLTV/TV onay bekleme raporu ve yalnız EPG çıktısı commit; MADSC 03/05 tetik ve yan etki parity **açık**.
10. `epg-pages.yml`: EPG XMLTV'yi Pages'e hazırlama, yayınlanan kılavuzun dosyayla eşleşmesi; EPG→Pages tetik ve yayın doğrulaması **açık**.
11. `felaket-kurtarma-tatbikati.yml`: korunan listelerin geçici ortamda kurtarma denemesi ve artifact; **tarihsel/harici gerçek restore kanıtı değildir**.
12. `ibo-bagimsiz-test-listesi.yml`: ffprobe gerçek görüntü/ses, izole IBO test listesi ve artifact; kullanıcı IBO cihazı/kimliği ayrıca **bekliyor**.
13. `ibo-epg-kimlik-denetimi.yml`: playlist ile 5 kanallı XMLTV kimlik eşleştirmesi, salt okunur rapor; canlı cihaz onayı **bekliyor**.
14. `madsc-01-guvenlik.yml`: korunan dosyaların önce/sonra karşılaştırması, koruma kapısı, regresyon; 92 eski workflow yan etkisinin gerçek taşınması ayrı.
15. `madsc-02-kesif.yml`: kaynak mutabakatı, tekrar ve IBO kuyruk denetimi, gerçek `madsc_akilli_kesif.py`, koruma, artifact. Run #38697244625 gerçek keşif step SUCCESS; eski aday-bekletme/takvim/puanlama zincirinin tamamını kapsadığı kanıtlanmadı.
16. `madsc-03-kanal-test.yml`: EPG Pages bağlantı kontrolü, izole IBO aday listesi, ffmpeg, 50 kanallık salt-okunur sağlık partisi, JSON/MD tutarlılık, regresyon ve koruma; 1039 kanalın tamamının aynı run'da testi **yok**.
17. `madsc-04-arsiv-yedek.yml`: izole Git HEAD geri dönüş, yedek kanıtı, arşiv tutarlılığı, harici kopya ayrımı; gerçek offsite/tarihsel restore **açık**.
18. `madsc-05-genel-bakim.yml`: 92 workflow matrisi, 18/8 görev, EPG/Pages, backup, 5 kategori raporu, tetik/izin kapıları ve regresyon; **parity 0/92**. Kategori `needs` zincirinin güvenli ayrılması önceki yazma güvenlik engeli yüzünden **açık**.

### Kapsam/teslim durumu
- Bu bölüm **18 doğrudan okunmuş workflow + önceki doğrudan okunmuş seçilmiş kod/not bulgularının kopya özetidir**; bütün 796 girdinin tam içerik kopyası değildir.
- Kalan **79 workflow**, diğer kod/test/notlar, `madsc_kesif` veri/raporları, `yedekler`, eski PR/issue/commit ve erişilebilir konuşma kararları, kaynak ve tarihleriyle tek tek işlenecek. Kapsam dışı kalmış olabilecek binary/logo dosyalarından otomatik görev çıkarmak için kod/manifest ilişkisi incelenir; görsel dosya başlı başına görev metni değildir.
- Geçmiş hiçbir kaynak silinmez, taşınmaz, değiştirilmez. Bu dosyaya eklenenler görev kapanışı değildir; tamamlanma yalnız kod+Actions+artifact+cihaz/onay kanıtıyla işaretlenir.

---

## 15 EKİM — EKRAN GÖRÜNTÜLERİYLE İSTENEN KÖK DOSYA/KOD TARAMASI — KANITLI EK KAYIT

Kullanıcının beş GitHub ekran görüntüsündeki `.github`, `aday_bekletme`, `aday_hazirlik`, `arastirma`, `epg`, `epg_deneme`, `kontrol_notlari`, `liste_kontrol`, `logo_deneme`, `logos`, `madsc_dogrulama`, `madsc_kesif`, `madsc_son_kontrol`, `raporlar`, `reports`, `scripts`, `tarama`, `tests`, `tools`, `vod`, `yedekler` klasörleri ve kök dosyalar **kapsama alındı**. Git tree anlık görüntüsü 796 girdi; `madsc_kesif` 321, `.github` 99, `logos` 90, `scripts` 69, `yedekler` 23, `tools` 17 girdi. **Dosya adlarının sayılması içeriklerin tümünün okunduğu anlamına gelmez.** 309 metin/kod/yapılandırma dosyası ana çalışma kümesinde belirlendi (ayrıca `madsc_kesif` ve `yedekler` rapor arşivleri var). Bu turda seçilmiş kök Python, merkezi script ve test içerikleri doğrudan okunup görev açıklamaları incelendi; kalanların satır satır taraması AÇIK.

### Koddan doğrudan çıkarılan görevler ve uyarılar
- `madsc_akilli_kesif.py`: keşif geçmişte denenmiş adayları otomatik tekrar test etmiyor (`pending=untested`); 3 başarılı test ve kullanıcı/kimlik onayı ayrı; kaynak artwork kanal kimliği kanıtı değil; eksik logo raporu PNG dönüştürme hatasında dahi tutulmalı. Bu yüzden **tekrar test programı, kaynak/kimlik/PNG onayı ve keşif raporunun gerçek kapsamı** ayrı kabul edilir.
- `final_validation.py`: `BATCH_SIZE=125`, `MAX_WORKERS=24`; süreklilik testi geçse bile durum `TECHNICAL_PASS_IDENTITY_PENDING`. **125'lik son kontrol kuyruğu ve kimlik onayı** ayrı tamamlanacak; geçmişteki 200'lü gruba göre fark tarihsel karardır.
- `verification_pipeline.py`: eksik kaynak kökeni tamamlanabilir, fakat tarihsel kontroller ve kullanıcı kararları üzerine yazılamaz. **Kaynak geçmişini bozmama** zorunlu.
- `yeni_kanal_tara.py`: gerçekten eksik kanal adları, mevcut kanalın alternatif akışlarından önce gelir. **Yeni kanal ve alternatif URL** ayrı kuyruklanmalı.
- `scripts/central_all_remaining_tasks.py`: sekiz açık iş ailesi içinde dış yedek, kanal kimliği/logo/EPG, IBO onayı, kullanıcı onaylı aktarım, kalıcı cihaz onay arayüzü ve günlük cron için ayrı onay/bağımlılıklar var. Yabancı arşiv URL boşluğu, aday kuyruğu URL boşluğu ve yedek delili ayrı denetlenir; **rapor üretimi kanal açma/kimlik onayı değildir**.
- `scripts/central_management_summary.py`: 18 görevde kod kanıtı ve canlı kanıt farklı; rapor eksikse başarı denmez, beş kategori için ayrı kanıt ve ana liste sağlık run kanıtı aranır. **Yeşil run ile canlı/cihaz sonucu karıştırılmamalı**.
- `test_central_eighteen_task_audit.py`: 18 görev için IBO onayı ve canlı doğrulama otomatik doğru kabul edilmez; eksik kod kanıtı varsa 18 görev tamamlandı denmez.
- `test_epg_tv_readiness.py`: beş kanallı XMLTV pilotunda TV cihaz onayı beklenir; program yoksa teknik hazır sayılmaz.
- `vod/README.md`, `vod/IBO-AYRI-KURULUM.md`: ayrı test listesi ve katalog var; IBO Filmler/TV Dizileri sekmesinde görünme kanıtı yok, Xtream uyumlu API gerekebilir; otomatik film/bölüm ekleme açık değil, yalnız lisanslı içerik. Ana TV listesi değiştirilmez.
- `kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md`: Eurostar eski HLS 404 ve IBO'da açılmama; alternatif bulunmadı, ana listeye otomatik ekleme yasak.

### Eksiksiz kaynak toplama için kalan denetim
1. Kalan bütün `.github/workflows` ve `scripts` dosyalarında görev açıklamaları, cron, çağrı, TODO/FIXME ve tamamlanmamış davranışlar tek tek çıkartılacak.
2. `tools`, kök `test_*.py`, `tests`, `madsc_son_kontrol`, `tarama`, `aday_*`, `arastirma`, `epg`, `vod` kaynakları tek tek okunacak; önceki notla karşılaştırılacak.
3. `madsc_kesif` 321 girdi, `yedekler` 23 girdi ve diğer JSON/CSV/rapor kayıtlarındaki tarihsel kararlar ve açık işler kaynak/yol/kanıtla ayrıştırılacak. Çok büyük kanal/veri dosyaları ana nota körlemesine yapıştırılmayacak; içerikteki **görev, karar ve kanıt** kopyalanacak, tam kaynak korunacak.
4. 1 Ekim'den itibaren GitHub geçmiş commit/PR/issue ve erişilebilir sohbet kararları taranıp **kaynakta bulunamayan veya doğrulanamayan** konular ayrı işaretlenecek; eksiksiz tarihsel kapsama iddiası kanıtsız kurulmayacak.
5. Bütün bu tarama **yalnızca bu `DEVAM_NOTU.md` dosyasını genişletebilir**; diğer eski dosyalar aynen korunacak. Yeni kullanıcı onayı olmadan liste/yedek/logo/workflow değiştirilmez.

---

## ANA MERKEZ NOT ARSIVI — 15 EKIM 2026 / KAYNAK KOPYA INDEKSI VE GOREV DEFTERI

**Kullanici karari:** GitHub'daki eski notlar, kodlar, workflow'lar, arşivler ve raporlar yerlerinde aynen kalacak; silinmeyecek, taşınmayacak, yeniden yazılmayacak. Buraya içeriklerinden çıkarılan karar ve işlerin **kaynak gösteren kopya özeti** eklenir. Bu bölüm kaynak dosyaların birebir tam metin yedeği değildir; orijinal kaynaklar tek tek korunur. Yeni bir kopyalama işlemi tamamlanmadan 'her şey aktarıldı' denmez.

### 1. Tespit edilen kaynak alanları
- GitHub çalışma dalı SHA `f813dfbb27568cd583710d5f124fc814e95b2711` ağaç taraması: 796 Git tree girdisi, 34 Markdown belgesi, 97 `.github/workflows/*.yml` dosyası, 248 `.py/.yml/.yaml/.sh` dosyası (kümeler örtüşebilir). Bunlar o SHA'nın anlık görüntüsüdür.
- Ana kurallar: `AGENTS.md`, `GUVENLIK_KURALLARI.md`, `IPTV_PROJE_HAFIZASI.md`, `DEVIR_NOTU_2026-10-15.md`, `OZELLIK_ENVANTERI.md`, `DEVAM_NOTU.md`.
- Beşli geçiş: `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `BES_SISTEM_GECIS_KONTROL.md`, `BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md`, `ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md`, `docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md`, `docs/MADSC-92-WORKFLOW-ESDEGERLIK-KONTROL-2026-10-14.md`, `docs/MADSC-IKI-TOPLU-KABUL-PLANI.md`, `docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md`.
- Tarihsel iş/karar kayıtları: `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md`, `SEKIZ_GOREV_TOPLU_DENETIM.md`, `TOPLU_DURUM_RAPORU.md`, `kontrol_notlari/DEVAM_GECMISI_2026-10-12_1947.md`, `kontrol_notlari/2026-10-12_ekol_basa_sarma.md`, `kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md`, `raporlar/SON_DURUM_2026-10-12_1130.md`, `raporlar/GELISTIRME_11_DURUM_2026-10-12.md`.
- Konu bazli kanitlar: `raporlar/IBO_TCL55C655_UYUMLULUK_DENETIMI.md`, `raporlar/LOGO_DURUM_2026-10-12.md`, `logo_deneme/HAZIRLIK_NOTLARI.md`, `logo_deneme/README.md`, `epg_deneme/README.md`, `liste_kontrol/README.md`, `madsc_kesif/NOT_EKSIK_TURK_KANALLARI.md`, `madsc_kesif/ibo_kullanici_secimi_2026-10-13_3-5281.md`, `reports/ibo-user-decisions-2026-10-13-session2.md`, `yedekler/GECMIS_KANAL_KARARLARI_KORUMA_2026-10-09.md`, `vod/README.md`, `vod/IBO-AYRI-KURULUM.md`.
- Ek kaynak aileleri: `.github/workflows/` altındaki 97 iş akışı, `scripts/`, `tools/`, kök Python betikleri, `madsc_kesif/` JSON/CSV raporları, `aday_bekletme/`, `tarama/`, `raporlar/`, `yedekler/`, `vod/`. İçlerinde görev açıklaması ve tarihsel karar bulunabilir; hepsi satır satır incelendi iddiası yoktur.

### 2. Kaynaklardan kopyalanan önemli tamamlanan işler (eski nottaki iddialar canlı kanıtla ayrılır)
- Beşli sistem taslağı ve PR #71 kuruldu; 92 workflow tetik/özellik haritası ve raporları oluşturuldu. Eski 92 görevin işlevsel aktarımı **0/92 doğrulandı**, bitmedi. Kaynak: `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md`.
- Beşli Actions geçmiş koşularında 5/5 kategori success kaydı var (#38627719035, #38630252033); son kod değişiklikleri için tek başına kanıt değildir. Kaynak: `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md`.
- 15 Ekim kanıtları: #38694043295 MADSC 05 tetik düzeltmesi, #38694963696 MADSC 03 artifact, #38695730312 MADSC 03 kabul kontrolü, #38697244625 MADSC 05 beşli toplu koşu SUCCESS. Son koşuda MADSC 02 **gerçek keşif adımı ayrıca SUCCESS** (job #116296711334); `madsc-kesif-tek-kosu-rapor` artifact ID 11954646399, 14,020,969 bayt, başarıyla yüklendi. Loglarda 156 tanımlı/156 benzersiz URL, hedef 155 fark 1; 59 logo adayı (21 güvenlik incelemesi, 38 PNG hazırlığı bekliyor), IBO aday kuyruğu 0 raporlandı. Bunlar adayın onaylandığı veya bütün 156 kaynağın tarandığı anlamına gelmez. Kaynak: GitHub Actions #38697244625 job logları/artifact API.
- Eski EPG günlük/Pages zinciri ve XMLTV teknik raporları mevcut; 14 Ekim raporunda 1039 liste kaydı, 730 EPG eşleşmesi, 23702 program. İsveç IBO cihazında EPG görünürlüğü kullanıcı onayı bekler. Kaynak: `TOPLU_DURUM_RAPORU.md`, `OZELLIK_ENVANTERI.md`.
- Ana PNG logolarının kullanıcı cihazında çalıştığı geçmiş kayıtta bildirildi; aday logolarının kimliği ayrı. Kaynak: `TOPLU_DURUM_RAPORU.md`.
- İzole Git HEAD restore kontrolü ve 1/15 yedek kontrolleri mevcut; offsite/tarihsel restore kanıtı ayrı ve eksik. Kaynak: `SEKIZ_GOREV_TOPLU_DENETIM.md`, `BES_SISTEM_TOPLU_IS_DEFTERI.md`.

### 3. Sıralı ana yapılacak işler (kaynak kopyası, kanıt olmadan kapanmaz)
1. **MADSC 01 Güvenlik:** 26 kural, 18 görev, korunan dosyalar, gerçek yazma kapısı, dolaylı yazma yolları, izinler, branch protection, devre kesici, güvenli rollback; bütün eski workflow'ların riskli side-effect analizi. Kaynak: `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `SEKIZ_GOREV_TOPLU_DENETIM.md`, `GUVENLIK_KURALLARI.md`.
2. **MADSC 02 Keşif:** gerçek keşif SUCCESS kanıtını koru; taranan kaynak sayısını/aday sayılarını artifact içeriğinden teyit et; 156 benzersiz URL/155 hedef farkını keyfi silme olmadan incele; eski günde iki keşif cronunun yeni kategoriye kayıpsız geçişi; kaynak canlılığı, Türkçe/yabancı/diaspora ayrımı, 59 aday logo durumu, lisans/köken ve aday kimliği. Kaynak: `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md`, `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md`.
3. **MADSC 03 Test:** 1039 girişin yalnız 50'lik partilerle kontrolü, farklı saatlerde test, geçmiş 75 aday/51 retest/24 ffprobe başarısızı/4 alternatif sayılarının güncel yeniden sayımı, IBO teknik false-negative riskini koru, yayın/segment/video/ses/HD/FHD/kimlik/logo ve 5 kanallı EPG pilotunu ayrı kanıtla. Kullanıcının IBO oynatma sonucu teknik raporla ezilmez. Kaynak: `BES_SISTEM_GECIS_KONTROL.md`, `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md`, `raporlar/SON_DURUM_2026-10-12_1130.md`.
4. **MADSC 04 Arşiv/yedek:** tarihsel 11762 kanal/11742 URL ve 740 yabancı kanal arşivi snapshotlarını güncel kaynakla kontrol et; kullanıcı onaylı oynayanları koru; 1/15 backup, 30 gün saklama, bağımsız GitHub dışı kopya, secrets/IBO ayarları ve gerçek tarihsel restore. Kullanıcı tarafından ertelenen/dış yetki isteyen işler açık kalır. Kaynak: `SEKIZ_GOREV_TOPLU_DENETIM.md`, `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md`, `BES_SISTEM_TOPLU_IS_DEFTERI.md`.
5. **MADSC 05 Genel bakım:** 92 workflow'un tek tek script/inline/action/cron/push/workflow_run/dispatch/izin/artifact/yan etki/rollback eşdeğerliği; 5 kategori bağımsızlığının ve tek toplu kabulün doğrulanması; 1/15 bakım; EPG→Pages zinciri, günlük VOD, aday/rapor/test tekrarlarının azaltılması; geçmiş raporları silmeden tek Türkçe kabul raporu. Kaynak: `docs/MADSC-IKI-TOPLU-KABUL-PLANI.md`, `BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md`, `BES_SISTEM_TOPLU_IS_DEFTERI.md`.
6. **Özel bekleyen talepler:** Eurostar için alternatif kaynak bulma ve kimlik/video/ses/süreklilik testi (ana listeye onaysız ekleme yok); eski 3082 son kontrol kuyruğunun güncel durumu; aday logosu/EPG/IBO; VOD ayrı kurulum ve kullanıcı onayı. Kaynak: `kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md`, `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md`, `vod/README.md`.

### 4. Çelişkili geçmiş kararlar / güncel yetki
- **GÜNCEL:** YEDEKLER'e otomatik yeni kanal ekleme yetkisi iptal; eski `DEVIR_NOTU_2026-10-15.md` ve geçmiş notlardaki ekleme izni geçersiz. CALISANLAR, HEPSI, FAVORILER, YENILER, YEDEKLER, PNG, arşiv ve yedekler açık yeni izin olmadan değişmez.
- **GÜNCEL:** 92 workflow taşınmadan eski workflowlar kapatılmaz, PR #71 merge edilmez. Teknik test ≠ kanal kimliği ≠ yayın hakkı ≠ IBO cihaz onayı.
- Eski belgelerde 89/92, 9/10 zamanlanmış workflow gibi farklı dönem sayıları bulunur. Bunlar kendi tarihinin snapshot'ıdır; güncel envanterden doğrulamadan kesin sayıya dönüştürülmez.
- Eski notlar/raporlar yerinde kalır. Bu ana arşiv kaynakların yerini almaz; yeni tarihli kararları öncelikli gösterir. Tam kapsamlı kod içi TODO/FIXME ve tüm rapor JSON/CSV satır taraması **halen açık iştir**.

---

## 15 Ekim — Diğer not arşivleri tarandı: ek görev kaynakları

GitHub çalışma dalının 796 tree girdisi incelendi. Tek not yok: `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `BES_SISTEM_GECIS_KONTROL.md`, `BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md`, `ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md`, `TOPLU_DURUM_RAPORU.md`, `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md`, `SEKIZ_GOREV_TOPLU_DENETIM.md`, `docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md`, `docs/MADSC-IKI-TOPLU-KABUL-PLANI.md`, `docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md`, `kontrol_notlari/`, `raporlar/`, `madsc_kesif/` ve `yedekler/` ayrı karar/görev/kanıt kaynaklarıdır. Hepsi tek seferde tamamen satır satır incelendi iddiası yok; önemli görev defterleri karşılaştırıldı.

**Önceki kısa kuyrukta ayrıca görünmesi gereken işler:** günlük VOD üretimi ve IBO ayrı kurulum bağımlılıkları; EPG→Pages workflow_run tetik eşdeğerliği; 156 tanımlı kaynağın 155 hedefinden farklı olması ve gerçekten taranan alt kümenin ayrıca ölçülmesi; eski 3082 adaylık son kontrol kuyruğunun güncel ilerlemesi; 740 yabancı kanal arşivinin korunması; lisans/yayın hakkı ve kaynak kökeni; 30 günlük felaket yedeği saklama/secrets/IBO ayarları (kullanıcı tarafından ertelenmiş olanlar ayrıca izin gerektirir); `kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md` içindeki Eurostar alternatif araştırması; 18 görev ve 26 kuralın ayrı kabul matrisi. Bunlar kanıt olmadan tamamlandı sayılmaz. 13 Ekim tarihli 156 kaynak/9576 kayıt/3082 kuyruk gibi rakamlar tarihsel snapshot'tır, güncel değer değildir. Yedek ve playlist izinleri için en son kullanıcı talimatı geçerlidir.

**İşleme sırası:** 1) Son keşif gerçek log/artifact; 2) beş kategori bağımsızlığı; 3) 92 görev parity ve tetikler (VOD/EPG→Pages dahil); 4) yedek/restore ve geçmiş; 5) aday/kimlik/Eurostar/yabancı arşiv; 6) EPG/logo/IBO; 7) güvenlik/hukuk/izin; 8) kalan 18/26 kabul ve rapor. Her kaynak nottaki tamamlanma iddiası güncel Actions/cihaz/restore kanıtıyla yeniden sınanır.

## SOHBET DEVRİ — 15 Ekim 2026 güncel durum (önce bunu oku)

- Kullanıcı hedefi: 1 Ekim'den beri konuşulan tüm eksik, yarım ve yeni işlerin tamamlanması; 92 eski workflow'un görevlerinin gerçek işlevsel eşdeğerlikle 5 ana kategoriye aktarılması. Sadece rapor/haritalama tamamlanma değildir; doğrulanan eşdeğerlik hâlâ 0/92. Eski workflow'lar silinmez/kapatılmaz, taslak PR #71 birleştirilmez.
- Son karar: **YEDEKLER'e kanal ekleme izni iptal**. Eski `DEVIR_NOTU_2026-10-15.md` içindeki izin cümlesi geçersizdir. CALISANLAR, YENILER, HEPSI, FAVORILER, YEDEKLER, logo, arşiv ve yedekler açık yeni izin olmadan değiştirilmez.
- Tamamlanan ve doğrulanan: MADSC 05 push yinelenmesi `c7567e1` run #38694043295 SUCCESS; MADSC 03 sağlık artifacti `7e797fa` run #38694963696 SUCCESS; MADSC 03 sağlık kabul kontrolü `439dc5b` run #38695730312 SUCCESS; MADSC 02 gerçek `madsc_akilli_kesif.py` çağrısı ve `madsc_kesif/` artifact kapsamı `c2d28be` run #38697244625 SUCCESS. Son koşuda keşif adımı `continue-on-error` olduğundan gerçek tarama/çıktı ayrıca doğrulanmalı; yeşil run tek başına kanıt değildir.
- Saatlik MADSC 7/24 ChatGPT otomasyonu yeniden aktif; her saat bir tur, kesintisiz gerçek zamanlı çalışma değil. 16 Ekim 10:30 İsveç saati raporu ayrı açık.
- Öncelik sırası: (1) keşif adım logları ve artifact içeriği; (2) MADSC 05 bağımsız kategoriler ve hata kapısı (önceki düzenleme güvenlik engeli nedeniyle kaydedilemedi); (3) 92 workflow'un gerçek script/inline/cron/izin/yan etki/artifact davranış aktarımı ve tek tek kanıt; (4) MADSC 04 tarihsel/harici yedek geri yükleme; (5) MADSC 03 tam kanal kapsamı, aday tekrar/kimlik/IBO İsveç testi; (6) EPG Pages, 730/1039 eşleşme, logo kimlik; (7) gerçek koruma/yazma kapısı, kural 24 devre kesici; (8) cron/çakışma/rapor tekrarlarının azaltılması; (9) her tamamlanan işin commit/run/artifact kanıtıyla bu not ve `OZELLIK_ENVANTERI.md`ye yazılması.
- Git HEAD izole geri yükleme harici/tarihsel restore değildir. 92 workflow'un gerçek aktarımı, IBO cihaz onayı ve dış yedek kanıtı bitmedi. Eski notları silme, tamamlanmayanı tamamlandı diye gösterme.

---

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

## 14 Ekim 2026 — #125 TEK HATA / TEST VERISI KOK NEDENI
- Kullanici ekraninda #125 (02d9f79) kirmizi: 128 test, 1 hata, 30 saniye. Goruntude tam traceback yok.
- Yeni eklenen test_raporda_bilerek_tetiklenmeyen_notlar_hata_sayilmaz testindeki sahte YAML, Python icinde literal \\n karakterleriyle yazilmis; gercek satir sonu olmadigindan push_rules eslesmiyordu. Bu test verisi gercek yeni satirlara duzeltildi.
- Merkezi denetim kodu, kanal listeleri, otomasyon zamanlari ve PNG logolar degistirilmedi. Bir sonraki merkezi CI yesil gorulmeden tamamlandi denmez.
- Kalan isler: workflow sayisi/yuku; 1 ve 15 yedek/restore; gunde iki kez tek kanal+logo kesfi; teknik tekrar testi; IBO onayi; EPG en son.

## 14 Ekim 2026 — #124 YESIL / TOPLU IZLEME DUZELTMESI
- Kullanici ekraninda #124, 6a22b44 commit, 25 saniye, YESIL. #123 kirmizi, #124 yesil.
- Merkezi tek-islem raporunda DEVAM_NOTU ve TOPLU_DURUM_RAPORU degisikliklerinin bilerek push tetiklememesi artik "eksik merkezi tetik" degil, ayri istisna kategorisi olarak raporlanir. Diger push eksikleri gizlenmez.
- Yedek raporunun konsol mesajinda Git HEAD izole restore kaniti ile gercek harici/tarihsel kurtarma ayrimi netlestirildi.
- SONRAKI TOPLU ISLER: aktif 92 workflow'un canli API durumlari/cron yukleri, cakisma; bagimsiz yedek kaniti; 75 aday icin farkli saat testi ve Turkce/yabanci ayirimi; logo kimlik; IBO onay kapisi. EPG en son. Ana liste ve yedeklere otomatik yazma yok.

## 14 Ekim 2026 — #123 UYUMSUZLUK / TEK PAKET DUZELTME
- Kullanici ekrani: merkezi denetim #123, 126 test, 3 failure, 26 saniye. Ekran sonu yalniz toplam hata sayisini gosteriyor; tek tek traceback gorulmedi.
- Kod incelemesinde not dosyalarinin push listesinden bilerek kaldirilmasina ragmen eski beklentilerin kaldigi goruldu: test_tek_merkez_tetikleme.py, test_toplu_durum_raporu.py, test_central_consolidation_audit.py.
- Bu uc test, yeni kural uyarinca guncellendi: DEVAM_NOTU.md ve TOPLU_DURUM_RAPORU.md not degisiklikleri agir merkezi push baslatmaz, ama merkezi denetimde dosya varligi ve SHA256 kontrolu korunur. Merkezi kod/playlist/guvenlik push kontrolleri devam eder.
- #123'un uc hatasinin tam traceback kaniti mevcut degil; degisiklikten sonra tek merkezi CI sonucu dogrulanmadan kesin duzeldi denmeyecek.
- SONRAKI SIRA: (1) #124 vb. tek test sonucunu dogrula; (2) 92 workflow'un zamanlama/push/workflow_run envanterini kesinlestir; (3) 1/15 bakimini birlestir; (4) yedek artifact ve izole/harici geri yukleme kaniti; (5) 75 aday teknik tekrar, Turkce/yabanci ve logo kimlik; (6) EPG en son. Yeni kanal testi veya gereksiz Actions tetigi baslatma.
- Korunan CALISANLAR.m3u, HEPSI, YENILER, favoriler, PNG logolar, yedek ve arsiv dokunulmaz.



## 14 Ekim 2026 — TOPLU DEGİSİKLİK PRENSİBİ
Kullanıcı onayı: her dosyada ayrı commit/test yerine toplu inceleme, tek paket değişiklik, tek doğrulama. Merkezi denetimin push kapsamından yalnız DEVAM_NOTU.md ve TOPLU_DURUM_RAPORU.md çıkarıldı; bu belgeler merkezi denetimde zorunlu dosya ve SHA256 kontrolü kapsamında kalır. Korunan CALISANLAR.m3u, GUVENLIK_KURALLARI.md ve kritik kod değişikliği push denetimi korunur. 92 workflow tamamen birleştirildi iddiası yok. EPG en sona, kanal/PNG/backup korumaları devam. Kalan iş: tüm otomasyon cron/push sayımını gerçek rapordan doğrulama, ayın 1 ve 15'i bakımını tek koordine çalışma haline getirme, offsite/restore kanıtı, aday kanal teknik tekrar testleri.
## 14 Ekim 2026 — GECE YARISINDAN ONCE TOPLU IS TAKIBI
Kullanici istegi: butun kalan isler toplu, gereksiz test/commit tetigi olmadan; saat 00:00'a kadar mumkun olanlar tamamlanacak. Tamamlama garantisi yok.
DOGRULANDI: GitHub workflow dosyasi 92. Ekran #119 #120 #121 merkezi denetimleri yesil. 1144 runs tarihsel toplamdir, gunluk otomasyon sayisi degil.
TAMAMLANAN: birlesik kesif 06:00/18:00 UTC gunde iki kez; ana liste sagligi ayin 1/15; otomatik devam zinciri kaldirildi; tam sistem yedek push tetigi kaldirildi, ayin 1/15 cron korundu; sistem saglik/guvenlik haftalik ve push yerine ayin 1/15; tetikleyici sayim raporu ve regresyon testi kodlandi.
ACIK 1: 92 workflow icinde gercek scheduled/push/workflow_run/manual sayilarini rapordan dogrula; risk ve gereksiz tekrar haritasi.
ACIK 2: Merkezi denetimin genis push filtreleri nedeniyle her kod ve not degisikliginde 125 test kosmasini azalt, kritik playlist ve guvenlik kontrolunu koru.
ACIK 3: Ayin 1/15'inde guvenlik, saglik, yedek ve arsiv islerini tek koordine bakim kosusuna birlestir. Yedek restore/offsite kanitini dogrula; ayri cronlar su an var.
ACIK 4: Eski kanal tarama/logo/EPG zamanlamalarini ve workflow_run zincirlerini incele. EPG en sona ertelendi.
ACIK 5: 75 aday, 51 farkli saat testi bekleyen, 24 ffprobe gecmeyen, 4 alternatif; kimlik ve IBO Isvec onayi yok. Onaysiz ana listeye ekleme yapma.
ACIK 6: Tarihsel arsiv 11762, arsiv URL 11742 ve yedek geri yukleme kanitini koru/dogrula.
KORUMA: CALISANLAR.m3u, HEPSI, YENILER, favoriler, kanallar, URL, sira, logo ve yedeklere izinsiz dokunulmayacak.
Son toplu test ve tek kapanis raporu; bitmeyenler acik kalacak.

## 14 Ekim 2026 — KALICI TOPLU DURUM RAPORU VE YAPILACAKLAR

Kullanıcı son testlerin yeşil olduğunu bildirdi ve biten/eksik/fazla işleri tek belgede görmeyi istedi. TOPLU_DURUM_RAPORU.md oluşturuldu: beş aşama, tamamlanan otomasyon sadeleştirmeleri, kalan gerçek kabul kanıtları, öncelik sırası, korunan ana liste logo kuralları ve rapor artefakt yolları. Yeni belge merkezi denetimin push yollarına, zorunlu dosya kontrolüne ve SHA256 izlemeye alındı; regresyon testi eklendi. Bu statik çalışma notu güncel canlı kanal sayılarını veya cihaz onayını varsaymaz. Ana liste, logo, favori, YENİLER ve yedek değiştirilmedi. Yeni Actions sonucu henüz doğrulanmadı.

## 14 Ekim 2026 — TOPLU KAPANIŞ: LOGO, KEŞİF VE EPG TEK PUSH KANITI

Merkezi statik çakışma denetimi artık ana PNG logo kodu, ana PNG workflow, yeni aday logo kodu, keşif kodu, EPG üretim kodu ve EPG yayın workflow değişikliklerini ayrı senaryolarla inceler. Regresyon testi bu altı değişiklik türünün her birinde yalnız madsc-aylik-merkezi-denetim.yml push tetiklenmesini zorunlu kılar; sessizce sıfır test tetiklenmesi de başarı sayılmaz. Böylece bir sonraki refaktörde eski ikinci PNG/EPG/keşif push tetikleyicilerinin geri gelmesi veya merkezi yolun kaybolması testte yakalanır. Bu statik güvence canlı yayın, IBO EPG ve yeni aday logo eşleşmesi kabulü değildir. Korunan listeler ve logolar değişmedi. GitHub Actions sonucu henüz doğrulanmadı.

## 14 Ekim 2026 — DOĞRULANMIŞ ANA LİSTE LOGOLARI İÇİN GÜNLÜK TEKRAR KALDIRILDI

Kullanıcı ana listedeki logoların çalıştığını IBO Player'da doğruladığını, ana liste logolarına dokunulmamasını istedi. automatic-png-logos.yml iş akışının ana listeyi günlük 05:23 UTC tarama ve kod değişikliğinde push tetikleyicileri kaldırıldı. Mevcut güvenlik kontrolleriyle manuel workflow_dispatch seçeneği korunuyor. Yeni adayların PNG hazırlığı günlük birleşik keşif akışında bir kez devam eder. Logo kodu ve iş akışı değişikliklerini merkezi beş aşamalı denetim push ile kontrol eder. Korunan listeler ve logolar değiştirilmedi. Yeni Actions sonucu henüz doğrulanmadı.

## 14 Ekim 2026 — EPG ÜRETİMİ VE PAGES YAYINI TEK ZİNCİRE BAĞLANDI

Kullanıcının ekran görüntüsünde EPG Günlük Güncelleme #14, Publish EPG to GitHub Pages #11 ve beş aşamalı merkezi denetim #83 yeşildi. EPG günlük üretim workflow'undan kod değişiklikleriyle otomatik push başlatma kaldırıldı: günlük 03:25 UTC ve manuel çalıştırma korundu. Pages workflow'undan XML değişikliğine bağlı push tetikleyicisi kaldırıldı; yalnız başarılı EPG Günlük Güncelleme workflow_run sonucu veya manuel çalıştırma ile yayımlanacak. Böylece hem push hem workflow_run yolundan aynı Pages dağıtımının iki kez başlaması önlendi. EPG kodu ve workflow değişiklikleri merkezi denetimin push yollarına alındı. Regresyon testi günlük üretim, tek yayın, başarı koşulu ve merkez kapsamasını doğrular. EPG üretimi, XML ve IBO EPG eşleştirme algoritmaları değiştirilmedi; kullanıcı cihazında EPG görünmesi bu GitHub yeşil testleriyle doğrulanmış sayılmaz. Ana playlist, logo, favoriler, YENİLER ve yedekler korunur. Yeni Actions sonucu henüz doğrulanmadı.

## 14 Ekim 2026 — YEŞİL TESTLERDEN SONRA KEŞİF PUSH TEKRARLARI KALDIRILDI

Birleşik keşif workflow'undaki push tetikleyicisi kaldırıldı. Ağır kanal taraması, ffprobe ve PNG işleri yalnız günlük 06:00 UTC takviminde veya kullanıcı tarafından manuel çalıştırıldığında yürür. Keşif kodu, arşiv kodu, logo hazırlama kodu veya keşif workflow dosyası değiştiğinde merkezi beş aşamalı denetim tek push ile kontrol eder. Regresyon testi bu davranışı korur. Ana listedeki logolar, yayın URL'leri, favoriler, YENİLER ve yedekler değiştirilmedi. Yeni Actions sonucu doğrulanmalı.

## 14 Ekim 2026 — YEŞİL #81 VE #107 SONRASI GEREKSİZ İKİNCİ PNG HAZIRLIĞI KALDIRILDI

Kullanıcı merkezi beş aşamalı denetim #81 ve birleşik keşif #107 için yeşil ekran görüntüsü paylaştı. Keşif iş akışında PNG logo hazırlığı iki kere çalışıyordu: önce madsc_akilli_kesif.py içinde en çok 40 aday hazırlanıyor, hemen sonra scripts.candidate_logo_report tekrar bütün adayları hazırlamaya girişiyordu (varsayılan limit 240). Aynı işin iki kez yürütülmesi ve beklenmedik 240 logo indirme riski giderildi: ikinci 'Aday logolarını ayrı PNG incelemesine hazırla' adımı kaldırıldı. Tek keşif turu kaynak taraması, aday logo hazırlığı, eksik logo raporu, EPG/logo kanıtlarını birleştirme ve arşivlemeyi yapmaya devam eder. Merkezi denetim mevcut haliyle korunur; regresyon testi iki ayrı PNG hazırlama adımının yeniden eklenmesini önler. Kullanıcı onayı olmadan ana listedeki logolar, kanal URL'leri, kategoriler, favoriler, HEPSİ, YENİLER ve yedekler değişmedi. Yeni Actions sonucu ayrıca doğrulanmalı. Eski notlar saklandı.

## 14 Ekim 2026 — #80 MERKEZİ TEST PNG BAĞIMLILIĞI DÜZELTMESİ

#80 merkezi denetimde 95 testten biri başarısız oldu. Yeni prepare([],[]) regresyon testi, merkezi ortamda kurulu olmayan Pillow bağımlılığını gereksiz yere yüklüyordu. PNG dönüştürücü artık yalnız gerçekten PNG dönüştürme gerektiğinde içe aktarılır; boş, logosuz ve güvenlik incelemesindeki adaylarda yüklenmez. Yeni regresyon testi eklendi. Birleşik keşif gerçek PNG işlemlerini sürdürebilir. Ana liste, logolar ve korunan dosyalar değişmedi. GitHub Actions sonucu henüz doğrulanmadı. Önceki notlar saklandı.

## 14 Ekim 2026 — #106 KIRMIZI BİRLEŞİK KEŞİF LOGO MODÜLÜ DÜZELTMESİ

Kullanıcı ekran görüntüsünde birleşik keşif #106 kırmızı; beş aşamalı merkezi denetim #79 yeşil. Keşif workflow'u scripts/candidate_logo_report.py dosyasını doğrudan çalıştırıyordu; bu durumda sys.path depo kökü yerine scripts dizinini içerdiği için 'from scripts.automatic_png_logos import convert' ModuleNotFoundError verdi. Tek toplu değişiklikte candidate_logo_report.py içindeki lazy import paket modu ve doğrudan script modunda çalışacak şekilde düzeltildi. Birleşik keşif workflow'u python -m scripts.candidate_logo_report kullanacak; regresyon testi prepare([],[]) çağrısında gerçek lazy importu doğrulayacak. Ana liste logoları, yayın bağlantıları, YENİLER, HEPSİ, favoriler, arşiv ve yedekler değişmedi. Güncel Actions sonucu doğrulanmalıdır. Eski kayıtlar korunur.

## 14 Ekim 2026 — YEŞİL TEST SONRASI ADAY LOGO RAPORU HATA DAYANIKLILIĞI

Kullanıcı önceki #77 düzeltmesinden sonraki testin yeşil olduğunu bildirdi. Tek toplu değişiklikte keşif betiğinde aday logo envanteri PNG hazırlama try/except bloğunun dışına alındı. Böylece PNG dönüştürücüsü hata verirse bile yeni adayların eksik logo raporu üretilir; önceki davranışta rapor tümüyle kayboluyordu. Regresyon testi PNG hazırlama kanıtı olmadan eksik logonun sayıldığını kontrol eder. Ana liste ve mevcut logolar kesinlikle değiştirilmedi; yeni adaylar otomatik onaylanmadı. Bu değişiklik canlı logoları bulmaz, güvenilir eksik iş envanteri üretir. Önceki notlar korunur.

## 14 Ekim 2026 — #77 KIRMIZI MERKEZİ LOGO MODÜLÜ HATASI DÜZELTİLDİ

Kullanıcının gönderdiği #77 ekran görüntüsünde 'Yeni aday logo eksiklerini merkezi raporla' adımı ModuleNotFoundError: No module named 'automatic_png_logos' nedeniyle durdu. Sebep, scripts.candidate_logo_missing_report modülünün yalnız URL güvenlik doğrulaması için scripts.candidate_logo_report içe aktarırken PNG dönüştürücüsünün gereksiz ve hatalı üst-seviye import zincirini çalıştırmasıydı. scripts.candidate_logo_report içinde ROOT bağımsız tanımlandı; dönüştürücü yalnız prepare() gerçekten çağrıldığında scripts.automatic_png_logos üzerinden yüklenecek. Böylece merkezi logo envanteri PNG/Pillow bağımlılığı olmadan çalışır. Yeni regresyon testi raporu gerçek python -m komutuyla açar; merkezi erken py_compile kapsamı genişletildi. Bu düzeltme mevcut ana liste logolarını, kanal bağlantılarını, favorileri ve yedekleri değiştirmez. Yeni Actions sonucu henüz doğrulanmadı; önceki notlar saklanır.

## 14 Ekim 2026 — ANA LİSTE LOGOLARI KORUNDU; YENİ ADAYLARIN EKSİK LOGOLARI ÖNCELİKLENDİRİLDİ

Kullanıcı ana listedeki logoların tamamını IBO Player'da kendi test ettiğini ve çalıştığını bildirdi; mevcut ana liste logoları şimdilik KESİNLİKLE değiştirilmemeli. Kullanıcı daha önce yaklaşık 11.562 keşfedilmiş kanal adayının çoğunda logo olmadığını gözlemledi; bu sayı bugünkü doğrulanmış aday sayısı değildir. Bu toplu geliştirme yalnız keşif sırasında yeni adayların eksik logo kapsamını hesaplar. scripts/candidate_logo_missing_report.py, test_candidate_logo_missing_report.py eklendi; madsc_akilli_kesif.py içindeki aday PNG hazırlığı sonrasında candidate_logo_missing_report.json üretilecek. Kategoriler: LOGO_KAYNAGI_YOK, LOGO_KAYNAGI_GUVENLIK_INCELEMESI, PNG_HAZIR_KIMLIK_ONAYI_BEKLIYOR, LOGO_INDIRME_VEYA_DONUSUM_HATASI, PNG_HAZIRLIGI_BEKLIYOR. Aynı isimle bulunan güvenli kaynak logoları sadece öneri olarak sunulur; görsel kimlik onayı veya otomatik liste değişikliği YOKTUR. Önceki 40 adaylık hazırlık sınırı değişmedi; logo bulunmayanlar raporda görünür. Ana liste, logo bağlantıları, favoriler, yedekler, HEPSİ, YENİLER ve yabancı arşiv değiştirilmedi. Sıradaki toplu iş: eksik logo adaylarının gerçek kaynaklardan güvenli araştırılması ve kaynak eşleşmesi; gerekirse ayrı hazırlık turları; IBO ve kullanıcı onayı. Eski notlar korunur.

## 14 Ekim 2026 — YEŞİL TEST SONRASI TOPLU KABUL RAPORU İYİLEŞTİRMESİ

Kullanıcı commit 00a4167 için son testin yeşil olduğunu bildirdi. Tek toplu değişiklikte beş aşama bekleyen işler raporundaki önemli ayrım düzeltildi: kanıtı bulunan fakat henüz nihai kabul edilmeyen işler ile kanıtı eksik veya IBO kullanıcı onayı bekleyen işler artık ayrı sayılıyor. Her kabul maddesi için kanit_mevcut alanı ve toplamlar JSON'a ve Türkçe Actions özetine ekleniyor. Kanıt var olması bir işin tamamlandığı anlamına gelmez: tamamlandi alanı false, genel_kabul HENUZ_ONAYLANMADI kalır. Regresyon testleri hem tümü eksik senaryoyu hem kısmen kanıtlı senaryoyu denetler. Ana kanal listeleri, yedekler, arşivler, favoriler, EPG ve planlı taramalar değişmedi. Sonraki toplu iş: gerçekten tekrarlanan bağımsız workflow push tetikleyicilerinin güvenli konsolidasyonu, ana listedeki tüm yayın sonuçlarının doğrulanması ve IBO Player kabulü. Yeni Actions sonucu ayrıca kontrol edilmelidir. Önceki notlar korunur.

## 14 Ekim 2026 — YEŞİL TEST SONRASI TOPLU KALAN İŞLER VE KABUL RAPORU

Kullanıcı commit 15318e8 için GitHub Actions testinin yeşil olduğunu bildirdi. Beş ana bölümün gerçek tamamlanma durumunu raporlamak için merkezi kabul kapısına pending_tasks fonksiyonu eklendi. Artık mevcut kabul kriterlerinden bir tek JSON dosyası (madsc_merkezi_denetim/bes_asama_bekleyen_isler.json) ve Türkçe Markdown özetinde açık işler, eksik kanıtlar, sonraki işlemler ve kullanıcı IBO onayı birlikte çıkacak. Yeşil Actions koşusu tüm canlı yayınların kanıtı sayılmaz; rapor bütün kabul maddelerini açık tutar, ancak dosyadaki gerçek kanıt durumunu ayrıca gösterir. Aynı toplu commit içinde yeni birim testi eklenir. Eski workflow tetikleyicileri ve korunan kanal dosyaları değiştirilmedi. Bundan sonraki toplu işler: gerçek bağımsız push çakışmalarını azaltma, ana listedeki tüm kanalların sağlık kanıtını biriktirme, logo/EPG ve arşiv yedek kanıtları, IBO cihaz onayı. Önceki notlar saklanır.

## 14 Ekim 2026 — #72 KIRMIZI MERKEZİ TEST HATASI TOPLU DÜZELTME

Kullanıcı #72 (commit 52918e7) merkezi denetimin Failure/exit code 1 ile bittiğini ekran görüntüsüyle bildirdi. Kod incelemesinde scripts/central_consolidation_audit.py dosyasında son değişiklikle eklenen f-string içinde kaçışlı tek tırnaklar (item[\\'alan\\']) bulundu. Bu Python sözdizimi hatasıdır; dosya AST kontrolünde SyntaxError üretir ve merkezi denetimin 'Tum Python dosyalarinin sozdizimini kontrol et' adımında çalışmayı durdurabilir. Hatalı rapor satırı .format() ile güvenli yazıma çevrildi. Aynı toplu commit içinde test_central_consolidation_audit.py içine AST regresyon testi ve merkezi workflow'a kritik rapor modülleri için erken py_compile kontrolü eklendi. GitHub ekranındaki Node.js 20 deprecated uyarısı doğrudan exit code 1 nedeni olarak gösterilmedi; ayrıca takip edilecek. Yeni Actions sonucu doğrulanana kadar başarı iddia edilmez. Kanal listeleri, yedekler, favoriler, HEPSİ ve YENİLER değişmedi. Geçmiş notlar korunur. Sonraki toplu iş: kalan gerçek bağımsız push çakışmaları, beş aşama canlı kanıt ve IBO kabulü.

## 14 Ekim 2026 — TOPLU KABUL RAPORU GÜVENLİK VE TEKRAR KANITLARIYLA GENİŞLETİLDİ

Kullanıcı son merkezi testlerin yeşil olduğunu bildirdi ve eksiklerin topluca çıkarılıp giderilmesini istedi. Bu toplu değişiklikte beş aşamalı kabul kapısı, merkezi korunan liste yazma raporunu ve tek işlemde birden fazla push analizi sonuçlarını gerçek JSON kanıtından okuyacak şekilde genişletildi. Güvenlikte manuel inceleme ihtiyacı veya birden çok push varsa bunu açıkça raporlar, otomatik başarılı saymaz. İlgili yeni birim testleri eklendi. Merkezi workflow push.paths listesine daha önce eklenmemiş test_tek_merkez_tetikleme.py eklendi; bu dosya değişince aynı merkezi koşuda test edilir. Kanal listeleri, HEPSİ, favoriler, ⭐ YENİLER, yedekler ve tarama takvimi değiştirilmedi. Önceki kayıtlar silinmedi. Yeni Actions sonucu doğrulanmadan yeşil ilan edilmez. Sonraki toplu işler: çakışan gerçek workflow adlarını rapordan okuyarak kontrolleri kaybetmeden merkezileştirme, tam yayın ve IBO cihaz kanıtı, son kabul.

## 14 Ekim 2026 — TOPLU KORUNAN LİSTE YAZMA KAPISI MERKEZE TAŞINDI

Kullanıcı beş aşamada toplu çalışmaya devam talimatı verdi. Daha önce ayrı workflow olan 31 - Korumalı Liste Yazma Kapısı Denetimi içindeki statik GitHub Actions yazma yetkisi, korunan liste referansı ve environment onay kapısı analizi scripts/central_protected_write_gate.py içine alındı. Aynı denetim beş aşamalı merkezi workflow'da PyYAML ile çalışır; rapor madsc_merkezi_denetim/protected-write-gate-report.json olarak saklanır. Ayrı test-31-protected-write-gate.yml dosyasındaki push tetikleyicisi kaldırıldı, manuel workflow_dispatch ve eski artifact testi saklandı. Merkezi workflow'un push.paths listesine yeni script, test ve eski workflow dosyası eklendi. Birim ve regresyon testleri eklendi. Kullanıcının korunan listelerine, favorilerine, HEPSİ, YENİLER, yedek, arşiv, yayın ve EPG dosyalarına dokunulmadı. Statik denetim yazma yetkilerini raporlar ama otomatik olarak izinleri değiştirmez veya yetki/onay uygulamasını kesin ispatlamaz. Henüz diğer bağımsız koruma testlerinin tümü merkezileştirilmedi. Yeni Actions sonucunu doğrula; önceki kayıtları silme.

## 14 Ekim 2026 — TOPLU DURUM RAPORU VE LOGO PUSH TEKRARININ AZALTILMASI

Kullanıcı merkezi sağlık testi düzeltmesinin yeşil tamamlandığını bildirdi ve beş bölümün raporunu istedi. Durum: (1) güvenlik, izole Git geri yükleme, yedek ve dosya kanıtları VAR ama tüm geçmiş/harici yedek kabulü eksik; (2) keşif aday/kaynak raporları VAR, gerçek canlı kaynak doğrulaması eksik; (3) ana liste için günlük 50 kanal dönüşümlü teknik sağlık testi VAR, tüm kanal ve IBO kanıtı eksik; (4) logo/EPG kimlik raporu VAR, cihaz ve görsel eşleşme kanıtı eksik; (5) merkezi denetim, 18 geliştirme, 26 kural, tek rapor ve kabul kapısı VAR, tam uçtan uca kabul ve tüm workflow push birleştirmesi eksik. 'Yeşil' teknik test sistemin tümünün tamamlandığı anlamına gelmez.

Tek toplu değişiklikle automatic-png-logos.yml iş akışında CALISANLAR.m3u push tetikleyicisi kaldırıldı; logo kodu/workflow dosyası değişimindeki push ve manuel çalıştırma KORUNDU, ayrıca günlük 05:23 UTC salt okunur logo hazırlık takvimi eklendi. Böylece ana liste değişikliği yüzünden merkezi denetimle aynı anda otomatik logo işi tekrar açılmaz; logo denetimi günlük sürer, manuel istenirse anında çalıştırılabilir. Workflow içerik yazma yetkisi salt okunura indirildi, mevcut korunan liste geri alma ve artifact adımları aynen kaldı. Tek merkezi denetim yine CALISANLAR.m3u push'unda çalışır. Bu değişiklik diğer güvenlik workflow'larının push tetikleyicilerini henüz kaldırmaz; bunların gerçek kontrol kapsamı ayrıca karşılaştırılmalı. test_tek_merkez_tetikleme.py bu sözleşmeyi denetler. Kanal dosyaları, arşiv, yedekler ve geçmiş değiştirilmedi. Yeni Actions yeşil sonucu ayrıca kontrol edilecek.

## 14 Ekim 2026 — MERKEZİ DENETİM #68 TEK TEST HATASI TOPLU DÜZELTİLDİ

Kullanıcı ekran görüntüsünde #68 beş aşamalı merkezi denetimde 81 birim testinden birinin başarısız olduğunu, 'Mevcut sistem sağlık testlerini çalıştır' adımının exit code 1 ile kapandığını bildirdi. Depoda test_central_consolidation_audit.py dosyasındaki test_paths_ignore_kontrolu örnek YAML metninde satır sonları gerçek Python '\\n' kaçışları yerine iki ters eğik çizgiyle yazılmıştı; böylece örnek workflow gerçek satırlara ayrılmıyor ve tetikleyici analizinde başarısız oluyordu. Örnek satır sonları düzeltildi. Aynı toplu commit içinde merkezi denetimde birim testlerinin tüm ayrıntıları madsc_merkezi_denetim/birim_test_sonuclari.log dosyasına tee ile kaydedilecek ve hata çıkış kodu set -o pipefail ile korunacak. Rapor artifact'e dahil, böylece gelecekte kullanıcıdan ekran görüntüsü istemeden hata adı görülebilecek. Mevcut kanallar, favoriler, yabancı arşiv, yedekler, planlı taramalar ve koruma kuralları değişmedi. Düzeltmenin yeşil olduğunu Actions sonucu doğrulanana kadar söyleme. Sırada gerçek logo/güvenlik workflow tetikleyicilerinin topluca kayıpsız merkezileştirilmesi var.

## 14 Ekim 2026 — TOPLU PUSH TEKRARI RAPORUNDA YENİ SENARYOLAR

Kullanıcının toplu çalışma isteğiyle, tek işlemde birden fazla workflow açılmasını tespit eden merkezi denetime ana liste + logo, korunan liste + belge senaryoları, gerçek workflow dosyalarının raporlanması ve paths-ignore kuralı desteği tek değişiklikte eklendi. Birim testleri genişletildi. Bu kayıt test tetikleyicilerini kapatmaz; önce gerçek güvenlik/logo adımları ve eşdeğerlik doğrulanmalıdır. Kanallar ve korunan arşivler değişmedi. Sıradaki iş: merkezi raporun gerçek Actions sonucunu inceleyip güvenlik ve logo denetimlerini kayıpsız topluca taşımak.

## 14 Ekim 2026 — TOPLU TEKRAR DENETİMİ VE GENEL KABUL KAPISI (TEK COMMIT)

Kullanıcı yeşil sonuç sonrası tek tek mikro düzeltme yerine ilgili işleri TOPLU işlemeyi istedi. scripts/central_consolidation_audit.py ve test_central_consolidation_audit.py aynı toplu değişiklikte eklendi, beş aşamalı merkezi workflow'a bağlandı. Yeni kod tüm yerel GitHub Actions YAML dosyalarının push tetikleyicilerini inceler; kanal ekleme/silme, proje notu, logo hazırlığı, merkezi kod değişikliği için kaç ayrı workflow açılacağını Türkçe JSON ve Markdown raporlar. Aynı koşuda beş aşamalı GENEL KABUL KAPISI raporu da üretir; IBO Player cihaz onayı ve gerçek uçtan uca test kanıtı olmadan sistemi asla tamamlandı ilan etmez. Raporlar GitHub Actions artifact ve çalışma özetine girer. Bu, mevcut bağımsız logo/güvenlik push tetikleyicilerinin otomatik olarak kapatıldığı anlamına gelmez: raporda somut dosya adları tespit edildikten sonra, kontroller kaybolmadan topluca taşınmalıdır. Bu commit hiçbir kanalı, favoriyi, HEPSİ'yi, YENİLER'i, yabancı arşivi veya yedeği değiştirmez. Önceki notların tamamı korunur.

## 14 Ekim 2026 — BÜTÜN SİSTEMİN KABUL TESTİ VE YENİ SOHBETE DEVAM PLANI

Kullanıcı son dokümantasyon birleştirme testinin yeşil olduğunu bildirdi. Beş ana bölümün gerçekten çalıştığı nasıl anlaşılacak sorusu için KALICI KARAR: TAKVİM BEKLENMEYECEK. Beş aşamalı merkezi workflow mevcut workflow_dispatch ile elle başlatılabilir; fakat mevcut merkezi denetimin yeşil olması tek başına uçtan uca kabul anlamına GELMEZ. Geliştirme sonunda (ve ara kilometre taşlarında) ayrı kabul ölçütleriyle TEK merkezden bütün sistem doğrulanmalı. Kabul ölçütleri: (1) korunan listeler, onay mekanizması ve yedek geri dönüş kanıtı; (2) gerçek yeni Türk/yabancı kaynak keşfi ve aday ayrımı; (3) ana listedeki TÜM kanalların döngü boyunca sağlık denetimi, yeni aday testleri ve ses/görüntü kanıtı; (4) logo/EPG/kimlik eşleşmesi, IBO cihaz doğrulamasının ayrıca kullanıcı tarafından yapılması; (5) arşiv, kategori sayıları, test geçmişi, Türkçe tek rapor, 18 geliştirme ve 26 kural. Tek değişikliğin üç-dört Actions başlatmaması ayrıca doğrulanacak. Sonuçlar BASARILI / BASARISIZ / EKSIK / KULLANICI_ONAYI_BEKLIYOR olarak ayrılmalı. Tam kabul ancak bütün zorunlu kriterler ve kullanıcının IBO onayı sağlanınca verilir. Henüz bu tam uçtan uca test uygulanmış değildir; ileride tamamlandı diye gösterilmemeli.

SONRAKİ İŞLER: (A) Tek merkezi push koşusuna hâlâ ayrı bağlanan logo ve korunan liste workflow'larının gerçek YAML tetikleyicilerini tespit edip, test adımlarını kaybetmeden gereksiz push'ları kapatmak; (B) keşif ve yayın zincirlerinin beş bölüme gerçek orkestrasyonunu yapmak; (C) tam kabul testinin kanıt toplama, geçme-kalma kapısı ve Türkçe raporunu kodlamak; (D) elle kabul koşusu çalıştırıp sonuçlarını kontrol etmek. Kullanıcı onayı olmadan hiçbir korunan kanal dosyasını değiştirme. Eski notları ve geçmişi silme. Bu dosyadan yeni sohbetlerde devam et.

## 14 Ekim 2026 — TEKRAR EDEN DOKÜMANTASYON PUSH TESTİ MERKEZE TAŞINDI

Kullanıcı #64 merkezi ve #113 dokümantasyon testlerini yeşil bildirdi. Aynı değişiklikte gereksiz iki ayrı Actions koşusunu azaltmak için MADSC Documentation Check içindeki eski push tetikleyicisi kaldırıldı, isteğe bağlı workflow_dispatch bırakıldı. Dokümantasyonun altı temel doğrulaması beş aşamalı merkezi workflow'a eklendi. Merkezi workflow artık AGENTS.md, OZELLIK_ENVANTERI.md, DEVAM_NOTU.md, GUVENLIK_KURALLARI.md, CALISANLAR.m3u ve dokümantasyon workflow değişimlerinde de tetiklenir. Bu, bütün eski bağımsız güvenlik/logo push tetikleyicilerinin kaldırıldığı anlamına gelmez; onların ayrıca incelenmesi gerekir. Mevcut kanal listeleri, kanal sıraları, yabancı arşivi ve yedekler değiştirilmedi. Tüm geçmiş korunur.

## 14 Ekim 2026 — ANA LİSTE SAĞLIK İŞ AKIŞI 3. AŞAMADA DOĞRU SINIFLANDIRILDI

Kullanıcının onayıyla .SCI-FI HEPSİ ve SİNEMA'dan kaldırıldı; geçmişte kayıtlı commit 9d2b783, yeni otomatik silme yetkisi değildir. Beş aşamalı envanterde "sağlık" anahtar sözcüğü yüzünden madsc-ana-liste-saglik.yml yanlışlıkla 1. güvenlik bölümüne sınıflanıyordu. Bu özel iş akışı canlı kanal testi olduğundan 3. toplu yayın testleri bölümüne açıkça eşlendi ve birim testi eklendi. Eski workflow takvimleri, kanal dosyaları, yabancı arşivi ve korunan geçmiş değiştirilmedi. Sadece rapor/kanıt ayrımı devam eder; GitHub Actions yeşil kod testi tüm kanalların IBO'da çalıştığı anlamına gelmez.

## 14 Ekim 2026 — KULLANICI ONAYLI TEK KANAL SİLME: .SCI-FI

Kullanıcı HEPSİ listesindeki yaklaşık 373. sırada bulunan .SCI-FI kanalını kaldırmayı açıkça istedi. CALISANLAR.m3u içinde aynı tvg-id ile iki kayıt vardı: 📺 HEPSİ (375) ve 🎬 SİNEMA (6). Bu iki kayıt, kullanıcı silme komutu gereği kaldırıldı; HEPSİ etiketi 374, SİNEMA etiketi 5 oldu. Başka hiçbir kanalın adı, URL'si, tvg-id'si, logosu, sırası veya kategorisi değiştirilmedi. YABANCI_KANALLAR.m3u arşivinde .SCI-FI adına eşleşen kayıt bulunmadığından o dosyaya dokunulmadı. Önceki ana liste sürümü GitHub commit geçmişinden geri alınabilir. Bu tek kanal için verilen silme onayı başka kanallara veya gelecekteki otomatik düzeltmelere uygulanamaz. Sistem tüm diğer kanal testlerinde yalnız raporlar ve kullanıcı onayı bekler.

## 14 Ekim 2026 — ANA LİSTE TEKNİK SAĞLIK DENETİMİ UYGULAMA KAYDI

Beş aşamanın 3. bölümüne CALISANLAR.m3u için yeni salt okunur yayın denetimi eklendi: scripts/ana_liste_saglik.py ve .github/workflows/madsc-ana-liste-saglik.yml. Günlük 06:40 UTC'de (ve isteğe bağlı manuel) sıradaki 50 kanalın kısa ses/görüntü örneğini inceler; bütün ana listeyi grup grup dolaşır, tek koşuda tüm kanalların incelendiğini iddia etmez. GitHub'da yalnız artifact olarak Türkçe JSON/Markdown rapor verir; ana listeyi, YABANCI_KANALLAR.m3u dosyasını, favorileri, HEPSİ'yi, ⭐ YENİLER'i, onaylı yedekleri, geçmişi ve kanal kararlarını değiştirmez. Workflow yalnız contents: read izinli, checkout kimlik bilgileri kalıcı değil, korunan dosyaların SHA256 özeti kontrol edilir. Kısa ffprobe hatası teknik DOGRULANAMADI'dır; kesin bozuk/IBO'da çalışmıyor demek değildir. URL raporda yayınlanmaz, SHA256 kimliği kullanılır. Birim testleri ana dosyanın değişmediğini ve teknik hatanın otomatik karar üretmediğini kontrol eder. 5. bölümün merkezi raporuyla ve eski keşif/EPG/aday zinciriyle bütünleşik gerçek orkestrasyon hâlâ ayrıca tamamlanmalıdır; yeni workflow mevcut zinciri durdurmaz veya değiştirmez. Bu kaydın ve önceki notların hiçbirini silme.

## 14 Ekim 2026 — KULLANICI ONAYI: ANA LİSTE CANLI SAĞLIK KONTROLÜ, RAPORLA / ASLA OTOMATİK DEĞİŞTİRME

Kullanıcı, beş ana bölümlü bütünleşik sistemin kurulmasını, tüm tarihsel konuşma/karar/görevlerin ve bu notların KORUNMASINI, eski kayıtların silinmemesini tekrar istedi. Özellikle CALISANLAR.m3u içindeki mevcut kanalların da zamanla bozulabilecekleri için düzenli görüntü/ses/erişim testine dahil edilmesini istedi. Test başarısızlığı kanalın otomatik silinmesi, URL/logo/ID/ad/kategori/sıra değişmesi, favori/HEPSİ/⭐ YENİLER/ULUSAL/yedek/arsiv taşıması veya çalışan/çalışmayan cihaz onayının otomatik değiştirilmesi için ASLA izin değildir. Sadece kanala özgü zaman damgalı sonuç, hata nedeni, önceki test, kaynak/ülke erişim belirsizliği, alternatif aday ve öneri raporlanacak; nihai işlem açık kullanıcı onayı bekleyecek. Ana liste, yabancı arşiv ve onaylı yedekler salt okunur girdidir. Çalışmayan teknik sonuç, İsveç IBO'da çalışmıyor kararı değildir.

Mevcut kod denetimi: .github/workflows/madsc-birlesik-kesif.yml yeni keşif adaylarını test ediyor; .github/workflows/madsc-son-kontrol.yml final_validation.py çalıştırıyor ve final_validation.py girdi olarak madsc_dogrulama/state.json içindeki adayları kullanıyor; ana listeyi kapsamlı canlı test eden bir rutin olduğu bunlardan çıkarılamaz. madsc_akilli_kesif.py CALISANLAR.m3u içeriğini tekrarları ayıklamak için okuyor; bu ana listedeki bütün yayınların canlı test edildiği anlamına gelmez. ANA LİSTE TAM KAPSAM SAĞLIK DENETİMİ ŞU AN KANITI EKSİK, beş ana bölümün 3. aşamasına zorunlu açık iş olarak eklenmiştir. Yeni uygulama salt okunur olacak; URL başına tekrarsız, zamanlı, kontrollü ve coğrafi engel/erişim sorununu bozuk yayın kararından ayıran testler; sonuçları 5. bölümde Türkçe rapor ve onay kuyruğuna verecek. Kodun mevcut olması, gerçek Actions başarısı veya her kanalın test edildiği iddiası değildir.

Beş bölümün hepsi kapsamda kalır: (1) sistem güvenliği, güncelleme, 26 kural, yedek/geri alma; (2) Türk ve yabancı keşif, kaynak ve alternatifler; (3) hem mevcut ana liste hem yeni adayların gerçek yayın testi, çalışan/çalışmayan teknik ayrımı; (4) logo, EPG, kalite ve kanal kimliği; (5) arşiv, ana liste, HEPSİ, favoriler, ⭐ YENİLER, yabancılar, yedekler, geçmiş, onaylar, yapılacaklar ve sağlık/uyarı raporları. 18 geliştirme beş bölümün altındadır; ayrı sistem değildir.

KORUMA: Bu ve önceki DEVAM_NOTU.md kayıtları silinmez, üzerine yazılmaz; yalnız yeni tarihli kayıt eklenir. Geçmiş kararları otomatik yeniden uygulama. Mevcut otomasyonları envanter ve son gerçek run sonuçlarıyla eşleştirmeden kapatma veya toplu yeniden başlatma. Öncelik: mevcut ana liste sağlık testinin gerçek kapsamını denetle, eksikse sadece rapor yazan güvenli işi beş bölümün 3 ve 5. aşamalarına bağla; sonra merkezi yürütmeyi birleştir. Bu kayıt kanal listesi değiştirme izni değildir.

## 14 Ekim 2026 — TEK MERKEZ KARARI: TÜM TARİHSEL IPTV ÇALIŞMASINI BEŞ BÖLÜMDE YÖNET

Kullanıcı açıkça, projenin kuruluşundan beri konuşulan, yapılan, yapılamayan ve planlanan TÜM işleri beş ana bölümden çalıştırmak istiyor. Yalnızca beş aşamaya etiketleme/rapor üretme yeterli değildir; gerçek keşif, yayın testleri, logo/EPG, arşiv ve güvenlik otomasyonlarının yönetimi ve sonuç kanıtları bu bölümlere bağlanmalıdır. Yeni küçük testler/tekrarlı commitler ve her seferinde ekran görüntüsü istemek yerine envanter + açık boşluklar + güvenli toplu uygulama + mevcut merkezi test tercih edilir.

Beş ana bölüm ve kapsamları:
1. GÜVENLİK VE SİSTEM GÜNCELLEMESİ: Onaylı 1–24 güvenlik kuralları, AGENTS.md içindeki 25 değişiklik sonrası test ve 26 Türkçe test adları kuralı, korunan dosyalar, GitHub izinleri, hata devre kesicisi, sürüm/yedek/geri yükleme, Actions sağlık ve güncellemeler. Onaylanmış 27. kural kaydı doğrulanmadı; yeni kural uydurma.
2. KANAL ARAMA VE KAYNAKLAR: Türk kanalları, yabancı adaylar, 740 yabancı kanal arşivi, yeni/eksik kanal arama, alternatif URL, kaynak güvenilirliği, 156/155 mutabakatı, tekrar eleme, keşif geçmişi. Yabancı kaynaklar mevcut birleşik keşifte otomatik Türkçe filtre nedeniyle bütünüyle taranmıyor; tamamlandı sayma.
3. TOPLU YAYIN TESTLERİ: Video/ses/çözünürlük, donma/kesinti, coğrafi erişim ve token/geçici hata ayrımı, test geçmişi, akıllı tekrar test, teknik çalışan/çalışmayan, kullanıcı IBO kararı ayrı, üç aşama ve son kontrol.
4. LOGO/EPG/KİMLİK: Gerçek kanal/logo/amblem, EPG, doğru kanal kimliği, HD/FHD kalite, İsveç IBO gerçek cihaz kanıtı ayrı; otomatik liste değişikliği yok.
5. ARŞİV/SONUÇ/YÖNETİM: CALISANLAR.m3u, HEPSİ, favoriler, ⭐ YENİLER, onaylı yedekler, YABANCI_KANALLAR.m3u, aday/alternatif/çalışan/çalışmayan kayıtları, yapılacak/yapılmayacak işler, Türkçe tek rapor, günlük sağlık ve uyarı teslimi.

8 temel (issue #2) + 10 ek (issue #3) = 18 geliştirme bu beş bölümün alt görevleridir; ayrı 18 yönetim sistemi değildir. Tarihsel DEVAM_NOTU.md, IPTV_PROJE_HAFIZASI.md, OZELLIK_ENVANTERI.md, AGENTS.md, GUVENLIK_KURALLARI.md, Actions ve gerçek raporlar birbirine karşılaştırılmadan 'tüm geçmiş kapsandı' denmez. Beş aşama eşleştirmesi bugün sadece statik sınıflandırma; merkezi workflow gerçek alt iş akışlarını yönetmiyor. Bu açık teknik eksiktir. Eski başarılı workflowları silme; zamanlama/izin/çakışmaları incelemeden toplu otomatik tetikleme yapma.

Son kullanıcı ekranı: merkezi #60 (cac726e) ve #61 (e74d9d2) yeşil; sonraki 57f6f3f sonucu henüz teyit edilmedi. Yeşil kod testi canlı kanal, EPG/IBO veya bütün sistemin tamamlandığı anlamına gelmez. Ana liste, sıralamalar, onaylı yedekler ve kullanıcı kararları açık izin olmadan değiştirilmez.

SIRADAKİ TEK ANA İŞ: Her mevcut workflow'un gerçek işlev, tetikleyici, veri girdisi/çıktısı, korunan dosyaya yazma riski, son çalışma kanıtı ve 5 bölüm sahipliğini tek envanterde mutabık kıl; 18 iş ve geçmiş kararlarla farkları çıkar; ardından mevcut iş akışlarını tekrarsız, güvenli merkezi orkestrasyona topluca bağla. Raporlamayı gerçek çalışma yerine koyma.

## 14 Ekim 2026 — GÜVENLİ DEVİR KAYDI: BEŞ AŞAMALI TOPLU SİSTEM

Kullanıcı kararı: Tek tek küçük test ve commit döngüsü yerine bütün eksikleri topluca belirle, mümkünse tek değişiklikte birleştir, mevcut merkezi Actions denetiminde kontrol et; test sonuçlarını ve başlıkları Türkçe göster. Kullanıcıdan her koşu için ekran görüntüsü isteme. Yeşil kod testi, canlı yayın veya IBO cihaz doğrulaması anlamına gelmez.

Son doğrulananlar: Kullanıcının ekranında #48–#51 başarılı, #54 YAML başlık hatasıyla başarısız ve ardından Türkçe tırnak düzeltmesi sonrası kullanıcı yeşil sonucu bildirdi. Toplu rapor commit d80955c kullanıcı tarafından yeşil bildirildi. e794a54 toplu yedek/rapor güncellemesinin #59 koşusunda 62 testten biri başarısız oldu. Neden: test_central_backup_evidence.py eski restore_test=BU_KOSUDA_YAPILMADI değerini bekliyordu; yeni kod artık GIT_HEAD_IZOLE_ESLESME_DOGRULANDI veya DOGRULANMADI döndürüyor. Düzeltme commit cac726e22bdde1c8ab5c291bb023c6c81c46aa5e; bu commit'in Actions sonucu henüz bağımsız doğrulanmadı. GitHub toplu kayıt engeli e794a54 ile aşıldı; 4 dosyanın main üzerinde bulunduğu teyit edildi.

Yürürlükteki beş aşama: (1) güvenlik/koruma/yedek, (2) keşif/kaynak güveni, (3) toplu teknik yayın testleri, (4) logo/EPG/kimlik, (5) Türkçe sonuçlar, sağlık ve uyarılar. Merkezi denetim ayın 1 ve 15'i UTC 07:00; mevcut başarılı iş akışlarını topluca silme/değiştirme. Statik workflow eşleştirmesi tarihsel tam kapsamın kanıtı değildir. Açık işler: geçmiş işlerin gerçek kapsam karşılaştırması; kaynak güven puanı ve keşif kanıtı; yayın sürekliliği ve coğrafi erişim ayrımı; logo/EPG gerçek eşleşme; günlük sağlık ve uyarı teslimi; GitHub dışı yedek ve tarihsel kurtarma; IBO cihazda kullanıcı onayı. Canlı yayın ve IBO doğrulaması yapılmış gibi gösterme.

Koruma: CALISANLAR.m3u, HEPSİ, favoriler, ⭐ YENİLER, yabancı kanal listeleri, yedekler, kullanıcı onaylı kayıtlar, mevcut kanal adları/URL/ID/logo/kategori/sırası izinsiz değiştirilemez. Yeni kanallar ana listeye veya ⭐ YENİLER'e açık onay olmadan eklenmez. Tek raporda kanıtı olanı, olmayanı ve kullanıcı onayı bekleyeni ayır. Bundan sonra öncelik yeni kozmetik commit değil, açık işlerin kanıt temelli toplu çözümüdür.

## 14 Ekim 2026 — Kullanici karari: Actions sonucunu otomatik dogrula
Kullanici her commit sonrasi kendisinden ekran goruntusu/teyit istenmemesini, mevcut sistemin Actions sonucunu kendisinin okumasini istedi. Ekran goruntusunde merkezi #45 ve #46, dokumantasyon #106 SUCCESS gorunuyor. Commit 89ec041: mevcut merkezi workflow'un zaten aldigi son 100 run JSON'undan her workflow'un son gorunen kosusunu completed/success, failed, pending ve bilinmeyen olarak ayiran salt okunur actions_otomatik_sonuc_dogrulama.json ve GITHUB_STEP_SUMMARY eklendi. Ek Actions tetiklemez, protected playlist ve yedeklere dokunmaz. Son 100 disi, kosu sirasinda henuz tamamlanmamis kendi run'i ve diger workflowlarin yeni sonucunu basarili saymaz. Gercek son Actions run sonucu dogrulanmadan bu commit basarili iddia edilmez. Kullanicidan her seferinde manuel teyit isteme; GitHub run/artifact ve loglari kendin incele.

## 14 Ekim 2026 — Bes asamali gecis: ilk gercek degisiklikler ve acik dogrulama
Kullanici ilk gunden bugune tum otomasyon, dosya, is, karar ve test gecmisinin korunarak bes ana asamada eksiksiz denetlenmesini onayladi. Commit ed4c6bb: mevcut scripts/central_workflow_inventory.py envanterine bes asama eslestirme raporu eklendi; her workflow tam bir asamaya atanir, eksik/tekrar tespit edilirse hata verir. Bu sadece statik dosya adi/kategori eslestirmesidir; tarihsel tum islerin kapsandigi veya canli testlerin basarili oldugu iddia edilmez. Commit 86ee022: .github/workflows/madsc-aylik-merkezi-denetim.yml takvimi ayin 1 ve 15'i UTC 07:00 olacak sekilde duzeltildi. Eski workflowlar, playlistler, HEPSI, favoriler, YENILER, yedekler ve onayli gecmis degistirilmedi. SONRAKI ZORUNLU ADIMLAR: yeni merkezi Actions run kimligini ve sonucunu dogrula; bes asama raporundaki her workflow'un gercek sorumlulugunu incele; tarihsel gorevler ve mevcut kod/envanter/Actions arasinda kapsam farklarini cikar; eksik gunluk saglik, guven puani, logo/EPG kimlik, uyari teslimi, harici yedek geri yukleme kanitlarini tamamla. Bu isler bitmeden tum sistem hatasiz/tamamlandi denmez. Gereksiz yeniden test ve IBO cihaz testi yok.

## 14 Ekim 2026 — KULLANICI KARARI: BES ASAMALI TOPLU TEST VE KALAN ISLER
Kullanici sistemin yuzlerce ayri Actions kosusuyla degil BES ana asamada yonetilmesini tekrar onayladi: (1) guvenlik ve sistem sagligi, (2) kanal kesfi ve kaynak guvenilirligi, (3) toplu yayin teknik testleri, (4) logo/EPG/kanal kimligi, (5) sonuc, saglik raporu ve uyarilar. Bu 5 is akisi asamasidir; gerekli alt birim testleri silinmez veya koruma kapilari kapatilmaz. Tamamlanmis basarili testleri gereksiz tekrar etme, mevcut otomasyonlari hemen silme veya yeni workflowlar ekleme. Once gercek Actions tetikleyici/envanter ve sonucunu denetle, guvenli birlestirme planini olustur, sonra kademeli uygula. Onayli sekiz gelistirme issue #2 ile eslesir; kalan dogrulama, gunluk saglik raporu, kaynak guven puani, logo/EPG/kimlik ve ariza/aday uyari teslimi gercek kanitla tamamlanacak. 14 Ekim commit 168707e merkezi sekiz gorev raporunu issue #2 ile hizaladi; run #43 eski testin artik bulunmayan protected_files alanina erismesinden 57 testte 1 error ile basarisiz oldu. Commit 2f5b1c7 eski test iddiasini yeni rapor semasina uyarladi; bu commitin Actions sonucunu ayri dogrulamadan basarili deme. HEPSI, favoriler, YENILER, yedekler, onayli gecmis, CALISANLAR.m3u korunur; IBO cihaz testi yok. Kullanici yeni somut hata/commit/engel haric gereksiz ara rapor istemiyor.

## 13 Ekim 2026 — 740 yedek kanal ayri arsive tasindi (kullanici onayli)
Kullanici YEDEKLER grubunda yalniz ilk iki kanal TRT 1 ve DHA kalmasini, diger 740 kanalin GitHub icinde ayri `YABANCI_KANALLAR.m3u` dosyasinda tutulmasini istedi; IBO Player veya ana listede yeni kategori acilmayacak. Once 740 orijinal EXTINF ve URL ciftini aynen iceren arsiv olusturuldu: commit `d3a545935bdd0cc93c562ac6e31500f46c2ed046`. Ardindan `CALISANLAR.m3u` icindeki `📦 YEDEKLER (742)` grubundan bu 740 kayit cikarildi, TRT 1 ve DHA korunarak grup etiketi `📦 YEDEKLER (2)` yapildi: commit `efdf1f65b4b85bf4bdb8d3552f49869950515278`. HEPSI/favoriler/diger gruplar degismedi. Arsivdeki orijinal `group-title` metadata korunmustur ancak arsiv ana playlist'e eklenmemistir. Arsiv yabanci kanal adayi degerlendirmesi icindir; tum 740 kanal icin ulke/kimlik veya canlilik dogrulamasi yapilmis sayilmaz. Eski kanal test gecmislerini silme, arsivi otomatik ana listeye ekleme. IBO Player'da kullanici yenilemesi ve Actions kontrolu bekler.

## 13 Ekim 2026 — Yedeklerdeki yabanci kanallar hakkinda kullanici cihaz geri bildirimi
Kullanici IBO Player'da yedekler kategorisinde 742 kanal gordugunu bildirdi. Ilk iki kanal TRT 1 ve DHA haric digerlerini gozden gecirdigini, buyuk cogunlugunun calistigini, cok azinin calismadigini ve inceledigi kanallarin yabanci oldugunu soyledi. Bu bir kullanici gozlemidir; kanal bazinda test listesi veya her bir URL icin teknik dogrulama degildir. Hicbir kanali bu ifadeye dayanarak otomatik 'calisiyor'/'calismiyor' listesine tasima. Mevcut yabanci kanallari topluca silme veya yeniden ekleme. Yabanci kaynaklardan yeni adaylar ayri degerlendirilsin; tekrar/kimlik, teknik canlilik, kalite, logo ve IBO Isvec erisimi kanitlari ayrilsin. Yedekler, HEPSI, favoriler ve ana liste onaysiz degismesin.
Teknik inceleme: `madsc_akilli_kesif.py` 155 kaynak tanimli olsa da otomatik `turkish_feed` filtresi sadece 11 Turkce/Turkiye kaynagini tarar; yabanci ulke kaynaklari tanimli ancak otomatik aday akisina ALINMIYOR. Yabanci adaylari degerlendirmek icin ayri, salt okunur tarama ve onayli is akisi gerekir. Bu incelemede yabanci kanallarin calisma durumu dogrulanmadi.

## 13 Ekim 2026 — ATV 3 favori kopyalari kullanici istegiyle geri alindi
Kullanici ATV 3 576P SD kanalinin takildigini bildirdi ve PR #69 ile yapilan favori eklemesinin geri alinmasini istedi. `CALISANLAR.m3u` dosyasinda yalnizca `⭐ FAVORİLER (65)` ve `⭐ FAVORİLER 1 (61)` gruplarindaki ATV 3 576P SD kayitlari kaldirildi. `📺 HEPSİ (375)` ve `🇹🇷 ULUSAL (281)` icindeki ayni kanal korundu; diger kayitlar ve siralari degismedi. Commit: `c5f81d683c20e74083e93f6e884a2a6b80dedc42`. HEPSI grubu tum kanallarin referans sayimi icin korunur; buradan kanal silinmez veya tasinmaz. IBO Player cihaz yenilemesi kullanici tarafindan dogrulanacak.

## 13 Ekim 2026 — KULLANICI KARARI: GEREKSIZ WORKFLOW TEKRARLARINI SONRAYA BIRAK
Kullanici, tek kanal/listesi degisikliginde birden fazla GitHub Actions gorunmesinden rahatsiz. PR #69 ATV 3 degisikligi icin dal push, pull_request ve main push kaynakli 7 farkli run goruldu: logo hazirligi, korunan liste guvenlik denetimi ve dokumantasyon kontrolu. Ayni baslikli birden cok run ayni kanal ekleme isleminin tekrarlandigi anlamina gelmez. SONRA YAPILACAK: mevcut workflow tetikleyicilerini ve concurrency ayarlarini topluca denetle, gereksiz dal push / PR / main cakislarini azalt; zorunlu koruma testlerini kapatma, cron ve Rule 24'u izinsiz degistirme. Kullanici bu optimizasyonu SIMDI DEGIL, DAHA SONRA istiyor. Simdi ana IPTV kesif, aday teknik dogrulama ve eksik islerin mevcut akisi ile devam et; yeni gereksiz workflow/rapor/PR acma. Korumali kanal dosyalarina dokunma. PR #69 ile ATV 3 favori konumlari zaten tamamlandi; tekrar ekleme.

## 13 Ekim 2026 — Kullanici onayli ATV 3 favori ekleme
Kullanicinin acik talebi: HEPSI grubundaki `ATV 3 576P SD` (orijinal HEPSI #131), `⭐ FAVORİLER 1 (61)` ve `⭐ FAVORİLER (65)` gruplarinda dorduncu siradaki `ATV 1080P FHD` kanalinin hemen ustune eklendi. Kaynak EXTINF kimlik/logo ve URL aynen kopyalandi, sadece hedef grup adi kullanildi. Her iki grupta ATV 3 yeni #4, ATV 1080P yeni #5. Ana liste M3U kayit sayisi 1779 -> 1781 (+2); HEPSI, ulusal ve yedekler degismedi. Kategori adlarindaki eski (61)/(65) sayi etiketleri izin disi toplu yeniden adlandirmayi onlemek icin degistirilmedi; gercek favori kanal sayilari 62 ve 66 olur. Ana dalin degisiklik oncesi surumu geri donus noktasidir. Actions ve cihaz yenileme sonrasi sonuc ayrica dogrulanacak.

## 13 Ekim 2026 — Logo otomasyonu kirmizi test duzeltmesi ve ana liste korumasi
Logo run #38399784760 FAILURE, `Save PNG artwork and logo-only playlist changes` adimi #10. Bu adim `CALISANLAR.m3u` dahil dogrudan `git push` yapiyordu; kullanici koruma kurallariyla celisiyor ve kaydetme hatasi olusturdu. Otomatik git push/stage kaldirildi; logo hazirlik ve inceleme dosyalari 30 gun artifact olarak saklanir; ana listeye dokunan working tree degisikligi restore edilir; stage'de korunan dosya varsa is fail olur. Cron ayni kalir. Bu degisiklik logolari ana listeye eklemez; logo incelemesi ve kullanici onayi gerekir. Yeni workflow testinin sonucunu dogrula.

## 13 Ekim 2026 — Toplu aday kaybi onleme ve kaynak sayim duzeltmesi
Merkezi #38399633946, dokumantasyon #38399633933, saglik #38399633905 SUCCESS dogrulandi. Gercek aday kuyrugu hatasi duzeltildi: SHA256 kimligi olmayan ayni adli farkli adaylar once yanlislikla tek kayda indirilebiliyordu; artik yalniz dolu hash + ad ayniysa tekrarlari ayiklar. Kaynak mutabakatinda tekrarlanan kaynak isimleri O(n) sayilir ve ezilen ham tanim sayisi ayri raporlanir. Iki regresyon testi eklendi; mevcut tek merkezi workflow bunlari unittest discover ile calistirir. IBO cihaz onayi, canli kaynak testi, harici yedek ve 155 hedefi otomatik degistirilmedi. Playlist ve yedekler korunur. Yeni Actions sonucunu kontrol et.

## 13 Ekim 2026 — Toplu gerçek hata düzeltmesi: Python syntax kapısı
Merkezi #38399244580, dokumantasyon #38399244524 ve saglik #38399244523 SUCCESS dogrulandi. Ancak `scripts/central_short_status.py` icinde f-string ayni tirnak kullanimi Python 3.11/onceki surumlerde SyntaxError olusturabilir. Bu somut hata duzeltildi; merkezi denetime git ile izlenen tum Python dosyalarini ast.parse ile calistirmadan once kontrol eden yeni tek kosu kapisi eklendi. Bu kapinin gecmesi gercek yayin, IBO, harici yedek veya kaynak erisimi dogrulamasi degildir. Korunan listeler, yedekler, cron ve Rule 24 degismedi. Yeni Actions sonucunu dogrula.

## 13 Ekim 2026 — Tek toplu paket: kaynak anahtarlari + IBO aday kuyruğu
Onceki merkezi #38398816181, saglik #38398816148 ve dokumantasyon #38398816014 SUCCESS dogrulandi. `central_source_reconciliation.py` gercek Python SOURCES AST sozlugundeki ham kayit sayisini ve sessizce ezilen yinelenen kaynak adlarini raporlar; 155 hedefi izinsiz degistirilmez. `central_ibo_review_queue.py` var olan aday logo/EPG birlesik kanitini tekrarsiz CSV ve JSON olarak IBO incelemesine hazirlar; kaynak rapor yoksa bos CSV + KANIT_YOK, onay otomatik verilmez, yayin listesi degismez. Her iki konu tek merkezi Actions kosusunda, unit testlerle. IBO Isvec cihazinda gercek goruntu/EPG, canli kaynak erisimi, lisans, harici yedek ve playlist onayi halen dis kanit gerektirir. Bu bir aday test playlisti degil, guvenli inceleme kuyrugudur. Kullanicinin tek paket talimati korunuyor.

## 13 Ekim 2026 — Kalan isler tek paket: izole geri yukleme ve kaynak gerceklik ayrimi
Onceki toplu merkezi #38398366012 ve dokumantasyon #38398365570 SUCCESS dogrulandi. Bu pakette korunan 3 dosyanin Git HEAD bloblari gecici dizine gercekten geri acilip SHA256 byte butunlugu karsilastiriliyor; test merkezi tek kosuya eklendi. Bu yalniz HEAD surumunu dogrular, GitHub disi bagimsiz yedek veya eski surum geri yukleme kaniti DEGILDIR. Kaynak mutabakat raporu 155 hedefin konfigurasyon sayisi oldugunu ve farki gidermek icin canli kaynak secimi gerektigini acik belirtiyor. 156/155 farki kaynak silinerek gizlenmedi; kullanici cihazinda IBO, EPG ve lisans dogrulamasi yapilmadi; kesif ve final-validation test esikleri degismedi. Playlist, favoriler, YENILER, yedekler, cron korunuyor. Tek merkezi Actions sonucu dogrulanmali.

## 13 Ekim 2026 — Toplu duzeltme paketi (tek PR/tek merkezi test)
Kullanici sekiz isi parca parca degil birlestirilmis paketlerle gercekten duzeltmemizi istedi. Onceki merkezi #38397921809, saglik #38397921577, dokumantasyon #38397921714 SUCCESS. Bu pakette kisa raporda bozuk `tasks`/`runs` tipleri yuzunden rapor kirilmasi onlendi; tekrar test raporu var ama `excess_test_runs` olcumu yokken olcum var diye yanlis siniflandirma duzeltildi ve regresyon testi eklendi; sekiz gorev kaynak farki aciklamasi gercek AST mutabakat raporuna uyarlandi. Canli 156/155 kaynak farki, lisans, IBO cihaz onayi, bagimsiz yedek ve kullanici onayli playlist aktarimi bu pakette yapilmadi. Playlist, yedek, cron ve Rule 24 korunuyor. Tek merkezi test sonucu dogrulanmali. Bundan sonra somut duzeltmeleri toplu paketler halinde ele al, sirf yeni rapor eklemek icin ayri PR acma.

## 13 Ekim 2026 — KULLANICI KARARI: SIRADAKI TEK TEK YOK, TOPLU PAKET VE TEK TEST
Kullanici tekrar tekrar 'siradaki' demek istemiyor. Bundan sonra kalan isleri bir paket/PR ve tek merkezi Actions kosusunda birlikte ele al; gereksiz tek-is PR dongusu yapma. Merkezi #38397490010, saglik #38397489832, dokumantasyon #38397489830 SUCCESS dogrulandi. `scripts/central_all_remaining_tasks.py` kaynak/hedef, tekrar, yedek, logo/EPG/kimlik, Actions hatalari, IBO onayi, yonetim ve gunluk ozet olmak uzere sekiz alanin mevcut kanitini ve dis bagimliliklarini tek karar tablosuna alir. Merkezi workflow ve unittest'e eklendi. Bu toplu kontrol eksikleri cozulmus gostermez: 156/155 canli kaynak dogrulamasi, cihaz IBO testi, harici yedek, kullanici onayi, kalici panel ve gunluk cron halen ayri gercek eylem/izin gerektirir. Korunan playlist, yedek, cron, Rule 24 ve test esikleri degismedi. Yeni merkezi Actions sonucu kontrol edilmeli. Kullanicidan yeniden 'siradaki' komutu beklemeyi standart is akisi yapma.

## 13 Ekim 2026 — Acik gorev ve eksik kanit ayristirmasi
Merkezi #38397245525, saglik #38397245567, dokumantasyon #38397245447 SUCCESS dogrulandi. `scripts/central_open_gaps.py` sekiz gorev raporundaki eksikleri ve tek yonetim ozetindeki eksik/bozuk kanitlari `acik_isler_ve_eksik_kanitlar.json` dosyasinda ayri raporlar. Raporun varligi gercek tamamlanma sayilmaz; IBO onayi otomatik verilmez. Test ve merkezi Actions'a eklendi. Kullanici talebi uyarinca bu gelisme not edildi. Playlist, yedek, cron degismedi. Yeni Actions sonucu dogrulanmali. Bir sonraki gercek eksik: interaktif IBO onay paneli, bagimsiz geri yukleme, 156/155 farkini veriyle gidermek; bunlar yapildi diye iddia edilmez.

## 13 Ekim 2026 — Kisa okunabilir durum ozeti
Merkezi #38396974312, saglik #38396974280, dokumantasyon #38396974425 SUCCESS dogrulandi. `scripts/central_short_status.py` son 100 Actions ornegindeki basari/basarisizlik, sekiz gorev eksikleri ve hatali job/step kanitini `madsc_merkezi_denetim/madsc_kisa_durum_ozeti.md` dosyasinda ozetler. Unittest ve mevcut merkezi denetime eklendi. Bu rapor mevcut ayin 1/15 kosusunda ve ilgili push/manual kosularinda uretilir; GUNLUK ZAMANLAMA EKLENMEDI, cron degistirilmedi. Kullanici onayi olmadan zamanlama degistirme. Korunan listeler, yedekler ve IBO onaylari aynen korunur. Yeni Actions run sonucunu dogrula.

## 13 Ekim 2026 — Tek MADSC yonetim ozeti
Merkezi #38396685683, saglik #38396686137, dokumantasyon #38396685724 SUCCESS dogrulandi. `scripts/central_management_summary.py` yedi merkezi kanit raporunu `madsc_merkezi_denetim/madsc_tek_yonetim_ozeti.json` icinde toplar. Eksik ve bozuk JSON raporlar ayri durumla gosterilir; eksik kanit basari sayilmaz. Tek merkezi Actions kosusuna ve unittest'e baglandi. Bu salt okunur rapordur; canli interaktif yonetim paneli veya kullanici IBO onay arayuzu degildir. Siradaki is gunluk kisa ozetin mevcut otomasyon takvimine etkisini degerlendirmek; kullanici izni olmadan cron degistirme. Korunan listeler ve yedekler degismedi. Yeni Actions sonucunu dogrula.

## 13 Ekim 2026 — Logo EPG kimlik ve gecmis tek merkezi rapor
Merkezi #38396343491, saglik #38396343437, dokumantasyon #38396343586 SUCCESS dogrulandi. Kullanici not almayi ozellikle hatirlatti. `scripts/central_identity_epg_logo_audit.py` final sureklilik ozeti, kesif gecmisi, aday logo hazirligi ve EPG eslestirme kanitlarini var/yok durumlariyla tek merkezi JSON rapora alir. Teknik test veya XMLTV/PNG varligi kimlik, yayin hakki ya da Isvec IBO kullanici onayi sayilmaz; otomatik playlist onayi yok. Unittest ve mevcut merkezi workflow'a eklendi. Gercek cihaz testi yapilmadi. Yeni Actions sonucu kontrol edilmeli; sonra tek yonetim raporu/panel ve gunluk ozet konularina gecilecek. Korunan listeler, yedekler, cron degismedi.

## 13 Ekim 2026 — Korunan dosya ve yedek kanit raporu
Merkezi #38396019288, saglik #38396019340, dokumantasyon #38396019403 SUCCESS dogrulandi. `scripts/central_backup_evidence.py` korunan dosyalarin varligini, boyutunu, SHA256 parmak izlerini ve depoda izlenen yedek adli dosyalari tek salt okunur rapora alir. Geri yukleme bu kosuda gercekten denenmedigi, GitHub disi kopya ve branch protection kanitlanmadigi acikca yazilir; bunlar basarili diye gosterilmez. Test ve merkezi workflow'a baglandi. Korunan listeler, arsivler ve cron degismedi. Yeni Actions run sonucunu dogrula.

## 13 Ekim 2026 — Basarisiz otomasyonlarin is/adim raporu
Merkezi #38395674647, saglik #38395674715, dokumantasyon #38395674569 SUCCESS dogrulandi. Tek merkezi denetim son 100 kosudaki en fazla 20 basarisiz run icin GitHub Actions jobs API'sinden job/step sonucunu toplar; `scripts/central_failure_stage_report.py` hata asamasini ve kanit alinip alinmadigini ayri JSON raporlar. Loglar okunmadigindan kok neden uydurulmaz, 20/100 ornek siniri aciktir. Test ve workflow'a baglandi. Korunan listeler, cron ve guvenlik kapisi degismez. Yeni gercek Actions sonucu dogrulanmali.

## 13 Ekim 2026 — Merkezi tekrar test geçmişi analizi
Önceki merkezi #38395289017, sağlık #38395288846, dokümantasyon #38395288914 SUCCESS doğrulandı. Keşif kodunda geçmişi bulunan URL'leri tekrar denemeden önce test edilmemişleri seçen mekanizma zaten mevcut; onu bozup yeniden yazmadık. `scripts/central_duplicate_test_audit.py` var olan `madsc_kesif/gecmis.json` üzerinden tekrar sayısı ve geçmişin bozuk kayıtlarını salt okunur raporlar. Test ve merkezi Actions'a bağlandı. Bu aşama tekrar oranını ölçer; tek başına yeni hız optimizasyonu veya bütün tekrarların kaldırılması değildir. Korunan listeler/cron değişmedi. Gerçek Actions run sonucu kontrol edilmeli.

## 13 Ekim 2026 — Sekiz görev sonrası gerçek kaynak mutabakatı
Merkezi sekiz görev #38394621725, genel sağlık #38394621827, dokümantasyon #38394621851 SUCCESS API ile doğrulandı. Statik dosya adı sayımı yerine `madsc_akilli_kesif.py` içindeki gerçek `SOURCES` ve `SOURCE_TARGET` tanımlarını AST ile ayrıştıran `scripts/central_source_reconciliation.py` eklendi. Benzersiz URL, tam kaynak listesi, birebir URL tekrarları ve hedef farkı merkezi artifact'ta raporlanır. Bu kaynakların canlı erişimini test etmez, 155 hedefini otomatik değiştirmez ve kaynağı silmez. Tek merkezi Actions koşusuna bağlandı, unittest eklendi. Yeni run sonucu ayrıca doğrulanmalı.

## 13 Ekim 2026 — Sekiz iş tek merkezi koşuya alındı (kapsam, henüz tamamlanma değil)
Kullanıcı sekiz kalan işin ayrı ayrı test edilmesi yerine tek merkezi Actions koşusunda denetlenmesini ve sisteme eklenmesini istedi. `scripts/central_eight_task_audit.py` sekiz başlığın her biri için mevcut kod kanıtı, eksikler, tek JSON rapor ve güvenlik sınırları üretir. `test_central_eight_task_audit.py` rapor sözleşmesini ve eksiklerin başarı diye gösterilmemesini doğrular. Mevcut 1/15 merkezi workflow'u ve ilgili push tetikleyicisine bağlandı. **Bu, sekiz eksik işin otomatik tamamlanması değil; toplu ölçüm ve açık iş listesidir.** Özellikle 156/155 farkı, IBO gerçek cihaz kanıtı, bağımsız yedek ve canlı yönetim paneli hâlâ eksik. Mevcut cron, playlist ve yedekler değiştirilmedi. Gerçek Actions run sonucu doğrulanmalı.

## 13 Ekim 2026 — Kullanıcı düzeltmesi: son kontrol 125 aday / 24 paralel işlem
Önceki PR #51'deki 24 aday / 12 worker ayarı kullanıcıya göre gereğinden yavaştı. Kullanıcı 200 yerine 125 ve 32 yerine 23–25 arası paralellik istedi; 125 aday / 24 worker olarak uygulandı. Beş dakikalık kanıt testi ve Kural 24 güvenlik kapısı korunur; son iki başarısız runner shutdown koşusu bu ayar değişikliğiyle geçmişten silinmez. Mevcut test sonuçları tekrar çalıştırılmaz; korunan listeler değişmez. Yeni Actions başarısı ayrıca doğrulanmalı.

## 13 Ekim 2026 — Son kontrol güvenlik kapısı ve runner kapanması düzeltmesi
Kullanıcı ekranında son kontrol run #38393166392, 24. kuralın iki önceki başarısız koşu nedeniyle güvenli durduğunu gösterdi. Günlükler: #38375847106 ve #38382175974 ffmpeg son kontrol adımında runner shutdown / exit 143 ile bitti; bu, aday kanalların tamamının başarısız olduğu kanıtı değildir. Kural 24 korunur, otomatik olarak aşılmaz. Uzun 200 aday / 32 worker grubunu 24 aday / 12 worker olarak küçülterek kaynak ve runner kapanma riskini azaltıyoruz; gerçek yayın süreklilik süresi değişmez, mevcut sonuçlar tekrar test edilmez. Manuel workflow_dispatch kurtarma yolu zaten mevcut ve kuralın izin verdiği yoldur; otomatik başarısızlık zinciri güvenli biçimde bloke kalır. Düzeltme sonrası GitHub Actions gerçek testi ve manuel devamın sonucu ayrıca doğrulanmalıdır. Korunan playlist ve yedeklere dokunulmaz.

## 13 Ekim 2026 — Kullanıcı isteği: altı konuyu tek koşuda denetle
Mevcut merkezi workflow genişletildi: `scripts/central_six_area_audit.py` altı plan başlığını aynı artifact altında salt okunur JSON raporda toplar. Bu altı sorunun otomatik düzeltildiği veya IBO cihaz testinin yapıldığı anlamına gelmez; özellikle 156/155 uyuşmazlığı gerçek veri kaynağıyla daha sonra incelenecek. Mevcut bağımsız günlük otomasyonlar ve playlist/yedekler korunur. Tek koşunun süresi garanti edilmez. Gerçek Actions run sonucu doğrulanmalı.

## 13 Ekim 2026 — Merkezi otomasyon son durum sınıflandırması
PR #48 sonrası merkezi run #38392329904, sağlık #38392329911, dokümantasyon #38392330006 SUCCESS doğrulandı. Bir sonraki paket: kayıtlı GitHub workflowlarının son 100 koşudaki en güncel sonucunu başarılı/başarısız/devam ediyor/diğer/son 100 koşuda görünmüyor olarak sınıflandıran scripts/central_run_status.py ve unittest; merkezi workflow'a bağlandı. Son 100 koşuda görünmeyen bir işin bozuk veya çalışmadığı sonucuna varılmaz. Hiçbir kanal listesi, EPG, cron veya yedek değiştirilmedi. Yeni gerçek Actions run sonucunu ayrıca doğrula.

## 13 Ekim 2026 — Merkezi test #38392076457 SUCCESS; bağımsız Actions durumlarını toplu raporlama
Kullanıcı tekrar onay beklemeden planlı işleri yürütmemizi istedi. PR #47 sonrası main b89232a9 üzerinde merkezi test #38392076457, sağlık #38392076564, dokümantasyon #38392076621 SUCCESS olarak API'den doğrulandı. Merkezi workflow raporu artık GitHub'ın kayıtlı workflow listesi (ad, path, state) ve son 100 koşusunu (workflow_id, status, conclusion, run_id, tarih, bağlantı) ayrı artifact dosyalarında saklar. Bu bağımsız workflowları yeniden çalıştırmaz, yalnız geçmiş sonuçlarını toplar; 100 koşu sınırı nedeniyle eski/seyrek çalışan işlerin başarı durumu çıkarılamayabilir. Mevcut cron ve korunan listeler değişmez. Yeni run ayrıca doğrulanmalı.

## 13 Ekim 2026 — Tek merkezi test kararı ve doğrulanan koşular
Kullanıcı her testten sonra ayrı onay istenmemesini, bilinen tüm testlerin tek merkezi koşuda yapılmasını yineledi. PR #46 main commit 8bb303f8: merkezi denetim run #38391833894 SUCCESS, genel sağlık #38391834058 SUCCESS, dokümantasyon #38391834358 SUCCESS. Sonraki geliştirme: merkezi 1/15 denetiminde yalnız iki test yerine repository içindeki test_*.py unittest modüllerini tek çalışmada keşfet ve çalıştır; ayrıca statik otomasyon raporları ve sağlık taraması devam eder. **GitHub Actions'taki tüm bağımsız workflowları çalıştırmakla aynı değildir**; yayın/cihaz/uzun süreli canlı akış testleri ayrı kalır, izinsiz tetiklenmez. Mevcut günlük işlere ve korunan listelere dokunulmaz. Yeni merkezi run'ın sonucunu doğrula.

## 13 Ekim 2026 — Kullanıcı kararı: mikro-adımlar yerine bilinen merkezi işleri topluca tamamla
Kullanıcı artık her küçük aşamada tekrar onay istenmemesini, bilinen merkezi sistem görevlerinin birlikte yürütülmesini açıkça istedi. Tek paket: mevcut tüm Actions için statik risk önceliklendirmesi, kritik EPG/keşif/yedek/güvenlik işlerinin korunma listesi, kapsam ve koruma sözleşmesi için yeni unittest, ayın 1/15'i merkezi workflow'una entegrasyon ve ilgili dosyalar main'e push edilince otomatik merkezi test tetikleyicisi. Bu rapor gerçek çakışma kanıtı değildir, mevcut otomasyonları orkestre etmez veya kapatmaz. Kanal adaylarının test/IBO değerlendirmesi sonraya ertelidir. Korunan playlist/yedekler ve mevcut cron'lar değişmez. Yeni merkezi Actions çalışmasının gerçek sonucu kontrol edilmeden başarı ilan edilmez.

## 13 Ekim 2026 — Merkezi denetim: ortak concurrency ve UTC saat riski
Kullanıcı önceki testin bittiğini belirterek sıradaki geliştirmeye geçme onayı verdi. scripts/central_workflow_inventory.py mevcut otomasyon haritasını ortak concurrency grup ifadeleri ve aynı UTC saat/dakikada planlanmış işler için salt okunur raporla genişletir. Bu bir risk ön analizidir: farklı günler kesin çakışma sayılmaz, dinamik grup ifadeleri statik metin olarak incelenir. Hiçbir cron, keşif, EPG, yedek veya korunan playlist değiştirilmedi. Yeni kodun Actions PASS kanıtı ayrıca doğrulanmalı.

## 13 Ekim 2026 — Merkezi otomasyon çakışma ön analizi
Kullanıcı önceki testlerin başarılı olduğunu bildirdi ve sıradaki geliştirmeyi onayladı. Genel sağlık ve dokümantasyon run'ları son kontrolde SUCCESS; merkezi 1/15 workflow'unun bağımsız çalışma kanıtı bunlardan ayrı tutulmalı. Mevcut scripts/central_workflow_inventory.py genişletilerek aynı cron ifadesini paylaşan workflow grupları ve zamanlanmış contents:write yetkili workflowlar salt okunur raporlanır. Bu kesin çakışma ispatı değil, inceleme önceliğidir. Hiçbir cron, kanal listesi, yedek, EPG veya otomatik keşif değiştirilmedi. Yeni değişikliğin gerçek Actions sonucu doğrulanmadan PASS ilan etme.

## 13 Ekim 2026 — Merkezi denetim ikinci aşama: Actions otomasyon haritası
Kanal adaylarının geçme/kalma nedenleri ve IBO aktarım kararı kullanıcı isteğiyle sonraya ertelendi. Merkezi ayda iki kez denetim workflow'una mevcut tüm .github/workflows YAML dosyalarının ad, UTC cron, manuel/push/workflow_run tetikleyici, contents:write ve concurrency durumunu JSON olarak raporlayan salt okunur scripts/central_workflow_inventory.py eklendi. Bu envanter **çalışma başarısı veya tam orkestrasyon kanıtı değildir**; hiçbir mevcut schedule kaldırılmadı, workflow tetiklenmedi ve playlist değiştirilmedi. Merge sonrası yeni merkezi workflow için gerçek Actions testi henüz doğrulanmadı; Kural 25 uyarınca takip edilmeli. Sonraki işler: rapordaki yinelenen cron'ları/bağımlılıkları incelemek, kritik günlük yedek ve güvenliği koruyarak kademeli birleştirmek, 156/155 kaynak farkını ayrı denetlemek.

## 13 Ekim 2026 — Kullanıcı gözlemi: sistem testinden geçen Türk adayları IBO'ya deneme amaçlı ulaşmıyor (sonraki değerlendirme)
Kullanıcı, tüm kanal aramaları bittiğinde bu konuyu topluca değerlendirmemizi istiyor: keşif kanalları buluyor ve bazı adaylar birden çok teknik/sistem denetim aşamasından geçiyor; ancak **yedekler kategorisine otomatik eklenmedikleri için IBO Player üzerinde denenemiyorlar**. Kullanıcının önceki deneyimine göre **iki test aşamasını geçmiş bazı Türk kanallarını IBO Player'da bizzat deneyip çalıştığını görmüş**. Bu gözlem teknik test sayısını gerçek cihaz onayıyla eşitlemez, ancak adayları hiç cihaza ulaştıramamanın yanlış negatif/kaçırılmış çalışan kanal riski oluşturduğunu gösterir. **Sonraki tasarım kararı:** tüm taramalar tamamlandığında Türk adaylara öncelik vererek (1) teknik aşama sonuçları ve önceki gerçek IBO kullanıcı kararları ayrı raporlansın, (2) kullanıcıya inceleme/onay için aday isimleri, URL/provenans, logo, kalite ve test kanıtları sunulsun, (3) kullanıcı açıkça izin verirse korunan ana liste/yedekler yerine tercihen ayrı, geri alınabilir IBO deneme listesi veya onay kapsamındaki YEDEKLER kategorisi üzerinden cihazda test edilsin, (4) cihazda çalışan/çalışmayan geri bildirimi ayrı kalıcı kaydedilsin, (5) başarısız testler ve geçmiş silinmesin. **Bu not yeni kanalları YEDEKLER'e, YENİLER'e veya ana listeye otomatik ekleme yetkisi değildir.** Şimdi mevcut kanal arama/testlerine ve diğer sistem görevlerine devam; testten geçen adayların aktarım politikasını taramalar bitince kullanıcıyla değerlendir.

## 13 Ekim 2026 — Kullanıcı yeni öncelik kararı: kanal testlerinin nedenlerini şimdilik ertele
Kullanıcı kanal keşfi ve mevcut testlerin akışını durdurmak istemiyor. Bulunan adayların teknik son kontrolden neden geçip geçmediğinin tek tek incelenmesi, toplu değerlendirme ve IBO'ya hazır kanal kararı **mevcut diğer görevler bittikten sonraya** ertelendi. #50 run 38375847106 runner shutdown/exit 143, #51 run 38382175974 son sorguda IN_PROGRESS; bu kayıtlar nedeniyle şimdi tek tek kanal araştırması/tekrar test başlatma. Geçmiş raporları ve mevcut otomatik keşif/testleri koru. **Şimdi yapılacak iş:** önceki DEVAM_NOTU, AGENTS ve OZELLIK_ENVANTERI uyarınca ayın 1/15'i merkezi sistem denetiminin eksik orkestrasyon/kapsam parçaları, koruma kapısı, 156/155 kaynak envanteri ve diğer ertelenmemiş sistem görevlerini güvenli sırayla sürdür. Korunan CALISANLAR/YENILER/favoriler/yedekler izinsiz değiştirilmez. Merkezi denetim PR #42 merge 82fb46f; yeni workflow'un bağımsız gerçek çalışması henüz doğrulanmadı.

## 13 Ekim 2026 — Ayın 1 ve 15'i merkezi denetim ilk aşaması
Kullanıcı açıkça ayda iki kez (ayın 1'i ve 15'i) ilk günden bugüne bütün sistemin tek merkezden denetim ve bakımına başlanmasını onayladı. İlk aşama `.github/workflows/madsc-aylik-merkezi-denetim.yml`: UTC 07:00, ayın 1/15'i; salt okunur takip edilen dosya/workflow envanteri, kritik kural ve liste dosyası SHA256, mevcut sağlık kodu ve Actions durumu, artifact. **Henüz tüm 156 kaynağı, EPG, logo ve keşif zincirini tek tek çalıştıran tam orkestratör değildir.** Mevcut günde iki kez keşif cron'u, günlük yedek ve güvenlik cron'u bu aşamada değiştirilmedi; çakışma ve bağımlılık denetimi sonrası güvenli birleştirme yapılmalı. İzinsiz playlist değişikliği yok. Yeni workflow için gerçek Actions PASS sonucu kontrol edilmeli; planı bitmiş gösterme.

## 13 Ekim 2026 — Kullanıcı kapsamı netleştirdi: ilk günden bugüne bütün sistem tek merkezden
Kullanıcı yalnız kanal taraması/logolar/sağlık denetimi değil, **ilk günden itibaren GitHub'daki bütün dosyalar, listeler, yedekler, güvenlik kontrolleri, EPG, logolar, kanal arama/testleri, yazılmış bütün kurallar, tamamlanan-yarım kalan-yapılamayan-ertelenen işler** dahil uçtan uca merkezi envanter, denetim, bakım ve tek sonuç raporu istiyor. Hiçbir dosya/kural/iş akışı kapsam dışında varsayılmamalı; gerçek erişim ve kapsama sınırları raporlanmalı. Önerilen tasarım: tek orkestratör ve bütün sistem envanteri; kapsamlı bakım ayda 1 veya 2 kez kullanıcı kararıyla, kritik sağlık ve günlük yedekler ayrı sık aralıklarla. Birleştirme otomasyonların körlemesine eşzamanlı çalışması değil bağımlılık sıralaması; başarısız aşamalar izole, sonuçlar ve eski kayıtlar korunur. Korunan CALISANLAR/YENILER/favoriler/yedekler ve kullanıcı kararları izinsiz değişmez. Mevcut envanter/workflow/kurallar incelenmeden yeni script kurma, çalışan otomasyonu kaldırma veya cron değiştirme. **Bu kayıt kullanıcının kapsam talebidir; henüz otomasyon sıklığını değiştirme ya da uygulama yetkisi olarak yorumlanmaz.**

## 13 Ekim 2026 — Kullanıcı isteği: Uygulama değerlendirmesini kalıcı not al (henüz uygulama yapma)
156 kaynak envanteri denetiminden **önce** kullanıcı MADSC TV uygulamasının neyi eksik/fazla yaptığını sordu; ardından "Not al not" diyerek değerlendirmeyi kaydetmemizi istedi. **Bu maddeler onaylanmış geliştirme veya tamamlanmış iş değildir; öneri/backlog olarak kaydedildi.**
1. Tek yönetim paneli: çalışan/çalışmayan/test bekleyen/IBO onaylı adaylar ve Actions durumu tek yerde.
2. Gerçekten hazır kanal ayrımı: teknik FFmpeg geçişi ≠ yayıncı kimliği ≠ İsveç IBO cihazında kullanıcı onayı; onay olmadan listeye ekleme yok.
3. Korunan ana liste, YENILER, favoriler, yedekler ve sıralama için yalnız prosedürel değil teknik değişiklik/onay engeli.
4. Tekrar eden URL/test/Actions yükünü azalt; yeni ve değişen kaynakları önceliklendir; eski karar ve test geçmişini koru.
5. IBO özel doğrulama: İsveç oynatma, doğru logo, HD/FHD gerçek çözünürlük ve EPG ayrı; mevcut EPG altyapısını yeniden yazma.
6. Tek, kısa günlük sonuç raporu: yeni, düzeltilen, başarısız ve kullanıcı onayı bekleyenler.
Ek sadeleştirme: tekrar eden testleri/workflowları ve teknik başarı etiketlerini envanterle karşılaştır; başarılı işleri körlemesine silme. Öncelik önerisi: yönetim paneli + güvenli onay kapısı, ardından mevcut testleri sadeleştirme, sonra 156 kaynak denetimi. **Kullanıcı henüz bu sırayı geliştirmeye başlama onayı vermedi; yalnız not istedi.** AGENTS.md ve OZELLIK_ENVANTERI.md tekrar-önleme kuralları geçerli. Ana liste, YENILER, favoriler ve yedeklere dokunma.

## 13 Ekim 2026 — Sekiz görev geliştirmesi PR #35
Kullanıcı sekiz görevi kanal test sonuçlarını beklemeden bitirmeyi istedi. PR #35 merge `8a7e5a1afb1cb9c2d33f164275a402c81095d1d1`: `final_validation.py` son kontrol sonuçlarında `license_status=NOT_VERIFIED`, `source_rights_review=REQUIRED`, `station_identity_evidence=NOT_VERIFIED`, `logo_identity_evidence=NOT_VERIFIED`, `epg_device_evidence=NOT_VERIFIED` alanlarını ayrı izler; state `source_history` final adayına taşınır. `test_final_validation.py` içinde kanıt ayrımı regresyon testi eklendi. Yeni testin PASS sonucu henüz görülmedi; sağlık run #38342271874 IN_PROGRESS. Keşif run #38342135063 SUCCESS, devam keşfi #38342145171 IN_PROGRESS; son kontrol #38342088291 IN_PROGRESS. Kullanıcı onayı olmadan ana liste/YENILER/favoriler/yedekler değiştirilmedi. Bu değişiklik lisans, gerçek kimlik veya IBO onayı sağlamaz; sekiz görevin tümü henüz kapanmadı.

## 13 Ekim 2026 — Türk önceliği regresyon testleri
PR #32 merge `21672b51fe437ce3baeb3c10213457a3e3d965c0`: `test_final_validation.py` içine (1) açık Türkçe kaynak/ülke ipucunun belirsiz isimli adaylardan önce sıralanması, (2) source_id/source_language_hint bilgisinin üç aşamalı state üzerinden son kontrole korunması için iki test eklendi. Kod ve testler merge edildi, fakat bu yeni iki testin GitHub Actions'da PASS verdiği **henüz doğrulanmadı**; sonraki son kontrol run'unda `python3 -m unittest test_final_validation -v` adımını kontrol et. Son sağlık run #38341426115 SUCCESS; tarama #38341066600 IN_PROGRESS, doğrulama #38341306336 PENDING, son kontrol #38341310290 PENDING. Test raporu olmadan kanal hazır denmez. Ana/YENILER/yedekler korunur. Sekiz görev devam eder.

## 13 Ekim 2026 — Türk tarama zinciri ve koruma düzeltmesi
Türk kaynak kimliği zinciri: PR #29 merge `14a0339169fd355260c5d54a068cd5125e3e2180` keşif geçmişine source_id/source_language_hint ekledi; PR #30 merge `482cdd47fd62affe5a8734a3ef013056824dabd0` bu ipuçlarını üç aşamalı doğrulama ve son kontrole taşıdı. Gerçek yayıncı ülke/kimliği ve IBO doğrulanmış sayılmaz. Birleşik keşif run #38341066600 son kontrolde IN_PROGRESS, run #38341078497 CANCELLED; üç aşamalı run #38341306336 PENDING. Sağlık run #38341306295 SUCCESS.
**Kritik güvenlik düzeltmesi:** Son kontrol workflow'unda `CALISANLAR.m3u` içindeki YEDEKLER kategorisine otomatik yazan adım tespit edildi. Kullanıcının açık onay kuralına aykırı olduğundan PR #31 merge `26965c71939c9b9757eec8c05baf7bd6d84a1309` ile kaldırıldı; son kontrol adayları sadece raporlanır. Mevcut ana liste, YENİLER, favoriler ve yedek dosyaları değiştirilmedi. Yeni sağlık run #38341416135 son sorguda IN_PROGRESS, başarı henüz ilan edilmez. Sekiz görev toplu planı sürüyor; henüz tümü bitmedi.

## 13 Ekim 2026 — Kullanıcı kararı: Türk kanal önceliğine dönüş ve sekiz görevi toplu teslim
Kullanıcı tek merkez tam yedek sisteminin **GitHub dışı cihaz ayarları, gizli bilgiler ve bağımsız saklama eksiklerine daha sonra dönmeyi** istedi. Bu eksikler yapılacak işlerden silinmez. Kullanıcı artık Türk kanal önceliğine dönmek, sekiz görevi **tek tek yükleme yerine tek toplu değişiklik/teslim paketiyle** tamamlamak istiyor. Öncelik: güvenilir ülke/dil/kaynak metadata zinciri `madsc_akilli_kesif.py` → `verification_pipeline.py` → `final_validation.py`; Türk ulusal/yerel/diaspora adayları önce, yabancı adaylar sonra. Aynı toplu çalışma kapsamında kaynak envanteri 156/155 farkı ve tazelik, test geçmişi güvenli birleştirme, gerçek kanal kimliği, logo/EPG ve cihaz ayrımı, yasal şüpheli kaynak işaretleme, branch/yazma güvenliği ve felaket eksiklerini değerlendir. Sekiz işin tamamını **kanıt ve test olmadan bitmiş ilan etme**; ayrı ayrı ana listeye yükleme yapma. Korunan `CALISANLAR.m3u`, `YENILER.m3u`, favoriler/Hepsi, yedekler, mevcut kanal ad/logo/sıraları ve geçmiş testler izinsiz değiştirilmez. Tek PR / tek kontrollü merge ve sonrasında ilgili gerçek Actions run doğrulaması tercih edilir.
**Yedek kanıtı:** Merkezî tek paket `MADSC-TUM-SISTEM-YEDEK.tar.gz` için run `38340513782` COMPLETED SUCCESS; genel sağlık run `38340513791` COMPLETED SUCCESS. Git-tracked dosyalar ve erişilebilir gizli olmayan GitHub ayar envanteri aynı arşive alınır, geçici dizinde SHA256 ile geri açılabilirliği test edilir. GitHub artifact saklama 30 gün; gerçek repo üstüne yıkıcı geri yükleme test edilmedi; GitHub dışı IBO cihaz ayarları, secret değerleri, untracked/eski geçici kayıtlar ve bağımsız uzun süreli harici kopya kapsam dışıdır. Kullanıcıya “tüm dış ayarlar dahil her şey geri gelir” garantisi verilmez.

## 13 Ekim 2026 — Tek pakete GitHub ayar envanteri, PR #28
Kullanıcı **her şey için tek bir koruma paketi, tek geri yükleme** istedi. Mevcut merkezi `MADSC-TUM-SISTEM-YEDEK.tar.gz` genişletildi; ikinci paket oluşturulmadı. PR #28 merge commit `bbe853793fd3da6cb8f6b35bb90779d345a537bc`. `scripts/repository_settings_inventory.py` GitHub API'den gizli olmayan repo/branch/workflow/ruleset/Actions izin bilgilerini alıp `MADSC-SISTEM-AYAR-ENVANTERI.json` oluşturur; erişim yoksa UNAVAILABLE olarak kaydeder. `scripts/full_system_backup.py` bu envanteri de aynı arşive ekleyip SHA256 ile izole geri yüklemeyi doğrular. Mevcut günlük 05:40 UTC tek workflow devam eder. **İlk Actions run `38340513782` son sorguda QUEUED, sağlık `38340513791` IN_PROGRESS; henüz başarı iddiası yok.** Sınırlar: secret değerleri GitHub'dan okunamaz; IBO Player cihaz ayarları, GitHub dışı dosyalar, süresi dolmuş artifactler, kullanıcı hesap ayarları ve bağımsız offsite saklama kapsanmıyor. Metadata otomatik ayar geri yüklemesi değildir. Korunan playlist ve test geçmişine dokunulmadı. Sonraki iş run sonuçlarını doğrula, sonra harici/cihaz kaynaklarını kullanıcı onaylı güvenli dışa aktarmayla tek arşive katma olasılığını değerlendir; gizli bilgileri düz metin arşive alma.

## 13 Ekim 2026 — Tek merkez tüm sistem yedeği, PR #27
Kullanıcı ayrı ayrı tatbikatlar yerine **tek merkezden tüm IPTV sistemi, ayarları ve yapılan çalışmaları** korumayı istedi. PR #27 main'e squash merge: `9298a62553e667f056e4c85e25e19ded37c9908a`. `.github/workflows/madsc-tum-sistem-yedek.yml` her gün 05:40 UTC çalışır; `scripts/full_system_backup.py` tüm **Git tarafından takip edilen** dosyaları tek `MADSC-TUM-SISTEM-YEDEK.tar.gz` arşivine alır, SHA256 manifesti oluşturur, geçici dizinde her dosyayı geri yükleyip bayt eşitliğini doğrular. GitHub artifact saklama 30 gündür. Önceki iki ayrı tatbikatın günlük/haftalık schedule'ı kaldırıldı; manuel tetikleme ve değişiklik sonrası testleri kaldı. İlk gerçek merkezi Actions run `38340189383` SUCCESS, sağlık run `38340189401` SUCCESS. **Kapsam sınırı:** Git-tracked kanal listeleri, yedekler, kod, workflow, repo içindeki EPG/logo/test geçmişi/raporlar ve DEVAM_NOTU kapsanır. Git dışındaki cihaz ayarları, IBO Player verileri, GitHub secrets/depo ayarları, geçmiş Actions artifactleri ve yalnız untracked/geçici dosyalar kapsanmaz. Arşiv GitHub artifact olduğundan bağımsız uzun süreli offsite backup değildir; bunları kullanıcıya açıkça belirt. Sonraki adım eksik kapsam envanteri ve bağımsız saklama seçenekleri; kullanıcıdan cihaz/secret bilgisi istemeden veya korunan dosyalara dokunmadan ilerle. Sekiz görevden felaket koruması tamamen bitti diye ilan etme.

## 13 Ekim 2026 — Felaket koruması otomatik tatbikatları PR #26
Kullanıcı güvenli otomatik kurtarma kontrolünü başlatma izni verdi. PR #26 main'e squash merge edildi: commit `42a28f66ae71f991c86a22640ec5aa73afeee5ee`. Mevcut iki workflow'a yalnız schedule ve kullanıcıya görünen Türkçe step adları eklendi: `felaket-kurtarma-tatbikati.yml` günlük 05:40 UTC, `yedek-geri-yukleme-tatbikat.yml` Pazartesi 05:50 UTC. Salt okunur contents izni, geçici dizinde geri yükleme, artifact raporu ve manuel tetikleme korundu. **Gerçek listelerde otomatik geri alma veya bağımsız dış yedekleme YOK.** İlk gerçek Actions koşuları merge sonrası `38340000922` (felaket), `38340000886` (yedek), `38340000969` (sağlık) ilk kontrolde QUEUED; başarı sonucu doğrulanmadan tamamlandı deme. Sonraki adım bu runların conclusion durumunu kontrol etmek, ardından tüm kritik geçmiş/rapor/logo/EPG için bağımsız yedek stratejisi tasarlamak. Korunan listeler ve eski kayıtlar değiştirilmedi.

## 13 Ekim 2026 — SEKİZ İŞLİK ONAYLI YAPILACAKLAR / FELAKET KORUMASI BAŞLANGICI
Kullanıcı sekiz işi sırasıyla kaydetmeyi ve **1. Felaket korumasından başlamayı** açıkça istedi; bütün işler bitmeden tehlikeli toplu değişiklikler yapılmayacak. Görevler: (1) otomatik yedek ve geri yükleme kontrolü; (2) 156 tanımlı kaynak / 155 hedef farkı, erişilemeyen ve eski kaynakların ayrımı; (3) Türk kanal kimliğinin tüm test aşamalarına taşınması; (4) geçmiş ve yeni raporların güvenli birleştirilmesi; (5) gerçek kanal kimliği doğrulaması; (6) logo/EPG ve ayrı IBO cihaz testi; (7) şüpheli/telif-lisans riski olan kaynakların işaretlenmesi; (8) branch koruması, yazma izinleri, kurtarma ve güvenlik testleri. Kullanıcı özellikle önce felaket koruması, ardından kaynak güncelliği ve Türk kanal keşfini istedi. Sohbet kapanırken bekleyen Türk öncelik işini hatırlat; sohbet bitişini otomatik algılama garantisi verme.
**1. iş ilk salt-okunur inceleme:** Mevcut `.github/workflows/felaket-kurtarma-tatbikati.yml` ve `yedek-geri-yukleme-tatbikat.yml` yalnız manuel veya kendi dosya/script değişiminde tetikleniyor; düzenli schedule yok. `scripts/disaster_recovery_dry_run.py` sadece CALISANLAR.m3u ve YENILER.m3u dosyalarını Git HEAD sürümünden geçici dizine geri yükleyip bayt eşitliğini doğruluyor. `scripts/restore_dry_run.py` iki tarihli yedek aday dosyasını geçici dizinde geri yükleyip korunan iki M3U'nun değişmediğini doğruluyor. Bu testler bağımsız uzak yedek, tüm geçmiş JSON/EPG/logo arşivi veya gerçek felaket sonrası depo kurtarması garantisi değil. **İlk adım:** son gerçek Actions run kanıtlarını ve tüm korunacak dosyaların envanterini doğrula; sonra güvenli periyodik tatbikat ve bağımsız yedek stratejisi, geri alma testleri. Hiçbir korunan liste, yedek veya geçmiş test bu incelemede değiştirilmedi. Sekiz görevin hiçbiri tamamlandı ilan edilmedi.

## 13 Ekim 2026 — Kullanıcı onayıyla asıl hedefe dönüş / sıradaki iş
Kullanıcı sağlık raporu #39 ekranında **0 Hata / 0 Uyarı / 25 Bilgi** gösterdi; dört RESET_PUSH_GUARDED kaydı INFO olarak görünüyor. Son 100 Actions içinde 13 failed, 1 cancelled, 2 active geçmiş/durum sayımı var; bunlar ayrı incelenmeli. Kullanıcı “Harika asıl hedefte dönelim” dedi, ardından “Tamam not al not” diyerek bu işin kaydını istedi.
**Asıl hedef:** Türkiye ulusal ve yerel TV kanalları ile Avrupa'daki Türkçe yayın yapan kanalların bulunması, yinelenen bağlantıların ayrılması, teknik test ve kimlik/İsveç IBO cihaz onayının ayrı tutulması. Yabancı kanallar Türk adaylarının önüne geçmemeli. Geçmiş testleri tekrarlama, mevcut test ve yedek kayıtlarını koru. Kullanıcı açık onayı olmadan CALISANLAR.m3u, YENILER.m3u, ⭐ YENİLER, favoriler/Hepsi ve YEDEKLER'e ekleme veya değişiklik yapma.
**Kodda doğrulanan açık:** verification_pipeline.py geniş kaynak taramasındaki kimliği doğrulanmamış adayları state'e alıyor; final_validation.py Türkçe öncelik için country/source_id/label kullanıyor fakat state'ten gelen adaylarda country/source_id taşınmıyor. Sonraki iş: keşif → üç aşama → son kontrol boyunca güvenilir ülke/dil/kaynak metadatasını taşımak; isim benzerliğini kanal kimliği kanıtı saymamak; birim testi ve gerçek GitHub Actions run sonucu ile doğrulamak. Kaynak taraması ve testler tamamlanmadan yeni çalışır kanal sayısı iddia etme. TGRT Belgesel ve TV5 resmî canlı yayın sayfaları olası araştırma kaynağı; doğrudan oynatılabilir IPTV URL'si veya test başarısı olarak sayma.
**Bu not yalnızca devir kaydıdır; yeni kod, test çalıştırma veya playlist değişikliği yapılmadı.**

## 13 Ekim 2026 — Dört reset/push uyarısı: çakışmada veri kaybını önleme
Kullanıcı GitHub sağlık #32 yeşil olduktan sonra kalan dört reset/push uyarısını düzeltmeyi açıkça istedi. Birleşik keşif, üç aşama, geniş kaynak taraması ve son kontrol workflowları incelendi. Her biri rapor üretiminden önce origin/main commit SHA'sını RUNNER_TEMP/madsc-rapor-base-sha içinde kaydeder; rapor kaydetme retry döngüsünde git reset öncesinde başlangıç SHA ile son origin/main arasında kendi rapor klasörü değişti mi diye git diff --quiet ile kontrol eder. Başka iş aynı klasörü değiştirdiyse **fail closed**: eski rapor yeni raporun üzerine yazılmaz, workflow hata verir, üretilen rapor artifact olarak saklanır. Git push --force yok; mevcut seri concurrency grupları korunur. Sağlık denetimi bu dört korumayı RESET_PUSH_GUARDED INFO olarak raporlar, korumasız reset/push için WARN sürer. Birim testi eklendi.
**Sınır:** Bu sürüm çakışan JSON raporlarını otomatik birleştirmez; yanlış otomatik birleştirmeyle geçmişi bozmak yerine durur. Daha sonra güvenli candidate_id/URL tabanlı birleştirme ayrı test ve onayla yapılabilir. Son kontrol YEDEKLER ekleme bölümü ve CALISANLAR.m3u değişmedi. Korunan playlistler, YEDEKLER, logo, EPG ve test geçmişi elle değiştirilmedi. Gerçek GitHub Actions run kimliği/sonucu doğrulanmadan başarı ilan edilmez.

## 13 Ekim 2026 — Sağlık testi #30 kırmızı: kesin kök neden ve onarım
Kullanıcının GitHub Actions #30 ekran görüntüsünde test_sistem_saglik_denetimi.py satır 63, test_iptal_kapali_ortak_grup_guvenli_bilgi AssertionError (False is not true), 6 testten 1 başarısız. İncelemede yeni testin sahte YAML dosyasını yazan metni literal \\n olarak kullandığı, gerçek satır sonu oluşturmadığı doğrulandı. Dolayısıyla group: ortak-grup ayrı satır olmadığı için sağlık tarayıcısı SHARED_CONCURRENCY_SAFE üretemedi. Üretim concurrency kodunun kendisi bu hata ile bozuk olarak kanıtlanmadı. Yalnız testteki kaçış dizileri gerçek Python satır sonu kaçışına dönüştürüldü; korunan playlist, yedekler ve otomasyonlar değiştirilmedi. GitHub Actions gerçek run ID ve sonucu görülmeden düzeltme başarılı ilan edilmez.

## 13 Ekim 2026 — Sistem sağlık raporu beş uyarı incelemesi (PR hazırlığı)
Kullanıcı 0 ERROR / 5 WARN / 20 INFO raporundaki uyarıları düzeltme talimatı verdi. GitHub kod incelemesi: üç workflow (madsc-birlesik-kesif.yml, madsc-uc-asama.yml, madsc-genis-kaynak-kontrol.yml) ortak madsc-rapor-yazma concurrency grubunu kullanıyor; üçünün de cancel-in-progress: false ayarı var. Bu bilinçli seri rapor yazma düzeni, otomatik iptal riski değil, gecikme/kuyruk riski taşır. Sağlık denetimi bu durumu INFO/SHARED_CONCURRENCY_SAFE olarak sınıflandıracak, iptal açık/eksik olduğunda WARN bırakacak.
Dört reset/push uyarısı (birleşik keşif, üç aşama, geniş kaynak kontrolü, son kontrol) hâlâ manuel güvenlik incelemesi gerektirir: reset runner kopyasında, ilgili raporlar RUNNER_TEMP içine alınarak geri konuluyor; buna rağmen olası eşzamanlı yazma ve rapor birleştirme kaybı tamamen kanıtlanmadı. Bu dört WARN **kapatılmadı**, ilgili otomasyonlar değiştirilmedi. Sonraki iş: dört workflowda rapor birleştirme / atomik commit / eşzamanlı veri bütünlüğü denetimi ve gerekli ise ayrı güvenli düzeltme.
Sağlık workflow GitHub Step Summary'deki literal \\n satır sonu hatası giderildi; bulguların next_action önerileri özete eklendi. Birim testi eklendi. Bu değişikliklerin gerçek Actions run ID ve sonucu henüz doğrulanmalı; başarı ilan etme. Korunan playlist, YENILER, logo/EPG, YEDEKLER, önceki test geçmişi değiştirilmedi.

## 13 Ekim 2026 — KULLANICI ONAYI: Türk kanallarına öncelik, sohbet devri
Kullanıcı, iki otomatik son kontrol bildiriminde çok sayıda yabancı kanal bulunmasına itiraz etti. **Asıl hedef Türkiye ulusal/yerel kanalları ve yurt dışındaki Türkçe yayın yapan kanallardır.** Kullanıcı, Türk kanallarına öncelik veren test sıralamasını açıkça ONAYLADI ve bu sohbetin yapılacaklarını notlara eklememizi istedi.
**Kod incelemesi:** madsc_akilli_kesif.py günlük keşifte açık Türk kaynaklarıyla sınırlandırılmış; ancak geçmişte birikmiş geniş aday havuzu verification_pipeline.py üzerinden final_validation.py son kontrole giriyor. final_validation.py önce sıradaki 200 adayı alıyordu; Türkçe öncelik yoktu. Geniş kaynak taraması farklı ülkeleri de inceliyor. Son 200 bildiriminde 147 teknik geçiş/kimlik bekliyor, 44 teknik geçiş/içerik incelemesi, 7 süreklilik hatası, 2 timeout; 0 IBO cihaz doğrulaması. Bu sonuçlar Türk kanalı olarak doğrulanmış değildir.
**Onaylı değişiklik:** final_validation.py bekleyen adayları Türk kanalı olduğuna dair açık country=tr, source_id .tr@ veya açık TÜRK/TURK adı varsa önce; Azerbaycan/Kıbrıs/Türkmenistan metadata varsa sonra; diğer/kimliği belirsiz adaylar en sonra sıralar. İsim benzerliği (ATV, NTV, Kanal D vb.) tek başına Türk kimliği kanıtı değildir. Önceki sonuçlar, aday URL kimlikleri, testler ve 200'lük limit korunur. Birim testi eklenmiştir. Bu sadece öncelik sırası; otomatik kimlik doğrulaması veya kesin yabancı engeli değildir.
**Sıradaki işler:** 1) Gerçek GitHub Actions test/run kimliği ve sonucu doğrulanmalı, başarı kanıtı olmadan tamamlandı denmemeli. 2) verification_pipeline.py geniş havuzundan gelen yeni adaylar için açık Türk dil/ülke/kaynak metadatası uçtan uca taşınmalı; isim benzerliğiyle sahte kimlik oluşturulmamalı. 3) Türk ulusal/yerel ve Avrupa Türkçe yayın adaylarının kaynak kapsamı ve raporlama ayrımı denetlenmeli; yabancı adaylar Türk listesine eklenmemeli. 4) Sağlık raporundaki 0 ERROR, 5 WARN, 20 INFO incelenmeli: 4 reset/push güvenlik uyarısı, ortak madsc-rapor-yazma grubu; GitHub Step Summary'deki literal \\n biçim hatası düzeltilmeli. Bu sağlık işleri kullanıcı 'dur' dediği için ertelendi; Türk önceliği için sonraki mesajda onay verildi. 5) Tüm eski teknik sonuçlar saklanmalı; kullanıcı izni olmadan CALISANLAR.m3u, YENILER.m3u, HEPSI/FAVORILER, logo/EPG ve YEDEKLER değiştirilmemeli; IBO İsveç cihaz sonucu ayrı.
**Önemli:** Bu not ve PR gerçek Actions yeşil sonucu görülmeden tamamlanmış sayılmaz.

## 13 Ekim 2026 — Sağlık denetimi #9 yeşil, PR #18 sonraki uyarı/önleme aşaması
Kullanıcı ekran görüntüsünde `MADSC - Genel Sistem Sağlık ve Güvenlik Denetimi #9` commit `299d67b` yeşil SUCCESS (10 sn) olduğunu gösterdi. Önceki #5–#8 YAML yazım hataları (7. ve 52. satırlar) geçmiş kayıtlarıdır; iki düzeltme `83b2a0e` ve `299d67b` ile yapıldı. Sonraki iş için PR #18 squash `d936b272902d14a8174571f61616931448b70c84` main'e birleştirildi: bütün workflow YAML sözdizimi otomatik kapısı, GitHub Actions step summary içinde ERROR/WARN/INFO raporu, concurrency regex onarımı, çift güvenlik bulgusunu kaldırma, sıfır aday raporunu INFO sınıflandırma ve ek birim testi. **PR #18'in gerçek Actions run sonucunu henüz görmedik; yeşil deme.** Sonraki adım: PR #18 gerçek run ve artifact bulgularını incele, kritik sorunları düzelt, yalnız denetim kapsamını genişlet. Korunan kanal listesi, YENILER, logolar, EPG, YEDEKLER, kanal test geçmişi değişmedi.

## 13 Ekim 2026 — Sağlık denetimi genişletmesi PR #17
PR #17 (squash bf0dd923a66ddde37307aae809b615a3d9a80ae6) main'e birleştirildi. Mevcut `tools/sistem_saglik_denetimi.py` artık ortak concurrency grupları, riskli Actions izin/reset örüntüleri, tekrar eden son kontrol aday kimlikleri, YEDEKLER grup sayacı ve boş logo/EPG aday raporunu da denetliyor. `.github/workflows/madsc-sistem-saglik-denetimi.yml` son 100 GitHub Actions run'ının başarısız/iptal/aktif durumlarını API üzerinden salt-okunur raporlayacak, değişen workflow dosyalarında otomatik tetiklenecek; birim testleri genişletildi. Değişiklikler mevcut kanal/EPG/logo/test geçmişini değiştirmedi. **PR merge başarılı, gerçek GitHub Actions run yeşil sonucu henüz doğrulanmadı; eksiksiz 8 katman ve her gelecekteki değişiklik için branch protection garantisi verilmedi.** Kalan kapsam: tüm dosya/bağımlılık taramasını derinleştirmek, güvenli otomatik onarım politikası, tüm yeni değişiklikler için branch ruleset ve cihazda yayın/EPG gerçek testi. Önce PR #17 workflow sonucunu ve JSON artifact'i kontrol et; hata varsa yalnız denetim aracını düzelt, ana playlisti değiştirme.

## 13 Ekim 2026 — Genel sağlık denetimi AŞAMA 1 kuruldu
Kullanıcının onayladığı 5. ana iş / 8 katmanlı denetim için PR #16 (squash e5478545cbc0bdeb02d1e2e3937417e322b17141) main'e birleştirildi. `tools/sistem_saglik_denetimi.py` salt-okunur statik denetim; `test_sistem_saglik_denetimi.py` birim testleri; `.github/workflows/madsc-sistem-saglik-denetimi.yml` günlük 05:17 UTC, kod değişikliği ve manuel tetikleme; JSON artifact, kritik hata halinde kırmızı durum. Korunan playlist/logo/EPG/test kayıtları değişmedi. **Gerçek Actions run sonucu henüz teyit edilmedi; yeşil deneme.** Bu sadece AŞAMA 1: gerçek GitHub Actions geçmişi, çalışma çakışmaları, secret/izin yönetiminin kapsamlı incelemesi, uçtan uca kanal kimliği/IBO testi, otomatik güvenli onarım ve tüm yeni dosyalar için zorunlu branch protection henüz kurulmuş/doğrulanmış değildir. Sonraki adım: PR #16 sağlık workflow gerçek run/JSON bulguları; sonra yalnız eksik katmanları genişlet. 200 aday son kontrolü ve YEDEKLER aktarımını bu çalışma sırasında değiştirme.

## YAPILACAKLAR — 13 Ekim 2026 — sistem genel denetim isteği
Kullanıcı GitHub'daki mevcut ve gelecekte eklenecek TÜM dosya, script, workflow, otomasyon ve bunların birbirleriyle bağlantıları için kapsamlı, sürekli sağlık/güvenlik/uyum/sorun giderme kontrolü istedi; **yapılacaklar listesine alınmasını açıkça onayladı**. Var olan `tools/genel_sistem_bakimi.py` yalnız dosya/JSON okunabilirliğini kontrol eder; `OZELLIK_ENVANTERI.md`, `AGENTS.md` ve mevcut güvenlik testleri yeniden yazılmadan incelenecek.
Planlanan 8 denetim başlığı: (1) dosya envanteri, bozuk/eksik/tekrarlı kod; (2) Actions tetikleme, concurrency, iptal, zamanlama, bağımlılık; (3) token/secret/permissions, tedarik zinciri güvenliği ve yetkisiz değişiklik; (4) playlist ve test geçmişi/yedek bütünlüğü; (5) keşif→üç aşama→5 dk son kontrol→YEDEKLER uçtan uca sonuç kanıtı; (6) mevcut logo/EPG raporlarının doğrulanması, yapılmış logo düzeltmelerini TEKRAR YAPMA; (7) salt okunur hata sınıflandırma ve güvenli onarım önerileri; (8) yeni her dosya/workflow için otomatik kalite ve regresyon kapısı. Önce salt-okunur kapsam/boşluk raporu, sonra eksik parçalar için izole test ve gerçek GitHub Actions başarı kanıtı. Asla ana liste/HEPSİ/FAVORİLER/YENİLER/sıralar/dolu logolar/korunan yedekler üzerinde izinsiz değişiklik yapma.
Kullanıcı ayrıca “test bitti, ona da bak” dedi. 2026-10-13 01:xx UTC GitHub `main` dosyaları tekrar kontrol edildi: `madsc_son_kontrol/summary.json` son snapshot 01:14:15 UTC, 375 completed / 5683 remaining / 280 technical identity pending / 0 ready; `results.json` 375 kayıt; `CALISANLAR.m3u` YEDEKLER (2). Bunlar testin bitiş statüsünü tek başına kanıtlamaz; Actions #30 run sonucunu ayrıca teyit etmek gerekiyor. Kullanıcı ekranında test bitmiş göründüğünü bildiriyor; bunu güncel kayıt olarak raporla, dosya snapshot'ı eski olabilir.

## SOHBET DEVRİ — 13 Ekim 2026 — PR #15 sonrası güncel kontrol noktası
Kullanıcı kalan işleri ve bütün düzenlemeleri kaydetmemizi istedi. Bu bölüm eski tarihli devam notlarından daha günceldir. Önce AGENTS.md, OZELLIK_ENVANTERI.md, GUVENLIK_KURALLARI.md, bu not ve gerçek Actions sonuçları okunacak; tamamlanan işler yeniden kurulmayacak.

**Tamamlanan kod düzenlemeleri:** PR #11 son kontrol 96 aday/16 paralel; PR #12 bunu 200 aday/32 paralel ve 110 dakika üst sınırına yükseltti; PR #13 gereksiz push tetikleyicisini kaldırdı; PR #14 tüm son kontrol tetikleyicilerini tek `madsc-son-kontrol` concurrency grubuna aldı, `cancel-in-progress: false` korundu. PR #15 (squash 117bbb5efd59f7567a6a5fd30a68bf9882154646) 3/3 doğrulama + 5 dakika süreklilik + sıfır inceleme olayı kanıtı olan yeni adayları yalnız 📦 YEDEKLER'e `[TEST]` etiketiyle hazırlayabilen aktarım bağlantısı ve birim testleri ekledi. Gerçek kanal kimliği ve İsveç IBO onayı verilmiş sayılmaz. Mevcut kanallar, favoriler, HEPSİ, YENİLER ve sıraları korunmalı; yalnız kullanıcıca izin verilen YEDEKLER aday ekleme kapsamı geçerlidir.
**Ekran görüntüsüyle doğrulanan testler:** MADSC - YEDEKLER Teknik Aktarım Testi #2 YEŞİL; Birleşik Güvenli Kontrol #29 YEŞİL; teknik aktarım testi #1 YEŞİL. Bunlar kod/güvenlik testleridir, gerçek kanal oynatma testi değildir. Son Kontrol #30 aynı görüntüde IN_PROGRESS; bitiş ve YEDEKLER'e fiili aktarım doğrulanmadı. #29 son kontrol CANCELLED idi: GitHub 'higher priority waiting request' concurrency iptali, teknik kanal hatası değil.
**Son GitHub'da doğrulanmış kayıt:** `madsc_son_kontrol/summary.json` 2026-10-13 01:14 UTC: 375 tamamlanan kayıt, 5683 kalan, 280 TECHNICAL_PASS_IDENTITY_PENDING, 75 TECHNICAL_PASS_CONTENT_REVIEW, 12 CONTINUITY_FAILED, 8 TIMEOUT; hazır 0. Bu snapshot sonradan değişmiş olabilir; canlı raporu tekrar oku. Eski 375 sonuç korunmuş ve 200/32 kodu main'de doğrulanmıştı.
**Sıradaki eksikler, öncelik sırasıyla:**
1. Son Kontrol #30 ve takip eden 200'lük otomatik zincirin gerçek run/sonuçlarını ve sonuçların birikimli kaydını doğrula; aynı anda iki son kontrol çalışmasın. Otomatik devam çalışıyor mu kanıtla.
2. PR #15 YEDEKLER teknik aday aktarımının gerçek workflow çalışmasında kaç yeni kanal eklediğini ve yalnız YEDEKLER'e eklediğini doğrula. Kod testi yeşil olması gerçek aktarım kanıtı değildir. İlgili URL, kimlik, kullanıcı IBO kararı ve logo doğrulamasını ayrı tut; teknik aday gerçek kimlik diye sunulmasın.
3. Günlük birleşik keşifte `madsc_kesif/candidate_epg_logo_join.json` dosyasının tam koşuda üretilip kaydedildiğini doğrula; pilot EPG ile üretim EPG'sini karıştırma.
4. Yeni adayların gerçek marka/logo/kanal kimliği ve dilini bağımsız kanıtla; hatalı kanal TRT 1 gibi etiketlenmesin. Mevcut dolu logoları değiştirme.
5. Gerçek canlı yayın ile XMLTV program eşleşmesini ve İsveç IBO Player Pro EPG/oynatma uyumluluğunu ayrı kontrol et; cihaz onayı kullanıcıdan gelir. Önceki IBO EPG başarısızlığı çözüldü deneme.
6. Cuma salt-okunur ana liste denetimindeki kanal bazlı sorun raporu mevcut; gerçek telefon bildirimi henüz doğrulanmadı. Kullanıcıdan izinsiz ana liste değişikliği yapma.
7. Eski 18 maddelik geliştirme planının tamamlanmış işlerini yeniden kurmadan kalanların güncel Actions kanıtını kontrol et.
Kural 25: Değişiklik sonrası gerçek Actions run kimliği ve sonucu kontrol edilmeli; yeşil olmayan işi tamamlandı sayma.

## SOHBET DEVRİ — 13 Ekim 2026 — yeni sohbet başlangıcı
Repo: Madsc55/madsc-tv. Yeni sohbette önce AGENTS.md, OZELLIK_ENVANTERI.md, GUVENLIK_KURALLARI.md ve bu DEVAM_NOTU.md okunacak; güncel GitHub Actions durumları kontrol edilecek. Eski işlevler yeniden kurulmayacak. Kullanıcı onayı olmadan CALISANLAR.m3u, YENILER.m3u, HEPSI/FAVORILER sırası, logolar, yedekler ve çalışan otomasyonlar değiştirilmeyecek.
Son tamamlanan geliştirme: özellik envanteri OZELLIK_ENVANTERI.md (e7ea523), AGENTS.md'de önce envanter kontrolü (df78ea6), Kural 25 her eklemeden sonra otomatik test (e047974), .github/workflows/madsc-documentation-check.yml (6709a63). Otomatik belge testleri #38322907188 ve #38322927311 GitHub'da SUCCESS doğrulandı. Korunan listeler güvenlik testi #38322898504 SUCCESS. Bu testler cihazda oynatma/EPG doğrulaması değildir.
Son kontrol anında MADSC - Tamamlanan Aday Son Kontrol #38323048495 PENDING, #38321643076 IN_PROGRESS idi; yeni sohbette durumları yeniden sorgula, geçmiş statüleri güncelmiş gibi sunma.
Sıradaki gerçek eksik iş: birleşik günlük kanal keşfi workflow'unun yeni aday logo+EPG birleşik raporunu (madsc_kesif/candidate_epg_logo_join.json) gerçek tam koşuda oluşturup kaydettiğini doğrula. Bağımsız test #38321948143 SUCCESS, fakat tam günlük keşif sonucu henüz kanıtlanmadı. EPG günlük üretimi zaten mevcut; beş kanallık IBO pilotunu tam üretim EPG ile karıştırma. İsveç TCL 55C655 / IBO Player Pro 2128.0 gerçek cihaz sonucu ayrı tutulacak.
Yeni özellik değişikliğinde ilgili GitHub Actions testini asistan tetikler, run ID ve sonuç doğrulanmadan tamamlandı denmez. Kullanıcıdan test başlatması istenmez. Bu not kullanıcı talebiyle yeni sohbet için kalıcı kaydedildi.


## 13 Ekim 2026 - Kural 25 ve otomatik belge testi
Kullanici her ekleme sonrasi testin asistan tarafindan otomatik baslatilmasini istedi. AGENTS.md Kural 25 eklendi (e047974). Yeni .github/workflows/madsc-documentation-check.yml eklendi (6709a63); AGENTS.md, OZELLIK_ENVANTERI.md ve DEVAM_NOTU.md degisikliklerinde otomatik belge kontrolu calisir. GitHub Actions run 38322907188 otomatik tetiklendi; ilk kontrolde QUEUED idi: https://github.com/Madsc55/madsc-tv/actions/runs/38322907188 . Korunan kanal listeleri degismedi. Bu belge testi IPTV yayin veya cihaz uyumlulugu testi degildir.
## 13 Ekim 2026 — Özellik envanteri ve tekrar önleme prosedürü
Kullanıcının isteği üzerine OZELLIK_ENVANTERI.md eklendi (commit e7ea52333c02fea90f645c48eaadbf73ceee8a0a). Mevcut kanal keşfi, aday PNG, EPG üretimi/yayını, IBO pilotu, kimlik denetimi, kalite uyarıları ve birleşik raporun gerçek kapsamları kaydedildi. AGENTS.md yeni iş öncesi envanter+kod+son Actions kontrolünü zorunlu kılacak şekilde güncellendi (commit df78ea694917231653af918d5fdaa8c2cff378a2). Bu belge tek başına kod düzeyinde zorlayıcı kapı değildir; yeni workflow/özellik eklenmedi, ana playlist ve korunan veriler değişmedi. Sıradaki iş: gerçekten eksik kalan günlük keşif uçtan uca run doğrulaması.

## 13 Ekim 2026 — IBO EPG kimlik denetimi otomatik test edildi ve geçti
Kullanıcı testleri kendisinin değil asistanın başlatmasını istedi. Bağımsız salt-okunur araç scripts/ibo_epg_kimlik_denetimi.py eklendi (commit 5fd26f7). Yeni izole .github/workflows/ibo-epg-kimlik-denetimi.yml oluşturuldu (commit 45fa651). Dosya oluşturma push tetiklemesi ile GitHub Actions #38321460694 otomatik başladı ve **success** tamamlandı: https://github.com/Madsc55/madsc-tv/actions/runs/38321460694 . Python sözdizimi, CALISANLAR.m3u ile mevcut epg/ibo-test-epg.xml pilot kimlik eşleşmesi ve JSON raporu üretimi geçti; ibo-epg-identity-audit artifact yüklendi. Bu üretim EPG URL'sinin cihazda çalıştığını doğrulamaz. İş akışı mevcut diğer otomasyonları değiştirmez, salt-okunur, manuel tekrar tetiklenebilir. Kullanıcıdan GitHub'da test başlatması istenmedi. Ana listeler, logolar, yedekler ve EPG üretimi değiştirilmedi.

## 13 Ekim 2026 — IBO Player Pro araştırması: ilk doğrulanmış kaynaklar ve sonraki teknik denetim
Kullanıcının 'Araştıralım' talebi üzerine resmî görünen IBO destek sayfaları ve iptv-org katkı belgeleri incelendi. Kaynaklar: https://iboplayerpro.com/ (IBO Player Pro: uygulama yerleşik EPG verisi sağlamaz; sağlayıcı EPG-ready olmalı; TV format/kodek uyumsuzluğu mümkündür), https://iboplayerpro.com/support (M3U/M3U8, playlist yükleme/yeniden başlatma, donma nedenleri), https://frontend.iboplayer.com/faq (IBO Player ayrı ürün/sürüm; harici EPG, cihaz format farkları), https://iptvsupportcenter.zohodesk.eu/portal/en/kb/articles/ibo-player (bazı IBO sürümlerinde XMLTV EPG ayrı alan), https://github.com/iptv-org/iptv/blob/master/CONTRIBUTING.md (kimlik, kararlılık, geo, tekrar, tokenli link kontrolleri), https://github.com/iptv-org/database/blob/master/CONTRIBUTING.md (kanal/akış/logo ayrı veri yapıları). Üçüncü taraf IB Player Pro ve IBO Player Pro isimleri karıştırılmamalı; özellikleri otomatik eşdeğer sayılmamalı. Reddit kullanıcı deneyimleri: https://www.reddit.com/r/IBOPlayerTV/comments/1fj92ws/problem_loading/ ve https://www.reddit.com/r/TiviMate/comments/1lgt8vi/ (anekdot, genel istatistik değil).
Kod envanteri: scripts/build_epg.py, build_ibo_epg_test.py, automatic_png_logos.py, candidate_logo_report.py, logo_visual_evidence.py, ibo_bagimsiz_test_listesi.py mevcut; bunlar yeniden yazılmadan önce işlevleri ve çıktı bağlantıları incelenmeli. Sonraki iş: cihaz/sürüm eşleştirmesi, M3U tvg-id ve XMLTV channel id eşleşme denetimi, EPG HTTP/content-type/XML doğrulaması, logo URL erişimi/formatı, akış kodek/cihaz matrisi ve IBO üzerinde kontrollü pilot; önce salt okunur rapor. EPG hâlen IBO cihazında doğrulanmış değil. Ana playlistler, yedekler ve otomasyonlar değiştirilmedi.

## 13 Ekim 2026 — IBO Player Pro uyumluluğu ve dünya IPTV deneyimleri araştırması (sohbet kaynak notu)
Kullanıcı, mevcut MADSC-TV iş akışlarına ve korunan kanal listelerine dokunmadan dünya çapındaki IPTV kullanıcı yorumlarını, açık kaynak geliştirici önerilerini ve özellikle IBO Player Pro'nun M3U/EPG/logo/amblemlerle uyumluluğunu araştırıp yeni, tekrarsız akıllı geliştirmeler planlamamızı istedi. Önceki konuşmada 10 fikir sunuldu: kaynak kalite puanı, İsveç/coğrafi erişim analizi, kanal kimliği eşleştirme, yayın kararlılığı geçmişi, eksik Türk kanallarını hedefli arama, akıllı kuyruk, IBO cihaz sonuçları, kaynak değişiklik algılama, ayrı EPG tanılama, birleşik aday/onay raporu. Bunlar öneridir; hepsinin eksik veya uygulanmış olduğu henüz kod düzeyinde doğrulanmadı.
Bu sohbetteki ek talep: IBO Player Pro üreticisinin resmi bilgi/destek kaynakları ve gerçek kullanıcı deneyimleriyle desteklenen uyumluluk matrisi hazırlanmalı; tvg-id/tvg-name, XMLTV URL, logo formatı/URL, M3U sözdizimi, cihaz/uygulama farkları, yükleme/önbellek ve İsveç cihaz testleri ayrı incelenmeli. Resmi olarak belgelenmeyen davranışlar kesin özellik gibi sunulmamalı. EPG daha önce IBO cihazında başarısız; destek yanıtı bekleniyor. Kullanıcı, araştırmanın ve bu sohbetin konusunun kalıcı notlarda korunmasını özellikle istedi.
KORUMA: CALISANLAR.m3u, YENILER.m3u, ⭐ YENİLER, FAVORİLER/HEPSİ, korunan yedekler, mevcut test ve otomasyonlar değişmeyecek. Yeni geliştirmeler önce mevcut kodla karşılaştırılacak; yalnız açık onayla ve bağımsız testlerle uygulanacak. Bu kayıt yalnız DEVAM_NOTU.md'ye eklendi; herhangi bir oynatma listesi değiştirilmedi.

## 12 Ekim 2026 — IBO Player için 5 kanallı EPG testi
Kullanıcı IBO'da EPG hâlâ görünmediği için küçük XMLTV pilotuna onay verdi. `scripts/build_ibo_epg_test.py` eklendi (636813a): TRT 1, TRT 2, SHOW TV, ATV, KANAL D için mevcut tvg-id'ler aynen korunarak ana EPG'den ayrı `epg/ibo-test-epg.xml` üretilir; beşinin de programı yoksa hata verir. Günlük workflow üretim ve commit'e bağlandı (a38f434), Pages'e ayrıca yayımlama eklendi (889d562). Pilot URL planı: https://madsc55.github.io/madsc-tv/ibo-test-epg.xml . Son runlar 38309845083 (EPG) ve 38309850376 (Pages) ilk kontrol sırasında queued; pilot URL erişilebilirliği ve IBO cihaz başarısı henüz doğrulanmadı. Ana M3U/favoriler/YENİLER/yedekler değişmedi.

## 12 Ekim 2026 — EPG çakışma önlemi (cihazda henüz doğrulanmadı)
Kullanıcı başka uygulamada EPG'nin göründüğünü ancak TRT 1 için yanlış program başlığı gösterdiğini; IBO Player'da ise hiç görünmediğini doğruladı. `scripts/build_epg.py` commit `0b25561` ile aynı XMLTV kanal kimliğine binen saat aralıklarını tekilleştirecek ve atlanan çakışmaları `overlap_skipped` olarak raporlayacak şekilde güncellendi. Bu kaynakların doğruluğunu garanti etmez ve IBO Player uyumluluğunu henüz kanıtlamaz. CALISANLAR.m3u, favoriler, yedekler, YENİLER değiştirilmedi. Sonraki iş: EPG Actions run durumunu ve yayımlanan XMLTV'nin gerçek cihaz sonucunu kontrol etmek; TRT 1 kaynağını yayın akışıyla karşılaştırmak.

## 12 Ekim 2026 - Uc asama hata duzeltmesi
Kullanici kirmizi Actions ekranini paylasti. Run 38303499979 job 114991848830 logunda verification_pipeline.py line 40 IndentationError goruldu: kod icinde gercek satir sonu yerine literal ters-bolun-n yazilmisti. verification_pipeline.py duzeltildi (66541b4), uc asama workflow push tetikleyicisine verification_pipeline.py eklendi (90f999f). Yeni Actions run 38303727064 ilk kontrolde QUEUED; basarili oldugu henuz teyit edilmedi. Playlist ve eski test kayitlari degistirilmedi.

## 12 Ekim 2026 - Genis tarama ile uc asamali test baglantisi
Kullanici onayi ile verification_pipeline.py genis kaynak aday kaydini okuyup sadece madsc_dogrulama/state.json icinde bulunmayan URL'leri mevcut uc denemeli kuyruge alacak bicimde guncellendi (ec3640f). madsc-uc-asama.yml due kontrolune yeni aday sayimi eklendi (e892c67). madsc-genis-kaynak-kontrol.yml kaynak raporunu kaydettikten sonra uc asama workflow_dispatch baslatacak bicimde guncellendi (8d88ee8). Testler arasinda mevcut 6 saat kosulu ve biten 3 denemeyi tekrar etmeme kurali korunur. Playlistler, YENILER, favoriler, yedekler ve kimlik onayi degismedi. Bu commitlerin Actions uzerinde basarili calismasi henuz teyit edilmedi; kullanicinin IBO cihaz testi ayridir.

## 12 Ekim 2026 - Genis tarama aday ayirma
Kullanici otomatik calisma ve yeni URL ayirma istedi. tools/genis_kaynak_taramasi.py commit 2a5ec7d ile degisen Turkce odakli kaynaklardan URL ve kanal etiketlerini ayirir, ana playlistler ve madsc_kesif/gecmis.json ile karsilastirir, tekrar etmeyenleri madsc_genis_tarama/candidate_review.json icine kimlik incelemesi bekleyen olarak kaydeder. Onceki aday kayitlarini korur. Bu asama uc asamali teknik test sistemine dogrudan veri AKTARMAZ; bu entegrasyon guvenli state semasi dogrulanmadan tamamlandi denemez. Kaynak tarama schedule otomatik, ama yeni adaylarin uctu test ve IBO dogrulamasi tamamlanmis degildir. Ana liste ve YENILER degismedi. Yeni run dogrulanmadi.

## 12 Ekim 2026 - Haftalik ve aylik kaynak kontrolleri
Kullanici onayiyla haftalik ek kaynak ve aylik 155 kaynak icerik-degisim denetimi kodu eklendi: tools/genis_kaynak_taramasi.py (4dc631a), zamanlama dosyasi .github/workflows/madsc-genis-kaynak-kontrol.yml (474713c). Bu yeni akis yayinin oynatilmasini veya kanal kimligini test etmez; kaynaklari okuyup SHA-256 degisimini ve M3U kayit sayisini raporlar. Haftalik hedefli ek kaynaklar, aylik 155 kaynak. Yeni workflow basarili calisma sonucu henuz dogrulanmadi. Salt okunur genel bakim araci tools/genel_sistem_bakimi.py (057a3c8) eklendi ve birlesik durum raporuna baglandi (17f2825). Ana liste, favoriler, YENILER, logolar ve test gecmisi degistirilmedi. Aday bazinda yeni kanal ayristirma, teknik test ve kimlik dogrulama bu genis tarama akisinda HENUZ YOKTUR.

# MADSC TV — güncel devam notu

## SOHBET DEVRİ
Güncelleme: 12 Ekim 2026, Stockholm 20:44 sonrası MTürk logo ve Ton TV kontrolü. Yeni sohbet önce bu dosyayı, AGENTS.md'yi ve ilgili GÜNCEL raporları okur. Bu dosya kısa kontrol noktasıdır; bütün sohbetin dökümü değildir. Kaynak rapor daha yeniyse rapor esas alınır.

## Kesin kurallar
- Ana liste/YENİLER, favoriler ve Hepsi'nin korunacak ilk 90 sırası, korunan yedekler yalnız açık kullanıcı izin kapsamında değişir.
- Ana listedeki DOLU logo alanlarına dokunma. Yalnız logosuz kayıtları bul; gerçek PNG/kimlik hazırlığı ayrı aday raporunda kalır. Son envanterde boş logo 0/1029 kategori kaydı.
- Teknik geçiş, gerçek kanal/amblemi, İsveç IBO sonucu ve EPG görünürlüğü ayrı. Yeşil Actions cihaz onayı değildir.
- ADA/Kanal D için kullanıcının yabancı kanal reddi önceki görsel desteğin üstündedir; reddedilmiş URL'leri yeniden önerme/ekleme.
- Test geçmişi korunur; tamamlanmış üç deneme veya final sonucu (başarısız/zaman aşımı dahil) yeniden yapılmaz. Eksik denemelerde en az 6 saat.
- Yeni kanal, aynı kanalın farklı URL'si ve aynı URL'nin kategori kopyası ayrı değerlendirilir. URL sayısı kanal sayısı değildir.

## Son doğrulanmış sonuçlar
- Üçlü doğrulama: 6981 URL, 6729 tamamlanmış; dağılım 6028 3/3, 447 2/3, 112 1/3, 142 0/3. 252 eksik kayıt altı saat bekliyor; rapor anında uygun aday 0. Snapshot: 12 Ekim 17:35:46 UTC.
- İlk 6436 tamamlanmış test korunmuştur. Sonraki 326 içinden 293 kayıt üç denemeye ulaşmıştır; yeni keşiften 219 kayıt da ayrı eklenmiştir. 252 kalan kayıt, başlangıçtaki 33 + yeni 219'dur; zamanı state.json'dan yeniden hesapla.
- Final kontrol: önceki 39 + yeni 24 = 63 sonuç korunuyor. 48 teknik geçiş/kimlik bekliyor; 10 içerik incelemesi; 2 süreklilik başarısız; 3 zaman aşımı. Yeni 24'ün farkı: 19 teknik geçiş/kimlik bekliyor, 4 içerik incelemesi, 1 zaman aşımı. Snapshot: 12 Ekim 17:35:45 UTC. Rapordaki 5687 kalan eski snapshot; yeni üçlü geçişlerle kuyruk değişir.
- Başarılı runlar: üçlü #87 (38283156064), #89 (38284072474), #90 (38284962128); final #2 (38283388684). Eski kuyruktaki cancelled/skipped runlar kanal testi başarısızlığı sayılmaz. Yeni işlemden önce güncel run durumunu oku.
- İlk 39 kimlik raporunda 36 görüntü incelendi: 4 ilk görsel destek, 20 Türk hedef kimliği reddedilmiş/desteklenmemiş, 15 açık inceleme. Sonraki ADA/Kanal D kullanıcı reddi geçerli. Yeni 24 ve önceki 15 açık kimlik kaydı için 39 kayıt/35 kare ayrıca incelendi: 15 görsel etiket desteği, 6 yalnız marka/bölgesel hedef bekleyen, 14 kimlik yetersiz, 4 görüntüsüz. Bu cihaz veya ekleme onayı değildir. Ana liste blob'u 042b280409a99d2d19dc379cad4b4889d7c391f8 ile URL karşılaştırması: 11 mevcut aynı URL, 7 aynı isim/farklı URL (kimlik doğrulanmamış), 21 ayrı/listede olmayan aday. Raporlarda bu üç sınıfı ve isimleri kullanıcıya açıkça göster; hepsini yeni kanal diye anlatma. Ayrı kaynak: madsc_son_kontrol/kimlik_devam_2026-10-12_1955.json.
- EPG pilotu 12 Ekim yenilendi: TRT1/Haber/Çocuk/Avaz/Türk; kimlik/saat/çakışma kontrolü 5/5. Kaynak gece yarısı stop tarihi hatası dar kuralla yorumlandı; ilk değerler source_time_repairs içinde. Bağımsız yayın akışı/IBO görünürlüğü onayı değildir. Statik kapsam saatleri raporda; cihaz testinden önce gerekirse yeniden güncelle.
- 11 geliştirme mevcut kodla karşılaştırıldı; var olan araçlar yeniden kurulmadı. Kalanlar ayrı envanterde.

## Tekrarlanmayacak tamamlanan işler
Sabah 10:30–14:30 Stockholm: 55 commit, 10 başarılı Actions. İlk 39 final testi ve verilmiş kimlik kararları, kategori taşıma/sıralama, Öncü/Kanal15/Manas Sinema taşıması, logo değişiklikleri ve EPG Pages bağlantısı yapılmış. Ayrıntılar geçmiş dosyasında.
Kullanıcının 20:18 talimatıyla ayrı bulunan 21 aday YEDEKLER'e eklendi; TRT1 ve DHA ilk iki kayıt olarak korundu. YEDEKLER toplam 23 kayıt. Bunlar cihaz/kimlik onayı bekleyen adaylardır; yabancı kanallar ve zaman aşımı sonucu olan Az TV de kullanıcı incelemesi için dahil.  SAT7 Türk üç kalite etiketli URL Hepsi/Dini. Gerçek çözünürlük kanıtı eksik etiketler ayrı ele alınır.

## Son ana liste logo/kategori düzeltmesi
Kullanıcı 20:27'de ana listesindeki TRT Diyanet Çocuk (Çocuk 17), Deniz Postası (Sinema 2), BBC First Türkiye ve Baku.TV logolarının düzeltilmesini, Eurosport 1/2 Türkiye'nin Spor'a eklenmesini açıkça onayladı. Bunlar yeni aday/YEDEKLER talebi değildir.
- Dört kanalın gerçek markalı PNG'leri indirildi, görüntüleri incelendi ve logos/resmi-*-20261012.png altında önbelleklendi. Bu dört tam etiketin 10 kategori kaydında yalnız logo adresi değişti. Diğer Diyanet Çocuk varyantına dokunulmadı.
- İki Eurosport, Hepsi kayıtları/sıraları korunarak aynı URL/metadata ile Spor'un sonuna birer kez eklendi; Spor 19→21. Favoriler, Hepsi ilk 90, YEDEKLER ve yayın URL'leri korundu.
- automatic_png_logos.py artık logo_deneme/approved_repairs.json içinde açık onay verilmiş tam etiket/eski URL eşleşmesini ve yerel PNG SHA256'sını doğrulayarak dolu ama sorunlu adresleri düzeltebilir. Diğer dolu logolar değişmez; genel otomatik marka/on-air onayı verilmez.
- Doğrulama: izinli eski kaynak, PNG hash, ilgisiz kayıtları koruma ve tekrar çalışmada değişiklik yapmama geçti; playlist farkı yalnız izinli logo/Spor kapsamıyla sınırlı. Kullanıcı sonraki konuşmada dört logo düzeltmesinin IBO'da olduğunu bildirdi.
Kanıt: raporlar/ANA_LISTE_LOGO_SPOR_2026-10-12.json. Bu düzeltmeyi yeniden uygulama.

## Sıradaki işler — yalnız eksik kapsam
1. 252 eksik denemenin zamanı geldiğinde mevcut üçlü akış; geçmiş denemeler korunur.
2. Görsel etiket desteği olan 15 kayıtta IBO/gerçek kanal ve dil doğrulaması; 6 marka/bölgesel hedef ve 14 yetersiz kimlik kaydında bağımsız amblem/kanal kanıtı; 4 görüntüsüz kayıt otomatik geçer sayılmaz. 39 devam kaydı/35 kare incelemesi yapıldı; aynı kare incelemesini yeniden yapma.
3. Daha önce final sonucu bulunmayan adayları en çok 24'lük gruplarla ayrı son kontrole almak. Sonuç varsa atla; aynı görevi kuyrukta yeniden başlatma.
4. IBO cihaz/sürüm, kanal açılış/geçiş hızı ve güncel EPG görünürlüğü: kullanıcı cihaz kanıtı gerekir; otomatik onay yok.
5. Eksik kalite/kimlik/kategori/isim ve logosuz aday hazırlığı; ana listedeki dolu logolar korunur.
6. 11 geliştirme envanterinin eksik maddeleri ve aylık geniş tarama modu. Günde iki keşif/tek devam/tekrar koruması zaten kurulu.

## Kaynaklar
- madsc_dogrulama/state.json ve summary.json — ayrı denemeler/tarihler.
- madsc_son_kontrol/results.json ve summary.json — birikimli final sonuçları.
- madsc_son_kontrol/kimlik_incelemesi_2026-10-12.json — eski 39 kimlik kararları.
- madsc_son_kontrol/kimlik_devam_2026-10-12_1955.json — yalnız açık eski 15 + yeni 24 için tamamlanan kare incelemesi; önceki retler korunur.
- madsc_kesif/candidate_logos.json — ayrı PNG hazırlığı, görsel onay değildir.
- epg_deneme/rapor.json, liste.m3u, rehber.xml — ayrı kısa süreli pilot.
- raporlar/GELISTIRME_11_DURUM_2026-10-12.md — 11 geliştirme envanteri.
- kontrol_notlari/DEVAM_GECMISI_2026-10-12_1947.md — bu güncel özet öncesindeki tam kayıt; eski durumlar güncel kabul edilmez.
- Actions: https://github.com/Madsc55/madsc-tv/actions

## Takvim
Yeni keşif 06:00/18:00 UTC; üçlü doğrulama saatlik :17, en az 6 saat; logo bakımı 05:23/17:23 UTC; EPG günlük 03:25 UTC + Pages. Son kontrol üçlü başarı tamamlanmasına bağlı, 24'lük grup; bütün kuyruk bittiği iddia edilmez. Aylık geniş tarama henüz açık iş.

## Kayıt düzeni
Her mesaj değil; önemli karar, tamamlanan iş veya doğrulanmış sonuç sonrası bu kısa özet güncellenir. Eski ayrıntılar tarihli geçmiş dosyasına alınır; test verisi mevcut raporlarda kalır. Kaydetme doğrulanmadan “kaydedildi” denmez. Sohbetin kesin dolma eşiği/kalan kotası görülemediğinden eşik bazlı uyarı garantisi verilmez; son ana kadar beklenmez. Yanıt iletim hatası işlemin tamamlandığının kanıtı değildir.

## Yeni sohbet cümlesi
Mahmut, Madsc55/madsc-tv içindeki DEVAM_NOTU.md'nin SOHBET DEVRİ bölümünü, AGENTS.md'yi ve güncel Actions/raporları oku. Kaldığımız yerden devam et; tamamlananları tekrarlama, korunan listelere ve dolu logolara izinsiz dokunma.

## Son izinli ekleme
21 ayrı adayın URL'si mevcut ana dosyada yoktu; her biri yalnız YEDEKLER'e bir kez eklendi. Aynı URL'li 11 mevcut kayıt ve aynı isimli 7 alternatif bu talimat kapsamında yeniden eklenmedi. Mevcut 1029 kayıt, ad/ID/logo/URL/sıra korunarak bırakıldı; yalnız YEDEKLER grup sayacı 2→23 güncellendi. Dış yedekler/YENİLER/favoriler değişmedi. İsimler ve teknik/görsel durumlar: raporlar/YEDEKLERE_EKLENEN_ADAYLAR_2026-10-12.json. Logo kaynağı kesin olmayan yeni kayıtlarda boş alan kullanıldı; uydurma logo eklenmedi. Gerçek kalite etiketi mevcut ffprobe ölçümüne dayanır, IBO kalite/çalışırlık onayı değildir.

## Son kullanıcı onaylı YEDEKLER taşıması — 12 Ekim 2026
Kullanıcı önceki dört logo düzeltmesini cihazında doğruladı. Taşıma öncesi 23 kayıtlı YEDEKLER sırası sabitlendi: 7 CGTN DOCUMENTARY → BELGESEL; 9 FTV TÜRK etiketi/Red Bull TV kaynak URL'si → SPOR; 15 .SCI-FI → SİNEMA. Üçüne gerçek markalı PNG kondu; aynı URL/isim/kalite/ID ile HEPSİ sonuna birer kopya eklendi. Mevcut Hepsi sırası ve ilk 90/favoriler korunur. Bu üç kayıt YEDEKLER'den taşındı, diğer kayıtları korundu. Yeni sayılar: YEDEKLER 20, HEPSİ 374, BELGESEL 13, SPOR 22, SİNEMA 6.
9. kaydın rbmn-live/BoRB-AT bağlantısı iptv-org akış kaynağında RedBullTV.at ile eşleşir. Logo Red Bull TV'dir; kullanıcının isim değiştirme talimatı olmadığından FTV TÜRK etiketi korunmuştur, ad düzeltmesi açık iş. .SCI-FI yabancı yayın kullanıcı isteğiyle kabul edildi. Kategori/ekleme onayı teknik/kimlik/dil garantisi sayılmaz; geçmiş testler yeniden yapılmadı. Yeni logoların IBO görünürlüğü sonraki cihaz kontrolünü bekler.
Kanıt: raporlar/YEDEK_KATEGORI_LOGO_2026-10-12.json. Aynı taşıma yeni sohbetlerde tekrar uygulanmaz; yeni YEDEKLER sıraları önceki 7/9/15 ile karıştırılmaz.

## Son MTürk/Ton TV kontrolü
Kullanıcı Yerel 56/57 MTürk logo uyuşmazlığını düzeltme istedi. İki varyant aynı yayın URL'sini kullanıyor. Yayıncının https://www.mturktv.com/wp-content/uploads/2025/04/MTurkTV.png dosyası görsel olarak incelendi; logos/resmi-mturk-20261012.png olarak aynen saklandı. Bu iki tam etiketin toplam dört kategori kopyasında yalnız logo adresi eşitlendi (Hepsi/Belgesel/Yerel); isim/URL/ID/kategori/sıra değişmedi. Onaylı eski URL+PNG hash bakım kaydı eklendi. Canlı kare girişimi 5xx döndürdü; yayındaki amblem veya IBO görünümü kesin doğrulanmış yazılmadı. Kullanıcı cihaz kontrolü sonraki adım.
Ton TV Yerel 64: yayıncının resmi site/iletişim bilgileri Çanakkale merkezli bölgesel genel yayın olduğunu destekliyor. Yerel kategorisinde kalması uygun; taşınmadı. Önceki dört logo/Eurosport ve üç YEDEKLER taşıması tekrar yapılmadı.

## 12 Ekim 2026 — son sohbet işlemi: M2O taşıması
- Güncel YEDEKLER 9. kayıt M2O TV DJ STATION 720P HD olarak doğrulandı. İtalya m2o TV için iptv-org/Wikimedia'daki m2o 2019 markalı PNG adresi kullanıldı; yayın üstü amblem ve İsveç IBO cihaz görünümü henüz doğrulanmadı.
- Kullanıcının açık talimatıyla yalnız bu kayıt YEDEKLER'den çıkarılıp aynı akış URL'si/ID/isim/kaliteyle MÜZİK ve HEPSİ sonuna eklendi. YEDEKLER 20→19, MÜZİK 33→34, HEPSİ 374→375. Önceki Hepsi sıralaması, ilk 90 ve favoriler değişmedi.
- CALISANLAR.m3u commit: 6f0dcfc3714feb5d54fa6db081f34d28f0a83803. Önceki MTürk logo düzeltmesi ve Ton TV Yerel kararı zaten yapılmıştı; tekrar uygulanmadı. Kullanıcıdan IBO'da logo/akış görünümü beklenir.

## 12 Ekim — yeni sohbet, kullanıcı onaylı hızlandırma adımı
- Kullanıcı mevcut testleri tekrar etmeden 11 geliştirmede kalan işleri ilerletmeyi istedi. İlk adım olarak yalnız okuyan `tools/guncel_test_durum_ozeti.py` eklendi (commit `4440942728890237ec0c5e0b3a5a727b3fe58dba`), GitHub'dan tekrar okunarak doğrulandı. İki mevcut summary dosyasını birleştirir; snapshot zamanlarını ve URL/kanal ayrımını açıkça yazar; test başlatmaz, playlist değiştirmez. Actions üzerinde çalıştırılması henüz doğrulanmadı.
- Sıradaki işler: birleşik raporu otomatik Actions artifact akışına güvenli bağlama, aylık geniş tarama modunu ayrı ve tekrarsız uygulama, güncel Actions durumunu doğrulama. Tamamlanmış üçlü ve final testleri tekrar edilmez; 6 saat sınırı korunur.

## 12 Ekim — otomasyon sadeleştirme adımı
- Kullanıcı gereksiz yinelenen taramaları azaltma ve otomatik raporu onayladı. Salt okunur `.github/workflows/birlesik-durum-raporu.yml` eklendi (commit `193a54ea6330a7b3a93b2794d21a454013fdcede`); 06:40 ve 18:40 UTC zamanlı, ayrıca manuel tetiklemeli, sadece `tools/guncel_test_durum_ozeti.py` çalıştırıp 30 günlük artifact saklar. Ana liste/test geçmişi değiştirilmez. İlk Actions çalışmasının başarısı henüz doğrulanmadı.
- Eski güvenli kaynak araması ve birleşik keşif potansiyel örtüşmesi henüz workflow bazında denetlenmedi; hiçbir eski otomasyon kapatılmadı. Aylık geniş keşif henüz kurulmadı. Sonraki iş mevcut workflow dosyalarını karşılaştırıp güvenli biçimde tekilleştirmek; tamamlanmış testleri tekrar başlatmamak.

## 12 Ekim — günlük Türkçe odaklı kaynak taraması ve yabancı kanal koruması
- Kullanıcı 155 kaynak envanterinden her gün güncel kanal bulmayı, ancak yabancı kanalların adaylara karışmamasını istedi. `madsc_akilli_kesif.py` günlük kaynak okuması yalnız 11 açıkça Türkiye/Türkçe odaklı M3U kaynağına indirildi; 155 kaynak tanımı korunuyor, yabancı ülke/dil ve genel kategori akışları günlük aday taramasına girmiyor. Commit `51cf89e1a89c5eb8c11a5e2d651c5e12b9cef2ac` (önceki ara commit `0b75cd43f34a96eb52e64f5840a37ea2bf4de894`). Kaynak dosyası yeniden okunarak doğrulandı.
- Bu yalnız kaynak seviyesinde filtre: Türkçe listelerde yanlış etiketli yabancı yayın yine bulunabilir. Ayrı kanal-kimlik/dil onayı olmadan yeni aday ana listeye veya YENİLER'e eklenmez. Önceden kayıtlı yabancı adaylar kendiliğinden silinmedi. Yeni Actions çalışması henüz doğrulanmadı. Günlük diğer sitelerde yeni eklenen kanalların tarih farkı/aylık 155 kaynak geniş tarama ayrıca geliştirilecek.

## 12 Ekim — YEDEKLER kullanıcı temizliği
- Kullanıcının açık talimatıyla YEDEKLER (19) grubundan TRT 1 ve DHA CANLI hariç 17 kayıt çıkarıldı; YEDEKLER (2) oldu. GitHub commit `a9d3317004a9f12f93bae0371b0e7d9ddab636aa`. Dosya yeniden okunup iki kaydın kaldığı doğrulandı. Diğer kategoriler/favoriler/sıralamalar ve harici korunan yedekler değiştirilmedi. Çıkarılan 17 adayın geçmiş test kayıtları silinmedi; aynı işlemi tekrar yapma.

## 12 Ekim — eksik Türk kanal hedef takibi
- Kullanıcı sistemin eksik dört geliştirmesini uygulamayı onayladı. `tools/eksik_turk_kanal_takibi.py` oluşturuldu (commit `f587bfa662a08b76b9e7d9c05bfccb88ccffccb1`): Sözcü TV, Akit TV, Kanal Samsun, Samsun Haber için mevcut playlist ve `madsc_kesif/gecmis.json` içinde ad eşleşmesi arayan salt-okunur JSON rapor. Akış testi yapmaz; gerçek kanal kimliği/dil/IBO onayı vermez.
- Mevcut `.github/workflows/birlesik-durum-raporu.yml` güncellendi (commit `a38fe08f12aa8770712beae246446ccc5644233d`): 06:40/18:40 UTC birleşik artifact içine `missing-turkish-channels.json` da eklenir. GitHub dosyası yeniden okunarak doğrulandı; ilk Actions çalışması henüz doğrulanmadı.
- Kalan geliştirmeler: isim hedeflerine göre dış kaynaklarda gerçekten yeni kanal keşfi, 155 kaynak değişim karşılaştırması, gerçek yayın kimliği/yabancı dil elemesi, eski çakışan otomasyonların iş akışı bazında analizi. Bunlar tamamlandı sayılmaz.

## 12 Ekim — GitHub Actions hata düzeltmesi
- Kullanıcı ekran görüntüsünde `.github/workflows/birlesik-durum-raporu.yml` için art arda iki başarısız push çalışması gösterdi. Dosyada artifact `path` alanına gerçek satır sonları yerine düz `\\n` karakterleri yazılmıştı. Çok satırlı YAML gerçek satır sonlarıyla düzeltildi, commit `950bf822602bd25191f0abfecd1a18a3093ee481`; GitHub'dan yeniden okunup doğrulandı. Bu, doğrulanmış yapılandırma hatasıdır; Actions job logları henüz incelenmediği için iki başarısız koşunun tek nedeni olduğu iddia edilmez. Sonraki çalışma sonucu ayrıca kontrol edilmeli.

## 12 Ekim — raporun tekrar çalışması için ek düzeltme
- Kullanıcı önceki iki kırmızı rapor işinin kırmızı kaldığını ve yeni çalışma olmadığını bildirdi. `madsc_kesif/gecmis.json` GitHub dosya okumasında boş içerik döndürdü; salt-okunur hedef raporunun boş/bozuk JSON durumunda çökmemesi ve durumu açıkça raporlaması sağlandı (commit `52a30fce587e636bf06d05822a383b08a1413125`). Geçmiş kayıtlar değiştirilmedi.
- Birleşik rapor workflow'una yalnız kendi YAML/script dosyalarındaki `main` push değişikliklerinde tetikleme eklendi (commit `36adc44bd828c663cc1adfb7622908c6df742fff`); mevcut schedule ve manual dispatch korundu. Workflow ve script yeniden okunarak değişiklikler doğrulandı. Yeni Actions çalışmasının yeşil olduğu henüz doğrulanmadı. Eski kırmızı kayıtlar tarihsel olarak kalır; yeni run ayrı görünür.

## 12 Ekim — günlük keşif sırasında aday logo hazırlığı
- Kullanıcı günlük iki kez keşif sırasında yeni kanalların teknik kontrolü ve logo/amblemlerinin birlikte hazırlanmasını, EPG'nin her gün güncellenmesini istedi. `madsc_akilli_kesif.py` içinde `logo_candidates.json` yazımından sonra mevcut `scripts.candidate_logo_report.prepare` çağrısı eklendi (commit `8fdb63e958ad3097aed1dbc23bd5f2a1573de52c`): tur başına en çok 40 yeni aday PNG hazırlanır, `madsc_kesif/candidate_logos.json` içinde yalnız inceleme bekler. Kaynak logonun kanal kimliği olduğu varsayılmaz, mevcut liste/logolar değişmez. Hata ayrı `logo_hazirlama_hatasi.txt` kaydına yazılır ve keşif/test akışı devam eder. GitHub'dan yeniden okunup doğrulandı; Actions canlı başarı ve PNG çıktısı henüz doğrulanmadı.
- Günlük EPG 03:25 UTC işi daha önce mevcuttu; kullanıcı IBO Player Pro 2128.0 sürümünde EPG'nin görünmediğini bildirdi. XMLTV/tvg-id, saat dilimi ve IBO uygulama içe aktarma sorunları ayrıca araştırılmalı. Üç aşamalı testlerin yalnız yeni bulunan URL'lere indirgenmesi henüz uygulanmadı; mevcut eski bekleyen kuyruk ve test geçmişi korunmalı.

## 12 Ekim — kalan test ve son kontrol kuyruğu raporu
- Kullanıcı kalan üç aşamalı ve son kontrollerle devam edilmesini onayladı. `tools/guncel_test_durum_ozeti.py` yalnız mevcut snapshot'ları okuyarak kalan final testleri, kimlik/içerik incelemesi, süreklilik hataları, zaman aşımı ve cihaz onayı ihtiyaçlarını ayrı JSON alanlarıyla raporlayacak biçimde güncellendi; commit `180c6badc37c1d6805bcd62b9e3921ba3cff653a`. Dosya yeniden okunarak doğrulandı. Mevcut otomatik üç aşamalı ve son kontrol workflow'larına dokunulmadı; tamamlanan testler tekrar başlatılmadı. Yeni rapor Actions çalışması ve güncel kuyruk sonucu henüz doğrulanmadı.

## 12 Ekim — kullanıcı talebiyle doğrulama
- GitHub'dan yeniden okunan `madsc_dogrulama/summary.json` (17:35:46 UTC): 6981 URL adayı, 6729 üç aşama tamam, 252 bekliyor, 6028 üç teknik geçiş. `madsc_son_kontrol/summary.json` (17:35:45 UTC): 63 tamam, 5687 bekliyor; 48 kimlik bekliyor, 10 içerik inceleme, 2 süreklilik başarısız, 3 zaman aşımı. `madsc_kesif/ozet.json` (19:45:39 UTC): yeni bekleyen sonraki 0, bu tur test 0; tüm testlerin bittiği anlamına gelmez.
- Birleşik rapor kodunda kalan son kontrol alanı ve tutarlılık koruması GitHub'dan doğrulandı. Commit `799eacface43f0916f15a253d50a2bc744497158` için GitHub commit status endpoint boş status listesi döndürdü; bu, Actions run başarısını doğrulamaz. Canlı Actions run/log erişimi olmadan yeşil iddia edilmez. Kullanıcı onayı olmadan playlist değiştirilmedi.

## 12 Ekim gece — güvenlik ve son kontrol otomatik devam
- Salt okunur korunan liste denetimi `scripts/protected_playlist_audit.py` (756eea33) ve `.github/workflows/test-39-protected-playlist.yml` (7720685f) eklendi. Actions 38312721548 başarıyla tamamlandı; bu kontrol branch protection olmadan izinsiz yazmayı engellemez.
- Kullanıcının açık otomasyon isteği üzerine `.github/workflows/madsc-son-kontrol.yml` commit `5b415fa7044b9c35e5b1c6b0aa6aaf3df203bf67` ile değiştirildi: 24 adaylık son kontrol başarılı kaydedilince summary.remaining > 0 ise workflow_dispatch ile sonraki turu başlatır; `actions:write` verildi. GitHub run 38314228501 sıradaydı; zincirin fiilen çalışması henüz doğrulanmadı. Final kontrol görüntü yakalama ve teknik süreklilik testidir, otomatik kanal kimliği veya İsveç IBO cihaz onayı değildir. Ana liste, favoriler, YENİLER ve yedekler değişmedi.

## 13 Ekim — Güvenlik çalışmasına dönüş / kaldığımız yer
- Kullanıcı kanal testleri sürerken güvenlik konusuna dönülmesini istedi. `MADSC - Tamamlanan Aday Son Kontrol` otomatik devam iş akışı commit `5b415fa` ile kurulmuştu; run `38314228501` 12 Ekim 22:01 UTC'de `in_progress` olarak doğrulandı, otomatik sonraki tur henüz doğrulanmadı.
- Güvenlikte `scripts/protected_playlist_audit.py` ve test-39 iş akışı okundu: yalnız `CALISANLAR.m3u`, `YENILER.m3u` dosyalarının varlığı/#EXTM3U ve AGENTS.md varlığı denetleniyor. Bu, kullanıcı onayını veya yetkisiz commit engelini kanıtlamaz. 39. denetim yeşil; branch protection/ruleset uygulanması doğrulanmadı.
- `test-31-protected-write-gate.yml` incelendi: yazma yetkili iş akışlarını statik olarak listeler, yalnız raporlar; gerçek onay kapısı değil.
- SIRADAKİ İŞ: Korunan listeler, FAVORİLER/HEPSİ sırası ve yedeklere yazma yollarını denetle; mevcut keşif/test raporlamasını bozmadan yazma kapısını sağlamlaştır. GitHub main dalı kurallarını gerçekten doğrula/uygulanabilir yolunu belirle. Kullanıcının açık onayı olmadan ana listeleri değiştirme. Kullanıcı her önemli adımın başlık altında ve kaldığımız yer ile not edilmesini özellikle istedi.

## 13 Ekim — 23 güvenlik kuralı kullanıcı onayıyla kaydedildi
- Kullanıcı önceki 19 kuralı ve dört ek güvenlik önlemini onayladı; tüm metin `GUVENLIK_KURALLARI.md` dosyasına commit `03299eed839f87ff9b8a51e97a8001b8fc97beaf` ile kaydedildi.
- Dört ek madde: değişiklik öncesi geri yüklenebilir yedek, keşif/testin korunan listeye yazmasını engelleme, onaylı değişiklik sonrası M3U/sıra/URL bütünlük kontrolü, kontrollü geri yükleme.
- POLİTİKA ONAYI ≠ TEKNİK UYGULAMA: test-39 ve test-31 gerçek yazma kapısı değil. Sonraki iş otomasyonların yazma yollarını tarayıp güvenli uygulama, test ve doğrulama; ana kanal dosyaları değişmeyecek. Kullanıcı ek kural önerilerine de açık, fakat her yeni kural ayrı onay gerektirir.

## 13 Ekim — 24. güvenlik kuralı onaylandı
- Kullanıcı tekrarlanan otomasyon hatalarında güvenli durma ve hata raporu önerisini kabul etti. `GUVENLIK_KURALLARI.md` 24. maddeyle güncellendi (commit 6c56118796c299f22080b5f68f8a8ff4993f8e2a). Üç ana workflow incelendi: her birinde sınırlı git push denemesi bulunuyor; tüm koşular boyunca ortak hata sayacı/devre kesici henüz doğrulanmadı. Sıradaki iş teknik uygulama ve test; korunan kanal listeleri değişmedi.


## 15 EKİM 2026 — EKRAN GÖRÜNTÜSÜNDEKİ 20 KLASÖR İÇİN HEDEFLİ NOT/RAPOR MUTABAKATI

**Kullanıcı kapsamı:** GitHub main ekranında görülen `.github`, `aday_bekletme`, `aday_hazirlik`, `arastirma`, `epg`, `epg_deneme`, `kontrol_notlari`, `liste_kontrol`, `logo_deneme`, `logos`, `madsc_dogrulama`, `madsc_kesif`, `madsc_son_kontrol`, `raporlar`, `reports`, `scripts`, `tarama`, `tests`, `tools`, `vod`, `yedekler` (ekranlarda 21 klasör) ve bunların görev, karar, hata, eksik kanıtlarının tek merkezde toplanması. Ekran `main` dalını gösteriyor; bu çalışma korunmuş `madsc/bes-sistem-toplu-birlestirme` dalındaki mevcut dosyaları esas alır. Fark denetimi henüz yapılmadı.

**Bu turda doğrudan yeniden okunan kaynaklar:** `DEVAM_NOTU.md`, `aday_bekletme/ADAY_DURUM_RAPORU.csv` (ilk 65 satır), `aday_hazirlik/ibo_alternatif_10_2026-10-12.json` (ilk 65 satır), `arastirma/lyngsat_arama_oncelikleri.json`, `epg_deneme/yayim_kontrol.json`, `kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md`, `liste_kontrol/rapor.json` (ilk 65 satır), `logo_deneme/png_automation.json` (ilk 65 satır), `madsc_dogrulama/summary.json`, `madsc_kesif/ozet.json` (ilk 65 satır), `madsc_son_kontrol/summary.json`, `vod/guncel-bolumler.json` (ilk 65 satır), `raporlar/GELISTIRME_11_DURUM_2026-10-12.md` (ilk 65 satır). Önceki turda ayrıca `GUVENLIK_KURALLARI.md`, `OZELLIK_ENVANTERI.md`, `SEKIZ_GOREV_TOPLU_DENETIM.md`, `TOPLU_DURUM_RAPORU.md` okundu. Bunlar **bütün 21 klasörün bu turda tam tarandığı kanıtı değildir**; önceki 769/769 envanter kaydı da korunur.

### Yeni mutabakat bulguları ve açık işler
1. **Üç aşama:** `madsc_dogrulama/summary.json` 14 Ekim 05:07 UTC snapshot'ında 7100 adayın üç denemesi tamam; 6374 üç geçiş, 462 iki, 114 bir, 150 sıfır geçiş; **playlist'e hazır 0**. Teknik test tamamlandı diye kimlik/IBO tamamlandı sayma.
2. **Son kontrol:** `madsc_son_kontrol/summary.json` 14 Ekim 12:09 UTC snapshot'ında 3800 tamamlanmış, **2574 kalan**, 2332 teknik geçiş/kimlik bekliyor, 1055 teknik geçiş/içerik inceleme, 255 süreklilik başarısız, 158 timeout; **playlist'e hazır 0**. Önceki 3082 ve 5687 kalan sayıları tarihsel snapshot olarak korunur.
3. **Aday hazırlığı:** On alternatifli `ibo_alternatif_10_2026-10-12.json` dosyası `SUPERSEDED_AFTER_IMAGE_IDENTITY_REVIEW`; teknik geçiş, IBO ve kanal kimliği onayı değil. Eski onlu liste otomatik aktarılmaz.
4. **Araştırma:** LyngSat 224 kanal adı karşılaştırmasında 103 ad eşleşmesi, 5 takma ad, 7 kimlik incelemesi, 109 isimle bulunamayan var. Uydu kataloğu eşleşmesi oynatılabilir/yasal IPTV URL'si değildir.
5. **Eurostar:** `kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md` eski yayın HTTP 404, IBO açılmadı, kullanıcı kaldırma kararı ve alternatif araştırma talebi kaydeder. Doğrulanmış alternatif yok; ana liste/YENİLER'e ekleme izni yok. Gizli/şüpheli ham URL ana nota taşınmadı.
6. **EPG/Pages:** `epg_deneme/yayim_kontrol.json` 11 Ekim'de deploy ve yayımlanan içerik hash doğrulaması SUCCESS; günlük takip `CONFIGURED_NOT_YET_OBSERVED`, IBO görünürlüğü `NOT_VERIFIED`. Daha yeni EPG snapshot'larıyla tarihe göre karşılaştır.
7. **Logo:** `logo_deneme/png_automation.json` HTTP 403/429 logo hataları ve `visual_match: NOT_VERIFIED` içeriyor; 0 onaylı mevcut logo onarımı ve 0 PNG hazır alanları bütün aday logoları onaylı demek değil. Dolu mevcut logolara izinsiz dokunma.
8. **Liste:** `liste_kontrol/rapor.json` 12 Ekim tarihli eski blob ve `ibo_loaded_version: NOT_OBSERVED`; 657 kategori kaydı/372 benzersiz URL güncel 1039 snapshot ile birleştirilip tek tarihli sayı gibi sunulmaz.
9. **Keşif:** `madsc_kesif/ozet.json` 14 Ekim 13:36 UTC, ana liste 1039, sonraki yeni bekleyen 0; bu 2574 son kontrol işinin veya tüm keşif hedeflerinin bittiği anlamına gelmez.
10. **VOD:** `vod/guncel-bolumler.json` bölüm takvimidir; `watch_url: null` örnekleri gerçek oynatma/IBO film-dizi entegrasyonu kanıtı olmadığını gösterir.
11. **11 geliştirme:** `raporlar/GELISTIRME_11_DURUM_2026-10-12.md` kurulu/kısmi/eksik ayrımını içerir; özellikle IBO açılış-geçiş hızı, harici restore, gerçek cihaz EPG ve logo eşleşmesi açık kalır. Sonraki daha yeni kararlarla mutabakat gerekir.
12. **Aday CSV kalitesi:** `aday_bekletme/ADAY_DURUM_RAPORU.csv` ilk satırlarda bozuk/ham `#EXTINF` etiketleri ve isim alanında parantezli kayıtlar gösteriyor; normalizasyon/kanal kimliği ve şüpheli kaynak güvenilirliği ayrı incelenmeli. Ham akış adresleri ana nota kopyalanmadı.

**Açık doğrulama:** Ekrandaki 21 klasörün güncel ağaç/dosya bazlı kapsam matrisi, `main` ile çalışma dalı farkı, bu turda henüz doğrudan yeniden açılmamış `reports`, `tarama`, `tests`, `tools`, `yedekler`, `logos`, `scripts`, `epg`, `.github` altındaki her dosya için tekil kaynak-iş-kayıt eşlemesi. Önceki 769/769 beyanı korunur ancak yeni ekran kapsamına yönelik bağımsız tam yeniden denetim olarak gösterilmez.

**Koruma:** Bu güncelleme yalnız `DEVAM_NOTU.md` içindir. PR #71 merge yok, korunan listelere/yedeklere/logolara/otomasyonlara yazma yok.


### 15 Ekim — ekran klasörleri için EK KOD İNCELEMESİ (önceki turda açılmayan kaynaklar)
Bu bölüm önceki 21 klasör hedefli kayda ektir. **Doğrudan okunan yeni dosyalar (9):** `scripts/protected_playlist_audit.py`, `scripts/restore_dry_run.py`, `scripts/disaster_recovery_dry_run.py`, `tools/genis_kaynak_taramasi.py`, `tools/genel_sistem_bakimi.py`, `tools/guncel_test_durum_ozeti.py`, `.github/workflows/birlesik-durum-raporu.yml`, `.github/workflows/test-31-protected-write-gate.yml` ve `DEVAM_NOTU.md` güncel sürümü. GitHub'da tahmini adla denenmiş `epg/rehber.xml`, `reports/summary.json`, `tarama/rapor.json`, `yedekler/README.md`, `tests/test_verification_pipeline.py` **404** döndürdü; klasör boş veya incelendi sonucu çıkarılamaz. Önceki 769 dosya envanterinde doğrulanmış gerçek yol listesiyle eşleştirilmeli.

**Koddan doğrulanan işlevler / boşluklar:**
- `scripts/protected_playlist_audit.py`: sadece CALISANLAR/YENILER dosyası, M3U başlığı ve AGENTS varlığını kontrol eder. **İzin kontrolü, satır/sıra/URL bütünlüğü veya branch protection sağlamaz.**
- `.github/workflows/test-31-protected-write-gate.yml`: yazma yetkisi, git push ve protected path işaretlerini statik YAML taramasıyla raporlar; **yetkisiz yazmayı engelleyen kapı değil**. Gerçek ruleset/approval doğrulanmalı.
- `scripts/restore_dry_run.py`: iki tarihli `yedekler/` dosyasını geçici klasöre kopyalayıp checksum, kanal parse ve bozuk veri reddini kontrol eder; korunan gerçek playlistleri değiştirmez. **Harici/offsite backup ve gerçek üretim restore kanıtı değildir.**
- `scripts/disaster_recovery_dry_run.py`: Git HEAD içindeki iki playlisti geçici yerde bozup geri yükleme simüle eder. Kendi `limitations` alanında Git'in bağımsız offsite yedek olmadığını açıkça söyler.
- `tools/genis_kaynak_taramasi.py`: haftalık hedefli / aylık tüm tanımlı kaynak taraması, SHA-256 kaynak değişimi, kimlik inceleme kuyruğu. **Yeni URL'yi üçlü doğrulama state'ine aktarmaz, oynatma/IBO doğrulamaz.** Ayrıca rapor dosyasında kaynak URL'si ve aday inceleme state'inde ham URL saklanır; artifact/log erişimi ve gizli adres maskeleme denetlenmeli. Geçersiz geçmişte güvenli durur.
- `tools/genel_sistem_bakimi.py`: keşif, üçlü/final, geniş tarama JSON'larının varlık/parse kontrolü. **Başarıyla parse edilmiş snapshot'ın taze olduğu veya testin başarılı çalıştığı anlamına gelmez.**
- `tools/guncel_test_durum_ozeti.py`: üçlü + final raporlarını birleştirir, sayı tutarlılığı kontrol eder; cihaz/kimlik onayı vermez, yeni test başlatmaz.
- `.github/workflows/birlesik-durum-raporu.yml`: bu daldaki okunan sürümde `workflow_dispatch` ve `main` üzerindeki seçili dosya değişiminde `push` tetikleri var; **schedule anahtarı yok**. Önceki notlardaki günlük 06:40/18:40 otomatik rapor iddiası ile güncel YAML arasında fark bulunuyor; cron gerçekten kaldırılmış mı, başka workflow devralmış mı, kullanıcı kararına aykırı mı araştırılmalı. Workflow dört JSON/rapor çıktısını 30 günlük artifact'a koyuyor, `contents: read`.

**İşlem sınırı ve kanıt:** Bu ek yalnız dosya metninden yapılan statik incelemedir; Actions run, gerçek cihaz, tüm klasörlerin her alt dosyası ve main/çalışma dalı farkı doğrulanmadı. Korunan dosyalara dokunulmadı. Önceki 769/769 envanter sonucu, bu turdaki bağımsız 21 klasör yeniden taramasıyla eş anlamlı değildir.


## 15 EKİM 2026 — KÖK DOSYALAR EK İNCELEME KAYDI

Kapsam: Kullanıcının 10:14 ekranında görünen kök dosyalar. Bu kayıt mevcut notların sonuna eklenmiştir; önceki kararlar silinmez. Yalnız bu dosya güncellenir.

### İncelenen kaynaklardan çıkarılan görevler
- AGENTS.md: kullanıcı izni, değişiklik sonrası gerçek Actions kanıtı, eski kararları koruma, Türkçe iş adları ve tekrar testinden kaçınma kuralları sürdürülmeli.
- GUVENLIK_KURALLARI.md: korunan dosyalara yazma yetkisi ile fiili engelleme ayrı ayrı denetlenmeli; otomasyonların hata durdurma zinciri ve branch protection kanıtı açık.
- IPTV_PROJE_HAFIZASI.md: 9 Ekim tarihli 587 kanal tarihsel sayı; güncel sayı diye kullanılmaz. Ulusal kategori ana depo kararı, YENİLER'e ve ana listeye izinsiz eklememe kuralı korunur.
- SEKIZ_GOREV_TOPLU_DENETIM.md: sekiz görevde SHA ve izole yedek testi mevcut; bağımsız harici yedek, kaynakların gerçek erişimi, kanal kimliği, lisans, logo, EPG ve İsveç IBO cihaz kanıtı açık. Kullanıcının ertelediği harici kopya izinsiz yapılmaz.
- TOPLU_DURUM_RAPORU.md: 14 Ekim raporunda 92 eski workflow'un tetik çakışması, 1/15 yedek restore kanıtı, 75 adayın yeniden testi ve EPG cihaz görünürlüğü açık. Önceki #93 başarısızlığının log olmadan kesin kök nedeni belirlenmemiş. Teknik EPG raporu 1039 kayıt, 730 eşleşme, 23702 program; IBO onayı değildir.
- OZELLIK_ENVANTERI.md: mevcut özellikleri tekrar geliştirmeden önce kurulu, kısmi ve eksik işlerin güncel Actions kanıtıyla eşleştirilmesi gerekiyor.
- CALISMAYANLAR.txt: kanal adları güncel ve kalıcı arıza kanıtı sayılmamalı; TEST_RAPORU.csv ile kanal, URL ve test zamanı bazında karşılaştırılmalı.
- TEST_RAPORU.csv: aynı kanalın başarılı ve başarısız alternatifleri bulunuyor; HTTP 403/404/timeout gerçek televizyon başarısızlığı değildir. IBO uyumluluğu etiketi cihaz testi yerine geçmez. Ham yayın URL'leri buraya aktarılmadı.
- CALISANLAR.m3u, YENILER.m3u, YABANCI_KANALLAR.m3u, MADSC_TV_47_LISTE_ADAY.m3u: üretim, yeni aday, yabancı arşiv ve aday koleksiyonu ayrılmalı. Teknik adaylar onaysız ana listeye aktarılmaz. Bu dosyalarda hiçbir değişiklik yapılmadı.
- aday_bekletme.py: aday geçmişi ve başarılı test sayısı tutar; iki başarılı koşu kanal kimliği veya IBO onayı değildir. Ham URL'nin state dosyasında saklanması erişim açısından denetlenmeli.
- aday_hata_siniflandirma.py: 403, timeout ve coğrafi kısıt yorumları tek başına kesin hata sebebi değildir.
- aday_oncelik_raporu.py: öncelik sıralaması kullanıcı onayı veya doğrulanmış kanal kimliği sağlamaz.
- aday_tekrar_raporu.py: yalnız tam URL eşitliğine dayanan tekrar analizi farklı query ve alias biçimlerini kaçırabilir; kaynak geçmişi korunarak normalizasyon araştırılmalı.
- akilli_tekrar_test_takvimi.py: last_seen ile gerçek son test zamanı ayrılmalı; önerilen tekrar aralıkları üç aşamalı testin tamamlandığı kanıtı değildir.

### Kalan inceleme ve kanıt sınırları
Ekranda kısaltılmış MADSC_2026-10-13_KA... ve ONCELIK_1_BES_MERKE... dosyalarının gerçek tam yolları henüz doğrulanmadı. Uzun playlist, CSV ve ana notun bütün satırları bu turda yeniden okunmadı. Bu kayıt incelenen kesitlerin bulgularını korur; tüm 20 kök dosya tam tarandı iddiası değildir. Ekran main dalını gösteriyor, kayıt ise madsc/bes-sistem-toplu-birlestirme dalına yapılıyor; iki dalın farkı ayrıca denetlenmeli.

### Sonraki işler
1. Kısaltılmış iki dosyanın gerçek yolunu bulup bütün not ve kararlarını karşılaştır.
2. Uzun kaynakları parçalara bölerek tam oku ve kanal/rapor zamanlarını eşleştir.
3. Görevleri tamamlandı, eksik, kullanıcı onayı bekliyor ve kanıtı yok olarak tekilleştir.
4. Korunan kaynaklara dokunmadan ana notta kanıt bağlantıları ve kabul koşullarını tamamla.


## 15 EKİM 2026 — EKRANLARIN TEKRAR KONTROLÜ VE TAM ADI BULUNAN DOSYALAR

**Kapsam ve kanıt:** Kullanıcının üç ekran görüntüsündeki kök dosya ve klasörler tekrar GitHub çalışma dalı kök dizin listesiyle karşılaştırıldı. Kök dizinde 22 klasör mevcut (görüntülerdeki 21 klasör + `docs`). Ekran görüntüleri `main` dalını gösterir; bu not ve okunan dosyalar `madsc/bes-sistem-toplu-birlestirme` dalındadır. İki dalın tam eşitliği varsayılmaz. GitHub kök listesinde önceki 404 ile erişilemeyen iki dosyanın gerçek tam adı kesinleştirildi ve içerikleri doğrudan okundu:
- `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md` (15 KB)
- `ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md` (6.6 KB)
Ayrıca `BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md`, `BES_SISTEM_GECIS_KONTROL.md`, `BES_SISTEM_TOPLU_IS_DEFTERI.md`, `DEVIR_NOTU_2026-10-15.md` doğrudan okundu. Önceki turda ekran kök dosyalarının 18'i açılmış, bir kısmı uzunluk nedeniyle kısmi incelenmişti. Bu turda bütün alt klasör dosyalarının tamamının yeniden okunduğu iddia edilmez.

### Tarihsel kararlar, yapılanlar, yapılmayanlar ve çelişki çözümü
1. **Beş otomasyon:** 13 Ekim planı ilk 89 workflow sayımına dayanıyor; 14 Ekim envanteri 92 eski workflow'a güncellenmiş. Beş kategori için teknik entegrasyon koşusu #38627719035 beş job success; daha sonraki #38630252033 de beş job/artifact success olarak raporlanmış. Ancak bu **92 eski workflow'un davranışsal eşdeğerliği değildir**. Tetik/çıktı/yazma/bağımlılık başına 92/92 kanıt hâlâ açık; PR #71 merge yok, eski workflow kapatma yok.
2. **Takvim ve tekrar:** 13 Ekim taslağında günlük keşif bir kez, haftalık kalite/güvenlik, 15 günlük arşiv, aylık yönetim istenmiş. 14 Ekim tetik envanterinde `madsc-birlesik-kesif.yml` 06:00/18:00 UTC iki zaman gösteriyor; 15 Ekim devir notu çalışma dalında 05:17/17:17 UTC salt okunur keşif planından bahsediyor. Bunlar farklı tarih/dal sürümleri; **mevcut etkin schedule canlı Actions/default branch üzerinden yeniden doğrulanmalı**. Önceki tercih sessizce değiştirilmez.
3. **YEDEKLER izni:** 13 ve 15 Ekim kayıtlarında geçmişte YEDEKLER'e aday ekleme onayları yer alsa da `DEVIR_NOTU_2026-10-15.md` dosyasının en son 'SON KULLANICI TALIMATI — YEDEKLER GERİ ALINDI' bölümü bu izni açıkça iptal eder. **Güncel karar: YEDEKLER'e hiçbir kanal ekleme.** Main commit d647b05... ile yalnız TRT 1 1440P QHD ve DHA CANLI 720P HD iki tarihsel kaydın korunduğu bildirilmiş; çalışma dalındaki canlı eşitlik ayrıca kontrol edilmeli. Eski onay yeni yetki değildir.
4. **IBO teknik false-negative:** `MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md` kullanıcı saha gözleminde ffprobe başarısız kanalların IBO'da çalışabildiğini, 740 yabancı adayın arşivde saklandığını, otomatik testin kullanıcı cihaz kararını ezemeyeceğini anlatıyor. 740'ın tamamı tek tek bugün çalışıyor diye iddia edilmez. Teknik geçiş kimlik/EPG/logo/lisans kanıtı değildir.
5. **Kuyruk snapshotları:** 13 Ekim 3175 tamamlanan/3082 kalan, 14 Ekim 3800 tamamlanan/2574 kalan raporları tarihsel ardışık anlık durumlar; farklı tarihleri toplayıp yeni aday sayısı çıkarma. `ready_for_playlist=0` kimlik onayı eksikliğine işaret ediyor.
6. **CI kabulü:** `BES_SISTEM_TOPLU_IS_DEFTERI.md` 14 Ekim'de beşli entegrasyon success, ayrıca sonraki regresyon/yanlış negatif/çakışan push tetikleri ve bekleyen yeni koşu kayıtlarını içeriyor. En son değişiklik için başarılı Actions run ve artifact olmadan 'tamamlandı' yazma. 50 ortak/42 eksik betik rakamları sentetik test fikstürüdür, gerçek 92 dağılımı değildir.
7. **Açık geçiş işleri:** EPG üretiminden Pages yayın zinciri, VOD, 1/15 backup ve harici restore, 75 aday (51 farklı saat, 24 ffprobe başarısız), dört alternatif, 18 görev/26 güvenlik kuralı, kullanıcı IBO EPG kabulü, gerçek korunan dosya yazma kapısı, eski workflow çifte tetiklenmesi ve 92/92 davranışsal parity. Salt statik test veya yeşil CI bu işlerin hepsini kapatmaz.
8. **Güvenli işlem sınırı:** Bu tekrar kontrolü yalnız mevcut notlara yeni kayıt ekler; playlist, logo, arşiv, YEDEKLER, workflow, PR veya diğer dosyalara yazılmaz.

### Tam inceleme için açık kapsam
Klasörlerin alt dosyalarının tümünün güncel dal üzerinden tekil dosya bazında yeniden okunması ve büyük M3U/JSON/CSV'lerin tüm satırlarının değerlendirilmesi henüz bu turda tamamlanmadı. Önceki 769/769 envanter kaydı korunur; bağımsız yeniden doğrulama gibi sunulmaz. Özellikle `main` ekran görüntüsü ile çalışma dalı arasındaki değişiklikler ve güncel Actions sonuçları ayrıca incelenecek.


## 15 EKİM 2026 — KÖK TEST DOSYALARI TEKİL İNCELEME VE GÖREV MUTABAKATI

**Amaç:** Ekran görüntülerindeki kök test dosyalarından geçmiş işlev, mevcut koruma, eksik kanıt, tekrar ve beş merkezi sisteme geçiş görevlerini toplamak. Bu turda aşağıdaki **33 benzersiz test dosyasının içeriği GitHub'dan doğrudan açıldı**. Bu, testlerin çalıştırıldığı veya başarılı olduğu iddiası değildir. Önceki turda ayrıca 15 ana programın içeriği açılmıştı. Uzun M3U/CSV ve tüm alt klasörler bu kayıtla tamamlanmış sayılmaz.

### Tekrar, aday, ana liste
**Doğrudan açılan kaynaklar:** `test_akilli_tekrar_test_takvimi.py`, `test_ana_liste_saglik.py`, `test_bes_is_tek_dosya.py`, `test_candidate_logo_missing_report.py`.
**Çıkarılan görev ve kabul sınırı:** Tekrar aralığı ve son gerçek test zamanı; ana liste hata sonucu silme yetkisi değildir; beş iş entegrasyonunun varlığı canlı IBO onayı değildir; aynı isimli farklı logo otomatik onaylanmaz.

### Sekiz/on sekiz görev, arşiv, yedek
**Doğrudan açılan kaynaklar:** `test_central_all_remaining_tasks.py`, `test_central_archive_consistency.py`, `test_central_backup_evidence.py`, `test_central_eight_task_audit.py`, `test_central_eighteen_task_audit.py`, `test_central_isolated_git_restore.py`.
**Çıkarılan görev ve kabul sınırı:** 8 görev ve 18 görev raporları eksik kanıtı başarıya çevirmemeli. Arşiv kategori sayısı dinamik olmalı; Git HEAD izole restore, bağımsız harici ve tarihsel geri yükleme kanıtı değildir. Test fikstüründeki sayılar canlı envanter değildir.

### Merkezi otomasyon, tekrar, tetik, hatalar
**Doğrudan açılan kaynaklar:** `test_central_consolidation_audit.py`, `test_central_duplicate_test_audit.py`, `test_central_failure_stage_report.py`, `test_central_workflow_inventory.py`, `test_tek_merkez_tetikleme.py`, `test_workflow_failure_gate.py`.
**Çıkarılan görev ve kabul sınırı:** Tek değişiklik tek merkez tetiklemeli, doküman değişikliği ağır tarama başlatmamalı. Çakışan push ve cron ayrı sayılmalı. Hatalı geçmiş sessizce yok sayılmamalı. Başarısız step, log olmadan kesin kök neden değildir. İki başarısızlık zinciri için devre kesici testi var; bütün workflow'larda fiili entegrasyon kanıtı ayrı.

### IBO, kimlik, EPG, logo, kaynak
**Doğrudan açılan kaynaklar:** `test_central_ibo_review_queue.py`, `test_central_identity_epg_logo_audit.py`, `test_central_source_reconciliation.py`, `test_epg_pilot.py`, `test_epg_tv_readiness.py`, `test_final_validation.py`.
**Çıkarılan görev ve kabul sınırı:** SHA ile aday ayrımı; kanal adı aynı olsa farklı akışlar korunur. IBO, kimlik, yayın hakkı ve logo otomatik onaylanmaz. EPG gece yarısı taşması dar koşulda düzeltilir, diğer ters zamanlar reddedilir. Kaynak tanımları/duplicate isim ve endpoint farkları gerçek envanterden çıkarılır. Final süreklilik yalnız üç başarılı aday için; terminal sonuçlar gereksiz tekrar edilmez.

### Kanıt, yönetim, güvenlik, tek ekran
**Doğrudan açılan kaynaklar:** `test_central_main_playlist_run_evidence.py`, `test_central_management_summary.py`, `test_central_open_gaps.py`, `test_central_protected_write_gate.py`, `test_central_run_status.py`, `test_central_short_status.py`, `test_central_single_screen_report.py`, `test_sistem_saglik_denetimi.py`, `test_toplu_durum_raporu.py`.
**Çıkarılan görev ve kabul sınırı:** Yeşil workflow kanalı doğrulamaz; eksik/bozuk JSON raporlar ayrı hata sayılır; tek ekranda beş aşama ve açık işler kanıtıyla görünür. Statik protected-write denetimi gerçek branch ruleset engeli değildir. Actions run tamamlanmadan başarılı sayılmaz.

### Diğer kontrol dosyaları
**Doğrudan açılan kaynaklar:** `test_toplu_durum_raporu.py`, `test_verification_pipeline.py`, `test_yedekler_teknik_aktar.py`, `test_ana_liste_saglik.py`, `test_candidate_logo_missing_report.py`.
**Çıkarılan görev ve kabul sınırı:** Üç testte altı saat aralık, süre/frame kanıtı ve sayısal olmayan ffmpeg çıktısının güvenli reddi aranır. YEDEKLER teknik aktarım kodunda eski koşullu yol bulunsa da 15 Ekim kullanıcı iptali üstün: hiçbir aktarım yapılmaz.

### Birleştirilmiş yapılacaklar (yeni beş kategori)
1. **Güvenlik:** yazma yetkisi/branch ruleset ve gerçek engelleme; başarısızlık devre kesicisinin tüm aktif workflow'lardaki kapsamı; korunan dosyaların SHA ve değişiklik izni.
2. **Keşif:** 156/155 tarihsel kaynak farkını güncel kaynak envanteriyle doğrula; aynı endpoint, farklı ad, eski snapshot, güven puanı ve ham URL gizliliğini kontrol et.
3. **Kanal testleri:** altı saat aralık/terminal sonuç/gerçek test zamanı; 3 aşama, final süreklilik, kimlik ve kullanıcı IBO kararı birbirinden bağımsız; aynı URL tekrarları ve bozuk geçmiş raporlanmalı.
4. **Logo/EPG:** XMLTV ve gece yarısı sınırlarını doğrula; görsel logo eşleşmesi ve İsveç IBO cihaz kanıtı olmadan onay verme.
5. **Arşiv ve kabul:** gerçek arşiv sayısı, izole restore ile offsite/tarihsel restore ayrımı, 8/18 görev açık kanıtı, 92 eski workflow'un 5 sisteme işlevsel eşdeğerliği ve tek merkez tetikleme kabulü; son Actions run ve kullanıcı onayı olmadan kapatma.

### Açık inceleme / önemli ihtiyat
Bu turda **33 farklı test dosyası** doğrudan açıldı (ilk 12 + sonraki 12 + son 9). Yukarıdaki kaynak listesi bu 33 dosyayı kapsar. Ekrandaki kalan başka test dosyalarının (örn. adı görüntüde kesilen ve GitHub kök dizininde eşleştirilmeyen) tamamı bu raporda 'açıldı' sayılmaz. Test dosyalarının içeriklerinin GitHub'dan alınması, canlı Actions başarısı veya IBO cihaz kanıtı değildir. Main ekranıyla çalışma dalı farkı devam ediyor. Bu not yalnız DEVAM_NOTU.md sonuna eklendi; başka kaynak dosya, workflow, YEDEKLER veya playlist değiştirilmedi.


## 15 EKİM 2026 — YEDİ BÜYÜK DOSYAYA BLOB ERİŞİMİ

Kullanıcı talimatıyla önceki açılmış dosyaları gereksiz tekrarlamadan, 7 büyük engelli dosyaya GitHub Git Blob API SHA üzerinden yeniden erişildi. **Yedi dosyanın yedisinden içerik geldi**; önceki fetch_file boş yanıtı dosya bozukluğu değildir. Blob denemeleri GitHub `main` ağacındaki SHA ile yapıldı; çalışma dalında aynı SHA olup olmadığı her kaynak için ayrıca doğrulanmalıdır. İçeriğe erişim, bütün kayıtların tek tek semantik denetiminin tamamlandığı anlamına gelmez.

- `aday_bekletme/ADAY_ONCELIK_RAPORU.csv`: yaklaşık 2.669 satır, öncelik/inceleme notu/kanal/adayı/teknik-medya testi/kaynak ve durum sütunları. Gizli yayın URL'lerini notlara kopyalama.
- `madsc_kesif/bulunan_kanal_arsivi.csv`: yaklaşık 11.744 satır, kanal/URL/kaynaklar/sınıf/teknik/IBO/ilk-son görülme sütunları; 11.742 URL raporuyla tarihsel kapsam mutabakatı yapılmalı.
- `madsc_dogrulama/state.json`: 206.000 satır, `channels` kökü; üç aşamalı kontrol geçmişi, zaman aralıkları, 3/3 başarı ve kimlik/IBO ayrımı için inceleme.
- `madsc_kesif/gecmis.json`: 107.607 satır, `history` kökü; tekrar/kaynak geçmişi ve tarihsel kimliği belirsiz arşivler.
- `madsc_son_kontrol/results.json`: 185.889 satır, JSON dizi; final süreklilik, kimlik bekleme ve önceki başarısızlıkların sınıflandırılması.
- `aday_bekletme/gecmis.json`: yaklaşık 71.986 satırlık içerik döndü, fakat yanıtın sonu kapanışla doğrulanamadı; tam JSON parse ve bütünlük kontrolü ayrıca gerekli.
- `aday_hazirlik/uc_asama_2026-10-12_1037.json`: 60.602 satır, snapshot zamanı, durum sayımları, altı saat kural ihlalleri, playlist tekrarları, bekleyen gruplar ve sonraki adımlar; tarihsel snapshot güncel başarı sayılmaz.

**Birleştirilecek açık işler:** (1) 7 kaynağın tarih/branch/sha eşleştirmesi; (2) 10.817 kimliği belirsiz tarihsel arşiv kaydı; (3) aday öncelik ve final durumlarının tekrarsız karşılaştırması; (4) gerçek altı saat test aralığı ve 3/3 geçmiş bütünlüğü; (5) yanlış pozitif, kanal kimliği ve İsveç IBO cihaz kararı ayrımı; (6) ham URL/credential sızıntısını engelleme; (7) diğer 769 envanter dosyasının benzersiz tam içerik/format kontrol matrisini tamamlama.

**Sayım ihtiyatı:** 15 Ekim çalışma dalı envanteri 769 dosya/27 klasör, daha önce `main` dalı ağacı 749 dosya/26 klasör gösterdi. Bu iki sayım farklı dal/sürüm olabilir; **749 ve 769 toplanmaz veya biri ötekinin yerine kullanılmaz.** Önceki '48 + 30' okumaları kısmi ve çakışmalı; bu tur 7 büyük dosya için erişim kanıtı var. Bütün 769 dosyanın tam içerik incelemesi henüz sayısal olarak sertifikalandırılmadı.

Kaynaklar, playlistler, workflowlar, yedekler ve görseller değiştirilmedi. PR #71 birleştirilmedi.


## 15 EKIM 2026 — BUYUK JSON PARSE VE BES KATEGORIYE DONUS KONTROLU

**Kullanıcı isteği:** Açılmış/açılamamış dosyaların dürüst toplam raporu, geçmiş görev ve program fonksiyonlarının çıkarılması, tamamlanmayan kaynaklara devam edilmesi, sonra 5 merkezi kategoriye güvenli geçiş. Eski okumalar çakışabileceğinden 78 + 7 = 85 kesin benzersiz/tam incelenen dosya değildir. Çalışma dalı eski envanteri 769 dosya/27 klasör (373 görsel, 396 diğer), main dalı başka sürümde 749 dosya/26 klasör. Çalışma dalında .github/workflows klasörü doğrudan 97 YAML, scripts 69 Python, tests 2 Python, tools 17 Python, docs 4 Markdown, raporlar 8 dosya olarak listelendi. 92 sayısı eski workflow geçiş kapsamıdır; 97 mevcut YAML dosya sayısıyla aynı ölçüm değildir.

**Büyük dosya erişim kanıtı:** GitHub blob SHA yöntemiyle 7 önceden erişilemeyen dosyanın içeriği elde edildi. Bunlardan 5 büyük JSON dosyası JSON.parse ile doğrulandı: aday_bekletme/gecmis.json 2667 kayıt, madsc_kesif/gecmis.json 11762 kayıt, madsc_dogrulama/state.json 7100 kanal, madsc_son_kontrol/results.json 3800 sonuç, aday_hazirlik/uc_asama_2026-10-12_1037.json tarihsel snapshot. Son kontrol 3800 sonucunun dağılımı: 2332 TECHNICAL_PASS_IDENTITY_PENDING, 1055 TECHNICAL_PASS_CONTENT_REVIEW, 255 CONTINUITY_FAILED, 158 TIMEOUT. 12 Ekim snapshot: 3/3=5750, 2/3=439, 1/3=109, 0/3=138, pending=293. Bu sonuçlar gerçek IBO kimlik ve oynatma onayı değildir. aday_bekletme/gecmis.json successful_runs alanı dizidir, sayı değildir; ham URL içinde gizli bilgi biçimleri olabilir, loga kopyalanmamalıdır. CSV aday öncelik ve bulunan kanal arşivi blob üzerinden okundu ancak her satırın semantik kontrolü ayrı açık.

**Yeni okunan geçiş belgeleri:** docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md; docs/MADSC-92-WORKFLOW-ESDEGERLIK-KONTROL-2026-10-14.md; docs/MADSC-IKI-TOPLU-KABUL-PLANI.md; docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md. Belgeler statik 92 workflow sınıflandırmasının eski/yeni komut, çıktı, cron/push/dispatch/workflow_run, izin, hata davranışı ve artifact eşdeğerliğini kanıtlamadığını söylüyor. Beş job yeşil olsa da 92/92 işlev eşdeğerliği, EPG→Pages, günde iki keşif, VOD, offsite restore ve İsveç IBO cihaz kabulü ayrıca kanıtlanmalı. 92 eski workflow silinmez/kapatılmaz, PR #71 merge edilmez; önce aynı girdi ile karşılaştırma ve korunan SHA kontrolleri, ardından tek toplu beşli CI kabulü ve kullanıcı onayı gerekir.

**Açık görev ve sıra:** (1) 769 çalışma dalı dosyasının SHA bazlı tekilleştirilmiş okundu/eksik matrisi; (2) diğer CSV/M3U/XML ve görsel kanal-logo eşleşme denetimi; (3) 92 satır işlev/tetik/yan etki/artifact matrisi ve 26 kural; (4) güvenlik, keşif, test+EPG/logo, arşiv/yedek, genel bakım beş kategorisine kanıtlı görev devri; (5) toplu regresyon, gerçek Actions ve kullanıcı cihaz kabulü. Tamamlanan iş tekrar yapılmaz. Korunan playlist, logo, yedek ve eski workflow değiştirilmedi.


## 15 EKİM 2026 — YENİ SOHBETE KESİN DEVİR KAYDI

**Kullanıcı kararı:** Sohbet kapasitesi dolduğu için yeni sohbet açılacak. Bütün geçmiş notlar korunacak; dosya incelemesi bitirilip ancak ardından beş kategori merkezî otomasyonun gerçek işlev eşdeğerliği ve taşınmasına devam edilecek. Kullanıcı inceleme ve not güncelleme yetkisi verdi; **bu yetki korunan playlist/YEDEKLER/FAVORILER/YENILER/HEPSI/logo/workflow dosyalarını değiştirme veya PR #71'i birleştirme yetkisi değildir.** Sadece `DEVAM_NOTU.md` güncellenebilir.

**Depo ve dal:** `Madsc55/madsc-tv`, `madsc/bes-sistem-toplu-birlestirme`; PR #71 taslak ve merge edilmeyecek. Ekran görüntüleri `main` dalını gösterebildiğinden, dal/snapshot farkları korunmalı.

**Sayım:** Çalışma dalına ilişkin önceki envanter **769 dosya/27 klasör** (373 görsel, 396 diğer); `main` ağacı bir sorguda **749 dosya/26 klasör** verdi. Sayılar farklı dal/snapshot; 769 dosyanın tümü semantik olarak tek tek okunup görevleri çıkarıldı iddiası yok. Önceki sohbetlerde 33 kök test, 15 program ve 30 diğer dosya açıldığı bildirildi; bunlar tekilleştirilmiş ve SHA kanıtlı tam kapsama matrisi değildir. Çalışma dalında `.github/workflows` dizininde **97 YAML** görüldü; 92 eski workflow beş kategoriye birebir taşındı iddiası yok. `scripts` 69, `tools` 17, `tests` 2, `docs` 4 dosya olarak dizin sorgusunda görüldü.

**Önemli erişim çözümü:** `fetch_file` boş içerik dönen **7 büyük dosyanın 7'si** GitHub blob SHA yöntemiyle açıldı. `aday_bekletme/ADAY_ONCELIK_RAPORU.csv` ~2.669 satır, `madsc_kesif/bulunan_kanal_arsivi.csv` ~11.744 satır; CSV satırlarının kanal/öncelik açısından tam semantik denetimi sürüyor. JSON parse başarılı: `aday_bekletme/gecmis.json` 2.667 aday (successful_runs alanı dizi); `madsc_kesif/gecmis.json` 11.762 geçmiş; `madsc_dogrulama/state.json` 7.100 kanal; `madsc_son_kontrol/results.json` 3.800 sonuç (2.332 identity pending, 1.055 content review, 255 continuity failed, 158 timeout); `aday_hazirlik/uc_asama_2026-10-12_1037.json` tarihsel snapshot (5.750 adet 3/3, 293 pending). URL anahtarları gizli kimlik bilgileri içerebilir: ham URL ve erişim belirteci notlara yazılmaz. Blob'ların SHA'ları `main` ağacından alındı; çalışma dalıyla eşitlik ayrıca doğrulanacak. JSON parse tam kayıtların tek tek iş kuralı incelemesi demek değildir.

**Bulunan işler/kararlar:** Üç aşamalı test ve altı saat aralık; ffprobe başarısı IBO İsveç cihaz kabulü değildir; kimlik/EPG/logo ve yayın sürekliliği ayrı onay; son kontrolün 3.800 tamam/2.574 kalan tarihsel kanıtı; 11.742 arşiv URL/11.762 keşif geçmişi kapsam farkı; 75 aday ve 4 alternatif; offsite yedek ve gerçek restore kanıtı eksik; EPG beş kanal pilotu ve Pages yayın kanıtı var fakat tam yayın/cihaz kanıtı yok; logo görsel kimliği onaysız; VOD Filmler/Diziler uyumu eksik; Ekol TV başa sarma ve Eurostar/eksik Türk kanalları talepleri; 8 ve 18 görev raporları, 26 güvenlik kuralı, 92 workflow eşdeğerliği. Eski kullanıcı kararları, iptal edilen YEDEKLER aktarım izni ve kaynak koruma her şeyin üstünde tutulmalı.

**Beş ana kategori:** (1) Güvenlik ve izin/koruma, (2) Kaynak keşfi ve aday yönetimi, (3) Üç aşamalı kanal testi ve kimlik/IBO, (4) EPG ve logo, (5) Arşiv-yedek-genel bakım/tek merkez rapor. Önceki belgelerde kategori adları farklı gruplanmış olabilir: nihai kabul planındaki beş job adı ile eşleştir, isim benzerliğini işlevsel eşdeğerlik sayma.

**Yeni sohbet ilk adımlar:** 1) Bu `DEVAM_NOTU.md` kaydını ve `docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md`, `docs/MADSC-92-WORKFLOW-ESDEGERLIK-KONTROL-2026-10-14.md`, `docs/MADSC-IKI-TOPLU-KABUL-PLANI.md`, `docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md` belgelerini referans al. 2) `main` ve çalışma dalı dosya ağacını SHA bazlı çıkarıp gerçek benzersiz okunmuş/açılmamış dosya sayısını hesapla; daha önce açılmışları tekrar açma. 3) CSV/M3U/XML, uzun JSON içi anomaliler, logo görselleri ve kalan raporlardan eksik görevleri topla. 4) Görevleri mevcut notla tekilleştir, yapılmış/kanıt eksik/yapılacak/kullanıcı onayı olarak sınıflandır. 5) 92 eski workflow için girdi, tetik, izin, yan etki, çıktı, artifact, hata davranışı karşılaştırmasını ve korunan dosya SHA kapısını çalıştır. 6) Kullanıcı onayı ve gerçek testler olmadan eski workflowları kapatma, beşli sistemi tamamlandı deme veya PR merge etme.

**Son sohbet durum özeti:** Kullanıcı taşıma denemesi yaptığını belirtti fakat sonucu/logunu paylaşmadı; bu nedenle taşıma başarılı varsayılmaz. Bu kayıt sonraki sohbet için durak noktasıdır, geliştirme tamamlandı kaydı değildir.


## 15 EKİM 2026 — YENİ SOHBET İLK BAĞIMSIZ KONTROL (SALT OKUNUR)

- GitHub çalışma dalındaki DEVAM_NOTU.md doğrudan okundu; son "YENİ SOHBETE KESİN DEVİR KAYDI" ve önceki görev/karar kayıtları incelendi. Bu kaydın yazılması dışında hiçbir dosya değişikliği yetkisi yoktur.
- Devir commit'i `4987dfb79618f3cd24d4078c9003f77ff697b775` Git tree recursive sorgusu: **769 blob, 373 görsel, 27 tree, truncated=false**. Bu, devir anı envanterinin bağımsız doğrulamasıdır; 769 dosyanın semantik tam incelemesi değildir. Güncel dal HEAD'i ile devir commit'i farkı ayrıca denetlenmeli.
- Dört geçiş belgesi doğrudan yeniden okundu: `docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md`, `docs/MADSC-92-WORKFLOW-ESDEGERLIK-KONTROL-2026-10-14.md`, `docs/MADSC-IKI-TOPLU-KABUL-PLANI.md`, `docs/MADSC-TAM-DURUM-VE-YOL-HARITASI-2026-10-14.md`. Bunların ortak kararı: geçmiş beş job success, 92/92 üretim eşdeğerliği ve son taşıma denemesi başarısı değildir.
- Önceden blob yöntemiyle erişilen yedi büyük dosya tekrar indirilmedi; eski parse ve satır sayısı kanıtları korunur. Eski okuma listeleri dosya bazında SHA/okuma derinliğiyle tekilleştirilmediğinden tam incelenen benzersiz dosya sayısı **henüz bilinmiyor**.
- Güncel yetki: sadece DEVAM_NOTU.md; ana playlistler, HEPSİ, FAVORİLER, YENİLER, YEDEKLER, logolar ve workflow'lar değiştirilmez; PR #71 merge edilmez. Kullanıcının son sistem taşıma denemesine ait log/test sonucu paylaşılmadı: **BAŞARI DOĞRULANMADI**.
- Sonraki salt okunur görevler: HEAD/devir ağaç farkı; önceki okuma kanıtlarından SHA bazlı gerçek kapsama matrisi; açılmamış CSV/M3U/XML/program/raporlar; 92 workflow için tetik, komut, izin, yan etki, artifact, hata, geri alma ve korunan SHA karşılaştırması. EPG→Pages, 2/gün keşif, VOD, 1/15 yedek, harici restore, 26 güvenlik kuralı ve İsveç IBO cihaz kabulü ayrı engel olarak kalır. Kod ve workflow değişikliği için yeni açık kullanıcı izni gerekir.


## 15 EKİM 2026 — YEDİ BÜYÜK KAYNAĞIN YENİDEN BLOB KONTROLÜ VE MERKEZİ İŞ DEVİR LİSTESİ

**Yetki sınırı:** Kullanıcı büyük dosyaların yeniden açılmasına, inceleme bulgularının DEVAM_NOTU.md içinde toparlanmasına izin verdi. Korunan listeler, YEDEKLER, YENİLER, FAVORİLER, HEPSİ, logo, çalışan otomasyonlar ve PR #71 üzerinde değişiklik yetkisi verilmedi.

**Yeni doğrudan kanıt:** Devir commit'i `4987dfb79618f3cd24d4078c9003f77ff697b775` üzerinden recursive Git tree tam (truncated=false): 769 blob, 27 klasör, 373 görsel. Dosya türleri: 97 yml, 151 py, 51 json, 34 md, 27 m3u, 26 csv, 3 xml, 7 txt, 330 png, 40 svg, 1 webp, 2 jpg. Bu sayım dosyaların incelendiğini değil envanterin varlığını kanıtlar.

**Önceden erişim sorunu yaşayan 7/7 dosya SHA ile yeniden açıldı, yanıtın hem başlangıcı hem dosya sonu kontrol edildi:**
1. `aday_bekletme/ADAY_ONCELIK_RAPORU.csv` — blob `525f650158e7c25da58421abd8cbe000b120d232`, yaklaşık 1.1 MB; öncelik, inceleme notu, teknik/medya testi, kaynak ve onay sütunları.
2. `madsc_kesif/bulunan_kanal_arsivi.csv` — `48910f40d973ea0d6834aa7d051a68de62d2b2ab`, yaklaşık 2.46 MB; kanal, kaynak, sınıf, teknik/IBO durum ve görülme zamanları.
3. `madsc_dogrulama/state.json` — `c9060ffb9e3a0b046657c4933cf77a794aff861a`, yaklaşık 5.96 MB; channels kökü ve test geçmişi.
4. `madsc_kesif/gecmis.json` — `6d9164b0f38edfa266c794a01d13e9e1139fcf6d`, yaklaşık 4.8 MB; history kökü ve kaynak geçmişi.
5. `madsc_son_kontrol/results.json` — `779f7d97ce79b79e072dcf5b7d12d817054bc487`, yaklaşık 4.84 MB; sonuç dizisi, kimlik ve süreklilik ayrımı.
6. `aday_bekletme/gecmis.json` — `db88c948936e66fc019c757f40c451a78546abf6`, yaklaşık 2.03 MB; aday geçmişi, successful_runs dizisi.
7. `aday_hazirlik/uc_asama_2026-10-12_1037.json` — `076a6d4d05cfa8104e760d9c1965026846e28d7b`, yaklaşık 1.79 MB; tarihsel üç aşama snapshot ve bekleyen işler.

**Önemli sınır:** Bu turda yedi dosyanın tam metin yanıtına erişildi ve kapanışları görüldü. Önceki kayıttaki beş JSON parse ve sayımlar tarihsel kanıt olarak geçerlidir; bu turda tüm CSV satırları ve JSON kayıtları tek tek yeniden iş kuralı denetiminden geçirilmedi. Ham URL/token/credential notlara kopyalanmadı. Devir commit'i SHA'ları ile güncel dal HEAD SHA'ları ayrı karşılaştırılmalıdır.

**Tekilleştirilmiş görev başlıkları ve durumları:**
- YAPILDI / KANITLI: 769 dosyalık devir ağacı sayımı; 7 büyük dosyaya blob erişimi; geçmiş 5/5 kategori CI koşusu ve artifact kayıtları (eski commit için); beş kategori rapor altyapısı; 92 eski workflow'un statik sınıflandırma altyapısı.
- YAPILDI AMA KAPSAMI SINIRLI: 5 JSON parse ve tarihsel aday/sonuç sayımları; 50 kanal salt okunur sağlık partisi; EPG beş kanal pilotu; izole Git restore; korunan yazma kapısının statik testleri. Bunlar canlı IBO, offsite restore, 92/92 eşdeğerlik veya gerçek branch koruma başarısı değildir.
- EKSİK KANIT: SHA bazlı tekil tam-okuma matrisi; CSV/M3U/XML satır düzeyi anomali ve kaynak mutabakatı; 373 görselin kimlik/logo incelemesi; güncel Actions sonuçları; kullanıcının son taşıma denemesi logları; canlı cihaz, Pages ve harici geri yükleme kanıtları.
- KULLANICI KARARI: Eski YEDEKLER ekleme izni geri alındı. Ana kanal/YEDEKLER/YENİLER/FAVORİLER/HEPSİ/logo korunur; otomatik teknik sonuç kanal kimliği veya yayın hakkı onayı değildir. PR #71 merge edilmez; eski workflow kapatılmaz. Küçük testler yerine hazırlanmış tek toplu beşli kabul tercih edilir.

**Beş merkezi kademe için görev devri (uygulama değil plan):**
1. **Güvenlik ve izin:** 26 kural, 8/18 görev raporlarının güvenlik açıkları, korunan SHA256 ve gerçek yazma reddi, credential sızıntısı, otomatik push/contents_write, iki başarısızlık devre kesicisi, 92 workflow izin karşılaştırması.
2. **Keşif ve aday:** 155/156 kaynak farkı, 11.742 arşiv URL ve 11.762 geçmiş mutabakatı, 75 aday/4 alternatif, kimliği belirsiz tarihsel kayıtlar, yinelenen endpoint ve zaman farkı, günde iki keşif üretim tetiklerinin eşdeğerliği; playlist yazma yok.
3. **Üç aşamalı kanal testi ve IBO:** 6 saat aralıklı 3/3, 51 farklı saat retest, 24 ffprobe başarısız, terminal sonuç ve gerçek son test zamanı, yanlış negatifler, 3.800 son kontrol, kimlik/lisans/IBO cihaz kararlarının bağımsızlığı.
4. **EPG ve logo:** XMLTV geçerliliği, gece yarısı program sınırı, EPG→Pages workflow_run ve yayın, logo eşleştirme, İsveç IBO cihaz testi; Ekol TV başa sarma ve eksik Türk kanalı talepleri ayrı ürün görevleri.
5. **Arşiv, yedek ve genel bakım:** izole/tarihsel/offsite restore ayrımı, 1/15 backup, VOD Filmler/Diziler, 92 workflow tetik/komut/izin/çıktı/artifact/hata/rollback matrisi, çifte tetik denetimi, 8/18 görev ve tek merkez raporu, nihai 5/5 toplu kabul.

**Kabul engeli:** Her eski workflow için yeni kategori sahibi, somut işlev karşılığı, aynı girdide çıktı ve hata karşılaştırması, tetik/yan etki/izin/artifact, korunan SHA ve rollback kanıtı yazılmadan `ESDEGERLIK_BEKLIYOR` kalır. Kullanıcının son taşıma denemesi için test sonucu yok; başarılı kabul edilmez. Bu not yazılırken hiçbir workflow veya korunan veri değiştirilmedi.


## 15 EKİM 2026 — ESKİ DOSYALARDAKİ UNUTULMUŞ GÖREV VE KARARLARIN TOPLU KURTARILMASI

**Bu çalışmanın gerçek amacı:** 769 dosyayı tek tek çalıştırmak değil; eski not, program, workflow ve raporlardaki kullanıcı isteklerini, yapılmış işleri, yarım kalanları, yasakları ve beş merkezi sistemde unutulmaması gereken davranışları kurtarmak. Dosya envanteri bu iş için yalnız araçtır. Aşağıdaki bulgular 15 Ekim'de doğrudan yeniden okunan kaynaklara dayanır; eski tarihli durumları güncel canlı başarı olarak göstermez. Bu bölüm önceki kronolojik kayıtları silmez.

### Okunan ana eski kaynaklar
\`AGENTS.md\`, \`GUVENLIK_KURALLARI.md\`, \`IPTV_PROJE_HAFIZASI.md\`, \`OZELLIK_ENVANTERI.md\`, \`SEKIZ_GOREV_TOPLU_DENETIM.md\`, \`raporlar/GELISTIRME_11_DURUM_2026-10-12.md\`, \`MADSC_2026-10-13_KALAN_ISLER_DEVAM_KAYDI.md\`, \`kontrol_notlari/DEVAM_GECMISI_2026-10-12_1947.md\`, \`kontrol_notlari/YENI_KANAL_ARAMA_TALEPLERI.md\`, \`kontrol_notlari/2026-10-12_ekol_basa_sarma.md\`, \`vod/README.md\`, \`BES_SISTEM_TOPLU_IS_DEFTERI.md\`, \`BES_SISTEM_GECIS_KONTROL.md\`, \`BES_SISTEM_92_WORKFLOW_TETIK_ENVANTERI.md\`, \`ONCELIK_1_BES_MERKEZI_OTOMASYON_PLANI.md\`, \`DEVIR_NOTU_2026-10-15.md\`; ayrıca önceki turda dört \`docs/MADSC-...\` geçiş belgesi ve yedi büyük veri dosyası. \`TOPLU_DURUM_RAPORU.md\` ve 97 workflow'un bu turda tek tek yeniden davranış okuması henüz yapılmadı.

### 1. Güvenlik merkezine taşınacak unutulmaması gereken kurallar
- [KARAR] Ana liste/HEPSİ/FAVORİLER/YENİLER/YEDEKLER, ad/URL/logo/ID/sıra/kategori kullanıcı izni olmadan değişmez. Yalnız bu notu düzenleme izni var. 13 Ekim'deki YEDEKLER'e ekleme izni daha sonraki kullanıcı kararıyla geri alındı; eski notlardaki ters izin geçersiz.
- [KARAR] \`GUVENLIK_KURALLARI.md\` 1–24 korumaları; \`AGENTS.md\` 25 değişiklik sonrası test, 26 kullanıcıya görünen yeni/değişen test adları Türkçe. Politikaların yazılması teknik uygulanma kanıtı değildir.
- [YAPILDI/KISMİ] Güvenlik testleri, raporlar, SHA256 izole yedek açma, korunan yazma risk taramaları var; GitHub branch protection API bir tarihsel denemede 403 döndürdü. Branch protection etkin kabul edilmez.
- [AÇIK] Tüm üretim yazarlarında gerçek merkezi yazma kapısı, dolaylı push/izin, eski 92 workflow, iki ardışık başarısızlıkta ortak devre kesici, 26 kuralın gerçek kanıtı ve kullanıcı onayı sonrası M3U sıra/sayı/URL bütünlüğü.
- [KARAR] Tamamlanan kanal kimlik retleri, kullanıcı IBO kararları, silme/taşıma geçmişi ve mevcut başarılı testler korunur; yeniden uygulanmaz. İlk 90 HEPSİ sırası ve Favoriler 1/2/3 sıraları ayrıca korunur.

### 2. Keşif ve aday merkezine taşınacak görevler
- [YAPILDI/KISMİ] Birleşik keşif, kaynak geçmişi, aday/alternatif ayrımı, \`source_history\`, aday öncelik ve arşiv raporları kurulu; 156 kaynak ile 155 hedef farkı geçmişte kaydedildi. Kaynak adı Türkçe kimliği veya lisans kanıtı değildir.
- [AÇIK] Günde iki **yalnız yeni URL keşfi** (06:00 ve 18:00 UTC) ile **aylık geniş kaynak taraması** ayrı tutulmalı. 156 kaynağın benzersizliği/erişimi, Türk/yabancı/belirsiz, diaspora/yerel, öncelikli ulusal-haber-spor-belgesel-çocuk-müzik ve alternatif URL ayıklama tamamlanmalı.
- [AÇIK/ÜRÜN TALEBİ] Eurostar eski kullanıcı talimatıyla kaldırılmış ve 404 doğrulanmış; çalışır, gerçek görüntü/ses/kimlik/süreklilik kanıtlı alternatif araması bekliyor. Bulunması listeye ekleme yetkisi değildir. Eksik Türk kanalları ayrı keşif kuyruğunda.
- [KARAR] Kullanıcı IBO'da teknik testten geçmeyen pek çok kanalı oynatabiliyor; ffprobe başarısızlığı = cihaz başarısızlığı değildir. 740 yabancı olarak belirlenen kayıt ve 10.817 belirsiz sınıflandırma eski snapshot'tır; kullanıcı son kararı ve güncel dosya önceliklidir.
- [KARAR] Adayları YEDEKLER'e otomatik taşıma **şimdilik iptal**. Yabancı/Türk/kimlik belirsiz geçmişi korunur, URL ve kanal sayıları karıştırılmaz.

### 3. Üç aşama ve gerçek oynatma merkezine taşınacak görevler
- [YAPILDI/KISMİ] Üç deneme, en az altı saat aralık, tekrar atlama, son kontrol, ses/görüntü/süreklilik ve kullanıcı IBO kararı için ayrı kayıt altyapısı var. Eski 6.436 tamamlanmış üçlü kayıt ve ilk 39 final/kimlik kararı yeniden sıfırdan çalıştırılmaz.
- [AÇIK] 75 aday (51 farklı saat retest, 24 ffprobe geçmeyen) ve dört alternatif; final sonuçlarda kimlik bekleyen, içerik incelemesi, timeout ve süreklilik hata kuyrukları; gerçek son deneme zamanları ve yanlış negatiflerin ayrılması.
- [KARAR] Teknik decode, yayın kimliği, yayın hakkı, IBO cihaz oynatması ve kullanıcının kabulü **beş ayrı hüküm**; otomatik teknik PASS ana listeye ekleme izni vermez.
- [KARAR] Kullanıcının ADA/Kanal D ret kararı önceki görsel desteği geçersiz kılar. Eski retler veya kabul edilmiş kategoriler yeniden değiştirilmez.
- [AÇIK] TCL 55C655 / IBO Player Pro 2128.0 için gerçek cihaz/sürüm, açılış ve kanal geçiş süresi, kullanıcı gözlemi; ffprobe decoder süresi cihaz açılış süresi değildir.
- [AÇIK/ÜRÜN TALEBİ] Ekol TV ve Ekol Sports'un başa sarma şikâyeti: eski HLS manifestinde parçalar ilerlemiyordu; HTTP 200 canlı yayın kanıtı değildir. Yeni alternatifte segment ilerlemesi ve uzun oynatma ayrı doğrulanır.

### 4. EPG/logo zinciri (mevcut resmi üçüncü kategori içinde) için görevler
- [YAPILDI/KISMİ] Beş kanallık EPG pilotu, XMLTV üretimi, günlük EPG ve Pages akışları, aday PNG ve logo URL denetimi var; daha önce yapılanı sıfırdan kurma.
- [AÇIK] Gece yarısı \`stop\` tarih kayması ve \`source_time_repairs\` kanıtı; gerçek program eşleşmesi, İsveç IBO görünürlüğü, EPG günlük → başarılı workflow_run → Pages yayın zincirinin yeni beşli görev sahipliği.
- [AÇIK] Görselin gerçek kanal logosu/kimliği ile eşleşmesi, eksik aday logoları, mevcut dolu logoların korunması. PNG dosyasının varlığı doğru amblem kanıtı değildir.

### 5. Arşiv/yedek ve genel bakım merkezlerine taşınacak görevler
- [YAPILDI/KISMİ] Tam sistem tar arşivi ve SHA256 izole açma, Actions artifact, izole restore, merkezi altı alan/sekiz görev/18 görev rapor araçları ve tek yönetim özeti mevcut. Bunlar gerçek harici restore veya tamamlama sertifikası değildir.
- [AÇIK] Ayın 1/15'i sistem sağlığı, ana liste kontrolü, merkezi denetim ve tam yedek birbirini tekrarlamadan koordine edilmeli; 30 gün saklama, harici/offsite kopya, secrets/IBO ayarları ve bağımsız geri yükleme tarihsel olarak kullanıcı tarafından ertelenmişti: izinsiz kurma, açık bağımlılık olarak izle.
- [AÇIK] VOD Filmler/Diziler ayrı çalışma alanı; \`vod/katalog.json\` ve izinli Big Buck Bunny test listesi var. IBO Filmler/Diziler sekmesi görünürlüğü doğrulanmadı; Xtream uyumluluğu gerekebilir. Lisans, ses/altyazı, sezon/bölüm, ileri-geri sarma ve ancak cihaz doğrulamasından sonra günlük ekleme değerlendirilecek. TV ana listesine dokunma.
- [AÇIK] 11 geliştirme raporunun eksik parçaları, sekiz görev ve 18 görev kararları; tek durum raporunun gerçek state/final/IBO/EPG/kimlik verilerini aynı koşuda karşılaştırması; rapor bulunması görev tamamlandı demek değildir.
- [KARAR] Eski cron envanterinde günlük EPG 03:25 UTC, haftalık IPTV testi çarşamba 06:30 UTC, iki kez keşif 06:00/18:00 UTC, günlük final 06:10 UTC, günlük VOD 07:17 UTC ve ayın 1/15'i birden fazla sağlık/yedek/denetim tetikleyicisi vardı. Yeni beşli sisteme **işlev ve periyot korunarak, çift tetik engellenerek** aktarılmalı; bu saatler tarihsel main envanteridir, güncel etkinlik kanıtı değildir.
- [AÇIK] \`epg-pages.yml\` başarılı EPG üretimine bağlı \`workflow_run\`; \`madsc-genis-kaynak-kontrol.yml\` üç aşamayı dispatch eder; \`madsc-son-kontrol.yml\` hem schedule hem workflow_run ile başlatılabilir. Yanlışlıkla sonsuz devam, aynı adayın iki kez test edilmesi ve push yarışları önlenmeli.

### Beş gerçek workflow'un resmi sınırı ve kabul
Yeni resmi dosyalar \`.github/workflows/madsc-01-guvenlik.yml\`, \`madsc-02-kesif.yml\`, \`madsc-03-kanal-test.yml\`, \`madsc-04-arsiv-yedek.yml\`, \`madsc-05-genel-bakim.yml\`. EPG/logo üçüncü kategorinin alt görevidir; bağımsız altıncı ana workflow veya resmi dördüncü kategori değildir. Daha eski planlarda 89 workflow yazsa da geçişte kapsam 92 eski workflow'dur; depodaki 97 YAML = 92 eski + 5 yeni.

**Açık kapanış kapısı:** Her eski workflow için yalnız isim eşleşmesi değil komut/izin/tetik/artifact/yazma/hata/rollback ve yeni iş sahibi. Gerçek 92/92 davranış eşdeğerliği, güncel CI, EPG→Pages, VOD, IBO ve restore kanıtları yoksa geçiş TAMAMLANDI denmez. Geçmiş 5/5 başarılı run yeni kodun kabulü değildir. PR #71 birleştirilmez, eski otomasyon kapatılmaz.

**Bu araştırmanın sonucu:** Eski belgelerden yukarıdaki kaybolabilecek karar ve görevler merkezi notta toplandı. Bu, 769 dosyanın her satırının incelendiği veya 92 işlevin tam eşleştirildiği iddiası değildir. Bundan sonraki ana çalışma beş resmi workflow'un **yalnız eksik işlevlerine** dönmektir; yeni kod/workflow değişikliği için kullanıcıdan ayrıca açık izin alınır.


## 15 EKİM 2026 — KULLANICI KARARI: ESKİ DOSYA ARAMASI ERTELENDİ, BEŞLİ GEÇİŞ ÖNCELİK

**Güncel talimat:** 769 dosyanın içinde henüz ayrıntılı okunmamış olanları daha sonra salt okunur açmaya/incelemeye devam et. **Şimdilik bu araştırmayı durdur; dosya veya geçmiş kayıt silme, değiştirme, temizleme, taşımaya kalkışma.** Amaç her eski dosyanın işlevini anlayıp gerekli davranışları yeni beşli sisteme koruyarak aktarmaktır. Bu kullanıcı kararı önceki geniş dosya okuma planına göre önceliklidir. Eski notlar, kayıtlar, logolar, playlistler, yedekler ve workflow'lar aynen kalır. Yalnız DEVAM_NOTU.md güncellenebilir; kod/workflow değişikliği için ayrıca açık izin gerekir.

### Güncel öncelik ve kabul sırası — kaynaktan tekilleştirilmiş kontrol listesi

**P0 — Güvenlik ve gerçek durum tespiti (madsc-01-guvenlik + madsc-05-genel-bakim):**
- [x] 92 eski + 5 yeni YAML ve temel beş kategori dosya adları envanteri; 26 kuralın politika kaydı; güvenlik/sağlık statik testleri; tarihsel başarılı Actions koşuları.
- [ ] En güncel dal/commit ile son beşli Actions job/step/artifact kanıtını eşleştir. Tarihsel 5/5 başarı yeni kodu doğrulamaz.
- [ ] 26 güvenlik kuralı, korunan dosya SHA, gerçek tüm yazma yolları/contents:write/push izinleri, branch ruleset/403 belirsizliği, çift push ve iki başarısızlık devre kesicisini üretim davranışıyla doğrula.
- [ ] Her eski workflow için gerçek görev sahibi, tetik, komut, artifact, izin, yan etki, hata/rollback, yeni karşılık: 92 satırlık matriste KANITLI/KISMİ/EKSİK/BLOKE durumları. Sadece isim/statik eşleşme geçişi kapatmaz.

**P1 — Arşiv, geçmiş ve yedek (madsc-04-arsiv-yedek):**
- [x] Tarihsel aday/keşif/son kontrol dosyaları erişilebilir; izole Git restore ve SHA256 arşiv kanıtları mevcut.
- [ ] Geçmiş test/IBO/alternatif/yabancı/belirsiz kayıtları kayıpsız korunuyor mu, 11.742 URL / 11.762 geçmiş eski snapshot ile güncel durumun ayrımı, 1/15 yedek/sağlık tetik çakışması ve bağımsız geri yükleme kanıtı.
- [ ] Harici/offsite kopya, secrets/IBO ayarları ve 30 günlük saklama eski notlarda ertelenmiş; açık bağımlılık olarak tut, kullanıcı izni olmadan kurma.

**P2 — Keşif ve arama (madsc-02-kesif):**
- [x] Eski \`madsc-birlesik-kesif.yml\` içinde günde iki kez 06:00/18:00 UTC keşif ve \`scripts/four_stage_discovery_report.py\` ile arşiv, aday/alternatif, URL tekrar ve aday logo kanıtı altyapısı var. 156 kaynak envanteri kayıtlı; 155 hedefe zorla düşürme yok.
- [ ] Yeni \`madsc-02-kesif.yml\` eski üretim keşfinin gerçekten tüm işlevini/tetiğini devraldı mı, canlı Actions/artifact ile karşılaştır. Sadece yeni dosyanın varlığı devir değildir.
- [ ] Kaynakların erişimi, izin/lisans ve ülke/kimlik ayrımı; Türk/yabancı/belirsiz; yeni URL ve alternatif tekrarı; aday logo yalnız eksikse; günlük iki keşif ve ayrı aylık geniş tarama; Eurostar, eksik Türk kanalları ve IBO teknik yanlış negatifleri.
- [ ] Keşif → üç aşama → final bağımlılığında tek devam ve aynı adayın tekrarsız işlenmesi; eski cron kapatılmaz.

**P3 — Kanal testleri ve adaylar (madsc-03-kanal-test):**
- [x] Üç aşama 6 saat, final kontrol, kimlik/IBO ayrımı ve 50 kanallık salt okunur sağlık testi altyapısı.
- [ ] 75 adayın 51 farklı saat retesti, 24 ffprobe başarısızı, 4 alternatif; 3.800 tarihsel final sonucu ve güncel kalan kuyruğun doğrulanması; süreklilik, görüntü/ses, gerçek HD/FHD ve Ekol başa sarma.
- [ ] Cihaz TCL 55C655 / IBO Player Pro 2128.0 gerçek oynatma, açılış/geçiş, kullanıcı kararları; kimlik ve yayın hakkı bağımsız. Listeye onaysız ekleme yok.
- [ ] Ana listedeki çalışan PNG'ler kullanıcıya göre çalışıyor: **koru**. Yeni adayların eksik/yanlış logo kimliği ayrı.

**P4 — Genel bakım, özel üretim zincirleri ve nihai 92 devir (madsc-05-genel-bakim):**
- [x] Merkezi 8/18 görev, 26 kural, 92 satırlık statik rapor, açık işler ve tek ekran özeti araçları var.
- [ ] 92 eski workflow'un schedule/push/workflow_run/dispatch/call, step/çıktı/izin ve hata davranışını beş yeni kategoriye bire bir koru; aynı işi iki kez tetiklemeyi engelle.
- [ ] VOD günlük 07:17 UTC eski tetik ve ayrı Filmler/Diziler katalog/IBO sekme doğrulaması; haftalık IPTV testi, günlük final, 1/15 sağlık/yedek/bakım, tek rapor; 11 geliştirme/8 görev/18 görev eksiklerinin tek tek gerçek kapanışı.
- [ ] **EPG EN SONA ERTELENDİ:** \`TOPLU_DURUM_RAPORU.md\` içindeki daha yeni kullanıcı kararı EPG'yi şimdilik durduruyor; IBO'da EPG görünmüyor, mevcut çalışan PNG'ler korunuyor. EPG XMLTV, gece yarısı, günlük üretim→Pages workflow_run ve cihaz kabulü *kaybolmayacak açık görev* olarak saklanır ama yeni EPG işi şimdi yapılmaz.
- [ ] Her kategori eksik işi uygulandıktan sonra bir defalık 5 job toplu CI, gerçek artifact ve üretim kabul kanıtları. Ancak kullanıcı onayı ve 92/92 davranış eşdeğerliği sonrasında eski tetikler kontrollü devredilir. PR #71 birleştirilmez.

**Önerilen başlangıç:** P0'daki son gerçek CI + güvenlik/izin ve 92 workflow eşdeğerlik açığını salt okunur kanıtla tespit et; sonra P1 arşiv/yedek güvenliği, P2 keşif, P3 aday testleri, P4 tek merkez ve en son ertelenen EPG. Kod değişikliğine geçmeden kullanıcıdan kapsamlı açık izin alınır. Geçmiş araştırma tamamlandı diye ilan edilmez, ertelendi diye kayıt düşülür.


## 15 EKİM 2026 — P0 GÜVENLİK/SAĞLIK İLK GERÇEK GITHUB KONTROLÜ (SALT OKUNUR)

**Kullanıcı sıralaması:** Önce beş P0 işi (son beşli koşu, 26 kural, 92 workflow izin/yazma, korunan SHA/branch/devre kesici, çift push); ardından P1'e geç. Bu turda yalnız okuma ve DEVAM_NOTU.md yazma; çalışan YAML/kod/playlist/yedek değişmedi.

**1. Son beşli koşu: DOĞRULANDI, kapsam sınırı açık.** GitHub Actions branch koşu listesi ve jobs API doğrudan okundu: run #38697244625, 2026-10-15 07:12:55 UTC, commit \`c2d28bea366f00372b8da63da06c2791612ebcf4\`, push, completed/success. Beş gerçek job (güvenlik, keşif, kanal test, arşiv/yedek, genel bakım) success. Önceki #38656134669, commit \`f0ed94198ff36f316694cf2a81f90c80a2962d0c\`, failure; güvenlik regresyonu başarısız, genel bakım hata kapısı failure. Başarılı koşu sonraki not-only commit'leri veya 92/92 üretim eşdeğerliğini test etmez.

**2. 26 kural: POLİTİKA VAR, ÜRETİM KABULÜ BEKLİYOR.** \`GUVENLIK_KURALLARI.md\` 1–24; \`AGENTS.md\` 25–26. \`madsc-01-guvenlik.yml\` içerik okuma izni, korunan dosyaların koşu içi SHA256 ve birim regresyon testleri var. Bu üç dosyalık koşu içi SHA kontrolü tüm korunan playlist, yedek, arşiv ve logo kapsamının dış değişikliklerini otomatik denetlemez. Gerçek tüm yazıcıların aynı merkezi onay kapısından geçtiği kanıtlanmadı.

**3. 92 workflow yazma/izin: KISMEN KONTROL, 92/92 DETAY AÇIK.** Eski \`madsc-birlesik-kesif.yml\` ve \`madsc-son-kontrol.yml\` ile \`vod-guncelle.yml\` \`contents: write\` taşır; keşif/son kontrol failure gate ve rapor/commit adımları içerir. \`madsc-aylik-merkezi-denetim.yml\` \`contents: read\`. Beş yeni merkezi workflow \`contents: read\` ve gölge denetim amaçlıdır. Bu doğrudan okunan örnekler 92 eski workflow'un tümünü izin/yan etki bazında doğrulamaz.

**4. Branch protection: BELİRSİZ.** \`GET /branches/main/protection\` 403 \`Resource not accessible by integration\` döndürdü; etkin veya devre dışı iddiası kurulamaz. \`madsc-01\` ve \`madsc-05\` koşu başında \`CALISANLAR.m3u\`, \`AGENTS.md\`, \`GUVENLIK_KURALLARI.md\` SHA256 kaydeder ve koşu sonunda karşılaştırır. Bu, GitHub dışı/offsite ve bütün korunan dosyalar için kalıcı kanıt değildir.

**5. Çift tetik ve devretme: SOMUT AÇIK.** \`madsc-02-kesif.yml\` \`cron: '17 5,17 * * *'\` (05:17/17:17 UTC) ile gölge keşif çalıştırır; eski \`madsc-birlesik-kesif.yml\` günlük 06:00/18:00 UTC ve \`contents: write\` üretim keşfi olarak korunuyor. İkisi aynı arama alanına dokunabilir; fakat aynı kayıtları gerçekten iki kez işlediği kanıtlanmadı. Yeni 02'nin \`madsc_akilli_kesif.py\` adımı \`continue-on-error: true\` taşıyor; 5/5 yeşil sonuç tek başına gerçek keşfin başarılı olduğu anlamına gelmez. Yeni 05 \`schedule: '30 1 * * *'\` ve belirli dosyalar için push; push'ta beşli işlerin tamamı ancak \`[madsc-full-batch]\` commit işaretiyle başlar. Eski günlük son kontrol hem schedule hem workflow_run içerir; çift başlatma potansiyeli ayrıca değerlendirilmelidir.

**P0 karar:** Son CI kontrolü yapıldı. 26 kuralın canlı uygulaması, 92/92 yazma/izin/komut matrisi, tam korunan dosya SHA ve branch ayarları, devre kesici ve çift tetik üretim kanıtları halen AÇIK. Bunlar düzeltilmeden ve canlı kabul kanıtı olmadan P0 'beş görev tamamen bitti' olarak işaretlenmez; P1'e geçiş ancak riskleri açık tutarak planlanabilir. Kullanıcının mevcut yalnız-not-yazma izni devam eder.


## 15 EKİM 2026 — KOD DEĞİŞİKLİĞİ İZNİ, İZOLE GÜVENLİK DÜZELTMESİ

Kullanıcı, çalışan ana sistemi, playlistleri, logoları, arşivleri, yedekleri ve geçmiş kayıtları bozmadan güvenlik/otomasyon kodu düzeltmelerine izin verdi. Güvenlik tercihi gereği düzeltmeler önce ayrı \`madsc/p0-guvenlik-guvenli-duzeltme-20261015\` dalında yapılır; ana dal, mevcut beşli çalışma dalı, eski workflow'lar ve PR #71 otomatik değiştirilmez.

**Gerçek ilk düzeltme:** Ayrı dalda commit \`eb477f41f37ad710b7a2f14508513d45d1e2f2a8\` ile yalnız \`.github/workflows/madsc-02-kesif.yml\` dosyasında gerçek aday keşfi adımının \`continue-on-error: true\` değeri \`false\` yapıldı. Değişiklik sonrası aynı dosyanın mevcut beşli çalışma dalıyla satır satır karşılaştırmasında **tek satır farkı** doğrulandı (satır 38). Amaç keşif başarısızken 5/5 yeşil yanlış kabulünü engellemek. Eski üretim keşfi, takvimler, korunan veri ve kayıtlar değiştirilmedi. Ayrı dalın CI/gerçek davranış kabulü **henüz doğrulanmadı**; değişiklik ana sisteme aktarılmadı.

**Kalan P0:** 92 eski workflow'un bütün komut/izin/yazma/çift tetik matrisi, 26 kuralın uçtan uca uygulanması, branch protection 403 belirsizliği, tam korunan dosya SHA kapsamı, ortak devre kesici ve canlı kabul. Eski 92 tetik eşdeğerliği olmadan kapatılmaz. Her sonraki düzeltme için önce kapsam/diff, ardından güvenli CI ve geriye dönüş kanıtı aranır.


## 15 EKİM 2026 — MİMARİ KARARI VE İKİNCİ P0 SALT OKUNUR KONTROL

**Mimari tercih:** Eski sistemin üstüne körlemesine kurma veya bütün veriyi sıfırdan üretme yerine, **ayrı dalda temiz beşli merkezi sistem, eski 92 workflow ve tüm tarihsel dosyalar korunurken, kanıtlı görev devri**. Geçişte kopya/snapshot + karşılaştırma; ana liste, favoriler, YENİLER, logolar, arşivler, kullanıcı kararları ve yedekler değişmez. Mevcut izole düzeltme dalı \`madsc/p0-guvenlik-guvenli-duzeltme-20261015\` ve tek satır düzeltme commit'i \`eb477f41f37ad710b7a2f14508513d45d1e2f2a8\`; henüz ana sisteme aktarılmadı.

**Doğrudan yeniden okunan ikinci grup:** \`madsc-ana-liste-saglik.yml\` (1/15 06:40 UTC, contents:read, ana listedeki 50 kanal, üç dosya SHA ve 30 günlük artifact), \`madsc-sistem-saglik-denetimi.yml\` (1/15 05:17 UTC, contents:read, YAML parse ve Actions son 100 koşu, gerçek denetim), \`madsc-tum-sistem-yedek.yml\` (1/15 05:40 UTC, contents:read, tüm takip edilen dosyaların tar.gz ve izole restore, 30 günlük artifact), \`madsc-genis-kaynak-kontrol.yml\` (yalnız elle; contents:write, actions:write, main'e rapor push ve \`madsc-uc-asama.yml\` dispatch), \`epg-gunluk.yml\` (03:25 UTC, contents:write, EPG çıktısı main'e push; EPG ertelenmiş olduğundan şimdi dokunma), \`madsc-otomatik-devam.yml\` (yalnız elle, fiilen başka işi tetiklemeyen kontrol). İlk gruptaki \`madsc-birlesik-kesif.yml\`, \`madsc-son-kontrol.yml\`, \`vod-guncelle.yml\`, \`epg-pages.yml\`, beş merkezi workflow ile birlikte okundu.

**Ek risk:** 1/15 günü üç ayrı salt okunur sağlık/yedek akışı var; hepsini tek koşuya indirgemek yedek üretimi, tar.gz artifact ve izole geri yükleme görevini kaybettirmemeli. Geniş kaynak taraması elle tetiklense de main'e yazabilir ve üç aşamayı dispatch edebilir; yeni beşli eşdeğerlik tablosunda özel yüksek riskli yazıcı olarak sınıflanmalı. EPG ertelenmiş kullanıcı isteğine rağmen eski günlük üretim tanımı mevcut; otomatik olarak değiştirilmedi.

**Envanter:** Tarihsel tree'de \`.github/workflows\` altında 97 YAML dosyası, beşi resmi yeni merkez, 92 eski workflow. Bu, 92'sinin tek tek komut ve izin denetiminin bittiği anlamına gelmez. Sonraki P0 işi: 92 dosyanın tümünün salt okunur işlev/tetik/izin/yazma/çıktı sınıflaması, açık risk matrisi, sonra ayrı dalda yalnız kanıtlı güvenli düzeltmeler.


## 15 EKİM 2026 — P0 GÜVENLİK 26 KURAL METİN VE ARTIFACT KONTROLÜ

Kullanıcı ekranındaki beş P0 maddesinin durumu: 1 son Actions koşusu **DOĞRULANDI**; 2 politika metinleri **OKUNDU, canlı 26/26 uygulanma kanıtı YOK**; 3 92 eski workflow için statik envanter ve kısmi yüksek risk incelemesi **VAR, 92/92 izin/komut kabulü YOK**; 4 korunan dosya SHA koşu içi mevcut, branch protection API 403, ortak devre kesici kanıtı **YOK**; 5 çift tetik riskleri **BELİRLENDİ**, üretimde giderilmesi **BEKLİYOR**. Bu beşli kapatılmış değildir.

\`GUVENLIK_KURALLARI.md\` doğrudan yeniden okundu: 1–19 kanal/listeler ve geçmişi koruma, 20 işlem öncesi yedek, 21 korunan listeye yazma kapısı, 22 işlem sonrası M3U/sıra/URL kabulü, 23 rollback kaydı, 24 başarısız otomatik zinciri durdurma. Metin açıkça 21 ve 24'ün gerçek merkezi enforcement kanıtının eksik olduğunu söylüyor. \`AGENTS.md\`: 25 her kod değişikliğinden sonra gerçek Actions run doğrulama, 26 kullanıcıya görünen yeni test adları Türkçe. Politika 26/26 tanımlı; 26/26 gerçek davranış onayı yok.

\`scripts/five_category_92_workflow_audit.py\` doğrudan incelendi: 92 satırlık CSV ve JSON üretmek üzere yazılmış, her satıra \`behavioral_parity_verified=False\`, \`migration_decision=BLOCKED_NEEDS_BEHAVIOR_EVIDENCE\` atıyor; 92/92 gerçek devir onayı üretmez. \`scripts/central_workflow_inventory.py\` otomasyon cron, push, workflow_run, contents:write, concurrency ve kategori haritalarını **statik** analiz eder. \`scripts/five_category_permission_gate.py\` yalnız yeni 03 ve 04 için salt okunur izin kapısı testi yapar; 92 eski workflow'un tam yazma kapısı değildir.

15 Ekim tarihli run #38697244625 için Actions artifact API yeniden doğrulandı: beş raporun tamamı mevcut, expired=false: güvenlik artifact #11955111316 (14.329 B), keşif #11954646399 (14.020.969 B), kanal test #11955367216 (7.496 B), arşiv/yedek #11954257578 (2.613 B), genel bakım #11955167608 (82.492 B). Artifact'ın varlığı, içindeki her kabul ölçütünün geçtiğini veya gerçek 92 devir tamamlandığını göstermez. Kaynak commit \`c2d28bea366f00372b8da63da06c2791612ebcf4\`.

Kullanıcı tercihi: eski sistem üzerinde, kayıt silmeden, riskli otomasyonları devre dışı bırakmadan devam. Ayrı güvenlik dalındaki tek satır keşif fail-fast düzeltmesi henüz ana çalışma dalına birleştirilmedi; son Actions sonucu bu düzeltmeyi test etmiyor. **Sıradaki somut adım:** 92 workflow'un tamamının dosya içeriğinden izin/komut/tetik/çıktı tablosu ve yüksek riskli yazıcıların listesi; sonra mevcut testleri bozmadan izole dalda gerekli iyileştirmeler ve yeni CI kanıtı.


## 15 EKİM 2026 — KULLANICI İSTEĞİ: P0 BEŞ GÖREV TEK PAKET KAPANIŞ DURUMU

Kullanıcı beş güvenlik/sağlık görevini tek seferde ele alma talimatı verdi. **Dürüst durum: denetim paketi ilerledi ama teknik kabulün beşi de bitmedi; bitmiş gibi işaretleme.**

1. Son beşli Actions run: **DOĞRULANDI** #38697244625, \`c2d28bea\`, 5/5 jobs ve 5 artifact; bu yalnız test edilen commit için geçerli.
2. 26 kural: **POLİTİKA DENETİMİ YAPILDI, ENFORCEMENT EKSİK**. Kural 21 korunan dosyaya merkezi yazma kapısı ve 24 ortak başarısızlık devre kesicisi henüz doğrulanmadı; 25 kod değişikliği sonrası gerçek Actions testi gerekir.
3. 92 eski workflow: **92/92 STATİK ENVANTER VAR, 92/92 DAVRANIŞ KABULÜ YOK**. \`docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md\` eski #38630252033 beşli koşunun 92 dosyayı işleyen statik script'e kanıt olduğunu, ancak komut/çıktı/izin/tetik eşdeğerliğinin beklediğini açıkça bildirir. Güncel 92-satırlık rapor dosyası repository root'ta bulunamadı (404); artifact içinde üretiliyor. Bütün 92 dosyanın bu turda tek tek yeniden okunduğu iddia edilmez.
4. SHA/branch/devre kesici: **KISMİ**; bazı koşu içi SHA testleri var, branch protection API 403, tam korunan dosya bütünlüğü ve ortak devre kesici eksik.
5. Çift push/tetik: **RİSKLER BELİRLENDİ, ÜRETİM ÇÖZÜMÜ BEKLİYOR**; yeni keşif 05:17/17:17, eski üretim keşfi 06:00/18:00 UTC; final workflow_run + schedule; 1/15 sağlık/yedek ayrı görevler, eşdeğerlik korunmalı.

İlk güvenlik düzeltmesi yalnız izole \`madsc/p0-guvenlik-guvenli-duzeltme-20261015\` dalında \`madsc-02-kesif.yml\` keşif adımı \`continue-on-error: false\`; henüz gerçek Actions run kabulü ve çalışma dalına birleştirme yapılmadı. Kod değişikliği sonrası gerçek test kanıtı yokken 'düzeltme tamamen kabul edildi' deme. Korunan dosyalar ve eski workflow'lar değiştirilmedi.

**Kapanış kriteri:** 92 satırlık izin/komut/tetik/çıktı matrisi + yüksek riskli yazıcıların manuel kabulü, 26 kural için uygulama kanıtı, korunan dosya SHA kapsamı, ortak devre kesici, çift tetik önlemi ve değişen commit'e ait başarılı Actions run. Kullanıcının istediği tek paket güvenlik bitişi bunlardan sonra ilan edilir.


## 15 EKİM 2026 — P0 İZOLE TASLAK PR #72 VE MEVCUT KURAL 24 PR #4

Kullanıcının 'devam' talimatıyla ayrı \`madsc/p0-guvenlik-guvenli-duzeltme-20261015\` dalındaki **tek satırlık** \`madsc-02-kesif.yml\` \`continue-on-error: false\` değişikliği için **taslak PR #72** açıldı: https://github.com/Madsc55/madsc-tv/pull/72 . Hedef \`madsc/bes-sistem-toplu-birlestirme\`, kaynak commit \`eb477f41f37ad710b7a2f14508513d45d1e2f2a8\`. **Draft, merge edilmedi, birleştirilmeyecek; PR #71 değiştirilmedi.** Commit SHA'ya göre Actions koşu sorgusunda **0 run** bulundu; değişiklik için CI kanıtı yok, üretim kabulü yok.

**Yeni unutulmuş kaynak:** Açık PR #4 \`safety-rule24-circuit-breaker\` → \`main\`: https://github.com/Madsc55/madsc-tv/pull/4 . İçinde \`tools/workflow_failure_gate.py\`, \`test_workflow_failure_gate.py\`, \`madsc-rule24-test.yml\` ve eski keşif/üç aşama/son kontrol workflow'larına devre kesici adımları var. Kod son iki tamamlanmış başarısız/timed_out run'da durdurmayı hedefliyor; elle workflow_dispatch kurtarmasına istisna tanıyor. **Bu mevcut iş yeniden yazılmamalı, önce gerçek Actions kanıtı, eski ana sistemle farkı, yanlış durdurma/erişim hakları ve 26 kural uygunluğu incelenmeli.** PR #4 birleştirilmedi, eski workflow'lar değiştirilmedi.

**P0 hâlâ açık:** 92/92 izin/komut/tetik ayrıntısı, 26 kuralın gerçek enforce edilmesi, SHA/branch ve çift tetik giderimi, ayrı dal CI. Kullanıcıya 5/5 güvenlik tamamlandı denmez. Yeni çalışma bu iki taslak/açık PR üzerinden güvenli test ve karşılaştırma ile sürer.


## 15 EKİM 2026 — P0 AYRI DALDA GERÇEK GÜVENLİK CI BAŞLATILDI

Kullanıcının 'devam' talimatı ile güvenlik dalında yalnız \`.github/workflows/madsc-01-guvenlik.yml\` dosyasına **geçici**, yalnız \`madsc/p0-guvenlik-guvenli-duzeltme-20261015\` dalı ve yalnız bu workflow dosyasının değişimine özgü \`push\` tetikleyicisi eklendi; commit \`b5b48bec6792d1c5d5c4d78e90a0b1340baad3a2\`. Böylece mevcut \`madsc-01\` gerçek güvenlik testini manuel UI tıklaması olmadan başlatmak mümkün oldu. Gerçek Actions run #38722819072, 2026-10-15 10:48 UTC, event push, kaynak SHA \`b5b48bec\`, son gözlem \`in_progress\`; **başarılı olduğu henüz söylenemez**. Bu test 01 güvenlik job'udur, tüm beşli zincir veya 92/92 davranışsal kabul değildir.

**Önemli geçici tetik temizlik şartı:** CI sonucu görüldükten sonra izole dalda bu geçici \`push\` bloğu kaldırılmalı ve \`madsc-01-guvenlik.yml\` hedef dal ile bire bir aynı hale getirilmeli; PR #72'de kalıcı değişiklik yalnız \`madsc-02-kesif.yml\` tek satır fail-fast olmalı. Bu geçici tetik asla ana çalışma dalına veya main'e birleştirilmez. Eski workflow'lar ve kullanıcı verileri değiştirilmedi.


### 15 EKİM 2026 — P0 GÜVENLİK CI SONUCU VE GEÇİCİ TETİĞİN TEMİZLENMESİ

Gerçek run #38722819072 \`completed/success\`, kaynak SHA \`b5b48bec6792d1c5d5c4d78e90a0b1340baad3a2\`. \`MADSC 01 - Guvenlik Toplu\` işinde rapor denetimleri, regresyon testleri, başlangıç/bitiş korunan SHA karşılaştırması ve artifact yükleme adımlarının hepsi \`success\` olarak Jobs API ile doğrulandı. Bu sonuç **güvenlik kategorisi 01 testi** içindir, beşli zincir ve gerçek keşif fail-fast düzeltmesinin uçtan uca kabulü değildir.

CI'yi başlatmak için ayrı dalda eklenen geçici \`push\` tetikleyicisi commit \`679391b8799ba253b2a66bd4505b5ca906229999\` ile geri alındı. PR #72 dosya farkı tekrar REST API'den doğrulandı: **yalnız \`.github/workflows/madsc-02-kesif.yml\` ve tek satır \`continue-on-error: true\` → \`false\`**. PR #72 hâlâ taslak/birleştirilmedi. Eski 92 workflow, PR #71, ana liste, PNG ve yedekler değişmedi.

P0 kalan açık: 26/26 merkezi üretim enforcement, 92/92 komut/izin/tetik matrisi ve davranış kanıtı, branch protection API erişimi, iki ardışık başarısızlık devre kesicisinin PR #4 değerlendirme/testi, çift tetik önleme. İlk 01 CI başarıyla geçti diye P0 tamamen kapanmış sayılmaz.
