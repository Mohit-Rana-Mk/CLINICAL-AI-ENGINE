import pytest
from app.ai_engine.synonym_mapper import SynonymMapper

@pytest.fixture
def mapper():
    return SynonymMapper()

def test_exact_synonyms(mapper):
    assert mapper.map_synonym("dyspnea") == "shortness of breath"
    assert mapper.map_synonym("trouble breathing") == "shortness of breath"
    assert mapper.map_synonym("queasy") == "nausea"
    assert mapper.map_synonym("upset stomach") == "nausea"
    assert mapper.map_synonym("throwing up") == "vomiting"

def test_canonical_passthrough(mapper):
    # If passed a canonical term, it should return it
    assert mapper.map_synonym("fever") == "fever"
    assert mapper.map_synonym("shortness of breath") == "shortness of breath"

def test_unknown_term(mapper):
    # If the term isn't in the database, just return it as-is so downstream tasks can still process it
    assert mapper.map_synonym("weird elbow pain") == "weird elbow pain"

def test_case_and_whitespace(mapper):
    assert mapper.map_synonym("DYSPNEA") == "shortness of breath"
    assert mapper.map_synonym("Queasy") == "nausea"
    assert mapper.map_synonym("  tired  ") == "fatigue"
