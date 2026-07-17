import os
import wave
import struct
import math
import pytest
from app.speech.voice_preprocessor import AudioPreprocessor
from app.speech.speaker_noise_removal import NoiseReducer
from app.speech.speech_to_text import LocalSpeechTranscriber

def generate_dummy_wav(filepath: str, duration_sec=2, sample_rate=44100):
    """Generates a simple 440Hz sine wave dummy WAV file for testing."""
    num_samples = int(duration_sec * sample_rate)
    
    with wave.open(filepath, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            value = int(32767.0 * math.sin(2.0 * math.pi * 440.0 * i / sample_rate))
            wav_data = struct.pack('<h', value)
            wav_file.writeframesraw(wav_data)

@pytest.fixture
def dummy_audio_file(tmp_path):
    file_path = tmp_path / "test_audio.wav"
    generate_dummy_wav(str(file_path))
    return str(file_path)

def test_audio_preprocessor(dummy_audio_file):
    preprocessor = AudioPreprocessor(target_sample_rate=16000, target_channels=1)
    
    output_path = preprocessor.process(dummy_audio_file)
    
    assert os.path.exists(output_path)
    
    # Verify properties
    with wave.open(output_path, 'r') as wav_file:
        assert wav_file.getframerate() == 16000
        assert wav_file.getnchannels() == 1
        
    os.remove(output_path)

def test_speaker_noise_removal(dummy_audio_file):
    preprocessor = AudioPreprocessor()
    processed_path = preprocessor.process(dummy_audio_file)
    
    reducer = NoiseReducer()
    cleaned_path = reducer.process(processed_path)
    
    assert os.path.exists(cleaned_path)
    os.remove(processed_path)
    os.remove(cleaned_path)

def test_speech_to_text(dummy_audio_file):
    # This is an integration test for the pipeline
    preprocessor = AudioPreprocessor()
    reducer = NoiseReducer()
    transcriber = LocalSpeechTranscriber(model_size="tiny", device="cpu") # use tiny for faster testing
    
    processed_path = preprocessor.process(dummy_audio_file)
    cleaned_path = reducer.process(processed_path)
    
    # Transcribe the sine wave (it won't have words, but we test the structure)
    result = transcriber.transcribe(cleaned_path)
    
    assert "transcription" in result
    assert "detected_language" in result
    assert "confidence_score" in result
    assert "duration_seconds" in result
    
    os.remove(processed_path)
    os.remove(cleaned_path)
