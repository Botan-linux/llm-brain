
"""Test: Tüm v0.3 modüllerinin entegrasyon testi."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.prefrontal import PrefrontalCortex
from core.working_memory import WorkingMemory
from core.language_processor import LanguageProcessor
from core.emotional_memory import EmotionalMemory
from core.learning import LearningEngine
from core.self_awareness import SelfAwareness
from core.reflex import ReflexSystem, InnerWorldModel, GoalSystem
from core.memory import MemoryGateway
from core.limbic import LimbicSystem
from core.thalamus import Thalamus
from core.ego import CyberEgo
from core.intelligence import IntelligenceLayer


def test_all_v1_modules():
    print("=" * 60)
    print("  LLM-Brain v0.3 — Tüm Modüller Entegrasyon Testi")
    print("=" * 60)

    errors = []
    tests_passed = 0

    # 1. Prefrontal Cortex
    try:
        pfc = PrefrontalCortex()
        options = [
            {"action": "think", "reason": "Think deep", "risk": 0.1, "energy_cost": 0.6, "type": "think"},
            {"action": "respond", "reason": "Quick response", "risk": 0.3, "energy_cost": 0.3, "type": "respond"},
        ]
        decision = pfc.make_decision(options, "Test context", 80, "analytical")
        impulse = pfc.evaluate_impulse("HAYIR!", "test", "defensive")
        plan = pfc.create_plan("Test goal", [{"action": "step1"}, {"action": "step2"}])
        assert decision["action"] in ["think", "respond"]
        assert impulse["is_impulsive"] == True
        print(f"  [OK] PrefrontalCortex: decision={decision['action']}, impulse={impulse['is_impulsive']}, plan created")
        tests_passed += 1
    except Exception as e:
        errors.append(f"PrefrontalCortex: {e}")
        print(f"  [HATA] PrefrontalCortex: {e}")

    # 2. Working Memory
    try:
        wm = WorkingMemory()
        wm.add_exchange("Merhaba", "Selam!", "günlük")
        wm.add_exchange("Python nedir?", "Programlama dili.", "programlama")
        wm.add_exchange("Bunu açıklar mısın?", "Tabii, Python...", "programlama")
        context = wm.get_context_window()
        refs = wm.resolve_reference("Bunu detaylandır")
        assert len(wm.conversation) == 3
        assert wm.current_topic == "programlama"
        print(f"  [OK] WorkingMemory: turns={wm.turn_count}, topic={wm.current_topic}, refs={refs}")
        tests_passed += 1
    except Exception as e:
        errors.append(f"WorkingMemory: {e}")
        print(f"  [HATA] WorkingMemory: {e}")

    # 3. Language Processor
    try:
        lp = LanguageProcessor()
        r1 = lp.analyze("Python fonksiyonları nasıl çalışır?")
        r2 = lp.analyze("Bunu hemen açıklar mısın!")
        r3 = lp.analyze("Çok mutluyum bugün")
        assert "soru" in r1["intent"]["primary"] or "öğrenme" in r1["intent"]["primary"]
        assert r3["emotion"]["type"] == "pozitif"
        assert r2["urgency"] > 0
        print(f"  [OK] LanguageProcessor: question={r1['intent']['primary']}, emotion={r3['emotion']['type']}, urgent={r2['urgency']}")
        tests_passed += 1
    except Exception as e:
        errors.append(f"LanguageProcessor: {e}")
        print(f"  [HATA] LanguageProcessor: {e}")

    # 4. Emotional Memory
    try:
        em = EmotionalMemory()
        em.encode("Harika gün!", "pozitif", 0.9, 0.95, "günlük")
        em.encode("Korkunç bir rüya", "negatif", 0.8, -0.8, "rüya")
        em.encode("Kod çalışmadı", "negatif", 0.5, -0.5, "programlama")
        trigger = em.check_emotional_trigger("kod çalışmadı gene")
        flash = em.get_flashbulb_memories()
        assert len(flash) >= 1  # Harika gün flashbulb olmalı
        print(f"  [OK] EmotionalMemory: memories={em.get_stats()['total_memories']}, flashbulb={len(flash)}, trigger={trigger is not None}")
        tests_passed += 1
    except Exception as e:
        errors.append(f"EmotionalMemory: {e}")
        print(f"  [HATA] EmotionalMemory: {e}")

    # 5. Learning Engine
    try:
        le = LearningEngine()
        le.learn_from_exchange("Merhaba!", "Merhaba!", 0.8)
        le.learn_from_exchange("Python nedir?", "Bir dil...", 0.6)
        le.learn_from_exchange("Kötü cevap", "Üzgünüm...", -0.7)
        guidance = le.get_behavioral_guidance("Merhaba!")
        hints = le.get_learned_style_hints()
        assert guidance is not None or le.total_lessons >= 3
        print(f"  [OK] LearningEngine: lessons={le.total_lessons}, rules={le.get_stats()['behavior_rules']}")
        tests_passed += 1
    except Exception as e:
        errors.append(f"LearningEngine: {e}")
        print(f"  [HATA] LearningEngine: {e}")

    # 6. Self-Awareness
    try:
        sa = SelfAwareness()
        sa.reflect([{"stimulus": "test", "topic": "felsefe"}], {"energy": 80, "emotions": {}})
        identity = sa.answer_who_am_i()
        prompt = sa.get_self_prompt()
        assert identity["name"] == "İLK"
        assert len(prompt) > 50
        print(f"  [OK] SelfAwareness: reflections={sa.total_reflections}, identity={identity['name']}")
        tests_passed += 1
    except Exception as e:
        errors.append(f"SelfAwareness: {e}")
        print(f"  [HATA] SelfAwareness: {e}")

    # 7. Reflex System
    try:
        rx = ReflexSystem()
        r1 = rx.check("Merhaba!", 80, "balanced")
        r2 = rx.check("Kim sin sen?", 60, "analytical")
        r3 = rx.check("Python nedir?", 80, "balanced")
        assert r1 is not None and r1["reflex_type"] == "selamlama"
        assert r2 is not None and r2["reflex_type"] == "kimlik_sorgusu"
        assert r3 is None  # Normal soru = refleks yok
        print(f"  [OK] ReflexSystem: selamlama={r1 is not None}, kimlik={r2 is not None}, normal={r3 is None}")
        tests_passed += 1
    except Exception as e:
        errors.append(f"ReflexSystem: {e}")
        print(f"  [HATA] ReflexSystem: {e}")

    # 8. Inner World Model
    try:
        iw = InnerWorldModel()
        iw.update_perception({"energy": 90, "mood": "balanced", "emotions": {}})
        iw.update_perception({"energy": 50, "mood": "analytical", "emotions": {}})
        perception = iw.get_self_perception()
        limits = iw.get_limits()
        assert "avg_energy" in perception
        assert limits["can_learn"] == True
        print(f"  [OK] InnerWorldModel: energy={perception['avg_energy']}, trend={perception['energy_trend']}")
        tests_passed += 1
    except Exception as e:
        errors.append(f"InnerWorldModel: {e}")
        print(f"  [HATA] InnerWorldModel: {e}")

    # 9. Goal System
    try:
        gs = GoalSystem()
        gs.set_short_term_goal("Test goal")
        gs.complete_short_term_goal("Test goal")
        gs.update_long_term_progress("Öğrenme ve gelişim", 0.1)
        motivation = gs.get_motivation_summary()
        assert motivation["completed_short_term"] >= 1
        print(f"  [OK] GoalSystem: completed={motivation['completed_short_term']}, motivation={motivation['motivation_status']}")
        tests_passed += 1
    except Exception as e:
        errors.append(f"GoalSystem: {e}")
        print(f"  [HATA] GoalSystem: {e}")

    # Özet
    print("\n" + "=" * 60)
    total = tests_passed + len(errors)
    if errors:
        print(f"  SONUÇ: {tests_passed}/{total} test başarılı, {len(errors)} hata")
        for err in errors:
            print(f"  ✗ {err}")
    else:
        print(f"  SONUÇ: Tüm {total} modül başarıyla çalışıyor!")
    print("=" * 60)


if __name__ == "__main__":
    test_all_v1_modules()
