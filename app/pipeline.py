import logging
import uuid
from typing import Dict, Any

from app.translation.language_router import TranslationRouter
from app.nlp.intent_classifier import get_intent_classifier
from app.nlp.severity_detector import get_severity_detector
from app.nlp.clinical_json_builder import get_clinical_json_builder
from app.nlp.followup_engine import get_followup_engine

logger = logging.getLogger(__name__)

class ClinicalPipeline:
    def __init__(self):
        logger.info("Initializing Final Clinical Pipeline...")
        self.language_router = TranslationRouter()
        self.intent_classifier = get_intent_classifier()
        self.severity_detector = get_severity_detector()
        self.json_builder = get_clinical_json_builder()
        self.followup_engine = get_followup_engine()
        
        # In a real scenario, you'd also load:
        # self.body_part_detector = get_body_part_detector()
        # self.entity_extractor = get_entity_extractor()
        # self.symptom_linker = get_symptom_linker()
        # self.ocr_pipeline = OCRPipeline()
        # self.speech_to_text = SpeechToText()

    def process(self, text_input: str, session_id: str = None, patient_id: str = None) -> Dict[str, Any]:
        """
        Master Orchestrator for the Clinical AI Engine.
        """
        if not session_id:
            session_id = str(uuid.uuid4())
            
        logger.info(f"Processing input for session {session_id}")
        
        # 1. Language Routing & Translation (handles Hinglish & Foreign text)
        translation_result = self.language_router.process(text_input)
        processed_text = translation_result["english_text"]
        detected_language = translation_result["detected_language"]
        
        # 2. NLP Analysis
        intent_result = self.intent_classifier.classify(processed_text)
        severity_result = self.severity_detector.detect(processed_text)
        
        # Mocking entity extraction for pipeline orchestration
        extracted_symptoms = ["chest pain"] if "chest pain" in processed_text.lower() else []
        extracted_body_parts = ["chest"] if "chest" in processed_text.lower() else []
        
        # 3. Build Clinical Data
        clinical_data = self.json_builder.build(
            patient_id=patient_id,
            session_id=session_id,
            intent=intent_result.value,
            language=detected_language,
            severity=severity_result.value,
            symptoms=extracted_symptoms,
            body_parts=extracted_body_parts,
            confidence_score=0.9
        )
        
        # 4. Generate Follow-up Action
        followup_action = self.followup_engine.generate_followup(clinical_data)
        
        # 5. Final Output Assembly
        final_output = {
            "clinical_data": clinical_data["clinical_payload"],
            "metadata": clinical_data["metadata"],
            "followup_action": followup_action
        }
        
        return final_output

# Singleton instance
clinical_pipeline_instance = None

def get_clinical_pipeline():
    global clinical_pipeline_instance
    if clinical_pipeline_instance is None:
        clinical_pipeline_instance = ClinicalPipeline()
    return clinical_pipeline_instance

if __name__ == "__main__":
    pipeline = get_clinical_pipeline()
    # Test Mixed Language / Hinglish
    result = pipeline.process("Mujhe severe chest pain hai")
    import json
    print(json.dumps(result, indent=2))
