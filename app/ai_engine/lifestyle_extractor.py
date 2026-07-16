import re
from typing import List


class LifestyleExtractor:
    """
    Detects general lifestyle risk factors from patient text.
    Returns a list of identified lifestyle tags that are relevant
    for clinical risk assessment.

    Categories detected:
        - Physical activity level
        - Diet patterns
        - Sleep quality
        - Occupation type
    """

    def __init__(self):
        # Each entry: (tag_label, compiled_regex)
        # Order within a category matters — most specific first
        self._patterns: List[tuple] = [
            # ── Physical Activity ──────────────────────────────────────────
            (
                "physically active",
                re.compile(
                    r"\b(?:physically\s+active|exercises?\s+regularly|works?\s+out|"
                    r"goes?\s+to\s+(?:the\s+)?gym|jogs?|runs?\s+daily|plays?\s+sports?|"
                    r"very\s+active|active\s+lifestyle)\b",
                    re.IGNORECASE,
                ),
            ),
            (
                "sedentary",
                re.compile(
                    r"\b(?:sedentary|no\s+exercise|does\s+not\s+exercise|doesn'?t\s+exercise|"
                    r"never\s+exercises?|inactive|no\s+physical\s+activity|"
                    r"minimal\s+(?:activity|exercise)|couch|sitting\s+all\s+day)\b",
                    re.IGNORECASE,
                ),
            ),
            (
                "moderate exercise",
                re.compile(
                    r"\b(?:walks?\s+(?:daily|regularly|every\s+day|for\s+exercise)|"
                    r"light\s+exercise|occasional(?:ly)?\s+exercise[sd]?|"
                    r"exercises?\s+(?:sometimes|occasionally))\b",
                    re.IGNORECASE,
                ),
            ),

            # ── Diet ──────────────────────────────────────────────────────
            (
                "vegetarian",
                re.compile(
                    r"\b(?:vegetarian|vegan|plant[- ]based\s+diet|no\s+meat|"
                    r"pure\s+veg)\b",
                    re.IGNORECASE,
                ),
            ),
            (
                "non-vegetarian",
                re.compile(
                    r"\b(?:non[- ]veg(?:etarian)?|eats?\s+meat|meat\s+eater|"
                    r"consumes?\s+(?:chicken|mutton|beef|pork|fish|seafood))\b",
                    re.IGNORECASE,
                ),
            ),
            (
                "junk food",
                re.compile(
                    r"\b(?:junk\s+food|fast\s+food|processed\s+food|fried\s+food|"
                    r"oily\s+food|unhealthy\s+(?:diet|eating)|lots\s+of\s+sugar|"
                    r"high\s+sugar\s+diet|high\s+fat\s+diet)\b",
                    re.IGNORECASE,
                ),
            ),
            (
                "diabetic diet",
                re.compile(
                    r"\b(?:diabetic\s+diet|diet\s+control(?:led)?|following\s+a\s+diet|"
                    r"low\s+carb(?:ohydrate)?\s+diet|low\s+glycemic)\b",
                    re.IGNORECASE,
                ),
            ),

            # ── Sleep ──────────────────────────────────────────────────────
            (
                "poor sleep",
                re.compile(
                    r"\b(?:poor\s+sleep|sleep\s+problems?|trouble\s+sleeping|"
                    r"can'?t\s+sleep|insomnia|disturbed\s+sleep|sleep\s+depri(?:ved|vation)|"
                    r"not\s+sleeping\s+well"
                    r"|only\s+\d+\s+hours?\s+(?:of\s+)?sleep"    # "only 4 hours of sleep"
                    r"|only\s+sleep\s+\d+\s+hours?"              # "only sleep 4 hours"
                    r"|sleep\s+(?:only\s+)?\d+\s+hours?\s+a\s+night)\b",  # "sleep 4 hours a night"
                    re.IGNORECASE,
                ),
            ),
            (
                "good sleep",
                re.compile(
                    r"\b(?:sleeps?\s+well|good\s+sleep|adequate\s+sleep|"
                    r"7[- ]?8\s+hours?\s+(?:of\s+)?sleep|enough\s+sleep)\b",
                    re.IGNORECASE,
                ),
            ),

            # ── Occupation ────────────────────────────────────────────────
            (
                "desk job",
                re.compile(
                    r"\b(?:desk\s+job|office\s+job|works?\s+at\s+(?:a\s+)?desk|"
                    r"office\s+worker|computer\s+job|IT\s+job|mostly\s+sitting)\b",
                    re.IGNORECASE,
                ),
            ),
            (
                "manual labour",
                re.compile(
                    r"\b(?:manual\s+(?:labour|labor|work)|labourer|laborer|"
                    r"construction\s+worker|farmer|field\s+work|physical\s+(?:job|work))\b",
                    re.IGNORECASE,
                ),
            ),
            (
                "night shift",
                re.compile(
                    r"\b(?:night\s+shift|works?\s+(?:at\s+)?nights?|night\s+duty|"
                    r"overnight\s+work|graveyard\s+shift)\b",
                    re.IGNORECASE,
                ),
            ),
        ]

    def extract(self, text: str) -> List[str]:
        """
        Extracts lifestyle risk factors from patient text.

        Args:
            text (str): Patient's reported text.

        Returns:
            List[str]: A list of matched lifestyle tags (deduplicated).
        """
        if not text or not text.strip():
            return []

        found = []
        for label, pattern in self._patterns:
            if pattern.search(text):
                found.append(label)

        return found


