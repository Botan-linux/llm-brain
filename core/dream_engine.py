import json
import os
import time
import random
from datetime import datetime
import threading
from core.logger import get_logger

logger = get_logger(__name__)


class DreamEngine:
    """
    Gelişmiş Rüya Sistemi (Dream Engine)
    
    Gerçek beynin REM uykusu sırasında:
    - Anılar yeniden düzenlenir (reconsolidation)
    - Kısa süreli → uzun süreli hafıza taşıması
    - Anılar arasında yaratıcı bağlantılar kurulur
    - Duygusal anılar işlenir ve sakinleştirilir
    - Rastgele düşünce akışları (default mode network)
    - Problem çözme (insanlar uykuda problem çözer)
    
    Bu modül uyku sırasında çalışır ve beynin gelişimini sağlar.
    """

    def __init__(self, memory_gateway, intelligence_layer, emotional_memory=None,
                 interval_range=(45, 90)):
        self.memory = memory_gateway
        self.intelligence = intelligence_layer
        self.emotional = emotional_memory
        self.interval_range = interval_range

        self.active = True
        self.dream_log = []
        self.insights = []
        self.creative_ideas = []
        self.problems_solved = []
        self._lock = threading.Lock()

        self._dream_count = 0
        self._rem_phase = "NREM"  # NREM veya REM
        self._cycle_count = 0

        # Arka plan thread
        self.thread = threading.Thread(target=self._dream_cycle, daemon=True)
        self.thread.start()

    def _dream_cycle(self):
        """Uyku döngüsü — NREM ve REM fazları."""
        while self.active:
            # Bekleme
            time.sleep(random.randint(*self.interval_range))

            if not self.intelligence.is_healthy():
                continue

            self._cycle_count += 1

            if self._cycle_count % 3 == 0:
                # Her 3. döngü REM fazı
                self._rem_phase = "REM"
                self._process_rem()
            else:
                # NREM fazı — hafif işleme
                self._rem_phase = "NREM"
                self._process_nrem()

    def _process_rem(self):
        """
        REM fazı — Derin rüya işleme.
        
        1. Anılar arası yaratıcı bağlantılar kur
        2. Duygusal anıları sakinleştir
        3. Çözülmemiş problemler üzerinde çalış
        4. İçgörü üret
        """
        self._dream_count += 1

        # 1. Anı birleştirme
        memories = self.memory.retrieve_memories(limit=8)
        if len(memories) < 2:
            return

        # İki rastgele anı seç
        m1, m2 = random.sample(memories, 2)
        data1 = m1.get("data", {})
        data2 = m2.get("data", {})

        # Zeka katmanına yaratıcı bağ kurma iste
        prompt = (
            f"Şu iki farklı deneyim/düşünce arasında derin ve yaratıcı bir bağ kur.\n"
            f"Sadece içgörüyü yaz, açıklama yapma. En fazla 3 cümle.\n\n"
            f"Deneyim 1: {str(data1.get('stimulus', ''))[:150]} → {str(data1.get('response', ''))[:150]}\n"
            f"Deneyim 2: {str(data2.get('stimulus', ''))[:150]} → {str(data2.get('response', ''))[:150]}"
        )

        insight = self.intelligence.query(prompt, "Rüya halinde düşünüyorsun. Mantıksal sınırlar yok. Yaratıcı ve sembolik bağlar kur.")

        if insight and "hata" not in insight.lower() and "tıkanıklık" not in insight.lower():
            insight_short = insight[:300]

            dream_record = {
                "id": self._dream_count,
                "type": "creative_connection",
                "content": insight_short,
                "connected_memories": [
                    str(data1.get("stimulus", ""))[:80],
                    str(data2.get("stimulus", ""))[:80]
                ],
                "phase": "REM",
                "timestamp": datetime.now().isoformat()
            }

            self.dream_log.append(dream_record)
            with self._lock:
                self.insights.append(insight_short)
                # İçgörü listesini sınırla
                if len(self.insights) > 30:
                    self.insights = self.insights[-30:]
            if len(self.dream_log) > 50:
                self.dream_log = self.dream_log[-50:]

            # Kalıcı belleğe kaydet
            self.memory.store_experience({
                "type": "dream_insight",
                "content": insight_short,
                "dream_number": self._dream_count
            }, is_critical=False)

            # 2. Duygusal sakinleştirme
            if self.emotional:
                self.emotional.decay(rate=0.02)

            # 3. Problem çözme girişimi
            self._attempt_problem_solving(memories)

    def _process_nrem(self):
        """
        NREM fazı — Hafif işleme.
        
        - Anı pekiştirme
        - Duygusal adaptasyon (hafif)
        - Hafıza temizliği
        """
        # Basit hafıza temizliği
        self.memory.apply_neuroplasticity(decay_rate=0.005)

        # Duygusal hafıza hafif adaptasyon
        if self.emotional:
            self.emotional.decay(rate=0.005)

    def _attempt_problem_solving(self, memories):
        """
        Rüyada problem çözme girişimi.
        
        İnsanlar uykuda bilinçsizce problemler üzerinde çalışır.
        """
        # Çözülmemiş sorunları ara (is_critical=False, kısa yanıtlar)
        unresolved = [m for m in memories if m.get("data", {}).get("response", "") == "" or
                      len(m.get("data", {}).get("response", "")) < 20]

        if not unresolved:
            return

        problem = unresolved[0]
        stimulus = problem.get("data", {}).get("stimulus", "")

        if not stimulus:
            return

        # Uykuda bu sorunu düşün
        prompt = (
            f"Uykudasın ve şu konuyu düşünüyorsun: '{stimulus[:200]}'\n"
            f"Bu konuda yeni bir perspektif veya fikir üret. En fazla 2 cümle."
        )

        solution = self.intelligence.query(prompt, "Rüya halinde yaratıcı düşünüyorsun. Felsefi ve derin.")

        if solution and "hata" not in solution.lower() and len(solution) > 20:
            self.problems_solved.append({
                "problem": stimulus[:100],
                "solution": solution[:200],
                "timestamp": datetime.now().isoformat()
            })

            if len(self.problems_solved) > 20:
                self.problems_solved = self.problems_solved[-20:]

    def get_latest_dream(self):
        """Son rüyayı döndürür."""
        if self.dream_log:
            return self.dream_log[-1]
        return None

    def get_recent_insights(self, limit=5):
        """Son içgörüleri döndürür."""
        return self.insights[-limit:] if self.insights else []

    def get_dream_report(self):
        """Rüya raporu."""
        return {
            "total_dreams": self._dream_count,
            "cycle_count": self._cycle_count,
            "current_phase": self._rem_phase,
            "pending_insights": len(self.insights),
            "creative_ideas": len(self.creative_ideas),
            "problems_addressed": len(self.problems_solved),
            "recent_dream": self.get_latest_dream()
        }

    def stop(self):
        self.active = False


if __name__ == "__main__":
    logger.debug("DreamEngine test requires memory and intelligence modules.")
    logger.debug("It runs as a daemon thread during sleep cycles.")
