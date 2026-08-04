"""
Telegram Bot API üzerinden kanala mesaj/fotoğraf gönderir.
"""
import requests

from config import BOT_TOKEN, CHANNEL_ID
from scrapers.base import Deal


def post_deal(deal: Deal) -> bool:
    """Bir indirimi kanala gönderir. Görsel varsa fotoğraflı, yoksa metin olarak."""
    caption = deal.format_message()

    if deal.image_url:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        payload = {
            "chat_id": CHANNEL_ID,
            "photo": deal.image_url,
            "caption": caption,
            "parse_mode": "HTML",
        }
    else:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": caption,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        }

    try:
        resp = requests.post(url, data=payload, timeout=10)
        resp.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[telegram] Gönderim hatası: {e}")
        return False
