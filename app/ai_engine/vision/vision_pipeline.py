import logging
from typing import Any

from app.ai_engine.vision.image_preprocessor import ImagePreprocessor
from app.ai_engine.vision.image_classifier import ImageClassifier
from app.ai_engine.vision.vision_response import VisionResponseBuilder


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

        self.preprocessor = ImagePreprocessor()
        self.classifier = ImageClassifier()
        self.response_builder = VisionResponseBuilder()


    def analyze(
        self,
        image_path: str,
        metadata: dict | None = None
    ) -> dict[str, Any]:

        try:

            processed = self.preprocessor.preprocess(
                image_path
            )

            if processed.get("status") != "success":
                return processed


            classification = self.classifier.classify(
                processed.get("image"),
                metadata
            )


            result = {
                "status": "success",
                "classification": classification,
                "metadata": metadata or {}
            }


            return self.response_builder.build(
                result
            )


        except Exception as e:

            logger.exception(
                "Vision pipeline failed"
            )

            return {
                "status": "failed",
                "error": str(e)
            }