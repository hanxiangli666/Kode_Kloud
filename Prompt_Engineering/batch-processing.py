import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

prompts = [
    "What is the capital of France?",
    "What is the largest mammal?",
    "What is the square root of 16?",
    "Who is the president of the United States?"]


def process_prompts(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "system", "content": "You are a helpful assistant."}],
        max_tokens=100,
        temperature=0.7
    )

    return response.choices[0].message.content

results = []

for prompt in prompts:
    result = process_prompts(prompt)
    results.append(result)

for i, result in enumerate(results):
    print(f"Prompt {i+1}: {prompts}")
    print(f"Response {i+1}: {result}\n")