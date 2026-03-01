#!/usr/bin/env python3
"""
Basic Document Chunking Demo
Using LangChain's RecursiveCharacterTextSplitter
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

# 启动提示 / Startup banner
print("✂️ Basic Document Chunking Demo")
print("=" * 50)

# 示例文档：远程办公政策 / Sample policy document
policy_document = """
TechCorp Remote Work Policy

Employees may work remotely up to 3 days per week with manager approval. 
Remote work days must be scheduled in advance and approved by your direct supervisor.
All remote work must comply with company security policies and use approved equipment.
Employees working remotely are expected to maintain regular communication with their team.
Performance expectations remain the same regardless of work location.

Remote work is not a substitute for childcare or eldercare responsibilities.
Employees must have a dedicated workspace free from distractions.
All company equipment must be returned if remote work arrangement is terminated.
"""

# 展示原始文档信息 / Show original document info
print("📄 Original Document:")
print(f"Length: {len(policy_document)} characters")
print(f"Content: {policy_document[:100]}...")
print()

# 创建文本切分器 / Create text splitter
print("🔧 Creating LangChain RecursiveCharacterTextSplitter...")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,  # 每块最大字符数 / Maximum characters per chunk
    chunk_overlap=50,  # 块之间重叠 / Overlap between chunks
    separators=["\n\n", "\n", " ", ""]  # 分隔符优先级 / Separator priority
)

# 执行切分 / Split the document
print("✂️ Splitting document into chunks...")
chunks = splitter.split_text(policy_document)

# 输出切分数量 / Show chunk count
print(f"✅ Created {len(chunks)} chunks")
print()

# 展示每个切块 / Display each chunk
print("📋 Chunk Details:")
for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i}:")
    print(f"  Length: {len(chunk)} characters")
    print(f"  Content: {chunk}")
    print(f"  Separator: {'-' * 30}")
    print()

# 总结优势 / Summarize benefits
print("💡 Basic Chunking Benefits:")
print("✅ Breaks large documents into manageable pieces")
print("✅ Each chunk focuses on specific information")
print("✅ Configurable chunk size and overlap")
print("✅ Handles multiple separators automatically")
print("✅ Simple and reliable")

# 写入完成标记 / Write completion marker
with open("basic_chunking_complete.txt", "w") as f:
    f.write("Basic chunking demo completed successfully")

# 结束提示 / Completion banner
print("\n✅ Basic chunking demo completed!")
