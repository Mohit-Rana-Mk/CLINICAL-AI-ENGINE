import re

from app.ai_engine.constants import COMMON_SYMPTOMS
from app.ai_engine.negation_detector import NegationDetector
from app.ai_engine.schemas import ExtractedEntities
from app.ai_engine.synonym_mapper import SynonymMapper
from app.ai_engine.temporal_extractor import TemporalExtractor
from app.ai_engine.synonym_mapper import SynonymMapper

class MedicalEntityExtractor:
    """
    Production Medical Entity Extraction Engine.

    Responsibilities
    ----------------
    - Symptom extraction
    - Negation detection
    - Synonym normalization
    - Duration extraction
    - Severity extraction
    - Pain scale extraction
    - Temperature extraction
    - Body location extraction
    - Associated symptom extraction
    """

    def __init__(self):
        # Initialize our newly upgraded NLP modules
        self.negation_detector = NegationDetector()
        self.temporal_extractor = TemporalExtractor()
        self.synonym_mapper = SynonymMapper()
        
        self.severity_keywords = ["mild", "moderate", "severe", "extreme"]
        self.locations = ["chest", "head", "stomach", "abdomen", "back", "leg", "arm", "throat"]

    def extract(self, text: str) -> ExtractedEntities:

        text_lower = text.lower()
        
        # 1. Extract Symptoms with Synonym Mapping and Negation Detection
        from app.ai_engine.constants import COMMON_SYMPTOMS

        detected_symptoms = set()

        # Sort terms by length descending to match longest phrases first
        all_terms = set(self.synonym_mapper.synonym_to_canonical.keys()) | set(COMMON_SYMPTOMS)
        all_synonyms = sorted(all_terms, key=len, reverse=True)
        
        for syn in all_synonyms:
            pattern = rf"\b{re.escape(syn)}\b"
            if re.search(pattern, text_lower):
                canonical_symptom = self.synonym_mapper.map_synonym(syn)
                # Check negation on the specific phrase found in the text
                if not self.negation_detector.is_negated(text_lower, syn):
                    detected_symptoms.add(canonical_symptom)
                    
        # 2. Extract Duration
        duration = self.temporal_extractor.extract(text)
        
        # 3. Extract Severity & Pain Scale
        severity = None

        for keyword in self.severity_keywords:

            if re.search(
                rf"\b{keyword}\b",
                text_lower,
            ):
                severity = keyword
                break
                
        # Pain scale (e.g., 7/10 or 7 out of 10)
        pain_match = re.search(r"\b(\d+)\s*(?:/|out of)\s*10\b", text_lower)
        if pain_match:

            pain = pain_match.group(1)

            if severity:

                severity += f" ({pain}/10)"

            else:
                severity += f", pain scale {pain_level}"
                
        # 4. Extract Temperature
        temperature = None
        temp_match = re.search(r"\b(\d{2,3}(?:\.\d)?)\s*(?:degrees|degree|f|c|fahrenheit|celsius)?\b", text_lower)
        if temp_match:
            val = float(temp_match.group(1))
            # Basic sanity check for human body temp bounds
            if 35 <= val <= 108: 
                temperature = str(val)
                
        # 5. Extract Body Location
        body_location = None
        for loc in self.locations:
            if re.search(rf"\b{loc}\b", text_lower):
                body_location = loc
                break

        return ExtractedEntities(

            symptoms=sorted(list(detected_symptoms)),

            duration=duration,

            severity=severity,

            body_location=body_location,
            temperature=temperature
        )