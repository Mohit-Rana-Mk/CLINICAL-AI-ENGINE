import logging

from app.ai_engine.schemas import Recommendation

logger = logging.getLogger(__name__)


class RecommendationAgent:
    """
    Production Clinical Recommendation Agent.

    Responsibilities
    ----------------
    - Generate immediate actions
    - Generate precautions
    - Monitoring advice
    - Follow-up recommendations
    - Lifestyle guidance
    """

    def __init__(self):
        logger.info("Recommendation Agent initialized")

    def run(
        self,
        diagnosis=None,
        emergency=None,
        patient_context=None,
        entities=None,
        risk=None,
    ) -> Recommendation:

        logger.info("Generating clinical recommendations")

        emergency_status = False

        if emergency:

            if isinstance(emergency, dict):
                emergency_status = emergency.get(
                    "is_emergency",
                    False,
                )
            else:
                emergency_status = getattr(
                    emergency,
                    "is_emergency",
                    False,
                )

        risk_level = "LOW"

        if risk:

            if isinstance(risk, dict):
                risk_level = risk.get(
                    "overall_risk",
                    "LOW",
                )
            else:
                risk_level = getattr(
                    risk,
                    "overall_risk",
                    "LOW",
                )

        risk_level = str(risk_level).upper()

        # =====================================
        # Emergency
        # =====================================

        if emergency_status:

            return Recommendation(
                immediate_action=(
                    "Seek emergency medical care immediately."
                ),
                precautions=[
                    "Call emergency services.",
                    "Do not drive yourself.",
                    "Remain with another responsible adult.",
                    "Avoid eating or drinking unless advised.",
                ],
                monitoring=[
                    "Monitor breathing.",
                    "Monitor consciousness.",
                    "Monitor chest pain progression.",
                ],
                doctor_visit="Immediate Emergency Department evaluation",
                lifestyle=[],
            )

        # =====================================
        # Critical / High Risk
        # =====================================

        if risk_level in {
            "CRITICAL",
            "HIGH",
        }:

            return Recommendation(
                immediate_action=(
                    "Arrange urgent medical evaluation today."
                ),
                precautions=[
                    "Avoid strenuous physical activity.",
                    "Take prescribed medications only.",
                    "Seek care immediately if symptoms worsen.",
                ],
                monitoring=[
                    "Monitor blood pressure.",
                    "Monitor heart rate.",
                    "Monitor symptom progression.",
                ],
                doctor_visit="Consult physician within 24 hours",
                lifestyle=[
                    "Maintain hydration.",
                    "Avoid smoking.",
                    "Avoid alcohol.",
                    "Get adequate rest.",
                ],
            )

        # =====================================
        # Moderate Risk
        # =====================================

        if risk_level in {
            "MODERATE",
            "MEDIUM",
        }:

            return Recommendation(
                immediate_action=(
                    "Book a medical consultation."
                ),
                precautions=[
                    "Continue symptom monitoring.",
                    "Avoid overexertion.",
                ],
                monitoring=[
                    "Track symptoms daily.",
                    "Record temperature if fever develops.",
                ],
                doctor_visit="Visit doctor within 2–3 days",
                lifestyle=[
                    "Healthy diet",
                    "Stay hydrated",
                    "Adequate sleep",
                    "Light physical activity if tolerated",
                ],
            )

        # =====================================
        # Low Risk
        # =====================================

        return Recommendation(
            immediate_action=(
                "Continue home care and observe symptoms."
            ),
            precautions=[
                "Follow routine healthy habits.",
            ],
            monitoring=[
                "Return if symptoms worsen or new symptoms appear.",
            ],
            doctor_visit="Consult a physician if symptoms persist",
            lifestyle=[
                "Balanced diet",
                "Regular exercise",
                "Adequate sleep",
                "Maintain hydration",
            ],
        )