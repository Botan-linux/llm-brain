"""
Yapılandırma doğrulama yardımcıları.
"""

import re
import os
import json


def validate_config(config):
    """
    Model yapılandırmasını doğrular.

    Args:
        config: dict — MODEL_CONFIG sözlüğü

    Returns:
        list: Uyarı ve hata mesajları listesi
    """
    issues = []

    # API Key kontrolü
    if not config.get("api_key"):
        issues.append({
            "level": "warning",
            "field": "api_key",
            "message": "LLM API anahtarı ayarlanmamış. Zeka katmanı çalışmayacak.",
            "fix": "config.json dosyasına 'api_key' ekleyin veya LLM_API_KEY ortam değişkenini tanımlayın."
        })

    # Base URL kontrolü
    base_url = config.get("base_url", "")
    if not base_url:
        issues.append({
            "level": "error",
            "field": "base_url",
            "message": "LLM base URL ayarlanmamış.",
            "fix": "config.json dosyasına 'base_url' ekleyin (ör: 'https://api.example.com')."
        })
    elif not base_url.startswith(("http://", "https://")):
        issues.append({
            "level": "error",
            "field": "base_url",
            "message": f"Geçersiz base URL formatı: '{base_url}'",
            "fix": "URL 'http://' veya 'https://' ile başlamalı."
        })

    # Model name kontrolü
    name = config.get("name", "")
    if not name or not isinstance(name, str):
        issues.append({
            "level": "error",
            "field": "name",
            "message": "Model adı ayarlanmamış veya geçersiz.",
            "fix": "config.json dosyasına 'name' alanı ekleyin (ör: 'gpt-4', 'claude-3')."
        })

    # Version kontrolü — opsiyonel ama ayarlanırsa geçerli bir format olmalı
    version = config.get("version")
    if version is not None and version != "":
        version_pattern = re.compile(r"^(v?\d+(?:\.\d+)*)$|^\d{4}-\d{2}-\d{2}$")
        if not isinstance(version, str) or not version_pattern.match(version):
            issues.append({
                "level": "warning",
                "field": "version",
                "message": f"Geçersiz versiyon formatı: '{version}'",
                "fix": "Versiyon 'v1', 'v2.1' veya '2023-06-01' formatında olmalıdır."
            })

    # Config.json dosya kontrolü
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    if not os.path.exists(config_path):
        issues.append({
            "level": "info",
            "field": "config_file",
            "message": "config.json dosyası bulunamadı, varsayılan değerler kullanılıyor.",
            "fix": "Proje köküne config.json dosyası oluşturun."
        })
    else:
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            issues.append({
                "level": "error",
                "field": "config_file",
                "message": f"config.json dosyası geçersiz JSON içeriyor: {e}",
                "fix": "JSON syntax hatasını düzeltin."
            })

    # .env dosya kontrolü
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    has_env = os.path.exists(env_path)
    if has_env:
        issues.append({
            "level": "info",
            "field": "env_file",
            "message": ".env dosyası bulundu, ortam değişkenleri yüklenecek.",
            "fix": None
        })

    return issues


def validate_storage():
    """
    Storage dizin yapısını doğrular.
    Eksik klasörleri oluşturur.

    Returns:
        list: Uyarı mesajları
    """
    issues = []
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "storage")

    required_dirs = ["long_term", "short_term", "logs"]
    for dirname in required_dirs:
        dirpath = os.path.join(base, dirname)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
            issues.append({
                "level": "info",
                "field": dirname,
                "message": f"Storage dizini oluşturuldu: {dirname}/",
                "fix": None
            })

    return issues
