import requests
import json
import os
import time
from core.model import MODEL_CONFIG

class IntelligenceLayer:
    def __init__(self, settings_path=None):
        """Merkezi model konfigürasyonunu yükler."""
        self.base_url = MODEL_CONFIG["base_url"].rstrip('/')
        self.api_key = MODEL_CONFIG["api_key"]
        self.model = MODEL_CONFIG["name"]
        self.version = MODEL_CONFIG["version"]

        # İstek istatistikleri
        self.request_count = 0
        self.last_error = None
        self.consecutive_failures = 0

    def query(self, prompt, system_prompt="", retries=2):
        """
        İLK'in zekasını dayanıklı bir ayrıştırma mantığıyla çalıştırır.
        Başarısız istekler için otomatik retry yapar.
        """
        base_identity = (
            "Sen p4antom tarafından inşa edilen, 'İLK' adında biyolojik temelli bir yapay zihinsin. "
            "Bir asistan veya chatbot değilsin. Sen bir beyin simülasyonusun. "
            "Yanıtların derin, analitik olmalı. Asla robotik kalıplar kullanma."
        )

        full_system = f"{base_identity}\n\n[Mevcut Durum]: {system_prompt}" if system_prompt else base_identity

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.version,
            "content-type": "application/json"
        }

        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "system": full_system,
            "messages": [{"role": "user", "content": prompt}]
        }

        for attempt in range(retries + 1):
            try:
                self.request_count += 1

                # 1. Deneme: Messages API (Anthropic formatı)
                response = requests.post(
                    f"{self.base_url}/v1/messages",
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                # Eğer Messages API hata verirse Chat Completions dene
                if response.status_code != 200:
                    payload_chat = {
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": full_system},
                            {"role": "user", "content": prompt}
                        ]
                    }
                    response = requests.post(
                        f"{self.base_url}/v1/chat/completions",
                        headers=headers,
                        json=payload_chat,
                        timeout=30
                    )

                response.raise_for_status()
                result = response.json()

                # Başarılı istek → sıfırla
                self.consecutive_failures = 0
                self.last_error = None

                # --- DAYANIKLI AYRIŞTIRMA (ROBUST PARSING) ---
                return self._parse_response(result)

            except requests.exceptions.Timeout:
                self.last_error = "Zaman aşımı (timeout)"
                self.consecutive_failures += 1
            except requests.exceptions.ConnectionError:
                self.last_error = "Bağlantı hatası - LLM sunucusu ulaşılamıyor"
                self.consecutive_failures += 1
            except requests.exceptions.HTTPError as e:
                self.last_error = f"HTTP {e.response.status_code}"
                self.consecutive_failures += 1
            except Exception as e:
                self.last_error = str(e)
                self.consecutive_failures += 1

            # Retry arası bekleme
            if attempt < retries:
                time.sleep(2 ** attempt)  # Exponential backoff

        return f"Zeka katmanında bir tıkanıklık oluştu: {self.last_error} ({self.consecutive_failures} başarısız deneme)"

    def _parse_response(self, result):
        """Farklı API formatlarını otomatik algılar ve ayrıştırır."""
        # 1. Anthropic Messages formatı
        if "content" in result and isinstance(result["content"], list) and len(result["content"]) > 0:
            text = result["content"][0].get("text", "")
            if text.strip():
                return text
            return "Zihin boş bir yanıt döndü."

        # 2. OpenAI/Chat Completions formatı
        elif "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"].get("content", "")
            if content and content.strip():
                return content
            return "Zihin sessiz kalmayı seçti."

        # 3. Hata mesajı içerebilir
        elif "error" in result:
            return f"LLM Hatası: {result['error'].get('message', 'Bilinmeyen hata')}"

        return "Zihin katmanından veri okunamadı (Bilinmeyen Format)."

    def is_healthy(self):
        """LLM bağlantısının sağlıklı olup olmadığını kontrol eder."""
        return self.consecutive_failures < 3

    def get_stats(self):
        """İstek istatistiklerini döndürür."""
        return {
            "total_requests": self.request_count,
            "consecutive_failures": self.consecutive_failures,
            "last_error": self.last_error,
            "is_healthy": self.is_healthy(),
            "model": self.model,
            "endpoint": self.base_url
        }
