"""
====================================================================
结构化输出食谱生成器 / Structured-Output Recipe Generator
====================================================================

中文说明：
本脚本演示如何通过命令行收集用户输入的食材，并调用 OpenAI Chat Completions
生成结构化（JSON 风格）食谱文本输出。

English Description:
This script demonstrates how to collect ingredients from CLI input and call
OpenAI Chat Completions to generate a structured (JSON-style) recipe output.
"""

# ===== 1) 导入依赖 / Import dependencies =====
# 中文：
# - os：读取环境变量（例如 OPENAI_API_KEY）
# - load_dotenv：从 .env 文件加载配置
# - OpenAI：OpenAI 官方 Python SDK 客户端类
# English:
# - os: reads environment variables (e.g., OPENAI_API_KEY)
# - load_dotenv: loads configuration from .env
# - OpenAI: official OpenAI Python SDK client class
import os
from dotenv import load_dotenv
from openai import OpenAI

# ===== 2) 加载环境变量 / Load environment variables =====
# 中文：
# load_dotenv(override=True) 会读取 .env，并允许其值覆盖系统中同名变量。
# English:
# load_dotenv(override=True) reads .env and allows its values to override
# existing variables with the same names.
load_dotenv(override=True)

# ===== 3) 读取 API Key 并初始化客户端 / Read API key and initialize client =====
# 中文：从环境变量获取密钥，避免在代码中硬编码敏感信息。
# English: Retrieves API key from environment variables to avoid hardcoding secrets.
api_key = os.getenv("OPENAI_API_KEY")

# 中文：创建 OpenAI 客户端对象，后续 API 请求都通过它发送。
# English: Creates an OpenAI client object used for all subsequent API requests.
client = OpenAI(api_key=api_key)

# ===== 4) 采集食材输入 / Collect ingredient inputs =====
# 中文：
# 使用列表保存用户输入的所有食材。
# 通过 while True 循环不断接收输入；当输入 done 时结束。
# English:
# Uses a list to store all user-entered ingredients.
# The while True loop keeps accepting inputs; entering 'done' stops the loop.
ingredients = []

while True:
    ingredient = input("Enter an ingredient (or type 'done' to finish): ")
    if ingredient.lower() == 'done':
        break
    ingredients.append(ingredient)


# ===== 5) 定义食谱生成函数 / Define recipe generation function =====
# 中文：根据用户输入食材构造消息列表，并请求模型返回食谱内容。
# English: Builds a message list from user ingredients and requests recipe output from the model.
def recipe_generator(ingredients):
    """
    中文：
    基于食材列表生成食谱文本（目标是 JSON 风格结构化输出）。

    English:
    Generates recipe text from an ingredient list (targeting JSON-style structured output).

    参数 / Args:
        ingredients (list[str]): 食材列表 / List of ingredients

    返回 / Returns:
        str: 模型返回的文本 / Model returned text
    """

    # 中文：初始化消息容器；后续逐步填充对话上下文。
    # English: Initializes a messages container to build conversation context.
    messages = []

    # 中文：把每个食材转换为一条用户消息，要求模型“包含该食材”。
    # English: Converts each ingredient into a user message requesting inclusion in the recipe.
    for ingredient in ingredients:
        messages.append({"role": "user", "content": f"Include {ingredient} in the recipe."})

    # 中文：追加系统/助手消息，强调输出格式和任务角色。
    # English: Appends system/assistant messages to emphasize output format and role instruction.
    messages.extend([
        {"role": "system", "content": "JSON Format"},
        {"role": "assistant", "content": "you are a high-end chef. Generate a recipe baded on the following ingredients. Must be exported in JSON format with the following keys: 'title', 'ingredients', 'instructions'."}
    ])

    # 中文：调用 Chat Completions API，设置模型、输出长度和随机性参数。
    # English: Calls Chat Completions API with model, output length, and randomness settings.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=300,
        temperature=0.9,
        messages=messages,
    )

    # 中文：提取第一条候选结果中的文本内容并返回。
    # English: Extracts and returns text from the first completion choice.
    return response.choices[0].message.content


# ===== 6) 执行主流程并打印结果 / Execute main flow and print result =====
# 中文：调用食谱生成函数并在控制台输出模型回复。
# English: Calls the recipe generator and prints model output to console.
print(recipe_generator(ingredients))