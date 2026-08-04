"""
Tüm scraper'ların döndürdüğü ortak veri yapısı.
Her scraper bu formatta bir liste döndürmeli, böylece geri kalan
kod (bot.py, main.py) hangi siteden geldiğini bilmeden çalışabilir.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Deal:
    id: str                 # Ürünü benzersiz tanımlayan bir kimlik (aynı ürünü tekrar
                             # paylaşmamak için kullanılır - örn. ürün URL'si ya da ürün kodu)
    title: str               # Ürün adı
    url: str                 # Ürün linki
    price: float              # İndirimli fiyat
    old_price: Optional[float]  # İndirim öncesi fiyat (varsa)
    discount_percent: Optional[int]  # Hesaplanmış / sitede yazan indirim yüzdesi
    image_url: Optional[str]  # Ürün görseli (varsa)
    source: str               # "trendyol", "hepsiburada" gibi

    def format_message(self) -> str:
        """Telegram'a gönderilecek mesaj metnini hazırlar."""
        lines = [f"🔥 <b>{self.title}</b>"]

        if self.old_price and self.discount_percent:
            lines.append(
                f"~{self.old_price:.2f} TL~ → <b>{self.price:.2f} TL</b> "
                f"(%{self.discount_percent} indirim)"
            )
        else:
            lines.append(f"<b>{self.price:.2f} TL</b>")

        lines.append(f"📍 Kaynak: {self.source.capitalize()}")
        lines.append(f"🔗 {self.url}")
        return "\n".join(lines)
