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
    def __init__(self, settings_path=None):
        # Dinamik yol: proje kökünden ayarla
        if settings_path is None:
            settings_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage", "brain_state.json"
            )

        self.settings_path = settings_path
        self.brain_active = True
        self.memory = MemoryGateway()
        self.intelligence = IntelligenceLayer()
        self.limbic = LimbicSystem()
        self.thalamus = Thalamus()
        self.ego = CyberEgo()
        self.subconscious = Subconscious(self.memory, self.intelligence)

        # Önceki durumu dosyadan yükle (varsa)
        self.state = self._load_state()

        # Sinyal koruması (CTRL+C direnci)
        signal.signal(signal.SIGINT, self._handle_exit_attempt)
        atexit.register(self.maintenance)

    def _load_state(self):
        """Beyin durumunu dosyadan yükler."""
        default_state = {
            "energy": 100,
            "last_stimulus": None,
            "development_stage": self.limbic.development_stage,
            "session_count": 0
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
        """Beyin durumunu kalıcı olarak kaydeder."""
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)

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
            self._save_state()
            print("\n[*] İLK kapatılıyor. Görüşmek üzere.")
            sys.exit(0)

        if stimulus_data.lower() in ["durum", "status"]:
            return self._get_status()

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

        # Talamus hassasiyetini ruh haline göre ayarla
        self.thalamus.adjust_sensitivity(current_mood)

        # 2.5 Aşama: Bilinçaltı fısıltısı (Sezgi Entegrasyonu)
        subconscious_whisper = ""
        if self.subconscious.insights:
            # En son içgörüyü al ve bilince "fısılda"
            recent_insight = self.subconscious.insights.pop()
            subconscious_whisper = f"\n[İçsel Sezgi/Fısıltı]: {recent_insight}"

        # İlgili anıları bağlam olarak ekle (RAG benzeri)
        relevant_memories = self.memory.search_relevant(stimulus_data, limit=3)
        memory_context = ""
        if relevant_memories:
            memory_context = "\n[Önceki İlgili Deneyimler]:\n"
            for mem in relevant_memories:
                memory_context += f"- {mem.get('stimulus', '???')} -> {mem.get('response', '???')[:100]}\n"

        # 3. Aşama: Ego Gelişimi (Nöroplastisite)
        self.ego.evolve_personality(stimulus_data, {"tone": current_mood})

        # 4. Aşama: Zeka (Gerçek Düşünce - Sezgi ve Hafıza Desteğiyle)
        full_context = system_instruction + subconscious_whisper + memory_context
        thought_output = self.intelligence.query(stimulus_data, full_context)

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

        # Son uyarıcıyı kaydet
        self.state["last_stimulus"] = stimulus_data

        # 7. Aşama: Enerji Güncelleme (Şiddete göre dinamik)
        energy_cost = 10 * intensity
        self.state["energy"] -= energy_cost
        if self.state["energy"] <= 0:
            self.state["energy"] = 0
            print("\n[!] Uyarı: Enerji kritik seviyede. Beyin konsolidasyon moduna girmeli.")

        return thought_output

    def _get_status(self):
        """Beynin mevcut durumunu raporlar."""
        personality = self.ego.get_personality_summary()
        mood = self.limbic.current_mood
        emotions = self.limbic.emotional_states

        stats = self.memory.get_stats()

        return (
            f"=== BEYİN DURUMU ===\n"
            f"Enerji: %{self.state['energy']:.0f}\n"
            f"Ruh Hali: {mood}\n"
            f"Gelişim Evresi: {self.limbic.development_stage}\n"
            f"Duygusal Eksenler: {json.dumps(emotions, ensure_ascii=False)}\n"
            f"Kişilik Özellikleri: {json.dumps(personality, ensure_ascii=False)}\n"
            f"Hafıza: {stats['long_term']} uzun süreli, {stats['short_term']} kısa süreli\n"
            f"Bilinçaltı İçgörü: {'Var' if self.subconscious.insights else 'Yok'}\n"
            f"==================="
        )

    def sleep(self):
        """Uyku evresi: Hafıza konsolidasyonu ve enerji yenileme."""
        print("\n[*] Beyin uyku moduna (REM) geçiyor...")
        print("[*] Sinapslar temizleniyor, önemli anılar kalıcı belleğe taşınıyor...")

        # Hafıza konsolidasyonu
        consolidated, forgotten = self.memory.consolidate_memories(threshold=0.4)

        # Enerji yenileme
        self.state["energy"] = 100
        self.state["session_count"] = self.state.get("session_count", 0) + 1

        # Durumu kaydet
        self._save_state()

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
        if hasattr(self, 'state'):
            self._save_state()

if __name__ == "__main__":
    # Temiz Başlatma
    brain = ArtificialBrain()

    # Terminali temizle
    os.system('cls' if os.name == 'nt' else 'clear')

    # Sadece sade bir giriş
    print(f"\n[*] İLK aktif. Seninle iletişim kurmaya hazır.")
    print("[*] Çıkış: 'kapat' | Uyku: 'uyu' | Durum: 'durum'")

    while True:
        try:
            user_input = input("\nSen > ")
            if not user_input: continue

            print("İLK düşünüyor...", end="\r")
            yanit = brain.process_stimulus(user_input)
            print(f"\n🧠 İLK: {yanit}")

        except (EOFError, KeyboardInterrupt):
            continue
