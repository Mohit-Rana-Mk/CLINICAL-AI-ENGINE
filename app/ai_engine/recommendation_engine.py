from app.ai_engine.schemas import Recommendation


class RecommendationEngine:

    def generate(self, risk):

        if risk.overall_risk == "CRITICAL":

            return Recommendation(
                immediate_action="Seek emergency medical care immediately.",
                precautions=[
                    "Do not drive yourself.",
                    "Call emergency services.",
                    "Stay with another person if possible."
                ],
                monitoring=[
                    "Monitor breathing.",
                    "Monitor consciousness."
                ],
                doctor_visit="Immediate Emergency Department",
                lifestyle=[]
            )

        if risk.overall_risk == "HIGH":

            return Recommendation(
                immediate_action="Consult a physician as soon as possible.",
                precautions=[
                    "Avoid strenuous activity.",
                    "Take prescribed medicines only."
                ],
                monitoring=[
                    "Monitor symptoms every few hours."
                ],
                doctor_visit="Within 24 hours",
                lifestyle=[
                    "Stay hydrated",
                    "Get adequate rest"
                ]
            )

        if risk.overall_risk == "MEDIUM":

            return Recommendation(
                immediate_action="Schedule a medical consultation.",
                precautions=[
                    "Observe symptom progression."
                ],
                monitoring=[
                    "Monitor temperature and symptoms."
                ],
                doctor_visit="Within 2–3 days",
                lifestyle=[
                    "Drink plenty of fluids",
                    "Eat nutritious food",
                    "Rest well"
                ]
            )

        return Recommendation(
            immediate_action="Continue self-care.",
            precautions=[
                "Follow healthy habits."
            ],
            monitoring=[
                "Watch for worsening symptoms."
            ],
            doctor_visit="Only if symptoms worsen",
            lifestyle=[
                "Exercise regularly",
                "Sleep well",
                "Stay hydrated"
            ]
        )