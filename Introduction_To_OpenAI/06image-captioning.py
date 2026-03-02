import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

image_url = "https://assets-prd.ignimgs.com/2022/06/10/netflix-one-piece-1654901410673.jpg"

def generate_caption(image_url):
    resonse = client.chat.completions.create(
        model="gpt-4o",
        messages = [{"role":"user","content":[{"type":"text","text":"What is in this image?"},{"type":"image_url","image_url":{"url":image_url}}]}],
        max_tokens=150
    )
    return resonse.choices[0].message.content

print(generate_caption(image_url))