import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def generate_image():
    response = client.images.generate(
        model="dall-e-3",
        prompt= "Lebron James dunking a basketball in the style of Picasso",
        size="1024x1024"
    )
    return response.data[0].url

image_url = generate_image()
print(f"Generated image URL: {image_url}")