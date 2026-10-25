# K5 — 92 workflow eşdeğerlik: gerçek koşu teşhisi (2026-10-26)

Bu rapor canlı GitHub Actions koşusu `40244488710` ve K5 denetim sonuçlarından derlenmiştir. **92/92 kabulü değildir.**

## Doğrulanan koşu
- K5 kanıt kayıt testi: **4/4 geçti**.
- K5 kanıt kayıt komutu: çalıştı; `production_parity_verified=false`.
- MADSC 05: **failure**.
- K1: **failure**, 26 güvenlik kuralının tamamı runtime kanıtlı değil.
- K2/K3/K4: **skipped** (K1 başarısız olduğu için).
- Önceki 92 workflow envanter çıktısı: **92 kayıt; davranışsal kabul 0; 46 eşleşmeyen script; 30 doğrulanmamış çıktı/artifact; 27 yüksek öncelikli inceleme**.

## K5 öncelikli iş sırası
1. K1'in 26/26 gerçek çalışma kanıtı engelini çöz; başarısızlığı yeşile boyama.
2. 27 yüksek riskli workflow'u tek tek eski/yeni tetik, giriş/çıkış, yan etki ve hata davranışıyla karşılaştır.
3. Kalan 65 workflow için aynı kanıtı üret; `k5_workflow_behavior_evidence.json` içine yalnız gerçek Actions run URL ve commit SHA ile kanıt gir.
4. K2 kaynak izinleri, K3 IBO cihaz testleri ve K4 geri yükleme kabulünü doğrula.
5. Sonra 92/92 bağımsız kabulü değerlendir; bu aşamaya kadar eski workflow kapatma ve yayın dosyası değişikliği yok.

## K5 güvenlik ilkesi
Kayıt formatı doğrulaması **davranışsal eşdeğerlik kanıtı değildir**. Sahte/eksik kayıtlar reddedilir. `main`, CALISANLAR, IBO listeleri, YEDEKLER, YENİLER, FAVORİLER, logo ve arşiv korunur.

Koşu: https://github.com/Madsc55/madsc-tv/actions/runs/40244488710
