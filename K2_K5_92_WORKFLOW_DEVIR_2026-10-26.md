# K2 → K5: 92 eski workflow eşdeğerliği devir ve kabul engelleri

Tarih: 2026-10-26. **Bu belge 92/92 kabulü değildir.**

## Doğrulanan gerçek durum
- Beşli sistemin referans dalı: `madsc/bes-sistem-toplu-birlestirme`.
- Bu dalda `scripts/five_category_92_workflow_audit.py`, `scripts/acceptance_26_92.py`, `docs/MADSC-92-ESDEGERLIK-KARAR-MATRISI.md` mevcut.
- Referans matriste 92 eski workflow'un **statik envanterinin** çıkarıldığı, ancak **davranışsal eşdeğerliğin 0/92** olduğu açıkça belirtiliyor. Dosya sayımı ve ortak script adı davranışsal kabul değildir.
- K2'nin `fix/k2-discovery-safety-20261025` dalında K5'in bu kabul betikleri ve beşli kategori workflow'ları bulunmuyor. K2 PR #81, beşli birleşim dalına değil farklı entegrasyon tabanına hazırlanmıştır. Bu yüzden K2'deki yeşil CI, K5 92/92'yi kanıtlamaz.
- K2'nin kaynak kayıtları `k2_kaynak_onaylari.json` içinde henüz kanıtlı `ONAYLI` kaynak bulunmuyor. Fail-closed tarama davranışı korunmalıdır.

## K5 için 92/92 kabul kanıtı (her eski workflow için)
1. Eski workflow yolu, commit SHA'sı, kategorisi ve yeni workflow/komut karşılığı.
2. Eski/yeni tetik: cron, dispatch, push, workflow_run, path/branch filtresi, eşzamanlılık.
3. En az yetki, yazma yolları, korunan veri, geri alma ve başarısızlıkta durma.
4. Aynı örnek girdiyle komut davranışı ve artifact/çıktı şema karşılaştırması.
5. Hata/timeout/tekrar/çakışma senaryosu için koşu ve log kanıtı.
6. Gerçek Actions run ID'si, commit SHA'sı ve karar: GEÇTİ / BLOKE / BEKLİYOR.

## Bağımlılıklar
- K1: 26/26 runtime güvenlik kanıtı ve yazma değişmezliği.
- K2: izinli kaynakla canlı keşif, rapor dalı geçmişi ve iki ardışık koşu.
- K3: HLS görüntü/ses, çoklu zaman ve gerçek IBO cihaz kabulü.
- K4: bağımsız harici yedekten izole geri yükleme.
- K5: 92 satırın tamamında tetik, çıktı, hata ve yan etki eşdeğerliği.

## Güvenli ilerleme kuralı
Hiçbir eski workflow bu belgeye dayanarak silinmez, devre dışı bırakılmaz veya yeniden yönlendirilmez. Ana listeler, YENİLER, YEDEKLER, FAVORİLER, logo ve arşiv korunur. `main` dalına merge yapılmaz. K5 kabul sayısı kanıt olmadan artırılmaz.

## Sonraki somut K5 işi
Referans dalda `scripts/five_category_92_workflow_audit.py` ve `scripts/acceptance_26_92.py` kullanılarak **güncel SHA** üzerinde 92 satırlık rapor üretilecek; en yüksek riskli otomatik yazıcılar önce incelenecek. Ardından kategori bazlı davranış testleri ve gerçek Actions artifact'leriyle tek tek kapatılacak.
