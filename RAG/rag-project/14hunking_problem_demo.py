#!/usr/bin/env python3
# 1) 该脚本演示不切分导致检索返回整篇文档的问题; This script demonstrates the problem of retrieving whole documents without chunking.
# 2) 它实现了将大文档整体写入向量库并查询的反例; It implements a counterexample by storing a full document and querying it.
# 3) 使用的 AI 技术是向量数据库检索，但刻意缺少切分步骤; The AI technique is vector retrieval, deliberately without chunking.
# 4) 在整个脚本集合中，它是动机与痛点展示的环节; In the full set, it serves as the motivation and pain-point demo.
# 5) 它与后续 chunked_search.py 形成因果关系，推动改进方案; It leads directly to chunked_search.py as the fix.
"""
Chunking Problem Demo
Shows why document chunking is essential for RAG systems
"""

import chromadb

# 启动提示 / Startup banner
print("✂️ Document Chunking Problem Demo")
print("=" * 40)

# 初始化向量库 / Initialize ChromaDB
client = chromadb.Client()
collection = client.create_collection("policies")

# 构造大文档 / Create a large document
large_document = """
TechCorp Employee Handbook - Remote Work Policy

Section 1: Eligibility and Approval Process
Employees may work remotely up to 3 days per week with manager approval. 
Remote work days must be scheduled in advance and approved by your direct supervisor.

Section 2: Equipment and Technology Requirements
Remote employees must have a secure and reliable internet connection with minimum speeds of 25 Mbps download and 5 Mbps upload.
All work must be performed on company-approved devices and software.
Personal devices are not permitted for work purposes.

Section 3: Workspace and Environment Standards
Remote work is not a substitute for childcare or eldercare responsibilities.
Employees must have a dedicated workspace free from distractions.
The workspace must be professional and suitable for video calls.

Section 4: Performance and Evaluation
Performance evaluations will be conducted quarterly.
Remote work performance will be assessed based on deliverables and communication.
"""

# 整文单块存储 / Store the large document as a single chunk
collection.add(
    documents=[large_document],
    ids=["large_document"]
)

# 发起检索 / Run search
print("🔍 Searching for: 'internet speed requirements'")
print()

# 检索指定信息 / Search for specific information
results = collection.query(
    query_texts=["internet speed requirements"],
    n_results=1
)

# 展示问题 / Show problem with result
result_text = results['documents'][0][0]
print("❌ Problem: Returns entire document!")
print(f"Result: {result_text[:200]}...")
print()
print("💡 Solution: Break document into chunks!")
print("✅ Each chunk contains specific information")
print("✅ Better search precision")

# 写入完成标记 / Write completion marker
with open("chunking_problem_complete.txt", "w") as f:
    f.write("Chunking problem demo completed")
