import re
import logging

logger = logging.getLogger(__name__)


class MedicalNormalizer:
    def __init__(self, extra_terms: dict = None):
        """
        Args:
            extra_terms: Optional dict of additional abbreviation→full-form
                         mappings to merge with the built-in dictionary.
        """
        self.normalization_dict = {
            "HTN":  "Hypertension",
            "T2DM": "Type 2 Diabetes",
            "BP":   "Blood Pressure",
            "HR":   "Heart Rate",
            "DX":   "Diagnosis",
            "RX":   "Prescription",
            "HX":   "History",
            "TX":   "Treatment",
            "SX":   "Symptoms",
            "SOB":  "Shortness of Breath",
            "MI":   "Myocardial Infarction",
            "CHF":  "Congestive Heart Failure",
            "URI":  "Upper Respiratory Infection",
            "UTI":  "Urinary Tract Infection",
            "N/V":  "Nausea and Vomiting",
        }

        if extra_terms:
            self.normalization_dict.update(
                {k.upper(): v for k, v in extra_terms.items()}
            )

        self._build_regex()

    def _build_regex(self):
        """Compiles the regex pattern from the current normalization_dict."""
        normal_keys = [re.escape(k) for k in self.normalization_dict if '/' not in k]
        slash_keys  = [re.escape(k) for k in self.normalization_dict if '/' in k]

        parts = []
        if normal_keys:
            parts.append(r'\b(' + '|'.join(normal_keys) + r')\b')
        if slash_keys:
            parts.append(r'(?<![A-Za-z])(' + '|'.join(slash_keys) + r')(?![A-Za-z])')

        self.regex = re.compile('|'.join(parts), re.IGNORECASE)

    def normalize_text(self, text: str) -> str:
        """Replaces medical abbreviations with their full forms (case-insensitive)."""
        if not text:
            return ""

        def replace_match(match):
            term = next(g for g in match.groups() if g is not None)
            return self.normalization_dict.get(term.upper(), term)

        return self.regex.sub(replace_match, text)

    def find_abbreviations(self, text: str) -> list:
        """Returns a list of all recognized medical abbreviations found in the text."""
        if not text:
            return []
        return [
            next(g for g in match.groups() if g is not None)
            for match in self.regex.finditer(text)
        ]
