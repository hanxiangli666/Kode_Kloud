import os
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv(override=True)

# 从环境变量中获取 API Key
# 这样代码里就不再包含真实的密钥了
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

prompt = "What is the capital of France?"

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("tts_example.mp3")
    os.system("start tts_example.mp3")  # For macOS, use "afplay". For Windows, use "start" or "wmplayer".


def generate_text(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7,
    )
    return response.choices[0].message.content

def generate_and_speak(prompt):
    generated_text = generate_text(prompt)
    print("Generated Text:", generated_text)
    text_to_speech(generated_text)

print(generate_and_speak(prompt))