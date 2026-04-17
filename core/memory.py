import os
import json
from datetime import datetime
import re
from core.logger import get_logger

logger = get_logger(__name__)

class MemoryGateway:
    def __init__(self, storage_path=None):
        if storage_path is None:
            storage_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "storage"
            )

        self.storage_path = storage_path
        self.long_term_path = os.path.join(storage_path, "long_term/")
        self.short_term_path = os.path.join(storage_path, "short_term/")

        # Klasörleri oluştur
        for path in [self.long_term_path, self.short_term_path]:
            if not os.path.exists(path):
                os.makedirs(path)

    def store_experience(self, data, is_critical=False):
        """Bir deneyimi belleğe sessizce kaydeder."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
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
        stimulus = data.get("stimulus", "")
        response = data.get("response", "")
        mood = data.get("mood_state", "")
        content = (
            f"# Deneyim Kaydı - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"**Ruh Hali:** {mood}\n\n"
            f"## Uyaran\n{stimulus}\n\n"
            f"## Yanıt\n{response}\n"
        )
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
                        logger.error(f"{filename} güncellenemedi: {e}")

    def consolidate_memories(self, threshold=0.4):
        """Kısa süreli hafızayı uzun süreli hafızaya taşır veya eler."""
        logger.info("Hafıza konsolidasyonu (Uyku Evresi) başlatıldı...")
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
                logger.warning(f"{filename} konsolide edilemedi: {e}")

        logger.info(f"Konsolidasyon: {consolidated_count} anı pekiştirildi, {forgotten_count} anı unutuldu.")
        return consolidated_count, forgotten_count

    def retrieve_memories(self, limit=10):
        """Anıları getirir (ağırlık sırasına göre)."""
        memories = []
        for filename in os.listdir(self.long_term_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.long_term_path, filename), 'r') as f:
                    memories.append(json.load(f))

        # Ağırlığa göre sırala (Nöroplastisite: Önemli anılar önce gelir)
        sorted_memories = sorted(memories, key=lambda x: x["metadata"]["weight"], reverse=True)
        return sorted_memories[:limit]

    def search_relevant(self, query, limit=3):
        """Uyaranla ilgili anıları basit kelime eşleşmesiyle arar."""
        all_memories = self.retrieve_memories(limit=50)
        if not all_memories:
            return []

        # Sorgudaki kelimeleri çıkar
        query_words = set(re.findall(r'\w+', query.lower(), re.UNICODE))
        if not query_words:
            return []

        scored = []
        for mem in all_memories:
            data = mem.get("data", {})
            stimulus = str(data.get("stimulus", "")).lower()
            response = str(data.get("response", "")).lower()
            text = stimulus + " " + response

            text_words = set(re.findall(r'\w+', text, re.UNICODE))

            # Jaccard benzerliği
            intersection = query_words & text_words
            union = query_words | text_words
            if union:
                score = len(intersection) / len(union)
            else:
                score = 0

            # Ağırlığı da hesaba kat
            weight = mem.get("metadata", {}).get("weight", 0)
            final_score = score * 0.7 + (weight / 2.0) * 0.3

            if score > 0.05:  # Minimum eşik
                scored.append({
                    "stimulus": data.get("stimulus", ""),
                    "response": data.get("response", ""),
                    "mood": data.get("mood_state", ""),
                    "score": final_score,
                    "weight": weight
                })

        # Skora göre sırala
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]

    def get_stats(self):
        """Hafıza istatistiklerini döndürür."""
        long_term_count = len([f for f in os.listdir(self.long_term_path) if f.endswith(".json")])
        short_term_count = len([f for f in os.listdir(self.short_term_path) if f.endswith(".json")])
        return {
            "long_term": long_term_count,
            "short_term": short_term_count,
            "total": long_term_count + short_term_count
        }
