
"""Test: Hafıza sistemi - bağlamsal arama ve konsolidasyon."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.memory import MemoryGateway
import tempfile
import shutil


def test_memory():
    print("=" * 50)
    print("  Hafıza Sistemi Testi")
    print("=" * 50)

    # Geçici bir klasörde test yap
    test_dir = tempfile.mkdtemp()
    try:
        memory = MemoryGateway(storage_path=test_dir)

        # 1. Deneyim kaydet
        print("\n[*] Deneyimler kaydediliyor...")
        memory.store_experience({
            "stimulus": "Python nedir?",
            "response": "Python yüksek seviyeli bir programlama dilidir.",
            "mood_state": "analytical"
        }, is_critical=True)

        memory.store_experience({
            "stimulus": "JavaScript frameworkleri",
            "response": "React, Vue, Angular popüler frameworklerdir.",
            "mood_state": "balanced"
        }, is_critical=True)

        memory.store_experience({
            "stimulus": "Yapay zeka nedir?",
            "response": "Yapay zeka, makinelerin insan gibi düşünmesini sağlar.",
            "mood_state": "analytical"
        }, is_critical=True)

        # Kısa süreli hafızaya da bir şey kaydet
        memory.store_experience({
            "stimulus": "Merhaba",
            "response": "Selam!",
            "mood_state": "balanced"
        }, is_critical=False)

        # 2. İstatistikler
        stats = memory.get_stats()
        print(f"[OK] İstatistikler: {stats}")
        assert stats["long_term"] == 3, f"Uzun süreli hafıza 3 olmalı, {stats['long_term']}"
        assert stats["short_term"] == 1, f"Kısa süreli hafıza 1 olmalı, {stats['short_term']}"

        # 3. Bağlamsal arama
        print("\n[*] Bağlamsal arama test ediliyor...")
        results = memory.search_relevant("Python programlama", limit=2)
        print(f"[OK] 'Python programlama' araması: {len(results)} sonuç")
        assert len(results) > 0, "Arama sonucu boş olmamalı"

        # İlk sonucun Python ile ilgili olması gerekir
        first = results[0]
        print(f"    En iyi eşleşme: '{first['stimulus']}' (skor: {first['score']:.2f})")
        assert "python" in first["stimulus"].lower(), "İlk sonuç Python ile ilgili olmalı"

        # 4. Nöroplastisite
        print("\n[*] Nöroplastisite uygulanıyor...")
        memory.apply_neuroplasticity(decay_rate=0.5)
        memories = memory.retrieve_memories(limit=10)
        all_decayed = all(m["metadata"]["weight"] < 1.0 for m in memories)
        print(f"[OK] Ağırlıklar azaldı: {[m['metadata']['weight'] for m in memories]}")
        assert all_decayed, "Tüm ağırlıklar azalmalı"

        # 5. Konsolidasyon
        print("\n[*] Konsolidasyon test ediliyor...")
        # Kısa süreli hafızaya düşük ağırlıklı veri ekle
        memory.store_experience({"stimulus": "gecici"}, is_critical=False)
        memory.apply_neuroplasticity(decay_rate=1.5)  # Ağırlığı sıfırla

        consolidated, forgotten = memory.consolidate_memories(threshold=0.4)
        print(f"[OK] Konsolidasyon: {consolidated} pekiştirildi, {forgotten} unutuldu")

        # Son kontrol
        final_stats = memory.get_stats()
        print(f"\n[OK] Son durum: {final_stats}")
        # Konsolidasyon sonrası kısa süreli temizlenmeli
        assert final_stats["short_term"] == 0, f"Kısa süreli hafıza 0 olmalı, {final_stats['short_term']}"

        print("\n" + "=" * 50)
        print("  SONUÇ: Tüm hafıza testleri başarılı!")
        print("=" * 50)

    finally:
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    test_memory()
