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
