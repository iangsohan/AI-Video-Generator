# audio.py

import io
import base64
from pydub import AudioSegment
from video_generator.util.client.google import synthesize_text

def generate_audio(script):
    # Synthesize text to audio
    synthesized_text = synthesize_text(script)
    
    # Decode the base64-encoded audio content
    audio_content_byte = base64.b64decode(synthesized_text)
    
    # Load the audio content as an AudioSegment object
    audio_content = io.BytesIO(audio_content_byte)
    audio = AudioSegment.from_file(audio_content, format="wav")
    
    # Add background music to the audio
    audio = add_background_music(audio)
    
    # Return the combined audio
    print("Successfully generated audio!")
    return audio


def add_background_music(audio):
    # Get the duration of the main audio
    main_duration = len(audio)
    
    # Load the background music
    background_music = AudioSegment.from_file("video_generator/assets/media/background.mp3", format="mp3")
    
    # Decrease the volume of the background music
    background_music = background_music - 6
    
    # Crop the background music to match the duration of the main audio
    background_music = background_music[:main_duration]
    
    # Apply fade-in and fade-out effects to the background music
    background_music = background_music.fade_in(5000).fade_out(5000)
    
    # Overlay the background music onto the main audio
    main_audio = audio.overlay(background_music)
    
    # Return the combined audio
    return main_audio
