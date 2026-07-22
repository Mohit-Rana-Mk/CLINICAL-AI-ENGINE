import logging

logger = logging.getLogger(__name__)


class SymptomAgent:
    """
    Production Symptom Intelligence Agent.

    Responsibilities
    ----------------
    - Structure extracted symptoms
    - Estimate symptom priority
    - Detect missing clinical information
    - Never diagnose disease
    """

    CRITICAL_SYMPTOMS = {
        "chest pain",
        "breathing difficulty",
        "loss of consciousness",
        "stroke",
        "severe bleeding",
        "seizure",
        "confusion",
        "unconscious",
    }

    HIGH_PRIORITY_SYMPTOMS = {
        "shortness of breath",
        "persistent vomiting",
        "high fever",
        "severe headache",
        "abdominal pain",
        "bloody stool",
        "bloody vomit",
    }

    def run(
        self,
        message: str,
        entities,
    ):

        logger.info("Running Symptom Agent")

        symptoms = [
            symptom.strip()
            for symptom in entities.symptoms
            if symptom.strip()
        ]

        symptom_set = {
            symptom.lower()
            for symptom in symptoms
        }

        missing_information = []

        if not entities.duration:
            missing_information.append(
                "Symptom duration"
            )

        if not entities.severity:
            missing_information.append(
                "Symptom severity"
            )

        if not entities.body_location:
            missing_information.append(
                "Affected body location"
            )

        if not entities.associated_symptoms:
            missing_information.append(
                "Associated symptoms"
            )

        if symptom_set & self.CRITICAL_SYMPTOMS:
            priority = "CRITICAL"

        elif symptom_set & self.HIGH_PRIORITY_SYMPTOMS:
            priority = "HIGH"

        elif symptoms:
            priority = "MEDIUM"

        else:
            priority = "LOW"

        return {
            "original_message": message,
            "symptoms": symptoms,
            "symptom_count": len(symptoms),
            "body_location": entities.body_location,
            "duration": entities.duration,
            "severity": entities.severity,
            "temperature": entities.temperature,
            "associated_symptoms": entities.associated_symptoms,
            "priority": priority,
            "missing_information": missing_information,
            "complete_information": len(missing_information) == 0,
        }