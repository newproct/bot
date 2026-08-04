# Telegram İndirim Botu

Trendyol ve Hepsiburada'da belirlediğin arama terimlerine göre indirimli
ürünleri periyodik olarak tarayıp Telegram kanalına otomatik paylaşan bot.

## Kurulum — GitHub Actions ile (önerilen, ücretsiz, sunucu gerektirmez)

Bu yöntemde bot, GitHub'ın kendi sunucularında zamanlanmış olarak (cron) çalışır.
Bilgisayarının açık olması gerekmez.

1. GitHub'da yeni bir **repo** oluştur (private de olabilir) ve bu klasördeki
   tüm dosyaları o repoya yükle (GitHub web arayüzünden "Add file > Upload files"
   ile de yapabilirsin, git bilmene gerek yok).
2. Repo sayfasında **Settings > Secrets and variables > Actions** yoluna git.
3. "New repository secret" ile iki secret ekle:
   - `BOT_TOKEN` → BotFather'dan aldığın token
   - `CHANNEL_ID` → kanalının ID'si (örn. `@kanaladi`)
4. **Settings > Actions > General** kısmından "Workflow permissions" ayarını
   **"Read and write permissions"** yap (bot, `posted_deals.json` dosyasını
   güncelleyip commit edebilsin diye gerekli).
5. Repo'nun **Actions** sekmesine git, "İndirim Botu Tarama" workflow'unu
   göreceksin. Otomatik olarak her 30 dakikada bir çalışacak — istersen
   "Run workflow" butonuyla hemen de tetikleyebilirsin.

Zamanlamayı değiştirmek istersen `.github/workflows/scan.yml` içindeki
`cron: "*/30 * * * *"` satırını düzenle (GitHub'ın cron'u UTC saat dilimini
kullanır, Türkiye saatinden 3 saat geridir — yaz saati uygulamasına göre değişebilir).

---

## Kurulum — Kendi bilgisayarında / sunucuda (alternatif)

1. **Bot oluştur:** Telegram'da [@BotFather](https://t.me/BotFather)'a git,
   `/newbot` yaz, adım adım ilerle. Sana bir **token** verecek.

2. **Kanal oluştur ve botu ekle:**
   - Telegram'da yeni bir kanal oluştur (herkese açık veya kapalı olabilir).
   - Botunu kanala **yönetici (admin)** olarak ekle — mesaj gönderme yetkisi vermelisin.
   - Kanal herkese açıksa `CHANNEL_ID` olarak `@kanaladi` kullan.
   - Kapalıysa sayısal chat ID'sini bulman gerekir (örn. `@userinfobot` gibi
     araçlarla ya da botunu ekleyip bir Telegram API isteğiyle).

3. **Bağımlılıkları kur:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ayarları doldur:**
   `.env.example` dosyasını `.env` olarak kopyala ve kendi bilgilerinle doldur:
   ```bash
   cp .env.example .env
   ```

5. **Ayarları düzenle:**
   `config.py` içinde:
   - `SEARCH_QUERIES`: hangi ürün/kategorileri arasın
   - `MIN_DISCOUNT_PERCENT`: minimum indirim yüzdesi
   - `CHECK_INTERVAL_MINUTES`: kaç dakikada bir taransın

6. **Çalıştır:**
   ```bash
   python main.py
   ```

## ⚠️ Önemli Uyarılar

- **`scrapers/trendyol.py` ve `scrapers/hepsiburada.py` içindeki CSS
  seçiciler örnektir.** Siteler sık sık HTML yapılarını değiştiriyor ve
  bot koruması (Cloudflare vb.) kullanıyor olabilirler. Kodu çalıştırmadan
  önce tarayıcının "Öğeyi İncele" (F12) özelliğiyle güncel sayfa yapısını
  kontrol edip seçicileri güncellemen gerekebilir.
- **Kazıma (scraping), sitelerin kullanım şartlarına aykırı olabilir.**
  Uzun vadede ve sorunsuz çalışması için **Trendyol Partner** ve
  **Hepsiburada Ortaklık Programı** gibi resmi affiliate/API
  programlarına üye olup onların sağladığı ürün feed'lerini kullanmak
  hem daha stabil hem de yasal açıdan daha güvenli bir yoldur — üstelik
  satış olduğunda komisyon da kazanırsın.
- Bot'u 7/24 çalıştırmak istersen bir sunucuya (VPS, Raspberry Pi, ücretsiz
  bir cloud servisi vb.) deploy etmen gerekir; bu terminal oturumu kapanınca
  script de durur.

## Sürekli Çalıştırma (deploy) Fikirleri
- Basit bir VPS (Hetzner, DigitalOcean) üzerinde `systemd` servisi olarak
- Docker container + herhangi bir bulut sağlayıcı
- Ücretsiz katmanlı platformlar (Railway, Render vb.)

## Yapıyı Genişletme
- Yeni bir site eklemek istersen: `scrapers/` altına yeni bir dosya oluştur,
  `fetch_deals(query, min_discount)` fonksiyonunu `base.Deal` listesi
  döndürecek şekilde yaz, sonra `scrapers/__init__.py` içindeki
  `SOURCE_MAP`'e ekle.
- Affiliate API'ye geçmek istersen sadece ilgili scraper dosyasının içini
  (requests+BeautifulSoup yerine API çağrısı) değiştirmen yeterli — geri
  kalan kod (main.py, telegram_poster.py) hiç değişmeden çalışır.
