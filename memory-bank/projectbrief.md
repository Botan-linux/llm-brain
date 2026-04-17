# İLK — Yapay Beyin Simülasyonu

## Amaç
İnsan beyninin temel yapılarını Python ile simüle eden yapay zeka çatısı. Kullanıcı mesajı alır, 16 modüllü nöral pipeline'dan geçirir, düşünce/duygu/hafıza süreçlerini işleterek bağlamsal ve kişilikli yanıt üretir.

## Teknoloji
- Python 3.11+
- LLM: Gemini (OpenAI-compatible API)
- REST API: FastAPI + Uvicorn
- Deploy: Docker + Render.com (free 512MB)
- Keepalive: cron-job.com (2dk ping)
- Config: .env ortam değişkenleri > config.json > varsayılan

## Sürüm
v0.3.0

## GitHub
https://github.com/Botan-linux/llm-brain

## Modüller (16)
brain.py (merkez) + core/ altında 15 modül:
- Thalamus (giriş kapısı)
- Reflex (refleks yanıtlar)
- Limbic (duygu işleme)
- Emotional Memory (duygu hafızası)
- Working Memory (çalışma hafızası)
- Language Processor (dil işleme)
- Learning (öğrenme)
- Subconscious (bilinçaltı)
- Self Awareness (öz-farkındalık)
- Prefrontal (karar verme)
- Intelligence (zeka katmanı)
- Ego (benlik)
- Dream Engine (rüya motoru)
- Memory (hafıza yönetimi)
- Logger (loglama)
