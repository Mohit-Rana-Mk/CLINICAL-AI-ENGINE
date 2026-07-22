import logging
from fastapi import APIRouter, HTTPException

from app.pipeline import get_clinical_pipeline
from app.schemas.nlp_request import NLPAnalyzeRequest, NLPAnalyzeResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/nlp", tags=["NLP Subsystem"])


@router.post(
    "/analyze",
    response_model=NLPAnalyzeResponse,
    summary="Analyze patient symptoms via NLP pipeline",
    description=(
        "Accepts patient text input (in any language including Hinglish), "
        "runs it through the full NLP pipeline (translation -> intent -> severity -> entity extraction), "
        "and returns a structured Clinical JSON payload plus a follow-up question."
    ),
)
def analyze(req: NLPAnalyzeRequest):
    """
    Main NLP endpoint 

    - Handles multilingual / Hinglish text automatically.
    - Returns a standardized Clinical JSON envelope.
    - Maintains per-session conversational memory for follow-up questions.
    """
    try:
        logger.info(f"NLP /analyze called | session={req.session_id} | patient={req.patient_id}")

        pipeline = get_clinical_pipeline()
        result = pipeline.process(
            text_input=req.text,
            session_id=req.session_id,
            patient_id=req.patient_id,
        )

        logger.info(f"NLP pipeline completed | session={result['metadata']['session_id']}")
        return result

    except Exception as e:
        logger.exception("NLP Pipeline failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/health",
    summary="NLP engine health check",
    description="Verifies the NLP pipeline is loaded and ready to accept requests.",
)
def nlp_health():
    """Quick liveness check for the NLP subsystem."""
    try:
        pipeline = get_clinical_pipeline()
        return {
            "status": "healthy",
            "pipeline": "ClinicalPipeline",
            "ready": pipeline is not None,
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"NLP engine not ready: {str(e)}")