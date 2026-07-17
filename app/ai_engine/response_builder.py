import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ResponseBuilder:
    """
    Production Response Builder.

    Converts all internal AI engine outputs into
    the final standardized API response.
    """

    ENGINE_VERSION = "1.0.0"

    def _serialize(self, value):

        if value is None:
            return None

        if hasattr(value, "model_dump"):
            return value.model_dump()

        if isinstance(value, dict):
            return {
                k: self._serialize(v)
                for k, v in value.items()
            }

        if isinstance(value, list):
            return [
                self._serialize(item)
                for item in value
            ]

        return value

    def build(
        self,
        *,
        patient_context,
        entities,
        agents,
        risk,
        explanation,
        summary,
        confidence,
        rag_result,
        follow_up=None,
    ):

        logger.info(
            "Building final API response"
        )

        documents = []

        for doc in rag_result.get(
            "documents",
            [],
        ):

            if hasattr(doc, "document"):

                documents.append(
                    {
                        "title": doc.document.title,
                        "category": doc.document.category,
                        "source": doc.document.source,
                        "similarity_score": round(
                            doc.similarity_score,
                            3,
                        ),
                    }
                )

            else:

                documents.append(
                    self._serialize(doc)
                )

        response = {

            "status": "success",

            "timestamp": datetime.utcnow().isoformat(),

            "pipeline": {

                "engine": "Clinical AI Engine",

                "version": self.ENGINE_VERSION,

            },

            "patient_context":
                self._serialize(
                    patient_context
                ),

            "entities":
                self._serialize(
                    entities
                ),

            "agents": {

                "symptom_analysis":
                    self._serialize(
                        agents.get(
                            "symptom_analysis"
                        )
                    ),

                "diagnosis_analysis":
                    self._serialize(
                        agents.get(
                            "diagnosis_analysis"
                        )
                    ),

            },

            "emergency":
                self._serialize(
                    agents.get(
                        "emergency_analysis"
                    )
                ),

            "follow_up_questions":
                self._serialize(
                    follow_up
                ),

            "risk_assessment":
                self._serialize(
                    risk
                ),

            "recommendation":
                self._serialize(
                    agents.get(
                        "recommendation_analysis"
                    )
                ),

            "medication_alerts":
                self._serialize(
                    agents.get(
                        "medication_analysis"
                    )
                ),

            "explanation":
                self._serialize(
                    explanation
                ),

            "clinical_summary":
                self._serialize(
                    summary
                ),

            "confidence":
                self._serialize(
                    confidence
                ),

            "rag": {

                "documents": documents,

                "citations":
                    self._serialize(
                        rag_result.get(
                            "citations",
                            [],
                        )
                    ),

                "metadata":
                    self._serialize(
                        rag_result.get(
                            "metadata",
                            {},
                        )
                    ),
            },
        }

        logger.info(
            "Response built successfully"
        )

        return response