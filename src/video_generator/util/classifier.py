# classifier.py

import json
import torch
from torchvision import models, transforms

def classify_image(image, expected_animal):
    """
    Classify an image using a pre-trained ResNet50 model.

    Args:
    - image (PIL.Image): The image to be classified.
    - expected_animal (str): The expected animal name.

    Returns:
    - bool: True if the image is classified as the expected animal, False otherwise.
    """
    # weights=ResNet50_Weights.DEFAULT
    model = models.resnet152(pretrained=True)
    model.eval()
    # https://storage.googleapis.com/openimages/v6/oidv6-class-descriptions.csv
    f = open("video_generator/assets/labels/labels.json")
    labels = json.load(f)

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

    # Retrieve the predicted label for the image
    _, predicted_idx = torch.max(output, 1)
    predicted_label = labels[predicted_idx.item()]

    # Check if the predicted label contains the expected animal name
    if expected_animal.lower() in predicted_label.lower():
        return True

    # Print a message if the image is misclassified
    print(f"Image classification identified an incorrect value: {predicted_label}")
    return False