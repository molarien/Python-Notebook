from openai import OpenAI
import numpy as np


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="OLLAMA_API_KEY"
)

model = "phi3"
prompt = "Should oxford commas always be used?"


response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt}
    ]
)


print(response.choices[0].message.content)