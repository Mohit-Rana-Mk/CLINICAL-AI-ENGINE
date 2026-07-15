from app.ai_engine.schemas import Recommendation



class RecommendationEngine:


    def generate(
        self,
        risk,
        emergency=None,
        entities=None
    ) -> Recommendation:


        symptoms = []


        if entities:

            symptoms = [
                symptom.lower()
                for symptom in entities.symptoms
            ]



        # =================================
        # Emergency Case
        # =================================

        if (
            risk.overall_risk == "CRITICAL"
            or (
                emergency
                and emergency.is_emergency
            )
        ):


            reasons = []


            if "chest pain" in symptoms:

                reasons.append(
                    "Chest pain detected"
                )


            if "breathing difficulty" in symptoms:

                reasons.append(
                    "Breathing difficulty detected"
                )


            return Recommendation(

                immediate_action=(
                    "Emergency medical evaluation "
                    "is required immediately."
                ),


                precautions=[

                    "Do not drive yourself.",

                    "Call emergency services.",

                    "Remain with another person if possible."

                ],


                monitoring=[

                    "Monitor breathing status.",

                    "Monitor consciousness level.",

                    "Observe worsening symptoms."

                ],


                doctor_visit=(
                    "Emergency Department evaluation"
                ),


                lifestyle=[]

            )



        # =================================
        # High Risk
        # =================================

        if risk.overall_risk == "HIGH":


            return Recommendation(

                immediate_action=(
                    "Medical consultation recommended "
                    "as soon as possible."
                ),


                precautions=[

                    "Avoid strenuous activities.",

                    "Follow prescribed medications only."

                ],


                monitoring=[

                    "Track symptom changes.",

                    "Monitor vital signs if available."

                ],


                doctor_visit=(
                    "Medical consultation within 24 hours"
                ),


                lifestyle=[

                    "Maintain hydration.",

                    "Take adequate rest."

                ]

            )



        # =================================
        # Medium Risk
        # =================================

        if risk.overall_risk == "MEDIUM":


            return Recommendation(

                immediate_action=(
                    "Schedule a medical consultation."
                ),


                precautions=[

                    "Observe symptom progression."

                ],


                monitoring=[

                    "Monitor symptoms regularly.",

                    "Record any worsening signs."

                ],


                doctor_visit=(
                    "Consult physician within 2-3 days"
                ),


                lifestyle=[

                    "Maintain balanced nutrition.",

                    "Stay hydrated.",

                    "Get adequate rest."

                ]

            )



        # =================================
        # Low Risk
        # =================================

        return Recommendation(

            immediate_action=(
                "Continue monitoring symptoms "
                "and maintain healthy habits."
            ),


            precautions=[

                "Follow recommended precautions."

            ],


            monitoring=[

                "Watch for worsening symptoms."

            ],


            doctor_visit=(
                "Consult doctor if symptoms persist "
                "or worsen."
            ),


            lifestyle=[

                "Exercise regularly.",

                "Maintain healthy sleep.",

                "Stay hydrated."

            ]

        )