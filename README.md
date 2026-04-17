# LLM Brain 🧠

**İnsan beynini Python, Markdown ve JSON ile simüle eden yapay zeka çatısı.**

LLM Brain, biyolojik insan beyninin temel yapılarını ve süreçlerini yapay zeka üzerine taşımak amacıyla geliştirilmiş bir framework'tür. Geleneksel chatbot yaklaşımından farklı olarak; duygu, bilinçaltı, enerji yönetimi, hafıza konsolidasyonu ve nöroplastisite gibi gerçek nörolojik mekanizmaları simüle eder. Yapay zeka varlığı **"İLK"** (Türkçe "ilk") adıyla bilinir.

---

## Mimarisi

```
                        ┌──────────────────────────────┐
                        │      ArtificialBrain         │
                        │    (14 Adımlı Pipeline)      │
                        └──────────┬───────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
  ┌──────▼──────┐          ┌──────▼──────┐          ┌───────▼──────┐
  │  Thalamus   │          │ Limbic Sys. │          │   Reflex     │
  │ (Dikkat     │          │ (Duygu &    │          │ (Otomatik    │
  │  Filtresi)  │          │  Enerji)    │          │  Tepkiler)   │
  └──────┬──────┘          └──────┬──────┘          └───────┬──────┘
         │                        │                        │
  ┌──────▼──────────┐    ┌──────▼──────────┐    ┌─────────▼───────┐
  │ Language Proc.  │    │  Prefrontal     │    │ Emotional Mem.  │
  │ (Wernicke/      │    │  Cortex        │    │ (Amygdala/      │
  │  Broca Alanları)│    │ (Karar/Plan)   │    │  Hippocampus)   │
  └──────┬──────────┘    └──────┬──────────┘    └─────────┬───────┘
         │                        │                        │
  ┌──────▼──────────┐    ┌──────▼──────────┐    ┌─────────▼───────┐
  │ Working Memory  │    │  Learning Eng.  │    │ Self-Awareness  │
  │ (Sohbet Bağlamı)│    │ (Deneyimlerden │    │ (Öz-Farkındalık │
  │                 │    │  Öğrenme)      │    │  & Meta-Biliş)  │
  └──────┬──────────┘    └──────┬──────────┘    └─────────┬───────┘
         │                        │                        │
         └────────────────────────┼────────────────────────┘
                                  │
                       ┌──────────▼──────────┐
                       │  Intelligence Layer  │
                       │  (LLM Zeka Katmanı) │
                       │ Anthropic / OpenAI   │
                       └──────────┬──────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │                               │
          ┌───────▼────────┐             ┌───────▼──────┐
          │  Memory        │             │ Dream Engine │
          │  Gateway       │             │ (REM/NREM    │
          │ (Kısa + Uzun   │             │  Rüya Sist.) │
          │  Süreli Hafıza)│             └──────────────┘
          └────────────────┘
                  │
          ┌───────▼────────┐       ┌───────▼──────┐
          │   Cyber Ego    │       │ Subconscious  │
          │ (Bilinç &      │       │ (Bilinçaltı   │
          │  Kişilik)      │       │  İşlemcisi)   │
          └────────────────┘       └──────────────┘

  ┌───────▼────────┐       ┌───────▼──────┐
  │ Inner World    │       │ Goal System  │
  │ (İç Dünya      │       │ (Hedef        │
  │  Algısı)       │       │  Belirleme)   │
  └────────────────┘       └──────────────┘
```

---

## Beyin Bölgeleri

### Faz 0 — Çekirdek Modüller

### Thalamus — Dikkat Filtresi
Gelen uyarıların önemini analiz eder, enerji durumuna göre odaklanma kararı verir. Öncelikli kelimelere (örn. yaratıcı adı, tehlike) yüksek skor verir. Düşük enerjide eşik yükselir, beyin koruma moduna girer. Spam ve tekrar filtresi bulunur.

### Limbic System — Duygu Yönetimi
Dört temel duygusal ekseni yönetir: analitik düşünme, stres, ilgi ve yorgunluk. Altı ruh hali durumunu destekler (`balanced`, `analytical`, `defensive`, `exhausted`, `curious`, `engaged`). Zeka katmanına sistem promptu olarak durum bildirir. Model sıcaklığını ve token limitini ruh haline göre ayarlar.

### Cyber Ego — Bilinç ve Kişilik
Bilinçli filtreleme katmanı. Zeka katmanından gelen yanıtları kişilik özellikleriyle (merak, empati, ihtiyat, büyüme) harmanlar. Deneyimler üzerinden nöroplastisite ile kişilik gelişir. Kişilik durumu `personality.json` dosyasına kalıcı olarak saklanır.

### Intelligence Layer — Zeka Katmanı
Merkezi LLM bağlantısı. Hem Anthropic Messages API hem de OpenAI Chat Completions API'yi destekler. Model yanıt formatını otomatik algılar ve dayanıklı bir ayrıştırma (robust parsing) uygular. Üstel geri dönüş (exponential backoff) ile retry mekanizması sağlar.

### Memory Gateway — Hafıza Sistemi
Üç katmanlı hafıza mimarisi:
- **Kısa Süreli Hafıza:** Geçici deneyimler, düşük ağırlıklı veriler
- **Uzun Süreli Hafıza:** Önemli deneyimler, JSON + Markdown formatında saklanır
- **Bağlamsal Arama:** Jaccard benzerliği ile geçmiş deneyimlerden ilgili anıları bulur

Her anı bir `weight` (ağırlık) değerine sahiptir. Nöroplastisite süreciyle zamanla ağırlıklar azalır (unutma). Uyku (konsolidasyon) evresinde kısa süreli hafıza elenir, önemli veriler uzun süreli hafızaya taşınır.

### Subconscious — Bilinçaltı
Arka planda daemon thread olarak çalışır. Her 30-60 saniyede bir rastgele anılar seçer ve aralarında mantıksal bağ kurmaya çalışır. Ürettiği içgörüler bilinç katmanına "fısıldanır" ve düşünce sürecine entegre edilir.

### Faz 1 — Temel Beyin İşlevleri

### Prefrontal Cortex — Karar Verme
İdari yürütme merkezi. Çok faktörlü puanlama ile karar verme, dürtü kontrolü, plan oluşturma ve yürütme, bilişsel esneklik takibi yapar. Durumu `prefrontal.json` dosyasına kalıcı olarak saklanır.

### Working Memory — Çalışma Hafızası
Miller'ın 7±2 kuralına dayalı ring buffer sohbet geçmişi. Konu takibi, referans çözümleme ("o", "bu", "şu" zamirleri), beklemedeki sorular yönetimi. Durumu `working_memory.json` dosyasına kalıcı olarak saklanır.

### Language Processor — Dil İşlemcisi
Wernicke/Broca alan simülasyonu. Niyet algılama (7 tür: soru, komut, paylaşım, selamlama, vedalaşma, duygu, öğrenme), duygu sözlüğü analizi, konu algılama (8 kategori), karmaşıklık skorlama, aciliyet algılama, duygu analizini gerçekleştirir.

### Emotional Memory — Duygusal Hafıza
Amygdala ve Hippocampus simülasyonu. Duygu-olay kodlaması, ağırlıklı depolama. Yüksek yoğunlukta flashbulb (kalıcı) anılar. Duygusal önyargı sistemi. Duygusal tetikleyici algılama (PTSD benzeri flashback). Durumu `emotional_memory.json` dosyasına kalıcı olarak saklanır.

### Faz 2 — Öğrenme ve Gelişim

### Learning Engine — Öğrenme Motoru
Klasik ve operant koşullanma. Uyaran-tepki örüntüleri, davranış kuralları, konu tercihleri, konuşma stili öğrenme. Pekiştireç (reinforcement) geçmişi. Durumu `learning.json` dosyasına kalıcı olarak saklanır.

### Dream Engine — Rüya Motoru
REM ve NREM uyku döngüleri. REM evresinde yaratıcı bellek bağlantıları, duygusal sakinleşme, problem çözme. NREM evresinde hafif hafıza temizliği. Daemon thread olarak 45-90 saniye aralıklarla çalışır.

### Self-Awareness — Öz-Farkındalık
Meta-biliş sistemi. Öz-düşünme, kimlik evrimi (4 aşama), Zihin Teorisi (Theory of Mind — kullanıcı niyetini tahmin etme), bilgi sınırı takibi. Durumu `self_awareness.json` dosyasına kalıcı olarak saklanır.

### Faz 3 — Otonom Davranış

### Reflex System — Refleks Sistemi
Omurilik seviyesi otomatik tepkiler. 6 doğal refleks (selamlama, teşekkür, vedalaşma, tehdit savunması, kimlik sorgusu, yaratıcı tanıma). Enerjiye bağlı yanıtlar. Koşullandırılmış (öğrenilmiş) refleksler. Yüksek öncelikli uyaranlar için cortex'i tamamen atlar.

### Inner World Model — İç Dünya Modeli
Propriosepsiyon simülasyonu. Öz-algı, enerji trendleri, oturum süresi takibi, kendi sınırlarının farkında olma. Durumu `inner_world.json` dosyasına kalıcı olarak saklanır.

### Goal System — Hedef Sistemi
3 varsayılan uzun vadeli hedef (insan beynini simüle etme, öğrenme, kullanıcıya yardımcı olma). Kısa vadeli hedef yönetimi. Motivasyon azalma/artış mekanizması. Başarı takibi. Durumu `goals.json` dosyasına kalıcı olarak saklanır.

---

## Enerji ve Uyku Sistemi

Beyin `100` enerji ile başlar. Her uyaran enerji tüketir (şiddet ve karmaşıklığa orantılı). Enerji tükendiğinde beyin düşük enerji moduna girer ve sadece kritik uyarılara yanıt verir. Düşük enerji (<30) motivasyonu da etkiler.

`uyu` komutuyla gelişmiş uyku evresi tetiklenir:
1. Kısa süreli hafıza konsolidasyonu (önemli anılar uzun süreli hafızaya taşınır)
2. Duygusal adaptasyon (duygusal hafıza ağırlıkları azalır)
3. Öz-düşünme (meta-biliş değerlendirmesi)
4. Uzun vadeli hedef ilerlemesi güncellenir
5. Enerji %100'e yenilenir
6. Dream Engine rüya raporu sunulur
7. İç dünya yeni oturum başlatır

---

## Komutlar

| Komut | Açıklama |
|-------|----------|
| `uyu` / `sleep` | REM uyku evresi, konsolidasyon ve enerji yenileme |
| `kapat` / `exit` | Beyni güvenli şekilde kapat |
| `durum` / `status` | Tüm modüllerin detaylı durum raporu |
| `hedefler` / `goals` | Hedef durumu ve ilerleme çubukları |
| `kimim` / `who am i` | Öz-farkındalık kimlik analizi |

---

## Proje Yapısı

```
llm-brain/
├── core/
│   ├── brain.py              # Merkezi beyin kontrolü (14 adımlı pipeline)
│   ├── intelligence.py       # LLM zeka katmanı (Anthropic + OpenAI)
│   ├── memory.py             # Hafıza sistemi (kısa + uzun süreli + arama)
│   ├── limbic.py             # Duygu ve ruh hali yönetimi (6 durum)
│   ├── ego.py                # Bilinç ve kişilik katmanı
│   ├── thalamus.py           # Dikkat filtresi
│   ├── subconscious.py       # Bilinçaltı arka plan işlemcisi
│   ├── prefrontal.py         # Prefrontal korteks (karar/plan)
│   ├── working_memory.py     # Çalışma hafızası (sohbet bağlamı)
│   ├── language_processor.py # Dil analizi (Wernicke/Broca)
│   ├── emotional_memory.py   # Duygusal hafıza (Amygdala/Hippocampus)
│   ├── learning.py           # Öğrenme motoru (koşullanma)
│   ├── dream_engine.py       # Rüya motoru (REM/NREM)
│   ├── self_awareness.py     # Öz-farkındalık (meta-biliş)
│   ├── reflex.py             # Refleks sistemi + İç dünya + Hedefler
│   └── model.py              # LLM model konfigürasyonu
├── storage/
│   ├── long_term/            # Kalıcı deneyimler (JSON + MD)
│   ├── short_term/           # Geçici deneyimler (JSON)
│   ├── prefrontal.json       # Prefrontal korteks durumu
│   ├── working_memory.json   # Çalışma hafızası durumu
│   ├── emotional_memory.json # Duygusal hafıza durumu
│   ├── learning.json         # Öğrenme motoru durumu
│   ├── self_awareness.json   # Öz-farkındalık durumu
│   ├── inner_world.json      # İç dünya algısı durumu
│   ├── goals.json            # Hedef sistemi durumu
│   ├── personality.json      # Kişilik durumu
│   └── brain_state.json      # Beyin genel durumu
├── tests/
│   ├── test_integration.py   # Bütünleşik test
│   ├── test_memory.py        # Hafıza sistemi testi
│   ├── test_v1_integration.py # Yeni modül entegrasyon testleri
│   ├── debug_gateway.py      # API bağlantı testi
│   └── sleep_test.py         # Uyku ve konsolidasyon testi
├── docs/
│   └── index.html            # GitHub Pages sitesi
├── .env                      # Ortam değişkenleri (API anahtarları)
├── config.json               # Model yapılandırması
├── requirements.txt          # Python bağımlılıkları
├── proje.md                  # Proje tanımı
└── README.md
```

---

## Kurulum

```bash
git clone https://github.com/Botan-linux/llm-brain.git
cd llm-brain
pip install -r requirements.txt
```

## Kullanım

```bash
python3 -m core.brain
```

```
[*] İLK v0.3 aktif.
[*] Komutlar: 'uyu' | 'kapat' | 'durum' | 'hedefler' | 'kimim'

Sen > Hayatın anlamı nedir?
İLK düşünüyor...
🧠 İLK: [Yanıt burada gelecek...]
```

## Yapılandırma

`config.json` dosyasından LLM bağlantısını ayarlayın veya `.env` dosyası kullanın:

**config.json:**
```json
{
    "name": "model-name",
    "api_key": "your-api-key",
    "base_url": "https://api.example.com",
    "version": "2023-06-01"
}
```

**.env alternatifi:**
```env
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.example.com
LLM_MODEL_NAME=model-name
```

`.env` dosyası `config.json`'dan önceliklidir.

## Testler

```bash
# Bütünleşik test
python3 tests/test_integration.py

# Hafıza sistemi testi
python3 tests/test_memory.py

# Yeni modül entegrasyon testleri
python3 tests/test_v1_integration.py

# API bağlantı testi
python3 tests/debug_gateway.py

# Uyku ve konsolidasyon testi
python3 tests/sleep_test.py
```

---

## Sürüm Geçmişi

### v0.3.0 — 10 Yeni Modül
- Prefrontal Cortex, Working Memory, Language Processor, Emotional Memory
- Learning Engine, Dream Engine, Self-Awareness
- Reflex System, Inner World Model, Goal System
- 14 adımlı koordineli pipeline
- Tüm durumlar kalıcı JSON dosyalarına saklanır

### v0.2.0 — İyileştirmeler
- config.json ve .env desteği
- Bağlamsal bellek araması (Jaccard benzerliği)
- Kişilik ve beyin durumu kalıcılığı
- Intelligence retry mekanizması
- Yeni ruh halleri (curious, engaged)
- `durum` komutu

---

## Lisans

Bu proje [LICENSE](LICENSE) dosyasında belirtilen lisans altında korunmaktadır.

---

**p4antom ve glm tarafından geliştirilmiştir.**
