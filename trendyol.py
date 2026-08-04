"""
Trendyol Scraper
-----------------
ÖNEMLİ: Trendyol'un sayfa yapısı (HTML class isimleri vs.) zaman içinde
değişebilir ve bot koruması olabilir. Bu dosya bir İSKELET/ÖRNEKTİR —
çalıştırmadan önce gerçek sayfayı tarayıcıda inceleyip (F12 > Elements)
aşağıdaki CSS seçicilerini güncellemen gerekebilir.

Daha stabil ve yasal bir alternatif: Trendyol Partner (affiliate) programına
üye olup onların ürün feed/API'sini kullanmak.
"""
import requests
from bs4 import BeautifulSoup
from typing import List

from .base import Deal

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}


def fetch_deals(query: str, min_discount: int = 30) -> List[Deal]:
    """
    Belirtilen arama terimi için Trendyol'da indirimli ürünleri arar.
    NOT: Aşağıdaki seçiciler örnektir, gerçek siteye göre test edilip
    güncellenmelidir.
    """
    deals: List[Deal] = []
    url = f"https://www.trendyol.com/sr?q={query}&sst=DISCOUNT"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[trendyol] İstek hatası: {e}")
        return deals

    soup = BeautifulSoup(resp.text, "html.parser")

    # --- Bu kısım siteye göre güncellenmeli ---
    # Örnek: ürün kartlarını bul
    product_cards = soup.select("div.p-card-wrppr")

    for card in product_cards:
        try:
            title_el = card.select_one("span.prdct-desc-cntnr-name")
            price_el = card.select_one("div.prc-box-dscntd")
            old_price_el = card.select_one("div.prc-box-orgnl")
            link_el = card.select_one("a")
            img_el = card.select_one("img")

            if not (title_el and price_el and link_el):
                continue

            title = title_el.get_text(strip=True)
            price = _parse_price(price_el.get_text(strip=True))
            old_price = _parse_price(old_price_el.get_text(strip=True)) if old_price_el else None
            product_url = "https://www.trendyol.com" + link_el.get("href", "")
            image_url = img_el.get("src") if img_el else None

            discount_percent = None
            if old_price and price and old_price > 0:
                discount_percent = round((1 - price / old_price) * 100)

            if discount_percent is not None and discount_percent < min_discount:
                continue

            deals.append(Deal(
                id=product_url,
                title=title,
                url=product_url,
                price=price,
                old_price=old_price,
                discount_percent=discount_percent,
                image_url=image_url,
                source="trendyol",
            ))
        except Exception as e:
            print(f"[trendyol] Ürün ayrıştırma hatası: {e}")
            continue

    return deals


def _parse_price(text: str) -> float:
    """'1.299,90 TL' gibi bir metni 1299.90 float'a çevirir."""
    cleaned = text.replace("TL", "").strip()
    cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0
