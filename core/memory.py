import os
import json
from datetime import datetime

class MemoryGateway:
    def __init__(self, storage_path="storage/"):
        self.storage_path = storage_path
        self.long_term_path = os.path.join(storage_path, "long_term/")
        self.short_term_path = os.path.join(storage_path, "short_term/")

        # Klasörleri oluştur
        for path in [self.long_term_path, self.short_term_path]:
            if not os.path.exists(path):
                os.makedirs(path)

    def store_experience(self, data, is_critical=False):
        """Bir deneyimi belleğe sessizce kaydeder."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        metadata = {
            "weight": 1.0,
            "access_count": 1,
            "last_access": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }

        if is_critical:
            self._save_markdown(data, f"experience_{timestamp}.md")
            self._save_json(data, f"experience_{timestamp}.json", metadata, is_permanent=True)
        else:
            self._save_json(data, f"temp_{timestamp}.json", metadata, is_permanent=False)

    def _save_json(self, data, filename, metadata, is_permanent=True):
        folder = self.long_term_path if is_permanent else self.short_term_path
        path = os.path.join(folder, filename)
        output = {
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "type": "permanent" if is_permanent else "ephemeral",
            "metadata": metadata
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=4, ensure_ascii=False)

    def _save_markdown(self, data, filename):
        path = os.path.join(self.long_term_path, filename)
        content = f"# Deneyim Kaydı - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{data}\n"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def update_synapse(self, filename, boost=0.1):
        """Anı hatırlandığında sinapsı güçlendirir."""
        path = None
        for folder in [self.long_term_path, self.short_term_path]:
            temp_path = os.path.join(folder, filename)
            if os.path.exists(temp_path):
                path = temp_path
                break
        if not path or not path.endswith(".json"): return
        with open(path, 'r', encoding='utf-8') as f:
            content = json.load(f)
        content["metadata"]["weight"] += boost
        content["metadata"]["access_count"] += 1
        content["metadata"]["last_access"] = datetime.now().isoformat()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4, ensure_ascii=False)

    def apply_neuroplasticity(self, decay_rate=0.01):
        """Unutma sürecini simüle eder."""
        for folder in [self.long_term_path, self.short_term_path]:
            for filename in os.listdir(folder):
                if filename.endswith(".json"):
                    path = os.path.join(folder, filename)
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = json.load(f)
                        content["metadata"]["weight"] -= decay_rate
                        if content["metadata"]["weight"] < 0: content["metadata"]["weight"] = 0
                        with open(path, 'w', encoding='utf-8') as f:
                            json.dump(content, f, indent=4, ensure_ascii=False)
                    except Exception as e:
                        print(f"[!] Hata: {filename} güncellenemedi: {e}")

    def consolidate_memories(self, threshold=0.4):
        """Kısa süreli hafızayı uzun süreli hafızaya taşır veya eler."""
        print("[*] Hafıza konsolidasyonu (Uyku Evresi) başlatıldı...")
        files = os.listdir(self.short_term_path)
        consolidated_count = 0
        forgotten_count = 0

        for filename in files:
            if not filename.endswith(".json"): continue
            path = os.path.join(self.short_term_path, filename)

            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = json.load(f)

                weight = content["metadata"]["weight"]

                if weight >= threshold:
                    # Uzun süreliye taşı
                    new_filename = filename.replace("temp_", "experience_")
                    new_path = os.path.join(self.long_term_path, new_filename)
                    content["type"] = "permanent"

                    with open(new_path, 'w', encoding='utf-8') as f:
                        json.dump(content, f, indent=4, ensure_ascii=False)

                    # Markdown özetini de oluştur
                    self._save_markdown(content["data"], new_filename.replace(".json", ".md"))
                    consolidated_count += 1
                else:
                    forgotten_count += 1

                # Her durumda kısa süreliden sil
                os.remove(path)

            except Exception as e:
                print(f"[!] {filename} konsolide edilemedi: {e}")

        print(f"[+] Sonuç: {consolidated_count} anı pekiştirildi, {forgotten_count} anı unutuldu.")
        return consolidated_count, forgotten_count

    def retrieve_memories(self, limit=10):
        """Anıları getirir."""
        # JSON dosyalarını ve içeriklerini oku
        memories = []
        for filename in os.listdir(self.long_term_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.long_term_path, filename), 'r') as f:
                    memories.append(json.load(f))

        # Ağırlığa göre sırala (Nöroplastisite: Önemli anılar önce gelir)
        sorted_memories = sorted(memories, key=lambda x: x["metadata"]["weight"], reverse=True)
        return sorted_memories[:limit]
