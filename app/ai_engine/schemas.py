from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ==========================================================
# Patient Context
# ==========================================================

class PatientContext(BaseModel):

    patient_id: Optional[int] = None

    age: Optional[int] = None

    gender: Optional[str] = None

    medical_history: List[str] = Field(default_factory=list)

    medications: List[str] = Field(default_factory=list)

    allergies: List[str] = Field(default_factory=list)

    vitals: Dict[str, Any] = Field(default_factory=dict)

    lab_reports: Dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# Entity Extraction
# ==========================================================

class ExtractedEntities(BaseModel):

    symptoms: List[str] = Field(default_factory=list)

    duration: Optional[str] = None

    severity: Optional[str] = None

    body_location: Optional[str] = None

    temperature: Optional[str] = None

    associated_symptoms: List[str] = Field(default_factory=list)


# ==========================================================
# Emergency
# ==========================================================

    # --- Day 7 additions ---
    family_history: List[str] = []

    smoking_status: Optional[str] = None  # e.g. "current smoker", "ex-smoker", "non-smoker"

    alcohol_use: Optional[str] = None     # e.g. "occasional drinker", "heavy drinker", "non-drinker"

    travel_history: List[str] = []        # e.g. ["Rajasthan", "Delhi"]

    lifestyle_factors: List[str] = []     # e.g. ["sedentary", "desk job", "no exercise"]

    pregnancy_status: Optional[str] = None

    occupation: Optional[str] = None

class EmergencyAssessment(BaseModel):

    is_emergency: bool = False

    level: str = "NONE"

    reason: str = ""

    recommendation: str = ""

    detected_patterns: List[str] = Field(default_factory=list)


# ==========================================================
# Follow Up
# ==========================================================

class FollowUpQuestions(BaseModel):

    questions: List[str] = Field(default_factory=list)


# ==========================================================
# Risk Assessment
# ==========================================================

class RiskFactor(BaseModel):

    factor: str

    impact: str

    weight: int


class RiskAssessment(BaseModel):

    overall_risk: str

    heart_risk: str

    respiratory_risk: str

    infection_risk: str

    neurological_risk: str

    risk_score: int

    risk_factors: List[RiskFactor] = Field(default_factory=list)


# ==========================================================
# Medication
# ==========================================================

class MedicationAlertItem(BaseModel):

    medication: str

    alert_type: str

    severity: str

    message: str

    source: str = "Clinical Medication Rules"


class MedicationAlert(BaseModel):

    has_alert: bool

    alert_count: int = 0

    alerts: List[MedicationAlertItem] = Field(default_factory=list)

    summary: str = ""


# ==========================================================
# Recommendation
# ==========================================================

class Recommendation(BaseModel):

    immediate_action: str

    precautions: List[str] = Field(default_factory=list)

    monitoring: List[str] = Field(default_factory=list)

    doctor_visit: str

    lifestyle: List[str] = Field(default_factory=list)


# ==========================================================
# Explainability
# ==========================================================

class ClinicalReasoning(BaseModel):

    finding: str

    evidence: str

    impact: str


class Explanation(BaseModel):

    reasoning: List[ClinicalReasoning] = Field(default_factory=list)

    clinical_summary: str


# ==========================================================
# Summary
# ==========================================================

class ClinicalSummary(BaseModel):

    summary: str


# ==========================================================
# Confidence
# ==========================================================

class ConfidenceResult(BaseModel):

    confidence_score: int

    confidence_level: str

    reasons: List[str] = Field(default_factory=list)


# ==========================================================
# Final API Response
# ==========================================================

class ClinicalAIResponse(BaseModel):

    status: str

    patient_context: Dict[str, Any]

    entities: Dict[str, Any]

    agents: Dict[str, Any] = Field(default_factory=dict)

    emergency: Dict[str, Any]

    risk_assessment: Dict[str, Any]

    recommendation: Dict[str, Any]

    medication_alerts: Dict[str, Any]

    explanation: Dict[str, Any]

    clinical_summary: Dict[str, Any]

    confidence: Dict[str, Any]

    follow_up_questions: Dict[str, Any] = Field(default_factory=dict)

    rag: Dict[str, Any] = Field(default_factory=dict)

    pipeline: Dict[str, Any] = Field(default_factory=dict)

    timestamp: Optional[str] = None