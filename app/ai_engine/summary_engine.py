from pydantic import BaseModel

from app.ai_engine.schemas import (
    PatientContext,
    ExtractedEntities,
    RiskAssessment,
)


class ClinicalSummary(BaseModel):
    summary: str


class ClinicalSummaryGenerator:

    def generate(
        self,
        patient: PatientContext,
        entities: ExtractedEntities,
        risk: RiskAssessment,
    ) -> ClinicalSummary:

        age = (
            f"{patient.age}-year-old"
            if patient.age
            else "Patient"
        )

        gender = patient.gender or ""

        symptoms = (
            ", ".join(entities.symptoms)
            if entities.symptoms
            else "no reported symptoms"
        )

        history = (
            ", ".join(patient.medical_history)
            if patient.medical_history
            else "No significant medical history"
        )

        summary = (
            f"{age} {gender} presented with {symptoms}. "
            f"Past medical history: {history}. "
            f"Overall clinical risk is {risk.overall_risk}."
        )

        return ClinicalSummary(summary=summary)