import json
import os
import time
from datetime import datetime


class PrefrontalCortex:
    """
    Prefrontal Korteks — İnsan beyninin yönetici merkezi.
    
    Gerçek beynin prefrontal korteksi şu işlevleri yerine getirir:
    - Karar verme: Birden fazla seçenek arasından en uygununu seçme
    - Plan yapma: Hedefe ulaşmak için adımları belirleme
    - Öz-denetim (self-control): Dürtüleri kontrol etme, acele karar vermeme
    - Bilişsel esneklik: Perspektif değiştirme, alternatif düşünme
    - Çıkarım çıkarım: Nedensellik ilişkileri kurma
    """

    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "prefrontal.json"
            )
        self.storage_path = storage_path
        self._load()

        # Aktif plan
        self.active_plan = None
        self.current_step_index = 0
        self.plan_history = []

    def _load(self):
        """Önceki durumu yükle."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.decision_log = data.get("decision_log", [])
                    self.impulse_threshold = data.get("impulse_threshold", 0.7)
                    self.cognitive_flexibility = data.get("cognitive_flexibility", 0.5)
                    self.plan_memory = data.get("plan_memory", [])
                    self.total_decisions = data.get("total_decisions", 0)
                    self.self_control_score = data.get("self_control_score", 0.5)
            except (json.JSONDecodeError, IOError):
                self._reset()
        else:
            self._reset()

    def _reset(self):
        self.decision_log = []
        self.impulse_threshold = 0.7
        self.cognitive_flexibility = 0.5
        self.plan_memory = []
        self.total_decisions = 0
        self.self_control_score = 0.5

    def _save(self):
        """Durumu kaydet."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({
                "decision_log": self.decision_log[-100:],  # Son 100 karar
                "impulse_threshold": self.impulse_threshold,
                "cognitive_flexibility": self.cognitive_flexibility,
                "plan_memory": self.plan_memory[-50:],
                "total_decisions": self.total_decisions,
                "self_control_score": self.self_control_score
            }, f, indent=4, ensure_ascii=False)

    def make_decision(self, options, context, energy_level, emotional_state):
        """
        Birden fazla seçenek arasından karar verir.
        
        Gerçek beynin prefrontal korteksi:
        1. Seçenekleri değerlendirir
        2. Duygusal durumu hesaba katar
        3. Enerji durumunu göz önünde bulundurur
        4. Önceki deneyimlerden öğrenir
        5. En uygun kararı verir
        
        Args:
            options: Seçenek listesi [{"action": "...", "reason": "...", "risk": 0.5}, ...]
            context: Mevcut bağlam (string)
            energy_level: Enerji seviyesi (0-100)
            emotional_state: Duygusal durum (string)
        
        Returns:
            dict: Seçilen eylem ve gerekçe
        """
        if not options:
            return {"action": "bekle", "reason": "Seçenek yok — nötr bekleme kararı.", "confidence": 0.0}

        # 1. Her seçeneği puanla
        scored_options = []
        for option in options:
            score = self._evaluate_option(option, context, energy_level, emotional_state)
            scored_options.append((option, score))

        # 2. Puanlara göre sırala
        scored_options.sort(key=lambda x: x[1], reverse=True)

        # 3. Öz-denetim: Düşük enerjide riskli kararlardan kaçın
        selected = scored_options[0][0]
        confidence = scored_options[0][1]

        if energy_level < 30:
            # Düşük enerjide güvenli seçeneğe yönel
            for opt, score in scored_options:
                if opt.get("risk", 0.5) < 0.4:
                    selected = opt
                    confidence = score
                    break

        if emotional_state in ["defensive", "exhausted"]:
            # Stres altında öz-denetim devreye girer
            if selected.get("risk", 0.5) > 0.7 and confidence < self.impulse_threshold:
                # Dürtüsel kararı engelle, daha güvenli alternatif seç
                for opt, score in scored_options[1:]:
                    if opt.get("risk", 0.5) < selected.get("risk", 0.5):
                        selected = opt
                        confidence = score * 0.9  # Güvenli seçeneğe güven biraz düşer
                        self.self_control_score = min(1.0, self.self_control_score + 0.05)
                        break

        # 4. Kararı kaydet
        decision = {
            "context": context[:200],
            "selected_action": selected.get("action", "bilinmeyen"),
            "confidence": round(confidence, 3),
            "energy_at_decision": energy_level,
            "emotional_state": emotional_state,
            "alternatives_count": len(options) - 1,
            "timestamp": datetime.now().isoformat()
        }
        self.decision_log.append(decision)
        self.total_decisions += 1

        # Bilişsel esneklik: Farklı bağlamlarda farklı kararlar veriyorsan artar
        self._update_cognitive_flexibility()

        # Periyodik kaydet
        if self.total_decisions % 5 == 0:
            self._save()

        return {
            "action": selected.get("action", "bilinmeyen"),
            "reason": selected.get("reason", ""),
            "confidence": round(confidence, 3)
        }

    def _evaluate_option(self, option, context, energy, emotion):
        """Tek bir seçeneği çok faktörlü değerlendirir."""
        score = 0.5  # Temel skor

        # Risk analizi
        risk = option.get("risk", 0.5)
        if risk < 0.3:
            score += 0.2  # Düşük risk = bonus
        elif risk > 0.7:
            score -= 0.15  # Yüksek risk = ceza

        # Enerji faktörü: Yüksek enerji gerektiren eylemler düşük enerjide ceza alır
        energy_cost = option.get("energy_cost", 0.5)
        if energy < 40 and energy_cost > 0.5:
            score -= 0.2

        # Önceki deneyimler: Benzer bağlamlarda aynı eylem iyi sonuç vermişse bonus
        prev = self._find_previous_outcome(option.get("action", ""), context)
        if prev is not None:
            score += prev * 0.2  # -1 ile 1 arası, olumlu ise bonus

        # Duygusal uyum: Duygusal durumla eylemin uyumu
        if emotion == "analytical" and option.get("type") == "think":
            score += 0.1
        if emotion == "curious" and option.get("type") == "explore":
            score += 0.1
        if emotion == "exhausted" and option.get("type") == "rest":
            score += 0.15

        # Neden kalitesi: Gerekçe sunulmuşsa bonus
        if option.get("reason") and len(option.get("reason", "")) > 20:
            score += 0.05

        return max(0, min(1, score))

    def _find_previous_outcome(self, action, context):
        """Geçmişte bu eylemin benzer bağlamda nasıl sonuçlandığını bulur."""
        if not self.decision_log:
            return None

        context_words = set(context.lower().split()[:10])
        relevant = []

        for decision in self.decision_log[-20:]:  # Son 20 karara bak
            if decision.get("selected_action") == action:
                # Basit kelime benzerliği
                prev_words = set(decision.get("context", "").lower().split()[:10])
                overlap = len(context_words & prev_words)
                if overlap > 2:
                    relevant.append(decision.get("confidence", 0.5))

        if relevant:
            # Ortalama sonuç (0.5'ten yüksekse olumlu, düşükse olumsuz)
            avg = sum(relevant) / len(relevant)
            return (avg - 0.5) * 2  # -1 ile 1 arasına normalize et
        return None

    def _update_cognitive_flexibility(self):
        """Bilişsel esnekliği güncelle — farklı kararlar verme eğilimi."""
        if len(self.decision_log) < 5:
            return

        recent_actions = [d["selected_action"] for d in self.decision_log[-10:]]
        unique_actions = len(set(recent_actions))
        diversity = unique_actions / len(recent_actions)

        # Çeşitlilik yüksekse bilişsel esneklik artar
        target = 0.3 + (diversity * 0.5)
        self.cognitive_flexibility += (target - self.cognitive_flexibility) * 0.1
        self.cognitive_flexibility = round(max(0.1, min(1.0, self.cognitive_flexibility)), 3)

    def create_plan(self, goal, steps, priority="normal"):
        """
        Bir hedef için plan oluştur.
        
        Args:
            goal: Hedef açıklaması (string)
            steps: Adımlar listesi [{"action": "...", "depends_on": [0, 1]}, ...]
            priority: "low", "normal", "high", "critical"
        
        Returns:
            dict: Plan bilgisi
        """
        plan = {
            "id": len(self.plan_memory) + 1,
            "goal": goal,
            "steps": steps,
            "priority": priority,
            "status": "active",
            "current_step": 0,
            "created_at": datetime.now().isoformat(),
            "completed_steps": [],
            "blocked": False
        }

        self.active_plan = plan
        self.current_step_index = 0
        self.plan_memory.append(plan)
        self._save()

        return plan

    def advance_plan(self, result=None):
        """Aktif planda bir sonraki adıma geç."""
        if not self.active_plan or self.active_plan["status"] != "active":
            return None

        step = self.active_plan["steps"][self.current_step_index]

        # Adımı tamamlandı olarak işaretle
        self.active_plan["completed_steps"].append({
            "step": step,
            "result": result,
            "completed_at": datetime.now().isoformat()
        })

        self.current_step_index += 1

        if self.current_step_index >= len(self.active_plan["steps"]):
            self.active_plan["status"] = "completed"
            self.active_plan["completed_at"] = datetime.now().isoformat()
            completed_plan = self.active_plan
            self.active_plan = None
            self.current_step_index = 0
            self._save()
            return {"status": "plan_completed", "plan": completed_plan}

        self._save()
        return {
            "status": "next_step",
            "step": self.active_plan["steps"][self.current_step_index],
            "progress": f"{self.current_step_index}/{len(self.active_plan['steps'])}"
        }

    def get_current_plan_status(self):
        """Aktif planın durumunu döndürür."""
        if not self.active_plan:
            return {"status": "no_active_plan"}
        return {
            "status": self.active_plan["status"],
            "goal": self.active_plan["goal"],
            "progress": f"{self.current_step_index}/{len(self.active_plan['steps'])}",
            "current_step": self.active_plan["steps"][self.current_step_index] if self.current_step_index < len(self.active_plan["steps"]) else None
        }

    def evaluate_impulse(self, action, context, emotional_state):
        """
        Dürtü kontrolü — acele edilmiş bir karar mı?
        
        Gerçek beynin prefrontal korteksi dürtüleri (impulse) kontrol eder.
        Özellikle amygdala (limbik sistem) aşırı tepki verdiğinde frenler.
        
        Returns:
            dict: Dürtü kontrol sonucu
        """
        # Dürtüsellik skorları
        impulsivity = 0.0

        # Kısa ve yoğun eylemler dürtüsel
        if len(action) < 10:
            impulsivity += 0.3
        if action.isupper():
            impulsivity += 0.4
        if "!" in action:
            impulsivity += 0.2

        # Stres altında dürtüsellik artar
        if emotional_state in ["defensive", "exhausted"]:
            impulsivity += 0.2

        # Öz-denetim kontrolü
        is_impulsive = impulsivity > self.impulse_threshold

        if is_impulsive:
            # Öz-denetim tetiklendi — dürtüsellik eşiği güçlenir
            self.self_control_score = min(1.0, self.self_control_score + 0.03)
            return {
                "is_impulsive": True,
                "impulsivity_score": round(impulsivity, 3),
                "recommendation": "Bu eylem dürtüsel görünüyor. Birkaç saniye beklemeyi düşün.",
                "should_delay": True
            }
        else:
            return {
                "is_impulsive": False,
                "impulsivity_score": round(impulsivity, 3),
                "recommendation": "Eylem mantıklı görünüyor.",
                "should_delay": False
            }

    def get_stats(self):
        """Prefrontal korteks istatistikleri."""
        return {
            "total_decisions": self.total_decisions,
            "recent_decisions": len(self.decision_log),
            "self_control_score": round(self.self_control_score, 3),
            "cognitive_flexibility": round(self.cognitive_flexibility, 3),
            "impulse_threshold": round(self.impulse_threshold, 3),
            "active_plan": self.get_current_plan_status(),
            "completed_plans": len([p for p in self.plan_memory if p.get("status") == "completed"]),
            "total_plans": len(self.plan_memory)
        }


if __name__ == "__main__":
    pfc = PrefrontalCortex()
    
    # Test: Karar verme
    options = [
        {"action": "derin_araştır", "reason": "Konuyu detaylı incele, bilgi topla.", "risk": 0.1, "energy_cost": 0.6, "type": "think"},
        {"action": "hızlı_yanıt", "reason": "Kısa ve öz cevap ver.", "risk": 0.3, "energy_cost": 0.3, "type": "respond"},
        {"action": "bekle", "reason": "Daha fazla bağlam bekle.", "risk": 0.0, "energy_cost": 0.1, "type": "rest"},
    ]
    
    decision = pfc.make_decision(options, "Kullanıcı karmaşık bir soru sordu", 80, "analytical")
    print(f"Karar: {decision}")
    
    # Test: Dürtü kontrolü
    impulse = pfc.evaluate_impulse("HAYIR!", "saldırı", "defensive")
    print(f"Dürtü kontrolü: {impulse}")
    
    # Test: Plan
    plan = pfc.create_plan("Proje hakkında öğren", [
        {"action": "README oku"},
        {"action": "Kod analiz et"},
        {"action": "Özet çıkar"},
    ])
    print(f"Plan: {plan}")
    
    print(f"Stats: {pfc.get_stats()}")
