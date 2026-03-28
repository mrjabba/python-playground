#import requests
from openai import OpenAI

"""
Small practice script to use with Docker's new Model Runner
"""
# hit our docker model instance
BASE_URL = "http://localhost:12434/engines/llama.cpp/v1"

client = OpenAI(base_url=BASE_URL, api_key="whatever")

MODEL_NAME = "ai/smollm3:latest"
PROMPT = "Write a short poem about Typescript programming."

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": PROMPT}    
]

responses = client.chat.completions.create(
    model=MODEL_NAME,
    messages=messages
)

print(responses.choices[0].message.content)

print('Done!!!!')
