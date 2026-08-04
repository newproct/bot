"""
Aynı ürünü kanala tekrar tekrar paylaşmamak için basit bir kayıt sistemi.
JSON dosyasında paylaşılan ürün ID'lerini tutar.
"""
import json
import os
from typing import Set

from config import POSTED_DEALS_FILE


def load_posted_ids() -> Set[str]:
    if not os.path.exists(POSTED_DEALS_FILE):
        return set()
    try:
        with open(POSTED_DEALS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except (json.JSONDecodeError, IOError):
        return set()


def save_posted_ids(ids: Set[str]) -> None:
    with open(POSTED_DEALS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f, ensure_ascii=False, indent=2)


def mark_as_posted(deal_id: str) -> None:
    ids = load_posted_ids()
    ids.add(deal_id)
    save_posted_ids(ids)
