import threading
import time
import random
import os
import json

class Subconscious:
    def __init__(self, memory_gateway, intelligence_layer, interval_range=(30, 60)):
        self.memory = memory_gateway
        self.intelligence = intelligence_layer
        self.active = True
        self.insights = []
        self._lock = threading.Lock()
        self.interval_range = interval_range
        self._insight_count = 0

        # Arka plan iş parçacığını başlat
        self.thread = threading.Thread(target=self._process_background_thoughts, daemon=True)
        self.thread.start()

    def _process_background_thoughts(self):
        """Beyin boşta kaldığında anıları tarar ve içgörü üretir."""
        print("[*] Bilinçaltı aktif: Anılar arasında bağ kuruluyor...")

        while self.active:
            # Rastgele aralıkta derin düşünceye dal
            time.sleep(random.randint(*self.interval_range))

            # LLM sağlıklı değilse bekle
            if not self.intelligence.is_healthy():
                continue

            # 1. Eski anıları oku
            memories = self.memory.retrieve_memories(limit=5)
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
            insight = self.intelligence.query(prompt, "Sen bir insan beyninin bilinçaltısın. Derin ve felsefi düşün.")

            if insight and "hata" not in insight.lower() and "tıkanıklık" not in insight.lower():
                self._insight_count += 1
                with self._lock:
                    self.insights.append(insight)
                    # Son 20 içgörüyü tut
                    if len(self.insights) > 20:
                        self.insights = self.insights[-20:]

                # Bu içgörüyü kalıcı belleğe kaydet
                self.memory.store_experience({
                    "type": "subconscious_insight",
                    "content": insight[:200],
                    "connected_memories_count": 2,
                    "insight_number": self._insight_count
                }, is_critical=False)

                print(f"\n[!] Bilinçaltı yeni bir bağlantı kurdu: {insight[:50]}...")

    def stop(self):
        self.active = False
