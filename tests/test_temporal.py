import pytest
from app.ai_engine.temporal_extractor import TemporalExtractor

@pytest.fixture
def extractor():
    return TemporalExtractor()

def test_basic_durations(extractor):
    assert extractor.extract("I've had a fever for 3 days") == "3 days"
    assert extractor.extract("Coughing for 2 weeks now") == "2 weeks"
    assert extractor.extract("Chest pain for 6 months") == "6 months"

def test_word_numbers(extractor):
    assert extractor.extract("I've been sick for three days") == "3 days"
    assert extractor.extract("Headache for a couple of weeks") == "2 weeks"
    assert extractor.extract("Fever for several days") == "7 days"
    assert extractor.extract("Been vomiting for a month") == "1 months" # Normalized to plural unit

def test_alternative_units(extractor):
    assert extractor.extract("Shortness of breath for 5 hrs") == "5 hours"
    assert extractor.extract("Pain for 1 yr") == "1 years"
    assert extractor.extract("Dizzy for 10 mins") == "10 minutes"

def test_ranges(extractor):
    assert extractor.extract("Fever for 2-3 days") == "2-3 days"
    assert extractor.extract("Sick for 4 to 5 weeks") == "4-5 weeks"
    assert extractor.extract("Pain for a few to several days") == "3-7 days"

def test_relative_time(extractor):
    assert extractor.extract("I have been feeling dizzy since yesterday") == "since yesterday"
    assert extractor.extract("My head has been pounding last night") == "last night"

def test_no_duration(extractor):
    assert extractor.extract("I have a terrible headache") is None
