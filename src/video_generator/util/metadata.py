# metadata.py

from video_generator.util.client.openai import openai_response

def get_title(animal):
    # Define the file path for the title prompt text file
    file_path = "video_generator/assets/prompts/title_prompt.txt"
    
    # Read the content of the title prompt text file
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    
    # Replace the placeholder 'ANIMAL_NAME' with the provided animal
    prompt = prompt.replace('ANIMAL_NAME', animal)
    
    # Generate the title using OpenAI's API based on the modified prompt
    title = openai_response(prompt)
    
    # Return the generated title
    print("Successfully generated title!")
    return title


def get_description(animal, title):
    # Define the file path for the description prompt text file
    file_path = "video_generator/assets/prompts/description_prompt.txt"
    
    # Read the content of the description prompt text file
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    
    # Replace the placeholders 'ANIMAL_NAME' and 'TITLE' with the provided animal and title, respectively
    prompt = prompt.replace('ANIMAL_NAME', animal)
    prompt = prompt.replace('TITLE', title)
    
    # Generate the description using OpenAI's API based on the modified prompt
    description = openai_response(prompt)
    
    # Return the generated description
    print("Successfully generated description!")
    return description
