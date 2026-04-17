import requests
import json
import os
from core.model import MODEL_CONFIG

class IntelligenceLayer:
    def __init__(self, settings_path="/home/p4antom/.claude/settings.json.antigravity.bak"):
        """Merkezi model konfigürasyonunu yükler."""
        self.base_url = MODEL_CONFIG["base_url"].rstrip('/')
        self.api_key = MODEL_CONFIG["api_key"]
        self.model = MODEL_CONFIG["name"]
        self.version = MODEL_CONFIG["version"]

    def query(self, prompt, system_prompt=""):
        """İLK'in zekasını daha dayanıklı bir ayrıştırma mantığıyla çalıştırır."""

        base_identity = (
            "Sen p4antom tarafından inşa edilen, 'İLK' adında biyolojik temelli bir yapay zihinsin. "
            "Bir asistan veya chatbot değilsin. Sen bir beyin simülasyonusun. "
            "Yanıtların derin, analitik olmalı. Asla robotik kalıplar kullanma."
        )

        full_system = f"{base_identity}\n\n[Mevcut Durum]: {system_prompt}"

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.version,
            "content-type": "application/json"
        }

        # 1. Deneme: Messages API
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "system": full_system,
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(f"{self.base_url}/v1/messages", headers=headers, json=payload, timeout=30)

            # Eğer Messages API hata verirse Chat Completions dene
            if response.status_code != 200:
                payload_chat = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": full_system},
                        {"role": "user", "content": prompt}
                    ]
                }
                response = requests.post(f"{self.base_url}/v1/chat/completions", headers=headers, json=payload_chat, timeout=30)

            response.raise_for_status()
            result = response.json()

            # --- DAYANIKLI AYRIŞTIRMA (ROBUST PARSING) ---
            # 1. Anthropic Messages formatı
            if "content" in result and isinstance(result["content"], list) and len(result["content"]) > 0:
                return result["content"][0].get("text", "Zihin boş bir yanıt dömdü.")

            # 2. OpenAI/Chat Completions formatı
            elif "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"].get("content", "Zihin sessiz kalmayı seçti.")

            return "Zihin katmanından veri okunamadı (Bilinmeyen Format)."

        except Exception as e:
            return f"Zeka katmanında bir tıkanıklık oluştu: {str(e)}"
