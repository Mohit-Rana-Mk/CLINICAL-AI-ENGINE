from typing import Any

from pydantic import BaseModel, Field

from app.ai_engine.schemas import (
    ClinicalSummary,
    ConfidenceResult,
    EmergencyAssessment,
    Explanation,
    ExtractedEntities,
    FollowUpQuestions,
    MedicationAlert,
    PatientContext,
    Recommendation,
    RiskAssessment,
)


# ==========================================================
# RAG
# ==========================================================


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


class RAGMetadata(BaseModel):
    query: str | None = None
    documents_retrieved: int = 0
    top_k: int = 0
    execution_time_seconds: float | None = None
    error: str | None = None


class RAGResult(BaseModel):
    documents: list[RAGDocument] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    metadata: RAGMetadata = Field(default_factory=RAGMetadata)


# ==========================================================
# Pipeline
# ==========================================================


class PipelineInfo(BaseModel):
    version: str
    engine: str
    steps_completed: int | None = None
    execution_time_seconds: float | None = None
    response_metadata: dict[str, Any] | None = None


# ==========================================================
# Agents
# ==========================================================


class AgentResults(BaseModel):
    symptom_analysis: dict[str, Any] | None = None
    diagnosis_analysis: dict[str, Any] | None = None


# ==========================================================
# Timeline
# ==========================================================


class TimelineEvent(BaseModel):
    timestamp: str | None = None
    event_type: str
    role: str | None = None
    description: str


class TimelineStatistics(BaseModel):
    generated_at: str | None = None
    total_events: int = 0
    breakdown: dict[str, int] = Field(default_factory=dict)


# ==========================================================
# Patient Memory
# ==========================================================


class PatientMemory(BaseModel):
    symptoms: list[str] = Field(default_factory=list)
    diagnoses: list[str] = Field(default_factory=list)
    medications: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    risk_history: list[dict] = Field(default_factory=list)
    recommendations: list[Any] = Field(default_factory=list)
    last_updated: str | None = None


# ==========================================================
# Final Response
# ==========================================================


class AIResponse(BaseModel):

    request_id: str

    execution_time_seconds: float

    status: str

    timestamp: str | None = None

    pipeline: PipelineInfo | None = None

    patient_context: PatientContext

    entities: ExtractedEntities

    agents: AgentResults | None = None

    emergency: EmergencyAssessment

    follow_up_questions: FollowUpQuestions

    risk_assessment: RiskAssessment

    recommendation: Recommendation

    medication_alerts: MedicationAlert

    explanation: Explanation

    clinical_summary: ClinicalSummary

    confidence: ConfidenceResult

    rag: RAGResult = Field(default_factory=RAGResult)

    patient_memory: PatientMemory | None = None

    timeline: list[TimelineEvent] = Field(default_factory=list)

    timeline_statistics: TimelineStatistics | None = None

    # Operational and explainability artifacts are produced by the pipeline and
    # intentionally retained in the public response for traceability.
    input_processing: dict[str, Any] | None = None
    vision: dict[str, Any] | None = None
    image_analysis: dict[str, Any] | None = None
    reasoning: dict[str, Any] | None = None
    decision_trace: list[Any] = Field(default_factory=list)
    audit: dict[str, Any] = Field(default_factory=dict)
    patient_profile: dict[str, Any] | None = None
    conversation_history: list[dict[str, Any]] = Field(default_factory=list)
    personalization: dict[str, Any] | None = None
