import re

from app.ai_engine.constants import COMMON_SYMPTOMS
from app.ai_engine.negation_detector import NegationDetector
from app.ai_engine.schemas import ExtractedEntities
from app.ai_engine.synonym_mapper import SynonymMapper
from app.ai_engine.temporal_extractor import TemporalExtractor


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

        self.negation_detector = NegationDetector()
        self.temporal_extractor = TemporalExtractor()
        self.synonym_mapper = SynonymMapper()

        self.severity_keywords = [
            "mild",
            "moderate",
            "severe",
            "extreme",
            "worst",
            "persistent",
            "constant",
            "intermittent",
        ]

        self.locations = [
            "head",
            "forehead",
            "eye",
            "ear",
            "nose",
            "throat",
            "neck",
            "chest",
            "back",
            "abdomen",
            "stomach",
            "pelvis",
            "arm",
            "hand",
            "leg",
            "knee",
            "foot",
        ]

    def extract(self, text: str) -> ExtractedEntities:

        text_lower = text.lower()

        detected_symptoms = set()

        associated_symptoms = []

        # ------------------------------------------
        # Symptom Detection
        # ------------------------------------------

        all_terms = (
            set(self.synonym_mapper.synonym_to_canonical.keys())
            | set(COMMON_SYMPTOMS)
        )

        all_terms = sorted(
            all_terms,
            key=len,
            reverse=True,
        )

        for term in all_terms:

            pattern = rf"\b{re.escape(term)}\b"

            if not re.search(pattern, text_lower):
                continue

            if self.negation_detector.is_negated(
                text_lower,
                term,
            ):
                continue

            canonical = self.synonym_mapper.map_synonym(term)

            detected_symptoms.add(canonical)

        # ------------------------------------------
        # Duration
        # ------------------------------------------

        duration = self.temporal_extractor.extract(text)

        # ------------------------------------------
        # Severity
        # ------------------------------------------

        severity = None

        for keyword in self.severity_keywords:

            if re.search(
                rf"\b{keyword}\b",
                text_lower,
            ):
                severity = keyword
                break

        pain_match = re.search(
            r"\b([0-9]|10)\s*(?:/|out of)\s*10\b",
            text_lower,
        )

        if pain_match:

            pain = pain_match.group(1)

            if severity:

                severity += f" ({pain}/10)"

            else:

                severity = f"{pain}/10"

        # ------------------------------------------
        # Temperature
        # ------------------------------------------

        temperature = None

        temp = re.search(
            r"\b(\d{2,3}(?:\.\d+)?)\s*(?:°|degrees?|c|f|celsius|fahrenheit)?\b",
            text_lower,
        )

        if temp:

            value = float(temp.group(1))

            if 35 <= value <= 108:

                temperature = str(value)

        # ------------------------------------------
        # Body Location
        # ------------------------------------------

        body_location = None

        for location in self.locations:

            if re.search(
                rf"\b{location}\b",
                text_lower,
            ):

                body_location = location
                break

        # ------------------------------------------
        # Associated Symptoms
        # ------------------------------------------

        association_keywords = [
            "along with",
            "also",
            "together with",
            "associated with",
            "plus",
            "and",
        ]

        if len(detected_symptoms) > 1:

            associated_symptoms = sorted(
                list(detected_symptoms)
            )

        # ------------------------------------------
        # Return
        # ------------------------------------------

        return ExtractedEntities(

            symptoms=sorted(list(detected_symptoms)),

            duration=duration,

            severity=severity,

            body_location=body_location,

            temperature=temperature,

            associated_symptoms=associated_symptoms,

        )