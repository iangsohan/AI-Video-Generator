# images.py

import time
from video_generator.util.client.unsplash import query_image
from video_generator.util.classifier import classify_image

def retrieve_images(animal, image_count=20, width=1280, height=720):
    images = []
    while len(images) != image_count:
        try:
            # Query an image related to the animal from Unsplash API
            image, image_url = query_image(animal, width, height)
            
            # Classify the retrieved image
            if classify_image(image, image_url, animal):
                # Check if the image can be resized within a certain aspect ratio threshold
                if resize_within_threshold(image, width, height):
                    if image not in images:
                        # Append the resized image to the list of images
                        images.append(image.resize((width, height)))
        except Exception as e:
            # Handle exception when no Unsplash API requests are remaining
            print(f"No Unsplash API Requests Remaining: {e}")

            # Sleep until more image queries are available
            time.sleep(1800)
    
    # Convert all images to the RGB color mode
    images = [image.convert('RGB') for image in images]
    
    # Return the list of retrieved images
    print(f"Successfully retrieved {len(images)} images!")
    return images


def resize_within_threshold(image, target_width=1280, target_height=720, aspect_ratio_threshold=0.4):
    # Get the original width and height of the image
    original_width, original_height = image.size
    
    # Calculate the original aspect ratio of the image
    original_aspect_ratio = original_width / original_height
    
    # Calculate the aspect ratio after resizing to the target dimensions
    resized_aspect_ratio = target_width / target_height
    
    # Check if the difference between original and resized aspect ratios is within the threshold
    if abs(original_aspect_ratio - resized_aspect_ratio) <= aspect_ratio_threshold:
        return True
    else:
        print("Image could not be resized!")
        return False
