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
        ]

        self.locations = [
            "chest",
            "head",
            "stomach",
            "abdomen",
            "back",
            "leg",
            "arm",
            "throat",
        ]

    def extract(
        self,
        text: str,
    ) -> ExtractedEntities:

        text = text or ""
        text_lower = text.lower()

        # ----------------------------------
        # Symptom Extraction
        # ----------------------------------

        detected_symptoms = set()

        all_terms = (
            set(
                self.synonym_mapper.synonym_to_canonical.keys()
            )
            | set(COMMON_SYMPTOMS)
        )

        all_terms = sorted(
            all_terms,
            key=len,
            reverse=True,
        )

        for term in all_terms:

            pattern = rf"\b{re.escape(term)}\b"

            if re.search(pattern, text_lower):

                canonical = self.synonym_mapper.map_synonym(
                    term
                )

                if not self.negation_detector.is_negated(
                    text_lower,
                    term,
                ):
                    detected_symptoms.add(canonical)

        # ----------------------------------
        # Duration
        # ----------------------------------

        duration = self.temporal_extractor.extract(
            text
        )

        # ----------------------------------
        # Severity
        # ----------------------------------

        severity = None

        for keyword in self.severity_keywords:

            if re.search(
                rf"\b{keyword}\b",
                text_lower,
            ):
                severity = keyword
                break

        # ----------------------------------
        # Pain Scale
        # ----------------------------------

        pain_match = re.search(
            r"\b(\d+)\s*(?:/|out of)\s*10\b",
            text_lower,
        )

        if pain_match:

            pain = pain_match.group(1)

            if severity:

                severity = (
                    f"{severity} ({pain}/10)"
                )

            else:

                severity = (
                    f"Pain scale {pain}/10"
                )

        # ----------------------------------
        # Temperature
        # ----------------------------------

        temperature = None

        temp_match = re.search(
            r"\b(\d{2,3}(?:\.\d)?)\s*(?:degrees|degree|f|c|fahrenheit|celsius)?\b",
            text_lower,
        )

        if temp_match:

            value = float(
                temp_match.group(1)
            )

            if 35 <= value <= 108:
                temperature = str(value)

        # ----------------------------------
        # Body Location
        # ----------------------------------

        body_location = None

        for location in self.locations:

            if re.search(
                rf"\b{location}\b",
                text_lower,
            ):
                body_location = location
                break

        # ----------------------------------
        # Associated Symptoms
        # ----------------------------------

        associated_symptoms = []

        if (
            "fever" in detected_symptoms
            and "cough" in detected_symptoms
        ):
            associated_symptoms.append(
                "possible_respiratory_infection"
            )

        if (
            "chest pain" in detected_symptoms
            and "breathing difficulty"
            in detected_symptoms
        ):
            associated_symptoms.append(
                "possible_cardiopulmonary_condition"
            )

        return ExtractedEntities(

            symptoms=sorted(
                detected_symptoms
            ),

            duration=duration,

            severity=severity,

            body_location=body_location,

            temperature=temperature,

            associated_symptoms=associated_symptoms,
        )