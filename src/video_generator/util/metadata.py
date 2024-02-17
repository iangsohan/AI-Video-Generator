# metadata.py

from video_generator.util.client.openai import openai_response

def get_title(animal):
    file_path = "video_generator/assets/prompts/title_prompt.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    prompt = prompt.replace('ANIMAL_NAME', animal)
    title = openai_response(prompt)
    print("Successfully generated title!")
    return title


def get_description(animal, title):
    file_path = "video_generator/assets/prompts/description_prompt.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    prompt = prompt.replace('ANIMAL_NAME', animal)
    prompt = prompt.replace('TITLE', title)
    description = openai_response(prompt)
    print("Successfully generated description!")
    return description
