import pytest
from app.ai_engine.lifestyle_extractor import LifestyleExtractor


@pytest.fixture
def extractor():
    return LifestyleExtractor()


# ── Physical activity tests ─────────────────────────────────────────────────

def test_sedentary_lifestyle(extractor):
    result = extractor.extract("I have a sedentary lifestyle.")
    assert "sedentary" in result

def test_no_exercise(extractor):
    result = extractor.extract("I do no exercise at all.")
    assert "sedentary" in result

def test_physically_active(extractor):
    result = extractor.extract("I exercise regularly and go to the gym.")
    assert "physically active" in result

def test_moderate_exercise_walks(extractor):
    result = extractor.extract("I walk daily for 30 minutes.")
    assert "moderate exercise" in result


# ── Diet tests ──────────────────────────────────────────────────────────────

def test_vegetarian(extractor):
    result = extractor.extract("I follow a vegetarian diet.")
    assert "vegetarian" in result

def test_non_vegetarian(extractor):
    result = extractor.extract("I am a non-vegetarian.")
    assert "non-vegetarian" in result

def test_junk_food(extractor):
    result = extractor.extract("I mostly eat junk food and fast food.")
    assert "junk food" in result

def test_diabetic_diet(extractor):
    result = extractor.extract("I am on a diabetic diet.")
    assert "diabetic diet" in result


# ── Sleep tests ─────────────────────────────────────────────────────────────

def test_poor_sleep(extractor):
    result = extractor.extract("I only sleep 4 hours a night.")
    assert "poor sleep" in result

def test_insomnia(extractor):
    result = extractor.extract("I have insomnia.")
    assert "poor sleep" in result

def test_good_sleep(extractor):
    result = extractor.extract("I sleep well for 7-8 hours.")
    assert "good sleep" in result


# ── Occupation tests ────────────────────────────────────────────────────────

def test_desk_job(extractor):
    result = extractor.extract("I have a desk job.")
    assert "desk job" in result

def test_manual_labour(extractor):
    result = extractor.extract("I work as a farmer doing manual labour in the fields.")
    assert "manual labour" in result

def test_night_shift(extractor):
    result = extractor.extract("I work night shifts at a hospital.")
    assert "night shift" in result


# ── Combined & edge cases ───────────────────────────────────────────────────

def test_multiple_factors_detected(extractor):
    result = extractor.extract(
        "I have a sedentary lifestyle and mostly eat junk food."
    )
    assert "sedentary" in result
    assert "junk food" in result

def test_no_lifestyle_mention(extractor):
    result = extractor.extract("Patient presents with fever.")
    assert result == []

def test_empty_string(extractor):
    assert extractor.extract("") == []

def test_whitespace_only(extractor):
    assert extractor.extract("   ") == []
