import sys
import types
import pytest
from app.nlp.intent_classifier import get_intent_classifier, Intent
from app.nlp.severity_detector import get_severity_detector, Severity
from app.nlp.body_part_detector import get_body_part_detector

# Detect if packages are REAL (not MagicMock stubs injected by other test files).
# sys.modules may contain a MagicMock if test_pipeline.py ran first.
def _is_real_module(name: str) -> bool:
    mod = sys.modules.get(name)
    return isinstance(mod, types.ModuleType)

_HAS_ST = _is_real_module("sentence_transformers")
_HAS_SPACY = _is_real_module("spacy")


@pytest.mark.skipif(not _HAS_ST, reason="sentence_transformers not installed")
def test_intent_classifier_rules():
    """Rule-based heuristics — no ML model needed."""
    classifier = get_intent_classifier()
    assert classifier.classify("I am having chest pain") == Intent.EMERGENCY
    assert classifier.classify("I need a refill on my meds") == Intent.PRESCRIPTION_REFILL
    assert classifier.classify("What are my lab results?") == Intent.LAB_RESULT_INQUIRY


@pytest.mark.skipif(not _HAS_ST, reason="sentence_transformers not installed — skipping embedding fallback")
def test_intent_classifier_embedding_fallback():
    """Embedding fallback — requires the real sentence_transformers model."""
    classifier = get_intent_classifier()
    assert classifier.classify("I have a headache and feel sick.") == Intent.NEW_DIAGNOSIS


def test_severity_detector():
    """Pure rule-based — no ML packages needed."""
    detector = get_severity_detector()

    assert detector.detect("I am having a heart attack!") == Severity.CRITICAL
    assert detector.detect("I have severe pain.") == Severity.HIGH
    assert detector.detect("I have a moderate fever.") == Severity.MEDIUM
    assert detector.detect("Just a mild cold.") == Severity.LOW
    assert detector.detect("I need advice on diet.") == Severity.LOW  # Default fallback


@pytest.mark.skipif(not _HAS_SPACY, reason="spacy en_core_web_sm model not installed")
def test_body_part_detector():
    detector = get_body_part_detector()

    res1 = detector.detect("I have pain in my left arm.")
    assert len(res1) == 1
    assert res1[0]["linked_part"] == "left arm"

    res2 = detector.detect("My lower back hurts a lot.")
    assert len(res2) == 1
    assert res2[0]["linked_part"] == "lower back"

    res3 = detector.detect("I have a headache.")
    assert len(res3) == 1
    assert res3[0]["linked_part"] == "head"
