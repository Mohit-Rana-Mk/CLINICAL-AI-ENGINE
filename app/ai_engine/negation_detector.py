import re

class NegationDetector:
    def __init__(self):
        # Words that negate a symptom that comes AFTER them (e.g., "no fever")
        self.pre_negations = {
            "no", "not", "denies", "without", "don't", "do not", 
            "never", "absence of", "negative for", "free of", 
            "didn't", "did not", "doesn't", "does not", "zero"
        }
        
        # Words that negate a symptom that comes BEFORE them (e.g., "fever: none")
        self.post_negations = {
            "denied", "unlikely", "none", "negative", "absent"
        }
        
        # Words or punctuation that break a thought, stopping the negation window
        self.termination_terms = {
            "but", "however", "although", "except", "yet",
            ",", ".", ";"
        }
        
        # Number of words to look around the symptom
        self.window_size = 5

    def _truncate_by_termination(self, text_chunk: str, reverse: bool = False) -> str:
        """
        Truncates the text chunk if it hits a termination term (boundary).
        """
        if not text_chunk.strip():
            return text_chunk
            
        # Pad punctuation with spaces so they become separate tokens
        for p in [",", ".", ";"]:
            text_chunk = text_chunk.replace(p, f" {p} ")
            
        tokens = text_chunk.split()
        
        if reverse:
            # Looking backwards: find the LAST termination term and take everything AFTER it
            last_term_idx = -1
            for i in range(len(tokens)-1, -1, -1):
                if tokens[i].lower() in self.termination_terms:
                    last_term_idx = i
                    break
            if last_term_idx != -1:
                tokens = tokens[last_term_idx + 1:]
        else:
            # Looking forwards: find the FIRST termination term and take everything BEFORE it
            first_term_idx = -1
            for i, token in enumerate(tokens):
                if token.lower() in self.termination_terms:
                    first_term_idx = i
                    break
            if first_term_idx != -1:
                tokens = tokens[:first_term_idx]
                
        return " ".join(tokens)

    def is_negated(self, text: str, symptom: str) -> bool:
        """
        Checks if a symptom is negated in the given text.
        Handles pre-negations, post-negations, and termination terms.
        """
        text_lower = text.lower()
        symptom_lower = symptom.lower()

        matches = list(re.finditer(rf"(?<!\w){re.escape(symptom_lower)}(?!\w)", text_lower))
        
        if not matches:
            return False
            
        # We check each occurrence.
        for match in matches:
            start_idx = match.start()
            end_idx = match.end()
            
            is_match_negated = False
            
            # --- 1. Check Pre-Negation (Look backwards) ---
            preceding_text = text_lower[:start_idx]
            words_before = preceding_text.split()[-self.window_size:]
            window_before = " ".join(words_before)
            
            clean_window_before = self._truncate_by_termination(window_before, reverse=True)
            
            for trigger in self.pre_negations:
                pattern = rf"\b{re.escape(trigger)}\b"
                if re.search(pattern, clean_window_before):
                    is_match_negated = True
                    break
                    
            # --- 2. Check Post-Negation (Look forwards) ---
            if not is_match_negated:
                following_text = text_lower[end_idx:]
                words_after = following_text.split()[:self.window_size]
                window_after = " ".join(words_after)
                
                clean_window_after = self._truncate_by_termination(window_after, reverse=False)
                
                for trigger in self.post_negations:
                    pattern = rf"\b{re.escape(trigger)}\b"
                    if re.search(pattern, clean_window_after):
                        is_match_negated = True
                        break
            
            # If this specific mention of the symptom is NOT negated, 
            # then the patient has it. We can stop checking.
            if not is_match_negated:
                return False
                
        # If we reach here, EVERY mention of the symptom was negated.
        return True
