from pydantic import BaseModel
from datetime import datetime, UTC

from app.ai_engine.schemas import (
    ExtractedEntities,
    PatientContext,
    RiskAssessment,
)


class ClinicalSummary(BaseModel):
    summary: str


class ClinicalSummaryGenerator:
    """
    Generates a physician-ready clinical summary
    with longitudinal patient information.
    """

    def generate(
        self,
        patient: PatientContext,
        entities: ExtractedEntities,
        risk: RiskAssessment,
        patient_memory: dict | None = None,
        personalization: dict | None = None,
    ) -> ClinicalSummary:

        patient_memory = patient_memory or {}
        personalization = personalization or {}

        age = (
            f"{patient.age} years"
            if patient.age is not None
            else "Unknown"
        )

        gender = patient.gender or "Unknown"

        symptoms = (
            ", ".join(entities.symptoms)
            if entities.symptoms
            else "None"
        )

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

        previous_symptoms = ", ".join(
            str(symptom)
            for symptom in patient_memory.get("symptoms", [])
        ) or "None"

        diagnoses = []

        for item in patient_memory.get("diagnoses", []):
            if isinstance(item, str):
                diagnoses.append(item)
            elif isinstance(item, dict):
                diagnoses.append(item.get("condition", str(item)))
            else:
                diagnoses.append(str(item))

        previous_diagnoses = ", ".join(diagnoses) if diagnoses else "None"

        recommendations = []

        for item in patient_memory.get("recommendations", []):
            if isinstance(item, str):
                recommendations.append(item)

            elif isinstance(item, dict):

                if "immediate_action" in item:
                    recommendations.append(item["immediate_action"])
                else:
                    recommendations.append(str(item))

            else:
                recommendations.append(str(item))

        previous_recommendations = (
            ", ".join(recommendations)
            if recommendations
            else "None"
        )

        lifestyle = "\n".join(
            str(item)
            for item in personalization.get("lifestyle", [])
        ) or "None"

        preventive = "\n".join(
            str(item)
            for item in personalization.get("preventive_care", [])
        ) or "None"

        alerts = "\n".join(
            str(item)
            for item in personalization.get("alerts", [])
        ) or "None"

        risk_factor_lines = []

        for factor in (risk.risk_factors or []):

                if hasattr(factor, "factor"):

                    risk_factor_lines.append(
                    f"- {factor.factor} ({factor.impact})"
                )

                elif isinstance(factor, dict):

                    risk_factor_lines.append(
                    f"- {factor.get('factor')} ({factor.get('impact')})"
                )

        risk_factor_text = "\n".join(risk_factor_lines)

        if not risk_factor_text:
            risk_factor_text = "None"

        summary = f"""
==============================
CLINICAL SUMMARY
==============================

Generated: {datetime.now(UTC).isoformat(timespec="seconds")}

PATIENT
-------
Age: {age}
Gender: {gender}

CURRENT VISIT
-------------
Symptoms: {symptoms}
Duration: {entities.duration or "Unknown"}
Severity: {entities.severity or "Unknown"}
Location: {entities.body_location or "Unknown"}

MEDICAL HISTORY
---------------
{history}

CURRENT MEDICATIONS
-------------------
{medications}

KNOWN ALLERGIES
---------------
{allergies}

PREVIOUS CLINICAL HISTORY
-------------------------
Previous Symptoms:
{previous_symptoms}

Previous Diagnoses:
{previous_diagnoses}

Previous Recommendations:
{previous_recommendations}

VITALS
------
Temperature: {vitals.get("temperature", "Unknown")}
Pulse: {vitals.get("pulse", "Unknown")}
Blood Pressure: {vitals.get("blood_pressure", "Unknown")}
SpO₂: {vitals.get("spo2", "Unknown")}

LAB REPORTS
-----------
HbA1c: {labs.get("hba1c", "Unknown")}
Glucose: {labs.get("glucose", "Unknown")}
Hemoglobin: {labs.get("hemoglobin", "Unknown")}

RISK ASSESSMENT
---------------
Overall Risk: {risk.overall_risk or "Unknown"}
Risk Score: {risk.risk_score if risk.risk_score is not None else 0}/100

Heart Risk: {risk.heart_risk}
Respiratory Risk: {risk.respiratory_risk}
Neurological Risk: {risk.neurological_risk}
Infection Risk: {risk.infection_risk}

RISK FACTORS
------------
{risk_factor_text}

PERSONALIZED LIFESTYLE
----------------------
{lifestyle}

PREVENTIVE CARE
---------------
{preventive}

PERSONALIZED ALERTS
-------------------
{alerts}

CLINICAL IMPRESSION
-------------------
Current reported symptoms:

{symptoms}

Overall AI-assessed clinical risk is
{risk.overall_risk}.

This report incorporates longitudinal
patient history and previous encounters
to improve clinical reasoning.

This system is intended to support,
not replace, physician judgment.
""".strip()

        return ClinicalSummary(
            summary=summary
        )