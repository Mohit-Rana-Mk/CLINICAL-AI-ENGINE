import logging

logger = logging.getLogger(__name__)


class EmergencyAgent:
    """
    Production Emergency Triage Agent.

    Responsibilities
    ----------------
    - Detect life-threatening symptom patterns
    - Assign emergency severity
    - Recommend immediate action
    - Never provide a diagnosis
    """

    EMERGENCY_PATTERNS = {
        "cardiac_emergency": [
            "chest pain",
            "pressure in chest",
            "heart pain",
        ],
        "respiratory_emergency": [
            "breathing difficulty",
            "shortness of breath",
            "unable to breathe",
        ],
        "neurological_emergency": [
            "stroke",
            "facial weakness",
            "loss of consciousness",
            "seizure",
            "confusion",
            "slurred speech",
        ],
        "bleeding_emergency": [
            "severe bleeding",
            "blood loss",
            "vomiting blood",
            "bloody stool",
        ],
        "anaphylaxis": [
            "swollen tongue",
            "swollen throat",
            "difficulty swallowing",
        ],
    }

    def run(
        self,
        symptoms: list[str],
    ):

        logger.info("Running Emergency Agent")

        symptom_set = {
            symptom.lower().strip()
            for symptom in symptoms
        }

        detected_patterns = []

        for category, keywords in self.EMERGENCY_PATTERNS.items():

            if any(
                keyword in symptom_set
                for keyword in keywords
            ):
                detected_patterns.append(category)

        detected_patterns = list(
            dict.fromkeys(detected_patterns)
        )

        if detected_patterns:

            if len(detected_patterns) >= 2:
                level = "CRITICAL"
            else:
                level = "HIGH"

            return {
                "is_emergency": True,
                "level": level,
                "detected_patterns": detected_patterns,
                "reason": self._generate_reason(
                    detected_patterns
                ),
                "recommendation": (
                    "Immediate medical evaluation is recommended. "
                    "Call emergency services or proceed to the nearest "
                    "Emergency Department immediately."
                ),
            }

        return {
            "is_emergency": False,
            "level": "NONE",
            "detected_patterns": [],
            "reason": "No life-threatening symptom pattern detected.",
            "recommendation": (
                "Continue routine clinical assessment and monitor symptoms."
            ),
        }

    def _generate_reason(
        self,
        patterns: list[str],
    ):

        explanations = {
            "cardiac_emergency":
                "Cardiac emergency symptoms detected.",
            "respiratory_emergency":
                "Respiratory emergency symptoms detected.",
            "neurological_emergency":
                "Neurological emergency symptoms detected.",
            "bleeding_emergency":
                "Evidence of severe bleeding detected.",
            "anaphylaxis":
                "Possible severe allergic reaction detected.",
        }

        return " ".join(
            explanations[p]
            for p in patterns
            if p in explanations
        )