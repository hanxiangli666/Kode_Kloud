#!/usr/bin/env python3
# 1) 该脚本演示让大模型按语义分段的智能切分流程; This script demonstrates LLM-guided semantic chunking.
# 2) 它实现了提示驱动的主题切分并与基础字符切分做对比; It implements prompt-driven topic splitting and contrasts it with basic chunking.
# 3) 使用的 AI 技术包括 LLM 推理与文本切分器联动; AI techniques used include LLM reasoning paired with a text splitter.
# 4) 在本目录的学习链路中，它是高级切分的阶段性总结; In the learning sequence, it serves as the advanced chunking milestone.
# 5) 它与其它脚本的关系是提供高质量分块以提升后续检索与RAG效果; It provides higher-quality chunks that improve later retrieval and RAG steps.
"""
Agentic Chunking Demo
Using LLM to intelligently split documents based on semantic meaning

This script demonstrates **Agentic Chunking** - the most advanced chunking method
where an AI model analyzes the document and decides optimal split points based on
topic shifts and semantic coherence, rather than arbitrary character counts.
"""

import os
import sys
from pathlib import Path

# 导入：LangChain 组件与切分器 / Imports: LangChain components and splitters
# 说明：本脚本使用 LangChain 的 ChatOpenAI 调用模型，并用文本切分器做基线对比 / This script uses LangChain ChatOpenAI and a splitter for baseline comparison.
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_dotenv(dotenv_path: Path, override: bool = False) -> None:
    """Minimal .env loader (no extra dependency).

    - Supports: KEY=VALUE
    - Ignores: blank lines and lines starting with '#'
    - override=True means .env wins over existing environment variables
    """

    # 读取 .env：不存在则直接跳过 / Load .env: skip silently if missing
    if not dotenv_path.exists():
        return

    # 逐行解析 KEY=VALUE / Parse KEY=VALUE lines
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue

        # 写入环境变量：override=True 时以 .env 为准 / Write env vars: when override=True, .env wins
        if override or key not in os.environ:
            os.environ[key] = value


def sanitize_api_key(api_key: str) -> str:
    # 清理 key：去掉首尾空白与可能的 Bearer 前缀 / Sanitize: trim whitespace and optional Bearer prefix
    api_key = (api_key or "").strip()
    if api_key.lower().startswith("bearer "):
        api_key = api_key[7:].strip()
    return api_key


# 启动横幅：便于在终端中区分脚本输出 / Startup banner: easy to spot in terminal output
print("🤖 Agentic Chunking Demo")
print("=" * 50)

# 路径定位：以当前脚本目录作为项目根 / Path: use script directory as project root
project_dir = Path(__file__).resolve().parent

# 加载配置：优先读取同目录 .env，并覆盖同名环境变量 / Config: load .env (same folder) and override existing vars
load_dotenv(project_dir / ".env", override=True)

# 读取 OpenAI 相关配置 / Read OpenAI-related settings
API_KEY = sanitize_api_key(os.environ.get("OPENAI_API_KEY", ""))
API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1").strip()
MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME", "gpt-4.1-mini").strip()

# 关键检查：没有 key 就无法进行 Agentic Chunking / Guard: without API key, agentic chunking cannot run
if not API_KEY:
    print("❌ Error: OPENAI_API_KEY not found.")
    print("Please create/update the .env file in this folder:")
    print(f"  {project_dir}\\.env")
    print("And set OPENAI_API_KEY=...")
    sys.exit(1)

# 安全诊断：只打印长度/尾部，不泄露完整 key / Safe diagnostics: never print full key
key_has_whitespace = any(ch.isspace() for ch in API_KEY)
key_tail = API_KEY[-4:] if len(API_KEY) >= 4 else "(short)"
print(f"🔐 API key loaded: length={len(API_KEY)}, tail={key_tail}, whitespace={key_has_whitespace}")

# 输出当前端点与模型：便于确认走的是哪个环境配置 / Show endpoint & model: confirm runtime configuration
print(f"🔌 API Endpoint: {API_BASE}")
print(f"🧠 Model: {MODEL_NAME}")
print()

# 示例文档：包含多个主题段落，用于展示“语义切分”的优势 / Sample doc: multiple topics to showcase semantic chunking
sample_document = """
TechCorp Company Overview

Company History: Founded in 1995 in a garage in Silicon Valley, TechCorp started as a small software consultancy. By 2000, it had grown to 500 employees and went public. The early years were marked by rapid expansion and the release of its flagship product, the TechOS. The founders, Jane Smith and John Doe, built the company on principles of innovation and customer focus.

Product Lineup: Today, TechCorp offers a wide range of enterprise software solutions. The CloudSuite is our most popular offering, providing scalable cloud infrastructure for businesses of all sizes. We also offer DataGuard for enterprise security, protecting sensitive data with military-grade encryption. AI-Core handles machine learning integration, making AI accessible to non-technical teams. Each product is designed to work seamlessly with the others.

Remote Work Policy: Employees may work remotely up to 3 days per week with manager approval. Remote work must be conducted using company-approved devices with VPN access enabled. All employees must be available during core hours (10 AM - 4 PM) and maintain regular communication with their team. Remote work is not a substitute for childcare or eldercare.

Future Vision: Looking ahead, TechCorp is betting big on quantum computing. We plan to invest $1B over the next 5 years in R&D for quantum technologies. Our goal is to be the first company to offer commercial quantum cloud services by 2030. This investment will create new positions for quantum researchers and engineers across all our locations.
"""

# 文档概览：长度与主题数量 / Document overview: length and topic count
print("📄 Sample Document:")
print(f"Length: {len(sample_document)} characters")
print("Contains 4 distinct topics: History, Products, Remote Work, Future")
print()

# 对比实验：先做基础切分，再做 agentic 切分 / Comparison: basic chunking first, then agentic chunking
print("🔧 Comparison: Basic Chunking vs Agentic Chunking")
print("-" * 50)

# 基线切分器：字符长度 + 分隔符优先级 / Baseline splitter: character length + separator priority
basic_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""],
)

# 生成基础 chunks 并打印预览 / Build basic chunks and print previews
basic_chunks = basic_splitter.split_text(sample_document)
print(f"\n📊 Basic Chunking Result: {len(basic_chunks)} chunks")
print("   (Based on character count, may split mid-topic)")
for i, chunk in enumerate(basic_chunks, 1):
    preview = chunk[:60].replace("\n", " ").strip()
    print(f"   Chunk {i}: {preview}...")
print()


def agentic_chunking(text: str) -> list[str]:
    # Agentic Chunking：让 LLM 判断主题边界并输出分隔符 / Agentic chunking: let the LLM decide topic boundaries
    print("🤔 Agent is analyzing the document for semantic topic shifts...")

    # 初始化 ChatOpenAI：使用环境变量提供的 key/base/model / Initialize ChatOpenAI with env-provided key/base/model
    llm = ChatOpenAI(
        model_name=MODEL_NAME,
        openai_api_key=API_KEY,
        openai_api_base=API_BASE,
        temperature=0,
    )

    # 构造提示词：要求输出以 ---SPLIT--- 分隔的原文 chunks / Prompt: request chunks separated by ---SPLIT--- without rewriting content
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert document editor specializing in semantic document analysis.
Your task is to split the provided text into semantically distinct chunks based on topic shifts.

Rules:
1. Keep related sentences together - don't break up a single topic
2. Split ONLY when the topic changes significantly (e.g., History -> Products -> Policy -> Future)
3. Each chunk should be about ONE coherent topic
4. Output the chunks separated by '---SPLIT---'
5. Do not modify the original text - just split it at appropriate boundaries
6. Include section headers with their content in the same chunk""",
            ),
            ("user", "{text}"),
        ]
    )

    # 链路：Prompt -> LLM -> 字符串解析 / Chain: prompt -> LLM -> parse string output
    chain = prompt | llm | StrOutputParser()

    try:
        # 调用模型并按分隔符切块 / Invoke model and split by delimiter
        response = chain.invoke({"text": text})
        return [c.strip() for c in response.split("---SPLIT---") if c.strip()]
    except Exception as e:
        # 错误处理：API 失败时返回空列表，不让脚本崩溃 / Error handling: return [] on API failures
        print(f"\n❌ API Error: {e}")
        return []


# 执行 agentic chunking：得到语义 chunks / Run agentic chunking: produce semantic chunks
agentic_chunks = agentic_chunking(sample_document)

# 结果展示：有结果就逐块打印主题与预览 / Display: print topic and preview per chunk when available
if agentic_chunks:
    print(f"\n📊 Agentic Chunking Result: {len(agentic_chunks)} chunks")
    print("   (Based on semantic meaning and topic shifts)")
    print()

    # 简单主题识别：用关键词猜测该 chunk 的主题 / Lightweight topic labeling by keywords
    for i, chunk in enumerate(agentic_chunks, 1):
        if "History" in chunk or "Founded" in chunk:
            topic = "Company History"
        elif "Product" in chunk or "CloudSuite" in chunk:
            topic = "Products"
        elif "Remote" in chunk or "work" in chunk.lower():
            topic = "Remote Work Policy"
        elif "Future" in chunk or "quantum" in chunk.lower():
            topic = "Future Vision"
        else:
            topic = "General"

        print(f"📦 Chunk {i} - Topic: {topic}")
        print(f"   Length: {len(chunk)} characters")
        preview = chunk[:80].replace("\n", " ").strip()
        print(f"   Preview: {preview}...")
        print()

    # 对比总结：基础切分 vs 语义切分 / Summary: basic vs semantic
    print("🔍 Comparison Summary:")
    print("-" * 50)
    print(f"Basic Chunking:   {len(basic_chunks)} chunks (character-based)")
    print(f"Agentic Chunking: {len(agentic_chunks)} chunks (semantic-based)")
    print()
    print("💡 Key Differences:")
    print("✅ Agentic chunking identifies natural topic boundaries")
    print("✅ Each chunk contains ONE coherent topic")
    print("✅ Better semantic coherence for RAG retrieval")
    print("✅ AI understands context and meaning")
    print("✅ No arbitrary character limit splitting")
    print()

    # 写入完成标记：便于课程步骤检查 / Write completion marker for course workflow
    with open("agentic_chunking_complete.txt", "w", encoding="utf-8") as f:
        f.write("Agentic chunking demo completed successfully")

    print("✅ Agentic chunking demo completed!")
else:
    # 无结果：通常是 API 配置/权限/网络问题 / No chunks: commonly API config/permission/network issue
    print("\n⚠️ Agent failed to produce chunks. Check API connection.")
