import threading
import time
import random
import os
import json

class Subconscious:
    def __init__(self, memory_gateway, intelligence_layer):
        self.memory = memory_gateway
        self.intelligence = intelligence_layer
        self.active = True
        self.insights = []

        # Arka plan iş parçacığını başlat
        self.thread = threading.Thread(target=self._process_background_thoughts, daemon=True)
        self.thread.start()

    def _process_background_thoughts(self):
        """Beyin boşta kaldığında anıları tarar ve içgörü üretir."""
        print("[*] Bilinçaltı aktif: Anılar arasında bağ kuruluyor...")

        while self.active:
            # Her 30-60 saniyede bir derin düşünceye dal
            time.sleep(random.randint(30, 60))

            # 1. Eski anıları oku
            memories = self.memory.retrieve_memories(limit=5)
            if len(memories) < 2:
                continue

            # 2. İki rastgele anıyı seç ve aralarında bağ kurmaya çalış
            m1, m2 = random.sample(memories, 2)

            # Zeka katmanına bu iki anı arasındaki bağlantıyı sor
            prompt = f"Şu iki anı arasında mantıksal bir bağ kur ve yeni bir içgörü üret:\nAnı 1: {m1}\nAnı 2: {m2}"
            insight = self.intelligence.query(prompt, "Sen bir insan beyninin bilinçaltısın. Derin ve felsefi düşün.")

            if insight and "hata" not in insight.lower():
                self.insights.append(insight)
                # Bu içgörüyü kalıcı belleğe 'insight' olarak kaydet
                self.memory.store_experience({
                    "type": "subconscious_insight",
                    "content": insight,
                    "connected_memories": [m1, m2]
                }, is_critical=False)
                print(f"\n[!] Bilinçaltı yeni bir bağlantı kurdu: {insight[:50]}...")

    def stop(self):
        self.active = False
