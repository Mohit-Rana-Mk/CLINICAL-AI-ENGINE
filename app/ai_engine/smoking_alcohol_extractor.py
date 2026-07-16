import re
from typing import Tuple, Optional


class SmokingAlcoholExtractor:
    """
    Detects smoking status and alcohol use patterns in patient text.
    Returns normalized status strings for both.

    Smoking status values:
        "current smoker" | "ex-smoker" | "non-smoker" | None (not mentioned)

    Alcohol use values:
        "heavy drinker" | "social drinker" | "occasional drinker" | "non-drinker" | None
    """

    def __init__(self):
        # --- Smoking patterns (order matters: most specific first) ---
        self._smoking_patterns = [
            # Ex-smoker / quit smoking
            (
                "ex-smoker",
                re.compile(
                    r"\b(?:quit|stopped|gave up|used to|former(?:ly)?)\s+(?:smoking|smoke|smoker)\b"
                    r"|\bex[- ]?smoker\b"
                    r"|\bsmoking\s+(?:cessation|free)\b",
                    re.IGNORECASE,
                ),
            ),
            # Non-smoker / never smoked / denies tobacco
            (
                "non-smoker",
                re.compile(
                    r"\b(?:never\s+smoked|non[- ]?smoker|do\s+not\s+smoke|don'?t\s+smoke"
                    r"|no\s+smoking\s+history|no\s+history\s+of\s+smoking"
                    r"|denies?\s+(?:tobacco|smoking|smoke)\s+use"
                    r"|no\s+tobacco\s+use|tobacco[- ]?free)\b",
                    re.IGNORECASE,
                ),
            ),
            # Current smoker (active)
            (
                "current smoker",
                re.compile(
                    # 'tobacco' alone is excluded here — denial is caught above.
                    # We require tobacco to be paired with an active verb or quantity.
                    r"\b(?:smoke[sd]?|smoking|smoker|cigarette[s]?|bidi|hookah|vape[sd]?|vaping)\b"
                    r"|\btobacco\s+(?:use|user|consumption|abuse|addict)\b"
                    r"|\b(?:smokes?|uses?)\s+tobacco\b",
                    re.IGNORECASE,
                ),
            ),
        ]

        # --- Alcohol patterns (order matters: most specific first) ---
        self._alcohol_patterns = [
            # Non-drinker
            (
                "non-drinker",
                re.compile(
                    r"\b(?:never\s+drinks?|non[- ]?drinker|do\s+not\s+drink|don'?t\s+drink"
                    r"|no\s+alcohol|abstain[s]?\s+from\s+alcohol|teetotal(?:er)?)\b",
                    re.IGNORECASE,
                ),
            ),
            # Heavy drinker
            (
                "heavy drinker",
                re.compile(
                    r"\b(?:heavy\s+(?:drinker|drinking|alcohol|use)"
                    r"|alcohol(?:ic|ism|ism)?"
                    r"|drinks?\s+(?:daily|every\s+day|heavily|excessively|a\s+lot)"
                    r"|binge\s+drink(?:ing|er)?)\b",
                    re.IGNORECASE,
                ),
            ),
            # Social / occasional drinker
            (
                "social drinker",
                re.compile(
                    r"\b(?:social(?:ly)?\s+drink(?:s|er|ing)?"
                    r"|drinks?\s+(?:socially|occasionally|sometimes|rarely|at\s+parties)"
                    r"|occasional(?:ly)?\s+drink(?:s)?)\b",
                    re.IGNORECASE,
                ),
            ),
            # Any other alcohol mention (fallback — "I drink" etc.)
            (
                "occasional drinker",
                re.compile(
                    r"\b(?:drink[s]?|drinking|alcohol|wine|beer|whisky|whiskey|vodka|rum|liquor)\b",
                    re.IGNORECASE,
                ),
            ),
        ]

    def extract(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts smoking status and alcohol use from patient text.

        Args:
            text (str): Patient's reported text.

        Returns:
            Tuple[Optional[str], Optional[str]]:
                (smoking_status, alcohol_use)
                Each is None if not mentioned.
        """
        if not text or not text.strip():
            return None, None

        smoking_status = self._match_first(text, self._smoking_patterns)
        alcohol_use = self._match_first(text, self._alcohol_patterns)

        return smoking_status, alcohol_use

    def _match_first(self, text: str, patterns: list) -> Optional[str]:
        """Returns the label of the first matching pattern."""
        for label, pattern in patterns:
            if pattern.search(text):
                return label
        return None


