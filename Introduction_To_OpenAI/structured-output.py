import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

#create sth that can accept ingredients

ingredients = []

while True:
    ingredient = input("Enter an ingredient (or type 'done' to finish): ")
    if ingredient.lower() == 'done':
        break
    ingredients.append(ingredient)

# create a function that can generate a recipe based on the ingredients
def recipe_generator(ingredients):

    messages = []
    for ingredient in ingredients:
        messages.append({"role": "user", "content": f"Include {ingredient} in the recipe."})
    

    messages.extend([        
        {"role": "system", "content": "JSON Format"},
        {"role": "assistant", "content": "you are a high-end chef. Generate a recipe baded on the following ingredients. Must be exported in JSON format with the following keys: 'title', 'ingredients', 'instructions'."}]

    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=300,
        temperature=0.9,
        messages= messages,
    )

    return response.choices[0].message.content
print(recipe_generator(ingredients))