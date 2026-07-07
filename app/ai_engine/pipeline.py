import logging

from app.ai_engine.context_loader import PatientContextLoader
from app.ai_engine.entity_extractor import MedicalEntityExtractor
from app.ai_engine.emergency_detector import EmergencyDetector
from app.ai_engine.followup_engine import FollowUpEngine
from app.ai_engine.risk_engine import RiskEngine
from app.ai_engine.recommendation_engine import RecommendationEngine
from app.ai_engine.medication_checker import MedicationChecker
from app.ai_engine.explainability_engine import ExplainabilityEngine
from app.ai_engine.summary_engine import ClinicalSummaryGenerator
from app.ai_engine.confidence_engine import ConfidenceEngine

logger = logging.getLogger(__name__)


class ClinicalPipeline:

    def __init__(self):
        self.context_loader = PatientContextLoader()
        self.entity_extractor = MedicalEntityExtractor()
        self.emergency_detector = EmergencyDetector()
        self.followup_engine = FollowUpEngine()
        self.risk_engine = RiskEngine()
        self.recommendation_engine = RecommendationEngine()
        self.medication_checker = MedicationChecker()
        self.explainability_engine = ExplainabilityEngine()
        self.summary_engine = ClinicalSummaryGenerator()
        self.confidence_engine = ConfidenceEngine()

    def run(
        self,
        message: str,
        patient_id: int | None = None,
    ):

        patient_context = self.context_loader.load(patient_id)

        entities = self.entity_extractor.extract(message)

        emergency = self.emergency_detector.detect(
            entities.symptoms
        )

        follow_up = self.followup_engine.generate(
            entities.symptoms
        )

        risk = self.risk_engine.predict(
            entities.symptoms
        )

        recommendation = self.recommendation_engine.generate(
            risk
        )

        medication_alert = self.medication_checker.check(
            patient_context.medications,
            patient_context.allergies
        )

        explanation = self.explainability_engine.generate(
            patient_context,
            entities,
            emergency,
            risk
        )

        summary = self.summary_engine.generate(
            patient_context,
            entities,
            risk
        )

        confidence = self.confidence_engine.calculate(
            patient_context,
            entities,
            emergency,
            risk
        )

        return {
            "status": "success",
            "patient_context": patient_context.model_dump(),
            "entities": entities.model_dump(),
            "emergency": emergency.model_dump(),
            "follow_up_questions": follow_up.model_dump(),
            "risk_assessment": risk.model_dump(),
            "recommendation": recommendation.model_dump(),
            "medication_alerts": medication_alert.model_dump(),
            "explanation": explanation.model_dump(),
            "clinical_summary": summary.model_dump(),
            "confidence": confidence.model_dump()
        }