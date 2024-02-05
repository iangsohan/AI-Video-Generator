# config.py
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Access the API keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')
