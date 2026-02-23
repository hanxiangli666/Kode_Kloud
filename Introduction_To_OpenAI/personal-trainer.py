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


# find a way to read the csv file and use the data to generate a report on the factors that affect sleep health
df = pd.read_csv("Prompt_Engineering\Sleep_health_and_lifestyle_dataset.csv")

goals = []

while True:
    goal = input("What are your fitness goals? (e.g., weight loss, muscle gain, improved endurance) (type 'done' to finish): ")
    if goal.lower() == 'done':
        break

    goals.append(goal)

def trainer(df, goals):
    messages = []
    messages.append({"role": "user", "content": f"Create a workout plan to achieve the goal of {goals}."})

    messages.extend([        
        {"role": "system", "content": "direct, point"},
        {"role": "assistant", "content": f"you are a personal trainer. The person you are responding to is an athelete. Be specific to their role as an athelete. Reference this data {df} in your response. Generate a workout plan based on the following goals: {goals}."}])
    response = client.chat.completions.create(
        model="gpt-4o",
        messages= messages,
        max_tokens=500,
        temperature=0.8,
    )

    return response.choices[0].message.content

print(trainer(df, goals))