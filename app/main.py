from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.database.connection import engine
from app.ai_engine.orchestrator import ClinicalAIEngine
from app.schemas.ai_response import AIResponse
from app.api.routes import nlp as nlp_router

import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Clinical AI Engine",
    version="1.0.0"
)

# ── NLP Engine Routes (Richa's pipeline) ──────────────────────────────────────
app.include_router(nlp_router.router)

ai_engine = ClinicalAIEngine()


class ChatRequest(BaseModel):
    message: str
    patient_id: int |None = None


@app.get("/")
def home():
    return {
        "message": "Clinical AI Engine Running",
        "status": "success"
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "Connected Successfully",
            "status": "Healthy"
        }

    except SQLAlchemyError as e:
        logger.exception("Database Health Check Failed")

        raise HTTPException(
            status_code=500,
            detail=f"Database Error: {str(e)}"
        )


@app.get("/ai/test")
def ai_test():
    return ai_engine.process(
        "fever and cough",
        patient_id=1
    )


@app.post(
    "/ai/analyze",
    response_model=AIResponse
)
def analyze(req: ChatRequest):

    try:
        logger.info(f"Received request for patient {req.patient_id}")

        result = ai_engine.process(
            message=req.message,
            patient_id=req.patient_id
        )

        logger.info("AI pipeline completed successfully")

        return result

    except Exception as e:
        logger.exception("AI Pipeline Failed")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )