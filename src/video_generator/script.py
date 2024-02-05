# script.py

from video_generator.util.client.openai import openai_response

def generate_script(animal, word_count=1000):
    """
    Generate a script using OpenAI API based on a prompt.

    Args:
    - animal (str): The name of the animal for which the script is generated.
    - word_count (int): The desired word count for the script.

    Returns:
    - str: The generated script.
    """
    # Path to the script prompt file
    prompt_path = "video_generator/assets/prompts/script_prompt.txt"

    # Read the script prompt from the file
    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompt = file.read()

    # Replace placeholders in the prompt with actual values
    prompt = prompt.replace('WORD_COUNT', str(word_count))
    prompt = prompt.replace('ANIMAL_NAME', animal)

    # Generate script using OpenAI API
    script = openai_response(prompt)

    # Transcribe the script to a text file
    transcribe(animal, script)

    print("Successfully generated script!")
    return script


def transcribe(animal, script, language="en-GB"):
    """
    Transcribe the generated script to a text file.

    Args:
    - animal (str): The name of the animal.
    - script (str): The script content.
    - language (str): The language code for transcription (default is "en-GB").
    """
    # Encode and decode the script to handle Unicode characters
    script = script.encode('utf-8').decode('utf-8')

    # Save the transcribed script to a text file
    with open(f"videos/{animal}/script-{language}.txt", 'w', encoding='utf-8') as file:
        file.write(script)
