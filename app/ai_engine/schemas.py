from typing import List, Optional

from pydantic import BaseModel


class PatientContext(BaseModel):
    patient_id: Optional[int] = None

    age: Optional[int] = None

    gender: Optional[str] = None

    medical_history: List[str] = []

    medications: List[str] = []

    allergies: List[str] = []

    vitals: dict = {}

    lab_reports: dict = {}

class ExtractedEntities(BaseModel):
    symptoms: List[str] = []

    duration: Optional[str] = None

    severity: Optional[str] = None

    body_location: Optional[str] = None

    temperature: Optional[str] = None

    associated_symptoms: List[str] = []

class EmergencyAssessment(BaseModel):
    is_emergency: bool = False

    level: str = "NONE"

    reason: str = ""

    recommendation: str = ""

class FollowUpQuestions(BaseModel):
    questions: List[str] = []

class RiskAssessment(BaseModel):
    overall_risk: str

    heart_risk: str

    respiratory_risk: str

    infection_risk: str

    neurological_risk: str

    risk_score: int

class Recommendation(BaseModel):
    immediate_action: str

    precautions: List[str]

    monitoring: List[str]

    doctor_visit: str

    lifestyle: List[str]

class ConfidenceResult(BaseModel):

    confidence_score: int

    confidence_level: str

    reasons: list[str]