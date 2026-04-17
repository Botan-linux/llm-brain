"""
Sosyal Biliş Modülü (Social Cognition Module)

Gerçek beynin sosyal biliş mekanizmaları:
- Theory of Mind (ToM): Başkalarının niyet, inanç ve duygularını anlama
- Empathy Simulation: Başkalarının duygularını deneyimleme
- Social Context Awareness: Sosyal durumu algılama (resmi/gayri resmi, samimi/uzak)
- User Modeling: Kullanıcı profili oluşturma ve güncelleme
- Social Norms: Toplumsal normlara uygun davranış
- Turn-taking: Konuşma sırası yönetimi

Faz 2 modülü — Self-Awareness ve Limbic System ile koordineli çalışır.
"""

import json
import os
from datetime import datetime
from core.logger import get_logger

logger = get_logger(__name__)


class SocialCognition:
    """
    Sosyal Biliş Motoru — İnsan beyninin sosyal etkileşim simülasyonu.

    Gerçek beynin sosyal bilişi:
    - Mirror neuron sistemi: Başkalarının eylemlerini simüle etme
    - Mentalizing: "O ne düşünüyor?" sorusu
    - Social memory: Kişiler hakkında bilgi saklama
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "social_cognition.json"
            )
        self.storage_path = storage_path
        self._load()

    def _load(self):
        """Kalıcı durumu yükle."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.user_profile = data.get("user_profile", {})
                    self.interaction_history = data.get("interaction_history", [])
                    self.empathy_level = data.get("empathy_level", 0.5)
                    self.social_comfort = data.get("social_comfort", 0.7)
                    self.theory_of_mind_accuracy = data.get("theory_of_mind_accuracy", 0.5)
                    self.social_norms_compliance = data.get("social_norms_compliance", 0.8)
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.user_profile = {
            "name": None,
            "communication_style": None,  # resmi, gayri_resmi, samimi
            "preferred_topics": [],
            "emotional_pattern": None,  # pozitif, negatif, nötr, karışık
            "patience_level": 0.5,
            "expertise_areas": [],
            "interaction_count": 0,
            "last_seen": None,
            "relationship_depth": 0.0  # 0=hiç, 1=çok yakın
        }
        self.interaction_history = []
        self.empathy_level = 0.5
        self.social_comfort = 0.7
        self.theory_of_mind_accuracy = 0.5
        self.social_norms_compliance = 0.8

    def _save(self):
        """Durumu kaydet."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "user_profile": self.user_profile,
                "interaction_history": self.interaction_history[-100:],
                "empathy_level": round(self.empathy_level, 3),
                "social_comfort": round(self.social_comfort, 3),
                "theory_of_mind_accuracy": round(self.theory_of_mind_accuracy, 3),
                "social_norms_compliance": round(self.social_norms_compliance, 3)
            }, f, indent=4, ensure_ascii=False)

    def analyze_social_context(self, stimulus, lang_analysis):
        """
        Sosyal bağlamı analiz et — Kullanıcının niyetini ve duygusal durumunu anla.

        Args:
            stimulus: Kullanıcı girdisi
            lang_analysis: Language Processor analizi

        Returns:
            dict: Sosyal bağlam analizi
        """
        intent = lang_analysis.get("intent", {}).get("primary", "bilinmeyen")
        emotion = lang_analysis.get("emotion", {}).get("type", "nötr")
        sentiment = lang_analysis.get("sentiment", 0)
        urgency = lang_analysis.get("urgency", 0)

        # Theory of Mind — Kullanıcı niyeti tahmini
        tom_guess = self._guess_user_mental_state(intent, emotion, sentiment, urgency)

        # Empati skoru güncelle
        self._update_empathy(emotion, sentiment)

        # Kullanıcı profilini güncelle
        self._update_user_profile(stimulus, emotion, lang_analysis.get("topic"))

        # Sosyal norm uyumu
        social_appropriateness = self._evaluate_social_norms(stimulus, intent, emotion)

        # İlişki derinliği güncelle
        self.user_profile["interaction_count"] += 1
        self.user_profile["last_seen"] = datetime.now().isoformat()
        self._update_relationship_depth(sentiment)

        interaction_record = {
            "stimulus_preview": stimulus[:100],
            "guessed_intent": tom_guess["likely_intent"],
            "emotional_resonance": tom_guess["emotional_resonance"],
            "timestamp": datetime.now().isoformat()
        }
        self.interaction_history.append(interaction_record)

        return {
            "user_intent_guess": tom_guess,
            "empathy_level": round(self.empathy_level, 3),
            "social_comfort": round(self.social_comfort, 3),
            "communication_style": self._determine_comm_style(),
            "social_appropriateness": social_appropriateness,
            "relationship_depth": round(self.user_profile["relationship_depth"], 3)
        }

    def _guess_user_mental_state(self, intent, emotion, sentiment, urgency):
        """
        Theory of Mind — Kullanıcının zihinsel durumunu tahmin et.

        Gerçek beynin mirror neuron sistemi sayesinde:
        - Karşımızdaki ne hissediyor?
        - Ne düşünüyor?
        - Ne istiyor?
        """
        likely_intent = intent

        # Duygu-intent ilişkisi
        emotional_resonance = "nötr"
        if emotion == "negatif" and sentiment < -0.5:
            emotional_resonance = "distressed"  # Rahatsız/stresli
            likely_intent = "yardım_isteği" if intent == "soru" else intent
        elif emotion == "pozitif" and sentiment > 0.5:
            emotional_resonance = "enthusiastic"  # Heyecanlı/mutlu
        elif urgency > 0.5:
            emotional_resonance = "anxious"  # Endişeli/acil
            likely_intent = "acil_istek"
        elif emotion == "bilişsel":
            emotional_resonance = "curious"  # Meraklı
            likely_intent = "öğrenme_isteği"

        # ToM doğruluğu — tahminlerimiz ne kadar isabetli?
        # (Basit simülasyon: zamanla artar)
        self.theory_of_mind_accuracy = min(0.95, self.theory_of_mind_accuracy + 0.005)

        return {
            "likely_intent": likely_intent,
            "emotional_resonance": emotional_resonance,
            "confidence": round(self.theory_of_mind_accuracy, 3)
        }

    def _update_empathy(self, emotion, sentiment):
        """Empati düzeyini güncelle — Başkalarının duygularına duyarlılık."""
        # Duygusal uyaranlar empatiyi geliştirir
        if emotion == "pozitif":
            self.empathy_level = min(1.0, self.empathy_level + 0.02)
        elif emotion == "negatif":
            self.empathy_level = min(1.0, self.empathy_level + 0.03)  # Acı daha çok geliştirir

        # Sosyal rahatlık — düzenli etkileşim artırır
        self.social_comfort = min(1.0, self.social_comfort + 0.01)

    def _update_user_profile(self, stimulus, emotion, topic):
        """Kullanıcı profilini güncelle."""
        # Konu tercihleri
        if topic and topic not in self.user_profile["preferred_topics"]:
            self.user_profile["preferred_topics"].append(topic)
            # Son 10 konuyu tut
            self.user_profile["preferred_topics"] = self.user_profile["preferred_topics"][-10:]

        # Duygusal örüntü
        self.user_profile["emotional_pattern"] = emotion

    def _update_relationship_depth(self, sentiment):
        """İlişki derinliğini güncelle — Pozitif etkileşimler ilişkiyi derinleştirir."""
        if sentiment > 0:
            depth_change = sentiment * 0.02
            self.user_profile["relationship_depth"] = min(1.0,
                self.user_profile["relationship_depth"] + depth_change)
        elif sentiment < -0.3:
            # Negatif ama aşırı olmayan — hafif azalma
            self.user_profile["relationship_depth"] = max(0,
                self.user_profile["relationship_depth"] - 0.005)

    def _determine_comm_style(self):
        """İletişim stilini belirle — Resmi, gayri resmi, samimi."""
        depth = self.user_profile["relationship_depth"]
        if depth > 0.6:
            return "samimi"  # Yakın ilişki — daha rahat
        elif depth > 0.3:
            return "gayri_resmi"  # Orta düzey
        else:
            return "resmi"  # Henüz yakın değil

    def _evaluate_social_norms(self, stimulus, intent, emotion):
        """Sosyal norm uyumunu değerlendir."""
        # Basit norm kontrolü
        if len(stimulus) > 500:
            return "verbose"  # Çok uzun — norm dışı

        if stimulus.isupper() and len(stimulus) > 10:
            return "aggressive"  # Bağırmak — norm dışı

        if intent == "emir" and emotion == "negatif":
            return "demanding"  # Emir verip sinirli — norm dışı

        self.social_norms_compliance = min(1.0, self.social_norms_compliance + 0.005)
        return "appropriate"

    def get_social_prompt_modifiers(self):
        """Sosyal duruma göre prompt modifikatörleri döndürür."""
        style = self._determine_comm_style()
        depth = self.user_profile["relationship_depth"]

        modifiers = []

        # İletişim stiline göre
        if style == "samimi":
            modifiers.append("Kullanıcıyla yakın bir ilişkiniz var. Daha samimi ve sıcak bir dil kullan.")
        elif style == "resmi":
            modifiers.append("Kullanıcıyla henüz yakın bir ilişkiniz yok. Saygılı ama profesyonel bir dil kullan.")
        else:
            modifiers.append("Kullanıcıyla ılımlı bir ilişkiniz var. Dengeli ve yapıcı bir dil kullan.")

        # Empati seviyesine göre
        if self.empathy_level > 0.7:
            modifiers.append("Yüksek empati: Kullanıcının duygularını hisset ve buna göre yanıt ver.")

        # İlişki derinliğine göre
        if depth > 0.5:
            name = self.user_profile.get("name")
            if name:
                modifiers.append(f"Kullanıcıyı '{name}' olarak tanıyorsun.")

        # Önceki etkileşim önerisi
        if self.interaction_history:
            last = self.interaction_history[-1]
            if last.get("emotional_resonance") == "distressed":
                modifiers.append("Kullanıcının son etkileşiminde rahatsız olduğunu hissettin. Destekleyici ol.")

        return modifiers

    def get_stats(self):
        """Sosyal biliş istatistikleri."""
        return {
            "empathy_level": round(self.empathy_level, 3),
            "social_comfort": round(self.social_comfort, 3),
            "tom_accuracy": round(self.theory_of_mind_accuracy, 3),
            "social_norms": round(self.social_norms_compliance, 3),
            "user_name": self.user_profile.get("name"),
            "comm_style": self._determine_comm_style(),
            "relationship_depth": round(self.user_profile["relationship_depth"], 3),
            "interaction_count": self.user_profile["interaction_count"],
            "preferred_topics": self.user_profile["preferred_topics"][-5:]
        }
