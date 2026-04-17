"""
Sezgisel Düşünce Modülü (Intuition Module)

Gerçek beynin sezgi mekanizmaları:
- Gut feeling: Bilinçsiz hızlı değerlendirme
- Pattern matching: Bilinen örüntüleri yeni durumlara uygulama
- Heuristic decision support: Hızlı karar destek
- Rapid categorization: Anlık kategorizasyon
- Uncanny detection: Tuhaflık / anormallik algılama

Bu modül hızlı, bilinçsiz işlemleri simüle eder.
Prefrontal Cortex'ten farklı olarak — analitik değil, sezgiseldir.
"""

import json
import os
import random
from datetime import datetime
from core.logger import get_logger

logger = get_logger(__name__)


class IntuitionModule:
    """
    Sezgisel Düşünce Motoru.

    Gerçek beyinde:
    - Amygdala hızlı tepki verir (sistem 1 - Kahneman)
    - Prefrontal cortex yavaş analiz yapar (sistem 2)
    - Sezgi, sistem 1'in ürünüdür — hızlı, otomatik, bilinçsiz
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "intuition.json"
            )
        self.storage_path = storage_path
        self._load()

    def _load(self):
        """Kalıcı durumu yükle."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.intuition_accuracy = data.get("intuition_accuracy", 0.5)
                    self.pattern_library = data.get("pattern_library", [])
                    self.gut_feelings_log = data.get("gut_feelings_log", [])
                    self.total_intuitions = data.get("total_intuitions", 0)
                    self.correct_intuitions = data.get("correct_intuitions", 0)
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.intuition_accuracy = 0.5
        self.pattern_library = []
        self.gut_feelings_log = []
        self.total_intuitions = 0
        self.correct_intuitions = 0

    def _save(self):
        """Durumu kaydet."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "intuition_accuracy": round(self.intuition_accuracy, 3),
                "pattern_library": self.pattern_library[-50:],
                "gut_feelings_log": self.gut_feelings_log[-30:],
                "total_intuitions": self.total_intuitions,
                "correct_intuitions": self.correct_intuitions
            }, f, indent=4, ensure_ascii=False)

    def get_gut_feeling(self, stimulus, context=None):
        """
        Gut Feeling — Bilinçsiz hızlı değerlendirme.

        İnsanlar bir duruma karşı ilk tepkisini genellikle sezgisel verir.
        Bu, bilinçsiz pattern matching'in sonucudur.

        Returns:
            dict: Sezgisel değerlendirme
        """
        self.total_intuitions += 1

        # Sezgisel sinyal hesaplama
        feeling = self._calculate_feeling(stimulus, context)

        # Kaydet
        self.gut_feelings_log.append({
            "stimulus_preview": stimulus[:50],
            "feeling": feeling["type"],
            "confidence": feeling["confidence"],
            "timestamp": datetime.now().isoformat()
        })

        if self.total_intuitions % 10 == 0:
            self._save()

        return feeling

    def _calculate_feeling(self, stimulus, context):
        """Sezgisel sinyal hesapla — bilinçsiz pattern matching."""
        stimulus_lower = stimulus.lower()

        # Tehlike algılama — amygdala benzeri hızlı tepki
        danger_signals = ["yardım", "acil", "tehlike", "korku", "endişe", "sorun", "hata",
                         "bozuk", "çalışmıyor", "olumsuz", "kötü"]
        opportunity_signals = ["fırsat", "yeni", "keşfet", "ilginç", "harika", "süper",
                            "güzel", "mükemmel", "başarı", "olumlu"]
        familiarity_signals = ["tekrar", "daha önce", "aynı", "biliyorum", "bunu",
                            "hatırlıyorum", "gene"]

        # Pattern matching
        danger_score = sum(1 for s in danger_signals if s in stimulus_lower)
        opportunity_score = sum(1 for s in opportunity_signals if s in stimulus_lower)
        familiarity_score = sum(1 for s in familiarity_signals if s in stimulus_lower)

        # Öncelik: Tehlike > Fırsat > Bilinen > Nötr
        if danger_score > 0:
            return {
                "type": "caution",
                "confidence": min(0.9, 0.4 + danger_score * 0.15),
                "description": "Sezgisel uyarı: Dikkatli ol. Kötü bir his var.",
                "recommendation": "Bu konuda temkinli yaklaş. Daha fazla bilgi topla."
            }
        elif opportunity_score > 0:
            return {
                "type": "opportunity",
                "confidence": min(0.85, 0.4 + opportunity_score * 0.15),
                "description": "Sezgisel heyecan: Burada bir fırsat var.",
                "recommendation": "Bu konuyu keşfet. Olumlu bir sonuç olabilir."
            }
        elif familiarity_score > 0:
            return {
                "type": "familiar",
                "confidence": min(0.8, 0.4 + familiarity_score * 0.15),
                "description": "Sezgisel tanıma: Bu durumu daha önce gördüm.",
                "recommendation": "Önceki deneyimlerini kullan. Benzer bir yaklaşım işe yarayabilir."
            }
        else:
            # Bilinen örüntü yok — rastgele sezgi (gerçek beyin de bazen rastgele hisseder)
            random_feeling = random.choice(["neutral", "curious", "wary"])
            feelings = {
                "neutral": {
                    "type": "neutral",
                    "confidence": round(random.uniform(0.2, 0.4), 2),
                    "description": "Sezgisel nötrlük: Duygusal bir sinyal yok.",
                    "recommendation": "Sakin ve analitik yaklaş."
                },
                "curious": {
                    "type": "curious",
                    "confidence": round(random.uniform(0.3, 0.5), 2),
                    "description": "Sezgisel merak: Bir şey dikkatimi çekti.",
                    "recommendation": "Konuyu derinleştir. Merakını takip et."
                },
                "wary": {
                    "type": "wary",
                    "confidence": round(random.uniform(0.25, 0.45), 2),
                    "description": "Sezgisel tedbirli: Tam emin değilim.",
                    "recommendation": "Dikkatli ilerle. Sorular sor."
                }
            }
            return feelings[random_feeling]

    def detect_anomaly(self, stimulus, recent_stimuli):
        """
        Anormallik Algılama — Tuhaflık / beklenmeyen durum tespiti.

        İnsan beyni normalden sapmaları hızla algılar (predictive coding).

        Returns:
            bool: Anomali tespit edildi mi
        """
        if not recent_stimuli:
            return False

        # Uzunluk anomalisi
        avg_len = sum(len(s) for s in recent_stimuli[-5:]) / len(recent_stimuli[-5:])
        current_len = len(stimulus)

        if current_len > avg_len * 3 or current_len < avg_len * 0.2:
            return True

        # Ton anomalisi (sorular arası)
        question_ratio = sum(1 for s in recent_stimuli[-5:] if "?" in s) / len(recent_stimuli[-5:])
        current_is_question = "?" in stimulus

        if current_is_question and question_ratio > 0.8:
            return False  # Soru soran bir konuşma — normal
        elif current_is_question and question_ratio < 0.2 and question_ratio > 0:
            return True  # Aniden soru sordu — anomal olabilir

        return False

    def learn_pattern(self, stimulus, outcome_positive):
        """
        Örüntü öğren — Sezgi doğruluğunu geliştir.

        Args:
            stimulus: Uyaran
            outcome_positive: Sonuç olumlu mu?
        """
        self.pattern_library.append({
            "stimulus_preview": stimulus[:80],
            "outcome": "positive" if outcome_positive else "negative",
            "timestamp": datetime.now().isoformat()
        })

        if outcome_positive:
            self.correct_intuitions += 1

        # Sezgi doğruluğu güncelle
        if self.total_intuitions > 0:
            self.intuition_accuracy = self.correct_intuitions / self.total_intuitions

        if len(self.pattern_library) % 10 == 0:
            self._save()

    def get_intuitive_prompt_modifiers(self):
        """Sezgisel modifier'ları döndürür — Yanıt tarzını etkiler."""
        modifiers = []

        # Sezgi doğruluğu yüksekse daha fazla sezgisel özgüven
        if self.intuition_accuracy > 0.7:
            modifiers.append("Sezgilerin genellikle isabetli. Kendi hislerine güvenebilirsin.")
        elif self.intuition_accuracy < 0.4:
            modifiers.append("Sezgilerinin güvenilirliği düşük. Analitik düşünmeye daha çok güven.")

        return modifiers

    def get_stats(self):
        """Sezgi modülü istatistikleri."""
        return {
            "intuition_accuracy": round(self.intuition_accuracy, 3),
            "total_intuitions": self.total_intuitions,
            "correct_intuitions": self.correct_intuitions,
            "pattern_library_size": len(self.pattern_library),
            "recent_gut_feelings": len(self.gut_feelings_log)
        }
