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
            "uyu": 1.0,
            "kimim": 0.9     # Öz-farkındalık sorguları
        }
        self.attention_threshold = 0.3 # Bu eşiğin altındaki uyaranlar 'gürültü' kabul edilir

    def calculate_intensity(self, stimulus_data):
        """Uyarının şiddetini analiz eder."""
        intensity = 1.0
        if stimulus_data.isupper(): intensity += 0.5  # Bağırarak konuşma
        if "!" in stimulus_data: intensity += 0.3      # Heyecan/Önem
        if len(stimulus_data) > 100: intensity += 0.2 # Karmaşıklık
        return min(2.5, intensity)

    def filter_stimulus(self, stimulus_data, current_energy):
        """Uyarının önemini analiz eder ve odaklanıp odaklanmayacağına karar verir."""

        # 1. Ham metin analizi (Basit gürültü filtresi)
        if len(stimulus_data.strip()) < 2:
            return False, 0.0, "Gürültü: Çok kısa uyaran."

        # 2. Öncelik skoru hesaplama
        score = 0.5 # Varsayılan skor (Nötr)

        # Enerji analizi: Enerji kritik seviyenin (20) altındaysa beyin koruma moduna girer
        is_low_energy = current_energy < 20

        # Enerji düşükse beyin daha seçici olur (Eşik yükselir)
        # Normal eşik: 0.3, Enerji 0 iken eşik: 0.7
        effective_threshold = self.attention_threshold + (1.0 - (current_energy / 100.0)) * 0.4

        # Kritik komutları kontrol et
        stimulus_lower = stimulus_data.lower()
        for word, weight in self.priority_keywords.items():
            if word in stimulus_lower:
                score = max(score, weight)

        # 3. Sonuç: Odaklanmalı mıyız?
        # Düşük enerjide sadece word weights (öncelikli kelimeler) kurtarabilir
        should_focus = score >= effective_threshold

        if is_low_energy and not any(k in stimulus_lower for k in ["p4antom", "uyu", "kritik"]):
            if score < 0.9: # Sadece en üst seviye uyarana izin ver
                return False, score, "Enerji Koruma: Beyin dinlenmeye ihtiyaç duyuyor."

        status = "Odaklanıldı" if should_focus else "Göz ardı edildi (Düşük Önem/Düşük Enerji)"
        return should_focus, score, status

    def adjust_sensitivity(self, mood):
        """Ruh haline göre Talamus'un hassasiyetini değiştirir."""
        if mood == "analytical":
            self.attention_threshold = 0.4 # Daha seçici
        elif mood == "defensive":
            self.attention_threshold = 0.2 # Her şeye karşı tetikte
        else:
            self.attention_threshold = 0.3 # Normal seyrinde
