import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class ResponseMapper:
    """
    Maps internal pipeline responses to HealTrack platform specification formats.
    """
    @staticmethod
    def map_to_healtrack(pipeline_response: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Mapping AI Engine response to HealTrack format")
        
        return {
            "status": pipeline_response.get("status", "success"),
            "request_id": pipeline_response.get("request_id"),
            "timestamp": pipeline_response.get("timestamp"),
            "healtrack_payload": {
                "patient_context": pipeline_response.get("patient_context", {}),
                "entities": pipeline_response.get("entities", {}),
                "image_analysis": pipeline_response.get("image_analysis", {}),
                "voice_analysis": pipeline_response.get("voice_analysis", {}),
                "retrieved_evidence": pipeline_response.get("rag", {}).get("documents", []),
                "differential_diagnosis": pipeline_response.get("agents", {}).get("diagnosis_analysis", {}).get("possible_conditions", []),
                "risk_assessment": pipeline_response.get("risk_assessment", {}),
                "recommendations": pipeline_response.get("recommendation", {}),
                "doctor_summary": pipeline_response.get("clinical_summary", {}),
                "confidence": pipeline_response.get("confidence", {}),
                "audit_id": pipeline_response.get("audit", {}).get("audit_id"),
            },
            "timeline": pipeline_response.get("timeline", []),
            "follow_up_questions": pipeline_response.get("follow_up_questions", {}),
        }