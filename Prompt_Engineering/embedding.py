import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.embeddings.create(
    input="The quick brown fox jumps over the lazy dog",
    model="text-embedding-3-large",
)

print(response.data[0].embedding)
