"""
====================================================================
OpenAI DALL-E 图像生成示例 / OpenAI DALL-E Image Generation Example
====================================================================

中文说明：
本脚本演示如何使用 OpenAI 的 DALL-E 模型根据自然语言提示词（prompt）
生成艺术风格的图像。该能力适用于创意内容生成、设计辅助、原型设计等场景。

English Description:
This script demonstrates how to use OpenAI's DALL-E model to generate
artistic images based on natural language prompts (text). This is useful
for creative content generation, design assistance, prototyping, and more.
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
# 中文：从 .env 文件读取配置；override=True 允许 .env 值覆盖现有环境变量。
# English: Load config from .env; override=True lets .env values override existing env vars.
load_dotenv(override=True)

# ===== 3) 读取 API Key 并初始化客户端 / Read API key and initialize client =====
# 中文：从环境变量获取 OPENAI_API_KEY，避免密钥硬编码到源码。
# English: Get OPENAI_API_KEY from env vars to avoid hardcoding secrets.
api_key = os.getenv("OPENAI_API_KEY")

# 中文：创建 OpenAI 客户端，后续图像生成请求通过该对象发送。
# English: Create OpenAI client for sending subsequent image generation requests.
client = OpenAI(api_key=api_key)

# ===== 4) 定义图像生成函数 / Define image generation function =====
# 中文：
# 函数封装了对 DALL-E API 的调用逻辑。
# 参数解释：
#   - model: 使用的模型（dall-e-3 是最新、最智能的版本）
#   - prompt: 文本描述，越详细越好，可包含风格、灯光、视角等信息
#   - size: 生成图像的分辨率（1024x1024 是常见尺寸）
# English:
# Wraps the DALL-E API call logic.
# Parameters:
#   - model: model to use (dall-e-3 is latest and most capable)
#   - prompt: text description; more details yield better results
#   - size: output image resolution (1024x1024 is common)
def generate_image():
    response = client.images.generate(
        model="dall-e-3",
        prompt="Lebron James dunking a basketball in the style of Picasso",
        size="1024x1024"
    )
    # 中文：response.data[0].url 是生成图像的 CDN 链接（可直接在浏览器打开或下载）。
    # English: response.data[0].url is a CDN link to the generated image (openable/downloadable).
    return response.data[0].url

# ===== 5) 执行图像生成并输出结果 / Execute image generation and print result =====
# 中文：调用函数获取图像 URL，打印到控制台。用户可复制该链接到浏览器查看生成的图像。
# English: Call function to get image URL and print it. Users can paste the link in a browser to view.
image_url = generate_image()
print(f"Generated image URL: {image_url}")