# google.py

import html
import requests
from config import GOOGLE_API_KEY

def translate(animal, script, language="en-GB"):
    source = "en"
    target = language.split('-')[0].strip()
    if target == source:
        return script
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "key": GOOGLE_API_KEY,
        "q": script,
        "source": source,
        "target": target,
        "contentType": "text"
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    translation_data = response.json()
    script = translation_data["data"]["translations"][0]["translatedText"]
    translation = html.unescape(script)
    translation = translation.encode('utf-8').decode('utf-8')
    print(f"Successfully translated script to {language}!")
    return translation


def synthesize_text(text, language="en-GB"):
    url = "https://texttospeech.googleapis.com/v1/text:synthesize"
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
    params = {"key": GOOGLE_API_KEY}
    response = requests.post(url, params=params, json=data)
    response.raise_for_status()
    synthesized_text = response.json()["audioContent"]
    return synthesized_text
