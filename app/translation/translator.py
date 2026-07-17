from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import logging

logger = logging.getLogger(__name__)

class LocalTranslator:
    """
    Local translation model using NLLB-200 for Indian languages.
    Translates regional languages to English.
    """
    
    # Mapping fasttext ISO codes to NLLB-200 BCP-47 codes
    LANGUAGE_MAPPING = {
        "hi": "hin_Deva", # Hindi
        "pa": "pan_Guru", # Punjabi
        "ta": "tam_Taml", # Tamil
        "te": "tel_Telu", # Telugu
        "kn": "kan_Knda", # Kannada
        "ml": "mal_Mlym", # Malayalam
        "gu": "guj_Gujr", # Gujarati
        "mr": "mar_Deva", # Marathi
        "ur": "urd_Arab", # Urdu
        "bn": "ben_Beng", # Bengali (bonus)
    }

    def __init__(self, model_name="facebook/nllb-200-distilled-600M", device="cpu"):
        self.model_name = model_name
        self.device = device
        
        logger.info(f"Loading translation model {model_name} on {device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        logger.info("Translation model loaded successfully.")

    def translate(self, text: str, source_lang_code: str) -> str:
        """
        Translates text from the source language to English.
        """
        if not text.strip():
            return ""

        # Default to English if not mapped, though router should prevent this
        nllb_src_lang = self.LANGUAGE_MAPPING.get(source_lang_code, "eng_Latn")
        
        # Ensure the tokenizer uses the correct source language
        self.tokenizer.src_lang = nllb_src_lang
        
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        
        # Target language is always English (eng_Latn)
        translated_tokens = self.model.generate(
            **inputs, 
            forced_bos_token_id=self.tokenizer.convert_tokens_to_ids("eng_Latn"),
            max_length=512
        )
        
        translated_text = self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translated_text
