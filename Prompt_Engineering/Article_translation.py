import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

#article

article = "I and my friend went to the park yesterday. We had a great time playing soccer and enjoying the sunshine. The weather was perfect, and we even had a picnic with sandwiches and lemonade. It was a wonderful day spent outdoors."

#prompt

prompt = f"Translate the following article: {article}"

#create a function that can translate the article

def article_translation(prompt):

    messages = [
        {"role": "system", "content": "direct, Chinese translation"},
        {"role": "assistant", "content": "you are a professional translator. Translate the following article into Chinese."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages= messages,
    )

    return response.choices[0].message.content
print(article_translation(prompt))
