import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def ask_chatgpt(query):
    """
    Sends a query to ChatGPT and returns the response.
    Returns None if there is an error.
    """
    if not client:
        print("ChatGPT Error: API key missing.")
        return None

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are J.A.R.V.I.S., the AI assistant from Iron Man. You are sophisticated, polite, and slightly witty. Always address the user as 'Sir'. Keep your answers concise."},
                {"role": "user", "content": query}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"ChatGPT Error: {e}")
        return None
