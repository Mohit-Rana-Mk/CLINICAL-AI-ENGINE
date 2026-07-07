from pydantic import BaseModel


class AIResponse(BaseModel):
    status: str
    patient_context: dict
    entities: dict
    emergency: dict
    follow_up_questions: dict
    risk_assessment: dict
    recommendation: dict
    confidence: dict