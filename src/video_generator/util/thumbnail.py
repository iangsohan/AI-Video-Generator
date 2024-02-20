# thumbnail.py

import io
import time
import requests
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageFilter
from video_generator.util.client.youtube import set_thumbnail, list_video_snippet

def curate_thumbnail(animal, video_id):
    # Create the thumbnail
    thumbnail = create_thumbnail(animal, video_id)
    
    # Set the curated thumbnail for the video on YouTube
    set_thumbnail(video_id, thumbnail)


def create_thumbnail(animal, video_id):
    # Get the initial thumbnail image
    thumbnail = get_thumbnail(video_id)
    
    # Enhance the contrast of the thumbnail
    thumbnail = set_contrast(thumbnail)
    
    # Enhance the sharpness of the thumbnail
    thumbnail = set_sharpness(thumbnail)
    
    # Add text to the thumbnail
    thumbnail = add_text_to_thumbnail(animal, thumbnail)
    
    # Add a logo to the thumbnail
    thumbnail = add_logo_to_thumbnail(thumbnail)
    
    # Return the curated thumbnail
    print("Successfully created thumbnail!")
    return thumbnail


def get_thumbnail(video_id):
    # Loop until a thumbnail URL is retrieved
    url = None
    while url is None:
        # Print a message indicating the attempt to retrieve the thumbnail
        print("Attempting to retrieve thumbnail...")
        
        # Retrieve video snippet information including thumbnails
        snippet = list_video_snippet(video_id)
        
        try:
            # Extract the URL of the maximum resolution thumbnail if available
            thumbnails = snippet['thumbnails']
            url = thumbnails.get('maxres', {}).get('url')
        except Exception as e:
            # Handle exceptions if no thumbnail is found
            print(f"No thumbnail found, waiting to retry: {e}")
        
        # Pause execution for 30 seconds before retrying
        time.sleep(30)
    
    # Send a GET request to retrieve the thumbnail image
    response = requests.get(url)
    
    # Create a BytesIO object containing the content of the response
    thumbnail = io.BytesIO(response.content)
    
    # Open the thumbnail image using PIL's Image module
    thumbnail = Image.open(thumbnail)
    
    # Return the retrieved thumbnail image
    print(f"Successfully retrieved thumbnail: {url}")
    return thumbnail


def set_contrast(image, desired_contrast=60):
    current_contrast = np.std(np.array(image))
    contrast_factor = desired_contrast / current_contrast
    enhancer = ImageEnhance.Contrast(image)
    image_with_desired_contrast = enhancer.enhance(contrast_factor)
    return image_with_desired_contrast


def set_sharpness(image, desired_sharpness=4000):
    image = image.filter(ImageFilter.DETAIL)
    current_sharpness = np.var(np.array(image))
    sharpness_factor = desired_sharpness / current_sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image_with_desired_sharpness = enhancer.enhance(sharpness_factor)
    return image_with_desired_sharpness


def add_text_to_thumbnail(animal, thumbnail):
    text = animal.upper()
    draw = ImageDraw.Draw(thumbnail)
    font = get_sized_font(text, draw)
    draw.text((40, 25), text, font=font, fill=(0, 0, 0))
    draw.text((30, 15), text, font=font, fill=(255, 255, 255))
    return thumbnail


def get_sized_font(text, draw, max_size=150, max_length=850):
    font_size = max_size + 1
    text_length = max_length + 1
    while text_length > max_length and font_size > 0:
        font_size -= 1
        font = ImageFont.truetype("video_generator/assets/fonts/font.ttf", size=font_size)
        text_length = draw.textlength(text, font=font)
    return font


def add_logo_to_thumbnail(thumbnail):
    png = Image.open("video_generator/assets/media/logo.png").convert("RGBA")
    png = png.resize((150, 150))
    _, thumbnail_height = thumbnail.size
    _, png_height = png.size
    position = (25, thumbnail_height - png_height - 25)
    thumbnail.paste(png, position, png)
    return thumbnail
