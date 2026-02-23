import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


# find a way to read the csv file and use the data to generate a report on the factors that affect student performance
df = pd.read_csv("Prompt_Engineering\StudentPerformanceFactors.csv")

# create a function that can generate a report based on the data in the csv file

def analyze_data(df):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"You are a resaearch assistant. Provide key insights from {df} in point form."}],
        max_tokens=500,
        temperature=0.2,
    )
    return response.choices[0].message.content

print(analyze_data(df))

