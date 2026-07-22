import pytest
from app.ai_engine.negation_detector import NegationDetector

@pytest.fixture
def detector():
    return NegationDetector()

def test_basic_pre_negation(detector):
    assert detector.is_negated("I have no fever", "fever") == True
    assert detector.is_negated("Patient denies nausea", "nausea") == True
    assert detector.is_negated("He does not have a cough", "cough") == True

def test_basic_post_negation(detector):
    assert detector.is_negated("Headache: absent", "headache") == True
    assert detector.is_negated("Fever is unlikely", "fever") == True

def test_positive_cases(detector):
    # Simply mentioning the symptom without negation
    assert detector.is_negated("I have a fever", "fever") == False
    assert detector.is_negated("Patient reports nausea", "nausea") == False

def test_boundary_termination(detector):
    # The "but" should stop the "no" from bleeding over to negate "fever"
    text1 = "I have no history of asthma, but I do have a fever."
    assert detector.is_negated(text1, "fever") == False
    
    # The comma should terminate the forward search, stopping "none" from negating "cough"
    text2 = "Cough is present, fever: none."
    assert detector.is_negated(text2, "cough") == False

def test_multiple_mentions(detector):
    # If a symptom is mentioned twice, and one mention is positive (not negated),
    # the patient ultimately has the symptom, so it should return False.
    text = "I don't have a cough. Actually, I do have a mild cough."
    assert detector.is_negated(text, "cough") == False

def test_case_insensitivity(detector):
    assert detector.is_negated("NO FEVER", "fever") == True
    assert detector.is_negated("no fever", "FEVER") == True
