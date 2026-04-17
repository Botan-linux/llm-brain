"""
Memory Bank Senkronizasyon Modülü

Her oturum sonunda memory-bank dosyalarını otomatik günceller.
CLAUDE.md protokolü için gerekli olan activeContext ve progress dosyalarını
beyin durumuna göre otomatik oluşturur.
"""

import json
import os
from datetime import datetime
from core.logger import get_logger

logger = get_logger(__name__)


class MemoryBankSync:
    """
    Memory Bank Otomatik Senkronizasyon.

    İLK'in durumunu CLAUDE.md protokolü için okunabilir formatta saklar.
    Her oturum sonunda / session değişiminde çalışır.
    """

    def __init__(self, brain_instance=None):
        self.brain = brain_instance
        self.memory_bank_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "memory-bank"
        )

    def sync_all(self):
        """Tüm memory-bank dosyalarını güncelle."""
        if not self.brain:
            logger.warning("MemoryBankSync: Beyin instance bağlantısı yok.")
            return

        try:
            self._update_active_context()
            self._update_progress()
            logger.info("Memory Bank senkronizasyonu tamamlandı.")
        except Exception as e:
            logger.error(f"Memory Bank senkronizasyon hatası: {e}")

    def _update_active_context(self):
        """activeContext.md — Mevcut bağlam ve aktif durum."""
        state = self.brain.state
        limbic = self.brain.limbic
        prefrontal = self.brain.prefrontal
        goals = self.brain.goals

        content = f"""# Aktif Bağlam — {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Mevcut Durum
- **Enerji:** %{state.get('energy', 0):.0f}
- **Ruh Hali:** {limbic.current_mood}
- **Oturum:** #{state.get('session_count', 0)}
- **Son Uyaran:** {state.get('last_stimulus', 'Yok')[:100]}

## Duygusal Durum
"""
        for emotion, value in limbic.emotional_states.items():
            bar = "█" * int(value * 10) + "░" * (10 - int(value * 10))
            content += f"- {emotion}: {bar} {value:.2f}\n"

        content += f"""
## Prefrontal Korteks
- **Toplam Karar:** {prefrontal.total_decisions}
- **Bilişsel Esneklik:** {prefrontal.cognitive_flexibility:.2f}
- **Öz-Denetim:** {prefrontal.self_control_score:.2f}

## Aktif Hedefler
- **Motivasyon:** {goals.get_motivation_summary().get('motivation_status', '?')}
- **Başarı:** {goals.get_motivation_summary().get('total_achievements', 0)}
"""

        filepath = os.path.join(self.memory_bank_path, "activeContext.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _update_progress(self):
        """progress.md — Proje gelişim logu."""
        filepath = os.path.join(self.memory_bank_path, "progress.md")

        # Mevcut içeriği oku (varsa)
        existing = ""
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    existing = f.read()
            except Exception:
                pass

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        new_entry = f"\n### {timestamp}\n"
        new_entry += f"- Enerji: %{self.brain.state.get('energy', 0):.0f}\n"
        new_entry += f"- Ruh Hali: {self.brain.limbic.current_mood}\n"
        new_entry += f"- Oturum: #{self.brain.state.get('session_count', 0)}\n"

        # Yeni modüller varsa
        new_entry += f"- Modüller: 18 aktif (Thalamus, Limbic, Prefrontal, Creativity, Social Cognition dahil)\n"
        new_entry += f"- Sürüm: 0.4.0-dev\n"

        content = existing.rstrip() + "\n" + new_entry

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
