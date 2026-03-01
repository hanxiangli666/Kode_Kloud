#!/usr/bin/env python3
# 1) 该脚本演示基于 TF-IDF 的关键词检索流程; This script demonstrates keyword retrieval using TF-IDF.
# 2) 它实现了向量化、相似度计算与排名输出; It implements vectorization, similarity scoring, and ranking output.
# 3) 使用的 AI 技术是经典的 TF-IDF 统计模型; The AI technique is the classical TF-IDF statistical model.
# 4) 在整体脚本中，它是与 BM25 并列的传统检索基线; In the full set, it is a traditional baseline alongside BM25.
# 5) 它与 keyword_limitation_demo.py 一起说明词项方法的边界; It pairs with keyword_limitation_demo.py to show lexical limits.
"""
Simple TF-IDF Search Demo
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import get_doc_info

# 启动提示 / Startup banner
print("🔍 TF-IDF Search Demo")
print("=" * 50)

# 读取文档 / Load documents from techcorp-docs
docs, doc_paths = get_doc_info()

# 构建 TF-IDF 矩阵 / Create TF-IDF matrix
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(docs)

# 示例查询 / Example searches
queries = ["remote work policy", "health insurance benefits", "pet policy dogs"]

for query in queries:
    print(f"🔎 Searching for: '{query}'")
    
    # 查询向量化 / Transform query to TF-IDF
    query_vector = vectorizer.transform([query])
    
    # 计算相似度 / Calculate similarities
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    
    # 取 Top 结果 / Get top results
    top_indices = similarities.argsort()[-3:][::-1]
    
    print("Results:")
    for i, idx in enumerate(top_indices, 1):
        # 仅显示文件名和分数 / Show only filename and score
        doc_name = doc_paths[idx].split('/')[-1]  # Just the filename
        print(f"  {i}. Score: {similarities[idx]:.4f} - {doc_name}")
    print()

# 完成提示 / Completion banner
print("✅ TF-IDF search completed!")