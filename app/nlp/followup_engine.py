import logging
try:
    from cachetools import LRUCache
except ImportError:
    LRUCache = None

logger = logging.getLogger(__name__)

class FollowupEngine:
    def __init__(self, max_sessions=1000):
        # Store up to 1000 concurrent patient sessions locally in memory
        self.session_memory = (
            LRUCache(maxsize=max_sessions)
            if LRUCache is not None
            else {}
        )
        
    def generate_followup(self, clinical_data: dict) -> dict:
        """
        Generates a follow-up action based on current clinical data and past context.
        """
        metadata = clinical_data.get("metadata", {})
        session_id = metadata.get("session_id", "default_session")
        payload = clinical_data.get("clinical_payload", clinical_data)
        
        # Retrieve past context if this is a multi-turn conversation
        past_context = self.session_memory.get(session_id, {
            "symptoms": [],
            "history": []
        })
        
        # Update past context with new symptoms (avoid duplicates using set logic)
        current_symptoms = set(payload.get("symptoms", []))
        existing = set(past_context["symptoms"])
        past_context["symptoms"] = list(existing.union(current_symptoms))
        
        # Determine followup
        intent = payload.get("intent", "")
        severity = payload.get("severity", "")
        duration = payload.get("duration", "")
        body_parts = payload.get("body_parts", [])
        
        question = ""
        is_urgent = False
        
        if severity == "Critical":
            question = "This sounds critical. Are you experiencing any trouble breathing or severe chest pain right now? Please seek immediate emergency medical care."
            is_urgent = True
        elif intent == "new_diagnosis":
            if not severity:
                question = f"On a scale of 1-10, how bad is the {', '.join(current_symptoms) if current_symptoms else 'pain'}?"
            elif not duration:
                question = "How long have you been experiencing these symptoms?"
            elif current_symptoms and not body_parts:
                question = "Can you point to where exactly you are feeling this?"
            else:
                question = "Are there any other symptoms you are experiencing?"
        elif intent == "prescription_refill":
            question = "Which specific medication do you need a refill for, and do you have any remaining doses?"
        elif intent == "follow_up":
            question = "Have the symptoms improved or worsened since your last check-in?"
        else:
            question = "Is there anything else I can help you with today?"
            
        # Save updated state back to memory
        self.session_memory[session_id] = past_context
        
        return {
            "question": question,
            "is_urgent": is_urgent
        }

# Singleton instance
followup_engine_instance = None

def get_followup_engine():
    global followup_engine_instance
    if followup_engine_instance is None:
        followup_engine_instance = FollowupEngine()
    return followup_engine_instance
