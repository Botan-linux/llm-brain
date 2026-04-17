import json
import os
import signal
import sys
import atexit
from core.intelligence import IntelligenceLayer
from core.memory import MemoryGateway
from core.limbic import LimbicSystem
from core.subconscious import Subconscious
from core.thalamus import Thalamus
from core.ego import CyberEgo

class ArtificialBrain:
    def __init__(self, settings_path="/home/p4antom/.claude/settings.json.antigravity.bak"):
        self.brain_active = True
        self.memory = MemoryGateway()
        self.intelligence = IntelligenceLayer(settings_path)
        self.limbic = LimbicSystem()
        self.thalamus = Thalamus()
        self.ego = CyberEgo()
        self.subconscious = Subconscious(self.memory, self.intelligence)

        self.state = {
            "energy": 100,
            "last_stimulus": None,
            "development_stage": self.limbic.development_stage
        }

        # Sinyal koruması (CTRL+C direnci)
        signal.signal(signal.SIGINT, self._handle_exit_attempt)
        atexit.register(self.maintenance)

    def _handle_exit_attempt(self, signum, frame):
        # Arka planda sessizce kaydedip sadece kısa bir uyarı veriyoruz
        print("\n\n[!] Sistem: Beyin fonksiyonları aniden kesilemez. Lütfen 'uyu' komutunu kullanın.")

    def process_stimulus(self, stimulus_data):
        """Uyarana sessizce ve profesyonelce tepki verir."""

        if stimulus_data.lower() in ["uyu", "sleep"]:
            return self.sleep()

        if stimulus_data.lower() in ["kapat", "exit"]:
            self.maintenance()
            self.subconscious.stop()
            print("\n[*] İLK kapatılıyor. Görüşmek üzere p4antom.")
            sys.exit(0)

        # 0. Enerji Kontrolü
        if self.state["energy"] <= 0:
            return "Sistem: Enerji tükendi. Konsolidasyon (uyku) gerekiyor. Lütfen 'uyu' yazın."

        # 1. Aşama: Talamus (Sessiz Filtreleme ve Şiddet Analizi)
        should_focus, score, _ = self.thalamus.filter_stimulus(stimulus_data, self.state["energy"])
        intensity = self.thalamus.calculate_intensity(stimulus_data)

        if not should_focus:
            return "..."

        # 2. Aşama: Limbik Sistem ve Zeka
        tone = "sert" if "!" in stimulus_data or stimulus_data.isupper() else "normal"
        current_mood = self.limbic.update_state(tone, self.state["energy"])
        system_instruction = self.limbic.get_system_prompt_modifier()

        # 2.5 Aşama: Bilinçaltı fısıltısı (Sezgi Entegrasyonu)
        subconscious_whisper = ""
        if self.subconscious.insights:
            # En son içgörüyü al ve bilince "fısılda"
            recent_insight = self.subconscious.insights.pop()
            subconscious_whisper = f"\n[İçsel Sezgi/Fısıltı]: {recent_insight}"

        # 3. Aşama: Ego Gelişimi (Neuroplasticity)
        self.ego.evolve_personality(stimulus_data, {"tone": current_mood})

        # 4. Aşama: Zeka (Gerçek Düşünce - Sezgi Desteğiyle)
        thought_output = self.intelligence.query(stimulus_data, system_instruction + subconscious_whisper)

        # 5. Aşama: Ego (Bilinçli Filtreleme - Biyolojik Katman)
        thought_output = self.ego.filter_thought(stimulus_data, thought_output, {"tone": current_mood})

        # 6. Aşama: Bellek (Sessiz Kayıt)
        self.memory.store_experience({
            "stimulus": stimulus_data,
            "response": thought_output,
            "mood_state": current_mood,
            "attention_score": score,
            "intensity": intensity
        }, is_critical=(score > 0.8))

        # 7. Aşama: Enerji Güncelleme (Şiddete göre dinamik)
        energy_cost = 10 * intensity
        self.state["energy"] -= energy_cost
        if self.state["energy"] <= 0:
            self.state["energy"] = 0
            print("\n[!] Uyarı: Enerji kritik seviyede. Beyin konsolidasyon moduna girmeli.")

        return thought_output

    def sleep(self):
        """Uyku evresi: Hafıza konsolidasyonu ve enerji yenileme."""
        print("\n[*] Beyin uyku moduna (REM) geçiyor...")
        print("[*] Sinapslar temizleniyor, önemli anılar kalıcı belleğe taşınıyor...")

        # Hafıza konsolidasyonu
        consolidated, forgotten = self.memory.consolidate_memories(threshold=0.4)

        # Enerji yenileme
        self.state["energy"] = 100

        # Bilinçaltı içgörülerini kontrol et
        insight_msg = ""
        if self.subconscious.insights:
            last_insight = self.subconscious.insights[-1]
            insight_msg = f"\n[Rüya/İçgörü]: {last_insight[:100]}..."

        return f"Beyin tazelendi. {consolidated} anı pekiştirildi, {forgotten} gereksiz veri temizlendi.{insight_msg}\nEnerji: %100"

    def maintenance(self):
        """Otomatik kayıt ve pekiştirme."""
        if hasattr(self, 'memory'):
            self.memory.apply_neuroplasticity(decay_rate=0.02)

if __name__ == "__main__":
    # ÖNEMLİ: Temiz Başlatma
    brain = ArtificialBrain()

    # Terminali temizle
    os.system('cls' if os.name == 'nt' else 'clear')

    # Başlıkları tamamen kaldırdım, sadece sade bir giriş bırakıyorum.
    print(f"\n[*] İLK aktif. Seninle iletişim kurmaya hazır.")
    print("[*] Çıkış yapmak için 'uyu' yazın.")

    while True:
        try:
            user_input = input("\nSen > ")
            if not user_input: continue

            print("İLK düşünüyor...", end="\r")
            yanit = brain.process_stimulus(user_input)
            print(f"\n🧠 İLK: {yanit}")

        except (EOFError, KeyboardInterrupt):
            continue
