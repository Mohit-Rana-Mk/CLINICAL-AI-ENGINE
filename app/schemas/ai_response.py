from pydantic import BaseModel, Field

from app.ai_engine.schemas import (
    PatientContext,
    ExtractedEntities,
    EmergencyAssessment,
    FollowUpQuestions,
    RiskAssessment,
    Recommendation,
    MedicationAlert,
    Explanation,
    ClinicalSummary,
    ConfidenceResult,
)


# ==========================================
# RAG Models
# ==========================================

class RAGDocument(BaseModel):

    title: str

    category: str

    source: str

    similarity_score: float


class Citation(BaseModel):

    id: int

    title: str

    category: str

    source: str

    similarity_score: float


# ==========================================
# Final API Response
# ==========================================

class AIResponse(BaseModel):

    request_id: str

    execution_time_seconds: float

    status: str

    patient_context: PatientContext

    entities: ExtractedEntities

    rag_documents: list[RAGDocument] = Field(
        default_factory=list
    )

    rag_citations: list[Citation] = Field(
        default_factory=list
    )

    emergency: EmergencyAssessment

    follow_up_questions: FollowUpQuestions

    risk_assessment: RiskAssessment

    recommendation: Recommendation

    medication_alerts: MedicationAlert

    explanation: Explanation

    clinical_summary: ClinicalSummary

    confidence: ConfidenceResult