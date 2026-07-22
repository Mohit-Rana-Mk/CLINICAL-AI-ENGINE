import logging
import os
import shutil
import uuid

from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.ai_engine.orchestrator import ClinicalAIEngine
from app.database.connection import engine
from app.schemas.ai_response import AIResponse
from app.api.routes import nlp as nlp_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="HealTrack Clinical AI Engine",
    description="""
### Enterprise-Grade Clinical Decision Support & Multimodal AI Microservice

The HealTrack Clinical AI Engine combines deterministic medical protocols (WHO, NICE) with state-of-the-art NLP, RAG, and Multi-Agent reasoning to assist healthcare providers and power intelligent chatbot experiences.

#### 🚀 Core Capabilities
* **Multimodal Intelligence:** Automated routing and parsing for Text, Voice (.wav/.mp3), Medical Images (Skin, Eye, X-Ray), and Clinical Documents (Prescriptions/Lab Reports via PaddleOCR).
* **Evidence-Based RAG:** Semantic vector retrieval powered by Qdrant, referencing trusted global medical guidelines.
* **Longitudinal Memory:** Patient-specific profile tracking, multi-turn conversation history, and clinical timelines.
* **Safety & Compliance:** Built-in medication allergy checking, drug interaction warnings, and automated audit logging.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "System Status",
            "description": "Liveness, readiness, and database health check probes."
        },
        {
            "name": "Clinical AI Core",
            "description": "Primary clinical analysis endpoints for text consultation and multi-agent reasoning."
        },
        {
            "name": "Multimodal Processing",
            "description": "Specialized endpoints for ingesting Voice audio, Medical Images, and OCR Documents."
        },
        {
            "name": "Patient Analytics & History",
            "description": "Longitudinal patient data retrieval including chat history, clinical timelines, and summaries."
        },
        {
            "name": "NLP Subsystem",
            "description": "Dedicated microservice routes for Richa's multilingual NLP pipeline and translation."
        }
    ]
)

# ── NLP Engine Routes (Richa's pipeline) ──────────────────────────────────────
app.include_router(nlp_router.router)

ai_engine = ClinicalAIEngine()


class ChatRequest(BaseModel):
    message: str | None = Field(
        default=None,
        description="Clinical message",
    )
    patient_id: int | None = Field(
        default=None,
        ge=1,
    )
    file_name: str | None = None
    mime_type: str | None = None


@app.get("/", tags=["System Status"])
def home():
    return {
        "status": "success",
        "service": "Clinical AI Engine",
        "version": "1.0.0",
    }


@app.get("/ready", tags=["System Status"])
def ready():
    return {
        "status": "ready",
    }


@app.get("/health", tags=["System Status"])
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "engine": "ready",
        }
    except SQLAlchemyError as error:
        logger.exception("Health check failed")
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


@app.get("/ai/test", tags=["Clinical AI Core"])
def ai_test():
    return ai_engine.process(
        message="Patient has fever and cough for 3 days",
        patient_id=1,
    )


@app.post(
    "/ai/analyze",
    tags=["Clinical AI Core"],
    response_model=AIResponse,
)
def analyze(request: ChatRequest):
    if not request.message and not request.file_name:
        raise HTTPException(
            status_code=400,
            detail="Either message or file is required.",
        )

    logger.info("Received Clinical AI Request")
    try:
        result = ai_engine.process(
            message=request.message,
            patient_id=request.patient_id,
            file_name=request.file_name,
            mime_type=request.mime_type,
        )

        if result.get("status") == "error":
            raise HTTPException(
                status_code=500,
                detail=result.get(
                    "message",
                    "Clinical AI failed.",
                ),
            )

        return result

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Clinical AI failed")
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ==========================================================
# File Upload Helper
# ==========================================================
async def _save_temp_file(file: UploadFile) -> str:
    """Safely saves an uploaded file while preserving the original name for the AI routers."""
    safe_filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
    
    with open(safe_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return safe_filename


# ==========================================================
# Multimodal Endpoints
# ==========================================================

@app.post("/ai/voice", tags=["Multimodal Processing"], response_model=AIResponse)
async def process_voice(patient_id: int = Form(None), file: UploadFile = File(...)):
    """Transcribe and analyze patient voice audio."""
    temp_path = await _save_temp_file(file)
    try:
        result = ai_engine.process(
            patient_id=patient_id, 
            file_name=temp_path, 
            mime_type=file.content_type
        )
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Voice processing failed."))
        return result
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/ai/image", tags=["Multimodal Processing"], response_model=AIResponse)
async def process_image(patient_id: int = Form(None), file: UploadFile = File(...)):
    """Analyze medical images (Skin, Eye, X-Ray, etc.)."""
    temp_path = await _save_temp_file(file)
    try:
        result = ai_engine.process(
            patient_id=patient_id, 
            file_name=temp_path, 
            mime_type=file.content_type
        )
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "Image processing failed."))
        return result
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/ai/ocr", tags=["Multimodal Processing"], response_model=AIResponse)
async def process_ocr(patient_id: int = Form(None), file: UploadFile = File(...)):
    """Extract and analyze text from Lab Reports or Prescriptions."""
    temp_path = await _save_temp_file(file)
    try:
        result = ai_engine.process(
            patient_id=patient_id, 
            file_name=temp_path, 
            mime_type=file.content_type
        )
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message", "OCR processing failed."))
        return result
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# ==========================================================
# Granular Patient Data Endpoints
# ==========================================================

@app.get("/ai/timeline/{patient_id}", tags=["Patient Analytics & History"])
def get_timeline(patient_id: int):
    """Retrieve the generated clinical timeline for a patient."""
    history = ai_engine.pipeline.conversation_memory.get_history(patient_id)
    memory = ai_engine.pipeline.patient_memory.get(patient_id)
    
    timeline = ai_engine.pipeline.timeline_builder.build(history, memory)
    stats = ai_engine.pipeline.timeline_builder.statistics(timeline)
    
    return {
        "status": "success",
        "patient_id": patient_id,
        "timeline": timeline,
        "timeline_statistics": stats
    }


@app.get("/ai/history/{patient_id}", tags=["Patient Analytics & History"])
def get_history(patient_id: int, limit: int = 50):
    """Retrieve the conversational chat history."""
    history = ai_engine.pipeline.conversation_memory.get_recent_messages(patient_id, limit=limit)
    stats = ai_engine.pipeline.conversation_memory.summary(patient_id)
    
    return {
        "status": "success",
        "patient_id": patient_id,
        "conversation_history": history,
        "summary": stats
    }


@app.get("/ai/summary/{patient_id}", tags=["Patient Analytics & History"])
def get_summary(patient_id: int):
    """Retrieve the stored longitudinal patient memory and summary."""
    memory = ai_engine.pipeline.patient_memory.get(patient_id)
    summary_stats = ai_engine.pipeline.patient_memory.summary(patient_id)
    
    return {
        "status": "success",
        "patient_id": patient_id,
        "patient_memory": memory,
        "memory_statistics": summary_stats
    }


@app.get("/ai/recommendations/{patient_id}", tags=["Patient Analytics & History"])
def get_recommendations(patient_id: int):
    """Retrieve the latest clinical recommendations generated for the patient."""
    memory = ai_engine.pipeline.patient_memory.get(patient_id)
    recommendations = memory.get("recommendations", [])
    latest_recommendation = recommendations[-1] if recommendations else None
    
    return {
        "status": "success",
        "patient_id": patient_id,
        "latest_recommendation": latest_recommendation,
        "all_recommendations": recommendations
    }


# ==========================================================
# Custom OpenAPI Schema Configuration
# ==========================================================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="HealTrack Clinical AI Engine",
        version="1.0.0",
        description="Production-grade Clinical Decision Support System",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi