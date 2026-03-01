#!/usr/bin/env python3
"""
Keyword Search Limitations Demo
Shows why keyword search fails for semantic queries
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import read_techcorp_docs

# 启动提示 / Startup banner
print("🔍 Keyword Search Limitations Demo")
print("=" * 50)

# 读取文档（不打印详情）/ Load documents (without verbose output)
docs, doc_paths = read_techcorp_docs()

# 构建 TF-IDF 矩阵 / Create TF-IDF matrix
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs)

# 测试查询：体现关键词不足 / Test query that shows limitations
query = "distributed workforce policies"
print(f"🔎 Searching for: '{query}'")

# 查询向量化 / Transform query to TF-IDF
query_vector = vectorizer.transform([query])

# 计算相似度 / Calculate similarities
similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

# 取 Top 结果 / Get top results
top_indices = similarities.argsort()[-3:][::-1]

print("Results:")
for i, idx in enumerate(top_indices, 1):
    doc_name = doc_paths[idx].split('/')[-1]
    print(f"  {i}. Score: {similarities[idx]:.4f} - {doc_name}")

# 判断是否找到匹配 / Check for relevant documents
if similarities[top_indices[0]] < 0.05:
    print("  ❌ No relevant documents found!")
else:
    print("  ✅ Found some matches")

# 结论提示 / Conclusion note
print("\n💡 Problem: 'distributed workforce policies' doesn't match 'remote work policy'")
print("We need semantic search that understands meaning!")

# 完成提示 / Completion banner
print("\n✅ Keyword limitation demo completed!")
