import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.ai_engine.orchestrator import ClinicalAIEngine
from app.database.connection import engine
from app.schemas.ai_response import AIResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Clinical AI Engine",
    description="""
Production-ready Clinical Decision Support System

Features
- Patient Context Intelligence
- Medical Entity Extraction
- Retrieval-Augmented Generation (RAG)
- Multi-Agent Clinical Reasoning
- Emergency Detection
- Risk Assessment
- Medication Safety
- Explainable AI
- Clinical Summary
- Confidence Scoring
- Multimodal Input Support
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

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


@app.get("/")
def home():

    return {
        "status": "success",
        "service": "Clinical AI Engine",
        "version": "1.0.0",
    }


@app.get("/ready")
def ready():

    return {
        "status": "ready",
    }


@app.get("/health")
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


@app.get("/ai/test")
def ai_test():

    return ai_engine.process(
        message="Patient has fever and cough for 3 days",
        patient_id=1,
    )


@app.post(
    "/ai/analyze",
    response_model=AIResponse,
)
def analyze(request: ChatRequest):

    if (
        not request.message
        and not request.file_name
    ):

        raise HTTPException(
            status_code=400,
            detail="Either message or file is required.",
        )

    logger.info(
        "Received Clinical AI Request"
    )

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

        logger.exception(
            "Clinical AI failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )