import re
import logging

logger = logging.getLogger(__name__)

class MedicalTermNormalizer:
    """
    Normalizes literal English translations of regional symptoms into standardized medical terms.
    For example: "sweet food" -> "diabetes", "breathing difficulty" -> "dyspnea".
    """
    
    DICTIONARY = {
        # Hindi/Urdu literal translations
        r"\bsugar\b": "diabetes",
        r"\bsweet food\b": "diabetes",
        r"\bsweet blood\b": "diabetes",
        r"\bbreathing difficulty\b": "dyspnea",
        r"\bdifficulty breathing\b": "dyspnea",
        r"\bchest pain\b": "chest pain", # Keep this one as is, just an example
        r"\bheart ache\b": "chest pain",
        r"\bhead ache\b": "headache",
        r"\bstomach ache\b": "abdominal pain",
        r"\bbelly pain\b": "abdominal pain",
        r"\bloose motion\b": "diarrhea",
        r"\bwatery stool\b": "diarrhea",
        r"\bfeeling cold\b": "chills",
        r"\bbody pain\b": "myalgia",
        r"\bmuscle pain\b": "myalgia",
        r"\bjoint pain\b": "arthralgia",
        r"\bthrowing up\b": "vomiting",
        r"\bfeeling puke\b": "nausea",
        r"\bpuking\b": "vomiting",
        r"\bspinning head\b": "vertigo",
        r"\bdizziness\b": "vertigo",
        r"\bblood pressure high\b": "hypertension",
        r"\bhigh bp\b": "hypertension",
        r"\bblood pressure low\b": "hypotension",
        r"\blow bp\b": "hypotension",
        r"\bfast heartbeat\b": "tachycardia",
        r"\bslow heartbeat\b": "bradycardia",
        r"\byellow eyes\b": "jaundice",
        r"\byellow skin\b": "jaundice",
        r"\bcan't sleep\b": "insomnia",
        r"\bno sleep\b": "insomnia",
    }
    
    def __init__(self):
        # Compile regexes for faster matching, ignoring case
        self.compiled_dict = {
            re.compile(pattern, re.IGNORECASE): replacement
            for pattern, replacement in self.DICTIONARY.items()
        }
        
    def normalize(self, text: str) -> str:
        """
        Scans the translated text and replaces literal phrasing with medical terminology.
        """
        if not text:
            return ""
            
        normalized_text = text
        for pattern, replacement in self.compiled_dict.items():
            normalized_text = pattern.sub(replacement, normalized_text)
            
        return normalized_text
