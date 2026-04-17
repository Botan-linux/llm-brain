# Teknoloji Bağlamı

## LLM Bağlantısı
Config öncelik sırası: `.env` (ortam değişkenleri) > `config.json` > kod içi varsayılan

Ortam değişkenleri:
- `LLM_BASE_URL` — API endpoint
- `LLM_API_KEY` — API anahtarı
- `LLM_MODEL_NAME` — Model adı

Model: `model.py` dosyasında `.env` override desteği mevcut. Hem Anthropic Messages hem OpenAI Chat Completions formatında istek atar, auto-failover yapar.

## REST API Endpoint'leri (plan)
| Method | Path | Açıklama |
|--------|------|----------|
| POST | /api/chat | Mesaj → Yanıt |
| GET | /api/status | Beyin durumu |
| POST | /api/sleep | Uyku modu |
| GET | /api/health | Canlılık kontrolü |

## Dosya Yapısı
```
llm-brain/
├── core/           # 15 modül
├── storage/        # JSON hafıza dosyaları
│   ├── long_term/  # Deneyim kayıtları
│   └── logs/       # Log dosyaları
├── memory-bank/    # Proje hafıza sistemi (Cline format)
├── sessions/       # Oturum özetleri
├── tests/          # Test dosyaları
├── docs/           # Dokümantasyon
├── config.json     # LLM yapılandırması
└── api.py          # REST API (yazılacak)
```
