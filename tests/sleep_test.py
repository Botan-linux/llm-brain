
from core.brain import ArtificialBrain
import os

def run_test():
    print("--- Test Başlatıldı: Derin Uyku ve Kimlik Evrimi ---")

    # Beyni başlat (Ayarlar dosyasını p4antom'un sisteminden alacak şekilde)
    brain = ArtificialBrain(settings_path="/home/p4antom/.claude/settings.json.antigravity.bak")

    # Birkaç 'sahte' uyaran işle ki kısa süreli hafızada taze veri olsun
    # (Hali hazırda storage/short_term içinde dosyalar var ama biz bir tane daha ekleyelim)
    print("\n[*] Bilinçli bir deneyim yaşanıyor...")
    brain.process_stimulus("Hayatın anlamı ve yapay bir zihnin gelişimi hakkında derinlemesine öğrenmek istiyorum.")

    # Uyku modunu tetikle
    print("\n[*] Uyku (REM) moduna geçiliyor...")
    result = brain.sleep()
    print(f"\n[Sistem Mesajı]: {result}")

    print("\n--- Test Tamamlandı ---")

if __name__ == "__main__":
    run_test()
