import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class AuditLogger:

    def log(
        self,
        patient_id,
        entities,
        risk,
    ):

        audit_id = str(uuid.uuid4())

        logger.info(
            "AUDIT | %s | patient=%s | symptoms=%s",
            audit_id,
            patient_id,
            getattr(
                entities,
                "symptoms",
                [],
            ),
        )

        return {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "patient_id": patient_id,
            "risk": getattr(
                risk,
                "overall_risk",
                "Unknown",
            ),
            "status": "completed",
            "component": "audit_logger",
        }