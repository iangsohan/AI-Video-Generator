# video.py

import numpy as np
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
from video_generator.util.metadata import get_title, get_description
from video_generator.util.thumbnail import curate_thumbnail
from video_generator.util.client.youtube import upload_video, insert_captions

def curate_video(animal, script, audio, images):
    """
    Curate a video by combining audio, images, and uploading to YouTube.

    Args:
    - animal (str): The name of the animal.
    - script (str): The script content for captions.
    - audio (AudioSegment): The audio for the video.
    - images (list): List of images for the video frames.
    """
    # Create the video
    video = create_video(animal, audio, images)
    
    # Upload the video to YouTube
    video_id = publish_video(animal, video)
    
    # Curate the video thumbnail and insert captions
    curate_thumbnail(animal, video_id)
    insert_captions(video_id, script)


def create_video(animal, audio, images):
    """
    Create a video by combining audio and images.

    Args:
    - animal (str): The name of the animal.
    - audio (AudioSegment): The audio for the video.
    - images (list): List of images for the video frames.

    Returns:
    - VideoClip: The generated video clip.
    """
    # TODO: Handle audio without saving to file.
    # Export audito to MP3 and create AudioFileClip
    audio_file_path = f"videos/{animal}/audio.mp3"
    audio.export(audio_file_path, format="wav")
    audio_clip = AudioFileClip(audio_file_path)

    # Calculate the duration each image should appear in the video
    duration_per_image = audio.duration_seconds / len(images)

    image_clips = []
    for i, image in enumerate(images):
        # Create an ImageClip from the image array and set its duration
        image_clip = ImageClip(np.array(image)).set_duration(duration_per_image)

        # Apply crossfadein to all clips except the first one
        if i != 0:
            image_clip = image_clip.crossfadein(1)

        # Apply crossfadeout to all clips except the last one
        if i != len(images) - 1:
            image_clip = image_clip.crossfadeout(1)
            image_clip.set_duration(duration_per_image + 5)
        image_clips.append(image_clip)

    # Concatenate all image clips into a single video
    video = concatenate_videoclips(image_clips, method="compose")
    video = video.set_audio(audio_clip)

    # Return the generated video
    print("Successfully created video!")
    return video


def publish_video(animal, video):
    """
    Upload a video to YouTube.

    Args:
    - animal (str): The name of the animal.
    - video (VideoClip): The video clip to be uploaded.

    Returns:
    - str: The video ID on YouTube.
    """
    # Get title and description for the video
    title = get_title(animal)
    description = get_description(animal, title)
    
    # Upload the video to YouTube and get the video ID
    video_id = upload_video(animal, title, description, video)
    return video_id
