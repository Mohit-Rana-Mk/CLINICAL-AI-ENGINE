from app.ai_engine.schemas import ConfidenceResult


class ConfidenceEngine:

    def calculate(
        self,
        patient_context,
        entities,
        emergency,
        risk
    ):

        score = 50

        reasons = []

        # ------------------------

        if entities.symptoms:
            score += 15
            reasons.append("Symptoms identified")

        # ------------------------

        if patient_context.age is not None:
            score += 10
            reasons.append("Patient age available")

        # ------------------------

        if patient_context.gender:
            score += 5
            reasons.append("Patient gender available")

        # ------------------------

        if patient_context.medical_history:
            score += 10
            reasons.append("Medical history available")

        # ------------------------

        if patient_context.medications:
            score += 5
            reasons.append("Medication history available")

        # ------------------------

        if patient_context.allergies:
            score += 5
            reasons.append("Allergy history available")

        # ------------------------

        if emergency.is_emergency:
            score += 10
            reasons.append("Emergency rule matched")

        # ------------------------

        score = min(score, 100)

        if score >= 90:
            level = "Very High"

        elif score >= 75:
            level = "High"

        elif score >= 60:
            level = "Medium"

        else:
            level = "Low"

        return ConfidenceResult(
            confidence_score=score,
            confidence_level=level,
           reasons=reasons
        )