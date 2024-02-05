# openai.py

import openai
from config import OPENAI_API_KEY

def openai_response(prompt):
    """
    Get a response from the OpenAI GPT-3.5 Turbo model based on the provided prompt.

    Args:
    - prompt (str): The user's prompt for generating a response.

    Returns:
    - str: The generated response content from the OpenAI model.
    """
    # Create an OpenAI client instance using the provided API key
    ai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    # Construct a chat completion request with system and user messages
    response = ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the generated response content from the API response
    response_content = response.choices[0].message.content
    
    # Return the generated response content
    return response_content
