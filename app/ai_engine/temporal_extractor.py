from __future__ import annotations

import re

class TemporalExtractor:
    def __init__(self):
        # Map word numbers to digits for normalization
        self.word_to_num = {
            "one": "1", "a": "1", "an": "1",
            "two": "2", "a couple of": "2", "couple of": "2", "couple": "2",
            "three": "3", "a few": "3", "few": "3",
            "four": "4", "five": "5", "six": "6",
            "seven": "7", "several": "7",
            "eight": "8", "nine": "9", "ten": "10"
        }
        
        # Standardize units
        self.unit_map = {
            "hr": "hours", "hrs": "hours", "hour": "hours", "hours": "hours",
            "min": "minutes", "mins": "minutes", "minute": "minutes", "minutes": "minutes",
            "day": "days", "days": "days",
            "week": "weeks", "weeks": "weeks", "wk": "weeks", "wks": "weeks",
            "month": "months", "months": "months", "mo": "months", "mos": "months",
            "year": "years", "years": "years", "yr": "years", "yrs": "years"
        }
        
        # Regex components
        num_pattern = r"(?:\d+|one|a|an|two|a couple of|couple of|couple|three|a few|few|four|five|six|seven|several|eight|nine|ten)"
        unit_pattern = r"(?:hour|hours|hr|hrs|min|mins|minute|minutes|day|days|week|weeks|wk|wks|month|months|mo|mos|year|years|yr|yrs)"
        
        # Create prioritized regex patterns
        # 1. Ranges: "2 to 3 days", "2-3 weeks"
        self.range_regex = re.compile(rf"({num_pattern})\s*(?:to|-|and)\s*({num_pattern})\s*({unit_pattern})", re.IGNORECASE)
        # 2. Basic: "3 days", "a few weeks"
        self.basic_regex = re.compile(rf"({num_pattern})\s*({unit_pattern})", re.IGNORECASE)
        # 3. Relative
        self.relative_regex = re.compile(r"(since yesterday|last night|this morning|past few days)", re.IGNORECASE)

    def _normalize_number(self, text: str) -> str:
        text = text.lower().strip()
        return self.word_to_num.get(text, text)
        
    def _normalize_unit(self, text: str) -> str:
        text = text.lower().strip()
        return self.unit_map.get(text, text)

    def extract(self, text: str) -> str | None:
        """
        Extracts and normalizes the temporal duration from the text.
        """
        # 1. Try relative time phrases first (e.g. "since yesterday")
        rel_match = self.relative_regex.search(text)
        if rel_match:
            return rel_match.group(1).lower()
            
        # 2. Try ranges (e.g., "2-3 days")
        range_match = self.range_regex.search(text)
        if range_match:
            num1 = self._normalize_number(range_match.group(1))
            num2 = self._normalize_number(range_match.group(2))
            unit = self._normalize_unit(range_match.group(3))
            return f"{num1}-{num2} {unit}"
            
        # 3. Try basic duration (e.g., "3 days", "a few weeks")
        basic_match = self.basic_regex.search(text)
        if basic_match:
            num = self._normalize_number(basic_match.group(1))
            unit = self._normalize_unit(basic_match.group(2))
            return f"{num} {unit}"
            
        return None
