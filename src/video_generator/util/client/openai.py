# openai.py

import openai
from config import OPENAI_API_KEY

def openai_response(prompt):
    ai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    response_content = response.choices[0].message.content
    return response_content
