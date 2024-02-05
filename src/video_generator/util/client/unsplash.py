# unsplash.py

import io
import requests
from PIL import Image
from config import UNSPLASH_API_KEY

def query_image(animal, width, height):
    """
    Query an image related to a specified animal from Unsplash using the Unsplash API.

    Args:
    - animal (str): The name of the animal for image query.
    - width (int): The desired width of the image.
    - height (int): The desired height of the image.

    Returns:
    - PIL.Image: The queried image in PIL Image format.
    """
    # Construct the URL for querying a random image related to the specified animal
    url = f'https://api.unsplash.com/photos/random?query={animal}&client_id={UNSPLASH_API_KEY}&w={width}&h={height}&orientation=landscape'
    
    # Make a GET request to the Unsplash API
    response = requests.get(url)
    
    # Parse the JSON data from the response
    data = response.json()
    
    # Extract the URL of the full-sized image from the Unsplash API response
    image_url = data["urls"]["full"]
    print(image_url)
    
    # Open the image from the URL using PIL
    image = Image.open(io.BytesIO(requests.get(image_url).content))
    
    # Return the queried image in PIL Image format
    return image
