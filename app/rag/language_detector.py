import os
import re
import logging
import urllib.request
import fasttext

logger = logging.getLogger(__name__)

class LanguageDetector:
    """
    Language Detector using fasttext for identifying the language of medical text.
    Automatically downloads the 'lid.176.bin' model if not found locally.
    """
    
    MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
    MODEL_FILENAME = "lid.176.bin"
    
    def __init__(self, models_dir="models"):
        self.models_dir = models_dir
        self.model_path = os.path.join(self.models_dir, self.MODEL_FILENAME)
        
        # Ensure the models directory exists
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Download the model if it doesn't exist
        if not os.path.exists(self.model_path):
            self._download_model()

        # Load the model
        logger.info(f"Loading fasttext model from {self.model_path}...")

        # Suppress fasttext warning about predict
        fasttext.FastText.eprint = lambda x: None
        self.model = fasttext.load_model(self.model_path)
        logger.info("Model loaded successfully.")

    def _download_model(self):
        """Downloads the fasttext language identification model."""
        logger.info(f"Downloading language model to {self.model_path} (~126MB, first-time only)...")
        try:
            urllib.request.urlretrieve(self.MODEL_URL, self.model_path)
            logger.info("Download complete.")
        except Exception as e:
            logger.error(f"Failed to download the model: {e}")
            if os.path.exists(self.model_path):
                os.remove(self.model_path)
            raise

    def sanitize_text(self, text: str) -> str:
        """
        Cleans text to be compatible with fasttext.
        fasttext expects a single line of text.
        """
        if not text:
            return ""
        # Remove newlines and extra spaces
        clean_text = re.sub(r'[\r\n]+', ' ', text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        return clean_text

    def detect_language(self, text: str) -> dict:
        """
        Detects the language of the provided text.
        
        Args:
            text (str): The text to identify.
            
        Returns:
            dict: A dictionary containing 'language' (ISO code) and 'confidence' (float).
                  Returns None for both if detection fails.
        """
        clean_text = self.sanitize_text(text)
        if not clean_text:
            return {"language": None, "confidence": 0.0}
            
        try:
            # k=1 returns the top 1 prediction
            predictions, confidences = self.model.predict(clean_text, k=1)
            
            # fasttext labels look like '__label__en'
            label = predictions[0].replace('__label__', '')
            confidence = float(confidences[0])
            
            return {
                "language": label,
                "confidence": round(confidence, 4)
            }
        except Exception as e:
            logger.error(f"Error during language detection: {e}")
            return {"language": None, "confidence": 0.0}


