#!/usr/bin/env python3
# 1) 该脚本展示关键词检索在语义查询上的失败; This script shows keyword search failing on semantic queries.
# 2) 它实现了 TF-IDF 检索并展示分数不足的案例; It implements TF-IDF retrieval and surfaces weak matches.
# 3) 使用的 AI 技术是基于词项的向量化，局限于字面匹配; The AI technique is term-based vectorization with lexical limits.
# 4) 在整体脚本中，它是引出语义检索需求的关键节点; In the overall set, it triggers the need for semantic search.
# 5) 它与 semantic_search_demo.py 前后衔接，形成问题与解决的关系; It pairs with semantic_search_demo.py as problem and solution.
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
