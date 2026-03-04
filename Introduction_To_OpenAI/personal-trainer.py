"""
====================================================================
AI 个人健身教练示例 / AI Personal Trainer Example
====================================================================

中文说明：
本脚本演示如何结合用户输入（健身目标）和数据分析（睡眠和生活方式数据）
来生成个性化的健身计划。流程是：加载健康数据 → 收集用户目标 → 
调用 Chat API 结合数据和目标生成训练计划。

English Description:
This script combines user input (fitness goals) with data analysis 
(sleep and lifestyle data) to generate personalized workout plans.
Flow: load health data → collect user goals → call Chat API with data + goals
→ generate personalized workout plan.
"""

# ===== 1) 导入依赖 / Import dependencies =====
# 中文：
# - os：环境变量读取
# - load_dotenv：从 .env 文件加载配置
# - OpenAI：OpenAI 官方 Python SDK 客户端
# - pandas：数据处理和 CSV 读取
# English:
# - os: environment variable access
# - load_dotenv: load configuration from .env file
# - OpenAI: official OpenAI Python SDK client
# - pandas: data processing and CSV reading
import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# ===== 2) 加载环境变量 / Load environment variables =====
# 中文：从 .env 文件读取配置；override=True 允许覆盖系统中同名变量。
# English: Load config from .env; override=True lets .env values override
# existing environment variables.
load_dotenv(override=True)

# ===== 3) 读取 API Key 并初始化客户端 / Read API key and initialize client =====
# 中文：从环境变量获取 OPENAI_API_KEY，避免把密钥硬编码到源码。
# English: Get OPENAI_API_KEY from environment to avoid hardcoding secrets.
api_key = os.getenv("OPENAI_API_KEY")

# 中文：创建 OpenAI 客户端，后续健身计划生成请求通过该对象发送。
# English: Create OpenAI client for fitness plan generation requests.
client = OpenAI(api_key=api_key)


# ===== 4) 读取健康与生活方式数据 / Load health and lifestyle data =====
# 中文：
# 使用 pandas 的 read_csv() 从 CSV 文件读取睡眠健康和生活方式数据。
# 该数据包含用户的睡眠模式、运动习惯等信息，后续会用来个性化健身计划。
# English:
# Use pandas to load sleep health and lifestyle data from CSV file.
# Contains user sleep patterns, exercise habits, etc. for personalized planning.
df = pd.read_csv("Introduction_To_OpenAI\\Sleep_health_and_lifestyle_dataset.csv")

# ===== 5) 交互式收集用户健身目标 / Interactively collect user fitness goals =====
# 中文：
# 通过 while True 循环不断询问用户的健身目标（如减重、增肌、耐力提升）。
# 用户输入 'done' 结束目标输入，所有目标存储在列表中。
# English:
# Loop to ask user for fitness goals (weight loss, muscle gain, endurance, etc.).
# User types 'done' to finish; all goals stored in list.
goals = []

while True:
    goal = input("What are your fitness goals? (e.g., weight loss, muscle gain, improved endurance) (type 'done' to finish): ")
    if goal.lower() == 'done':
        break

    goals.append(goal)


# ===== 6) 定义个人教练函数 / Define personal trainer function =====
def trainer(df, goals):
    """
    中文：
    基于用户目标和健康数据生成个性化健身计划。
    函数接收 DataFrame（含健康数据）和目标列表，
    调用 Chat API 并请求生成详细的训练计划。
    
    English:
    Generate personalized fitness plan based on user goals and health data.
    Takes DataFrame with health data and goals list,
    calls Chat API to generate detailed training plan.
    
    参数 / Args:
        df (pandas.DataFrame): 含睡眠和生活方式数据的 DataFrame / Health data DataFrame
        goals (list): 用户的健身目标列表 / List of user fitness goals
    
    返回 / Returns:
        str: AI 生成的个性化健身计划 / AI-generated personalized fitness plan
    """
    # 中文：
    # 将 DataFrame 转换为可读的字符串格式，便于模型理解健康数据的结构。
    # English:
    # Convert DataFrame to readable string format for model to understand health data.
    data_str = df.to_string()
    
    # 中文：
    # 构建 messages 数组，定义了"身份"和"任务"：
    # - system：定义 AI 是个人教练，需要参考用户的健康数据，为运动员制定计划
    # - user：用户的具体请求（创建针对特定目标的训练计划）
    # 
    # 注意：这里不需要 assistant 消息——assistant 应该只在 few-shot 示例中使用。
    # English:
    # Build messages array defining "identity" and "task":
    # - system: AI is personal trainer, must reference health data, plan for athlete
    # - user: specific request (create training plan for goals)
    # 
    # Note: no assistant message—only needed in few-shot examples.
    messages = [
        {
            "role": "system",
            "content": f"You are a professional personal trainer specializing in athletes. You have access to the following health and lifestyle data:\n\n{data_str}\n\nUse this data to understand the user's baseline health metrics (sleep patterns, activity levels, etc.) and create a specific, actionable training plan that aligns with their goals and current health status."
        },
        {
            "role": "user",
            "content": f"Create a detailed workout plan to achieve my fitness goals: {', '.join(goals)}."
        }
    ]

    # 中文：
    # 调用 Chat Completions API：
    # - model="gpt-4o"：使用完整能力的模型以确保高质量的个性化计划
    # - temperature=0.8：温度适度较高。健身计划需要一定的创意和个性化，不能太生硬
    # - max_tokens=500：足够生成详细的训练计划和建议
    # English:
    # Call Chat Completions API:
    # - model="gpt-4o": full-capability model for high-quality personalization
    # - temperature=0.8: moderate-high for personalized, creative plan (not robotic)
    # - max_tokens=500: sufficient for detailed plan and advice
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=500,
        temperature=0.8,
    )

    # 中文：提取并返回 AI 生成的健身计划文本
    # English: Extract and return AI-generated fitness plan text
    return response.choices[0].message.content


# ===== 7) 执行训练计划生成并输出结果 / Execute training plan generation and output =====
# 中文：
# 调用 trainer 函数，传入加载的数据和用户输入的目标，
# 获取个性化的健身计划，打印到控制台。
# English:
# Call trainer() with loaded data and user goals,
# get personalized fitness plan, print to console.
print(trainer(df, goals))