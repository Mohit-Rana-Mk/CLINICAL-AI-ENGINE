import re
from typing import List


class FamilyHistoryExtractor:
    """
    Detects mentions of family members' medical conditions in patient text.
    Uses rule-based pattern matching to identify family history without
    requiring any external NLP libraries.
    """

    def __init__(self):
        # Pre-check: if these appear before 'family history', skip the match
        self._negation_prefix = re.compile(
            r"\b(?:no|no\s+known|denies?(?:\s+any)?|without|negative\s+for)\s+"
            r"family\s+(?:history|h/o)",
            re.IGNORECASE,
        )

        # Trigger phrase patterns — capture the condition that follows
        self._patterns = [
            # "family history of hypertension" — stop only at sentence-ending punctuation,
            # NOT at commas, so 'family history of diabetes, hypertension, and cancer'
            # is captured whole and then split by the post-processing step.
            re.compile(
                r"family\s+history\s+of\s+(.+?)(?=\s*[.;]|$)",
                re.IGNORECASE,
            ),
            # "my father has / had / was diagnosed with / suffered from ..."
            re.compile(
                r"(?:my|his|her|our)\s+(?:father|mother|dad|mom|brother|sister|"
                r"grandfather|grandmother|grandpa|grandma|parent|sibling|uncle|aunt|"
                r"son|daughter|child|children|family)\s+"
                r"(?:has|have|had|was diagnosed with|were diagnosed with|"
                r"suffered from|suffers from|died of|died from|passed away from)\s+"
                r"(.+?)(?=\s*[.,;]|$)",
                re.IGNORECASE,
            ),
            # "runs in the family / runs in my family"
            re.compile(
                r"(.+?)\s+runs\s+in\s+(?:the|my|our)\s+family",
                re.IGNORECASE,
            ),
            # "hereditary / inherited condition: diabetes"
            re.compile(
                r"(?:hereditary|inherited|genetic)\s+(?:condition\s+of|tendency\s+for|risk\s+of)?\s+"
                r"(.+?)(?=\s*[.,;]|$)",
                re.IGNORECASE,
            ),
        ]

    def extract(self, text: str) -> List[str]:
        """
        Extracts family medical history mentions from the given text.

        Args:
            text (str): Patient's reported text.

        Returns:
            List[str]: A list of extracted conditions (deduplicated, lower-cased).
        """
        if not text or not text.strip():
            return []

        # Split text into sentences for per-sentence negation checking
        sentences = re.split(r'(?<=[.!?])\s+', text)

        conditions = []
        for sentence in sentences:
            # Skip this sentence if it negates family history
            if self._negation_prefix.search(sentence):
                continue

            for pattern in self._patterns:
                for match in pattern.finditer(sentence):
                    raw = match.group(1).strip().rstrip(".,;")
                    if not raw:
                        continue
                    # Split multi-conditions joined by 'and' or ','
                    parts = re.split(r',\s*|\s+and\s+', raw)
                    for part in parts:
                        part = part.strip().rstrip(".,;")
                        if part:
                            conditions.append(part.lower())

        # Deduplicate while preserving order
        seen = set()
        unique = []
        for c in conditions:
            if c not in seen:
                seen.add(c)
                unique.append(c)

        return unique


