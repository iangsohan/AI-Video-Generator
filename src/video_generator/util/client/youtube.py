# youtube.py

import io
import tempfile
from googleapiclient.http import MediaIoBaseUpload, MediaFileUpload
from auth.authorization import get_authenticated_service

youtube = get_authenticated_service()

def upload_video(animal, title, description, video):
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
        video_file_path = temp_file.name
        video.write_videofile(video_file_path, fps=24)
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
        media_body=MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    )
    request.execute()
    _, response = request.next_chunk()
    video_id = response['id']
    print(f"Video id '{video_id}' was successfully uploaded.")
    return video_id


def insert_captions(video_id, script, language):
    language = language.split('-')[0].strip()
    request = youtube.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "language": language,
                "name": "Subtitles"
            }
        },
        media_body=MediaIoBaseUpload(io.BytesIO(script.encode('utf-8')), mimetype='text/plain')
    )
    request.execute()
    print("Succeeded to publish subtitles!")


def set_thumbnail(video_id, thumbnail):
    image_bytes = io.BytesIO()
    thumbnail.save(image_bytes, format='JPEG')
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaIoBaseUpload(image_bytes, mimetype='image/jpeg')
    )
    request.execute()
    print("Successfully published thumbnail!")


def list_video_snippet(video_id):
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    snippet = response['items'][0]['snippet']
    return snippet
