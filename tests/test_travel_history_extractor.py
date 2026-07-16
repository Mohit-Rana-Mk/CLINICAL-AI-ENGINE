import pytest
from app.ai_engine.travel_history_extractor import TravelHistoryExtractor


@pytest.fixture
def extractor():
    return TravelHistoryExtractor()


# ── Happy-path tests ────────────────────────────────────────────────────────

def test_returned_from_known_state(extractor):
    result = extractor.extract("I recently returned from Rajasthan.")
    assert "Rajasthan" in result

def test_multiple_locations(extractor):
    result = extractor.extract(
        "I recently returned from Rajasthan and visited Delhi last week."
    )
    assert "Rajasthan" in result
    assert "Delhi" in result

def test_traveled_to_city(extractor):
    result = extractor.extract("I traveled to Mumbai for work.")
    assert "Mumbai" in result

def test_came_from_location(extractor):
    result = extractor.extract("I came from Bihar last month.")
    assert "Bihar" in result

def test_international_location(extractor):
    result = extractor.extract("I went to Southeast Asia for a holiday 3 weeks ago.")
    assert "Southeast Asia" in result

def test_forest_area_keyword(extractor):
    result = extractor.extract("I came from a forest area near Uttarakhand.")
    assert "Uttarakhand" in result or "forest area" in result

def test_was_in_pattern(extractor):
    result = extractor.extract("I was in Bihar last month.")
    assert "Bihar" in result


# ── Negation / residence tests ──────────────────────────────────────────────

def test_no_travel_history_returns_empty(extractor):
    result = extractor.extract("No travel history.")
    assert result == []

def test_living_in_not_travel(extractor):
    """Permanent residence must NOT be detected as travel history."""
    result = extractor.extract("I have been living in Chennai for 5 years.")
    assert result == []

def test_born_in_not_travel(extractor):
    result = extractor.extract("I was born in Delhi.")
    assert result == []

def test_based_in_not_travel(extractor):
    result = extractor.extract("I am based in Mumbai.")
    assert result == []


# ── Deduplication tests ─────────────────────────────────────────────────────

def test_no_duplicate_locations(extractor):
    result = extractor.extract(
        "I traveled to Rajasthan. I recently returned from Rajasthan."
    )
    assert result.count("Rajasthan") == 1


# ── Edge cases ──────────────────────────────────────────────────────────────

def test_empty_string(extractor):
    assert extractor.extract("") == []

def test_whitespace_only(extractor):
    assert extractor.extract("   ") == []

def test_no_travel_mention(extractor):
    result = extractor.extract("Patient has a headache and fever for 3 days.")
    assert result == []
