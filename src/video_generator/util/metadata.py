# metadata.py

from video_generator.util.client.openai import openai_response

def get_title(animal):
    """
    Generate a video title using OpenAI GPT-3.5 Turbo based on a predefined prompt.

    Args:
    - animal (str): The name of the animal for which the title is generated.

    Returns:
    - str: The generated video title.
    """
    # Load the title prompt from the file
    file_path = "video_generator/assets/prompts/title_prompt.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    
    # Replace placeholder with the actual animal name in the prompt
    prompt = prompt.replace('ANIMAL_NAME', animal)
    
    # Generate title using OpenAI GPT-3.5 Turbo
    title = openai_response(prompt)
    
    # Print success message
    print("Successfully generated title!")
    
    # Return the generated video title
    return title


def get_description(animal, title):
    """
    Generate a video description using OpenAI GPT-3.5 Turbo based on a predefined prompt.

    Args:
    - animal (str): The name of the animal associated with the video.
    - title (str): The title of the video.

    Returns:
    - str: The generated video description.
    """
    # Load the description prompt from the file
    file_path = "video_generator/assets/prompts/description_prompt.txt"
    with open(file_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    
    # Replace placeholders with the actual animal name and title in the prompt
    prompt = prompt.replace('ANIMAL_NAME', animal)
    prompt = prompt.replace('TITLE', title)
    
    # Generate description using OpenAI GPT-3.5 Turbo
    description = openai_response(prompt)
    
    # Print success message
    print("Successfully generated description!")
    
    # Return the generated video description
    return description
