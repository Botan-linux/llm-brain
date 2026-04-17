"""
Yaratıcılık Modülü (Creativity Module)

Gerçek beynin yaratıcılık mekanizmaları:
- Divergent thinking: Bir soruna çoklu alternatif çözümler üretme
- Convergent thinking: Çoklu çözümler arasından en iyiyi seçme
- Metafor oluşturma: Farklı kavramlar arasında benzerlik kurma
- Analogy detection: "X, Y'ye benzer" kalıpları
- Lateral thinking: Doğrusal olmayan düşünce yolları
- Insight: Ani "aha!" anları

Faz 2 modülü — Prefrontal Cortex ile koordineli çalışır.
"""

import json
import os
import random
import time
import threading
from datetime import datetime
from core.logger import get_logger

logger = get_logger(__name__)


class CreativityModule:
    """
    Yaratıcılık Motoru — İnsan beyninin divergent/convergent düşünce simülasyonu.

    Gerçek beynin yaratıcılığı:
    - Default Mode Network (DMN): Boşta iken rastgele fikir üretimi
    - Semantic network: Kavramlar arasında zıplama (lateral thinking)
    - Remote associates: Uzak ilişkili kavramları birleştirme
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "creativity.json"
            )
        self.storage_path = storage_path
        self._load()

        # Yaratıcı fikir havuzu
        self.idea_pool = []
        self.pending_connections = []
        self.insight_count = 0

    def _load(self):
        """Kalıcı durumu yükle."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.idea_pool = data.get("idea_pool", [])
                    self.creative_score = data.get("creative_score", 0.5)
                    self.insight_count = data.get("insight_count", 0)
                    self.analogy_history = data.get("analogy_history", [])
                    self.divergent_sessions = data.get("divergent_sessions", 0)
                    self.total_ideas_generated = data.get("total_ideas_generated", 0)
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.idea_pool = []
        self.creative_score = 0.5
        self.insight_count = 0
        self.analogy_history = []
        self.divergent_sessions = 0
        self.total_ideas_generated = 0

    def _save(self):
        """Durumu kaydet."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "idea_pool": self.idea_pool[-50:],  # Son 50 fikir
                "creative_score": round(self.creative_score, 3),
                "insight_count": self.insight_count,
                "analogy_history": self.analogy_history[-20:],
                "divergent_sessions": self.divergent_sessions,
                "total_ideas_generated": self.total_ideas_generated
            }, f, indent=4, ensure_ascii=False)

    def generate_alternatives(self, problem, context="", count=3):
        """
        Divergent Thinking — Bir soruna çoklu alternatif çözümler üret.

        Gerçek beyin bir problemi çözerken birden fazla açıdan yaklaşır:
        - Mantıksal analiz
        - Yaratıcı/metaforik yaklaşım
        - Deneysel/empirik yaklaşım
        - Felsefi/soyut yaklaşım

        Returns:
            list: Alternatif çözüm listesi
        """
        self.divergent_sessions += 1

        # Temel alternatifler (yaratıcılık puanına göre çeşitlilik artar)
        approaches = [
            {
                "type": "analitik",
                "description": f"'{problem}' konusunu mantıksal çerçeveden analiz et",
                "style": "Adım adım dedüktif yaklaşım"
            },
            {
                "type": "metaforik",
                "description": f"'{problem}' için bir metafor düşün — bu konuyu başka bir alana benzet",
                "style": "Analojik ve sembolik düşünce"
            },
            {
                "type": "yaratıcı",
                "description": f"'{problem}' hakkında sıra dışı bir perspektif sun",
                "style": "Divergent ve kontra-intüitif yaklaşım"
            },
            {
                "type": "deneyimsel",
                "description": f"'{problem}' için geçmiş deneyimlerden örneklerle yaklaş",
                "style": "İndüktif ve örneklendirme"
            },
        ]

        # Yaratıcılık puanına göre daha fazla alternatif ekle
        if self.creative_score > 0.6:
            approaches.append({
                "type": "felsefi",
                "description": f"'{problem}' konusunun derin felsefi boyutunu araştır",
                "style": "Varoluşsal ve soyut düşünce"
            })

        if self.creative_score > 0.8:
            approaches.append({
                "type": "disiplinler_arası",
                "description": f"'{problem}' konusunu farklı disiplinlerin perspektifinden ele al",
                "style": "Çok disiplinli sentez"
            })

        # Rastgele seç (sayı kadar)
        selected = random.sample(approaches, min(count, len(approaches)))
        self.total_ideas_generated += len(selected)

        return selected

    def create_analogy(self, source_concept, target_domain):
        """
        Analogy Detection — İki farklı alan arasında benzerlik kur.

        İnsan beyni yeni konuları anlamak için bilinen konulara benzetir.
        Örnek: "Beyin bir bilgisayara benzer" (classic analogy)

        Returns:
            str: Metafor/analoji açıklaması
        """
        # Basit metafor şablonları
        templates = [
            f"{source_concept}, {target_domain} alanında _____ gibi çalışır.",
            f"{source_concept} ve {target_domain} arasında ilginç bir paralellik var: her ikisi de _____.",
            f"{source_concept}'i {target_domain} perspektifinden düşündüğümüzde, _____ gibi bir yapı emerges.",
        ]

        analogy = random.choice(templates)

        # Kaydet
        self.analogy_history.append({
            "source": source_concept,
            "target": target_domain,
            "template": analogy[:100],
            "timestamp": datetime.now().isoformat()
        })

        self.creative_score = min(1.0, self.creative_score + 0.02)
        if len(self.analogy_history) % 5 == 0:
            self._save()

        return analogy

    def record_insight(self, insight_text, source="internal"):
        """
        İçgörü kaydet — Ani "aha!" anları.

        İnsanlar düşünürken bazen ani içgörüler yaşar (insight).
        Bu içgörüler kalıcı olarak saklanır.
        """
        self.insight_count += 1
        self.idea_pool.append({
            "id": self.insight_count,
            "content": insight_text[:300],
            "source": source,
            "timestamp": datetime.now().isoformat(),
            "used": False
        })

        # Yaratıcılık skoru artar
        self.creative_score = min(1.0, self.creative_score + 0.03)

        # İleriye dönük düşünce: Gelecekte kullanılabilecek bağlantılar
        if len(self.idea_pool) >= 2:
            self._generate_pending_connections()

        if self.insight_count % 3 == 0:
            self._save()

    def get_random_insight(self):
        """Rastgele bir daha önceki içgörü döndür — İlham kaynağı."""
        if not self.idea_pool:
            return None

        unused = [i for i in self.idea_pool if not i["used"]]
        if unused:
            insight = random.choice(unused)
            insight["used"] = True
            return insight["content"]

        # Hepsi kullanılmış — rastgele birini dön
        return random.choice(self.idea_pool)["content"]

    def get_creative_prompt_enhancement(self, original_prompt, mood="balanced"):
        """
        Orijinal prompt'u yaratıcılık katmanı ile zenginleştir.

        Ruh haline göre farklı yaratıcılık katmanları ekler:
        - curious: "Bu konuyu farklı açılardan düşün..."
        - happy: "Bu konuda ilham verici bir yaklaşım..."
        - analytical: "Bu konuyu derinlemesine analiz et..."
        """
        enhancements = {
            "curious": "\n[Yaratıcılık Katmanı]: Bu konuyu bilinenin ötesinde, yeni açılardan düşün. Alışılmadık bağlantılar kur.",
            "happy": "\n[Yaratıcılık Katmanı]: Bu konuda ilham verici ve motive edici bir yaklaşım sun. Pozitif enerjiyi yaratıcı düşünceye dönüştür.",
            "analytical": "\n[Yaratıcılık Katmanı]: Analitik derinliğin yanı sıra, konuyu farklı perspektiflerden de ele al. Disiplinler arası bağlar kur.",
            "engaged": "\n[Yaratıcılık Katmanı]: Konuya tamamen dal. Derin ve tutkulu bir yaklaşımla, sıra dışı fikirler üret.",
            "balanced": "\n[Yaratıcılık Katmanı]: Bu konuyu hem mantıksal hem yaratıcı açıdan düşün. Dengeli bir yaklaşım benimse.",
        }

        base = enhancements.get(mood, enhancements["balanced"])

        # Daha önceki içgörülerden birini ekle (ilham)
        random_insight = self.get_random_insight()
        if random_insight:
            base += f"\n[İçsel İlham]: {random_insight}"

        return base

    def _generate_pending_connections(self):
        """Fikir havuzundaki kavramlar arasında potansiyel bağlantılar üret."""
        recent = self.idea_pool[-5:]
        for i in range(len(recent)):
            for j in range(i + 1, len(recent)):
                self.pending_connections.append({
                    "idea_1": recent[i]["content"][:50],
                    "idea_2": recent[j]["content"][:50],
                    "strength": round(random.uniform(0.1, 0.5), 2),
                    "explored": False
                })

        # Bağlantı havuzunu sınırla
        if len(self.pending_connections) > 30:
            self.pending_connections = [c for c in self.pending_connections if not c["explored"]][-20:]

    def get_stats(self):
        """Yaratıcılık modülü istatistikleri."""
        return {
            "creative_score": round(self.creative_score, 3),
            "total_ideas_generated": self.total_ideas_generated,
            "insight_count": self.insight_count,
            "idea_pool_size": len(self.idea_pool),
            "unused_ideas": len([i for i in self.idea_pool if not i["used"]]),
            "analogy_count": len(self.analogy_history),
            "divergent_sessions": self.divergent_sessions,
            "pending_connections": len(self.pending_connections)
        }
