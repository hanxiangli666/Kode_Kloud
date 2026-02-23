import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

audio_file_path = open("Prompt_Engineering\大话西游 - 副本.wav", "rb")  # 替换为你的音频文件路径

transcription = client.audio.transcriptions.create(
    file=audio_file_path,
    model="whisper-1"
)

print(transcription.text)