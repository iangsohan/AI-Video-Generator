# thumbnail.py

import io
import time
import requests
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageEnhance, ImageFilter
from video_generator.util.client.youtube import set_thumbnail, list_video_snippet

def curate_thumbnail(animal, video_id):
    thumbnail = create_thumbnail(animal, video_id)
    set_thumbnail(video_id, thumbnail)


def create_thumbnail(animal, video_id):
    thumbnail = get_thumbnail(video_id)
    thumbnail = set_contrast(thumbnail)
    thumbnail = set_sharpness(thumbnail)
    thumbnail = add_text_to_thumbnail(animal, thumbnail)
    thumbnail = add_logo_to_thumbnail(thumbnail)
    print("Successfully created thumbnail!")
    return thumbnail


def get_thumbnail(video_id):
    url = None
    while url is None:
        print("Attempting to retrieve thumbnail...")
        snippet = list_video_snippet(video_id)
        try:
            thumbnails = snippet['thumbnails']
            url = thumbnails.get('maxres', {}).get('url')
        except Exception as e:
            print(f"No thumbnail found, waiting to retry: {e}")
        time.sleep(30)
    response = requests.get(url)
    thumbnail = io.BytesIO(response.content)
    thumbnail = Image.open(thumbnail)
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
