import sys
from unittest.mock import MagicMock
import pytest

# Stub heavy ML deps before any app imports so tests run without them installed
for mod in ["sentence_transformers", "torch", "spacy"]:
    sys.modules.setdefault(mod, MagicMock())

from app.nlp.clinical_json_builder import get_clinical_json_builder, ClinicalJSONBuilder


@pytest.fixture
def builder():
    return get_clinical_json_builder()


def test_builder_returns_dict(builder):
    """The builder must return a dict with the expected top-level keys."""
    result = builder.build()
    assert isinstance(result, dict)
    assert "metadata" in result
    assert "clinical_payload" in result


def test_metadata_envelope(builder):
    """Metadata must contain all required fields."""
    result = builder.build(patient_id="P001", session_id="S001")
    meta = result["metadata"]

    assert meta["patient_id"] == "P001"
    assert meta["session_id"] == "S001"
    assert "timestamp" in meta
    assert meta["timestamp"].endswith("Z")  # ISO 8601
    assert "nlp_engine_version" in meta


def test_auto_generates_session_id(builder):
    """If no session_id is passed, one should be auto-generated."""
    result = builder.build()
    session_id = result["metadata"]["session_id"]
    assert session_id is not None
    assert len(session_id) > 0


def test_clinical_payload_schema(builder):
    """Clinical payload must contain all expected keys."""
    result = builder.build()
    payload = result["clinical_payload"]

    required_keys = [
        "intent", "language", "severity", "symptoms",
        "duration", "body_parts", "negations", "vitals",
        "medications", "family_history", "lifestyle",
        "lab_results", "confidence_score"
    ]
    for key in required_keys:
        assert key in payload, f"Missing key in clinical_payload: {key}"


def test_default_values(builder):
    """Default values should be empty strings, lists, or dicts — never None."""
    result = builder.build()
    payload = result["clinical_payload"]

    assert payload["intent"] == ""
    assert payload["language"] == "en"
    assert payload["severity"] == ""
    assert isinstance(payload["symptoms"], list)
    assert isinstance(payload["body_parts"], list)
    assert isinstance(payload["negations"], list)
    assert isinstance(payload["vitals"], dict)
    assert isinstance(payload["medications"], list)
    assert isinstance(payload["family_history"], list)
    assert isinstance(payload["lifestyle"], dict)
    assert isinstance(payload["lab_results"], list)
    assert payload["confidence_score"] == 1.0


def test_custom_values_are_preserved(builder):
    """Values explicitly passed to build() must appear in the payload."""
    result = builder.build(
        intent="new_diagnosis",
        language="hi",
        severity="High",
        symptoms=["fever", "cough"],
        body_parts=["chest"],
        confidence_score=0.87
    )
    payload = result["clinical_payload"]

    assert payload["intent"] == "new_diagnosis"
    assert payload["language"] == "hi"
    assert payload["severity"] == "High"
    assert "fever" in payload["symptoms"]
    assert "cough" in payload["symptoms"]
    assert "chest" in payload["body_parts"]
    assert payload["confidence_score"] == 0.87


def test_version_in_metadata():
    """Version should be configurable on the builder instance."""
    builder = ClinicalJSONBuilder(version="2.0.0")
    result = builder.build()
    assert result["metadata"]["nlp_engine_version"] == "2.0.0"


def test_mutable_defaults_dont_leak(builder):
    """Calling build() twice must return independent dicts (no shared mutable state)."""
    result1 = builder.build(symptoms=["fever"])
    result2 = builder.build(symptoms=["headache"])

    assert result1["clinical_payload"]["symptoms"] == ["fever"]
    assert result2["clinical_payload"]["symptoms"] == ["headache"]
