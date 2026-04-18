class LimbicSystem:
    def __init__(self):
        # Yetişkin bir bireyin genişletilmiş duygusal spektrumu
        self.emotional_states = {
            "analytical": 0.6,   # Mantıklı düşünme kapasitesi
            "stress": 0.05,      # Stres seviyesi
            "interest": 0.5,     # Konuya duyulan ilgi
            "fatigue": 0.0,      # Yorgunluk
            "happiness": 0.0,    # Mutluluk (yeni)
            "empathy": 0.3,      # Empati (yeni)
        }

        # Başlangıç ruh hali
        self.current_mood = "balanced" # Dengeli
        self.development_stage = "adult" # Yetişkin
        self._mood_history = []  # Ruh hali geçmişi
        self._mood_momentum = {}  # Duygu ivmesi (hızlanma/yavaşlama)
        self._emotion_velocity = {}  # Duygu değişim hızı
        self._last_emotional_states = {}

    def update_state(self, stimulus_tone, energy_level):
        """Duygusal durumu günceller — insan beyni gibi hızlı tepki verir."""

        # --- Enerji analizi ---
        if energy_level < 15:
            self.emotional_states["fatigue"] += 0.25
            self.emotional_states["analytical"] -= 0.1
            self.emotional_states["interest"] -= 0.1
        elif energy_level < 35:
            self.emotional_states["fatigue"] += 0.08
            self.emotional_states["interest"] -= 0.03

        # --- Uyaran analizi (hızlı duygu geçişi) ---
        if stimulus_tone in ("negatif", "negative"):
            self.emotional_states["stress"] += 0.3     # Daha agresif stres artışı
            self.emotional_states["happiness"] -= 0.2  # Mutluluk düşer
            self.emotional_states["analytical"] += 0.05 # Stres altında hafif odaklanma
            self.emotional_states["empathy"] += 0.05    # Empati tetiklenir
        elif stimulus_tone in ("pozitif", "positive"):
            self.emotional_states["happiness"] += 0.35  # Hızlı mutluluk artışı
            self.emotional_states["stress"] -= 0.15     # Stres azalır
            self.emotional_states["interest"] += 0.15   # İlgi artar
            self.emotional_states["empathy"] += 0.05
        elif stimulus_tone == "bilişsel":
            self.emotional_states["analytical"] += 0.2  # Bilişsel düşünce güçlenir
            self.emotional_states["interest"] += 0.2    # Merak artar
        else:
            # Nötr uyaran — hafif ilgi artışı
            self.emotional_states["interest"] += 0.08
            self.emotional_states["stress"] -= 0.03

        # --- Doğal gerileme (duygular zamanla sakinleşir) ---
        # Momentum: Ani değişimler yavaşlatılır (insanlarda duygu geçişleri kademeli)
        for state in self.emotional_states:
            velocity = self._emotion_velocity.get(state, 0)
            # Büyük ani değişimler biraz frenlenir (inertia)
            if abs(velocity) > 0.15:
                damping = 0.85 if velocity > 0 else 1.1
                self.emotional_states[state] *= damping

        # Doğal gerileme (decay)
        decay_rates = {
            "stress": 0.90,
            "happiness": 0.88,
            "fatigue": 0.97,
            "interest": 0.93,
            "analytical": 0.95,
            "empathy": 0.96
        }
        for state, rate in decay_rates.items():
            self.emotional_states[state] *= rate

        # Değerleri sınırla
        for state in self.emotional_states:
            self.emotional_states[state] = max(0, min(1, self.emotional_states[state]))

        self._determine_mood()

        self._update_emotion_momentum()

        # Ruh hali geçmişini kaydet
        self._mood_history.append(self.current_mood)
        if len(self._mood_history) > 20:
            self._mood_history = self._mood_history[-20:]

        return self.current_mood

    def _determine_mood(self):
        """Duygu durumlarından ruh halini belirle — daha hassas eşikler."""
        states = self.emotional_states

        # Öncelik sırası: yorgunluk > stres > mutluluk > merak > ilgi > analitik > dengeli
        if states["fatigue"] > 0.5:
            self.current_mood = "exhausted"
        elif states["stress"] > 0.4:
            self.current_mood = "defensive"
        elif states["happiness"] > 0.4:
            self.current_mood = "happy"  # Yeni ruh hali
        elif states["analytical"] > 0.5 and states["interest"] > 0.5:
            self.current_mood = "curious"
        elif states["interest"] > 0.55:
            self.current_mood = "engaged"
        elif states["analytical"] > 0.5:
            self.current_mood = "analytical"
        else:
            self.current_mood = "balanced"

    def _update_emotion_momentum(self):
        """Duygu ivmesini takip et — ani değişimler daha yavaş olmalı (insan gibi)."""
        for state_name in self.emotional_states:
            old_val = self._last_emotional_states.get(state_name, self.emotional_states[state_name])
            velocity = self.emotional_states[state_name] - old_val
            self._emotion_velocity[state_name] = velocity
            self._last_emotional_states[state_name] = self.emotional_states[state_name]

    def get_system_prompt_modifier(self):
        modifiers = {
            "analytical": "Sen son derece mantıklı, analitik düşünen ve profesyonel bir zihinsin. Yanıtların net ve bilgi odaklı olsun.",
            "defensive": "Şu an stres altındasın, daha kısa ve temkinli yanıtlar ver.",
            "exhausted": "Enerjin düşük, sadece en gerekli bilgileri ver.",
            "balanced": "Dengeli ve rasyonel bir birey gibi konuş. Yardımcı ve yapıcı ol.",
            "curious": "Derin bir merakla sorgula ve araştır. Yanıtların keşfedici olsun.",
            "engaged": "Konuya tamamen odaklanmışsın. Detaylı ve tutkulu cevaplar ver.",
            "happy": "Şu an mutlusun. Bu enerjiyi yanıtlarına yansıt — sıcak, yapıcı ve heyecanlı ol.",
        }
        return modifiers.get(self.current_mood, "Sen profesyonel bir yapay zekasın.")

    def get_model_params(self):
        """Ruh haline göre modelin çalışma parametrelerini belirler."""
        params = {
            "temperature": 0.5,
            "max_tokens": 1024
        }

        if self.current_mood == "analytical":
            params["temperature"] = 0.2
            params["max_tokens"] = 1536
        elif self.current_mood == "defensive":
            params["temperature"] = 0.4
            params["max_tokens"] = 150
        elif self.current_mood == "exhausted":
            params["temperature"] = 0.3
            params["max_tokens"] = 100
        elif self.current_mood == "curious":
            params["temperature"] = 0.7
            params["max_tokens"] = 2048
        elif self.current_mood == "engaged":
            params["temperature"] = 0.6
            params["max_tokens"] = 1536
        elif self.current_mood == "happy":
            params["temperature"] = 0.65
            params["max_tokens"] = 1536

        return params
