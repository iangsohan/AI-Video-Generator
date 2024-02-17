# script.py

from video_generator.util.client.openai import openai_response

def generate_script(animal, word_count=1000):
    prompt_path = "video_generator/assets/prompts/script_prompt.txt"
    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    prompt = prompt.replace('WORD_COUNT', str(word_count))
    prompt = prompt.replace('ANIMAL_NAME', animal)
    script = openai_response(prompt)
    script = script.encode('utf-8').decode('utf-8')
    print("Successfully generated script!")
    return script
