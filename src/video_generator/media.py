# images.py

import os
from moviepy.editor import VideoFileClip
from PIL import Image
import numpy as np
import tempfile
import re
import requests
from video_generator.util.client.unsplash import query_image
from video_generator.util.classifier import classify_image
from video_generator.util.client.pexels import query_videos

def retrieve_images(animal, image_count=30, width=1280, height=720):
    """
    Retrieve a specified number of images related to a given animal using the Unsplash API.

    Args:
    - animal (str): The name of the animal to query images for.
    - image_count (int): The desired number of images to retrieve.
    - width (int): The width of the images to be retrieved.
    - height (int): The height of the images to be retrieved.

    Returns:
    - list: List of retrieved images.
    """
    images = []
    try:
        while len(images) != image_count:
            image = query_image(animal, width, height)
            
            # Check if the image passes classification criteria
            if classify_image(image, animal):
                image = resize_within_threshold(image)
                if image is not None and image not in images:
                    images.append(image)

    except Exception:
        # Handle exceptions related to Unsplash API requests
        print("No Unsplash API Requests Remaining...")

    # Check if the retrieved image count is sufficient; raise an error if not
    if len(images) < image_count * 3 / 4:
        raise ValueError(f"Will not proceed with only {str(len(images))} images...")

    images = [image.convert('RGB') for image in images]
    print(f"Successfully retrieved {len(images)} images!")
    return images


def resize_within_threshold(image, target_width=1280, target_height=720, aspect_ratio_threshold=0.4):
    """
    Resize an image within specified width, height, and aspect ratio thresholds.

    Args:
    - image (PIL.Image): The image to be resized.
    - target_width (int): The target width for resizing.
    - target_height (int): The target height for resizing.
    - aspect_ratio_threshold (float): The allowed difference in aspect ratio.

    Returns:
    - PIL.Image or None: The resized image if within threshold, None otherwise.
    """
    original_width, original_height = image.size
    original_aspect_ratio = original_width / original_height
    
    # Resize the image to the target dimensions
    resized_image = image.resize((target_width, target_height))
    resized_width, resized_height = resized_image.size
    resized_aspect_ratio = resized_width / resized_height
    
    # Check if the resized image's aspect ratio is within the specified threshold
    if abs(original_aspect_ratio - resized_aspect_ratio) <= aspect_ratio_threshold:
        return resized_image
    else:
        # Return None if the aspect ratio is not within the threshold
        print("Image could not be resized!")
        return None


def retrieve_videos(animal, video_count, min_resolution=(1920, 1080), aspect_ratio_threshold=0.4):
    """
    Query Pexels API for videos based on the provided animal keyword and filter the results based on resolution and aspect ratio.
    
    Args:
        animal (str): The keyword to search for animal-related videos.
        min_resolution (tuple, optional): Minimum resolution required for videos. Defaults to (1920, 1080).
        aspect_ratio_threshold (float, optional): Allowed difference in aspect ratio from 16:9. Defaults to 0.4.
        per_page (int, optional): Number of videos to fetch per page. Defaults to 5.
        page (int, optional): Page number of results to fetch. Defaults to 1.
    
    Returns:
        list: List of filtered VideoClip objects that meet the specified criteria.
    """
    # Set to store unique video IDs
    unique_video_ids = set()
    
    # List to store VideoClip objects of filtered videos
    filtered_videos = []

    while(len(filtered_videos) < video_count - 1):
        videos = query_videos(animal, video_count)
        
        # Iterate over retrieved videos
        for video in videos:
            for file in video['video_files']:
                # Check if video meets minimum resolution criteria
                if file['width'] >= min_resolution[0] and file['height'] >= min_resolution[1]:
                    # Calculate original aspect ratio
                    original_aspect_ratio = file['width'] / file['height']
                    
                    # Check if aspect ratio is within threshold
                    if abs(original_aspect_ratio - 16/9) <= aspect_ratio_threshold:
                        # Extract video ID using regex pattern
                        video_id = re.search(r's=(.*?)&', file['link']).group(1)
                        
                        # Check if video ID already exists
                        if video_id not in unique_video_ids:
                            # Add video ID to set to track uniqueness
                            unique_video_ids.add(video_id)
                            
                            # Download the video
                            video_clip = get_video_from_url(file['link'])
                            
                            # Classify the first frame of the video
                            first_frame = Image.fromarray(np.uint8(video_clip.get_frame(0)))
                            
                            # Check if the video matches the provided animal keyword
                            if classify_image(first_frame, animal):
                                # Resize the video to specified dimensions
                                resized_video = video_clip.resize(width=1280, height=720)
                                
                                # Add resized video to the list of filtered videos
                                trimmed_video = trim_video_clip(resized_video)
                                silent_video = trimmed_video.set_audio(None)
                                filtered_videos.append(silent_video)
        
    # Return list of filtered VideoClip objects
    filtered_videos = filtered_videos[:video_count]
    print(f"Retrieved {len(filtered_videos)} videos!")
    return filtered_videos


def download_video_clips(animal, video_clips):
    """
    Download video clips to local storage.
    
    Args:
        animal (str): Name of the animal being processed.
        video_clips (list): List of VideoClip objects to download.
    """
    # List to store paths of saved video files
    saved_paths = []
    
    # Output folder for saving video files
    output_folder = f"videos/{animal}"
    
    # Iterate over video clips and save them to files
    for i, clip in enumerate(video_clips, start=1):
        output_path = os.path.join(output_folder, f"video_{i}.mp4")
        
        # Write the video clip to a file
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        
        # Add the path of the saved video file to the list
        saved_paths.append(output_path)


def get_video_from_url(video_url):
    """
    Download a video from a URL and create a VideoClip object.
    
    Args:
        video_url (str): URL of the video to download.
    
    Returns:
        moviepy.editor.VideoClip: VideoClip object representing the downloaded video.
    """
    # Create a temporary file to store the downloaded video
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
        
        # Download the video content from the URL and write it to the temporary file
        response = requests.get(video_url)
        temp_file.write(response.content)
    
    # Create a VideoClip object from the temporary file
    video_clip = VideoFileClip(temp_file_path)
    
    return video_clip


def trim_video_clip(video_clip, max_duration=10):
    """
    Trim a VideoClip to the maximum specified duration.

    Args:
        video_clip (moviepy.editor.VideoClip): The VideoClip to be trimmed.
        max_duration (float): Maximum duration in seconds.

    Returns:
        moviepy.editor.VideoClip: Trimmed VideoClip.
    """
    # Get the duration of the original video clip
    duration = video_clip.duration

    # Trim the video clip if its duration exceeds the maximum duration
    if duration > max_duration:
        trimmed_clip = video_clip.subclip(0, max_duration)
    else:
        trimmed_clip = video_clip

    return trimmed_clip