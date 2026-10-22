# MADSC — 92 Workflow Gerçek Tetik Envanteri (14 Ekim 2026)

Kaynak: GitHub `main` dalındaki `.github/workflows/` dizini; 92 YAML dosyasının içeriği ayrı ayrı okundu. Bu belge **tetik envanteridir**, görev eşdeğerliği veya canlı iş sonucu değildir.

## Otomatik takvimi bulunan 10 workflow
| Dosya | UTC cron | Korunması gereken iş |
|---|---|---|
| epg-gunluk.yml | 25 3 * * * | EPG XMLTV üretimi, teknik pilot |
| iptv-test.yml | 30 6 * * 3 | Haftalık IPTV yayın testi |
| madsc-ana-liste-saglik.yml | 40 6 1,15 * * | Korunan ana listeyi salt okunur sağlık denetimi |
| madsc-aylik-merkezi-denetim.yml | 0 7 1,15 * * | Merkezi test, kural ve rapor |
| madsc-birlesik-kesif.yml | 0 6,18 * * * | Günde iki kez aday keşfi |
| madsc-sistem-saglik-denetimi.yml | 17 5 1,15 * * | Sistem sağlık/güvenlik |
| madsc-son-kontrol.yml | 10 6 * * * | Günlük son kontrol; ayrıca workflow_run |
| madsc-tum-sistem-yedek.yml | 40 5 1,15 * * | Tam sistem yedek |
| vod-guncelle.yml | 17 7 * * * | Günlük VOD güncelleme |
| epg-pages.yml | workflow_run, cron yok | Başarılı EPG üretimi ardından Pages dağıtımı |

Not: Yukarıdaki ilk dokuz satırda cron vardır; `epg-pages.yml` yalnız zincir tetikleyicisidir. Bu tabloda 9 zamanlanmış workflow ve 1 zincir workflow gösterilir. `madsc-birlesik-kesif.yml` tek workflow'da iki günlük çalışma saatine sahiptir.

## Doğrulanan önemli ilişkiler
- `epg-pages.yml`: `EPG Günlük Güncelleme` workflow_run tamamlanması ardından başarı kapısıyla yayın.
- `madsc-genis-kaynak-kontrol.yml`: manuel koşuda `madsc-uc-asama.yml` dispatch eder.
- `madsc-uc-asama.yml`: kendi dosya adına dispatch referansı içerir; kod akışı ayrıca incelenmeden döngü denemez.
- `madsc-son-kontrol.yml`: schedule ve workflow_run birlikte; aynı görevin iki yoldan başlayıp başlamadığı kontrol edilmeli.
- Çok sayıda eski `test-13`–`test-39` ve aday workflow'u push tetikleyicisi taşır. Bunların görev kapsamı ve push path filtreleri ayrıntılı incelenmeden kapatılmaz.

## Sonraki zorunlu kabul kapıları
1. 92 workflow için tek tek **iş komutu, artifact, veri yazma, bağımlılık, güvenlik kapısı** haritası.
2. 5 yeni ana workflow'da görev eşdeğerliği ve **aynı işi iki kez çalıştırmama** kanıtı.
3. Korunan dosyalarda değişiklik olmadan EPG/Pages, yedek, VOD ve yayın testlerinin yeni zincirde çalıştığının kanıtı.
4. Açık 75 aday, harici yedek geri yükleme, EPG IBO onayı ve diğer DEVAM_NOTU/TOPLU_DURUM_RAPORU eksiklerinin kendi sistemlerinde takip edilmesi.
5. Eski workflow'lar yalnız yeni sistemde görev eşdeğerliği kanıtlandıktan sonra otomatik tetiklerden ayrılır; dosyalar ve geçmiş silinmez.

Bu inceleme sırasında hiçbir workflow, korunan playlist, logo, arşiv veya yedek değiştirilmedi.
