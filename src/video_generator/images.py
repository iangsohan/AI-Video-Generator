# images.py

import requests
import torch
from video_generator.util.client.unsplash import query_image
from torchvision import models, transforms

def retrieve_images(animal, image_count=30, width=1280, height=720):
    """
    Retrieve a specified number of images related to a given animal using the Unsplash API.

    Args:
    - animal (str): The name of the animal to query images for.
    - image_count (int): The desired number of images to retrieve.
    - width (int): The width of the images to be retrieved.
    - height (int): The height of the images to be retrieved.

    Returns:
    - list: List of retrieved images.
    """
    images = []
    try:
        while len(images) != image_count:
            image = query_image(animal, width, height)
            
            # Check if the image passes classification criteria
            if classify_image(image, animal):
                image = resize_within_threshold(image)
                if image is not None and image not in images:
                    images.append(image)

    except Exception:
        # Handle exceptions related to Unsplash API requests
        print("No Unsplash API Requests Remaining...")

    # Check if the retrieved image count is sufficient; raise an error if not
    if len(images) < image_count * 2 / 3:
        raise ValueError(f"Will not proceed with only {str(len(images))} images...")

    images = [image.convert('RGB') for image in images]
    print(f"Successfully retrieved {len(images)} images!")
    return images


def classify_image(image, expected_animal):
    """
    Classify an image using a pre-trained ResNet50 model.

    Args:
    - image (PIL.Image): The image to be classified.
    - expected_animal (str): The expected animal name.

    Returns:
    - bool: True if the image is classified as the expected animal, False otherwise.
    """
    # Load the ResNet50 model and set it to evaluation mode
    model = models.resnet50(pretrained=True)
    model.eval()

    # Define image preprocessing transformations
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Apply the transformations to the image
    img_tensor = preprocess(image)
    img_tensor = torch.unsqueeze(img_tensor, 0)

    # Make a forward pass through the model
    with torch.no_grad():
        output = model(img_tensor)

    # Fetch the labels for the model's predictions
    labels_url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    labels = requests.get(labels_url).json()

    # Retrieve the predicted label for the image
    _, predicted_idx = torch.max(output, 1)
    predicted_label = labels[predicted_idx.item()]

    # Check if the predicted label contains the expected animal name
    if expected_animal.lower() in predicted_label.lower():
        return True

    # Print a message if the image is misclassified
    print(f"Image classification identified an incorrect value: {predicted_label}")
    return False


def resize_within_threshold(image, target_width=1280, target_height=720, aspect_ratio_threshold=0.4):
    """
    Resize an image within specified width, height, and aspect ratio thresholds.

    Args:
    - image (PIL.Image): The image to be resized.
    - target_width (int): The target width for resizing.
    - target_height (int): The target height for resizing.
    - aspect_ratio_threshold (float): The allowed difference in aspect ratio.

    Returns:
    - PIL.Image or None: The resized image if within threshold, None otherwise.
    """
    original_width, original_height = image.size
    original_aspect_ratio = original_width / original_height
    
    # Resize the image to the target dimensions
    resized_image = image.resize((target_width, target_height))
    resized_width, resized_height = resized_image.size
    resized_aspect_ratio = resized_width / resized_height
    
    # Check if the resized image's aspect ratio is within the specified threshold
    if abs(original_aspect_ratio - resized_aspect_ratio) <= aspect_ratio_threshold:
        return resized_image
    else:
        # Return None if the aspect ratio is not within the threshold
        print("Image could not be resized!")
        return None
