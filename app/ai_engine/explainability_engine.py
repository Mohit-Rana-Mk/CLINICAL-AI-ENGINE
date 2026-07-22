from pydantic import BaseModel

from app.ai_engine.schemas import (
    PatientContext,
    ExtractedEntities,
    EmergencyAssessment,
    RiskAssessment,
)



class ClinicalReasoning(BaseModel):

    finding: str

    evidence: str

    impact: str




class Explanation(BaseModel):

    reasoning: list[ClinicalReasoning]

    clinical_summary: str




class ExplainabilityEngine:
    """
    Explainable Clinical Reasoning Engine.

    Converts clinical decisions into
    human-readable reasoning.
    """



    def generate(
        self,
        patient: PatientContext,
        entities: ExtractedEntities,
        emergency: EmergencyAssessment | dict,
        risk: RiskAssessment | dict,
    ) -> Explanation:

        patient = patient or PatientContext()
        entities = entities or ExtractedEntities()

        emergency = emergency or {}
        risk = risk or {}

        reasoning = []



        # =====================================
        # Normalize Emergency Object
        # =====================================

        if isinstance(emergency, dict):

            emergency_status = emergency.get(
                "is_emergency",
                False
            )

            emergency_level = emergency.get(
                "level",
                "UNKNOWN"
            )

            emergency_reason = emergency.get(
                "reason",
                "Emergency assessment generated"
            )


        else:

            emergency_status = emergency.is_emergency

            emergency_level = emergency.level

            emergency_reason = emergency.reason




        # =====================================
        # Normalize Risk Object
        # =====================================

        if isinstance(risk, dict):

            risk_level = risk.get(
                "overall_risk",
                "UNKNOWN"
            )

            risk_score = risk.get(
                "risk_score",
                0
            )


        else:

            risk_level = risk.overall_risk

            risk_score = risk.risk_score




        # =====================================
        # Symptoms
        # =====================================

        symptoms = [

            symptom.lower()

            for symptom in getattr(entities, "symptoms", [])

        ]



        if "chest pain" in symptoms:

            reasoning.append(

                ClinicalReasoning(

                    finding="Chest pain",

                    evidence="Reported patient symptom",

                    impact=(
                        "High priority symptom requiring "
                        "cardiovascular emergency evaluation."
                    )

                )

            )



        if "breathing difficulty" in symptoms or "shortness of breath" in symptoms:

            reasoning.append(

                ClinicalReasoning(

                    finding="Breathing difficulty",

                    evidence="Reported patient symptom",

                    impact=(
                        "May indicate serious cardiac or "
                        "respiratory involvement."
                    )

                )

            )




        # =====================================
        # Medical History
        # =====================================

        if patient.medical_history:

            for condition in patient.medical_history:

                reasoning.append(

                    ClinicalReasoning(

                        finding=condition,

                        evidence="Patient medical history",

                        impact=(
                            "Additional clinical risk "
                            "factor considered."
                        )

                    )

                )




        # =====================================
        # Allergies
        # =====================================

        if patient.allergies:

            for allergy in patient.allergies:

                reasoning.append(

                    ClinicalReasoning(

                        finding=f"Allergy: {allergy}",

                        evidence="Patient allergy records",

                        impact=(
                            "Medication selection should "
                            "consider allergy history."
                        )

                    )

                )




        # =====================================
        # Emergency Reasoning
        # =====================================

        if emergency_status:

            reasoning.append(

                ClinicalReasoning(

                    finding=(
                        f"Emergency classification: "
                        f"{emergency_level}"
                    ),

                    evidence=emergency_reason,

                    impact=(
                        "Immediate medical evaluation "
                        "recommended."
                    )

                )

            )




        # =====================================
        # Risk Reasoning
        # =====================================

        reasoning.append(

            ClinicalReasoning(

                finding=(
                    f"Overall risk: {risk_level}"
                ),

                evidence=(
                    f"Risk score calculated as "
                    f"{risk_score}/100"
                ),

                impact=(
                    "Determines urgency and "
                    "recommendation priority."
                )

            )

        )




        # =====================================
        # Summary
        # =====================================

        symptom_text = (

            ", ".join(
                entities.symptoms
            )

            if entities.symptoms

            else "no symptoms"

        )


        summary = (

            f"The patient presents with {symptom_text}. "

            f"Clinical assessment identified "
            f"{risk_level} risk. "

            f"Emergency status: "
            f"{'Detected' if emergency_status else 'Not detected'}."

        )



        return Explanation(

            reasoning=reasoning,

            clinical_summary=summary

        )