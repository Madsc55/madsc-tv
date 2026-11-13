# MADSC TV ANA MERKEZ — YENİ SOHBET DEVİR NOTU
Tarih: 2026-10-25. Bu dosya üretim kabulü değildir.

## Amaç
92 eski workflow'un K1–K5'e gerçek davranışsal entegrasyonu; güvenlik, keşif, kanal test, arşiv/geri yükleme ve genel bakımın tek kanıt zincirinde çalışması.

## Sert sınırlar
Ana kanal listeleri, YEDEKLER, YENİLER, FAVORİLER, cihaz favorileri, logolar ve arşiv korunacak. Kanıtsız eski workflow kapatma yok. main'e merge yok, PR #71 merge yok. IBO cihaz testini kullanıcı yapar. Tekrarlanan gereksiz test ve kullanıcıdan tekrar bilgi isteme yok.

## Okunan kaynaklar
- `madsc/bes-sistem-toplu-birlestirme` dalında `DEVAM_NOTU.md`: tarihsel CI kayıtları, 26 runtime kuralı ve 92 davranışsal eşdeğerlik kanıt eksikliği; eski beşli CI K1 fail-closed nedeniyle K2–K4 skipped, K5 envanter başarılı.
- `main` üzerindeki `DEVAM_NOTU.md`: tarihsel 13 Ekim güvenlik kuralları ve yazma kapısı eksikleri; güncel birleşim durumu için tek başına yeterli değil.
- `fix/ibo-only-xmltv-20261025/IBO_EPG_KISA_DEVIR_2026-10-25.md`: IBO 2128.0 EPG başarısız denemeleri.
- Önceki K1–K5 sohbetlerinden aktarılan kayıtlar: main HEAD 8a138320 olduğu bildirildi; 1599/1599 offline ve beş kapı başarılı bildirildi, ama production_ready=false; 0/26 runtime, 0/92 parity, K3/K4 gerçek kabul kanıtları eksik. Bu kayıtlar güncel GitHub Actions ile yeniden doğrulanmalı.
- Beklenen K1 dalı `k1/runtime-26-immutability-evidence-20261024` bu depoda bulunamadı; K2 `K2_DEVIR_NOTU_2026-10-24.md` beklenen entegrasyon kök yolunda bulunamadı; dosya ve dalı repo genelinde keşfet.

## GitHub merkezi kayıtlar
- Issue #78 K1–K5 birleşik kabul: https://github.com/Madsc55/madsc-tv/issues/78
- Issue #77 IBO EPG: https://github.com/Madsc55/madsc-tv/issues/77
- PR #75 ve #76 deneysel EPG, doğrulanmış IBO başarısı yok. PR #71 birleştirilmez.

## IBO durumu
Sürüm 2128.0 build 2128000. TiviMate/UHF EPG gösteriyor, IBO kanalları oynatıyor ama rehber boş. Ana XMLTV, 5 kanallı XMLTV, ayrı M3U8, GitHub Raw, jsDelivr, kısa eşleşen ID denemeleri başarısız. 5 kanallı XMLTV'de 309 program var. IBO'nun XMLTV'yi gerçekten isteyip istemediği bilinmiyor. Erişim logları görülebilen kontrollü HTTPS endpoint gerekli; kurulmuş değil.

## İlk işler
1. Eski ve yeni depolarda tüm K1–K5 notları, AGENTS.md, devir dosyaları, aktif PR ve branch envanterini çıkar.
2. Güncel SHA'lara ait Actions run/job/log/artifact ve cancelled/failed sonuçları oku; eski başarılardan güncel kabul türetme.
3. K1 26/26 gerçek runtime yazma/immutability kanıtı; K2 keşif canlı kanıtı; K3 HLS ses/görüntü ve 75x6 saat; K4 harici restore; K5 92/92 parity.
4. Aynı testleri gereksiz tekrar etmeden bağımlılık sırasıyla kodu düzelt, test et, notu güncelle. main'e merge etme.
5. IBO #77 HTTP erişim kanıtı olmadan yeni rastgele XMLTV denemesi yaptırma.

## Kanıt durumu
Bu not hazırlanırken tüm aktif PR ve güncel Actions sonuçları bütünüyle denetlenmedi; gerçek üretim kabulü yapılmadı. Kesin tamamlanma yüzdesi kanıt sayımı olmadan verilmez.
