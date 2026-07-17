import sys
import pytest
from unittest.mock import patch, MagicMock

# Stub heavy ML deps before any app imports so tests run without them installed
for mod in ["sentence_transformers", "torch", "spacy", "transformers",
            "faster_whisper", "noisereduce", "scipy", "scipy.io",
            "scipy.io.wavfile", "paddleocr", "paddlepaddle", "fitz",
            "cv2", "fasttext", "cachetools"]:
    sys.modules.setdefault(mod, MagicMock())

from app.pipeline import ClinicalPipeline, get_clinical_pipeline


# ─── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_pipeline():
    """
    Returns a ClinicalPipeline instance with all heavy ML dependencies patched out
    so the test suite runs fast without downloading models.
    """
    with patch("app.pipeline.TranslationRouter") as MockRouter, \
         patch("app.pipeline.get_intent_classifier") as MockIntent, \
         patch("app.pipeline.get_severity_detector") as MockSeverity, \
         patch("app.pipeline.get_clinical_json_builder") as MockBuilder, \
         patch("app.pipeline.get_followup_engine") as MockFollowup:

        # Configure mock return values
        mock_router_instance = MagicMock()
        mock_router_instance.process.return_value = {
            "original_text": "I have chest pain",
            "detected_language": "en",
            "confidence": 0.99,
            "was_translated": False,
            "english_text": "I have chest pain"
        }
        MockRouter.return_value = mock_router_instance

        mock_intent_instance = MagicMock()
        mock_intent_instance.classify.return_value = MagicMock(value="emergency")
        MockIntent.return_value = mock_intent_instance

        mock_severity_instance = MagicMock()
        mock_severity_instance.detect.return_value = MagicMock(value="Critical")
        MockSeverity.return_value = mock_severity_instance

        mock_builder_instance = MagicMock()
        mock_builder_instance.build.return_value = {
            "metadata": {
                "patient_id": None,
                "session_id": "test-session-001",
                "timestamp": "2026-07-17T00:00:00Z",
                "nlp_engine_version": "1.0.0"
            },
            "clinical_payload": {
                "intent": "emergency",
                "language": "en",
                "severity": "Critical",
                "symptoms": ["chest pain"],
                "body_parts": ["chest"],
                "confidence_score": 0.9
            }
        }
        MockBuilder.return_value = mock_builder_instance

        mock_followup_instance = MagicMock()
        mock_followup_instance.generate_followup.return_value = {
            "question": "Are you experiencing trouble breathing?",
            "is_urgent": True
        }
        MockFollowup.return_value = mock_followup_instance

        pipeline = ClinicalPipeline()
        yield pipeline


# ─── Tests ────────────────────────────────────────────────────────────────────

def test_pipeline_output_structure(mock_pipeline):
    """The pipeline must return a dict with clinical_data, metadata, and followup_action."""
    result = mock_pipeline.process("I have chest pain", session_id="test-session-001")

    assert "clinical_data" in result
    assert "metadata" in result
    assert "followup_action" in result


def test_pipeline_metadata_contains_session_id(mock_pipeline):
    """The metadata in the final output must carry the correct session_id."""
    result = mock_pipeline.process("I have chest pain", session_id="test-session-001")
    assert result["metadata"]["session_id"] == "test-session-001"


def test_pipeline_auto_generates_session_id(mock_pipeline):
    """If no session_id is passed, the pipeline must auto-generate one."""
    result = mock_pipeline.process("I have chest pain")
    assert result["metadata"]["session_id"] is not None


def test_pipeline_followup_action_shape(mock_pipeline):
    """Follow-up action must have a question string and is_urgent boolean."""
    result = mock_pipeline.process("I have chest pain", session_id="test-session-001")
    followup = result["followup_action"]

    assert "question" in followup
    assert "is_urgent" in followup
    assert isinstance(followup["question"], str)
    assert isinstance(followup["is_urgent"], bool)


def test_pipeline_calls_language_router(mock_pipeline):
    """The pipeline must call language_router.process() on the input text."""
    mock_pipeline.process("I have chest pain", session_id="s1")
    mock_pipeline.language_router.process.assert_called_once_with("I have chest pain")


def test_pipeline_calls_intent_classifier(mock_pipeline):
    """The pipeline must call intent_classifier.classify()."""
    mock_pipeline.process("I have chest pain", session_id="s1")
    mock_pipeline.intent_classifier.classify.assert_called_once()


def test_pipeline_calls_severity_detector(mock_pipeline):
    """The pipeline must call severity_detector.detect()."""
    mock_pipeline.process("I have chest pain", session_id="s1")
    mock_pipeline.severity_detector.detect.assert_called_once()


def test_pipeline_calls_followup_engine(mock_pipeline):
    """The pipeline must call followup_engine.generate_followup()."""
    mock_pipeline.process("I have chest pain", session_id="s1")
    mock_pipeline.followup_engine.generate_followup.assert_called_once()


def test_pipeline_empty_input(mock_pipeline):
    """Passing an empty string should not crash the pipeline."""
    mock_pipeline.language_router.process.return_value = {
        "detected_language": "en",
        "english_text": "",
        "confidence": 0.0,
        "was_translated": False,
        "original_text": ""
    }
    # Should not raise
    result = mock_pipeline.process("", session_id="s_empty")
    assert result is not None


def test_get_clinical_pipeline_returns_singleton():
    """get_clinical_pipeline() should return the same instance on repeated calls."""
    with patch("app.pipeline.TranslationRouter"), \
         patch("app.pipeline.get_intent_classifier"), \
         patch("app.pipeline.get_severity_detector"), \
         patch("app.pipeline.get_clinical_json_builder"), \
         patch("app.pipeline.get_followup_engine"):
        p1 = get_clinical_pipeline()
        p2 = get_clinical_pipeline()
        assert p1 is p2
