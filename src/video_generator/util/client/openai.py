# openai.py

import openai
from config import OPENAI_API_KEY

def openai_response(prompt):
    # Create an OpenAI client with the provided API key
    ai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    # Send the prompt to the chat completion endpoint of the GPT-3.5-turbo model
    response = ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the content of the response message
    response_content = response.choices[0].message.content
    
    # Return the response content
    return response_content
