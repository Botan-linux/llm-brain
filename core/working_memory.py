import json
import os
from datetime import datetime
from collections import deque


class WorkingMemory:
    """
    Çalışma Hafızası (Working Memory)
    
    Gerçek beynin çalışma hafızası:
    - George Miller'ın "7±2" kuralı: İnsan beyni aynı anda 5-9 bilgi tutabilir
    - Sohbet bağlamını takip eder (konuşma ne hakkında, nerede kaldık)
    - Geçici bilgi işler (hesaplama, karşılaştırma)
    - Dikkat dağılırsa bilgi kaybolur
    
    Bu modül:
    - Sohbet geçmişini yönetir
    - Konu değişikliklerini algılar
    - Önemli bağlam bilgilerini tutar
    - Referans çözümleme yapır ("o", "bunu", "şimdi" vb.)
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "working_memory.json"
            )
        self.storage_path = storage_path

        # Miller'ın 7±2 kuralı
        self.capacity = 7
        self.max_capacity = 9

        # Sohbet geçmişi (ring buffer — kapasite dolduğunda eski mesajlar düşer)
        self.conversation = deque(maxlen=self.max_capacity)

        # Mevcut bağlam
        self.current_topic = None
        self.topic_history = []
        self.turn_count = 0

        # Aktif referanslar ("o", "bu", "şimdi" gibi zamirlerin_referansları)
        self.active_references = {}

        # Bekleyen sorular (kullanıcı soru sordu ama yanıt henüz verilmedi)
        self.pending_questions = []

        # Önceki durumu yükle
        self._load()

    def _load(self):
        """Önceki working memory durumunu yükle."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.current_topic = data.get("current_topic")
                    self.topic_history = data.get("topic_history", [])[-20:]
                    self.turn_count = data.get("turn_count", 0)
                    self.active_references = data.get("active_references", {})
                    self.total_sessions = data.get("total_sessions", 0)
                    self.total_turns = data.get("total_turns", 0)
                    # Konuşma geçmişi kalıcı değil, yeni oturumda sıfırlanır
            except (json.JSONDecodeError, IOError):
                self._reset_persistent()
        else:
            self._reset_persistent()

    def _reset_persistent(self):
        self.total_sessions = 1
        self.total_turns = 0
        self.current_topic = None
        self.topic_history = []
        self.turn_count = 0
        self.active_references = {}

    def _save(self):
        """Kalıcı verileri kaydet (sohbet geçmişi hariç)."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "current_topic": self.current_topic,
                "topic_history": self.topic_history[-20:],
                "turn_count": self.turn_count,
                "active_references": self.active_references,
                "total_sessions": self.total_sessions,
                "total_turns": self.total_turns
            }, f, indent=4, ensure_ascii=False)

    def add_exchange(self, user_input, brain_response, detected_topic=None):
        """
        Bir konuşma dönüşünü (user → brain) hafızaya ekle.
        
        Gerçek beynin çalışma hafızasında:
        1. Yeni bilgi eski bilgiyi itebilir (retroactive interference)
        2. Önemli bilgi daha uzun kalır
        3. Bağlam (context) korunur
        """
        self.turn_count += 1
        self.total_turns += 1

        exchange = {
            "turn": self.turn_count,
            "user": user_input,
            "brain": brain_response,
            "topic": detected_topic or self.current_topic,
            "timestamp": datetime.now().isoformat()
        }

        self.conversation.append(exchange)

        # Referans güncelle
        self._update_references(user_input, brain_response)

        # Konu değişikliğini kontrol et
        if detected_topic and detected_topic != self.current_topic:
            self._change_topic(detected_topic)

        # Bekleyen soruları güncelle
        self._update_pending_questions(user_input, brain_response)

        # Kapasite kontrolü
        if len(self.conversation) >= self.capacity:
            # Dikkat dağılıyor — bazı referanslar kaybolabilir
            self._prune_references()

        # Periyodik kaydet
        if self.turn_count % 3 == 0:
            self._save()

    def _update_references(self, user_input, brain_response):
        """Aktif referansları güncelle."""
        # Kullanıcının bahsettiği önemli varlıkları çıkar
        entities = self._extract_entities(user_input)
        for entity in entities:
            self.active_references[entity.lower()] = {
                "mention": entity,
                "context": user_input[:100],
                "turn": self.turn_count
            }

        # Beynin bahsettiği önemli kavramları da ekle
        brain_entities = self._extract_entities(brain_response)
        for entity in brain_entities[:5]:  # Beynin referansları daha az ağırlıklı
            key = entity.lower()
            if key not in self.active_references:
                self.active_references[key] = {
                    "mention": entity,
                    "context": brain_response[:100],
                    "turn": self.turn_count
                }

        # Max 15 referans tut
        if len(self.active_references) > 15:
            oldest = sorted(self.active_references.items(), key=lambda x: x[1]["turn"])
            for key, _ in oldest[:len(self.active_references) - 15]:
                del self.active_references[key]

    def _extract_entities(self, text):
        """Basit varlık çıkarma (isim tamlamaları, tırnak içindeki ifadeler, büyük harfli kelimeler)."""
        entities = []
        # Tırnak içindeki ifadeler
        import re
        quoted = re.findall(r'["\']([^"\']+)["\']', text)
        entities.extend(quoted)

        # Büyük harfle başlayan kelimeler (Türkçe ve İngilizce)
        words = text.split()
        for word in words:
            cleaned = re.sub(r'[^\w]', '', word)
            if cleaned and cleaned[0].isupper() and len(cleaned) > 2 and cleaned.lower() not in [
                "sen", "ben", "bu", "şu", "o", "ne", "nasıl", "neden", "merhaba",
                "the", "this", "that", "what", "how", "why", "hello", "bir",
                "ve", "ile", "için", "ama", "fakat", "ancak", "veya", "and", "but", "or"
            ]:
                entities.append(cleaned)

        return list(set(entities))[:10]

    def _change_topic(self, new_topic):
        """Konu değişikliğini kaydet."""
        if self.current_topic:
            self.topic_history.append({
                "topic": self.current_topic,
                "duration_turns": self.turn_count,
                "ended_at": datetime.now().isoformat()
            })
        self.current_topic = new_topic

    def _update_pending_questions(self, user_input, brain_response):
        """Bekleyen soruları takip et."""
        # Kullanıcı soru sordu mu?
        if "?" in user_input or user_input.lower().startswith(("ne ", "nasıl ", "neden ", "kim ", "hangi ", "kaç ")):
            self.pending_questions.append({
                "question": user_input,
                "answered": False,
                "turn": self.turn_count
            })

        # Beyin cevap verdi mi?
        if self.pending_questions:
            self.pending_questions[-1]["answered"] = True

        # Cevaplanmamış soruları temizle (3 turdan fazlaysa)
        self.pending_questions = [
            q for q in self.pending_questions
            if not q["answered"] or (self.turn_count - q["turn"]) < 3
        ]

    def _prune_references(self):
        """Kapasite aşımında eski referansları sil."""
        if len(self.active_references) > 10:
            oldest = sorted(self.active_references.items(), key=lambda x: x[1]["turn"])
            for key, _ in oldest[:3]:
                del self.active_references[key]

    def resolve_reference(self, text):
        """
        Zamir ve referansları çözümle.
        "O ne demek?" → "O"nun ne olduğunu bul.
        "Bunu açıklar mısın?" → "Bu"nun ne olduğunu bul.
        """
        text_lower = text.lower()
        pronouns = {
            "o": None, "bu": None, "şu": None,
            "bunu": None, "onu": None, "şunu": None,
            "onun": None, "bunlar": None, "onlar": None
        }

        resolved = {}
        for pronoun in pronouns:
            if pronoun in text_lower:
                # En son referansı bul
                if self.active_references:
                    latest_ref = sorted(
                        self.active_references.values(),
                        key=lambda x: x["turn"],
                        reverse=True
                    )
                    if latest_ref:
                        resolved[pronoun] = latest_ref[0]["mention"]
                        resolved[f"{pronoun}_context"] = latest_ref[0]["context"]

        return resolved if resolved else None

    def get_context_window(self, max_turns=None):
        """
        Sohbet bağlamı penceresi döndürür.
        LLM'in bağlam olarak kullanabileceği format.
        """
        if max_turns is None:
            max_turns = min(5, len(self.conversation))

        recent = list(self.conversation)[-max_turns:]
        context = ""
        for exchange in recent:
            context += f"Sen: {exchange['user']}\n"
            context += f"İLK: {exchange['brain'][:200]}\n\n"

        return context.strip()

    def get_full_context(self):
        """Tüm bağlam bilgilerini birleştir."""
        parts = []

        # Mevcut konu
        if self.current_topic:
            parts.append(f"[Mevcut Konu]: {self.current_topic}")

        # Konu geçmişi
        if self.topic_history:
            topics = [t["topic"] for t in self.topic_history[-5:]]
            parts.append(f"[Önceki Konular]: {', '.join(topics)}")

        # Referanslar
        if self.active_references:
            refs = [v["mention"] for v in self.active_references.values()]
            parts.append(f"[Aktif Referanslar]: {', '.join(refs[:10])}")

        # Sohbet bağlamı
        context_window = self.get_context_window(max_turns=3)
        if context_window:
            parts.append(f"[Son Sohbet]:\n{context_window}")

        return "\n".join(parts)

    def get_stats(self):
        """Working memory istatistikleri."""
        return {
            "turn_count": self.turn_count,
            "total_turns_ever": self.total_turns,
            "total_sessions": self.total_sessions,
            "current_topic": self.current_topic,
            "topics_discussed": len(self.topic_history) + (1 if self.current_topic else 0),
            "conversation_length": len(self.conversation),
            "active_references": len(self.active_references),
            "pending_questions": len([q for q in self.pending_questions if not q["answered"]]),
            "capacity_usage": f"{len(self.conversation)}/{self.max_capacity}"
        }


if __name__ == "__main__":
    wm = WorkingMemory()

    wm.add_exchange("Python öğrenmek istiyorum", "Python harika bir dil! Nereden başlamak istersin?", "programlama")
    wm.add_exchange("Fonksiyonlardan başlayalım", "Fonksiyonlar kodun yapı taşlarıdır.", "programlama")
    wm.add_exchange("Peki değişkenler?", "Değişkenler veri saklar.", "programlama")
    wm.add_exchange("Bu konuyu beğendim", "Sevindim! Başka ne öğrenmek istersin?", None)

    print("Context:", wm.get_full_context())
    print("Stats:", wm.get_stats())
    
    # Referans çözümleme testi
    resolved = wm.resolve_reference("Bunu daha detaylı anlat")
    print("Resolved:", resolved)
