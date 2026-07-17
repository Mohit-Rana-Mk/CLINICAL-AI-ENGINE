import json
from typing import List, Dict, Any

# Mock dataset covering Multilingual, noisy OCR, and voice transcripts
MOCK_DATASET = [
    {
        "id": "test_001",
        "type": "text",
        "input_text": "I have severe chest pain and left arm numbness.",
        "expected": {
            "intent": "emergency",
            "severity": "Critical",
            "symptoms": ["chest pain", "arm numbness"],
            "body_parts": ["chest", "left arm"]
        }
    },
    {
        "id": "test_002",
        "type": "translated_text",
        "original_text": "Mujhe 3 din se bukhar aur khansi hai.",
        "input_text": "I have fever and cough for 3 days.",
        "expected": {
            "intent": "new_diagnosis",
            "severity": "Medium",
            "symptoms": ["fever", "cough"],
            "duration": "3 days"
        }
    },
    {
        "id": "test_003",
        "type": "noisy_ocr",
        "input_text": "Tab. Paracetamo1 500 nng Twic e Dai1y",
        "expected": {
            "medications": [{"name": "Paracetamol", "dose": "500 mg", "frequency": "Twice Daily"}]
        }
    },
    {
        "id": "test_004",
        "type": "voice_transcript",
        "input_text": "Uh, yeah, so I... I ran out of my Metformin yesterday.",
        "expected": {
            "intent": "prescription_refill",
            "severity": "Low",
            "medications": [{"name": "Metformin"}]
        }
    }
]

def load_test_dataset() -> List[Dict[str, Any]]:
    """
    Returns the mock dataset for benchmarking.
    """
    return MOCK_DATASET
