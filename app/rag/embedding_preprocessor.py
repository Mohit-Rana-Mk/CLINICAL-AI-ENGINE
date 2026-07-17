import re

# Comprehensive list of medical abbreviations to standardize
ABBREVIATIONS = {
    # 1. Vital Signs & Measurements
    "BP": "Blood Pressure",
    "HR": "Heart Rate",
    "RR": "Respiratory Rate",
    "Temp": "Temperature",
    "T": "Temperature",
    "SpO2": "Oxygen Saturation",
    "O2Sat": "Oxygen Saturation",
    "Wt": "Weight",
    "Ht": "Height",
    "BMI": "Body Mass Index",
    
    # 2. Common Diseases & Conditions
    "HTN": "Hypertension",
    "T2DM": "Type 2 Diabetes Mellitus",
    "DM2": "Type 2 Diabetes Mellitus",
    "T1DM": "Type 1 Diabetes Mellitus",
    "DM1": "Type 1 Diabetes Mellitus",
    "CAD": "Coronary Artery Disease",
    "MI": "Myocardial Infarction",
    "CHF": "Congestive Heart Failure",
    "COPD": "Chronic Obstructive Pulmonary Disease",
    "CKD": "Chronic Kidney Disease",
    "CVA": "Cerebrovascular Accident",
    "GERD": "Gastroesophageal Reflux Disease",
    
    # 3. Lab Tests & Results
    "CBC": "Complete Blood Count",
    "BMP": "Basic Metabolic Panel",
    "CMP": "Comprehensive Metabolic Panel",
    "LFT": "Liver Function Test",
    "HbA1c": "Hemoglobin A1c",
    "A1C": "Hemoglobin A1c",
    "WBC": "White Blood Cell count",
    "RBC": "Red Blood Cell count",
    "ECG": "Electrocardiogram",
    "EKG": "Electrocardiogram",
    
    # 4. Medication Dosages & Frequencies
    "PO": "By mouth",
    "IV": "Intravenous",
    "QD": "Once daily",
    "BID": "Twice a day",
    "TID": "Three times a day",
    "QID": "Four times a day",
    "PRN": "As needed",
    
    # 5. General Clinical Terminology
    "Hx": "History",
    "Tx": "Treatment",
    "Dx": "Diagnosis",
    "Rx": "Prescription",
    "Sx": "Symptoms",
    "Pt": "Patient",
    "DOB": "Date of Birth",
    "CC": "Chief Complaint",
}

def preprocess_for_embeddings(text: str) -> str:
    """
    Preprocesses text for embedding models by expanding medical abbreviations
    and standardizing units, while preserving the original casing of the text.
    """
    if text is None:
        return None
    if not text:
        return ""

    processed_text = text

    # Standardize units (e.g., mgs, miligrams -> mg)
    # We'll use case-insensitive replacement for units, using negative lookbehind for letters
    # so we can catch "10mgs" where there is no space between the number and unit.
    processed_text = re.sub(r'(?<![a-zA-Z])(mgs|miligrams?|milligrams?)\b', 'mg', processed_text, flags=re.IGNORECASE)
    processed_text = re.sub(r'(?<![a-zA-Z])(mcgs|micrograms?)\b', 'mcg', processed_text, flags=re.IGNORECASE)
    
    # Ensure there is a space between number and unit (e.g. 10mg -> 10 mg)
    processed_text = re.sub(r'(\d)(mg|mcg|ml|kg)\b', r'\1 \2', processed_text, flags=re.IGNORECASE)

    # Expand abbreviations
    # Sort by length descending to replace longer abbreviations first (e.g., 'T2DM' before 'T')
    # Wait, 'T' is tricky because it might just be the letter 'T'. 
    # We will do an exact case match for things like 'T' to avoid breaking words or normal sentences, 
    # but for most abbreviations we can do case-insensitive match if they are longer. 
    # To be safe and since these are acronyms, we will match them EXACTLY as they appear in the dictionary,
    # or fully capitalized. The user said "preserve the original casing", so maybe we should match the exact casing
    # to avoid replacing lowercase "t" with "Temperature".

    # Let's match exactly the casing in the dictionary for safety, especially for short abbreviations.
    sorted_abbr = sorted(ABBREVIATIONS.items(), key=lambda x: len(x[0]), reverse=True)
    
    for abbr, expansion in sorted_abbr:
        # Use exact case matching to prevent false positives like 't' -> 'Temperature'
        # \b ensures word boundaries
        pattern = r'\b' + re.escape(abbr) + r'\b'
        processed_text = re.sub(pattern, expansion, processed_text)

    return processed_text
