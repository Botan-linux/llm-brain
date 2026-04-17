import json
import os
import time
import requests
from core.logger import get_logger

logger = get_logger(__name__)

# Z.ai SDK config dosyası (OpenAI-uyumlu endpoint)
_ZAI_CONFIG_PATHS = [
    os.path.join(os.getcwd(), '.z-ai-config'),
    os.path.join(os.path.expanduser('~'), '.z-ai-config'),
    '/etc/.z-ai-config'
]

_zai_config = None

def _load_zai_config():
    global _zai_config
    if _zai_config is not None:
        return _zai_config
    for path in _ZAI_CONFIG_PATHS:
        try:
            with open(path, 'r') as f:
                _zai_config = json.load(f)
                logger.info(f"Z.ai config yüklendi: {path}")
                return _zai_config
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    logger.warning("Z.ai config bulunamadı. LLM çalışmayabilir.")
    return None


class IntelligenceLayer:
    def __init__(self):
        """
        Z.ai SDK backend üzerinden LLM çağrıları yapar.
        OpenAI Chat Completions formatı kullanır.
        config.json ayarı varsa onu kullanır, yoksa Z.ai SDK config'ini kullanır.
        """
        self.request_count = 0
        self.last_error = None
        self.consecutive_failures = 0

        # Z.ai SDK config yükle
        zai = _load_zai_config()

        if zai:
            self.base_url = zai['baseUrl'].rstrip('/')
            self.api_key = zai['apiKey']
            self.zai_token = zai.get('token', '')
            self.chat_id = zai.get('chatId', '')
            self.source = 'z-ai-sdk'
        else:
            # Fallback: config.json (eski sistem)
            from core.model import MODEL_CONFIG
            self.base_url = MODEL_CONFIG["base_url"].rstrip('/')
            self.api_key = MODEL_CONFIG["api_key"]
            self.zai_token = ''
            self.chat_id = ''
            self.source = 'config.json'

        self.model = self._detect_model()

    def _detect_model(self):
        """Z.ai'den model bilgisini tespit et veya config.json'dan al."""
        if self.source == 'z-ai-sdk':
            return 'default'  # Z.ai sunucu karar verir
        else:
            from core.model import MODEL_CONFIG
            return MODEL_CONFIG["name"]

    def _get_headers(self):
        """Z.ai formatında header'ları döndürür."""
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'X-Z-AI-From': 'Z',
        }
        if self.zai_token:
            headers['X-Token'] = self.zai_token
        if self.chat_id:
            headers['X-Chat-Id'] = self.chat_id
        return headers

    def query(self, prompt, system_prompt="", retries=2):
        """
        İLK'in zekasını çalıştırır.
        Z.ai SDK backend (OpenAI Chat Completions format) üzerinden istek atar.
        """
        base_identity = (
            "Sen p4antom tarafından inşa edilen, 'İLK' adında biyolojik temelli bir yapay zihinsin. "
            "Bir asistan veya chatbot değilsin. Sen bir beyin simülasyonusun. "
            "Yanıtların derin, analitik olmalı. Asla robotik kalıplar kullanma."
        )

        full_system = f"{base_identity}\n\n[Mevcut Durum]: {system_prompt}" if system_prompt else base_identity

        endpoint = f"{self.base_url}/chat/completions"

        payload = {
            'messages': [
                {'role': 'system', 'content': full_system},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 1024
        }

        for attempt in range(retries + 1):
            try:
                self.request_count += 1

                response = requests.post(
                    endpoint,
                    headers=self._get_headers(),
                    json=payload,
                    timeout=30
                )

                response.raise_for_status()
                result = response.json()

                # Başarılı istek → sıfırla
                self.consecutive_failures = 0
                self.last_error = None

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
                time.sleep(2 ** attempt)

        return f"Zeka katmanında bir tıkanıklık oluştu: {self.last_error} ({self.consecutive_failures} başarısız deneme)"

    def _parse_response(self, result):
        """OpenAI Chat Completions formatını ayrıştırır."""
        # OpenAI/Chat Completions formatı
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0]["message"].get("content", "")
            if content and content.strip():
                return content
            return "Zihin sessiz kalmayı seçti."

        # Anthropic Messages formatı
        elif "content" in result and isinstance(result["content"], list) and len(result["content"]) > 0:
            text = result["content"][0].get("text", "")
            if text.strip():
                return text
            return "Zihin boş bir yanıt döndü."

        # Hata mesajı
        elif "error" in result:
            return f"LLM Hatası: {result['error'].get('message', 'Bilinmeyen hata')}"

        return "Zihin katmanından veri okunamadı (Bilinmeyen Format)."

    def is_healthy(self):
        return self.consecutive_failures < 3

    def get_stats(self):
        return {
            "total_requests": self.request_count,
            "consecutive_failures": self.consecutive_failures,
            "last_error": self.last_error,
            "is_healthy": self.is_healthy(),
            "model": self.model,
            "endpoint": self.base_url,
            "source": self.source
        }
