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
            # Check for potential Hinglish (English alphabet but Hindi words)
            # A simple heuristic: if fasttext says 'en' but we want to handle Hinglish
            # we will process chunks. For now, if the user explicitly triggers Hinglish
            # or if we detect mixed text. We will assume the text might be mixed.
            english_text = self._process_mixed_language(text)
            translated = english_text != text
        else:
            # Direct translation for purely foreign scripts
            english_text = self.translator.translate(text, source_lang_code=lang_code)
            translated = True
            
    def _process_mixed_language(self, text: str) -> str:
        """
        Chunks the sentence, transliterates Hinglish to Devanagari,
        and translates the Hindi chunks while keeping English chunks.
        """
        try:
            from indic_transliteration import sanscript
            from indic_transliteration.sanscript import transliterate
            import spacy
            
            # Simple chunking by words for the prototype
            words = text.split()
            processed_chunks = []
            
            for word in words:
                # Detect language of the word
                det = self.detector.detect_language(word)
                if det.get("language") in ["hi", "ur", "mr"] or word.lower() in ["mujhe", "hai", "dard", "bukhar", "aur", "khansi", "se"]:
                    # It's likely phonetic Hindi, transliterate it
                    # ITRANS or HK format is typical, but we'll use a simple transliteration
                    devanagari = transliterate(word, sanscript.ITRANS, sanscript.DEVANAGARI)
                    # Translate the Devanagari back to English
                    eng_word = self.translator.translate(devanagari, source_lang_code="hi")
                    processed_chunks.append(eng_word)
                else:
                    # Keep English as-is
                    processed_chunks.append(word)
                    
            return " ".join(processed_chunks)
        except ImportError:
            logger.warning("indic-transliteration or spacy not installed. Returning original text.")
            return text
            
        # 3. Normalize literal translations to medical terms
        normalized_text = self.normalizer.normalize(english_text)
        
        return {
            "original_text": text,
            "detected_language": lang_code,
            "confidence": confidence,
            "was_translated": translated,
            "english_text": normalized_text
        }
