# classifier.py

import json
import torch
from torchvision import models, transforms

def classify_image(image, expected_animal):
    # Open the labels JSON file and load the labels
    with open("video_generator/assets/labels/labels.json") as f:
        labels = json.load(f)
    
    # Check if the expected animal is present in the loaded labels
    return auto_image_classifier(image, labels, expected_animal)


def auto_image_classifier(image, labels, expected_animal):
    # Load the pretrained ResNet-152 model
    model = models.resnet152(pretrained=True)
    
    # Set the model to evaluation mode
    model.eval()
    
    # Define image preprocessing transformations
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
    # Preprocess the image
    img_tensor = preprocess(image)
    img_tensor = torch.unsqueeze(img_tensor, 0)
    
    # Perform inference using the model
    with torch.no_grad():
        output = model(img_tensor)
    
    # Get the index of the predicted class
    _, predicted_idx = torch.max(output, 1)
    
    # Get the predicted label corresponding to the predicted index
    predicted_label = labels[predicted_idx.item()]
    
    # Check if the predicted label contains the expected animal
    if expected_animal.lower() in predicted_label.lower():
        return True
    else:
        # Print a message if the image classification identifies an incorrect value
        print(f"Image classification identified an incorrect value: {predicted_label}")
        return False
