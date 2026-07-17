import uuid
from typing import Dict, Any, List
from datetime import datetime

class ClinicalJSONBuilder:
    def __init__(self, version="1.0.0"):
        self.version = version

    def build(self, 
              patient_id: str = None,
              session_id: str = None,
              intent: str = "",
              language: str = "en",
              severity: str = "",
              symptoms: List[Dict[str, Any]] = None,
              duration: str = "",
              body_parts: List[Dict[str, str]] = None,
              negations: List[str] = None,
              vitals: Dict[str, Any] = None,
              medications: List[Dict[str, str]] = None,
              family_history: List[str] = None,
              lifestyle: Dict[str, Any] = None,
              lab_results: List[Dict[str, Any]] = None,
              confidence_score: float = 1.0) -> Dict[str, Any]:
        """
        Constructs the final standardized Clinical JSON.
        """
        # Ensure default lists/dicts
        symptoms = symptoms or []
        body_parts = body_parts or []
        negations = negations or []
        vitals = vitals or {}
        medications = medications or []
        family_history = family_history or []
        lifestyle = lifestyle or {}
        lab_results = lab_results or []
        
        # Generate session_id if none provided
        session_id = session_id or str(uuid.uuid4())
        
        json_output = {
            "metadata": {
                "patient_id": patient_id,
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "nlp_engine_version": self.version
            },
            "clinical_payload": {
                "intent": intent,
                "language": language,
                "severity": severity,
                "symptoms": symptoms,
                "duration": duration,
                "body_parts": body_parts,
                "negations": negations,
                "vitals": vitals,
                "medications": medications,
                "family_history": family_history,
                "lifestyle": lifestyle,
                "lab_results": lab_results,
                "confidence_score": confidence_score
            }
        }
        
        return json_output

# Singleton instance
clinical_json_builder_instance = None

def get_clinical_json_builder():
    global clinical_json_builder_instance
    if clinical_json_builder_instance is None:
        clinical_json_builder_instance = ClinicalJSONBuilder()
    return clinical_json_builder_instance
