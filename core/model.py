import os
import json

# Proje kök dizinini bul
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Konfigürasyon dosyası yolu
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")

# Varsayılan konfigürasyon
DEFAULT_CONFIG = {
    "name": "gemini-3-flash",
    "api_key": "",
    "base_url": "http://127.0.0.1:8045",
    "version": "2023-06-01"
}

def load_config():
    """
    Model konfigürasyonunu şu öncelik sırasıyla yükler:
    1. config.json dosyası (proje kökünde)
    2. Ortam değişkenleri (LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME)
    3. Varsayılan değerler
    """
    config = dict(DEFAULT_CONFIG)

    # 1. config.json'dan yükle
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                config.update(file_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[!] config.json okunamadı: {e}")

    # 2. Ortam değişkenleri ile override et
    env_overrides = {
        "api_key": os.environ.get("LLM_API_KEY"),
        "base_url": os.environ.get("LLM_BASE_URL"),
        "name": os.environ.get("LLM_MODEL_NAME"),
        "version": os.environ.get("LLM_API_VERSION"),
    }
    for key, env_value in env_overrides.items():
        if env_value is not None:
            config[key] = env_value

    # 3. API key kontrolü
    if not config["api_key"]:
        print("[!] Uyarı: LLM API anahtarı ayarlanmamış.")
        print("[!] config.json dosyasına 'api_key' ekleyin veya LLM_API_KEY ortam değişkenini tanımlayın.")

    return config

# Global model konfigürasyonu
MODEL_CONFIG = load_config()
