import pytest
from app.nlp.intent_classifier import get_intent_classifier, Intent
from app.nlp.severity_detector import get_severity_detector, Severity
from app.nlp.body_part_detector import get_body_part_detector

# Mock testing without having to download massive models or rely on slow inference during CI
# In a real environment, we would patch the SentenceTransformer or use small models.

def test_intent_classifier():
    classifier = get_intent_classifier()
    
    # Test heuristics
    assert classifier.classify("I am having chest pain") == Intent.EMERGENCY
    assert classifier.classify("I need a refill on my meds") == Intent.PRESCRIPTION_REFILL
    assert classifier.classify("What are my lab results?") == Intent.LAB_RESULT_INQUIRY
    
    # Test fallback embedding behavior (assuming "all-MiniLM-L6-v2" can correctly match)
    # This might take a second to run the first time if the model downloads.
    # We will test a straightforward one.
    assert classifier.classify("I have a headache and feel sick.") == Intent.NEW_DIAGNOSIS

def test_severity_detector():
    detector = get_severity_detector()
    
    assert detector.detect("I am having a heart attack!") == Severity.CRITICAL
    assert detector.detect("I have severe pain.") == Severity.HIGH
    assert detector.detect("I have a moderate fever.") == Severity.MEDIUM
    assert detector.detect("Just a mild cold.") == Severity.LOW
    assert detector.detect("I need advice on diet.") == Severity.LOW # Default fallback

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
