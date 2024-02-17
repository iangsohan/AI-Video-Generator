# classifier.py

import json
import webbrowser
import torch
from torchvision import models, transforms

def classify_image(image, expected_animal):
    model = models.resnet152(pretrained=True)
    model.eval()
    f = open("video_generator/assets/labels/labels.json")
    labels = json.load(f)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img_tensor = preprocess(image)
    img_tensor = torch.unsqueeze(img_tensor, 0)
    with torch.no_grad():
        output = model(img_tensor)
    _, predicted_idx = torch.max(output, 1)
    predicted_label = labels[predicted_idx.item()]
    if expected_animal.lower() in predicted_label.lower():
        return True
    print(f"Image classification identified an incorrect value: {predicted_label}")
    return False


def classify_image_manually(image_url):
    webbrowser.open(image_url)
    decision = input("Do you want to continue with this image? (y/n): ")
    if decision.upper() == "Y":
        return True
    return False
