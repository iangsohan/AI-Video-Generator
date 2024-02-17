# video.py

import tempfile
import numpy as np
from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips
from video_generator.util.metadata import get_title, get_description
from video_generator.util.thumbnail import curate_thumbnail
from video_generator.util.client.youtube import upload_video, insert_captions
from video_generator.util.client.google import translate

LANGUAGE_CODES = ["en-GB", "hi-IN", "es-ES", "fr-FR", "cmn-CN"]

def curate_video(animal, script, audio, images):
    video = create_video(audio, images)
    video_id = publish_video(animal, video)
    curate_thumbnail(animal, video_id)
    for language in LANGUAGE_CODES:
        translation = translate(animal, script, language)
        insert_captions(video_id, translation, language)


def create_video(audio, images):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        audio.export(temp_file.name, format="wav")
        audio_file_path = temp_file.name
        audio_clip = AudioFileClip(audio_file_path)
    duration_per_image = audio.duration_seconds / len(images)
    image_clips = []
    for image in images:
        image_clip = ImageClip(np.array(image)).set_duration(duration_per_image)
        image_clip = image_clip.crossfadein(1)
        image_clip = image_clip.crossfadeout(1)
        image_clips.append(image_clip)
    intro_clip = VideoFileClip("video_generator/assets/media/intro.mp4")
    intro_clip = intro_clip.fadeout(1)
    video = concatenate_videoclips(image_clips, method="compose")
    video = video.set_audio(audio_clip)
    video = concatenate_videoclips([intro_clip, video], method="compose")
    print("Successfully created video!")
    return video


def publish_video(animal, video):
    title = get_title(animal)
    description = get_description(animal, title)
    video_id = upload_video(animal, title, description, video)
    return video_id
