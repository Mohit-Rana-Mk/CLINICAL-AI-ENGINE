import logging

logger = logging.getLogger(__name__)


class DecisionTrace:

    def build(
        self,
        entities,
        agents,
        risk,
    ):

        logger.info("Building decision trace")

        return [
            {
                "step": 1,
                "module": "Entity Extraction",
                "status": "completed",
            },
            {
                "step": 2,
                "module": "Risk Engine",
                "status": "completed",
                "risk": getattr(
                    risk,
                    "overall_risk",
                    "Unknown",
                ),
            },
            {
                "step": 3,
                "module": "Diagnosis Agent",
                "status": "completed",
            },
            {
                "step": 4,
                "module": "Recommendation Agent",
                "status": "completed",
            },
        ]