import logging
from datetime import date, datetime
from uuid import UUID

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
            return self._serialize(value.model_dump())

        if isinstance(value, (datetime, date, UUID)):
            return value.isoformat()

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
        vision=None,
        reasoning=None,
        decision_trace=None,
        audit=None,
    ):

        logger.info(
            "Building final API response"
        )

        agents = agents or {}
        rag_result = rag_result or {}

        emergency = self._serialize(agents.get("emergency_analysis")) or {
            "is_emergency": False,
            "level": "NONE",
            "reason": "Emergency assessment unavailable.",
            "recommendation": "Seek clinical assessment if symptoms worsen.",
            "detected_patterns": [],
        }
        medication_alerts = self._serialize(agents.get("medication_analysis")) or {
            "has_alert": False,
            "alert_count": 0,
            "alerts": [],
            "summary": "No medication safety alerts detected.",
        }
        recommendation = self._serialize(agents.get("recommendation_analysis")) or {
            "immediate_action": "Continue routine clinical assessment.",
            "precautions": [],
            "monitoring": [],
            "doctor_visit": "Seek medical advice if symptoms persist or worsen.",
            "lifestyle": [],
        }

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

            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",

            "pipeline": {

                "engine": "Clinical AI Engine",

                "version": self.ENGINE_VERSION,

                "response_metadata": {
                "generated_by": "response_builder",
                "engine_version": self.ENGINE_VERSION,
            },

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

            "vision": self._serialize(
                vision
            ),

            "image_analysis": self._serialize(
                vision.get("image_analysis", {})
                if vision
                else {}
            ),

            "emergency": emergency,

            "follow_up_questions":
                self._serialize(
                    follow_up
                ),

            "risk_assessment":
                self._serialize(
                    risk
                ),

            "recommendation": recommendation,

            "medication_alerts": medication_alerts,

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

            "reasoning": self._serialize(
                reasoning
            ),

            "decision_trace": self._serialize(
                decision_trace or []
            ),

            "audit": self._serialize(
                audit or {}
            ),
        }

        logger.info(
            "Response built successfully"
        )

        return response
