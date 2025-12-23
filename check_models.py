from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("No API Key found in .env")
    exit()

try:
    print("Initializing Client...")
    client = genai.Client(api_key=api_key)
    
    print("Testing connection with 'gemini-2.5-flash'...")
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents='Hello, are you there?'
    )
    print("Success! Response from Gemini:")
    print(response.text)

except Exception as e:
    print(f"Error: {e}")
