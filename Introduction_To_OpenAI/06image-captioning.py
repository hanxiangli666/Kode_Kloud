"""
====================================================================
OpenAI 图像理解与描述示例 / OpenAI Image Understanding & Captioning
====================================================================

中文说明：
本脚本演示如何使用 OpenAI 的 GPT-4V（Vision）能力来"理解"和"描述"
一张图像。用户提供图像 URL，模型分析其内容并生成自然语言描述。

English Description:
This script demonstrates how to use OpenAI's GPT-4V (Vision) capability
to understand and describe an image. Provide an image URL, and the model
analyzes its content and generates natural language descriptions.
"""

# ===== 1) 导入依赖 / Import dependencies =====
# 中文：
# - os：读取环境变量
# - load_dotenv：从 .env 文件加载配置
# - OpenAI：OpenAI 官方 Python SDK 客户端
# English:
# - os: read environment variables
# - load_dotenv: load configuration from .env file
# - OpenAI: official OpenAI Python SDK client
import os
from dotenv import load_dotenv
from openai import OpenAI

# ===== 2) 加载环境变量 / Load environment variables =====
# 中文：从 .env 文件读取配置；override=True 允许其覆盖系统中同名变量。
# English: Load config from .env; override=True lets .env values override
# existing environment variables with the same names.
load_dotenv(override=True)

# ===== 3) 读取 API Key 并初始化客户端 / Read API key and initialize client =====
# 中文：从环境变量获取 OPENAI_API_KEY，避免密钥硬编码到源码。
# English: Get OPENAI_API_KEY from environment to avoid hardcoding secrets.
api_key = os.getenv("OPENAI_API_KEY")

# 中文：创建 OpenAI 客户端，后续图像理解请求通过该对象发送。
# English: Create OpenAI client for sending image understanding requests.
client = OpenAI(api_key=api_key)

# ===== 4) 定义待分析的图像 URL / Define image URL to analyze =====
# 中文：这是一个网络图像的 URL。也可以是本地图像的 base64 编码。
# English: A publicly accessible image URL. Can also be base64-encoded local image.
image_url = "https://assets-prd.ignimgs.com/2022/06/10/netflix-one-piece-1654901410673.jpg"


# ===== 5) 定义图像描述生成函数 / Define caption generation function =====
# 中文：
# 这是一个多模态请求：既包含文本消息，也包含图像数据。
# 关键是 "content" 数组中混合了 text 和 image_url 两种类型。
# English:
# This is a multimodal request with both text and image.
# Key: the "content" array mixes "text" and "image_url" types.
def generate_caption(image_url):
    """
    中文：
    根据图像 URL 生成描述文本。
    
    English:
    Generate descriptive text from an image URL.
    
    参数 / Args:
        image_url (str): 图像的公开可访问 URL / Publicly accessible image URL
    
    返回 / Returns:
        str: 图像描述文本 / Image description text
    """
    # 中文：调用 Chat Completions API，但这次混合了文本与图像。
    # English: Call Chat Completions API with mixed text and image content.
    response = client.chat.completions.create(
        # 中文：gpt-4o 是多模态模型，能同时处理文本和图像。
        # English: gpt-4o is a multimodal model that handles both text and images.
        model="gpt-4o",
        
        # 中文：
        # messages 数组包含一条用户消息，其 content 也是数组形式：
        # - {"type":"text", "text":"..."} 是文本问题
        # - {"type":"image_url", "image_url":{"url":...}} 是图像数据
        # English:
        # messages array contains one user message with array content:
        # - {"type":"text", "text":"..."} is the text question
        # - {"type":"image_url", "image_url":{"url":...}} is the image data
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is in this image?"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        
        # 中文：限制输出长度为最多 150 tokens，保持描述简洁。
        # English: Limit output to 150 tokens for concise descriptions.
        max_tokens=150
    )
    
    # 中文：提取第一条候选结果中的文本内容并返回。
    # English: Extract and return text from the first completion choice.
    return response.choices[0].message.content


# ===== 6) 执行图像描述生成并输出结果 / Execute caption generation and print =====
# 中文：调用函数，传入图像 URL，输出模型生成的图像描述。
# English: Call the function with image URL and print the generated caption.
print(generate_caption(image_url))