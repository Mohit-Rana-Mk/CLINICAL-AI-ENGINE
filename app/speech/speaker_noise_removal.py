import os
import noisereduce as nr
from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment

class NoiseReducer:
    def __init__(self, prop_decrease=1.0):
        """
        Initializes the NoiseReducer.
        
        Args:
            prop_decrease (float): The proportion to reduce the noise by (0.0 to 1.0). 
                                   1.0 means full reduction.
        """
        self.prop_decrease = prop_decrease

    def process(self, input_path: str, output_path: str = None) -> str:
        """
        Applies spectral gating noise reduction and volume normalization to a WAV file.
        
        Args:
            input_path (str): Path to the input 16kHz mono WAV file.
            output_path (str, optional): Path to save the cleaned file.
            
        Returns:
            str: Path to the cleaned WAV file.
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Audio file not found: {input_path}")
            
        if not input_path.lower().endswith(".wav"):
            raise ValueError("Noise reduction currently only supports WAV files. Run it through the preprocessor first.")

        print(f"Applying noise reduction to: {input_path}")
        
        # Load data
        rate, data = wavfile.read(input_path)
        
        # Perform noise reduction
        # Using stationary noise reduction which is fast and good for background hums
        reduced_noise = nr.reduce_noise(y=data, sr=rate, prop_decrease=self.prop_decrease)
        
        # Determine output path
        if output_path is None:
            base, _ = os.path.splitext(input_path)
            output_path = f"{base}_cleaned.wav"
            
        # Save temporary cleaned audio
        wavfile.write(output_path, rate, reduced_noise)
        
        # Normalize volume using pydub
        print("Normalizing audio volume...")
        audio = AudioSegment.from_wav(output_path)
        
        # Normalize to target peak (e.g., -3.0 dBFS)
        target_dBFS = -3.0
        change_in_dBFS = target_dBFS - audio.max_dBFS
        normalized_audio = audio.apply_gain(change_in_dBFS)
        
        # Overwrite with normalized audio
        normalized_audio.export(output_path, format="wav")
        
        print(f"Successfully cleaned and normalized to: {output_path}")
        return output_path
