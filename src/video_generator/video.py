# video.py

import tempfile
import numpy as np
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips
from video_generator.util.metadata import get_title, get_description
from video_generator.util.thumbnail import curate_thumbnail
from video_generator.util.client.youtube import upload_video, insert_captions
from video_generator.util.client.google import translate

# Define a list of language codes for translation and captioning
LANGUAGE_CODES = ["en-GB", "hi-IN", "es-ES", "fr-FR", "cmn-CN"]

def curate_video(animal, script, audio, images):
    # Create the main video
    video = create_video(audio, images)
    
    # Publish the video to YouTube
    video_id = publish_video(animal, video)
    
    # Curate the video thumbnail
    curate_thumbnail(animal, video_id)
    
    # Translate the script and insert captions for different languages
    for language in LANGUAGE_CODES:
        translation = translate(animal, script, language)
        insert_captions(video_id, translation, language)


def create_video(audio, images):
    # Create a temporary WAV audio file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        audio.export(temp_file.name, format="wav")
        audio_file_path = temp_file.name
        audio_clip = AudioFileClip(audio_file_path)
    
    # Calculate the duration per image based on the audio duration and the number of images
    duration_per_image = audio.duration_seconds / len(images)
    
    # Create ImageClip objects for each image
    image_clips = []
    for image in images:
        image_clip = ImageClip(np.array(image)).set_duration(duration_per_image)
        image_clip = image_clip.crossfadein(1)
        image_clip = image_clip.crossfadeout(1)
        image_clips.append(image_clip)
    
    # Create an intro clip
    intro_clip = VideoFileClip("video_generator/assets/media/intro.mp4")
    intro_clip = intro_clip.fadeout(1)
    
    # Concatenate the image clips to create the main video
    video = concatenate_videoclips(image_clips, method="compose")
    video = video.set_audio(audio_clip)
    video = concatenate_videoclips([intro_clip, video], method="compose")
    
    # Print a success message
    print("Successfully created video!")
    
    # Return the created video
    return video


def publish_video(animal, video):
    # Get the title and description for the video
    title = get_title(animal)
    description = get_description(animal, title)
    
    # Upload the video to YouTube and get the video ID
    video_id = upload_video(animal, title, description, video)
    
    # Return the video ID
    return video_id
