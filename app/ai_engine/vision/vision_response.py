import logging
from typing import Any

logger = logging.getLogger(__name__)


class VisionResponseBuilder:
    """
    Builds final response from image analysis results.
    """

    def build(
        self,
        pipeline_result: dict[str, Any]
    ) -> dict[str, Any]:

        if pipeline_result.get("status") != "success":
            return {
                "status": "failed",
                "image_analysis": None,
                "error": pipeline_result.get(
                    "error",
                    "Vision analysis failed"
                )
            }

        classification = pipeline_result.get(
            "classification",
            {}
        )

        return {
            "status": "success",
            "image_analysis": {
                "category": classification.get(
                    "category",
                    "unknown",
                ),
                "prediction": classification.get(
                    "prediction",
                ),
                "model": classification.get(
                    "model",
                ),
                "confidence": classification.get(
                    "confidence",
                    0.0,
                ),
                "recommendation": self.get_recommendation(
                    classification.get(
                        "category",
                        "unknown",
                    )
                ),
            },
            "metadata": pipeline_result.get(
                "metadata",
                {}
            )
        }

    def get_recommendation(
        self,
        category: str
    ) -> str:

        recommendations = {
    "skin": "Consult a dermatologist for clinical evaluation.",
    "eye": "Consult an ophthalmologist for a comprehensive eye examination.",
    "tongue": "Clinical oral examination is recommended.",
    "wound": "Seek medical assessment for wound management.",
    "xray": "Radiologist review is recommended.",
    "ecg": "Cardiology evaluation is recommended.",
    "unknown": "Manual clinical review is recommended.",
        }

        return recommendations.get(
            category,
            recommendations["unknown"]
        )