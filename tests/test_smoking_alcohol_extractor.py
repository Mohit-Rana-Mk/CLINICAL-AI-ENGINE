import pytest
from app.ai_engine.smoking_alcohol_extractor import SmokingAlcoholExtractor


@pytest.fixture
def extractor():
    return SmokingAlcoholExtractor()


# ── Smoking status tests ────────────────────────────────────────────────────

def test_current_smoker_cigarettes(extractor):
    smoking, _ = extractor.extract("I smoke about 10 cigarettes a day.")
    assert smoking == "current smoker"

def test_current_smoker_bidi(extractor):
    smoking, _ = extractor.extract("He smokes bidis regularly.")
    assert smoking == "current smoker"

def test_ex_smoker_quit(extractor):
    smoking, _ = extractor.extract("I quit smoking 2 years ago.")
    assert smoking == "ex-smoker"

def test_ex_smoker_label(extractor):
    smoking, _ = extractor.extract("Patient is an ex-smoker.")
    assert smoking == "ex-smoker"

def test_non_smoker_never(extractor):
    smoking, _ = extractor.extract("I have never smoked.")
    assert smoking == "non-smoker"

def test_non_smoker_label(extractor):
    smoking, _ = extractor.extract("Non-smoker.")
    assert smoking == "non-smoker"

def test_denies_tobacco_not_smoker(extractor):
    """'denies tobacco use' must NOT be classified as current smoker."""
    smoking, _ = extractor.extract("Patient denies tobacco use.")
    assert smoking == "non-smoker"

def test_no_tobacco_not_smoker(extractor):
    smoking, _ = extractor.extract("No tobacco use.")
    assert smoking == "non-smoker"

def test_no_smoking_mention_returns_none(extractor):
    smoking, _ = extractor.extract("Patient has a headache.")
    assert smoking is None


# ── Alcohol use tests ───────────────────────────────────────────────────────

def test_heavy_drinker_alcoholic(extractor):
    _, alcohol = extractor.extract("He is an alcoholic.")
    assert alcohol == "heavy drinker"

def test_heavy_drinker_daily(extractor):
    _, alcohol = extractor.extract("She drinks daily.")
    assert alcohol == "heavy drinker"

def test_social_drinker(extractor):
    _, alcohol = extractor.extract("I drink socially at parties.")
    assert alcohol == "social drinker"

def test_non_drinker_teetotaler(extractor):
    _, alcohol = extractor.extract("I am a teetotaler.")
    assert alcohol == "non-drinker"

def test_non_drinker_no_alcohol(extractor):
    _, alcohol = extractor.extract("No alcohol.")
    assert alcohol == "non-drinker"

def test_no_alcohol_mention_returns_none(extractor):
    _, alcohol = extractor.extract("Patient has chest pain.")
    assert alcohol is None


# ── Combined tests ──────────────────────────────────────────────────────────

def test_both_detected(extractor):
    smoking, alcohol = extractor.extract(
        "I smoke 10 cigarettes a day and drink occasionally."
    )
    assert smoking == "current smoker"
    assert alcohol is not None

def test_both_negative(extractor):
    smoking, alcohol = extractor.extract("Non-smoker and teetotaler.")
    assert smoking == "non-smoker"
    assert alcohol == "non-drinker"


# ── Edge cases ──────────────────────────────────────────────────────────────

def test_empty_string(extractor):
    assert extractor.extract("") == (None, None)

def test_whitespace_only(extractor):
    assert extractor.extract("   ") == (None, None)
