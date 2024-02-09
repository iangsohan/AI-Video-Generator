# pexels.py

import requests
from config import PEXELS_API_KEY

def query_videos(animal, video_count):
    # Construct the API URL for fetching videos
    url = f"https://api.pexels.com/videos/search?query={animal}&per_page={video_count}&page=1"
    
    # Set authorization headers
    headers = {
        "Authorization": PEXELS_API_KEY,
    }
    
    # Send GET request to Pexels API
    response = requests.get(url, headers=headers)
    
    # Parse JSON response to extract video data
    videos = response.json()['videos']

    return videos