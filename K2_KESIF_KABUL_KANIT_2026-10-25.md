# K2 keşif kabul kanıtı — 2026-10-25

## Gerçek Actions kanıtı (eski main sürümü)

- Workflow: `.github/workflows/madsc-birlesik-kesif.yml`
- Run: https://github.com/Madsc55/madsc-tv/actions/runs/40128823038
- Tarih: 2026-10-24; dal: `main`; sonuç: `success`.
- İş: `kesif`, başarılı. Kaynak tarama/aday test, kalıcı arşiv öncesi-sonrası, dört aşamalı rapor adımları başarılı.
- Artifact `madsc-kesif-raporu`: 12574431442 (18.096.913 bayt), mevcut.
- Artifact `candidate-logo-pngs`: 12573921683 (15.558.905 bayt), mevcut.
- EPG aday birleştirme adımı bilinçli olarak `skipped`; K2 için EPG kabulü kanıtlanmadı.

## K2 güvenlik düzeltmesi

- Dal: `fix/k2-discovery-safety-20261025`
- Commit: `9def2a33973909e5874e348a8eda69b26abac782`
- PR: https://github.com/Madsc55/madsc-tv/pull/81 (taslak; hedef merkezi fix dalı, main değil).
- Keşif checkout'u artık `main` üzerine reset edilmez; raporlar otomatik `main` commit/push yerine Actions artifact ile korunur; token `contents:read`.
- **Yeni dalda Actions koşusu henüz kanıtlanmadı.** Eski main koşusu yeni düzeltmenin testi değildir.

## Kalan kabul kapıları

1. PR #81 için workflow YAML ve K1 güvenlik incelemesi.
2. Düzeltme dalından gerçek `workflow_dispatch` koşusu; başarılı sonuç ve iki artifact kanıtı.
3. K2 kaynak/aday raporlarının K3 ve K5 tarafından gerçekten tüketildiğinin uçtan uca doğrulanması.
4. K2 raporlarını artifact'tan okuyan tüketiciler varsa, önce bunların uyarlanması; eski `madsc_kesif/` dosyalarının main'e yazılmasına bağımlı entegrasyon bozulmamalı.
5. 92 eski workflow davranış eşdeğerliği ve beşli üretim kabulü merkez #78'de ayrıca doğrulanmalı.

Korunan ana kanal listeleri, favoriler, logolar, yedekler değiştirilmedi. Bu not üretim onayı değildir.

## Yeni saptanan entegrasyon riski (inceleme zorunlu)

`scripts/discovery_archive.py` geçmişi `madsc_kesif/gecmis.json` ve `bulunan_kanal_arsivi.csv` üzerinden kalıcı okur/yazar. PR #81'in artifact-only yaklaşımı, sonraki koşuda bu dosyaların Git checkout'unda güncel bulunmasını **garanti etmez**; K2 tekrar-test engelleme geçmişi ve K3/K5 dosya tüketimi gerileyebilir. Bu nedenle PR #81 mevcut hâliyle **birleştirilmemeli**. Çözüm: kalıcı geçmişin güvenli ve atomik olarak saklanıp sonraki koşuda geri yüklenmesi; rapor tüketicilerinin de yeni konuma taşınması veya mevcut sözleşmenin korunması. Canlı uçtan uca test olmadan onay yok.

## 25 Ekim ek düzeltme: ayrı kalıcı rapor dalı

- Kalıcı arşiv dalı oluşturuldu: `madsc/k2-discovery-report-store` (`main` mevcut rapor durumundan başlangıç).
- Workflow düzeltme commit'i: `dcb4402cad078150873bf5d2b99d49d12205a909`.
- Başlangıçta arşiv dalındaki `madsc_kesif/` geçmişi yüklenir; `gecmis.json` ve `bulunan_kanal_arsivi.csv` boş/eksikse keşif hata verir (sessiz geçmiş sıfırlaması yok).
- Sonunda ayrı Git worktree içinde raporlar commit edilip yalnızca `madsc/k2-discovery-report-store` dalına push edilir; `main` için push komutu yoktur. Aynı anda yazma çakışmasında push başarısız olur, artifact saklanır; sessiz üzerine yazma yoktur.
- `contents: write` izni yalnızca rapor dalına push gereksinimi nedeniyle geri getirildi. GitHub token düzeyinde dal kapsamlı izin sınırlaması yok; güvenlik değerlendirmesi ve branch koruma kuralları ayrıca gerekli.
- **Henüz yeni workflow canlı koşusu ve K3/K5 tüketici uyumu doğrulanmadı.** Özellikle `main/madsc_kesif` okuyan mevcut tüketiciler için rapor dalından okuma veya artifact üzerinden okuma geçişi tamamlanmadan merge yapılmamalı.

## Çakışma kontrolü düzeltmesi

- Commit `b5c8cec3822adfbf76990a65c7de496db391fc71` çalışma dosyası farkını çakışma sanıyordu; normal rapor üretiminde yanlış pozitif verebilirdi.
- Commit `453cf3a964ff7dcdd63e3dc96b0c6a6a187bee12` bunun yerine rapor dalının keşif başındaki commit SHA değerini kaydedip yazmadan önce dal SHA'sını yeniden kontrol eder. Push non-fast-forward durumunda başarısız olur; geçmişin üzerine sessiz yazılmaz.
- Bu commit için PR tetiklemeli Actions koşusu bulunmadı; canlı kabul henüz yok.

## 25 Ekim — kaynak onay kapısı

- `k2_kaynak_onaylari.json` başlangıçta `sources: {}`: **0 onaylı kaynak**; kullanıcı veya yetkili kaynak onayı kanıtı olmadan onay uydurulmadı.
- `scripts/k2_source_approval_audit.py` şema, URL eşitliği, onaylayan, tarih ve kanıt alanlarını denetler (commit `2e5eabf1b2cde54915daa5c331fcfee7d5f50f61`).
- Keşif workflow'u hiç onaylı kaynak yoksa açık hata verir (`e398f6677e34a1d4b1648184e657727148dc6dfd`).
- `madsc_akilli_kesif.py` artık doğrudan çağrılsa bile yalnız `ONAYLI` ve kanıtlı kaynakları tarar (`159159660dadcb7c7a7369976fda8d6bde394c18`).
- **Mevcut 0 onay nedeniyle yeni keşif koşusunun başarıya ulaşması beklenmez.** Bu bir onay eksikliği ve güvenlik kapısıdır, tamamlanmış K2 kabulü değildir. Onay kaynağı sağlanmadan bu kontrol devre dışı bırakılmamalı.

## K2 kaynak onayı CI — gerçek sonuç

- Workflow: `K2 - Kaynak Onayı Birim Testleri`; commit `1db79abb1e48ea4de0b33f64d8bfa253788f6be6`.
- Run `40226332452`: `completed/success`.
- Run `40226336764`: `completed/success`.
- Bu iki koşu yalnız onay kayıtlarının birim testlerini doğrular; tam keşif ve gerçek cihaz kabulü değildir.
- Kaynak onay kayıtları hâlâ boş olduğundan keşif fail-closed durumdadır. Kaynak yetkilendirme kanıtı ve uçtan uca doğrulama eksiktir.

## K2 yeni test ve yol düzeltmesi

- Run `40229056952`, `40229061269`, `40229063557`, `40229067258`: `completed/success` (kaynak tekrar kontrolü testleri).
- Kaynak onay dosyası artık çalışma dizinine göre değil, tarayıcı dosyasının bulunduğu dizine göre okunur; farklı dizinden çağrılınca yanlış dosya kullanılma riski azaltıldı (`f1060b25eb3ff7f48ada9d9ac794d60f9f4464dc`).
- Regresyon testi eklendi (`9123d926f9f60a1351d13a89a86b3747e7aee689`).
- Son test commit'inin Actions sonucu ayrıca doğrulanmalıdır; kaynak onayı hâlâ sıfırdır.
