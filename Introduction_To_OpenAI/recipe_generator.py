"""
====================================================================
AI 食谱生成器示例 / AI Recipe Generator Example
====================================================================

中文说明：
本脚本演示如何使用 OpenAI Chat API 根据用户提供的食材列表
生成创意食谱。流程是：交互式收集食材 → 构建食材请求 → 
调用 Chat API 生成食谱 → 输出。

English Description:
This script demonstrates how to use OpenAI Chat API to generate creative recipes
based on user-provided ingredients. Flow: collect ingredients interactively →
build ingredient request → call Chat API to generate recipe → output.
"""

# ===== 1) 导入依赖 / Import dependencies =====
# 中文：
# - os：环境变量读取
# - load_dotenv：从 .env 文件加载配置
# - OpenAI：OpenAI 官方 Python SDK 客户端
# English:
# - os: environment variable access
# - load_dotenv: load configuration from .env file
# - OpenAI: official OpenAI Python SDK client
import os
from dotenv import load_dotenv
from openai import OpenAI

# ===== 2) 加载环境变量 / Load environment variables =====
# 中文：从 .env 文件读取配置；override=True 允许覆盖系统中同名变量。
# English: Load config from .env; override=True lets .env values override
# existing environment variables.
load_dotenv(override=True)

# ===== 3) 读取 API Key 并初始化客户端 / Read API key and initialize client =====
# 中文：从环境变量获取 OPENAI_API_KEY，避免把密钥硬编码到源码。
# English: Get OPENAI_API_KEY from environment to avoid hardcoding secrets.
api_key = os.getenv("OPENAI_API_KEY")

# 中文：创建 OpenAI 客户端，后续食谱生成请求通过该对象发送。
# English: Create OpenAI client for recipe generation requests.
client = OpenAI(api_key=api_key)

# ===== 4) 交互式收集食材 / Interactively collect ingredients =====
# 中文：
# 使用 while True 循环不断询问用户输入食材。
# 用户输入 'done' 时结束收集，所有食材存储在列表中。
# 这允许用户输入任意数量的食材。
# English:
# Use while True loop to keep asking for ingredients.
# User types 'done' to finish; all ingredients stored in list.
# Allows any number of ingredients.
ingredients = []

while True:
    ingredient = input("Enter an ingredient (or type 'done' to finish): ")
    if ingredient.lower() == 'done':
        break
    ingredients.append(ingredient)


# ===== 5) 定义食谱生成函数 / Define recipe generation function =====
def recipe_generator(ingredients):
    """
    中文：
    根据食材列表生成创意食谱。
    接收食材列表，构建系统和用户消息，调用 Chat API，返回食谱。
    
    English:
    Generate creative recipe from ingredient list.
    Takes ingredient list, builds messages, calls Chat API, returns recipe.
    
    参数 / Args:
        ingredients (list[str]): 食材列表 / List of ingredients
    
    返回 / Returns:
        str: AI 生成的食谱 / AI-generated recipe text
    """
    # 中文：
    # 构建 messages 数组。这里使用最佳实践：
    # - system：定义 AI 身份（高端厨师）和输出要求
    # - user：用户的实际请求（包含所有食材）
    #
    # 注意：不要为每个食材创建单独的 user 消息。
    # 那样会导致冗长的 messages 数组，模型指令也变得分散。
    # 更好的方式是把所有食材合并到一条用户消息中。
    # English:
    # Build messages array using best practice:
    # - system: define AI identity (high-end chef) and output requirements
    # - user: actual request with all ingredients
    #
    # Note: Don't create separate user message for each ingredient.
    # That creates bloated messages, scattered instructions.
    # Better: combine all ingredients into one user message.
    
    messages = [
        {
            "role": "system",
            "content": "You are a high-end chef with expertise in creative cuisine. Generate an elegant, sophisticated recipe using the provided ingredients. Include dish name, step-by-step instructions, cooking time, and serving suggestions. Keep the output concise and professional."
        },
        {
            "role": "user",
            "content": f"Create a creative and delicious recipe using these ingredients: {', '.join(ingredients)}."
        }
    ]

    # 中文：
    # 调用 Chat Completions API：
    # - model="gpt-4o"：使用完整能力模型确保食谱创意和质量
    # - temperature=0.9：温度较高。食谱生成需要创意和风格化，不能太平板
    # - max_tokens=300：足够生成详细的食谱（名称、步骤、时间等）
    # English:
    # Call Chat Completions API:
    # - model="gpt-4o": full-capability for creative, quality recipes
    # - temperature=0.9: high enough for creativity (not bland)
    # - max_tokens=300: sufficient for detailed recipe (name, steps, timing)
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=300,
        temperature=0.9,
        messages=messages,
    )

    # 中文：提取并返回 AI 生成的食谱文本
    # English: Extract and return AI-generated recipe text
    return response.choices[0].message.content


# ===== 6) 执行食谱生成并输出结果 / Execute recipe generation and print result =====
# 中文：
# 调用 recipe_generator 函数，传入收集的食材列表，
# 获取 AI 生成的食谱，打印到控制台。
# English:
# Call recipe_generator() with collected ingredient list,
# get AI-generated recipe, print to console.
print(recipe_generator(ingredients))