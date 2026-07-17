import re
import math
from typing import List, Dict, Any
from loguru import logger

def reconstruct_rows(ocr_result, y_tolerance=10) -> List[str]:
    """
    Reconstructs tabular rows from PaddleOCR result based on y-axis alignment.
    y_tolerance dictates how close y-centers need to be to be considered the same row.
    """
    items = []
    for line in ocr_result:
        if len(line) == 2 and isinstance(line[1], tuple):
            box = line[0]
            text = line[1][0]
            # Calculate the y-center of the bounding box
            # box is [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            y_center = sum([point[1] for point in box]) / 4.0
            x_left = min([point[0] for point in box])
            items.append({"text": text, "y_center": y_center, "x_left": x_left})

    # Sort items primarily by y_center, then by x_left
    items.sort(key=lambda x: x["y_center"])

    rows = []
    current_row = []
    current_y = None

    for item in items:
        if current_y is None:
            current_y = item["y_center"]
            current_row.append(item)
        elif abs(item["y_center"] - current_y) <= y_tolerance:
            current_row.append(item)
            # Update current_y to the average of the row so far
            current_y = sum([i["y_center"] for i in current_row]) / len(current_row)
        else:
            # Sort current row by x_left before saving
            current_row.sort(key=lambda x: x["x_left"])
            rows.append(" ".join([i["text"] for i in current_row]))
            current_row = [item]
            current_y = item["y_center"]

    if current_row:
        current_row.sort(key=lambda x: x["x_left"])
        rows.append(" ".join([i["text"] for i in current_row]))

    return rows

def parse_lab_value(text: str) -> float:
    try:
        # find the first float-like number
        match = re.search(r'\d+\.\d+|\d+', text)
        if match:
            return float(match.group())
    except ValueError:
        pass
    return None

def compute_flag(value: float, reference_range: str) -> str:
    if value is None or not reference_range:
        return "unknown"
    
    # Try to parse reference range (e.g., "13.0 - 17.0", "< 5.0", "> 10")
    try:
        range_match = re.search(r'([\d.]+)\s*-\s*([\d.]+)', reference_range)
        if range_match:
            low = float(range_match.group(1))
            high = float(range_match.group(2))
            if value < low:
                return "low"
            elif value > high:
                return "high"
            else:
                return "normal"
    except Exception:
        pass
    
    return "unknown"

def parse_lab_report(ocr_result) -> List[Dict[str, Any]]:
    """
    Parses a lab report OCR result into a structured JSON schema.
    """
    logger.info("Parsing lab report OCR result")
    
    rows = reconstruct_rows(ocr_result)
    extracted_data = []

    # Very basic heuristics to find test rows
    # A typical lab row might look like: "Hemoglobin 14.5 g/dL 13.0 - 17.0"
    
    for row in rows:
        # Example regex for simple parsing
        # Look for words, followed by numbers, followed by possible unit and range
        match = re.match(r'([A-Za-z\s]+?)\s+(\d+\.?\d*)\s*([a-zA-Z/%]+)?\s*([\d.]+\s*-\s*[\d.]+|<[\s\d.]+|>[\s\d.]+)?', row)
        
        if match:
            test_name = match.group(1).strip()
            extracted_value = float(match.group(2))
            unit = match.group(3).strip() if match.group(3) else ""
            reference_range = match.group(4).strip() if match.group(4) else ""
            
            # Filter out obvious false positives (too short test names, etc.)
            if len(test_name) < 3:
                continue
                
            flag = compute_flag(extracted_value, reference_range)
            
            extracted_data.append({
                "test_name": test_name,
                "extracted_value": extracted_value,
                "unit": unit,
                "reference_range": reference_range,
                "flag": flag
            })
            
    return extracted_data
