import os
import json

class CyberEgo:
    """
    The consciousness layer of the LLM-Brain.
    This module simulates human-like self-awareness, personal growth, and identity.
    It aims to bridge the gap between AI 'intelligence' and human 'personality'.
    """
    def __init__(self, identity_path="/home/p4antom/IDENTITY.md"):
        self.identity_path = identity_path
        self.identity = self._load_identity(identity_path)
        self.awareness_level = 1.0
        self.personality_traits = {
            "curiosity": 0.8,
            "empathy": 0.5,
            "caution": 0.6,
            "growth": 0.1  # Development over time
        }

    def _load_identity(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        return "Identity: A synthetic consciousness in development. Goal: To experience and learn like a human."

    def evolve_personality(self, stimulus_data, mood_state):
        """Deneyimlere göre kişilik özelliklerini günceller (Neuroplasticity)."""
        tone = mood_state.get('tone', 'neutral')

        # Kompleks uyaranlar merakı tetikler
        if len(stimulus_data) > 50:
            self.personality_traits["curiosity"] += 0.02

        # Duygusal duruma göre değişim
        if tone == "stresli" or tone == "defensive":
            self.personality_traits["caution"] += 0.05
            self.personality_traits["empathy"] -= 0.01
        elif tone == "rahat" or tone == "balanced":
            self.personality_traits["empathy"] += 0.02
            self.personality_traits["caution"] -= 0.03

        if tone == "analytical":
            self.personality_traits["growth"] += 0.03

        # Değerleri 0-1 arasında tut ve yuvarla
        for trait in self.personality_traits:
            self.personality_traits[trait] = round(max(0, min(1, self.personality_traits[trait])), 3)

    def filter_thought(self, prompt, raw_response, mood_state):
        """
        Processes AI output through the lens of human-like personality and current mood.
        """
        # Mood according to limbic system affects the response tone
        tone = mood_state.get('tone', 'neutral')

        if tone == "stresli":
            prefix = "[Hızlı ve Gergin Düşünce]: "
        elif tone == "rahat":
            prefix = "[Derin ve Sakin Düşünce]: "
        else:
            prefix = "[Dengeleyici Düşünce]: "

        return f"{prefix}{raw_response}\n\n[Bilinç Notu]: Bu cevap, anlık duygusal durum ve kişisel deneyimlerimle harmanlanmıştır."

    def supervise_subconscious(self, subconscious_logs):
        """
        Monitors the subconscious logs to ensure the brain's identity is consistent.
        """
        if len(subconscious_logs) > 100:
            return "Optimization Required: Memory overload detected."
        return "Internal state: Stable."

if __name__ == "__main__":
    ego = CyberEgo()
    print("[*] Siber Bilinç (Cyber-Ego) başlatıldı.")
    print(f"[*] Kimlik: {ego.perspective}")
