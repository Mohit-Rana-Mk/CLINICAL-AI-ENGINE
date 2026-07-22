import logging
from typing import Any

logger = logging.getLogger(__name__)


class VisionPipeline:
    """
    Complete medical image analysis pipeline.

    Flow:
    Image
      ↓
    Preprocessing
      ↓
    Classification
      ↓
    Response Building
    """

    def __init__(self):
        # Vision dependencies (NumPy/Pillow and an eventual inference model) are
        # optional.  Do not import them while starting a text-only API service.
        self.preprocessor = None
        self.classifier = None
        self.response_builder = None

    def _ensure_components(self) -> None:
        if self.preprocessor is not None:
            return
        from app.ai_engine.vision.image_classifier import ImageClassifier
        from app.ai_engine.vision.image_preprocessor import ImagePreprocessor
        from app.ai_engine.vision.vision_response import VisionResponseBuilder

        self.preprocessor = ImagePreprocessor()
        self.classifier = ImageClassifier()
        self.response_builder = VisionResponseBuilder()


    def analyze(
        self,
        image_path: str,
        metadata: dict | None = None
    ) -> dict[str, Any]:

        try:

            self._ensure_components()

            processed = self.preprocessor.preprocess(
                image_path
            )

            if processed.get("status") != "success":
                return processed


            classification = self.classifier.classify(
                processed.get("image"),
                metadata
            )

            if classification.get("status") != "success":
                return classification


            result = {
                "status": "success",
                "classification": classification,
                "metadata": metadata or {},
                "pipeline": "vision",
            }


            return self.response_builder.build(
                result
            )


        except Exception as exc:

            logger.exception(
                "Vision pipeline failed"
            )

            return {
                "status": "failed",
                "error": str(exc)
            }

    def process(self, image_path: str) -> dict[str, Any]:
        """Backward-compatible entry point used by ClinicalPipeline."""
        return self.analyze(
            image_path=image_path, 
            metadata={"filename": image_path}
        )
