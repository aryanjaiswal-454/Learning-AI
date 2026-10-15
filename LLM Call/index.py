import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(r"D:\GenAI\.env")
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    messages=[
        {
            "role":"user",
            # role can u
            "content":"Explain the importance of fast language models",
        }
    ],
    model="openai/gpt-oss-120b",
)

print(response.choices[0].message.content)

# echo $GROQ_API_KEY