import pytest
from app.ai_engine.entity_extractor import MedicalEntityExtractor

@pytest.fixture
def extractor():
    return MedicalEntityExtractor()

def test_full_integration(extractor):
    text = "I have a mild fever of 101.5 degrees for 3 days. No cough or nausea. I have a migraine."
    
    result = extractor.extract(text)
    
    # Check that synonyms mapped correctly and negations were caught
    assert "fever" in result.symptoms
    assert "headache" in result.symptoms # Derived from "migraine" via synonym mapper
    assert "cough" not in result.symptoms # Negated by "No"
    assert "nausea" not in result.symptoms # Negated by "No"
    
    # Check other entities
    assert result.duration == "3 days"
    assert result.temperature == "101.5"
    assert "mild" in result.severity

def test_pain_scale(extractor):
    text = "Severe stomach ache. Pain is 8/10."
    result = extractor.extract(text)
    
    assert "severe" in result.severity
    assert "8/10" in result.severity
    assert result.body_location == "stomach"