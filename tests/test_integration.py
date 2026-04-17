
"""Test: Beyin durumu raporu ve tüm modüllerin entegrasyon kontrolü."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory import MemoryGateway
from core.limbic import LimbicSystem
from core.thalamus import Thalamus
from core.ego import CyberEgo
from core.intelligence import IntelligenceLayer
from core.subconscious import Subconscious


def test_all_modules():
    """Tüm modüllerin başlatılmasını ve temel fonksiyonlarını test eder."""
    print("=" * 50)
    print("  LLM-Brain Modül Entegrasyon Testi")
    print("=" * 50)

    errors = []

    # 1. Memory Gateway
    try:
        memory = MemoryGateway()
        memory.store_experience({"test": "deneme"}, is_critical=True)
        stats = memory.get_stats()
        print(f"\n[OK] Memory Gateway: {stats}")
    except Exception as e:
        errors.append(f"Memory Gateway: {e}")
        print(f"\n[HATA] Memory Gateway: {e}")

    # 2. Limbic System
    try:
        limbic = LimbicSystem()
        mood = limbic.update_state("normal", 80)
        params = limbic.get_model_params()
        print(f"[OK] Limbic System: mood={mood}, params={params}")
    except Exception as e:
        errors.append(f"Limbic System: {e}")
        print(f"[HATA] Limbic System: {e}")

    # 3. Thalamus
    try:
        thalamus = Thalamus()
        focus, score, status = thalamus.filter_stimulus("Merhaba dünya!", 100)
        intensity = thalamus.calculate_intensity("MERHABA DÜNYA!")
        tstats = thalamus.get_stats()
        print(f"[OK] Thalamus: focus={focus}, score={score}, intensity={intensity}, stats={tstats}")
    except Exception as e:
        errors.append(f"Thalamus: {e}")
        print(f"[HATA] Thalamus: {e}")

    # 4. Ego
    try:
        ego = CyberEgo()
        ego.evolve_personality("Bu çok karmaşık bir soru mu?", {"tone": "analytical"})
        personality = ego.get_personality_summary()
        thought = ego.filter_thought("test", "Merhaba dünya!", {"tone": "balanced"})
        print(f"[OK] CyberEgo: personality={personality}")
    except Exception as e:
        errors.append(f"CyberEgo: {e}")
        print(f"[HATA] CyberEgo: {e}")

    # 5. Intelligence Layer
    try:
        intel = IntelligenceLayer()
        istats = intel.get_stats()
        print(f"[OK] Intelligence Layer: stats={istats}")
    except Exception as e:
        errors.append(f"Intelligence Layer: {e}")
        print(f"[HATA] Intelligence Layer: {e}")

    # 6. Subconscious (başlat, hemen durdur)
    try:
        sub = Subconscious(memory, intel, interval_range=(60, 120))
        sub.stop()
        print(f"[OK] Subconscious: started and stopped")
    except Exception as e:
        errors.append(f"Subconscious: {e}")
        print(f"[HATA] Subconscious: {e}")

    # Özet
    print("\n" + "=" * 50)
    if errors:
        print(f"  SONUÇ: {len(errors)} HATA bulundu")
        for err in errors:
            print(f"  - {err}")
    else:
        print("  SONUÇ: Tüm modüller başarıyla çalışıyor!")
    print("=" * 50)


if __name__ == "__main__":
    test_all_modules()
