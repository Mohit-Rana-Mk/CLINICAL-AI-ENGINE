import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class ResponseBuilder:
    """
    Converts internal Clinical AI pipeline
    objects into a production-ready API response.
    """

    def _serialize(self, value):

        if value is None:
            return None

        if hasattr(value, "model_dump"):
            return value.model_dump()

        if isinstance(value, dict):
            return {
                key: self._serialize(val)
                for key, val in value.items()
            }

        if isinstance(value, list):
            return [
                self._serialize(item)
                for item in value
            ]

        return value

    def build(
        self,
        patient_context,
        entities,
        agents=None,
        risk=None,
        explanation=None,
        summary=None,
        confidence=None,
        rag_result=None,
        agent_result=None,
    ):

        logger.info(
            "Building final clinical response"
        )

        if agents is None:
            agents = agent_result or {}

        if rag_result is None:
            rag_result = {}

        # ----------------------------------------
        # RAG Documents
        # ----------------------------------------

        rag_documents = []

        for doc in rag_result.get("documents", []):

            rag_documents.append(
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

        emergency = agents.get(
            "emergency_analysis"
        )

        recommendation = agents.get(
            "recommendation_analysis"
        )

        medication = agents.get(
            "medication_analysis"
        )

        response = {

            "status": "success",

            "timestamp": datetime.utcnow().isoformat(),

            "pipeline": {
                "version": "1.0.0",
                "engine": "Clinical AI Engine",
            },

            "patient_context":
                self._serialize(
                    patient_context
                ),

            "entities":
                self._serialize(
                    entities
                ),

            "agents":
                self._serialize(
                    {
                        "symptom_analysis":
                            agents.get(
                                "symptom_analysis"
                            ),

                        "diagnosis_analysis":
                            agents.get(
                                "diagnosis_analysis"
                            ),
                    }
                ),

            "emergency":
                self._serialize(
                    emergency
                ),

            "risk_assessment":
                self._serialize(
                    risk
                ),

            "recommendation":
                self._serialize(
                    recommendation
                ),

            "medication_alerts":
                self._serialize(
                    medication
                ),

            "clinical_summary":
                self._serialize(
                    summary
                ),

            "explanation":
                self._serialize(
                    explanation
                ),

            "confidence":
                self._serialize(
                    confidence
                ),

            "rag": {

                "documents":
                    rag_documents,

                "citations":
                    rag_result.get(
                        "citations",
                        []
                    ),

                "metadata":
                    rag_result.get(
                        "metadata",
                        {}
                    ),
            },
        }

        return response