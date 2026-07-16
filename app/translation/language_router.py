import logging
from app.rag.language_detector import LanguageDetector
from app.translation.translator import LocalTranslator
from app.translation.medical_translation import MedicalTermNormalizer

logger = logging.getLogger(__name__)

class TranslationRouter:
    """
    Detects the language of the input text and routes it to the local 
    translator if it is not English. Then applies medical normalization.
    """
    def __init__(self):
        self.detector = LanguageDetector()
        self.translator = LocalTranslator()
        self.normalizer = MedicalTermNormalizer()
        
    def process(self, text: str) -> dict:
        """
        Processes incoming text.
        Returns a dict containing original text, detected language, and English translation.
        """
        if not text or not text.strip():
            return {
                "original_text": "",
                "detected_language": "en",
                "confidence": 0.0,
                "english_text": ""
            }
            
        # 1. Detect language
        detection = self.detector.detect_language(text)
        lang_code = detection.get("language", "en")
        confidence = detection.get("confidence", 0.0)
        
        # 2. Route for translation if not English
        if lang_code == "en":
            english_text = text
            translated = False
        else:
            english_text = self.translator.translate(text, source_lang_code=lang_code)
            translated = True
            
        # 3. Normalize literal translations to medical terms
        normalized_text = self.normalizer.normalize(english_text)
        
        return {
            "original_text": text,
            "detected_language": lang_code,
            "confidence": confidence,
            "was_translated": translated,
            "english_text": normalized_text
        }
