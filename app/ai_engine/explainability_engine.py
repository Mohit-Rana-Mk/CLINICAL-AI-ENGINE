from pydantic import BaseModel

from app.ai_engine.schemas import (
    PatientContext,
    ExtractedEntities,
    EmergencyAssessment,
    RiskAssessment,
)


class Explanation(BaseModel):
    reasoning: list[str]
    clinical_summary: str


class ExplainabilityEngine:

    def generate(
        self,
        patient: PatientContext,
        entities: ExtractedEntities,
        emergency: EmergencyAssessment,
        risk: RiskAssessment,
    ) -> Explanation:

        reasons = []

        # -----------------------
        # Patient Context
        # -----------------------

        if patient.age is not None:
            reasons.append(
                f"Patient age: {patient.age} years."
            )

        if patient.gender:
            reasons.append(
                f"Gender: {patient.gender}."
            )

        if patient.medical_history:
            reasons.append(
                "Past medical history: " +
                ", ".join(patient.medical_history)
            )

        if patient.medications:
            reasons.append(
                "Current medications: " +
                ", ".join(patient.medications)
            )

        if patient.allergies:
            reasons.append(
                "Known allergies: " +
                ", ".join(patient.allergies)
            )

        # -----------------------
        # Symptoms
        # -----------------------

        if entities.symptoms:
            reasons.append(
                "Reported symptoms: " +
                ", ".join(entities.symptoms)
            )

        # -----------------------
        # Emergency
        # -----------------------

        if emergency.is_emergency:
            reasons.append(
                f"Emergency detected ({emergency.level})."
            )

        # -----------------------
        # Risk
        # -----------------------

        reasons.append(
            f"Overall clinical risk: {risk.overall_risk}."
        )

        summary = (
            f"The patient presents with "
            f"{', '.join(entities.symptoms)}. "
            f"Overall clinical risk is {risk.overall_risk}."
        )

        return Explanation(
            reasoning=reasons,
            clinical_summary=summary,
        )