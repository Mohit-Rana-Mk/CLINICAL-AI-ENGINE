import os
from pydub import AudioSegment

class AudioPreprocessor:
    def __init__(self, target_sample_rate=16000, target_channels=1):
        """
        Initializes the AudioPreprocessor.
        Converts audio to a standardized format: 16kHz, mono WAV.
        """
        self.target_sample_rate = target_sample_rate
        self.target_channels = target_channels

    def process(self, input_path: str, output_path: str = None) -> str:
        """
        Reads an audio file, converts it to 16kHz mono WAV, and saves it.
        
        Args:
            input_path (str): Path to the input audio file (.wav, .mp3, .m4a, etc.)
            output_path (str, optional): Path to save the processed file. 
                                         If None, creates a temporary file.
                                         
        Returns:
            str: Path to the processed WAV file.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Audio file not found: {input_path}")

        print(f"Preprocessing audio: {input_path}")
        
        try:
            # Load audio (pydub automatically infers format from extension if ffmpeg is available)
            audio = AudioSegment.from_file(input_path)
            
            # Convert to target properties
            audio = audio.set_frame_rate(self.target_sample_rate)
            audio = audio.set_channels(self.target_channels)
            
            # Determine output path
            if output_path is None:
                base, _ = os.path.splitext(input_path)
                output_path = f"{base}_processed.wav"
                
            # Export
            audio.export(output_path, format="wav")
            print(f"Successfully processed to: {output_path}")
            return output_path
            
        except Exception as e:
            raise RuntimeError(f"Failed to process audio. Please ensure ffmpeg is installed. Error: {str(e)}")
