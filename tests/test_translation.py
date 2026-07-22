import pytest
from unittest.mock import patch, MagicMock
from app.translation.language_router import TranslationRouter
from app.translation.medical_translation import MedicalTermNormalizer

def test_medical_normalizer():
    normalizer = MedicalTermNormalizer()
    
    # Test literal translation fixes
    assert normalizer.normalize("I have sweet blood and breathing difficulty") == "I have diabetes and dyspnea"
    assert normalizer.normalize("My head ache is bad") == "My headache is bad"
    assert normalizer.normalize("Feeling puke and spinning head") == "nausea and vertigo"
    
    # Test case insensitivity
    assert normalizer.normalize("SUGAR is high") == "diabetes is high"
    
    # Test passthrough
    assert normalizer.normalize("Normal sentence") == "Normal sentence"

@patch('app.translation.translator.AutoModelForSeq2SeqLM.from_pretrained')
@patch('app.translation.translator.AutoTokenizer.from_pretrained')
def test_translation_router_hindi(mock_tokenizer, mock_model):
    # Mock the language detector and translator to avoid downloading 2.4GB model in unit tests
    with patch('app.translation.language_router.LanguageDetector.detect_language') as mock_detect:
        mock_detect.return_value = {"language": "hi", "confidence": 0.99}
        
        # Setup Router
        router = TranslationRouter()
        
        # Mock translator logic
        router.translator.translate = MagicMock(return_value="I have severe sweet food.")
        
        # Process Hindi text: "Mujhe bahut sugar hai."
        result = router.process("Mujhe bahut sugar hai.")
        
        assert result["detected_language"] == "hi"
        assert result["was_translated"] is True
        
        # It should translate to "I have severe sweet food."
        # Then MedicalNormalizer should change "sweet food" to "diabetes"
        assert result["english_text"] == "I have severe diabetes."

@patch('app.translation.translator.AutoModelForSeq2SeqLM.from_pretrained')
@patch('app.translation.translator.AutoTokenizer.from_pretrained')
def test_translation_router_english(mock_tokenizer, mock_model):
    with patch('app.translation.language_router.LanguageDetector.detect_language') as mock_detect:
        mock_detect.return_value = {"language": "en", "confidence": 0.98}
        
        router = TranslationRouter()
        
        # It should NOT call translate if English
        router.translator.translate = MagicMock()
        
        result = router.process("I have severe head ache.")
        
        assert result["detected_language"] == "en"
        assert result["was_translated"] is False
        assert router.translator.translate.call_count == 0
        
        # Normalizer should still run on English text ("head ache" -> "headache")
        assert result["english_text"] == "I have severe headache."
