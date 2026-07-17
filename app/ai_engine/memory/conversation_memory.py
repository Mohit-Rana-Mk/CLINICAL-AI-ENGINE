import logging
from collections import defaultdict
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class ConversationMemory:
    """
    Production Conversation Memory.

    Responsibilities
    ----------------
    - Store conversation history
    - Retrieve previous messages
    - Maintain session context
    - Provide recent conversation
    - Clear conversations

    NOTE
    ----
    Current implementation is in-memory.

    Future replacements:
    - Redis
    - PostgreSQL
    - MongoDB
    """

    def __init__(self):

        self._memory = defaultdict(list)

    def add_message(
        self,
        patient_id: int | None,
        role: str,
        message: str,
    ) -> None:

        if patient_id is None:
            patient_id = 0

        self._memory[patient_id].append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "role": role,
                "message": message,
            }
        )

        logger.info(
            "Conversation stored | patient=%s",
            patient_id,
        )

    def get_history(
        self,
        patient_id: int | None,
    ) -> list[dict[str, Any]]:

        if patient_id is None:
            patient_id = 0

        return self._memory.get(
            patient_id,
            [],
        )

    def get_recent_messages(
        self,
        patient_id: int | None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:

        history = self.get_history(
            patient_id
        )

        return history[-limit:]

    def clear(
        self,
        patient_id: int | None,
    ) -> None:

        if patient_id is None:
            patient_id = 0

        self._memory.pop(
            patient_id,
            None,
        )

        logger.info(
            "Conversation cleared | patient=%s",
            patient_id,
        )

    def total_messages(
        self,
        patient_id: int | None,
    ) -> int:

        return len(
            self.get_history(
                patient_id
            )
        )

    def summary(
        self,
        patient_id: int | None,
    ) -> dict:

        history = self.get_history(
            patient_id
        )

        return {
            "patient_id": patient_id,
            "messages": len(history),
            "last_message": (
                history[-1]
                if history
                else None
            ),
        }