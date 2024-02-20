# google.py

import html
import requests
from config import GOOGLE_API_KEY

def translate(animal, script, language="en-GB"):
    # Define the source language as English
    source = "en"
    
    # Extract the target language code from the provided language string
    target = language.split('-')[0].strip()
    
    # If the target language is the same as the source language, return the original script
    if target == source:
        return script
    
    # Construct the URL for the translation API
    url = "https://translation.googleapis.com/language/translate/v2"
    
    # Set parameters for the translation request
    params = {
        "key": GOOGLE_API_KEY,
        "q": script,
        "source": source,
        "target": target,
        "contentType": "text"
    }
    
    # Send a POST request to the translation API
    response = requests.post(url, params=params)
    
    # Raise an exception for HTTP errors
    response.raise_for_status()
    
    # Parse the JSON response
    translation_data = response.json()
    
    # Extract the translated text from the response data
    script = translation_data["data"]["translations"][0]["translatedText"]
    
    # Unescape HTML entities in the translated text
    translation = html.unescape(script)
    
    # Return the translated text
    print(f"Successfully translated script to {language}!")
    return translation


def synthesize_text(text, language="en-GB"):
    # Define the URL for the Text-to-Speech API
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    
    # Define the data payload for the API request
    data = {
        "input": {"text": text},
        "voice": {"languageCode": language, "name": f"{language}-Wavenet-B"},
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "speakingRate": 0.9,
            "volumeGainDb": -1,
            "pitch": 2
        },
    }
    
    # Set parameters for the API request
    params = {"key": GOOGLE_API_KEY}
    
    # Send a POST request to the Text-to-Speech API
    response = requests.post(url, params=params, json=data)
    
    # Raise an exception for HTTP errors
    response.raise_for_status()
    
    # Parse the JSON response and extract the audio content
    synthesized_text = response.json()["audioContent"]
    
    # Return the synthesized audio content
    return synthesized_text
