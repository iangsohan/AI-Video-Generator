# images.py

from video_generator.util.client.unsplash import query_image
from video_generator.util.classifier import classify_image_manually

def retrieve_images(animal, image_count=50, width=1280, height=720):
    images = []
    try:
        while len(images) != image_count:
            image, image_url = query_image(animal, width, height)
            image = resize_within_threshold(image)
            if classify_image_manually(image_url):
                if image is not None and image not in images:
                    images.append(image)
    except Exception:
        print("No Unsplash API Requests Remaining...")
    images = [image.convert('RGB') for image in images]
    print(f"Successfully retrieved {len(images)} images!")
    return images


def resize_within_threshold(image, target_width=1280, target_height=720, aspect_ratio_threshold=0.4):
    original_width, original_height = image.size
    original_aspect_ratio = original_width / original_height
    resized_image = image.resize((target_width, target_height))
    resized_width, resized_height = resized_image.size
    resized_aspect_ratio = resized_width / resized_height
    if abs(original_aspect_ratio - resized_aspect_ratio) <= aspect_ratio_threshold:
        return resized_image
    else:
        print("Image could not be resized!")
        return None
