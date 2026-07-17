import logging
import time
import uuid

from app.ai_engine.multimodal.multimodal_pipeline import MultimodalPipeline
from app.ai_engine.pipeline import ClinicalPipeline

logger = logging.getLogger(__name__)


class ClinicalAIEngine:
    """
    Production Clinical AI Orchestrator.

    Responsibilities
    ----------------
    • Handle every incoming request
    • Process multimodal inputs
    • Execute Clinical Pipeline
    • Standardize API responses
    • Capture execution metadata
    """

    def __init__(self):

        logger.info("Initializing Clinical AI Engine")

        self.multimodal_pipeline = MultimodalPipeline()
        self.pipeline = ClinicalPipeline()

    def process(
        self,
        message: str | None = None,
        patient_id: int | None = None,
        file_name: str | None = None,
        mime_type: str | None = None,
    ):

        request_id = str(uuid.uuid4())

        start = time.perf_counter()

        logger.info(
            "[%s] Clinical request received",
            request_id,
        )

        try:

            # ---------------------------------------
            # Multimodal Processing
            # ---------------------------------------

            multimodal_result = self.multimodal_pipeline.process(
                text=message,
                file_name=file_name,
                mime_type=mime_type,
            )

            processed_message = message or ""

            if isinstance(multimodal_result, dict):

                if multimodal_result.get("type") == "text":

                    processed_message = multimodal_result.get(
                        "content",
                        "",
                    )

            elif hasattr(multimodal_result, "text"):

                processed_message = multimodal_result.text

            # ---------------------------------------
            # Run Clinical Pipeline
            # ---------------------------------------

            pipeline_response = self.pipeline.run(
                message=processed_message,
                patient_id=patient_id,
            )

            if pipeline_response.get("status") == "error":

                return {
                    "request_id": request_id,
                    "execution_time_seconds": round(
                        time.perf_counter() - start,
                        3,
                    ),
                    **pipeline_response,
                }

            execution_time = round(
                time.perf_counter() - start,
                3,
            )

            logger.info(
                "[%s] Completed successfully in %.3fs",
                request_id,
                execution_time,
            )

            pipeline_response["request_id"] = request_id

            pipeline_response[
                "execution_time_seconds"
            ] = execution_time

            pipeline_response[
                "input_processing"
            ] = (
                multimodal_result.model_dump()
                if hasattr(multimodal_result, "model_dump")
                else multimodal_result
            )

            return pipeline_response

        except Exception as error:

            execution_time = round(
                time.perf_counter() - start,
                3,
            )

            logger.exception(
                "[%s] Clinical AI failed",
                request_id,
            )

            return {
                "status": "error",
                "request_id": request_id,
                "execution_time_seconds": execution_time,
                "message": str(error),
            }