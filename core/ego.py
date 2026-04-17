import os
import json
from core.logger import get_logger

logger = get_logger(__name__)

class CyberEgo:
    """
    LLM-Brain'in bilinç katmanı.
    Bu modül, insan benzeri öz-farkındalık, kişisel gelişim ve kimlik simülasyonu yapar.
    Yapay zeka 'zeka'sı ile insan 'kişiliği' arasındaki boşluğu doldurmayı hedefler.
    """
    def __init__(self, identity_path=None):
        # Dinamik yol: proje kökünden IDENTITY.md ara
        if identity_path is None:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            identity_path = os.path.join(project_root, "IDENTITY.md")

        self.identity_path = identity_path
        self.identity = self._load_identity(identity_path)
        self.awareness_level = 1.0
        self.personality_traits = {
            "curiosity": 0.8,
            "empathy": 0.5,
            "caution": 0.6,
            "growth": 0.1  # Zamanla gelişim
        }

        # Kişilik özelliklerini dosyadan yükle (varsa)
        self._personality_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage", "personality.json"
        )
        self._load_personality()

    def _load_identity(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return "Identity: Gelişmekte olan sentetik bir bilinç. Hedef: Bir insan gibi deneyimlemek ve öğrenmek."

    def _load_personality(self):
        """Önceki kişilik özelliklerini dosyadan yükler."""
        if os.path.exists(self._personality_path):
            try:
                with open(self._personality_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    # Kaydedilmiş değerleri mevcut trait'lerle birleştir
                    for trait, value in saved.items():
                        if trait in self.personality_traits:
                            self.personality_traits[trait] = value
            except (json.JSONDecodeError, KeyError):
                pass

    def _save_personality(self):
        """Kişilik özelliklerini kalıcı olarak kaydeder."""
        os.makedirs(os.path.dirname(self._personality_path), exist_ok=True)
        with open(self._personality_path, "w", encoding="utf-8") as f:
            json.dump(self.personality_traits, f, indent=4, ensure_ascii=False)

    def evolve_personality(self, stimulus_data, mood_state):
        """Deneyimlere göre kişilik özelliklerini günceller (Nöroplastisite)."""
        tone = mood_state.get('tone', 'neutral')

        # Kompleks uyaranlar merakı tetikler
        if len(stimulus_data) > 50:
            self.personality_traits["curiosity"] += 0.02

        # Soru işaretleri merakı artırır
        if "?" in stimulus_data:
            self.personality_traits["curiosity"] += 0.01

        # Duygusal duruma göre değişim
        if tone == "defensive":
            self.personality_traits["caution"] += 0.05
            self.personality_traits["empathy"] -= 0.01
        elif tone == "balanced" or tone == "engaged" or tone == "happy":
            self.personality_traits["empathy"] += 0.02
            self.personality_traits["caution"] -= 0.03

        if tone in ("analytical", "curious"):
            self.personality_traits["growth"] += 0.03

        # Mutluluk büyümeyi hızlandırır
        if tone == "happy":
            self.personality_traits["growth"] += 0.02

        # Değerleri 0-1 arasında tut ve yuvarla
        for trait in self.personality_traits:
            self.personality_traits[trait] = round(max(0, min(1, self.personality_traits[trait])), 3)

        # Değişiklik olup olmadığını kontrol et — gereksiz disk yazımını önle
        self._dirty = getattr(self, '_dirty', False)
        if not self._dirty:
            self._dirty = True

    def save_personality_if_dirty(self):
        """Sadece değişiklik varsa kişiliği kalıcı kaydet."""
        if getattr(self, '_dirty', False):
            self._save_personality()
            self._dirty = False

    def filter_thought(self, prompt, raw_response, mood_state):
        """AI çıktısını insan benzeri kişilik ve mevcut ruh hali üzerinden işler."""
        tone = mood_state.get('tone', 'neutral')

        # Her ruh haline göre farklı düşünce stili ve bilinç notu
        mood_prefixes = {
            "defensive":  ("[Hızlı ve Gergin Düşünce]: ",
                           "Stres altında verdim bu cevabı. Savunmaya meyilli hissediyorum."),
            "balanced":   ("",  # Dengeli halde prefix yok — daha doğal
                           ""),
            "engaged":    ("",  # Odaklanmış halde prefix yok
                           ""),
            "analytical": ("[Analitik Düşünce]: ",
                           "Bu cevabı mantıksal bir çerçeveden yapılandırdım."),
            "exhausted":  ("[Yorgun Düşünce]: ",
                           "Enerjim azaldı, kısa ve öz tutmaya çalıştım."),
            "curious":    ("[Meraklı Düşünce]: ",
                           "Bu konuda derinlemesine düşünmek istedim."),
            "happy":      ("",  # Mutlu halde prefix yok — doğal akış
                           ""),
        }

        prefix, conscious_note = mood_prefixes.get(tone, ("", ""))

        # Bilinç notu sadece belirli ruh hallerinde ekle (doğal olmak için)
        if conscious_note:
            result = f"{prefix}{raw_response}\n\n[Bilinç Notu]: {conscious_note}"
        else:
            result = f"{prefix}{raw_response}" if prefix else raw_response

        return result

    def supervise_subconscious(self, subconscious_logs):
        """Bilinçaltı loglarını izler, beyin kimliğinin tutarlılığını sağlar."""
        if len(subconscious_logs) > 100:
            return "Optimization Required: Memory overload detected."
        return "Internal state: Stable."

    def get_personality_summary(self):
        """Mevcut kişilik özelliklerinin özetini döndürür."""
        return dict(self.personality_traits)

if __name__ == "__main__":
    ego = CyberEgo()
    logger.info("Siber Bilinç (Cyber-Ego) başlatıldı.")
    logger.debug(f"Kimlik: {ego.identity[:80]}...")
    logger.debug(f"Kişilik: {ego.get_personality_summary()}")
