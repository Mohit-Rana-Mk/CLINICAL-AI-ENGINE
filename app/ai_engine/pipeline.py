import logging
import time

from app.ai_engine.context_loader import PatientContextLoader
from app.ai_engine.entity_extractor import MedicalEntityExtractor
from app.ai_engine.rag.rag_service import RAGService
from app.ai_engine.agents.coordinator import AgentCoordinator
from app.ai_engine.risk_engine import RiskEngine
from app.ai_engine.explainability_engine import ExplainabilityEngine
from app.ai_engine.summary_engine import ClinicalSummaryGenerator
from app.ai_engine.confidence_engine import ConfidenceEngine
from app.ai_engine.followup_engine import FollowUpEngine
from app.ai_engine.response_builder import ResponseBuilder

logger = logging.getLogger(__name__)


class ClinicalPipeline:

    def __init__(self):

        logger.info("Initializing Clinical AI Pipeline")

        self.context_loader = PatientContextLoader()
        self.entity_extractor = MedicalEntityExtractor()
        self.rag_service = RAGService()
        self.agent_coordinator = AgentCoordinator()
        self.risk_engine = RiskEngine()
        self.followup_engine = FollowUpEngine()
        self.explainability_engine = ExplainabilityEngine()
        self.summary_engine = ClinicalSummaryGenerator()
        self.confidence_engine = ConfidenceEngine()
        self.response_builder = ResponseBuilder()

    def run(
        self,
        message: str,
        patient_id: int |None = None,
    ):

        start = time.perf_counter()

        try:

            logger.info("========== Clinical AI Pipeline Started ==========")

            logger.info("[1/10] Loading patient context")
            patient_context = self.context_loader.load(patient_id)

            logger.info("[2/10] Extracting medical entities")
            entities = self.entity_extractor.extract(message)

            logger.info("[3/10] Running risk assessment")
            risk = self.risk_engine.predict(
                symptoms=entities.symptoms,
                patient_context=patient_context,
            )

            logger.info("[4/10] Retrieving clinical evidence")
            rag_result = self.rag_service.process(
                query=message,
                patient_context=patient_context,
                emergency_status=None,
                risk_assessment=risk,
            )

            logger.info("[5/10] Running clinical agents")
            agents = self.agent_coordinator.run(
                message=message,
                patient_context=patient_context,
                entities=entities,
                rag_result=rag_result,
            )

            logger.info("[6/10] Generating follow-up questions")
            follow_up = self.followup_engine.generate(
                entities.symptoms
            )

            logger.info("[7/10] Generating explainability")
            explanation = self.explainability_engine.generate(
                patient_context,
                entities,
                agents.get("emergency_analysis"),
                risk,
            )

            logger.info("[8/10] Generating clinical summary")
            summary = self.summary_engine.generate(
                patient_context,
                entities,
                risk,
            )

            logger.info("[9/10] Calculating confidence")
            confidence = self.confidence_engine.calculate(
                patient_context,
                entities,
                agents.get("emergency_analysis"),
                risk,
                rag_result.get("documents", []),
            )

            logger.info("[10/10] Building response")
            response = self.response_builder.build(
                patient_context=patient_context,
                entities=entities,
                agents=agents,
                risk=risk,
                explanation=explanation,
                summary=summary,
                confidence=confidence,
                rag_result=rag_result,
            )

            response["follow_up_questions"] = (
                follow_up.model_dump()
                if hasattr(follow_up, "model_dump")
                else follow_up
            )

            response["rag_prompt"] = rag_result.get(
                "prompt",
                "",
            )

            logger.info(
                "Clinical AI Pipeline completed successfully in %.3fs",
                time.perf_counter() - start,
            )

            return response

        except Exception as error:

            logger.exception(
                "Clinical Pipeline Failed | patient_id=%s | message=%s",
                patient_id,
                message,
            )

            return {
                "status": "error",
                "message": str(error),
            }