class SynonymMapper:
    def __init__(self):
        # Maps canonical (standard) medical terms to their common layman synonyms.
        # This acts as our lightweight UMLS (Unified Medical Language System).
        self._synonym_dict = {
            "fever": ["high temperature", "running a temp", "pyrexia", "hot", "febrile"],
            "shortness of breath": ["dyspnea", "trouble breathing", "can't catch breath", "breathless", "gasping"],
            "nausea": ["feel sick", "queasy", "upset stomach", "sick to my stomach", "feeling sick"],
            "headache": ["migraine", "head pounding", "head hurting", "head pain"],
            "fatigue": ["tired", "exhausted", "worn out", "no energy", "lethargic"],
            "cough": ["hacking", "coughing"],
            "chest pain": ["chest hurting", "heart hurting", "pain in chest", "angina"],
            "dizziness": ["dizzy", "lightheaded", "vertigo", "spinning"],
            "vomiting": ["throwing up", "puking", "heaving", "emesis"],
            "muscle ache": ["body ache", "myalgia", "muscles hurting", "aching muscles"]
        }
        
        # Build a reverse lookup dictionary for O(1) mapping from synonym to canonical term
        self.synonym_to_canonical = {}
        for canonical, synonyms in self._synonym_dict.items():
            # Map the canonical term to itself
            self.synonym_to_canonical[canonical.lower()] = canonical
            # Map all synonyms to the canonical term
            for syn in synonyms:
                self.synonym_to_canonical[syn.lower()] = canonical

    def map_synonym(self, text: str) -> str:
        """
        Takes a potential symptom/phrase and returns its canonical medical term.
        If it's not found in the synonym list, returns the original text.
        """
        text_lower = text.lower().strip()
        
        # Exact match check
        if text_lower in self.synonym_to_canonical:
            return self.synonym_to_canonical[text_lower]
            
        return text
