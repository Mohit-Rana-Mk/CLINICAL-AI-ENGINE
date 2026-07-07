from app.ai_engine.schemas import EmergencyAssessment


class EmergencyDetector:

    def detect(self, symptoms: list[str]) -> EmergencyAssessment:

        symptom_set = {s.lower() for s in symptoms}

        # Chest pain + breathing difficulty
        if (
            "chest pain" in symptom_set
            and "breathing difficulty" in symptom_set
        ):
            return EmergencyAssessment(
                is_emergency=True,
                level="CRITICAL",
                reason="Chest pain with breathing difficulty may indicate a life-threatening cardiac or respiratory emergency.",
                recommendation="Call emergency services or go to the nearest emergency department immediately."
            )

        # Chest pain alone
        if "chest pain" in symptom_set:
            return EmergencyAssessment(
                is_emergency=True,
                level="HIGH",
                reason="Chest pain requires urgent medical evaluation.",
                recommendation="Seek immediate assessment by a healthcare professional."
            )

        # Breathing difficulty alone
        if "breathing difficulty" in symptom_set:
            return EmergencyAssessment(
                is_emergency=True,
                level="CRITICAL",
                reason="Breathing difficulty may represent a serious respiratory emergency.",
                recommendation="Call emergency services immediately."
            )

        return EmergencyAssessment()