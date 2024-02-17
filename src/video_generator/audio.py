# audio.py

import io
import base64
from pydub import AudioSegment
from video_generator.util.client.google import synthesize_text

def generate_audio(script):
    synthesized_text = synthesize_text(script)
    audio_content_byte = base64.b64decode(synthesized_text)
    audio_content = io.BytesIO(audio_content_byte)
    audio = AudioSegment.from_file(audio_content, format="wav")
    print("Successfully generated audio!")
    return audio
