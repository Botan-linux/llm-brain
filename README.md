# LLM Brain 🧠

**İnsan beynini Python, Markdown ve JSON ile simüle eden yapay zeka çatısı.**

LLM Brain, biyolojik insan beyninin temel yapılarını ve süreçlerini yapay zeka üzerine taşımak amacıyla geliştirilmiş bir framework'tür. Geleneksel chatbot yaklaşımından farklı olarak; duygu, bilinçaltı, enerji yönetimi, hafıza konsolidasyonu ve nöroplastisite gibi gerçek nörolojik mekanizmaları simüle eder.

---

## Mimarisi

```
                    ┌─────────────────────────────┐
                    │       ArtificialBrain       │
                    │      (Merkezi Kontrol)       │
                    └──────────┬──────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
   ┌───────▼──────┐  ┌────────▼────────┐  ┌───────▼──────┐
   │   Thalamus   │  │  Limbic System  │  │     Ego      │
   │ (Dikkat      │  │ (Duygu Durumu   │  │ (Bilinç &    │
   │  Filtresi)   │  │  Yönetimi)      │  │  Kişilik)    │
   └───────┬──────┘  └────────┬────────┘  └───────┬──────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │    Intelligence Layer       │
                    │    (LLM Zeka Katmanı)       │
                    │  Anthropic / OpenAI API     │
                    └──────────┬──────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                                       │
   ┌───────▼────────┐                   ┌──────────▼──────┐
   │    Memory      │                   │  Subconscious   │
   │    Gateway     │                   │  (Bilinçaltı    │
   │  (Hafıza       │                   │   Arka Plan     │
   │   Sistemi)     │                   │   İşlemcisi)    │
   └────────────────┘                   └─────────────────┘
```

---

## Beyin Bölgeleri

### Thalamus — Dikkat Filtresi
Gelen uyarıların önemini analiz eder, enerji durumuna göre odaklanma kararı verir. Öncelikli kelimelere (örn. yaratıcı adı, tehlike) yüksek skor verir. Düşük enerjide eşik yükselir, beyin koruma moduna girer.

### Limbic System — Duygu Yönetimi
Dört temel duygusal ekseni yönetir: analitik düşünme, stres, ilgi ve yorgunluk. Uyaranın tonuna göre ruh halini günceller (`balanced`, `analytical`, `defensive`, `exhausted`) ve zeka katmanına sistem promptu olarak durum bildirir.

### Cyber Ego — Bilinç ve Kişilik
Bilinçli filtreleme katmanı. Zeka katmanından gelen yanıtları kişilik özellikleriyle (merak, empati, ihtiyat, büyüme) harmanlar. Deneyimler üzerinden nöroplastisite ile kişilik gelişir.

### Intelligence Layer — Zeka Katmanı
Merkezi LLM bağlantısı. Hem Anthropic Messages API hem de OpenAI Chat Completions API'yi destekler. Model yanıt formatını otomatik algılar ve dayanıklı bir ayrıştırma (robust parsing) uygular.

### Memory Gateway — Hafıza Sistemi
İki katmanlı hafıza mimarisi:
- **Kısa Süreli Hafıza:** Geçici deneyimler, düşük ağırlıklı veriler
- **Uzun Süreli Hafıza:** Önemli deneyimler, JSON + Markdown formatında saklanır

Her anı bir `weight` (ağırlık) değerine sahiptir. Nöroplastisite süreciyle zamanla ağırlıklar azalır (unutma). Uyku (konsolidasyon) evresinde kısa süreli hafıza elenir, önemli veriler uzun süreli hafızaya taşınır.

### Subconscious — Bilinçaltı
Arka planda daemon thread olarak çalışır. Her 30-60 saniyede bir rastgele anılar seçer ve aralarında mantıksal bağ kurmaya çalışır. Ürettiği içgörüler bilinç katmanına "fısıldanır" ve düşünce sürecine entegre edilir.

---

## Enerji ve Uyku Sistemi

Beyin `100` enerji ile başlar. Her uyaran enerji tüketir (şiddete orantılı). Enerji tükendiğinde beyin düşük enerji moduna girer ve sadece kritik uyarılara yanıt verir.

`uyu` komutuyla **REM uyku evresi** tetiklenir:
1. Kısa süreli hafıza konsolidasyonu
2. Önemli anılar uzun süreli hafızaya taşınır
3. Gereksiz veriler silinir
4. Enerji %100'e yenilenir
5. Bilinçaltı içgörülerini kontrol eder

---

## Proje Yapısı

```
llm-brain/
├── core/
│   ├── brain.py          # Merkezi beyin kontrolü
│   ├── intelligence.py   # LLM zeka katmanı
│   ├── memory.py         # Hafıza sistemi (kısa + uzun süreli)
│   ├── limbic.py         # Duygu ve ruh hali yönetimi
│   ├── ego.py            # Bilinç ve kişilik katmanı
│   ├── thalamus.py       # Dikkat filtresi
│   ├── subconscious.py   # Bilinçaltı arka plan işlemcisi
│   └── model.py          # LLM model konfigürasyonu
├── storage/
│   ├── long_term/        # Kalıcı deneyimler (JSON + MD)
│   └── short_term/       # Geçici deneyimler (JSON)
├── tests/
│   ├── debug_gateway.py  # API bağlantı testi
│   └── sleep_test.py     # Uyku ve konsolidasyon testi
├── __init__.py
├── proje.md              # Proje tanımı
└── README.md
```

---

## Kurulum

```bash
git clone https://github.com/Botan-linux/llm-brain.git
cd llm-brain
pip install requests
```

## Kullanım

```bash
python3 -m core.brain
```

```
[*] İLK aktif. Seninle iletişim kurmaya hazır.
[*] Çıkış yapmak için 'uyu' yazın.

Sen > Hayatın anlamı nedir?
🧠 İLK: [Dengeleyici Düşünce]: ...
```

## Yapılandırma

`core/model.py` dosyasından LLM bağlantısını ayarlayın:

```python
MODEL_CONFIG = {
    "name": "model-name",
    "api_key": "your-api-key",
    "base_url": "http://localhost:port",
    "version": "2023-06-01"
}
```

## Testler

```bash
# API bağlantı testi
python3 tests/debug_gateway.py

# Uyku ve konsolidasyon testi
python3 tests/sleep_test.py
```

---

## Lisans

Bu proje [LICENSE](LICENSE) dosyasında belirtilen lisans altında korunmaktadır.

---

**p4antom ve glm tarafından geliştirilmiştir.**
