import re
from typing import List, Dict, Any
from loguru import logger
from .ocr_pipeline import get_text_from_ocr_result

def extract_medicine(text: str) -> List[Dict[str, str]]:
    """
    Very basic heuristic to find medicines in a prescription text.
    Looks for common dosage forms and units.
    """
    medicines = []
    
    # Common medicine keywords
    medicine_patterns = [
        r'(Tab\.|Tablet|Cap\.|Capsule|Syr\.|Syrup|Inj\.|Injection)\s+([a-zA-Z0-9\s-]+)',
        r'([a-zA-Z0-9\s-]+)\s+(\d+\s*(?:mg|ml|mcg|g))'
    ]
    
    for line in text.split('\n'):
        for pattern in medicine_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                medicines.append({
                    "name": match.group(0).strip(),
                    "raw_line": line.strip()
                })
                break
                
    return medicines

def parse_prescription(ocr_result) -> Dict[str, Any]:
    """
    Parses a prescription OCR result into structured data.
    """
    logger.info("Parsing prescription OCR result")
    
    text = get_text_from_ocr_result(ocr_result)
    
    extracted_data = {
        "doctor_name": None,
        "hospital": None,
        "medicines": extract_medicine(text),
        "raw_text": text
    }
    
    # Attempt to find doctor name (often near the top or prefixed with Dr.)
    dr_match = re.search(r'(Dr\.\s*[A-Za-z\s]+)', text, re.IGNORECASE)
    if dr_match:
        extracted_data["doctor_name"] = dr_match.group(1).strip()
        
    return extracted_data
