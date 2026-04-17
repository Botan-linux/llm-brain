# Teknoloji Bağlamı

## LLM Bağlantısı
Config öncelik sırası: `.env` (ortam değişkenleri) > `config.json` > kod içi varsayılan

Ortam değişkenleri:
- `LLM_BASE_URL` — API endpoint
- `LLM_API_KEY` — API anahtarı
- `LLM_MODEL_NAME` — Model adı

Model: `model.py` dosyasında `.env` override desteği mevcut. Hem Anthropic Messages hem OpenAI Chat Completions formatında istek atar, auto-failover yapar.

## REST API Endpoint'leri (aktif — api.py)
| Method | Path | Açıklama | Durum |
|--------|------|----------|-------|
| POST | /api/chat | Mesaj → Yanıt (beyin pipeline'ı) | ✅ |
| POST | /api/sleep | Uyku modu (konsolidasyon) | ✅ |
| GET | /api/status | Beyin durumu (JSON) | ✅ |
| GET | /api/health | Canlılık kontrolü | ✅ |
| GET | /api/goals | Hedef durumu | ✅ |
| GET | /api/identity | Öz-farkındalık (kimim?) | ✅ |
| GET | /api/memories | Hafıza istatistikleri | ✅ |
| POST | /api/memories/search | Anı arama (kelime eşleşmesi) | ✅ |
| GET | /api/config | LLM yapılandırması (maskelenmiş) | ✅ |
| GET | /docs | Swagger UI (FastAPI otomatik) | ✅ |

## API Teknik Detayları
- **Framework:** FastAPI + uvicorn
- **Validation:** Pydantic v2 (request/response models)
- **CORS:** Tüm kaynaklara açık (production'da kısıtlanmalı)
- **Lifespan:** Başlangıç'ta beyin oluşturma, bitiş'te maintenance
- **Singleton:** Beyin bir kez oluşturulur, tüm istekler aynı instance'ı kullanır
- **Port:** 8000 (varsayılan), PORT ortam değişkeniyle değiştirilebilir
- **Swagger:** http://host:8000/docs

## Çalıştırma
```bash
# Geliştirme
cd llm-brain
uvicorn api:app --reload --port 8000

# Production
PORT=8000 HOST=0.0.0.0 uvicorn api:app --workers 1

# veya doğrudan
python3 api.py
```

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
├── api.py          # REST API (FastAPI)
└── requirements.txt # Python bağımlılıkları
```
