from pydantic import BaseModel

from app.ai_engine.schemas import (
    PatientContext,
    ExtractedEntities,
    RiskAssessment,
)


class ClinicalSummary(BaseModel):
    summary: str


class ClinicalSummaryGenerator:
    """
    Generates a concise physician-ready clinical summary.
    """

    def generate(
        self,
        patient: PatientContext,
        entities: ExtractedEntities,
        risk: RiskAssessment,
    ) -> ClinicalSummary:

        age = (
            f"{patient.age}-year-old"
            if patient.age is not None
            else "Unknown age"
        )

        gender = patient.gender or "Unknown"

        symptoms = (
            ", ".join(entities.symptoms)
            if entities.symptoms
            else "None reported"
        )

        duration = entities.duration or "Unknown"

        severity = entities.severity or "Unknown"

        location = entities.body_location or "Not specified"

        history = (
            ", ".join(patient.medical_history)
            if patient.medical_history
            else "None"
        )

        medications = (
            ", ".join(patient.medications)
            if patient.medications
            else "None"
        )

        allergies = (
            ", ".join(patient.allergies)
            if patient.allergies
            else "None"
        )

        vitals = patient.vitals or {}

        labs = patient.lab_reports or {}

        risk_factor_lines = []

        for factor in risk.risk_factors:
            risk_factor_lines.append(
                f"- {factor.factor} ({factor.impact}, Weight {factor.weight})"
            )

        risk_factor_text = (
            "\n".join(risk_factor_lines)
            if risk_factor_lines
            else "None identified"
        )

        summary = f"""
==============================
CLINICAL SUMMARY
==============================

Patient
-------
Age: {age}
Gender: {gender}

Chief Complaint
---------------
Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}
Body Location: {location}

Past Medical History
--------------------
{history}

Current Medications
-------------------
{medications}

Known Allergies
---------------
{allergies}

Vital Signs
-----------
Temperature: {vitals.get("temperature", "Unknown")}
Pulse: {vitals.get("pulse", "Unknown")}
Blood Pressure: {vitals.get("blood_pressure", "Unknown")}
SpO₂: {vitals.get("spo2", "Unknown")}

Laboratory Findings
-------------------
HbA1c: {labs.get("hba1c", "Unknown")}
Glucose: {labs.get("glucose", "Unknown")}
Hemoglobin: {labs.get("hemoglobin", "Unknown")}

Risk Assessment
---------------
Overall Risk: {risk.overall_risk}
Heart Risk: {risk.heart_risk}
Respiratory Risk: {risk.respiratory_risk}
Infection Risk: {risk.infection_risk}
Neurological Risk: {risk.neurological_risk}
Risk Score: {risk.risk_score}/100

Risk Factors
------------
{risk_factor_text}

Clinical Impression
-------------------
The patient presents with {symptoms}.
Current AI assessment classifies the overall clinical risk as {risk.overall_risk}.
This output is intended to support, not replace, clinical judgment. Correlate with physical examination, investigations, and clinician assessment before making treatment decisions.
""".strip()

        return ClinicalSummary(
            summary=summary
        )