import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client pointing to local Ollama server
# We don't need a real API key for local AI, but the client requires a string.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama" 
)

def ask_chatgpt(query):
    """
    Sends a query to the local AI (Ollama) and returns the response.
    Returns None if there is an error.
    """
    if not client:
        print("AI Error: Client not initialized.")
        return None

    try:
        response = client.chat.completions.create(
            model="llama3",  # Using the local model we downloaded
            messages=[
                {"role": "system", "content": "You are J.A.R.V.I.S., the AI assistant from Iron Man. You are sophisticated, polite, and slightly witty. Always address the user as 'Sir'. Keep your answers concise."},
                {"role": "user", "content": query}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Local AI Error: {e}")
        return None