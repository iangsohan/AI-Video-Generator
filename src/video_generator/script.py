# script.py

from video_generator.util.client.openai import openai_response

def generate_script(animal, word_count=750):
    # Path to the file containing the script prompt
    prompt_path = "video_generator/assets/prompts/script_prompt.txt"
    
    # Open the script prompt file and read its content
    with open(prompt_path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    
    # Replace placeholders in the script prompt with actual values
    prompt = prompt.replace('WORD_COUNT', str(word_count))
    prompt = prompt.replace('ANIMAL_NAME', animal)
    
    # Generate a script using OpenAI's API based on the modified prompt
    script = openai_response(prompt)
    
    # Decode the script from bytes to UTF-8 string format
    script = script.encode('utf-8').decode('utf-8')
    
    # Return the generated script
    print("Successfully generated script!")
    return script
