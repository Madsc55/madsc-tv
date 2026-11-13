# K3 — 75 kanal / 6 saat kanit protokolu

## Sinirlar

`scripts/k3_alti_saat_kanit.py` yalnizca **gercek, zaman damgali, periyodik** video ve ses cozumleme gozlemlerini degerlendirir. Kendi basina yayin testi yapmaz. Simule veya birim testi verisi gercek yayin kaniti degildir. Her aday icin en az 6 saatlik zaman araligi, 300 saniyeyi asmayan gozlem bosluklari, butun gozlemlerde gercek `video_ok=true` ve `audio_ok=true` gerekir. En az 75 **ayri** `channel_id` kaydi gerekir. Sonuc olumlu olsa bile `kesintisiz_oynatma_kaniti=YOK` kalir.

## Giris ve komut

Yayin URL'si veya gizli token icermeyen JSONL satirlari:

```json
{"channel_id":"opaque-id-001","timestamp":"2026-10-25T10:00:00+00:00","video_ok":true,"audio_ok":true}
```

Her satir gercek FFmpeg video/ses cozumleme sonucundan uretilmeli; benzersiz `channel_id` kimlikleri tek bir yayini birden fazla kanal gibi gostermemeli. Kimlik/URL eslestirmesi gizli ve ayri tutulmali. Her 5 dakikadan daha sik periyodik probe olusturulabilir.

```sh
python3 scripts/k3_alti_saat_kanit.py /guvenli/yol/gercek_k3_olcumleri.jsonl --output /guvenli/yol/k3_ozet.json
```

Kod eksik/bozuk zaman damgasi, yinelenen olcum, eksik ses/video ve alti saatten kisa kaniti reddeder. Kabul olusmadiginda cikis kodu 1 olur. Bu kanit cihazda kesintisiz oynatmayi ispatlamaz.

## Kapanis kontrolu

1. 75 ayri yayinin yetkili, gercek, zaman damgali olcumleri toplanmali ve kanit dosyasi korunmali.
2. IBO gercek cihazinda goruntu/ses, kanal kimligi, XMLTV/EPG saat dilimi ve program eslesmesi manuel dogrulanmali.
3. K1–K5 davranissal entegrasyon ve geriye donuk uyumluluk CI kanitlari kontrol edilmeli.
4. Ana M3U, yedek, favori ve arsiv listeleri otomatik degistirilmemeli; kabul tamamlanmadan PR #79 main'e alinmamali.
