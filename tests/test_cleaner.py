import pytest
from app.rag.document_cleaner import DocumentCleaner
from app.rag.medical_normalizer import MedicalNormalizer


@pytest.fixture
def cleaner():
    return DocumentCleaner()


@pytest.fixture
def normalizer():
    return MedicalNormalizer()


# --- DocumentCleaner: noise removal ---

def test_page_number_removed(cleaner):
    assert "Page 12" not in cleaner.clean_text("Page 12 of 15\nSome text.")

def test_confidential_header_removed(cleaner):
    assert "CONFIDENTIAL" not in cleaner.clean_text("CONFIDENTIAL\nSome text.")

def test_patient_record_header_removed(cleaner):
    assert "Patient Record" not in cleaner.clean_text("Patient Record\nSome text.")

def test_divider_dashes_removed(cleaner):
    assert "---" not in cleaner.clean_text("Some text.\n---\nMore text.")

def test_markdown_table_pipes_converted(cleaner):
    result = cleaner.clean_text("Header\n|---|---|\ndata")
    assert "|" not in result          # pipes are stripped
    assert "---" in result            # content (dashes become text) survives

def test_bracketed_page_number_removed(cleaner):
    assert "- 13 -" not in cleaner.clean_text("- 13 -\nSome text.")

def test_dosage_number_preserved(cleaner):
    assert "500" in cleaner.clean_text("Paracetamol\n500\nmg")

def test_confidential_mid_sentence_preserved(cleaner):
    assert "per HIPAA" in cleaner.clean_text("This is confidential per HIPAA.")

def test_date_removed(cleaner):
    assert "17/10/2024" not in cleaner.clean_text("Collected on: 17/10/2024\nSome text.")

def test_time_removed(cleaner):
    assert "04:55 PM" not in cleaner.clean_text("Reported on: 04:55 PM\nSome text.")


# --- DocumentCleaner: Markdown stripping ---

def test_html_br_tag_stripped(cleaner):
    assert "<br>" not in cleaner.clean_text("line1<br>line2")

def test_markdown_bold_stripped(cleaner):
    assert "**" not in cleaner.clean_text("**LYMPHOCYTE** is low.")

def test_markdown_header_stripped(cleaner):
    assert "##" not in cleaner.clean_text("## HAEMATOLOGY\nSome text.")

def test_markdown_table_pipes_stripped(cleaner):
    assert "|HEMOGLOBIN|" not in cleaner.clean_text("|HEMOGLOBIN|15|g/dl|")


# --- DocumentCleaner: extra_patterns ---

def test_extra_patterns_applied():
    cleaner = DocumentCleaner(extra_patterns=[r'(?i)\bproprietary\b'])
    assert "proprietary" not in cleaner.clean_text("This is proprietary data.")


# --- MedicalNormalizer: expansion ---

def test_htn_normalized(normalizer):
    assert "Hypertension" in normalizer.normalize_text("Patient has HTN.")

def test_t2dm_normalized(normalizer):
    assert "Type 2 Diabetes" in normalizer.normalize_text("Dx of T2DM confirmed.")

def test_sob_normalized(normalizer):
    assert "Shortness of Breath" in normalizer.normalize_text("Complains of SOB.")

def test_nv_normalized(normalizer):
    assert "Nausea and Vomiting" in normalizer.normalize_text("Reports N/V.")

def test_hr_normalized(normalizer):
    assert "Heart Rate" in normalizer.normalize_text("HR is 120.")

def test_bp_normalized(normalizer):
    assert "Blood Pressure" in normalizer.normalize_text("Monitor BP daily.")

def test_hx_normalized(normalizer):
    assert "History" in normalizer.normalize_text("Hx of hypertension.")


# --- MedicalNormalizer: case-insensitive ---

def test_lowercase_abbreviation_normalized(normalizer):
    assert "Hypertension" in normalizer.normalize_text("Patient has htn.")

def test_mixed_case_abbreviation_normalized(normalizer):
    assert "Hypertension" in normalizer.normalize_text("Patient has Htn.")


# --- MedicalNormalizer: extra_terms ---

def test_extra_terms_added():
    normalizer = MedicalNormalizer(extra_terms={"DM": "Diabetes Mellitus"})
    assert "Diabetes Mellitus" in normalizer.normalize_text("Patient has DM.")


# --- MedicalNormalizer: find_abbreviations ---

def test_find_abbreviations_returns_matches(normalizer):
    found = normalizer.find_abbreviations("Patient has HTN and SOB.")
    assert "HTN" in [f.upper() for f in found]
    assert "SOB" in [f.upper() for f in found]

def test_find_abbreviations_empty_text(normalizer):
    assert normalizer.find_abbreviations("") == []

def test_find_abbreviations_no_matches(normalizer):
    assert normalizer.find_abbreviations("No abbreviations here.") == []
