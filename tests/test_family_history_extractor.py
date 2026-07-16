import pytest
from app.ai_engine.family_history_extractor import FamilyHistoryExtractor


@pytest.fixture
def extractor():
    return FamilyHistoryExtractor()


# ── Happy-path tests ────────────────────────────────────────────────────────

def test_family_history_of_single_condition(extractor):
    result = extractor.extract("There is a family history of hypertension.")
    assert "hypertension" in result

def test_family_history_of_multiple_conditions_split(extractor):
    """'and'-joined conditions must be returned as separate items."""
    result = extractor.extract("There is a family history of hypertension and diabetes.")
    assert "hypertension" in result
    assert "diabetes" in result
    # Must NOT be returned as one merged string
    assert "hypertension and diabetes" not in result

def test_family_member_verb_pattern(extractor):
    result = extractor.extract("My father had a heart attack at age 55.")
    assert any("heart attack" in c for c in result)

def test_family_member_diagnosed_with(extractor):
    result = extractor.extract("My mother was diagnosed with Type 2 Diabetes last year.")
    assert any("type 2 diabetes" in c for c in result)

def test_runs_in_family_pattern(extractor):
    result = extractor.extract("Heart disease runs in my family.")
    assert any("heart disease" in c for c in result)

def test_multiple_family_members(extractor):
    result = extractor.extract(
        "My grandfather suffered from kidney failure and my grandmother had arthritis."
    )
    assert any("kidney failure" in c for c in result)
    assert any("arthritis" in c for c in result)

def test_comma_separated_conditions(extractor):
    result = extractor.extract("Family history of diabetes, hypertension, and cancer.")
    assert "diabetes" in result
    assert "hypertension" in result


# ── Negation tests ──────────────────────────────────────────────────────────

def test_no_family_history_returns_empty(extractor):
    """'no family history of' must NOT extract the condition."""
    result = extractor.extract("I have no family history of any illness.")
    assert result == []

def test_denies_family_history_returns_empty(extractor):
    result = extractor.extract("Patient denies any family history of cardiac disease.")
    assert result == []


# ── Edge cases ──────────────────────────────────────────────────────────────

def test_empty_string(extractor):
    assert extractor.extract("") == []

def test_whitespace_only(extractor):
    assert extractor.extract("   ") == []

def test_no_family_mention(extractor):
    result = extractor.extract("Patient has a headache and fever for 3 days.")
    assert result == []

def test_deduplication(extractor):
    """Same condition mentioned twice should appear only once."""
    result = extractor.extract(
        "Family history of diabetes. My father also had diabetes."
    )
    assert result.count("diabetes") == 1
