class SynonymMapper:
    def __init__(self):
        # Maps canonical (standard) medical terms to common layman & Hinglish synonyms
        self._synonym_dict = {
            "fever": [
                "high temperature", "running a temp", "pyrexia", "hot", "febrile",
                "bukhar", "bukhar hai", "tezz bukhar", "feverish"
            ],
            "shortness of breath": [
                "dyspnea", "trouble breathing", "can't catch breath", "breathless", "gasping",
                "saans phulna", "saas lene me dikkat", "saans ki takleef", "breathing difficulty"
            ],
            "nausea": [
                "feel sick", "queasy", "upset stomach", "sick to my stomach", "feeling sick",
                "ulti jaisa", "ji ghabrana", "vomiting tendency"
            ],
            "headache": [
                "migraine", "head pounding", "head hurting", "head pain",
                "sir dard", "sir me dard", "sir me bhari pan", "bhari pan", "head heaviness"
            ],
            "fatigue": [
                "tired", "exhausted", "worn out", "no energy", "lethargic",
                "thakan", "kamzori", "weakness"
            ],
            "cough": [
                "hacking", "coughing", "khansi", "khansi hai", "sukhi khansi"
            ],
            "chest pain": [
                "chest hurting", "heart hurting", "pain in chest", "angina",
                "seene me dard", "chhati me dard", "heart pain"
            ],
            "dizziness": [
                "dizzy", "lightheaded", "vertigo", "spinning",
                "chakkar", "chakkar aana", "sir ghoomna"
            ],
            "vomiting": [
                "throwing up", "puking", "heaving", "emesis",
                "ulti", "ultiya"
            ],
            "muscle ache": [
                "body ache", "myalgia", "muscles hurting", "aching muscles",
                "badan dard", "jism me dard"
            ]
        }
        
        # Build reverse lookup dictionary for O(1) mapping from synonym to canonical term
        self.synonym_to_canonical = {}
        for canonical, synonyms in self._synonym_dict.items():
            self.synonym_to_canonical[canonical.lower()] = canonical
            for syn in synonyms:
                self.synonym_to_canonical[syn.lower()] = canonical

    def map_synonym(self, text: str) -> str:
        text_lower = text.lower().strip()
        if text_lower in self.synonym_to_canonical:
            return self.synonym_to_canonical[text_lower]
        return text