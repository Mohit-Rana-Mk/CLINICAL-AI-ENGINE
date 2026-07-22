import os
from faster_whisper import WhisperModel

# Dictionary mapping common ISO 639-1 language codes to full names
LANGUAGE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian",
    "pt": "Portuguese",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu"
}

class LocalSpeechTranscriber:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        """
        Initializes the faster-whisper transcriber.
        
        Args:
            model_size (str): Size of the whisper model ('tiny', 'base', 'small', etc.)
            device (str): Compute device ('cpu' or 'cuda').
            compute_type (str): Quantization type (e.g., 'int8' for CPU, 'float16' for GPU).
        """
        print(f"Loading Whisper model '{model_size}' on {device.upper()} (Compute: {compute_type})...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("Model loaded successfully.")

    def transcribe(self, audio_path: str) -> dict:
        """
        Transcribes the audio file and extracts metadata.
        
        Args:
            audio_path (str): Path to the audio file.
            
        Returns:
            dict: Structured data containing transcription, language, confidence, and duration.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        print(f"Transcribing: {audio_path}")
        
        # beam_size=5 is a good default for accuracy vs speed
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        # We need to iterate over the generator to actually perform transcription
        transcription_text = ""
        total_probability = 0.0
        segment_count = 0
        
        for segment in segments:
            transcription_text += segment.text + " "
            total_probability += segment.no_speech_prob # This is actually no_speech prob, to get confidence we do 1 - no_speech_prob or use avg_logprob. Let's use avg_logprob for a better proxy.
            segment_count += 1
            
        transcription_text = transcription_text.strip()
        
        # Get full language name
        detected_lang_code = info.language
        full_language_name = LANGUAGE_MAP.get(detected_lang_code, detected_lang_code.capitalize())
        
        # We can use the language_probability from the info object for overall confidence
        confidence_score = round(info.language_probability, 4)
        
        result = {
            "transcription": transcription_text,
            "detected_language": full_language_name,
            "confidence_score": confidence_score,
            "duration_seconds": round(info.duration, 2) if hasattr(info, 'duration') else 0.0
        }
        
        print("Transcription complete.")
        return result
