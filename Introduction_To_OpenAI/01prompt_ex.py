# ================================
# OpenAI 提示词引擎示例 / OpenAI Prompt Engine Example
# ================================
# 功能描述 / Description:
# 本脚本演示如何使用 OpenAI API 与 ChatGPT 进行交互。
# 它展示了如何安全地管理 API 密钥、构建 API 请求、
# 以及处理 API 响应。
# 
# This script demonstrates how to interact with ChatGPT using OpenAI API.
# It shows how to securely manage API keys, construct API requests,
# and handle API responses.
# ================================

import os
from dotenv import load_dotenv
from openai import OpenAI

# ===== 第一步 / Step 1: 环境变量配置 / Environment Configuration =====
# 加载 .env 文件中的环境变量
# 这样可以将敏感信息（如 API 密钥）保存在本地文件中，不会上传到 git 仓库
# Load environment variables from .env file
# This allows us to store sensitive information (like API keys) locally
# without uploading them to the git repository
load_dotenv()

# ===== 第二步 / Step 2: 获取和初始化 OpenAI 客户端 / Get and Initialize OpenAI Client =====
# 从环境变量中获取 OpenAI API Key
# 使用 os.getenv() 方法从系统环境变量或 .env 文件中读取
# Retrieve the OpenAI API Key from environment variables
# Using os.getenv() to read from system environment or .env file
api_key = os.getenv("OPENAI_API_KEY")

# 创建 OpenAI 客户端实例，用于与 OpenAI API 通信
# 所有的 API 调用都会通过这个客户端对象进行
# Create an OpenAI client instance to communicate with OpenAI API
# All API calls will be made through this client object
client = OpenAI(api_key=api_key)

# ===== 第三步 / Step 3: 定义提示词 / Define the Prompt =====
# 这是我们要发送给 ChatGPT 的问题/提示词
# 它组合了系统指令（让 AI 充当 NBA 专家）和具体的问题
# This is the question/prompt we want to send to ChatGPT
# It combines a system instruction (making AI act as NBA expert) and specific question
prompt = "You are a NBA basketball expert. Who is better, Michael Jordan or LeBron James?"


# ===== 第四步 / Step 4: 定义提示词引擎函数 / Define Prompt Engine Function =====
def prompt_engine(prompt):
    """
    调用 OpenAI API 的函数 / Function to call OpenAI API
    
    参数 / Parameters:
        prompt (str): 要发送给 ChatGPT 的提示词 / The prompt to send to ChatGPT
    
    返回 / Returns:
        str: ChatGPT 的响应内容 / The response content from ChatGPT
    """
    # 调用 OpenAI Chat Completions API
    # 这是一个阻塞式调用，会等待 API 服务器返回响应
    # Call OpenAI Chat Completions API
    # This is a blocking call that waits for the API server to return response
    response = client.chat.completions.create(
        # 模型选择：gpt-4o-mini 是一个相对经济的模型选项（比 gpt-4 便宜但功能仍很强大）
        # Model selection: gpt-4o-mini is a cost-effective option (cheaper than gpt-4 but still powerful)
        model="gpt-4o-mini",
        
        # 消息列表：定义对话的内容和结构
        # role="user" 表示这是用户发送的消息
        # Messages list: defines the content and structure of the conversation
        # role="user" indicates this is a message sent by the user
        messages=[
            {"role": "user", "content": prompt}
        ],
        
        # 最大令牌数：限制 API 响应的长度
        # 1 个令牌约等于 4 个字符。这里限制最多 500 个令牌
        # Max tokens: limits the length of API response
        # 1 token roughly equals 4 characters. Here we limit to max 500 tokens
        max_tokens=500,
        
        # 温度参数（Temperature）：控制 AI 的创意程度
        # 范围 0-2。0 = 确定性响应，1 = 平衡，2 = 非常有创意但可能不稳定
        # Temperature parameter: controls the creativity level of AI
        # Range 0-2. 0=deterministic, 1=balanced, 2=very creative but unstable
        temperature=1,
        
        # Top-P 采样参数：另一种控制随机性的方法
        # 范围 0-1。1 = 考虑所有可能的词汇，0 = 只考虑最有可能的词
        # Top-P sampling parameter: alternative way to control randomness
        # Range 0-1. 1=consider all vocabulary, 0=only most likely words
        top_p=1
    )

    # 提取并返回 API 响应中的文本内容
    # response.choices[0] 表示第一个（也是唯一一个）选择
    # .message.content 提取其中的文本内容
    # Extract and return the text content from API response
    # response.choices[0] represents the first (and only) choice
    # .message.content extracts the text content from it
    return response.choices[0].message.content


# ===== 第五步 / Step 5: 执行和输出 / Execute and Output =====
# 调用 prompt_engine 函数，发送提示词并打印 ChatGPT 的响应
# Call prompt_engine function to send prompt and print ChatGPT's response
print(prompt_engine(prompt))



