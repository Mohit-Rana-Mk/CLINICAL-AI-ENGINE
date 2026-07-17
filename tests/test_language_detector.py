import pytest
from app.rag.language_detector import LanguageDetector
import os


@pytest.fixture(scope="module")
def detector():
    """
    Module-scoped fixture: loads the fasttext model once for all tests
    to avoid repeated expensive model loads.
    The model is stored relative to the language_detector module file.
    """
    module_dir = os.path.dirname(
        os.path.abspath(
            __import__("app.rag.language_detector", fromlist=["language_detector"]).__file__
        )
    )
    models_dir = os.path.join(module_dir, "models")
    return LanguageDetector(models_dir=models_dir)


# ── Language detection tests ────────────────────────────────────────────────

def test_english_detected(detector):
    result = detector.detect_language(
        "Patient presents with severe headache and fever for 3 days."
    )
    assert result["language"] == "en"
    assert result["confidence"] > 0.5

def test_hindi_detected(detector):
    result = detector.detect_language("मरीज को 3 दिन से तेज सिरदर्द और बुखार है।")
    assert result["language"] == "hi"
    assert result["confidence"] > 0.9

def test_telugu_detected(detector):
    result = detector.detect_language(
        "రోగికి 3 రోజుల నుండి తీవ్రమైన తలనొప్పి మరియు జ్వరం ఉంది."
    )
    assert result["language"] == "te"
    assert result["confidence"] > 0.9

def test_spanish_detected(detector):
    result = detector.detect_language(
        "El paciente presenta dolor de cabeza severo."
    )
    assert result["language"] == "es"
    assert result["confidence"] > 0.5

def test_low_confidence_for_numbers_only(detector):
    """Pure numbers have no language signal — confidence should be very low."""
    result = detector.detect_language("12345 67890")
    assert result["confidence"] < 0.5


# ── Sanitize text tests (no model needed) ──────────────────────────────────

def test_sanitize_removes_newlines(detector):
    text = "line one\nline two\r\nline three"
    result = detector.sanitize_text(text)
    assert "\n" not in result
    assert "\r" not in result
    assert result == "line one line two line three"

def test_sanitize_collapses_spaces(detector):
    text = "too   many    spaces"
    result = detector.sanitize_text(text)
    assert result == "too many spaces"

def test_sanitize_empty_returns_empty_string(detector):
    assert detector.sanitize_text("") == ""

def test_sanitize_none_returns_empty_string(detector):
    assert detector.sanitize_text(None) == ""


# ── Edge cases ──────────────────────────────────────────────────────────────

def test_empty_string_returns_none_language(detector):
    result = detector.detect_language("")
    assert result["language"] is None
    assert result["confidence"] == 0.0

def test_whitespace_only_returns_none_language(detector):
    result = detector.detect_language("   ")
    assert result["language"] is None
    assert result["confidence"] == 0.0
