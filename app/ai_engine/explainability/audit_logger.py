import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class AuditLogger:
    """
    Clinical AI Audit Logger.

    Every AI decision is stored for:
    - Clinical auditing
    - Explainability
    - Debugging
    - Compliance

    Future:
    PostgreSQL
    MongoDB
    Elasticsearch
    """

    def __init__(self):

        self.log_dir = Path("logs/audit")
        self.log_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def log(
        self,
        *,
        patient_id: int | None,
        message: str,
        response: dict[str, Any],
    ) -> str:

        audit_id = str(uuid.uuid4())

        payload = {

            "audit_id": audit_id,

            "timestamp": datetime.utcnow().isoformat(),

            "patient_id": patient_id,

            "message": message,

            "response": response,
        }

        file_path = (
            self.log_dir
            / f"{audit_id}.json"
        )

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                payload,
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(
            "Audit saved %s",
            audit_id,
        )

        return audit_id