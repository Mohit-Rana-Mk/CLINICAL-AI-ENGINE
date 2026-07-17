import spacy
from loguru import logger
from typing import List, Dict

class BodyPartDetector:
    def __init__(self, model_name="en_core_web_sm"):
        logger.info(f"Initializing BodyPartDetector with spaCy model: {model_name}")
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            logger.warning(f"spaCy model '{model_name}' not found. Downloading...")
            spacy.cli.download(model_name)
            self.nlp = spacy.load(model_name)
            
        # A basic vocabulary list of body parts to match against.
        # In a real clinical engine, this would be expanded or use a specialized medical model like en_core_sci_sm.
        self.body_parts_vocab = {
            "head", "arm", "leg", "chest", "stomach", "abdomen", "back", "neck",
            "eye", "ear", "nose", "throat", "mouth", "tooth", "teeth", "shoulder",
            "hand", "finger", "knee", "foot", "toe", "ankle", "wrist", "hip", "pelvis"
        }

    def detect(self, text: str) -> List[Dict[str, str]]:
        """
        Uses dependency parsing to extract body parts and their associated modifiers 
        (e.g., 'left arm' instead of just 'arm').
        """
        doc = self.nlp(text)
        extracted_body_parts = []
        
        for token in doc:
            if token.lemma_.lower() in self.body_parts_vocab:
                # Find modifiers like "left", "right", "upper", "lower" attached to this body part
                modifiers = [child.text.lower() for child in token.children if child.dep_ in ("amod", "compound")]
                
                if modifiers:
                    full_body_part = " ".join(modifiers) + " " + token.text.lower()
                else:
                    full_body_part = token.text.lower()
                    
                extracted_body_parts.append({
                    "entity": token.text,
                    "linked_part": full_body_part
                })
                
        return extracted_body_parts

# Singleton instance
body_part_detector_instance = None

def get_body_part_detector():
    global body_part_detector_instance
    if body_part_detector_instance is None:
        body_part_detector_instance = BodyPartDetector()
    return body_part_detector_instance
