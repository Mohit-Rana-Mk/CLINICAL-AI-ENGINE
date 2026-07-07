from app.ai_engine.entity_extractor import MedicalEntityExtractor


def test_extract_symptoms():
    extractor = MedicalEntityExtractor()

    result = extractor.extract(
        "I have fever and cough"
    )

    assert "fever" in result.symptoms
    assert "cough" in result.symptoms