import logging
import time

from app.ai_engine.agents.coordinator import AgentCoordinator
from app.ai_engine.confidence_engine import ConfidenceEngine
from app.ai_engine.context_loader import PatientContextLoader
from app.ai_engine.entity_extractor import MedicalEntityExtractor
from app.ai_engine.explainability_engine import ExplainabilityEngine
from app.ai_engine.followup_engine import FollowUpEngine
from app.ai_engine.memory.conversation_memory import ConversationMemory
from app.ai_engine.memory.patient_memory import PatientMemory
from app.ai_engine.memory.patient_profile import PatientProfile
from app.ai_engine.memory.timeline_builder import TimelineBuilder
from app.ai_engine.personalization_engine import PersonalizationEngine
from app.ai_engine.rag.rag_service import RAGService
from app.ai_engine.response_builder import ResponseBuilder
from app.ai_engine.risk_engine import RiskEngine
from app.ai_engine.summary_engine import ClinicalSummaryGenerator
from app.ai_engine.vision.vision_pipeline import VisionPipeline
from app.ai_engine.vision.vision_response import VisionResponseBuilder
from app.ai_engine.explainability.reasoning_engine import ReasoningEngine
from app.ai_engine.explainability.decision_trace import DecisionTrace
from app.ai_engine.explainability.audit_logger import AuditLogger
from app.translation.language_router import TranslationRouter

logger = logging.getLogger(__name__)


class ClinicalPipeline:
    """
    Production Clinical AI Pipeline.

    Workflow

    1. Load Patient Context
    2. Conversation Memory
    3. Patient Profile
    4. Entity Extraction
    5. Risk Assessment
    6. Retrieve Clinical Evidence (RAG)
    7. Multi-Agent Reasoning
    8. Follow-up Questions
    9. Explainability
    10. Clinical Summary
    11. Confidence Score
    12. Patient Memory
    13. Timeline
    14. Personalization
    15. Build Final Response
    """

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
        self.patient_memory = PatientMemory()
        self.conversation_memory = ConversationMemory()
        self.timeline_builder = TimelineBuilder()
        self.personalization_engine = PersonalizationEngine()
        self.response_builder = ResponseBuilder()
        self.vision_pipeline = VisionPipeline()
        self.vision_response = VisionResponseBuilder()
        self.reasoning_engine = ReasoningEngine()
        self.decision_trace = DecisionTrace()
        self.audit_logger = AuditLogger()
        self.translation_router = TranslationRouter()

    def run(
        self,
        message: str | None = None,
        patient_id: int | None = None,
        image_path: str | None = None,
    ):

        start = time.perf_counter()

        try:

            logger.info(
                "========== Clinical AI Pipeline Started =========="
            )

            if (
                (message is None or not str(message).strip())
                and image_path is None
            ):
                return {
                    "status": "error",
                    "message": "Either message or image is required.",
                }
            

            # -------------------------------------------------
            # 0. Language Translation & Normalization (Hinglish -> English)
            # -------------------------------------------------
            if message and str(message).strip():
                translation_result = self.translation_router.process(message)
                message = translation_result.get("english_text", message)
                logger.info(f"Processed / Translated Input: '{message}'")

            # -------------------------------------------------
            # 1. Patient Context
            # -------------------------------------------------

            logger.info("[1/15] Loading patient context")

            patient_context = self.context_loader.load(
                patient_id
            )

            vision_result = {
                "status": "not_requested",
                "image_analysis": {},
            }
            if image_path:

                logger.info("Running Vision Pipeline")

                pipeline_result = self.vision_pipeline.process(
                    image_path=image_path,
                )

                vision_result = self.vision_response.build(
                    pipeline_result,
                    )


            # -------------------------------------------------
            # 2. Conversation Memory
            # -------------------------------------------------

            logger.info("[2/15] Saving conversation")

            self.conversation_memory.add_message(
                patient_id=patient_id,
                role="patient",
                message=message if message else "[Image Uploaded]",
            )

            conversation_history = (
                self.conversation_memory.get_history(
                    patient_id
                )
            )

            # -------------------------------------------------
            # 3. Patient Profile
            # -------------------------------------------------

            logger.info("[3/15] Building patient profile")

            patient_profile = PatientProfile()

            patient_profile.update_from_context(
                patient_context
            )

            # -------------------------------------------------
            # 4. Entity Extraction
            # -------------------------------------------------

            logger.info("[4/15] Extracting medical entities")

            entities = self.entity_extractor.extract(
                message or ""
            )

            # -------------------------------------------------
            # 5. Risk Assessment
            # -------------------------------------------------

            logger.info("[5/15] Running risk assessment")

            risk = self.risk_engine.predict(
                symptoms=entities.symptoms,
                patient_context=patient_context,
            )

            # -------------------------------------------------
            # 6. Retrieve Medical Evidence
            # -------------------------------------------------

            logger.info("[6/15] Retrieving medical evidence")

            rag_result = self.rag_service.process(
                query=message or "",
                patient_context=patient_context,
                emergency_status=None,
                risk_assessment=risk,
            )

            # -------------------------------------------------
            # 7. Multi-Agent Reasoning
            # -------------------------------------------------

            logger.info("[7/15] Running clinical agents")

            agents = self.agent_coordinator.run(
                message=message or "",
                patient_context=patient_context,
                entities=entities,
                rag_result=rag_result,
                risk=risk,
            )

            # -------------------------------------------------
            # 8. Follow-up Questions
            # -------------------------------------------------

            logger.info("[8/15] Generating follow-up questions")

            follow_up = self.followup_engine.generate(
                symptoms=entities.symptoms,
                patient_context=patient_context,
                emergency=agents.get("emergency_analysis"),
                risk=risk,
                rag_documents=rag_result.get("documents", []),
                )

            # -------------------------------------------------
            # 9. Explainability
            # -------------------------------------------------

            logger.info("[9/15] Generating explainability")

            explanation = self.explainability_engine.generate(
                patient_context,
                entities,
                agents.get("emergency_analysis"),
                risk,
            )


            # -------------------------------------------------
            # 12. Update Patient Memory
            # -------------------------------------------------

            logger.info("[12/15] Updating patient memory")

            diagnosis = None

            diagnosis_agent = agents.get("diagnosis_analysis")

            if hasattr(diagnosis_agent, "model_dump"):
                diagnosis_agent = diagnosis_agent.model_dump()

            if not isinstance(diagnosis_agent, dict):
                diagnosis_agent = {}

            possible_conditions = diagnosis_agent.get(
                "possible_conditions",
                []
            )

            if possible_conditions:

                first = possible_conditions[0]

                if isinstance(first, dict):
                    diagnosis = first.get("condition")
                else:
                    diagnosis = str(first)

            recommendation = agents.get("recommendation_analysis")

            if hasattr(recommendation, "model_dump"):
                recommendation = recommendation.model_dump()

            self.patient_memory.update(
                patient_id=patient_id,
                symptoms=entities.symptoms,
                diagnosis=diagnosis,
                medications=patient_context.medications,
                allergies=patient_context.allergies,
                risk=(
                    risk.model_dump()
                    if hasattr(risk, "model_dump")
                    else risk
                ),
                recommendation=recommendation,
            )

            patient_memory = self.patient_memory.get(
                patient_id
            )

            # -------------------------------------------------
            # 13. Timeline
            # -------------------------------------------------

            logger.info("[13/15] Building clinical timeline")

            timeline = self.timeline_builder.build(
                conversation_history=conversation_history,
                patient_memory=patient_memory,
            )

            timeline_statistics = (
                self.timeline_builder.statistics(
                    timeline
                )
            )

            # -------------------------------------------------
            # 14. Personalization
            # -------------------------------------------------

            logger.info("[14/15] Generating personalization")

            personalization = (
                self.personalization_engine.generate(
                    patient_context=patient_context,
                    patient_memory=patient_memory,
                )
            )
            
            # -------------------------------------------------
            # 10. Clinical Summary
            # -------------------------------------------------

            logger.info("[10/15] Generating clinical summary")

            summary = self.summary_engine.generate(
                patient=patient_context,
                entities=entities,
                risk=risk,
                patient_memory=patient_memory,
                personalization=personalization,
            )
            # -------------------------------------------------
            # 11. Confidence Score
            # -------------------------------------------------

            logger.info("[11/15] Calculating confidence")

            confidence = self.confidence_engine.calculate(
                patient_context,
                entities,
                agents.get("emergency_analysis"),
                risk,
                rag_result.get("documents", []),
            )

            reasoning = self.reasoning_engine.generate(
                entities,
                risk,
                agents,
                rag_result,
            )

            decision_trace = self.decision_trace.build(
                entities,
                agents,
                risk,
            )

            audit = self.audit_logger.log(
                patient_id,
                entities,
                risk,
            )
            

            # -------------------------------------------------
            # 15. Build Final Response
            # -------------------------------------------------

            logger.info("[15/15] Building final response")

            response = self.response_builder.build(
                patient_context=patient_context,
                entities=entities,
                agents=agents,
                risk=risk,
                explanation=explanation,
                summary=summary,
                confidence=confidence,
                rag_result=rag_result,
                follow_up=follow_up,
                vision=vision_result,
                reasoning=reasoning,
                decision_trace=decision_trace,
                audit=audit,
            )

            response["patient_profile"] = (
                patient_profile.build_summary()
            )

            response["patient_memory"] = (
                patient_memory
            )

            response["conversation_history"] = (
                self.conversation_memory.get_recent_messages(
                    patient_id,
                    limit=10,
                )
            )

            response["timeline"] = timeline

            response["timeline_statistics"] = (
                timeline_statistics
            )

            response["personalization"] = (
                personalization
            )

            response["pipeline"] = {
                "version": "3.0",
                "engine": "Clinical AI Engine",
                "steps_completed": 15,
                "execution_time_seconds": round(
                    time.perf_counter() - start,
                    3,
                ),
            }

            logger.info(
                "Clinical AI Pipeline completed successfully in %.3fs",
                time.perf_counter() - start,
            )

            return response

        except Exception as e:

            logger.exception(
                "Clinical Pipeline Failed"
            )

        return {
            "status":"error",
            "message":str(e),
            "error_type":type(e).__name__,
        }
