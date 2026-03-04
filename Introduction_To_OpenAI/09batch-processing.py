"""
====================================================================
OpenAI 批量处理示例 / OpenAI Batch Processing Example
====================================================================

中文说明：
本脚本演示如何批量处理多个提示词（prompts），逐一调用 Chat API，
收集所有结果，最后统一展示。适用于数据标注、内容生成、批量分析等场景。

English Description:
This script demonstrates batch processing of multiple prompts by calling
Chat API for each one, collecting results, and displaying them all at once.
Useful for data annotation, content generation, bulk analysis, etc.
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

# 中文：创建 OpenAI 客户端，后续批量请求通过该对象发送。
# English: Create OpenAI client for batch API requests.
client = OpenAI(api_key=api_key)

# ===== 4) 定义待处理的提示词集合 / Define batch of prompts to process =====
# 中文：这是一个列表，包含多个要发送给模型的问题。
# English: A list of multiple questions to send to the model.
prompts = [
    "What is the capital of France?",
    "What is the largest mammal?",
    "What is the square root of 16?",
    "Who is the president of the United States?"]


# ===== 5) 定义单个提示词处理函数 / Define single prompt processing function =====
def process_prompts(prompt):
    """
    中文：
    使用 Chat API 处理单个提示词，返回模型的回答。
    
    English:
    Process a single prompt using Chat API and return model's response.
    
    参数 / Args:
        prompt (str): 单个提示词 / Single prompt
    
    返回 / Returns:
        str: 模型的回答文本 / Model's response text
    """
    # 中文：调用 Chat Completions API，发送提示词和系统角色指令
    # English: Call Chat Completions API with prompt and system role
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "system", "content": "You are a helpful assistant."}],
        max_tokens=100,
        temperature=0.7
    )

    # 中文：提取并返回模型生成的文本内容
    # English: Extract and return model-generated text
    return response.choices[0].message.content


# ===== 6) 批量处理：逐个发送提示词，收集结果 / Batch process: send each prompt, collect results =====
# 中文：
# 初始化结果列表，用于存储所有的 API 响应。
# 然后遍历提示词列表，逐个调用 process_prompts()，并将结果追加到列表。
# English:
# Initialize results list to store all API responses.
# Iterate through prompts, call process_prompts() for each, append to results.
results = []

for prompt in prompts:
    result = process_prompts(prompt)
    results.append(result)


# ===== 7) 输出结果：显示所有提示词和对应的回答 / Output results: display all prompts and responses =====
# 中文：
# 遍历结果列表，配合原始提示词列表，逐行打印每个提示词和对应的回答。
# 这样用户可以清晰看到完整的"问-答"配对。
# English:
# Iterate through results, pair with original prompts, print each Q&A pair.
# Users see complete "question-answer" matching.
for i, result in enumerate(results):
    print(f"Prompt {i+1}: {prompts[i]}")
    print(f"Response {i+1}: {result}\n")