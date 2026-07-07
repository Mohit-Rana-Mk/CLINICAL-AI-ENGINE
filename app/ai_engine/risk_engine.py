from app.ai_engine.schemas import RiskAssessment


class RiskEngine:

    def predict(self, symptoms: list[str]) -> RiskAssessment:

        symptom_set = {s.lower() for s in symptoms}

        heart = "LOW"
        respiratory = "LOW"
        infection = "LOW"
        neuro = "LOW"

        score = 10

        # Heart Risk
        if "chest pain" in symptom_set:
            heart = "HIGH"
            score += 40

        # Respiratory Risk
        if "breathing difficulty" in symptom_set:
            respiratory = "HIGH"
            score += 35

        if "cough" in symptom_set:
            respiratory = "MEDIUM"
            score += 15

        # Infection Risk
        if "fever" in symptom_set:
            infection = "MEDIUM"
            score += 20

        if "fever" in symptom_set and "cough" in symptom_set:
            infection = "HIGH"
            score += 20

        # Neurological Risk
        if "headache" in symptom_set:
            neuro = "MEDIUM"
            score += 10

        # Overall Risk
        if score >= 80:
            overall = "CRITICAL"
        elif score >= 60:
            overall = "HIGH"
        elif score >= 30:
            overall = "MEDIUM"
        else:
            overall = "LOW"

        return RiskAssessment(
            overall_risk=overall,
            heart_risk=heart,
            respiratory_risk=respiratory,
            infection_risk=infection,
            neurological_risk=neuro,
            risk_score=min(score, 100)
        )