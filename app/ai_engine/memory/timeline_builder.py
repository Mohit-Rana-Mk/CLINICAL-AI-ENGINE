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

        timeline: list[dict[str, Any]] = []

        # -------------------------------------
        # Conversation History
        # -------------------------------------

        for item in conversation_history or []:

            timeline.append(
                {
                    "timestamp": item.get("timestamp"),
                    "event_type": "conversation",
                    "role": item.get("role"),
                    "description": item.get("message"),
                }
            )

        timestamp = patient_memory.get("last_updated")

        # -------------------------------------
        # Symptoms
        # -------------------------------------

        for symptom in patient_memory.get(
            "symptoms",
            [],
        ):

            timeline.append(
                {
                    "timestamp": timestamp,
                    "event_type": "symptom",
                    "description": str(symptom),
                }
            )

        # -------------------------------------
        # Diagnoses
        # -------------------------------------

        for diagnosis in patient_memory.get(
            "diagnoses",
            [],
        ):

            timeline.append(
                {
                    "timestamp": timestamp,
                    "event_type": "diagnosis",
                    "description": str(diagnosis),
                }
            )

        # -------------------------------------
        # Recommendations
        # -------------------------------------

        for recommendation in patient_memory.get(
            "recommendations",
            [],
        ):

            description = ""

            if hasattr(
                recommendation,
                "immediate_action",
            ):

                description = (
                    f"{recommendation.immediate_action}. "
                    f"Doctor Visit: "
                    f"{recommendation.doctor_visit}"
                )

            elif isinstance(
                recommendation,
                dict,
            ):

                description = (
                    f"{recommendation.get('immediate_action', '')}. "
                    f"Doctor Visit: "
                    f"{recommendation.get('doctor_visit', '')}"
                )

            else:

                description = str(
                    recommendation
                )

            timeline.append(
                {
                    "timestamp": timestamp,
                    "event_type": "recommendation",
                    "description": description,
                }
            )

        # -------------------------------------
        # Sort Timeline
        # -------------------------------------

        timeline.sort(
            key=lambda event: event.get(
                "timestamp"
            )
            or "",
        )

        logger.info(
            "Clinical timeline generated (%d events)",
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

        stats: dict[str, int] = {}

        for event in timeline:

            event_type = event.get(
                "event_type",
                "unknown",
            )

            stats[event_type] = (
                stats.get(
                    event_type,
                    0,
                )
                + 1
            )

        return {
            "generated_at": (
                datetime.utcnow().isoformat(
                    timespec="seconds"
                )
                + "Z"
            ),
            "total_events": len(
                timeline
            ),
            "breakdown": stats,
        }