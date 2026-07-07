import logging

from app.ai_engine.pipeline import ClinicalPipeline

logger = logging.getLogger(__name__)


class ClinicalAIEngine:

    def __init__(self):
        self.pipeline = ClinicalPipeline()

    def process(
        self,
        message: str,
        patient_id: int | None = None,
    ):

        logger.info("========== Clinical AI Pipeline Started ==========")

        try:

            result = self.pipeline.run(
                message=message,
                patient_id=patient_id,
            )

            logger.info("========== Pipeline Completed ==========")

            return result

        except Exception as e:

            logger.exception("Pipeline Failed")

            return {
                "status": "error",
                "message": str(e)
            }