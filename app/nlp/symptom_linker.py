from typing import List, Dict, Any
from loguru import logger
import spacy

class SymptomLinker:
    def __init__(self, model_name="en_core_web_sm"):
        logger.info(f"Initializing SymptomLinker with spaCy model: {model_name}")
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            logger.warning(f"spaCy model '{model_name}' not found. Downloading...")
            spacy.cli.download(model_name)
            self.nlp = spacy.load(model_name)

    def link(self, text: str, symptoms: List[str], body_parts: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Links extracted symptoms to extracted body parts using dependency parsing and proximity.
        """
        logger.debug("Linking symptoms to body parts")
        linked_results = []
        text_lower = text.lower()
        
        # Simple heuristic: for each symptom, find the closest body part in the text
        # In a more advanced implementation, we would use dependency paths.
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            best_part = None
            min_dist = float('inf')
            
            # Find index of symptom
            symptom_idx = text_lower.find(symptom_lower)
            
            if symptom_idx != -1:
                for part_obj in body_parts:
                    part_str = part_obj["linked_part"]
                    part_idx = text_lower.find(part_str)
                    
                    if part_idx != -1:
                        # Calculate character distance
                        dist = abs(symptom_idx - part_idx)
                        if dist < min_dist:
                            min_dist = dist
                            best_part = part_str
            
            linked_results.append({
                "symptom": symptom,
                "body_part": best_part if min_dist < 50 else None # 50 char threshold
            })
            
        return linked_results

# Singleton instance
symptom_linker_instance = None

def get_symptom_linker():
    global symptom_linker_instance
    if symptom_linker_instance is None:
        symptom_linker_instance = SymptomLinker()
    return symptom_linker_instance
