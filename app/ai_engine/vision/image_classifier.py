import logging
from typing import Any

logger = logging.getLogger(__name__)


class ImageClassifier:
    """
    Classifies medical images using AI models.

    Placeholder classifier layer.
    Actual model inference can be integrated later.
    """

    def __init__(self):
        self.models = {
            "skin": "skin_disease_model",
            "eye": "eye_disease_model",
            "wound": "wound_severity_model",
        }

    def classify(
        self,
        image: Any,
        metadata: dict | None = None
    ) -> dict:

        filename = ""

        if metadata:
            filename = metadata.get(
                "filename",
                ""
            ).lower()

        category = self.detect_category(filename)

        return {
            "category": category,
            "model": self.models.get(
                category,
                "unknown"
            ),
            "confidence": 0.0,
            "status": "success",
        }

    def detect_category(
        self,
        filename: str
    ) -> str:

        keywords = {
            "skin": [
                "skin",
                "rash",
                "lesion"
            ],
            "eye": [
                "eye",
                "retina"
            ],
            "wound": [
                "wound",
                "burn"
            ],
        }

        for category, words in keywords.items():
            if any(
                word in filename
                for word in words
            ):
                return category

        return "unknown"