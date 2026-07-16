import pytest
from app.rag.metadata_builder import build_metadata

def test_build_metadata_empty():
    metadata = build_metadata("")
    assert metadata["word_count"] == 0
    assert "generated_at" in metadata
    # Ensure none of the explicitly optional fields are present if not passed
    assert "disease" not in metadata
    assert "page" not in metadata

def test_build_metadata_with_fields():
    chunk = "This is a test chunk about cardiology."
    metadata = build_metadata(
        chunk=chunk,
        disease="Hypertension",
        speciality="Cardiology",
        page=12,
        version="v1.0",
        custom_field="value"
    )

    assert metadata["word_count"] == 7
    assert metadata["disease"] == "Hypertension"
    assert metadata["speciality"] == "Cardiology"
    assert metadata["page"] == 12
    assert metadata["version"] == "v1.0"
    assert metadata["custom_field"] == "value"
    
    # Check that missing fields aren't in the dict
    assert "language" not in metadata
    assert "source" not in metadata

def test_build_metadata_none_values():
    chunk = "Test chunk"
    # Even if someone explicitly passes None, it should be filtered out
    metadata = build_metadata(chunk, language=None, disease="Diabetes")
    assert "language" not in metadata
    assert metadata["disease"] == "Diabetes"
    assert metadata["word_count"] == 2
