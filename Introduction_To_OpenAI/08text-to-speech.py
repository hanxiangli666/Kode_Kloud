"""
====================================================================
OpenAI Text-to-Speech 文字转语音示例 / Text-to-Speech Example
====================================================================

中文说明：
本脚本演示一个"生成-转语音"的完整流程：
1) 调用 Chat API 生成回答文本
2) 使用 TTS (Text-to-Speech) 模型将文本转换为音频
3) 自动播放生成的音频文件

支持多种性别和风格的声音（voice），可用于虚拟助手、有声书、播客等场景。

English Description:
This script demonstrates a complete "generate-then-speak" flow:
1) Call Chat API to generate answer text
2) Use TTS model to convert text to audio
3) Auto-play the generated audio file

Supports multiple voice options (voice) for VA, audiobooks, podcasts, etc.
"""

# ===== 1) 导入依赖 / Import dependencies =====
# 中文：
# - os：用于环境变量读取和系统命令执行（如播放音频）
# - load_dotenv：从 .env 文件加载配置
# - OpenAI：OpenAI 官方 Python SDK 客户端
# English:
# - os: environment variables and system commands (e.g., play audio)
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

# 中文：创建 OpenAI 客户端，后续所有 API 请求（Chat、TTS）通过该对象发送。
# English: Create OpenAI client for Chat and TTS requests.
client = OpenAI(api_key=api_key)

# ===== 4) 定义初始提示词 / Define initial prompt =====
# 中文：这是要发送给 Chat API 的问题。最后会生成答案，再转语音。
# English: Question to send to Chat API. Answer will be generated, then spoken.
prompt = "What is the capital of France?"


# ===== 5) 定义文本转语音函数 / Define text-to-speech function =====
def text_to_speech(text):
    """
    中文：
    将文本转换为语音，保存为 MP3 文件，并自动播放。
    
    English:
    Convert text to speech, save as MP3, and auto-play.
    
    参数 / Args:
        text (str): 要转换为语音的文本 / Text to convert to speech
    """
    # 中文：
    # - model="tts-1"：使用最快、成本最低的 TTS 模型（还有 tts-1-hd 但更贵更慢）
    # - voice：选择声音。可选项：alloy(中性)、echo(男性)、fable(故事风)、
    #   onyx(深沉)、nova(明亮)、shimmer(温和)
    # - input：要转语音的文本
    # - with_streaming_response：启用流式响应，边生成边保存
    # English:
    # - model="tts-1": fastest, cheapest TTS model (tts-1-hd is slower/pricier)
    # - voice: choose voice—alloy, echo, fable, onyx, nova, shimmer
    # - input: text to convert
    # - with_streaming_response: enable streaming (save as generated)
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",  # 中文：改为其他选项可听到不同声音 / English: try other options for different voices
        input=text
    ) as response:
        # 中文：流式保存响应数据到本地 MP3 文件
        # English: Stream response data to local MP3 file
        response.stream_to_file("tts_example.mp3")
    
    # 中文：用系统命令播放音频文件（这里是 Windows 命令；Mac/Linux 需要改）
    # English: Play audio using system command (Windows; Mac/Linux need different command)
    os.system("start tts_example.mp3")  # For Windows only


# ===== 6) 定义文本生成函数 / Define text generation function =====
def generate_text(prompt):
    """
    中文：
    使用 Chat API 生成文本回答。
    
    English:
    Use Chat API to generate a text response.
    
    参数 / Args:
        prompt (str): 送给模型的提示词 / Prompt for the model
    
    返回 / Returns:
        str: 模型生成的文本 / Generated text from the model
    """
    # 中文：调用 Chat Completions API
    # English: Call Chat Completions API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7,
    )
    # 中文：提取生成的文本内容并返回
    # English: Extract and return generated text
    return response.choices[0].message.content


# ===== 7) 定义组合函数：生成并朗读 / Define combined function: generate and speak =====
def generate_and_speak(prompt):
    """
    中文：
    完整流程：先生成文本，打印显示，再转语音并播放。
    
    English:
    Complete flow: generate text, print it, convert to speech and play.
    
    参数 / Args:
        prompt (str): 初始提示词 / Initial prompt
    """
    # 中文：第 1 步：生成文本
    # English: Step 1: Generate text
    generated_text = generate_text(prompt)
    
    # 中文：第 2 步：显示生成的文本
    # English: Step 2: Display generated text
    print("Generated Text:", generated_text)
    
    # 中文：第 3 步：将生成的文本转语音加播放
    # English: Step 3: Convert to speech and play
    text_to_speech(generated_text)


# ===== 8) 执行主流程 / Execute main flow =====
# 中文：调用组合函数，开启"生成-朗读"的完整链路
# English: Call the combined function to start the "generate-speak" pipeline
generate_and_speak(prompt)