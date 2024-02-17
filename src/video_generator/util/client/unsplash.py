# unsplash.py

import io
import requests
from PIL import Image
from config import UNSPLASH_API_KEY

def query_image(animal, width, height):
    url = f'https://api.unsplash.com/photos/random?query={animal}&client_id={UNSPLASH_API_KEY}&w={width}&h={height}&orientation=landscape'
    response = requests.get(url)
    data = response.json()
    image_url = data["urls"]["full"]
    image = Image.open(io.BytesIO(requests.get(image_url).content))
    return image, image_url
