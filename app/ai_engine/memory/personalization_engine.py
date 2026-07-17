import logging
from typing import Any

logger = logging.getLogger(__name__)


class PersonalizationEngine:
    """
    Production Personalization Engine.

    Generates patient-specific recommendations using:

    - Demographics
    - Medical history
    - Previous diagnoses
    - Previous symptoms
    - Risk history
    - Medications
    - Allergies
    - Lifestyle
    """

    def generate(
        self,
        patient_context,
        patient_memory: dict[str, Any],
    ) -> dict:

        recommendations = set()
        alerts = set()
        lifestyle = set()
        preventive_care = set()

        history = []

        if patient_context:

            history = [
                disease.lower()
                for disease in (
                    patient_context.medical_history or []
                )
            ]

            age = getattr(
                patient_context,
                "age",
                None,
            )

            gender = getattr(
                patient_context,
                "gender",
                None,
            )

        else:

            age = None
            gender = None

        symptoms = [
            symptom.lower()
            for symptom in patient_memory.get(
                "symptoms",
                [],
            )
        ]

        diagnoses = [
            diagnosis.lower()
            for diagnosis in patient_memory.get(
                "diagnoses",
                [],
            )
        ]

        medications = patient_memory.get(
            "medications",
            [],
        )

        allergies = patient_memory.get(
            "allergies",
            [],
        )

        risk_history = patient_memory.get(
            "risk_history",
            [],
        )

        # --------------------------------------------------
        # Age
        # --------------------------------------------------

        if age is not None:

            if age >= 60:

                preventive_care.add(
                    "Annual cardiac, kidney and vision screening is recommended."
                )

            elif age >= 40:

                preventive_care.add(
                    "Annual diabetes, blood pressure and lipid profile screening is recommended."
                )

        # --------------------------------------------------
        # Gender
        # --------------------------------------------------

        if gender:

            if gender.lower() == "female":

                preventive_care.add(
                    "Follow recommended women's preventive health screenings."
                )

            elif gender.lower() == "male":

                preventive_care.add(
                    "Maintain regular cardiovascular health screening."
                )

        # --------------------------------------------------
        # Medical History
        # --------------------------------------------------

        if "diabetes" in history:

            lifestyle.add(
                "Maintain strict blood glucose monitoring."
            )

            preventive_care.add(
                "Schedule HbA1c testing every 3-6 months."
            )

        if "hypertension" in history:

            lifestyle.add(
                "Reduce sodium intake and monitor blood pressure daily."
            )

        if "asthma" in history:

            alerts.add(
                "Avoid smoke, dust and respiratory irritants."
            )

        if "heart disease" in history:

            preventive_care.add(
                "Maintain regular cardiology follow-up."
            )

        # --------------------------------------------------
        # Symptoms
        # --------------------------------------------------

        symptom_rules = {

            "fever":
                "Maintain hydration and monitor body temperature.",

            "headache":
                "Monitor blood pressure if symptoms persist.",

            "cough":
                "Increase fluid intake and monitor breathing.",

            "fatigue":
                "Ensure adequate hydration, nutrition and rest.",

            "dizziness":
                "Avoid driving until symptoms resolve.",
        }

        for symptom in symptoms:

            if symptom in symptom_rules:

                recommendations.add(
                    symptom_rules[symptom]
                )

        if "chest pain" in symptoms:

            alerts.add(
                "Immediate emergency medical evaluation is strongly recommended."
            )

        if "shortness of breath" in symptoms:

            alerts.add(
                "Seek urgent clinical assessment."
            )

        # --------------------------------------------------
        # Previous Diagnoses
        # --------------------------------------------------

        if "diabetes" in diagnoses:

            preventive_care.add(
                "Continue regular diabetic follow-up."
            )

        if "hypertension" in diagnoses:

            preventive_care.add(
                "Continue routine blood pressure monitoring."
            )

        # --------------------------------------------------
        # Medications
        # --------------------------------------------------

        if medications:

            recommendations.add(
                "Continue prescribed medications unless advised otherwise by your physician."
            )

        # --------------------------------------------------
        # Allergies
        # --------------------------------------------------

        if allergies:

            alerts.add(
                "Verify allergies before prescribing any medication."
            )

        # --------------------------------------------------
        # Previous Risk Trends
        # --------------------------------------------------

        if len(risk_history) >= 3:

            preventive_care.add(
                "Longitudinal risk trend available. Compare current and previous assessments."
            )

        logger.info(
            "Personalization generated successfully."
        )

        return {

            "recommendations": sorted(
                recommendations
            ),

            "alerts": sorted(
                alerts
            ),

            "lifestyle": sorted(
                lifestyle
            ),

            "preventive_care": sorted(
                preventive_care
            ),

            "patient_snapshot": {

                "known_conditions": len(history),

                "previous_symptoms": len(symptoms),

                "previous_diagnoses": len(diagnoses),

                "medications": len(medications),

                "allergies": len(allergies),

                "risk_records": len(risk_history),
            },
        }