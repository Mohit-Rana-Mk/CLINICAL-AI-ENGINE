import logging

from app.ai_engine.schemas import ConfidenceResult

logger = logging.getLogger(__name__)


class ConfidenceEngine:
    """
    Production Confidence Engine.

    Estimates confidence based on:

    - Patient information completeness
    - Symptom extraction quality
    - Clinical risk assessment
    - Emergency detection
    - Retrieved medical evidence
    """

    MAX_CONFIDENCE = 95
    BASE_CONFIDENCE = 45

    def calculate(
        self,
        patient_context,
        entities,
        emergency,
        risk,
        rag_documents=None,
    ) -> ConfidenceResult:

        logger.info("Calculating confidence score")

        patient_context = patient_context or type(
            "EmptyContext",
            (),
        {
        "age": None,
        "gender": None,
        "medical_history": [],
        "medications": [],
        "allergies": [],
        "vitals": {},
        "lab_reports": {},
        },
    )()

        entities = entities or type(
            "EmptyEntities",
            (),
        {
        "symptoms": [],
        "duration": None,
        "severity": None,
        "associated_symptoms": [],
        },
    )()

        confidence = self.BASE_CONFIDENCE
        reasons = []

        # =====================================
        # Normalize Emergency
        # =====================================

        emergency_status = (
            emergency.get("is_emergency", False)
            if isinstance(emergency, dict)
            else getattr(emergency, "is_emergency", False)
        )

        # =====================================
        # Normalize Risk
        # =====================================

        if isinstance(risk, dict):
            risk_score = risk.get("risk_score")
            risk_factors = risk.get("risk_factors", [])
        else:
            risk_score = getattr(risk, "risk_score", None)
            risk_factors = getattr(risk, "risk_factors", [])

        # =====================================
        # Symptoms
        # =====================================

        if getattr(entities, "symptoms", []):
            confidence += 15
            reasons.append(
                "Clinical symptoms identified from patient input"
            )
        else:
            reasons.append(
                "Insufficient symptom information"
            )

        # =====================================
        # Patient Context
        # =====================================

        if patient_context.age is not None:
            confidence += 5
            reasons.append("Patient age available")

        if patient_context.gender:
            confidence += 5
            reasons.append("Patient gender available")

        if patient_context.medical_history:
            confidence += 10
            reasons.append("Medical history available")

        if patient_context.medications:
            confidence += 5
            reasons.append("Medication history available")

        if patient_context.allergies:
            confidence += 5
            reasons.append("Allergy information available")

        if patient_context.vitals:
            confidence += 5
            reasons.append("Vital signs available")

        if patient_context.lab_reports:
            confidence += 5
            reasons.append("Laboratory data available")

        # =====================================
        # Emergency Detection
        # =====================================

        if emergency_status:
            confidence += 10
            reasons.append(
                "Emergency pattern detected from clinical rules"
            )

        # =====================================
        # Risk Assessment
        # =====================================

        if risk_score is not None:
            confidence += 10
            reasons.append(
                "Risk assessment generated successfully"
            )

        if risk_factors:
            confidence += 5
            reasons.append(
                "Clinical risk factors identified"
            )

        # =====================================
        # Retrieved Evidence
        # =====================================

        if rag_documents:
            confidence += 5
            reasons.append(
                "Clinical evidence retrieved from medical knowledge base"
            )

        # =====================================
        # Missing Information
        # =====================================

        missing = []

        if not entities.duration:
            missing.append("symptom duration")

        if not entities.severity:
            missing.append("symptom severity")

        if not entities.associated_symptoms:
            missing.append("associated symptoms")

        if missing:
            confidence -= 10
            reasons.append(
                "Missing clinical details: "
                + ", ".join(missing)
            )

        # =====================================
        # Final Calibration
        # =====================================

        confidence = max(
            0,
            min(confidence, self.MAX_CONFIDENCE),
        )

        if confidence >= 85:
            level = "High"
        elif confidence >= 70:
            level = "Moderate"
        elif confidence >= 50:
            level = "Low"
        else:
            level = "Very Low"

        logger.info(
            "Confidence calculated (%d%% - %s)",
            confidence,
            level,
        )

        evidence_count = len(rag_documents or [])
        
        return ConfidenceResult(
            confidence_score=confidence,
            confidence_level=level,
            reasons=reasons,
            evidence_count=evidence_count,
        )