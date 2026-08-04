"""
Hepsiburada Scraper
---------------------
ÖNEMLİ: Trendyol scraper'ındaki uyarının aynısı burada da geçerli —
bu bir İSKELET/ÖRNEKTİR, gerçek kullanım öncesi site yapısına göre
CSS seçicilerinin doğrulanması/güncellenmesi gerekir.

Daha stabil ve yasal alternatif: Hepsiburada'nın ortaklık/affiliate
programı üzerinden ürün verisi çekmek.
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
    Belirtilen arama terimi için Hepsiburada'da indirimli ürünleri arar.
    NOT: Aşağıdaki seçiciler örnektir, gerçek siteye göre test edilip
    güncellenmelidir.
    """
    deals: List[Deal] = []
    url = f"https://www.hepsiburada.com/ara?q={query}&siralama=indirimoranu"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[hepsiburada] İstek hatası: {e}")
        return deals

    soup = BeautifulSoup(resp.text, "html.parser")

    # --- Bu kısım siteye göre güncellenmeli ---
    product_cards = soup.select("li[class*='productListContent-']")

    for card in product_cards:
        try:
            title_el = card.select_one("h3")
            price_el = card.select_one("[data-test-id='price-current-price']")
            old_price_el = card.select_one("[data-test-id='price-prev-price']")
            link_el = card.select_one("a")
            img_el = card.select_one("img")

            if not (title_el and price_el and link_el):
                continue

            title = title_el.get_text(strip=True)
            price = _parse_price(price_el.get_text(strip=True))
            old_price = _parse_price(old_price_el.get_text(strip=True)) if old_price_el else None
            href = link_el.get("href", "")
            product_url = href if href.startswith("http") else "https://www.hepsiburada.com" + href
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
                source="hepsiburada",
            ))
        except Exception as e:
            print(f"[hepsiburada] Ürün ayrıştırma hatası: {e}")
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
