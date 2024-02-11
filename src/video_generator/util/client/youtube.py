# youtube.py

import io
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.http import MediaFileUpload
from auth.authorization import get_authenticated_service

# Build YouTube API client using OAuth 2.0 credentials
youtube = get_authenticated_service()

def upload_video(animal, title, description, video):
    """
    Upload a video to YouTube.

    Args:
    - animal (str): The name of the animal associated with the video.
    - title (str): The title of the video.
    - description (str): The description of the video.
    - video (VideoClip): The video clip to be uploaded.

    Returns:
    - str: The uploaded video's ID on YouTube.
    """
    # TODO: Handle video without saving to file.
    # Write video to an MP4 file
    video_path = f"videos/{animal}/video.mp4"
    video.write_videofile(video_path, fps=24)

    # Construct the request for uploading the video to YouTube
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["animals", "safari", animal, "expedition", "yt:cc=on"],
                "categoryId": 15
            },
            "status": {
                "privacyStatus": "public",
                "madeForKids": False
            }
        },
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )

    # Execute the request and get the response
    request.execute()
    _, response = request.next_chunk()
    video_id = response['id']
    
    # Print success message
    print(f"Video id '{video_id}' was successfully uploaded.")
    
    # Return the uploaded video's ID on YouTube
    return video_id


def insert_captions(video_id, script, language):
    """
    Insert captions (subtitles) for a video on YouTube.

    Args:
    - video_id (str): The ID of the video on YouTube.
    - script (str): The script content for captions.
    """
    language = language.split('-')[0].strip()

    # Construct the request for inserting captions
    request = youtube.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "language": language,
                "name": "Subtitles"
            }
        },
        media_body=MediaIoBaseUpload(io.BytesIO(script.encode('utf-8')), mimetype='text')
    )
    
    # Execute the request
    request.execute()
    
    # Print success message
    print("Succeeded to publish subtitles!")


def set_thumbnail(video_id, thumbnail):
    """
    Set a thumbnail for a video on YouTube.

    Args:
    - video_id (str): The ID of the video on YouTube.
    - thumbnail (PIL.Image): The thumbnail image.
    """
    # Convert the thumbnail image to bytes
    image_bytes = io.BytesIO()
    thumbnail.save(image_bytes, format='JPEG')
    
    # Construct the request for setting the thumbnail
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaIoBaseUpload(image_bytes, mimetype='image/jpeg')
    )
    
    # Execute the request
    request.execute()
    
    # Print success message
    print("Successfully published thumbnail!")


def list_video_snippet(video_id):
    """
    List the snippet information for a video on YouTube.

    Args:
    - video_id (str): The ID of the video on YouTube.

    Returns:
    - dict: The snippet information for the video.
    """
    # Construct the request for listing video snippet information
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    
    # Execute the request and get the response
    response = request.execute()
    snippet = response['items'][0]['snippet']
    
    # Return the snippet information for the video
    return snippet
