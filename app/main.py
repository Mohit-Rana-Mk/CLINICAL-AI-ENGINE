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
Production-ready Clinical Decision Support System.

Features

• Patient Context Intelligence

• Medical Entity Extraction

• Retrieval-Augmented Generation (RAG)

• Multi-Agent Clinical Reasoning

• Emergency Detection

• Clinical Risk Assessment

• Medication Safety Checks

• Explainable AI

• Clinical Summary Generation

• Confidence Scoring
""",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

ai_engine = ClinicalAIEngine()


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Patient clinical message",
    )

    patient_id: int | None = Field(
        default=None,
        ge=1,
        description="Patient identifier",
    )


@app.get("/")
def home():

    return {
        "status": "success",
        "service": "Clinical AI Engine",
        "version": "1.0.0",
        "message": "Clinical AI Engine is running.",
    }


@app.get("/ready")
def readiness():

    return {
        "status": "ready",
        "service": "Clinical AI Engine",
    }


@app.get("/health")
def health():

    try:

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "ai_engine": "ready",
        }

    except SQLAlchemyError as error:

        logger.exception("Database health check failed")

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(error)}",
        )


@app.get("/ai/test")
def ai_test():

    logger.info("Running AI test endpoint")

    return ai_engine.process(
        message="fever and cough",
        patient_id=1,
    )


@app.post(
    "/ai/analyze",
    response_model=AIResponse,
)
def analyze(req: ChatRequest):

    if not req.message.strip():

        raise HTTPException(
            status_code=400,
            detail="Clinical message cannot be empty.",
        )

    logger.info(
        "Received AI request | patient_id=%s",
        req.patient_id,
    )

    try:

        result = ai_engine.process(
            message=req.message.strip(),
            patient_id=req.patient_id,
        )

        if result.get("status") == "error":

            logger.error(
                "Pipeline returned error | patient_id=%s",
                req.patient_id,
            )

            raise HTTPException(
                status_code=500,
                detail=result.get(
                    "message",
                    "Clinical AI pipeline failed.",
                ),
            )

        logger.info(
            "Clinical AI pipeline completed successfully"
        )

        return result

    except HTTPException:
        raise

    except Exception as error:

        logger.exception(
            "Unexpected Clinical AI failure | patient_id=%s",
            req.patient_id,
        )

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )