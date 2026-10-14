# MADSC — YENI SOHBETE DEVIR NOTU (2026-10-15)

## Kesin proje kimligi
- GitHub: Madsc55/madsc-tv
- Ana oynatma listesi: CALISANLAR.m3u
- Birlesme calisma dali: madsc/bes-sistem-toplu-birlestirme
- Acik taslak PR: #71
- Bes is akisi: .github/workflows/madsc-01-guvenlik.yml, madsc-02-kesif.yml, madsc-03-kanal-test.yml, madsc-04-arsiv-yedek.yml, madsc-05-genel-bakim.yml.
- Hedef: eski ~92 is akisinin gorevlerini 5 ana sistemde toplamak. 92 is akisinin islevsel esdegerligi HENUZ kanitlanmadi. Eski akislar silinmeyecek/devre disi birakilmayacak; PR kullanici onayi olmadan birlestirilmeyecek.

## Kullanici icin DEGISTIRILEMEZ kurallar
- CALISANLAR.m3u icindeki mevcut kanal isimleri, ID, logo, URL, kategori ve siralari korunacak.
- Favoriler, FAVORILER 1/2, HEPSI, ⭐ YENILER ve diger kategorilere izinsiz dokunulmayacak.
- Mevcut yedekler silinmeyecek; yedekler ve korunan arsivler korunacak.
- ⭐ YENILER'e acik onay olmadan kanal eklenmeyecek; yeni kanal varsa kendi onayiyla ve alfabetik.
- Kullanici IBO Player'da ayni M3U adresini kullanmak istiyor. AYRI M3U adresi girmeye zorlanmayacak.
- Kullanici, iki/uc asamali teknik testi gecen, mevcut listede olmayan adaylarin var olan 📦 YEDEKLER kategorisinin SONUNA eklenmesini acikca istedi. Bu is icin onay var, fakat aday URL ve test kanitlari dogrulanmadan eklenmemeli. Kullanici IBO'da test edip calisiyor/calis miyor geri bildirim verecek. Teknik gecis IBO veya kanal kimligi onayi degildir.
- Mevcut CALISANLAR.m3u kontrolunde 1039 #EXTINF kaydi ve 📦 YEDEKLER (2) bulundu: TRT 1 1440P QHD ve DHA CANLI 720P HD. Bu iki kayit korunmali. Sayilar 2026-10-15 kontrolunden; yeni kontrolde tekrar say.
- Kullanici ara raporlar ve surekli kucuk commitler istemiyor; somut toplu is ve net sonuclar istiyor.

## Gercekten yapilan isler
- 5 kategori ve merkezi denetim/92 workflow haritasi calisma dalinda olusturuldu.
- 92 workflow icin behavioral_parity_verified=False, migration_decision=BLOCKED_NEEDS_BEHAVIOR_EVIDENCE; audit yesil olmasi tum otomasyonlarin tasindigi anlamina GELMEZ.
- Kesif is akisi calisma dalinda 05:17 ve 17:17 UTC salt okunur zamanlama tanimiyla hazirlandi (commit 64de193). GitHub schedule sadece default branch uzerinden calistigindan CANLI otomatik calisiyor deneme.
- EPG/Pages ve yedek kabul kontrolleri eklendi. 24 numarali MADSC 05 toplu kosusu kirmiziydi: assertion kontrol kodundaki 'contents: write' literalini yanlislikla yakaladi. Duzeltme commitleri 32c5747 ve ae46448; yeni kosu sonucu henüz teyit edilmedi.
- Ayrik IBO test listesi ureten scripts/export_ibo_two_stage_trial.py eklendi (5d07e23); madsc-03-kanal-test.yml icine cagrisi eklendi (85cbf5b). Bu ayrik test listesi kullanicinin nihai istedigi cozum DEGIL; hedef mevcut YEDEKLER kategorisidir.
- EPG/Pages gercek yayin baglantisi, offsite yedek ve eski 92 akisinin tam fonksiyon aktarimi HENUZ tamamlanmadi.

## Kritik kanal test kanitlari — veri erisimi COZULDU
- Default branch madsc_son_kontrol/summary.json (2026-10-14T12:09Z): completed 3800, TECHNICAL_PASS_IDENTITY_PENDING=2332, TECHNICAL_PASS_CONTENT_REVIEW=1055, CONTINUITY_FAILED=255, TIMEOUT=158, ready_for_playlist=0. Bunlar 3387 yeni Turk kanali demek degildir.
- Buyuk dosyalar GitHub fetch_file ile BOS content donuyor, fakat SHA uzerinden mcp__GitHub__fetch_blob ILE TAM ICERIK GELIYOR:
  - madsc_son_kontrol/results.json blob SHA: 779f7d97ce79b79e072dcf5b7d12d817054bc487 (~4.8 MB)
  - madsc_dogrulama/state.json blob SHA: c9060ffb9e3a0b046657c4933cf77a794aff861a (~5.9 MB)
- Her yeni sohbette once fetch_file ile GUNCEL SHA'yi al, sonra fetch_blob ile JSON'u oku; sabit SHA'yi yeni surumde koru diye kullanma.
- final_validation_manifest.json dogrudan okunabiliyor; 39 aday var, 30 URL o andaki ana listede yoktu. Adaylarin hepsi gecmis testlerden gecmis sayilamaz; results.json ile candidate_id eslestir.
- final_validation.py: candidate_id = sha256(url).hexdigest()[:20]; son kontrol sonucu status TECHNICAL_PASS_IDENTITY_PENDING veya TECHNICAL_PASS_CONTENT_REVIEW. madsc_dogrulama/state.json 'channels' icinde URL ve checks[]; len(checks)==3 ve her check.passed true gerekli.
- Ana listedeki tum URL'leri karsilastirarak tekrar adaylari ayikla. Turkce/Turkiye kanallarini oncele; isim, kaynak ve gercek kimlik karistirilmasin. Yalniz ad eslestirmesi yeterli degil, candidate_id URL hash eslestirmesi yap.
- Son konusmada teknik kayitlara blob uzerinden basariyla erisildi; fakat **YEDEKLER'e tek bir yeni kanal HENUZ EKLENMEDI**. Kullanici bu isin hizla tamamlanmasini istiyor.
- Iki asama/uc asama ayirimini net tut: state checks=3, son kontrol 5 dakikalik sureklilik; kimlik ve cihaz testi henuz yapilmamis.
- Ana listeye ekleme gerekiyorsa sadece var olan 📦 YEDEKLER grubuna yeni EXTINF+URL satirlari ekle; once ve sonra tum eski EXTINF ve URL'lerin ayni kaldigini programatik dogrula. Grup sayaci (2) degisecekse yalniz YEDEKLER meta verisi guncellensin; diger kategori sayaclari sabit. Kullanici eski yedeklerin sirasi ve kayitlari korunmasini istiyor. Degisikligi dogrudan main'e yapmadan once mevcut proje kurallari ve yetkili degisiklik akisini kontrol et; calisma dalindaki degisiklik IBO'nun canli listesini degistirmez.

## Yeni sohbette ONCELIK SIRASI
1. Sonuclari blob'dan al, URL-hash ile state kayitlariyla eslestir; gecen, mevcut listede olmayan, Turkce/Turkiye adaylarini ayikla. Kullanici onayi YEDEKLER eklemesi icin var.
2. Var olan YEDEKLER (2) kayitlarini koruyarak adaylari kullanicinin mevcut IBO M3U adresinden gorebilecegi sekilde gercekten ekle. Yanlis/kimligi belirsiz kanali Turk kanali diye sunma. Eger guvenilir aday yoksa acikca bildir, uydurma.
3. MADSC 05 #24 assertion duzeltmesinden sonraki kosunun sonucunu dogrula.
4. 5 sistem icin gercek islev tasimaya devam et: EPG/Pages, kurtarilabilir yedekleme, kesif, kanal testleri, 92 eski workflow parity. Korunan listeler, favoriler, izinler ve otomasyonlar dokunulmaz.
5. Toplu testleri once hazirla, tek seferde calistir; kullaniciyi surekli bekletme/tekrar sorularla yorma.

## Onemli commitler
- 2e0fddb: parity regresyon
- 64de193: kesif cron (calisma dalinda)
- 7a0cd5d: kesif zamanlama testi
- fb45519: EPG/Pages + backup kabul batch, #24 failure
- 5d07e23: isolated IBO exporter
- 85cbf5b: IBO exporter workflow baglantisi
- 32c5747 + ae46448: #24 false-positive permission assertion fix

## Yeni sohbet acilis cumlesi
'Mahmut, Madsc55/madsc-tv projesine DEVIR_NOTU_2026-10-15.md dosyasindan devam et. Once iki/uc asama testinden gecen Turk kanal adaylarini GitHub blob raporlarindan dogrulayip CALISANLAR.m3u icindeki mevcut 📦 YEDEKLER kategorisine, eski kanallara ve kategorilere dokunmadan ekle. Sonra MADSC 05 testi ve 5 sistemin gercek entegrasyonuna don. Ayrica yeni M3U adresi istemiyorum.'

## SON KULLANICI TALIMATI — YEDEKLER GERİ ALINDI
- Kullanici onceki IBO adaylarini YEDEKLER'e ekleme istegini simdilik IPTAL ETTI. Daha sonra yapilacak; simdi ekleme YAPMA.
- 2026-10-15 ana dal CALISANLAR.m3u dosyasinda 📦 YEDEKLER (14) kategorisindeki son 12 kanal cikarildi; yalnizca ilk iki kanal TRT 1 1440P QHD ve DHA CANLI 720P HD korundu.
- Ana dal commit: d647b05a013718889eafa8ca3817b885a9df8b9b.
- Diger kategorilerdeki kanallar degistirilmedi. Yeni sohbette onceki 'yedeklere hemen ekle' onceligi ARTIK GECERSIZ. Kullanici yeniden istemedikce yeni kanal ekleme; 5 sistemin kalan islerine devam et.
