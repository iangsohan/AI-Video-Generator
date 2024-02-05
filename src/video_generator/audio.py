# audio.py

import base64
from io import BytesIO
from pydub import AudioSegment
from video_generator.util.client.google import synthesize_text

def generate_audio(script):
    """
    Generate audio from a text script using Google Text-to-Speech API.

    Args:
    - script (str): The script content to be converted to audio.

    Returns:
    - AudioSegment: The generated audio segment.
    """
    # Synthesize text using Google Text-to-Speech API
    synthesized_text = synthesize_text(script)

    # Decode base64-encoded audio content
    audio_content_byte = base64.b64decode(synthesized_text)

    # Convert bytes to BytesIO object
    audio_content = BytesIO(audio_content_byte)

    # Create an AudioSegment directly from BytesIO
    audio = AudioSegment.from_file(audio_content, format="wav")

    print("Successfully generated audio!")
    return audio
