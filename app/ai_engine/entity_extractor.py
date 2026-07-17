import re

from app.ai_engine.schemas import ExtractedEntities
from app.ai_engine.negation_detector import NegationDetector
from app.ai_engine.temporal_extractor import TemporalExtractor
from app.ai_engine.synonym_mapper import SynonymMapper
from app.ai_engine.family_history_extractor import FamilyHistoryExtractor
from app.ai_engine.smoking_alcohol_extractor import SmokingAlcoholExtractor
from app.ai_engine.travel_history_extractor import TravelHistoryExtractor
from app.ai_engine.lifestyle_extractor import LifestyleExtractor
from app.ai_engine.constants import COMMON_SYMPTOMS, BODY_LOCATIONS


class MedicalEntityExtractor:
    def __init__(self):
        # ── Existing rule-based NLP modules ───────────────────────────────
        self.negation_detector = NegationDetector()
        self.temporal_extractor = TemporalExtractor()
        self.synonym_mapper = SynonymMapper()

        # ── Day 7: New lifestyle & social history extractors ──────────────
        self.family_history_extractor = FamilyHistoryExtractor()
        self.smoking_alcohol_extractor = SmokingAlcoholExtractor()
        self.travel_history_extractor = TravelHistoryExtractor()
        self.lifestyle_extractor = LifestyleExtractor()

        # ── Keyword lists (now sourced from constants) ─────────────────────
        self.severity_keywords = ["mild", "moderate", "severe", "extreme"]

    def extract(self, text: str) -> ExtractedEntities:
        text_lower = text.lower()

        # ── 1. Extract Symptoms with Synonym Mapping and Negation Detection ─
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

        # ── 2. Extract Duration ───────────────────────────────────────────
        duration = self.temporal_extractor.extract(text)

        # ── 3. Extract Severity & Pain Scale ─────────────────────────────
        severity = None
        for keyword in self.severity_keywords:
            if re.search(rf"\b{keyword}\b", text_lower):
                severity = keyword
                break

        # Pain scale (e.g., 7/10 or 7 out of 10)
        pain_match = re.search(r"\b(\d+)\s*(?:/|out of)\s*10\b", text_lower)
        if pain_match:
            pain_level = f"{pain_match.group(1)}/10"
            if not severity:
                severity = f"pain scale {pain_level}"
            else:
                severity += f", pain scale {pain_level}"

        # ── 4. Extract Temperature ────────────────────────────────────────
        temperature = None
        temp_match = re.search(r"\b(\d{2,3}(?:\.\d)?)\s*(?:degrees|degree|f|c|fahrenheit|celsius)?\b", text_lower)
        if temp_match:
            val = float(temp_match.group(1))
            # Basic sanity check for human body temp bounds
            if 35 <= val <= 108:
                temperature = str(val)

        # ── 5. Extract Body Location (uses expanded BODY_LOCATIONS) ───────
        body_location = None
        # Sort by length descending so "upper back" is matched before "back"
        for loc in sorted(BODY_LOCATIONS, key=len, reverse=True):
            if re.search(rf"\b{re.escape(loc)}\b", text_lower):
                body_location = loc
                break

        # ── 6. Day 7: Family History ──────────────────────────────────────
        family_history = self.family_history_extractor.extract(text)

        # ── 7. Day 7: Smoking & Alcohol Status ───────────────────────────
        smoking_status, alcohol_use = self.smoking_alcohol_extractor.extract(text)

        # ── 8. Day 7: Travel History ──────────────────────────────────────
        travel_history = self.travel_history_extractor.extract(text)

        # ── 9. Day 7: Lifestyle Factors ───────────────────────────────────
        lifestyle_factors = self.lifestyle_extractor.extract(text)

        # ── 10. Extract Pregnancy Status ──────────────────────────────────
        pregnancy_status = None
        pregnancy_match = re.search(r"\b(pregnant|pregnancy|expecting|trimester|\d+\s*(?:weeks|months)\s*pregnant)\b", text_lower)
        if pregnancy_match:
            pregnancy_status = pregnancy_match.group(1)

        # ── 11. Extract Occupation ────────────────────────────────────────
        occupation = None
        occupation_match = re.search(r"\b(?:work as a|job is|i am a|profession is|working as a)\s+([a-zA-Z\s]+?)(?:\.|and|but|,|$)", text_lower)
        if occupation_match:
            occupation = occupation_match.group(1).strip()

        return ExtractedEntities(
            symptoms=list(detected_symptoms),
            duration=duration,
            severity=severity,
            body_location=body_location,
            temperature=temperature,
            family_history=family_history,
            smoking_status=smoking_status,
            alcohol_use=alcohol_use,
            travel_history=travel_history,
            lifestyle_factors=lifestyle_factors,
            pregnancy_status=pregnancy_status,
            occupation=occupation,
        )