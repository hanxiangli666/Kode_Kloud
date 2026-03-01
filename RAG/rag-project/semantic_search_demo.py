#!/usr/bin/env python3
"""
Semantic Search Demo using Local Embeddings
Uses sentence-transformers for semantic similarity
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from utils import read_techcorp_docs

# 启动提示 / Startup banner
print("🧠 Semantic Search Demo (Local Embeddings)")
print("=" * 50)

# 读取文档（不打印详情）/ Load documents (without verbose output)
docs, doc_paths = read_techcorp_docs()

# 加载本地向量模型 / Load local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 生成文档向量 / Generate embeddings for all documents
doc_embeddings = model.encode(docs)

# 测试查询（关键词失败场景）/ Test query that failed with keyword search
query = "distributed workforce policies"
print(f"🔎 Searching for: '{query}'")

# 生成查询向量 / Generate embedding for query
query_embedding = model.encode([query])

# 计算余弦相似度 / Calculate cosine similarities
similarities = np.dot(query_embedding, doc_embeddings.T).flatten()

# 取 Top 结果 / Get top results
top_indices = similarities.argsort()[-3:][::-1]

print("Results:")
for i, idx in enumerate(top_indices, 1):
    doc_name = doc_paths[idx].split('/')[-1]
    print(f"  {i}. Score: {similarities[idx]:.4f} - {doc_name}")

# 判断是否相关 / Check if we found relevant documents
if similarities[top_indices[0]] > 0.3:
    print("  ✅ Found relevant documents!")
else:
    print("  ❌ No relevant documents found!")

# 结论说明 / Conclusion note
print("\n💡 Semantic search success because:")
print("- Understands 'distributed workforce policies' ≈ 'remote work policy'")
print("- Embeddings capture meaning, not just keywords!")

# 完成提示 / Completion banner
print("\n✅ Semantic search demo completed!")
