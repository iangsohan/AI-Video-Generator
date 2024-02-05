# google.py

import requests
import html
from config import GOOGLE_API_KEY

# Supported language codes for translation
LANGUAGE_CODES = ["es-ES", "hi-IN", "fr-FR", "cmn-CN"]

def translate(script, language):
    """
    Translate a given script to the specified language using the Google Translation API.

    Args:
    - script (str): The text script to be translated.
    - language (str): The target language code.

    Returns:
    - str: The translated script.
    """
    # API endpoint for translation
    url = "https://translation.googleapis.com/language/translate/v2"
    
    # Set parameters for the translation request
    params = {
        "key": GOOGLE_API_KEY,
        "q": script,
        "source": "en",
        "target": language.split('-')[0].strip(),
    }
    
    # Make a POST request to the Google Translation API
    response = requests.post(url, params=params)
    response.raise_for_status()
    
    # Extract the translation data from the response
    translation_data = response.json()
    script = translation_data["data"]["translations"][0]["translatedText"]
    
    # Unescape HTML entities in the translated script
    translation = html.unescape(script)
    
    # Print a success message
    print(f"Successfully translated script to {language}!")
    
    # Return the translated script
    return translation


def synthesize_text(text):
    """
    Synthesize text into audio using the Google Text-to-Speech API.

    Args:
    - text (str): The text to be synthesized.

    Returns:
    - str: The synthesized audio content.
    """
    # API endpoint for text synthesis
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"
    
    # Set data parameters for the synthesis request
    data = {
        "input": {"text": text},
        "voice": {"languageCode": "en-GB", "name": "en-GB-Wavenet-B"},
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "speakingRate": 0.8,
            "volumeGainDb": -1,
            "pitch": 2
        },
    }
    
    # Set parameters for the API key
    params = {"key": GOOGLE_API_KEY}
    
    # Make a POST request to the Google Text-to-Speech API
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    
    # Extract the synthesized audio content from the response
    synthesized_text = response.json()["audioContent"]
    
    # Return the synthesized audio content
    return synthesized_text
