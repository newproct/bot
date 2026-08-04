"""
GitHub Actions (veya benzeri cron ortamları) için tek seferlik çalıştırıcı.
main.py'daki sürekli döngü yerine, tetiklendiğinde bir kere tarama yapıp çıkar.
Zamanlama işini GitHub Actions'ın cron'u üstlenir.
"""
import logging

import config
from scrapers import SOURCE_MAP
from dedup import load_posted_ids, mark_as_posted
from telegram_poster import post_deal
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("indirim-botu")


def scan_and_post():
    log.info("Tarama başlıyor...")
    posted_ids = load_posted_ids()
    new_deal_count = 0

    for source_name in config.ENABLED_SOURCES:
        scraper = SOURCE_MAP.get(source_name)
        if not scraper:
            log.warning(f"Bilinmeyen kaynak: {source_name}")
            continue

        for query in config.SEARCH_QUERIES:
            log.info(f"[{source_name}] '{query}' aranıyor...")
            try:
                deals = scraper.fetch_deals(query, min_discount=config.MIN_DISCOUNT_PERCENT)
            except Exception as e:
                log.error(f"[{source_name}] Tarama hatası: {e}")
                continue

            for deal in deals:
                if deal.id in posted_ids:
                    continue

                success = post_deal(deal)
                if success:
                    mark_as_posted(deal.id)
                    posted_ids.add(deal.id)
                    new_deal_count += 1
                    log.info(f"Paylaşıldı: {deal.title}")
                    time.sleep(2)

    log.info(f"Tarama bitti. {new_deal_count} yeni indirim paylaşıldı.")


if __name__ == "__main__":
    if not config.BOT_TOKEN or not config.CHANNEL_ID:
        raise SystemExit("HATA: BOT_TOKEN ve CHANNEL_ID ayarlanmamış (GitHub Secrets kontrol et).")
    scan_and_post()
