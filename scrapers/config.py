"""
İndirim Botu - Ayarlar
-----------------------
Buradaki değerleri kendi bilgilerinle doldur ya da .env dosyası kullan.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Ayarları
BOT_TOKEN = os.getenv("BOT_TOKEN", "")           # @BotFather'dan alınan token
CHANNEL_ID = os.getenv("CHANNEL_ID", "")         # Örn: @kanaladiniz  veya -1001234567890

# Tarama Ayarları
CHECK_INTERVAL_MINUTES = 30                       # Kaç dakikada bir tarasın
MIN_DISCOUNT_PERCENT = 30                         # Bu yüzdenin altındaki indirimleri paylaşma

# Hangi kaynaklar aktif olsun
ENABLED_SOURCES = ["trendyol", "hepsiburada"]

# Aranacak kategoriler / aramalar (her scraper kendi mantığında kullanır)
SEARCH_QUERIES = [
    "elektronik",
    "kulaklık",
    "ayakkabı",
    # İstediğin kadar arama terimi/kategori ekleyebilirsin
]

# Daha önce paylaşılan ürünleri hatırlamak için kullanılan dosya
POSTED_DEALS_FILE = "posted_deals.json"
