import logging

from app.ai_engine.schemas import RiskAssessment

logger = logging.getLogger(__name__)


class RiskEngine:
    """
    Production Clinical Risk Engine.

    Responsibilities
    ----------------
    - Estimate organ-system specific risks
    - Calculate overall clinical risk
    - Explain contributing risk factors
    """

    def predict(
        self,
        symptoms: list[str],
        patient_context=None,
    ) -> RiskAssessment:

        logger.info("Calculating clinical risk")

        symptom_set = {
            symptom.lower().strip()
            for symptom in symptoms
        }

        heart = "LOW"
        respiratory = "LOW"
        infection = "LOW"
        neurological = "LOW"

        risk_score = 0
        risk_factors = []

        # =====================================
        # Cardiac Risk
        # =====================================

        if "chest pain" in symptom_set:

            heart = "HIGH"
            risk_score += 35

            risk_factors.append(
                {
                    "factor": "Chest pain",
                    "impact": "HIGH",
                    "weight": 35,
                }
            )

        # =====================================
        # Respiratory Risk
        # =====================================

        if "breathing difficulty" in symptom_set:

            respiratory = "HIGH"
            risk_score += 30

            risk_factors.append(
                {
                    "factor": "Breathing difficulty",
                    "impact": "HIGH",
                    "weight": 30,
                }
            )

        elif "cough" in symptom_set:

            respiratory = "MEDIUM"
            risk_score += 10

            risk_factors.append(
                {
                    "factor": "Cough",
                    "impact": "MEDIUM",
                    "weight": 10,
                }
            )

        # =====================================
        # Infection Risk
        # =====================================

        if "fever" in symptom_set:

            infection = "MEDIUM"
            risk_score += 15

            risk_factors.append(
                {
                    "factor": "Fever",
                    "impact": "MEDIUM",
                    "weight": 15,
                }
            )

        # =====================================
        # Neurological Risk
        # =====================================

        if "headache" in symptom_set:

            neurological = "MEDIUM"
            risk_score += 10

            risk_factors.append(
                {
                    "factor": "Headache",
                    "impact": "MEDIUM",
                    "weight": 10,
                }
            )

        if "loss of consciousness" in symptom_set:

            neurological = "HIGH"
            risk_score += 35

            risk_factors.append(
                {
                    "factor": "Loss of consciousness",
                    "impact": "HIGH",
                    "weight": 35,
                }
            )

        if "seizure" in symptom_set:

            neurological = "HIGH"
            risk_score += 35

            risk_factors.append(
                {
                    "factor": "Seizure",
                    "impact": "HIGH",
                    "weight": 35,
                }
            )

        # =====================================
        # Medical History
        # =====================================

        history = []

        if (
            patient_context
            and getattr(patient_context, "medical_history", None)
        ):
            history = [
                item.lower()
                for item in patient_context.medical_history
            ]

        if any("diabetes" in item for item in history):

            risk_score += 10

            risk_factors.append(
                {
                    "factor": "Diabetes history",
                    "impact": "MODERATE",
                    "weight": 10,
                }
            )

        if any("hypertension" in item for item in history):

            risk_score += 10

            risk_factors.append(
                {
                    "factor": "Hypertension history",
                    "impact": "MODERATE",
                    "weight": 10,
                }
            )

        # =====================================
        # Score Calibration
        # =====================================

        risk_score = min(risk_score, 100)

        if risk_score >= 80:
            overall = "CRITICAL"

        elif risk_score >= 60:
            overall = "HIGH"

        elif risk_score >= 30:
            overall = "MEDIUM"

        else:
            overall = "LOW"

        logger.info(
            "Risk assessment completed (%s - %d)",
            overall,
            risk_score,
        )

        return RiskAssessment(
            overall_risk=overall,
            heart_risk=heart,
            respiratory_risk=respiratory,
            infection_risk=infection,
            neurological_risk=neurological,
            risk_score=risk_score,
            risk_factors=risk_factors,
        )