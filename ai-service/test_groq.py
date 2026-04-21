import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

# Client Initialization
client = Groq(api_key=api_key)

try:
    # API call
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   
        messages=[
            {"role": "user", "content": "Explain phishing attack in 2 lines"}
        ],
    )

    print("API is working!\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("Error:", str(e))