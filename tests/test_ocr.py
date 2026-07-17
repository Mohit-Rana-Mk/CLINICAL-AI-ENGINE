import pytest
from app.ocr.lab_report_parser import reconstruct_rows, parse_lab_report
from app.ocr.prescription_parser import parse_prescription

# Dummy PaddleOCR result format: [ [[box coords]], (text, confidence) ]
dummy_lab_ocr_result = [
    ([[[10, 10], [100, 10], [100, 20], [10, 20]]], ("Hemoglobin", 0.99)),
    ([[[110, 10], [150, 10], [150, 20], [110, 20]]], ("14.5", 0.98)),
    ([[[160, 10], [200, 10], [200, 20], [160, 20]]], ("g/dL", 0.95)),
    ([[[210, 10], [290, 10], [290, 20], [210, 20]]], ("13.0 - 17.0", 0.96)),
    
    ([[[10, 30], [100, 30], [100, 40], [10, 40]]], ("Platelets", 0.99)),
    ([[[110, 30], [150, 30], [150, 40], [110, 40]]], ("100", 0.98)),
    ([[[160, 30], [200, 30], [200, 40], [160, 40]]], ("x10^9/L", 0.95)),
    ([[[210, 30], [290, 30], [290, 40], [210, 40]]], ("150 - 450", 0.96)),
]

dummy_prescription_ocr_result = [
    ([[[10, 10], [150, 10], [150, 20], [10, 20]]], ("Dr. John Doe", 0.99)),
    ([[[10, 30], [150, 30], [150, 40], [10, 40]]], ("City Hospital", 0.98)),
    ([[[10, 50], [150, 50], [150, 60], [10, 60]]], ("Tab. Paracetamol 500mg", 0.95)),
    ([[[10, 70], [150, 70], [150, 80], [10, 80]]], ("1-0-1 after meals", 0.96)),
]

def test_reconstruct_rows():
    rows = reconstruct_rows(dummy_lab_ocr_result)
    assert len(rows) == 2
    assert "Hemoglobin 14.5 g/dL 13.0 - 17.0" in rows[0]
    assert "Platelets 100 x10^9/L 150 - 450" in rows[1]

def test_parse_lab_report():
    parsed_data = parse_lab_report(dummy_lab_ocr_result)
    assert len(parsed_data) == 2
    
    hemo = parsed_data[0]
    assert hemo["test_name"] == "Hemoglobin"
    assert hemo["extracted_value"] == 14.5
    assert hemo["unit"] == "g/dL"
    assert hemo["reference_range"] == "13.0 - 17.0"
    assert hemo["flag"] == "normal"
    
    platelets = parsed_data[1]
    assert platelets["test_name"] == "Platelets"
    assert platelets["extracted_value"] == 100.0
    assert platelets["unit"] == "x10^9/L"
    assert platelets["reference_range"] == "150 - 450"
    assert platelets["flag"] == "low"

def test_parse_prescription():
    parsed_data = parse_prescription(dummy_prescription_ocr_result)
    assert parsed_data["doctor_name"] == "Dr. John Doe"
    assert len(parsed_data["medicines"]) > 0
    assert "Paracetamol" in parsed_data["medicines"][0]["name"]
