"""
====================================================================
AI 文章翻译示例 / AI Article Translation Example
====================================================================

中文说明：
本脚本演示如何使用 OpenAI Chat API 进行多语言翻译。
流程是：准备源语言文章 → 构建翻译指令 → 调用 Chat API → 接收翻译结果。
可用于新闻翻译、文档本地化、多语言内容管理等场景。

English Description:
This script demonstrates how to use OpenAI Chat API for multilingual translation.
Flow: prepare source article → build translation instructions → call Chat API → receive translation.
Useful for news translation, document localization, multilingual content management, etc.
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

# 中文：创建 OpenAI 客户端，后续翻译请求通过该对象发送。
# English: Create OpenAI client for translation requests.
client = OpenAI(api_key=api_key)

# ===== 4) 定义待翻译的源文章 / Define source article to translate =====
# 中文：这是一篇英文文章，待翻译成中文。可替换为任何其他语言和长度的文章。
# English: An English article to be translated to Chinese. Can be replaced with any language/length.
article = "I and my friend went to the park yesterday. We had a great time playing soccer and enjoying the sunshine. The weather was perfect, and we even had a picnic with sandwiches and lemonade. It was a wonderful day spent outdoors."

# ===== 5) 构建翻译提示词 / Build translation prompt =====
# 中文：将文章嵌入到提示词（prompt）中，告诉模型需要翻译什么。
# English: Embed article into prompt to tell model what to translate.
prompt = f"Translate the following article: {article}"


# ===== 6) 定义文章翻译函数 / Define article translation function =====
def article_translation(prompt):
    """
    中文：
    使用 Chat API 进行翻译。messages 数组定义对话上下文：
    - system：系统角色指令，告诉模型身份和任务要求
    - user：用户的实际翻译请求
    
    English:
    Use Chat API for translation. messages array defines conversation context:
    - system: system role instruction—model's identity and task requirements
    - user: actual user translation request
    
    参数 / Args:
        prompt (str): 包含待翻译文章的提示词 / Prompt with article to translate
    
    返回 / Returns:
        str: 翻译后的文本 / Translated text
    """
    # 中文：
    # messages 数组定义对话流程。最佳实践是：
    # 1. system：定义模型角色和翻译规范（如"你是专业翻译"、"直接、自然的中文"）
    # 2. user：用户的实际请求（要翻译的内容）
    # English:
    # messages array defines conversation flow. Best practice:
    # 1. system: model role and translation standards ("professional translator", "natural Chinese")
    # 2. user: actual user request (content to translate)
    messages = [
        {
            "role": "system",
            "content": "You are a professional translator. Translate the following article into Chinese. Ensure the translation is direct, natural, and maintains the original meaning."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # 中文：
    # 调用 Chat Completions API：
    # - model="gpt-4o-mini"：使用轻量级模型（成本低，翻译能力仍强）
    # - temperature=0.1：非常低的随机性。翻译需要"忠实于原文"，不需要创意
    # - messages：上面定义的对话上下文
    # English:
    # Call Chat Completions API:
    # - model="gpt-4o-mini": lightweight model (low cost, strong translation)
    # - temperature=0.1: very low randomness—translation needs "faithfulness," not creativity
    # - messages: conversation context defined above
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=messages,
    )

    # 中文：提取并返回模型生成的翻译文本
    # English: Extract and return model-generated translation text
    return response.choices[0].message.content


# ===== 7) 执行翻译并输出结果 / Execute translation and print result =====
# 中文：调用翻译函数，传入提示词，获取翻译结果，打印到控制台。
# English: Call translation function with prompt, get result, print to console.
print(article_translation(prompt))
