"""
====================================================================
AI 研究助手示例 / AI Research Assistant Example
====================================================================

中文说明：
本脚本演示如何使用 OpenAI Chat API 分析 CSV 数据文件，
生成数据洞察和研究报告。流程是：加载数据 → 格式化数据 → 
送给 Chat API 分析 → 生成洞察。

English Description:
This script demonstrates how to use OpenAI Chat API to analyze CSV data,
generate data insights and research reports. Flow: load data → format data →
send to Chat API for analysis → generate insights.
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

# 中文：创建 OpenAI 客户端，后续数据分析请求通过该对象发送。
# English: Create OpenAI client for data analysis requests.
client = OpenAI(api_key=api_key)


# ===== 4) 读取 CSV 数据文件 / Read CSV data file =====
# 中文：
# 使用 pandas 的 read_csv() 函数从指定路径读取 CSV 文件。
# 该文件包含学生表现因素数据，后续会用来分析与生成报告。
# English:
# Use pandas' read_csv() to load CSV file from specified path.
# File contains student performance factors data for analysis and reporting.
df = pd.read_csv("Introduction_To_OpenAI\\StudentPerformanceFactors.csv")


# ===== 5) 定义数据分析函数 / Define data analysis function =====
def analyze_data(df):
    """
    中文：
    接收 pandas DataFrame，将其转换为可读的字符串格式，
    然后发送给 Chat API，让 AI 生成分析报告。
    
    English:
    Receive pandas DataFrame, convert to readable string format,
    send to Chat API for AI-powered analysis report generation.
    
    参数 / Args:
        df (pandas.DataFrame): 包含学生表现数据的 DataFrame / DataFrame with student performance data
    
    返回 / Returns:
        str: AI 生成的分析洞察文本 / AI-generated analysis insights
    """
    # 中文：
    # df.to_string() 将 DataFrame 转换为可读的表格字符串。
    # 这比直接传 {df} 要好得多——模型能直观看到数据的结构和内容。
    # English:
    # df.to_string() converts DataFrame to readable table format.
    # Much better than directly converting df to string—model sees data structure clearly.
    data_str = df.to_string()
    
    # 中文：
    # 构建提示词，要求 AI 根据提供的数据表格生成关键洞察。
    # temperature=0.2 设置很低的随机性，使 AI 专注于数据分析而非创意输出。
    # English:
    # Build prompt requesting AI to generate key insights from data.
    # temperature=0.2 is low randomness—AI focuses on data analysis not creativity.
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"You are a research assistant. Please analyze the following student performance data and provide key insights in point form:\n\n{data_str}"
            }
        ],
        max_tokens=500,
        temperature=0.2,
    )
    
    # 中文：提取并返回 AI 生成的分析文本
    # English: Extract and return AI-generated analysis text
    return response.choices[0].message.content


# ===== 6) 执行数据分析并输出结果 / Execute data analysis and print results =====
# 中文：
# 调用 analyze_data() 函数，传入加载的 DataFrame，
# 获取 AI 生成的分析报告，并打印到控制台。
# English:
# Call analyze_data() with loaded DataFrame,
# get AI-generated analysis report, print to console.
print(analyze_data(df))

