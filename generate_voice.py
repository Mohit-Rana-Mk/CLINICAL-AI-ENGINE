import wave
import struct

# Create a 1-second silent WAV file
file_name = "dummy_patient_audio.wav"
with wave.open(file_name, "w") as audio_file:
    audio_file.setnchannels(1)  # Mono
    audio_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
    audio_file.setframerate(44100) # 44.1 kHz
    
    # Write 44100 frames of silence (0)
    for _ in range(44100):
        audio_file.writeframesraw(struct.pack('<h', 0))

print(f"Sample voice file '{file_name}' created successfully!")