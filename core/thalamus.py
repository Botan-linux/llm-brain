import re

class Thalamus:
    def __init__(self):
        # Önemli anahtar kelimeler ve öncelik seviyeleri (Bilişsel ve Biyolojik)
        self.priority_keywords = {
            "merak": 0.8,
            "öğrenme": 0.7,
            "tehlike": 0.9,
            "acı": 1.0,      # Negatif geri bildirim en yüksek öncelik
            "ödül": 0.8,     # Pozitif pekiştirme
            "p4antom": 1.0,  # Yaratıcı her zaman en üst öncelik
            "botan": 1.0,    # Yaratıcı her zaman en üst öncelik
            "uyu": 1.0,
            "sleep": 1.0,
            "kimim": 0.9,    # Öz-farkındalık sorguları
            "yardım": 0.7,
            "nasıl": 0.6,
            "neden": 0.6,
            "ne": 0.4,
        }
        self.attention_threshold = 0.3 # Bu eşiğin altındaki uyaranlar 'gürültü' kabul edilir
        self._total_filtered = 0
        self._total_passed = 0

    def calculate_intensity(self, stimulus_data):
        """Uyarının şiddetini analiz eder."""
        intensity = 1.0
        if stimulus_data.isupper(): intensity += 0.5  # Bağırarak konuşma
        if "!" in stimulus_data: intensity += 0.3      # Heyecan/Önem
        if len(stimulus_data) > 100: intensity += 0.2 # Karmaşıklık
        if len(stimulus_data) > 300: intensity += 0.3 # Çok karmaşık
        # Birden fazla soru işareti
        if stimulus_data.count("?") > 1: intensity += 0.2
        return min(2.5, intensity)

    def filter_stimulus(self, stimulus_data, current_energy):
        """Uyaranın önemini analiz eder ve odaklanıp odaklanmayacağına karar verir."""

        # 1. Ham metin analizi (Basit gürültü filtresi)
        if len(stimulus_data.strip()) < 2:
            self._total_filtered += 1
            return False, 0.0, "Gürültü: Çok kısa uyaran."

        # Tekrar kontrolü (aynı uyaran ardışık gelirse)
        if hasattr(self, '_last_stimulus') and stimulus_data.strip() == self._last_stimulus:
            self._total_filtered += 1
            return False, 0.0, "Gürültü: Tekrar eden uyaran."
        self._last_stimulus = stimulus_data.strip()

        # 2. Öncelik skoru hesaplama
        score = 0.5 # Varsayılan skor (Nötr)

        # Enerji analizi: Enerji kritik seviyenin (20) altındaysa beyin koruma moduna girer
        is_low_energy = current_energy < 20

        # Enerji düşükse beyin daha seçici olur — ama insanda bile %50'ye kadar çalışır
        # Eski formül: +(1.0 - energy/100) * 0.4 → %40'da threshold 0.54'e çıkıyordu (çok agresif)
        # Yeni formül: +(1.0 - energy/100) * 0.15 → %40'da threshold 0.39 (insan benzeri)
        effective_threshold = self.attention_threshold + (1.0 - (current_energy / 100.0)) * 0.15

        # Kritik komutları kontrol et
        stimulus_lower = stimulus_data.lower()
        for word, weight in self.priority_keywords.items():
            if word in stimulus_lower:
                score = max(score, weight)

        # Uzunluk skoru ekle
        word_count = len(stimulus_data.split())
        if word_count > 5:
            score += 0.05
        if word_count > 10:
            score += 0.1
        if word_count > 20:
            score += 0.1

        # Soru işareti olan girdiler her zaman dikkati çeker
        if "?" in stimulus_data:
            score = max(score, 0.55)

        # 3. Sonuç: Odaklanmalı mıyız?
        should_focus = score >= effective_threshold

        # Sadece KRİTİK enerji (< 15) ve düşük öncelikli uyaranlar filtrelenir
        # İnsan bile çok yorgunken selamlayabilir, soru sorabilir
        if is_low_energy and not any(k in stimulus_lower for k in ["p4antom", "botan", "uyu", "sleep", "kritik"]):
            if score < 0.7:
                self._total_filtered += 1
                return False, score, "Enerji Koruma: Sadece önemli uyaranlara odaklanılıyor."

        if should_focus:
            self._total_passed += 1
        else:
            self._total_filtered += 1

        status = "Odaklanıldı" if should_focus else "Göz ardı edildi (Düşük Önem/Düşük Enerji)"
        return should_focus, score, status

    def adjust_sensitivity(self, mood):
        """Ruh haline göre Talamus'un hassasiyetini değiştirir."""
        if mood == "analytical":
            self.attention_threshold = 0.4 # Daha seçici
        elif mood == "defensive":
            self.attention_threshold = 0.2 # Her şeye karşı tetikte
        elif mood == "curious":
            self.attention_threshold = 0.2 # Meraklı, her şeye açık
        elif mood == "exhausted":
            self.attention_threshold = 0.6 # Çoğu şeyi göz ardı eder
        else:
            self.attention_threshold = 0.3 # Normal seyrinde

    def get_stats(self):
        """Talamus istatistiklerini döndürür."""
        total = self._total_passed + self._total_filtered
        return {
            "total_stimuli": total,
            "passed": self._total_passed,
            "filtered": self._total_filtered,
            "pass_rate": (self._total_passed / total * 100) if total > 0 else 0,
            "current_threshold": self.attention_threshold
        }
