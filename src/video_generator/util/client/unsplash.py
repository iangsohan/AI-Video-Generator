# unsplash.py

import io
import requests
from PIL import Image
from config import UNSPLASH_API_KEY

def query_image(animal, width, height):
    # Construct the URL for querying a random image with the specified parameters
    url = f'https://api.unsplash.com/photos/random?query={animal}&client_id={UNSPLASH_API_KEY}&w={width}&h={height}&orientation=landscape'
    
    # Send a GET request to the Unsplash API
    response = requests.get(url)
    
    # Parse the JSON response
    data = response.json()
    
    # Extract the URL of the full-size image from the response data
    image_url = data["urls"]["full"]
    
    # Open the image from its URL and convert it to a PIL Image object
    image = Image.open(io.BytesIO(requests.get(image_url).content))
    
    # Return the PIL Image object
    return image
