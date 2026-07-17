import logging
from datetime import datetime
from typing import Any


logger = logging.getLogger(__name__)


class DecisionTrace:
    """
    Clinical Decision Trace.

    Records every major decision taken by the
    Clinical AI pipeline.

    Future:
    - Graph visualization
    - Explainable AI dashboard
    - Clinical reasoning timeline
    """

    def __init__(self):

        self._steps: list[dict[str, Any]] = []

    def add_step(
        self,
        stage: str,
        details: Any,
    ) -> None:

        self._steps.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "stage": stage,
                "details": details,
            }
        )

    def build(self) -> list[dict[str, Any]]:

        return self._steps

    def clear(self) -> None:

        self._steps.clear()

    def statistics(self) -> dict:

        return {
            "total_steps": len(self._steps),
            "generated_at": datetime.utcnow().isoformat(),
        }