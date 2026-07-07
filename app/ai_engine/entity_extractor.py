import re

from app.ai_engine.constants import COMMON_SYMPTOMS
from app.ai_engine.schemas import ExtractedEntities


class MedicalEntityExtractor:

    def extract(self, text: str) -> ExtractedEntities:
        text_lower = text.lower()

        symptoms = []

        for symptom in COMMON_SYMPTOMS:
            if symptom in text_lower:
                symptoms.append(symptom)

        duration = None

        duration_match = re.search(
            r"(\d+)\s*(day|days|week|weeks|month|months)",
            text_lower
        )

        if duration_match:
            duration = duration_match.group()

        return ExtractedEntities(
            symptoms=symptoms,
            duration=duration
        )