"""
====================================================================
OpenAI Whisper 语音转文字示例 / OpenAI Whisper Speech-to-Text Example
====================================================================

中文说明：
本脚本演示如何使用 OpenAI 的 Whisper 模型将音频文件（WAV、MP3 等）
转录为文本。Whisper 支持多种语言、方言、环境噪音，应用于记录、翻译、字幕生成等。

English Description:
This script shows how to use OpenAI's Whisper model to transcribe audio files
(WAV, MP3, etc.) to text. Whisper supports multiple languages, accents, and
noisy environments—useful for recording, translation, subtitle generation, etc.
"""

# ===== 1) 导入依赖 / Import dependencies =====
# 中文：
# - os：用于文件操作和环境变量读取
# - load_dotenv：从 .env 文件加载配置
# - OpenAI：OpenAI 官方 Python SDK 客户端
# English:
# - os: file operations and environment variable access
# - load_dotenv: load configuration from .env file
# - OpenAI: official OpenAI Python SDK client
import os
from dotenv import load_dotenv
from openai import OpenAI

# ===== 2) 加载环境变量 / Load environment variables =====
# 中文：从 .env 文件读取配置；override=True 允许覆盖系统中同名变量。
# English: Load config from .env; override=True lets .env values override
# existing environment variables with the same names.
load_dotenv(override=True)

# ===== 3) 读取 API Key 并初始化客户端 / Read API key and initialize client =====
# 中文：从环境变量获取 OPENAI_API_KEY，避免把密钥硬编码到源码。
# English: Get OPENAI_API_KEY from environment to avoid hardcoding secrets.
api_key = os.getenv("OPENAI_API_KEY")

# 中文：创建 OpenAI 客户端，后续语音转录请求通过该对象发送。
# English: Create OpenAI client for sending speech transcription requests.
client = OpenAI(api_key=api_key)

# ===== 4) 打开音频文件 / Open audio file =====
# 中文：
# 以二进制只读模式打开音频文件。支持的格式：mp3、mp4、mpeg、mpga、m4a、wav、webm。
# 注意：文件路径是相对路径，需要确保文件存在于该位置；
# 若文件不存在，open() 会抛出 FileNotFoundError。
# English:
# Open audio file in binary read mode. Supported: mp3, mp4, mpeg, mpga, m4a, wav, webm.
# Note: relative path—ensure the file exists; if not, open() raises FileNotFoundError.
audio_file_path = open("Introduction_To_OpenAI\\Journey_To_The_West.wav", "rb")

# ===== 5) 调用 Whisper 模型进行转录 / Call Whisper model for transcription =====
# 中文：
# - file：音频文件对象（二进制）
# - model：使用的转录模型（目前只有 "whisper-1"）
# Whisper 会分析音频并输出转录的文本结果。
# English:
# - file: audio file object (binary)
# - model: transcription model to use (currently only "whisper-1")
# Whisper analyzes audio and outputs transcribed text.
transcription = client.audio.transcriptions.create(
    file=audio_file_path,
    model="whisper-1"
)

# ===== 6) 输出转录结果 / Output transcription result =====
# 中文：transcription.text 包含完整的转录文本。直接打印到控制台。
# English: transcription.text contains the full transcription as a string.
print(transcription.text)