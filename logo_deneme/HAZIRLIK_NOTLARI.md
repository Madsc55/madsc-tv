# Testler sürerken hazırlık — 11 Ekim 2026

## Sonuç raporu taslağı

Üç aşama tamamlanınca ayrı raporda şu alanlar bulunmalı: kanal adı, alternatif bağlantı veya yeni kanal sınıfı, üç denemenin ayrı tarihleri ve sonuçları, toplam 3/3–2/3–1/3–0/3, kimlik onayı, İsveç IBO Pro onayı, logo ve EPG durumu, kalan işlem. Denemeleri henüz tamamlanmayanlar BEKLIYOR olarak gösterilmeli; eksik deneme başarısız sayılmamalı. Üç başarılı deneme cihaz/kimlik onayı yerine geçmez. Tekrarsız URL sayısı kanal sayısı diye sunulmamalı.

Mevcut scripts/birlesik_aday_raporu.py eski puan ve 24 saat kararlılık CSV dosyalarını kullanıyor; madsc_dogrulama/state.json içindeki yeni üç deneme geçmişini henüz okumuyor. Bu nedenle o eski rapor mevcut üç denemenin sonucu sayılmayacak. Yeni akışa bağlanması geliştirme aşamasına bırakıldı.

## EPG incelemesi

Mevcut epg-gunluk.yml, GITHUB_TOKEN ile EPG dosyalarını commit/push ediyor. epg-pages.yml yalnız ilgili push ve manuel başlatmada çalışıyor; tamamlanan günlük EPG işiyle doğrudan bağlantısı yok. GitHub belgelerine göre GITHUB_TOKEN ile yapılan push yeni push iş akışını başlatmaz. Dolayısıyla kodda otomatik yenileme-yayımlama bağlantısı eksik. Bu, daha önce gözlenen Pages/depo farkını açıklayabilecek somut bir mekanizmadır; her yayımlama çalıştırmasının nedeni bu notta kesinleştirilmiş değildir.

Kaynak: https://docs.github.com/en/actions/concepts/security/github_token

Sonraki düzeltmede yayımlama aynı akış içinde veya başarı sonrası açık tetikle bağlanmalı; yayımlanan XML'in gerçek erişimi ve dosya özeti güncel çıktı ile karşılaştırılmalı. Bu hazırlıkta üretim workflow'ları değiştirilmedi. epg_deneme içindeki beş kanallık paket ayrıca hazır, cihaz görünürlüğü bekliyor.

## Güvenlik incelemesi

tools/workflow_safety.py sorgu parametrelerindeki bilinen gizli alanları ve kullanıcı bilgisini maskeliyor; URL yolunun tamamını koruyor. Bazı IPTV adresleri erişim bilgisini URL yolunda taşıyabildiği için bu yardımcı tek başına bütün adresleri gizlediği kabul edilmemeli. scripts/birlesik_aday_raporu.py YAYIN_URL alanını olduğu gibi dışarı yazıyor. Raporlara yayının tam URL'si yerine bağlantı özeti/hash ve maskeli sunucu bilgisi vermek sonraki geliştirme adımıdır.

Bu bulgular kod incelemesidir; erişim yetkilerinin tümü ve yedekten geri dönüş henüz denetlenmiş sayılmaz. Ana liste ve geçmiş raporlar bu hazırlıkta değiştirilmedi. Logo raporu yayın URL'si içermez.

## Uygulama sırası

Önce mevcut üç deneme, doğru kanal kimliği ve gerçek İsveç IBO Pro kontrolleri tamamlanır. Ardından kararlaştırılan geliştirmeler ve aylık geniş tarama/günde iki yeni aday keşfi takvimi uygulanır. Bu dosya hazırlık notudur; geliştirmelerin kurulmuş olduğunu bildirmez.
