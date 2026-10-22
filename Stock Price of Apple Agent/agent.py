from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model = "openai/gpt-oss-120b",
    messages=[
        {
            "role":"user",
            "content":"What is Apple's stock ticker and current price?"
        },        
    ]
)

msg = response.choices[0].message.content
print(msg)