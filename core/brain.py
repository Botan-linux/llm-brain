import json
import os
import signal
import sys
import atexit
from core.intelligence import IntelligenceLayer
from core.memory import MemoryGateway
from core.limbic import LimbicSystem
from core.thalamus import Thalamus
from core.ego import CyberEgo
from core.prefrontal import PrefrontalCortex
from core.working_memory import WorkingMemory
from core.language_processor import LanguageProcessor
from core.emotional_memory import EmotionalMemory
from core.learning import LearningEngine
from core.dream_engine import DreamEngine
from core.self_awareness import SelfAwareness
from core.reflex import ReflexSystem, InnerWorldModel, GoalSystem
from core.subconscious import Subconscious


class ArtificialBrain:
    """
    İLK — Yapay Beyin Simülasyonu v0.3
    
    İnsan beyninin temel yapılarını ve süreçlerini simüle eder:
    - Thalamus: Dikkat filtresi
    - Limbic System: Duygu yönetimi
    - Prefrontal Cortex: Karar verme, plan yapma, öz-denetim
    - Intelligence Layer: LLM zeka katmanı
    - Cyber Ego: Bilinç ve kişilik
    - Memory Gateway: Uzun/kısa süreli hafıza
    - Working Memory: Konuşma bağlamı
    - Emotional Memory: Duygu-hafıza ilişkilendirme
    - Language Processor: Dil analizi
    - Learning Engine: Deneyimlerden öğrenme
    - Dream Engine: Rüya ve yaratıcılık
    - Self-Awareness: Öz-farkındalık
    - Reflex System: Otomatik tepkiler
    - Inner World Model: İç dünya algısı
    - Goal System: Hedef belirleme
    """

    def __init__(self, settings_path=None):
        if settings_path is None:
            settings_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "brain_state.json"
            )

        self.settings_path = settings_path

        # === Temel Modüller (Faz 0) ===
        self.memory = MemoryGateway()
        self.intelligence = IntelligenceLayer()
        self.limbic = LimbicSystem()
        self.thalamus = Thalamus()
        self.ego = CyberEgo()

        # === Faz 1: Temel Beyin İşlevleri ===
        self.prefrontal = PrefrontalCortex()
        self.working_memory = WorkingMemory()
        self.language_processor = LanguageProcessor()
        self.emotional_memory = EmotionalMemory()

        # === Faz 2: Öğrenme ve Gelişim ===
        self.learning = LearningEngine()
        self.dream_engine = DreamEngine(self.memory, self.intelligence, self.emotional_memory)
        self.self_awareness = SelfAwareness()
        self.subconscious = Subconscious(self.memory, self.intelligence)

        # === Faz 3: Otonom Davranış ===
        self.reflex = ReflexSystem()
        self.inner_world = InnerWorldModel()
        self.goals = GoalSystem()

        # Durum yükle
        self.state = self._load_state()

        # Sinyal koruması
        signal.signal(signal.SIGINT, self._handle_exit_attempt)
        atexit.register(self.maintenance)

    def _load_state(self):
        default_state = {
            "energy": 100,
            "last_stimulus": None,
            "development_stage": self.limbic.development_stage,
            "session_count": 0,
            "version": "0.3"
        }
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    default_state.update(saved)
            except (json.JSONDecodeError, IOError):
                pass
        return default_state

    def _save_state(self):
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)

    def _handle_exit_attempt(self, signum, frame):
        print("\n\n[!] Sistem: Beyin fonksiyonları aniden kesilemez. Lütfen 'uyu' komutunu kullanın.")

    def process_stimulus(self, stimulus_data):
        """Ana uyaran işleme pipeline'ı — tüm beyin bölgeleri koordineli çalışır."""

        # --- Komutlar ---
        cmd = stimulus_data.lower().strip()

        if cmd in ["uyu", "sleep"]:
            return self.sleep()

        if cmd in ["kapat", "exit"]:
            self.maintenance()
            self.dream_engine.stop()
            self._save_state()
            self.inner_world.new_session()
            print("\n[*] İLK kapatılıyor. Görüşmek üzere.")
            sys.exit(0)

        if cmd in ["durum", "status"]:
            return self._get_status()

        if cmd in ["hedefler", "goals"]:
            return self._format_goals()

        if cmd in ["kimim", "kimim ben", "who am i"]:
            identity = self.self_awareness.answer_who_am_i()
            return f"Ben {identity['name']}. {identity['nature']}.\n{identity['self_description']}\nGüçlü yönlerim: {', '.join(identity['strengths'])}\nZayıf yönlerim: {', '.join(identity['weaknesses'])}"

        # --- 0. Enerji Kontrolü ---
        if self.state["energy"] <= 0:
            return "Sistem: Enerji tükendi. Konsolidasyon (uyku) gerekiyor."

        # --- 1. REFLEKS KONTROLÜ (Omurilik seviyesi — en hızlı) ---
        reflex_result = self.reflex.check(stimulus_data, self.state["energy"], self.limbic.current_mood)
        if reflex_result:
            if reflex_result["is_automatic"] and not reflex_result["bypassed_cortex"]:
                # Sosyal reflexler cortex'e de gönderilir
                pass
            elif reflex_result["bypassed_cortex"]:
                # Yüksek öncelikli reflex — cortex'i tamamen atla
                self.state["energy"] -= 1
                self.working_memory.add_exchange(stimulus_data, reflex_result["response"])
                self.inner_world.update_perception(self.state)
                return reflex_result["response"]

        # --- 2. DİL İŞLEME (Wernicke/Broca alanları) ---
        lang_analysis = self.language_processor.analyze(stimulus_data)
        detected_topic = lang_analysis["topic"]

        # --- 3. TALAMUS (Dikkat filtresi) ---
        should_focus, score, _ = self.thalamus.filter_stimulus(stimulus_data, self.state["energy"])
        intensity = self.thalamus.calculate_intensity(stimulus_data)

        # Dil analizi score'u ile birleştir
        if lang_analysis["urgency"] > 0.5:
            score = max(score, lang_analysis["urgency"])
            should_focus = True

        if not should_focus:
            self.working_memory.add_exchange(stimulus_data, "...")
            return "..."

        # --- 4. LİMBİK SİSTEM (Duygu) ---
        tone = lang_analysis.get("emotion", {}).get("type", "nötr")
        current_mood = self.limbic.update_state(tone, self.state["energy"])
        system_instruction = self.limbic.get_system_prompt_modifier()
        self.thalamus.adjust_sensitivity(current_mood)

        # --- 5. DUYGUSAL HAFIZA (Amygdala/Hippocampus) ---
        emotional_context = self.emotional_memory.get_emotional_context(stimulus_data)
        emotional_trigger = self.emotional_memory.check_emotional_trigger(stimulus_data, detected_topic)

        # --- 6. ÇALIŞMA HAFIZASI (Bağlam) ---
        working_context = self.working_memory.get_full_context()
        reference_resolution = self.working_memory.resolve_reference(stimulus_data)

        # --- 7. ÖĞRENME MOTORU (Davranış rehberliği) ---
        behavioral_guidance = self.learning.get_behavioral_guidance(stimulus_data)
        style_hints = self.learning.get_learned_style_hints()

        # --- 8. BİLİNÇALTI FISILDAMASI ---
        subconscious_whisper = ""
        with self.dream_engine._lock:
            if self.dream_engine.insights:
                recent_insight = self.dream_engine.insights.pop()
                subconscious_whisper = f"\n[İçsel Sezgi]: {recent_insight}"

        # --- 9. ÖZ-FARKINDALIK (Meta-biliş) ---
        user_intent = self.self_awareness.guess_user_intent(stimulus_data, lang_analysis)
        self_identity = self.self_awareness.get_self_prompt()

        # --- 10. PREFRONTAL KORTEKS (Karar verme) ---
        options = [
            {"action": "derin_yanıt", "reason": "Detaylı ve analitik düşünce.", "risk": 0.1, "energy_cost": 0.7, "type": "think"},
            {"action": "hızlı_yanıt", "reason": "Kısa ve öz cevap.", "risk": 0.2, "energy_cost": 0.3, "type": "respond"},
            {"action": "öğrenme_odaklı", "reason": "Öğrenme fırsatı yakala.", "risk": 0.1, "energy_cost": 0.5, "type": "explore"},
        ]

        # Dürtü kontrolü
        impulse = self.prefrontal.evaluate_impulse(stimulus_data, "genel", current_mood)
        if impulse["should_delay"] and lang_analysis["urgency"] < 0.5:
            options.append({"action": "bekle_ve_düşün", "reason": "Dürtüsel tepki engellendi, derin düşün.", "risk": 0.0, "energy_cost": 0.1, "type": "rest"})

        decision = self.prefrontal.make_decision(options, stimulus_data, self.state["energy"], current_mood)

        # --- 11. ZEKA KATMANI (Gerçek düşünce) ---
        # Tüm bağlamları birleştir
        full_context = self_identity + "\n\n"
        full_context += f"[Mevcut Durum]: {system_instruction}\n"

        # Prefrontal kararını bağlama ekle
        if decision.get("action") == "hızlı_yanıt":
            full_context += "[Prefrontal Kararı]: Kısa ve öz yanıt ver. Gereksiz detaya girme.]\n"
        elif decision.get("action") == "bekle_ve_düşün":
            full_context += "[Prefrontal Kararı]: Derin düşünce modu. Önce düşün, sonra cevap ver.]\n"
        elif decision.get("action") == "öğrenme_odaklı":
            full_context += "[Prefrontal Kararı]: Öğrenme fırsatı. Bilgiyi yapılandır.]\n"

        if working_context:
            full_context += f"\n{working_context}\n"
        if emotional_context and emotional_context.get("dominant_emotion"):
            full_context += f"\n[Baskın Duygu Durumu]: {emotional_context['dominant_emotion']}\n"
        if emotional_trigger:
            full_context += f"\n[Duygusal Tetikleyici]: {emotional_trigger['recommendation']}\n"
        if reference_resolution:
            for pronoun, referent in reference_resolution.items():
                if not pronoun.endswith("_context"):
                    full_context += f"\n[Referans Çözümü]: '{pronoun}' = {referent}\n"
        if behavioral_guidance:
            full_context += f"\n[Öğrenilmiş Davranış]: {behavioral_guidance['action']} (güven: {behavioral_guidance['confidence']})\n"
        if style_hints:
            full_context += f"\n[Stil İpuçları]: {'; '.join(style_hints[:3])}\n"
        if subconscious_whisper:
            full_context += subconscious_whisper

        if impulse["should_delay"]:
            full_context += "\n[Öz-Denetim Uyarısı]: Bu uyarana dürtüsel tepki verme. Daha derin düşün.]"

        # İlgili anılar
        relevant_memories = self.memory.search_relevant(stimulus_data, limit=3)
        if relevant_memories:
            full_context += "\n[İlgili Geçmiş Deneyimler]:\n"
            for mem in relevant_memories:
                full_context += f"- {mem.get('stimulus', '')[:80]} -> {mem.get('response', '')[:80]}\n"

        thought_output = self.intelligence.query(stimulus_data, full_context)

        # --- 12. EGO (Bilinçli filtreleme) ---
        thought_output = self.ego.filter_thought(stimulus_data, thought_output, {"tone": current_mood})

        # --- 13. HAFIZA KAYDI (Tüm sistemler) ---
        # Uzun/kısa süreli hafıza
        self.memory.store_experience({
            "stimulus": stimulus_data,
            "response": thought_output,
            "mood_state": current_mood,
            "attention_score": score,
            "intensity": intensity,
            "intent": lang_analysis["intent"]["primary"],
            "topic": detected_topic
        }, is_critical=(score > 0.8))

        # Duygusal hafıza
        self.emotional_memory.encode(
            event=stimulus_data,
            emotion_type=lang_analysis["emotion"]["type"],
            intensity=lang_analysis["emotion"]["intensity"],
            valence=lang_analysis["sentiment"],
            context=detected_topic or ""
        )

        # Çalışma hafızası
        self.working_memory.add_exchange(stimulus_data, thought_output, detected_topic)

        # Öğrenme motoru
        outcome = lang_analysis["sentiment"] * 0.5  # Basit outcome hesabı
        self.learning.learn_from_exchange(stimulus_data, thought_output, outcome, detected_topic or "")

        # Kişilik evrimi (nöroplastisite)
        self.ego.evolve_personality(stimulus_data, {"tone": current_mood})

        # --- 14. ENERJİ GÜNCELLEME ---
        energy_cost = 8 * intensity + lang_analysis["complexity"] * 5
        self.state["energy"] -= energy_cost
        if self.state["energy"] <= 0:
            self.state["energy"] = 0
            print("\n[!] Enerji kritik seviyede. Uyku gerekiyor.")

        self.state["last_stimulus"] = stimulus_data

        # İç dünya güncelle
        self.inner_world.update_perception({
            "energy": self.state["energy"],
            "mood": current_mood,
            "emotions": self.limbic.emotional_states
        })

        # Motivasyon düşüşü
        if self.state["energy"] < 30:
            self.goals.decay_motivation(rate=0.02)

        # Periyodik öz-düşünme
        if self.working_memory.turn_count % 10 == 0:
            recent_exps = self.memory.retrieve_memories(limit=5)
            self.self_awareness.reflect(
                [{"stimulus": m["data"].get("stimulus", ""), "topic": m["data"].get("topic")} for m in recent_exps],
                {"energy": self.state["energy"], "emotions": self.limbic.emotional_states}
            )

        return thought_output

    def _get_status(self):
        """Gelişmiş durum raporu."""
        wm = self.working_memory.get_stats()
        lp = self.language_processor.get_stats()
        em = self.emotional_memory.get_stats()
        le = self.learning.get_stats()
        sa = self.self_awareness.get_stats()
        rx = self.reflex.get_stats()
        iw = self.inner_world.get_self_perception()
        gs = self.goals.get_motivation_summary()
        pfc = self.prefrontal.get_stats()
        dream = self.dream_engine.get_dream_report()

        return (
            f"╔══════════════════════════════════════════════╗\n"
            f"║         İLK BEYİN DURUM RAPORU v0.3        ║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ Enerji:          %{self.state['energy']:>5.0f}                    ║\n"
            f"║ Ruh Hali:        {self.limbic.current_mood:<25}║\n"
            f"║ Gelişim:         {self.limbic.development_stage:<25}║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ SOHBET                                   ║\n"
            f"║  Tur:            {wm['turn_count']:<25}║\n"
            f"║  Konu:           {wm['current_topic'] or 'yok':<25}║\n"
            f"║  Referanslar:    {wm['active_references']:<25}║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ DİL İŞLEME                              ║\n"
            f"║  İşlenen:        {lp['processed_count']:<25}║\n"
            f"║  Öğrenilen:      {lp['learned_patterns']:<25}║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ HAFIZA                                   ║\n"
            f"║  Uzun süreli:    {self.memory.get_stats()['long_term']:<25}║\n"
            f"║  Kısa süreli:    {self.memory.get_stats()['short_term']:<25}║\n"
            f"║  Duygusal:       {em['total_memories']:<25}║\n"
            f"║  Flashbulb:      {em['flashbulb_count']:<25}║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ ÖĞRENME                                  ║\n"
            f"║  Ders:           {le['total_lessons']:<25}║\n"
            f"║  Davranış kural:  {le['behavior_rules']:<25}║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ ÖZ-FARKINDALIK                           ║\n"
            f"║  Öz-düşünme:     {sa['total_reflections']:<25}║\n"
            f"║  Güven:          {sa['self_confidence']:<25}║\n"
            f"║  Merak:          {sa['curiosity']:<25}║\n"
            f"║  Bilinen konu:   {sa['known_topics']:<25}║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ PREFRONTAL KORTEKS                      ║\n"
            f"║  Karar:          {pfc['total_decisions']:<25}║\n"
            f"║  Öz-denetim:     {pfc['self_control_score']:<25}║\n"
            f"║  Bilişsel esneklik: {pfc['cognitive_flexibility']:<22}║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ RÜYA / BİLİNÇALTI                       ║\n"
            f"║  Rüya sayısı:    {dream['total_dreams']:<25}║\n"
            f"║  Faz:            {dream['current_phase']:<25}║\n"
            f"║  Bekleyen:       {dream['pending_insights']:<25}║\n"
            f"╠══════════════════════════════════════════════╣\n"
            f"║ OTONOM DAVRANIŞ                         ║\n"
            f"║  Refleks:        {rx['total_reflexes']:<25}║\n"
            f"║  Motivasyon:     {gs['motivation_status']:<25}║\n"
            f"║  Başarı:         {gs['total_achievements']:<25}║\n"
            f"║  İç dünya:       {iw.get('session_duration', '?'):<25}║\n"
            f"╚══════════════════════════════════════════════╝"
        )

    def _format_goals(self):
        gs = self.goals.get_motivation_summary()
        lt = gs["long_term_progress"]
        lines = ["=== HEDEF DURUMU ==="]
        lines.append(f"Motivasyon: {gs['motivation_status']} ({gs['motivation_level']})")
        lines.append(f"Aktif kısa vadeli: {gs['active_short_term']}")
        lines.append(f"Tamamlanan: {gs['completed_short_term']}")
        lines.append(f"Toplam başarı: {gs['total_achievements']}")
        lines.append("\nUzun vadeli:")
        for goal, progress in lt.items():
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            lines.append(f"  {goal}: {bar} %{progress}")
        return "\n".join(lines)

    def sleep(self):
        """Gelişmiş uyku evresi."""
        print("\n[*] Beyin uyku moduna (REM) geçiyor...")

        # Hafıza konsolidasyonu
        consolidated, forgotten = self.memory.consolidate_memories(threshold=0.4)

        # Duygusal adaptasyon
        self.emotional_memory.decay(rate=0.03)

        # Enerji yenileme
        self.state["energy"] = 100
        self.state["session_count"] = self.state.get("session_count", 0) + 1

        # Öz-düşünme
        recent_exps = self.memory.retrieve_memories(limit=10)
        self.self_awareness.reflect(
            [{"stimulus": m["data"].get("stimulus", ""), "topic": m["data"].get("topic")} for m in recent_exps],
            {"energy": 100, "emotions": self.limbic.emotional_states}
        )

        # Uzun vadeli hedef ilerlemesi
        self.goals.update_long_term_progress("Öğrenme ve gelişim", 0.02)
        self.goals.update_long_term_progress("Kullanıcıya yardımcı olmak", 0.01)

        # Durumu kaydet
        self._save_state()
        self.inner_world.new_session()

        # Rüya raporu
        dream_report = self.dream_engine.get_dream_report()
        insight_msg = ""
        if dream_report.get("recent_dream"):
            insight_msg = f"\n[Rüya]: {dream_report['recent_dream']['content'][:100]}..."

        return (
            f"Beyin tazelendi. {consolidated} anı pekiştirildi, {forgotten} veri temizlendi."
            f"{insight_msg}\nEnerji: %100 | Oturum: #{self.state['session_count']}"
        )

    def maintenance(self):
        """Otomatik bakım."""
        if hasattr(self, 'memory'):
            self.memory.apply_neuroplasticity(decay_rate=0.02)
        if hasattr(self, 'state'):
            self._save_state()
        if hasattr(self, 'goals'):
            self.goals.decay_motivation(rate=0.005)
        if hasattr(self, 'subconscious'):
            self.subconscious.stop()


if __name__ == "__main__":
    brain = ArtificialBrain()

    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"\n[*] İLK v0.3 aktif.")
    print("[*] Komutlar: 'uyu' | 'kapat' | 'durum' | 'hedefler' | 'kimim'")

    while True:
        try:
            user_input = input("\nSen > ")
            if not user_input: continue

            print("İLK düşünüyor...", end="\r")
            yanit = brain.process_stimulus(user_input)
            print(f"\n🧠 İLK: {yanit}")

        except (EOFError, KeyboardInterrupt):
            continue
