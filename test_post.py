"""
Test Scripti
-------------
Scraper'lar çalışmadan, sadece Telegram bağlantısının doğru ayarlandığını
kontrol etmek için sahte bir ürünle deneme mesajı gönderir.
"""
import config
from scrapers.base import Deal
from telegram_poster import post_deal

if __name__ == "__main__":
    if not config.BOT_TOKEN or not config.CHANNEL_ID:
        raise SystemExit("HATA: BOT_TOKEN ve CHANNEL_ID ayarlanmamış.")

    test_deal = Deal(
        id="test-001",
        title="TEST ÜRÜNÜ - Bu gerçek değil",
        url="https://example.com",
        price=199.90,
        old_price=399.90,
        discount_percent=50,
        image_url=None,
        source="test",
    )

    success = post_deal(test_deal)
    if success:
        print("Başarılı! Kanalı kontrol et.")
    else:
        print("Gönderim başarısız. BOT_TOKEN/CHANNEL_ID ayarlarını ve botun kanalda admin olduğunu kontrol et.")
