# youtube.py

import io
import tempfile
from googleapiclient.http import MediaIoBaseUpload, MediaFileUpload
from auth.authorization import get_authenticated_service

# Authenticate with the YouTube API
youtube = get_authenticated_service()

def upload_video(animal, title, description, video):
    # Create a temporary MP4 video file
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        video_file_path = temp_file.name
        video.write_videofile(video_file_path, fps=24)
    
    # Construct the request to upload the video
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": [
                    animal, "animals",
                    "safari", "expedition",
                    "wildlife", "nature",
                    "yt:cc=on"],
                "categoryId": 15
            },
            "status": {
                "privacyStatus": "private",
                "madeForKids": False
            }
        },
        media_body=MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    )
    
    # Execute the request to upload the video
    request.execute()
    
    # Extract the video ID from the response
    _, response = request.next_chunk()
    video_id = response['id']
    
    # Print a success message with the uploaded video ID
    print(f"Video id '{video_id}' was successfully uploaded.")
    
    # Return the uploaded video ID
    return video_id


def insert_captions(video_id, script, language):
    # Extract the language code from the provided language string
    language = language.split('-')[0].strip()
    
    # Construct the request to insert captions
    request = youtube.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "language": language,
                "name": "Subtitle"
            }
        },
        media_body=MediaIoBaseUpload(io.BytesIO(script.encode('utf-8')), mimetype='text/plain')
    )
    
    # Execute the request to insert captions
    request.execute()
    print("Succeeded to publish subtitles!")


def set_thumbnail(video_id, thumbnail):
    # Convert the thumbnail image to bytes
    image_bytes = io.BytesIO()
    thumbnail.save(image_bytes, format='JPEG')
    
    # Construct the request to set the thumbnail
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaIoBaseUpload(image_bytes, mimetype='image/jpeg')
    )
    
    # Execute the request to set the thumbnail
    request.execute()
    
    # Print a success message
    print("Successfully published thumbnail!")


def list_video_snippet(video_id):
    # Construct the request to list video snippet information
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    
    # Execute the request to list video snippet information
    response = request.execute()
    
    # Extract and return the snippet information
    snippet = response['items'][0]['snippet']
    return snippet
