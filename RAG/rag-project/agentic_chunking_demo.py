#!/usr/bin/env python3
"""
Agentic Chunking Demo
Using LLM to intelligently split documents based on semantic meaning

This script demonstrates **Agentic Chunking** - the most advanced chunking method
where an AI model analyzes the document and decides optimal split points based on
topic shifts and semantic coherence, rather than arbitrary character counts.
"""
import os
import sys
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 程序启动提示 / Startup banner
print("🤖 Agentic Chunking Demo")
print("=" * 50)

# 配置：使用环境变量读取 API 设置 / Config: read API settings from env vars
API_KEY = os.environ.get("OPENAI_API_KEY")
API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
MODEL_NAME = "openai/gpt-4.1-mini"

# 如果没有 API Key 就直接退出 / Exit if API key is missing
if not API_KEY:
    print("❌ Error: OPENAI_API_KEY not found.")
    print("Please ensure the environment is configured correctly.")
    sys.exit(1)

# 打印当前使用的端点和模型 / Show selected endpoint and model
print(f"🔌 API Endpoint: {API_BASE}")
print(f"🧠 Model: {MODEL_NAME}")
print()

# 示例文档：包含多个不同主题 / Sample document with multiple topics
sample_document = """
TechCorp Company Overview

Company History: Founded in 1995 in a garage in Silicon Valley, TechCorp started as a small software consultancy. By 2000, it had grown to 500 employees and went public. The early years were marked by rapid expansion and the release of its flagship product, the TechOS. The founders, Jane Smith and John Doe, built the company on principles of innovation and customer focus.

Product Lineup: Today, TechCorp offers a wide range of enterprise software solutions. The CloudSuite is our most popular offering, providing scalable cloud infrastructure for businesses of all sizes. We also offer DataGuard for enterprise security, protecting sensitive data with military-grade encryption. AI-Core handles machine learning integration, making AI accessible to non-technical teams. Each product is designed to work seamlessly with the others.

Remote Work Policy: Employees may work remotely up to 3 days per week with manager approval. Remote work must be conducted using company-approved devices with VPN access enabled. All employees must be available during core hours (10 AM - 4 PM) and maintain regular communication with their team. Remote work is not a substitute for childcare or eldercare.

Future Vision: Looking ahead, TechCorp is betting big on quantum computing. We plan to invest $1B over the next 5 years in R&D for quantum technologies. Our goal is to be the first company to offer commercial quantum cloud services by 2030. This investment will create new positions for quantum researchers and engineers across all our locations.
"""

# 显示示例文档的基本信息 / Show basic info for the sample doc
print("📄 Sample Document:")
print(f"Length: {len(sample_document)} characters")
print(f"Contains 4 distinct topics: History, Products, Remote Work, Future")
print()

# 先与基础切分方式做对比 / Compare with basic chunking first
print("🔧 Comparison: Basic Chunking vs Agentic Chunking")
print("-" * 50)

# 基础切分：按字符数进行切块 / Basic chunking by character count
basic_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50,
    separators=["\n\n", "\n", " ", ""]
)

# 生成基础切分结果并预览 / Build basic chunks and preview
basic_chunks = basic_splitter.split_text(sample_document)
print(f"\n📊 Basic Chunking Result: {len(basic_chunks)} chunks")
print("   (Based on character count, may split mid-topic)")
for i, chunk in enumerate(basic_chunks, 1):
    preview = chunk[:60].replace('\n', ' ').strip()
    print(f"   Chunk {i}: {preview}...")
print()

# 使用 LLM 进行 Agentic Chunking / Agentic chunking with an LLM
def agentic_chunking(text):
    """
    Uses an LLM to split text into semantically distinct chunks.
    The AI analyzes topic shifts and creates meaningful boundaries.
    """
    # 提示正在进行语义分析 / Indicate semantic analysis is running
    print("🤔 Agent is analyzing the document for semantic topic shifts...")
    
    # 初始化 LLM 客户端 / Initialize LLM client
    llm = ChatOpenAI(
        model=MODEL_NAME,
        openai_api_key=API_KEY,
        openai_api_base=API_BASE,
        temperature=0  # 确保输出稳定 / Deterministic output for consistency
    )

    # 构造提示词：让模型充当“切分代理” / Prompt: instruct the model to chunk
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert document editor specializing in semantic document analysis.
Your task is to split the provided text into semantically distinct chunks based on topic shifts.

Rules:
1. Keep related sentences together - don't break up a single topic
2. Split ONLY when the topic changes significantly (e.g., History -> Products -> Policy -> Future)
3. Each chunk should be about ONE coherent topic
4. Output the chunks separated by '---SPLIT---'
5. Do not modify the original text - just split it at appropriate boundaries
6. Include section headers with their content in the same chunk"""),
        ("user", "{text}")
    ])

    # 组合链路：提示词 -> 模型 -> 文本输出解析 / Chain: prompt -> model -> parser
    chain = prompt | llm | StrOutputParser()
    
    try:
        # 调用模型并按分隔符切分输出 / Invoke and split by delimiter
        response = chain.invoke({"text": text})
        # 按分隔符切分并清理 / Split by delimiter and clean up
        chunks = [c.strip() for c in response.split("---SPLIT---") if c.strip()]
        return chunks
    except Exception as e:
        # 捕获 API 错误并返回空结果 / Handle API errors and return empty result
        print(f"\n❌ API Error: {e}")
        return []

# 执行 Agentic Chunking / Run agentic chunking
agentic_chunks = agentic_chunking(sample_document)

# 根据是否有结果输出不同内容 / Branch based on result presence
if agentic_chunks:
    print(f"\n📊 Agentic Chunking Result: {len(agentic_chunks)} chunks")
    print("   (Based on semantic meaning and topic shifts)")
    print()
    
    # 逐块判断主题并打印预览 / Detect topic and print preview per chunk
    for i, chunk in enumerate(agentic_chunks, 1):
        # 从内容判断主题 / Identify the likely topic from the chunk
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
        preview = chunk[:80].replace('\n', ' ').strip()
        print(f"   Preview: {preview}...")
        print()

    # 对比总结 / Comparison summary
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
    
    print("💡 When to Use Agentic Chunking:")
    print("✅ Documents with clear topic sections")
    print("✅ When semantic coherence is critical")
    print("✅ Complex documents with mixed content")
    print("✅ When retrieval quality matters more than speed")
    print()
    
    print("⚠️  Considerations:")
    print("• Requires LLM API calls (cost and latency)")
    print("• Best for smaller documents or preprocessing")
    print("• May need fallback for very large documents")
    
    # 写入完成标记文件 / Write completion marker file
    with open("agentic_chunking_complete.txt", "w") as f:
        f.write("Agentic chunking demo completed successfully")
    
    print("\n✅ Agentic chunking demo completed!")
else:
    # 无结果时提示检查 API / Warn when no chunks returned
    print("\n⚠️ Agent failed to produce chunks. Check API connection.")
