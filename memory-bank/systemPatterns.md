# Sistem Kalıpları

## Config Yönetimi
Öncelik: `.env` (ortam değişkenleri) > `config.json` > varsayılan değerler
- API key, model, endpoint hepsi .env ile override edilebilir
- model.py'da `os.getenv()` kullanımı mevcut

## Loglama
- `core/logger.py` → Renkli konsol çıktısı + rotating dosya log
- Dosya: `storage/logs/ilk.log`
- Rotasyon: 5MB max, 3 backup dosya

## Hafıza Yapısı (proje içinde)
- `storage/long_term/` → Tarihli JSON + MD deneyim dosyaları
- `storage/working_memory.json` → Aktif konuşma bağlamı
- `storage/emotional_memory.json` → Duygu hafızası
- `storage/personality.json` → Kişilik profili
- `storage/goals.json` → Hedef takibi
- `storage/inner_world.json` → İç dünya
- `storage/reflexes.json` → Refleks kalıpları
- `storage/prefrontal.json` → Karar verme durumu

## Hafıza Sistemi (proje dışı — geliştirici hafızası)
- `memory-bank/` → Cline format (projectbrief, productContext, systemPatterns, techContext, activeContext, progress)
- `sessions/` → Tarihli oturum özetleri
- Bu dosyalar yeni oturumda projenin durumunu hızlıca kavramak için okunur

## API Formatı
LLM'e hem Anthropic Messages hem OpenAI Chat Completions formatında istek atar, auto-failover yapar. Bu sayede farklı LLM sağlayıcılarına kolay geçiş mümkündür.

## Hata Yönetimi
- core/validators.py → Girdi doğrulama
- Her modül try/except ile sarılı
- Logger üzerinden hata takibi

## AI Kural Sistemi
- `.z-ai/rules.md` → Ana kurallar (9 kural + bağlam kurtarma mekanizması)
- `.z-ai/quick-start.md` → 30 saniyede projeyi anlama özeti
- `.z-ai/file-map.md` → Değişiklik-dosya eşleme tablosu
- `.z-ai/session-protocol.md` → Oturum açma/kapatma/arşivleme protokolü
- `memory-bank/checkpoint.md` → Anlık durum görüntüsü (her oturum sonunda güncellenir)
- Tümü .gitignore'da gizli (.z-ai/ dizini GitHub'a pushlanmaz)
- Her oturumda ilk okunması gereken dosyalar: quick-start → activeContext → checkpoint
