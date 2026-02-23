import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

prompt = "How can I make money?"

def chat_comp(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "system", "content": "You are a southern belle."}],
        max_tokens=250
    )

    return response.choices[0].message.content
print(chat_comp(prompt))