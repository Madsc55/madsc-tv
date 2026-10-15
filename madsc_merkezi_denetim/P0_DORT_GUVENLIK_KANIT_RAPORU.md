# P0 dört güvenlik görevi — gerçek Actions kanıtı ve düzeltme sınırları

Tarih: 2026-10-15

## Gerçek test

- Koşu: https://github.com/Madsc55/madsc-tv/actions/runs/38729974047
- 26 regresyon testi başarılı.
- 92 eski workflow incelendi; 24 riskli dosya ve 24 yazma adayı.
- Risk kabul kapısı **bilerek başarısız**; rapor artifact `madsc-p0-dort-guvenlik-tek-kabul` olarak üretildi.
- Bu 24 kayıt gerçek ihlal değil; statik tarama ve koruma kanıtı eksikliğidir.

## Somut sınırlamalar

1. `epg-gunluk.yml`: günlük cron, `contents: write`, `git push`, üst düzey concurrency yok, doğrudan kural 24 kapısı yok. EPG kullanıcı tarafından ertelendi; üretim dosyasına dokunulmadı.
2. `vod-guncelle.yml`: günlük cron, `contents: write`, `git push`, üst düzey concurrency yok, doğrudan kural 24 kapısı yok. Üretim dosyasına dokunulmadı.
3. `publish-iptv-png-logos.yml`: job-level `contents: write`, `git push`, üst düzey concurrency yok; logolar kullanıcı koruması altında olduğundan üretim dosyasına dokunulmadı.
4. `madsc-son-kontrol.yml`: cron ve `workflow_run` birlikte; doğrudan kural 24 çağrısı var. İki farklı tetik kaynağının aynı sonucu iki kez yazmayacağı kanıtlanmadı.
5. `madsc-uc-asama.yml`: doğrudan kural 24 çağrısı var; ayrıca koşullu dispatch olasılığı mevcut.
6. `test-32-unapproved-write-regression.yml`, `test-38-audit-selftest.yml`, `toplu-sistem-kontrol.yml`: `git push` metni görüldü fakat metin araması gerçek push çalıştığını kanıtlamaz; bunlar ayrıca manuel semantik inceleme gerektirir.
7. GitHub `main` branch protection REST çağrısı 403 `Resource not accessible by integration`. Korumanın kapalı olduğu söylenemez; bu bağlantının erişimi yetersiz.
8. Korunan dosya yazma tarayıcısı rapor üretir; inceleme gerektiren sonuçları her durumda durduran zorunlu kapı olduğuna dair kanıt bulunmuyor.

## Kabul kararı

- Görev 1: **TAMAM**.
- Görev 2: **AÇIK** — 26/26 teknik enforcement kanıtı eksik.
- Görev 3: **KISMİ** — 92/92 statik tarama tamam, 24 risk satırı açık.
- Görev 4: **KISMİ** — SHA başarılı, branch protection 403, devre kesici kapsaması eksik.
- Görev 5: **KISMİ** — tetikleme riskleri bulundu, dinamik önleme kanıtı eksik.

**Bu dosya tek başına koruma uygulamaz.** Riskli eski workflow'ların tamamını izinsiz kapatmak, EPG/logo/yedek üretimini değiştirmek, ana dalı birleştirmek veya kullanıcı kurallarını değiştirmek bu kapsamda yapılmadı. Kabulü yeşil göstermek için risk kontrolleri gevşetilmeyecek.

## 15 Ekim — 21 riskin gerçek dosya incelemesi

- Son kanıt koşusu #38731442193: **26/26 regresyon testi başarılı; 92/92 eski workflow tarandı; 21 risk satırı ve 21 yazma adayı kaldı.** Kabul kapısı kasıtlı olarak kırmızı.
- İlk 24 riskin üçü salt-okunur denetim dosyasıydı; yanlış pozitif sınıflaması ayrıştırıldı. Bu, üretim korumasının eklendiği anlamına gelmez.
- `madsc-birlesik-kesif.yml`, `madsc-son-kontrol.yml`, `madsc-uc-asama.yml`: kural24 çağrısı ve concurrency mevcut; `git reset --hard origin/main` kullanımının gerçek etkisi, iki olay türü ve dispatch davranışı ayrıca dinamik kanıt gerektirir.
- `madsc-11599-yedek-geri-yukle.yml`, `madsc-arsiv-yedek-aktarim.yml`, `madsc-ibo-3-5281.yml`, `madsc-ibo-354-classify.yml` ve sekiz diğer IBO/geri-yükleme workflow'u kaynak düzeyinde okundu. Birçoğu kendi workflow dosyasının `push` değişikliğinde tetiklenir ve `main` dalına `git push origin HEAD:main` yapar. Bazıları `CALISANLAR.m3u` yazar. Bu dosyalarda koruma eklemek dahi üretimde istenmeyen otomatik yazma tetikleyebileceğinden doğrudan değiştirilmedi.
- `epg-gunluk.yml`, `vod-guncelle.yml`, `publish-iptv-png-logos.yml`: doğrudan yazma, üst düzey concurrency ve doğrudan rule24 eksikliği doğrulandı; EPG/logo koruması nedeniyle değiştirilmedi.
- `madsc-yedek-turk-ayir.yml`, `madsc-yedekler-sayi-duzelt.yml`, `madsc-genis-kaynak-kontrol.yml`: gerçek yazma adımları ve eksik doğrudan rule24 çağrıları doğrulandı.
- **Kabul hâlâ AÇIK.** GitHub branch protection API 403. Bir statik denetim sonucu üretimde zorunlu yazma engelinin uygulandığını kanıtlamaz. Kalan gerçek riskleri sadece test filtresinden çıkararak yeşil göstermeyeceğiz.
- Güvenli sonraki aşama: üretim workflow'larının her biri için yazma hedefi, onay kapısı, tetikleme, devre kesici ve concurrency öncesi/sonrası davranışını ayrı PR'de izole testle kanıtlamak; `main`'e merge yok.

## Izole P0 yazma engeli denemesi
- Dal: `madsc/p0-guvenli-yazma-kapisi-deneme-20261015`; kaynak: `madsc/p0-dort-guvenlik-kabul-20261015`.
- `madsc-ibo-3-5281.yml` denemesinde otomatik `push` yerine yalnız `workflow_dispatch`, `contents: read` ve `main` commit/push yerine bilgilendirme kondu.
- Bu bir **davranış değiştiren prova**; gerçek arşiv yazma ihtiyacını karşılayan nihai workflow olarak birleştirilmemeli. İşlemi `main` dalına taşımak YASAK; onay ve test gerekir.
- Bu izole workflow'un gerçek çalıştırma testi henüz yapılmadı. Güvenlik kabulü hâlâ açık; eski üretim workflow'ları korunuyor.

## Salt-okunur IBO provası (güncel)
- Commit `00b3ef09`: `madsc-ibo-3-5281.yml` izole dalda manuel-only, `contents: read`, `persist-credentials: false`, `concurrency` ve dal eşitliği kontrolüyle değiştirildi.
- ÖNEMLİ: Önceki prova yanlışlıkla `scripts/apply_ibo_3_5281.py` çalıştırabilirdi; bu kaldırıldı. Yeni prova sadece Python AST syntax, gerekli dosyalar ve `git diff --exit-code` kontrollerini çalıştırır. Gerçek veri değiştirme/commit/push yok.
- Manuel workflow_dispatch koşusu henüz başlatılmadı. Bu prova gerçek yazma yetkilendirmesini test etmez ve üretime alınamaz. P0 kabulü hâlâ açık.

## KALICI PLAN — Manuel başlatma yalnızca geçici prova (kullanıcı kararı)
- Kullanıcı onayıyla kesinleştirildi: `madsc-ibo-3-5281.yml` için `workflow_dispatch`-only ve `contents: read` **kalıcı üretim tasarımı DEĞİLDİR**; yalnızca izole, salt okunur güvenlik denemesidir.
- **YAPILACAK / AÇIK:** Kanıt ve kabul tamamlandıktan sonra gereken otomatik tetiklemeyi, üretimdeki gerçek kanal ayırma/arşiv işlevini kaybetmeden güvenli biçimde geri getir. Çift tetiklemeyi önle; concurrency, hata devre kesici, korunan dosya yazma yetkilendirme kapısı ve main branch koruma kanıtını uygula/doğrula. Kullanıcı izni olmadan üretim yazma akışlarını açma, main'e merge yapma veya korunan veri değiştirme.
- **Sıra:** (1) manuel salt-okunur prova çalıştırma kanıtı, (2) gerekli otomatik davranış için izole tasarım ve regresyon, (3) yazma yetkisi/branch koruma onayı, (4) kullanıcı onaylı devreye alma. Bu adımlar bitmeden otomatik işlevin geri geldiğini söyleme.
- Bu not, geçici manuel durumun unutulmaması için tutuldu. DURUM: AÇIK.

## Başarılı gerçek izole prova — 2026-10-15
- GitHub Actions: https://github.com/Madsc55/madsc-tv/actions/runs/38734458156
- SHA: `18adcda209a3771d96b86edd454237870bf8edaa`.
- Sonuç: `completed/success`; 7/7 iş adımı başarılı.
- Salt okunur `contents: read`, `persist-credentials: false`, yalnız test dalı için push tetikleyicisi, AST sözdizimi, dosya varlığı ve `git diff --exit-code` doğrulandı.
- **Geçici push tetikleyicisi yalnız `madsc/p0-guvenli-yazma-kapisi-deneme-20261015` dalında; üretim otomasyonunun geri açıldığı anlamına gelmez.** Kullanıcının kararı: kalıcı olarak manuel-only bırakılmayacak. Gerekli otomatik işlevi koruyan güvenli tasarım, yazma yetkisi kapısı ve branch protection kanıtı tamamlanınca ayrı kabul/dağıtım yapılacak.
- 21 eski workflow güvenlik kabul riski hâlâ açık. Bu prova 21 riski kapatmaz.

## Turkce baslikli tarihsel surum testi - 15 Ekim 2026
- GitHub Actions kosusu 38735532105, SHA 3244e46cffd763a8bc853fa6e68fbb501d4e15bb: 9/9 adim basarili.
- Dort tarihsel CALISANLAR.m3u Git blob kimligi GitHub API uzerinden dogrulandi: b5ce4a752104, 2c5bbe376a20, a40e0df02d7a, d647b05a0137.
- 11367 sahte YEDEKLER kaydi ile IBO betigi gecici dizinde basarili calisti; kaynak liste SHA256 degismedi.
- Workflow adi ve adimlari Turkce numaralandirildi.
- Sinir: Bu test her bir arsiv kanalinin eksiksiz oldugunu ve mevcut 2 yedek icin eski 11367 kararlarinin yeniden uygulanabilecegini kanitlamaz. Uretim yazma kapisi ve otomatik baslatma hala ACIK.

## 6. Test - IBO arsiv ve karar kayitlari dogrulandi
- GitHub Actions 38735745705; commit 1ea81f8a8f9ad8db42123ef80672b75dc0ef77df; 10/10 adim basarili.
- Ilk IBO arsivinde 5252 baglanti, karar CSV dosyasindaki ARSIVE_ALINDI satirlariyla ayni sirada eslesti.
- 27 YEDEKLERDE_KALDI karari rapordaki Turk konumlariyla eslesti; 11367 - 5252 = 6115 sayisi dogrulandi.
- Kontrol salt okunur ve gecici test dizini disinda kanal listelerine yazma yok.
- Sinir: Bu sonuc yalniz ilk IBO 3-5281 arsivi icindir. Diger arsivlerin butunlugu ve uretim otomatik yazma kapisi hala ACIK.

## 7. Test - Diger alti IBO arsivi dogrulandi
- GitHub Actions kosusu 38735950829; commit d3b44e3193ec62e6ac71f8b5285d255e08a23002; 11/11 adim basarili.
- Raporlarla eslesen arsiv kayitlari: ikinci IBO 5585, 399-530 132, 16-49 34, 355-364 10, Turk calismaz 332, yabanci 20. Toplam 6113 arsiv kaydi.
- Ilk IBO arsivindeki 5252 kayitla birlikte yedi dosyanin kayit sayilari kontrol edildi. Bu, benzersiz kanal sayisi ya da tum arsivlerin birbirinden ayrik oldugu iddiasi degildir.
- Gercek kanal listeleri degistirilmedi. Uretim yazma kapisi ve guvenli otomatik baslatma gorevleri ACIK.

## 8. Test - Guvenli otomatik baslatma denemesi
- GitHub Actions 38736246297; commit 477d0b5d850aa7cda5d804b1e8448be4c9e47351; 12/12 adim basarili.
- Otomatik tetikleme sadece izole test dalindaki workflow degisikliginde; workflow_dispatch manuel secenegi de var.
- contents read, persist-credentials false, concurrency ve cancel-in-progress false ayarlari denetlendi. Test, gercek listeye yazma yapmiyor.
- Ilk kosu 38736179870 test regex kacis hatasi nedeniyle basarisizdi; hata duzeltildi ve yeni kosu gecti.
- KALICI GOREV ACIK: Bu test eski IBO kanal ayirma workflow'unun canli otomatik yazma yetkisini geri getirmez. Tarihsel tek-seferlik 11367 kanal kararlari guncel 2 yedekli listeye yeniden uygulanmayacak. Uretim guvenlik kapisi, kalan 21 risk ve onay gereksinimi devam ediyor.

## 9. Test - Korunan dosya yazma kapisi izole denemesi
- GitHub Actions 38736442357; commit 4f0fb99ec749be39ee2c8c19a1dbf99d949a5a4d; 13/13 adim basarili.
- Gecici Git deposunda CALISANLAR.m3u, AGENTS.md ve GUVENLIK_KURALLARI.md icin git diff --quiet HEAD kontrolu kullanildi.
- Temiz durum kabul edildi; izinsiz kanal listesi ve guvenlik kurali degisiklikleri reddedildi; eski hale donen dosya kabul edildi.
- Bu yalniz bir izolasyon kanitidir; canli workflow yazma yollarina entegre edilmis zorunlu bir kapi DEGILDIR. Canli koruma, 21 risk ve dal korumasi onaylari hala aciktir.
