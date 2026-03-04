"""
============================================================
OpenAI Chat Completions 双语示例 / OpenAI Chat Completions Bilingual Example
============================================================

中文说明：
本脚本演示如何使用 OpenAI Python SDK 调用聊天补全接口（Chat Completions）。
核心流程包括：加载环境变量、初始化客户端、构造消息、请求模型、输出结果。

English Description:
This script demonstrates how to call the Chat Completions API using the OpenAI Python SDK.
The core flow includes: loading environment variables, initializing the client,
building messages, requesting a model response, and printing the result.
"""

# ===== 1) 导入依赖 / Import dependencies =====
# 中文：
# - os：读取环境变量（例如 API Key）
# - load_dotenv：从 .env 文件加载环境变量
# - OpenAI：OpenAI 官方 Python 客户端类
# English:
# - os: reads environment variables (such as API key)
# - load_dotenv: loads environment variables from a .env file
# - OpenAI: official OpenAI Python client class
import os
from dotenv import load_dotenv
from openai import OpenAI

# ===== 2) 加载环境变量 / Load environment variables =====
# 中文：将 .env 文件中的配置注入当前运行环境，便于后续通过 os.getenv 读取。
# English: Injects values from .env into the current process environment
# so they can be read via os.getenv.
load_dotenv()

# ===== 3) 读取 API Key / Read API key =====
# 中文：从环境变量中读取 OPENAI_API_KEY，避免将密钥硬编码在源码中。
# English: Reads OPENAI_API_KEY from environment variables to avoid hardcoding
# secrets directly in source code.
api_key = os.getenv("OPENAI_API_KEY")

# ===== 4) 初始化 OpenAI 客户端 / Initialize OpenAI client =====
# 中文：创建与 OpenAI 服务通信的客户端对象，后续所有请求都通过它发出。
# English: Creates the client object used to communicate with OpenAI services.
client = OpenAI(api_key=api_key)

# ===== 5) 定义用户提示词 / Define user prompt =====
# 中文：这是用户想让模型回答的问题。
# English: This is the question we want the model to answer.
prompt = "How can I make money?"


# ===== 6) 封装聊天调用函数 / Wrap chat call in a function =====
def chat_comp(prompt):
    """
    中文：
    调用 Chat Completions API，返回模型生成的文本。

    English:
    Calls the Chat Completions API and returns the generated text.

    参数 / Args:
        prompt (str): 用户输入的问题 / User input question

    返回 / Returns:
        str: 模型回复文本 / Model reply text
    """
    # 中文：向 chat.completions.create 发送请求。
    # English: Sends a request to chat.completions.create.
    response = client.chat.completions.create(
        # 中文：指定模型名称。
        # English: Specifies the model name.
        model="gpt-4o",

        # 中文：构造消息列表（对话上下文）。
        # - role="user"：用户消息
        # - role="system"：系统角色设定（风格/行为指令）
        # English: Builds the message list (conversation context).
        # - role="user": user message
        # - role="system": system instruction (style/behavior)
        messages=[
            {"role": "user", "content": prompt},
            {"role": "system", "content": "You are a southern belle."}
        ],

        # 中文：限制模型最多生成 250 tokens，控制输出长度与成本。
        # English: Limits generation to 250 tokens to control output length and cost.
        max_tokens=250
    )

    # 中文：从响应结构中提取第一条候选结果的文本内容。
    # English: Extracts text content from the first completion choice.
    return response.choices[0].message.content


# ===== 7) 执行并打印结果 / Execute and print result =====
# 中文：调用封装函数并输出模型回答。
# English: Calls the wrapper function and prints the model response.
print(chat_comp(prompt))