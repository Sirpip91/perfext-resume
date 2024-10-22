from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()


response = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": "List programming languages 1 to 10",
    }],
    model="gpt-3.5-turbo",
)

# Extract the message from the response
latest_message = response.choices[0].message.content

# Print the response content
print(latest_message)
