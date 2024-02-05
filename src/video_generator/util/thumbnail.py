# thumbnail.py

import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageFilter
import requests
import io
import time
from video_generator.util.client.youtube import set_thumbnail, list_video_snippet

def curate_thumbnail(animal, video_id):
    """
    Curate and set a thumbnail for a YouTube video.

    Args:
    - animal (str): The name of the animal associated with the video.
    - video_id (str): The ID of the video on YouTube.
    """
    # Generate and set the thumbnail for the video
    thumbnail = create_thumbnail(animal, video_id)
    set_thumbnail(video_id, thumbnail)


def create_thumbnail(animal, video_id):
    """
    Create a custom thumbnail for a YouTube video.

    Args:
    - animal (str): The name of the animal associated with the video.
    - video_id (str): The ID of the video on YouTube.

    Returns:
    - PIL.Image: The generated thumbnail.
    """
    # Retrieve the existing thumbnail for the video
    thumbnail = get_thumbnail(video_id)
    
    # Enhance the thumbnail with contrast and sharpness adjustments
    thumbnail = set_contrast(thumbnail)
    thumbnail = set_sharpness(thumbnail)
    
    # Add text and logo overlays to the thumbnail
    thumbnail = add_text_to_thumbnail(animal, thumbnail)
    thumbnail = add_logo_to_thumbnail(thumbnail)
    
    # Print success message
    print("Successfully created thumbnail!")
    
    # Return the generated thumbnail
    return thumbnail


def get_thumbnail(video_id):
    """
    Get the existing thumbnail for a YouTube video.

    Args:
    - video_id (str): The ID of the video on YouTube.

    Returns:
    - PIL.Image: The existing thumbnail.
    """
    url = None
    
    # Retry until a valid thumbnail URL is obtained
    while url is None:
        print("Attempting to retrieve thumbnail...")
        
        # Get video snippet information from YouTube API
        snippet = list_video_snippet(video_id)
        
        try:
            thumbnails = snippet['thumbnails']
            
            # Attempt to get the URL of the 'maxres' thumbnail, else retry
            url = thumbnails.get('maxres', {}).get('url')
        except Exception as e:
            print(f"No thumbnail found, waiting to retry: {e}")
        
        # Wait for 30 seconds before retrying
        time.sleep(30)
    
    # Retrieve the thumbnail image from the obtained URL
    response = requests.get(url)
    thumbnail = io.BytesIO(response.content)
    thumbnail = Image.open(thumbnail)
    
    # Print success message
    print(f"Successfully retrieved thumbnail: {url}")
    
    # Return the existing thumbnail
    return thumbnail


def set_contrast(image, desired_contrast=60):
    """
    Adjust the contrast of an image to the desired level.

    Args:
    - image (PIL.Image): The image to adjust.
    - desired_contrast (float): The desired contrast level.

    Returns:
    - PIL.Image: The image with adjusted contrast.
    """
    # Calculate the current contrast of the image
    current_contrast = np.std(np.array(image))
    
    # Calculate the contrast factor needed to achieve the desired contrast
    contrast_factor = desired_contrast / current_contrast
    
    # Apply contrast adjustment using PIL's ImageEnhance
    enhancer = ImageEnhance.Contrast(image)
    image_with_desired_contrast = enhancer.enhance(contrast_factor)
    
    return image_with_desired_contrast


def set_sharpness(image, desired_sharpness=4000):
    """
    Adjust the sharpness of an image to the desired level.

    Args:
    - image (PIL.Image): The image to adjust.
    - desired_sharpness (float): The desired sharpness level.

    Returns:
    - PIL.Image: The image with adjusted sharpness.
    """
    # Apply detail filter to enhance image details
    image = image.filter(ImageFilter.DETAIL)
    
    # Calculate the current sharpness of the image
    current_sharpness = np.var(np.array(image))
    
    # Calculate the sharpness factor needed to achieve the desired sharpness
    sharpness_factor = desired_sharpness / current_sharpness
    
    # Apply sharpness adjustment using PIL's ImageEnhance
    enhancer = ImageEnhance.Sharpness(image)
    image_with_desired_sharpness = enhancer.enhance(sharpness_factor)
    
    return image_with_desired_sharpness


def add_text_to_thumbnail(animal, thumbnail):
    """
    Add text overlay to a thumbnail.

    Args:
    - animal (str): The text to be added to the thumbnail.
    - thumbnail (PIL.Image): The thumbnail to which text is added.

    Returns:
    - PIL.Image: The thumbnail with added text.
    """
    # Initialize the drawing context and font for text
    draw = ImageDraw.Draw(thumbnail)
    font = ImageFont.truetype("video_generator/assets/fonts/font.ttf", size=150)
    
    # Add text in black and white for a shadow effect
    draw.text((40, 25), animal.upper(), font=font, fill=(0, 0, 0))
    draw.text((30, 15), animal.upper(), font=font, fill=(255, 255, 255))
    
    return thumbnail


def add_logo_to_thumbnail(thumbnail):
    """
    Add a logo overlay to a thumbnail.

    Args:
    - thumbnail (PIL.Image): The thumbnail to which the logo is added.

    Returns:
    - PIL.Image: The thumbnail with added logo.
    """
    # Load the logo image with an alpha channel
    png = Image.open("video_generator/assets/images/logo.png").convert("RGBA")
    
    # Resize the logo to a fixed size
    png = png.resize((150, 150))
    
    # Get the height of the thumbnail and the logo
    _, thumbnail_height = thumbnail.size
    _, png_height = png.size
    
    # Calculate the position to paste the logo on the thumbnail
    position = (25, thumbnail_height - png_height - 25)
    
    # Paste the logo onto the thumbnail with transparency
    thumbnail.paste(png, position, png)
    
    return thumbnail
