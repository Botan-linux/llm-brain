import json
import os
from datetime import datetime
from collections import Counter
import re


class LearningEngine:
    """
    Öğrenme Motoru (Learning Engine)
    
    Gerçek beynin öğrenme mekanizmaları:
    - Klasik koşullanma: Aynı uyaran → aynı tepki kalıbı (pattern öğrenme)
    - Operant koşullanma: Olumlu sonuç → davranış tekrarı, olumsuz → kaçınma
    - Gözlemsel öğrenme: Başkalarının deneyimlerinden öğrenme
    - Desen tanıma: Tekrar eden kalıpları algılama
    - Genellemleme: Benzer durumlara öğrenmeyi aktarma
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "learning.json"
            )
        self.storage_path = storage_path
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.stimulus_response_patterns = data.get("stimulus_response_patterns", {})
                    self.behavior_rules = data.get("behavior_rules", [])
                    self.learned_concepts = data.get("learned_concepts", {})
                    self.topic_preferences = data.get("topic_preferences", {})
                    self.conversation_style = data.get("conversation_style", {})
                    self.total_lessons = data.get("total_lessons", 0)
                    self.reinforcement_history = data.get("reinforcement_history", [])
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.stimulus_response_patterns = {}
        self.behavior_rules = []
        self.learned_concepts = {}
        self.topic_preferences = {}
        self.conversation_style = {
            "avg_response_length": 100,
            "formality": 0.5,
            "verbosity": 0.5
        }
        self.total_lessons = 0
        self.reinforcement_history = []

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "stimulus_response_patterns": self.stimulus_response_patterns,
                "behavior_rules": self.behavior_rules[-50:],
                "learned_concepts": self.learned_concepts,
                "topic_preferences": self.topic_preferences,
                "conversation_style": self.conversation_style,
                "total_lessons": self.total_lessons,
                "reinforcement_history": self.reinforcement_history[-50:]
            }, f, indent=4, ensure_ascii=False)

    def learn_from_exchange(self, stimulus, response, outcome_valence=0.0, context=""):
        """
        Bir etkileşimden öğren.
        
        Bu, beynin temel öğrenme döngüsüdür:
        1. Uyaran gelir
        2. Tepki verilir
        3. Sonuç değerlendirilir (olumlu/olumsuz)
        4. Gelecekteki davranış güncellenir
        
        Args:
            stimulus: Kullanıcı girdisi
            response: Beynin yanıtı
            outcome_valence: Sonuç değerlendirmesi (-1 olumsuz, 0 nötr, 1 olumlu)
            context: Bağlam
        """
        self.total_lessons += 1

        # 1. Stimulus-Response patern kaydet
        self._record_pattern(stimulus, response)

        # 2. Konu tercihini güncelle
        self._update_topic_preference(stimulus, outcome_valence)

        # 3. Konuşma stilini güncelle
        self._update_conversation_style(stimulus, response)

        # 4. Davranış kuralı çıkar
        self._extract_behavior_rule(stimulus, response, outcome_valence)

        # 5. Pekiştirme geçmişini kaydet
        self.reinforcement_history.append({
            "stimulus_preview": stimulus[:50],
            "outcome": outcome_valence,
            "context": context[:100],
            "timestamp": datetime.now().isoformat()
        })

        # Periyodik kaydet
        if self.total_lessons % 5 == 0:
            self._save()

    def _record_pattern(self, stimulus, response):
        """Uyaran-yanıt kalıplarını kaydet."""
        # Uyarandan anahtar kalıp çıkar
        key = self._extract_pattern_key(stimulus)

        if key not in self.stimulus_response_patterns:
            self.stimulus_response_patterns[key] = {
                "count": 0,
                "last_response_preview": "",
                "success_rate": 0.0,
                "avg_valence": 0.0
            }

        pattern = self.stimulus_response_patterns[key]
        pattern["count"] += 1
        pattern["last_response_preview"] = response[:100]

    def _extract_pattern_key(self, text):
        """Metinden kalıp anahtarı çıkar."""
        words = re.findall(r'\w+', text.lower(), re.UNICODE)
        # Stop words temizle
        stop_words = {"bir", "ve", "ile", "için", "ama", "fakat", "ancak", "veya", "bu", "şu", "o",
                      "the", "and", "or", "but", "this", "that", "is", "are", "was", "were", "a", "an"}
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        # İlk 3 kelimeyi anahtar yap
        return " ".join(filtered[:3]) if filtered else text[:30].lower()

    def _update_topic_preference(self, stimulus, valence):
        """Konu tercihlerini güncelle (operant koşullanma)."""
        # Basit konu tespiti
        topic_words = re.findall(r'\w+', stimulus.lower(), re.UNICODE)
        for word in topic_words:
            if len(word) > 4:  # Kısa kelimeleri atla
                if word not in self.topic_preferences:
                    self.topic_preferences[word] = {"mentions": 0, "positive": 0, "negative": 0}
                self.topic_preferences[word]["mentions"] += 1
                if valence > 0.2:
                    self.topic_preferences[word]["positive"] += 1
                elif valence < -0.2:
                    self.topic_preferences[word]["negative"] += 1

    def _update_conversation_style(self, stimulus, response):
        """Konuşma stilini öğren."""
        # Yanıt uzunluğu
        resp_len = len(response)
        current_avg = self.conversation_style["avg_response_length"]
        self.conversation_style["avg_response_length"] = round(
            current_avg * 0.9 + resp_len * 0.1, 1
        )

        # Formalite (kullanıcı formal mı, informal mı?)
        if any(w in stimulus.lower() for w in ["sen", "seni", "lan", "hayır", "kapat", "siktir"]):
            self.conversation_style["formality"] = max(0.1, self.conversation_style["formality"] - 0.05)
        elif any(w in stimulus.lower() for w in ["lütfen", "teşekkür", "rica", "merhaba"]):
            self.conversation_style["formality"] = min(1.0, self.conversation_style["formality"] + 0.03)

    def _extract_behavior_rule(self, stimulus, response, valence):
        """
        Basit davranış kuralları çıkar.
        
        Örnek: "Selam" → olumlu sonuç → "Selam verildiğinde selamla" kuralı
        """
        # Sadece güçlü valence'li deneyimlerden kural çıkar
        if abs(valence) < 0.5:
            return

        key = self._extract_pattern_key(stimulus)
        action = "pozitif_yanıt" if valence > 0 else "kaçın"

        # Aynı kural zaten var mı?
        for rule in self.behavior_rules:
            if rule["pattern"] == key:
                rule["count"] += 1
                rule["last_valence"] = valence
                return

        # Yeni kural
        if len(self.behavior_rules) < 100:  # Max 100 kural
            self.behavior_rules.append({
                "pattern": key,
                "action": action,
                "valence": valence,
                "count": 1,
                "last_valence": valence,
                "created_at": datetime.now().isoformat()
            })

    def get_behavioral_guidance(self, stimulus):
        """
        Öğrenilen kurallara göre davranış rehberliği ver.
        
        Beyin benzer bir uyaran gördüğünde geçmiş öğrenmelerine
        göre nasıl davranması gerektiğini bilir.
        
        Returns:
            dict or None: Davranış rehberliği
        """
        key = self._extract_pattern_key(stimulus)
        guidance = []

        # Tam eşleşme
        for rule in self.behavior_rules:
            if rule["pattern"] == key:
                guidance.append({
                    "type": "exact_match",
                    "action": rule["action"],
                    "confidence": min(1.0, rule["count"] * 0.2 + abs(rule["valence"]) * 0.3),
                    "rule_count": rule["count"]
                })

        # Kısmi eşleşme
        key_words = set(key.split())
        for rule in self.behavior_rules:
            rule_words = set(rule["pattern"].split())
            overlap = len(key_words & rule_words)
            if overlap > 0 and rule["pattern"] != key:
                guidance.append({
                    "type": "partial_match",
                    "action": rule["action"],
                    "confidence": min(0.7, overlap * 0.15 + abs(rule["valence"]) * 0.2),
                    "matched_pattern": rule["pattern"]
                })

        if not guidance:
            return None

        # En yüksek güvenilirlikli rehberliği seç
        guidance.sort(key=lambda x: x["confidence"], reverse=True)
        return guidance[0]

    def get_learned_style_hints(self):
        """Öğrenilen konuşma stili ipuçları döndürür."""
        hints = []

        style = self.conversation_style
        if style["formality"] > 0.7:
            hints.append("Kullanıcı formale yakın konuşuyor, saygılı ol.")
        elif style["formality"] < 0.3:
            hints.append("Kullanıcı rahat konuşuyor, samimi ol.")

        if style["avg_response_length"] < 80:
            hints.append("Kısa ve öz yanıtlar tercih ediliyor.")
        elif style["avg_response_length"] > 200:
            hints.append("Detaylı ve uzun yanıtlar tercih ediliyor.")

        # Popüler konular
        if self.topic_preferences:
            top_topics = sorted(
                self.topic_preferences.items(),
                key=lambda x: x[1]["mentions"],
                reverse=True
            )[:3]
            topic_names = [t[0] for t in top_topics if t[1]["positive"] > t[1]["negative"]]
            if topic_names:
                hints.append(f"Kullanıcının ilgilendiği konular: {', '.join(topic_names)}")

        return hints

    def reinforce(self, pattern_key, valence):
        """Manuel pekiştirme — dışarıdan gelen geri bildirim."""
        for rule in self.behavior_rules:
            if rule["pattern"] == pattern_key:
                rule["last_valence"] = valence
                rule["count"] += 1
                break
        self.reinforcement_history.append({
            "type": "manual_reinforcement",
            "pattern": pattern_key,
            "valence": valence,
            "timestamp": datetime.now().isoformat()
        })
        self._save()

    def get_stats(self):
        return {
            "total_lessons": self.total_lessons,
            "known_patterns": len(self.stimulus_response_patterns),
            "behavior_rules": len(self.behavior_rules),
            "learned_concepts": len(self.learned_concepts),
            "tracked_topics": len(self.topic_preferences),
            "conversation_style": self.conversation_style
        }


if __name__ == "__main__":
    le = LearningEngine()

    le.learn_from_exchange("Merhaba!", "Merhaba! Size nasıl yardımcı olabilirim?", 0.8)
    le.learn_from_exchange("Python hakkında bilgi ver", "Python yüksek seviyeli bir dildir...", 0.6)
    le.learn_from_exchange("Python hakkında bilgi ver", "Python geniş bir topluluğa sahiptir...", 0.7)
    le.learn_from_exchange("Çok kötü bir cevaptı", "Özür dilerim, daha iyi açıklamaya çalışayım.", -0.8)

    print("Guidance:", le.get_behavioral_guidance("Python hakkında bilgi ver"))
    print("Style hints:", le.get_learned_style_hints())
    print("Stats:", le.get_stats())
