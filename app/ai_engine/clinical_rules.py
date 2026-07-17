CHEST_PAIN_RULE = {
    "symptoms": [
        "chest pain"
    ],
    "risk": "HIGH",
    "emergency": True,
    "reason":
    "Chest pain requires cardiovascular emergency evaluation."
}


BREATHING_DIFFICULTY_RULE = {
    "symptoms": [
        "breathing difficulty"
    ],
    "risk": "HIGH",
    "emergency": True,
    "reason":
    "Breathing difficulty may indicate respiratory compromise."
}


FEVER_RULE = {
    "symptoms": [
        "fever"
    ],
    "risk": "MEDIUM",
    "emergency": False,
    "reason":
    "Fever requires infection assessment."
}


CLINICAL_RULES = [
    CHEST_PAIN_RULE,
    BREATHING_DIFFICULTY_RULE,
    FEVER_RULE
]