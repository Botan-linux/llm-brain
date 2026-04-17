import re
import os
import json
from datetime import datetime
from core.logger import get_logger

logger = get_logger(__name__)


class LanguageProcessor:
    """
    Dil İşleme Merkezi (Language Processor)
    
    Gerçek beynin Wernicke ve Broca alanları gibi çalışır:
    - Niyet analizi: Kullanıcı ne istiyor? (soru, emir, paylaşım, duygu)
    - Duygu analizi: Metnin duygusal tonu (pozitif, negatif, nötr, karmaşık)
    - Konu tespiti: Konuşma ne hakkında?
    - Karmaşıklık: Cümlenin karmaşıklık seviyesi
    - Aciliyet: Acil bir istek mi?
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "language_patterns.json"
            )
        self.storage_path = storage_path

        # Niyet kalıpları (Türkçe + İngilizce)
        self.intent_patterns = {
            "soru": {
                "patterns": [
                    r"\?$",
                    r"^(ne|nasıl|neden|kim|hangi|kaç|nerede|zaman|mi)\b",
                    r"(mı|mu|mü|mı)\?",
                    r"(nedir|nasıldır|kimdir|nerededir)\b",
                    r"(anlat|açıkla|söyle|explain|tell)\b",
                    r"^(what|how|why|who|which|where|when|is|are|do|does|can|could|would)\b",
                    r"(explain|tell|describe|clarify)\b"
                ],
                "weight": 0.9
            },
            "emir": {
                "patterns": [
                    r"^(yap|et|ol|ver|al|getir|göster|bul|oku|yaz|başlat|durdur|sil|kapat|aç|güncelle|kaydet)",
                    r"^(lütfen|please)\b",
                    r"!(?=[^.!?]*$)",  # Cümle sonunda ünlem
                    r"^(do|make|create|delete|update|start|stop|show|find|read|write|open|close|save|run)\b",
                    r"^(please)\b",
                ],
                "weight": 0.8
            },
            "paylaşım": {
                "patterns": [
                    r"^(ben|bence|gibi|gördüm|oldu|yaptım|düşünüyorum)\b",
                    r"(hissediyorum|anlatayım|söyleyeyim|biliyorsun|biliyorum)\b",
                    r"^(i think|i believe|i feel|in my opinion|it seems)\b",
                    r"(i guess|i suppose)\b"
                ],
                "weight": 0.6
            },
            "selamlama": {
                "patterns": [
                    r"^(merhaba|selam|hey|günaydın|iyi akşamlar|nasılsın|ne haber)",
                    r"^(hello|hi|hey|good morning|good evening|how are you|what's up)\b",
                ],
                "weight": 0.3
            },
            "vedalaşma": {
                "patterns": [
                    r"^(hoşça kal|görüşürüz|bye|güle güle|kendine iyi bak)",
                    r"^(goodbye|bye|see you|farewell|take care)\b",
                ],
                "weight": 0.3
            },
            "duygu_ifadesi": {
                "patterns": [
                    r"^(çok|çoktan|harika|mükemmel|berbat|korkunç|inanılmaz|süper|güzel|kötü)",
                    r"(seviyorum|rahatsızlanıyorum|korkuyorum|endişeliyim|mutluyum|üzgünüm|sinirliyim|heyecanlıyım)\b",
                    r"^(great|awesome|amazing|terrible|horrible|incredible|wonderful|beautiful|ugly)\b",
                    r"(i love|i hate|i'm scared|worried|happy|sad|angry|excited)\b"
                ],
                "weight": 0.7
            },
            "öğrenme_isteği": {
                "patterns": [
                    r"(öğrenmek|anlamak|bilmek|kavramak|öğret|anlat)\b",
                    r"(nedir|nasıl çalışır|nasıl yapılır|ne demek)\b",
                    r"(learn|understand|teach|explain|know)\b"
                ],
                "weight": 0.85
            }
        }

        # Duygu kelime listeleri (Türkçe + İngilizce)
        self.emotion_lexicon = {
            "pozitif": [
                "sevgi", "mutluluk", "güzellik", "harika", "mükemmel", "süper", "güzel",
                "iyi", "teşekkür", "bravo", "bravo", "eğlenceli", "neşe", "coşku",
                "başarı", "huzur", "keyif", "heyecan", "ilgi", "merak", "umut",
                "gurur", "minnettar", "hoş", "tatlı", " şirin", "akıllı", "zeki",
                "mutlu", "mutluluk",
                "love", "happiness", "beauty", "amazing", "wonderful", "great", "awesome",
                "good", "thanks", "fun", "joy", "excitement", "success", "peace",
                "pleasure", "happy"
            ],
            "negatif": [
                "korku", "öfke", "üzüntü", "hayal kırıklığı", "kötü", "berbat", "feci",
                "sinir", "stres", "endişe", "acı", "sancı", "yorgunluk", "sıkıntı",
                "hata", "sorun", "problem", "başarısızlık", "yetersizlik", "kafa karışıklığı",
                "anlaşılamaz", "sinir bozucu", "rahatsız", "korkunç", "lanet", "bulaş",
                "fear", "anger", "sadness", "bad", "terrible", "awful", "stress", "anxiety",
                "pain", "tired", "problem", "issue", "failure", "frustration",
                "confusion", "annoying", "horrible"
            ],
            "bilişsel": [
                "düşünmek", "analiz", "mantık", "neden", "sonuç", "araştır", "incele",
                "kıyasla", "değerlendir", "kanıt", "veri", "istatistik", "teori",
                "hipotez", "deney", "mantıksal", "akılcıl", "rasyonel",
                "think", "analyze", "logic", "reason", "result", "research", "compare",
                "evaluate", "evidence", "data", "theory", "hypothesis", "experiment",
                "rational"
            ]
        }

        # Konu anahtar kelimeleri (Türkçe + İngilizce)
        self.topic_keywords = {
            "programlama": ["python", "javascript", "kod", "program", "fonksiyon", "değişken", "sınıf", "api", "html", "css", "react", "node", "git", "loop", "array", "database", "sql",
                            "code", "coding", "developer", "software", "algorithm", "framework", "library", "function", "variable", "class", "method", "debugging"],
            "yapay_zeka": ["ai", "yapay zeka", "makine öğrenmesi", "derin öğrenme", "neural", "model", "llm", "gpt", "çatışma", "algoritma", "eğitim", "dataset", "transformer",
                          "artificial intelligence", "machine learning", "deep learning", "neural network", "language model", "transformer", "training", "dataset"],
            "felsefe": ["anlam", "varlık", "bilinç", "özgür irade", "etik", "ahlak", "hakikat", "gerçeklik", "felsefe", "düşünce", "varoluş", "zaman", "ölüm", "yaşam",
                        "meaning", "existence", "consciousness", "free will", "ethics", "morality", "truth", "reality", "philosophy", "thought", "life"],
            "bilim": ["fizik", "kimya", "biyoloji", "matematik", "evren", "uzay", "atom", "enerji", "kuantum", "gen", "dna", "hücre", "teorisi",
                      "physics", "chemistry", "biology", "mathematics", "universe", "space", "atom", "quantum", "cell", "evolution"],
            "teknoloji": ["bilgisayar", "internet", "yazılım", "donanım", "robot", "otomasyon", "bulut", "güvenlik", "şifre", "ağ", "sunucu",
                          "computer", "internet", "hardware", "robot", "automation", "cloud", "security", "encryption", "server", "network"],
            "duygusal": ["hisset", "mutlu", "üzgün", "korku", "sevgi", "öfke", "endişe", "heyecan", "umut", "hayal"],
            "günlük": ["merhaba", "nasılsın", "ne haber", "günaydın", "iyi geceler", "teşekkür", "hoşça kal",
                       "hello", "how are you", "good morning", "good night", "thanks", "goodbye"],
            "kimlik": ["kimim", "ben kimim", "ne yapabilirim", "özelliğim", "yetenek", "hedef", "amaç", "hayatım",
                       "who am i", "what can i do", "my abilities", "my purpose", "goal", "mission"]
        }

        # Öğrenilen dil kalıpları
        self.learned_patterns = {}
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.learned_patterns = data.get("learned_patterns", {})
                    self.processed_count = data.get("processed_count", 0)
                    self.intent_distribution = data.get("intent_distribution", {})
            except (json.JSONDecodeError, IOError):
                self.processed_count = 0
                self.intent_distribution = {}
        else:
            self.processed_count = 0
            self.intent_distribution = {}

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "learned_patterns": self.learned_patterns,
                "processed_count": self.processed_count,
                "intent_distribution": self.intent_distribution
            }, f, indent=4, ensure_ascii=False)

    def analyze(self, text):
        """
        Metni tam analiz eder — tüm boyutları bir arada döndürür.
        
        Returns:
            dict: intent, emotion, topic, complexity, urgency, sentiment
        """
        result = {
            "intent": self.detect_intent(text),
            "emotion": self.analyze_emotion(text),
            "topic": self.detect_topic(text),
            "complexity": self.analyze_complexity(text),
            "urgency": self.detect_urgency(text),
            "sentiment": self.analyze_sentiment(text),
            "language": self.detect_language(text),
            "has_question": "?" in text,
            "word_count": len(text.split()),
            "char_count": len(text)
        }

        # İstatistikleri güncelle
        self.processed_count += 1
        intent_name = result["intent"]["primary"]
        self.intent_distribution[intent_name] = self.intent_distribution.get(intent_name, 0) + 1

        if self.processed_count % 10 == 0:
            self._save()

        return result

    def detect_language(self, text):
        """
        Metnin dilini otomatik tespit eder.
        
        Returns:
            str: "tr" (Türkçe) veya "en" (İngilizce)
        """
        text_lower = text.lower()

        # Türkçe'ye özgü karakterleri kontrol et
        turkish_chars = set('öüşçğı')
        for char in text_lower:
            if char in turkish_chars:
                return "tr"

        # Yaygın Türkçe kelimeleri kontrol et
        turkish_words = [
            "merhaba", "nasılsın", "teşekkür", "lütfen", "bir", "ve", "ile",
            "için", "ama", "ancak", "veya", "bu", "şu", "o", "nasıl",
            "neden", "ne", "kim", "nasılsın", "nedir", "yapmak", "olmak"
        ]
        words = set(re.findall(r'\w+', text_lower, re.UNICODE))
        for word in words:
            if word in turkish_words:
                return "tr"

        # Varsayılan: İngilizce
        return "en"

    def detect_intent(self, text):
        """
        Metnin niyetini (intent) tespit eder.
        
        Gerçek beynin Broca alanı konuşma niyetini çözer:
        - Bu bir soru mu? Bilgi mi isteniyor?
        - Bir emir mi verilmiş?
        - Bir duygu mu paylaşılıyor?
        - Sadece selamlama mı?
        
        Returns:
            dict: primary intent ve confidence skorları
        """
        text_lower = text.lower().strip()
        scores = {}

        for intent_name, intent_data in self.intent_patterns.items():
            score = 0.0
            for pattern in intent_data["patterns"]:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                score += len(matches) * intent_data["weight"]
            if score > 0:
                scores[intent_name] = round(min(1.0, score / 2.0), 3)

        # Öğrenilmiş kalıpları kontrol et
        for pattern, learned_intent in self.learned_patterns.items():
            if pattern in text_lower:
                scores[learned_intent] = scores.get(learned_intent, 0) + 0.3

        if not scores:
            scores["genel_sohbet"] = 0.5

        # Sırala
        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return {
            "primary": sorted_intents[0][0],
            "confidence": sorted_intents[0][1],
            "all_intents": {k: v for k, v in sorted_intents if v > 0.1}
        }

    def analyze_emotion(self, text):
        """
        Metnin duygusal tonunu analiz eder.
        
        Returns:
            dict: emotion_type, intensity, valence
        """
        text_lower = text.lower()
        words = set(re.findall(r'\w+', text_lower, re.UNICODE))

        emotion_scores = {}
        for emotion_type, keywords in self.emotion_lexicon.items():
            matches = 0
            for word in words:
                # Tam eşleşme VEYA kelime içinde varlık kontrolü
                for keyword in keywords:
                    if word == keyword or keyword in word:
                        matches += 1
                        break
            if matches > 0:
                emotion_scores[emotion_type] = matches / max(len(words), 1)

        if not emotion_scores:
            return {
                "type": "nötr",
                "intensity": 0.0,
                "valence": 0.0  # -1 (negatif) ile 1 (pozitif) arası
            }

        # En baskın duygu
        dominant = max(emotion_scores.items(), key=lambda x: x[1])
        emotion_type = dominant[0]
        intensity = min(1.0, dominant[1] * 3)  # Scale up

        # Valence (duygu yönü)
        valence_map = {"pozitif": 1.0, "negatif": -1.0, "bilişsel": 0.3}
        valence = valence_map.get(emotion_type, 0.0)
        valence = round(valence * intensity, 3)

        return {
            "type": emotion_type,
            "intensity": round(intensity, 3),
            "valence": valence
        }

    def detect_topic(self, text):
        """
        Konuşmanın konusunu tespit eder.
        
        Returns:
            str: Konu adı veya None
        """
        text_lower = text.lower()
        words = set(re.findall(r'\w+', text_lower, re.UNICODE))

        topic_scores = {}
        for topic, keywords in self.topic_keywords.items():
            matches = 0
            for keyword in keywords:
                # Çok kelimeli anahtar kelimeler (ör: "yapay zeka") için alt string kontrolü
                if ' ' in keyword:
                    if keyword in text_lower:
                        matches += 2  # Çok kelimeli eşleşme daha değerli
                else:
                    # Tek kelimeli: set intersection
                    if keyword in words:
                        matches += 1
            if matches:
                topic_scores[topic] = matches

        if not topic_scores:
            return None

        return max(topic_scores.items(), key=lambda x: x[1])[0]

    def analyze_complexity(self, text):
        """
        Metnin karmaşıklığını analiz eder.
        
        Gerçek beynin karmaşık cümleler daha fazla işlem kapasitesi gerektirir.
        
        Returns:
            float: 0 (basit) ile 1 (çok karmaşık) arası
        """
        complexity = 0.0
        words = text.split()

        # Kelime sayısı
        if len(words) > 20:
            complexity += 0.2
        if len(words) > 50:
            complexity += 0.2

        # Ortalama kelime uzunluğu
        avg_len = sum(len(w) for w in words) / max(len(words), 1)
        if avg_len > 6:
            complexity += 0.1

        # Cümle sayısı (nokta/virgül/ünlem)
        sentences = re.split(r'[.!?;]', text)
        if len(sentences) > 2:
            complexity += 0.15

        # Soru işareti
        if "?" in text:
            complexity += 0.05

        # Parantez, tire, iki nokta
        if any(c in text for c in "()[]{}-:"):
            complexity += 0.1

        # Sayılar
        if re.search(r'\d+', text):
            complexity += 0.05

        # Tekrar eden kelimeler
        unique_ratio = len(set(words)) / max(len(words), 1)
        if unique_ratio < 0.5:
            complexity += 0.1

        return round(min(1.0, complexity), 3)

    def detect_urgency(self, text):
        """Aciliyet tespiti."""
        text_lower = text.lower()
        urgency = 0.0

        urgent_words = ["acil", "hemen", "şimdi", "derhal", "lütfeeen", "yaa", "lütfenn", "help", "urgent", "important", "immediately", "asap", "now"]
        for word in urgent_words:
            if word in text_lower:
                urgency += 0.3

        if text.isupper():
            urgency += 0.3
        if text.count("!") >= 2:
            urgency += 0.2

        return round(min(1.0, urgency), 3)

    def analyze_sentiment(self, text):
        """
        Genel duygu analizi (sentiment).
        
        Returns:
            float: -1 (çok negatif) ile 1 (çok pozitif) arası
        """
        emotion = self.analyze_emotion(text)
        base = emotion["valence"]

        # Ünlem işaretleri duyguyu güçlendirir
        exclamation_count = text.count("!")
        if exclamation_count > 0:
            base *= (1 + exclamation_count * 0.2)

        # Büyük harf = güçlü duygu
        if text.isupper():
            base *= 1.3

        return round(max(-1.0, min(1.0, base)), 3)

    def learn_pattern(self, text, corrected_intent):
        """Yeni bir dil kalıbı öğren."""
        # Basit: text'in ilk 3 kelimesini kalıp olarak kaydet
        words = text.lower().split()[:3]
        pattern = " ".join(words)
        if pattern not in self.learned_patterns:
            self.learned_patterns[pattern] = corrected_intent
            self._save()
            return True
        return False

    def get_stats(self):
        return {
            "processed_count": self.processed_count,
            "learned_patterns": len(self.learned_patterns),
            "intent_distribution": self.intent_distribution
        }


if __name__ == "__main__":
    lp = LanguageProcessor()

    tests = [
        "Python fonksiyonları nasıl çalışır?",
        "Bunu hemen açıklar mısın!",
        "Çok mutluyum bugün harika bir gün",
        "Bence yapay zeka insanları yok edebilir",
        "Kuantum fiziği hakkında ne biliyorsun?",
        "MERHABA NASILSIN?",
    ]

    for t in tests:
        result = lp.analyze(t)
        logger.debug("'%s'", t)
        logger.debug("  Niyet: %s (%s)", result['intent']['primary'], result['intent']['confidence'])
        logger.debug("  Duygu: %s (şiddet: %s)", result['emotion']['type'], result['emotion']['intensity'])
        logger.debug("  Konu: %s", result['topic'])
        logger.debug("  Karmaşıklık: %s", result['complexity'])
        logger.debug("  Aciliyet: %s", result['urgency'])
        logger.debug("  Sentiment: %s", result['sentiment'])
