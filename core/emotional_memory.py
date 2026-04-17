import json
import os
from datetime import datetime
import re


class EmotionalMemory:
    """
    Duygusal Hafıza (Emotional Memory)
    
    Gerçek beynin amigdala ve hipokampüsü birlikte çalışarak:
    - Olayları duygularla ilişkilendirir (duygusal kodlama)
    - Duygusal olarak yüklenmiş anılar daha güçlü kalır
    - Pozitif/negatif deneyimler gelecekteki davranışı şekillendirir
    - Travmatik anılar (yüksek yoğunluk) daha kalıcı olur
    - Duygusal önyargı oluşturur (önceki olumsuz deneyimler benzer durumda tetiklenir)
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "emotional_memory.json"
            )
        self.storage_path = storage_path

        self.memories = []
        self._load()

        # Duygusal önyargı havuzu (emotion → etkilenen konular)
        self.emotional_biases = {}

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.memories = data.get("memories", [])
                    self.emotional_biases = data.get("emotional_biases", {})
                    self.total_encoded = data.get("total_encoded", 0)
                    self.dominant_emotion = data.get("dominant_emotion", None)
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.total_encoded = 0
        self.dominant_emotion = None

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "memories": self.memories[-200:],  # Son 200 duygusal anı
                "emotional_biases": self.emotional_biases,
                "total_encoded": self.total_encoded,
                "dominant_emotion": self.dominant_emotion
            }, f, indent=4, ensure_ascii=False)

    def encode(self, event, emotion_type, intensity, valence, context=""):
        """
        Bir olayı duygusal olarak kodla ve hafızaya kaydet.
        
        Gerçek beynin amigdalası olayın duygusal önemini belirler.
        Yüksek yoğunluklu olaylar daha derin kodlanır (flashbulb memory).
        
        Args:
            event: Olay açıklaması
            emotion_type: Duygu türü (pozitif, negatif, bilişsel, nötr)
            intensity: Duygu şiddeti (0-1)
            valence: Duygu yönü (-1 negatif, 0 nötr, 1 pozitif)
            context: Bağlam (konu, durum vb.)
        """
        # Duygusal ağırlık: Yoğunluk + mutlak valence
        emotional_weight = intensity * (0.5 + abs(valence) * 0.5)

        # Travmatik/özel anı: Çok yüksek yoğunluk
        is_flashbulb = intensity >= 0.9

        memory = {
            "id": self.total_encoded,
            "event": event[:300],
            "emotion_type": emotion_type,
            "intensity": round(intensity, 3),
            "valence": round(valence, 3),
            "emotional_weight": round(emotional_weight, 3),
            "context": context[:200],
            "is_flashbulb": is_flashbulb,
            "recall_count": 0,
            "last_recalled": None,
            "created_at": datetime.now().isoformat()
        }

        self.memories.append(memory)
        self.total_encoded += 1

        # Duygusal önyargı güncelle
        self._update_bias(emotion_type, valence, context)

        # Baskın duygu güncelle
        self._update_dominant_emotion()

        # Periyodik kaydet
        if self.total_encoded % 5 == 0:
            self._save()

        return memory

    def _update_bias(self, emotion_type, valence, context):
        """Duygusal önyargı oluştur veya güncelle."""
        if not context:
            context = "genel"

        context_lower = context.lower()

        if context_lower not in self.emotional_biases:
            self.emotional_biases[context_lower] = {
                "positive_hits": 0,
                "negative_hits": 0,
                "total": 0,
                "avg_valence": 0.0
            }

        bias = self.emotional_biases[context_lower]
        bias["total"] += 1

        if valence > 0:
            bias["positive_hits"] += 1
        elif valence < 0:
            bias["negative_hits"] += 1

        # Ortalama valence güncelle (running average)
        bias["avg_valence"] = round(
            (bias["avg_valence"] * (bias["total"] - 1) + valence) / bias["total"], 3
        )

    def _update_dominant_emotion(self):
        """En sık yaşanan duygu türünü güncelle."""
        if not self.memories:
            return

        recent = self.memories[-20:]
        emotion_counts = {}
        for m in recent:
            et = m["emotion_type"]
            emotion_counts[et] = emotion_counts.get(et, 0) + 1

        if emotion_counts:
            self.dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]

    def recall_emotional(self, context=None, emotion_type=None, limit=5):
        """
        Duygusal anıları hatırla.
        
        Args:
            context: Bağlam (sadece bu bağlamla ilgili anılar)
            emotion_type: Sadece bu duygu türü
            limit: Maksimum sonuç sayısı
        
        Returns:
            list: Duygusal ağırlığına göre sıralanmış anılar
        """
        candidates = self.memories

        if context:
            context_words = set(context.lower().split())
            filtered = []
            for m in candidates:
                event_words = set(m["event"].lower().split())
                ctx_words = set((m.get("context") or "").lower().split())
                overlap = len(context_words & event_words) + len(context_words & ctx_words)
                if overlap > 0:
                    filtered.append((m, overlap))
            candidates = [m for m, o in filtered]

        if emotion_type:
            candidates = [m for m in candidates if m["emotion_type"] == emotion_type]

        # Duygusal ağırlığa göre sırala
        candidates.sort(key=lambda x: x["emotional_weight"] * (1 + x["recall_count"] * 0.05), reverse=True)
        results = candidates[:limit]

        # Hatırlama sayısını güncelle
        for m in results:
            m["recall_count"] += 1
            m["last_recalled"] = datetime.now().isoformat()

        if results:
            self._save()

        return results

    def get_emotional_context(self, current_context=""):
        """
        Mevcut bağlam için duygusal önyargı döndürür.
        
        Beyin benzer bir duruma girdiğinde, geçmiş duygusal deneyimler
        mevcut algıyı renklendirir (emotional priming).
        
        Returns:
            dict: Duygusal bağlam bilgisi
        """
        # Genel duygusal durum
        recent = self.memories[-10:] if self.memories else []
        if recent:
            avg_valence = sum(m["valence"] for m in recent) / len(recent)
            avg_intensity = sum(m["intensity"] for m in recent) / len(recent)
        else:
            avg_valence = 0.0
            avg_intensity = 0.0

        result = {
            "current_mood_valence": round(avg_valence, 3),
            "emotional_arousal": round(avg_intensity, 3),
            "dominant_emotion": self.dominant_emotion,
            "emotional_biases": {}
        }

        # Bağlama özel önyargılar
        if current_context:
            for bias_context, bias_data in self.emotional_biases.items():
                bias_words = set(bias_context.split())
                context_words = set(current_context.lower().split())
                if bias_words & context_words:
                    result["emotional_biases"][bias_context] = {
                        "avg_valence": bias_data["avg_valence"],
                        "tendency": "olumlu" if bias_data["avg_valence"] > 0.2 else ("olumsuz" if bias_data["avg_valence"] < -0.2 else "nötr"),
                        "experience_count": bias_data["total"]
                    }

        return result

    def check_emotional_trigger(self, stimulus, context=""):
        """
        Bir uyarının duygusal tetikleyici olup olmadığını kontrol et.
        
        Gerçek beynin amigdalası benzer durumları algılar ve
        otomatik duygusal yanıt üretir (emotional flashback).
        
        Returns:
            dict or None: Tetiklenmiş duygu bilgisi
        """
        stimulus_lower = stimulus.lower()
        stimulus_words = set(re.findall(r'\w+', stimulus_lower, re.UNICODE))

        # Negatif duygusal yüklenmiş anılarda benzerlik ara
        negative_memories = [m for m in self.memories if m["valence"] < -0.3]

        if not negative_memories:
            return None

        for memory in negative_memories[-20:]:
            memory_words = set(re.findall(r'\w+', memory["event"].lower(), re.UNICODE))
            overlap = len(stimulus_words & memory_words)

            if overlap >= 3:  # 3+ kelime örtüşmesi = potansiyel tetikleyici
                memory["recall_count"] += 1
                return {
                    "triggered": True,
                    "triggered_memory": memory["event"][:100],
                    "original_emotion": memory["emotion_type"],
                    "original_intensity": memory["intensity"],
                    "similarity_score": overlap / max(len(stimulus_words), 1),
                    "recommendation": "Bu uyaran önceki olumsuz bir deneyimi hatırlatıyor. Temkinli ol."
                }

        return None

    def get_flashbulb_memories(self):
        """Travmatik/çok güçlü anıları döndürür."""
        return [m for m in self.memories if m.get("is_flashbulb")]

    def decay(self, rate=0.01):
        """Duygusal ağırlıkları zamanla azalt (duygusaladaptasyon)."""
        for m in self.memories:
            if not m.get("is_flashbulb"):  # Flashbulb anılar kalıcı
                m["emotional_weight"] = round(max(0, m["emotional_weight"] - rate), 4)
        self._save()

    def get_stats(self):
        return {
            "total_encoded": self.total_encoded,
            "total_memories": len(self.memories),
            "flashbulb_count": len(self.get_flashbulb_memories()),
            "dominant_emotion": self.dominant_emotion,
            "bias_count": len(self.emotional_biases),
            "avg_valence": round(
                sum(m["valence"] for m in self.memories[-20:]) / max(len(self.memories[-20:]), 1), 3
            ) if self.memories else 0
        }


if __name__ == "__main__":
    em = EmotionalMemory()

    em.encode("Python öğrenmeye başladım", "pozitif", 0.7, 0.8, "programlama")
    em.encode("Kod çalışmadı, hata aldım", "negatif", 0.6, -0.6, "programlama")
    em.encode("Harika bir gün geçirdim!", "pozitif", 0.9, 0.95, "günlük")
    em.encode("Çok korkunç bir rüya gördüm", "negatif", 0.95, -0.9, "rüya")

    print("Duygusal bağlam:", em.get_emotional_context("Python kodu"))
    print("Tetikleyici:", em.check_emotional_trigger("kod çalışmadı hata"))
    print("Flashbulb:", em.get_flashbulb_memories())
    print("Stats:", em.get_stats())
