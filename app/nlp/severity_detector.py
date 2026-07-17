from enum import Enum
import re
from loguru import logger

class Severity(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

# Heuristic keyword matching
SEVERITY_KEYWORDS = {
    Severity.CRITICAL: [
        r"\bchest\s+pain\b", r"\bcan'?t\s+breathe\b", r"\bheart\s+attack\b", r"\bstroke\b",
        r"\bsevere\s+bleeding\b", r"\bsuicide\b", r"\bunconscious\b"
    ],
    Severity.HIGH: [
        r"\bsevere\b", r"\bunbearable\b", r"\bworst\b", r"\bsudden\b", r"\bhigh\s+fever\b", 
        r"\bvery\s+high\b", r"\bintense\b", r"\bthrowing\s+up\s+blood\b"
    ],
    Severity.MEDIUM: [
        r"\bmoderate\b", r"\bfever\b", r"\bpain\b", r"\bachy\b", r"\bthrowing\s+up\b",
        r"\bvomiting\b", r"\bdiahrrea\b"
    ],
    Severity.LOW: [
        r"\bmild\b", r"\bslight\b", r"\blittle\b", r"\bcold\b", r"\bcheckup\b", r"\bdiet\b",
        r"\broutine\b", r"\bgeneral\b"
    ]
}

class SeverityDetector:
    def __init__(self):
        logger.info("Initializing Categorical Severity Detector")

    def detect(self, text: str) -> Severity:
        """
        Detects the severity level of the patient's text.
        Returns one of: Low, Medium, High, Critical.
        """
        text_lower = text.lower()
        
        # Check in order of highest severity to lowest
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            patterns = SEVERITY_KEYWORDS[severity]
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    logger.debug(f"Matched severity keyword '{pattern}' -> {severity}")
                    return severity
                    
        # Default to LOW if no specific urgency is found
        return Severity.LOW

# Singleton instance
severity_detector_instance = None

def get_severity_detector():
    global severity_detector_instance
    if severity_detector_instance is None:
        severity_detector_instance = SeverityDetector()
    return severity_detector_instance
