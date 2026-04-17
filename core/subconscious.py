import threading
import time
import random
import os
import json
from core.logger import get_logger

logger = get_logger(__name__)

class Subconscious:
    def __init__(self, memory_gateway, intelligence_layer, interval_range=(30, 60)):
        self.memory = memory_gateway
        self.intelligence = intelligence_layer
        self.active = True
        self.insights = []
        self._lock = threading.Lock()
        self.interval_range = interval_range
        self._insight_count = 0
        self._own_failures = 0  # Kendi hata sayacı (global is_healthy bağımsız)

        # Arka plan iş parçacığını başlat
        self.thread = threading.Thread(target=self._process_background_thoughts, daemon=True)
        self.thread.start()

    def _process_background_thoughts(self):
        """Beyin boşta kaldığında anıları tarar ve içgörü üretir."""
        logger.info("Bilinçaltı aktif: Anılar arasında bağ kuruluyor...")

        while self.active:
            # Rastgele aralıkta derin düşünceye dal
            time.sleep(random.randint(*self.interval_range))

            # Kendi hata sayacı ile kontrol — global is_healthy() ana thread'deki hatalardan etkilenmesin
            if self._own_failures >= 5:
                logger.warning("Bilinçaltı: 5 art arda hata, beklemede...")
                time.sleep(120)
                self._own_failures = 0

            # 1. Eski anıları oku
            try:
                memories = self.memory.retrieve_memories(limit=5)
            except Exception as e:
                logger.debug(f"Bilinçaltı: Hafıza okuma hatası: {e}")
                continue

            if len(memories) < 2:
                continue

            # 2. İki rastgele anıyı seç ve aralarında bağ kurmaya çalış
            m1, m2 = random.sample(memories, 2)

            # 3. Zeka katmanına bu iki anı arasındaki bağlantıyı sor
            prompt = (
                f"Şu iki anı arasında mantıksal bir bağ kur ve yeni bir içgörü üret:\n"
                f"Anı 1: {json.dumps(m1.get('data', {}), ensure_ascii=False)[:200]}\n"
                f"Anı 2: {json.dumps(m2.get('data', {}), ensure_ascii=False)[:200]}"
            )

            try:
                insight = self.intelligence.query(prompt, "Sen bir insan beyninin bilinçaltısın. Derin ve felsefi düşün.")
            except Exception as e:
                self._own_failures += 1
                logger.debug(f"Bilinçaltı: LLM çağrı hatası: {e}")
                continue

            # Başarılı çağrı → reset
            self._own_failures = 0

            if not insight:
                continue
            if "hata" in insight.lower() or "tıkanıklık" in insight.lower() or "bağlantı" in insight.lower():
                self._own_failures += 1
                continue

            self._insight_count += 1
            with self._lock:
                self.insights.append(insight)
                if len(self.insights) > 20:
                    self.insights = self.insights[-20:]

            try:
                self.memory.store_experience({
                    "type": "subconscious_insight",
                    "content": insight[:200],
                    "connected_memories_count": 2,
                    "insight_number": self._insight_count
                }, is_critical=False)
            except Exception:
                pass

            logger.info(f"Bilinçaltı yeni bir bağlantı kurdu: {insight[:50]}...")

    def stop(self):
        self.active = False
