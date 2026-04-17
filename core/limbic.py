class LimbicSystem:
    def __init__(self):
        # Yetişkin bir bireyin temel duygusal spektrumu
        self.emotional_states = {
            "analytical": 0.7,   # Mantıklı düşünme kapasitesi
            "stress": 0.1,       # Stres seviyesi
            "interest": 0.5,     # Konuya duyulan ilgi
            "fatigue": 0.0       # Yorgunluk
        }

        # Başlangıç ruh hali
        self.current_mood = "balanced" # Dengeli
        self.development_stage = "adult" # Yetişkin

    def update_state(self, stimulus_tone, energy_level):
        """Yetişkin mantığıyla duygusal durumu günceller."""

        # Enerji analizi
        if energy_level < 20:
            self.emotional_states["fatigue"] += 0.3
            self.emotional_states["analytical"] -= 0.1
        elif energy_level < 50:
            self.emotional_states["fatigue"] += 0.1

        # Uyaran analizi
        if stimulus_tone in ("negatif", "negative"):
            self.emotional_states["stress"] += 0.2
            self.emotional_states["analytical"] += 0.1 # Stres altında odaklanma
        else:
            self.emotional_states["interest"] += 0.05
            self.emotional_states["stress"] -= 0.05

        # Değerleri sınırla
        for state in self.emotional_states:
            self.emotional_states[state] = max(0, min(1, self.emotional_states[state]))

        self._determine_mood()
        return self.current_mood

    def _determine_mood(self):
        states = self.emotional_states

        if states["fatigue"] > 0.6:
            self.current_mood = "exhausted"
        elif states["stress"] > 0.5:
            self.current_mood = "defensive"
        elif states["analytical"] > 0.6 and states["interest"] > 0.6:
            self.current_mood = "curious"
        elif states["analytical"] > 0.6:
            self.current_mood = "analytical"
        elif states["interest"] > 0.6:
            self.current_mood = "engaged"
        else:
            self.current_mood = "balanced"

    def get_system_prompt_modifier(self):
        modifiers = {
            "analytical": "Sen son derece mantıklı, analitik düşünen ve profesyonel bir zihinsin. Yanıtların net ve bilgi odaklı olsun.",
            "defensive": "Şu an stres altındasın, daha kısa ve temkinli yanıtlar ver.",
            "exhausted": "Enerjin düşük, sadece en gerekli bilgileri ver.",
            "balanced": "Dengeli ve rasyonel bir birey gibi konuş. Yardımcı ve yapıcı ol.",
            "curious": "Derin bir merakla sorgula ve araştır. Yanıtların keşfedici olsun.",
            "engaged": "Konuya tamamen odaklanmışsın. Detaylı ve tutkulu cevaplar ver."
        }
        return modifiers.get(self.current_mood, "Sen profesyonel bir yapay zekasın.")

    def get_model_params(self):
        """Ruh haline göre modelin çalışma parametrelerini belirler."""
        params = {
            "temperature": 0.5,
            "max_tokens": 1024
        }

        if self.current_mood == "analytical":
            params["temperature"] = 0.2 # Daha kesin ve tutarlı
            params["max_tokens"] = 1536  # Daha detaylı açıklama yapabilir
        elif self.current_mood == "defensive":
            params["temperature"] = 0.4
            params["max_tokens"] = 150   # Kısa ve öz keskin yanıtlar
        elif self.current_mood == "exhausted":
            params["temperature"] = 0.3
            params["max_tokens"] = 100   # Minimum enerji harcaması
        elif self.current_mood == "curious":
            params["temperature"] = 0.7  # Daha yaratıcı
            params["max_tokens"] = 2048
        elif self.current_mood == "engaged":
            params["temperature"] = 0.6
            params["max_tokens"] = 1536

        return params
