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

        diagnosis_status = (
        "completed"
        if agents and agents.get("diagnosis_analysis")
        else "skipped"
        )

        recommendation_status = (
        "completed"
        if agents and agents.get("recommendation_analysis")
        else "skipped"
        )

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
                "status": diagnosis_status,
            },
            {
                "step": 4,
                "module": "Recommendation Agent",
                "status": recommendation_status,
            },
            {
                "step": 5,
                "module": "Response Builder",
                "status": "completed",
            },
        ]