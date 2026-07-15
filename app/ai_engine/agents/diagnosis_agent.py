import logging

logger = logging.getLogger(__name__)


class DiagnosisAgent:
    """
    Production Clinical Diagnosis Agent.

    Responsibilities
    ----------------
    - Generate differential diagnoses
    - Consider symptoms
    - Consider medical history
    - Consider retrieved clinical evidence
    - Estimate confidence
    - Never produce a confirmed diagnosis
    """

    PRIORITY_ORDER = {
        "CRITICAL": 0,
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3,
    }

    def run(
        self,
        symptoms: list[str],
        rag_result: dict,
        patient_context,
    ):

        logger.info("Running Diagnosis Agent")

        symptom_set = {
            symptom.lower().strip()
            for symptom in symptoms
        }

        history = getattr(
            patient_context,
            "medical_history",
            [],
        )

        history_lower = {
            item.lower()
            for item in history
        }

        possible_conditions = []
        supporting_evidence = []
        patient_risk_factors = list(history)
        retrieved_clinical_evidence = []

        # ==========================================
        # Chest Pain + Dyspnea
        # ==========================================

        if {
            "chest pain",
            "breathing difficulty",
        }.issubset(symptom_set):

            possible_conditions.extend(
                [
                    {
                        "condition": "Acute Coronary Syndrome",
                        "priority": "CRITICAL",
                        "reason": "Chest pain associated with breathing difficulty.",
                    },
                    {
                        "condition": "Pulmonary Embolism",
                        "priority": "CRITICAL",
                        "reason": "Respiratory symptoms with chest pain.",
                    },
                    {
                        "condition": "Aortic Dissection",
                        "priority": "HIGH",
                        "reason": "Life-threatening chest pain differential.",
                    },
                ]
            )

            supporting_evidence.extend(
                [
                    "Chest pain reported",
                    "Breathing difficulty reported",
                ]
            )

        # ==========================================
        # Fever
        # ==========================================

        if "fever" in symptom_set:

            possible_conditions.extend(
                [
                    {
                        "condition": "Respiratory Infection",
                        "priority": "MEDIUM",
                        "reason": "Fever may indicate infection.",
                    },
                    {
                        "condition": "Viral Illness",
                        "priority": "LOW",
                        "reason": "Common viral presentation.",
                    },
                ]
            )

            supporting_evidence.append("Fever reported")

        # ==========================================
        # Cough
        # ==========================================

        if "cough" in symptom_set:

            possible_conditions.extend(
                [
                    {
                        "condition": "Upper Respiratory Tract Infection",
                        "priority": "MEDIUM",
                        "reason": "Persistent cough.",
                    },
                    {
                        "condition": "Bronchitis",
                        "priority": "LOW",
                        "reason": "Respiratory tract irritation.",
                    },
                ]
            )

            supporting_evidence.append("Cough reported")

        # ==========================================
        # Headache
        # ==========================================

        if "headache" in symptom_set:

            possible_conditions.append(
                {
                    "condition": "Primary Headache Disorder",
                    "priority": "LOW",
                    "reason": "Headache without neurological findings.",
                }
            )

            supporting_evidence.append("Headache reported")

        # ==========================================
        # Abdominal Pain
        # ==========================================

        if "abdominal pain" in symptom_set:

            possible_conditions.append(
                {
                    "condition": "Acute Abdominal Condition",
                    "priority": "MEDIUM",
                    "reason": "Requires abdominal evaluation.",
                }
            )

            supporting_evidence.append("Abdominal pain reported")

        # ==========================================
        # Risk Factors
        # ==========================================

        if "type 2 diabetes" in history_lower:

            supporting_evidence.append(
                "History of Type 2 Diabetes"
            )

        if "hypertension" in history_lower:

            supporting_evidence.append(
                "History of Hypertension"
            )

        # ==========================================
        # Retrieved Evidence
        # ==========================================

        for item in rag_result.get(
            "documents",
            [],
        ):

            retrieved_clinical_evidence.append(
                {
                    "title": item.document.title,
                    "category": item.document.category,
                    "source": item.document.source,
                    "similarity_score": round(
                        item.similarity_score,
                        3,
                    ),
                }
            )

        # ==========================================
        # Remove Duplicate Conditions
        # ==========================================

        unique = {}

        for condition in possible_conditions:

            unique[
                condition["condition"]
            ] = condition

        possible_conditions = list(
            unique.values()
        )

        # ==========================================
        # Sort
        # ==========================================

        possible_conditions.sort(
            key=lambda x: self.PRIORITY_ORDER.get(
                x["priority"],
                999,
            )
        )

        # ==========================================
        # Confidence
        # ==========================================

        confidence = 35

        confidence += min(
            len(symptom_set) * 8,
            24,
        )

        confidence += min(
            len(history) * 4,
            12,
        )

        confidence += min(
            len(retrieved_clinical_evidence) * 4,
            16,
        )

        if any(
            item["priority"] == "CRITICAL"
            for item in possible_conditions
        ):
            confidence += 10

        confidence = min(
            confidence,
            95,
        )

        # ==========================================
        # Output
        # ==========================================

        return {
            "possible_conditions": possible_conditions,
            "supporting_evidence": supporting_evidence,
            "patient_risk_factors": patient_risk_factors,
            "retrieved_clinical_evidence": retrieved_clinical_evidence,
            "confidence": confidence,
            "clinical_note": (
                "Differential diagnoses are generated using symptoms, "
                "medical history and retrieved clinical evidence. "
                "These results support clinical decision making and "
                "are not confirmed medical diagnoses."
            ),
        }