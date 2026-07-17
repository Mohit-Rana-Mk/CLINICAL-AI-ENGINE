from enum import Enum
import re
from loguru import logger
from typing import Optional
from sentence_transformers import SentenceTransformer, util
import torch

class Intent(str, Enum):
    NEW_DIAGNOSIS = "new_diagnosis"
    FOLLOW_UP = "follow_up"
    PRESCRIPTION_REFILL = "prescription_refill"
    LAB_RESULT_INQUIRY = "lab_result_inquiry"
    TREATMENT_INQUIRY = "treatment_inquiry"
    GENERAL_HEALTH_ADVICE = "general_health_advice"
    EMERGENCY = "emergency"

# Strong keyword heuristics
INTENT_KEYWORDS = {
    Intent.EMERGENCY: [r"\bchest\s+pain\b", r"\bcan'?t\s+breathe\b", r"\bsuicide\b", r"\bbleeding\s+heavily\b", r"\bheart\s+attack\b", r"\bstroke\b"],
    Intent.PRESCRIPTION_REFILL: [r"\brefill\b", r"\bran\s+out\b", r"\brenew\b", r"\bmore\s+medicine\b"],
    Intent.LAB_RESULT_INQUIRY: [r"\breport\b", r"\blab\b", r"\btest\s+result[s]?\b", r"\bblood\s+work\b", r"\bhemoglobin\b"],
    Intent.TREATMENT_INQUIRY: [r"\bside\s+effect[s]?\b", r"\bhow\s+to\s+take\b", r"\bdosage\b", r"\bwith\s+food\b"],
    Intent.FOLLOW_UP: [r"\bbetter\b", r"\bstill\s+have\b", r"\bfeeling\s+worse\b", r"\bfollow\s*up\b"],
}

# Fallback reference sentences for embeddings
REFERENCE_SENTENCES = {
    Intent.NEW_DIAGNOSIS: ["I have a headache and fever.", "My stomach hurts and I am vomiting.", "I'm feeling sick with a cough."],
    Intent.FOLLOW_UP: ["My cough is better but I still have a fever.", "The medicine is working.", "I'm not feeling any better since my last visit."],
    Intent.PRESCRIPTION_REFILL: ["I ran out of my Metformin.", "I need a refill for my prescription.", "Can you renew my inhaler?"],
    Intent.LAB_RESULT_INQUIRY: ["What does this high Hemoglobin mean?", "I got my blood test back.", "Can you explain my lab results?"],
    Intent.TREATMENT_INQUIRY: ["Should I take this medicine with food?", "What are the side effects of this drug?", "How much should I take?"],
    Intent.GENERAL_HEALTH_ADVICE: ["What is a good diet for high blood pressure?", "How can I improve my sleep?", "Is it safe to exercise every day?"],
    Intent.EMERGENCY: ["I am having severe chest pain and left arm numbness.", "I can't breathe.", "Someone is bleeding heavily."]
}

class IntentClassifier:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        logger.info(f"Initializing IntentClassifier with fallback model: {model_name}")
        # Keep things local and fast on CPU
        self.model = SentenceTransformer(model_name, device="cpu")
        
        self.reference_embeddings = {}
        for intent, sentences in REFERENCE_SENTENCES.items():
            # Compute embeddings for reference sentences
            self.reference_embeddings[intent] = self.model.encode(sentences, convert_to_tensor=True)

    def classify(self, text: str) -> Intent:
        """
        Classifies the intent of the patient's input.
        Uses a hybrid approach: Rule-Based heuristics first, then Zero-Shot embeddings fallback.
        """
        logger.debug(f"Classifying intent for text: '{text}'")
        text_lower = text.lower()
        
        # 1. Rule-Based / Keyword Heuristics
        for intent, patterns in INTENT_KEYWORDS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    logger.debug(f"Matched keyword pattern '{pattern}' for intent: {intent}")
                    return intent
                    
        # 2. Fallback to Embeddings (Cosine Similarity)
        logger.debug("No strong keyword match found. Falling back to embeddings.")
        query_embedding = self.model.encode(text, convert_to_tensor=True)
        
        best_intent = None
        best_score = -1.0
        
        for intent, ref_embeddings in self.reference_embeddings.items():
            # Calculate cosine similarity between query and all reference sentences for this intent
            cosine_scores = util.cos_sim(query_embedding, ref_embeddings)
            # Get the max score for this intent
            max_score = torch.max(cosine_scores).item()
            
            if max_score > best_score:
                best_score = max_score
                best_intent = intent
                
        logger.debug(f"Best fallback match: {best_intent} with score: {best_score:.4f}")
        
        # If score is very low, we might default to GENERAL_HEALTH_ADVICE or NEW_DIAGNOSIS, 
        # but for now we just return the best match.
        return best_intent or Intent.GENERAL_HEALTH_ADVICE

# Singleton instance
classifier_instance = None

def get_intent_classifier():
    global classifier_instance
    if classifier_instance is None:
        classifier_instance = IntentClassifier()
    return classifier_instance
