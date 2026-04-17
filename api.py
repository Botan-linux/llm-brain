"""
İLK — Yapay Beyin Simülasyonu REST API
FastAPI wrapper — v0.3.0

Endpoint'ler:
  POST   /api/chat       → Mesaj → Yanıt
  POST   /api/sleep      → Uyku modu
  GET    /api/status     → Beyin durumu (JSON)
  GET    /api/health     → Canlılık kontrolü
  GET    /api/goals      → Hedef durumu
  GET    /api/identity   → Öz-farkındalık (kimim?)
  GET    /api/memories   → Hafıza istatistikleri
  POST   /api/memories/search → Anı arama
  GET    /api/config     → LLM yapılandırması (maskelenmiş)
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from contextlib import asynccontextmanager

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.brain import ArtificialBrain


# === Global Brain Instance ===
_brain: Optional[ArtificialBrain] = None


def get_brain() -> ArtificialBrain:
    """Beyin singleton'ı döndürür. İlk erişimde oluşturur."""
    global _brain
    if _brain is None:
        _brain = ArtificialBrain()
    return _brain


# === Lifespan (başlangıç/bitiş) ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Başlangıç
    brain = get_brain()
    from core.logger import get_logger
    logger = get_logger(__name__)
    logger.info("İLK REST API başlatıldı.")
    yield
    # Bitiş
    brain.maintenance()
    logger.info("İLK REST API kapatıldı.")


# === FastAPI App ===
app = FastAPI(
    title="İLK — Yapay Beyin Simülasyonu",
    description="İnsan beyninin 16 modüllü Python simülasyonu REST API'si",
    version="0.3.0",
    lifespan=lifespan
)

# CORS — tüm kaynaklara izin ver
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Request/Response Models ===

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000, description="Kullanıcı mesajı")
    session_id: Optional[str] = Field(None, max_length=100, description="Oturum ID (opsiyonel)")


class ChatResponse(BaseModel):
    response: str
    energy: float
    mood: str
    session_turn: int


class SleepResponse(BaseModel):
    message: str
    energy: float
    session_count: int
    consolidated: int
    forgotten: int


class HealthResponse(BaseModel):
    status: str
    llm_healthy: bool
    model: str
    version: str
    uptime_info: str


class MemorySearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="Arama sorgusu")
    limit: int = Field(5, ge=1, le=50, description="Sonuç sayısı")


# === Endpoints ===

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Beyin ve LLM canlılık kontrolü."""
    brain = get_brain()
    intel_stats = brain.intelligence.get_stats()

    return HealthResponse(
        status="operational" if intel_stats["is_healthy"] else "degraded",
        llm_healthy=intel_stats["is_healthy"],
        model=intel_stats["model"],
        version="0.3.0",
        uptime_info=f"Enerji: %{brain.state['energy']:.0f} | Oturum: #{brain.state['session_count']} | Ruh Hali: {brain.limbic.current_mood}"
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Ana sohbet endpoint'i — mesajı beyne gönderir, yanıt döndürür."""
    brain = get_brain()

    # Enerji kontrolü
    if brain.state["energy"] <= 0:
        return ChatResponse(
            response="Sistem: Enerji tükendi. Konsolidasyon (uyku) gerekiyor.",
            energy=0,
            mood=brain.limbic.current_mood,
            session_turn=brain.working_memory.turn_count
        )

    response = brain.process_stimulus(request.message)

    return ChatResponse(
        response=response,
        energy=brain.state["energy"],
        mood=brain.limbic.current_mood,
        session_turn=brain.working_memory.turn_count
    )


@app.post("/api/sleep", response_model=SleepResponse)
async def sleep():
    """Beyni uyku moduna alır — hafıza konsolidasyonu + enerji yenileme."""
    brain = get_brain()

    # Konsolidasyon öncesi hafıza durumu
    mem_stats_before = brain.memory.get_stats()
    short_term_before = mem_stats_before["short_term"]

    response_text = brain.sleep()

    # Konsolidasyon sonrası
    mem_stats_after = brain.memory.get_stats()
    consolidated = short_term_before - mem_stats_after["short_term"]
    forgotten = max(0, consolidated - (mem_stats_after["long_term"] - mem_stats_before["long_term"]))

    return SleepResponse(
        message=response_text,
        energy=brain.state["energy"],
        session_count=brain.state["session_count"],
        consolidated=consolidated,
        forgotten=forgotten
    )


@app.get("/api/status")
async def status():
    """Gelişmiş beyin durumu raporu (JSON formatında)."""
    brain = get_brain()
    wm = brain.working_memory.get_stats()
    lp = brain.language_processor.get_stats()
    em = brain.emotional_memory.get_stats()
    le = brain.learning.get_stats()
    sa = brain.self_awareness.get_stats()
    rx = brain.reflex.get_stats()
    gs = brain.goals.get_motivation_summary()
    pfc = brain.prefrontal.get_stats()
    dream = brain.dream_engine.get_dream_report()
    intel = brain.intelligence.get_stats()
    mem = brain.memory.get_stats()

    return {
        "version": "0.3.0",
        "state": {
            "energy": brain.state["energy"],
            "mood": brain.limbic.current_mood,
            "development_stage": brain.limbic.development_stage,
            "session_count": brain.state["session_count"],
            "last_stimulus": brain.state["last_stimulus"],
        },
        "conversation": wm,
        "language": lp,
        "memory": mem,
        "emotional_memory": em,
        "learning": le,
        "self_awareness": sa,
        "prefrontal": pfc,
        "reflex": rx,
        "dream": dream,
        "intelligence": intel,
        "goals": gs,
    }


@app.get("/api/goals")
async def goals():
    """Hedef durumu."""
    brain = get_brain()
    gs = brain.goals.get_motivation_summary()
    return gs


@app.get("/api/identity")
async def identity():
    """Öz-farkındalık — 'Kimim?' yaniti."""
    brain = get_brain()
    identity = brain.self_awareness.answer_who_am_i()
    return identity


@app.get("/api/memories")
async def memory_stats():
    """Hafıza istatistikleri."""
    brain = get_brain()
    return brain.memory.get_stats()


@app.post("/api/memories/search")
async def memory_search(request: MemorySearchRequest):
    """Anı arama — kelime eşleşmesi ile ilgili deneyimleri bulur."""
    brain = get_brain()
    results = brain.memory.search_relevant(request.query, limit=request.limit)
    return {"query": request.query, "results": results, "count": len(results)}


@app.get("/api/config")
async def config():
    """LLM yapılandırması (api_key maskelenmiş)."""
    brain = get_brain()
    intel = brain.intelligence
    api_key = intel.api_key
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if api_key and len(api_key) > 12 else "***"

    return {
        "model": intel.model,
        "base_url": intel.base_url,
        "api_key_masked": masked_key,
        "version": intel.version,
        "total_requests": intel.request_count,
        "is_healthy": intel.is_healthy(),
        "last_error": intel.last_error,
    }


# === Devre Dışı Bırakma (production'da yorum satırı yap) ===

# @app.post("/api/shutdown")
# async def shutdown():
#     """Beyni güvenli kapatır."""
#     brain = get_brain()
#     brain.maintenance()
#     import asyncio
#     asyncio.get_event_loop().call_later(1, os._exit, 0)
#     return {"message": "İLK kapatılıyor..."}


# === Doğrudan Çalıştırma ===

if __name__ == "__main__":
    import uvicorn

    # Ortam değişkeninden port al (varsayılan: 8000)
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"\n  İLK REST API v0.3.0")
    print(f"  http://{host}:{port}")
    print(f"  Docs: http://{host}:{port}/docs")
    print(f"  ────────────────────────\n")

    uvicorn.run("api:app", host=host, port=port, reload=False)
