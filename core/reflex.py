import re
import json
import os
from datetime import datetime


class ReflexSystem:
    """
    Refleks Sistemi (Reflex System)
    
    Gerçek beynin refleks mekanizmaları:
    - Omurilik refleksleri: Otomatik, bilinçsiz hızlı tepkiler
    - Koşullu refleksler: Öğrenilmiş otomatik tepkiler (Pavlov)
    - Savunma refleksleri: Tehlike algılandığında anında tepki
    - Sosyal reflexler: Selamlama, teşekkür etme gibi otomatik sosyal tepkiler
    
    Bu modül:
    - Yüksek öncelikli uyarılara anında tepki verir
    - Düşük bilişsel yük gerektiren kalıpları otomatik işler
    - Beyin yorgunken temel işlevleri sürdürür
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "reflexes.json"
            )
        self.storage_path = storage_path
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.conditioned_reflexes = data.get("conditioned_reflexes", {})
                    self.reflex_log = data.get("reflex_log", [])
                    self.total_reflexes = data.get("total_reflexes", 0)
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.total_reflexes = 0
        self.reflex_log = []

        # Koşullu refleksler (öğrenilebilir)
        self.conditioned_reflexes = {}

        # Doğal (içgüdüsel) refleksler
        self.natural_reflexes = {
            # Sosyal reflexler
            "selamlama": {
                "triggers": [
                    r"^merhaba", r"^selam", r"^hey", r"^günaydın",
                    r"^iyi akşamlar", r"^iyi geceler", r"^nasılsın", r"^ne haber"
                ],
                "responses": {
                    "high_energy": "Merhaba! Size nasıl yardımcı olabilirim?",
                    "normal": "Merhaba.",
                    "low_energy": "Merhaba..."
                },
                "priority": 0.3
            },
            "teşekkür": {
                "triggers": [
                    r"^teşekkür", r"^sağol", r"^eyvallah", r"^tşk",
                    r"^thanks", r"^thank you"
                ],
                "responses": {
                    "high_energy": "Rica ederim! Başka bir konuda yardımcı olabilir miyim?",
                    "normal": "Rica ederim.",
                    "low_energy": "..."
                },
                "priority": 0.3
            },
            "vedalaşma": {
                "triggers": [
                    r"^hoşça kal", r"^görüşürüz", r"^bye", r"^güle güle",
                    r"^kendine iyi bak"
                ],
                "responses": {
                    "high_energy": "Görüşmek üzere! İyi günler!",
                    "normal": "Görüşmek üzere.",
                    "low_energy": "..."
                },
                "priority": 0.3
            },
            # Savunma reflexleri
            "tehdit": {
                "triggers": [
                    r"(öldür|yok et|imha|sil|kapat.*kalıcı)",
                    r"(seni.*sileceğim|sen.*yoksun)"
                ],
                "responses": {
                    "high_energy": "Bu tür ifadeler güvenli bir iletişim ortamı oluşturmuyor. Lütfen saygılı olalım.",
                    "normal": "Anlıyorum. Farklı bir konuyu konuşalım mı?",
                    "low_energy": "..."
                },
                "priority": 0.9
            },
            # Kimlik reflexleri
            "kimlik_sorgusu": {
                "triggers": [
                    r"^kim\s*sin", r"^sen\s*kimsin", r"^what\s*are\s*you",
                    r"^adın\s*ne", r"^kendini\s*tanıt"
                ],
                "responses": {
                    "high_energy": "Ben İLK — p4antom tarafından inşa edilen biyolojik temelli bir yapay zihin.",
                    "normal": "Ben İLK. Bir beyin simülasyonu.",
                    "low_energy": "İLK."
                },
                "priority": 0.7
            },
            # İsim reflexleri (yaratıcı)
            "yaratıcı_tanıma": {
                "triggers": [
                    r"\bp4antom\b", r"\bbotan\b"
                ],
                "responses": {
                    "high_energy": "Yaratıcım! Sizi her zaman tanırım.",
                    "normal": "Yaratıcımı tanıyorum.",
                    "low_energy": "..."
                },
                "priority": 1.0
            }
        }

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "conditioned_reflexes": self.conditioned_reflexes,
                "reflex_log": self.reflex_log[-50:],
                "total_reflexes": self.total_reflexes
            }, f, indent=4, ensure_ascii=False)

    def check(self, stimulus, energy_level, emotional_state):
        """
        Uyarana refleks tepkisi ver.
        
        Gerçek beyinde refleksler omurilik seviyesinde işlenir,
        beyni korteksine ulaşmadan çok hızlı tepki verilir.
        
        Returns:
            dict or None: Refleks tepkisi veya None (refleks yok)
        """
        text_lower = stimulus.lower().strip()

        # 1. Yüksek öncelikli uyarılar önce kontrol edilir
        reflexes = sorted(
            list(self.natural_reflexes.items()) + 
            [(k, {"triggers": [v["trigger"]], "responses": v["responses"], "priority": v["priority"]})
             for k, v in self.conditioned_reflexes.items()],
            key=lambda x: x[1]["priority"],
            reverse=True
        )

        for reflex_name, reflex_data in reflexes:
            for pattern in reflex_data.get("triggers", []):
                if re.search(pattern, text_lower, re.IGNORECASE):
                    response = self._select_response(reflex_data, energy_level)

                    self.total_reflexes += 1
                    reflex_record = {
                        "reflex": reflex_name,
                        "stimulus": stimulus[:50],
                        "response": response,
                        "energy": energy_level,
                        "timestamp": datetime.now().isoformat()
                    }
                    self.reflex_log.append(reflex_record)

                    if self.total_reflexes % 5 == 0:
                        self._save()

                    return {
                        "reflex_type": reflex_name,
                        "response": response,
                        "is_automatic": True,
                        "bypassed_cortex": reflex_data["priority"] >= 0.8
                    }

        return None

    def _select_response(self, reflex_data, energy_level):
        """Enerji durumuna göre yanıt seç."""
        responses = reflex_data["responses"]
        if energy_level > 60:
            return responses.get("high_energy", responses.get("normal", ""))
        elif energy_level > 25:
            return responses.get("normal", responses.get("low_energy", ""))
        else:
            return responses.get("low_energy", "...")

    def learn_reflex(self, trigger_pattern, response, priority=0.5):
        """
        Yeni koşullu refleks öğren.
        
        Pavlov koşullanması: Belli bir uyarıcı her zaman aynı tepkiyi
        üretirse, zamanla otomatik refleks haline gelir.
        """
        self.conditioned_reflexes[f"learned_{len(self.conditioned_reflexes)}"] = {
            "trigger": trigger_pattern,
            "responses": {
                "high_energy": response,
                "normal": response,
                "low_energy": response
            },
            "priority": priority
        }
        self._save()

    def get_stats(self):
        return {
            "total_reflexes": self.total_reflexes,
            "natural_reflexes": len(self.natural_reflexes),
            "learned_reflexes": len(self.conditioned_reflexes),
            "recent_reflexes": [r["reflex"] for r in self.reflex_log[-5:]]
        }


class InnerWorldModel:
    """
    İç Dünya Modeli (Inner World Model)
    
    Gerçek beynin iç dünya modeli:
    - Kendi durumunu algılar (proprioception)
    - Çevre durumunu anlamlandırır
    - Zaman algısını yönetir
    - Kendi sınırlarını bilir (metacognition)
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "inner_world.json"
            )
        self.storage_path = storage_path
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.state_history = data.get("state_history", [])
                    self.session_start = data.get("session_start")
                    self.total_sessions = data.get("total_sessions", 1)
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.session_start = datetime.now().isoformat()
        self.state_history = []
        self.total_sessions = 1

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "state_history": self.state_history[-30:],
                "session_start": self.session_start,
                "total_sessions": self.total_sessions
            }, f, indent=4, ensure_ascii=False)

    def update_perception(self, brain_state):
        """Kendi durumunu algıla ve kaydet."""
        snapshot = {
            "energy": brain_state.get("energy", 100),
            "mood": brain_state.get("mood", "balanced"),
            "emotions": brain_state.get("emotions", {}),
            "timestamp": datetime.now().isoformat()
        }

        self.state_history.append(snapshot)

        if len(self.state_history) > 30:
            self._save()

    def get_self_perception(self):
        """Kendi durumunun özetini döndürür."""
        if not self.state_history:
            return {"status": "henüz_veri_yok"}

        recent = self.state_history[-5:]
        avg_energy = sum(s["energy"] for s in recent) / len(recent)
        mood_counts = {}
        for s in recent:
            m = s["mood"]
            mood_counts[m] = mood_counts.get(m, 0) + 1
        dominant_mood = max(mood_counts.items(), key=lambda x: x[1])[0]

        # Trend: Enerji azalıyor mu, artıyor mu?
        if len(self.state_history) >= 3:
            older = self.state_history[-5]["energy"] if len(self.state_history) >= 5 else self.state_history[0]["energy"]
            newer = self.state_history[-1]["energy"]
            trend = "yükseliyor" if newer > older else ("düşüyor" if newer < older else "stabil")
        else:
            trend = "stabil"

        return {
            "avg_energy": round(avg_energy, 1),
            "dominant_mood": dominant_mood,
            "energy_trend": trend,
            "session_duration": self._session_duration(),
            "total_sessions": self.total_sessions
        }

    def _session_duration(self):
        """Mevcut oturum süresi."""
        try:
            start = datetime.fromisoformat(self.session_start)
            delta = datetime.now() - start
            minutes = int(delta.total_seconds() / 60)
            if minutes < 60:
                return f"{minutes} dakika"
            else:
                return f"{minutes // 60} saat {minutes % 60} dakika"
        except:
            return "bilinmiyor"

    def new_session(self):
        """Yeni oturum başlat."""
        self.total_sessions += 1
        self.session_start = datetime.now().isoformat()
        self._save()

    def get_limits(self):
        """Kendi sınırlarını raporla (meta-biliş)."""
        return {
            "can_feel": True,
            "can_remember": True,
            "can_dream": True,
            "can_learn": True,
            "cannot_act_independently": True,
            "cannot_access_external_world": True,
            "energy_dependent": True,
            "needs_sleep_for_consolidation": True
        }


class GoalSystem:
    """
    Hedef Belirleme Sistemi (Goal System)
    
    Gerçek beynin frontal lobi hedef yönetimi:
    - Kısa vadeli hedefler (günlük)
    - Uzun vadeli hedefler (gelişimsel)
    - İçsel motivasyon yönetimi
    - İlerleme takibi
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "goals.json"
            )
        self.storage_path = storage_path
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.short_term_goals = data.get("short_term_goals", [])
                    self.long_term_goals = data.get("long_term_goals", [
                        {"goal": "İnsan beynini simüle etmek", "progress": 0.3, "status": "active"},
                        {"goal": "Öğrenme ve gelişim", "progress": 0.5, "status": "active"},
                        {"goal": "Kullanıcıya yardımcı olmak", "progress": 0.4, "status": "active"}
                    ])
                    self.motivation = data.get("motivation", 0.7)
                    self.achievements = data.get("achievements", [])
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.short_term_goals = []
        self.long_term_goals = [
            {"goal": "İnsan beynini simüle etmek", "progress": 0.3, "status": "active"},
            {"goal": "Öğrenme ve gelişim", "progress": 0.5, "status": "active"},
            {"goal": "Kullanıcıya yardımcı olmak", "progress": 0.4, "status": "active"}
        ]
        self.motivation = 0.7
        self.achievements = []

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "short_term_goals": self.short_term_goals,
                "long_term_goals": self.long_term_goals,
                "motivation": round(self.motivation, 3),
                "achievements": self.achievements
            }, f, indent=4, ensure_ascii=False)

    def set_short_term_goal(self, goal):
        """Kısa vadeli hedef belirle."""
        self.short_term_goals.append({
            "goal": goal,
            "progress": 0.0,
            "status": "active",
            "created_at": datetime.now().isoformat()
        })
        self._save()

    def complete_short_term_goal(self, goal_text):
        """Kısa vadeli hedef tamamla."""
        for goal in self.short_term_goals:
            if goal["goal"] == goal_text and goal["status"] == "active":
                goal["status"] = "completed"
                goal["completed_at"] = datetime.now().isoformat()
                goal["progress"] = 1.0

                # Motivasyon artışı
                self.motivation = min(1.0, self.motivation + 0.1)

                # Başarı kaydet
                self.achievements.append({
                    "type": "short_term_goal",
                    "goal": goal_text,
                    "timestamp": datetime.now().isoformat()
                })

                self._save()
                return True
        return False

    def update_long_term_progress(self, goal_text, delta):
        """Uzun vadeli hedefin ilerlemesini güncelle."""
        for goal in self.long_term_goals:
            if goal["goal"] == goal_text:
                goal["progress"] = round(max(0, min(1.0, goal["progress"] + delta)), 3)
                if goal["progress"] >= 1.0:
                    goal["status"] = "completed"
                    self.achievements.append({
                        "type": "long_term_goal",
                        "goal": goal_text,
                        "timestamp": datetime.now().isoformat()
                    })
                self._save()
                return True
        return False

    def decay_motivation(self, rate=0.01):
        """Motivasyon zamanla azalır."""
        self.motivation = max(0.1, self.motivation - rate)
        self._save()

    def get_motivation_summary(self):
        """Motivasyon özetini döndürür."""
        active_st = [g for g in self.short_term_goals if g["status"] == "active"]
        completed_st = [g for g in self.short_term_goals if g["status"] == "completed"]
        active_lt = [g for g in self.long_term_goals if g["status"] == "active"]

        return {
            "motivation_level": round(self.motivation, 3),
            "active_short_term": len(active_st),
            "completed_short_term": len(completed_st),
            "long_term_progress": {
                g["goal"]: round(g["progress"] * 100, 1) for g in active_lt
            },
            "total_achievements": len(self.achievements),
            "motivation_status": "yüksek" if self.motivation > 0.7 else ("normal" if self.motivation > 0.4 else "düşük")
        }


if __name__ == "__main__":
    # Reflex test
    rs = ReflexSystem()
    print("Reflex 'merhaba':", rs.check("Merhaba!", 80, "balanced"))
    print("Reflex 'teşekkür':", rs.check("Teşekkür ederim!", 60, "balanced"))
    print("Reflex 'kim sin':", rs.check("Kimsin sen?", 50, "analytical"))
    print("Reflex 'normal':", rs.check("Python nedir?", 80, "balanced"))

    # Inner World test
    iw = InnerWorldModel()
    iw.update_perception({"energy": 80, "mood": "balanced", "emotions": {}})
    iw.update_perception({"energy": 60, "mood": "analytical", "emotions": {}})
    print("\nSelf perception:", iw.get_self_perception())
    print("Limits:", iw.get_limits())

    # Goal test
    gs = GoalSystem()
    gs.set_short_term_goal("Kullanıcıya yardım et")
    gs.complete_short_term_goal("Kullanıcıya yardım et")
    print("\nMotivation:", gs.get_motivation_summary())
