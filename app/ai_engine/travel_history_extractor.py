import re
from typing import List


# A curated list of common Indian states, cities, and international regions
# used as location seeds for travel history extraction.
KNOWN_LOCATIONS = [
    # Indian States
    "Rajasthan", "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Maharashtra",
    "Gujarat", "Karnataka", "Tamil Nadu", "West Bengal", "Odisha",
    "Andhra Pradesh", "Telangana", "Kerala", "Punjab", "Haryana",
    "Uttarakhand", "Himachal Pradesh", "Jammu", "Kashmir", "Goa",
    "Assam", "Manipur", "Meghalaya", "Sikkim", "Tripura", "Nagaland",
    # Major Indian Cities
    "Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore", "Bengaluru",
    "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Chandigarh",
    "Patna", "Bhopal", "Bhubaneswar", "Surat", "Indore", "Nagpur", "Varanasi",
    # Countries & Regions (for infection risk context)
    "China", "Bangladesh", "Pakistan", "Nepal", "Sri Lanka",
    "Southeast Asia", "Africa", "South America", "Middle East",
    "Europe", "USA", "United States", "UK", "United Kingdom",
    # Generic rural/forest keywords
    "forest area", "jungle", "rural area", "tribal area", "flood zone",
]

# Lowercase lookup set for fast matching
_KNOWN_LOCATIONS_LOWER = {loc.lower(): loc for loc in KNOWN_LOCATIONS}


class TravelHistoryExtractor:
    """
    Detects recent travel mentions in patient text and extracts the locations.
    Returns a deduplicated list of place names found.
    """

    def __init__(self):
        # --- Pattern 1: Travel verb followed by a location ---
        self._verb_pattern = re.compile(
            r"\b(?:traveled?|travelled?|visited?|returned?\s+from|came?\s+from|"
            r"been\s+to|went\s+to|trip\s+to|journey\s+to|coming\s+from|"
            r"arrived?\s+from)\s+(.+?)(?=[.,;]|$)",
            re.IGNORECASE,
        )

        # --- Pattern 2: "I was in / I am in [place] last / recently" ---
        self._was_in_pattern = re.compile(
            r"\b(?:I\s+was|I\s+am|we\s+were|we\s+are)\s+in\s+(.+?)\s+"
            r"(?:last\s+\w+|recently|for\s+\w+|over\s+the)",
            re.IGNORECASE,
        )

        # --- Pattern 3: Direct keyword scan for known locations ---
        # Compiled as one big alternation for speed
        escaped = [re.escape(loc) for loc in KNOWN_LOCATIONS]
        self._location_scan_pattern = re.compile(
            r"\b(" + "|".join(escaped) + r")\b",
            re.IGNORECASE,
        )

        # --- Travel trigger words (to decide if location scan should run) ---
        self._travel_trigger = re.compile(
            r"\b(?:travel|trip|visit|tour|journey|went|return|arrived|"
            r"came\s+from|moved?\s+from|recently\s+from)\b",
            re.IGNORECASE,
        )

        # --- Residence exclusion: these phrases mean 'living there', not travel ---
        self._residence_pattern = re.compile(
            r"\b(?:living\s+in|reside[sd]?\s+in|based\s+in|settled\s+in|"
            r"stay(?:ing|ed)?\s+in|born\s+in|grew\s+up\s+in|grown\s+up\s+in|"
            r"native\s+of|originally\s+from)\b",
            re.IGNORECASE,
        )

    def extract(self, text: str) -> List[str]:
        """
        Extracts travel history locations from patient text.

        Args:
            text (str): Patient's reported text.

        Returns:
            List[str]: A deduplicated list of place names found.
        """
        if not text or not text.strip():
            return []

        # Split into sentences and filter out residence sentences upfront
        sentences = re.split(r'(?<=[.!?])\s+', text)
        travel_sentences = [
            s for s in sentences if not self._residence_pattern.search(s)
        ]
        # Rejoin for pattern matching
        filtered_text = ' '.join(travel_sentences)

        if not filtered_text.strip():
            return []

        found_locations = []

        # Strategy 1: Extract whatever follows travel verbs
        for match in self._verb_pattern.finditer(filtered_text):
            raw_place = match.group(1).strip().rstrip(".,;")
            # Try to match against known locations within the extracted phrase
            for known_lower, canonical in _KNOWN_LOCATIONS_LOWER.items():
                if known_lower in raw_place.lower():
                    found_locations.append(canonical)
            # If no known location matched, store the raw phrase (trimmed)
            if not found_locations or raw_place.lower() not in [
                l.lower() for l in found_locations
            ]:
                raw_trimmed = raw_place.strip()
                if raw_trimmed and len(raw_trimmed) < 50:
                    if not re.match(r'^(the|a|an|some|there|here)$', raw_trimmed, re.IGNORECASE):
                        already_covered = any(
                            raw_trimmed.lower() in l.lower() or l.lower() in raw_trimmed.lower()
                            for l in found_locations
                        )
                        if not already_covered:
                            found_locations.append(raw_trimmed)

        # Strategy 2: 'I was in [place] last / recently' pattern
        for match in self._was_in_pattern.finditer(filtered_text):
            raw_place = match.group(1).strip().rstrip(".,;")
            for known_lower, canonical in _KNOWN_LOCATIONS_LOWER.items():
                if known_lower in raw_place.lower():
                    found_locations.append(canonical)

        # Strategy 3: If a travel trigger exists, also scan for known locations
        if self._travel_trigger.search(filtered_text):
            for match in self._location_scan_pattern.finditer(filtered_text):
                canonical = _KNOWN_LOCATIONS_LOWER[match.group(1).lower()]
                found_locations.append(canonical)

        # Deduplicate (case-insensitive) while preserving order
        seen = set()
        unique = []
        for loc in found_locations:
            key = loc.lower()
            if key not in seen:
                seen.add(key)
                unique.append(loc)

        return unique



