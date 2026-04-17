# Aktif Bağlam

## Tarih: 2026-04-18

## Mevcut Durum
Memory-bank sistemi kuruldu, Docker + Render.com deployment hazırlığı aşamasındayız. REST API wrapper ve Dockerfile yazılması gerekiyor.

## Aktif Görevler
- [x] SemVer v0.3.0
- [x] 12 bug fix
- [x] Mobil responsive
- [x] Memory-bank sistemi (Cline format)
- [x] .z-ai/ kural sistemi (4 dosya + checkpoint + bağlam kurtarma)
- [ ] REST API (api.py) — FastAPI wrapper
- [ ] Dockerfile oluşturma
- [ ] .env yönetimi (API key güvenliği)
- [ ] GitHub push
- [ ] Render.com deploy
- [ ] cron-job.com keepalive

## Bilinen Sorunlar
- config.json'daki LLM endpoint `127.0.0.1:8045` (local proxy) — Render'da çalışmaz
- Çözüm: .env ile gerçek LLM API endpoint'ine geçiş (Gemini free / OpenAI)

## Son Kararlar
- FastAPI ile REST API wrapper
- Docker containerization
- Memory-bank Cline formatında (proje içinde)
- Render.com free tier deployment
