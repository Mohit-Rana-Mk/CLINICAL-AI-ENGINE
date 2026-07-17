import logging
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class TimelineBuilder:
    """
    Builds a chronological clinical timeline
    from conversation history and patient memory.

    Future:
    - Database timeline
    - EMR timeline
    - Hospital visits
    - Lab history
    """

    def build(
        self,
        conversation_history: list[dict[str, Any]],
        patient_memory: dict[str, Any],
    ) -> list[dict[str, Any]]:

        timeline = []

        for item in conversation_history:

            timeline.append(
                {
                    "timestamp": item.get("timestamp"),
                    "event_type": "conversation",
                    "role": item.get("role"),
                    "description": item.get("message"),
                }
            )

        for symptom in patient_memory.get(
            "symptoms",
            [],
        ):

            timeline.append(
                {
                    "timestamp": patient_memory.get(
                        "last_updated"
                    ),
                    "event_type": "symptom",
                    "description": symptom,
                }
            )

        for diagnosis in patient_memory.get(
            "diagnoses",
            [],
        ):

            timeline.append(
                {
                    "timestamp": patient_memory.get(
                        "last_updated"
                    ),
                    "event_type": "diagnosis",
                    "description": diagnosis,
                }
            )

        for recommendation in patient_memory.get(
            "recommendations",
            [],
        ):

            timeline.append(
                {
                    "timestamp": patient_memory.get(
                        "last_updated"
                    ),
                    "event_type": "recommendation",
                    "description": recommendation,
                }
            )

        timeline.sort(
            key=lambda x: x.get("timestamp") or "",
            reverse=False,
        )

        logger.info(
            "Clinical timeline generated (%s events)",
            len(timeline),
        )

        return timeline

    def latest_event(
        self,
        timeline: list[dict[str, Any]],
    ) -> dict | None:

        if not timeline:
            return None

        return timeline[-1]

    def statistics(
        self,
        timeline: list[dict[str, Any]],
    ) -> dict:

        stats = {}

        for event in timeline:

            event_type = event["event_type"]

            stats[event_type] = (
                stats.get(event_type, 0) + 1
            )

        return {
            "generated_at": datetime.utcnow().isoformat(),
            "total_events": len(timeline),
            "breakdown": stats,
        }